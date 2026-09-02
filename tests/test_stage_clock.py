"""The run that overran its own end_time could not say where the time went.

Measured on 28c9f3bb, our cheapest task: training stopped with 2:58 left and the run
printed "Training successfully done" 29 seconds AFTER end_time. `save_before_remaining_time`
is 3 minutes, so the reserve is already short — and of that 3m28s only the 21.6s final
eval was attributable, because the whole window carried one timestamped log line.

Raising the reserve buys safety with training time, so the size has to come from knowing
which stage dominates. That is what this instruments. The tests below care about two
things: that the stages are actually marked (an uninstrumented stage is invisible again),
and that the timer can never be the reason a run fails.
"""

from __future__ import annotations

import ast
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAINER = os.path.join(ROOT, "scripts", "text_trainer.py")
MODULE = os.path.join(ROOT, "scripts", "dev_absorption.py")


def _source(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


@pytest.fixture
def clock_cls():
    """StageClock alone — text_trainer as a whole needs transformers."""
    import sys
    import time

    # StageClock resolves the deadline parser with `from dev_absorption import ...`, so
    # scripts/ has to be importable or every budget column silently reads "end_time
    # unknown" — which is also what a broken import would look like in production.
    if os.path.join(ROOT, "scripts") not in sys.path:
        sys.path.insert(0, os.path.join(ROOT, "scripts"))
    ns = {"time": time, "print": print}
    tree = ast.parse(_source(TRAINER))
    node = next(n for n in tree.body
                if isinstance(n, ast.ClassDef) and n.name == "StageClock")
    exec(compile(ast.Module(body=[node], type_ignores=[]), TRAINER, "exec"), ns)  # noqa: S102
    return ns["StageClock"]


def _end_time_in(seconds):
    import datetime
    t = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=seconds)
    return t.strftime("%Y-%m-%d %H:%M:%S")


# --- it reports what the decision needs -------------------------------------------


def test_it_reports_duration_and_remaining_budget(clock_cls):
    """A duration alone cannot say whether a stage was affordable."""
    lines = []
    c = clock_cls(_end_time_in(600), log=lambda m, **k: lines.append(m))
    c.mark("first stage")
    assert "first stage" in lines[0]
    assert "to end_time" in lines[0], lines[0]
    assert "cumulative" in lines[0], lines[0]


def test_a_negative_budget_is_shown_as_negative(clock_cls):
    """The overrun that started this is only visible if the sign survives."""
    lines = []
    c = clock_cls(_end_time_in(-40), log=lambda m, **k: lines.append(m))
    c.mark("late stage")
    assert "-" in lines[0].split("cumulative")[1], lines[0]


def test_stages_are_measured_separately_not_cumulatively(clock_cls):
    import time
    lines = []
    c = clock_cls(_end_time_in(600), log=lambda m, **k: lines.append(m))
    time.sleep(0.15)
    c.mark("a")
    c.mark("b")
    # The second stage did essentially nothing; if the timer reported cumulative time as
    # the per-stage figure, every stage after a slow one would look slow too.
    assert float(lines[0].split(": ")[1].split("s ")[0]) >= 0.1
    assert float(lines[1].split(": ")[1].split("s ")[0]) < 0.1


def test_an_unknown_deadline_still_reports_durations(clock_cls):
    lines = []
    c = clock_cls(None, log=lambda m, **k: lines.append(m))
    c.mark("no deadline here")
    assert "end_time unknown" in lines[0], lines[0]


# --- and it can never be the reason a run fails ------------------------------------


def test_an_unparseable_deadline_does_not_raise(clock_cls):
    lines = []
    c = clock_cls("not a timestamp", log=lambda m, **k: lines.append(m))
    c.mark("stage")
    assert lines and "stage" in lines[0]


def test_a_logger_that_throws_does_not_reach_the_caller(clock_cls):
    """print is replaced in some harnesses; a diagnostic must not care."""
    def boom(*a, **k):
        raise RuntimeError("log sink is gone")

    c = clock_cls(_end_time_in(600), log=boom)
    c.mark("stage")  # must not raise


def test_the_timer_is_wrapped_so_it_cannot_propagate():
    tree = ast.parse(_source(TRAINER))
    cls = next(n for n in ast.walk(tree)
               if isinstance(n, ast.ClassDef) and n.name == "StageClock")
    mark = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "mark")
    assert any(isinstance(n, ast.Try) for n in mark.body), (
        "mark() is not wrapped; a timer that can raise is a timer that can cost a run"
    )


# --- the stages that must be visible ------------------------------------------------


@pytest.mark.parametrize("stage", [
    "run_training",                       # where the 3m26s actually went
    "post-run settle",                    # the flat 5s per launch, spent past the deadline
    "NaN/Inf + zero-weight scan",         # both submission guards, one stage
    "dev absorption",                     # now on by default
    "restore_submission_architectures",   # the one whose loss costs the entry
])
def test_each_stage_of_the_tail_is_marked(stage):
    src = _source(TRAINER)
    marks = [line for line in src.splitlines() if "_clock.mark(" in line]
    assert any(stage in m for m in marks), (
        "%r is not marked, so it stays invisible in exactly the window that overran" % stage
    )


def test_the_clock_is_created_before_the_first_launch():
    """Created after the loop, it would miss the stage that dominates."""
    src = _source(TRAINER)
    created = src.index("_clock = StageClock(")
    first_mark = src.index("_clock.mark(")
    assert created < first_mark
    assert "end_time" in src[created:created + 200], (
        "the clock is created without a deadline, so every budget column reads unknown"
    )


def test_there_is_one_deadline_parser_not_three():
    """dev_absorption, customized_trainer and this clock all read the same field.

    Two parsers of one timestamp is two ways to disagree about when the run ends, and the
    disagreement would show up as a submission killed while the log said there was time.
    """
    src = _source(TRAINER)
    assert "from dev_absorption import seconds_until_deadline" in src
    assert "strptime" not in src.split("class StageClock")[1].split("def _arg_pattern")[0], (
        "StageClock parses end_time itself instead of reusing seconds_until_deadline"
    )
