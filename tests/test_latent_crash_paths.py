"""Four latent ways a run ends before it produces anything. None was reachable today.

They are grouped because they share a shape rather than a subsystem: each is a small
expression that works on every input it has actually been given, and raises or silently
poisons on an input nothing currently produces. That is why they sat in the audit as "low
priority" — and also why they are worth closing cheaply, since the thing that makes each
one reachable is an ordinary edit somewhere else.

  arg regexes      a flag as the command's LAST token did not match, and the miss
                   returned None straight into train_cmd
  batch override   "0" is truthy, so it was adopted, and batch=0 then divides
  LOCAL_RANK       int("") at module scope, so the import fails rather than the run
  .prewsm          a failed restore left a second adapter in the submission directory

The regex one is the one with teeth. Three of its six call sites are the OOM ladder's own
rungs, so the failure would land on a run already in trouble, and `train_cmd = None` is not
a degraded command — it is the next launch crashing on a value that was never a string.
"""

from __future__ import annotations

import ast
import os
import re
import warnings

import pytest

SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
TRAINER = os.path.join(SCRIPTS, "text_trainer.py")
ADAPTIVE = os.path.join(SCRIPTS, "adaptive_config.py")
CUSTOM = os.path.join(SCRIPTS, "customized_trainer.py")

RANK_FILES = ["train_instruct.py", "utility.py", "train_dpo.py", "customized_trainer.py", "train_grpo.py"]


def _source(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def _load(path, names, extra=None):
    ns = {"re": re, "os": os, "print": lambda *a, **k: None}
    ns.update(extra or {})
    flag = annotations.compiler_flag
    for node in ast.parse(_source(path)).body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            exec(compile(ast.Module(body=[node], type_ignores=[]), path, "exec", flags=flag), ns)  # noqa: S102
    missing = set(names) - ns.keys()
    assert not missing, f"could not load {missing} from {path}"
    return ns


@pytest.fixture(scope="module")
def cmd_helpers():
    return _load(TRAINER, {"_arg_pattern", "replace_args_in_cmd", "extract_value_from_cmd"})


# --- the argument regexes -------------------------------------------------------


BASE = "python train.py --model x --per_device_train_batch_size 8 --learning_rate 1e-4"


def test_a_trailing_flag_is_found(cmd_helpers):
    """The defect: the pattern required whitespace after the value."""
    assert cmd_helpers["extract_value_from_cmd"](BASE, "learning_rate") == "1e-4"


def test_a_trailing_flag_can_be_replaced(cmd_helpers):
    out = cmd_helpers["replace_args_in_cmd"](BASE, "learning_rate", "5e-5")
    assert "--learning_rate 5e-5" in out
    assert "1e-4" not in out


def test_a_middle_flag_still_works(cmd_helpers):
    """Control — the case that always worked must not have been traded away."""
    out = cmd_helpers["replace_args_in_cmd"](BASE, "per_device_train_batch_size", "4")
    assert "--per_device_train_batch_size 4" in out
    assert "--learning_rate 1e-4" in out


def test_trailing_whitespace_form_is_unaffected(cmd_helpers):
    assert cmd_helpers["extract_value_from_cmd"](BASE + " ", "learning_rate") == "1e-4"


def test_a_missing_flag_returns_the_command_not_none(cmd_helpers):
    """None went straight back into train_cmd at all six call sites, unchecked.

    Three of them are the OOM ladder's rungs, so the crash would land on a run that
    was already failing — turning a degraded retry into no checkpoint at all.
    """
    out = cmd_helpers["replace_args_in_cmd"](BASE, "not_a_flag", "x")
    assert out == BASE, "a missing flag must leave the command intact"
    assert out is not None


def test_extract_still_reports_absence_as_none(cmd_helpers):
    """Callers test extract's None; only replace's was a hazard."""
    assert cmd_helpers["extract_value_from_cmd"](BASE, "not_a_flag") is None


def test_the_pattern_is_a_raw_string():
    """It was an f-string, so \\s was an invalid escape Python kept with a warning."""
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        compile(_source(TRAINER), TRAINER, "exec")


def test_both_helpers_share_one_pattern():
    """A flag readable by one and invisible to the other is how a rung goes quiet."""
    tree = ast.parse(_source(TRAINER))
    users = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
        and any(
            isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "_arg_pattern"
            for n in ast.walk(node)
        )
    }
    assert {"replace_args_in_cmd", "extract_value_from_cmd"} <= users


# --- the batch override ---------------------------------------------------------


def _override_block():
    """The env-override statement, executed against a supplied batch and env."""
    src = _source(ADAPTIVE)
    start = src.index('env_batch = os.getenv("INSTRUCT_BATCH_OVERRIDE")')
    end = src.index("# EXP-HYPER-PORT-C", start)
    return "\n".join(line[4:] if line.startswith("    ") else line for line in src[start:end].splitlines())


@pytest.mark.parametrize("value,expected", [("16", 16), ("1", 1), ("0", 32), ("-8", 32), ("junk", 32)])
def test_only_a_positive_override_is_adopted(monkeypatch, value, expected):
    """"0" is truthy, so it passed the `if env_batch:` guard and was adopted.

    batch=0 then divides: `64 // total_batch`, and
    `num_samples * epochs // (batch * gpu_count)` in three places.
    """
    monkeypatch.setenv("INSTRUCT_BATCH_OVERRIDE", value)
    ns = {"os": os, "batch": 32, "print": lambda *a, **k: None}
    exec(_override_block(), ns)  # noqa: S102
    assert ns["batch"] == expected


def test_no_override_leaves_the_batch_alone(monkeypatch):
    monkeypatch.delenv("INSTRUCT_BATCH_OVERRIDE", raising=False)
    ns = {"os": os, "batch": 32, "print": lambda *a, **k: None}
    exec(_override_block(), ns)  # noqa: S102
    assert ns["batch"] == 32


# --- LOCAL_RANK at module scope -------------------------------------------------


def _rank_block(path):
    src = _source(path)
    start = src.index("try:\n    # Module scope")
    end = src.index("LOCAL_RANK = 0", start) + len("LOCAL_RANK = 0")
    return src[start:end]


@pytest.mark.parametrize("path", RANK_FILES)
def test_every_trainer_guards_its_rank(path):
    """Five files, not the four the audit note listed — customized_trainer was missed."""
    src = _source(os.path.join(SCRIPTS, path))
    assert 'LOCAL_RANK = int(os.getenv("LOCAL_RANK", "0"))' not in src, (
        f"{path} still parses the rank unguarded at module scope"
    )
    assert "LOCAL_RANK" in src


@pytest.mark.parametrize("value,expected", [("3", 3), ("0", 0), ("", 0), ("junk", 0)])
def test_rank_parsing_survives_any_value(monkeypatch, value, expected):
    """A set-but-EMPTY variable returns "" from getenv, not the default, and int("") raises.

    At module scope that is an ImportError, so the log carries a failed import rather
    than a cause and the subprocess dies before a step runs.
    """
    monkeypatch.setenv("LOCAL_RANK", value)
    ns = {"os": os, "print": lambda *a, **k: None}
    exec(_rank_block(os.path.join(SCRIPTS, "utility.py")), ns)  # noqa: S102
    assert ns["LOCAL_RANK"] == expected


def test_rank_parsing_handles_an_unset_variable(monkeypatch):
    monkeypatch.delenv("LOCAL_RANK", raising=False)
    ns = {"os": os, "print": lambda *a, **k: None}
    exec(_rank_block(os.path.join(SCRIPTS, "utility.py")), ns)  # noqa: S102
    assert ns["LOCAL_RANK"] == 0


# --- the stray backup -----------------------------------------------------------


def test_a_failed_restore_removes_the_backup():
    """The backup lives inside submission_dir, so the uploader would ship it.

    Structural: _wsm_restore is a method on a class that needs torch to import, and
    the defect is that a branch did not exist rather than that it computed wrongly.
    """
    tree = ast.parse(_source(CUSTOM))
    fn = next(
        n for n in ast.walk(tree)
        if isinstance(n, ast.FunctionDef) and n.name == "_wsm_restore"
    )
    handlers = [n for n in ast.walk(fn) if isinstance(n, ast.ExceptHandler)]
    assert handlers, "_wsm_restore no longer catches anything"
    removes = [
        n for h in handlers for n in ast.walk(h)
        if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Attribute)
        and n.func.attr == "remove"
    ]
    assert removes, (
        "a failed restore leaves the .prewsm backup beside the adapter and the "
        "submission ships two"
    )


def test_the_restore_failure_is_still_loud():
    """Removing the stray must not be mistaken for recovering the restore."""
    tree = ast.parse(_source(CUSTOM))
    fn = next(
        n for n in ast.walk(tree)
        if isinstance(n, ast.FunctionDef) and n.name == "_wsm_restore"
    )
    text = " ".join(
        n.value for n in ast.walk(fn)
        if isinstance(n, ast.Constant) and isinstance(n.value, str)
    )
    assert "RESTORE FAILED" in text
