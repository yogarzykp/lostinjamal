"""An eval must not START when it cannot finish — including the first one.

The lead widens from a MEASURED cycle, so it cannot act on a cycle it has not yet seen.
On the gate's instruct stage, 2026-09-13:

    total_steps_per_epoch: 149 | periodic_save_steps: 500   <- 500 never fires
    step 149: Evaluating ... reason: epoch    <- the first AND only eval, 261s
    step 150: [deadline] eval cycle measured 261s; lead widened 3 -> 7 min
              [deadline] -61s remain but a full eval cycle takes 261s

The widening arrived 261 seconds too late; the stage finished at -80s to end_time where
the same stage had been +83s. The guard that refuses an unaffordable eval was already
there — it only had nothing to compare against on the FIRST cycle.

So the cost is now predicted before any cycle is measured, from quantities the callback
already sees: the dev row count, and the wall time of recent training steps against the
rows those steps consumed.

    predicted_cycle = dev_rows * (step_seconds / rows_per_step) * CYCLE_FACTOR

Calibrated on the KL stage of the same gate: dev 955 rows, 3.48 s/step at batch 4 x
grad_accum 4 = 16 rows, so 955 * 3.48/16 = 208 s; the measured cycle was 462 s — eval
(116 s, reported eval_runtime) plus the KL metric's two extra dev passes plus save and
copy. CYCLE_FACTOR 2.5 puts the prediction at 520 s, deliberately 12% above the
measurement: over-estimating costs one eval we could have afforded, under-estimating
costs the deadline and the save behind it. A real measurement supersedes the prediction
as soon as one exists.
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


def _cb(tmp_path, end_in, dev_rows=955, periodic=500, steps_per_epoch=149):
    handler = ct.WhenToEvalHandler(_end_in(end_in), 3, periodic_save_steps=periodic,
                                   steps_per_epoch=steps_per_epoch)
    cb = ct.CustomEvalSaveCallback(
        function_when_to_evaluate=handler,
        submission_dir=str(tmp_path / "sub"), output_dir=str(tmp_path / "out"),
        original_model_name="x", end_time=handler.end_time, checking_mode="none",
        dev_rows=dev_rows,
    )
    cb.early_stop_disabled = True
    cb.has_checkpoint = True
    return cb, handler


def _tick(cb, step, step_seconds, clock, monkeypatch):
    """One training step of the given wall duration, then on_step_end."""
    monkeypatch.setattr(ct.time, "monotonic", lambda: clock[0])
    clock[0] += step_seconds
    c = _Control()
    cb.on_step_end(args=_Args(), state=_State(step), control=c)
    return c


def test_the_predictor_reproduces_the_measured_kl_cycle(tmp_path, monkeypatch):
    """208s of raw forward work measured at 462s; the prediction must sit above it."""
    cb, _ = _cb(tmp_path, end_in=9999, dev_rows=955)
    clock = [1000.0]
    for s in range(1, 6):
        _tick(cb, s, 3.48, clock, monkeypatch)
    predicted = cb._predicted_cycle_secs(_Args())
    assert 460 <= predicted <= 620, f"predicted {predicted}s against a measured 462s"


def test_an_unaffordable_first_eval_is_refused(tmp_path, monkeypatch):
    """The b.log case: the epoch eval at step 149 with far less time than it needs."""
    cb, _ = _cb(tmp_path, end_in=9999, dev_rows=955, steps_per_epoch=149)
    clock = [1000.0]
    for s in range(145, 149):
        _tick(cb, s, 3.48, clock, monkeypatch)
    cb.end_time = _end_in(200)
    cb.function_when_to_evaluate.end_time = cb.end_time
    c = _tick(cb, 149, 3.48, clock, monkeypatch)   # epoch boundary
    assert c.should_evaluate is False, "started an eval that cannot finish before end_time"
    assert c.should_save is True, "the save must still happen — it is the artefact"
    assert cb.save_only is True


def test_an_affordable_first_eval_proceeds(tmp_path, monkeypatch):
    cb, _ = _cb(tmp_path, end_in=9999, dev_rows=955, steps_per_epoch=149)
    clock = [1000.0]
    for s in range(145, 149):
        _tick(cb, s, 3.48, clock, monkeypatch)
    cb.end_time = _end_in(3600)
    cb.function_when_to_evaluate.end_time = cb.end_time
    c = _tick(cb, 149, 3.48, clock, monkeypatch)
    assert c.should_evaluate is True and c.should_save is True
    assert cb.save_only is False


def test_a_measured_cycle_supersedes_the_prediction(tmp_path, monkeypatch):
    cb, _ = _cb(tmp_path, end_in=9999, dev_rows=955)
    clock = [1000.0]
    for s in range(1, 6):
        _tick(cb, s, 3.48, clock, monkeypatch)
    assert cb._predicted_cycle_secs(_Args()) > 400
    cb._eval_cycle_secs = 40.0          # a real, cheap cycle was seen
    assert cb._predicted_cycle_secs(_Args()) == 40.0


def test_without_step_timings_the_guard_stays_out_of_the_way(tmp_path, monkeypatch):
    """No steps timed yet — predict nothing rather than refuse on a guess."""
    cb, _ = _cb(tmp_path, end_in=200, dev_rows=955, steps_per_epoch=2)
    monkeypatch.setattr(ct.time, "monotonic", lambda: 1000.0)
    assert cb._predicted_cycle_secs(_Args()) is None
    c = _Control()
    cb.on_step_end(args=_Args(), state=_State(2), control=c)
    assert c.should_evaluate is True


def test_dev_rows_unknown_predicts_nothing(tmp_path, monkeypatch):
    cb, _ = _cb(tmp_path, end_in=9999, dev_rows=0)
    clock = [1000.0]
    for s in range(1, 6):
        _tick(cb, s, 3.48, clock, monkeypatch)
    assert cb._predicted_cycle_secs(_Args()) is None


def test_train_instruct_passes_the_dev_row_count():
    src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "scripts", "train_instruct.py"), encoding="utf-8").read()
    i = src.index("CustomEvalSaveCallback(")
    assert "dev_rows=" in src[i:i + 900], "the callback cannot predict a cycle it has no dev size for"
