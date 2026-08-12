"""The WSM merge gate must actually arm, and must compare like with like.

This file exists because the gate was silently inert for weeks. `_perform_wsm_merge`
read `self.current_best_loss` for its baseline, but that attribute is only ever
assigned when state is restored from Redis or after an already-accepted merge — so
on an ordinary run it was None, the gate turned itself off, the backup copy was
skipped, and the averaged adapter overwrote the scored submission with no way back.
The run printed "ACCEPTED unverified" and looked fine.

Nothing in the trainer failed, so nothing caught it. These tests assert the two
properties that were violated:

  1. the baseline comes from the live best (`best_checkpoint_info`), so the gate
     arms on a normal run;
  2. the merge is never written when it cannot be measured.

`_perform_wsm_merge` is exercised through a stand-in that carries only the
attributes the method touches — importing the real callback would drag in
transformers, redis and wandb for logic that is pure file and float handling.
"""

import os
import sys
import types

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

# customized_trainer imports wandb and (via state_manager) redis at module scope.
# Neither takes part in merge admission, which is file copying and float
# comparison, so a stub keeps this suite runnable without the training extras.
for _name in ("wandb", "redis"):
    if _name not in sys.modules:
        try:
            __import__(_name)
        except ImportError:
            sys.modules[_name] = types.ModuleType(_name)


class _Callback:
    """Minimal stand-in bound to the real _perform_wsm_merge / _wsm_restore."""

    def __init__(self, submission_dir, pool, best_checkpoint_info=None,
                 current_best_loss=None, merge_eval_fn=None):
        self.submission_dir = str(submission_dir)
        self._wsm_pool = pool
        self.best_checkpoint_info = best_checkpoint_info
        self.current_best_loss = current_best_loss
        self.merge_eval_fn = merge_eval_fn
        self.logs = []

    def _print(self, *a, **k):
        self.logs.append(" ".join(str(x) for x in a))


def _bind_real_methods(cls):
    """Attach the production methods so the tests cannot drift from the source."""
    import customized_trainer as ct

    cls._perform_wsm_merge = ct.CustomEvalSaveCallback._perform_wsm_merge
    cls._wsm_restore = ct.CustomEvalSaveCallback._wsm_restore
    return cls


ADAPTER = "adapter_model.safetensors"


def _make_pool(tmp_path, losses):
    """Two or more checkpoint dirs, each holding a one-tensor adapter."""
    torch = pytest.importorskip("torch")
    from safetensors.torch import save_file

    pool = []
    for i, loss in enumerate(losses):
        d = tmp_path / f"ckpt-{i}"
        d.mkdir()
        save_file({"w": torch.full((4,), float(i + 1))}, str(d / ADAPTER))
        pool.append({"loss": float(loss), "step": (i + 1) * 100, "path": str(d)})
    return pool


def _make_submission(tmp_path):
    """The best-only adapter as it sits in submission_dir before any merge.

    adapter_config.json has to be here: _perform_wsm_merge treats its absence as
    "this is not a LoRA submission" and bails before the gate is reached.
    """
    torch = pytest.importorskip("torch")
    from safetensors.torch import save_file

    sub = tmp_path / "submission"
    sub.mkdir()
    save_file({"w": torch.zeros(4)}, str(sub / ADAPTER))
    (sub / "adapter_config.json").write_text('{"peft_type": "LORA"}')
    return sub


@pytest.fixture
def cb_cls():
    return _bind_real_methods(type("CB", (_Callback,), {}))


def _submission_tensor(sub):
    from safetensors.torch import load_file

    return load_file(str(sub / ADAPTER))["w"]


def test_gate_arms_from_best_checkpoint_info(cb_cls, tmp_path, capsys):
    """The regression itself: a normal run has best_checkpoint_info, not current_best_loss.

    Before the fix this wrote the merge and reported it unverified. The merge here
    evaluates WORSE than the best single checkpoint, so an armed gate must roll the
    submission back to what it was.
    """
    sub = _make_submission(tmp_path)
    pool = _make_pool(tmp_path, [0.40, 0.50])
    before = _submission_tensor(sub).clone()

    cb = cb_cls(
        submission_dir=sub,
        pool=pool,
        best_checkpoint_info={"loss": 0.40, "step": 100},
        current_best_loss=None,          # exactly the state that disarmed the gate
        merge_eval_fn=lambda: 0.90,      # merge is worse
    )
    cb._perform_wsm_merge()

    out = capsys.readouterr().out
    assert "REJECTED" in out, out
    assert "unverified" not in out
    assert _submission_tensor(sub).equal(before), "submission was not rolled back"
    assert not os.path.exists(str(sub / (ADAPTER + ".prewsm"))), "backup left in submission_dir"


def test_accepted_merge_replaces_submission(cb_cls, tmp_path, capsys):
    sub = _make_submission(tmp_path)
    pool = _make_pool(tmp_path, [0.40, 0.50])
    before = _submission_tensor(sub).clone()

    cb = cb_cls(
        submission_dir=sub,
        pool=pool,
        best_checkpoint_info={"loss": 0.40, "step": 100},
        merge_eval_fn=lambda: 0.10,      # merge is better
    )
    cb._perform_wsm_merge()

    out = capsys.readouterr().out
    assert "ACCEPTED" in out, out
    assert not _submission_tensor(sub).equal(before), "merge was not written"
    assert not os.path.exists(str(sub / (ADAPTER + ".prewsm")))
    assert cb.current_best_loss == pytest.approx(0.10)


def test_unmeasurable_merge_is_never_written(cb_cls, tmp_path, capsys):
    """No merge_eval_fn: keep the checkpoint we did measure, untouched."""
    sub = _make_submission(tmp_path)
    pool = _make_pool(tmp_path, [0.40, 0.50])
    before = _submission_tensor(sub).clone()

    cb = cb_cls(
        submission_dir=sub,
        pool=pool,
        best_checkpoint_info={"loss": 0.40, "step": 100},
        merge_eval_fn=None,
    )
    cb._perform_wsm_merge()

    out = capsys.readouterr().out
    assert "SKIPPED" in out, out
    assert _submission_tensor(sub).equal(before), "unverifiable merge overwrote the submission"
    assert not os.path.exists(str(sub / (ADAPTER + ".prewsm")))


def test_no_baseline_at_all_is_never_written(cb_cls, tmp_path, capsys):
    """Eval wired but no best recorded yet — still nothing to compare against."""
    sub = _make_submission(tmp_path)
    pool = _make_pool(tmp_path, [0.40, 0.50])
    before = _submission_tensor(sub).clone()

    cb = cb_cls(
        submission_dir=sub,
        pool=pool,
        best_checkpoint_info=None,
        current_best_loss=None,
        merge_eval_fn=lambda: 0.10,
    )
    cb._perform_wsm_merge()

    assert "SKIPPED" in capsys.readouterr().out
    assert _submission_tensor(sub).equal(before)


def test_failed_merge_evaluation_rolls_back(cb_cls, tmp_path, capsys):
    """compute_loss can now return inf on a KL failure; float(inf) must not be accepted."""
    sub = _make_submission(tmp_path)
    pool = _make_pool(tmp_path, [0.40, 0.50])
    before = _submission_tensor(sub).clone()

    def _boom():
        raise RuntimeError("CUDA out of memory")

    cb = cb_cls(
        submission_dir=sub,
        pool=pool,
        best_checkpoint_info={"loss": 0.40, "step": 100},
        merge_eval_fn=_boom,
    )
    cb._perform_wsm_merge()

    assert "REJECTED" in capsys.readouterr().out
    assert _submission_tensor(sub).equal(before)


def test_infinite_merge_metric_is_rejected(cb_cls, tmp_path, capsys):
    sub = _make_submission(tmp_path)
    pool = _make_pool(tmp_path, [0.40, 0.50])
    before = _submission_tensor(sub).clone()

    cb = cb_cls(
        submission_dir=sub,
        pool=pool,
        best_checkpoint_info={"loss": 0.40, "step": 100},
        merge_eval_fn=lambda: float("inf"),
    )
    cb._perform_wsm_merge()

    assert "REJECTED" in capsys.readouterr().out
    assert _submission_tensor(sub).equal(before)


def test_current_best_loss_is_only_a_fallback(cb_cls, tmp_path, capsys):
    """A Redis-restored loss still works when there is no live best yet."""
    sub = _make_submission(tmp_path)
    pool = _make_pool(tmp_path, [0.40, 0.50])

    cb = cb_cls(
        submission_dir=sub,
        pool=pool,
        best_checkpoint_info=None,
        current_best_loss=0.40,
        merge_eval_fn=lambda: 0.90,
    )
    cb._perform_wsm_merge()

    assert "REJECTED" in capsys.readouterr().out


def test_live_best_wins_over_stale_redis_value(cb_cls, tmp_path, capsys):
    """When both exist, the baseline must be this run's best, not the restored one.

    A previous probe run's loss is not a valid yardstick for this run's merge.
    Here the stale value (0.05) would reject the merge and the live best (0.40)
    accepts it; the live best must decide.
    """
    sub = _make_submission(tmp_path)
    pool = _make_pool(tmp_path, [0.40, 0.50])

    cb = cb_cls(
        submission_dir=sub,
        pool=pool,
        best_checkpoint_info={"loss": 0.40, "step": 100},
        current_best_loss=0.05,
        merge_eval_fn=lambda: 0.20,
    )
    cb._perform_wsm_merge()

    assert "ACCEPTED" in capsys.readouterr().out


def test_compute_loss_ignores_state():
    """_merge_eval calls compute_loss(None, metrics); that must stay safe.

    Both sides of the admission test now route through this one function so they
    cannot drift apart. If compute_loss ever starts reading `state`, that call
    breaks and this catches it.
    """
    import customized_trainer as ct

    cb = object.__new__(ct.CustomEvalSaveCallback)
    cb.kl_coef = None
    cb.kl_metric_fn = None
    assert ct.CustomEvalSaveCallback.compute_loss(cb, None, {"eval_loss": 1.25}) == 1.25

    cb.kl_coef = 1.5
    cb.kl_metric_fn = lambda: 0.2
    assert ct.CustomEvalSaveCallback.compute_loss(cb, None, {"eval_loss": 1.0}) == pytest.approx(1.3)
