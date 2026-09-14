"""The DPO batch ceiling is the measured peak of one step, not a tier table.

2026-09-14, DPO smoke stage, SmolLM-135M (vocab 49152) on one H100:

    [adaptive] 1-GPU empirical bucket: batch=64 (target=64 for param=0.15B)
    [adaptive] PLAN: ... batch=70 ... max_len=1024          <- planner's length
    DPO max_length=2048, max_prompt_length=1024             <- what it trained at
    batch 70: Tried to allocate 52.50 GiB  = 2 * 70 * 2048 * 49152 * 4
    batch 35: Tried to allocate 26.25 GiB  = 2 * 35 * 2048 * 49152 * 4
    ladder: 70 -> 35 -> 17

That tensor is accelerate's .float() of the bf16 concatenated logits, and it is not the
peak. Profiled on the pinned stack (tests/../scratch repro, torch.profiler memory timeline,
three (B, L)): one step peaks in backward at 3.02 F above baseline, F = 2*B*L*V*4 — the saved
fp32 logits, the gather's full-size grad, and 2B per-row logsumexp grads held at once. With
checkpointed activations that is 24*L*V + 4*L*H*n bytes per pair, and it reconciles both OOM
snapshots within 0.6 GiB.

Three defects, three wires:
  * the bucket scaled by the planner's 1024 while DPO padded to 2048;
  * nothing accounted for the [2B, ...] concatenation;
  * the GQA boost lifted 64 -> 70 after the bucket had said 64.
"""

import ast
import os
import sys

import pytest

SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, SCRIPTS)
ADAPTIVE = os.path.join(SCRIPTS, "adaptive_config.py")

ac = pytest.importorskip("adaptive_config")

GiB = 1024 ** 3

# The run, as read from dpo-a.log and the model's config.json.
SMOL = dict(vocab_size=49152, hidden_size=576, num_hidden_layers=30,
            param_count=147_750_912, use_lora=False, dpo_max_length=2048,
            longest_pair=6717, vram_available_gb=78.66)


# ------------------------------------------------------------------ the arithmetic

def test_the_forward_alloc_is_reproduced_exactly():
    """The two OOM messages ARE the 2*B*L*V*4 tensor, to the byte."""
    assert 2 * 70 * 2048 * 49152 * 4 / GiB == 52.5
    assert 2 * 35 * 2048 * 49152 * 4 / GiB == 26.25


@pytest.mark.parametrize("batch,fits", [(70, False), (35, False), (24, True), (17, True)])
def test_the_peak_model_separates_the_rungs_that_oomed_from_the_ones_that_ran(batch, fits):
    """Both OOM rungs must be predicted NOT to fit in 79.11 GiB; the ladder's 17 and the
    ceiling's 24 must. A model that cannot tell those apart is not a model of this run."""
    per_pair = 24 * 2048 * 49152 + 4 * 2048 * 576 * 30
    resident = 8 * 147_750_912
    peak = (batch * per_pair + resident) / GiB
    assert (peak < 79.11) is fits, f"batch {batch}: predicted peak {peak:.1f} GiB"


def test_the_ceiling_on_this_run_is_24():
    assert ac.dpo_batch_ceiling(**SMOL) == 24


def test_the_ceiling_beats_the_ladder_and_stays_under_the_physics():
    """17 was the ladder's landing; ~32 is the unmargined physical limit."""
    cap = ac.dpo_batch_ceiling(**SMOL)
    assert 17 < cap < 32


def test_the_ceiling_scales_with_vocab_not_only_params():
    """The bucket cannot see the vocab term; the ceiling must. Same model, Qwen-sized vocab."""
    big_vocab = dict(SMOL, vocab_size=151_936)
    assert ac.dpo_batch_ceiling(**big_vocab) < ac.dpo_batch_ceiling(**SMOL) // 2


# --------------------------------------------------- no blind lowering (user's constraint)

def test_short_data_on_a_long_context_model_is_not_cut_for_a_length_it_never_reaches():
    """Llama-2-7B-shaped: 4096 context, ~1100-token rows. A length-only rule takes the 4-10B
    DPO bucket from 8 to 2; the physics allows far more, and the data never pads past 1100."""
    llama7b = dict(vocab_size=32000, hidden_size=4096, num_hidden_layers=32,
                   param_count=6.7e9, use_lora=True, dpo_max_length=4096,
                   vram_available_gb=78.0)
    cut_for_context = ac.dpo_batch_ceiling(**llama7b, longest_pair=None)
    sized_for_data = ac.dpo_batch_ceiling(**llama7b, longest_pair=1100)
    assert sized_for_data > cut_for_context * 3
    assert sized_for_data >= 8, "must not undercut the existing 4-10B DPO bucket on short data"


def test_effective_length_is_train_dpo_s_rule_then_the_data():
    assert ac.dpo_effective_length(2048, None) == 2048
    assert ac.dpo_effective_length(2048, 6717) == 2048         # data longer than the cap
    assert ac.dpo_effective_length(4096, 1100) == 1100         # data shorter than the cap
    assert ac.dpo_effective_length(131072, None) == 4096       # train_dpo's own 4096 cap
    assert ac.dpo_effective_length(None, None) == 4096         # train_dpo's fallback


# ------------------------------------------------------------------- resident term

def test_lora_frees_the_reference_copy():
    """TRL sets ref_model=None on a PeftModel; full FT deep-copies the policy. On a 135M
    model the resident term is noise; on 7B it is most of the card, and every tournament
    DPO above 1.5B is LoRA."""
    llama7b = dict(vocab_size=32000, hidden_size=4096, num_hidden_layers=32,
                   param_count=6.7e9, dpo_max_length=4096, longest_pair=1100,
                   vram_available_gb=78.0)
    full = ac.dpo_batch_ceiling(**llama7b, use_lora=False)
    lora = ac.dpo_batch_ceiling(**llama7b, use_lora=True)
    assert lora > full * 1.5, f"lora {lora} vs full {full}: the reference copy was not freed"


# ------------------------------------------------ a cap that cannot be costed stays out

@pytest.mark.parametrize("missing", ["vocab_size", "hidden_size", "num_hidden_layers",
                                     "param_count", "dpo_max_length", "vram_available_gb"])
def test_a_missing_input_yields_none_not_a_guess(missing):
    assert ac.dpo_batch_ceiling(**dict(SMOL, **{missing: None})) is None


def test_no_headroom_yields_one_not_zero():
    assert ac.dpo_batch_ceiling(**dict(SMOL, vram_available_gb=0.5)) == 1


# ------------------------------------------------------------------------ the wiring
#
# build_adaptive_run_config is a thousand-line function the repo tests structurally.
# The GPU run is the behavioural proof; these pin the three wires against regression.

@pytest.fixture(scope="module")
def source():
    with open(ADAPTIVE, encoding="utf-8") as fh:
        return fh.read()


@pytest.fixture(scope="module")
def tree(source):
    return ast.parse(source)


def _planner(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "build_adaptive_run_config":
            return node
    raise AssertionError("build_adaptive_run_config not found")


def _line_of(source, needle):
    i = source.find(needle)
    assert i >= 0, f"not in adaptive_config.py: {needle!r}"
    return source.count("\n", 0, i) + 1


def test_wire_1_the_bucket_scales_by_the_padded_length_on_dpo(source):
    """The one-directional length scaling must compare DPO's padded length, not the
    planner's max_length, against BUCKET_REFERENCE_LEN."""
    block = source[source.find("_bucket_len = max_length"):source.find("batch = min(batch, _bucket_scaled)")]
    assert "dpo_effective_length(" in block
    assert "if _bucket_len > BUCKET_REFERENCE_LEN" in block
    assert "if max_length > BUCKET_REFERENCE_LEN" not in block, "still reads the planner's length"


def test_wire_2_the_ceiling_sits_after_the_gqa_boost_and_the_kl_cap(source):
    boost = _line_of(source, "_maybe_gqa_batch_boost(batch,")
    kl_cap = _line_of(source, "_kl_batch = max(1, batch // 4)")
    ceiling = _line_of(source, "DPO measured-peak ceiling: batch")
    assert boost < ceiling and kl_cap < ceiling, (
        f"ceiling at {ceiling} must follow the boost ({boost}) and the KL cap ({kl_cap}) — "
        f"a boost applied after a ceiling is the defect")


def test_wire_2_the_ceiling_is_gated_to_dpo_on_one_gpu(tree):
    fn = _planner(tree)
    for node in ast.walk(fn):
        if isinstance(node, ast.If):
            src = ast.unparse(node.test)
            if "dpo_batch_ceiling" in ast.unparse(node):
                assert 'task_type_lc == "dpo"' in src.replace("'", '"'), src
                assert "gpu_count == 1" in src, src
                return
    raise AssertionError("no If wraps the dpo_batch_ceiling call")


def test_wire_3_the_operator_override_wins_over_the_ceiling(source):
    """INSTRUCT_BATCH_OVERRIDE is the bisect knob this ceiling was calibrated with."""
    block = source[source.find("_dpo_cap = dpo_batch_ceiling("):source.find("# Init LR — heuristic")]
    assert "elif _batch_overridden:" in block
    assert "not applied: INSTRUCT_BATCH_OVERRIDE" in block


def test_wire_3_the_override_flag_is_initialised_before_it_is_set(source):
    init = _line_of(source, "_batch_overridden = False")
    setl = _line_of(source, "_batch_overridden = True")
    use = _line_of(source, "elif _batch_overridden:")
    assert init < setl < use


def test_non_dpo_paths_never_reach_the_ceiling(tree):
    """instruct, KL, chat and GRPO must plan the same batch as before: the ceiling's only
    entry is the If above, and dpo_effective_length is consulted only under _is_dpo."""
    fn = _planner(tree)
    calls = [n for n in ast.walk(fn) if isinstance(n, ast.Call)
             and getattr(n.func, "id", "") in ("dpo_batch_ceiling", "dpo_effective_length")]
    assert len(calls) == 3, [ast.unparse(c) for c in calls]   # bucket wire + ceiling (2 calls)
    src = ast.unparse(fn)
    for c in calls:
        i = src.find(ast.unparse(c))
        before = src[max(0, i - 900):i]
        assert ("_is_dpo" in before) or ('task_type_lc == "dpo"' in before.replace("'", '"')), (
            f"call not under a DPO gate: {ast.unparse(c)[:60]}")
