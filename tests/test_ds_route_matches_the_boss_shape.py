"""The ZeRO-3 route must take the shape a real tournament proved, not an untested one.

The ds branch has never executed: it needs >9e9 params AND >1 GPU, and no box we have
had is multi-GPU. It cannot be verified before the tournament, and the boss round
guarantees it fires (DpoTask, GrpoTask, and a 35-71B instruct task).

The retained boss of tourn_2ba0f79237bffcf7 — same transformers 4.51.3, same trl 0.18.0 —
ships a different shape, read from its published dpo_config.py / grpo_config.py:

    9_12_b   ds, 4 GPU, LoRA, batch 32, gradient_checkpointing: False
    12_14_b  ds, 4 GPU, LoRA, batch 24, gradient_checkpointing: False
    14_15_b  ds, 8 GPU, LoRA, batch 18, gradient_checkpointing: False
    15_40_b  ds, 8 GPU, LoRA,           gradient_checkpointing: False
    GRPO:    distributed "ddp" on every bucket — never ds at any size

Two consequences we adopt:

1. Checkpointing OFF whenever we emit ds. With gradient_checkpointing False,
   torch.utils.checkpoint is never called, so the CheckpointError that 4723787's
   use_reentrant fix exists to prevent becomes impossible rather than merely handled.
   That fix stays in place and goes inert on this path — the right relationship for a
   guard we cannot test.

2. GRPO never routes to ds. Beyond matching the boss, it removes the second reference
   model TRL builds under ZeRO-3 (grpo_trainer.py:557-558 precedes the is_peft_model
   branch) sitting alongside vLLM colocate on the same cards.

The cost is activation memory, which is not sharded by ZeRO-3 and which we also cannot
measure on one GPU. The boss carries it at 9-40B with LoRA on 4-8 GPUs and retained the
title; that is the only evidence either option has.
"""

import os
import re
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

SRC = open(os.path.join(ROOT, "scripts", "adaptive_config.py"), encoding="utf-8").read()


def _emit_block():
    """The run_config literal that carries distributed / gradient_checkpointing."""
    i = SRC.index('"distributed":')
    return SRC[i - 200:i + 600]


def test_checkpointing_is_not_hardcoded_true_beside_ds():
    block = _emit_block()
    assert '"gradient_checkpointing": "True",' not in block, (
        "gradient_checkpointing is still an unconditional True next to the ds route; "
        "the boss sets it False on every ds bucket"
    )


def test_grpo_never_routes_to_ds():
    """Boss: distributed 'ddp' on every GRPO bucket, at every size."""
    block = _emit_block()
    assert "grpo" in block, "the distributed decision does not consider the task type"


@pytest.mark.parametrize("task,params,gpus,want_dist,want_ckpt", [
    # ds only above 9e9 on more than one card, and never for grpo
    ("instruct", 14e9, 2, "ds", "False"),
    ("instruct", 40e9, 8, "ds", "False"),
    ("dpo", 14e9, 4, "ds", "False"),
    ("grpo", 14e9, 8, "ddp", "True"),   # boss shape: grpo stays ddp at every size
    ("grpo", 40e9, 8, "ddp", "True"),
    # unchanged below the gate or on one card — every run we have ever made
    ("instruct", 8e9, 8, "ddp", "True"),
    ("instruct", 14e9, 1, "ddp", "True"),
    ("dpo", 2e9, 1, "ddp", "True"),
])
def test_route_and_checkpointing_match_the_boss(task, params, gpus, want_dist, want_ckpt):
    import adaptive_config as ac
    dist, ckpt = ac.resolve_distributed_shape(task, params, gpus)
    assert (dist, ckpt) == (want_dist, want_ckpt), f"{task} {params:.0e} x{gpus} -> {dist}/{ckpt}"


def test_the_reentrant_guard_is_still_present_and_now_inert_on_ds():
    """4723787 stays: if a future change turns checkpointing back on under ZeRO-3, the
    seam must still choose reentrant. Belt and braces, deliberately."""
    for name in ("train_dpo.py", "train_grpo.py", "train_instruct.py"):
        src = open(os.path.join(ROOT, "scripts", name), encoding="utf-8").read()
        assert "is_deepspeed_zero3_enabled" in src, f"{name} lost the ZeRO-3 probe"
        assert "use_reentrant" in src, f"{name} lost the use_reentrant seam"
