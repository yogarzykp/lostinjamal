"""Parity tests pinning our KL computation to the validator's.

Why this file exists, and why it was written BEFORE the trainer code
--------------------------------------------------------------------
On roughly one instruct task in five the validator ranks us on

    weighted_loss = eval_loss + kl_coef * KL(finetuned || base)

instead of plain eval loss. `kl_coef` is drawn uniform(0.1, 1.5) per task and
handed to our container as env `KL_COEF`, with `USE_KL=1`. Both boss-round
instruct tasks are KL-eligible, so this is not a side case.

If our KL differs from the validator's — even by a convention as small as
whether logits are shifted against labels — then we optimise and select
checkpoints against a metric that is not the one we are scored on, and the
error is invisible: training looks healthy, the score is just worse than it
should be. That makes exact parity the highest-consequence correctness item in
this work, and the one thing that can be verified completely on CPU with no GPU
and no dataset. Hence: reference first, implementation second, this file as the
spec.

THE REFERENCE
-------------
`validator_reference_kl` below is a line-for-line reimplementation of
`_calculate_instruct_kl_divergence` in the validator source:

    gradients-ai/G.O.D @ d0a2ddd
    validator/evaluation/evaluators/instruct_text.py:157-203

and `validator_reference_weighted_loss` mirrors the combination at
instruct_text.py:255-269. It exists only in tests. Production code must be
asserted equal to it, never import it.

THE NON-SHIFT QUIRK
-------------------
For a causal LM, `logits[:, i]` predicts token `i+1`, so the textbook alignment
of a per-token quantity against `labels` drops the last logit and the first
label. The validator does NOT do this: it masks `kl_per_token[:, i]` with
`labels[:, i] != -100` at the same index. That is arguably wrong as information
theory, and it is completely irrelevant — it is the quantity we are scored on,
so it is the quantity we must reproduce. `test_quirk_*` below pins that the
shifted variant gives a DIFFERENT number, so nobody can "fix" it later without
a failing test explaining why it is deliberate.
"""

import math

import pytest
import torch
import torch.nn.functional as F


# --------------------------------------------------------------------------
# Validator reference — do not import from production code.
# --------------------------------------------------------------------------

def validator_reference_kl(base_logits, finetuned_logits, labels):
    """Mean per-token KL(finetuned || base) over label != -100 positions.

    Transcribed from validator/evaluation/evaluators/instruct_text.py:181-203.
    Note there is no shift between logits and labels — see module docstring.
    """
    base_log_probs = F.log_softmax(base_logits, dim=-1)
    finetuned_log_probs = F.log_softmax(finetuned_logits, dim=-1)
    finetuned_probs = finetuned_log_probs.exp()

    kl_per_token = (finetuned_probs * (finetuned_log_probs - base_log_probs)).sum(dim=-1)
    mask = (labels != -100).float()

    total_kl = (kl_per_token * mask).sum().item()
    total_tokens = int(mask.sum().item())

    if total_tokens == 0:
        return 0.0
    return total_kl / total_tokens


def validator_reference_weighted_loss(eval_loss, kl_coef, kl_divergence):
    """instruct_text.py:263 — the ranked metric when a task is KL-flagged."""
    return eval_loss + kl_coef * kl_divergence


def _shifted_variant_kl(base_logits, finetuned_logits, labels):
    """The 'textbook' alignment the validator does NOT use. Reference for contrast only."""
    base_log_probs = F.log_softmax(base_logits[:, :-1], dim=-1)
    finetuned_log_probs = F.log_softmax(finetuned_logits[:, :-1], dim=-1)
    finetuned_probs = finetuned_log_probs.exp()

    kl_per_token = (finetuned_probs * (finetuned_log_probs - base_log_probs)).sum(dim=-1)
    mask = (labels[:, 1:] != -100).float()

    total = int(mask.sum().item())
    if total == 0:
        return 0.0
    return (kl_per_token * mask).sum().item() / total


# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

VOCAB = 37
SEQ = 11
BATCH = 3


def _logits(seed, batch=BATCH, seq=SEQ, vocab=VOCAB):
    g = torch.Generator().manual_seed(seed)
    return torch.randn(batch, seq, vocab, generator=g)


def _labels(seed, batch=BATCH, seq=SEQ, vocab=VOCAB, mask_frac=0.4):
    """Labels with a realistic mix: -100 for prompt/padding, real ids elsewhere."""
    g = torch.Generator().manual_seed(seed)
    lab = torch.randint(0, vocab, (batch, seq), generator=g)
    drop = torch.rand(batch, seq, generator=g) < mask_frac
    lab[drop] = -100
    return lab


# --------------------------------------------------------------------------
# Properties of the reference itself
# --------------------------------------------------------------------------

def test_identical_models_give_zero_kl():
    """KL(p || p) == 0. Guards against a sign flip or a swapped argument order."""
    logits = _logits(1)
    kl = validator_reference_kl(logits, logits.clone(), _labels(2))
    assert kl == pytest.approx(0.0, abs=1e-6)


def test_kl_is_non_negative():
    for seed in range(8):
        kl = validator_reference_kl(_logits(seed), _logits(seed + 100), _labels(seed + 200))
        assert kl >= -1e-6, f"seed {seed} produced negative KL {kl}"


def test_direction_is_finetuned_against_base():
    """KL is asymmetric; swapping the arguments must change the value.

    If this ever passes with equality, someone has implemented a symmetric
    divergence and the metric no longer matches the validator's.
    """
    base, ft, lab = _logits(11), _logits(12), _labels(13)
    forward = validator_reference_kl(base, ft, lab)
    reverse = validator_reference_kl(ft, base, lab)
    assert forward != pytest.approx(reverse, rel=1e-3)


def test_only_unmasked_positions_contribute():
    """Changing logits under a -100 label must not move the KL."""
    base, ft = _logits(21), _logits(22)
    lab = _labels(23)
    before = validator_reference_kl(base, ft, lab)

    masked = lab == -100
    assert masked.any(), "fixture must contain masked positions"
    perturbed = ft.clone()
    perturbed[masked] += 25.0  # violent change, entirely under the mask

    after = validator_reference_kl(base, perturbed, lab)
    assert after == pytest.approx(before, rel=1e-6)


def test_padding_is_excluded_because_padded_labels_are_minus_100():
    """The collate pads labels with -100 (instruct_text.py:150), so padding drops out.

    Built explicitly: a short row padded out to the batch width must score the
    same as that row evaluated alone.
    """
    base_full, ft_full = _logits(31, batch=1), _logits(32, batch=1)
    lab = torch.full((1, SEQ), -100)
    lab[0, :4] = torch.tensor([5, 6, 7, 8])  # only the first 4 positions are real

    kl_padded = validator_reference_kl(base_full, ft_full, lab)
    kl_trimmed = validator_reference_kl(
        base_full[:, :4], ft_full[:, :4], lab[:, :4]
    )
    assert kl_padded == pytest.approx(kl_trimmed, rel=1e-6)


def test_no_trainable_tokens_returns_zero():
    """instruct_text.py:199 — total_tokens == 0 returns 0.0 rather than dividing."""
    lab = torch.full((BATCH, SEQ), -100)
    assert validator_reference_kl(_logits(41), _logits(42), lab) == 0.0


def test_result_is_invariant_to_batching():
    """The validator accumulates with GRPO_KL_BATCH_SIZE = 1 and divides at the end.

    Our trainer will batch differently, so the metric must not depend on batch
    composition — it is a sum over masked positions over a count of them.
    """
    base, ft, lab = _logits(51), _logits(52), _labels(53)
    whole = validator_reference_kl(base, ft, lab)

    total_kl, total_tok = 0.0, 0
    for i in range(base.shape[0]):
        b, f, l = base[i : i + 1], ft[i : i + 1], lab[i : i + 1]
        n = int((l != -100).sum().item())
        if n:
            total_kl += validator_reference_kl(b, f, l) * n
            total_tok += n
    streamed = total_kl / total_tok

    assert whole == pytest.approx(streamed, rel=1e-6)


# --------------------------------------------------------------------------
# The quirk — pinned deliberately
# --------------------------------------------------------------------------

def test_quirk_validator_does_not_shift_logits_against_labels():
    """The shifted 'correct' alignment gives a different number. That is the point.

    We are scored on the unshifted quantity. If a future change makes these two
    agree, the implementation has silently switched conventions and every
    KL-flagged task is being optimised against the wrong target.
    """
    base, ft, lab = _logits(61), _logits(62), _labels(63)
    unshifted = validator_reference_kl(base, ft, lab)
    shifted = _shifted_variant_kl(base, ft, lab)
    assert unshifted != pytest.approx(shifted, rel=1e-3), (
        "unshifted and shifted KL agreed — fixture is degenerate, not a passing condition"
    )


def test_quirk_last_position_is_included():
    """Under the validator's convention the final logit participates.

    A shifted implementation drops it. Perturbing only the last position must
    therefore move our number.
    """
    base, ft = _logits(71), _logits(72)
    lab = torch.randint(0, VOCAB, (BATCH, SEQ))  # nothing masked
    before = validator_reference_kl(base, ft, lab)

    # Must be NON-uniform across vocab: log_softmax is shift-invariant, so adding
    # the same constant to every logit at a position leaves the distribution —
    # and therefore the KL — untouched.
    g = torch.Generator().manual_seed(73)
    perturbed = ft.clone()
    perturbed[:, -1, :] += torch.randn(BATCH, VOCAB, generator=g) * 5.0
    after = validator_reference_kl(base, perturbed, lab)

    assert after != pytest.approx(before, rel=1e-6)


# --------------------------------------------------------------------------
# Weighted loss
# --------------------------------------------------------------------------

def test_weighted_loss_is_additive_with_coefficient():
    assert validator_reference_weighted_loss(1.25, 0.8, 0.5) == pytest.approx(1.65)


@pytest.mark.parametrize("kl_coef", [0.1, 0.5, 1.0, 1.5])
def test_weighted_loss_across_the_validators_coefficient_range(kl_coef):
    """kl_coef is drawn uniform(0.1, 1.5) — INSTRUCT_KL_COEFFICIENT_MIN/MAX."""
    eval_loss, kl = 1.2, 0.4
    got = validator_reference_weighted_loss(eval_loss, kl_coef, kl)
    assert got == pytest.approx(eval_loss + kl_coef * kl)
    assert got >= eval_loss, "KL can only add to the ranked loss"


def test_kl_penalty_can_dominate_the_loss_difference_between_miners():
    """Sizing check for why this matters at all.

    Two miners a hair apart on raw eval loss can be ordered entirely by the KL
    term once kl_coef is in the upper half of the validator's range.
    """
    a_loss, a_kl = 1.2000, 0.30   # slightly better raw loss, drifted further
    b_loss, b_kl = 1.2050, 0.05   # slightly worse raw loss, stayed close
    kl_coef = 1.2

    assert a_loss < b_loss  # A wins on raw loss
    a = validator_reference_weighted_loss(a_loss, kl_coef, a_kl)
    b = validator_reference_weighted_loss(b_loss, kl_coef, b_kl)
    assert b < a, "B should win once KL is weighted — this is the ranking we must optimise"


# --------------------------------------------------------------------------
# Production parity — the gate this file exists to be
# --------------------------------------------------------------------------

def _load_production_kl():
    """Import our implementation if it exists yet. Returns None before it does."""
    import os
    import sys

    scripts = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    try:
        from kl_objective import instruct_kl_divergence  # noqa: WPS433
        return instruct_kl_divergence
    except Exception:
        return None


production_kl = _load_production_kl()
needs_production = pytest.mark.skipif(
    production_kl is None,
    reason="scripts/kl_objective.py not implemented yet — this file is the spec it must satisfy",
)


@needs_production
@pytest.mark.parametrize("seed", [0, 1, 2, 3, 4, 5, 6, 7])
def test_production_matches_validator_on_random_logits(seed):
    base, ft, lab = _logits(seed), _logits(seed + 500), _labels(seed + 900)
    expected = validator_reference_kl(base, ft, lab)
    got = production_kl(base, ft, lab)
    assert got == pytest.approx(expected, rel=1e-6, abs=1e-9)


@needs_production
def test_production_matches_validator_on_fully_masked_batch():
    lab = torch.full((BATCH, SEQ), -100)
    assert production_kl(_logits(81), _logits(82), lab) == pytest.approx(
        validator_reference_kl(_logits(81), _logits(82), lab)
    )


@needs_production
def test_production_reproduces_the_non_shift_quirk():
    base, ft, lab = _logits(91), _logits(92), _labels(93)
    got = production_kl(base, ft, lab)
    assert got == pytest.approx(validator_reference_kl(base, ft, lab), rel=1e-6)
    assert got != pytest.approx(_shifted_variant_kl(base, ft, lab), rel=1e-3), (
        "production used the shifted alignment — it must match the validator, not the textbook"
    )


@needs_production
def test_production_handles_half_precision_without_diverging():
    """Training runs in bf16. The metric must survive the dtype it will see."""
    base, ft, lab = _logits(101), _logits(102), _labels(103)
    ref = validator_reference_kl(base, ft, lab)
    got = production_kl(base.to(torch.bfloat16), ft.to(torch.bfloat16), lab)
    assert not math.isnan(got)
    assert got == pytest.approx(ref, rel=0.05), "bf16 KL drifted more than 5% from fp32"
