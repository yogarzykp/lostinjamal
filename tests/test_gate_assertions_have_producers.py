"""Every log line the GPU gate asserts on must still be produced by scripts/.

ops/smoke/gate.sh is the mandatory pre-submission gate. It does not trust exit codes —
every safety net in this codebase keeps going rather than dying — so each of its 44 rows
is a grep for a specific line in the run log. That makes the gate hostage to prints: a
refactor that reworded `[lr-search] sweep curve written` would turn 44/44 into a red gate,
and the first anyone would hear of it is an hour of H100 later. This file makes that a
CPU check, in three layers:

  1. PARSE the shell for every `grep "<pattern>"` aimed at a run log, reduce each
     BRE/ERE to the longest literal prefix the trainer must print, and require that
     literal to appear inside a print()/log_info()/logger.* call somewhere under
     scripts/ (AST, so a comment mentioning the string does not count). Three patterns
     are produced by the Python runtime or the pinned TRL/transformers rather than by
     scripts/; they are named in THIRD_PARTY and verified against the pinned packages.
  2. DRY-RUN gate.sh itself against canned logs written from those producers' format
     strings, with `python` stubbed so no trainer runs: this proves the greps, the
     `tail -1 | cut` pipelines and the three PYCHECK heredocs accept the shapes the
     producers emit, and that the log file names gate.sh reads are the ones the
     run_*.sh scripts write. 44 rows come out, as on a real run.
  3. bash -n every script under ops/smoke/, and preflight.sh's pin check under the
     interpreter running the tests.

What the shell parser can and cannot see (be honest, it is a regex not a shell):
  * it extracts `grep [flags] [--] "pattern" ...` and `'pattern'` on non-comment lines;
  * a pattern containing a shell variable (`^$MARKER`) is DYNAMIC and skipped;
  * a grep whose line names no log (`env | grep`, the dmesg Xid count) is skipped;
  * every skip is enumerated in EXPECTED_SKIPS, so a new grep that the parser cannot
    resolve fails a test until someone classifies it;
  * the literal prefix stops at the first regex metacharacter, so `max_len=[0-9]*`
    is checked as `max_len=` — the dry run (layer 2) covers the rest of the shape.

Two xfail(strict=True) tests at the end document gate gaps found while writing this:
a run that hit the NaN/zero-weight guard and shipped a noised base model still passes
every common gate, because `Training successfully done` is printed BEFORE that guard
(text_trainer.py) while gate.sh's comment claims the opposite; and the dedup check goes
vacuous when a `dedup crosscheck:` line follows the stats dict. They flip to XPASS —
and fail strict — the day gate.sh closes them.

Override GATE_PRODUCERS_SCRIPTS_DIR / GATE_PRODUCERS_SMOKE_DIR to point the checks at
another tree; that is how the mutation runs recorded in the review report were made.
"""

from __future__ import annotations

import ast
import inspect
import os
import re
import shutil
import stat
import subprocess
import sys
import traceback

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
SCRIPTS_DIR = os.environ.get("GATE_PRODUCERS_SCRIPTS_DIR", os.path.join(REPO, "scripts"))
SMOKE_DIR = os.environ.get("GATE_PRODUCERS_SMOKE_DIR", os.path.join(REPO, "ops", "smoke"))

# Scripts whose greps are assertions on a training log. gate.sh is the gate;
# lr_recovery.sh reads the same logs for its own verdicts and is held to the same bar.
LOG_ASSERTING_SCRIPTS = ("gate.sh", "lr_recovery.sh")


# ---------------------------------------------------------------------------------
# Layer 1a: parse the shell
# ---------------------------------------------------------------------------------

_GREP_RE = re.compile(
    r"""(?<![\w-])grep\s+(?P<flags>(?:-{1,2}[A-Za-z]+\s+)*)(?:--\s+)?"""
    r"""(?P<q>["'])(?P<pat>.*?)(?P=q)(?P<rest>[^|;&]*)"""
)
_SHELL_VAR_RE = re.compile(r"\$\{?[A-Za-z_]")
_LOG_REF_RE = re.compile(r"\$\{?(log|LOG)\b|\.log\b")


def _literal_prefix(pattern: str, ere: bool, fixed: bool) -> tuple[str, bool]:
    """Longest leading substring a matching line must contain literally.

    Returns (literal, anchored). Handles the two regex dialects the scripts use:
    BRE (default; `\\[` is a literal bracket, `\\{` `\\(` `\\|` `\\+` `\\?` are meta) and
    ERE (-E; `( ) { } | + ?` are meta unescaped). -F patterns are returned whole.
    """
    if fixed:
        return pattern, False
    anchored = pattern.startswith("^")
    i = 1 if anchored else 0
    bre_meta = set("[.*$")
    ere_meta = set("[.*$+?(){}|")
    out: list[str] = []
    while i < len(pattern):
        c = pattern[i]
        if c == "\\":
            if i + 1 >= len(pattern):
                break
            nxt = pattern[i + 1]
            if not ere and nxt in "{}()|+?":
                break  # escaped => meta in BRE
            out.append(nxt)  # escaped => literal in ERE, and \[ \] \. in BRE
            i += 2
            continue
        if c in (ere_meta if ere else bre_meta):
            break
        out.append(c)
        i += 1
    return "".join(out), anchored


def extract_greps(smoke_dir: str) -> list[dict]:
    """Every grep invocation in ops/smoke/*.sh, classified.

    Record keys: file, lineno, pattern, flags, ere, fixed, literal, anchored,
    target ('log' | 'env' | 'other'), skipped (None or a reason string).
    """
    records: list[dict] = []
    for name in sorted(os.listdir(smoke_dir)):
        if not name.endswith(".sh"):
            continue
        path = os.path.join(smoke_dir, name)
        with open(path, encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, 1):
                if line.lstrip().startswith("#"):
                    continue
                for m in _GREP_RE.finditer(line):
                    flag_chars = "".join(
                        tok.lstrip("-") for tok in m.group("flags").split() if not tok.startswith("--")
                    )
                    long_flags = [tok for tok in m.group("flags").split() if tok.startswith("--")]
                    ere = "E" in flag_chars or "--extended-regexp" in long_flags
                    fixed = "F" in flag_chars or "--fixed-strings" in long_flags
                    pattern = m.group("pat")
                    literal, anchored = _literal_prefix(pattern, ere, fixed)
                    if _LOG_REF_RE.search(m.group("rest")) or _LOG_REF_RE.search(line):
                        target = "log"
                    elif line.lstrip().startswith("env |") or line.lstrip().startswith("env|"):
                        target = "env"
                    else:
                        target = "other"
                    skipped = None
                    if _SHELL_VAR_RE.search(pattern):
                        skipped = "dynamic"
                    elif target != "log":
                        skipped = target
                    elif not literal:
                        skipped = "no-literal"
                    records.append(
                        dict(
                            file=name, lineno=lineno, pattern=pattern, flags=flag_chars,
                            ere=ere, fixed=fixed, literal=literal, anchored=anchored,
                            target=target, skipped=skipped,
                        )
                    )
    return records


# Every grep the parser cannot turn into a log assertion, with why. Adding a grep that
# lands here without adding it to this table fails test_parser_skips_are_all_classified.
EXPECTED_SKIPS = {
    # `env | grep -E "^(SWITCH|...)"` prints a stage's switches; the switch list is not
    # an assertion and is free to change, so it is recorded as <env-print>, not verbatim.
    ("run_instruct_replay.sh", "<env-print>", "env"),
    ("run_dpo_smoke.sh", "<env-print>", "env"),
    ("run_grpo_smoke.sh", "<env-print>", "env"),
    ("wait_gate.sh", "Xid", "other"),          # counts kernel Xid lines in dmesg, not a trainer print
    ("wait_gate.sh", "^$MARKER", "dynamic"),  # the caller passes the marker; tests/test_wait_gate.py covers it
}

# Patterns whose producer is not in scripts/ at all. Each is verified against the
# runtime or the pinned package in test_third_party_producer.
THIRD_PARTY = {
    "Traceback": "the Python runtime — traceback.format_exc() begins 'Traceback (most recent call last):'",
    "reward': ": "trl 0.18.0 GRPOTrainer logs metric key 'reward'; transformers 4.51.3 "
                 "ProgressCallback/PrinterCallback print str(logs) => {'reward': 0.4, ...}",
    "'learning_rate': ": "transformers Trainer._maybe_log_save_evaluate sets logs['learning_rate']; "
                         "printed by the same callbacks",
}

ALL_GREPS = extract_greps(SMOKE_DIR) if os.path.isdir(SMOKE_DIR) else []
LOG_GREPS = [g for g in ALL_GREPS if g["skipped"] is None and g["file"] in LOG_ASSERTING_SCRIPTS]
# Dedupe by (file, literal) so a pattern grepped twice (gate.sh greps the success line
# twice; lr_recovery.sh greps learning_rate on two branches) is one test case.
_seen: set = set()
GATE_CASES: list[dict] = []
for _g in LOG_GREPS:
    _key = (_g["file"], _g["literal"])
    if _key not in _seen:
        _seen.add(_key)
        GATE_CASES.append(_g)
GATE_LITERALS = sorted({g["literal"] for g in LOG_GREPS if g["file"] == "gate.sh"})


# ---------------------------------------------------------------------------------
# Layer 1b: find producers in scripts/ by AST
# ---------------------------------------------------------------------------------

# `log` is dev_absorption.absorb_dev_split's injected writer, defaulting to print
# (dev_absorption.py:162); nothing else in scripts/ uses that name for a call.
_LOG_NAMES = {"print", "log_info", "log"}
_LOG_ATTRS = {"info", "warning", "warn", "error", "debug", "critical", "exception", "write"}


def _is_log_call(func: ast.AST) -> bool:
    if isinstance(func, ast.Name):
        return func.id in _LOG_NAMES
    if isinstance(func, ast.Attribute):
        return func.attr in _LOG_ATTRS
    return False


def _py_files(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ("__pycache__", "tests", ".git")]
        for fn in sorted(filenames):
            if fn.endswith(".py"):
                yield os.path.join(dirpath, fn)


def _string_texts(node: ast.AST):
    """Every string a subtree can contribute to output: plain constants, and for
    f-strings each constant part AND the template with `{}` for each placeholder, so a
    literal that spans a placeholder is still findable."""
    for sub in ast.walk(node):
        if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
            yield sub.lineno, sub.value
        elif isinstance(sub, ast.JoinedStr):
            yield sub.lineno, "".join(
                v.value if isinstance(v, ast.Constant) and isinstance(v.value, str) else "{}"
                for v in sub.values
            )


def producer_strings(root: str) -> list[tuple[str, int, str, str]]:
    """(relpath, lineno, tier, text) for the strings scripts/ can print.

    tier "direct":   inside a print()/log_info()/logger.*() call — the line is emitted
                     where it is written.
    tier "indirect": any other string constant that is not a docstring — a message
                     built in one place and printed by a caller (lr_search.describe is
                     returned, then printed by train_instruct.py:889 / text_trainer.py:1168).
    Comments never count: the AST has none. Docstrings are excluded so that quoting a
    gate line in prose does not satisfy the gate.
    """
    out: list[tuple[str, int, str, str]] = []
    for path in _py_files(root):
        with open(path, encoding="utf-8") as fh:
            src = fh.read()
        try:
            tree = ast.parse(src, filename=path)
        except SyntaxError as exc:  # pragma: no cover — a broken file is its own failure
            raise AssertionError(f"{path} does not parse: {exc}")
        rel = os.path.relpath(path, root)
        docstring_ids: set[int] = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                body = node.body
                if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
                        and isinstance(body[0].value.value, str):
                    docstring_ids.add(id(body[0].value))
        direct_ids: set[int] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and _is_log_call(node.func):
                for arg in node.args:
                    for sub in ast.walk(arg):
                        direct_ids.add(id(sub))
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Constant, ast.JoinedStr)):
                continue
            if id(node) in docstring_ids:
                continue
            tier = "direct" if id(node) in direct_ids else "indirect"
            for ln, text in _string_texts(node):
                out.append((rel, ln, tier, text))
                break  # _string_texts on a Constant/JoinedStr yields exactly itself first
    return out


PRODUCERS = producer_strings(SCRIPTS_DIR) if os.path.isdir(SCRIPTS_DIR) else []


def producers_of(literal: str, tiers=("direct", "indirect")) -> list[tuple[str, int, str]]:
    return sorted({(rel, ln, tier) for rel, ln, tier, text in PRODUCERS if tier in tiers and literal in text})


def _case_id(g: dict) -> str:
    return f"{g['file']}:{g['literal']}"


# ---------------------------------------------------------------------------------
# Layer 1 tests
# ---------------------------------------------------------------------------------

def test_parser_found_the_gate():
    """The parser sees gate.sh's assertions at all — an empty extraction would make
    every parametrized test below vacuously absent, not failing."""
    assert os.path.isfile(os.path.join(SMOKE_DIR, "gate.sh"))
    gate_literals = [g["literal"] for g in GATE_CASES if g["file"] == "gate.sh"]
    # The five gate families, one representative each. A refactor that reshapes the
    # greps past this parser's regex should be noticed here, not as silent shrinkage.
    for must in ("Training successfully done", "[lr-search] sweeping at batch=",
                 "[kl] checkpoint metric:", "Using reward function",
                 "Processing chat template dataset type"):
        assert must in gate_literals, f"parser lost {must!r}; saw {gate_literals}"
    assert len(gate_literals) >= 16, gate_literals


def test_parser_skips_are_all_classified():
    """Every grep the parser could not resolve to a log assertion is a known one."""
    skipped = {
        (g["file"], "<env-print>" if g["skipped"] == "env" else g["pattern"], g["skipped"])
        for g in ALL_GREPS if g["skipped"]
    }
    assert skipped == EXPECTED_SKIPS, (
        f"unclassified greps (add to EXPECTED_SKIPS or make them log assertions):\n"
        f"  new: {sorted(skipped - EXPECTED_SKIPS)}\n  gone: {sorted(EXPECTED_SKIPS - skipped)}"
    )


@pytest.mark.parametrize("case", GATE_CASES, ids=_case_id)
def test_gate_pattern_has_producer(case):
    """The literal a gate grep needs is emitted by a print/log call under scripts/,
    or is one of the three THIRD_PARTY lines verified separately."""
    literal = case["literal"]
    if literal in THIRD_PARTY:
        pytest.skip(f"third-party producer: {THIRD_PARTY[literal]} (see test_third_party_producer)")
    hits = producers_of(literal)
    assert hits, (
        f"{case['file']}:{case['lineno']} greps {case['pattern']!r} (literal {literal!r}) "
        f"but no string under {SCRIPTS_DIR} carries that text — a red gate waiting "
        f"for a GPU hour to be discovered"
    )
    # Prefer a direct producer; an indirect-only hit is legitimate (a returned message)
    # but is worth seeing in the report, so name it in the assertion context.
    tiers = {t for _, _, t in hits}
    assert tiers & {"direct", "indirect"}, hits


@pytest.mark.parametrize("literal", sorted(THIRD_PARTY), ids=repr)
def test_third_party_producer(literal):
    """The three lines scripts/ does not print are produced by the runtime or the
    pinned packages, checked against the versions actually installed."""
    assert literal in GATE_LITERALS or any(g["literal"] == literal for g in GATE_CASES), (
        f"{literal!r} is in THIRD_PARTY but no script greps it any more — drop it"
    )
    if literal == "Traceback":
        try:
            raise RuntimeError("probe")
        except RuntimeError:
            text = traceback.format_exc()
        assert text.startswith("Traceback (most recent call last):")
        return
    import transformers
    import transformers.trainer_callback as tc
    from transformers import Trainer

    writer = inspect.getsource(tc.ProgressCallback.on_log) + inspect.getsource(tc.PrinterCallback.on_log)
    assert "write(str(shallow_logs))" in writer and "print(logs)" in writer, transformers.__version__
    if literal == "reward': ":
        import trl
        import trl.trainer.grpo_trainer as grpo

        assert 'self._metrics[mode]["reward"]' in inspect.getsource(grpo), trl.__version__
        rendered = str({"loss": 0.01, "reward": 0.4375, "reward_std": 0.1})
    else:
        assert 'logs["learning_rate"]' in inspect.getsource(Trainer._maybe_log_save_evaluate)
        rendered = str({"loss": 0.01, "learning_rate": 8e-06, "epoch": 0.1})
    # And the real grep, with the real pattern, on the rendered dict.
    grep = next(g for g in GATE_CASES if g["literal"] == literal)
    flags = "-ao" + ("E" if grep["ere"] else "")
    res = subprocess.run(["grep", flags, grep["pattern"]], input=rendered, capture_output=True, text=True)
    assert res.returncode == 0 and res.stdout.strip(), (grep["pattern"], rendered)


def _heredoc(name: str) -> str:
    with open(os.path.join(SMOKE_DIR, "gate.sh"), encoding="utf-8") as fh:
        src = fh.read()
    m = re.search(rf'cat > "\${name}" <<\'PYEOF\'\n(.*?)\nPYEOF', src, re.S)
    assert m, f"gate.sh no longer writes {name} as a PYEOF heredoc"
    return m.group(1)


@pytest.mark.parametrize(
    "heredoc, producer_file",
    [("PYCHECK_SPLIT", os.path.join("data", "split_policy.py")),
     ("PYCHECK_DEDUP", os.path.join("data", "dedup_knn.py"))],
)
def test_pycheck_dict_keys_exist_in_the_producer(heredoc, producer_file):
    """gate.sh parses `[split] {...}` and `[dedup] {...}` with ast.literal_eval and reads
    named keys; those keys must be ones the producer's stats dict carries."""
    keys = set(re.findall(r'd\.get\("(\w+)"', _heredoc(heredoc)))
    assert keys, heredoc
    path = os.path.join(SCRIPTS_DIR, producer_file)
    with open(path, encoding="utf-8") as fh:
        consts = {
            n.value for n in ast.walk(ast.parse(fh.read()))
            if isinstance(n, ast.Constant) and isinstance(n.value, str)
        }
    missing = keys - consts
    assert not missing, f"{heredoc} reads {sorted(missing)} but {producer_file} never names them"


# ---------------------------------------------------------------------------------
# The three ungated commits: the log lines around the changed code
# ---------------------------------------------------------------------------------

# (file, literal, gate_asserts). gate_asserts is checked against the parsed gate, so
# the claim "the gate does / does not see this line" is mechanical, not a comment.
COMMIT_LINES = [
    # 523124d — promotion before telemetry (customized_trainer.py on_evaluate / on_save)
    ("customized_trainer.py", "Updating the best checkpoint info at step: ", False),
    ("customized_trainer.py", "Copy the best checkpoint to the submission directory at step: ", False),
    ("customized_trainer.py", "[per-example] step=", False),
    ("customized_trainer.py", "[per-example] skipped (", False),
    ("customized_trainer.py", "[best_ckpt persist] save skipped: ", False),
    ("customized_trainer.py", "[kl] checkpoint metric: ", True),      # kl_gates, count > 0
    ("customized_trainer.py", "checkpoint metric unavailable after retry", True),  # kl_gates, must be 0
    # d91101f — shard index cleared before absorb (dev_absorption.py) + the caller
    ("dev_absorption.py", "[dev-absorb] absorbed ", False),
    ("dev_absorption.py", "[dev-absorb] staged directory has no weights", False),
    ("dev_absorption.py", "[dev-absorb] failed (", False),
    ("text_trainer.py", "[dev-absorb] skipped (", False),
    ("text_trainer.py", "[dev-absorb] off (DEV_ABSORPTION=0)", False),
    # 4723787 (+ daf4078) — the ZeRO-3 checkpointing branch in all three trainers
    ("train_instruct.py", "gradient checkpointing: use_reentrant=", False),
    ("train_dpo.py", "gradient checkpointing: use_reentrant=", False),
    ("train_grpo.py", "gradient checkpointing: use_reentrant=", False),
]


@pytest.mark.parametrize("rel, literal, gate_asserts", COMMIT_LINES, ids=lambda v: v if isinstance(v, str) else "")
def test_commit_log_line_survives(rel, literal, gate_asserts):
    hits = [(r, ln, t) for r, ln, t in producers_of(literal, tiers=("direct",)) if r == rel]
    assert hits, f"{rel} no longer prints {literal!r} from a print/log call"
    seen_by_gate = any(gl in literal for gl in GATE_LITERALS)
    assert seen_by_gate == gate_asserts, (
        f"{literal!r}: gate.sh {'does' if seen_by_gate else 'does not'} assert on it; "
        f"update COMMIT_LINES if that changed on purpose"
    )


def test_smoke_keeps_per_example_telemetry_on():
    """523124d flipped EMIT_PER_EXAMPLE_LOSSES to default OFF, on the promise
    (per_example_eval.enabled docstring) that ops/smoke/* export it ON so the gate keeps
    exercising the per-example pass. Hold the smoke scripts to that promise, on every
    path that reaches CustomEvalSaveCallback.on_evaluate's per-example block."""
    for script in ("run_instruct_replay.sh", "run_chat_smoke.sh"):
        with open(os.path.join(SMOKE_DIR, script), encoding="utf-8") as fh:
            body = fh.read()
        assert "export EMIT_PER_EXAMPLE_LOSSES=1" in body, script
    # and the trainer default really did move: the gate now runs a configuration the
    # tournament does not (telemetry ON there, OFF here). Recorded, not judged.
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "per_example_eval_under_test", os.path.join(SCRIPTS_DIR, "per_example_eval.py")
    )
    per_example_eval = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(per_example_eval)  # loaded from SCRIPTS_DIR, not sys.modules
    env_backup = os.environ.pop("EMIT_PER_EXAMPLE_LOSSES", None)
    try:
        assert per_example_eval.enabled() is False
        os.environ["EMIT_PER_EXAMPLE_LOSSES"] = "1"
        assert per_example_eval.enabled() is True
    finally:
        os.environ.pop("EMIT_PER_EXAMPLE_LOSSES", None)
        if env_backup is not None:
            os.environ["EMIT_PER_EXAMPLE_LOSSES"] = env_backup


# ---------------------------------------------------------------------------------
# Layer 2: dry-run gate.sh against canned logs
# ---------------------------------------------------------------------------------

def _gate_default_instruct_task() -> str:
    """gate.sh's INSTRUCT_TASK default, READ from gate.sh rather than re-typed here.

    It was re-typed, and on 2026-09-14 the default changed and this copy did not — a
    constant labelled "gate.sh's default" that is not gate.sh's default is worse than no
    constant, because it reads as though it were checked.
    """
    import re
    gate = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "ops", "smoke", "gate.sh")
    with open(gate, encoding="utf-8") as fh:
        m = re.search(r'^INSTRUCT_TASK="\$\{INSTRUCT_TASK:-([0-9a-f-]{36})\}"', fh.read(), re.M)
    assert m, "gate.sh no longer declares an INSTRUCT_TASK default in the expected shape"
    return m.group(1)


INSTRUCT_TASK = _gate_default_instruct_task()


def _log_info(msg: str, event: str = "print") -> str:
    """utility.log_info: logger.info(f"{event_name}: {message}") through the
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s' console formatter."""
    return f"2026-09-12 10:00:00,000 - root - INFO - {event}: {msg}"


# Each line cites the producer it was transcribed from. The transcription is the one
# manual step in this file; layer 1 proves the literals still exist, this layer proves
# gate.sh accepts the surrounding shape.
_INSTRUCT_BODY = [
    "[adaptive] arch=Qwen2ForCausalLM param=1,543,714,304 ds_n=27992 seq_p95=2675",  # adaptive_config.py:2496
    "[adaptive] PLAN: lr=1.00e-04 batch=8 epochs=2 max_len=2675 lora=False grad_accum=4",  # adaptive_config.py:2497
    # tokenize_instruct.py:204 prints dedup_knn.dedup_from_env's stats (keys dedup_knn.py:95,111,161,211)
    "[dedup] {'input': 27992, 'exact_removed': 12, 'jaccard_removed': 0, 'after_exact': 27980, "
    "'after_jaccard': 27980, 'enabled': True}",
    # tokenize_instruct.py:233 prints split_policy.leak_safe_split's stats (keys split_policy.py:164-173)
    "[split] {'n': 27980, 'buckets': 27980, 'collapsed': 0, 'oversized_buckets': 0, 'target': 2798, "
    "'dev': 2798, 'train': 25182, 'forced_leak': 0}",
    _log_info("min_data_size_num: 10; max_length: 2675"),                              # train_instruct.py:308
    _log_info("[lr-search] sweeping at batch=8 (training batch is 8)"),                 # train_instruct.py:787
    _log_info("[lr-search] sweep curve written (100 points, accepted=True)"),           # train_instruct.py:876
    _log_info("[lr-search] reloading model to discard the sweep's weights"),            # train_instruct.py:906
    "GO INTO CUSTOMIZED EVALUATE AT STEP: 500",                                         # customized_trainer.py:694
    "Updating the best checkpoint info at step: 500 with eval_loss: 0.05278521",        # customized_trainer.py:708
    "Copy the best checkpoint to the submission directory at step: 500",               # customized_trainer.py:966
]
_KL_LINE = "[kl] checkpoint metric: 0.052785 + 1.5 * 0.001234 = 0.054636"              # customized_trainer.py:331-334
_CHAT_LINE = "Processing chat template dataset type"                                   # tokenize_instruct.py:70
_GRPO_BODY = [
    "Using reward function 0: reward_specific_word_count with weight 1.0000",           # train_grpo.py:289
    # transformers trainer_callback.py ProgressCallback.on_log: write(str(shallow_logs));
    # 'reward' key from trl grpo_trainer.py:1246
    str({"loss": 0.0123, "grad_norm": 1.0, "learning_rate": 8e-06, "reward": 0.4375, "reward_std": 0.12, "epoch": 0.1}),
    str({"loss": 0.0119, "grad_norm": 1.1, "learning_rate": 7e-06, "reward": 0.5625, "reward_std": 0.11, "epoch": 0.2}),
]


def _done(task: str) -> list[str]:
    return [
        _log_info("Training successfully done", "finish"),                              # train_instruct.py:934
        f"Training successfully done for task {task}",                                  # text_trainer.py:1315
    ]


def healthy_canned_logs() -> dict[str, str]:
    """Keyed by --expected-repo-name, which is how the python stub picks a file."""
    instruct = _INSTRUCT_BODY + _done(INSTRUCT_TASK)
    return {
        "gate-instruct": "\n".join(instruct) + "\n",
        "gate-kl": "\n".join(_INSTRUCT_BODY + [_KL_LINE] + _done(INSTRUCT_TASK)) + "\n",
        "dpo-smoke-a": "\n".join(_done("2f7c1a90-5b3e-4a41-9c2f-7d1b6e0a48c3")) + "\n",
        "grpo-smoke-a": "\n".join(_GRPO_BODY + _done("9f1c2d3e-4b5a-6c7d-8e9f-0a1b2c3d4e5f")[1:]) + "\n",
        "chat-smoke": "\n".join([_CHAT_LINE] + instruct) + "\n",
    }


_PY_STUB = """#!/usr/bin/env bash
# Stand-in for python/python3 during the dry run (tests/test_gate_assertions_have_producers.py).
# gate.sh's own PYCHECK scripts run on the real interpreter; the dataset synthesisers are
# no-ops; `python -m text_trainer` replays the canned log for its --expected-repo-name.
real="$GATE_DRY_REAL_PYTHON"
case "${1:-}" in
  */arch.py|*/split.py|*/dedup.py) exec "$real" "$@" ;;
  */make_grpo_data.py) printf '{"reward_functions":[]}\\n' > "$GRPO_DATASET_TYPE_OUT"; exit 0 ;;
  */make_dpo_data.py|*/make_chat_data.py) exit 0 ;;
esac
repo=""; prev=""
for a in "$@"; do
  [ "$prev" = "--expected-repo-name" ] && repo="$a"
  prev="$a"
done
if [ -n "$repo" ]; then
  if [ -f "$GATE_DRY_CANNED_DIR/$repo.log" ]; then cat "$GATE_DRY_CANNED_DIR/$repo.log"; exit 0; fi
  echo "dry-run stub: no canned log for repo '$repo'" >&2; exit 3
fi
exec "$real" "$@"
"""

_RM_STUB = """#!/usr/bin/env bash
# gate.sh's reclaim step rm -rf's /workspace/scripts/soutputs/* and $REPO_DIR/scripts/wandb/*.
# Inside the dry run nothing outside GATE_DRY_ROOT may be touched.
for a in "$@"; do
  case "$a" in
    -*) ;;
    "$GATE_DRY_ROOT"/*) ;;
    *) exit 0 ;;
  esac
done
exec /bin/rm "$@"
"""

_ROW_RE = re.compile(r"^(PASS|FAIL)\s+(\S+)\s+(.*)$")


def _write_exec(path: str, body: str) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def run_dry_gate(tmp_path, canned: dict[str, str], paths: list[str], smoke_dir: str = SMOKE_DIR):
    """Run the real gate.sh with python stubbed. Returns (rows, stdout, work_dir)."""
    if os.path.isdir("/workspace/scripts") or shutil.which("nvidia-smi"):
        pytest.skip("dry run is for CPU boxes: gate.sh's reclaim step deletes real training "
                    "outputs and wait_gpu.sh would block on a live card")
    root = str(tmp_path)
    assert os.path.realpath(root) != os.path.realpath(REPO)
    stub_dir = os.path.join(root, "bin")
    canned_dir = os.path.join(root, "canned")
    work = os.path.join(root, "work")
    fake_repo = os.path.join(root, "fakerepo")
    cwd = os.path.join(root, "cwd")
    for d in (stub_dir, canned_dir, work, os.path.join(fake_repo, "scripts"), cwd):
        os.makedirs(d, exist_ok=True)
    for name in ("python", "python3"):
        _write_exec(os.path.join(stub_dir, name), _PY_STUB)
    _write_exec(os.path.join(stub_dir, "rm"), _RM_STUB)
    for repo, text in canned.items():
        with open(os.path.join(canned_dir, f"{repo}.log"), "w", encoding="utf-8") as fh:
            fh.write(text)
    env = {
        "PATH": stub_dir + os.pathsep + os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": root, "TMPDIR": root, "WORK": work, "REPO_DIR": fake_repo,
        "SKIP_PREFLIGHT": "1", "GATE_DRY_ROOT": root,
        "GATE_DRY_REAL_PYTHON": sys.executable, "GATE_DRY_CANNED_DIR": canned_dir,
        "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
    }
    res = subprocess.run(
        ["bash", os.path.join(smoke_dir, "gate.sh"), *paths],
        cwd=cwd, env=env, capture_output=True, text=True, timeout=300,
    )
    rows = [_ROW_RE.match(ln).groups() for ln in res.stdout.splitlines() if _ROW_RE.match(ln)]
    assert rows, f"gate.sh printed no result table\nstdout:\n{res.stdout}\nstderr:\n{res.stderr}"
    return rows, res.stdout, work


def _artefact_row(detail: str) -> bool:
    # Environment-dependent: /app/checkpoints does not exist on a CPU box. Everything
    # else in the table is decided by the log alone.
    return "model artefact" in detail


def test_dry_gate_all_49_log_gates_pass_on_the_producers_shapes(tmp_path):
    # 44 rows until 2026-09-12; the "no noise fallback" row added to common_gates puts
    # one more on each of the five paths.
    rows, out, _ = run_dry_gate(tmp_path, healthy_canned_logs(), [])
    assert len(rows) == 49, f"expected the 49 rows of a full gate, got {len(rows)}:\n{out}"
    bad = [r for r in rows if r[0] != "PASS" and not _artefact_row(r[2])]
    assert not bad, "log-decided gates failed on canned producer output:\n" + "\n".join(map(str, bad))
    # every path reported, so the log file names gate.sh reads are the ones the run
    # scripts wrote (a mismatch collapses a path to one 'no log at' row)
    assert {r[1] for r in rows} == {"instruct", "kl", "dpo", "grpo", "chat"}
    assert sum(1 for r in rows if r[1] == "instruct") == 12
    assert sum(1 for r in rows if r[1] == "kl") == 12
    assert sum(1 for r in rows if r[1] == "chat") == 13
    assert sum(1 for r in rows if r[1] == "grpo") == 7
    assert sum(1 for r in rows if r[1] == "dpo") == 5


def test_dry_gate_catches_a_missing_producer(tmp_path):
    """The dry run is only worth having if a silent log change turns it red."""
    canned = healthy_canned_logs()
    canned["gate-instruct"] = canned["gate-instruct"].replace("sweep curve written", "sweep curve persisted")
    rows, _, _ = run_dry_gate(tmp_path, canned, ["instruct"])
    fails = [r for r in rows if r[0] == "FAIL" and not _artefact_row(r[2])]
    assert fails == [("FAIL", "instruct", "sweep curve was not written")], rows


def test_gate_rejects_a_run_that_fell_back_to_noise(tmp_path):
    """Was a strict xfail until 2026-09-12: gate.sh read `Training successfully done` as
    proof the post-training checks ran, but text_trainer.py prints it BEFORE the NaN scan
    (:1315 vs :1321) and train_instruct.py:934 streams the same words the moment
    trainer.train() returns. A noised-base forfeit passed every common gate — the exact
    shape the ZeRO-3 checkpointing branch exists to prevent. common_gates now fails on
    `falling back to noise` / `[stage] noise fallback:`, both printed only on that path.
    """
    canned = healthy_canned_logs()
    canned["gate-instruct"] += "\n".join([
        f"NaN/Inf in submission checkpoint for task {INSTRUCT_TASK}; falling back to noise",  # text_trainer.py:1331
        f"Training failed for task {INSTRUCT_TASK}",                                          # text_trainer.py:1381
        "[stage] noise fallback: 11.0s (cumulative 11.0s, +2485s to end_time)",             # text_trainer.py:1397
    ]) + "\n"
    rows, _, _ = run_dry_gate(tmp_path, canned, ["instruct"])
    # "training completed" may still PASS — the trainer really did return with a model
    # before the post-training scan threw it away. What must never happen is the gate
    # ending green: the fallback has to surface as its own FAIL row.
    fell_back = [r for r in rows if r[0] == "FAIL" and "noised base" in r[2]]
    assert fell_back, f"a forfeit produced no FAIL row: {rows}"
    assert any(r[0] == "FAIL" for r in rows), "gate would have exited green on a forfeit"


@pytest.mark.xfail(
    strict=True,
    reason="gate.sh:144 takes `tail -1` of the [dedup] lines; tokenize_instruct.py:208 prints "
           "a `[dedup] dedup crosscheck: ...` line AFTER the stats dict whenever validator "
           "baseline_stats carry near_duplicate_rate, and PYCHECK_DEDUP treats a line with "
           "no dict as `n=0` => pass. Latent on the smoke box (BASELINE_STATS_PATH unset).",
)
def test_gate_dedup_check_survives_a_trailing_crosscheck_line(tmp_path):
    canned = healthy_canned_logs()
    collapsed = canned["gate-instruct"].replace("'after_exact': 27980, 'after_jaccard': 27980",
                                                "'after_exact': 1, 'after_jaccard': 1")
    collapsed = collapsed.replace(
        "[split]",
        "[dedup] dedup crosscheck: ours(exact)=1.0000 validator(near)=0.0100 — WARNING: we removed far "
        "more than the validator saw duplicates\n[split]",  # baseline_signals.py:248-250 via tokenize_instruct.py:208
        1,
    )
    canned["gate-instruct"] = collapsed
    rows, _, _ = run_dry_gate(tmp_path, canned, ["instruct"])
    dedup_rows = [r for r in rows if "dedup" in r[2]]
    assert dedup_rows and all(r[0] == "FAIL" for r in dedup_rows), rows


# ---------------------------------------------------------------------------------
# Layer 3: the shell parses, and preflight's CPU-safe part agrees with the pins
# ---------------------------------------------------------------------------------

SMOKE_SCRIPTS = sorted(f for f in os.listdir(SMOKE_DIR) if f.endswith(".sh")) if os.path.isdir(SMOKE_DIR) else []


@pytest.mark.parametrize("script", SMOKE_SCRIPTS)
def test_smoke_script_parses(script):
    res = subprocess.run(["bash", "-n", os.path.join(SMOKE_DIR, script)], capture_output=True, text=True)
    assert res.returncode == 0, res.stderr


def test_preflight_pin_check_passes_under_this_interpreter():
    """preflight.sh's first block compares the importable stack with the tournament pins.
    That block needs no GPU; run it under the interpreter running these tests. The rest
    of preflight needs /workspace/axo_py, redis, nvidia-smi, a CUDA-visible torch, 100G
    of disk and /cache — on a CPU box those rows FAIL and the script exits 1, by design."""
    pytest.importorskip("transformers")
    env = dict(os.environ)
    env["PATH"] = os.path.dirname(sys.executable) + os.pathsep + env.get("PATH", "")
    env["REPO_DIR"] = REPO
    res = subprocess.run(["bash", os.path.join(SMOKE_DIR, "preflight.sh")],
                         capture_output=True, text=True, env=env, timeout=300)
    for pin in ("transformers==4.51.3", "trl==0.18.0", "peft==0.15.1", "datasets==3.5.0"):
        assert re.search(rf"^\s*OK\s+{re.escape(pin)}", res.stdout, re.M), (
            f"preflight did not accept {pin} under {sys.executable}:\n{res.stdout}"
        )
    assert "FAIL  trainer stack" not in res.stdout, res.stdout
    import torch
    if not torch.cuda.is_available():
        assert res.returncode == 1
        assert "torch.cuda is unavailable" in res.stdout or "no nvidia-smi" in res.stdout, res.stdout
