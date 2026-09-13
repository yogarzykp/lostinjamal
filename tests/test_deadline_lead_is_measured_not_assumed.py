"""The deadline trigger must fire early enough for the eval cycle it starts.

WhenToEvalHandler fired `reason="end_time"` when less than save_before_remaining_time
(a fixed 3 minutes) remained, and THEN ran a full eval, the checkpoint metric, the
telemetry pass, the save and the copy — all after that mark — with post-training still
to come. Three GPU runs on 2026-09-13 measured the tail:

    instruct 8B  (dev 957): trigger at -178 s, eval 106 s + telemetry ~237 s + save -> -180 s
    KL 1.5B      (dev 955): trigger at -156 s, eval 116 s + KL metric (2 passes) + ...  -> -309 s
    instruct 8B  (dev 967): trigger at -176 s ...                                        -> -196 s

The validator kills ~173 s past our end_time, so each of these dies 10-140 s before its
post-training finishes. Three minutes assumed a tail nobody measured.

Now: the callback measures a full cycle (trigger -> end of on_save) at the first periodic
eval and widens the handler's lead to 1.25x that plus 45 s — never narrows it. And at
the trigger, if less time remains than a measured cycle takes, it saves without the eval
rather than start one that cannot finish.
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


class _State:
    def __init__(self, step):
        self.global_step, self.epoch, self.log_history = step, 1.0, [{"learning_rate": 1e-5, "loss": 1.0}]


class _Control:
    should_evaluate = False
    should_save = False
    should_training_stop = False


def _end_time_in(seconds):
    t = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=seconds)
    return t.strftime("%Y-%m-%d %H:%M:%S")


@pytest.fixture(autouse=True)
def _isolated(monkeypatch):
    monkeypatch.setenv("TRAINING_BEST_CKPT_PERSIST", "0")
    monkeypatch.delenv("EMIT_PER_EXAMPLE_LOSSES", raising=False)


def _make(tmp_path, end_in, periodic=100):
    handler = ct.WhenToEvalHandler(_end_time_in(end_in), 3, periodic_save_steps=periodic)
    cb = ct.CustomEvalSaveCallback(
        function_when_to_evaluate=handler,
        submission_dir=str(tmp_path / "sub"), output_dir=str(tmp_path / "out"),
        original_model_name="x", end_time=handler.end_time, checking_mode="none",
    )
    cb.early_stop_disabled = True
    cb.has_checkpoint = True
    return cb, handler


def _cycle(cb, step, seconds, monkeypatch):
    """One periodic eval cycle whose wall time is `seconds`, driven the way the Trainer
    drives it: on_step_end (trigger) -> on_evaluate -> on_save."""
    clock = [1000.0]
    monkeypatch.setattr(ct.time, "monotonic", lambda: clock[0])
    c = _Control()
    cb.on_step_end(args=None, state=_State(step), control=c)
    assert c.should_evaluate, "periodic trigger did not fire"
    clock[0] += seconds
    cb.on_evaluate(args=None, state=_State(step), control=c, metrics={"eval_loss": 1.0})
    ck = os.path.join(cb.output_dir, f"checkpoint-{step}")   # what the Trainer writes before on_save
    os.makedirs(ck, exist_ok=True); open(os.path.join(ck, "config.json"), "w").write("{}")
    cb.on_save(args=None, state=_State(step), control=c)


def test_a_measured_cycle_widens_the_deadline_lead(tmp_path, monkeypatch, capsys):
    cb, handler = _make(tmp_path, end_in=3600)
    assert handler.save_before_remaining_time == 3
    _cycle(cb, 100, seconds=361.0, monkeypatch=monkeypatch)   # the KL stage's measured tail
    # 1.25 x 361 + 45 = 496.25 s -> 9 minutes
    assert handler.save_before_remaining_time == 9, handler.save_before_remaining_time
    assert "eval cycle measured 361" in capsys.readouterr().out


def test_the_lead_never_narrows(tmp_path, monkeypatch):
    cb, handler = _make(tmp_path, end_in=3600)
    _cycle(cb, 100, seconds=361.0, monkeypatch=monkeypatch)
    _cycle(cb, 200, seconds=60.0, monkeypatch=monkeypatch)    # a faster cycle later
    assert handler.save_before_remaining_time == 9


def test_a_short_cycle_keeps_the_floor(tmp_path, monkeypatch):
    cb, handler = _make(tmp_path, end_in=3600)
    _cycle(cb, 100, seconds=20.0, monkeypatch=monkeypatch)   # 1.25*20+45 = 70 s -> 2 min < floor
    assert handler.save_before_remaining_time == 3


def test_deadline_fires_at_the_widened_lead(tmp_path, monkeypatch):
    """With a 9-minute lead, 8 minutes remaining must already be 'end_time'."""
    cb, handler = _make(tmp_path, end_in=3600, periodic=100)
    _cycle(cb, 100, seconds=361.0, monkeypatch=monkeypatch)
    handler.end_time = _end_time_in(8 * 60)
    got = handler(101)
    assert got == {"eval": True, "reason": "end_time"}, got


def test_at_the_trigger_an_eval_that_cannot_finish_is_skipped(tmp_path, monkeypatch, capsys):
    """Measured cycle 361 s, but only 150 s remain (the lead was widened too late, or a
    step was long): save without the eval instead of starting one that dies mid-way."""
    cb, handler = _make(tmp_path, end_in=3600)
    _cycle(cb, 100, seconds=361.0, monkeypatch=monkeypatch)
    handler.end_time = _end_time_in(150); cb.end_time = handler.end_time
    c = _Control()
    cb.on_step_end(args=None, state=_State(101), control=c)
    assert c.should_training_stop is True
    assert c.should_save is True
    assert c.should_evaluate is False, "started a 361 s eval with 150 s left"
    assert cb.save_only is True
    assert "saving without the eval" in capsys.readouterr().out


def test_without_a_measurement_the_deadline_eval_still_runs(tmp_path, monkeypatch):
    """No periodic cycle happened (short task): previous behaviour, eval at the trigger."""
    cb, handler = _make(tmp_path, end_in=150)
    c = _Control()
    cb.on_step_end(args=None, state=_State(5), control=c)
    assert c.should_training_stop is True and c.should_evaluate is True


def test_the_end_time_cycle_itself_does_not_feed_the_measurement(tmp_path, monkeypatch):
    """Only periodic/epoch cycles are representative; the deadline cycle may be save-only."""
    cb, handler = _make(tmp_path, end_in=150)
    clock = [1000.0]; monkeypatch.setattr(ct.time, "monotonic", lambda: clock[0])
    c = _Control()
    cb.on_step_end(args=None, state=_State(5), control=c)
    clock[0] += 900.0
    cb.on_save(args=None, state=_State(5), control=c)
    assert getattr(cb, "_eval_cycle_secs", None) is None
    assert handler.save_before_remaining_time == 3
