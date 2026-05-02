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
}

_FA_SUPPORTED_FAMILIES = {"llama", "mistral", "qwen", "phi", "gemma", "deepseek"}


def detect_arch_family(model_path: str) -> str:
    """Detect architecture family from config, NOT from model_name.

    Returns one of: llama, mistral, qwen, phi, gemma, deepseek, unknown.
    Survives model_name anonymization (per Gradients roadmap).
    """
    try:
        cfg = AutoConfig.from_pretrained(model_path, trust_remote_code=True)
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

    return "unknown"


def arch_supports_fa(arch_family: str) -> bool:
    """Whether arch supports flash_attention_2."""
    return arch_family in _FA_SUPPORTED_FAMILIES


def get_param_count(model_path: str) -> Optional[int]:
    """Param count from config (without loading weights). Survives anonymization."""
    try:
        cfg = AutoConfig.from_pretrained(model_path, trust_remote_code=True)
    except Exception:
        return None
    # Estimate from config dimensions
    h = getattr(cfg, "hidden_size", None)
    n = getattr(cfg, "num_hidden_layers", None)
    v = getattr(cfg, "vocab_size", None)
    inter = getattr(cfg, "intermediate_size", None)
    if not all([h, n, v, inter]):
        return None
    # Rough: embedding + n × (attn + mlp)
    embed = h * v
    attn_per_layer = 4 * h * h  # Q, K, V, O
    mlp_per_layer = 2 * h * inter + h * inter  # gate, up, down
    return embed + n * (attn_per_layer + mlp_per_layer)


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
    completion_len_p95: Optional[int] = None
    has_chat_template_signal: bool = False


def measure_dataset(dataset_path: str, tokenizer, max_samples: int = 1000) -> DatasetMetrics:
    """Probe dataset for length distribution. Handles both JSON array + JSONL.

    For seq_len_p95 → use to set max_length adaptively (no validator-blind 4096).
    Robust to: malformed JSON, missing fields, both JSON-array and JSONL formats.

    BUGFIX 2026-05-02: previously returned `max(n_samples, 1000)` which clipped
    to the SAMPLED count (capped by max_samples=500). For 4000-record TOFU
    dataset this returned num_samples=1000, triggering adaptive's small_data
    HP branch incorrectly. Now reports ACTUAL total dataset count (counted
    before sampling) so adaptive can pick correct medium/large branch.
    """
    seq_lens: List[int] = []
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
    # Use actual_total when known (post-bugfix); fall back to sampled count
    # (legacy behavior) only when file couldn't be parsed at all.
    final_num_samples = actual_total if actual_total > 0 else max(n_samples, 1000)
    return DatasetMetrics(
        num_samples=final_num_samples,
        seq_len_p50=p50,
        seq_len_p95=p95,
        seq_len_max=max(seq_lens),
        has_chat_template_signal=chat_signal,
    )


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
    return min(max_batch, 64)  # cap at 64 for stability


# ---------------------------------------------------------------------------
# LR scheduling helpers
# ---------------------------------------------------------------------------

def adaptive_warmup_steps(total_steps: int, frac: float = 0.10, cap: int = 200) -> int:
    """Warmup as fraction of total, capped."""
    return min(cap, max(10, int(total_steps * frac)))


def adaptive_epochs_from_init_loss(init_loss: float, dataset_size: int) -> int:
    """Convergence-aware epoch count.

    Rule: 1 if model already-trained (low init_loss), 3 if struggling.
    Scales down for large datasets (more samples = fewer passes needed).
    """
    if init_loss < 1.0:
        base = 1
    elif init_loss < 3.0:
        base = 2
    else:
        base = 3
    # Large dataset → fewer epochs
    if dataset_size > 50000:
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
    """
    reward_functions = dataset_type.get("reward_functions", []) if dataset_type else []
    slow_keywords = [
        "import langcheck", "from langcheck",
        "import detoxify", "from detoxify",
        "import textstat", "from textstat",
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
