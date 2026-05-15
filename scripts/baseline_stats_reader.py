"""Read validator-provided baseline_stats from BASELINE_STATS_PATH env var.

Ported 2026-05-15 from hyper-text/scripts/baseline_stats_reader.py (minimal core).

Validator's model-prep container (G.O.D commit a7ee3686, feature/model-prep-container
merged via PR #1096) computes pre-training stats:
  - init_loss (forward pass on dev split with untrained adapter)
  - grad_norms (one backward pass, p50/p95/max distribution)
  - gradient_noise_scale (McCandlish 2018 estimator)
  - activation_rms (per-layer)
  - dataset distributions (seq_length, near_dup, vocab_coverage, bits_per_byte)
  - weight_stats (max_abs_ratio, rms by group)
  - DPO-specific: ref_log_probs distribution
  - GRPO-specific: baseline_reward_scores (untrained-model rewards)

Path passed to miner container via BASELINE_STATS_PATH env var.
Schema: G.O.D/core/models/model_prep_models.py (discriminated union by task_type).

Fail-soft: returns None on any error (legacy task without baseline, missing file,
parse error). Consumers MUST handle None gracefully.

Use cases in adaptive_config (current):
  - init_loss → drives adaptive_epochs_from_init_loss (replaces 2.5 placeholder)
  - grad_norms p95 → max_grad_norm calibration (future hook)
  - GRPO baseline_reward_scores → β tuning (future hook)
"""

from __future__ import annotations

import json
import os
from typing import Any, Optional


def maybe_read_baseline_stats(
    env_var: str = "BASELINE_STATS_PATH",
) -> Optional[dict]:
    """Read validator baseline_stats JSON (if present).

    Returns:
        dict — parsed JSON content (discriminated by task_type field).
        None — env var unset, file missing, or parse error.

    Never raises. Logs reason on failure.
    """
    path = os.environ.get(env_var)
    if not path:
        return None
    if not os.path.isfile(path):
        print(
            f"[baseline-stats] env {env_var}={path} but file missing — skip",
            flush=True,
        )
        return None
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except Exception as exc:
        print(
            f"[baseline-stats] read fail (skip): {type(exc).__name__}: {exc}",
            flush=True,
        )
        return None

    if not isinstance(data, dict):
        print(
            f"[baseline-stats] expected dict, got {type(data).__name__} — skip",
            flush=True,
        )
        return None

    task_type = data.get("task_type", "?")
    print(
        f"[baseline-stats] loaded: task_type={task_type}, "
        f"top_keys={sorted(data.keys())}",
        flush=True,
    )
    return data


def get_init_loss(baseline_stats: Optional[dict]) -> Optional[float]:
    """Extract init_loss from validator baseline_stats.

    Schema variants observed (G.O.D model_prep_models.py):
      - Top-level: baseline_stats["init_loss"]
      - Under "training": baseline_stats["training"]["init_loss"]

    Returns None if missing/invalid. Caller falls back to ADAPTIVE_INIT_LOSS_OVERRIDE
    or default placeholder.
    """
    if not isinstance(baseline_stats, dict):
        return None
    # Try top-level first
    v = baseline_stats.get("init_loss")
    if isinstance(v, (int, float)):
        return float(v)
    # Try under "training" sub-key
    training = baseline_stats.get("training")
    if isinstance(training, dict):
        v = training.get("init_loss")
        if isinstance(v, (int, float)):
            return float(v)
    return None


def get_grad_norms_p95(baseline_stats: Optional[dict]) -> Optional[float]:
    """Extract grad_norms p95 from validator baseline_stats.

    Use case: tighten max_grad_norm when validator observed outlier grads
    (replaces our static weight-ratio outlier heuristic).

    Returns None if not present.
    """
    if not isinstance(baseline_stats, dict):
        return None
    training = baseline_stats.get("training") or {}
    gn = training.get("grad_norms")
    if not isinstance(gn, dict):
        return None
    # Schema may give {"p50": ..., "p95": ..., "max": ...} OR raw per-layer dict
    p95 = gn.get("p95")
    if isinstance(p95, (int, float)):
        return float(p95)
    # Fall back: compute from per-layer values if available
    if all(isinstance(v, (int, float)) for v in gn.values()):
        vals = sorted(float(v) for v in gn.values())
        if vals:
            idx = max(0, int(len(vals) * 0.95) - 1)
            return float(vals[idx])
    return None


def get_grpo_baseline_reward(baseline_stats: Optional[dict]) -> Optional[dict]:
    """Extract GRPO baseline_reward_scores from validator baseline_stats.

    Returns dict with reward statistics (mean, std, min, max) or None.
    Used for: GRPO β tuning when reward classifier doesn't hit.
    """
    if not isinstance(baseline_stats, dict):
        return None
    if baseline_stats.get("task_type", "").lower() != "grpotask":
        return None
    brs = baseline_stats.get("baseline_reward_scores")
    if isinstance(brs, dict):
        return brs
    return None


if __name__ == "__main__":
    # Smoke test (manual)
    import sys
    if len(sys.argv) > 1:
        os.environ["BASELINE_STATS_PATH"] = sys.argv[1]
    result = maybe_read_baseline_stats()
    print(f"Loaded: {result is not None}")
    if result:
        print(f"  init_loss: {get_init_loss(result)}")
        print(f"  grad_norms_p95: {get_grad_norms_p95(result)}")
        print(f"  grpo_reward: {get_grpo_baseline_reward(result)}")
