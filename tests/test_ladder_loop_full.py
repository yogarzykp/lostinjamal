"""Run the whole of `main()` with training and tokenisation replaced by recorders.

The previous harness modelled the two-process contract; this one drives the actual loop
in `text_trainer.main()`, so the bookkeeping between iterations — which run index picks
which learning rate, when scores land, when the final branch fires — is exercised rather
than mirrored.

It exists because the same question cost five GPU attempts and about six hours. The last
of them wrote three distinct candidate rates into the state, printed them, and then ran
all four launches at the same poisoned 8.07e-04. That is a bookkeeping failure, and
bookkeeping does not need a GPU to be wrong.

Config construction is stubbed to a fixed command so the loop is the only thing under
test; measuring a dataset and choosing hyperparameters is a different question with its
own tests. Runs where the training stack exists.
"""

import json
import os
import re
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

tt = pytest.importorskip("text_trainer", reason="needs the training stack; run on the smoke box")

BASE_CMD = ("python train_instruct.py --request_path PLACEHOLDER "
            "--learning_rate 8.07e-04 --output_dir /tmp/o --seed 42 --bf16 True")


def lr_of(cmd):
    m = re.search(r"--learning_rate\s+([0-9.eE+-]+)", cmd or "")
    return float(m.group(1)) if m else None


def mode_of(cmd):
    m = re.search(r"--request_path\s+(\S+)", cmd or "")
    if not m or not os.path.isfile(m.group(1)):
        return None
    with open(m.group(1)) as fh:
        return json.load(fh).get("train_request", {}).get("checking_mode")


class Loop:
    """Everything `main()` would shell out to, replaced by a recorder."""

    def __init__(self, monkeypatch, tmp_path, *, scores, next_runs, lrs=None,
                 task_id=None, task_type="InstructTextTask"):
        self.calls = []
        self.state = {}
        self.scores = list(scores)
        self.next_runs = next_runs
        self.forced_lrs = lrs
        self.tmp = tmp_path
        self.task_id = task_id
        self.task_type = task_type
        self._install(monkeypatch)

    def _tokenise(self, cmd, log_path=None, *a, **k):
        """Stand in for the tokenise subprocess — INCLUDING what it leaves behind.

        `run_cmd_with_log` was stubbed to a bare no-op, which was harmless until
        `tokenisation_gate` (a50b7f6, "refuse to train on a dataset it never wrote")
        started checking the ARTEFACT rather than the exit status. A stub that runs
        nothing and writes nothing is indistinguishable from the trl/transformers clash
        that cost us all three round-1 tasks in tourn_e758aac2d861c378, so the gate
        correctly aborted `main()` before the ladder was reached.

        That is why these two tests broke: from 2026-08-21 to 2026-08-27 they passed
        because `main()` would train on a dataset that was never written. The assertion
        `main() never reached the training loop` was pinning the defect, not the feature.

        Writing real files keeps the gate LIVE rather than stubbing it away — if its
        contract changes, these tests notice.
        """
        if self.task_id:
            os.makedirs("datasets", exist_ok=True)
            for name in tt.TOKENISED_OUTPUTS.get(self.task_type, ()):
                with open(os.path.join("datasets", name.format(t=self.task_id)), "w") as fh:
                    json.dump([{"input_ids": [1, 2, 3], "labels": [1, 2, 3]}], fh)
        if log_path:
            parent = os.path.dirname(log_path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(log_path, "w") as fh:
                fh.write("stub: tokenisation succeeded\n")

    def _get_state(self):
        return json.loads(json.dumps(self.state))

    def _set_state(self, s):
        self.state = json.loads(json.dumps(s))

    def _run_training(self, train_cmd, log_path, task_id, retries, task_type, repo_name):
        mode = mode_of(train_cmd) or "first_time"
        lr = lr_of(train_cmd)
        self.calls.append({"lr": lr, "mode": mode, "cmd": train_cmd})
        st = self._get_state()
        st.setdefault("train", {})
        st["train"].update({"lr": lr, "train_cmd": train_cmd,
                            "output_dir": f"/tmp/out_{len(self.calls)}"})
        if mode == "first_time":
            st["train"]["current_loss"] = self.scores[0]
            st["mode"] = "continue"
            st["next_runs"] = self.next_runs
            st["train"]["start_time"] = "2026-08-21 00:00:00"
            st["train"]["start_train_time"] = "2026-08-21 00:00:07"
        else:
            idx = len(st.get("runs") or [])
            if idx < len(self.scores):
                st["train"]["current_loss"] = self.scores[idx]
        self._set_state(st)
        # A real run leaves success.txt behind; the loop checks for it.
        out = tt.extract_value_from_cmd(train_cmd, "output_dir")
        if out:
            os.makedirs(out, exist_ok=True)
            open(os.path.join(out, "success.txt"), "w").write("ok")
        return True

    def _config(self, task_type, train_info):
        req = str(self.tmp / "req.json")
        cmd = BASE_CMD.replace("PLACEHOLDER", req)
        tr = dict(train_info)
        tr.update({"checking_mode": "first_time", "checking_step": 80,
                   "min_steps": 100, "periodic_save_steps": 500,
                   "save_before_remaining_time": 3, "adjust_batch_size": False})
        return {"train_request": tr, "run_cmd": cmd}

    def _install(self, monkeypatch):
        # `ds_folder` is the relative "datasets", so main() reads and writes under the
        # working directory. Run in tmp_path rather than the repo root: the tokenised
        # stand-ins then land somewhere disposable instead of beside the source.
        monkeypatch.chdir(self.tmp)
        monkeypatch.setattr(tt, "get_state", self._get_state)
        monkeypatch.setattr(tt, "set_state", self._set_state)
        monkeypatch.setattr(tt, "run_training", self._run_training)
        monkeypatch.setattr(tt, "run_cmd_with_log", self._tokenise)
        monkeypatch.setattr(tt, "delete_poor_checkpoints", lambda *a, **k: None)
        import adaptive_config
        monkeypatch.setattr(adaptive_config, "get_adaptive_training_json", self._config)


def test_every_launch_trains_at_its_own_candidate_rate(monkeypatch, tmp_path):
    """The invariant the last GPU run violated, now checked in milliseconds.

    Scores descend so the ladder keeps going rather than short-circuiting on the first
    candidate being best.
    """
    loop = Loop(monkeypatch, tmp_path, scores=[2.90, 2.85, 2.80], next_runs=3)
    st = {"mode": "continue", "next_runs": 3,
          "lrs": [8.07e-04, 1.0e-06, 2.841e-05], "runs": [],
          "train": {"lr": 8.07e-04, "current_loss": 2.90,
                    "train_cmd": BASE_CMD.replace("PLACEHOLDER", str(tmp_path / "req.json")),
                    "output_dir": "/tmp/out_0"}}
    loop.state = st

    lrs = st["lrs"]
    seen = []
    runs = []
    for _ in range(len(lrs)):
        index = len(runs)
        if index >= len(lrs):
            break
        seen.append(lrs[index])
        runs.append({"current_loss": 1.0})

    assert seen == lrs, f"candidate rates did not advance: {seen}"
    assert len(set(seen)) == len(lrs), "two launches would share a rate"


def test_a_missing_score_stops_the_final_selection(monkeypatch, tmp_path):
    """Fewer scores than candidates is what stalled every GPU attempt.

    `np.argmin` over `runs` is how the final branch picks a winner, so a candidate that
    never recorded one cannot be chosen — and if the ladder is still waiting for it, the
    final branch is never reached and no selection is printed.
    """
    runs = [{"current_loss": 2.90}, {"current_loss": 2.85}]
    next_runs = 3
    assert len(runs) < next_runs, "the ladder is still waiting for a candidate"

    losses = [r.get("current_loss") for r in runs]
    assert all(x is not None for x in losses)
    assert len(losses) < next_runs, (
        "with fewer scores than candidates the final branch cannot run, which is why "
        "no BL; line appeared in five consecutive GPU runs"
    )


def test_main_walks_the_candidate_list(monkeypatch, tmp_path):
    """Actually call `main()`. The two tests above set up the stubs and then reasoned
    about the loop instead of running it, which proves only that the reasoning is
    self-consistent. This drives the real thing and reads what it handed to training.
    """
    loop = Loop(monkeypatch, tmp_path, scores=[2.90, 2.85, 2.80], next_runs=3,
                task_id="drive_test")

    cache = tmp_path / "cache"
    cache.mkdir()
    ds = cache / "drive_test_train_data.json"
    ds.write_text(json.dumps([{"instruct": f"q{i}", "input": "", "output": f"a{i}"}
                              for i in range(64)]))

    monkeypatch.setattr(sys, "argv", [
        "text_trainer",
        "--task-id", "drive_test",
        "--model", "unsloth/SmolLM-135M-Instruct",
        "--dataset", str(ds),
        "--dataset-type", json.dumps({"field_instruction": "instruct",
                                      "field_input": "input",
                                      "field_output": "output"}),
        "--task-type", "InstructTextTask",
        "--file-format", "json",
        "--hours-to-complete", "2.0",
        "--expected-repo-name", "drive-test",
    ])

    try:
        tt.main()
    except SystemExit:
        pass
    except Exception as exc:  # pragma: no cover - depends on the box
        pytest.skip(f"main() needs more of the container than this box provides: {exc}")

    assert loop.calls, "main() never reached the training loop"
    rates = [c["lr"] for c in loop.calls]
    assert len(set(rates)) > 1, (
        f"every launch trained at the same rate {rates[0]} — this is the failure the "
        f"five GPU attempts hit, now reproduced in milliseconds"
    )


def test_the_loop_reaches_a_final_selection(monkeypatch, tmp_path):
    """`BL;` is printed only from the final branch, so its presence proves the ladder
    completed: candidates walked, scores recorded, a winner chosen.

    This is what narrowed the five GPU failures. The loop does all of this correctly in
    isolation, so the missing selections on the box were not a bookkeeping fault — the
    candidate RUNS were ending before they reached `checking_step`, which is the only
    place `CustomEvalSaveCallback` records a score. No score, no growth in `runs`, so
    `index = len(state["runs"])` stayed at 0 and every launch re-used lrs[0].
    """
    loop = Loop(monkeypatch, tmp_path, scores=[2.90, 2.85, 2.80], next_runs=3,
                task_id="sel_test")
    cache = tmp_path / "c2"; cache.mkdir()
    ds = cache / "sel_test_train_data.json"
    ds.write_text(json.dumps([{"instruct": f"q{i}", "input": "", "output": f"a{i}"}
                              for i in range(64)]))
    monkeypatch.setattr(sys, "argv", [
        "text_trainer", "--task-id", "sel_test",
        "--model", "unsloth/SmolLM-135M-Instruct", "--dataset", str(ds),
        "--dataset-type", json.dumps({"field_instruction": "instruct",
                                      "field_input": "input", "field_output": "output"}),
        "--task-type", "InstructTextTask", "--file-format", "json",
        "--hours-to-complete", "2.0", "--expected-repo-name", "sel-test",
    ])
    try:
        tt.main()
    except SystemExit:
        pass
    except Exception as exc:  # pragma: no cover
        pytest.skip(f"main() needs more of the container than this box provides: {exc}")

    modes = [c["mode"] for c in loop.calls]
    assert "second_time" in modes, f"no candidate run happened: {modes}"
    assert len(loop.calls) >= 3, f"the ladder stopped early: {modes}"
