"""Tests for decisions derived from validator baseline stats.

The load-bearing tests here are the invariance ones. Everything in
baseline_signals runs inside the config builder that produces every training
run, and it was written before any of it could be exercised on a GPU. The
guarantee that makes that acceptable is narrow and absolute: when the baseline
payload is absent, empty, malformed, or partial, every function must return the
caller's current value UNCHANGED — not a close value, the same object value. If
that holds, adding these cannot perturb a run that would otherwise have worked,
and a first GPU session can attribute any failure to something else.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from baseline_signals import (  # noqa: E402
    ENV_COMPLETION_LOSS,
    LOSS_PLAUSIBLE_MAX,
    LOSS_PLAUSIBLE_MIN,
    resolve_epoch_loss_signal,
)


FALLBACK = 2.5  # the placeholder adaptive_config uses when nothing is measured


def _stats(*, init_loss=None, completion=None, task_type="instruct"):
    training = {}
    if init_loss is not None:
        training["init_loss"] = init_loss
    if completion is not None:
        training["masked_completion_loss"] = completion
    return {"task_type": task_type, "training": training}


# --------------------------------------------------------------------------
# Invariance — the guarantee that makes blind-built code safe to ship
# --------------------------------------------------------------------------

BROKEN_PAYLOADS = [
    pytest.param(None, id="absent"),
    pytest.param({}, id="empty-dict"),
    pytest.param({"task_type": "instruct"}, id="no-training-block"),
    pytest.param({"training": None}, id="training-is-none"),
    pytest.param({"training": {}}, id="training-empty"),
    pytest.param({"training": []}, id="training-wrong-type"),
    pytest.param({"training": {"init_loss": None}}, id="init-loss-none"),
    pytest.param({"training": {"init_loss": "2.4"}}, id="init-loss-string"),
    pytest.param({"training": {"init_loss": float("nan")}}, id="init-loss-nan"),
    pytest.param({"training": {"init_loss": float("inf")}}, id="init-loss-inf"),
    pytest.param({"training": {"init_loss": -1.0}}, id="init-loss-negative"),
    pytest.param({"training": {"init_loss": 0.0}}, id="init-loss-zero"),
    pytest.param({"training": {"init_loss": 1e9}}, id="init-loss-absurd"),
    pytest.param({"training": {"masked_completion_loss": float("nan")}}, id="completion-nan"),
    pytest.param({"training": {"masked_completion_loss": True}}, id="completion-bool"),
    pytest.param("not a dict", id="payload-is-string"),
    pytest.param(42, id="payload-is-int"),
]


@pytest.mark.parametrize("payload", BROKEN_PAYLOADS)
def test_broken_payload_returns_fallback_exactly(payload):
    value, reason = resolve_epoch_loss_signal(payload, "instruct", FALLBACK)
    assert value == FALLBACK
    assert isinstance(reason, str) and reason, "every decision must carry a reason"


@pytest.mark.parametrize("payload", BROKEN_PAYLOADS)
@pytest.mark.parametrize("task_type", ["instruct", "dpo", "grpo", "chat", "", None])
def test_invariance_holds_for_every_task_type(payload, task_type):
    value, _ = resolve_epoch_loss_signal(payload, task_type, FALLBACK)
    assert value == FALLBACK


def test_disabled_switch_returns_fallback_even_with_good_data(monkeypatch):
    """The bisect switch must fully bypass the feature, not partially."""
    monkeypatch.setenv(ENV_COMPLETION_LOSS, "0")
    value, reason = resolve_epoch_loss_signal(
        _stats(init_loss=4.0, completion=3.2), "instruct", FALLBACK
    )
    assert value == FALLBACK
    assert ENV_COMPLETION_LOSS in reason


# --------------------------------------------------------------------------
# The substitution itself
# --------------------------------------------------------------------------

def test_instruct_prefers_masked_completion_loss():
    value, reason = resolve_epoch_loss_signal(
        _stats(init_loss=4.0, completion=2.2), "instruct", FALLBACK
    )
    assert value == pytest.approx(2.2)
    assert reason == "masked_completion_loss"


def test_instruct_falls_back_to_init_loss_when_completion_absent():
    value, reason = resolve_epoch_loss_signal(_stats(init_loss=4.0), "instruct", FALLBACK)
    assert value == pytest.approx(4.0)
    assert reason == "init_loss"


@pytest.mark.parametrize("task_type", ["dpo", "grpo", "DpoTask", "GrpoTask"])
def test_non_instruct_keeps_init_loss_even_if_completion_present(task_type):
    """Only instruct publishes masked_completion_loss; using it elsewhere would be
    reading a field that is not part of that task type's schema."""
    value, reason = resolve_epoch_loss_signal(
        _stats(init_loss=4.0, completion=2.2), task_type, FALLBACK
    )
    assert value == pytest.approx(4.0)
    assert reason == "init_loss"


@pytest.mark.parametrize("task_type", ["instruct", "InstructTextTask", "INSTRUCT"])
def test_task_type_matching_is_case_insensitive(task_type):
    value, _ = resolve_epoch_loss_signal(_stats(completion=1.5), task_type, FALLBACK)
    assert value == pytest.approx(1.5)


def test_implausible_completion_falls_through_to_init_loss_and_says_so():
    value, reason = resolve_epoch_loss_signal(
        _stats(init_loss=3.1, completion=900.0), "instruct", FALLBACK
    )
    assert value == pytest.approx(3.1)
    assert "implausible" in reason and "init_loss" in reason


def test_both_implausible_returns_fallback():
    value, reason = resolve_epoch_loss_signal(
        _stats(init_loss=1e6, completion=1e6), "instruct", FALLBACK
    )
    assert value == FALLBACK
    assert "implausible" in reason


@pytest.mark.parametrize("value", [LOSS_PLAUSIBLE_MIN, 1.0, 2.5, 7.0, LOSS_PLAUSIBLE_MAX])
def test_boundary_values_are_accepted(value):
    got, reason = resolve_epoch_loss_signal(_stats(completion=value), "instruct", FALLBACK)
    assert got == pytest.approx(value)
    assert reason == "masked_completion_loss"


@pytest.mark.parametrize(
    "value", [LOSS_PLAUSIBLE_MIN - 1e-6, LOSS_PLAUSIBLE_MAX + 1e-6, -0.5, 0.0]
)
def test_values_outside_the_band_are_rejected(value):
    got, _ = resolve_epoch_loss_signal(_stats(completion=value), "instruct", FALLBACK)
    assert got == FALLBACK


# --------------------------------------------------------------------------
# Does the substitution actually change anything? (sizing check)
# --------------------------------------------------------------------------

def test_substitution_can_move_the_epoch_count():
    """If this could never change a decision it would not be worth the risk.

    A long-prompt/short-answer dataset is exactly where whole-sequence init_loss
    and completion-only loss diverge: the prompt tokens are easy and drag the
    average down, so init_loss understates how much is left to learn on the part
    we actually train.

    The epoch rule is inlined rather than imported: dynamics_utils pulls in
    transformers, and this stays a dependency-free unit test. Mirrors
    scripts/dynamics_utils.py::adaptive_epochs_from_init_loss (thresholds 1.0/3.0).
    """

    def epochs_from_loss(loss):
        if loss < 1.0:
            return 1
        if loss < 3.0:
            return 2
        return 3

    stats = _stats(init_loss=2.8, completion=3.4)

    with_init, _ = resolve_epoch_loss_signal(
        {"task_type": "dpo", "training": stats["training"]}, "dpo", FALLBACK
    )
    with_completion, _ = resolve_epoch_loss_signal(stats, "instruct", FALLBACK)

    assert with_init == pytest.approx(2.8)
    assert with_completion == pytest.approx(3.4)
    assert epochs_from_loss(with_completion) > epochs_from_loss(with_init), (
        "expected the completion-masked signal to buy an extra epoch on this shape"
    )


# --------------------------------------------------------------------------
# Item 1 — sequence-length p95 correction
# --------------------------------------------------------------------------

from baseline_signals import (  # noqa: E402
    ENV_SEQLEN,
    SEQ_LEN_DISAGREEMENT_RATIO,
    SEQ_LEN_UNDERESTIMATE_RATIO,
    correct_seq_len_p95,
)


def _seq_stats(p95):
    return {"dataset": {"seq_length_distribution": {"mean": 1.0, "p50": 1, "p95": p95, "p99": 1, "max": 1}}}


SEQ_BROKEN = [
    pytest.param(None, id="absent"),
    pytest.param({}, id="empty"),
    pytest.param({"dataset": None}, id="dataset-none"),
    pytest.param({"dataset": {}}, id="dataset-empty"),
    pytest.param({"dataset": {"seq_length_distribution": None}}, id="dist-none"),
    pytest.param({"dataset": {"seq_length_distribution": {}}}, id="dist-empty"),
    pytest.param({"dataset": {"seq_length_distribution": {"p95": None}}}, id="p95-none"),
    pytest.param({"dataset": {"seq_length_distribution": {"p95": "900"}}}, id="p95-string"),
    pytest.param({"dataset": {"seq_length_distribution": {"p95": 0}}}, id="p95-zero"),
    pytest.param({"dataset": {"seq_length_distribution": {"p95": -5}}}, id="p95-negative"),
    pytest.param("nope", id="payload-string"),
]


@pytest.mark.parametrize("payload", SEQ_BROKEN)
def test_seqlen_broken_payload_keeps_measured_exactly(payload):
    got, reason = correct_seq_len_p95(payload, 900)
    assert got == 900
    assert isinstance(reason, str) and reason


def test_seqlen_switch_off_keeps_measured(monkeypatch):
    monkeypatch.setenv(ENV_SEQLEN, "0")
    got, reason = correct_seq_len_p95(_seq_stats(4000), 900)
    assert got == 900
    assert ENV_SEQLEN in reason


def test_raises_when_sample_under_reported_the_tail():
    """The failure this exists to prevent: a 500-record sample missing long examples."""
    got, reason = correct_seq_len_p95(_seq_stats(1800), 900)
    assert got == 1800
    assert "raised" in reason


def test_never_lowers_a_measured_p95():
    """One-directional by design: truncating real data is irreversible, extra context is not."""
    got, reason = correct_seq_len_p95(_seq_stats(400), 900)
    assert got == 900, "validator p95 must never pull our max_length down"


def test_small_disagreement_keeps_measured():
    got, _ = correct_seq_len_p95(_seq_stats(int(900 * (SEQ_LEN_UNDERESTIMATE_RATIO - 0.05))), 900)
    assert got == 900


def test_wild_disagreement_is_rejected_in_both_directions():
    high = int(900 * SEQ_LEN_DISAGREEMENT_RATIO * 1.5)
    low = int(900 / (SEQ_LEN_DISAGREEMENT_RATIO * 1.5))
    for prep in (high, low):
        got, reason = correct_seq_len_p95(_seq_stats(prep), 900)
        assert got == 900
        assert "disagrees" in reason


@pytest.mark.parametrize("measured", [0, -1, None, "900", 1.5])
def test_bad_local_measurement_is_returned_untouched(measured):
    got, _ = correct_seq_len_p95(_seq_stats(1800), measured)
    assert got == measured


# --------------------------------------------------------------------------
# Item 4 — near_duplicate_rate
# --------------------------------------------------------------------------

from baseline_signals import (  # noqa: E402
    ENV_NEARDUP,
    NEAR_DUP_SKIP_BELOW,
    dedup_crosscheck,
    should_skip_dedup,
)


def _dup_stats(rate):
    return {"dataset": {"near_duplicate_rate": rate}}


DUP_BROKEN = [
    pytest.param(None, id="absent"),
    pytest.param({}, id="empty"),
    pytest.param({"dataset": None}, id="dataset-none"),
    pytest.param({"dataset": {}}, id="dataset-empty"),
    pytest.param(_dup_stats(None), id="rate-none"),
    pytest.param(_dup_stats("0.0"), id="rate-string"),
    pytest.param(_dup_stats(True), id="rate-bool"),
    pytest.param(_dup_stats(float("nan")), id="rate-nan"),
    pytest.param(_dup_stats(-0.1), id="rate-negative"),
    pytest.param(_dup_stats(1.5), id="rate-above-one"),
    pytest.param("nope", id="payload-string"),
]


@pytest.mark.parametrize("payload", DUP_BROKEN)
def test_broken_payload_never_skips_dedup(payload):
    """Default must be to RUN dedup. Skipping on bad data would leave duplicates
    in the dev split that every selection decision reads."""
    skip, reason = should_skip_dedup(payload)
    assert skip is False
    assert isinstance(reason, str) and reason


def test_dedup_switch_off_never_skips(monkeypatch):
    monkeypatch.setenv(ENV_NEARDUP, "0")
    skip, reason = should_skip_dedup(_dup_stats(0.0))
    assert skip is False
    assert ENV_NEARDUP in reason


def test_skips_only_when_validator_saw_essentially_none():
    assert should_skip_dedup(_dup_stats(0.0))[0] is True
    assert should_skip_dedup(_dup_stats(NEAR_DUP_SKIP_BELOW / 2))[0] is True


@pytest.mark.parametrize("rate", [NEAR_DUP_SKIP_BELOW, 0.01, 0.08, 0.59, 1.0])
def test_runs_dedup_at_or_above_threshold(rate):
    skip, reason = should_skip_dedup(_dup_stats(rate))
    assert skip is False
    assert "running dedup" in reason


def test_crosscheck_returns_none_without_data():
    assert dedup_crosscheck(None, 10, 100) is None
    assert dedup_crosscheck(_dup_stats(0.1), 10, 0) is None


def test_crosscheck_flags_us_removing_far_more_than_validator_saw():
    line = dedup_crosscheck(_dup_stats(0.02), removed=400, total=1000)
    assert "WARNING" in line


def test_crosscheck_notes_near_dups_our_exact_pass_leaves():
    line = dedup_crosscheck(_dup_stats(0.60), removed=10, total=1000)
    assert "near-duplicates" in line


def test_crosscheck_is_quiet_when_the_two_agree():
    line = dedup_crosscheck(_dup_stats(0.12), removed=80, total=1000)
    assert "WARNING" not in line and "note:" not in line


# --------------------------------------------------------------------------
# Item 2 — DPO implicit_reward_gap (guard-only)
# --------------------------------------------------------------------------

from baseline_signals import DPO_GAP_WIDE, ENV_DPO_GAP, dpo_epoch_guard  # noqa: E402


def _gap_stats(gap):
    return {"task_type": "dpo", "training": {"implicit_reward_gap": gap}}


GAP_BROKEN = [
    pytest.param(None, id="absent"),
    pytest.param({}, id="empty"),
    pytest.param({"training": None}, id="training-none"),
    pytest.param({"training": {}}, id="training-empty"),
    pytest.param(_gap_stats(None), id="gap-none"),
    pytest.param(_gap_stats("2.5"), id="gap-string"),
    pytest.param(_gap_stats(True), id="gap-bool"),
    pytest.param(_gap_stats(float("nan")), id="gap-nan"),
    pytest.param(_gap_stats(float("inf")), id="gap-inf"),
    pytest.param("nope", id="payload-string"),
]


@pytest.mark.parametrize("payload", GAP_BROKEN)
def test_broken_payload_leaves_epochs_untouched(payload):
    got, reason = dpo_epoch_guard(payload, 3)
    assert got == 3
    assert isinstance(reason, str) and reason


def test_gap_switch_off_leaves_epochs_untouched(monkeypatch):
    monkeypatch.setenv(ENV_DPO_GAP, "0")
    got, reason = dpo_epoch_guard(_gap_stats(9.0), 3)
    assert got == 3
    assert ENV_DPO_GAP in reason


def test_wide_gap_caps_epochs_by_one():
    got, reason = dpo_epoch_guard(_gap_stats(DPO_GAP_WIDE + 0.5), 3)
    assert got == 2
    assert "capping" in reason


def test_wide_negative_gap_also_caps():
    """The magnitude is what matters — sign only says which side the ref prefers."""
    assert dpo_epoch_guard(_gap_stats(-(DPO_GAP_WIDE + 0.5)), 3)[0] == 2


@pytest.mark.parametrize("gap", [0.0, 0.4, 1.2, DPO_GAP_WIDE])
def test_narrow_gap_never_raises_epochs(gap):
    """The 'train harder on a narrow gap' half is deliberately NOT built:
    it needs a calibrated mapping we do not have."""
    for epochs in (1, 2, 3, 4):
        got, _ = dpo_epoch_guard(_gap_stats(gap), epochs)
        assert got == epochs, "guard must never increase epochs"


def test_never_caps_below_one():
    assert dpo_epoch_guard(_gap_stats(50.0), 1)[0] == 1
    assert dpo_epoch_guard(_gap_stats(50.0), 2)[0] == 1


@pytest.mark.parametrize("epochs", [0, 1, -1, None, "3", 2.5])
def test_non_capable_epoch_values_pass_through(epochs):
    got, _ = dpo_epoch_guard(_gap_stats(50.0), epochs)
    assert got == epochs
