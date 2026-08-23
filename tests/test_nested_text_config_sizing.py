"""A wrapped decoder must not be sized as if it were a 1B model.

Wrapper architectures keep the decoder's real dimensions one level down, in a sub-config
transformers calls `text_config`. Every sizing sensor here read the TOP level only, so on
such a model they all returned None at once — and the failure compounds rather than
surfacing: `get_param_count` returns None, adaptive_config's "assume 1B" default fires,
the vocab-aware OOM cap cannot arm because vocab_size is None, and a 9.65B model is
planned as a full fine-tune with a batch sized for something ten times smaller.

Independent of the transformers version. Upgrading so the architecture LOADS does not
move those numbers to the top level.

The regression risk runs the other way, and several tests below exist only to pin it:
this helper is dropped into the sizing path of EVERY task, so a flat config must keep
returning exactly what it returned before.
"""

import os
import sys

import pytest

SCRIPTS = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, SCRIPTS)

pytest.importorskip("transformers")

from dynamics_utils import cfg_get  # noqa: E402


class Flat:
    """A config that exposes its dimensions directly, like llama or qwen."""

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)


class Wrapped:
    """A config whose real decoder dimensions live under `text_config`."""

    def __init__(self, text_config, **top):
        self.text_config = text_config
        for k, v in top.items():
            setattr(self, k, v)


# --------------------------------------------------------------------------
# The regression direction: flat configs must be untouched
# --------------------------------------------------------------------------

def test_a_flat_config_reads_exactly_as_before():
    cfg = Flat(hidden_size=4096, vocab_size=151936, num_hidden_layers=32)
    assert cfg_get(cfg, "hidden_size") == 4096
    assert cfg_get(cfg, "vocab_size") == 151936
    assert cfg_get(cfg, "num_hidden_layers") == 32


def test_a_missing_field_still_returns_the_default():
    assert cfg_get(Flat(hidden_size=8), "num_key_value_heads") is None
    assert cfg_get(Flat(hidden_size=8), "num_key_value_heads", default=7) == 7


def test_the_nest_wins_when_both_declare_a_field():
    """Corrected after measuring; this test originally demanded the opposite.

    "Top level first" looks like the safe rule, and is wrong for exactly the models this
    exists for. transformers does not leave the top level empty on a wrapped config — it
    builds a config class, and the class supplies a DEFAULT for every standard field. A
    wrapped 9B decoder read back vocab_size=32000, the LlamaConfig default, while the
    real 151936 sat in text_config. A missing value announces itself; a default does not.
    """
    cfg = Wrapped(text_config=Flat(hidden_size=3584), hidden_size=4096)
    assert cfg_get(cfg, "hidden_size") == 3584, (
        "the wrapper's own value shadowed the decoder's; on a real wrapped config that "
        "value is a class default, not a measurement"
    )


def test_a_flat_config_is_untouched_because_it_has_no_nest():
    """The safety property, restated: this drops into the sizing path of EVERY task."""
    cfg = Flat(hidden_size=4096, vocab_size=32000, alibi=False)
    assert cfg_get(cfg, "hidden_size") == 4096
    assert cfg_get(cfg, "vocab_size") == 32000
    assert cfg_get(cfg, "alibi") is False


def test_a_false_value_is_not_treated_as_absent():
    """`alibi=False` is an answer, not a missing field — in the nest or out of it."""
    assert cfg_get(Wrapped(text_config=Flat(alibi=False), alibi=True), "alibi") is False
    assert cfg_get(Flat(alibi=False), "alibi") is False


# --------------------------------------------------------------------------
# The reason it exists
# --------------------------------------------------------------------------

def test_reads_through_a_nested_config_object():
    cfg = Wrapped(text_config=Flat(hidden_size=3584, vocab_size=151936,
                                   num_hidden_layers=28, intermediate_size=18944))
    assert cfg_get(cfg, "hidden_size") == 3584
    assert cfg_get(cfg, "vocab_size") == 151936
    assert cfg_get(cfg, "num_hidden_layers") == 28


def test_reads_through_a_nested_config_that_is_still_a_dict():
    """The case that actually occurs: a stack whose transformers does not know the nested
    type leaves it as the raw mapping it was parsed from."""
    cfg = Wrapped(text_config={"hidden_size": 3584, "vocab_size": 151936,
                               "num_hidden_layers": 28})
    assert cfg_get(cfg, "hidden_size") == 3584
    assert cfg_get(cfg, "vocab_size") == 151936


def test_alternate_nest_names_are_followed():
    for nest in ("llm_config", "language_config", "decoder"):
        cfg = Flat(**{nest: {"hidden_size": 2048}})
        assert cfg_get(cfg, "hidden_size") == 2048, f"{nest} was not consulted"


def test_multiple_names_are_tried_in_order():
    """intermediate_size OR ffn_dim, the OPT case, and it must work through a nest too."""
    assert cfg_get(Flat(ffn_dim=4096), "intermediate_size", "ffn_dim") == 4096
    assert cfg_get(Wrapped(text_config={"ffn_dim": 4096}),
                   "intermediate_size", "ffn_dim") == 4096
    assert cfg_get(Flat(intermediate_size=1, ffn_dim=2),
                   "intermediate_size", "ffn_dim") == 1


def test_nothing_anywhere_returns_the_default():
    assert cfg_get(Wrapped(text_config={}), "hidden_size") is None
    assert cfg_get(Flat(), "hidden_size", default=0) == 0


# --------------------------------------------------------------------------
# The consequence, end to end
# --------------------------------------------------------------------------

def _param_count_from(cfg_dict, tmp_path):
    import json
    from dynamics_utils import get_param_count
    root = os.path.join(str(tmp_path), "m")
    os.makedirs(root, exist_ok=True)
    with open(os.path.join(root, "config.json"), "w") as fh:
        json.dump(cfg_dict, fh)
    return get_param_count(root)


def test_param_count_no_longer_collapses_to_the_1b_default(tmp_path):
    """The compounding failure: None here becomes 'assume 1B' in adaptive_config."""
    nested = {
        "model_type": "llama",
        "architectures": ["LlamaForCausalLM"],
        "text_config": {
            "hidden_size": 3584, "num_hidden_layers": 28, "vocab_size": 151936,
            "intermediate_size": 18944, "num_attention_heads": 28,
        },
    }
    got = _param_count_from(nested, tmp_path)
    assert got is not None, (
        "get_param_count still returns None for a wrapped decoder, so adaptive_config "
        "will default to 1B and plan a full fine-tune for a model many times that size"
    )
    assert got > 5e9, f"counted {got:.3g} params for a ~9B decoder"


def test_the_same_dimensions_count_the_same_wherever_they_are_declared(tmp_path):
    dims = dict(hidden_size=3584, num_hidden_layers=28, vocab_size=151936,
                intermediate_size=18944, num_attention_heads=28)
    flat = {"model_type": "llama", "architectures": ["LlamaForCausalLM"], **dims}
    nested = {"model_type": "llama", "architectures": ["LlamaForCausalLM"],
              "text_config": dict(dims)}
    a = _param_count_from(flat, os.path.join(str(tmp_path), "flat"))
    b = _param_count_from(nested, os.path.join(str(tmp_path), "nested"))
    assert a == b, (
        f"flat counted {a}, nested counted {b} — the nested read is picking up the config "
        f"class's defaults instead of the declared dimensions"
    )


def test_the_vocab_aware_oom_cap_can_now_arm_on_a_wrapped_model(tmp_path):
    """The cap is gated on `vocab_size >= 100000 and param_count >= 1e9`. Both inputs
    came back None on a wrapped model, so the branch was structurally unreachable."""
    nested = {
        "model_type": "llama", "architectures": ["LlamaForCausalLM"],
        "text_config": {
            "hidden_size": 3584, "num_hidden_layers": 28, "vocab_size": 151936,
            "intermediate_size": 18944,
        },
    }
    param_count = _param_count_from(nested, tmp_path)
    from transformers import AutoConfig
    cfg = AutoConfig.from_pretrained(os.path.join(str(tmp_path), "m"))
    vocab = cfg_get(cfg, "vocab_size")
    assert vocab and vocab >= 100000 and param_count >= 1e9, (
        f"cap inputs still unusable: vocab_size={vocab}, param_count={param_count}"
    )
