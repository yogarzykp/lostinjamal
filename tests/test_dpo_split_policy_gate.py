"""A DPO baseline was not a baseline while the split could not be switched off.

tokenize_instruct.py has gated its leak-safe split behind INSTRUCT_SPLIT_POLICY since the
split was introduced, for a stated reason: the split is a behavioural change like every
other, and a baseline measurement is only a baseline if every new mechanism is off.
tokenize_dpo.py ran the same split with no gate, so a DPO bisect could not attribute a
difference to the split rather than to anything changed alongside it.

That was not an oversight nobody had noticed — ops/smoke/run_dpo_smoke.sh recorded it as a
limit on what its own stages prove. Closing the gap therefore has to close the note too,
which is what the last test here is for: a limitation that has been lifted and still reads
as live sends the next person to work around something that no longer exists.

The switch is DPO_SPLIT_POLICY and deliberately not INSTRUCT_SPLIT_POLICY. Nothing on the
way to train_dpo.py reads the instruct one, and a single variable silently steering two
task types is how a bisect ends up measuring something it did not name.

The behavioural tests exec the module body rather than importing it — tokenize_dpo pulls
`datasets` and typer at import — and put scripts/ on sys.path so data.split_policy
resolves. That second part is load-bearing: without it both arms fall through to the
except and return identical sizes, which reads exactly like a gate that does nothing.
"""

import ast
import json
import os
import sys
import tempfile

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
DPO = os.path.join(SCRIPTS, "tokenize_dpo.py")
INSTRUCT = os.path.join(SCRIPTS, "tokenize_instruct.py")
SMOKE = os.path.join(ROOT, "ops", "smoke", "run_dpo_smoke.sh")

GATE = "DPO_SPLIT_POLICY"


def _source(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


@pytest.fixture(scope="module")
def split_dataset():
    """Load split_dataset with its module-level helpers, without importing the module."""
    if SCRIPTS not in sys.path:
        sys.path.insert(0, SCRIPTS)
    pytest.importorskip("data.split_policy")
    tree = ast.parse(_source(DPO))
    ns = {"os": os, "json": json, "print": lambda *a, **k: None}
    import random as _random
    import re as _re
    ns.update({"random": _random, "re": _re})
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.ClassDef)):
            continue
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            continue
        try:
            exec(compile(ast.Module(body=[node], type_ignores=[]), DPO, "exec"), ns)  # noqa: S102
        except Exception:
            pass
    assert "split_dataset" in ns, "split_dataset could not be loaded"
    return ns["split_dataset"]


@pytest.fixture
def run_split(split_dataset, monkeypatch):
    def _run(policy, rows=600, dev_size=200):
        if policy is None:
            monkeypatch.delenv(GATE, raising=False)
        else:
            monkeypatch.setenv(GATE, policy)
        data = [
            {"prompt": f"p{i}", "chosen": f"c{i}", "rejected": f"r{i}"}
            for i in range(rows)
        ]
        with tempfile.TemporaryDirectory() as d:
            total = os.path.join(d, "total.json")
            train = os.path.join(d, "train.json")
            dev = os.path.join(d, "dev.json")
            with open(total, "w") as fh:
                json.dump(data, fh)
            split_dataset(total, train, dev, seed=42, dev_size=dev_size)
            return len(json.load(open(train))), len(json.load(open(dev)))
    return _run


# --- the gate has to actually change something ----------------------------------


def test_gate_off_gives_the_legacy_slice(run_split):
    """Legacy is a fixed positional slice: dev is exactly dev_size, whatever the data."""
    train, dev = run_split("0", rows=600, dev_size=200)
    assert (train, dev) == (400, 200)


def test_gate_on_gives_the_proportional_split(run_split):
    train, dev = run_split("1", rows=600, dev_size=200)
    assert dev != 200, "the policy split returned the legacy dev size — it did not run"
    assert train + dev == 600


def test_the_two_arms_actually_differ(run_split):
    """Control. Without scripts/ on sys.path both arms fall through to the except
    clause and return the same sizes, which looks identical to a gate that does
    nothing — the first version of this check passed for exactly that reason."""
    assert run_split("0", rows=600) != run_split("1", rows=600)


def test_default_keeps_the_new_policy(run_split):
    """Unset must not silently mean legacy: the gate is for bisects, not a rollback."""
    assert run_split(None, rows=600) == run_split("1", rows=600)


@pytest.mark.parametrize("value", ["0", "no", "false", "", "2"])
def test_only_the_literal_one_enables_the_policy(run_split, value):
    """Mirrors tokenize_instruct.py's `!= "1"` — anything else is the legacy path."""
    assert run_split(value, rows=600) == run_split("0", rows=600)


# --- the switch must be DPO's own -----------------------------------------------


def _env_names_read(path):
    """Env var names actually passed to os.getenv, from the AST.

    Not a text search. tokenize_dpo.py's own comment names INSTRUCT_SPLIT_POLICY in
    order to explain why it does NOT read it, so a substring check matches the prose
    that exists to document the opposite of what it would be asserting.
    """
    names = set()
    for node in ast.walk(ast.parse(_source(path))):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "getenv"
            and node.args
            and isinstance(node.args[0], ast.Constant)
        ):
            names.add(node.args[0].value)
    return names


def test_the_dpo_file_does_not_read_the_instruct_switch():
    """One variable steering two task types makes a bisect measure what it did not name."""
    read = _env_names_read(DPO)
    assert "INSTRUCT_SPLIT_POLICY" not in read
    assert GATE in read, f"{GATE} is not read at all; the gate would be inert"


def test_the_env_detector_can_bite():
    """Control for the check above — it must see a real getenv."""
    assert "INSTRUCT_SPLIT_POLICY" in _env_names_read(INSTRUCT)


def test_the_instruct_gate_is_untouched():
    """Symmetry, not replacement — instruct keeps its own switch."""
    assert 'os.getenv("INSTRUCT_SPLIT_POLICY", "1")' in _source(INSTRUCT)


def test_the_gate_defaults_to_the_policy_in_source():
    src = _source(DPO)
    assert f'os.getenv("{GATE}", "1")' in src, (
        f"{GATE} must default to '1'; a default of off would change every DPO run"
    )


# --- and the note that documented the gap has to stop describing it -------------


def test_the_smoke_script_sets_the_gate_in_every_stage():
    src = _source(SMOKE)
    for stage in ("a", "b", "gap"):
        assert f"{GATE}=" in src, f"{GATE} is never set in {SMOKE}"
    assert src.count(f"export {GATE}=") == 3, (
        "expected the gate to be set once per stage (a, b, gap)"
    )


def test_the_baseline_stage_turns_the_split_off():
    """Stage a exists to reproduce what ran before. The split is a new mechanism."""
    src = _source(SMOKE)
    stage_a = src[src.index("\n  a)") : src.index("\n  b)")]
    assert f"export {GATE}=0" in stage_a, (
        "stage a leaves the leak-safe split on, so it is not a clean baseline"
    )


def test_the_lifted_limitation_no_longer_reads_as_live():
    """A limitation that has been closed and still reads as current is worse than none.

    The script used to say the split "cannot be switched off from here". It can now.
    """
    src = _source(SMOKE)
    assert "cannot be\n# switched off from here" not in src
    assert "has no equivalent of\n# INSTRUCT_SPLIT_POLICY" not in src
