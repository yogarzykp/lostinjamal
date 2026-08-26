"""Two ways the model size can be wrong, both currently silent, neither changed here.

This file guards diagnostics, not behaviour, and that is the point. Both findings below
would alter a tournament run's training plan if acted on, and one of them would switch on
a path — ZeRO-3 — that has never executed in this repository's smoke suite. The house
pattern for an unmeasured action is to log it and decline it (see AUG_PRUNING_LR_FACTOR in
adaptive_config.py). These tests exist to pin that the logging is real and the value is
untouched, so the decision can be made from evidence later instead of an argument now.

**The MoE undercount is the sharper of the two, because it fires on the SUCCESS path.**
get_param_count sums one MLP per layer. A mixture-of-experts model carries one per expert,
so Mixtral-8x7B computes to 7.9B against a real 46.7B — with no WARN, because nothing
failed. Every size gate downstream reads that number: the LoRA gates at 5e9/1.5e9, the
DeepSpeed gate at 9e9, the batch buckets. At 7.9B a 47B model gets a full fine-tune, plain
DDP and a large batch. Not hypothetical: family_lr_table.py carries empirical mixtral rows
and general_hp_resolver maps phimoeforcausallm.

**The AutoConfig failure is narrower but points the same way.** Returning None lands the
caller on adaptive_config's 1B sentinel, and 1B is the aggressive direction, not the
conservative one — every gate above stays shut at once. The live door is gpt_oss:
text_trainer excludes it from the unloadable-architecture preflight on purpose, and
adaptive_config runs in that same process against transformers 4.51.3.

Tests exec the functions out of source; dynamics_utils imports torch at module scope, and a
suite that skips wherever the training extras are absent would not run on any machine we
develop on.
"""

from __future__ import annotations

import ast
import json
import os

import pytest

SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
DYNAMICS = os.path.join(SCRIPTS, "dynamics_utils.py")

WANTED = {
    "cfg_get",
    "_advise_param_count_from_raw_json",
    "_advise_moe_undercount",
    "get_param_count",
}


class _Cfg:
    def __init__(self, **kw):
        self.__dict__.update(kw)


def _source():
    with open(DYNAMICS, "r", encoding="utf-8") as fh:
        return fh.read()


@pytest.fixture
def loaded():
    """(get_param_count, messages, set_config) with AutoConfig replaced."""
    messages = []
    ns = {"os": os, "json": json, "print": lambda *a, **k: messages.append(" ".join(map(str, a)))}
    flag = annotations.compiler_flag
    tree = ast.parse(_source())
    for node in tree.body:
        take = (isinstance(node, ast.FunctionDef) and node.name in WANTED) or isinstance(node, ast.Assign)
        if not take:
            continue
        try:
            exec(compile(ast.Module(body=[node], type_ignores=[]), DYNAMICS, "exec", flags=flag), ns)  # noqa: S102
        except Exception:
            pass
    missing = WANTED - ns.keys()
    assert not missing, f"could not load {missing} out of dynamics_utils.py"

    state = {"cfg": None, "raise": None}

    class _AutoConfig:
        @staticmethod
        def from_pretrained(path, **kw):
            if state["raise"] is not None:
                raise state["raise"]
            return state["cfg"]

    ns["AutoConfig"] = _AutoConfig

    def set_config(cfg=None, error=None):
        state["cfg"], state["raise"] = cfg, error
        messages.clear()

    return ns["get_param_count"], messages, set_config


MIXTRAL = dict(
    hidden_size=4096, num_hidden_layers=32, vocab_size=32000,
    intermediate_size=14336, architectures=["MixtralForCausalLM"],
)
DENSE_B = 7.9157002


# --- the value must not move ------------------------------------------------------


def test_moe_return_value_is_unchanged(loaded):
    """The whole safety of this change rests on this assertion."""
    gpc, _, set_config = loaded
    set_config(_Cfg(num_local_experts=8, **MIXTRAL))
    with_experts = gpc("/m")
    set_config(_Cfg(**MIXTRAL))
    without = gpc("/m")
    assert with_experts == without, "declaring experts changed the returned size"
    assert abs(with_experts / 1e9 - DENSE_B) < 0.01


def test_autoconfig_failure_still_returns_none(loaded):
    gpc, _, set_config = loaded
    set_config(error=ValueError("model type `gpt_oss` not recognized"))
    assert gpc("/nonexistent-path-for-this-test") is None


# --- but it must be said out loud -------------------------------------------------


def test_moe_advisory_names_both_numbers(loaded):
    gpc, msgs, set_config = loaded
    set_config(_Cfg(num_local_experts=8, **MIXTRAL))
    gpc("/m")
    line = next((m for m in msgs if "experts" in m), None)
    assert line, "an MoE config produced no advisory"
    assert "7.92B" in line and "47.38B" in line, f"advisory does not carry both sizes: {line}"
    assert "ADVISORY" in line and "not applied" in line, (
        "the advisory must say it was not applied, or a reader will assume it was"
    )


@pytest.mark.parametrize(
    "key", ["num_local_experts", "num_experts", "n_routed_experts", "moe_num_experts"]
)
def test_every_expert_key_spelling_is_recognised(loaded, key):
    """Families spell it differently; missing one makes the advisory silently absent."""
    gpc, msgs, set_config = loaded
    set_config(_Cfg(**{key: 8}, **MIXTRAL))
    gpc("/m")
    assert any("experts" in m for m in msgs), f"{key} produced no advisory"


def test_a_dense_model_says_nothing(loaded):
    """Control. An advisory on every model would be noise nobody reads."""
    gpc, msgs, set_config = loaded
    set_config(_Cfg(**MIXTRAL))
    gpc("/m")
    assert not [m for m in msgs if "experts" in m]


@pytest.mark.parametrize("experts", [0, 1, None, "eight", -4])
def test_junk_expert_counts_do_not_produce_an_advisory(loaded, experts):
    """1 expert is a dense model; the rest are unusable. None of them is a finding."""
    gpc, msgs, set_config = loaded
    set_config(_Cfg(num_local_experts=experts, **MIXTRAL))
    assert gpc("/m") is not None
    assert not [m for m in msgs if "experts" in m]


def test_autoconfig_failure_is_classified_not_swallowed(loaded):
    """The old code had a bare `except Exception: return None` and said nothing."""
    gpc, msgs, set_config = loaded
    set_config(error=ValueError("model type `gpt_oss` not recognized"))
    gpc("/nonexistent-path-for-this-test")
    line = next((m for m in msgs if "param_count" in m), None)
    assert line, "an AutoConfig failure produced no log at all"
    assert "gpt_oss" in line, "the log does not carry the reason AutoConfig failed"
    assert "1B" in line, "the log does not say which default the caller will land on"


def test_raw_json_estimate_is_reported_when_the_file_is_readable(loaded, tmp_path):
    """AutoConfig needs the architecture registered; these four fields do not."""
    gpc, msgs, set_config = loaded
    (tmp_path / "config.json").write_text(json.dumps({
        "hidden_size": 4096, "num_hidden_layers": 32,
        "vocab_size": 32000, "intermediate_size": 14336,
    }))
    set_config(error=ValueError("model type `gpt_oss` not recognized"))
    assert gpc(str(tmp_path)) is None, "the advisory must not change the return value"
    line = next((m for m in msgs if "raw estimate" in m), None)
    assert line, "a readable config.json produced no raw estimate"
    assert "7.92B" in line
    assert "not applied" in line


def test_nested_text_config_is_read_in_the_raw_fallback(loaded, tmp_path):
    """Wrapper architectures keep the decoder's real fields one level down."""
    gpc, msgs, set_config = loaded
    (tmp_path / "config.json").write_text(json.dumps({
        "vocab_size": 32000,
        "text_config": {"hidden_size": 4096, "num_hidden_layers": 32, "intermediate_size": 14336},
    }))
    set_config(error=ValueError("unrecognised"))
    gpc(str(tmp_path))
    assert any("raw estimate" in m for m in msgs), "nested fields were not found"


def test_unreadable_config_says_so_rather_than_guessing(loaded, tmp_path):
    gpc, msgs, set_config = loaded
    set_config(error=ValueError("unrecognised"))
    gpc(str(tmp_path))
    line = next((m for m in msgs if "param_count" in m), None)
    assert line and "raw estimate" not in line, "an estimate was reported with no file to read"
