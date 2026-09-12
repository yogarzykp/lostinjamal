"""A non-finite checkpoint metric is "no measurement", not a very bad one.

compute_loss returns +inf when the KL metric fails twice (customized_trainer.py
~:355-363) — ranking that checkpoint last is right. But on_evaluate only guarded
None, so inf flowed on: at the first eval it was PROMOTED (best is None, so "improved"
is trivially true), copied to the submission dir with loss inf, and every later inf
incremented no_improve_count until the patience-only early stop truncated the run.
The WSM merge then compared the merged loss against inf and accepted anything.

Reproduced on CPU by the preflight on 2026-09-13 (class 5). With a metric that fails
for the whole run, the first checkpoint ships — arbitrary — and the run stops early.
"""

import importlib.machinery
import math
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
        self.global_step, self.epoch, self.log_history = step, 1.0, [{"learning_rate": 1e-5}]


@pytest.fixture(autouse=True)
def _isolated(monkeypatch):
    monkeypatch.setenv("TRAINING_BEST_CKPT_PERSIST", "0")
    monkeypatch.delenv("EMIT_PER_EXAMPLE_LOSSES", raising=False)


def _cb(tmp_path):
    cb = ct.CustomEvalSaveCallback(
        function_when_to_evaluate=lambda *a, **k: False,
        submission_dir=str(tmp_path / "sub"), output_dir=str(tmp_path / "out"),
        original_model_name="x",
    )
    cb.early_stop_disabled = False
    cb.early_stop_patience = 2
    return cb


def _ev(cb, step, loss):
    cb.on_evaluate(args=None, state=_State(step), control=None, metrics={"eval_loss": loss})


def test_an_inf_eval_is_not_promoted_and_not_counted_against_patience(tmp_path, capsys):
    cb = _cb(tmp_path)
    _ev(cb, 100, float("inf"))
    assert cb.best_checkpoint_info is None, "an unmeasured checkpoint was promoted"
    assert cb.no_improve_count == 0
    assert cb.eval_history == [], "inf entered the smoothing window"
    assert "unranked" in capsys.readouterr().out


def test_a_run_of_inf_evals_does_not_trip_early_stop(tmp_path):
    cb = _cb(tmp_path)
    for step in (100, 200, 300, 400):
        _ev(cb, step, float("inf"))
    assert cb.no_improve_count == 0
    assert cb.best_checkpoint_info is None


def test_a_finite_eval_after_infs_is_the_first_promotion(tmp_path):
    cb = _cb(tmp_path)
    _ev(cb, 100, float("inf"))
    _ev(cb, 200, 0.7)
    assert cb.best_checkpoint_info == {"loss": 0.7, "step": 200}


def test_nan_is_treated_the_same(tmp_path):
    cb = _cb(tmp_path)
    _ev(cb, 100, float("nan"))
    assert cb.best_checkpoint_info is None and cb.no_improve_count == 0


def test_a_failed_kl_metric_flows_through_as_unranked(tmp_path, capsys):
    """End to end: kl_metric_fn raises twice -> compute_loss inf -> on_evaluate unranked."""
    cb = _cb(tmp_path)
    cb.kl_coef = 1.5
    cb.kl_metric_fn = lambda: (_ for _ in ()).throw(RuntimeError("KL OOM"))
    _ev(cb, 100, 0.5)
    out = capsys.readouterr().out
    assert "checkpoint metric unavailable" in out and "unranked" in out
    assert cb.best_checkpoint_info is None


def test_wsm_never_accepts_a_merge_against_an_inf_baseline(tmp_path, capsys):
    """Drives the real merge to the compare: two real adapter checkpoints in the
    pool, a real adapter submission, a merge that evaluates to 0.55, and a best
    single of inf. Today: `0.55 < inf` -> ACCEPTED, and the merge overwrites the
    submission on the strength of a number that was never measured."""
    import json
    import torch
    from safetensors.torch import save_file

    cb = _cb(tmp_path)
    sub = tmp_path / "sub"; sub.mkdir()
    (sub / "adapter_config.json").write_text(json.dumps({"peft_type": "LORA", "r": 2}))
    save_file({"w": torch.ones(2, 2)}, str(sub / "adapter_model.safetensors"))
    for k, val in (("a", 1.0), ("b", 3.0)):
        d = tmp_path / f"ckpt_{k}"; d.mkdir()
        save_file({"w": torch.full((2, 2), val)}, str(d / "adapter_model.safetensors"))
        cb._wsm_pool.append({"loss": float("inf"), "step": 1, "path": str(d)})
    cb.best_checkpoint_info = {"loss": float("inf"), "step": 100}
    cb.current_best_loss = float("inf")
    cb.merge_eval_fn = lambda: 0.55

    cb._perform_wsm_merge()

    out = capsys.readouterr().out
    assert "ACCEPTED" not in out, out
    assert "SKIPPED" in out, out
    from safetensors.torch import load_file
    kept = load_file(str(sub / "adapter_model.safetensors"))["w"]
    assert torch.equal(kept, torch.ones(2, 2)), "the unverifiable merge overwrote the submission"
