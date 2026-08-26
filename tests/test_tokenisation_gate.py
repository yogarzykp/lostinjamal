"""Training must not launch against a dataset tokenisation never wrote.

This exists because of tourn_e758aac2d861c378_20260824, where it was the entire story.
A transformers/trl clash inside the axolotl venv made `import trl` raise, so tokenisation
wrote nothing. Nothing checked. The trainer launched anyway, died on FileNotFoundError,
and did that five times at roughly six seconds each before the noise fallback shipped a
perturbed base model. Three round-1 tasks, one cause, and every scored loss came back at
the untrained baseline — slightly worse than not training at all.

The gate's value is not the thirty seconds of futile retries it saves. It is that the
cause gets NAMED once, where it happens, instead of arriving as five identical stack
traces beneath a scoreboard line that reads as though we simply trained badly.

Two things it must get right, and the second is the one that would rot silently:

  the filenames        a gate that checks a name the trainer does not read is worse
                       than no gate — it passes forever and proves nothing
  zero rows            a split that collapses to [] parses, exists, is non-empty on
                       disk, and trains to completion on nothing

`run_cmd_with_log` surfaces no exit code, so the gate checks the artefact rather than the
status. That is the stronger check anyway: a tokeniser that exits 0 and writes nothing
fails this too.
"""

from __future__ import annotations

import ast
import json
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
TRAINER = os.path.join(SCRIPTS, "text_trainer.py")
DOCKERFILES = [
    os.path.join(ROOT, "ops", "docker", "standalone-text-trainer.dockerfile"),
    os.path.join(ROOT, "dockerfiles", "standalone-text-trainer.dockerfile"),
]

TASK_FILES = {
    "InstructTextTask": ("train_tokenized_{t}.json", "dev_tokenized_{t}.json"),
    "ChatTask": ("train_tokenized_{t}.json", "dev_tokenized_{t}.json"),
    "DpoTask": ("dpo_train_{t}.json", "dpo_dev_{t}.json"),
    "GrpoTask": ("grpo_train_{t}.json", "grpo_dev_{t}.json"),
}


def _source(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


@pytest.fixture
def gate(tmp_path, monkeypatch):
    """exec the gate alone — text_trainer imports transformers and yaml at module scope."""
    messages = []
    ns = {"os": os, "json": json, "print": lambda *a, **k: messages.append(" ".join(map(str, a)))}

    class _TT:
        INSTRUCTTEXTTASK = type("v", (), {"value": "InstructTextTask"})
        CHATTASK = type("v", (), {"value": "ChatTask"})
        DPOTASK = type("v", (), {"value": "DpoTask"})
        GRPOTASK = type("v", (), {"value": "GrpoTask"})

    ns["TaskType"] = _TT
    flag = annotations.compiler_flag
    for node in ast.parse(_source(TRAINER)).body:
        take = (isinstance(node, ast.FunctionDef) and node.name == "tokenisation_gate") or (
            isinstance(node, ast.Assign)
            and any(getattr(t, "id", "") == "TOKENISED_OUTPUTS" for t in node.targets)
        )
        if take:
            exec(compile(ast.Module(body=[node], type_ignores=[]), TRAINER, "exec", flags=flag), ns)  # noqa: S102
    assert "tokenisation_gate" in ns, "tokenisation_gate is not defined at module scope"
    monkeypatch.chdir(tmp_path)
    os.makedirs("datasets", exist_ok=True)
    fn = ns["tokenisation_gate"]
    fn.messages = messages
    return fn


def _write(task_type, task_id, rows_train=3, rows_dev=2, raw=None):
    for name, rows in zip(TASK_FILES[task_type], (rows_train, rows_dev)):
        path = os.path.join("datasets", name.format(t=task_id))
        with open(path, "w", encoding="utf-8") as fh:
            if raw is not None:
                fh.write(raw)
            else:
                json.dump([{"x": i} for i in range(rows)], fh)


def _log(text=""):
    path = "tokenise.log"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


# --- the healthy path must stay open ---------------------------------------------


@pytest.mark.parametrize("task_type", list(TASK_FILES))
def test_a_real_dataset_passes(gate, task_type):
    _write(task_type, "t1")
    assert gate("t1", task_type, _log()) is None


def test_an_unknown_task_type_is_not_blocked(gate):
    """Blocking what we do not understand would be a new way to lose a task."""
    assert gate("t1", "SomeFutureTask", _log()) is None


# --- and every way it can be empty must close it ----------------------------------


@pytest.mark.parametrize("task_type", list(TASK_FILES))
def test_nothing_written_is_caught(gate, task_type):
    """The observed failure: import error, tokeniser died, no output."""
    reason = gate("t1", task_type, _log("ImportError: cannot import name X"))
    assert reason and "never written" in reason


@pytest.mark.parametrize("missing", [0, 1])
def test_either_half_missing_is_caught(gate, missing):
    """train and dev are both required; the trainer opens both."""
    _write("InstructTextTask", "t1")
    os.remove(os.path.join("datasets", TASK_FILES["InstructTextTask"][missing].format(t="t1")))
    assert gate("t1", "InstructTextTask", _log()) is not None


def test_a_zero_byte_file_is_caught(gate):
    _write("InstructTextTask", "t1", raw="")
    reason = gate("t1", "InstructTextTask", _log())
    assert reason and "empty" in reason


def test_zero_rows_is_caught(gate):
    """The quiet one: [] parses, exists, is non-empty on disk, trains on nothing."""
    _write("InstructTextTask", "t1", raw="[]")
    reason = gate("t1", "InstructTextTask", _log())
    assert reason and "zero rows" in reason


def test_unparseable_json_is_caught(gate):
    _write("InstructTextTask", "t1", raw="{not json")
    reason = gate("t1", "InstructTextTask", _log())
    assert reason and "will not parse" in reason


# --- the filenames are the half that would rot silently ---------------------------


def test_the_gate_checks_the_names_the_trainers_actually_read():
    """A gate watching a filename nobody writes passes forever and proves nothing."""
    src = _source(TRAINER)
    tree = ast.parse(src)
    node = next(
        n for n in tree.body
        if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "TOKENISED_OUTPUTS" for t in n.targets)
    )
    literals = {c.value for c in ast.walk(node) if isinstance(c, ast.Constant) and isinstance(c.value, str)}
    for pair in TASK_FILES.values():
        for name in pair:
            assert name in literals, f"{name} is not in TOKENISED_OUTPUTS"


@pytest.mark.parametrize(
    "trainer,expected",
    [
        ("train_instruct.py", "train_tokenized_"),
        ("train_dpo.py", "dpo_train_"),
        ("train_grpo.py", "grpo_train_"),
    ],
)
def test_those_names_match_what_each_trainer_opens(trainer, expected):
    """Control against the source of truth rather than against this file's own table."""
    assert expected in _source(os.path.join(SCRIPTS, trainer))


# --- naming the cause is the whole point ------------------------------------------


def test_an_import_failure_is_called_out_as_one(gate):
    """Five identical six-second crashes are an environment fault, never a hyperparameter."""
    gate("t1", "InstructTextTask", _log("Traceback\nImportError: cannot import name 'X'\n"))
    blob = " ".join(gate.messages)
    assert "IMPORT failure" in blob
    assert "no retry of this task can fix it" in blob.replace("\n", " ")


def test_a_data_shaped_failure_is_not_blamed_on_the_image(gate):
    """Control — the import hint must not fire on every failure."""
    _write("InstructTextTask", "t1", raw="[]")
    gate("t1", "InstructTextTask", _log("wrote 0 rows after dedup"))
    assert "IMPORT failure" not in " ".join(gate.messages)


def test_the_tokenise_log_is_quoted(gate):
    """The cause is in the tokeniser's log; the trainer never got far enough to say."""
    gate("t1", "InstructTextTask", _log("line-one\nline-two\n"))
    blob = " ".join(gate.messages)
    assert "line-two" in blob


def test_an_unreadable_log_does_not_break_the_gate(gate):
    assert gate("t1", "InstructTextTask", "/no/such/log") is not None


# --- and it has to be wired ------------------------------------------------------


def test_the_gate_is_called_after_tokenisation():
    """A correct gate nobody calls is the defect class this repo keeps paying for."""
    tree = ast.parse(_source(TRAINER))
    calls = [
        n for n in ast.walk(tree)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "tokenisation_gate"
    ]
    assert calls, "tokenisation_gate is never called"


def test_the_gate_result_stops_the_training_loop():
    """It must set load_blocker — the existing break — not just print."""
    src = _source(TRAINER)
    i = src.index("_gate_reason = tokenisation_gate(")
    assert "load_blocker" in src[i : i + 400], (
        "the gate's verdict does not reach load_blocker, so training would launch anyway"
    )


# --- the pin that caused it all --------------------------------------------------


@pytest.mark.parametrize("path", DOCKERFILES)
def test_the_axolotl_venv_pins_its_own_stack(path):
    """trl==0.18.0 declares transformers>=4.50.0 with no upper bound.

    Left to the transitive graph the resolver was free to install a transformers that
    had dropped MODEL_FOR_VISION_2_SEQ_MAPPING_NAMES, which trl's lazy loader imports.
    """
    src = _source(path)
    i = src.index("axolotl==0.9.1")
    line = src[i : src.index("\n", i)]
    assert "transformers==4.51.3" in line, "transformers is not pinned in the axolotl resolve"
    assert "trl==0.18.0" in line, "trl is not pinned in the axolotl resolve"


@pytest.mark.parametrize("path", DOCKERFILES)
def test_the_image_proves_the_stack_imports_at_build_time(path):
    """A pin with no check is a hope: an edit that drops it fails only in a tournament."""
    src = _source(path)
    assert "from trl.trainer.dpo_trainer import DPOTrainer" in src, (
        "nothing proves the tokenisation stack imports before the image ships"
    )
    # The check imports several modules on one line, so match the names rather than a
    # sentence — the first version of this assertion looked for "import axolotl" and
    # failed against `import transformers, trl, axolotl, jinja2`, which is the thing it
    # was meant to accept.
    check = src[src.index("from trl.trainer.dpo_trainer") - 200 :][:400]
    for module in ("transformers", "trl", "axolotl", "jinja2"):
        assert module in check, f"the build-time check does not import {module}"


def test_both_dockerfiles_stay_identical():
    """TEXT_DOCKERFILE_PATHS tries the default then the legacy path; a fix in one only
    protects whichever the validator happens to pick."""
    a, b = (_source(p) for p in DOCKERFILES)
    assert a == b, "the two trainer dockerfiles have diverged"


# --- the packages that pushed the resolver ---------------------------------------

# Never install these in the axolotl venv: both declare an unbounded transformers
# requirement, so they PUSH the resolver upward rather than merely permitting it.
# langcheck wants transformers>=4.6, detoxify wants transformers with no bound at all.
TRANSFORMERS_PULLERS = ("langcheck", "detoxify")


def _axo_install_lines(path):
    """Only the executable install lines of the axolotl venv — never the comments.

    The comment above that block names langcheck and detoxify in order to record why
    they were removed. A substring check over the whole block matches that prose and
    fails against the very text that documents the fix.
    """
    src = _source(path)
    start = src.index("Create a virtual environment")
    block = src[start : src.index("# install the main dependencies", start)]
    return "\n".join(
        line for line in block.splitlines() if not line.lstrip().startswith("#")
    )


@pytest.mark.parametrize("path", DOCKERFILES)
@pytest.mark.parametrize("package", TRANSFORMERS_PULLERS)
def test_the_axolotl_venv_does_not_install_transformers_pullers(path, package):
    """The pin alone treats the symptom; this removes the pressure.

    The tokeniser imports none of the eleven packages that used to be installed here —
    verified across its whole local import tree, not just its own file. The position-1
    miner of the same tournament installs only axolotl and requests in this venv.
    """
    block = _axo_install_lines(path)
    assert package not in block, (
        f"{package} is back in the axolotl venv; it declares an unbounded transformers "
        f"requirement and is how the resolver moved off 4.51.3"
    )


@pytest.mark.parametrize("path", DOCKERFILES)
def test_the_build_check_covers_the_tokenisers_real_imports(path):
    """Assert the surface that actually runs, not a token sample of it.

    tokenize_instruct.py is the only thing executed from this venv, and it imports
    axolotl, transformers, torch, typer, yaml and requests. A check that imports fewer
    passes while the venv is missing something the tokeniser needs.
    """
    src = _source(path)
    check = src[src.index("from trl.trainer.dpo_trainer") - 300 :][:500]
    for module in ("axolotl", "transformers", "trl", "torch", "typer", "yaml", "requests"):
        assert module in check, f"the build-time check does not import {module}"


def test_the_tokeniser_still_imports_only_what_the_venv_provides():
    """Control tying the check above to source rather than to this file's own list."""
    tree = ast.parse(_source(os.path.join(SCRIPTS, "tokenize_instruct.py")))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    for package in TRANSFORMERS_PULLERS:
        assert package not in imported, (
            f"tokenize_instruct now imports {package}; the venv trim is no longer safe"
        )


def test_the_install_line_detector_can_bite():
    """Control: it must see a package that IS installed, and ignore the comments.

    Without this, a detector that accidentally strips everything would pass both
    assertions above forever.
    """
    for path in DOCKERFILES:
        lines = _axo_install_lines(path)
        assert "axolotl==0.9.1" in lines, "the detector dropped the install lines"
        assert "langcheck" not in lines
        assert "langcheck" in _source(path), (
            "the comment recording why langcheck was removed has itself been removed"
        )
