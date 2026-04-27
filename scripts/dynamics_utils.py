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


def measure_dataset(jsonl_path: str, tokenizer, max_samples: int = 1000) -> DatasetMetrics:
    """Probe dataset for length distribution. Sample-based for speed.

    For seq_len_p95 → use to set max_length adaptively (no validator-blind 4096).
    """
    seq_lens: List[int] = []
    n_samples = 0
    chat_signal = False
    with open(jsonl_path) as f:
        for i, line in enumerate(f):
            if i >= max_samples:
                break
            try:
                obj = json.loads(line)
            except Exception:
                continue
            text = obj.get("text") or obj.get("output") or obj.get("chosen") or ""
            if "<|" in text or "[INST]" in text:
                chat_signal = True
            tokens = tokenizer(text, add_special_tokens=False, return_length=True)
            seq_lens.append(len(tokens["input_ids"]))
            n_samples += 1

    if not seq_lens:
        seq_lens = [1024]  # safe fallback
    seq_lens.sort()
    p50 = seq_lens[len(seq_lens) // 2]
    p95 = seq_lens[int(0.95 * len(seq_lens))]
    return DatasetMetrics(
        num_samples=n_samples,
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


def adaptive_grpo_num_generations(batch_size: int, gpu_vram_gb: float) -> int:
    """Choose num_generations as divisor of batch_size that fits VRAM."""
    # Find divisors of batch_size in [4, 32]
    divisors = [d for d in range(4, min(33, batch_size + 1)) if batch_size % d == 0]
    if not divisors:
        return 8  # safe default
    # Pick highest divisor that's ≤ vram-aware cap
    cap = int(min(20, gpu_vram_gb * 0.5))  # rough heuristic
    valid = [d for d in divisors if d <= cap]
    if not valid:
        return divisors[0]
    return max(valid)
