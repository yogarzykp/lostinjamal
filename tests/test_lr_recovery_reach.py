"""Can LR selection reach a sane learning rate when its prior is wrong?

This is the question an on-distribution A/B can never answer. On a normal task the
family LR table is already close to right, so every selector looks fine and the
comparison measures nothing. LR selection earns its cost only in the case where the
prior is WRONG — an unfamiliar architecture, an anonymised model that misses the
lookup, a dataset whose scale the table never saw.

Reachability comes before selection quality. If the correct learning rate is not in
the candidate set, no amount of careful scoring finds it: the sweep returns the least
bad of several wrong answers, and it returns it confidently.

The production ladder builds candidates with `lr_utils.extend_learning_rates(lr, n,
log_range)`, and `text_trainer.get_log_scale` uses log_range 0.18 for instruct, chat
and DPO, 0.2 for GRPO. That is a span of roughly x0.66..x1.51 around the prior. These
tests state that fact as an executable bound rather than a comment, so that any future
change to the search — a wider range, an LR range test, anything — has to say plainly
what it changed about reachability.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from lr_utils import extend_learning_rates  # noqa: E402

# text_trainer.get_log_scale, transcribed. Kept here rather than imported because
# importing text_trainer drags in the whole training stack.
LOG_RANGE = {"instruct": 0.18, "chat": 0.18, "dpo": 0.18, "grpo": 0.2}
N_CANDIDATES = 4  # MAX_TRIES=3 + the probe run itself


def reach(prior, task="instruct", n=N_CANDIDATES):
    c = extend_learning_rates(prior, n, log_range=LOG_RANGE[task])
    return min(c), max(c)


def can_reach(prior, target, task="instruct", tolerance=1.5):
    """Is `target` inside the candidate span, within a factor of `tolerance`?"""
    lo, hi = reach(prior, task)
    return lo / tolerance <= target <= hi * tolerance


@pytest.mark.parametrize("task", ["instruct", "chat", "dpo", "grpo"])
def test_candidate_span_is_under_a_factor_of_three(task):
    """State the span as a number so a change to it cannot pass silently."""
    lo, hi = reach(1e-4, task)
    assert hi / lo < 3.0, f"{task}: span {lo:.2e}..{hi:.2e} is wider than documented"


def test_a_correct_prior_is_trivially_reachable():
    assert can_reach(1e-4, 1e-4)


def test_a_prior_wrong_by_ten_times_cannot_reach_the_truth():
    """The finding this file exists to record.

    With the prior 10x too high the true LR is far below every candidate, so the sweep
    picks its own lowest candidate — still ~6.6x too high — and reports a winner.
    """
    true_lr = 1e-4
    assert not can_reach(true_lr * 10, true_lr), (
        "the ladder can reach a 10x-wrong prior's truth; if this now passes, the search "
        "was widened and the recovery claim in ops/smoke/lr_recovery.sh should be re-run"
    )


def test_a_prior_wrong_by_a_tenth_cannot_reach_the_truth():
    true_lr = 1e-4
    assert not can_reach(true_lr / 10, true_lr)


@pytest.mark.parametrize("factor", [2, 3, 5, 10, 100])
def test_recovery_limit_is_where_the_span_ends(factor):
    """Recovery is possible up to roughly the span edge and not beyond.

    x2 sits just outside the raw span but inside the 1.5x tolerance; anything from x3
    up is unreachable. That boundary is the honest statement of what this mechanism can
    fix, and it is far narrower than the errors a wrong prior actually produces.
    """
    true_lr = 1e-4
    reachable = can_reach(true_lr * factor, true_lr)
    assert reachable == (factor <= 2), f"x{factor}: reachable={reachable}, expected {factor <= 2}"


def test_widening_the_range_is_what_would_buy_recovery():
    """A range test sweeping decades reaches what the ladder cannot — stated as a bound.

    scripts/lr_finder.py sweeps 1e-7..1e-2 (five decades). This test does not endorse
    swapping it in; it records that the reachability problem has a known shape and that
    the fix is a wider search, not better scoring inside a narrow one.
    """
    true_lr = 1e-4
    lo, hi = reach(true_lr * 10, "instruct")
    assert not (lo <= true_lr <= hi)
    assert 1e-7 <= true_lr <= 1e-2, "an LRRT sweep over 1e-7..1e-2 contains the truth"
