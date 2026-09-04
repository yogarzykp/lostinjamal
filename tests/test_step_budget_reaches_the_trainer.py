"""A step cap that never reaches the trainer is a log line, not a cap.

`adaptive_config` computed `run_config["max_steps"]` — from the GRPO caps and from the
"EXP-T universal cap" at the run_config exit — printed it, and dropped it. The chain broke
in TWO places, and fixing either one alone leaves the cap just as dead:

    run_config["max_steps"]     -> train_request["max_steps"]      never copied
    train_request["max_steps"]  -> training_args.max_steps         only reached the
                                                                   eval/save callback

`train_instruct.py` reads `train_request["max_steps"]`, which still carried
`args.max_steps` (-1) from `text_trainer.py:904`; and `training_args` comes from
`HfArgumentParser`, i.e. the command line, which never carries `--max_steps`. Measured
2026-09-04 on d99ce208 / falcon-rw-1b: the config logged `max_steps=499` while the trainer
logged `max_steps: -1` and ran a 750-step progress bar identical to the uncapped control.

So every `EXP-T universal cap fires: ... -> max_steps=N` line ever emitted on an instruct
run reported a decision that was discarded. Same seam as the max_length bug — see
tests/test_max_length_reaches_the_family_profile.py, whose fix sits ten lines above the
hole this file guards.

These are source-shape assertions rather than behavioural ones because both statements live
hundreds of lines inside functions that need torch, a GPU and a real dataset to reach. The
shape is the whole defect: the value was correct, and nothing carried it.
"""

from __future__ import annotations

import ast
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADAPTIVE = os.path.join(ROOT, "scripts", "adaptive_config.py")
TRAINER = os.path.join(ROOT, "scripts", "train_instruct.py")


def _source(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def _tree(path):
    return ast.parse(_source(path))


def _is_subscript_of(node, name, key):
    """True for `name["key"]` written as an expression node."""
    return (
        isinstance(node, ast.Subscript)
        and isinstance(node.value, ast.Name)
        and node.value.id == name
        and isinstance(node.slice, ast.Constant)
        and node.slice.value == key
    )


# --- break 1: run_config -> train_request ------------------------------------------


def test_the_cap_is_copied_into_the_request_dict():
    """Without this the trainer reads args.max_steps (-1) and runs the full epoch plan."""
    hits = [
        n for n in ast.walk(_tree(ADAPTIVE))
        if isinstance(n, ast.Assign)
        and any(_is_subscript_of(t, "train_request", "max_steps") for t in n.targets)
        and _is_subscript_of(n.value, "run_config", "max_steps")
    ]
    assert hits, (
        "adaptive_config never assigns train_request['max_steps'] = run_config['max_steps'], "
        "so every cap it computes is discarded before the trainer can see it"
    )


def test_the_copy_cannot_switch_grpo_and_dpo_on_by_itself():
    """This one line is enough to activate capping on paths the A/Bs never measured.

    train_grpo.py and train_dpo.py never touch training_args.max_steps either — but they
    pass the request value to CustomEvalSaveCallback, and customized_trainer.py:884 sets
    control.should_training_stop when global_step == max_steps. The GRPO branch of
    adaptive_config ALWAYS writes run_config["max_steps"] (the budget cap, plus the <500M
    drift cap), so an unguarded copy switches both on at once — on a path whose metric runs
    the other way, higher-wins, where -0.0124/-0.0430 nats of instruct evidence says nothing.

    So the copy must sit behind the same opt-in as the cap.
    """
    tree = _tree(ADAPTIVE)
    for node in ast.walk(tree):
        if not isinstance(node, ast.If):
            continue
        assigns = [
            n for n in ast.walk(node)
            if isinstance(n, ast.Assign)
            and any(_is_subscript_of(t, "train_request", "max_steps") for t in n.targets)
            and _is_subscript_of(n.value, "run_config", "max_steps")
        ]
        if not assigns:
            continue
        # The guard must reach the opt-in, directly or through a name bound to it.
        if "_cap_opt_in" in ast.dump(node.test) or "EXPT_" in ast.dump(node.test):
            return
    pytest.fail(
        "the train_request['max_steps'] copy is not behind the cap opt-in, so GRPO and DPO "
        "start capping by default on evidence that only covers instruct"
    )


def test_that_copy_is_guarded_so_an_uncapped_run_keeps_its_minus_one():
    """Instruct leaves the key absent unless a cap fires; an unguarded copy would KeyError."""
    tree = _tree(ADAPTIVE)
    for node in ast.walk(tree):
        if not isinstance(node, ast.If):
            continue
        assigns = [
            n for n in ast.walk(node)
            if isinstance(n, ast.Assign)
            and any(_is_subscript_of(t, "train_request", "max_steps") for t in n.targets)
            and _is_subscript_of(n.value, "run_config", "max_steps")
        ]
        if assigns and "max_steps" in ast.dump(node.test):
            return
    pytest.fail(
        "the train_request['max_steps'] copy is not inside an `if ... max_steps ...` guard; "
        "on an instruct run that was never capped the key is absent and this raises KeyError"
    )


# --- break 2: train_request -> training_args ----------------------------------------


def test_the_request_cap_is_applied_to_training_args():
    """HF's Trainer reads training_args.max_steps. Nothing else bounds the run."""
    hits = [
        n for n in ast.walk(_tree(TRAINER))
        if isinstance(n, ast.Assign)
        and any(
            isinstance(t, ast.Attribute)
            and t.attr == "max_steps"
            and isinstance(t.value, ast.Name)
            and t.value.id == "training_args"
            for t in n.targets
        )
    ]
    assert hits, (
        "train_instruct never assigns training_args.max_steps, so a cap that survives the "
        "request JSON still does not bound training — it only reaches the eval callback"
    )


def test_the_trainer_side_only_applies_a_positive_cap():
    """-1 means uncapped. Writing it through would be harmless but writing 0 would not."""
    src = _source(TRAINER)
    assert "max_steps > 0" in src, (
        "the training_args assignment is not gated on max_steps > 0, so a 0 or -1 from the "
        "request could be handed to HF as a real step budget"
    )


# --- and the cap must not fire on its own, because firing was measured to cost ------


def test_the_universal_cap_does_not_fire_without_an_explicit_opt_in():
    """Wiring the chain up turns a previously inert branch ON. Two equal-budget A/Bs on
    d99ce208 measured the capped arm WORSE in both regimes — -0.0124 nats at 66%
    truncation and -0.0430 at 16%, winning 197 and 76 of 1000 examples. A truncated cosine
    is just a higher-LR schedule, and the higher LR trained better. So the default must
    stay off; only an explicit EXPT_BUDGET_CAP=1 may enable it."""
    src = _source(ADAPTIVE)
    assert "EXPT_BUDGET_CAP" in src, (
        "no opt-in flag guards the universal cap — now that the wire is connected it would "
        "fire by default, which was measured to lose 0.012-0.043 nats"
    )
    tree = _tree(ADAPTIVE)
    for node in ast.walk(tree):
        if not isinstance(node, ast.If):
            continue
        if "EXPT_BUDGET_CAP" not in ast.dump(node.test):
            continue
        capped = [
            n for n in ast.walk(node)
            if isinstance(n, ast.Assign)
            and any(_is_subscript_of(t, "run_config", "max_steps") for t in n.targets)
            and isinstance(n.value, ast.Name)
            and n.value.id == "_budget_max_steps"
        ]
        if capped:
            return
    pytest.fail(
        "the universal cap's assignment is not inside an EXPT_BUDGET_CAP branch, so it "
        "fires by default"
    )
