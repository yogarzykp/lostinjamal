"""
Adaptive config — 100% dynamics-driven training plan generator.

DESIGN: replaces the bucket lookup + lrs_lookup hash-based LR selection
with metric-driven decisions. NO model_name dependencies (survives
Gradients anonymization roadmap 2026-04-28).

INTEGRATION: produces a `run_config` dict matching legacy
instruct_config.py / dpo_config.py / grpo_config.py format. Legacy
get_run_cmd() templates are reused (no template duplication).

USAGE: text_trainer.py routes to this module when ADAPTIVE_MODE=on.
State machine (initial → continue → finish) for LR refinement still
runs UNCHANGED on top of our initial plan.

Decision sources (per report_format_standard memory):
- arch detection: Gradients Discord 2026-04-28 anonymization roadmap
- VRAM-aware batch: empirical OOM patterns from text-jagger
- adaptive max_length: our experiment 2026-04-26 (max_length=4096 hurt DPO
  3.78 vs 3.06 at 1024)
- adaptive DPO β: tuned to dataset_size, range from DPO paper
  (Rafailov 2023 arxiv 2305.18290 §4 = β ∈ [0.1, 0.5])
- adaptive GRPO num_gen: divisor of batch_size constraint (TRL requirement),
  VRAM-aware cap
"""
import os
import json
from copy import deepcopy
from typing import Dict, Optional

import torch

from dynamics_utils import (
    DatasetMetrics,
    GpuMetrics,
    detect_arch_family,
    arch_supports_fa,
    get_param_count,
    measure_gpu,
    measure_dataset,
    estimate_max_batch_size,
    adaptive_warmup_steps,
    adaptive_epochs_from_init_loss,
    adaptive_dpo_beta,
    adaptive_grpo_num_generations,
    is_slow_reward_function,
)


# ---------------------------------------------------------------------------
# Dataset path resolution (post-tokenize convention from train_*.py)
# ---------------------------------------------------------------------------

def resolve_dataset_path(task_type: str, task_id: str) -> Optional[str]:
    """Map task_type + task_id to post-tokenize dataset path.

    Mirrors patterns from train_*.py:
    - Instruct: datasets/train_<task_id>.json
    - DPO: datasets/dpo_train_<task_id>.json
    - GRPO: datasets/<task_id>_train_data.json (raw, since GRPO does its own tokenize)
    """
    base = "datasets"
    candidates = [
        os.path.join(base, f"train_{task_id}.json"),
        os.path.join(base, f"dpo_train_{task_id}.json"),
        os.path.join(base, f"{task_id}_train_data.json"),
        os.path.join("/cache", "datasets", f"{task_id}_train_data.json"),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


# ---------------------------------------------------------------------------
# Subset rule selectors (decision logic with traceable rules)
# ---------------------------------------------------------------------------

def _select_lora_config(param_count: int, task_type: str) -> Dict:
    """LoRA decision: use for large models, rank scales with param_count.

    Rules (decision-traceable):
    - DPO/GRPO: LoRA if param > 1.5B (memory + reference model overhead)
    - Instruct: LoRA if param > 5B (full FT works for smaller)
    - r ∈ [64, 256] scaling with √(param/2B)
    """
    if param_count is None:
        return {"use_lora": False}

    threshold = 1.5e9 if task_type in ("dpo", "grpo") else 5e9
    if param_count <= threshold:
        return {"use_lora": False}

    r = max(64, min(256, int(64 * (param_count / 2e9) ** 0.5)))
    return {"use_lora": True, "lora_r": r, "lora_alpha": r * 2}


def _select_optimizer(param_count: int) -> str:
    """paged_adamw_8bit across all sizes — empirical win signal.

    Source: HF training_args.bin extraction 2026-05-03..05-08. Three winning
    repos all used paged_adamw_8bit regardless of param_count (135M to 7B+):
    ded7e684 (5C5FBvLa), 03f6b01c (5C7vE26G), 708e03d4 (5G1efLqq).
    Legacy bucket also defaults paged_adamw_8bit. The earlier "torch native
    for small" branch was unfounded — adapter v2 on 708e03d4 lost +0.85% to
    legacy partly because of this divergence.
    """
    return "paged_adamw_8bit"


def _select_max_length(
    seq_len_p95: int,
    validator_max: int = 4096,
    model_max_position: Optional[int] = None,
) -> int:
    """Adaptive max_length from data — VALIDATOR-ALIGNED via halving rule.

    EXP-K 2026-05-15: replicate G.O.D validator's sequence_len rule to avoid
    train/eval distribution mismatch.

    Source verbatim from G.O.D/validator/evaluation/common.py:429-431:
        max_embeddings = getattr(finetuned_model.config, "max_position_embeddings", None)
        if max_embeddings and max_embeddings < 2 * config_dict["sequence_len"]:
            config_dict["sequence_len"] = ceil(max_embeddings / 2)

    Where config_dict["sequence_len"] defaults to 4096 (validator/test_axolotl.yml:5).

    Implication: when model.max_position_embeddings < 8192, validator HALVES
    its eval sequence_len to ceil(max_pos / 2). For OPT-350m (max_pos=2048),
    validator uses seq_len=1024 for eval. If we train at max_len > 1024,
    the model sees longer contexts at train than at eval → distribution mismatch.

    Per hyper-text comment (also references same G.O.D code):
      "Motivating case: opt-125m (max_emb=2050) → validator halves to 1025;
       we were training at 2048 → 2× context mismatch, hurts eval."

    Previous EXP-1B safety (max_pos - 2) was a partial fix — it prevented OPT
    indexSelect crash but didn't align train/eval. Halve rule subsumes both:
    for OPT (max_pos=2048), halve gives 1024, well below the -2 safety threshold.

    Additional layer: data-aware floor max(1024, p95*1.1). Validator's halve
    operates on architecture; data-aware cap operates on dataset signal.
    Final = min(validator_halve, data_p95_floor, validator_max=4096).
    """
    import math
    base = min(validator_max, max(1024, int(seq_len_p95 * 1.1)))
    if model_max_position is not None and model_max_position > 0:
        # Validator halving rule (G.O.D common.py:429-431) — match it for
        # train/eval alignment.
        if model_max_position < 2 * validator_max:
            validator_halve = math.ceil(model_max_position / 2)
            base = min(base, validator_halve)
    return max(64, base)  # absolute floor — pathological short seqs still need 64


def _select_grpo_max_completion(seq_len_p95: int) -> int:
    """For GRPO: max_completion_length = task-aware.

    Source: Dr.GRPO (Liu 2025 arxiv 2510.06870) + REFA (arxiv 2412.16378)
    + lotob v1/v3/v4 wandb 2026-04-28/29 — max_completion=256 caused
    clipped_ratio=1.0 forever. Bump floor to 512 (paper recommends
    breathing room for EOS learning), ceiling 1024 (validator-aligned).
    """
    return min(1024, max(512, int(seq_len_p95 * 1.2)))


def _grpo_vanilla_batch_cap(param_count: int) -> int:
    """Vanilla bucket batch ceilings from scripts/grpo_config.py:GRPO_CONFIG.

    Lotob v1 2026-04-28: adaptive picked batch=64 vs vanilla batch=10
    (slow reward detected) → effective gen batch 50× vanilla → crash.
    Cap adaptive batch at vanilla bucket value to stay within known-safe.

    EXP-FF 2026-05-19: align boundaries with GRPO_CONFIG buckets.
    Empirical: 5df20458 winner (Qwen3-4B, 4.02B params) used GRPO_CONFIG[4_5_b]
    batch=42, but our old code returned 32 for 4.02B (because not <4e9).
    Updated boundaries match GRPO_CONFIG buckets exactly:
      0_1_b/1_2_b: batch=40 (<2B)
      2_4_b: batch=42 (2-4B)
      4_5_b/5_6_b: batch=42 (4-6B) — was 32
      6_9_b: batch=24 LoRA (6-9B) — was 32
      9_12_b: batch=16 LoRA (9-12B)
      12_15_b+: batch=8-16 LoRA (was 16 catch-all)
    """
    if param_count < 2e9:
        return 40
    if param_count < 4e9:
        return 42
    if param_count < 6e9:
        return 42   # was 32 — match GRPO_CONFIG[4_5_b] + [5_6_b] empirical
    if param_count < 9e9:
        return 24   # was 32 — match GRPO_CONFIG[6_9_b] LoRA bucket
    if param_count < 12e9:
        return 16   # match GRPO_CONFIG[9_12_b]
    return 16       # 12B+ scales smaller anyway


# ---------------------------------------------------------------------------
# EXP-HYPER-PORT 2026-05-20: Three hyper-text adaptive features ported.
#   A. adaptive-seq-len: halve max_length when token p99 << current cap
#   B. depth-warmup: √depth scaling of warmup_steps for deeper models
#   C. gqa-batch-boost: GQA-aware batch boost (×1.20 when gqa_ratio >= 4)
#
# Source: /Users/zulist/Documents/text/hyper-text/scripts/hp_override.py
#   A: _maybe_adaptive_sequence_len (lines 960-1088, Sprint C7)
#   B: _maybe_depth_scaled_warmup (lines 702-742, Sprint A3)
#   C: _maybe_gqa_batch_boost (lines 845-886, Sprint A1)
#
# Tournament audit 2026-05-20: winner 5C7vE26G77n7 uses all three.
# Fingerprint tags preserved verbatim for grep compatibility with winner logs.
# ---------------------------------------------------------------------------

def _maybe_halve_max_length_from_p99(current_max: int, token_p99: int) -> int:
    """Feature A: adaptive-seq-len — halve max_length when token p99 << current cap.

    Theory (hyper-text Sprint C7): padding compute ∝ batch × max_length.
    When data p99 tokens << max_length, kernel cycles wasted on masked-out
    positions. Halving reduces wasted compute by 2× without affecting eval
    (validator's eval data has same distribution; truncation_rate ≈ 0%).

    Trigger: token_p99 < current_max / 2 → halve current_max (floor 512).
    Disable: ADAPTIVE_SEQ_LEN_ENABLED=0.
    """
    if os.getenv("ADAPTIVE_SEQ_LEN_ENABLED", "1") != "1":
        return current_max
    if token_p99 <= 0 or current_max <= 512:
        return current_max
    if token_p99 < current_max / 2:
        new_max = max(512, current_max // 2)
        if new_max < current_max:
            print(
                f"[hp-override:adaptive-seq-len] → max_length {current_max}→{new_max} "
                f"(p99={token_p99}, threshold={current_max // 2}; 2× reduction threshold met)",
                flush=True,
            )
            return new_max
    return current_max


def _compute_depth_warmup(base_warmup: int, num_layers: int) -> int:
    """Feature B: depth-warmup — √depth scaling of warmup_steps for deeper models.

    Theory (Goyal+2017 ImageNet): warmup ∝ √depth. Deeper models need longer
    warmup for gradient stability through layers.

    Formula: int(base_warmup × √(num_layers / 16)), clamped to [base/2, base*3].
    Divisor 16 chosen to match hyper-text Sprint A3 (hp_override.py:729) AND
    the empirical winner fingerprint observed in 5C7vE26G77n7 Grafana logs:
      [hp-override:depth-warmup] depth=28 → warmup_steps 35→46 (√depth scaling)
      → 35 × √(28/16) = 35 × 1.323 = 46.30 → int(46) ✓

    Examples (base=35):
      16 layers → 35 (no change — reference depth)
      24 layers → 42 (Sheared-LLaMA bumped slightly)
      28 layers → 46 (Qwen2.5-7B, matches winner fingerprint)
      32 layers → 49 (Llama-7B/8B)
      40 layers → 55 (Phi-3-medium)
      80 layers → 78 (Llama-70B, clamped to base*3=105 ceiling)

    Tiny models (<=16 layers) get clamped DOWN by the lo bound to base/2.
    Spec said √(num_layers/30) but winner fingerprint clearly uses /16.
    Disable: DEPTH_WARMUP_ENABLED=0.
    """
    if os.getenv("DEPTH_WARMUP_ENABLED", "1") != "1":
        return base_warmup
    if not num_layers or num_layers <= 0 or base_warmup <= 0:
        return base_warmup
    import math
    scaled = int(base_warmup * math.sqrt(num_layers / 16.0))
    lo = max(1, base_warmup // 2)
    hi = base_warmup * 3
    new_warmup = max(lo, min(hi, scaled))
    return new_warmup


def _maybe_gqa_batch_boost(current_batch: int, num_q_heads: Optional[int],
                            num_kv_heads: Optional[int]) -> tuple[int, float]:
    """Feature C: gqa-batch-boost — GQA-aware batch boost when ratio >= 4.

    Theory (hyper-text Sprint A1): GQA models have num_kv_heads << num_q_heads
    → KV cache proportionally smaller (KV mem ∝ kv_heads). Frees memory for
    larger batches.

    Boost factor (conservative — only KV scales, other memory doesn't):
      gqa_ratio >= 4 → batch ×1.20 (Qwen2.5-7B at 7×, Mistral 4×)
      gqa_ratio >= 2 → batch ×1.10
      gqa_ratio < 2  → no change

    Returns (new_batch, gqa_ratio). new_batch == current_batch when no boost.
    Disable: GQA_BATCH_BOOST_ENABLED=0.
    """
    if os.getenv("GQA_BATCH_BOOST_ENABLED", "1") != "1":
        return current_batch, 1.0
    if not num_q_heads or not num_kv_heads or num_kv_heads <= 0:
        return current_batch, 1.0
    gqa_ratio = float(num_q_heads) / float(num_kv_heads)
    if gqa_ratio < 2:
        return current_batch, gqa_ratio
    boost = 1.20 if gqa_ratio >= 4 else 1.10
    new_batch = max(1, int(current_batch * boost))
    if new_batch <= current_batch:
        return current_batch, gqa_ratio
    return new_batch, gqa_ratio


# ---------------------------------------------------------------------------
# EXP-HYPER-PORT-E 2026-05-20: Per-layer LR multipliers (LARS-style).
# Source: hyper-text/scripts/hp_override.py:_compute_per_layer_lr_multipliers.
#
# Tournament audit 2026-05-20: winner 5C7vE26G77n7 ships 12 param-group
# optimizer fingerprint:
#   [per-layer-lr] custom optimizer built: 12 groups,
#   lr range [1.5000e-04, 5.0706e-04], base=3.0000e-04
#
# Theory (LARS, Goyal+2017): optimal layer LR ∝ ||W||_F. Layers with
# larger weight norms can absorb proportionally more LR without instability.
# Inverse of LAMB ratio. Formula:
#   multiplier_g = clamp(weight_norm_g / mean_norm, [0.5, 2.0])
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# EXP-TINKER 2026-05-20: Tinker Cookbook LR formula for Instruct LoRA SFT
# ---------------------------------------------------------------------------
# Source: Thinking Machines / John Schulman lab — tinker_cookbook/hyperparam_utils.py
#   get_lr(model_name, lora=False) = 5e-5 * (10 if lora else 1)
#                                  * (2000 / hidden_size) ** family_exponent
#   family exponents: qwen=0.0775, llama=0.781
#
# IMPORTANT: formula is SFT-only (lora=True path). GRPO/RL training uses
# 5-paper consensus 1e-6 instead — NOT this formula.
#
# Computed reference values (LoRA SFT):
#   Qwen3-4B   (hidden=2560) → 4.91e-4
#   Qwen2.5-7B (hidden=3584) → 4.77e-4
#   Llama-3.1-8B (hidden=4096) → 2.79e-4
# ---------------------------------------------------------------------------

# Family → Tinker exponent. Llama exponent reused for llama-derived families
# (tinyllama, smollm, shear) since they share llama-style scaling dynamics.
# Unknown families return None (caller must fall back).
_TINKER_FAMILY_EXPONENTS = {
    "qwen": 0.0775,
    "llama": 0.781,
    "tinyllama": 0.781,
    "smollm": 0.781,
    "shear": 0.781,
}


def _tinker_instruct_lora_lr(
    model_family: str,
    hidden_size: Optional[int],
    current_default_lr: float,
) -> Optional[float]:
    """Tinker Cookbook LR formula for Instruct LoRA SFT.

    Formula: 5e-5 * 10 * (2000 / hidden_size) ** family_exponent

    Args:
      model_family: resolved family string (qwen, llama, tinyllama, smollm, shear, ...).
      hidden_size: hidden dim from AutoConfig (required — formula uses it).
      current_default_lr: current default LR (for log comparison only; not used
        in computation). Caller decides whether to actually swap to the formula.

    Returns:
      Computed formula LR, or None when family unsupported / hidden_size missing.
      Caller decides whether to override (e.g. skip if family_lr_table HIGH conf).
    """
    if hidden_size is None or hidden_size <= 0:
        return None
    exponent = _TINKER_FAMILY_EXPONENTS.get(model_family)
    if exponent is None:
        return None
    try:
        lr = 5e-5 * 10.0 * (2000.0 / float(hidden_size)) ** exponent
    except Exception:
        return None
    # Sanity clamp (formula should produce ~2e-4..6e-4 for normal hidden sizes;
    # extreme inputs guarded just in case).
    if lr <= 0 or lr > 1e-2:
        return None
    return float(lr)


def _compute_per_layer_lr_multipliers(model_path: str) -> Optional[Dict[str, float]]:
    """LARS-style per-layer LR multipliers from model weight norms.

    Args:
      model_path: directory with safetensors / .bin weight files.

    Returns:
      Dict {layer_group: multiplier_float} or None on any failure/skip.
      Keys match per_layer_optimizer._LAYER_PATTERNS labels:
        attn.q_proj, attn.k_proj, attn.v_proj, attn.o_proj,
        mlp.gate_proj, mlp.up_proj, mlp.down_proj.

    Env gates:
      PER_LAYER_LR_ENABLED=0 → returns None (skip)
    """
    if os.getenv("PER_LAYER_LR_ENABLED", "1") != "1":
        return None
    try:
        from model_features import extract_weight_stats
    except Exception as exc:
        print(f"[hp-override:per-layer-lr] model_features import failed: {exc}", flush=True)
        return None

    weights = extract_weight_stats(model_path)
    by_group = (weights or {}).get("by_group") or {}
    if not by_group:
        if weights and weights.get("iter_error"):
            print(f"[hp-override:per-layer-lr] weight extraction skipped: "
                  f"{weights['iter_error']}", flush=True)
        return None

    # Only consider attn + mlp groups (norms have weight_norm ≈ √n_elem,
    # not informative for LR scaling).
    relevant = {
        g: float(w.get("weight_norm") or 0.0)
        for g, w in by_group.items()
        if (g.startswith("attn.") or g.startswith("mlp."))
        and float(w.get("weight_norm") or 0.0) > 0
    }
    if not relevant:
        return None

    norms = list(relevant.values())
    mean_norm = sum(norms) / len(norms)
    if mean_norm <= 0:
        return None

    multipliers = {}
    for group, norm in relevant.items():
        mult = norm / mean_norm
        # Clamp to safe range (avoid runaway LR on outlier layers)
        mult = max(0.5, min(2.0, mult))
        multipliers[group] = round(mult, 4)

    # Log compact summary (matches hyper-text format)
    sorted_mults = sorted(multipliers.items(), key=lambda kv: kv[1])
    lo = sorted_mults[0]
    hi = sorted_mults[-1]
    print(
        f"[hp-override:per-layer-lr] computed {len(multipliers)} multipliers "
        f"min={lo[0]}={lo[1]:.2f} max={hi[0]}={hi[1]:.2f} "
        f"mean_norm={mean_norm:.2f}",
        flush=True,
    )
    return multipliers


# ---------------------------------------------------------------------------
# Family-aware adaptive HP profiles (Phase 1: Instruct, focus SmolLM2-1.7B)
# ---------------------------------------------------------------------------
# Design philosophy:
# - PRIMARY: arch_family from config (anonymization-safe, survives Gradients roadmap)
# - ENHANCEMENT: model_name family signal (current tournaments still expose name)
# - GOES BEYOND master-text: multi-signal resolver (arch+name), seq_p95-aware
#   max_length bucketing, continuous data-size interpolation for warmup, family-
#   specific NEFTune scaling.
# Reference (NOT direct copy): master-text instruct_advisor.py
#   FAMILY_LR_PRIORS + _family_min_lr_rate + _apply_family_profile_overrides.
# Cross-validated against 5C5FB (PENCURI deploying master-text-style code) winning
# runs on tasks ded7e684 (test_loss 0.0502) + 05933c53 (0.0143).

LENGTH_BUCKETS = [512, 768, 1024, 1536, 2048, 3072, 4096]


_FAMILY_PROFILES = {
    # SmolLM family — updated 2026-05-11 per Wave 1+2 eval finding:
    # task 0c5c7124 SmolLM2-360M lost 9.10% gap (1.6494 vs winner 1.5118).
    # Root cause: min_lr_rate 0.075 (3.3× lower than 360M empirical winner cell 0.25),
    # lr_default skewed by 1.7B runs (6.2e-4 vs 360M cell median 4.28e-4).
    # qwen got min_lr_rate 0.25 fix in 97e6ba3 — smollm tertinggal, fixed here.
    # Empirical source: empirical_hp_rules.json cell smollm|0_06b|instruct (n=4)
    # median lr=4.28e-4, min_lr=0.25, wd=0.0, epochs=3, batch=140.
    # Original 5C5FB validation (ded7e684 test_loss 0.0502) was at 1.7B, doesn't
    # generalize down to 360M class.
    "smollm": {
        "min_lr_rate": 0.25,          # was 0.075 — match qwen + 360M empirical
        "weight_decay_small_data": 0.0,
        "weight_decay_default": 0.0,  # was 0.005 — empirical 360M winners used 0.0
        "packing": False,
        "max_packed_size": 1,
        "max_length_cap": 2048,
        "neftune_alpha_small_data": 5,
        "neftune_alpha_default": 3,
        "warmup_steps_small_data": 15,
        "warmup_steps_default": 35,
        "lr_default": 4.3e-4,        # was 6.2e-4 — empirical 360M cell median
        "lr_floor": 2.0e-4,           # was 2.4e-4 — slightly more headroom
        "reg_ratio_small_data": 0.60,
        "reg_ratio_default": 0.70,
    },
    "qwen": {
        # min_lr_rate 0.25 (was 0.18) — matches all observed winning training_args
        # across tasks (708e03d4 5G1efLqq, ded7e684 5C5FBvLa, 03f6b01c 5C7vE26G).
        # Higher floor reduces over-cooldown effect at end of training.
        #
        # UPDATE 2026-05-13 — size-bucketed LR:
        # Empirical winner LRs per param size:
        #   0.5B class (0bda471b 5DLkfAsZ unsloth-Qwen): 2.51e-4
        #   1.5B-3B class (708e03d4 5G1efLqq): 8.6e-5 (current default)
        # 0.5B winners use ~2.9× higher LR than 1.5B+ baseline. Apply via
        # lr_size_buckets dict consumed by adaptive_config logic post-resolve.
        "min_lr_rate": 0.25,
        "weight_decay_small_data": 0.0,
        "weight_decay_default": 0.0,
        "packing": True,
        "max_packed_size": 4,
        "max_length_cap": 4096,
        "neftune_alpha_small_data": 0,
        "neftune_alpha_default": 0,
        "warmup_steps_small_data": 35,
        "warmup_steps_default": 35,
        "lr_default": 8.6e-5,
        "lr_floor": 5.7e-5,
        # NEW 2026-05-13: size-bucketed LR override (overrides lr_default if size matches)
        # Keys: max_param_bound; value: lr for models below that bound
        "lr_size_buckets": {
            "0_7b": 2.5e-4,   # <0.7B (Qwen 0.5B class): 2.51e-4 empirical from 5DLkfAsZ
            "2_0b": 1.4e-4,   # 0.7B-2B (Qwen 1.5B class): interpolated
            # >=2B: falls through to lr_default (8.6e-5)
        },
        "reg_ratio_small_data": 1.08,
        "reg_ratio_default": 1.00,
    },
    "tinyllama": {
        "min_lr_rate": 0.20,
        "weight_decay_small_data": 0.0,
        "weight_decay_default": 0.0,
        "packing": True,
        "max_packed_size": 4,
        "max_length_cap": 4096,
        "neftune_alpha_small_data": 0,
        "neftune_alpha_default": 0,
        "warmup_steps_small_data": 35,
        "warmup_steps_default": 35,
        "lr_default": 7.2e-5,
        "lr_floor": 3.9e-5,
        "reg_ratio_small_data": 1.03,
        "reg_ratio_default": 1.00,
    },
    # Sheared-LLaMA family — NEW 2026-05-13.
    # Empirical from winner 5Ek3D5Jp on acd597ef (Sheared-LLaMA-1.3B):
    # lr=9.15e-5, min_lr_rate=0.25, wd=0.0, epochs=3 (stopped at 2),
    # full FT (no LoRA), batch=100 on validator.
    # Reason for dedicated profile: previously aliased to tinyllama
    # (lr=7.2e-5) which was 27% too low. Wave 1+2 acd597ef v1/v5
    # both LOSE +0.10% — patches didn't help because alias mismatch.
    "shear": {
        "min_lr_rate": 0.25,
        "weight_decay_small_data": 0.0,
        "weight_decay_default": 0.0,
        "packing": True,
        "max_packed_size": 4,
        "max_length_cap": 4096,
        "neftune_alpha_small_data": 0,
        "neftune_alpha_default": 0,
        "warmup_steps_small_data": 35,
        "warmup_steps_default": 35,
        "lr_default": 9.15e-5,   # empirical winner (was tinyllama 7.2e-5)
        "lr_floor": 7.5e-5,
        "reg_ratio_small_data": 1.03,
        "reg_ratio_default": 1.00,
    },
    "phi": {
        "min_lr_rate": 0.15,
        "weight_decay_small_data": 0.0,
        "weight_decay_default": 0.0,
        "packing": True,
        "max_packed_size": 4,
        "max_length_cap": 4096,
        "neftune_alpha_small_data": 0,
        "neftune_alpha_default": 0,
        "warmup_steps_small_data": 35,
        "warmup_steps_default": 35,
        "lr_default": 9.6e-5,
        "lr_floor": 7.5e-5,
        "reg_ratio_small_data": 1.06,
        "reg_ratio_default": 1.00,
    },
    "gemma": {
        "min_lr_rate": 0.15,
        "weight_decay_small_data": 0.0,
        "weight_decay_default": 0.0,
        "packing": True,
        "max_packed_size": 4,
        "max_length_cap": 4096,
        "neftune_alpha_small_data": 0,
        "neftune_alpha_default": 0,
        "warmup_steps_small_data": 35,
        "warmup_steps_default": 35,
        "lr_default": 8.5e-5,
        "lr_floor": 6.5e-5,
        "reg_ratio_small_data": 1.03,
        "reg_ratio_default": 1.00,
    },
    # OPT family — NEW 2026-05-15.
    # Critical: max_length_cap MUST account for OPTLearnedPositionalEmbedding's
    # internal +2 offset (positions stored at [2, max_pos+1] not [0, max_pos-1]).
    # opt-350m has max_position_embeddings=2048 → safe max_len ≤ 2046.
    # Round 1 task 3c42f: 5CcPT + 5GUHS crashed with PyTorch indexSelect assertion
    # at embedding lookup when packed sequences hit position_ids = 2048 (out of bounds).
    # Empirical from 3c42f winners (17 BOSS/PENCURI hotkeys succeeded): batch=48 lr~1e-4.
    # Different from smaller-context models — OPT is "small but constrained".
    "opt": {
        # EXP-X 2026-05-17: min_lr_rate 0.20 → 0.75 to mimic winner near-constant LR.
        # Grafana log 3c42f7f4 winner 5FW2Eaa: peak 5.96e-5, min 5.07e-5, min/peak ratio 0.85.
        # OPT family appears to benefit from constant LR throughout (no cosine decay).
        # Conservative move to 0.75 (not 0.85) to leave some decay headroom.
        "min_lr_rate": 0.75,
        "weight_decay_small_data": 0.0,
        "weight_decay_default": 0.0,
        "packing": False,             # disable packing for OPT (position overflow risk)
        "max_packed_size": 1,
        "max_length_cap": 2046,       # OPT internal +2 offset; max_pos=2048 → safe=2046
        "neftune_alpha_small_data": 0,
        "neftune_alpha_default": 0,
        "warmup_steps_small_data": 35,
        "warmup_steps_default": 35,
        # EXP-Y 2026-05-17: lr_default 1.0e-4 → 6.0e-5 winner-matched.
        # Grafana shows 3c42f winner peak 5.96e-5 (we were at 9.1e-5 from Tier 1 = +53% over).
        # New default 6e-5 matches winner peak. Floor 4e-5 (2/3 of default) keeps some range.
        "lr_default": 6.0e-5,         # was 1.0e-4 — winner empirical 3c42f 5FW2Eaa
        "lr_floor": 4.0e-5,           # was 5.0e-5 — adjusted proportionally
        "reg_ratio_small_data": 1.00,
        "reg_ratio_default": 1.00,
    },
    # Fallback when family unknown/unmappable (anonymization scenario or unseen arch)
    "unknown": {
        "min_lr_rate": 0.20,
        "weight_decay_small_data": 0.0,
        "weight_decay_default": 0.01,
        "packing": True,
        "max_packed_size": 2,
        "max_length_cap": 4096,
        "neftune_alpha_small_data": 5,
        "neftune_alpha_default": 0,
        "warmup_steps_small_data": 35,
        "warmup_steps_default": 35,
        "lr_default": None,   # fall back to param-based heuristic
        "lr_floor": None,
        "reg_ratio_small_data": 1.00,
        "reg_ratio_default": 1.00,
    },
}


def _classify_model_family_safe(model_name: Optional[str]) -> str:
    """Family from model_name string. Returns 'unknown' when name unavailable.

    Used as ENHANCEMENT layer on top of arch detection (anonymization-safe primary).
    Order matters — check most specific first (tinyllama before llama, etc).
    """
    if not model_name:
        return "unknown"
    name = model_name.lower()
    if "tinyllama" in name:
        return "tinyllama"
    # NEW 2026-05-13: Sheared-LLaMA family (was aliased to tinyllama, lr 27% too low)
    if "shear" in name:  # matches "Sheared-LLaMA" / "sheared-llama"
        return "shear"
    # NEW 2026-05-15: OPT family (was aliased to "unknown", caused PyTorch indexSelect
    # assertion fail at validator-side for opt-350m via max_len overflow with packing.
    # Round 1 task 3c42f opt-350m: 5CcPT + 5GUHS both crashed (KITA only). 17/22 other
    # miners succeeded → bug specific to our code path. Fix routes OPT family →
    # max_len-safe profile (cap at max_position_embeddings - 2 for OPT's internal offset).
    if "opt-" in name or "/opt" in name or name.startswith("opt"):
        if "gpt" not in name:  # exclude gpt-* names that happen to contain "opt"
            return "opt"
    if "smollm" in name:
        return "smollm"
    if "qwen" in name:
        return "qwen"
    if "phi" in name and "gpt" not in name:
        return "phi"
    if "gemma" in name:
        return "gemma"
    if "llama" in name:
        # Generic llama (non-tiny) → use tinyllama HP profile (similar dynamics)
        return "tinyllama"
    return "unknown"


def _resolve_family(
    arch_family: str,
    model_name: Optional[str],
    detected_base_model: Optional[str] = None,
) -> str:
    """Resolve effective family from BOTH structural arch + name signals.

    Priority order (UPDATED 2026-05-12 — critical bug fix):
    1. detected_base_model (from fingerprint, anon-resilient) → classify it
    2. model_name maps to specific profile family → use it
    3. Arch maps to known profile → use it
    4. Arch maps via aliasing (llama→tinyllama, mistral→tinyllama, deepseek→qwen)
    5. Fall back to "unknown" profile

    BUG FIX 2026-05-12: anonymized SmolLM2-360M reports arch=llama,
    name=firzahdzm/augmented-XXX (no "smollm" substring). Previously fell
    through to arch_aliases["llama"]→"tinyllama" — SmolLM profile patches
    were dead code. Now consults detected_base_model (e.g.
    "HuggingFaceTB/SmolLM2-360M" recovered via fingerprint) FIRST so
    family resolution works on anonymized models.
    """
    # Tier 1: fingerprint-recovered base_model (anon-resilient PRIMARY signal)
    if detected_base_model:
        det_family = _classify_model_family_safe(detected_base_model)
        if det_family in _FAMILY_PROFILES and det_family != "unknown":
            return det_family

    # Tier 2: raw model_name (pre-anonymization fallback)
    name_family = _classify_model_family_safe(model_name)
    if name_family in _FAMILY_PROFILES and name_family != "unknown":
        return name_family

    # Tier 3: arch family direct
    if arch_family in _FAMILY_PROFILES:
        return arch_family

    # Tier 4: arch aliases (conservative — only when no better signal)
    arch_aliases = {
        "llama": "tinyllama",
        "mistral": "tinyllama",
        "deepseek": "qwen",
    }
    if arch_family in arch_aliases:
        return arch_aliases[arch_family]

    return "unknown"


# ---------------------------------------------------------------------------
# Plan D (2026-05-03): Task character router — winner-log inspired.
# ---------------------------------------------------------------------------
# Reverse-engineered from a winning run on task 03f6b01c. The winner routed
# HP based on dataset signals (io_jaccard, heuristic flags, script) — NOT
# just (param, data_size, family). RICHER than master-text's static lookup.
#
# Categories:
# - "memorization": low io_jaccard + no cot/math/code → factual QA (TOFU-like)
#   Memorization tasks need LOWER LR + LESS regularization (NEFTune kills memorization)
# - "translation": high lang_ratio < 0.6 (multilingual) OR translation pairs
#   Translation benefits from family default (NEFTune helps generalization)
# - "code": code heuristic flag > 0.3
# - "reasoning": cot or math flag > 0.2
# - "skill" (default): use family HP as-is

def classify_task_character(profile: Dict, model_name: Optional[str] = None) -> str:
    """Route task to character class based on dataset profile + model name.

    Returns: "memorization" | "translation" | "code" | "reasoning" | "skill"

    Detection priority (refined 2026-05-03 after FairTranslate misclassification):
    1. code: explicit code patterns
    2. reasoning: cot/math density
    3. translation_multilingual: non-Latin script or mixed
    4. translation_pair: VERY low io_jaccard (<0.05) + similar input/output
       lengths — covers EN↔FR/DE/ES translation pairs that share Latin script
    5. memorization: low io_jaccard (0.05-0.3) + no cot/math/code → factual QA
    6. skill: default
    """
    flags = profile.get("heuristic_flags", {})
    cot = flags.get("cot", 0.0)
    math = flags.get("math", 0.0)
    code = flags.get("code", 0.0)
    io_j = profile.get("io_jaccard_p50", 0.0)
    io_j_mean = profile.get("io_jaccard_mean", 0.0)
    lang_ratio = profile.get("lang_ratio", 1.0)
    script = profile.get("script_overall", "unknown")
    in_p50 = max(1, profile.get("char_len_instruct_p50", 0))
    out_p50 = max(1, profile.get("char_len_output_p50", 0))
    length_ratio = out_p50 / in_p50

    # 1. Code (highest priority — code patterns very distinctive)
    if code > 0.3:
        return "code"
    # 2. Reasoning (CoT/math density)
    if cot > 0.3 or math > 0.2:
        return "reasoning"
    # 3. Translation MULTILINGUAL: non-Latin script OR CJK/mixed
    if lang_ratio < 0.6 or script in ("cjk", "arabic", "cyrillic", "mixed"):
        return "translation"
    # 4. Translation PAIR (Latin-Latin, e.g. EN→FR, EN→DE):
    #    VERY low io_jaccard signals different vocabularies between input/output.
    #    Length ratio near 1 = parallel translation pairs.
    if io_j_mean < 0.05 and 0.5 < length_ratio < 2.0:
        return "translation"
    # 5. Memorization: moderate-low io_jaccard + no other signals → factual QA
    if io_j < 0.3 and cot < 0.1 and code < 0.1 and math < 0.1:
        return "memorization"
    # 6. Default
    return "skill"


def _apply_task_character_overrides(
    hp: Dict,
    task_class: str,
    profile: Dict,
    param_count: int,
) -> Dict:
    """Adjust family-aware HP based on detected task character.

    Memorization tasks: LR 3× lower, NEFTune off, fewer epochs, looser plateau.
    Reasoning/code: medium-low LR, more epochs.
    Translation: keep family HP (already tuned for it).
    Skill: keep family HP.
    """
    hp = dict(hp)
    hp["_meta"] = dict(hp.get("_meta", {}))
    hp["_meta"]["task_class"] = task_class

    if task_class == "memorization":
        # Big-data memorization (fix 2026-05-04 from 05933c53 gpt-neo +12889% LOSE):
        # Set LR=3e-4 (winner empirical) AND DISABLE PACKING for short-sequence
        # tasks (p95<128). Packing aggregates many short samples per fwd-pass →
        # 14× fewer gradient updates than non-packed. Winner did 10,686 steps,
        # we did 740 with packing — same data exposure but far less SGD events.
        # Memorization task benefits from many small gradient updates not few large ones.
        data_size = profile.get("actual_total", 10000)
        # Use char-len p95 from profile as proxy for sequence length (~3-4 chars/token).
        out_p95_chars = profile.get("char_len_output_p95", 0) or 0
        if data_size > 100_000:
            hp["learning_rate"] = 3e-4
        else:
            hp["learning_rate"] = min(hp["learning_rate"], 1.5e-4)
        # Force disable packing for short-output memorization (output_p95 < 200 chars
        # ≈ 50 tokens) → maximize gradient update count. Without packing 25 short
        # samples per pack become 25 separate fwd passes = 25× more SGD updates.
        if out_p95_chars > 0 and out_p95_chars < 200:
            hp["packing"] = False
        # NEFTune hurts memorization (noise prevents fact retention)
        hp["neftune_noise_alpha"] = 0
        # Shorter epochs (memorization plateaus fast)
        hp["epoch_num"] = min(hp.get("epoch_num", 4), 2)
        # Looser plateau tolerance — memorization eval may bounce
        train_dev_j = profile.get("train_dev_jaccard", 0.0)
        hp["plateau_tolerance"] = round(0.02 + 0.06 * train_dev_j, 4)

    elif task_class == "code":
        # Code: lower LR, NEFTune off. Epochs DATA-SIZE-AWARE (fix 2026-05-03):
        # - small data <10K: 3 epochs (need passes)
        # - medium 10K-50K: 2 epochs (enough)
        # - large >50K: 1 epoch (one pass through 50K+ samples already plenty)
        # Previously hardcoded epoch>=3 which meant 100K Magicoder = 5.5hr training,
        # blowing past 2hr task budget.
        data_size = profile.get("actual_total", 10000)
        hp["learning_rate"] = min(hp["learning_rate"], 8e-5)
        # PARAM-SIZE-AWARE LR scale (fix 2026-05-03 from 0304997e Qwen 7B LOSE):
        # Big-model code task overfits/diverges with high LR. Winner used 2.9e-5
        # for 7B (3× lower than our 8e-5). Scale down for big models.
        if param_count and param_count >= 4e9:
            hp["learning_rate"] = min(hp["learning_rate"], 3e-5)
            # Big-model code also wants gentler cooldown
            hp["min_lr_rate"] = max(hp.get("min_lr_rate", 0.18), 0.25)
        hp["neftune_noise_alpha"] = 0
        if data_size < 10_000:
            hp["epoch_num"] = max(hp.get("epoch_num", 3), 3)
        elif data_size < 50_000:
            hp["epoch_num"] = min(hp.get("epoch_num", 2), 2)
        else:
            hp["epoch_num"] = 1  # huge code dataset, single epoch sufficient

    elif task_class == "reasoning":
        # Reasoning: keep moderate LR, NEFTune helps generalize, more epochs
        # Same data-size-aware adjustment for budget safety
        hp["learning_rate"] = min(hp["learning_rate"], 3e-4)
        hp["neftune_noise_alpha"] = max(hp.get("neftune_noise_alpha", 0), 3)
        data_size = profile.get("actual_total", 10000)
        if data_size < 10_000:
            hp["epoch_num"] = max(hp.get("epoch_num", 3), 4)
        elif data_size < 50_000:
            hp["epoch_num"] = min(hp.get("epoch_num", 3), 3)
        else:
            hp["epoch_num"] = 2

    elif task_class == "translation":
        # EXP-W 2026-05-17: REVISE EXP-P translation mult 0.4 → 0.85.
        # Original EXP-P (commit 5d0a458) misread winner's LATE-EPOCH LR (2.94e-5)
        # as peak. Full Grafana LR curve analysis (2026-05-17) shows actual winner
        # 5C7vE26G PEAK LR is 6.76e-5 (median 4.13e-5, min 1.36e-5, min_lr_rate 0.20).
        # — KITA v2 (no EXP-P): 8.07e-5 = winner+19% over → LOSE +2.13%
        # — KITA v3 (EXP-P × 0.4): 3.23e-5 = winner-52% under → LOSE +1.61% (over-corrected)
        # — Sweet spot: × 0.85 → 6.86e-5 (within 1% of winner 6.76e-5 peak)
        # Keep epoch cap 3 (winner empirically stopped at ep 2-3).
        hp["learning_rate"] = max(2.5e-5, hp["learning_rate"] * 0.85)
        hp["epoch_num"] = min(hp.get("epoch_num", 4), 3)

    # skill: keep family HP (NEFTune + family default LR)
    return hp


def _compute_instruct_adaptive_hp(
    arch_family: str,
    param_count: int,
    data_size: int,
    seq_p95: int,
    model_name: Optional[str] = None,
    detected_base_model: Optional[str] = None,
) -> Dict:
    """Build family-aware adaptive HP for Instruct task.

    RICHER than master-text:
    - master-text: (param_count, data_size, family_name)
    - ours: (arch_family, family_name, detected_base_model, param_count, data_size, seq_p95)

    Multi-signal priority (UPDATED 2026-05-12 — anon bug fix):
    1. detected_base_model (fingerprint-recovered, anon-resilient) — PRIMARY
    2. model_name string-match — fallback when fingerprint missed
    3. arch_family from config (last resort)

    Returns dict mergable into run_config.
    """
    family = _resolve_family(arch_family, model_name, detected_base_model)
    profile = _FAMILY_PROFILES[family]

    is_small_data = data_size < 3_000
    is_medium_data = 3_000 <= data_size < 20_000

    # Epoch by data_size — smoother bucketing than master-text
    # Sources: master-text empirical (data<3K → 4 epoch); our 2026-04-22 exp
    # showed best ckpt ≤ epoch 2 for medium-large (overfit at epoch 3).
    if is_small_data:
        epoch = 4
    elif is_medium_data:
        epoch = 4 if param_count < 4e9 else 3
    elif data_size < 50_000:
        epoch = 3
    else:
        epoch = 2

    wd = profile["weight_decay_small_data"] if is_small_data else profile["weight_decay_default"]
    min_lr_rate = profile["min_lr_rate"]

    # NEFTune: family-aware + small-data scaling
    neftune = (
        profile["neftune_alpha_small_data"] if is_small_data
        else profile["neftune_alpha_default"]
    )
    if data_size > 50_000:
        neftune = 0  # large data doesn't benefit from regularization noise

    warmup = profile["warmup_steps_small_data"] if is_small_data else profile["warmup_steps_default"]

    # Max length: bucket from seq_p95 + family cap (RICHER than master-text:
    # master-text profile.suggested_max_length is dataset-only. We combine with family cap.)
    # Floor 1024 (was 256) — matches _select_max_length elsewhere. Aggressive
    # truncation to 512 on tasks like 708e03d4 (Qwen 0.5B + p95=23 translation)
    # produced batch×steps token throughput 14% of legacy bucket, v2 lost +0.4%
    # to winner. Higher floor preserves data exposure even when sequences short.
    target_len = max(1024, int(seq_p95 * 1.15))
    bucketed = next((b for b in LENGTH_BUCKETS if target_len <= b), LENGTH_BUCKETS[-1])
    max_length = min(bucketed, profile["max_length_cap"])

    packing = profile["packing"]
    if family == "smollm" and param_count < 2e9:
        packing = False  # validated: SmolLM<2B harmed by packing

    reg_ratio = (
        profile["reg_ratio_small_data"] if is_small_data
        else profile["reg_ratio_default"]
    )

    # LR: family median if available, else param-based heuristic
    # NEW 2026-05-13: lr_size_buckets override — same family, different LR per size
    # Used by qwen profile to give 0.5B class 2.5e-4 vs 1.5B+ class 8.6e-5
    lr = None
    size_buckets = profile.get("lr_size_buckets")
    if size_buckets and param_count > 0:
        # Buckets defined as max_param_bound (suffix _Nb means N billion)
        # e.g. "0_7b" → 0.7e9, "2_0b" → 2.0e9
        for bucket_key, bucket_lr in sorted(size_buckets.items()):
            # Parse bucket key like "0_7b" → 0.7e9
            try:
                bound_str = bucket_key.lower().rstrip("b").replace("_", ".")
                bound = float(bound_str) * 1e9
                if param_count < bound:
                    lr = bucket_lr
                    print(f"[adaptive] lr_size_bucket hit: param={param_count:,} "
                          f"< {bound_str}B → lr={lr:.2e}", flush=True)
                    break
            except (ValueError, TypeError):
                continue

    if lr is None:
        if profile["lr_default"] is not None:
            lr = profile["lr_default"]
        elif param_count < 1.5e9:
            lr = 1e-4
        elif param_count < 5e9:
            lr = 5e-5
        else:
            lr = 2e-5

    if profile["lr_floor"] is not None:
        lr = max(lr, profile["lr_floor"])

    return {
        "epoch_num": epoch,
        "weight_decay": wd,
        "min_lr_rate": min_lr_rate,
        "neftune_noise_alpha": neftune,
        "warmup_steps": warmup,
        "max_length": max_length,
        "packing": packing,
        "reg_ratio": reg_ratio,
        "learning_rate": lr,
        "_meta": {
            "family_resolved": family,
            "family_arch_signal": arch_family,
            "family_name_signal": _classify_model_family_safe(model_name),
            "profile_source": "rich_hybrid_v1",
        },
    }


# ---------------------------------------------------------------------------
# Main: build run_config dict (matches legacy interface)
# ---------------------------------------------------------------------------

def build_adaptive_run_config(
    task_type: str,
    train_info: dict,
) -> tuple[Dict, str]:
    """100% dynamics-driven run_config builder.

    Returns:
        run_config: dict matching legacy instruct/dpo/grpo run_config format
        arch_family: detected architecture (for logging)

    Caller responsibility: pass to legacy get_run_cmd(run_config) for CLI
    template substitution. State machine then refines LR via multi-run.
    """
    task_type_lc = task_type.lower().replace("task", "").replace("text", "").strip("_")
    model_path = train_info["model_path"]
    task_id = train_info.get("task_id", "")

    # Validator-provided BASELINE_STATS (post G.O.D feature/model-prep-container
    # merge 2026-05-13). JSON env var with model weight stats, dataset stats,
    # init_loss, grad norms. Empty/missing on pre-merge or non-augmented tasks.
    # Spec: docs/tourn_miner.md (BASELINE_STATS env var, "Optional, safe to ignore")
    baseline_stats: Dict = {}
    try:
        _bs_raw = os.getenv("BASELINE_STATS", "").strip()
        if _bs_raw:
            baseline_stats = json.loads(_bs_raw)
            print(f"[adaptive] BASELINE_STATS env present: keys={list(baseline_stats.keys())}", flush=True)
    except Exception as _exc:
        print(f"[adaptive] BASELINE_STATS parse failed (skipped): {_exc}", flush=True)

    # Recover original base model from anonymized model_dir via fingerprint.
    # Validator scrubs `_name_or_path` from config.json but PRESERVES the
    # architecture-defining fields (hidden_size, num_hidden_layers, vocab_size,
    # intermediate_size). When fingerprint matches catalog entry, we recover
    # the original model_id → can use existing lrs_lookup hash table for HP.
    detected_base_model: Optional[str] = None
    try:
        from model_detection import identify_base_model
        _det = identify_base_model(model_path)
        if _det.get("base_model") and _det.get("confidence", 0.0) >= 0.9:
            detected_base_model = _det["base_model"]
            print(f"[adaptive] detected base_model={detected_base_model} via fingerprint "
                  f"key={_det.get('fingerprint_key')} confidence={_det.get('confidence')}", flush=True)
    except Exception as _exc:
        print(f"[adaptive] base_model detection failed (skipped): {_exc}", flush=True)

    # Sensor 1: model from config (NO model_name)
    arch = detect_arch_family(model_path)
    param_count = get_param_count(model_path)
    if param_count is None:
        # Fallback: assume 1B if can't determine
        param_count = 1_000_000_000
        print(f"[adaptive] WARN: param_count unknown, defaulting to 1B", flush=True)
    # NEW 2026-05-15: max_position_embeddings safety probe (for OPT bug + general).
    # Avoids PyTorch indexSelect assertion when packed sequences exceed model's
    # position embedding table. OPT has +2 internal offset (effective max = max_pos - 2).
    # EXP-HYPER-PORT-B/C 2026-05-20: also extract num_hidden_layers + attention head
    # counts for depth-warmup + gqa-batch-boost helpers.
    model_max_position = None
    num_hidden_layers: Optional[int] = None
    num_attention_heads: Optional[int] = None
    num_key_value_heads: Optional[int] = None
    hidden_size: Optional[int] = None  # EXP-TINKER 2026-05-20: for tinker LR formula
    vocab_size: Optional[int] = None  # 2026-05-23: needed for vocab-aware batch cap
    try:
        from transformers import AutoConfig
        _cfg = AutoConfig.from_pretrained(model_path, local_files_only=True, trust_remote_code=False)
        model_max_position = getattr(_cfg, "max_position_embeddings", None)
        num_hidden_layers = getattr(_cfg, "num_hidden_layers", None)
        num_attention_heads = getattr(_cfg, "num_attention_heads", None)
        num_key_value_heads = getattr(_cfg, "num_key_value_heads", None)
        hidden_size = getattr(_cfg, "hidden_size", None)
        vocab_size = getattr(_cfg, "vocab_size", None)
        if model_max_position:
            print(f"[adaptive] model max_position_embeddings={model_max_position}", flush=True)
    except Exception as _e:
        try:
            from transformers import AutoConfig
            _cfg = AutoConfig.from_pretrained(model_path, trust_remote_code=False)
            model_max_position = getattr(_cfg, "max_position_embeddings", None)
            num_hidden_layers = getattr(_cfg, "num_hidden_layers", None)
            num_attention_heads = getattr(_cfg, "num_attention_heads", None)
            num_key_value_heads = getattr(_cfg, "num_key_value_heads", None)
            hidden_size = getattr(_cfg, "hidden_size", None)
            vocab_size = getattr(_cfg, "vocab_size", None)
        except Exception as _e2:
            print(f"[adaptive] WARN: max_position probe failed ({_e2}), skipping safety cap", flush=True)

    # Sensor 2: dataset (post-tokenize path) — graceful fallback chain
    ds_metrics = None
    tokenizer = None
    try:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
    except Exception as e1:
        # Try without local_files_only (HF fallback)
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
        except Exception as e2:
            print(f"[adaptive] tokenizer load failed: {e1} / {e2}", flush=True)
            tokenizer = None

    ds_path = resolve_dataset_path(task_type_lc, task_id)
    if ds_path and tokenizer is not None:
        try:
            ds_metrics = measure_dataset(ds_path, tokenizer, max_samples=500)
            print(f"[adaptive] dataset metrics: n={ds_metrics.num_samples} p95={ds_metrics.seq_len_p95}", flush=True)
        except Exception as e:
            print(f"[adaptive] WARN: measure_dataset failed ({e}), using defaults", flush=True)

    if ds_metrics is None:
        # Conservative fallback: assume medium-size, medium-length
        ds_metrics = DatasetMetrics(
            num_samples=10000,
            seq_len_p50=512,
            seq_len_p95=1024,
            seq_len_p99=1536,  # EXP-HYPER-PORT-A 2026-05-20: token_p99 fallback
            seq_len_max=2048,
        )
        print(f"[adaptive] WARN: using conservative dataset defaults (no path or no tokenizer)", flush=True)

    # Sensor 3: GPU
    gpu = measure_gpu()

    # Decisions
    lora_cfg = _select_lora_config(param_count, task_type_lc)
    use_lora = lora_cfg.get("use_lora", False)
    max_length = _select_max_length(ds_metrics.seq_len_p95, model_max_position=model_max_position)

    # EXP-HYPER-PORT-A 2026-05-20: adaptive-seq-len — halve max_length when
    # token p99 << current cap (port from hyper-text Sprint C7). Reduces
    # padding compute (kernel cycles wasted on masked positions).
    # Fingerprint tag preserved for grep compat with winner 5C7vE26G77n7.
    _p99_for_halving = ds_metrics.seq_len_p99 or ds_metrics.seq_len_p95
    max_length = _maybe_halve_max_length_from_p99(max_length, _p99_for_halving)

    # VRAM-aware batch
    batch = estimate_max_batch_size(
        param_count=param_count,
        seq_len=max_length,
        gpu_metrics=gpu,
        use_lora=use_lora,
    )
    # Resolve GPU count BEFORE batch policy (used in conditional bucket choice).
    gpu_count = max(1, gpu.num_gpus)
    # Batch size policy — REWRITTEN 2026-05-15 from empirical winner data recon.
    #
    # KEY INSIGHT: Multi-GPU caps were OVERLY CONSERVATIVE for 1-GPU validator-side runs.
    # Tournament Instruct = 1 GPU on validator (per memory `tournament/utils.py`:
    # DPO×3, GRPO×2 multipliers; Instruct unmultiplied = 1 GPU).
    #
    # EMPIRICAL WINNER DATA (1-GPU H100 80GB Instruct tasks, May 2026 tournaments):
    #   Qwen-0.5B (0bda471b 5DLkfAsZ tl=1.7559) → batch=140 grad_acc=1
    #   Sheared-LLaMA-1.3B (acd597ef 5Ek3D5Jp tl=1.1017) → batch=100 grad_acc=1
    #   Mistral-7B-DPO (f2a461ec 5Hosruax tl=0.6865 rank2) → batch=28 grad_acc=1
    # All winning configs use Cluster A pattern: cosine_with_min_lr +
    # paged_adamw_8bit + weight_decay=0 + warmup_steps=35.
    # → BOSS scales effective batch INVERSELY with model size (memory-driven).
    #
    # KITA round 2 (Qwen-1.5B) eval@epoch1 = 1.30 vs BOSS = 1.20 (8% behind).
    # Likely cause: KITA eff_batch=32 vs BOSS=100 → less smooth gradient.
    # Apply BOSS empirical batches when running on 1 GPU.
    #
    # Multi-GPU caps preserved separately (DPO 3-GPU, GRPO 2-GPU validator paths).
    # 2-GPU local testing memory budget different (DDP overhead + KV cache).
    #
    # EXP-CC 2026-05-18: SKIP multi-GPU cap for GRPO tasks.
    # GRPO_CONFIG.get_grpo_config() already provides bucket-aware batch+gpu_count
    # tuned for validator-side memory budget. Applying additional cap here causes
    # under-utilization. Empirical: 5df20458 winner used GRPO_CONFIG["4_5_b"]
    # batch=42 LoRA on 2-GPU; our adaptive cap reduced to 8 (5× too low).
    # For DPO + Instruct: keep multi-GPU cap (no equivalent bucket system).
    if gpu_count > 1 and task_type_lc != "grpo":
        # Multi-GPU (validator DPO×3, Instruct OR local 2-GPU testing): keep conservative caps
        # Empirical: Qwen 2.5-3B at batch=64 OOMs at logits alloc (vocab 152k × bf16).
        # Gemma-2-9b vocab=256k OOMs at batch=8 (DDP inp.clone() 15.62 GiB).
        if 1.5e9 <= param_count < 5e9:
            batch = min(batch, 8)
        elif 5e9 <= param_count < 9e9:
            batch = min(batch, 14)
        elif param_count >= 9e9:
            batch = min(batch, 4)
        print(f"[adaptive] multi-GPU ({gpu_count}) cap applied: batch={batch}", flush=True)
    elif gpu_count > 1 and task_type_lc == "grpo":
        # EXP-CC: GRPO uses bucket-managed batch; will be further refined by
        # GRPO_CONFIG batch + _grpo_vanilla_batch_cap below. Skip adaptive cap here.
        print(f"[adaptive] EXP-CC: GRPO on multi-GPU ({gpu_count}) — skip adaptive cap, "
              f"defer to GRPO_CONFIG bucket (was batch={batch})", flush=True)
    else:
        # Single GPU (validator Instruct path): BOSS empirical buckets verified on
        # 3 model families. Larger batch = smoother gradient = faster epoch-1 convergence.
        if param_count < 0.5e9:
            # opt-350m: 17 BOSS winners batch=48; Qwen-0.5B: batch=140.
            # Wide variance — use family-aware override (opt profile caps to 48 via
            # max_length_cap=2046 reducing per-sample memory). Default mid for safety.
            _bucket = 64
        elif param_count < 2e9:
            # 0.5-2B: Qwen-0.5B verified 140, Sheared-1.3B verified 100, Qwen-1.5B target.
            # Use 100 as safe lower bound (smaller models won't OOM).
            _bucket = 100
        elif param_count < 4e9:
            # 2-4B: extrapolation midpoint (no verified data). Interpolate 100 → 28.
            _bucket = 60
        elif param_count < 10e9:
            # 4-10B: Mistral-7B verified 28.
            _bucket = 28
        else:
            # 10B+: conservative scale-down (no verified data, scale ~2× from 7B).
            _bucket = 14
        batch = min(batch, _bucket)
        print(f"[adaptive] 1-GPU empirical bucket: batch={batch} (target={_bucket} for param={param_count/1e9:.2f}B)", flush=True)
    env_batch = os.getenv("INSTRUCT_BATCH_OVERRIDE")
    if env_batch:
        try:
            batch = int(env_batch)
            print(f"[adaptive] batch overridden via env: {batch}", flush=True)
        except ValueError:
            pass

    # ----------------------------------------------------------------------
    # EXP-HYPER-PORT-C 2026-05-20: GQA-aware batch boost (aligned fingerprint).
    # ----------------------------------------------------------------------
    # Replaces EXP-O (2026-05-15) by switching log tag to hyper-text format
    # `[hp-override:gqa-batch-boost]` for grep compat with winner 5C7vE26G77n7
    # tournament fingerprints. Logic identical (×1.20 if gqa_ratio >= 4,
    # ×1.10 if >= 2). Retains 1-GPU gate (multi-GPU has DDP overhead).
    # Source: hyper-text/scripts/hp_override.py:_maybe_gqa_batch_boost (Sprint A1).
    if gpu_count == 1:  # only apply for 1-GPU validator path
        _old_batch = batch
        batch, _gqa_ratio = _maybe_gqa_batch_boost(batch, num_attention_heads, num_key_value_heads)
        if batch > _old_batch:
            _boost_applied = float(batch) / float(_old_batch)
            print(
                f"[hp-override:gqa-batch-boost] gqa_ratio={_gqa_ratio:.1f} "
                f"(q={num_attention_heads}/kv={num_key_value_heads}) "
                f"→ batch_size {_old_batch}→{batch} (×{_boost_applied:.2f})",
                flush=True,
            )

    # ----------------------------------------------------------------------
    # VOCAB-AWARE BATCH CEILING (PROD-VALIDATED BUG-FIX 2026-05-23):
    # ----------------------------------------------------------------------
    # Single-GPU bucket (line ~1219) sized for activation memory but ignored
    # logits tensor memory = batch × seq × vocab × dtype_bytes. For models
    # with vocab >= 100k (Qwen 152k, Gemma-2 256k), logits alone can exceed
    # available VRAM at batch=100+.
    #
    # Production evidence 2026-05-23: Qwen-1.5B (vocab=151,936) on H100 80GB:
    #   batch=120, seq=1024, bf16 → logits = 120 × 1024 × 151936 × 2B ≈ 75GB
    #   OOM tried alloc 69.55 GB. Plus model weights (3GB) + activations
    #   (~21GB) + optimizer state (24GB) = ~123GB needed, only 79GB available.
    # OOM-aware retry in run_training halved batch repeatedly until fit (~30s
    # per retry, burned 3-5 retries before train started).
    #
    # Mirror multi-GPU vocab awareness (line ~1199) for single-GPU path.
    # Formula: cap batch so logits ≤ 30GB safe budget at expected seq=1024.
    #   max_batch_logits = 30e9 / (1024 * vocab * 2)
    # For vocab=152k: max_batch ≈ 96. Use 48 as safety margin (allows GQA
    # boost ×1.20 → 58, well under 96).
    if gpu_count == 1 and vocab_size and vocab_size >= 100000 and param_count >= 1e9:
        _vocab_cap = 48
        if batch > _vocab_cap:
            print(
                f"[adaptive] vocab-aware OOM-safe cap: batch {batch}→{_vocab_cap} "
                f"(vocab={vocab_size}, param={param_count/1e9:.2f}B, "
                f"logits_at_orig=~{batch * 1024 * vocab_size * 2 / 1e9:.1f}GB)",
                flush=True,
            )
            batch = _vocab_cap

    # Init LR — heuristic from arch+param (LRRT can refine in Phase 2)
    # Range: log-scale based on param_count (smaller = higher LR for non-Instruct path).
    # Tiny bucket added 2026-05-03 from f5fbe40f GRPO 135M LOSE: winner used 8e-6
    # (half of our 1.5e-5 for <1.5B). Tiny models on GRPO need extra-low LR to
    # avoid KL drift (winner BETA_GRPO=0.5 penalises drift heavily).
    #
    # 2026-05-14: Family-aware GRPO override for <500M. Research extraction
    # (empirical_hp_rules.json `smollm|0_06b|grpo` n=5) showed SmolLM-360M GRPO
    # winners used 2.0e-4 (25× our 8e-6 default). Add narrow override gated on
    # family=smollm + task=grpo + param<500M. Doesn't affect other tiny GRPO
    # tasks (opt-350m winner=9.95e-6 ≈ default).
    _family_for_lr_gate = _resolve_family(arch, None, detected_base_model)
    if param_count < 5e8:
        if _family_for_lr_gate == "smollm" and task_type_lc == "grpo":
            init_lr = 2.0e-4
            print(f"[adaptive] smollm GRPO <500M LR override 2.0e-4 "
                  f"(was 8e-6 default; from empirical_hp_rules n=5)", flush=True)
        else:
            init_lr = 8e-6
    elif param_count < 1.5e9:
        init_lr = 1.5e-5
    elif param_count < 5e9:
        init_lr = 8e-6
    else:
        init_lr = 5e-6
    # ----------------------------------------------------------------------
    # EXP-B 2026-05-15: Tier 1 — Empirical family LR table lookup
    # ----------------------------------------------------------------------
    # Adopt hyper-text's 140-cell empirical LR table (derived from 783 prior
    # tournament winner training_args). Their winning round 2 5C7vE26G uses
    # this exact pipeline: Tier 1 family_lr → Tier 2 tier-config fallback.
    #
    # Our previous hardcoded lr_size_buckets for qwen <2B was 1.4e-4 — empirical
    # winners use 8.07e-5 (n=11, MED confidence) = 73% LOWER. This explains
    # KITA round 2 underperform (5D7iEJm5 tl=1.1191 missed top-8 by 0.0011).
    #
    # Apply only when confidence >= LOW-ok (n>=2, spread<3x). Single-shot LOW
    # data treated as noise — fall through to next tier.
    # GRPO sub-task selection: "grpo_python" if dataset has python execution
    # reward (rough heuristic; defer to caller for now).
    _family_lr_hit = None
    try:
        from family_lr_table import lookup_lr as _family_lookup_lr, confidence_meets
        from family_lr_table import family_from_architecture as _fam_from_arch
        # Determine architecture string for family_lr_table lookup.
        # Prefer AutoConfig.architectures[0] (most reliable for anonymized models).
        _arch_str_for_lookup = None
        try:
            from transformers import AutoConfig
            _cfg = AutoConfig.from_pretrained(model_path, local_files_only=True, trust_remote_code=False)
            archs = getattr(_cfg, "architectures", None) or []
            if archs:
                _arch_str_for_lookup = archs[0]
        except Exception:
            pass
        # Task type for table key
        _task_key = task_type_lc if task_type_lc in ("dpo", "grpo", "instruct") else "instruct"
        # GRPO python sub-key (heuristic: dataset_type contains "python" reward fn name)
        if _task_key == "grpo":
            _dt = train_info.get("dataset_type") or {}
            _rf = _dt.get("reward_functions") or []
            if isinstance(_rf, list) and any("python" in str(r).lower() for r in _rf):
                _task_key = "grpo_python"
        _result = _family_lookup_lr(
            architecture=_arch_str_for_lookup or "",
            size_b=param_count / 1e9,
            task=_task_key,
        )
        if _result is not None:
            _lr, _conf, _n = _result
            if confidence_meets(_conf, min_conf="LOW-ok"):
                _orig_init_lr = init_lr
                init_lr = _lr
                _family_lr_hit = (_lr, _conf, _n)
                print(f"[adaptive] Tier 1 family_lr HIT: lr={_lr:.4e} conf={_conf} n={_n} "
                      f"task={_task_key} arch={_arch_str_for_lookup} (was generic {_orig_init_lr:.4e})", flush=True)
            else:
                print(f"[adaptive] Tier 1 family_lr SKIP (low conf): {_lr:.4e} conf={_conf} n={_n}", flush=True)
        else:
            print(f"[adaptive] Tier 1 family_lr MISS (no entry for arch={_arch_str_for_lookup} task={_task_key})", flush=True)
    except Exception as _e:
        print(f"[adaptive] Tier 1 family_lr lookup fail-soft: {type(_e).__name__}: {_e}", flush=True)

    # ------------------------------------------------------------------
    # EXP-BOSS-1 FIX (2026-05-20): Wire AR-CSV into ACTIVE adaptive path.
    # ROOT CAUSE: Branch C added AR-CSV functions in lrs_lookup.py but only
    # wired into legacy dpo_config.py / instruct_config.py (ADAPTIVE_MODE=0).
    # Since ADAPTIVE_MODE=1 is default since 2026-05-08, AR-CSV was DEAD CODE
    # in production. Now active as Tier 2 fallback (after family_lr miss).
    # Anonymization-resistant: matches by (arch, closest_param_size).
    # ------------------------------------------------------------------
    _ar_csv_lr = None
    if _family_lr_hit is None and task_type_lc in ("instruct", "dpo"):
        try:
            from lrs_lookup import get_lr_from_ar_dpo, get_lr_from_ar_instruct
            if task_type_lc == "dpo":
                _ar_csv_lr = get_lr_from_ar_dpo(_arch_str_for_lookup, int(param_count))
            else:
                _ar_csv_lr = get_lr_from_ar_instruct(_arch_str_for_lookup, int(param_count))
            if _ar_csv_lr is not None:
                print(f"[adaptive] Tier 2 AR-CSV HIT: lr={_ar_csv_lr:.4e} "
                      f"(arch={_arch_str_for_lookup} size={int(param_count)} task={task_type_lc})", flush=True)
            else:
                print(f"[adaptive] Tier 2 AR-CSV MISS (no entry for arch={_arch_str_for_lookup})", flush=True)
        except Exception as _e:
            print(f"[adaptive] Tier 2 AR-CSV lookup fail-soft: {type(_e).__name__}: {_e}", flush=True)

    # NOTE 2026-05-15: previously here added EXP-D Tier 1.5 reward_classifier
    # for GRPO via suggest_lr_range geomean. Removed as REDUNDANT — KITA's
    # existing GRPO config path (line ~1369) already integrates reward_classifier
    # via suggest_params which returns lr+beta together (richer than range).
    # Existing code overrides init_lr properly. Kept reward_classifier.py port
    # for that existing integration. EXP-D effectively a no-op deadweight here.

    _lr_override_env = os.getenv("ADAPTIVE_LR_OVERRIDE")
    if _lr_override_env:  # guard against empty string from docker --env passthrough
        init_lr = float(_lr_override_env)

    # ----------------------------------------------------------------------
    # EXP-C 2026-05-15: Validator baseline_stats consumer
    # ----------------------------------------------------------------------
    # G.O.D model-prep container (PR #1096) computes pre-training stats and
    # passes path via BASELINE_STATS_PATH env. Provides:
    #   - init_loss (forward pass on dev split with untrained adapter) — replaces our 2.5 placeholder
    #   - grad_norms p95 — future hook for max_grad_norm tightening
    #   - GRPO baseline_reward_scores — future hook for β tuning
    # Fail-soft: returns None when env unset or file missing (legacy tasks).
    # Tier preference:
    #   1. ADAPTIVE_INIT_LOSS_OVERRIDE env (manual)
    #   2. validator baseline_stats init_loss (preferred when present)
    #   3. 2.5 default (placeholder)
    _baseline_stats = None
    _baseline_init_loss = None
    try:
        from baseline_stats_reader import maybe_read_baseline_stats, get_init_loss
        _baseline_stats = maybe_read_baseline_stats()
        if _baseline_stats is not None:
            _baseline_init_loss = get_init_loss(_baseline_stats)
            if _baseline_init_loss is not None:
                print(f"[adaptive] baseline_stats init_loss={_baseline_init_loss:.3f} "
                      f"(replaces 2.5 placeholder)", flush=True)
    except Exception as _e:
        print(f"[adaptive] baseline_stats reader fail-soft: {type(_e).__name__}: {_e}", flush=True)

    # Epochs from init_loss — use validator's actual measurement when available
    _override_init_loss = os.getenv("ADAPTIVE_INIT_LOSS_OVERRIDE")
    if _override_init_loss:
        init_loss_estimate = float(_override_init_loss)
    elif _baseline_init_loss is not None:
        init_loss_estimate = _baseline_init_loss
    else:
        init_loss_estimate = 2.5  # placeholder fallback (legacy tasks without baseline)
    epochs = adaptive_epochs_from_init_loss(init_loss_estimate, ds_metrics.num_samples, param_count)

    # ----------------------------------------------------------------------
    # Phase 1 (2026-05-02): Family-aware Instruct HP — RICHER than master-text
    # ----------------------------------------------------------------------
    # When ADAPTIVE_INSTRUCT_FAMILY=1 (default ON for instruct), override generic
    # HP defaults with family-aware profile. Falls back to generic when family
    # is "unknown" (anonymization-safe). See _compute_instruct_adaptive_hp.
    # Background: prior ADAPTIVE_MODE for instruct used init_lr=8e-6 for 1-5B
    # models — way below SmolLM family median 6.2e-4 (master-text). Caused
    # 3-6× worse eval per memory experiment_results_log. This block fixes that.
    instruct_hp = None
    if task_type_lc == "instruct" and os.getenv("ADAPTIVE_INSTRUCT_FAMILY", "1") == "1":
        instruct_hp = _compute_instruct_adaptive_hp(
            arch_family=arch,
            param_count=param_count,
            data_size=ds_metrics.num_samples,
            seq_p95=ds_metrics.seq_len_p95,
            model_name=train_info.get("model_name") or train_info.get("model"),
            detected_base_model=detected_base_model,  # fingerprint-recovered for anon-resilient family resolution
        )

        # ----------------------------------------------------------------------
        # Plan D (2026-05-03): Advanced dataset profiling + task character router
        # Reverse-engineered from a winning run on 03f6b01c. Key signals:
        # - io_jaccard < 0.3 + no cot/math/code → memorization task (TOFU-like)
        # - lang_ratio < 0.6 or non-latin script → translation
        # - cot/math flag → reasoning
        # - code flag → code task
        # Memorization tasks need LR 3× lower + NEFTune off (winner used ~1.4e-4
        # not master-text 6.2e-4 family default).
        # Enable via ADAPTIVE_TASK_ROUTER (default ON for instruct).
        # ----------------------------------------------------------------------
        if os.getenv("ADAPTIVE_TASK_ROUTER", "1") == "1" and ds_path:
            try:
                from dynamics_utils import profile_dataset_advanced
                profile = profile_dataset_advanced(ds_path, max_samples=256)
                task_class = classify_task_character(profile, model_name=train_info.get("model_name"))
                print(
                    f"[adaptive-instruct] profile: io_jaccard={profile['io_jaccard_p50']:.3f} "
                    f"train_dev_jaccard={profile['train_dev_jaccard']:.3f} "
                    f"flags=cot:{profile['heuristic_flags']['cot']:.2f} "
                    f"math:{profile['heuristic_flags']['math']:.2f} "
                    f"code:{profile['heuristic_flags']['code']:.2f} "
                    f"script={profile['script_overall']} lang_ratio={profile['lang_ratio']:.2f}",
                    flush=True,
                )
                print(f"[adaptive-instruct] task_class={task_class}", flush=True)
                old_lr = instruct_hp["learning_rate"]
                old_epoch = instruct_hp["epoch_num"]
                old_neftune = instruct_hp["neftune_noise_alpha"]
                instruct_hp = _apply_task_character_overrides(
                    instruct_hp, task_class, profile, param_count
                )
                if (instruct_hp["learning_rate"] != old_lr
                    or instruct_hp["epoch_num"] != old_epoch
                    or instruct_hp["neftune_noise_alpha"] != old_neftune):
                    print(
                        f"[adaptive-instruct] task_class={task_class} OVERRIDE: "
                        f"lr {old_lr:.2e}→{instruct_hp['learning_rate']:.2e}, "
                        f"epoch {old_epoch}→{instruct_hp['epoch_num']}, "
                        f"neftune {old_neftune}→{instruct_hp['neftune_noise_alpha']}",
                        flush=True,
                    )
                instruct_hp["_meta"]["dataset_profile"] = profile
            except Exception as exc:
                print(f"[adaptive-instruct] task router error: {exc}", flush=True)

        # ----------------------------------------------------------------------
        # Phase C (2026-05-02): Init loss probe — measures task difficulty
        # ----------------------------------------------------------------------
        if os.getenv("ADAPTIVE_INIT_LOSS_PROBE", "0") == "1" and ds_path:
            try:
                from dynamics_utils import probe_init_loss
                init_loss = probe_init_loss(
                    model_path=model_path,
                    dataset_path=ds_path,
                    max_length=min(512, instruct_hp["max_length"]),
                    batch_size=4,
                    num_batches=4,
                )
                if init_loss is not None:
                    print(f"[adaptive-instruct] init_loss probe: {init_loss:.4f}", flush=True)
                    # NOTE: Phase C heuristic for init_loss>3.5 was REVERTED on 2026-05-03
                    # because it INCREASED neftune+epoch on memorization tasks (TOFU)
                    # which actually HURT eval. Now Plan D task router handles that
                    # via io_jaccard signal. Keep init_loss probe for "easy task"
                    # signal (init_loss < 1.5) to reduce compute when model already knows.
                    if init_loss < 1.5:
                        old_epoch = instruct_hp["epoch_num"]
                        instruct_hp["epoch_num"] = max(2, old_epoch - 1)
                        instruct_hp["neftune_noise_alpha"] = max(0, instruct_hp["neftune_noise_alpha"] - 2)
                        instruct_hp["learning_rate"] = instruct_hp["learning_rate"] * 0.85
                        print(f"[adaptive-instruct] init_loss<1.5: epoch {old_epoch}→{instruct_hp['epoch_num']}, neftune-2, lr*0.85", flush=True)
                    instruct_hp["_meta"]["init_loss"] = init_loss
            except Exception as exc:
                print(f"[adaptive-instruct] init_loss probe error: {exc}", flush=True)

        # Override learnings — PRIMARY (these affect convergence)
        # Guard against empty string from docker --env passthrough (2026-05-14 bug fix)
        _instruct_lr_override = os.getenv("ADAPTIVE_LR_OVERRIDE")
        # EXP-B Tier order fix 2026-05-15: respect Tier 1 family_lr_table hit
        # IF EXP-B fired with confidence (HIGH/MED/MED-low/LOW-ok), it represents
        # empirical winner LR (n>=2 prior wins) and should override instruct_hp
        # legacy lr_default. Otherwise use instruct_hp.
        # Order: ADAPTIVE_LR_OVERRIDE env > Tier 1 family_lr > instruct_hp[learning_rate]
        if _instruct_lr_override:
            init_lr = float(_instruct_lr_override)
        elif _family_lr_hit is not None:
            # EXP-B Tier order fix: family_lr_table represents empirical winner
            # consensus (n>=2 prior wins, confidence-gated). Trust it over
            # instruct_hp's profile default + task_class override.
            # task_class adjustments still apply to OTHER HPs (epochs, neftune,
            # min_lr_rate, weight_decay) via instruct_hp dict consumed below.
            _tier1_lr, _tier1_conf, _tier1_n = _family_lr_hit
            init_lr = _tier1_lr
            print(f"[adaptive] Tier 1 (family_lr) preserved: lr={_tier1_lr:.4e} conf={_tier1_conf} n={_tier1_n} "
                  f"(would have been overridden by instruct_hp to {instruct_hp['learning_rate']:.4e})", flush=True)
        elif _ar_csv_lr is not None:
            # EXP-BOSS-1 FIX (2026-05-20): Tier 2 AR-CSV fallback.
            # Fires when family_lr_table misses (no winner data for this arch+size).
            # Provides architecture-keyed empirical LR (anonymization-resistant).
            init_lr = _ar_csv_lr
            print(f"[adaptive] Tier 2 AR-CSV preserved: lr={_ar_csv_lr:.4e} "
                  f"(would have been overridden by instruct_hp to {instruct_hp['learning_rate']:.4e})", flush=True)
        else:
            init_lr = instruct_hp["learning_rate"]

        # EXP-W 2026-05-17: REVISE EXP-P task_class-specific LR multiplier.
        # family_lr_table is task_class-agnostic (mixes translation+general). Apply
        # post-Tier1 multiplier to correct for known task_class overfit modes.
        #
        # Original EXP-P (commit 5d0a458) used 0.4 based on misreading late-epoch LR
        # as peak. Full Grafana analysis shows winner a208c065 PEAK LR 6.76e-5
        # (not 2.94e-5 late-epoch decay value). KITA Tier 1 8.07e-5 was only +19%
        # over winner. EXP-P × 0.4 over-corrected → kita ended 52% UNDER winner.
        # EXP-W revises to × 0.85 → 6.86e-5 (within 1% of winner 6.76e-5 peak).
        _task_class_lr_mult = {
            "translation": 0.85,  # winner-matched (EXP-W revision of EXP-P)
        }
        _tc = (instruct_hp.get("_meta", {}) or {}).get("task_class")
        if _tc in _task_class_lr_mult:
            _old_init_lr = init_lr
            init_lr = max(2.5e-5, init_lr * _task_class_lr_mult[_tc])
            if abs(init_lr - _old_init_lr) > 1e-9:
                print(f"[adaptive] EXP-P task_class={_tc} LR mult {_task_class_lr_mult[_tc]:.2f}× "
                      f"→ {init_lr:.4e} (was {_old_init_lr:.4e})", flush=True)

        # EXP-TINKER 2026-05-20: Tinker Cookbook LR formula for Instruct LoRA SFT.
        # Source: Thinking Machines (John Schulman lab) tinker_cookbook/hyperparam_utils.py
        #   lr = 5e-5 * 10 * (2000 / hidden_size) ** family_exponent
        # Override gates (ALL must hold):
        #   - TINKER_LR_FORMULA_ENABLED env (default "1")
        #   - task_type == "instruct" (already inside this block)
        #   - use_lora == True (formula is SFT-LoRA specific)
        #   - family resolved + in _TINKER_FAMILY_EXPONENTS
        #   - hidden_size known
        #   - no ADAPTIVE_LR_OVERRIDE env (manual override wins)
        #   - no Tier 1 family_lr_table hit (empirical winner consensus wins)
        # NOTE: GRPO path explicitly EXCLUDED — Tinker formula is for SFT only.
        if (
            os.getenv("TINKER_LR_FORMULA_ENABLED", "1") == "1"
            and use_lora
            and not _instruct_lr_override
            and _family_lr_hit is None
        ):
            _tinker_family = (instruct_hp.get("_meta", {}) or {}).get("family_resolved")
            _tinker_lr = _tinker_instruct_lora_lr(
                model_family=_tinker_family,
                hidden_size=hidden_size,
                current_default_lr=init_lr,
            )
            if _tinker_lr is not None:
                _old_init_lr = init_lr
                init_lr = _tinker_lr
                print(
                    f"[hp-override:tinker-lr] family={_tinker_family} h={hidden_size} "
                    f"formula={init_lr:.2e} (was {_old_init_lr:.2e})",
                    flush=True,
                )

        epochs = instruct_hp["epoch_num"]
        # EXP-K2 2026-05-16: instruct_hp.max_length may bypass validator halving
        # rule when family profile cap > model max_position/2. Re-apply halve
        # (G.O.D common.py:429-431) to keep train/eval distributions aligned.
        # Bug observed on opt-350m (max_pos=2048, profile cap=2046): instruct_hp
        # returned 2046, but validator halves eval to 1024 → 2× context mismatch.
        _instruct_max = instruct_hp["max_length"]
        max_length = min(_instruct_max, max_length)  # max_length carries _select_max_length result
        if max_length != _instruct_max:
            print(f"[adaptive] EXP-K2 max_length halving applied: instruct_hp={_instruct_max} → {max_length} "
                  f"(validator-aligned via max_pos={model_max_position})", flush=True)
        # warmup recomputed below after total_steps

    # Total steps for warmup
    total_steps = max(100, ds_metrics.num_samples * epochs // (batch * gpu_count))
    warmup = adaptive_warmup_steps(total_steps)
    # If instruct adaptive provides explicit warmup_steps, use it instead
    if instruct_hp is not None:
        warmup = instruct_hp["warmup_steps"]

    # EXP-HYPER-PORT-B 2026-05-20: depth-warmup — √depth scaling of warmup_steps
    # for deeper models (port from hyper-text Sprint A3). Goyal+2017 ImageNet:
    # deeper models need longer warmup for gradient stability through layers.
    # Fingerprint tag preserved for grep compat with winner 5C7vE26G77n7.
    if num_hidden_layers and num_hidden_layers > 0:
        _old_warmup = warmup
        _new_warmup = _compute_depth_warmup(warmup, num_hidden_layers)
        if _new_warmup != _old_warmup:
            print(
                f"[hp-override:depth-warmup] depth={num_hidden_layers} "
                f"→ warmup_steps {_old_warmup}→{_new_warmup} (√depth scaling)",
                flush=True,
            )
            warmup = _new_warmup

    # ---------------------------------------------------------------------
    # Augmentation-aware HP adjustment (post-merge BASELINE_STATS path)
    # ---------------------------------------------------------------------
    # When validator augments the base model (50% prob per AUGMENTATION_PROBABILITY),
    # the BaselineStats payload contains weight_rms per layer group. Compare
    # against canonical reference (canonical_weight_rms.json) to infer which
    # of 4 augmentation types was applied + adjust HP accordingly.
    # FAIL-SOFT: missing stats / unknown base model → no-op.
    aug_info: Dict = {"detected_type": None, "confidence": 0.0}
    if baseline_stats and detected_base_model:
        try:
            from model_detection import detect_augmentation
            aug_info = detect_augmentation(baseline_stats, detected_base_model)
            if aug_info.get("detected_type"):
                print(f"[adaptive] augmentation detected: type={aug_info['detected_type']} "
                      f"intensity={aug_info.get('intensity')} confidence={aug_info['confidence']} "
                      f"groups={aug_info.get('affected_groups')}", flush=True)
        except Exception as _exc:
            print(f"[adaptive] augmentation detection failed (skipped): {_exc}", flush=True)

    if aug_info.get("detected_type") == "MAGNITUDE_PRUNING":
        # Pruned weights need slightly higher LR to recover lost capacity.
        # Range: 5-15% weights zeroed; modest +15% LR bump.
        init_lr *= 1.15
        print(f"[adaptive] MAGNITUDE_PRUNING → init_lr×1.15 = {init_lr:.2e}", flush=True)
    elif aug_info.get("detected_type") == "LAYER_REINIT":
        # Random reinit needs longer warmup so reinit'd layer can converge with
        # rest of network. Double existing warmup; floor 70 if previously zero.
        warmup = max(70, warmup * 2)
        print(f"[adaptive] LAYER_REINIT → warmup_steps={warmup}", flush=True)
    elif aug_info.get("detected_type") == "GAUSSIAN_NOISE":
        # Already noisy; turn off NEFTune to avoid stacking regularization.
        # Only meaningful for Instruct (DPO/GRPO don't use NEFTune by default).
        if instruct_hp is not None:
            instruct_hp["neftune_alpha"] = 0
            print(f"[adaptive] GAUSSIAN_NOISE → neftune_alpha=0 (avoid stacking)", flush=True)
    # WEIGHT_SCALING: keep current HP — model is just rescaled, training dynamics
    # still match the base model.

    # Use validator-provided init_loss to refine epochs (replaces internal probe)
    if "training" in baseline_stats and isinstance(baseline_stats["training"], dict):
        _bs_init_loss = baseline_stats["training"].get("init_loss")
        if isinstance(_bs_init_loss, (int, float)) and _bs_init_loss > 0:
            try:
                refined_epochs = adaptive_epochs_from_init_loss(
                    float(_bs_init_loss), ds_metrics.num_samples, param_count
                )
                if refined_epochs != epochs:
                    print(f"[adaptive] BASELINE_STATS init_loss={_bs_init_loss:.4f} → "
                          f"epochs {epochs} → {refined_epochs}", flush=True)
                    epochs = refined_epochs
                    total_steps = max(100, ds_metrics.num_samples * epochs // (batch * gpu_count))
                    if instruct_hp is None:
                        warmup = adaptive_warmup_steps(total_steps)
            except Exception as _exc:
                print(f"[adaptive] init_loss epoch refine failed (skipped): {_exc}", flush=True)

    # Gradient accumulation: same logic as legacy (ensure total_batch ≥ 64)
    grad_accum = 1
    total_batch = batch * gpu_count
    if total_batch < 64:
        grad_accum = min(4, max(1, 64 // total_batch))

    # EXP-T 2026-05-16: hours-aware max_steps cap (TOURNAMENT BUDGET GUARDRAIL).
    # User said berkali-kali: training MUST respect hours_to_complete. Mirror
    # validator's deadline-kill behavior. If estimated step_time × epoch_steps
    # exceeds hours budget, cap max_steps to fit (allow at least 1 eval @step500).
    #
    # Step time estimates (empirically derived 2026-05-15/16):
    #   Instruct (no flash attn): ~0.05 * batch * (seq_len/1024) per step
    #   Instruct (SDPA/FA): ~0.02 * batch * (seq_len/1024)
    #   GRPO (vLLM): ~1-2s/step typical
    #   GRPO (HF gen): ~0.5 * num_gen * (max_completion/256) per sample
    #
    # Override via env ADAPTIVE_HOURS_BUDGET_OVERRIDE to bypass guardrail.
    _hours_budget = train_info.get("hours_to_complete", 2.0)
    if _hours_budget is None:
        _hours_budget = 2.0
    _hours_override = os.getenv("ADAPTIVE_HOURS_BUDGET_OVERRIDE")
    if _hours_override:
        try:
            _hours_budget = float(_hours_override)
            print(f"[adaptive] EXP-T hours_budget override: {_hours_budget}h", flush=True)
        except ValueError:
            pass
    _budget_seconds = float(_hours_budget) * 3600.0 * 0.92  # 8% safety margin (setup + save + upload)

    # CRITICAL FIX 2026-05-22: resolve family EARLY so OPT SDPA check at line 1729 doesn't UnboundLocalError.
    # Previously this block was AFTER line 1729, causing Python to treat `_family_resolved` as local
    # but referenced-before-assigned when training Round 2 DPO tasks (opt-125m + falcon-rw-1b).
    # Both KITA hotkeys crashed with: `UnboundLocalError: cannot access local variable '_family_resolved'`.
    # EXP-Q 2026-05-16: OPT family SDPA attention override.
    # Empirical 3c42f7f4 opt-350m winner 5FW2Eaa step time = 1.26s/it vs KITA 8.57s/it
    # (6.8× faster). Cause: OPT NOT in _FA_SUPPORTED_FAMILIES → we force disable_fa=True
    # → eager attention O(N²). Modern transformers (≥v4.40) supports SDPA for OPT
    # which is O(N²) memory but uses Pytorch native kernel — 3-5× faster than eager
    # without the FA-2 instability risk on OPT.
    # use_attn_implementation overrides disable_fa-derived choice (train_instruct.py:170-172).
    _family_resolved = (instruct_hp or {}).get("_meta", {}).get("family_resolved")
    _attn_impl_override = ""
    if _family_resolved == "opt":
        _attn_impl_override = "sdpa"
        print(f"[adaptive] EXP-Q OPT SDPA enabled (attn_implementation=sdpa) — "
              f"expected 3-5× step speedup vs eager", flush=True)

    # Estimate step time conservatively (over-estimate is safer than under-estimate)
    _effective_batch = max(1, batch * grad_accum)
    if task_type_lc == "grpo":
        # GRPO: generation dominates. Per-step time scales with batch × num_gen × completion length.
        # Default num_gen=5 if not yet computed. max_completion default 512.
        # vLLM: ~5× faster than HF gen. We can't detect at this point reliably; assume HF for safety.
        _num_gen_est = 5  # will be overridden later if vLLM auto-disables
        _max_compl_est = min(1024, max(256, int(ds_metrics.seq_len_p95 * 1.2)))
        _step_time_est = max(2.0, 0.5 * _num_gen_est * (_max_compl_est / 256.0))
    else:
        # Instruct: forward+backward only. SDPA vs eager differs ~5×.
        # Conservative: assume eager for non-FA families.
        _supports_fa = arch_supports_fa(arch) or _family_resolved == "opt"  # opt uses SDPA
        _fa_factor = 0.02 if _supports_fa else 0.06
        _step_time_est = max(0.5, _fa_factor * _effective_batch * (max_length / 1024.0))

    _budget_steps = int(_budget_seconds / _step_time_est)
    # Floor: must allow at least 1 eval cycle (periodic_save_steps=500)
    _eval_floor = 550
    if _budget_steps < _eval_floor:
        print(f"[adaptive] ⚠️  EXP-T: budget {_hours_budget}h / {_step_time_est:.1f}s/step "
              f"= {_budget_steps} steps < {_eval_floor} eval floor. Config too slow for budget.",
              flush=True)
    # Cap max_steps based on budget — but don't override existing GRPO tiny-cap if smaller
    _budget_max_steps = max(_eval_floor, _budget_steps)
    print(f"[adaptive] EXP-T hours_budget={_hours_budget}h step_time_est={_step_time_est:.1f}s "
          f"→ max_steps_budget={_budget_max_steps}", flush=True)

    # Common run_config keys (matches legacy structure)
    run_config = {
        "epoch_num": epochs,
        "batch_size": batch,
        "learning_rate": init_lr,
        "min_lr_rate": instruct_hp["min_lr_rate"] if instruct_hp else 0.25,
        "use_liger": False,  # arch-dependent, conservative default
        "optimizer": _select_optimizer(param_count),
        "use_lora": use_lora,
        "disable_fa": (
            "True" if os.getenv("DISABLE_FA_OVERRIDE", "0") == "1"
            else ("False" if arch_supports_fa(arch) else "True")
        ),
        "gpu_nums": gpu_count,
        "output_dir": train_info.get("output_dir", "/workspace/data/trained_model"),
        "request_path": train_info.get("request_path", ""),
        "distributed": "ds" if param_count > 9e9 and gpu_count >= 4 else "ddp",
        "gradient_checkpointing": "True",
        "gradient_accumulation_steps": grad_accum,
        "warmup_steps": warmup,
        "use_attn_implementation": _attn_impl_override,
        # Adaptive extras (legacy doesn't have but harmless)
        "max_length": max_length,
        "weight_decay": (
            instruct_hp["weight_decay"] if instruct_hp
            else (0.01 if task_type_lc == "instruct" else 0.0)
        ),
        "label_smoothing": 0.0,
        "packing": (
            ("True" if instruct_hp["packing"] else "False") if instruct_hp
            else ("True" if task_type_lc == "instruct" else "False")
        ),
        # NEFTune (lotob-neftune branch added template support).
        # Family-aware: SmolLM small data → 5; large data → 0.
        "neftune_noise_alpha": (
            instruct_hp["neftune_noise_alpha"] if instruct_hp
            else float(os.getenv("NEFTUNE_NOISE_ALPHA", "5.0" if task_type_lc == "instruct" else "0.0"))
        ),
    }

    # Log family resolution + key HP for traceability
    if instruct_hp is not None:
        meta = instruct_hp["_meta"]
        print(
            f"[adaptive-instruct] family={meta['family_resolved']} "
            f"(arch={meta['family_arch_signal']}, name={meta['family_name_signal']}) "
            f"epoch={epochs} lr={init_lr:.2e} min_lr_rate={run_config['min_lr_rate']} "
            f"wd={run_config['weight_decay']} max_len={max_length} "
            f"packing={run_config['packing']} neftune={run_config['neftune_noise_alpha']} "
            f"warmup={warmup} reg_ratio={instruct_hp['reg_ratio']}",
            flush=True,
        )

    # Task-specific
    if task_type_lc == "dpo":
        run_config["beta"] = adaptive_dpo_beta(ds_metrics.num_samples)
        run_config["loss_type"] = "sigmoid"  # vanilla wins per our 2026-04-23 tournament

        # ----------------------------------------------------------------------
        # EXP-N 2026-05-15: DPO β tune from validator implicit_reward_gap
        # ----------------------------------------------------------------------
        # When validator provides BASELINE_STATS_PATH for DPO task with
        # implicit_reward_gap signal, override β based on reference model strength.
        # Source: hyper-text Sprint 1 P0b (_maybe_baseline_dpo_beta_tune).
        # Calibration:
        #   gap < 0.5         → β=0.05 (ref weak, allow strong moves)
        #   gap in [0.5, 2.0] → β=0.10 (default, no change)
        #   gap > 2.0         → β=0.15 (ref strong, constrain)
        if _baseline_stats is not None:
            try:
                from baseline_stats_reader import suggest_dpo_beta_from_baseline
                _current_beta = run_config["beta"]
                _dpo_beta_result = suggest_dpo_beta_from_baseline(
                    _baseline_stats, current_beta=_current_beta
                )
                if _dpo_beta_result is not None:
                    _new_beta, _reason = _dpo_beta_result
                    run_config["beta"] = _new_beta
                    print(f"[adaptive-dpo] EXP-N baseline β tune: {_reason} (was {_current_beta:.3f})", flush=True)
            except Exception as _e:
                print(f"[adaptive-dpo] EXP-N baseline β tune fail-soft: {type(_e).__name__}: {_e}", flush=True)

    elif task_type_lc == "grpo":
        # vLLM optional override (image variants without vllm installed).
        if os.getenv("DISABLE_VLLM_OVERRIDE", "0") == "1":
            run_config["use_vllm"] = False
        # PATCH 2026-05-12: tiny-model vLLM auto-disable.
        # opt-350m and similar <500M models hit vLLM startup timeout (server
        # never comes up — observed retry9 spinning 5+ min on "Server is not
        # up yet"). vLLM minimum reliable model size is ~500M-1B; below that,
        # use HF generation directly (slower but reliable). Override-able via
        # FORCE_VLLM=1 env (for testing).
        if param_count < 5e8 and os.getenv("FORCE_VLLM", "0") != "1":
            run_config["use_vllm"] = False
            print(f"[adaptive-grpo-tiny-vllm] param={param_count:,} <500M, "
                  f"use_vllm=False (avoid vLLM startup timeout on tiny model)",
                  flush=True)
        # Cap batch by vanilla bucket (known-safe upper bound).
        # Slow reward funcs (textstat/langcheck/detoxify) need extra reduction.
        dataset_type = train_info.get("dataset_type", {}) or {}
        slow_reward = is_slow_reward_function(dataset_type)
        vanilla_cap = _grpo_vanilla_batch_cap(param_count)
        if slow_reward:
            vanilla_cap = max(8, vanilla_cap // 4)
            print(f"[adaptive] slow reward function detected → batch cap {vanilla_cap}", flush=True)
        batch = min(batch, vanilla_cap)
        run_config["batch_size"] = batch  # update with capped value

        num_gen = adaptive_grpo_num_generations(batch, gpu.vram_gb_per_gpu, slow_reward=slow_reward)
        # num_gen must divide batch (TRL constraint)
        while batch % num_gen != 0 and num_gen > 2:
            num_gen -= 1
        run_config["num_generations"] = num_gen
        # BETA 0.04 — verified from f5fbe40f winner (5CmAQ61V) + d878f32d winner
        # (5Ca32LwM) via HF training_args.bin extraction 2026-05-04. Both used
        # beta=0.04 with max_steps=-1 (epoch-based). Earlier 0.06 was inflated
        # to "dampen drift" but actual fix is to NOT cap max_steps prematurely
        # (was 300, winners trained full 2 epochs).
        run_config["beta"] = float(os.getenv("ADAPTIVE_BETA_OVERRIDE", "0.04"))
        # EXPERIMENTAL 2026-05-21: Dr.GRPO loss_type via TRL 0.18 native support.
        # Sea AI Lab paper 2503.20783 §3: removes length-bias from GRPO advantage
        # (sum/max_response_length instead of mean/per-completion-len).
        # scale_rewards=False: removes per-group std division per Dr.GRPO recommendation.
        # Previous "scale_rewards=True hurt us" comment was suspect — that test was
        # no-op vs no-op (scale_rewards was never plumbed to CLI, per agent finding
        # in exp_trl_dr_grpo_finding_2026_05_20.md). Now properly plumbed.
        # Env override: TRAINING_GRPO_LOSS_TYPE (default dr_grpo for experimental).
        run_config["loss_type"] = os.getenv("TRAINING_GRPO_LOSS_TYPE", "dr_grpo")
        run_config["scale_rewards"] = os.getenv("TRAINING_GRPO_SCALE_REWARDS", "False").lower() == "true"

        # Tier 1.5: GRPO reward classifier (lotob-grpo-hard).
        # Static analysis of reward_functions → suggests LR + β by landscape.
        # Active when ADAPTIVE_BETA_OVERRIDE/ADAPTIVE_LR_OVERRIDE not explicitly set.
        # Opt-out: TRAINING_REWARD_CLASSIFIER_ENABLED=0
        _classifier_lr_set_via_env = os.getenv("ADAPTIVE_LR_OVERRIDE") is not None
        _classifier_beta_set_via_env = os.getenv("ADAPTIVE_BETA_OVERRIDE") is not None
        classifier_hit = False  # NameError fix 2026-05-17: used by EXP-L baseline_beta gate below
        if (os.getenv("TRAINING_REWARD_CLASSIFIER_ENABLED", "true").lower()
                not in ("0", "false", "no")) and not (
                _classifier_lr_set_via_env and _classifier_beta_set_via_env):
            reward_fns = (train_info.get("dataset_type") or {}).get(
                "reward_functions", []
            )
            if reward_fns:
                try:
                    from reward_classifier import (
                        classify_reward_mix,
                        describe,
                        suggest_params,
                    )
                    fingerprint = classify_reward_mix(reward_fns)
                    classifier_params = suggest_params(
                        fingerprint,
                        model_size_b=(param_count / 1e9) if param_count else None,
                    )
                    if classifier_params is not None:
                        # EXP-EE 2026-05-19: for conflict landscapes, defer to GRPO_CONFIG
                        # bucket lr (validated empirical) over classifier suggestion.
                        # Evidence: 5df20458 winner 5CPgenyJ (balanced_conflict landscape)
                        # used bucket lr=6e-6, classifier suggested 1.35e-5 (2.25× higher).
                        # Bucket lr is data-grounded across many wins; classifier ranges
                        # for conflict are extrapolated from few samples (n<5 per bucket).
                        # For coherent + single + reward_hack: classifier still authoritative.
                        _landscape = (fingerprint or {}).get("landscape", "unknown")
                        _is_conflict = _landscape in ("balanced_conflict", "imbalanced_conflict")
                        if _is_conflict:
                            # Use GRPO_CONFIG bucket lr instead of classifier
                            try:
                                from grpo_config import get_grpo_config
                                _bucket_cfg = get_grpo_config(int(param_count))
                                _bucket_lr = _bucket_cfg.get("lr")
                                if _bucket_lr is not None and not _classifier_lr_set_via_env:
                                    init_lr = float(_bucket_lr)
                                    run_config["learning_rate"] = init_lr
                                    print(f"[classifier] EXP-EE: {_landscape} → defer to GRPO bucket "
                                          f"lr={init_lr:.2e} (classifier suggested "
                                          f"{classifier_params['learning_rate']:.2e})", flush=True)
                                else:
                                    if not _classifier_lr_set_via_env:
                                        init_lr = classifier_params["learning_rate"]
                                        run_config["learning_rate"] = init_lr
                            except Exception as _e:
                                if not _classifier_lr_set_via_env:
                                    init_lr = classifier_params["learning_rate"]
                                    run_config["learning_rate"] = init_lr
                                print(f"[classifier] EXP-EE bucket lookup fail-soft: {_e}", flush=True)
                        else:
                            if not _classifier_lr_set_via_env:
                                init_lr = classifier_params["learning_rate"]
                                run_config["learning_rate"] = init_lr
                        if not _classifier_beta_set_via_env:
                            run_config["beta"] = classifier_params["beta"]
                        classifier_hit = True
                        print(
                            f"[classifier] tier 1.5 hit: lr="
                            f"{classifier_params['learning_rate']:.2e} "
                            f"beta={classifier_params['beta']:.3f} "
                            f"({describe(fingerprint)})",
                            flush=True,
                        )
                    else:
                        print(
                            f"[classifier] no match (unknown reward funcs): "
                            f"{describe(fingerprint)}",
                            flush=True,
                        )
                except Exception as exc:
                    print(
                        f"[classifier] error, fail-soft: "
                        f"{type(exc).__name__}: {exc}",
                        flush=True,
                    )
        run_config["max_completion_length"] = _select_grpo_max_completion(ds_metrics.seq_len_p95)
        # Fix 2026-05-04: previous max_steps=300 was based on WRONG assumption that
        # winners trained minimal steps. Grafana check on f5fbe40f winner (5CmAQ61V)
        # showed they trained ~25K steps with stable LR — full epoch range.
        # Capping at 300 starves us of training; we LOSE all GRPO with 300-step cap.
        # Default: -1 = epoch-based no cap. Trust cosine LR schedule + KL anchor.
        #
        # PATCH 2026-05-12 — tiny-model GRPO drift mitigation:
        # Wave 1+2 020b2f24 (opt-350m GRPO) showed catastrophic KL drift even
        # with β=0.10 anchor (eval_loss -0.0423, KL 0.564). Tiny models drift
        # faster proportionally — cap total drift accumulation time.
        # For param<5e8: cap max_steps at ~1.5 epochs (limits exposure to drift
        # while preserving enough training for reward growth). Override-able
        # via ADAPTIVE_MAX_STEPS_OVERRIDE env.
        _base_max_steps = int(os.getenv("ADAPTIVE_MAX_STEPS_OVERRIDE", "-1"))
        if _base_max_steps == -1 and param_count < 5e8:
            # Tiny GRPO: cap at 1.5 epochs to limit drift time
            _steps_per_epoch_est = max(50, ds_metrics.num_samples // max(1, batch * gpu_count))
            _capped = int(_steps_per_epoch_est * 1.5)
            run_config["max_steps"] = _capped
            print(f"[adaptive-grpo-tiny] param={param_count:,} (<500M) max_steps "
                  f"capped at {_capped} (1.5 epochs ~{_steps_per_epoch_est} steps/ep) "
                  f"to limit KL drift", flush=True)
        else:
            run_config["max_steps"] = _base_max_steps
        # EXP-T 2026-05-16: apply hours_budget cap on top of any GRPO cap.
        # Pick the tighter of: existing cap OR budget cap. -1 means uncapped.
        _existing_grpo_cap = run_config["max_steps"]
        if _existing_grpo_cap == -1 or _budget_max_steps < _existing_grpo_cap:
            run_config["max_steps"] = _budget_max_steps
            print(f"[adaptive-grpo] EXP-T hours_budget tighter than GRPO cap: "
                  f"max_steps {_existing_grpo_cap} → {_budget_max_steps}", flush=True)
        # ----------------------------------------------------------------------
        # EXP-L 2026-05-15: GRPO β tune from validator baseline_reward_scores
        # ----------------------------------------------------------------------
        # When reward_classifier didn't hit (unknown reward fns) AND validator
        # provides baseline_stats with baseline_reward_scores, use that data
        # to tune β. Source: hyper-text Sprint 1 P0c.
        # Calibration (from hyper-text):
        #   mean(scores) >= 5 + cv < 0.5 → β=0.10 (strong+stable signal)
        #   mean(scores) < 1.0           → β=0.04 (weak+noisy, more exploration)
        # Only fires when classifier_hit is False (preserves classifier priority).
        if _baseline_stats is not None and not classifier_hit:
            try:
                from baseline_stats_reader import suggest_grpo_beta_from_baseline
                _current_beta = run_config.get("beta", 0.04)
                _baseline_beta_result = suggest_grpo_beta_from_baseline(
                    _baseline_stats, current_beta=_current_beta
                )
                if _baseline_beta_result is not None:
                    _new_beta, _reason = _baseline_beta_result
                    run_config["beta"] = _new_beta
                    print(f"[adaptive-grpo] EXP-L baseline β tune: {_reason}", flush=True)
            except Exception as _e:
                print(f"[adaptive-grpo] EXP-L baseline β tune fail-soft: {type(_e).__name__}: {_e}", flush=True)

        # Phase 1 sampling tuning (Dr.GRPO inspired): encourage natural EOS
        # NOTE: min_completion_length + vllm_enforce_eager NOT supported by TRL.
        run_config["temperature"] = 0.8
        run_config["top_p"] = 0.9
        run_config["vllm_gpu_memory_utilization"] = 0.4
        run_config["eval_batch_size"] = 1
        # Recompute total_steps + warmup with capped batch
        total_steps = max(100, ds_metrics.num_samples * epochs // (batch * gpu_count))
        warmup = adaptive_warmup_steps(total_steps)

    # ----------------------------------------------------------------------
    # EXP-A 2026-05-15: Dual-strategy "Floating with stable floor"
    # ----------------------------------------------------------------------
    # User insight + data: hyper-text 5C7vE26G WON Round 2 (a208c065 Qwen-1.5B)
    # with tl=1.1048 using SLOW training pattern: lr~5.5e-5, epochs=6, batch=60,
    # max_grad_norm=0.5, wd=0.005 (vs BOSS fast pattern: lr~1e-4, epochs=3, batch=100).
    #
    # KITA Round 2 5D7iEJm5 tl=1.1191 (rank #9, MISSED top 8 BY 0.0011) — extremely
    # close to advancing. Solution: deploy MIX of fast+slow strategies across our
    # 3-5 hotkeys to maximize chance one hits winner regime. Validator picks best.
    #
    # FLOOR (empirical safe baseline) defined per family in _FAMILY_PROFILES + EXP-2
    # batch buckets. FLOATING = strategy multiplier applied here (deterministic).
    #
    # Env-gated for local testing + tournament slot diversification:
    #   KITA_STRATEGY=fast (default): BOSS-style, current behavior. lr unchanged.
    #   KITA_STRATEGY=slow: hyper-text-style. lr×0.4, epochs×1.5, wd=0.005.
    #   KITA_STRATEGY=auto: pick based on dataset size (small=slow, large=fast).
    #
    # Tournament deployment: commit code with KITA_STRATEGY=fast as default. For
    # diversification, create separate marker commits with strategy hardcoded
    # (per-slot fork). See `tournament_submit_2026_05_14.md` for marker pattern.
    #
    # Skip override for GRPO/DPO — round 3 5C7vE26G TEMAN GRPO catastrophic fail
    # (tl=5.5309 vs winner 0.0194 = 283× worse). "Slow" pattern incompatible with
    # KL-drift-sensitive reward training. Instruct only.
    _kita_strategy = os.getenv("KITA_STRATEGY", "fast").strip().lower()
    if _kita_strategy == "auto":
        # Heuristic: small dataset → more epochs help (slow). Large → fast efficient.
        _kita_strategy = "slow" if ds_metrics.num_samples < 20000 else "fast"
        print(f"[adaptive] KITA_STRATEGY=auto resolved to '{_kita_strategy}' (ds_n={ds_metrics.num_samples})", flush=True)
    if _kita_strategy == "slow" and task_type_lc == "instruct":
        _orig_lr = init_lr
        _orig_epochs = epochs
        # Empirical from hyper-text 5C7vE26G round 2 winner training_args.bin:
        # batch=30 grad_acc=2 epochs=6 warmup_steps=67 max_grad_norm=0.5
        # wd=0.005 lr=5.479e-5. For our Qwen-1.5B with fast=1.4e-4, slow factor=0.39.
        init_lr = init_lr * 0.4
        epochs = max(3, int(epochs * 1.5))  # floor 3, e.g. 4→6
        if instruct_hp is not None:
            instruct_hp["weight_decay_default"] = 0.005
            instruct_hp["weight_decay_small_data"] = 0.005
        print(f"[adaptive] KITA_STRATEGY=slow override applied (hyper-text round 2 winner pattern):", flush=True)
        print(f"  lr: {_orig_lr:.3e} → {init_lr:.3e} (×0.4)", flush=True)
        print(f"  epochs: {_orig_epochs} → {epochs} (×1.5)", flush=True)
        print(f"  weight_decay: {instruct_hp.get('weight_decay_default', '?') if instruct_hp else '?'}", flush=True)

    print(f"[adaptive] arch={arch} param={param_count:,} ds_n={ds_metrics.num_samples} seq_p95={ds_metrics.seq_len_p95}", flush=True)
    print(f"[adaptive] PLAN: lr={init_lr:.2e} batch={batch} epochs={epochs} max_len={max_length} lora={use_lora} grad_accum={grad_accum} strategy={_kita_strategy}", flush=True)

    # HP override hooks (selective port from hyper-text Sprint patches 2026-05-13)
    # - probe_warmup_reduction: cuts probe warmup ~2× for more LR signal
    # - d2z_scheduler: switches to linear decay-to-zero when TPP > 1.0 + epochs >= 2
    # Both fail-soft + env-gated. Disable via TRAINING_*_ENABLED=0.
    try:
        from hp_override import apply_all as _hp_apply
        run_config = _hp_apply(
            run_config,
            train_info,
            n_train=ds_metrics.num_samples,
            param_count=param_count,
            seq_p95=ds_metrics.seq_len_p95,
        )
    except Exception as _exc:
        print(f"[hp-override] apply_all failed (skipped, fail-soft): {_exc}", flush=True)

    # SUGGESTION TIER (advisory only — NOT applied):
    # General HP resolver consults empirical_hp_rules.json (winner medians per
    # family×size×task_type). Logs side-by-side comparison for human inspection.
    # Decision NOT auto-applied because resolver lacks task_class disaggregation
    # (translation/skill cluster differs ~4× — see research_aggregate output).
    # Override per-task via env if resolver suggestion seems better:
    #   ADAPTIVE_LR_OVERRIDE=<value> python ...
    try:
        from general_hp_resolver import resolve_hp
        suggestion = resolve_hp(
            model_path,
            task_type_lc,
            num_dataset_samples=ds_metrics.num_samples,
        )
        sug_lr = suggestion.get("learning_rate")
        if sug_lr and sug_lr > 0:
            ratio = sug_lr / init_lr if init_lr > 0 else 0
            print(f"[resolver] SUGGESTION: lr={sug_lr:.2e} ({suggestion.get('_source_tier','?')} "
                  f"n={suggestion.get('_empirical_n','?')} task_class={suggestion.get('_task_class','?')}) "
                  f"vs adaptive_init_lr={init_lr:.2e} → ratio={ratio:.2f}x", flush=True)
    except Exception as _exc:
        print(f"[resolver] suggestion failed (skipped): {_exc}", flush=True)

    # EXP-T 2026-05-16: universal hours_budget enforcement at run_config exit.
    # For Instruct: max_steps not previously set. Apply budget cap here as guardrail.
    # For GRPO: already capped above. This re-checks final value.
    if "max_steps" not in run_config or run_config.get("max_steps", -1) == -1:
        # Only apply cap if epoch-based count exceeds budget by significant margin.
        # Compute rough epoch-based total steps for instruct.
        _est_epoch_steps = max(50, (ds_metrics.num_samples * run_config.get("epoch_num", 2)) // max(1, batch * gpu_count * grad_accum))
        if _est_epoch_steps > _budget_max_steps * 1.5:
            # Budget significantly tighter than epoch-based — cap to budget
            run_config["max_steps"] = _budget_max_steps
            print(f"[adaptive] EXP-T universal cap fires: est_epoch_steps={_est_epoch_steps} > "
                  f"1.5×budget={_budget_max_steps*1.5:.0f} → max_steps={_budget_max_steps}", flush=True)

    # ------------------------------------------------------------------
    # EXP-BOSS-2 (2026-05-20): Apply reg_ratio multiplier on final LR.
    # Root cause: train_info["reg_ratio"] (CLI --reg-ratio default 1.24383
    # in text_trainer.py:299) was extracted via _compute_instruct_adaptive_hp
    # into instruct_hp["reg_ratio"] but NEVER multiplied onto learning_rate.
    # BOSS lion_dance_1 applies × reg_ratio at end of all 3 config files
    # (instruct_config.py:286, dpo_config.py:232, grpo_config.py:350) with
    # CLI default 1.159624 — silent +16% LR boost.
    # Forensic: see research_adaptive_config_diff_2026_05_20.md +
    # research_lion_dance_1_evolution_2026_05_20.md.
    # ------------------------------------------------------------------
    _reg_ratio = train_info.get("reg_ratio", 1.0)
    if _reg_ratio != 1.0 and "learning_rate" in run_config:
        _orig_lr = run_config["learning_rate"]
        run_config["learning_rate"] *= _reg_ratio
        print(f"[adaptive] EXP-BOSS-2: reg_ratio={_reg_ratio:.5f} applied "
              f"(lr {_orig_lr:.2e} → {run_config['learning_rate']:.2e})", flush=True)

    # ------------------------------------------------------------------
    # EXP-HYPER-PORT-E 2026-05-20: per-layer LR multipliers (LARS-style)
    # ------------------------------------------------------------------
    # Compute weight-norm-derived multipliers per layer group (attn.q/k/v/o,
    # mlp.gate/up/down). Stored in run_config so get_adaptive_training_json
    # can attach to train_request → consumed by per_layer_optimizer in
    # train_*.py just before trainer.train(). FAIL-SOFT — missing/bad
    # weights yields None, training continues with single-LR.
    try:
        _multipliers = _compute_per_layer_lr_multipliers(model_path)
        if _multipliers:
            run_config["per_layer_lr_multipliers"] = _multipliers
    except Exception as _exc:
        print(f"[adaptive] per_layer_lr_multipliers compute failed (skipped): "
              f"{type(_exc).__name__}: {_exc}", flush=True)

    return run_config, arch


# ---------------------------------------------------------------------------
# Public API: drop-in replacement for *_config.py get_training_json
# ---------------------------------------------------------------------------

def get_adaptive_training_json(task_type: str, train_info: dict) -> dict:
    """Drop-in replacement for instruct_config.get_training_json (et al).

    Used by text_trainer.py when ADAPTIVE_MODE=on.

    Output structure mirrors legacy:
        {
            "train_request": {...trainer state...},
            "run_cmd": "torchrun ... train_*.py ..."
        }

    Reuses legacy get_run_cmd() for template substitution → state machine
    (initial/continue/finish) works UNCHANGED on top.
    """
    task_type_lc = task_type.lower().replace("task", "").replace("text", "").strip("_")

    # 1. Build run_config from metrics
    run_config, arch_family = build_adaptive_run_config(task_type, train_info)

    # 2. Reuse legacy template builder
    if task_type_lc in ("instruct", "chat"):
        from instruct_config import get_run_cmd as _get_run_cmd
    elif task_type_lc == "dpo":
        from dpo_config import get_run_cmd as _get_run_cmd
    elif task_type_lc == "grpo":
        from grpo_config import get_run_cmd as _get_run_cmd
    else:
        raise ValueError(f"Unknown task_type: {task_type}")

    run_cmd = _get_run_cmd(run_config, run_config["gpu_nums"])

    # 3. Build train_request (matches legacy structure)
    train_request = deepcopy(train_info)
    train_request["save_before_remaining_time"] = 3
    train_request["min_steps"] = 100
    train_request["adjust_batch_size"] = False
    train_request["periodic_save_steps"] = 500
    train_request["checking_step"] = 80
    train_request["adaptive_meta"] = {
        "arch_family": arch_family,
        "version": "v1_static",  # v1 = no init_loss/LRRT, v2 will add
    }

    # EXP-HYPER-PORT-E 2026-05-20: round-trip per-layer LR multipliers
    # through train_request JSON → consumed by per_layer_optimizer in
    # train_*.py just before trainer.train(). Skipped when feature
    # disabled / weight extraction failed (no key in run_config).
    if "per_layer_lr_multipliers" in run_config:
        train_request["per_layer_lr_multipliers"] = run_config["per_layer_lr_multipliers"]

    return {
        "train_request": train_request,
        "run_cmd": run_cmd,
    }
# tournament hotkey slot 1 variant (2026-05-14)
# Same code as 45f6190 — different commit hash for hotkey routing only
# tournament hotkey slot 2 variant (2026-05-14)
# Same code as 45f6190 — different commit hash for hotkey routing only
# tournament hotkey slot 3 variant (2026-05-14)
# Same code as 45f6190 — different commit hash for hotkey routing only
# tournament hotkey slot 4 variant (2026-05-14)
# Same code as 45f6190 — different commit hash for hotkey routing only
# tournament hotkey slot 5 variant (2026-05-14)
# Same code as 45f6190 — different commit hash for hotkey routing only
