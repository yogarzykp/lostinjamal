"""
HP override module — selective ports from hyper-text (TEMAN) Sprint patches.

Ported 2026-05-13 (pre-tournament). Each patch is fail-soft + env-gated.

Patches included:
1. probe_warmup_reduction (P0.3 from hyper-text Sprint B)
   — Reduce warmup for PROBE phase only. Final run re-bumps via
   text_trainer._compute_final_run_overrides. Net: ~2× more effective full-LR
   probe signal. Bias: small filter against extreme HIGH LRs (desirable).
2. d2z_scheduler (P0.2 from hyper-text Sprint B)
   — Switch lr_scheduler_type to `linear` (D2Z = decay-to-zero) when
   tokens-per-param > 1.0 AND epochs >= 2. Better convergence at
   compute-optimal sizing per Pareja arXiv:2412.13337.

Both patches operate on `run_config` dict (our format) before train_cmd
construction. Called from adaptive_config end of get_adaptive_training_json.

Env flags (all default ENABLED):
- TRAINING_PROBE_WARMUP_REDUCTION_ENABLED=1
- TRAINING_PROBE_WARMUP_RATIO=0.15
- TRAINING_PROBE_WARMUP_FLOOR=10
- TRAINING_SCHEDULER_D2Z_AUTO=1
- TRAINING_D2Z_TPP_THRESHOLD=1.0
- TRAINING_D2Z_MIN_EPOCHS=2
"""
from __future__ import annotations

import os
from typing import Dict, Optional


def _bool_env(name: str, default: bool = True) -> bool:
    """Parse env var as bool. Default true unless explicit disable."""
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() not in {"0", "false", "no", "off"}


def maybe_probe_warmup_reduction(run_config: Dict, checking_step: Optional[int]) -> Dict:
    """Reduce warmup for PROBE phase (state_manager.checking_step set).

    Args:
        run_config: dict with current `warmup_steps`
        checking_step: from train_request (state_manager); None for final run

    Returns:
        Mutated run_config (in-place + return for chaining)

    Theory (Pareja arXiv:2412.13337 + hyper-text empirical):
    - Modern SFT recipe: <= 10% warmup ratio
    - Probe with 70 steps + warmup=35 wastes 50% on warmup
    - Final run re-bumps via _compute_final_run_overrides (asymmetric)
    """
    if not _bool_env("TRAINING_PROBE_WARMUP_REDUCTION_ENABLED"):
        return run_config

    if not checking_step or not isinstance(checking_step, (int, float)) or checking_step <= 0:
        return run_config  # only probe runs have checking_step

    try:
        ratio = float(os.getenv("TRAINING_PROBE_WARMUP_RATIO", "0.15"))
        floor = int(os.getenv("TRAINING_PROBE_WARMUP_FLOOR", "10"))
    except (TypeError, ValueError):
        return run_config

    new_warmup = max(floor, int(int(checking_step) * ratio))
    cur = int(run_config.get("warmup_steps", 35))

    if new_warmup >= cur:
        return run_config  # don't increase

    run_config["warmup_steps"] = new_warmup
    print(
        f"[hp-override:probe-warmup] checking_step={checking_step} → "
        f"warmup_steps {cur}→{new_warmup} (ratio={ratio:.0%}, floor={floor}); "
        f"effective full-LR probe steps {checking_step-cur}→{checking_step-new_warmup}",
        flush=True,
    )
    return run_config


def _estimate_train_tokens(n_train: int, seq_p95: int, char_per_token: float = 4.0) -> int:
    """Rough token count estimate. seq_p95 already in tokens (post-tokenize),
    so just multiply by sample count."""
    return n_train * seq_p95


def maybe_d2z_scheduler(
    run_config: Dict,
    n_train: int,
    param_count: int,
    seq_p95: int,
    epochs: Optional[int] = None,
) -> Dict:
    """Switch lr_scheduler_type to `linear` (D2Z) when TPP > 1.0 AND epochs >= 2.

    Args:
        run_config: dict with current `lr_scheduler_type` and `lr_scheduler_kwargs`
        n_train: number of training samples
        param_count: total model parameters
        seq_p95: 95th percentile token length per sample
        epochs: training epochs (defaults to run_config["num_train_epochs"] or 3)

    Theory (D2Z paper):
    - cosine_with_min_lr=0.25 = "10% min" decay (weak)
    - Linear decay-to-zero = strictly better at compute-optimal TPP
    - Safe regime: TPP > 1 AND epochs >= 2 (enough data for full decay)
    """
    if not _bool_env("TRAINING_SCHEDULER_D2Z_AUTO"):
        return run_config

    if not n_train or not param_count or not seq_p95:
        return run_config

    try:
        tpp_threshold = float(os.getenv("TRAINING_D2Z_TPP_THRESHOLD", "1.0"))
        epochs_threshold = int(os.getenv("TRAINING_D2Z_MIN_EPOCHS", "2"))
    except (TypeError, ValueError):
        return run_config

    est_tokens = _estimate_train_tokens(n_train, seq_p95)
    tpp = est_tokens / float(param_count)

    if epochs is None:
        epochs = int(run_config.get("num_train_epochs", 3))

    if tpp <= tpp_threshold or epochs < epochs_threshold:
        print(
            f"[hp-override:d2z] no fire: tpp={tpp:.2f}≤{tpp_threshold} "
            f"OR epochs={epochs}<{epochs_threshold} "
            f"(n_train={n_train}, params={param_count/1e9:.2f}B, est_tokens={est_tokens})",
            flush=True,
        )
        return run_config

    # Switch to linear
    cur_sched = run_config.get("lr_scheduler_type", "cosine_with_min_lr")
    run_config["lr_scheduler_type"] = "linear"
    # Clear kwargs (linear doesn't use min_lr_rate)
    run_config["lr_scheduler_kwargs"] = {}

    print(
        f"[hp-override:d2z] fire: tpp={tpp:.2f}>{tpp_threshold} AND "
        f"epochs={epochs}>={epochs_threshold} → scheduler "
        f"{cur_sched}→linear (decay-to-zero); "
        f"(n_train={n_train}, params={param_count/1e9:.2f}B, est_tokens={est_tokens})",
        flush=True,
    )
    return run_config


def apply_all(
    run_config: Dict,
    train_info: Dict,
    n_train: int,
    param_count: int,
    seq_p95: int,
) -> Dict:
    """Apply all HP override patches in sequence. Fail-soft on each.

    Order:
    1. probe_warmup_reduction (modifies warmup_steps if probe phase)
    2. d2z_scheduler (modifies lr_scheduler_type if compute-optimal)

    Args:
        run_config: HP config dict to mutate
        train_info: dict possibly containing 'checking_step' (from state_manager)
        n_train, param_count, seq_p95: dataset + model metrics

    Returns:
        Mutated run_config (chained through all enabled patches)
    """
    checking_step = (
        train_info.get("checking_step")
        or train_info.get("train_request", {}).get("checking_step")
    )
    try:
        run_config = maybe_probe_warmup_reduction(run_config, checking_step)
    except Exception as exc:
        print(f"[hp-override:probe-warmup] error fail-soft: {exc}", flush=True)

    try:
        run_config = maybe_d2z_scheduler(run_config, n_train, param_count, seq_p95)
    except Exception as exc:
        print(f"[hp-override:d2z] error fail-soft: {exc}", flush=True)

    return run_config
