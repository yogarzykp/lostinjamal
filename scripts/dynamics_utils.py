"""
Dynamics-utils — sensor helpers for 100% adaptive config.

Design: NO model_name lookups, NO bucket logic. Pure metric extraction
from runtime probing of model + dataset + hardware.

Used by adaptive_config.py + lr_finder.py.
"""
import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import torch
from transformers import AutoConfig

# ---------------------------------------------------------------------------
# Architecture detection from config (NOT from model_name)
# ---------------------------------------------------------------------------

# Architecture family signals — derived from config attributes, not name.
# These survive Gradients' upcoming model anonymization.
_ARCH_SIGNATURES = {
    "llama":  {"hidden_act": "silu", "tie_word_embeddings": False, "rope_theta_default": 10000},
    "mistral": {"sliding_window": True},
    "qwen":   {"qkv_bias": True},
    "phi":    {"partial_rotary_factor": True},
    "gemma":  {"rms_norm_eps_high": True},
    "deepseek": {"yarn": True, "n_routed_experts": True},
    # OPT detection: model_type="opt" (anonymization preserves config.model_type).
    # CRITICAL anon-defense — task 3c42f (2026-05-15) crash root cause:
    # anon name strips "opt-" → _classify_model_family_safe returns "unknown" →
    # "unknown" profile has packing=True + max_length_cap=4096 → PyTorch
    # indexSelect assertion at OPTLearnedPositionalEmbedding (positions 2..2049
    # out of bounds). With "opt" detected here, _resolve_family Tier 3 routes
    # to opt profile (packing=False, max_length_cap=2046, lr_default=6e-5).
    "opt":    {"ffn_dim_marker": True},
}

_FA_SUPPORTED_FAMILIES = {"llama", "mistral", "qwen", "phi", "gemma", "deepseek"}


def detect_arch_family(model_path: str) -> str:
    """Detect architecture family from config, NOT from model_name.

    Returns one of: llama, mistral, qwen, phi, gemma, deepseek, opt, unknown.
    Survives model_name anonymization (per Gradients roadmap).
    """
    try:
        cfg = AutoConfig.from_pretrained(model_path, trust_remote_code=False)
    except Exception as e:
        print(f"[dynamics] AutoConfig failed: {e}", flush=True)
        return "unknown"

    model_type = getattr(cfg, "model_type", "").lower()
    # Trust model_type if present (most reliable post-anonymization since it's structural)
    for family in _ARCH_SIGNATURES:
        if family in model_type:
            return family

    # Heuristic fallback from architecture features
    if hasattr(cfg, "qkv_bias") and cfg.qkv_bias:
        return "qwen"
    if hasattr(cfg, "sliding_window") and cfg.sliding_window:
        return "mistral"
    if hasattr(cfg, "partial_rotary_factor"):
        return "phi"
    # OPT uses ffn_dim instead of intermediate_size (heuristic for anon)
    if hasattr(cfg, "ffn_dim") and not hasattr(cfg, "intermediate_size"):
        return "opt"

    return "unknown"


def arch_supports_fa(arch_family: str) -> bool:
    """Whether arch supports flash_attention_2."""
    return arch_family in _FA_SUPPORTED_FAMILIES


# Wrapper architectures nest the decoder's real dimensions one level down. transformers
# calls that sub-config `text_config` (the shape every model in G.O.D's 2026+ pool with a
# multimodal or wrapped decoder uses); a few families use another name.
#
# Every sizing sensor in this repo read the TOP level only, so on such a model they all
# came back None at once: get_param_count returned None and adaptive_config's 1B default
# fired, the vocab-aware OOM cap could not arm because vocab_size was None, and a 9.65B
# model was planned as if it were 1B — full fine-tune, batch sized for a model an order of
# magnitude smaller. This is independent of the transformers version: upgrading so the
# architecture LOADS does not make the numbers appear at the top level.
_NESTED_CONFIG_KEYS = ("text_config", "llm_config", "language_config", "decoder")


def cfg_get(cfg, *names, default=None):
    """Read a decoder dimension, preferring a nested text sub-config when one exists.

    The nest wins, and that ordering was corrected after measuring. The obvious rule —
    top level first, fall back to the nest — is wrong for the exact models this exists
    for, because transformers does not leave the top level EMPTY on a wrapped config: it
    builds a config class, and that class supplies defaults for every standard field. A
    wrapped 9B decoder came back with vocab_size=32000, the LlamaConfig default, while
    the real 151936 sat in `text_config` unread. A missing value announces itself; a
    default does not, and it is the shape that silently mis-sizes a run.

    A flat config has no nest at all, so it is untouched — which is the property that
    makes this safe to drop into the sizing path of every task. The only configs whose
    reading changes are those that actually declare a sub-config, and for those the
    sub-config IS the decoder while the top level belongs to the wrapper.
    """
    for nest in _NESTED_CONFIG_KEYS:
        sub = getattr(cfg, nest, None)
        if sub is None and isinstance(cfg, dict):
            sub = cfg.get(nest)
        if sub is None:
            continue
        for name in names:
            value = sub.get(name) if isinstance(sub, dict) else getattr(sub, name, None)
            if value is not None:
                return value

    for name in names:
        value = getattr(cfg, name, None)
        if value is None and isinstance(cfg, dict):
            value = cfg.get(name)
        if value is not None:
            return value

    return default


MOE_EXPERT_KEYS = ("num_local_experts", "num_experts", "n_routed_experts", "moe_num_experts")


def _advise_param_count_from_raw_json(model_path, exc):
    """Log what config.json says when AutoConfig could not read it. Never returns a value.

    AutoConfig needs the architecture registered in the installed transformers; the four
    fields the size formula uses do not. model_detection.py already reads this same file
    with a plain json.load for fingerprinting, so this borrows a technique the codebase
    already trusts rather than inventing one.
    """
    try:
        path = os.path.join(model_path, "config.json")
        if not os.path.isfile(path):
            print(f"[dynamics] param_count: AutoConfig failed ({exc}); no readable "
                  f"config.json — using the 1B default", flush=True)
            return
        with open(path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
        nested = raw.get("text_config") if isinstance(raw.get("text_config"), dict) else {}
        def _pick(*names):
            for nm in names:
                for src in (raw, nested):
                    if isinstance(src.get(nm), int):
                        return src[nm]
            return None
        h = _pick("hidden_size")
        n = _pick("num_hidden_layers")
        v = _pick("vocab_size")
        inter = _pick("intermediate_size", "ffn_dim")
        if not all([h, n, v, inter]):
            print(f"[dynamics] param_count: AutoConfig failed ({exc}); config.json "
                  f"readable but incomplete — using the 1B default", flush=True)
            return
        est = h * v + n * (4 * h * h + 3 * h * inter)
        print(f"[dynamics] param_count: AutoConfig failed ({exc}); config.json readable, "
              f"raw estimate={est/1e9:.2f}B (ADVISORY, not applied) — using the 1B default",
              flush=True)
    except Exception as _exc:
        print(f"[dynamics] param_count advisory unavailable ({_exc})", flush=True)


def _advise_moe_undercount(model_path, cfg, dense_total, h, inter, n):
    """Log the expert-corrected size when the config declares experts. Never applied."""
    try:
        experts = None
        for key in MOE_EXPERT_KEYS:
            value = cfg_get(cfg, key)
            if isinstance(value, int) and value > 1:
                experts = value
                break
        if experts is None:
            return
        corrected = dense_total + n * 3 * h * inter * (experts - 1)
        print(
            f"[dynamics] param_count: config declares {experts} experts — dense formula "
            f"gives {dense_total/1e9:.2f}B, expert-corrected would be "
            f"{corrected/1e9:.2f}B (ADVISORY, not applied). Every size gate downstream "
            f"is reading the dense number.",
            flush=True,
        )
    except Exception as _exc:
        print(f"[dynamics] MoE advisory unavailable ({_exc})", flush=True)


def get_param_count(model_path: str) -> Optional[int]:
    """Param count from config (without loading weights). Survives anonymization.

    Fixed 2026-05-12: OPT architecture uses ffn_dim instead of intermediate_size.
    Wave 1+2 020b2f24 (opt-350m GRPO) silently fell through to "param unknown,
    default 1B" fallback → size-gated β picked MID bucket (0.06) instead of TINY
    (0.10). Patch: fall back to ffn_dim, and use OPT-aware MLP formula (2× weights
    vs SwiGLU 3×).
    """
    try:
        cfg = AutoConfig.from_pretrained(model_path, trust_remote_code=False)
    except Exception as exc:
        # Still None — this is diagnostics, not a behaviour change. Callers fall back
        # to adaptive_config's 1B sentinel, which is the AGGRESSIVE direction: at 1B
        # the LoRA gates (5e9 instruct, 1.5e9 dpo/grpo) and the DeepSpeed gate (9e9)
        # all stay shut and the batch bucket is the 0.5-2B row, so an undetected large
        # model gets the least protective option on every axis at once.
        #
        # AutoConfig needs the architecture registered; the four numbers below do not.
        # Reporting the raw-JSON estimate makes the gap measurable instead of arguable
        # — the same advisory-only shape adaptive_config already uses for a competing
        # LR it declines to apply. Applying it is a separate decision and needs a run.
        _advise_param_count_from_raw_json(model_path, exc)
        return None
    h = cfg_get(cfg, "hidden_size")
    n = cfg_get(cfg, "num_hidden_layers")
    v = cfg_get(cfg, "vocab_size")
    # OPT uses ffn_dim, llama/qwen/mistral use intermediate_size
    inter = cfg_get(cfg, "intermediate_size", "ffn_dim")
    if not all([h, n, v, inter]):
        return None
    embed = h * v
    attn_per_layer = 4 * h * h  # Q, K, V, O
    # OPT has 2 MLP layers (fc1, fc2); SwiGLU has 3 (gate, up, down).
    arch_str = (cfg_get(cfg, "architectures") or [""])[0]
    is_opt = "opt" in (arch_str or "").lower()
    if is_opt:
        mlp_per_layer = 2 * h * inter   # fc1 + fc2
    else:
        mlp_per_layer = 3 * h * inter   # gate + up + down (SwiGLU)
    dense_total = embed + n * (attn_per_layer + mlp_per_layer)
    # A mixture-of-experts model carries one MLP per expert, so the dense formula
    # above undercounts it by roughly the expert count — Mixtral-8x7B computes to
    # 7.9B against a real 46.7B. This is the SUCCESS path: no WARN fires, and every
    # downstream guardrail (LoRA gate, DeepSpeed gate, batch buckets,
    # estimate_max_batch_size) reads that one number as if it were right.
    #
    # Advisory only, deliberately. Correcting the value would flip a 47B model from
    # full fine-tune + plain DDP + a large batch to LoRA + ZeRO-3 + a small one, and
    # ZeRO-3 has never executed in this repository's smoke suite. That is a training
    # plan change on an untested path, which is a decision to take with a measurement
    # rather than inside an arithmetic fix. The log is what makes the measurement
    # possible. This repo has seen MoE already: family_lr_table.py carries empirical
    # mixtral rows, and general_hp_resolver maps phimoeforcausallm.
    _advise_moe_undercount(model_path, cfg, dense_total, h, inter, n)
    return dense_total


# ---------------------------------------------------------------------------
# GPU / VRAM probing
# ---------------------------------------------------------------------------

@dataclass
class GpuMetrics:
    num_gpus: int
    vram_gb_per_gpu: float
    vram_available_gb: float
    name: str = ""


def measure_gpu() -> GpuMetrics:
    if not torch.cuda.is_available():
        return GpuMetrics(num_gpus=0, vram_gb_per_gpu=0, vram_available_gb=0)
    n = torch.cuda.device_count()
    props = torch.cuda.get_device_properties(0)
    total = props.total_memory / (1024 ** 3)
    free, _ = torch.cuda.mem_get_info(0)
    return GpuMetrics(
        num_gpus=n,
        vram_gb_per_gpu=total,
        vram_available_gb=free / (1024 ** 3),
        name=props.name,
    )


# ---------------------------------------------------------------------------
# Weight statistics — detect pruning/noise augmentation
# ---------------------------------------------------------------------------

@dataclass
class WeightStats:
    num_params: int
    sparsity: float          # fraction of weights ≈ 0 (post-pruning detect)
    rms_per_layer: Dict[str, float]
    rms_max: float
    rms_min: float
    rms_imbalance: float     # max/min ratio (LARS signal)


def measure_weight_stats(model, eps: float = 1e-8, sparsity_threshold: float = 1e-6) -> WeightStats:
    """Probe model for layer-wise statistics.

    Detects:
    - Sparsity (Gradients pruning augmentation)
    - Per-layer RMS imbalance (signal for LARS-style scaling)
    """
    rms_per_layer: Dict[str, float] = {}
    total_params = 0
    near_zero = 0

    for name, p in model.named_parameters():
        if not p.requires_grad and p.dtype not in (torch.float16, torch.bfloat16, torch.float32):
            continue
        flat = p.detach().float().reshape(-1)
        n = flat.numel()
        total_params += n
        # sparsity (post-pruning)
        near_zero += int((flat.abs() < sparsity_threshold).sum().item())
        # RMS
        rms = (flat.pow(2).mean().sqrt().item() + eps)
        rms_per_layer[name] = rms

    sparsity = near_zero / max(1, total_params)
    rms_vals = list(rms_per_layer.values())
    rms_max = max(rms_vals) if rms_vals else 0.0
    rms_min = min(rms_vals) if rms_vals else 1.0
    return WeightStats(
        num_params=total_params,
        sparsity=sparsity,
        rms_per_layer=rms_per_layer,
        rms_max=rms_max,
        rms_min=rms_min,
        rms_imbalance=rms_max / max(rms_min, eps),
    )


# ---------------------------------------------------------------------------
# Init loss measurement (forward pass on dataset subset)
# ---------------------------------------------------------------------------

@torch.no_grad()
def compute_init_loss(model, dataloader, max_batches: int = 8, device: str = "cuda") -> float:
    """Measure model's initial loss on dataset subset before training.

    Used by adaptive plan selector:
    - init_loss < 1 → already-trained or simple task → fewer epochs
    - init_loss > 5 → struggling → more epochs / aggressive LR
    """
    model.eval()
    total = 0.0
    count = 0
    for i, batch in enumerate(dataloader):
        if i >= max_batches:
            break
        batch = {k: v.to(device) for k, v in batch.items() if isinstance(v, torch.Tensor)}
        out = model(**batch)
        loss = out.loss if hasattr(out, "loss") else out["loss"]
        total += loss.item()
        count += 1
    model.train()
    return total / max(1, count)


# ---------------------------------------------------------------------------
# Phase C (2026-05-02): Init loss probe — RICHER than master-text approach.
# ---------------------------------------------------------------------------
# Master-text picks HP from (param_count, data_size, family) lookup table.
# We add: actual measurement of task difficulty for current model+dataset.
# Pre-training forward pass on small batches → init_loss → calibrate HP.
#
# Design:
# - Self-contained: caller passes model_path + dataset_path; we load briefly
# - Memory-safe: bf16 + no_grad + immediate cleanup after probe
# - Fast: 4-8 batches, small max_length probe (256-512), early return
# - Robust: graceful degradation if load fails (return None → caller falls back)


def probe_init_loss(
    model_path: str,
    dataset_path: str,
    *,
    max_length: int = 512,
    batch_size: int = 4,
    num_batches: int = 4,
    device: str = "cuda",
) -> Optional[float]:
    """Quick init_loss probe BEFORE training. Returns avg cross-entropy loss.

    Loads model briefly (bf16 + no_grad), builds tiny dataloader, runs forward
    on `num_batches`, returns mean loss. Memory cleaned up before return.

    Args:
        model_path: HF model path (local cache OK)
        dataset_path: JSON file with `instruct`/`output` records
        max_length: tokenization cap (default 512 for fast probe)
        batch_size: micro-batch (default 4)
        num_batches: forward pass count (default 4 → 16 samples total)

    Returns:
        Float init_loss, or None if probe fails (graceful fallback).
    """
    try:
        import gc
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from torch.utils.data import DataLoader, Dataset

        # Light-weight Dataset — tokenize on-the-fly
        class _ProbeDataset(Dataset):
            def __init__(self, items, tok, max_len):
                self.items = items
                self.tok = tok
                self.max_len = max_len

            def __len__(self):
                return len(self.items)

            def __getitem__(self, i):
                item = self.items[i]
                instr = str(item.get("instruct") or item.get("instruction") or item.get("prompt") or "")
                out = str(item.get("output") or item.get("text") or item.get("chosen") or "")
                # Build prompt + completion text (causal LM training format)
                full = f"{instr}\n{out}".strip()
                if not full:
                    return None
                enc = self.tok(
                    full,
                    truncation=True,
                    max_length=self.max_len,
                    padding="max_length",
                    return_tensors="pt",
                )
                return {
                    "input_ids": enc["input_ids"].squeeze(0),
                    "attention_mask": enc["attention_mask"].squeeze(0),
                    "labels": enc["input_ids"].squeeze(0).clone(),
                }

        # Load tokenizer + dataset items
        with open(dataset_path, "r") as f:
            data = json.load(f)
        if not isinstance(data, list):
            data = data.get("data", []) if isinstance(data, dict) else []
        items = [x for x in data[: batch_size * num_batches * 2] if isinstance(x, dict)]
        if not items:
            print(f"[probe_init_loss] no usable items in dataset", flush=True)
            return None

        tokenizer = AutoTokenizer.from_pretrained(model_path)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        ds = _ProbeDataset(items, tokenizer, max_length)
        dl = DataLoader(ds, batch_size=batch_size, shuffle=False)

        # Load model in bf16 for memory + speed
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.bfloat16,
            low_cpu_mem_usage=True,
        ).to(device)

        init_loss = compute_init_loss(model, dl, max_batches=num_batches, device=device)

        # Cleanup model from VRAM
        del model
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        return init_loss
    except Exception as exc:
        print(f"[probe_init_loss] failed: {type(exc).__name__}: {exc}", flush=True)
        return None


# ---------------------------------------------------------------------------
# Dataset stats
# ---------------------------------------------------------------------------

@dataclass
class DatasetMetrics:
    num_samples: int
    seq_len_p50: int
    seq_len_p95: int
    seq_len_max: int
    seq_len_p99: int = 0  # EXP-HYPER-PORT-A 2026-05-20: token p99 for adaptive-seq-len halving
    completion_len_p95: Optional[int] = None
    has_chat_template_signal: bool = False

    # BUGFIX 2026-08-10 — the fields above come from a single "pick the first
    # field that exists" chain (text, then output, then chosen, then prompt, …).
    # On a standard instruct row {instruct, input, output} that chain selects
    # `output`, so seq_len_* described the COMPLETION only and never the prompt.
    # Measured on a real task: p95 came out 64 tokens where the trained sequence
    # was 1513 — a 24x underestimate that sized max_length at 512 and truncated
    # the long tail of every batch.
    #
    # The fix is not to change what seq_len_* means, because two consumers want
    # two different quantities from it: instruct max_length needs the whole
    # trained sequence, while GRPO's completion-length heuristic was tuned
    # against the prompt-side number. So both are carried explicitly and each
    # consumer names the one it wants. seq_len_* keeps the legacy chain value so
    # nothing silently changes meaning under an existing caller.
    #
    # Populated only when measure_dataset is given a field_map; otherwise None
    # and callers fall back to seq_len_*.
    full_seq_p95: Optional[int] = None   # prompt + input + completion, as trained
    full_seq_p99: Optional[int] = None
    full_seq_max: Optional[int] = None
    prompt_p95: Optional[int] = None     # prompt side alone


def _tok_len(tokenizer, text: str) -> int:
    """Token count, tolerant of tokenizer quirks."""
    if not text:
        return 0
    try:
        return len(tokenizer(text).input_ids)
    except Exception:
        try:
            return len(tokenizer.encode(text))
        except Exception:
            return 0


def _row_lengths(row: dict, tokenizer, field_map: dict, task_type: str):
    """(prompt_tokens, full_sequence_tokens) for one row, per the task's field map.

    field_map is the dataset_type the validator handed us — the same mapping the
    tokenizer uses to build the trained sequence, so this measures the thing that
    actually has to fit inside max_length rather than whichever key happened to
    come first in a fallback chain.

    DPO: both chosen and rejected are trained, so the longer of the two is what
    binds max_length.
    """
    tt = (task_type or "").lower()

    if "dpo" in tt:
        prompt = str(row.get(field_map.get("field_prompt") or "prompt", "") or "")
        chosen = str(row.get(field_map.get("field_chosen") or "chosen", "") or "")
        rejected = str(row.get(field_map.get("field_rejected") or "rejected", "") or "")
        p = _tok_len(tokenizer, prompt)
        return p, p + max(_tok_len(tokenizer, chosen), _tok_len(tokenizer, rejected))

    if "grpo" in tt:
        prompt = str(row.get(field_map.get("field_prompt") or "prompt", "") or "")
        p = _tok_len(tokenizer, prompt)
        return p, p

    # instruct / chat
    parts_prompt = []
    for key in ("field_system", "field_instruction", "field_input"):
        name = field_map.get(key)
        if name:
            v = row.get(name)
            if isinstance(v, str) and v.strip():
                parts_prompt.append(v)
    if not parts_prompt:
        for name in ("instruct", "instruction", "input", "prompt"):
            v = row.get(name)
            if isinstance(v, str) and v.strip():
                parts_prompt.append(v)

    out_name = field_map.get("field_output") or "output"
    completion = row.get(out_name)
    completion = completion if isinstance(completion, str) else ""

    p = _tok_len(tokenizer, "\n\n".join(parts_prompt))
    return p, p + _tok_len(tokenizer, completion)


def measure_dataset(
    dataset_path: str,
    tokenizer,
    max_samples: int = 1000,
    field_map: dict = None,
    task_type: str = "instruct",
) -> DatasetMetrics:
    """Probe dataset for length distribution. Handles both JSON array + JSONL.

    Robust to: malformed JSON, missing fields, both JSON-array and JSONL formats.

    seq_len_* come from a legacy first-match field chain and are kept unchanged so
    existing callers keep their meaning. When `field_map` is supplied, full_seq_*
    and prompt_p95 are also computed by measuring exactly the fields the task
    trains on — see the note on DatasetMetrics for why that distinction exists and
    what it cost us before it did.

    BUGFIX 2026-05-02: previously returned `max(n_samples, 1000)` which clipped
    to the SAMPLED count (capped by max_samples=500). For 4000-record TOFU
    dataset this returned num_samples=1000, triggering adaptive's small_data
    HP branch incorrectly. Now reports ACTUAL total dataset count (counted
    before sampling) so adaptive can pick correct medium/large branch.
    """
    seq_lens: List[int] = []
    prompt_lens: List[int] = []
    full_lens: List[int] = []
    n_samples = 0
    chat_signal = False
    objs: List = []
    actual_total = 0  # NEW: track full dataset size before sampling

    # Try full JSON load first (most tournament datasets are JSON arrays)
    try:
        with open(dataset_path, "r") as f:
            data = json.load(f)
        if isinstance(data, list):
            actual_total = len(data)  # full count
            objs = data[:max_samples]
        elif isinstance(data, dict) and "data" in data:
            # Some datasets nested as {"data": [...]}
            if isinstance(data["data"], list):
                actual_total = len(data["data"])
                objs = data["data"][:max_samples]
            else:
                objs = []
    except (json.JSONDecodeError, ValueError):
        # Fallback: JSONL line-by-line — count total lines first
        try:
            with open(dataset_path, "r") as f:
                actual_total = sum(1 for _ in f)
            with open(dataset_path, "r") as f:
                for i, line in enumerate(f):
                    if len(objs) >= max_samples:
                        break
                    try:
                        objs.append(json.loads(line))
                    except Exception:
                        continue
        except Exception as e:
            print(f"[dynamics] dataset read failed: {e}", flush=True)
    except FileNotFoundError:
        print(f"[dynamics] dataset not found: {dataset_path}", flush=True)

    for obj in objs:
        if not isinstance(obj, dict):
            continue

        # Measure exactly what the task trains on, when we know the mapping.
        # Kept separate from the legacy chain below so no existing consumer
        # silently changes meaning — see the note on DatasetMetrics.
        if field_map:
            try:
                p_len, f_len = _row_lengths(obj, tokenizer, field_map, task_type)
                if f_len > 0:
                    prompt_lens.append(p_len)
                    full_lens.append(f_len)
            except Exception:
                pass

        # Check common field names for both instruct + DPO + GRPO datasets
        text = (
            obj.get("text")
            or obj.get("output")
            or obj.get("chosen")
            or obj.get("prompt")
            or obj.get("instruct")
            or obj.get("instruction")
            or obj.get("input")
            or ""
        )
        if not text or not isinstance(text, str):
            continue
        if "<|" in text or "[INST]" in text:
            chat_signal = True
        try:
            ids = tokenizer.encode(text, add_special_tokens=False)
            seq_lens.append(len(ids))
            n_samples += 1
        except Exception:
            continue

    if not seq_lens:
        # Conservative fallback if measurement fails entirely
        print(f"[dynamics] WARN: dataset measurement empty, using defaults", flush=True)
        seq_lens = [512, 1024, 2048]
    seq_lens.sort()
    p50 = seq_lens[len(seq_lens) // 2]
    p95_idx = min(len(seq_lens) - 1, int(0.95 * len(seq_lens)))
    p95 = seq_lens[p95_idx]
    # EXP-HYPER-PORT-A 2026-05-20: token p99 for adaptive-seq-len helper.
    # Ported from hyper-text dataset_profiler (validator-style token_p99).
    p99_idx = min(len(seq_lens) - 1, int(0.99 * len(seq_lens)))
    p99 = seq_lens[p99_idx]
    # Use actual_total when known (post-bugfix); fall back to sampled count
    # (legacy behavior) only when file couldn't be parsed at all.
    final_num_samples = actual_total if actual_total > 0 else max(n_samples, 1000)

    def _pct(values, q):
        if not values:
            return None
        s = sorted(values)
        return s[min(len(s) - 1, int(q * len(s)))]

    full_p95 = _pct(full_lens, 0.95)
    if full_p95 is not None:
        print(
            f"[dynamics] field-mapped lengths: prompt_p95={_pct(prompt_lens, 0.95)} "
            f"full_seq_p95={full_p95} full_seq_p99={_pct(full_lens, 0.99)} "
            f"(legacy chain p95={p95})",
            flush=True,
        )
        if p95 > 0 and full_p95 / p95 > 2.0:
            # Loud, because this is precisely the divergence that hid a 24x
            # underestimate: the legacy chain was measuring the completion while
            # the trained sequence was far longer.
            print(
                f"[dynamics] NOTE: legacy chain p95={p95} is {full_p95 / p95:.1f}x "
                f"below the field-mapped measurement — the chain is measuring a "
                f"different quantity than the one that must fit in max_length",
                flush=True,
            )

    return DatasetMetrics(
        num_samples=final_num_samples,
        seq_len_p50=p50,
        seq_len_p95=p95,
        seq_len_p99=p99,
        seq_len_max=max(seq_lens),
        has_chat_template_signal=chat_signal,
        full_seq_p95=full_p95,
        full_seq_p99=_pct(full_lens, 0.99),
        full_seq_max=max(full_lens) if full_lens else None,
        prompt_p95=_pct(prompt_lens, 0.95),
    )


# ---------------------------------------------------------------------------
# Plan D (2026-05-03): Advanced dataset profiler — winner-log inspired.
# ---------------------------------------------------------------------------
# Reverse-engineered from a winning run on task 03f6b01c (test_loss=1.4464
# sweep top 4) pulled from Grafana 2026-05-03. The `[dataset-profile-p1/p2]`
# log lines we observed reveal the signal set worth tracking:
# - char_len stats (instruct/output, p50/p95/p99/max)
# - est_token p99 (for max_length sizing)
# - io_jaccard (input/output token overlap → task character signal)
# - train_dev_jaccard (overfit risk: high overlap = some memorization expected)
# - heuristic flags: cot/math/code (task character routing)
# - script + lang_ratio (multilingual detection)
# - near_dup_ratio (data cleanliness)
#
# We use these to ROUTE task to correct HP profile (memorization vs translation
# vs reasoning vs code). Insight: master-text style (high LR + neftune) WORKS
# for translation/skill tasks, HURTS for memorization (TOFU 03f6b01c).


def _word_set(text: str, max_words: int = 200) -> set:
    """Tokenize-ish: lowercase, alphanumeric words, capped for speed."""
    if not text:
        return set()
    import re
    words = re.findall(r"[a-zA-Z一-鿿぀-ヿ؀-ۿ]+", text.lower())
    return set(words[:max_words])


def _jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / max(1, len(a | b))


def _detect_script(text: str) -> str:
    """Detect dominant script: latin/cjk/arabic/cyrillic/mixed."""
    if not text:
        return "unknown"
    import re
    counts = {
        "latin": len(re.findall(r"[a-zA-Z]", text)),
        "cjk": len(re.findall(r"[一-鿿぀-ヿ]", text)),
        "arabic": len(re.findall(r"[؀-ۿ]", text)),
        "cyrillic": len(re.findall(r"[Ѐ-ӿ]", text)),
    }
    total = sum(counts.values())
    if total == 0:
        return "unknown"
    dominant = max(counts, key=counts.get)
    if counts[dominant] / total > 0.7:
        return dominant
    return "mixed"


def _heuristic_flags(items: list, n_check: int = 100) -> dict:
    """Detect task character via simple keyword heuristics (winner-style)."""
    n = min(len(items), n_check)
    if n == 0:
        return {"cot": 0.0, "math": 0.0, "code": 0.0}
    # CoT markers: step-by-step reasoning
    cot_markers = ["step", "first,", "then,", "therefore", "because", "let's", "let us", "thinking"]
    # Math markers
    math_markers = ["=", "\\frac", "\\sum", "\\int", "+", "-", "*", "/", "%", "calculate", "solve"]
    # Code markers — STRICTER (avoid math false positives like Numini-20k):
    # require code-syntax keywords, not generic punctuation `{`/`}`/`()`/`*`
    code_markers_strict = ["def ", "class ", "import ", "function ", "console.log", "print(", "return ", "elif ", "lambda ", "var ", "let ", "const "]
    cot_n = math_n = code_n = 0
    for it in items[:n]:
        if not isinstance(it, dict):
            continue
        text = " ".join(str(it.get(k, "")) for k in ("instruct", "output", "instruction", "answer", "text") if it.get(k))
        text_l = text.lower()
        if any(m in text_l for m in cot_markers):
            cot_n += 1
        # Math: count of math symbols / length
        math_density = sum(text.count(m) for m in math_markers[:6]) / max(1, len(text))
        if math_density > 0.02:
            math_n += 1
        if any(m in text_l for m in code_markers_strict):
            code_n += 1
    return {
        "cot": round(cot_n / n, 3),
        "math": round(math_n / n, 3),
        "code": round(code_n / n, 3),
    }


def profile_dataset_advanced(dataset_path: str, max_samples: int = 256) -> dict:
    """Winner-inspired rich dataset profiler.

    Returns dict with task-character signals used by adaptive HP router:
    - char_len p50/p95/p99 for instruct + output
    - io_jaccard p50/mean (low → generative; high → reformat/translation)
    - train_dev_jaccard (overfit risk signal; higher = more memorization)
    - heuristic_flags: cot/math/code densities
    - script + lang_ratio
    - near_dup_ratio (deduplication signal)
    - actual_total samples count

    All optional — robust to missing fields, JSON-list or JSONL formats.
    Returns dict with available stats; missing stats default to safe values.
    """
    import json as _json
    out = {
        "actual_total": 0,
        "char_len_instruct_p50": 0, "char_len_instruct_p95": 0, "char_len_instruct_p99": 0,
        "char_len_output_p50": 0, "char_len_output_p95": 0, "char_len_output_p99": 0,
        "io_jaccard_p50": 0.0, "io_jaccard_mean": 0.0,
        "train_dev_jaccard": 0.0,
        "heuristic_flags": {"cot": 0.0, "math": 0.0, "code": 0.0},
        "script_overall": "unknown", "lang_ratio": 1.0,
        "near_dup_ratio": 0.0,
    }
    try:
        with open(dataset_path, "r") as f:
            content = f.read().strip()
        if content.startswith("["):
            data = _json.loads(content)
        else:
            data = [_json.loads(l) for l in content.splitlines() if l.strip()]
        if isinstance(data, dict) and "data" in data:
            data = data["data"]
        if not isinstance(data, list):
            return out
        out["actual_total"] = len(data)
    except Exception as exc:
        print(f"[profile_dataset_advanced] read failed: {exc}", flush=True)
        return out

    n = min(len(data), max_samples)
    sample = data[:n] if n > 0 else []

    # Char lengths
    instruct_lens, output_lens = [], []
    io_jaccards = []
    instruct_sets, output_sets = [], []
    output_texts_for_dup = []

    for it in sample:
        if not isinstance(it, dict):
            continue
        instr = str(it.get("instruct") or it.get("instruction") or it.get("prompt") or it.get("input") or "")
        outp = str(it.get("output") or it.get("answer") or it.get("text") or it.get("chosen") or "")
        if instr:
            instruct_lens.append(len(instr))
        if outp:
            output_lens.append(len(outp))
            output_texts_for_dup.append(outp[:200])
        if instr and outp:
            iset = _word_set(instr)
            oset = _word_set(outp)
            instruct_sets.append(iset)
            output_sets.append(oset)
            io_jaccards.append(_jaccard(iset, oset))

    def _percentile(lst, q):
        if not lst:
            return 0
        lst_sorted = sorted(lst)
        idx = min(len(lst_sorted) - 1, max(0, int(q * len(lst_sorted)) - 1))
        return lst_sorted[idx]

    if instruct_lens:
        out["char_len_instruct_p50"] = _percentile(instruct_lens, 0.50)
        out["char_len_instruct_p95"] = _percentile(instruct_lens, 0.95)
        out["char_len_instruct_p99"] = _percentile(instruct_lens, 0.99)
    if output_lens:
        out["char_len_output_p50"] = _percentile(output_lens, 0.50)
        out["char_len_output_p95"] = _percentile(output_lens, 0.95)
        out["char_len_output_p99"] = _percentile(output_lens, 0.99)
    if io_jaccards:
        out["io_jaccard_p50"] = round(_percentile(io_jaccards, 0.50), 3)
        out["io_jaccard_mean"] = round(sum(io_jaccards) / len(io_jaccards), 3)

    # Train-dev jaccard: split sample into proxy train/dev, compute overlap
    if len(output_sets) >= 20:
        split = len(output_sets) // 2
        train_set = set().union(*output_sets[:split])
        dev_set = set().union(*output_sets[split:])
        out["train_dev_jaccard"] = round(_jaccard(train_set, dev_set), 4)

    # Heuristic flags (task character)
    out["heuristic_flags"] = _heuristic_flags(sample)

    # Script + lang ratio (instruct text)
    if sample:
        joined = " ".join(str(it.get("instruct") or it.get("instruction") or "") for it in sample[:50])
        out["script_overall"] = _detect_script(joined)
        # lang_ratio: fraction of latin chars (rough multilingual signal)
        import re as _re
        latin_chars = len(_re.findall(r"[a-zA-Z]", joined))
        total_alpha = max(1, len(_re.findall(r"[\w]", joined)))
        out["lang_ratio"] = round(latin_chars / total_alpha, 3)

    # Near-dup: rough hash collision rate on output prefix
    if output_texts_for_dup:
        seen = set()
        dups = 0
        for t in output_texts_for_dup:
            if t in seen:
                dups += 1
            seen.add(t)
        out["near_dup_ratio"] = round(dups / len(output_texts_for_dup), 4)

    return out


# ---------------------------------------------------------------------------
# VRAM-aware batch size estimation
# ---------------------------------------------------------------------------

def estimate_max_batch_size(
    param_count: int,
    seq_len: int,
    gpu_metrics: GpuMetrics,
    use_lora: bool = False,
    bf16: bool = True,
) -> int:
    """Rough VRAM math for max safe batch.

    Model params: 2 bytes (bf16) × N
    Optimizer state (adamw_8bit): ~3 bytes × trainable params
    Activations: 4 × hidden × layers × seq_len × batch (rough)
    """
    bytes_per_param = 2 if bf16 else 4
    available_bytes = gpu_metrics.vram_available_gb * 1024 ** 3 * 0.75  # safety margin

    # Model
    model_bytes = param_count * bytes_per_param
    # Optimizer (LoRA → only adapter, much smaller)
    opt_bytes = 3 * (param_count * 0.01 if use_lora else param_count)
    # Reserved (activations): scale with seq_len
    # Heuristic: per-token activation ~ 4 × hidden × layers
    # Approx hidden×layers ≈ sqrt(N) for typical decoder
    per_sample_act_bytes = int((param_count ** 0.5) * seq_len * 4)
    free_for_act = available_bytes - model_bytes - opt_bytes
    if free_for_act <= 0:
        return 1
    max_batch = max(1, int(free_for_act / max(1, per_sample_act_bytes)))
    # Multi-GPU multiplies effective batch (per-device stays same)
    # 2026-05-15: cap raised 64 → 200 to allow BOSS-empirical batches.
    # Verified winners: Qwen-0.5B batch=140 (0bda471b 5DLkfAsZ tl=1.7559),
    # Sheared-1.3B batch=100 (acd597ef 5Ek3D5Jp tl=1.1017).
    # Downstream consumer (_compute_instruct_adaptive_hp) applies size buckets to
    # cap appropriately per param_count. This cap only governs VRAM-math ceiling.
    return min(max_batch, 200)


# ---------------------------------------------------------------------------
# LR scheduling helpers
# ---------------------------------------------------------------------------

def adaptive_warmup_steps(total_steps: int, frac: float = 0.10, cap: int = 200) -> int:
    """Warmup as fraction of total, capped."""
    return min(cap, max(10, int(total_steps * frac)))


def adaptive_epochs_from_init_loss(init_loss: float, dataset_size: int, param_count: int | None = None) -> int:
    """Convergence-aware epoch count.

    Rule: 1 if model already-trained (low init_loss), 3 if struggling.
    Scales down for large datasets (more samples = fewer passes needed).
    Tiny models (<500M) on big datasets keep epochs >= 2 — they need extra passes
    even with large data (fix 2026-05-03 from f5fbe40f GRPO 135M LOSE: winner used
    2 epochs for 135M on 393K dataset, our shortened-to-1 was insufficient).
    """
    if init_loss < 1.0:
        base = 1
    elif init_loss < 3.0:
        base = 2
    else:
        base = 3
    # Large dataset → fewer epochs (but tiny models need protection)
    if dataset_size > 50000:
        if param_count is not None and param_count < 5e8:
            base = max(2, base)  # tiny model floor stays at 2
        else:
            base = max(1, base - 1)
    return base


# ---------------------------------------------------------------------------
# Adaptive HP: DPO β, GRPO num_gen
# ---------------------------------------------------------------------------

def adaptive_dpo_beta(dataset_size: int) -> float:
    """β tuned to dataset size (smaller dataset → stricter anchor)."""
    if dataset_size > 10000:
        return 0.05
    elif dataset_size > 1000:
        return 0.1
    else:
        return 0.3


def is_slow_reward_function(dataset_type: dict) -> bool:
    """Reward functions using slow libraries need conservative batch/num_gen.

    Mirrors scripts/grpo_config.py:if_contain_slow_reward_function — duplicated
    here to keep dynamics_utils self-contained (no legacy imports).

    EXP-DD 2026-05-19: distinguish textstat fast vs slow methods.
    - langcheck (NLI model inference) → SLOW
    - detoxify (toxicity classifier) → SLOW
    - textstat methods → varies:
        * Pure string ops (avg_character_per_word, syllable_count, lexicon_count,
          sentence_count, char_count, letter_count) → FAST
        * Readability formulas (flesch_kincaid, gunning_fog, smog) → MEDIUM (still Python)
      All textstat is CPU Python, no model inference → treat as NOT slow.

    Empirical evidence: 5df20458 winner 5CPgenyJ used batch=42 with
    reward_long_words (textstat.avg_character_per_word). Our old code flagged
    this as slow → batch cap 8 (5× under-utilized). Removing textstat from
    slow_keywords matches winner's empirical config.
    """
    reward_functions = dataset_type.get("reward_functions", []) if dataset_type else []
    slow_keywords = [
        "import langcheck", "from langcheck",
        "import detoxify", "from detoxify",
        # EXP-DD: textstat REMOVED — empirically not slow enough to warrant batch cap
        # (winner 5df20458 used batch=42 with textstat without performance issues)
    ]
    for rf in reward_functions:
        func_def = rf.get("reward_func", "")
        if any(kw in func_def for kw in slow_keywords):
            return True
    return False


def adaptive_grpo_num_generations(batch_size: int, gpu_vram_gb: float, slow_reward: bool = False) -> int:
    """Choose num_generations as divisor of batch_size that fits VRAM + reward complexity.

    DeepSeekMath GRPO paper (Shao 2024 arxiv 2402.03300 §3.1): G=8 sweet spot.
    Slow reward functions (textstat/langcheck/detoxify) add per-completion overhead
    so cap is reduced. Lotob v1 2026-04-28 wandb showed crash at G=16 batch=64
    on H100 1× (effective gen batch 1024).
    """
    cap = 4 if slow_reward else 8
    cap = min(cap, max(2, int(gpu_vram_gb * 0.1)))  # VRAM safety floor

    # Divisors of batch_size in [2, cap]
    divisors = [d for d in range(2, cap + 1) if batch_size % d == 0]
    if not divisors:
        return 2  # safe minimum
    return max(divisors)


# ---------------------------------------------------------------------------
# GRPO reward-plateau guard — direct training-time mirror of validator score.
# Validator's eval_loss formula:
#   eval_loss = normalized_reward − BETA_GRPO × kl_divergence  (BETA_GRPO=0.5)
# Tracking the same combination during training gives a 1:1 early-stop signal
# without waiting for a slow eval pass. Higher proxy = better. Plateau →
# eval+save+stop preserves the best snapshot before reward saturates / KL drifts.
# ---------------------------------------------------------------------------


def _parse_bool(value: Optional[str], default: bool = True) -> bool:
    if value is None:
        return default
    return str(value).strip().lower() not in ("0", "false", "no", "off", "")


def grpo_proxy_score(
    rewards: List[float],
    kls: List[float],
    kl_coef: float = 0.5,
) -> Optional[float]:
    """Direct training-time mirror of validator's GRPO eval formula.

    Validator final score (G.O.D docker_evaluation.py:192):
        eval_loss = normalized_reward − BETA_GRPO × kl_divergence
                  = normalized_reward − 0.5 × kl_divergence

    Returns None when either window is empty (caller treats as not ready).
    """
    if not rewards or not kls:
        return None
    return (sum(rewards) / len(rewards)) - kl_coef * (sum(kls) / len(kls))


def grpo_plateau_window(total_steps: int) -> Tuple[int, int]:
    """Compute (warmup_steps, patience_steps) scaled per total training steps.

    Pure-scaling formula:
      - warmup   = 10% of total_steps
      - patience = 15% of post-warmup window
      - Adaptive floor min(50, total_steps//4) keeps Hook 3 active on short runs.

    Env overrides (per-component, take precedence over scaling):
      - TRAINING_GRPO_PLATEAU_WARMUP_STEPS
      - TRAINING_GRPO_PLATEAU_PATIENCE_STEPS

    Examples (worked through manually for sanity):
      total=126   → warmup=31  patience=23
      total=284   → warmup=50  patience=50  (both floored)
      total=1000  → warmup=100 patience=135
      total=39440 → warmup=3944 patience=5324
    """
    warmup_env = os.environ.get("TRAINING_GRPO_PLATEAU_WARMUP_STEPS")
    patience_env = os.environ.get("TRAINING_GRPO_PLATEAU_PATIENCE_STEPS")

    warmup_floor = min(50, max(10, total_steps // 4))
    try:
        if warmup_env:
            warmup = max(1, int(warmup_env))
        else:
            warmup = max(warmup_floor, int(total_steps * 0.10))
    except (TypeError, ValueError):
        warmup = max(warmup_floor, int(total_steps * 0.10))

    post_warmup = max(1, total_steps - warmup)
    patience_floor = min(50, max(10, post_warmup // 4))
    try:
        if patience_env:
            patience = max(1, int(patience_env))
        else:
            patience = max(patience_floor, int(post_warmup * 0.15))
    except (TypeError, ValueError):
        patience = max(patience_floor, int(post_warmup * 0.15))

    return warmup, patience


def maybe_grpo_plateau_stop(
    current_step: int,
    current_proxy: Optional[float],
    best_proxy: Optional[float],
    best_step: int,
    *,
    warmup_steps: Optional[int] = None,
    patience_steps: Optional[int] = None,
    enabled: Optional[bool] = None,
) -> Tuple[Optional[float], int, bool]:
    """Pure-function plateau decision. Caller updates state from first 2 returns.

    Env knobs (only consulted when corresponding arg is None):
      - TRAINING_GRPO_PLATEAU_ENABLED        (default 1)
      - TRAINING_GRPO_PLATEAU_WARMUP_STEPS   (default 500)
      - TRAINING_GRPO_PLATEAU_PATIENCE_STEPS (default 500)

    Returns (new_best_proxy, new_best_step, should_stop).
    Fail-soft: returns (best_proxy, best_step, False) on missing proxy.
    """
    if enabled is None:
        enabled = _parse_bool(
            os.environ.get("TRAINING_GRPO_PLATEAU_ENABLED"), default=True
        )
    if not enabled:
        return best_proxy, best_step, False
    if current_proxy is None:
        return best_proxy, best_step, False

    if warmup_steps is None:
        try:
            warmup_steps = int(os.environ.get("TRAINING_GRPO_PLATEAU_WARMUP_STEPS", "500"))
        except (TypeError, ValueError):
            warmup_steps = 500
    if patience_steps is None:
        try:
            patience_steps = int(os.environ.get("TRAINING_GRPO_PLATEAU_PATIENCE_STEPS", "500"))
        except (TypeError, ValueError):
            patience_steps = 500

    if current_step < warmup_steps:
        return best_proxy, best_step, False

    # First non-warmup observation seeds the best.
    if best_proxy is None or current_proxy > best_proxy:
        return current_proxy, current_step, False

    # Plateau check: best hasn't moved in patience_steps.
    if (current_step - best_step) > patience_steps:
        return best_proxy, best_step, True

    return best_proxy, best_step, False
# branch-rev:grpo-hard-1
# branch-rev:grpo-hard-2
# branch-rev:grpo-hard-3
