"""Halving the GRPO batch must not emit a command TRL rejects at parse time.

TRL 0.18.0's GRPOConfig.__post_init__ requires num_generations to divide
generation_batch_size = per_device_train_batch_size * num_processes *
gradient_accumulation_steps, and to be >= 2 (grpo_config.py:517-545 in the pinned
venv). The OOM ladder halved only the batch. At b=1 / GA=4 / num_gen=8 the config
raises ValueError; at b=2 / GA=1 / num_gen=5 the same. Neither is an OOM, so
get_error_type does not classify it, so the remaining attempts re-run the identical
crash to exhaustion and the run ends in the noise fallback. The preflight measured
MiniCPM5-1B (batch 40 / num_gen 5 / GA 1) crashing at the second rung.

fit_grpo_generations rewrites num_generations to the largest valid divisor not above
the current one, and raises gradient_accumulation_steps when the effective batch is
too small for any num_generations at all.
"""

import importlib.machinery
import os
import re
import sys
import types

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
if "wandb" not in sys.modules:
    _w = types.ModuleType("wandb"); _w.__spec__ = importlib.machinery.ModuleSpec("wandb", None)
    sys.modules["wandb"] = _w

tt = pytest.importorskip("text_trainer", reason="needs the training stack; run on the pinned venv")


def _cmd(b, ga, ng):
    return (f"python train_grpo.py --per_device_train_batch_size {b} "
            f"--gradient_accumulation_steps {ga} --num_generations {ng} --use_vllm True")


def _vals(cmd):
    g = lambda k: int(re.search(rf"--{k} (\d+)", cmd).group(1))
    return g("per_device_train_batch_size"), g("gradient_accumulation_steps"), g("num_generations")


def _trl_accepts(b, ga, ng, world=1):
    gbs = b * world * ga
    return ng >= 2 and ng <= gbs and gbs % ng == 0


@pytest.mark.parametrize("b,ga,ng,world", [
    (1, 4, 8, 1),   # the b=1 rung the preflight named: gbs 4, ng 8 -> invalid
    (2, 1, 5, 1),   # MiniCPM5-1B's second rung
    (1, 1, 2, 1),   # gbs 1: no ng can divide it; GA must rise
    (3, 1, 6, 1),
    (1, 2, 8, 2),   # two GPUs
])
def test_every_rung_the_ladder_emits_is_accepted_by_trl(b, ga, ng, world):
    out = tt.fit_grpo_generations(_cmd(b, ga, ng), b, world)
    nb, nga, nng = _vals(out)
    assert nb == b, "the helper must not touch the batch the ladder chose"
    assert _trl_accepts(nb, nga, nng, world), (b, ga, ng, "->", nb, nga, nng)
    assert nng <= max(ng, 2), "num_generations must never grow past what the planner chose"


def test_a_valid_rung_is_left_alone():
    cmd = _cmd(4, 2, 8)  # gbs 8, ng 8 -> valid
    assert tt.fit_grpo_generations(cmd, 4, 1) == cmd


def test_non_grpo_commands_are_untouched():
    cmd = "python train_dpo.py --per_device_train_batch_size 2 --gradient_accumulation_steps 4"
    assert tt.fit_grpo_generations(cmd, 2, 1) == cmd


def test_the_ladder_calls_it_after_halving():
    src = open(os.path.join(os.path.dirname(tt.__file__), "text_trainer.py"), encoding="utf-8").read()
    i = src.index('"Reducing batch size from')
    assert "fit_grpo_generations(" in src[i:i + 1500], "the OOM ladder halves the batch without refitting num_generations"


def test_walking_a_real_planner_shape_to_batch_one_never_emits_an_invalid_rung():
    """The full walk the preflight ran: from the planner's batch down to 1."""
    b, ga, ng, world = 40, 1, 5, 1
    cmd = _cmd(b, ga, ng)
    while b > 1:
        b //= 2
        cmd = tt.replace_args_in_cmd(cmd, "per_device_train_batch_size", str(b))
        cmd = tt.fit_grpo_generations(cmd, b, world)
        nb, nga, nng = _vals(cmd)
        assert _trl_accepts(nb, nga, nng, world), (nb, nga, nng)


def test_the_emitted_rungs_construct_a_real_trl_grpo_config(tmp_path):
    """Not my restatement of TRL's rule — TRL's own __post_init__, from the pinned venv."""
    trl = pytest.importorskip("trl")
    from trl import GRPOConfig

    # planner-valid starting shapes; the ladder is responsible only for what halving does
    for b, ga, ng in [(2, 4, 8), (40, 1, 5), (2, 1, 2), (6, 1, 6), (3, 2, 6), (14, 4, 7)]:
        cmd = _cmd(b, ga, ng)
        GRPOConfig(output_dir=str(tmp_path), per_device_train_batch_size=b,
                   gradient_accumulation_steps=ga, num_generations=ng)  # precondition: start is valid
        # walk the ladder from the planner's batch to 1, as text_trainer would on 1 GPU
        cur = b
        while True:
            nb, nga, nng = _vals(cmd)
            GRPOConfig(output_dir=str(tmp_path), per_device_train_batch_size=nb,
                       gradient_accumulation_steps=nga, num_generations=nng)  # raises ValueError if invalid
            if cur <= 1:
                break
            cur //= 2
            cmd = tt.replace_args_in_cmd(cmd, "per_device_train_batch_size", str(cur))
            cmd = tt.fit_grpo_generations(cmd, cur, 1)


def test_the_unfitted_rung_really_is_rejected_by_trl(tmp_path):
    """The failure this guards against, reproduced with the real config class."""
    from trl import GRPOConfig
    with pytest.raises(ValueError):
        GRPOConfig(output_dir=str(tmp_path), per_device_train_batch_size=1,
                   gradient_accumulation_steps=4, num_generations=8)
