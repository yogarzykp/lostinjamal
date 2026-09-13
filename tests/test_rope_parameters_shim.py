"""A config written by transformers 5.x must load under our 4.51.3 with the right rope.

transformers 5.x writes positional-encoding settings as one dict,
`rope_parameters: {rope_theta, rope_type, ...scaling}`, with no top-level `rope_theta`
or `rope_scaling`, and `dtype` instead of `torch_dtype`. Our pinned 4.51.3 knows none of
that: it keeps `rope_parameters` as an unknown attribute and builds the model from the
class defaults — rope_theta 10000, rope_scaling None.

Measured 2026-09-13 with real files (tests/fixtures/rope/): SmolLM2-360M saved by 5.12.1
loads as theta 10000 instead of 100000; Hermes-3-Llama-3.1-8B re-saved by 5.12.1 loads
as theta 10000 instead of 500000 AND loses its llama3 scaling. Every augmented mirror
(~50% of tasks, the tournament's own re-save of the base) and every merged base
arrives in this shape. The retained boss, on our exact pin, lost both augmented instruct
tasks and won both un-augmented ones.

It is worse than "consistently wrong": 4.51.3's save carries `rope_parameters` through
untouched and the validator's 5.12.1 honours it — measured — so we TRAIN at 10000 and
are SCORED at 100000/500000. The weights adapt to one encoding and are judged under
another.

The shim reads the raw JSON and hands the legacy keys back as from_pretrained kwargs,
which is the documented override path and touches neither PEFT (its `config` kwarg is
a PeftConfig) nor liger (it forwards unknown kwargs). The save side needs nothing: 5.12.1
reads a 4.x-shaped config correctly, also measured.
"""

import json
import os
import shutil
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
FIX = os.path.join(ROOT, "tests", "fixtures", "rope")

from config_shim import legacy_rope_kwargs, load_kwargs_for  # noqa: E402


def _raw(name):
    return json.load(open(os.path.join(FIX, name)))


# --- the mapping, on real files ----------------------------------------------------------

def test_smollm2_written_by_5x_gets_its_theta_back():
    kw = legacy_rope_kwargs(_raw("smollm2_written_by_5.12.1.json"))
    assert kw["rope_theta"] == 100000
    assert "rope_scaling" not in kw, "rope_type default must not invent a scaling dict"
    assert "torch_dtype" not in kw, "every load site sets torch_dtype explicitly; a second value would collide"


def test_hermes3_written_by_5x_gets_theta_and_llama3_scaling_back():
    kw = legacy_rope_kwargs(_raw("hermes3_llama3_scaling_written_by_5.12.1.json"))
    assert kw["rope_theta"] == 500000.0
    assert kw["rope_scaling"] == {
        "rope_type": "llama3", "factor": 8.0, "high_freq_factor": 4.0,
        "low_freq_factor": 1.0, "original_max_position_embeddings": 8192,
    }


def test_a_4x_shaped_config_is_left_alone():
    assert legacy_rope_kwargs(_raw("hermes3_upstream_4.x.json")) == {}


def test_top_level_keys_win_when_both_are_present():
    """A 4.51.3 re-save of a 5.x base carries both; the top-level value is what this
    stack used, and a caller that already set it must not be overridden."""
    raw = _raw("smollm2_written_by_5.12.1.json")
    raw["rope_theta"] = 100000
    assert legacy_rope_kwargs(raw) == {}


def test_garbage_is_ignored_not_raised():
    assert legacy_rope_kwargs({"rope_parameters": "not a dict"}) == {}
    assert legacy_rope_kwargs({"rope_parameters": {"rope_type": "default"}}) == {}
    assert legacy_rope_kwargs(None) == {}


def test_load_kwargs_for_a_directory_without_config_is_empty(tmp_path):
    assert load_kwargs_for(str(tmp_path)) == {}


# --- the thing that matters: the model's positional encoding ------------------------------

torch = pytest.importorskip("torch")
from transformers import AutoConfig, AutoModelForCausalLM, LlamaConfig, LlamaForCausalLM  # noqa: E402


def _tiny_llama_dir(tmp_path, name, **cfg_overrides):
    d = tmp_path / name
    cfg = LlamaConfig(vocab_size=64, hidden_size=32, intermediate_size=64, num_hidden_layers=1,
                      num_attention_heads=4, num_key_value_heads=4, max_position_embeddings=64,
                      rope_theta=500000.0,
                      rope_scaling={"rope_type": "llama3", "factor": 8.0, "high_freq_factor": 4.0,
                                    "low_freq_factor": 1.0, "original_max_position_embeddings": 8192})
    torch.manual_seed(0)
    LlamaForCausalLM(cfg).save_pretrained(str(d))
    raw = json.load(open(d / "config.json"))
    raw.update(cfg_overrides)
    json.dump(raw, open(d / "config.json", "w"))
    return str(d)


def _as_5x_shape(raw):
    """Rewrite a 4.x config.json dict the way transformers 5.12.1 saves it (measured)."""
    rp = {"rope_theta": raw.pop("rope_theta")}
    sc = raw.pop("rope_scaling", None) or {}
    rp.update(sc)
    rp.setdefault("rope_type", "default")
    raw["rope_parameters"] = rp
    raw.pop("torch_dtype", None)
    raw["dtype"] = "float32"
    return raw


def test_the_misread_is_real_on_this_stack(tmp_path):
    """Precondition for everything else: without the shim the encoding is wrong."""
    good = _tiny_llama_dir(tmp_path, "good")
    bad = tmp_path / "bad"; shutil.copytree(good, bad)
    json.dump(_as_5x_shape(json.load(open(bad / "config.json"))), open(bad / "config.json", "w"))

    c = AutoConfig.from_pretrained(str(bad))
    assert c.rope_theta == 10000.0 and c.rope_scaling is None


def test_the_shim_restores_the_exact_positional_encoding(tmp_path):
    good = _tiny_llama_dir(tmp_path, "good")
    bad = tmp_path / "bad"; shutil.copytree(good, bad)
    json.dump(_as_5x_shape(json.load(open(bad / "config.json"))), open(bad / "config.json", "w"))

    ref = AutoModelForCausalLM.from_pretrained(good)
    unshimmed = AutoModelForCausalLM.from_pretrained(str(bad))
    shimmed = AutoModelForCausalLM.from_pretrained(str(bad), **load_kwargs_for(str(bad)))

    ref_f, un_f, sh_f = (m.model.rotary_emb.inv_freq for m in (ref, unshimmed, shimmed))
    assert not torch.allclose(ref_f, un_f), "the 5.x shape loaded with the right inv_freq without the shim — fixture is wrong"
    assert torch.allclose(ref_f, sh_f), "the shim did not restore the positional encoding"
    assert shimmed.config.rope_theta == 500000.0
    assert shimmed.config.rope_scaling["rope_type"] == "llama3"


def test_a_shimmed_save_carries_both_shapes_consistently(tmp_path):
    """What the validator reads: 5.12.1 honours rope_parameters (measured). After a
    shimmed load, save_pretrained writes rope_theta=500000 AND the carried
    rope_parameters{500000} — train and score agree. Before the shim the pair was
    rope_theta=10000 beside rope_parameters{500000}: trained one way, scored another."""
    good = _tiny_llama_dir(tmp_path, "good")
    bad = tmp_path / "bad"; shutil.copytree(good, bad)
    json.dump(_as_5x_shape(json.load(open(bad / "config.json"))), open(bad / "config.json", "w"))
    m = AutoModelForCausalLM.from_pretrained(str(bad), **load_kwargs_for(str(bad)))
    m.save_pretrained(str(tmp_path / "out"))
    saved = json.load(open(tmp_path / "out" / "config.json"))
    assert saved["rope_theta"] == 500000.0
    assert saved["rope_parameters"]["rope_theta"] == 500000.0
    assert saved["rope_scaling"]["rope_type"] == "llama3"


# --- the wire ------------------------------------------------------------------------------

@pytest.mark.parametrize("script,marker", [
    ("train_instruct.py", "load_with_attn_fallback("),
    ("train_dpo.py", "load_with_attn_fallback("),
    ("train_grpo.py", "load_with_attn_fallback("),
    ("dev_absorption.py", "AutoModelForCausalLM.from_pretrained("),
    ("dynamics_utils.py", "AutoModelForCausalLM.from_pretrained("),
])
def test_every_model_load_site_goes_through_the_shim(script, marker):
    """Correct code nothing calls is this repo's most expensive bug class."""
    src = open(os.path.join(ROOT, "scripts", script), encoding="utf-8").read()
    starts = [i for i in range(len(src)) if src.startswith(marker, i)]
    assert starts, f"{script}: no {marker}"
    for i in starts:
        window = src[i:i + 900]
        assert "load_kwargs_for(" in window or "_rope_load_kwargs(" in window or "_rope_kw(" in window, (
            f"{script}: a model load at offset {i} does not pass **load_kwargs_for(...)"
        )


# --- the exact call shape the trainers use, executed ------------------------------------------

def _bad_and_good(tmp_path):
    good = _tiny_llama_dir(tmp_path, "good")
    bad = tmp_path / "bad"; shutil.copytree(good, bad)
    json.dump(_as_5x_shape(json.load(open(bad / "config.json"))), open(bad / "config.json", "w"))
    return good, str(bad)


def test_load_with_attn_fallback_carries_the_shim_through_a_retry(tmp_path):
    """train_instruct/dpo/grpo call load_with_attn_fallback(loader, path, model_kwargs=...,
    log=..., **load_kwargs_for(path)). The extra kwargs must reach the loader on the first
    attempt AND on the sdpa retry, and must not leak into model_kwargs (PEFT reuses it)."""
    from attn_fallback import load_with_attn_fallback
    good, bad = _bad_and_good(tmp_path)
    ref = AutoModelForCausalLM.from_pretrained(good).model.rotary_emb.inv_freq

    calls = []

    def loader(path, **kw):
        calls.append(dict(kw))
        if kw.get("attn_implementation") == "flash_attention_2":
            raise ImportError("flash_attn not installed")
        return AutoModelForCausalLM.from_pretrained(path, **kw)

    model_kwargs = dict(torch_dtype=torch.float32, attn_implementation="flash_attention_2")
    m = load_with_attn_fallback(loader, bad, model_kwargs=model_kwargs, log=lambda *_: None,
                                **load_kwargs_for(bad))
    assert torch.allclose(m.model.rotary_emb.inv_freq, ref)
    assert len(calls) == 2 and all("rope_theta" in c for c in calls), calls
    assert "rope_theta" not in model_kwargs, "the shim leaked into the shared model_kwargs"
    assert model_kwargs["attn_implementation"] == "sdpa"


def test_dev_absorption_loads_a_5x_shaped_submission_through_the_shim(tmp_path):
    """The one place we reload our OWN checkpoint — after a 4.51.3 save it is 4.x-shaped,
    but a submission that came from a merge or an adapter merge may not be."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("dev_absorption_rope", os.path.join(ROOT, "scripts", "dev_absorption.py"))
    da = importlib.util.module_from_spec(spec); spec.loader.exec_module(da)

    good, bad = _bad_and_good(tmp_path)
    # a real tokenizer + dev split + armed guard, the way the other real-stack test does it
    from tokenizers import Tokenizer, models, pre_tokenizers
    from transformers import PreTrainedTokenizerFast
    vocab = {f"<{i}>": i for i in range(64)}; vocab.update({"<pad>": 0, "<s>": 1, "</s>": 2})
    tok = Tokenizer(models.WordLevel(vocab=vocab, unk_token="<3>")); tok.pre_tokenizer = pre_tokenizers.Whitespace()
    PreTrainedTokenizerFast(tokenizer_object=tok, pad_token="<pad>", bos_token="<s>", eos_token="</s>", unk_token="<3>").save_pretrained(bad)
    (tmp_path / "bad" / "loss.txt").write_text("7,99.0")
    rows = [{"input_ids": [1, 5, 6, 7, 2], "labels": [1, 5, 6, 7, 2]}] * 12
    dev = tmp_path / "dev.json"; dev.write_text(json.dumps(rows))

    log = []
    got = da.absorb_dev_split(submission_dir=bad, dev_tokenized_path=str(dev), base_lr=1e-3,
                              end_time="2099-01-01 00:00:00", log=log.append)
    assert got is not None, "\n".join(log)
    assert any("[config-shim]" in m and "500000" in m for m in log), log
