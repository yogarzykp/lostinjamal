"""Decisions derived from the validator's baseline-stats measurements.

The validator's model-prep container profiles the base model and the dataset
before our container starts and hands us the result (BASELINE_STATS_PATH). Most
of that measurement went unused: we consumed `init_loss` and two beta
suggestions and ignored the rest, while making the same decisions from
heuristics and model config.

This module is the seam where those measurements turn into decisions. It exists
as its own file for three reasons: every function here is a pure
(stats, current_value) -> (new_value, reason) mapping that can be unit-tested
without a GPU, the call sites in adaptive_config stay one-liners, and it keeps
new logic out of the code paths that are still awaiting their first real run.

Rules every function here follows:

* Absent, malformed, or implausible input returns the caller's current value
  unchanged, with a reason string saying why. A missing baseline must produce a
  configuration byte-identical to the one we ship today — that is asserted in
  tests/test_baseline_signals.py, and it is what makes it safe to add these
  while the rest of the queue is still unverified.
* Every function returns a reason, and callers log it. A decision we cannot
  explain afterwards is a decision we cannot debug from a tournament log.
* Each is individually switchable via an env var, default ON. The switches exist
  so a first GPU session can bisect by turning features off one at a time; they
  are not feature flags to ship disabled.
"""

import math
import os

# Env switches. Default ON — set to "0" to disable one.
ENV_COMPLETION_LOSS = "BASELINE_USE_COMPLETION_LOSS"
ENV_SEQLEN = "BASELINE_USE_SEQLEN"
ENV_NEARDUP = "BASELINE_USE_NEARDUP"
ENV_DPO_GAP = "BASELINE_USE_DPO_GAP"

# A cross-entropy that is not in this range is not a loss we can reason about:
# below it the number is almost certainly not a loss at all, above it the model
# is not meaningfully evaluating the data. Either way, don't plan a run on it.
LOSS_PLAUSIBLE_MIN = 0.05
LOSS_PLAUSIBLE_MAX = 15.0


def _enabled(env_var: str) -> bool:
    return os.getenv(env_var, "1") == "1"


def _is_plausible_loss(value) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    v = float(value)
    if math.isnan(v) or math.isinf(v):
        return False
    return LOSS_PLAUSIBLE_MIN <= v <= LOSS_PLAUSIBLE_MAX


def resolve_epoch_loss_signal(baseline_stats, task_type: str, fallback: float):
    """Which measured loss should drive the epoch count.

    Returns (value, source).

    Epoch count is chosen from how far the base model is from the task: a low
    starting loss means little left to learn, a high one means more passes are
    worth it. We fed that decision `init_loss`, which the validator computes over
    whole sequences — prompt tokens included.

    But instruct training masks the prompt: we only ever compute loss on
    completion tokens, and the validator scores us on a completion-masked metric
    too. `masked_completion_loss` is that same quantity measured on the same
    data, so for instruct it is a strictly better-matched input to an unchanged
    heuristic. On a dataset with long prompts and short answers the two can
    differ enough to move the epoch count by a whole step.

    Only instruct publishes this field; DPO and GRPO keep `init_loss`.
    """
    if not _enabled(ENV_COMPLETION_LOSS):
        return fallback, f"{ENV_COMPLETION_LOSS}=0"

    if baseline_stats is None:
        return fallback, "no baseline stats"

    try:
        from baseline_stats_reader import get_masked_completion_loss
    except Exception as exc:
        return fallback, f"reader unavailable ({type(exc).__name__})"

    if (task_type or "").lower().startswith("instruct"):
        completion = get_masked_completion_loss(baseline_stats)
        if _is_plausible_loss(completion):
            return float(completion), "masked_completion_loss"
        if completion is not None:
            # Present but unusable — say so rather than silently falling through,
            # because a nonsense value here means the schema moved.
            return _init_loss_or(baseline_stats, fallback, note=f"completion_loss implausible ({completion})")

    return _init_loss_or(baseline_stats, fallback)


def _init_loss_or(baseline_stats, fallback: float, note: str = ""):
    from baseline_stats_reader import get_init_loss

    init = get_init_loss(baseline_stats)
    prefix = f"{note}; " if note else ""
    if _is_plausible_loss(init):
        return float(init), f"{prefix}init_loss"
    if init is not None:
        return fallback, f"{prefix}init_loss implausible ({init})"
    return fallback, f"{prefix}no measured loss"


# Our own p95 comes from a 500-record sample; if it sits below the validator's
# full-dataset p95 by more than this, the sample missed the tail.
SEQ_LEN_UNDERESTIMATE_RATIO = 1.15

# Beyond this the two numbers are not describing the same thing (different
# tokenizer, different prompt formatting, or a schema change) and neither should
# override the other.
SEQ_LEN_DISAGREEMENT_RATIO = 4.0


def correct_seq_len_p95(baseline_stats, measured_p95: int):
    """Raise a sampled sequence-length p95 when the validator's full-dataset one is higher.

    Returns (p95, reason).

    We estimate p95 by tokenizing 500 records (dynamics_utils.measure_dataset).
    The validator's model-prep tokenizes the whole dataset and publishes
    `dataset.seq_length_distribution`. On a dataset whose long examples are rare
    or clustered late, a 500-record sample under-reports the tail — and p95 sets
    max_length, so under-reporting it silently truncates real training data. That
    loss is irreversible; excess context merely costs some compute, which the
    existing batch-vs-max_length scaling already absorbs.

    So the correction is deliberately ONE-DIRECTIONAL: the validator's number can
    raise ours, never lower it. Asymmetric because the two errors are asymmetric.

    Guard for the case where the numbers disagree wildly: the validator measured
    the raw dataset with its own tokenizer while we measure our formatted,
    templated text, so a moderate offset is expected and a large one means they
    are not describing the same quantity. Past SEQ_LEN_DISAGREEMENT_RATIO we keep
    our own measurement, which is at least on the text we will actually train on.
    """
    if not _enabled(ENV_SEQLEN):
        return measured_p95, f"{ENV_SEQLEN}=0"
    if not isinstance(measured_p95, int) or measured_p95 <= 0:
        return measured_p95, "no local measurement"

    try:
        from baseline_stats_reader import get_seq_len_p95
    except Exception as exc:
        return measured_p95, f"reader unavailable ({type(exc).__name__})"

    prep_p95 = get_seq_len_p95(baseline_stats)
    if not isinstance(prep_p95, int) or prep_p95 <= 0:
        return measured_p95, "no validator seq_length_distribution"

    ratio = prep_p95 / measured_p95
    if ratio > SEQ_LEN_DISAGREEMENT_RATIO or ratio < (1.0 / SEQ_LEN_DISAGREEMENT_RATIO):
        return measured_p95, (
            f"validator p95={prep_p95} disagrees with measured {measured_p95} "
            f"({ratio:.1f}x) — keeping measured"
        )

    if ratio >= SEQ_LEN_UNDERESTIMATE_RATIO:
        return prep_p95, f"raised {measured_p95}->{prep_p95} from validator full-dataset p95"

    return measured_p95, f"measured p95 adequate (validator {prep_p95}, {ratio:.2f}x)"
