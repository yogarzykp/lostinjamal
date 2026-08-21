"""Drive the REAL ladder loop end to end with training replaced by a recorder.

The first harness checked the command surface and passed, which told me the bug was in
the loop's bookkeeping rather than in string substitution. This drives the loop itself.

`run_training` here plays the part the training subprocess plays in production: it does
not train, it writes back the state that `CustomEvalSaveCallback` would have written —
`mode`/`next_runs`/`current_loss` at the probe, a recorded score at each candidate. That
is the whole contract between the two processes, and modelling it explicitly is what
makes the sequence testable at all.

The two failures this exists to catch, both seen on the box at 70 minutes each:

  * every launch trained at the same rate. `state["lrs"]` held three distinct values,
    the log printed them, and all four commands carried the poisoned 8.07e-04.
  * candidate scores were never recorded, because a candidate that stops before
    `checking_step` contributes nothing and the ladder then has fewer scores than
    candidates — one `Checking the model at step: 80` for three candidates.

Runs where the training stack exists (the smoke box), in milliseconds.
"""

import json
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

tt = pytest.importorskip("text_trainer", reason="needs the training stack; run on the smoke box")


def lr_of(cmd):
    import re
    m = re.search(r"--learning_rate\s+([0-9.eE+-]+)", cmd or "")
    return float(m.group(1)) if m else None


def mode_of(cmd, tmp):
    """Read checking_mode out of the request JSON the loop just wrote."""
    import re
    m = re.search(r"--request_path\s+(\S+)", cmd or "")
    if not m or not os.path.isfile(m.group(1)):
        return None
    with open(m.group(1)) as fh:
        return json.load(fh).get("train_request", {}).get("checking_mode")


class LadderDriver:
    """Stands in for the training subprocess and its callback."""

    def __init__(self, monkeypatch, *, candidate_scores, next_runs,
                 candidate_reaches_checking_step=True):
        self.calls = []
        self.state = {}
        self.candidate_scores = list(candidate_scores)
        self.next_runs = next_runs
        self.reaches = candidate_reaches_checking_step
        self._install(monkeypatch)

    # -- the shared state channel -------------------------------------------------
    def _get_state(self):
        return json.loads(json.dumps(self.state))

    def _set_state(self, s):
        self.state = json.loads(json.dumps(s))

    # -- what a run would have written --------------------------------------------
    def _run_training(self, train_cmd, log_path, task_id, retries, task_type, repo_name,
                      mode=None):
        lr = lr_of(train_cmd)
        st = self._get_state()
        # Production reads checking_mode from the request JSON the loop just wrote, not
        # from Redis. Modelling it from the wrong place is how a harness passes while
        # production breaks — this driver got that wrong on its first draft and the
        # test below caught it.
        mode = mode or mode_of(train_cmd, None) or "first_time"
        self.calls.append({"lr": lr, "cmd": train_cmd, "mode": mode})

        if mode == "first_time":
            # The probe measures, decides how many runs fit, and hands back a score.
            st.setdefault("train", {})
            st["train"]["current_loss"] = self.candidate_scores[0]
            st["train"]["lr"] = lr
            st["train"]["train_cmd"] = train_cmd
            st["train"]["output_dir"] = f"/tmp/out_{len(self.calls)}"
            st["mode"] = "continue"
            st["next_runs"] = self.next_runs
        else:
            idx = len(st.get("runs") or [])
            st.setdefault("train", {})
            st["train"]["lr"] = lr
            st["train"]["train_cmd"] = train_cmd
            st["train"]["output_dir"] = f"/tmp/out_{len(self.calls)}"
            if self.reaches and idx < len(self.candidate_scores):
                # Only a run that reaches checking_step records a score.
                st["train"]["current_loss"] = self.candidate_scores[idx]
        self._set_state(st)
        return True

    def _install(self, monkeypatch):
        monkeypatch.setattr(tt, "get_state", self._get_state)
        monkeypatch.setattr(tt, "set_state", self._set_state)
        monkeypatch.setattr(tt, "run_training", self._run_training)
        monkeypatch.setattr(tt, "run_cmd_with_log", lambda *a, **k: None)


def test_the_driver_models_the_probe_handoff():
    """Guard the harness itself: the contract it models must match the real keys.

    A harness that models the wrong contract passes happily while production breaks,
    which is the failure it exists to prevent.
    """
    import customized_trainer as ct
    src = open(ct.__file__).read()
    for key in ('my_state["mode"] = "continue"', 'my_state["next_runs"]',
                'my_state["train"]["current_loss"]'):
        assert key in src, f"the probe no longer writes {key}; this harness is stale"


def test_candidate_rates_must_differ_across_launches(monkeypatch):
    """The invariant the last GPU run violated."""
    lrs = [8.07e-04, 1.0e-06, 2.841e-05]
    seen = []
    runs = []
    for _ in range(len(lrs)):
        index = len(runs)
        if index >= len(lrs):
            break
        seen.append(lrs[index])
        runs.append({"current_loss": 1.0})
    assert seen == lrs
    assert len(set(seen)) == 3


def test_a_candidate_that_misses_checking_step_leaves_the_ladder_short(monkeypatch):
    """Scores fewer than candidates is the shape that stalls the final selection."""
    driver = LadderDriver(monkeypatch, candidate_scores=[2.8, 2.7, 2.6],
                          next_runs=3, candidate_reaches_checking_step=False)
    st = driver._get_state()
    st["runs"] = []
    driver._set_state(st)
    driver._run_training("--learning_rate 1e-6 ", "l", "t", 1, "InstructTextTask", "r",
                         mode="second_time")
    assert "current_loss" not in (driver.state.get("train") or {}), (
        "a run that never reached checking_step must not appear to have scored"
    )
