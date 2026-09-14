"""An eval must not START when it cannot finish — including the very first one.

The deadline lead widens from a MEASURED cycle, so it cannot act on a cycle it has never
seen. On the gate's instruct stage, 2026-09-14:

    total_steps_per_epoch: 149 | periodic_save_steps: 500   <- 500 never fires
    step 149: Evaluating ... reason: epoch     <- the first AND only eval, 259s
    step 150: [deadline] eval cycle measured 259s; lead widened 3 -> 7 min
              [deadline] -56s remain but a full eval cycle takes 259s

The widening arrived 259 seconds too late and the stage finished 75s past end_time, where
the same stage had been +83s. It also cost the run its dev absorption, which refuses to
start with under 90s left.

A guard against exactly this already existed and did not fire, twice over:

  * on the periodic/epoch trigger it required `self.has_checkpoint`, and the first cycle
    is by definition the one with no checkpoint yet;
  * on the end_time trigger it required `self._eval_cycle_secs`, i.e. a cycle already
    measured — the same thing it was there to cover for.

Both now cost the cycle from quantities known before any eval runs. The estimate is used
ONLY to refuse an eval, never to widen the lead: refusing one that would have fit costs a
checkpoint candidate, while stopping training early costs training.

See CustomEvalSaveCallback._estimated_cycle_secs for the decomposition of the two
measured cycles this is calibrated against.
"""

import datetime
import importlib.machinery
import os
import sys
import types

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
if "wandb" not in sys.modules:
    _w = types.ModuleType("wandb"); _w.__spec__ = importlib.machinery.ModuleSpec("wandb", None)
    sys.modules["wandb"] = _w

ct = pytest.importorskip("customized_trainer")

# Qwen2-1.5B-Instruct in bf16, the model behind both measured cycles.
GIB_1B5 = 2.87
DEV_ROWS = 955
MEASURED_INSTRUCT_CYCLE = 259.0
MEASURED_KL_CYCLE = 462.0


class _Args:
    per_device_train_batch_size = 4
    gradient_accumulation_steps = 4
    world_size = 1


class _State:
    def __init__(self, step):
        self.global_step, self.epoch, self.log_history = step, 1.0, [{"learning_rate": 1e-5, "loss": 1.0}]


class _Control:
    should_evaluate = False
    should_save = False
    should_training_stop = False


def _end_in(seconds):
    t = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=seconds)
    return t.strftime("%Y-%m-%d %H:%M:%S")


@pytest.fixture(autouse=True)
def _isolated(monkeypatch):
    monkeypatch.setenv("TRAINING_BEST_CKPT_PERSIST", "0")
    monkeypatch.delenv("EMIT_PER_EXAMPLE_LOSSES", raising=False)


def _cb(tmp_path, end_in, dev_rows=DEV_ROWS, periodic=500, steps_per_epoch=149,
        model_gib=GIB_1B5, per_example=True, kl=False, has_checkpoint=False):
    handler = ct.WhenToEvalHandler(_end_in(end_in), 3, periodic_save_steps=periodic,
                                   steps_per_epoch=steps_per_epoch)
    cb = ct.CustomEvalSaveCallback(
        function_when_to_evaluate=handler,
        submission_dir=str(tmp_path / "sub"), output_dir=str(tmp_path / "out"),
        original_model_name="x", end_time=handler.end_time, checking_mode="none",
        dev_rows=dev_rows,
    )
    cb.early_stop_disabled = True
    cb._model_gib = model_gib
    # Both extra dev passes are wired by the train_*.py entry points, and both change
    # what a cycle costs, so the estimate has to see them the same way.
    if per_example:
        cb.per_example_eval_fn = lambda: [0.0] * dev_rows
    if kl:
        cb.kl_metric_fn = lambda: 0.0
        cb.kl_coef = 0.1
    cb.has_checkpoint = has_checkpoint
    return cb, handler


def _step(cb, step, remaining=None):
    """One on_step_end at the given step, optionally with the clock reset."""
    if remaining is not None:
        cb.end_time = _end_in(remaining)
        cb.function_when_to_evaluate.end_time = cb.end_time
    c = _Control()
    cb.on_step_end(args=_Args(), state=_State(step), control=c)
    return c


# ---------------------------------------------------------------- the cost model
#
# The estimate is an EMPIRICAL ENVELOPE, so the test for it is coverage of every cycle
# ever measured — including the one from the real tournament box, which the model shipped
# in be81e18 under-predicted by 51s. A cost model that sits below a known measurement
# starts an eval that cannot finish, and loses the save behind it.

# name, dev rows, model GiB, MEASURED cycle seconds, kl
MEASURED_CYCLES = [
    ("gate instruct", 955, 2.88, 259.0, False),
    ("gate KL", 955, 3.43, 463.0, True),
    ("gate DPO", 200, 0.25, 15.0, False),
    ("gate chat", 104, 0.25, 14.0, False),
    # task 59469903, gemma-2-2b, reconstructed from the loki record ts fields around step
    # 500: eval 109.2s + per-example 349.7s + save 5.71s + copy 5.21s.
    ("REAL tournament", 965, 4.86, 469.8, False),
]


@pytest.mark.parametrize("name,rows,gib,measured,kl",
                         MEASURED_CYCLES, ids=[c[0] for c in MEASURED_CYCLES])
def test_the_envelope_covers_every_measured_cycle(tmp_path, name, rows, gib, measured, kl):
    cb, _ = _cb(tmp_path, end_in=9999, dev_rows=rows, model_gib=gib, kl=kl)
    est = cb._estimated_cycle_secs()
    assert est > measured, (
        f"{name}: estimate {est:.0f}s is UNDER the measured {measured:.0f}s — this is the "
        f"error direction that starts an eval it cannot finish")
    assert est < measured * 2.5, (
        f"{name}: estimate {est:.0f}s against {measured:.0f}s refuses evals that would fit")


def test_the_model_that_shipped_in_be81e18_would_fail_this(tmp_path):
    """The regression this file exists for, stated as arithmetic.

    be81e18 costed a cycle as dev_rows/20 + dev_rows/15 + 15 + GiB*60, calibrated on the
    gate box. On the real tournament cycle that is 419s against a measured 470s.
    """
    rows, gib = 965, 4.86
    shipped = rows / 20.0 + rows / 15.0 + 15.0 + gib * 60.0
    assert shipped < 469.8, "the premise of this test no longer holds"
    cb, _ = _cb(tmp_path, end_in=9999, dev_rows=rows, model_gib=gib)
    assert cb._estimated_cycle_secs() > 469.8, "the replacement repeats the same defect"


def test_a_kl_cycle_costs_more_than_a_plain_one(tmp_path):
    """Measured: 0.141 s per row-GiB against 0.100, because KL evaluates against the base."""
    plain, _ = _cb(tmp_path, end_in=9999, kl=False)
    withkl, _ = _cb(tmp_path, end_in=9999, kl=True)
    assert withkl._estimated_cycle_secs() > plain._estimated_cycle_secs()


def test_the_estimate_scales_with_the_model(tmp_path):
    """A bigger model makes every dev pass dearer; the boss round's 35-71B must not cost
    the same as a 1.5B."""
    small, _ = _cb(tmp_path, end_in=9999, model_gib=GIB_1B5)
    large, _ = _cb(tmp_path, end_in=9999, model_gib=GIB_1B5 * 10)
    assert large._estimated_cycle_secs() > small._estimated_cycle_secs() * 4


def test_the_dev_split_is_shared_across_ranks(tmp_path):
    """Eval is data-parallel, so 8 ranks each walk an eighth of the split. Without this the
    boss round's model size would refuse every eval on a task where they are affordable."""
    one, _ = _cb(tmp_path, end_in=9999)
    eight, _ = _cb(tmp_path, end_in=9999)
    eight._world_size = 8
    assert eight._estimated_cycle_secs() < one._estimated_cycle_secs()


# ------------------------------------------------------- the guard that did not fire

def test_the_first_cycle_is_refused_with_no_prior_checkpoint(tmp_path):
    """THE REGRESSION. Step 149 of 150, 203s left, a 259s cycle, and no checkpoint yet.

    The guard used to require has_checkpoint, so on the one run shape that reaches its
    first cycle with the budget nearly gone it was dead code.
    """
    cb, _ = _cb(tmp_path, end_in=9999, steps_per_epoch=149, has_checkpoint=False)
    c = _step(cb, 149, remaining=203)
    assert c.should_evaluate is False, "started an eval that cannot finish before end_time"
    assert c.should_save is True, "the save must still happen — it is the only artefact"
    assert cb.save_only is True


def test_an_affordable_first_eval_proceeds(tmp_path):
    cb, _ = _cb(tmp_path, end_in=9999, steps_per_epoch=149, has_checkpoint=False)
    c = _step(cb, 149, remaining=3600)
    assert c.should_evaluate is True and c.should_save is True
    assert cb.save_only is False


def test_the_end_time_trigger_uses_the_estimate_when_nothing_was_measured(tmp_path):
    """The other half: end_time refused to check at all without a measured cycle."""
    cb, _ = _cb(tmp_path, end_in=9999, steps_per_epoch=-1, periodic=-1, has_checkpoint=True)
    assert cb._eval_cycle_secs is None
    c = _step(cb, 40, remaining=120)          # inside the 3-minute lead
    assert c.should_evaluate is False, "started an eval with 120s left and a ~300s cycle"
    assert c.should_save is True
    assert cb.save_only is True


def test_a_measured_cycle_supersedes_the_estimate(tmp_path):
    cb, _ = _cb(tmp_path, end_in=9999)
    assert cb._predicted_cycle_secs() > MEASURED_INSTRUCT_CYCLE
    cb._eval_cycle_secs = 40.0                # a real, cheap cycle was seen
    assert cb._predicted_cycle_secs() == 40.0


# ------------------------------------------------------- refuse to guess, not to run

def test_without_a_model_size_nothing_is_predicted(tmp_path):
    """on_train_begin could not read the model: cost nothing rather than refuse on a guess."""
    cb, _ = _cb(tmp_path, end_in=9999, model_gib=None, steps_per_epoch=149)
    assert cb._predicted_cycle_secs() is None
    c = _step(cb, 149, remaining=203)
    assert c.should_evaluate is True, "refused an eval on an estimate it does not have"


def test_dev_rows_unknown_predicts_nothing(tmp_path):
    cb, _ = _cb(tmp_path, end_in=9999, dev_rows=0)
    assert cb._predicted_cycle_secs() is None


def test_on_train_begin_reads_the_model_size(tmp_path):
    torch = pytest.importorskip("torch")
    cb, _ = _cb(tmp_path, end_in=9999, model_gib=None)
    model = torch.nn.Linear(1024, 1024, bias=False)          # 1M params, fp32 = 4 MiB
    cb.on_train_begin(args=_Args(), state=_State(0), control=_Control(), model=model)
    assert cb._model_gib == pytest.approx(4.0 / 1024, rel=0.02)


def test_on_train_begin_survives_a_model_it_cannot_size(tmp_path):
    cb, _ = _cb(tmp_path, end_in=9999, model_gib=None)

    class _Hostile:
        def parameters(self):
            raise RuntimeError("no")

    cb.on_train_begin(args=_Args(), state=_State(0), control=_Control(), model=_Hostile())
    assert cb._model_gib is None


# ------------------------------------------------------------------- the wiring

@pytest.mark.parametrize("entry", ["train_instruct.py", "train_dpo.py", "train_grpo.py"])
def test_the_entry_points_pass_the_dev_row_count(entry):
    src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "scripts", entry), encoding="utf-8").read()
    i = src.index("EvalSaveCallback(")
    assert "dev_rows=" in src[i:i + 1200], (
        f"{entry} builds a callback that cannot cost a cycle it has no dev size for")


# ------------------------------------------- a skipped cycle is not a measured cycle

def _run_cycle(cb, step, remaining, elapsed, monkeypatch):
    """Trigger a cycle at `step`, let `elapsed` seconds pass, then close it in on_save."""
    clock = [1000.0]
    monkeypatch.setattr(ct.time, "monotonic", lambda: clock[0])
    c = _step(cb, step, remaining=remaining)
    clock[0] += elapsed
    cb.has_checkpoint = True
    cb._record_eval_cycle()
    return c


def test_a_skipped_cycle_is_not_recorded_as_a_measured_one(tmp_path, monkeypatch):
    """THE SECOND REGRESSION, and the one that made the first fix worse than no fix.

    The trigger stamps _cycle_t0 BEFORE the guard decides. When the guard turns an epoch
    trigger into a bare save, that cheap save was timed and stored as the cost of a full
    cycle — and a measurement outranks the estimate. On the box the save-only at step 149
    measured 6s, so 178s of budget was judged sufficient at the end_time trigger for work
    that takes 250s. -94s, against -75s with no fix at all.
    """
    cb, _ = _cb(tmp_path, end_in=9999, steps_per_epoch=149, has_checkpoint=False)
    c = _run_cycle(cb, 149, remaining=205, elapsed=6.0, monkeypatch=monkeypatch)
    assert c.should_evaluate is False, "precondition: the guard skipped this eval"
    assert cb._eval_cycle_secs is None, (
        f"a save-only cycle was recorded as a {cb._eval_cycle_secs}s eval cycle")
    assert cb._predicted_cycle_secs() > MEASURED_INSTRUCT_CYCLE, (
        "the estimate must still stand — nothing has been measured")


def test_a_real_cycle_is_still_recorded(tmp_path, monkeypatch):
    """The exclusion must not swallow the measurement it exists to protect."""
    cb, _ = _cb(tmp_path, end_in=9999, steps_per_epoch=149, has_checkpoint=False)
    c = _run_cycle(cb, 149, remaining=3600, elapsed=259.0, monkeypatch=monkeypatch)
    assert c.should_evaluate is True, "precondition: this eval was affordable"
    assert cb._eval_cycle_secs == pytest.approx(259.0)
    assert cb._predicted_cycle_secs() == pytest.approx(259.0), "a measurement outranks the estimate"


def test_the_end_time_trigger_refuses_after_a_skipped_epoch_cycle(tmp_path, monkeypatch):
    """End to end over the box's exact numbers: skip at 149, then refuse at end_time."""
    cb, _ = _cb(tmp_path, end_in=9999, steps_per_epoch=149, has_checkpoint=False)
    _run_cycle(cb, 149, remaining=205, elapsed=6.0, monkeypatch=monkeypatch)
    cb.save_only = False
    c = _step(cb, 156, remaining=178)          # the end_time trigger, 2:58 left
    assert c.should_evaluate is False, "ran a 250s eval with 178s of budget"
    assert c.should_save is True
    assert cb.save_only is True
