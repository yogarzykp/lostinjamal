"""A sweep that OOMs must shrink and retry, not skip.

The smoke gate caught this on the KL path of 3a6658eb at max_length=2675:

    [lr-search] sweeping at batch=4 (training batch is 4)
    [lr-search] LRRT skipped (OutOfMemoryError: Tried to allocate 6.06 GiB ...)
    FAIL kl  LRRT failed open — fell back to the geometric ladder

Skipping is not a neutral fallback. Without lrrt_lr in the state the run uses the
geometric ladder, and our own 4-curve grid measured that picker 777x off where the
loss-minimum picker was 1.9x. So the skip costs the learning rate.

The batch had already been made small twice, each time by picking a smaller constant.
That is the wrong shape of fix — what fits depends on the sequence length the planner
chose for the task, which is exactly what changed when the max_length wire was repaired
(1536 -> 2675, about 1.74x the activations).
"""

from __future__ import annotations

import ast
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAINER = os.path.join(ROOT, "scripts", "train_instruct.py")


def _source():
    with open(TRAINER, "r", encoding="utf-8") as fh:
        return fh.read()


@pytest.fixture(scope="module")
def sweep_region():
    """The source of the loop that runs the sweep, isolated from the rest of main()."""
    src = _source()
    # From the START OF THE LINE, not from the identifier: slicing mid-line leaves the
    # first line with no indentation, textwrap.dedent then finds a common prefix of ""
    # and strips nothing, and ast.parse raises IndentationError on line 2. That made one
    # test fail unconditionally, which made every mutation below look caught.
    start = src.rindex("\n", 0, src.index("_attempt_bs = _sweep_bs")) + 1
    end = src.index("_min_pts = max(", start)
    end = src.rindex("\n", 0, end) + 1
    return src[start:end]


# --- it retries instead of skipping -------------------------------------------------


def test_the_sweep_is_wrapped_in_a_retry_loop(sweep_region):
    import textwrap
    # dedent, not re-indent: the region is already indented inside main(), and prefixing
    # more spaces produced an IndentationError that made this test fail unconditionally —
    # which in turn made every mutation look caught. A test that always fails is not a
    # strict test, it is a broken instrument.
    tree = ast.parse(textwrap.dedent(sweep_region))
    assert any(isinstance(n, ast.While) for n in ast.walk(tree)), (
        "the sweep runs once; an OOM still ends it"
    )


def test_the_retry_shrinks_the_batch(sweep_region):
    assert "_attempt_bs // 2" in sweep_region, (
        "the retry does not reduce the batch, so it repeats the allocation that failed"
    )


def test_the_retry_rebuilds_the_loader_at_the_new_batch(sweep_region):
    """A smaller _attempt_bs that never reaches a DataLoader changes nothing."""
    after_retry = sweep_region[sweep_region.index("_next_bs"):]
    assert "DataLoader(" in after_retry, "the loader is not rebuilt for the retry"
    assert "batch_size=_attempt_bs" in after_retry, (
        "the rebuilt loader does not use the reduced batch"
    )


def test_the_model_is_reloaded_between_attempts(sweep_region):
    """The failed attempt already stepped the weights toward divergence.

    Retrying on them would measure the damage rather than the model, and the result
    would look like a successful sweep.
    """
    assert "_reload_sweep_model()" in sweep_region, (
        "no reload between attempts; the retry sweeps weights the previous attempt "
        "already walked up the LR range"
    )


def test_the_reload_actually_replaces_the_model_used_by_the_sweep():
    src = _source()
    fn = src[src.index("def _reload_sweep_model"):src.index("def _is_oom")]
    for attr in ("trainer.model = ", "trainer.model_wrapped = "):
        assert attr in fn, (
            "%r is missing, so the trainer keeps the model the failed sweep damaged"
            % attr.strip())
    assert "trainer.optimizer = None" in fn, (
        "the optimizer still holds parameters of the destroyed model"
    )
    assert "return" in fn, "the reload returns nothing, so `model` is never rebound"


# --- and it still fails open on everything that is not an OOM ----------------------


def test_a_non_oom_failure_is_re_raised(sweep_region):
    """Fail-open is right for a broken sweep; it is wrong as a response to memory."""
    assert "if not _is_oom(" in sweep_region and "raise" in sweep_region, (
        "every exception is treated as an OOM, so a real bug in the finder becomes a "
        "silent retry loop"
    )


def test_the_ladder_stops_at_batch_one(sweep_region):
    assert "_attempt_bs <= 1" in sweep_region, (
        "nothing stops the halving at 1; max(1, x//2) is a fixed point and the loop "
        "would retry forever"
    )


def test_oom_is_detected_by_type_and_by_message():
    """torch raises OutOfMemoryError on new versions and a plain RuntimeError on old."""
    src = _source()
    fn = src[src.index("def _is_oom"):src.index("_loader = DataLoader(train_ds")]
    assert "OutOfMemoryError" in fn
    assert "out of memory" in fn.lower(), (
        "only the typed error is matched; older torch raises RuntimeError with the "
        "message and would be re-raised as if it were a real fault"
    )


def test_the_cache_is_released_before_retrying(sweep_region):
    """Retrying without freeing repeats the same allocation against the same shortfall."""
    assert "empty_cache()" in sweep_region


def test_the_retry_is_visible_in_the_log(sweep_region):
    """A silent shrink would leave the curve unexplainable after the fact."""
    assert "sweep OOM" in sweep_region and "retrying at batch=" in sweep_region
