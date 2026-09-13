"""The `ds`/`ddp` choice has to key on the GPUs the validator actually provisions.

`gpu_count >= 4` was calibrated against H100 counts. Text tournaments do not run on H100s:
validator/tournament/dstack_orchestrator.py picks H200s and converts the requirement by
TOTAL VRAM, so 4x H100 becomes ceil(4*80/141) = 3x H200 and 8x H100 becomes 5x H200.

That matters because #1363 (merged 2026-09-05) gives every text boss round a guaranteed
instruct task on a 35-71B model. The 35-40B half of that band lands on THREE GPUs, where
`>= 4` is false, so a 35B model would have trained under DDP — which replicates the whole
model on every GPU rather than sharding it. ZeRO-3 is what makes a model that size fit.

These are arithmetic assertions on the same expression the config builder uses, because the
builder itself needs torch and a live GPU probe to import.
"""

from __future__ import annotations

import ast
import math
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADAPTIVE = os.path.join(ROOT, "scripts", "adaptive_config.py")

H100_VRAM_GB = 80
H200_VRAM_GB = 141


def h200_count(h100_units: int) -> int:
    """The validator's own conversion, from dstack_orchestrator._get_h200_count_from_requirement."""
    return math.ceil(h100_units * H100_VRAM_GB / H200_VRAM_GB)


def _shape(param_count: float, gpu_count: int, task: str = "instruct"):
    """Run the shipped decision function, exec'd out of the source rather than re-typed.

    Re-typing it is how a test drifts into asserting what it wishes the code said. This
    used to eval the ternary at the "distributed" key; the decision now lives in
    resolve_distributed_shape (it also settles gradient_checkpointing, which has to move
    with it), so the function itself is what gets exec'd. It has no imports and no GPU
    probe, so this still needs neither torch nor a live device.
    """
    with open(ADAPTIVE, "r", encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "resolve_distributed_shape":
            mod = ast.Module(body=[node], type_ignores=[])
            ast.fix_missing_locations(mod)
            ns = {}
            exec(compile(mod, ADAPTIVE, "exec"), ns)  # noqa: S102 - our own source
            return ns["resolve_distributed_shape"](task, param_count, gpu_count)
    pytest.fail("no resolve_distributed_shape found in adaptive_config")


def _choice(param_count: float, gpu_count: int, task: str = "instruct") -> str:
    return _shape(param_count, gpu_count, task)[0]


# --- the band the boss round guarantees ---------------------------------------------


@pytest.mark.parametrize("params_b", [35.0, 38.0, 40.0])
def test_the_lower_half_of_the_boss_band_shards(params_b):
    """35-40B is a 4x-H100 requirement, which the validator serves as 3 H200s."""
    gpus = h200_count(4)
    assert gpus == 3, "the validator's conversion changed; re-derive this test"
    assert _choice(params_b * 1e9, gpus) == "ds", (
        f"{params_b}B on {gpus} GPUs chose DDP, which replicates the full model per GPU — "
        "70+ GB of weights before activations, and no sharding to make it fit"
    )


@pytest.mark.parametrize("params_b", [45.0, 71.0])
def test_the_upper_half_still_shards(params_b):
    gpus = h200_count(8)
    assert gpus == 5
    assert _choice(params_b * 1e9, gpus) == "ds"


# --- and the cases that must NOT change ---------------------------------------------


@pytest.mark.parametrize("params_b", [0.135, 1.5, 3.0, 8.0, 32.0])
def test_single_gpu_is_untouched(params_b):
    """Every run this repo has ever made was one GPU. None of them may move."""
    assert _choice(params_b * 1e9, 1) == "ddp"


@pytest.mark.parametrize("gpus", [1, 2, 3, 5, 8])
def test_a_small_model_never_shards(gpus):
    """ZeRO-3 on a model that fits is pure communication overhead."""
    assert _choice(3.0e9, gpus) == "ddp"


def test_the_boundary_is_the_param_threshold_not_the_gpu_count():
    """9e9 is the size line the original expression drew, and it is kept.

    Only the GPU-count half was wrong. A test that let both move could pass while the
    size threshold silently drifted.
    """
    assert _choice(9.0e9, 3) == "ddp", "at or below 9B should not shard"
    assert _choice(9.1e9, 3) == "ds", "above 9B on multiple GPUs should shard"



# --- the boss's shape, adopted because this path cannot be tested before it matters ---
#
# The retained boss of tourn_2ba0f79237bffcf7 (same transformers 4.51.3, same trl 0.18.0)
# sets gradient_checkpointing False on EVERY ds bucket, and routes GRPO to "ddp" at every
# size. Read from its published dpo_config.py (9_12_b / 12_14_b / 14_15_b / 15_40_b) and
# grpo_config.py. We adopt both: with checkpointing off, torch.utils.checkpoint is never
# called, so the CheckpointError the use_reentrant seam guards against becomes impossible
# rather than merely handled — and that seam stays in place, inert, in case this ever
# changes back.


@pytest.mark.parametrize("params_b,gpus", [(35.0, 3), (45.0, 5), (14.0, 2)])
def test_sharding_turns_gradient_checkpointing_off(params_b, gpus):
    dist, ckpt = _shape(params_b * 1e9, gpus)
    assert dist == "ds"
    assert ckpt == "False", (
        "ds with checkpointing ON is the only shape that can raise CheckpointError under "
        "ZeRO-3, and it is the one shape no box we have can test"
    )


@pytest.mark.parametrize("params_b,gpus", [(35.0, 3), (71.0, 5), (14.0, 8)])
def test_grpo_never_shards_at_any_size(params_b, gpus):
    """Boss: distributed 'ddp' on every GRPO bucket. It also avoids the second reference
    model TRL builds under ZeRO-3 sitting beside vLLM colocate on the same cards."""
    dist, ckpt = _shape(params_b * 1e9, gpus, task="grpo")
    assert (dist, ckpt) == ("ddp", "True")


@pytest.mark.parametrize("params_b,gpus", [(0.135, 1), (3.0, 8), (32.0, 1), (8.0, 4)])
def test_everything_below_the_gate_keeps_checkpointing_on(params_b, gpus):
    """Every run this repo has ever made. None may lose checkpointing."""
    assert _shape(params_b * 1e9, gpus) == ("ddp", "True")


def test_dpo_shards_like_instruct():
    assert _shape(14e9, 4, task="dpo") == ("ds", "False")
