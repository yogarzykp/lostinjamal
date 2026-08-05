"""Read validator-provided baseline_stats from BASELINE_STATS_PATH env var.

The validator's model-prep container profiles the base model and the dataset
BEFORE our training container starts, writes the result to the shared cache
volume, and hands us the path (G.O.D trainer/runtime.py: writes
`baseline_stats_{task_id}.json`, sets BASELINE_STATS_PATH). This is free
measurement on the exact GPU we are about to train on.

AUTHORITATIVE SCHEMA — G.O.D core/models/model_prep_models.py, verified
2026-08-05. Discriminated union on task_type: instruct | dpo | grpo | env.

  dataset:
    total_tokens, num_records, near_duplicate_rate, bits_per_byte,
    vocab_size, unique_tokens_in_data, vocab_coverage_ratio,
    seq_length_distribution {mean, p50, p95, p99, max}
    instruct: prompt_tokens, completion_tokens, completion_length_distribution
    dpo:      prompt_tokens, chosen_tokens, rejected_tokens,
              chosen_length_distribution, rejected_length_distribution,
              chosen_rejected_length_ratio
    grpo:     prompt_tokens, prompt_length_distribution
  weights:
    by_group: {group_name: {weight_rms, weight_norm, max_abs}}
  training:
    init_loss, init_loss_std, activation_rms {layer: rms},
    output_entropy, output_entropy_std
    instruct: masked_completion_loss
    dpo:      ref_log_prob_chosen, ref_log_prob_rejected, implicit_reward_gap
    grpo:     baseline_reward_scores {func_name: score}
  throughput (optional):
    tokens_per_sec, seq_len, micro_batch_size, n_gpus, gpu_name

CORRECTION 2026-08-05: an earlier version of this docstring described
`grad_norms` and `gradient_noise_scale`. NEITHER EXISTS — grepping the whole
G.O.D repository returns zero occurrences of `gradient_noise_scale`, and
`grad_norms` is absent from the schema. That description came from a port of a
different codebase and was never reconciled. The accessor that read
`training.grad_norms` always returned None and has been removed. Do not plan
against fields without checking model_prep_models.py first.

Fail-soft: returns None on any error (legacy task without baseline, missing
file, parse error). Consumers MUST handle None gracefully.
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


def suggest_dpo_beta_from_baseline(
    baseline_stats: Optional[dict],
    current_beta: float = 0.10,
) -> Optional[tuple]:
    """Tune DPO β from validator's implicit_reward_gap (Sprint 1 P0b equivalent).

    Source: hyper-text/scripts/hp_override.py:_maybe_baseline_dpo_beta_tune.

    Hypothesis: gap = |ref_log_prob_chosen - ref_log_prob_rejected| measures
    how opinionated the reference model is about the preference. Large gap
    means ref already aligned → high β (constrain policy from diverging).
    Small gap means ref is weak → low β (allow policy to learn freely).

    Calibration (TRL default β=0.1):
      gap < 0.5         → β = 0.05  (ref weak, allow strong moves)
      gap in [0.5, 2.0] → β = 0.10  (default — no change)
      gap > 2.0         → β = 0.15  (ref strong, constrain)

    Returns (new_beta, reason_str) or None when no override applies.
    """
    if not isinstance(baseline_stats, dict):
        return None
    if baseline_stats.get("task_type", "").lower() != "dpotask":
        return None
    training = baseline_stats.get("training") or {}
    gap = training.get("implicit_reward_gap")
    if gap is None or not isinstance(gap, (int, float)):
        return None

    abs_gap = abs(float(gap))
    if abs_gap < 0.5:
        new_beta, bucket = 0.05, "low-gap"
    elif abs_gap > 2.0:
        new_beta, bucket = 0.15, "high-gap"
    else:
        new_beta, bucket = 0.10, "normal-gap"

    if abs(new_beta - current_beta) < 1e-6:
        return None
    return (new_beta, f"gap={abs_gap:.3f} {bucket} → β={new_beta:.3f}")


def suggest_grpo_beta_from_baseline(
    baseline_stats: Optional[dict],
    current_beta: float = 0.04,
) -> Optional[tuple]:
    """Tune GRPO β from validator's baseline_reward_scores (Sprint 1 P0c equivalent).

    Source: hyper-text/scripts/hp_override.py:_maybe_baseline_grpo_beta_tune.

    Hypothesis: baseline_reward_scores dict reveals reward landscape:
      - high mean + low variance → strong signal, easy task → β higher (prevent over-optim)
      - low mean + high variance → noisy, hard task → β lower (allow exploration)
      - mid → keep current

    Calibration (heuristic from hyper-text):
      mean >= 5.0 and stdev/mean < 0.5 → β = 0.10 (strong+stable)
      mean < 1.0                       → β = 0.04 (weak signal, more exploration)
      else                             → None (no override)

    Returns:
      (new_beta, reason_str) — apply this
      None — no override / no baseline data / not applicable

    Args:
      baseline_stats: parsed validator JSON
      current_beta: current β (returned as new_beta if no override applies)
    """
    if not isinstance(baseline_stats, dict):
        return None
    if baseline_stats.get("task_type", "").lower() != "grpotask":
        return None
    training = baseline_stats.get("training") or {}
    rewards = training.get("baseline_reward_scores")
    if not isinstance(rewards, dict) or not rewards:
        return None

    vals = [float(v) for v in rewards.values() if isinstance(v, (int, float))]
    if not vals:
        return None

    mean_r = sum(vals) / len(vals)
    var = sum((v - mean_r) ** 2 for v in vals) / max(1, len(vals))
    std_r = var ** 0.5
    cv = std_r / abs(mean_r) if abs(mean_r) > 1e-6 else float("inf")

    new_beta = None
    reason = ""
    if mean_r >= 5.0 and cv < 0.5:
        new_beta = 0.10
        reason = f"strong+stable (mean={mean_r:.3f}, cv={cv:.3f}) → β=0.10"
    elif mean_r < 1.0:
        new_beta = 0.04
        reason = f"weak+noisy (mean={mean_r:.3f}, cv={cv:.3f}) → β=0.04"

    if new_beta is None or abs(new_beta - current_beta) < 1e-6:
        return None
    return (new_beta, reason)


def get_init_loss_std(baseline_stats: Optional[dict]) -> Optional[float]:
    """training.init_loss_std — spread of the pre-training loss probe.

    A large spread relative to init_loss means the base model's loss varies a lot
    across the dev batch, i.e. the task is heterogeneous. Useful as a confidence
    term: noisy evidence should move a learning-rate prior less than clean
    evidence does.
    """
    return _training_float(baseline_stats, "init_loss_std")


def get_output_entropy(baseline_stats: Optional[dict]) -> Optional[float]:
    """training.output_entropy — base model's predictive entropy before training.

    High entropy means the base model is unsure on this data (far from the task),
    low entropy means it is already confident (close to the task).
    """
    return _training_float(baseline_stats, "output_entropy")


def get_masked_completion_loss(baseline_stats: Optional[dict]) -> Optional[float]:
    """training.masked_completion_loss — instruct only.

    Loss over completion tokens alone, which is closer to what we actually train
    on than the whole-sequence init_loss.
    """
    return _training_float(baseline_stats, "masked_completion_loss")


def _training_float(baseline_stats: Optional[dict], key: str) -> Optional[float]:
    if not isinstance(baseline_stats, dict):
        return None
    training = baseline_stats.get("training")
    if not isinstance(training, dict):
        return None
    v = training.get(key)
    return float(v) if isinstance(v, (int, float)) else None


def get_weight_rms(baseline_stats: Optional[dict]) -> Optional[float]:
    """Aggregate weight RMS across layer groups (weights.by_group[*].weight_rms).

    Combined in quadrature — RMS values are root-mean-squares, so the correct
    aggregate of several groups is sqrt(mean(rms^2)), not the arithmetic mean.

    Weight scale sets how large a parameter update of a given learning rate is
    in relative terms, which is why it belongs in a learning-rate estimate at
    all. Returns None when the block is absent.
    """
    if not isinstance(baseline_stats, dict):
        return None
    weights = baseline_stats.get("weights")
    if not isinstance(weights, dict):
        return None
    by_group = weights.get("by_group")
    if not isinstance(by_group, dict) or not by_group:
        return None
    squares = []
    for group in by_group.values():
        if isinstance(group, dict):
            rms = group.get("weight_rms")
            if isinstance(rms, (int, float)) and rms > 0:
                squares.append(float(rms) ** 2)
    if not squares:
        return None
    return (sum(squares) / len(squares)) ** 0.5


def get_throughput(baseline_stats: Optional[dict]) -> Optional[dict]:
    """throughput block — measured fwd+bwd speed on the actual training GPU.

    The validator's prep container times a real forward+backward pass before our
    container starts and hands us the result. Returns a dict with:
        tokens_per_sec (float), seq_len (int), micro_batch_size (int),
        n_gpus (int), gpu_name (str)

    This is worth more than it looks: it is a measured throughput number for
    this model on this hardware, available before step 0 and costing us none of
    the training budget. The block is optional in the schema, so None is normal
    on older tasks.
    """
    if not isinstance(baseline_stats, dict):
        return None
    tp = baseline_stats.get("throughput")
    if not isinstance(tp, dict):
        return None
    tps = tp.get("tokens_per_sec")
    if not isinstance(tps, (int, float)) or tps <= 0:
        return None
    return {
        "tokens_per_sec": float(tps),
        "seq_len": int(tp.get("seq_len") or 0),
        "micro_batch_size": int(tp.get("micro_batch_size") or 0),
        "n_gpus": int(tp.get("n_gpus") or 0),
        "gpu_name": str(tp.get("gpu_name") or ""),
    }


def get_dataset_stat(baseline_stats: Optional[dict], key: str) -> Optional[Any]:
    """Any field under the dataset block (total_tokens, num_records, vocab_coverage_ratio, ...)."""
    if not isinstance(baseline_stats, dict):
        return None
    dataset = baseline_stats.get("dataset")
    if not isinstance(dataset, dict):
        return None
    return dataset.get(key)


def get_seq_len_p95(baseline_stats: Optional[dict]) -> Optional[int]:
    """dataset.seq_length_distribution.p95 — measured by the validator on the real dataset."""
    dist = get_dataset_stat(baseline_stats, "seq_length_distribution")
    if isinstance(dist, dict):
        v = dist.get("p95")
        if isinstance(v, (int, float)):
            return int(v)
    return None


if __name__ == "__main__":
    # Smoke test (manual)
    import sys
    if len(sys.argv) > 1:
        os.environ["BASELINE_STATS_PATH"] = sys.argv[1]
    result = maybe_read_baseline_stats()
    print(f"Loaded: {result is not None}")
    if result:
        print(f"  init_loss:        {get_init_loss(result)}")
        print(f"  init_loss_std:    {get_init_loss_std(result)}")
        print(f"  output_entropy:   {get_output_entropy(result)}")
        print(f"  weight_rms (agg): {get_weight_rms(result)}")
        print(f"  throughput:       {get_throughput(result)}")
        print(f"  seq_len_p95:      {get_seq_len_p95(result)}")
        print(f"  total_tokens:     {get_dataset_stat(result, 'total_tokens')}")
        print(f"  grpo_reward:      {get_grpo_baseline_reward(result)}")
