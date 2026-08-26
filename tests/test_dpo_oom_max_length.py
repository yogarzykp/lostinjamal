"""The OOM ladder's last rung must actually reach the DPO trainer.

The ladder degrades sequence length only after batch size is already 1. It wrote the
new value into the request JSON and stopped there: `train_dpo.py` derives its own
max_length from the model config and never read the request back. So for DPO the
ladder ended at batch=1 — every remaining retry re-ran an identical command, retries
ran out, and the task submitted nothing at all. A scored zero, not a worse number.

Two things pin the fix, and the second matters more than the first. A correct
function nobody calls is the failure mode this repo keeps paying for, so there are
assertions here that the wire exists, not only that the logic is right.

Why the ladder writes a SEPARATE key. The healthy-path `max_length` comes from
`_select_max_length`, which mirrors the *axolotl* evaluator's halving rule. DPO is
scored by a different evaluator that reads max_position_embeddings with no halving
(G.O.D/validator/evaluation/eval_dpo.py:155). Reading plain `max_length` here would
therefore shorten every healthy DPO run to a length its own evaluator never uses —
a silent regression dressed as a fix. `oom_max_length` means one thing only: an OOM
forced this cap.

These tests read the two functions out of their source files with ast and exec them,
rather than importing the modules. train_dpo.py pulls trl, peft, torch and
transformers at module scope; none of them take part in choosing an integer, and a
suite that skips whenever the training extras are absent would not have caught this
defect on any machine we actually develop on.
"""

from __future__ import annotations  # noqa: F401 — used for compiler_flag in _extract

import ast
import json
import os
import sys
import tempfile

import pytest

SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
TRAIN_DPO = os.path.join(SCRIPTS, "train_dpo.py")
TEXT_TRAINER = os.path.join(SCRIPTS, "text_trainer.py")


def _source(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def _extract(path, func_name, namespace):
    """exec one top-level function out of a module, without importing the module.

    Compiled with the `annotations` future flag on purpose. These scripts run on a
    newer interpreter inside the trainer image and use `int | None` in signatures;
    evaluated eagerly that is a TypeError on 3.9, which is what this suite runs on.
    Deferring annotations tests the function's behaviour rather than the local
    interpreter's version.
    """
    tree = ast.parse(_source(path))
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            module = ast.Module(body=[node], type_ignores=[])
            code = compile(module, path, "exec", flags=annotations.compiler_flag)
            exec(code, namespace)  # noqa: S102
            return namespace[func_name]
    raise AssertionError(f"{func_name} is not defined at module scope in {path}")


@pytest.fixture
def resolve():
    logged = []
    ns = {"log_info": logged.append}
    fn = _extract(TRAIN_DPO, "resolve_dpo_max_length", ns)
    fn.logged = logged
    return fn


@pytest.fixture
def halve():
    ns = {
        "os": os,
        "json": json,
        "print": lambda *a, **k: None,
        "MIN_OOM_MAX_LENGTH": 512,
        "extract_value_from_cmd": lambda cmd, key: cmd.split(f"--{key} ")[1].split()[0]
        if f"--{key} " in cmd
        else None,
    }
    return _extract(TEXT_TRAINER, "halve_request_max_length", ns)


def _request_file(tmpdir, **train_request):
    path = os.path.join(tmpdir, "request.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"train_request": train_request}, fh)
    return path, f"python train.py --request_path {path} --task_id x"


# --- the rung has to be written -------------------------------------------------


def test_ladder_records_an_oom_specific_key(halve):
    """Halving max_length alone left DPO no signal it could act on."""
    with tempfile.TemporaryDirectory() as tmp:
        path, cmd = _request_file(tmp, max_length=2048)
        assert halve(cmd) == 1024
        with open(path, encoding="utf-8") as fh:
            written = json.load(fh)["train_request"]
        assert written["max_length"] == 1024
        assert written["oom_max_length"] == 1024, (
            "the rung must leave a key that means 'an OOM forced this', "
            "distinct from the planner's max_length"
        )


def test_ladder_writes_nothing_when_it_cannot_degrade(halve):
    """At the floor there is no rung left; it must not fabricate a cap."""
    with tempfile.TemporaryDirectory() as tmp:
        path, cmd = _request_file(tmp, max_length=512)
        assert halve(cmd) is None
        with open(path, encoding="utf-8") as fh:
            written = json.load(fh)["train_request"]
        assert "oom_max_length" not in written


# --- and DPO has to honour it ---------------------------------------------------


def test_lower_oom_cap_wins(resolve):
    assert resolve(4096, {"oom_max_length": 1024}) == 1024


def test_higher_oom_cap_is_ignored(resolve):
    """The ladder only ever degrades. A larger value is not a licence to grow."""
    assert resolve(2048, {"oom_max_length": 4096}) == 2048


def test_equal_oom_cap_changes_nothing(resolve):
    assert resolve(2048, {"oom_max_length": 2048}) == 2048


def test_absent_key_leaves_the_healthy_path_alone(resolve):
    assert resolve(4096, {}) == 4096


def test_plain_max_length_is_not_consulted(resolve):
    """The regression this fix must not introduce.

    The planner's max_length mirrors the axolotl evaluator's halving rule and is
    routinely below what DPO's own evaluator uses. Honouring it here would shorten
    every healthy DPO run.
    """
    assert resolve(4096, {"max_length": 1024}) == 4096


@pytest.mark.parametrize("bad", [None, "1024", 0, -1, 3.5, True, False, []])
def test_junk_cap_is_ignored(resolve, bad):
    assert resolve(4096, {"oom_max_length": bad}) == 4096


def test_non_dict_request_is_survivable(resolve):
    assert resolve(4096, None) == 4096


def test_capping_is_announced(resolve):
    resolve(4096, {"oom_max_length": 1024})
    assert any("4096" in m and "1024" in m for m in resolve.logged), (
        "a silent cap is indistinguishable from the inert behaviour being fixed"
    )


# --- the wire itself ------------------------------------------------------------


def test_main_actually_calls_the_resolver():
    """A correct function nobody calls is exactly the defect being fixed here."""
    tree = ast.parse(_source(TRAIN_DPO))
    main = next(
        (n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"),
        None,
    )
    assert main is not None, "train_dpo.py has no main()"
    called = {
        n.func.id
        for n in ast.walk(main)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
    }
    assert "resolve_dpo_max_length" in called, (
        "main() must route max_length through the resolver; otherwise the ladder "
        "is inert again and every test above passes while the bug is live"
    )


def test_resolver_result_reaches_training_args():
    """Assigned to training_args.max_length, not merely computed and dropped.

    Checked through the AST rather than by slicing the source, because the string
    "resolve_dpo_max_length(" matches its own def line first — the version of this
    test that searched text passed against a call site that did not exist.
    """
    tree = ast.parse(_source(TRAIN_DPO))
    main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main")

    resolved_into = set()
    for node in ast.walk(main):
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Call):
            continue
        fn = node.value.func
        if isinstance(fn, ast.Name) and fn.id == "resolve_dpo_max_length":
            resolved_into |= {t.id for t in node.targets if isinstance(t, ast.Name)}
    assert resolved_into, "main() never assigns the result of resolve_dpo_max_length"

    for node in ast.walk(main):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if (
                isinstance(target, ast.Attribute)
                and target.attr == "max_length"
                and isinstance(target.value, ast.Name)
                and target.value.id == "training_args"
                and isinstance(node.value, ast.Name)
                and node.value.id in resolved_into
            ):
                return
    raise AssertionError(
        "training_args.max_length is not assigned from the resolver's result — "
        "the value would be computed and then dropped, which is the original defect"
    )
