"""A probe that produced no usable loss must never take main() down with it.

Static analysis on 2026-09-13 found main() has no outer guard and two concrete
raisers on the LR-ladder path: `delete_poor_checkpoints` does `min([run["current_loss"]
...])` and the final-run selection does `np.argmin([run["current_loss"] ...])`. A
`None` there is TypeError; a run appended without the key is KeyError. Either is an
uncaught exception before the fallback, exit != 0, no upload — the forfeit shape.

Two real ways a run arrives without a finite loss:
  - `_probe_loss` fell back to `train_loss` on an eval failure, and log_history had no
    loss yet, so it returned None (customized_trainer.py ~:365-407).
  - the run was stopped by the end_time handler before checking_step: success.txt is
    written, the run is appended to state["runs"], and `current_loss` was never set
    (text_trainer.py ~:1250-1255 writes state["train"] without it).

customized_trainer._current_min_loss (:74-99) already applies the safe rule on ITS
side. These tests pin the same rule on the text_trainer side and on the probe scorer.
"""

import importlib.machinery
import os
import sys
import types

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

if "wandb" not in sys.modules:
    _w = types.ModuleType("wandb")
    _w.__spec__ = importlib.machinery.ModuleSpec("wandb", None)
    sys.modules["wandb"] = _w

tt = pytest.importorskip("text_trainer", reason="needs the training stack; run on the pinned venv")
ct = pytest.importorskip("customized_trainer")


# --- text_trainer side -----------------------------------------------------------------

def _run(tmp_path, name, loss="MISSING"):
    d = tmp_path / name
    d.mkdir()
    r = {"output_dir": str(d), "train_cmd": f"python x --learning_rate 1e-{name[-1]}", "lr": f"1e-{name[-1]}"}
    if loss != "MISSING":
        r["current_loss"] = loss
    return r


def test_delete_poor_checkpoints_survives_a_none_loss(tmp_path):
    runs = [_run(tmp_path, "run1", None), _run(tmp_path, "run2", 1.0), _run(tmp_path, "run3", 2.0)]
    tt.delete_poor_checkpoints(runs)  # TypeError today
    assert os.path.isdir(runs[1]["output_dir"]), "the best measured run was deleted"
    assert not os.path.isdir(runs[2]["output_dir"]), "a measured-worse run was kept"
    assert os.path.isdir(runs[0]["output_dir"]), "an UNMEASURED run is not a poor one; it must be kept"


def test_delete_poor_checkpoints_survives_a_missing_key(tmp_path):
    runs = [_run(tmp_path, "run1"), _run(tmp_path, "run2", 0.5)]
    tt.delete_poor_checkpoints(runs)  # KeyError today
    assert os.path.isdir(runs[0]["output_dir"]) and os.path.isdir(runs[1]["output_dir"])


def test_delete_poor_checkpoints_with_nothing_measured_deletes_nothing(tmp_path):
    runs = [_run(tmp_path, "run1"), _run(tmp_path, "run2", None), _run(tmp_path, "run3", float("nan"))]
    tt.delete_poor_checkpoints(runs)
    assert all(os.path.isdir(r["output_dir"]) for r in runs)


def test_best_probe_index_ignores_unmeasured_runs(tmp_path):
    runs = [_run(tmp_path, "run1", None), _run(tmp_path, "run2", 0.9), _run(tmp_path, "run3", 0.4)]
    assert tt.best_probe_index(runs) == 2


def test_best_probe_index_with_nothing_measured_picks_the_last_run_and_says_so(tmp_path, capsys):
    """No finite loss anywhere: the final run still needs a command. Take the most
    recent probe's and say so loudly, rather than raise and forfeit."""
    runs = [_run(tmp_path, "run1"), _run(tmp_path, "run2", None)]
    assert tt.best_probe_index(runs) == 1
    assert "no probe produced a finite loss" in capsys.readouterr().out


def test_main_uses_best_probe_index_not_a_bare_argmin():
    """The wire: the helper exists AND the call site uses it."""
    import ast
    src = open(os.path.join(ROOT, "scripts", "text_trainer.py"), encoding="utf-8").read()
    assert 'np.argmin([run["current_loss"] for run in state["runs"]])' not in src, (
        "main() still ranks probes with a bare argmin over current_loss"
    )
    assert "best_probe_index(state[\"runs\"])" in src or "best_probe_index(state['runs'])" in src


# --- customized_trainer side ----------------------------------------------------------

class _S:
    def __init__(self, log_history):
        self.log_history = log_history
        self.global_step = 100


def _cb(tmp_path):
    cb = ct.CustomEvalSaveCallback(
        function_when_to_evaluate=lambda *a, **k: False,
        submission_dir=str(tmp_path / "sub"), output_dir=str(tmp_path / "out"),
        original_model_name="x",
    )
    return cb


def test_probe_loss_ranks_a_failed_eval_last_instead_of_scoring_it_on_train_loss(tmp_path, capsys):
    """Siblings are scored on held-out loss; a probe whose eval failed must not enter
    the same ranking with a TRAINING loss — on DPO that is the quantity that prefers
    the most destructive LR. inf ranks it last, deterministically, and never raises."""
    cb = _cb(tmp_path)
    cb.probe_eval_fn = lambda: (_ for _ in ()).throw(RuntimeError("eval OOM"))
    got = cb._probe_loss(_S([{"loss": 2.5}]))
    assert got == float("inf"), f"got {got!r}; a failed eval was scored on train loss"
    assert "eval OOM" in capsys.readouterr().out


def test_probe_loss_never_returns_none_when_no_scorer_is_wired(tmp_path):
    cb = _cb(tmp_path)
    cb.probe_eval_fn = None
    assert cb._probe_loss(_S([])) == float("inf"), "None reached the ladder from a probe with no loss yet"
    assert cb._probe_loss(_S([{"loss": 1.25}])) == 1.25
