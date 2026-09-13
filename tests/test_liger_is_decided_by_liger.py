"""Whether to use liger is liger's decision, not a hand-written list's.

The adaptive path hardcoded `"use_liger": False,  # arch-dependent, conservative default`
(adaptive_config.py) while the legacy path and the retained boss both call
get_use_liger(architecture). With liger off there is no fused cross-entropy, so the full
[B, T, V] logits are materialised — on gemma-2-2b that is a 256k vocab, which is the memory
pressure the vocab-aware batch cap exists to relieve. Tournament run 59469903 planned a
bucket of 60 and trained at 8.

The list itself was also wrong. Asked directly, liger-kernel 0.5.9 patches 19 model types:

    gemma gemma2 gemma3 gemma3_text glm4 granite llama llava mistral mixtral
    mllama mllama_text_model olmo2 paligemma phi3 qwen2 qwen2_5_vl qwen2_vl qwen3

The hand list had 8 and omitted `granite` — the model_type of two of the three 2026-pool
models our pinned transformers can actually build. It also cannot express the distinctions
that matter: detect_arch_family returns coarse families (`gemma`, `qwen`), which cannot tell
gemma2 from a gemma3 variant, and `get_use_liger` keys on the architecture CLASS name, which
anonymised tasks defeat.

So the decision reads `model_type` from the config and asks liger's own dispatch map. When
liger cannot be imported — this CPU venv, deliberately — it falls back to a mirror of the
pinned map, and a test asserts the mirror still matches the live map wherever liger IS
installed, so drift is caught in the image rather than in a tournament.
"""

import json
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import model_utility as mu  # noqa: E402

LIVE_0_5_9 = {
    "gemma", "gemma2", "gemma3", "gemma3_text", "glm4", "granite", "llama", "llava",
    "mistral", "mixtral", "mllama", "mllama_text_model", "olmo2", "paligemma", "phi3",
    "qwen2", "qwen2_5_vl", "qwen2_vl", "qwen3",
}


def _model_dir(tmp_path, **cfg):
    d = tmp_path / "m"
    d.mkdir(exist_ok=True)
    (d / "config.json").write_text(json.dumps(cfg))
    return str(d)


def test_the_mirror_matches_what_this_repo_pins():
    assert set(mu.LIGER_MODEL_TYPES_PINNED) == LIVE_0_5_9


@pytest.mark.skipif(
    __import__("importlib").util.find_spec("liger_kernel") is None,
    reason="liger-kernel is GPU-only and absent from the CPU venv; this runs in the image",
)
def test_the_mirror_has_not_drifted_from_the_installed_liger():
    """Where liger IS installed — the trainer image — the mirror must equal the live map."""
    from liger_kernel.transformers.monkey_patch import MODEL_TYPE_TO_APPLY_LIGER_FN as live
    assert set(mu.LIGER_MODEL_TYPES_PINNED) == set(live), (
        f"liger's dispatch map changed: only-in-mirror={set(mu.LIGER_MODEL_TYPES_PINNED) - set(live)}, "
        f"only-in-liger={set(live) - set(mu.LIGER_MODEL_TYPES_PINNED)}"
    )


@pytest.mark.parametrize("model_type,want", [
    ("qwen2", "True"), ("llama", "True"), ("gemma2", "True"), ("phi3", "True"),
    ("granite", "True"),        # two of the three buildable 2026-pool models
    ("qwen3", "True"), ("olmo2", "True"), ("glm4", "True"),
    ("qwen3_5", "False"),       # 2026 pool, liger does not patch it
    ("lfm2", "False"), ("lfm2_moe", "False"), ("gemma4", "False"),
    ("opt", "False"), ("", "False"),
])
def test_use_liger_follows_the_model_type(tmp_path, model_type, want):
    assert mu.get_use_liger_for_path(_model_dir(tmp_path, model_type=model_type)) == want


def test_a_wrapped_decoder_is_read_one_level_down(tmp_path):
    """Wrapper architectures keep model_type in text_config; a top-level read sees nothing."""
    d = _model_dir(tmp_path, architectures=["SomethingForConditionalGeneration"],
                   text_config={"model_type": "qwen2"})
    assert mu.get_use_liger_for_path(d) == "True"


def test_an_unreadable_config_fails_closed(tmp_path):
    """Never guess True: liger patches the model in place, and a wrong patch is a crash."""
    assert mu.get_use_liger_for_path(str(tmp_path / "does-not-exist")) == "False"
    bad = tmp_path / "bad"; bad.mkdir(); (bad / "config.json").write_text("{not json")
    assert mu.get_use_liger_for_path(str(bad)) == "False"


def test_the_adaptive_path_no_longer_hardcodes_false():
    src = open(os.path.join(ROOT, "scripts", "adaptive_config.py"), encoding="utf-8").read()
    assert '"use_liger": False' not in src, "adaptive still hardcodes use_liger False"
    assert "get_use_liger_for_path" in src, "adaptive does not ask liger about the model"


def test_the_legacy_hand_list_still_agrees_where_it_speaks(tmp_path):
    """get_use_liger (class-name based) stays for the legacy configs. Every class it says
    True for must still be a model_type liger patches — otherwise the two paths disagree."""
    pairs = [("Qwen2ForCausalLM", "qwen2"), ("LlamaForCausalLM", "llama"),
             ("Gemma2ForCausalLM", "gemma2"), ("MistralForCausalLM", "mistral"),
             ("MixtralForCausalLM", "mixtral"), ("Qwen3ForCausalLM", "qwen3"),
             ("Phi3ForCausalLM", "phi3"), ("GemmaForCausalLM", "gemma")]
    for cls, mt in pairs:
        assert mu.get_use_liger(cls) == "True"
        assert mt in mu.LIGER_MODEL_TYPES_PINNED, f"{cls} -> {mt} not patched by liger"
