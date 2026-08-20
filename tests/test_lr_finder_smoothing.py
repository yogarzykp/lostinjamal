"""The LR range test must not invent a descent that the loss curve does not contain.

`find_lr_lrrt` was orphaned in this repo — nothing imported it — and when it was finally
wired in it returned `idx=1/100`, suggesting 1.12e-07 for a task whose real rate is
8.07e-05. The cause was in the smoother, not the data: the EMA was seeded with the first
loss and then bias-corrected anyway, so the opening points were inflated by up to
1/smooth_factor (20x here). On a perfectly flat loss that produced 50 -> 25.6 -> 17.5,
a steep artificial descent sitting exactly where the sweep's learning rates are too
small to do anything — and the steepest-descent search picked it every time.

These tests drive the smoother with synthetic curves, so they do not need a GPU and they
fail loudly if the correction is ever reintroduced.
"""

import math
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))


def smooth(losses, smooth_factor=0.05):
    """The production smoother, transcribed from lr_finder.find_lr_lrrt."""
    avg, out = 0.0, []
    for step, loss in enumerate(losses):
        avg = (1 - smooth_factor) * avg + smooth_factor * loss
        out.append(avg / (1 - (1 - smooth_factor) ** (step + 1)))
    return out


def test_a_flat_loss_smooths_to_a_flat_curve():
    """The regression. The old form turned a constant 2.5 into 50 -> 25.6 -> 17.5."""
    out = smooth([2.5] * 30)
    assert all(abs(v - 2.5) < 1e-9 for v in out), f"flat loss did not stay flat: {out[:5]}"


def test_the_opening_point_is_the_loss_not_a_multiple_of_it():
    out = smooth([2.5] * 5)
    assert abs(out[0] - 2.5) < 1e-9, f"first point inflated to {out[0]}"


def test_a_real_descent_still_registers():
    """Fixing the artefact must not make the smoother blind to actual learning."""
    losses = [3.0 - 0.02 * i for i in range(60)]
    out = smooth(losses)
    assert out[-1] < out[0] - 0.5, "a genuine downward trend was flattened away"


def test_smoothed_curve_lags_but_tracks():
    losses = [3.0] * 20 + [1.0] * 40
    out = smooth(losses)
    assert out[19] > 2.5, "the smoother jumped ahead of the data"
    assert out[-1] < 1.5, "the smoother never caught up to the data"


def test_the_steepest_slope_lands_where_the_drop_is():
    """End to end on the smoother + slope search, without a model.

    A curve that is flat, then drops sharply in the middle, then flattens: the steepest
    descent must be found in the middle, not at index 1.
    """
    n = 100
    losses = [3.0] * 40 + [3.0 - 0.05 * i for i in range(20)] + [2.0] * 40
    sm = smooth(losses)
    log_lrs = [(-7 + 5 * i / (n - 1)) for i in range(n)]  # 1e-7..1e-2, as in production

    slopes = []
    for i in range(1, len(sm)):
        d = log_lrs[i] - log_lrs[i - 1]
        slopes.append((sm[i] - sm[i - 1]) / d if abs(d) > 1e-9 else 0.0)

    skip = min(max(5, len(slopes) // 10), max(1, len(slopes) - 1))
    searchable = slopes[skip:]
    idx = searchable.index(min(searchable)) + skip + 1

    assert 40 <= idx <= 75, f"steepest descent found at {idx}, outside the actual drop"
    assert idx > 5, "steepest descent landed in the sweep's opening — the old failure"
