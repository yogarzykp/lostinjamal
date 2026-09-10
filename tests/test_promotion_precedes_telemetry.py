"""The checkpoint promotion must not sit downstream of observational work.

On 2026-09-07, tournament task 59469903 evaluated twice: step 500 at eval_loss
0.05278521 and step 544 — the deadline eval — at 0.05173291. Only step 500 was
ever promoted, and the uploaded artefact's loss.txt proves it
(`500,0.05278521403670311`). The container was killed inside the per-example
telemetry pass 242s into the step-544 eval, and that pass ran BEFORE the
promotion. We shipped the worse of two checkpoints we had already measured and
gave away 0.00105 nats against a 0.0072 gap to rank 1 on that task.

These tests pin the ordering rather than the mechanism, because the mechanism is
allowed to change: what must not change is that nothing observational can stand
between the eval metric and the statement that decides which artefact we ship.
The champion's own callback has nothing at all in that gap
(god-text-tourn-2ba0f79237bffcf7-20260907-position-1
 scripts/customized_trainer.py:249-267).

Note the whole 783-test suite passed while the defect was live. A test that
cannot fail on the bug it describes is worth nothing, so each of these is
checked against the pre-fix ordering by construction: they fail if the telemetry
call is moved back above the promotion.
"""

import os
import sys
import types

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

# customized_trainer imports wandb at module scope, but the only use is init_wandb
# (customized_trainer.py:1747) — nothing on_evaluate touches. Stubbing it keeps this
# file runnable off the smoke box. importorskip was the alternative and is worse
# here: it would make these tests silently absent on the machine where the ordering
# is most likely to be refactored, and a test that cannot fail is not a test.
sys.modules.setdefault("wandb", types.ModuleType("wandb"))


class _State:
    """The slice of transformers' TrainerState that on_evaluate reads."""

    def __init__(self, step, epoch=1.0):
        self.global_step = step
        self.epoch = epoch
        self.log_history = [{"learning_rate": 1e-5}]


@pytest.fixture(autouse=True)
def _isolated_env():
    """Each test gets a clean env, and cross-instance best-checkpoint persistence off.

    CustomEvalSaveCallback.__init__ restores best_checkpoint_info from the process
    state store (customized_trainer.py:252-262), and state_manager falls back to a
    process-local dict when redis is absent — so without this, one test's promotion
    seeds the next test's starting best. That is the production behaviour working as
    designed; it just has to be switched off to test one callback at a time.
    """
    keep = {k: os.environ.get(k) for k in ("EMIT_PER_EXAMPLE_LOSSES", "TRAINING_BEST_CKPT_PERSIST")}
    os.environ["TRAINING_BEST_CKPT_PERSIST"] = "0"
    os.environ.pop("EMIT_PER_EXAMPLE_LOSSES", None)
    yield
    for k, v in keep.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v


def _callback(tmp_path):
    from customized_trainer import CustomEvalSaveCallback

    cb = CustomEvalSaveCallback(
        function_when_to_evaluate=lambda *a, **k: False,
        submission_dir=str(tmp_path / "submission"),
        output_dir=str(tmp_path / "out"),
        original_model_name="unsloth/gemma-2-2b",
    )
    cb.early_stop_disabled = True
    return cb


def _evaluate(cb, step, loss):
    cb.on_evaluate(args=None, state=_State(step), control=None, metrics={"eval_loss": loss})


def test_a_kill_inside_telemetry_still_leaves_the_better_checkpoint_promoted(tmp_path):
    """The exact 59469903 failure: the process dies inside the observational pass.

    SystemExit stands in for the container cleanup. If telemetry runs first, the
    promotion never happens and best_checkpoint_info still names the older,
    worse step — which is what shipped.
    """
    cb = _callback(tmp_path)
    _evaluate(cb, 500, 0.05278521403670311)
    assert cb.best_checkpoint_info["step"] == 500

    def _die():
        raise SystemExit("container cleaned up mid-pass")

    cb.per_example_eval_fn = _die
    os.environ["EMIT_PER_EXAMPLE_LOSSES"] = "1"
    try:
        with pytest.raises(SystemExit):
            _evaluate(cb, 544, 0.05173290893435478)
    finally:
        os.environ.pop("EMIT_PER_EXAMPLE_LOSSES", None)

    assert cb.best_checkpoint_info["step"] == 544, (
        "the better step-544 checkpoint was not promoted before the telemetry that "
        "killed the process — this is the 59469903 defect"
    )
    assert cb.best_checkpoint_info["loss"] == pytest.approx(0.05173290893435478)


def test_telemetry_observes_a_state_the_promotion_has_already_updated(tmp_path):
    """Ordering, stated positively and without an exception to carry it."""
    cb = _callback(tmp_path)
    _evaluate(cb, 500, 0.9)

    seen = {}

    def _observe():
        seen["step"] = cb.best_checkpoint_info["step"]
        return [0.1, 0.2]

    cb.per_example_eval_fn = _observe
    os.environ["EMIT_PER_EXAMPLE_LOSSES"] = "1"
    try:
        _evaluate(cb, 700, 0.5)
    finally:
        os.environ.pop("EMIT_PER_EXAMPLE_LOSSES", None)

    assert seen.get("step") == 700, (
        f"telemetry saw best={seen.get('step')}; it must run after the promotion, not before"
    )


def test_telemetry_still_runs_on_a_non_improving_eval(tmp_path):
    """Placement must not bias the sample it collects.

    The early-stop branch returns in several places, so putting telemetry at the
    end of the method would silently restrict it to improving evals — a biased
    sample of exactly the runs we would want to study.
    """
    cb = _callback(tmp_path)
    _evaluate(cb, 500, 0.5)

    calls = []
    cb.per_example_eval_fn = lambda: (calls.append(1), [0.1])[1]
    os.environ["EMIT_PER_EXAMPLE_LOSSES"] = "1"
    try:
        _evaluate(cb, 700, 0.9)  # worse: takes the not-improved branch
    finally:
        os.environ.pop("EMIT_PER_EXAMPLE_LOSSES", None)

    assert cb.best_checkpoint_info["step"] == 500, "a worse eval must not be promoted"
    assert calls, "telemetry was skipped on a non-improving eval"


def test_the_observational_pass_is_off_unless_asked_for(tmp_path):
    """Default OFF. Measured at 349.7s against 109.2s for the eval it duplicates,
    reproducing that eval's mean to 0.0046%, and writing to a file inside the
    container that nothing reads back."""
    from per_example_eval import enabled

    os.environ.pop("EMIT_PER_EXAMPLE_LOSSES", None)
    assert enabled() is False

    os.environ["EMIT_PER_EXAMPLE_LOSSES"] = "1"
    try:
        assert enabled() is True
    finally:
        os.environ.pop("EMIT_PER_EXAMPLE_LOSSES", None)
