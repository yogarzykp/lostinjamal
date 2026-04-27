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

    Source: our wandb finding 2026-04-27 — all GRPO runs hit
    completions/clipped_ratio: 1.0 at default 256 → reward gaming.
    Adaptive cap reduces ramble pathology.
    """
    return min(512, max(64, int(seq_len_p95 * 0.5)))


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

    # Sensor 2: dataset (post-tokenize path)
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    ds_path = resolve_dataset_path(task_type_lc, task_id)
    if ds_path:
        ds_metrics = measure_dataset(ds_path, tokenizer, max_samples=500)
    else:
        # Conservative fallback: assume medium-size, medium-length
        ds_metrics = DatasetMetrics(
            num_samples=10000,
            seq_len_p50=512,
            seq_len_p95=1024,
            seq_len_max=2048,
        )
        print(f"[adaptive] WARN: dataset path not found, using conservative defaults", flush=True)

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

    # Total steps for warmup
    total_steps = max(100, ds_metrics.num_samples * epochs // (batch * gpu_count))
    warmup = adaptive_warmup_steps(total_steps)

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
        "min_lr_rate": 0.25,
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
        "use_attn_implementation": "",
        # Adaptive extras (legacy doesn't have but harmless)
        "max_length": max_length,
        "weight_decay": 0.01 if task_type_lc == "instruct" else 0.0,
        "label_smoothing": 0.0,
        "packing": True if task_type_lc == "instruct" else False,
    }

    # Task-specific
    if task_type_lc == "dpo":
        run_config["beta"] = adaptive_dpo_beta(ds_metrics.num_samples)
        run_config["loss_type"] = "sigmoid"  # vanilla wins per our 2026-04-23 tournament

    elif task_type_lc == "grpo":
        # num_gen must divide batch
        num_gen = adaptive_grpo_num_generations(batch, gpu.vram_gb_per_gpu)
        # Adjust to divide batch
        while batch % num_gen != 0 and num_gen > 1:
            num_gen -= 1
        run_config["num_generations"] = num_gen
        run_config["beta"] = 0.04  # TRL default
        run_config["scale_rewards"] = "True"  # Dr.GRPO False hurt us
        run_config["max_completion_length"] = _select_grpo_max_completion(ds_metrics.seq_len_p95)
        run_config["vllm_gpu_memory_utilization"] = 0.4
        run_config["eval_batch_size"] = 1

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
