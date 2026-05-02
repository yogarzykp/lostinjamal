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
    """8bit optimizer for memory savings on large; torch native for small."""
    if param_count is None or param_count > 4e9:
        return "paged_adamw_8bit"
    return "adamw_torch"


def _select_max_length(seq_len_p95: int, validator_max: int = 4096) -> int:
    """Adaptive max_length from data — capped at validator default.

    Source: our experiment 2026-04-26 — DPO max_length=4096 hurt eval
    (3.78 vs 3.06 at 1024). p95-based selection avoids over-padding.
    """
    return min(validator_max, max(1024, int(seq_len_p95 * 1.1)))


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
    """
    if param_count < 2e9:
        return 40
    if param_count < 4e9:
        return 42
    if param_count < 9e9:
        return 32
    return 16


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
    # SmolLM family validated against 5C5FB winning run on ded7e684:
    # epoch=4 + min_lr=0.075 + wd=0.001 + packing=False + max_len=2048
    # → test_loss 0.0502 (vs our text-jagger 0.0989, +97% gap).
    "smollm": {
        "min_lr_rate": 0.075,
        "weight_decay_small_data": 0.001,
        "weight_decay_default": 0.005,
        "packing": False,
        "max_packed_size": 1,
        "max_length_cap": 2048,
        "neftune_alpha_small_data": 5,
        "neftune_alpha_default": 3,
        "warmup_steps_small_data": 15,
        "warmup_steps_default": 35,
        "lr_default": 6.2e-4,    # master-text smollm family median (count=9)
        "lr_floor": 2.4e-4,
        "reg_ratio_small_data": 0.60,
        "reg_ratio_default": 0.70,
    },
    "qwen": {
        "min_lr_rate": 0.18,
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


def _resolve_family(arch_family: str, model_name: Optional[str]) -> str:
    """Resolve effective family from BOTH structural arch + name signals.

    Priority order:
    1. Name maps to specific profile family → use it (most specific wins)
    2. Arch maps to known profile → use it
    3. Arch maps via aliasing (llama→tinyllama, mistral→tinyllama, deepseek→qwen)
    4. Fall back to "unknown" profile
    """
    name_family = _classify_model_family_safe(model_name)
    if name_family in _FAMILY_PROFILES and name_family != "unknown":
        return name_family

    if arch_family in _FAMILY_PROFILES:
        return arch_family
    arch_aliases = {
        "llama": "tinyllama",
        "mistral": "tinyllama",
        "deepseek": "qwen",
    }
    if arch_family in arch_aliases:
        return arch_aliases[arch_family]

    return "unknown"


def _compute_instruct_adaptive_hp(
    arch_family: str,
    param_count: int,
    data_size: int,
    seq_p95: int,
    model_name: Optional[str] = None,
) -> Dict:
    """Build family-aware adaptive HP for Instruct task.

    RICHER than master-text:
    - master-text: (param_count, data_size, family_name)
    - ours: (arch_family, family_name, param_count, data_size, seq_p95)

    Multi-signal: when model_name available, use it for family resolution.
    When not (anonymization), fall back to arch_family from config.

    Returns dict mergable into run_config.
    """
    family = _resolve_family(arch_family, model_name)
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
    target_len = max(256, int(seq_p95 * 1.15))
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

    # Sensor 1: model from config (NO model_name)
    arch = detect_arch_family(model_path)
    param_count = get_param_count(model_path)
    if param_count is None:
        # Fallback: assume 1B if can't determine
        param_count = 1_000_000_000
        print(f"[adaptive] WARN: param_count unknown, defaulting to 1B", flush=True)

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
            seq_len_max=2048,
        )
        print(f"[adaptive] WARN: using conservative dataset defaults (no path or no tokenizer)", flush=True)

    # Sensor 3: GPU
    gpu = measure_gpu()

    # Decisions
    lora_cfg = _select_lora_config(param_count, task_type_lc)
    use_lora = lora_cfg.get("use_lora", False)
    max_length = _select_max_length(ds_metrics.seq_len_p95)

    # VRAM-aware batch
    batch = estimate_max_batch_size(
        param_count=param_count,
        seq_len=max_length,
        gpu_metrics=gpu,
        use_lora=use_lora,
    )
    gpu_count = max(1, gpu.num_gpus)

    # Init LR — heuristic from arch+param (LRRT can refine in Phase 2)
    # Range: log-scale based on param_count (smaller = higher LR)
    if param_count < 1.5e9:
        init_lr = 1.5e-5
    elif param_count < 5e9:
        init_lr = 8e-6
    else:
        init_lr = 5e-6
    init_lr = float(os.getenv("ADAPTIVE_LR_OVERRIDE", str(init_lr)))

    # Epochs from init_loss (placeholder: average expected loss)
    # TODO Phase 2: actual init_loss measurement
    init_loss_estimate = float(os.getenv("ADAPTIVE_INIT_LOSS_OVERRIDE", "2.5"))
    epochs = adaptive_epochs_from_init_loss(init_loss_estimate, ds_metrics.num_samples)

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
        )

        # ----------------------------------------------------------------------
        # Phase C (2026-05-02): Init loss probe — measures task difficulty
        # for THIS model+dataset combo, then refines family HP. RICHER than
        # master-text which only uses (param, data_size, family) lookups.
        # Enable via ADAPTIVE_INIT_LOSS_PROBE=1 (default OFF; ~30-60s overhead).
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
                    # Refine HP based on measured task difficulty
                    if init_loss < 1.5:
                        # Model already strong — reduce regularization+epoch
                        old_epoch = instruct_hp["epoch_num"]
                        instruct_hp["epoch_num"] = max(2, old_epoch - 1)
                        instruct_hp["neftune_noise_alpha"] = max(0, instruct_hp["neftune_noise_alpha"] - 2)
                        instruct_hp["learning_rate"] = instruct_hp["learning_rate"] * 0.85
                        print(f"[adaptive-instruct] init_loss<1.5: epoch {old_epoch}→{instruct_hp['epoch_num']}, neftune-2, lr*0.85", flush=True)
                    elif init_loss > 3.5:
                        # Hard task — bump epochs + keep neftune for regularization
                        old_epoch = instruct_hp["epoch_num"]
                        instruct_hp["epoch_num"] = min(6, old_epoch + 1)
                        instruct_hp["neftune_noise_alpha"] = min(8, instruct_hp["neftune_noise_alpha"] + 1)
                        print(f"[adaptive-instruct] init_loss>3.5: epoch {old_epoch}→{instruct_hp['epoch_num']}, neftune+1", flush=True)
                    else:
                        print(f"[adaptive-instruct] init_loss in [1.5, 3.5]: family HP unchanged", flush=True)
                    instruct_hp["_meta"]["init_loss"] = init_loss
            except Exception as exc:
                print(f"[adaptive-instruct] init_loss probe error: {exc}", flush=True)

        # Override learnings — PRIMARY (these affect convergence)
        init_lr = float(os.getenv("ADAPTIVE_LR_OVERRIDE", str(instruct_hp["learning_rate"])))
        epochs = instruct_hp["epoch_num"]
        max_length = instruct_hp["max_length"]
        # warmup recomputed below after total_steps

    # Total steps for warmup
    total_steps = max(100, ds_metrics.num_samples * epochs // (batch * gpu_count))
    warmup = adaptive_warmup_steps(total_steps)
    # If instruct adaptive provides explicit warmup_steps, use it instead
    if instruct_hp is not None:
        warmup = instruct_hp["warmup_steps"]

    # Gradient accumulation: same logic as legacy (ensure total_batch ≥ 64)
    grad_accum = 1
    total_batch = batch * gpu_count
    if total_batch < 64:
        grad_accum = min(4, max(1, 64 // total_batch))

    # Common run_config keys (matches legacy structure)
    run_config = {
        "epoch_num": epochs,
        "batch_size": batch,
        "learning_rate": init_lr,
        "min_lr_rate": instruct_hp["min_lr_rate"] if instruct_hp else 0.25,
        "use_liger": False,  # arch-dependent, conservative default
        "optimizer": _select_optimizer(param_count),
        "use_lora": use_lora,
        "disable_fa": "False" if arch_supports_fa(arch) else "True",
        "gpu_nums": gpu_count,
        "output_dir": train_info.get("output_dir", "/workspace/data/trained_model"),
        "request_path": train_info.get("request_path", ""),
        "distributed": "ds" if param_count > 9e9 and gpu_count >= 4 else "ddp",
        "gradient_checkpointing": "True",
        "gradient_accumulation_steps": grad_accum,
        "warmup_steps": warmup,
        "use_attn_implementation": "",
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

    elif task_type_lc == "grpo":
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
        # Option B (2026-04-29): raise β 0.04→0.06 to anchor stronger to ref model.
        # Validator BETA_GRPO=0.5 (verified VPS 221 /root/G.O.D-eval-text/validator/
        # core/constants.py:277) → KL drift directly subtracted at eval. Top miner
        # 5DfdHDKN test_loss=0.195 implies KL≤0.6 across batch (~0.012/sample).
        # Our v1 -6.9 + v4 -24.5 imply KL ~14-50 across batch (~0.3-1.0/sample) —
        # 50× drift vs winner. Raise β to dampen drift.
        run_config["beta"] = float(os.getenv("ADAPTIVE_BETA_OVERRIDE", "0.06"))
        run_config["scale_rewards"] = "True"  # Dr.GRPO False hurt us
        run_config["max_completion_length"] = _select_grpo_max_completion(ds_metrics.seq_len_p95)
        # Option B: cap max_steps to limit drift accumulation. Top miner trained
        # minimal steps; over-training causes KL blowup. 300 = ~30 logged steps
        # at logging_steps=5, enough for reward signal without runaway drift.
        run_config["max_steps"] = int(os.getenv("ADAPTIVE_MAX_STEPS_OVERRIDE", "300"))
        # Phase 1 sampling tuning (Dr.GRPO inspired): encourage natural EOS
        # NOTE: min_completion_length + vllm_enforce_eager NOT supported by TRL.
        run_config["temperature"] = 0.8
        run_config["top_p"] = 0.9
        run_config["vllm_gpu_memory_utilization"] = 0.4
        run_config["eval_batch_size"] = 1
        # Recompute total_steps + warmup with capped batch
        total_steps = max(100, ds_metrics.num_samples * epochs // (batch * gpu_count))
        warmup = adaptive_warmup_steps(total_steps)

    print(f"[adaptive] arch={arch} param={param_count:,} ds_n={ds_metrics.num_samples} seq_p95={ds_metrics.seq_len_p95}", flush=True)
    print(f"[adaptive] PLAN: lr={init_lr:.2e} batch={batch} epochs={epochs} max_len={max_length} lora={use_lora} grad_accum={grad_accum}", flush=True)

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

    return {
        "train_request": train_request,
        "run_cmd": run_cmd,
    }
