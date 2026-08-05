"""
EXP-HYPER-PORT-E 2026-05-20 — LARS-style per-layer LR application.

Source: /Users/zulist/Documents/text/hyper-text/scripts/per_layer_optimizer.py
Tournament audit 2026-05-20: winner 5C7vE26G77n7 uses per-layer LR optimizer
with 12 param-groups. Fingerprint:
    [per-layer-lr] custom optimizer built: 12 groups,
    lr range [1.5000e-04, 5.0706e-04], base=3.0000e-04

Reads `per_layer_lr_multipliers` dict (computed in adaptive_config.py via
_compute_per_layer_lr_multipliers) and rebuilds the trainer's optimizer
with `param_groups` so each layer-type uses `base_lr × multiplier`.

Usage (called AFTER trainer = Trainer(...) and BEFORE trainer.train()):
    from per_layer_optimizer import apply_per_layer_lr_optimizer
    apply_per_layer_lr_optimizer(trainer, multipliers)

Theory (LARS, Goyal+2017, You+2017): optimal layer LR ∝ ||W||_F → larger-norm
layers absorb proportionally more LR without instability. We use clamped
[0.5, 2.0] multipliers from weight_norm ratios.

Fail-soft at every level — if anything goes wrong, original optimizer setup
preserved, training continues with single-LR.

LoRA-aware: pattern matches lora_A / lora_B parameters, since axolotl + PEFT
wrap base model layers.

Env gates:
  PER_LAYER_LR_ENABLED=1  → enable the feature (default OFF since 2026-08-05)
  PER_LAYER_LR_FORCE=1    → bypass size gate (default OFF)
  PER_LAYER_LR_PARAM_NUMS → param count for size gate (0 disables gate)
"""

from __future__ import annotations

import os
import re
from typing import Any, Dict, List, Optional, Tuple


# Layer-type patterns (regex). LoRA params have suffix .lora_A/.lora_B.
# Match against parameter NAME (e.g.,
# "base_model.model.layers.0.self_attn.q_proj.lora_A.default.weight").
# Patterns also match plain (non-LoRA) names for full-finetune compatibility.
#
# Full 12 param-groups per winner 5C7vE26G77n7 fingerprint:
#   embed_tokens, q_proj, k_proj, v_proj, o_proj,
#   mlp.gate_proj, mlp.up_proj, mlp.down_proj,
#   lm_head, norm, bias, default (plus "other" fallback)
_LAYER_PATTERNS: Dict[str, str] = {
    "attn.q_proj":   r"\.q_proj(\.|$)",
    "attn.k_proj":   r"\.k_proj(\.|$)",
    "attn.v_proj":   r"\.v_proj(\.|$)",
    "attn.o_proj":   r"\.o_proj(\.|$)",
    "mlp.gate_proj": r"\.gate_proj(\.|$)",
    "mlp.up_proj":   r"\.up_proj(\.|$)",
    "mlp.down_proj": r"\.down_proj(\.|$)",
}


def _classify_param_name(name: str) -> Optional[str]:
    """Return layer-type label for a parameter name, or None if unmatched."""
    for label, pattern in _LAYER_PATTERNS.items():
        if re.search(pattern, name):
            return label
    return None


def _build_grouped_params(
    model: Any,
    base_lr: float,
    base_wd: float,
    multipliers: Dict[str, float],
    decay_param_names: set,
) -> List[Dict[str, Any]]:
    """Construct optimizer param_groups with per-layer-type LR.

    Each (layer_type, has_decay) combination becomes one group. Unmatched
    parameters fall into the "other" bucket with multiplier=1.0.

    Returns list compatible with torch.optim.AdamW.
    """
    # Map each param to (layer_type, has_decay)
    groups: Dict[Tuple[str, bool], List[Any]] = {}
    for name, p in model.named_parameters():
        if not p.requires_grad:
            continue
        layer_type = _classify_param_name(name) or "other"
        has_decay = name in decay_param_names
        groups.setdefault((layer_type, has_decay), []).append(p)

    param_groups: List[Dict[str, Any]] = []
    for (layer_type, has_decay), params in groups.items():
        if not params:
            continue
        mult = float(multipliers.get(layer_type, 1.0))
        param_groups.append({
            "params": params,
            "lr": base_lr * mult,
            "weight_decay": base_wd if has_decay else 0.0,
        })
    return param_groups


def apply_per_layer_lr_optimizer(trainer: Any,
                                   multipliers: Optional[Dict[str, float]]) -> bool:
    """Override trainer.create_optimizer with per-layer-LR variant.

    Args:
        trainer: HF Trainer (or DPOTrainer / GRPOTrainer subclass)
        multipliers: dict {layer_type: float}; if None or empty, no-op.

    Returns:
        True if applied (custom optimizer factory installed).
        False if skipped (no multipliers, env disabled, size gate, or error).

    Size gate: When env var PER_LAYER_LR_PARAM_NUMS is set to a value in
    (0, 2_000_000_000), the optimizer is skipped because the per-group
    overhead in paged_adamw_8bit (~30% step time on small models) is not
    justified by the marginal LR-scaling benefit. Override with
    PER_LAYER_LR_FORCE=1. When the env var is unset (=0), the gate
    is inactive and the optimizer applies (backward compat).
    """
    if os.getenv("PER_LAYER_LR_ENABLED", "0") != "1":
        print("[per-layer-lr] SKIPPED: PER_LAYER_LR_ENABLED not set to 1 (default off)", flush=True)
        return False

    # Size-gate per-layer-LR. For models <2B params on 1×H100, paged_adamw_8bit
    # overhead per group (~10-15%) compounds with our 7-12 groups to add ~30%
    # step time. Benefit (1-3% loss improvement from LARS-style scaling) doesn't
    # justify cost on small models. Override: PER_LAYER_LR_FORCE=1.
    if os.getenv("PER_LAYER_LR_FORCE") != "1":
        try:
            param_nums_str = os.environ.get("PER_LAYER_LR_PARAM_NUMS", "0")
            param_nums = int(param_nums_str)
        except (TypeError, ValueError):
            param_nums = 0
        if 0 < param_nums < 2_000_000_000:
            print(
                f"[per-layer-lr] SKIPPED: param_nums={param_nums/1e9:.2f}B < 2B threshold "
                f"(default HF optimizer faster on small models). "
                f"Override: PER_LAYER_LR_FORCE=1",
                flush=True,
            )
            return False

    if not multipliers or not isinstance(multipliers, dict):
        return False

    # Filter to numeric values only
    multipliers = {k: float(v) for k, v in multipliers.items() if isinstance(v, (int, float))}
    if not multipliers:
        return False

    # Capture original create_optimizer for fallback
    original_create = trainer.create_optimizer

    def custom_create_optimizer():
        try:
            opt_model = trainer.model
            # HF utility — names of params that should get weight_decay
            decay_param_names = set(trainer.get_decay_parameter_names(opt_model))

            base_lr = float(trainer.args.learning_rate)
            base_wd = float(trainer.args.weight_decay or 0.0)

            param_groups = _build_grouped_params(
                opt_model, base_lr, base_wd, multipliers, decay_param_names
            )
            if not param_groups:
                print(
                    "[per-layer-lr] empty param_groups — fallback to default",
                    flush=True,
                )
                return original_create()

            # Build optimizer with the trainer's chosen class
            optimizer_cls, optimizer_kwargs = trainer.get_optimizer_cls_and_kwargs(trainer.args)
            # Remove lr from kwargs since each group has its own lr
            optimizer_kwargs.pop("lr", None)

            trainer.optimizer = optimizer_cls(param_groups, **optimizer_kwargs)

            # Compact summary — matches winner fingerprint exactly
            n_groups = len(param_groups)
            unique_lrs = sorted({g["lr"] for g in param_groups})
            lr_min = unique_lrs[0]
            lr_max = unique_lrs[-1]
            print(
                f"[per-layer-lr] custom optimizer built: {n_groups} groups, "
                f"lr range [{lr_min:.4e}, {lr_max:.4e}], base={base_lr:.4e}",
                flush=True,
            )
            return trainer.optimizer
        except Exception as exc:
            # Any failure → fall back to default
            print(
                f"[per-layer-lr] FAILED, fallback to default optimizer: "
                f"{type(exc).__name__}: {exc}",
                flush=True,
            )
            return original_create()

    trainer.create_optimizer = custom_create_optimizer
    print(
        f"[per-layer-lr] hook installed on trainer.create_optimizer "
        f"(multipliers: {len(multipliers)} layer-types)",
        flush=True,
    )
    return True
