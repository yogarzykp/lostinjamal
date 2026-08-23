"""An alarm that never clears is not read, even when it is true.

`UNBRACKETED(nothing probed above the incumbent)` fired on essentially every run,
including ones with a correct prior. It was never a false alarm — the condition is
genuinely true — but it said only THAT it happened, never why, so it read as a standing
complaint and stopped being read at all. A warning in that state has already stopped
guarding the once it matters.

The reason it is always true turns out to matter more than the warning. The upward probe
exists to prevent exactly this, and is gated on

    span_decades < MIN_EXPLORED_DECADES  AND  suggestion < incumbent / 2

Those can only hold together in a narrow window, because `explored` includes the
incumbent: a suggestion far BELOW it makes the span automatically WIDE and suppresses the
probe. The range test reads systematically ~20x low on a fine-tune — 1.3 decades — which
sits outside that window. So the guard blocks the probe in precisely the case it was
written for.

Fixing the guard would change which learning rate gets chosen, so it is NOT changed here.
These tests pin two things: the message now names the suppression, and candidate
generation is untouched.
"""

import os
import sys

import pytest

SCRIPTS = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, SCRIPTS)

import lr_search  # noqa: E402

INSTRUCT = "instruct"


def _tail(suggestion, incumbent):
    return lr_search.describe(suggestion, incumbent, INSTRUCT)


# ---------------------------------------------------------------------------
# The message must diagnose, not just complain
# ---------------------------------------------------------------------------

def test_the_warning_names_the_span_that_suppressed_the_upward_probe():
    """The real clean-prior run: suggestion 4.132e-07, incumbent 8.07e-05."""
    line = _tail(4.132e-07, 8.07e-05)
    assert "UNBRACKETED" in line
    assert "upward probe suppressed" in line, (
        f"the warning still reports only that nothing was above the incumbent, without "
        f"naming the guard that prevented it:\n{line}"
    )
    assert "1.91d" in line and "1.0d" in line, (
        f"the actual span and the threshold are not both in the message, so a reader "
        f"cannot tell how far outside the window this run was:\n{line}"
    )


def test_the_warning_still_fires_when_it_should():
    """Diagnosing it must not have quietly switched it off."""
    assert "UNBRACKETED" in _tail(4.132e-07, 8.07e-05)
    assert "UNBRACKETED" in _tail(4.132e-07, 8.07e-04)


def test_no_warning_when_something_is_actually_above_the_incumbent():
    for suggestion, incumbent in [
        (4.132e-07, 8.07e-06),   # 10x-low prior: a candidate lands above it
        (9.545e-05, 8.07e-05),   # suggestion already above
        (3.0e-05, 8.07e-05),     # inside the window — the upward probe fires
    ]:
        line = _tail(suggestion, incumbent)
        assert "UNBRACKETED" not in line, (
            f"warned despite bracketing the incumbent from above: {line}"
        )


def test_the_reason_distinguishes_suppressed_from_not_applicable():
    """Two different situations must not read identically."""
    suppressed = _tail(4.132e-07, 8.07e-05)
    assert "suppressed" in suppressed
    # A suggestion that is NOT well below the incumbent is a different case: the probe was
    # never applicable, rather than blocked.
    line = _tail(6.0e-05, 8.07e-05)
    if "UNBRACKETED" in line:
        assert "not applicable" in line, line


# ---------------------------------------------------------------------------
# The regression direction: selection behaviour must be untouched
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("suggestion,incumbent,expected", [
    # Taken from the real logs of runs we performed, not recomputed from the code.
    (4.132e-07, 8.07e-05, ["1.000e-06", "8.983e-06"]),   # clean prior, slope picker
    (4.132e-07, 8.07e-04, ["1.000e-06", "2.841e-05"]),   # poisoned 10x high
])
def test_candidate_generation_is_unchanged(suggestion, incumbent, expected):
    """These exact candidate lists appear in the recovery-gate logs. Diagnosing a warning
    must not move a learning rate."""
    got = [f"{c:.3e}" for c in lr_search.confirmation_candidates(
        suggestion, incumbent, INSTRUCT)]
    assert got == expected, (
        f"candidates changed from {expected} to {got} — a message-only change altered "
        f"which learning rates get probed"
    )


def test_the_upward_probe_still_fires_inside_its_window():
    """Pin the window itself, so a later fix to the guard is visibly a behaviour change."""
    cands = lr_search.confirmation_candidates(3.0e-05, 8.07e-05, INSTRUCT)
    assert any(c > 8.07e-05 for c in cands), (
        "the upward probe no longer fires even inside its window; that is a selection "
        "change, not a reporting change"
    )


def test_the_guard_still_blocks_the_probe_when_the_suggestion_is_far_below():
    """Recorded as the DEFECT it is, not as intended behaviour.

    Changing this changes which learning rate is chosen, so it is left alone until that
    is decided deliberately. The test exists so the decision is visible when it happens.
    """
    cands = lr_search.confirmation_candidates(4.132e-07, 8.07e-05, INSTRUCT)
    assert not any(c > 8.07e-05 for c in cands), (
        "the upward probe now reaches above the incumbent on a far-below suggestion — "
        "that is the fix we deliberately deferred, and it changes LR selection"
    )
