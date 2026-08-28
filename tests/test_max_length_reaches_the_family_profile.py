"""The corrected sequence length has to reach BOTH planners, not just the first one.

`measure_dataset` produces two p95 figures: `seq_len_p95`, from a first-match field chain
that lands on `output` alone, and `full_seq_p95`, from the real field map. The main
planner was already fixed to prefer the second — its own comment records that the first
"under-reported by 24x on a real task". The family profile a few hundred lines later was
not, and it recomputes max_length from whatever it is handed, and its answer is the one
the run gets. So the correction was computed, logged, and then discarded.

What that cost, measured on task 3a6658eb (clinical notes, Qwen2-1.5B):

    [dynamics] full_seq_p95=2400 full_seq_p99=2649 (legacy chain p95=1235)
    [adaptive] max_length sized from full_seq_p95=2400
    [adaptive] batch bucket scaled for length: 100 -> 38 (max_length=2640 ...)
    [adaptive-instruct] family=qwen ... max_len=1536          <- overrides 2640
    Dropped 27502 long samples from dataset                    <- 98.2% of train
    Dropped 983 long samples from dataset                      <- 98.3% of dev

Axolotl drops an over-long row rather than truncating it, so this is not a shortened
context, it is 27502 rows that never existed as far as the run is concerned.
"""

from __future__ import annotations

import ast
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADAPTIVE = os.path.join(ROOT, "scripts", "adaptive_config.py")
TOKENISE = os.path.join(ROOT, "scripts", "tokenize_instruct.py")


def _source(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


@pytest.fixture(scope="module")
def mod():
    """Top-level defs and constants only — the module itself needs torch."""
    ns = {"os": os, "math": __import__("math")}
    tree = ast.parse(_source(ADAPTIVE))
    flag = annotations.compiler_flag
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.Assign)):
            try:
                exec(compile(ast.Module(body=[node], type_ignores=[]),
                             ADAPTIVE, "exec", flags=flag), ns)  # noqa: S102
            except Exception:
                pass  # anything needing torch — not what this file is about
    return ns


def _call_kwarg(src, func_name, kwarg):
    tree = ast.parse(src)
    for n in ast.walk(tree):
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                and n.func.id == func_name):
            for kw in n.keywords:
                if kw.arg == kwarg:
                    return ast.unparse(kw.value)
    return None


# --- the wire itself ---------------------------------------------------------------


def test_the_family_profile_is_fed_the_corrected_length():
    got = _call_kwarg(_source(ADAPTIVE), "_compute_instruct_adaptive_hp", "seq_p95")
    assert got is not None, "_compute_instruct_adaptive_hp is never called with seq_p95"
    assert "full_seq_p95" in got, (
        "the family profile still receives the legacy chain p95 (%s). It recomputes "
        "max_length from this and its answer wins, so the correction above it is dead." % got
    )


def test_both_planners_size_from_the_same_expression():
    """Two planners disagreeing about the input is how this survived in one file."""
    src = _source(ADAPTIVE)
    tree = ast.parse(src)
    main = None
    for n in ast.walk(tree):
        if (isinstance(n, ast.Assign) and len(n.targets) == 1
                and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_len_p95"):
            main = ast.unparse(n.value)
    assert main, "_len_p95 no longer exists — this test needs rewiring, not deleting"
    family = _call_kwarg(src, "_compute_instruct_adaptive_hp", "seq_p95")
    assert family == main, (
        "main planner sizes from %r but the family profile sizes from %r" % (main, family)
    )


# --- and the arithmetic that made 1536 out of 2400 ---------------------------------


def _hp(mod, seq_p95, **kw):
    args = dict(arch_family="qwen", param_count=1_653_669_888, data_size=29_000,
                seq_p95=seq_p95, model_name="unsloth/Qwen2-1.5B-Instruct",
                detected_base_model=None)
    args.update(kw)
    return mod["_compute_instruct_adaptive_hp"](**args)


def test_the_legacy_value_really_does_produce_1536(mod):
    """Not hypothetical: this is the arithmetic that discarded 98% of 3a6658eb."""
    assert _hp(mod, 1235)["max_length"] == 1536


def test_the_measured_value_produces_a_cap_that_holds_the_data(mod):
    """p95=2400 means 95% of rows are under 2400; a 1536 cap deletes most of them."""
    got = _hp(mod, 2400)["max_length"]
    assert got >= 2400, "max_length %d cannot hold a p95 of 2400" % got


@pytest.mark.parametrize("p95", [800, 1235, 2400, 3000])
def test_the_cap_never_lands_under_the_p95_it_was_given(mod, p95):
    """The cap exists to hold the data, so falling under the p95 is never right."""
    got = _hp(mod, p95)["max_length"]
    assert got >= min(p95, 4096), "p95=%d produced max_length=%d" % (p95, got)


def test_a_family_cap_may_still_bind(mod):
    """Family caps are deliberate and stay — this test exists so that if one starts
    binding below the data, it is a visible decision rather than this bug again.

    The floor is 2046 rather than 2048 because OPT's cap is architectural: max_position
    2048 less the 2 that the indexSelect safety needs. That one is a hardware fact, not
    a tuning choice, and it is the only cap allowed under 2048.
    """
    caps = {f: p.get("max_length_cap") for f, p in mod["_FAMILY_PROFILES"].items()}
    low = {f: c for f, c in caps.items() if c is not None and c < 2046}
    assert not low, (
        "family cap(s) %s sit below the 1536 that discarded 98%% of 3a6658eb — if that "
        "is intended it needs a reason recorded here" % low
    )


# --- the instrument that reported health over the survivors ------------------------


def test_the_tokeniser_reports_how_many_rows_it_dropped():
    src = _source(TOKENISE)
    tree = ast.parse(src)
    fn = next(n for n in ast.walk(tree)
              if isinstance(n, ast.FunctionDef) and n.name == "tokenize_dataset")
    assert "input_rows" in [a.arg for a in fn.args.args], (
        "tokenize_dataset cannot know how many rows it was given, so its len-check can "
        "only ever describe the survivors"
    )
    body = ast.unparse(fn)
    assert "input_rows - len(result)" in body.replace(" ", " "), (
        "nothing computes the number of dropped rows"
    )


def test_the_split_hands_its_counts_over():
    tree = ast.parse(_source(TOKENISE))
    fn = next(n for n in ast.walk(tree)
              if isinstance(n, ast.FunctionDef) and n.name == "split_dataset")
    returns = [n for n in ast.walk(fn) if isinstance(n, ast.Return) and n.value is not None]
    assert returns, "split_dataset returns nothing, so the counts are lost"
    # `return None, None` is also a two-tuple, and would leave the drop check silent
    # while every structural assertion still passed.
    body = " ".join(ast.unparse(r.value) for r in returns)
    assert "train_items" in body and "dev_items" in body, (
        "split_dataset returns %s — that is a shape, not the counts" % body
    )


def test_both_tokenise_calls_pass_their_row_count():
    src = _source(TOKENISE)
    tree = ast.parse(src)
    calls = [n for n in ast.walk(tree)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
             and n.func.id == "tokenize_dataset"]
    assert len(calls) >= 2, "expected a train and a dev tokenise call"
    for c in calls:
        assert any(kw.arg == "input_rows" for kw in c.keywords), (
            "a tokenize_dataset call omits input_rows, so that split reports nothing"
        )


def test_a_large_drop_is_a_warning_not_a_statistic():
    """98.2% dropped previously printed as '1.0% reach the cap' — a reassuring line."""
    src = _source(TOKENISE)
    assert "WARNING" in src and "discarded" in src
    tree = ast.parse(src)
    fn = next(n for n in ast.walk(tree)
              if isinstance(n, ast.FunctionDef) and n.name == "tokenize_dataset")
    thresholds = [n.comparators[0].value for n in ast.walk(fn)
                  if isinstance(n, ast.Compare) and isinstance(n.left, ast.Name)
                  and n.left.id == "pct" and isinstance(n.comparators[0], ast.Constant)]
    assert thresholds, "no threshold governs the drop warning"
    assert max(thresholds) <= 50, (
        "the drop warning only fires above %s%% — a run that lost half its data would "
        "still read as healthy" % max(thresholds)
    )


# --- the third consumer of the same figure -----------------------------------------


def test_the_token_estimate_counts_the_whole_training_sequence():
    """hp_override estimates training tokens as n_train * seq_p95.

    A training sequence is the whole rendered row, prompt included, so the
    completion-only chain halves the estimate on any prompt-heavy task: 3a6658eb
    reported est_tokens=35.8M against a real 69.6M. The only gate reading it is d2z at
    TPP > 1.0 and our tasks sit two orders below that either way, so this corrects a
    number rather than a behaviour — but a wrong number that happens to be harmless
    today is still the thing that stops being harmless quietly.
    """
    src = _source(ADAPTIVE)
    tree = ast.parse(src)
    for n in ast.walk(tree):
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                and n.func.id == "_hp_apply"):
            kw = {k.arg: ast.unparse(k.value) for k in n.keywords}
            assert "full_seq_p95" in kw.get("seq_p95", ""), (
                "hp_override still receives the completion-only p95 (%s)" % kw.get("seq_p95")
            )
            return
    raise AssertionError("_hp_apply is never called — this test needs rewiring")


def test_every_length_consumer_that_sizes_training_uses_the_field_map():
    """One file, three consumers, and the correction reached two of them for months.

    GRPO's max_completion_length is deliberately excluded: it bounds the COMPLETION,
    which is exactly what the legacy chain measures, so it is right as it stands.
    """
    src = _source(ADAPTIVE)
    tree = ast.parse(src)
    bad = []
    for n in ast.walk(tree):
        if not (isinstance(n, ast.Call) and n.keywords):
            continue
        name = getattr(n.func, "id", None) or getattr(n.func, "attr", None)
        # DatasetMetrics is where the field is populated, not read; excluding the
        # producer is not the same as excusing a consumer.
        if name in ("_select_grpo_max_completion", "DatasetMetrics"):
            continue
        for k in n.keywords:
            if k.arg in ("seq_p95", "seq_len_p95"):
                expr = ast.unparse(k.value)
                if "full_seq_p95" not in expr:
                    bad.append("%s(%s=%s)" % (name, k.arg, expr))
    assert not bad, "length consumers still on the legacy chain: %s" % bad
