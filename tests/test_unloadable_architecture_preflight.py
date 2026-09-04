"""A model no retry can load must not be given the whole budget to prove it.

G.O.D's f7caab6 added a pool of 2026+ base models that one R1 task and one boss-round
task are drawn from, validated against transformers 5.12.x. We pin 4.51.3, which does not
know `qwen3_5`, `gemma4`, `lfm2` or `lfm2_moe` — 9 of the 12 entries. Before this
preflight the task tokenised, then ran MAX_TRIES identical loads that could never
succeed, and only reached the fallback with the clock nearly gone.

The dangerous direction is the OTHER one: diverting a task that WOULD have trained. A
network blip or a half-downloaded snapshot must never be read as "unloadable
architecture", because that converts a recoverable hiccup into a guaranteed base-model
score. Several tests below exist only to pin that.
"""

import ast
import io
import json
import os
import sys
import tempfile
import tokenize

import pytest

SCRIPTS = os.path.join(os.path.dirname(__file__), "..", "scripts")
TRAINER = os.path.join(SCRIPTS, "text_trainer.py")

transformers = pytest.importorskip("transformers")

sys.path.insert(0, SCRIPTS)


def _detector():
    """Import just the function, without dragging in the module's heavy imports."""
    from text_trainer import detect_unloadable_architecture
    return detect_unloadable_architecture


def _write_config(root, **fields):
    os.makedirs(root, exist_ok=True)
    with open(os.path.join(root, "config.json"), "w") as fh:
        json.dump(fields, fh)
    return root


def _code_only(path):
    """Source with comments stripped, so an assertion cannot match our own prose."""
    with open(path) as fh:
        src = fh.read()
    out, prev = [], (1, 0)
    for ttype, tstr, start, end, _ in tokenize.generate_tokens(io.StringIO(src).readline):
        if ttype == tokenize.COMMENT:
            continue
        if start[0] > prev[0]:
            out.append("\n" * (start[0] - prev[0]))
            out.append(" " * start[1])
        elif start[1] > prev[1]:
            out.append(" " * (start[1] - prev[1]))
        out.append(tstr)
        prev = end
    return "".join(out)


# --------------------------------------------------------------------------
# What it must catch
# --------------------------------------------------------------------------

def test_reports_an_architecture_transformers_cannot_build():
    detect = _detector()
    with tempfile.TemporaryDirectory() as tmp:
        path = _write_config(tmp, model_type="not_a_real_architecture_v9",
                             architectures=["TotallyUnknownForCausalLM"])
        reason = detect(path)
        assert reason, "an unbuildable architecture was reported as fine"
        assert "cannot build this architecture" in reason


def test_a_config_with_no_model_type_fails_open():
    """Inverted after measuring. This test originally demanded the opposite.

    transformers raises ValueError for BOTH "this architecture is not in my registry"
    and "there is no usable config here", but they mean opposite things: the first is
    permanent, the second is usually a download that did not finish. A config with no
    `model_type` is the second. Every pool model we need to catch DOES declare one.
    """
    detect = _detector()
    with tempfile.TemporaryDirectory() as tmp:
        path = _write_config(tmp, hidden_size=8)
        assert detect(path) is None, (
            "an incomplete config was treated as a permanent architecture verdict"
        )


# --------------------------------------------------------------------------
# What it must NOT catch — diverting a trainable task is the expensive mistake
# --------------------------------------------------------------------------

def test_a_supported_architecture_is_not_blocked():
    detect = _detector()
    with tempfile.TemporaryDirectory() as tmp:
        path = _write_config(
            tmp, model_type="llama", architectures=["LlamaForCausalLM"],
            hidden_size=8, num_hidden_layers=2, num_attention_heads=2,
            num_key_value_heads=2, vocab_size=64, max_position_embeddings=2048,
            intermediate_size=16,
        )
        assert detect(path) is None, "a loadable model was diverted to the fallback"


def test_a_missing_path_fails_open():
    """Not an architecture problem. Training must still be allowed to try."""
    detect = _detector()
    assert detect("/nonexistent/path/that/does/not/exist") is None


def test_unparseable_json_fails_open():
    """A half-written download is a hiccup, not a permanent architecture verdict."""
    detect = _detector()
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "m"))
        with open(os.path.join(tmp, "m", "config.json"), "w") as fh:
            fh.write("{ this is not json")
        assert detect(os.path.join(tmp, "m")) is None


def test_an_empty_directory_fails_open():
    detect = _detector()
    with tempfile.TemporaryDirectory() as tmp:
        assert detect(tmp) is None


# --------------------------------------------------------------------------
# Wiring: the reason the preflight exists is to skip work, so pin that it does
# --------------------------------------------------------------------------

CODE = _code_only(TRAINER)


def test_gpt_oss_is_excluded_from_the_preflight():
    """gpt_oss is also unknown to 4.51.3, but the existing path upgrades transformers
    for it in a subprocess — so the already-imported transformers here still reports it
    unloadable. Preflighting it would divert a task that recovers perfectly well."""
    assert "None if is_openai else detect_unloadable_architecture" in CODE, (
        "the preflight no longer excludes the openai/gpt_oss path, which the existing "
        "in-container transformers upgrade already handles"
    )


def test_tokenisation_is_skipped_when_the_model_cannot_load():
    """The tokenise call must sit inside `if not load_blocker:`.

    This used to assert on the literal `"tokenize_cmd, os.path.join(ds_folder"` and measure
    the character distance back to the guard. That string stopped existing when the
    tokenisation gate hoisted the log path into a `_tokenise_log` variable — so the test
    raised ValueError on a missing substring rather than failing with a diagnosis, and it
    said nothing about whether the guard had actually survived. It had.

    Ask the syntax tree where the call really sits. A refactor that moves the line is then
    invisible here, and only a refactor that moves it OUT of the guard fails.
    """
    tree = ast.parse(CODE)
    for node in ast.walk(tree):
        if not isinstance(node, ast.If) or not isinstance(node.test, ast.UnaryOp):
            continue
        if "load_blocker" not in ast.dump(node.test):
            continue
        for call in ast.walk(node):
            if (
                isinstance(call, ast.Call)
                and isinstance(call.func, ast.Name)
                and call.func.id == "run_cmd_with_log"
                and any(isinstance(a, ast.Name) and a.id == "tokenize_cmd" for a in call.args)
            ):
                return
    pytest.fail(
        "run_cmd_with_log(tokenize_cmd, ...) is not inside an `if not load_blocker:` block, "
        "so a model no retry can load still spends budget being tokenised for"
    )


def test_the_retry_ladder_is_skipped_when_the_model_cannot_load():
    loop = CODE.index("while True:")
    body = CODE[loop:loop + 400]
    assert "if load_blocker:" in body and "break" in body, (
        "the ladder no longer breaks on an unloadable model, so it will spend the whole "
        "budget on retries that cannot succeed"
    )


def test_the_fallback_still_runs_after_the_preflight_skips_training():
    """train_success must stay False so the existing, tested fallback path fires."""
    assert CODE.index("while True:") < CODE.index("add_random_noise.py"), (
        "the fallback no longer follows the loop"
    )
    assert "if not train_success:" in CODE


def test_detector_is_defined_before_first_use():
    tree = ast.parse(CODE)
    defined = next(n.lineno for n in ast.walk(tree)
                   if isinstance(n, ast.FunctionDef)
                   and n.name == "detect_unloadable_architecture")
    first_use = next(
        n.lineno for n in ast.walk(tree)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
        and n.func.id == "detect_unloadable_architecture"
    )
    assert defined < first_use
