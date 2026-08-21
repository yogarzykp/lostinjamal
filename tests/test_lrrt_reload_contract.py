"""After the LR sweep, the trainer must be left able to train correctly.

The sweep runs ~100 optimizer steps up to 1e-2, so the weights it leaves behind are
ruined and the model is reloaded. Getting the reload itself right is not enough: what
the trainer holds AFTER the reload decides whether the run that follows is real.

Two faults lived in that block, both mine:

  * the scheduler was rebuilt with `max_steps if max_steps > 0 else 1`. On an
    epoch-driven run max_steps is -1, so it built a schedule for ONE step and the
    learning rate collapsed to its floor immediately after step 1 — a run that trains,
    logs, and learns almost nothing.
  * `Trainer.create_optimizer()` returns early when `self.optimizer` is already set, so
    rebuilding could leave an optimizer still holding parameters of the model that was
    just discarded.

Both are silent. The run completes, the logs look ordinary, and only the loss says
something is wrong — which is exactly the class of failure this repo keeps producing.
"""

import os
import re
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "scripts", "train_instruct.py")


def _code_lines(path):
    """The file with comment-only lines removed.

    Comments are stripped BEFORE any boundary is located, not after. This block explains
    why it no longer rebuilds the scheduler and why it clears the optimizer, so its prose
    contains both `create_optimizer_and_scheduler` and `trainer.train()` — and a boundary
    search over the raw text matches inside the explanation and truncates the block. Two
    drafts of this file failed against correct code that way.
    """
    return "\n".join(l for l in open(path).read().splitlines()
                     if not l.strip().startswith("#"))


def reload_block():
    """The finally-block that runs after the sweep, code only."""
    code = _code_lines(SRC)
    start = code.index("[lr-search] reloading model")
    end = code.index("trainer.train()", start)
    return code[start:end]


def test_the_scheduler_is_not_rebuilt_with_a_guessed_step_count():
    """`num_training_steps=1` is the shape that collapsed the learning rate."""
    block = reload_block()
    assert "create_optimizer_and_scheduler" not in block, (
        "the reload rebuilds the scheduler; at this point the real step count is not "
        "known, and the previous guess of 1 destroyed the schedule"
    )
    assert "else 1" not in block


def test_optimizer_and_scheduler_are_cleared_so_train_rebuilds_them():
    block = reload_block()
    assert re.search(r"trainer\.optimizer\s*=\s*None", block), (
        "a stale optimizer would still reference the discarded model's parameters"
    )
    assert re.search(r"trainer\.lr_scheduler\s*=\s*None", block)


def test_both_model_handles_are_replaced():
    """Trainer keeps model and model_wrapped; replacing only one leaves the ruined
    weights reachable."""
    block = reload_block()
    assert re.search(r"trainer\.model\s*=\s*_fresh", block)
    assert re.search(r"trainer\.model_wrapped\s*=\s*_fresh", block)


def test_the_reload_is_unconditional():
    """It sits in `finally`, so a sweep that raises still gets its weights discarded.

    The first GPU attempt OOM'd inside the sweep; without this the run would have
    continued on damaged weights and looked entirely normal.
    """
    src = open(SRC).read()
    i = src.index("[lr-search] reloading model")
    before = src[:i]
    # The nearest enclosing block opener before the reload must be `finally:`; anything
    # else means the reload is conditional on the sweep having succeeded.
    openers = [k for k in ("finally:", "except ", "else:") if k in before]
    last = max(before.rindex(k) for k in openers)
    assert before[last:].startswith("finally:"), (
        "the reload must run even when the sweep raises; the first GPU attempt OOM'd "
        "inside the sweep and would otherwise have trained on damaged weights"
    )


def test_hf_create_optimizer_really_does_return_early():
    """Guard the premise. If transformers changes this, the reasoning above is stale."""
    transformers = pytest.importorskip("transformers")
    import inspect

    src = inspect.getsource(transformers.Trainer.create_optimizer)
    assert "self.optimizer is None" in src, (
        "Trainer.create_optimizer no longer short-circuits on an existing optimizer; "
        "revisit why the reload clears it"
    )
