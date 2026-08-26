"""Machinery that only watches must never be what ends a run.

Two hooks could, and both sat outside the guards around them.

`_maybe_kl_govern` is called from `on_log` BEFORE the try that wraps the rest of that
callback. Transformers does not wrap callback dispatch, so anything it raises travels up
through `trainer.log()` and ends training. Its float conversions were already guarded
internally, but the LR mutation block — `sched.base_lrs = [...]`, `pg["lr"] *= f` — was
not, and neither was attribute access on a partially-initialised instance. The governor
exists to *prevent* a bad run; killing the run outright is the one outcome worse than the
drift it watches for.

`on_step_end` read `my_state["train"]` and `min([run["current_loss"] for run in
my_state["runs"]])` with nothing between them and a lost state. `get_state()` returns a
bare `{}` when the redis key is gone or its JSON will not parse — "state lost mid-task" is
a shape this repo has already had to backstop elsewhere — and `on_step_end` runs every
step. A missing key ended the run rather than degrading it.

The min is tested for behaviour, having been lifted to module scope for exactly that
reason. The rest is tested structurally: the defect was never in arithmetic, it was in
where the guard sat, and the enclosing callbacks need torch, transformers and a live
TrainerState to exercise.
"""

import ast
import os

import pytest

SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
TRAINER = os.path.join(SCRIPTS, "customized_trainer.py")


def _source():
    with open(TRAINER, "r", encoding="utf-8") as fh:
        return fh.read()


@pytest.fixture(scope="module")
def tree():
    return ast.parse(_source())


@pytest.fixture(scope="module")
def min_prior():
    """exec the helper alone — the module needs torch and transformers to import."""
    tree = ast.parse(_source())
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "min_prior_run_loss":
            ns = {}
            exec(compile(ast.Module(body=[node], type_ignores=[]), TRAINER, "exec"), ns)  # noqa: S102
            return ns["min_prior_run_loss"]
    raise AssertionError("min_prior_run_loss is not defined at module scope")


# --- the min, tested for behaviour ----------------------------------------------

INF = float("inf")


def test_picks_the_lowest(min_prior):
    assert min_prior([{"current_loss": 2.0}, {"current_loss": 1.5}, {"current_loss": 3.0}]) == 1.5


def test_empty_history_is_not_a_crash(min_prior):
    """min([]) was a ValueError inside a hook that runs every step."""
    assert min_prior([]) == INF


def test_missing_runs_key_is_not_a_crash(min_prior):
    """get_state() returns {} on a lost redis key, so runs is absent entirely."""
    assert min_prior(None) == INF


@pytest.mark.parametrize("junk", ["", 0, {}, 3.5, {"current_loss": 1.0}])
def test_non_sequence_history_is_survivable(min_prior, junk):
    assert min_prior(junk) == INF


def test_half_written_run_is_skipped_not_fatal(min_prior):
    """A run dict recorded before its loss was known has no current_loss key."""
    assert min_prior([{"train_cmd": "x"}, {"current_loss": 4.0}]) == 4.0


def test_all_entries_unusable_falls_back(min_prior):
    assert min_prior([{"train_cmd": "x"}, {"current_loss": None}, "junk"]) == INF


def test_booleans_are_not_losses(min_prior):
    """bool is an int subclass; True would otherwise read as a loss of 1.0."""
    assert min_prior([{"current_loss": True}, {"current_loss": 2.5}]) == 2.5


def test_no_history_makes_the_current_run_the_best(min_prior):
    """+inf is the meaning, not a sentinel: anything compares <= to it."""
    assert 9999.0 <= min_prior([])


# --- the KL governor's guard ----------------------------------------------------


def _on_log_of_grpo_callback(tree):
    cls = next(
        n for n in ast.walk(tree)
        if isinstance(n, ast.ClassDef) and n.name == "GRPOCustomEvalSaveCallback"
    )
    return next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "on_log")


def _call_names(node):
    out = set()
    for n in ast.walk(node):
        if isinstance(n, ast.Call):
            if isinstance(n.func, ast.Attribute):
                out.add(n.func.attr)
            elif isinstance(n.func, ast.Name):
                out.add(n.func.id)
    return out


def test_governor_is_called_inside_a_try(tree):
    """It sits before the try that wraps the rest of on_log; it needs its own."""
    on_log = _on_log_of_grpo_callback(tree)
    guarded = any(
        "_maybe_kl_govern" in _call_names(t)
        for t in ast.walk(on_log)
        if isinstance(t, ast.Try)
    )
    assert guarded, (
        "_maybe_kl_govern is called outside every try in on_log; transformers does not "
        "wrap callback dispatch, so anything it raises ends the run"
    )


def test_governor_guard_catches_broadly(tree):
    """A narrow except would miss the LR mutation block and attribute errors."""
    on_log = _on_log_of_grpo_callback(tree)
    for t in ast.walk(on_log):
        if not (isinstance(t, ast.Try) and any("_maybe_kl_govern" in _call_names(b) for b in t.body)):
            continue
        types = {
            h.type.id for h in t.handlers
            if isinstance(h.type, ast.Name)
        }
        assert "Exception" in types, f"guard catches only {types or 'nothing'}"
        return
    raise AssertionError("no try wraps _maybe_kl_govern")


def test_a_failed_governor_disables_itself(tree):
    """Otherwise one broken step becomes per-step log spam for the whole run."""
    on_log = _on_log_of_grpo_callback(tree)
    for t in ast.walk(on_log):
        if not (isinstance(t, ast.Try) and any("_maybe_kl_govern" in _call_names(b) for b in t.body)):
            continue
        assigned = {
            tgt.attr
            for h in t.handlers
            for n in ast.walk(h)
            if isinstance(n, ast.Assign)
            for tgt in n.targets
            if isinstance(tgt, ast.Attribute)
        }
        assert "_kl_gov_ceiling" in assigned, (
            "the handler does not disable the governor; _kl_gov_ceiling = 0 is the "
            "existing disable path and stops the failure repeating every step"
        )
        return


def test_the_handler_does_not_rely_on_the_attribute_it_may_have_lost(tree):
    """AttributeError on _kl_gov_ceiling is one of the things being caught."""
    src = _source()
    idx = src.index("_maybe_kl_govern(logs.get")
    handler = src[idx : idx + 900]
    assert "getattr(self, \"_kl_gov_ceiling\"" in handler, (
        "the handler reads self._kl_gov_ceiling directly; if that attribute is what "
        "raised, the handler raises too and the guard achieves nothing"
    )


# --- the state reads ------------------------------------------------------------


def _double_subscript_assign_targets(tree):
    """Every a[K1][K2] = ... target in the module, as (K1, K2) string pairs."""
    out = set()
    for n in ast.walk(tree):
        if not isinstance(n, ast.Assign):
            continue
        for t in n.targets:
            if (
                isinstance(t, ast.Subscript)
                and isinstance(t.slice, ast.Constant)
                and isinstance(t.value, ast.Subscript)
                and isinstance(t.value.slice, ast.Constant)
            ):
                out.add((t.value.slice.value, t.slice.value))
    return out


def test_state_write_does_not_assume_the_train_key(tree):
    """my_state["train"][...] = x raises KeyError on the {} a lost state returns.

    Checked through the AST, not the text: this file's own docstrings quote the old
    code, and the first version of this test matched its own prose.
    """
    assert ("train", "current_loss") not in _double_subscript_assign_targets(tree), (
        "the probe loss is assigned through a bare double subscript again"
    )


def test_the_double_subscript_check_can_bite(tree):
    """Control for the test above — the detector must see real assignments."""
    found = _double_subscript_assign_targets(ast.parse(
        'd["a"]["b"] = 1\n'
    ))
    assert ("a", "b") in found


def test_min_site_uses_the_guarded_helper(tree):
    """A correct helper nobody calls would leave the crash exactly where it was."""
    calls = [
        n for n in ast.walk(tree)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
    ]
    assert any(c.func.id == "min_prior_run_loss" for c in calls), (
        "on_step_end no longer routes through min_prior_run_loss"
    )
    raw = [
        c for c in calls
        if c.func.id == "min" and c.args and isinstance(c.args[0], (ast.ListComp, ast.GeneratorExp))
    ]
    for c in raw:
        consts = {
            n.value for n in ast.walk(c.args[0])
            if isinstance(n, ast.Constant) and isinstance(n.value, str)
        }
        assert "current_loss" not in consts, (
            "a raw unguarded min over run losses is present again"
        )


# --- the first_time branch, which carried the identical exposure ------------------


@pytest.fixture(scope="module")
def parse_ts():
    """exec the timestamp parser alone, same reason as min_prior above."""
    tree = ast.parse(_source())
    ns = {"datetime": __import__("datetime")}
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "STATE_TIME_FORMAT" for t in node.targets
        ):
            exec(compile(ast.Module(body=[node], type_ignores=[]), TRAINER, "exec"), ns)  # noqa: S102
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "parse_state_timestamp":
            exec(compile(ast.Module(body=[node], type_ignores=[]), TRAINER, "exec"), ns)  # noqa: S102
            return ns["parse_state_timestamp"]
    raise AssertionError("parse_state_timestamp is not defined at module scope")


def test_a_real_timestamp_parses(parse_ts):
    got = parse_ts("2026-08-27 01:23:45")
    assert (got.year, got.month, got.day, got.hour) == (2026, 8, 27, 1)


@pytest.mark.parametrize(
    "junk",
    [None, "", "not a date", "2026-08-27", 1756250000, 3.5, True, [], {}, b"2026-08-27 01:23:45"],
)
def test_unusable_stamps_return_none_rather_than_raising(parse_ts, junk):
    """A lost state yields {}, so .get() hands this None; a truncated write hands junk."""
    assert parse_ts(junk) is None


def test_no_default_is_fabricated(parse_ts):
    """These stamps drive the remaining-time estimate.

    A made-up value would produce a confident wrong estimate of how many runs still
    fit, which is worse than declining to estimate at all.
    """
    assert parse_ts(None) is None
    assert parse_ts("garbage") is None


def test_first_time_branch_uses_the_parser(tree):
    """The wire. A correct parser nobody calls leaves the crash where it was."""
    called = [
        n for n in ast.walk(tree)
        if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Name)
        and n.func.id == "parse_state_timestamp"
    ]
    assert len(called) >= 2, (
        f"expected both start stamps to go through the parser, found {len(called)} call(s)"
    )


def test_strptime_is_no_longer_called_on_state_directly(tree):
    """The old shape: datetime.strptime(my_state["train"][...], fmt)."""
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
            continue
        if node.func.attr != "strptime" or not node.args:
            continue
        names = {n.id for n in ast.walk(node.args[0]) if isinstance(n, ast.Name)}
        assert "my_state" not in names, (
            "a state value is parsed inline again; route it through parse_state_timestamp"
        )


# --- gap two: the guard that nothing was pinning ---------------------------------


def _bare_subscript_reads(tree, name="my_state"):
    """String keys READ off `name` by subscript — writes create the key, reads raise."""
    out = set()
    for n in ast.walk(tree):
        if (
            isinstance(n, ast.Subscript)
            and isinstance(n.value, ast.Name)
            and n.value.id == name
            and isinstance(n.ctx, ast.Load)
            and isinstance(n.slice, ast.Constant)
            and isinstance(n.slice.value, str)
        ):
            out.add(n.slice.value)
    return out


def test_next_runs_is_read_defensively(tree):
    """Reverting this to my_state["next_runs"] passed every test in this file.

    The committed code was already right; nothing pinned it, so it could be undone
    silently. A lost state returns {} and the read is a KeyError inside a hook that
    runs every step.
    """
    assert "next_runs" not in _bare_subscript_reads(tree), (
        'my_state["next_runs"] is read by bare subscript; use .get("next_runs")'
    )


def test_the_bare_read_detector_can_bite():
    """Control: writes must not register, reads must."""
    written_only = _bare_subscript_reads(ast.parse('my_state["mode"] = "finish"\n'))
    assert written_only == set(), f"a write was misread as a read: {written_only}"
    read = _bare_subscript_reads(ast.parse('x = my_state["next_runs"]\n'))
    assert read == {"next_runs"}


def test_runs_is_also_read_defensively(tree):
    """Same shape, same fix — pinned here so neither can regress alone."""
    assert "runs" not in _bare_subscript_reads(tree)
