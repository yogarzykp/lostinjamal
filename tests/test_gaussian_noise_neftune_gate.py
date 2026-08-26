"""The GAUSSIAN_NOISE branch must not claim a change it did not make.

What was here wrote `instruct_hp["neftune_alpha"]` and printed that NEFTune had been
turned off. Nothing in the repository reads that key — every consumer reads
`neftune_noise_alpha` — so the write was inert and the print was false.

The second half is the one worth remembering. The write sat behind
`if instruct_hp is not None`, and that gate is inverted relative to the risk: it admits
only the branch where NEFTune is already 0 for all eight family profiles, and skips the
branch that actually ships 5.0 (an instruct task with ADAPTIVE_INSTRUCT_FAMILY=0). Live
where there was nothing to fix, silent where there was. Repairing the key alone would
therefore have restored nothing while reading like a fix.

So the branch is now env-gated and neutral by default, following the MAGNITUDE_PRUNING
precedent a few lines above it, and for the same stated reason: the action was never
measured. The trigger is an RMS-ratio band of (1.0001, 1.005) whose false-positive rate
is not established here, and a false fire would strip a regulariser from a task that was
never augmented. Confidence is a hardcoded 0.6 for this pattern, so a confidence
threshold would discriminate nothing and is deliberately absent rather than added as
reassurance.

These are structural tests, read out of the AST. `build_adaptive_run_config` is a
thousand-line function that cannot be exercised as a unit, and the defect was never in
arithmetic — it was in which key was written and which branch could reach it. Testing the
wire is testing the bug.
"""

import ast
import os

import pytest

SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
ADAPTIVE = os.path.join(SCRIPTS, "adaptive_config.py")

GATE_ENV = "AUG_GAUSSIAN_NEFTUNE_OFF"
OVERRIDE = "_aug_neftune_override"


@pytest.fixture(scope="module")
def tree():
    with open(ADAPTIVE, "r", encoding="utf-8") as fh:
        return ast.parse(fh.read())


@pytest.fixture(scope="module")
def source():
    with open(ADAPTIVE, "r", encoding="utf-8") as fh:
        return fh.read()


def _gaussian_branch(tree):
    """The `elif detected_type == "GAUSSIAN_NOISE"` body, found structurally."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.If):
            continue
        for cmp_node in ast.walk(node.test):
            if (
                isinstance(cmp_node, ast.Constant)
                and cmp_node.value == "GAUSSIAN_NOISE"
                and isinstance(node.test, ast.Compare)
            ):
                return node
    raise AssertionError("no branch tests for GAUSSIAN_NOISE in adaptive_config.py")


def _subscript_keys_written(node):
    """Every string key K in an assignment of the form something[K] = ..."""
    keys = set()
    for n in ast.walk(node):
        if not isinstance(n, ast.Assign):
            continue
        for target in n.targets:
            if isinstance(target, ast.Subscript) and isinstance(target.slice, ast.Constant):
                if isinstance(target.slice.value, str):
                    keys.add(target.slice.value)
    return keys


# --- the dead key ---------------------------------------------------------------


def test_the_orphan_key_is_never_written(tree):
    """`neftune_alpha` is read by nothing. Writing it is writing to /dev/null."""
    written = _subscript_keys_written(tree)
    assert "neftune_alpha" not in written, (
        "neftune_alpha is assigned somewhere; every consumer reads neftune_noise_alpha"
    )


def test_the_real_key_is_still_used(tree):
    """Control: the check above must be able to see keys at all."""
    assert "neftune_noise_alpha" in _subscript_keys_written(tree)


def test_branch_writes_the_key_consumers_read(tree):
    branch = _gaussian_branch(tree)
    written = _subscript_keys_written(branch)
    assert written, "the branch assigns no dict key at all"
    assert written == {"neftune_noise_alpha"}, f"unexpected keys written: {written}"


# --- the gate -------------------------------------------------------------------


def _getenv_calls(node):
    out = []
    for n in ast.walk(node):
        if (
            isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute)
            and n.func.attr == "getenv"
            and n.args
            and isinstance(n.args[0], ast.Constant)
        ):
            default = n.args[1].value if len(n.args) > 1 and isinstance(n.args[1], ast.Constant) else None
            out.append((n.args[0].value, default))
    return out


def test_branch_is_env_gated(tree):
    """Unmeasured actions do not fire by default in this file — see MAGNITUDE_PRUNING."""
    names = [name for name, _ in _getenv_calls(_gaussian_branch(tree))]
    assert GATE_ENV in names, f"the branch reads no {GATE_ENV} gate"


def test_gate_defaults_to_neutral(tree):
    """The default must leave training untouched."""
    calls = dict(_getenv_calls(_gaussian_branch(tree)))
    assert calls[GATE_ENV] == "0", (
        f"{GATE_ENV} defaults to {calls[GATE_ENV]!r}; an unmeasured action must default off"
    )


def test_no_confidence_threshold_is_faked(source):
    """confidence is a hardcoded 0.6 for this pattern, so a threshold gates nothing.

    Pinned so nobody adds one later as reassurance. If detect_augmentation ever starts
    computing a real confidence for GAUSSIAN_NOISE, delete this test along with the
    comment it guards.
    """
    branch_src = source[source.index('"GAUSSIAN_NOISE"') :][:3000]
    assert "confidence" not in branch_src.split("if os.getenv")[1][:800], (
        "a confidence gate was added; verify detect_augmentation computes one first"
    )


# --- both paths, which is the half the old code missed ---------------------------


def test_override_is_initialised_before_the_augmentation_branches(tree, source):
    """It must exist even when no augmentation is detected."""
    assert f"{OVERRIDE} = None" in source, f"{OVERRIDE} is never initialised"
    assert source.index(f"{OVERRIDE} = None") < source.index('"GAUSSIAN_NOISE"'), (
        "the override is initialised after the branch that sets it"
    )


def test_gated_on_sets_both_the_override_and_instruct_hp(tree):
    """instruct_hp alone is not enough — it is None on the path carrying 5.0."""
    branch = _gaussian_branch(tree)
    assigned = {
        t.id
        for n in ast.walk(branch)
        if isinstance(n, ast.Assign)
        for t in n.targets
        if isinstance(t, ast.Name)
    }
    assert OVERRIDE in assigned, (
        f"{OVERRIDE} is never set; the instruct_hp-is-None path would stay at 5.0, "
        "which is the only path where the value was ever non-zero"
    )
    assert "neftune_noise_alpha" in _subscript_keys_written(branch), (
        "instruct_hp is not updated, so the adaptive log would report a stale value"
    )


def test_run_config_consults_the_override_first(tree):
    """Otherwise the override is computed and dropped — the original defect's shape."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        for key, value in zip(node.keys, node.values):
            if not (isinstance(key, ast.Constant) and key.value == "neftune_noise_alpha"):
                continue
            names = {n.id for n in ast.walk(value) if isinstance(n, ast.Name)}
            if OVERRIDE in names:
                assert isinstance(value, ast.IfExp), "expected a conditional resolution"
                test_names = {n.id for n in ast.walk(value.test) if isinstance(n, ast.Name)}
                assert OVERRIDE in test_names, (
                    f"{OVERRIDE} appears but is not what the resolution branches on"
                )
                return
    raise AssertionError(
        f"run_config['neftune_noise_alpha'] never consults {OVERRIDE}; the gate would be "
        "inert on the instruct_hp-is-None path, exactly as before"
    )


# --- the log must stop lying -----------------------------------------------------


def _prints(node):
    out = []
    for n in ast.walk(node):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "print":
            parts = [a.value for a in ast.walk(n) if isinstance(a, ast.Constant) and isinstance(a.value, str)]
            out.append(" ".join(parts))
    return out


def test_every_path_through_the_branch_logs(tree):
    """Detection stays visible whether or not the action fires — the pruning precedent."""
    branch = _gaussian_branch(tree)
    inner = next((n for n in ast.walk(branch) if isinstance(n, ast.If) and n.orelse), None)
    assert inner is not None, "the branch has no gated/ungated split"
    assert _prints(inner), "the gated-on path is silent"
    assert any(_prints(o) for o in inner.orelse), "the default path is silent"


def test_default_path_does_not_announce_a_change(tree):
    """The precise defect: a print that said neftune was zeroed when nothing happened."""
    branch = _gaussian_branch(tree)
    inner = next(n for n in ast.walk(branch) if isinstance(n, ast.If) and n.orelse)
    text = " ".join(m for o in inner.orelse for m in _prints(o)).upper()
    assert "UNCHANGED" in text, f"the default path's log does not say nothing changed: {text!r}"
    assert "=0" not in text.replace(" ", ""), (
        "the default path still reads as though a value was set to 0"
    )
