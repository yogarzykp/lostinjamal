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
