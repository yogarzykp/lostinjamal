"""Candidate generation must reach a true LR that the ladder could not.

The ladder failed the recovery gate for one reason: reach. With a prior 10x too high it
could only offer x0.66..x1.51 around that prior, so the truth was never a candidate and
it returned its own floor, 6.6x high, confidently. These tests state the new mechanism's
reach as executable bounds so a future narrowing cannot pass silently.
"""

import math
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from lr_search import ABSOLUTE_BOUNDS, bounds_for, clamp, confirmation_candidates  # noqa: E402

TRUE_LR = 8.07e-05          # the unpoisoned baseline from the real run
POISON_HIGH = 8.07e-04      # what the recovery gate forced
POISON_LOW = 8.07e-06


def test_the_case_the_ladder_failed_is_now_reachable():
    """The whole point. Prior 10x high, LRRT finds the truth, the truth survives."""
    cands = confirmation_candidates(TRUE_LR, POISON_HIGH, "instruct")
    assert any(abs(math.log10(c / TRUE_LR)) < 0.05 for c in cands), (
        f"true LR not among candidates {cands}"
    )


def test_the_opposite_failure_is_reachable_too():
    cands = confirmation_candidates(TRUE_LR, POISON_LOW, "instruct")
    assert any(abs(math.log10(c / TRUE_LR)) < 0.05 for c in cands)


def test_a_disagreement_over_a_decade_adds_a_midpoint():
    cands = confirmation_candidates(TRUE_LR, POISON_HIGH, "instruct")
    assert len(cands) == 2, f"expected suggestion + midpoint, got {cands}"
    mid = sorted(cands)[1]
    assert TRUE_LR < mid < POISON_HIGH


def test_agreement_costs_no_extra_probe():
    """Six minutes per probe; do not spend it resolving a gap that is not there."""
    cands = confirmation_candidates(TRUE_LR * 1.2, TRUE_LR, "instruct")
    assert len(cands) == 1


def test_a_suggestion_equal_to_the_incumbent_probes_nothing():
    """The probe run already trained at the incumbent — that arm is paid for."""
    assert confirmation_candidates(TRUE_LR, TRUE_LR, "instruct") == []


@pytest.mark.parametrize("bad", [0.0, -1.0, float("nan")])
def test_degenerate_sweep_output_is_floored_not_propagated(bad):
    """find_lr_lrrt has branches that return something arbitrary rather than measured."""
    lo, _ = bounds_for("instruct")
    assert clamp(bad, "instruct") == lo


def test_bounds_are_clamped_not_rejected():
    lo, hi = bounds_for("instruct")
    assert clamp(1.0, "instruct") == hi
    assert clamp(1e-12, "instruct") == lo


def test_dpo_gets_a_lower_band_than_instruct():
    """One pair of bounds would clip legitimate DPO rates at the instruct floor."""
    assert bounds_for("dpo")[0] < bounds_for("instruct")[0]
    assert bounds_for("dpo")[1] < bounds_for("instruct")[1]
    assert clamp(5e-6, "dpo") == 5e-6, "a normal DPO rate must survive its own bounds"


@pytest.mark.parametrize("task", ["InstructTextTask", "ChatTask", "DpoTask", "GrpoTask"])
def test_task_type_strings_from_the_cli_resolve(task):
    """text_trainer passes the CLI spelling, not the short key."""
    assert bounds_for(task) in ABSOLUTE_BOUNDS.values()


def test_reach_beats_the_ladder_by_orders_of_magnitude():
    """State the improvement as a number, against the ladder's measured span."""
    lo, hi = bounds_for("instruct")
    ladder_span = 1.51 / 0.66          # text_trainer.get_log_scale 0.18
    assert (hi / lo) / ladder_span > 100


# --- bracketing restored from below (added after the 10x-LOW gate failed) -----------

def test_a_low_prior_now_gets_a_candidate_above_it():
    """The failure the recovery gate found: with a LOW prior nothing was tried above.

    The range test reads systematically low on a fine-tune, so a low suggestion plus a
    low prior leaves both on the same side and the incumbent wins at 10x low. Measured:
    candidates were [1.00e-06] against an incumbent of 8.07e-06, true 8.07e-05.
    """
    cands = confirmation_candidates(4.132e-07, POISON_LOW, "instruct")
    assert any(c > POISON_LOW for c in cands), (
        f"nothing above the incumbent {POISON_LOW:.2e}: {cands}"
    )
    best = min(cands + [POISON_LOW], key=lambda x: max(x / TRUE_LR, TRUE_LR / x))
    off = max(best / TRUE_LR, TRUE_LR / best)
    assert off <= 3.0, f"best reachable is {off:.2f}x from true, outside the 3x gate bar"


def test_a_wide_search_does_not_buy_an_extra_probe():
    """With a HIGH prior the span is ~2.9 decades and the truth is already inside it.

    An upward probe there would only re-test a rate the incumbent has already proved
    bad, at six minutes a probe.
    """
    high = confirmation_candidates(4.132e-07, POISON_HIGH, "instruct")
    assert not any(c > POISON_HIGH for c in high), f"wasted a probe above a high prior: {high}"


def test_a_correct_prior_does_not_buy_an_extra_probe():
    cands = confirmation_candidates(4.132e-07, TRUE_LR, "instruct")
    assert not any(c > TRUE_LR for c in cands), f"wasted a probe on a correct prior: {cands}"


def test_the_trigger_is_explored_span_not_direction():
    """High and low priors both put every candidate below the incumbent; only the narrow
    one earns the extra probe. Direction cannot be the trigger."""
    low = confirmation_candidates(4.132e-07, POISON_LOW, "instruct")
    high = confirmation_candidates(4.132e-07, POISON_HIGH, "instruct")
    assert all(c <= POISON_LOW * 1.05 or c > POISON_LOW for c in low)
    low_span = math.log10(max(low + [POISON_LOW]) / min(low + [POISON_LOW]))
    high_span = math.log10(max(high + [POISON_HIGH]) / min(high + [POISON_HIGH]))
    assert low_span < high_span, "the low case should have been the narrower search"


def test_describe_warns_when_nothing_brackets_from_above():
    """A kept incumbent must not read as a confirmation when nothing was tried above it."""
    from lr_search import describe
    # Force the unbracketed shape by making the span wide enough to skip the upward probe
    # while leaving every candidate below the incumbent.
    text = describe(1e-06, 8.07e-04, "instruct")
    assert "UNBRACKETED" in text, text
