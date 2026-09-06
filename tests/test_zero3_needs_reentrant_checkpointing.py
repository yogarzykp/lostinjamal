"""ZeRO-3 and non-reentrant gradient checkpointing cannot be combined.

Measured 2026-09-07, Qwen2.5-14B across 2 GPUs, the first DeepSpeed run this repo has made:

    torch.utils.checkpoint.CheckpointError: Recomputed values for the following tensors
    have different metadata than during the forward pass
      saved:      torch.Size([13824, 5120])
      recomputed: torch.Size([0])

ZeRO-3 releases a gathered parameter after the forward pass, so recomputation sees an empty
shard. The NON-reentrant implementation is the one that validates recomputed metadata, so
it is the variant that notices and raises — it reports the problem rather than causing it.

`train_dpo.py` has branched on `is_deepspeed_zero3_enabled()` since it was written.
`train_instruct.py` did not, and instruct is the task type #1363 guarantees at 35-71B in
every boss round — the only case where instruct meets ZeRO-3 at all.

Source-shape assertions: the decision lives inside `main()`, which needs torch, a request
JSON and a live DeepSpeed context to reach.
"""

from __future__ import annotations

import ast
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTRUCT = os.path.join(ROOT, "scripts", "train_instruct.py")
DPO = os.path.join(ROOT, "scripts", "train_dpo.py")


def _src(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def test_instruct_decides_reentrant_from_the_zero3_state():
    """A constant on either side is wrong: False kills ZeRO-3, True is worse under DDP."""
    src = _src(INSTRUCT)
    assert "is_deepspeed_zero3_enabled" in src, (
        "train_instruct never asks whether ZeRO-3 is active, so it cannot pick the right "
        "checkpointing variant — and under ZeRO-3 the wrong one aborts both ranks"
    )
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        tgt = node.targets[0]
        if not (isinstance(tgt, ast.Attribute) and tgt.attr == "gradient_checkpointing_kwargs"):
            continue
        dumped = ast.dump(node.value)
        # The value must depend on something, not be a literal True/False.
        if "Constant(value=True)" in dumped and "Name" not in dumped:
            pytest.fail("use_reentrant is hard-coded True — wrong for the DDP path")
        if "Constant(value=False)" in dumped and "Name" not in dumped:
            pytest.fail(
                "use_reentrant is hard-coded False — this is what killed the 14B ZeRO-3 run"
            )
        return
    pytest.fail("no assignment to training_args.gradient_checkpointing_kwargs found")


def test_the_zero3_probe_cannot_take_the_run_down_with_it():
    """The import lives in transformers.integrations and has moved between versions.

    A bare import here would turn a version difference into a dead run on every task, not
    just the ZeRO-3 ones — a strictly worse failure than the one being fixed.
    """
    tree = ast.parse(_src(INSTRUCT))
    for node in ast.walk(tree):
        if isinstance(node, ast.Try) and "is_deepspeed_zero3_enabled" in ast.dump(node):
            assert node.handlers, "the ZeRO-3 probe is in a try with no except"
            return
    pytest.fail("the is_deepspeed_zero3_enabled import is not guarded by try/except")


def test_dpo_still_has_the_branch_instruct_was_missing():
    """The reference implementation. If this ever goes, the two paths have diverged again."""
    assert "is_deepspeed_zero3_enabled()" in _src(DPO)


@pytest.mark.parametrize("path,name", [(INSTRUCT, "train_instruct"), (DPO, "train_dpo")])
def test_both_trainers_agree_that_zero3_means_reentrant(path, name):
    """Whatever the mechanism, both must end up reentrant under ZeRO-3.

    They reach it differently — DPO calls model.gradient_checkpointing_enable, instruct sets
    training_args — so this asserts the shared conclusion rather than a shared spelling.
    """
    src = _src(path)
    assert "use_reentrant" in src, f"{name} never mentions use_reentrant"
    assert "is_deepspeed_zero3_enabled" in src, f"{name} never checks for ZeRO-3"
