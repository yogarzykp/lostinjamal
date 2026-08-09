"""Per-example eval losses must match the validator's convention exactly.

Same discipline as the KL parity file: a transcription of the validator's own
code sits here as the reference, and production is asserted equal to it. This
matters because the two quantities the validator computes use DIFFERENT
conventions — the per-example cross-entropy shifts logits against labels, the KL
term does not — and quietly making them consistent would break one of them.
"""

import math
import os
import sys

import pytest
import torch
import torch.nn.functional as F

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from per_example_eval import (  # noqa: E402
    compare_paired,
    per_example_losses_from_logits,
    summarise,
    vector_fingerprint,
)


# --------------------------------------------------------------------------
# Validator reference — transcribed, test-only
# --------------------------------------------------------------------------

def validator_reference_per_example(logits, labels):
    """From validator/evaluation/evaluators/instruct_text.py in PR #1345."""
    shift_logits = logits[:, :-1, :].float()
    shift_labels = labels[:, 1:]
    per_token = F.cross_entropy(
        shift_logits.transpose(1, 2), shift_labels, ignore_index=-100, reduction="none"
    )
    supervised = (shift_labels != -100).float()
    summed = (per_token * supervised).sum(dim=1)
    token_counts = supervised.sum(dim=1)
    per_example = torch.where(
        token_counts > 0, summed / token_counts, torch.full_like(summed, float("nan"))
    )
    return per_example.tolist()


def _unshifted_variant(logits, labels):
    """The convention the KL term uses. Correct there, WRONG here."""
    per_token = F.cross_entropy(
        logits.float().transpose(1, 2), labels, ignore_index=-100, reduction="none"
    )
    supervised = (labels != -100).float()
    counts = supervised.sum(dim=1)
    summed = (per_token * supervised).sum(dim=1)
    return torch.where(counts > 0, summed / counts, torch.full_like(summed, float("nan"))).tolist()


def _unshifted_denominator_variant(logits, labels):
    """Shifted numerator, UNSHIFTED denominator — the specific bug the validator
    documents as wrong by n/(n-1) when the first token is supervised."""
    shift_logits = logits[:, :-1, :].float()
    shift_labels = labels[:, 1:]
    per_token = F.cross_entropy(
        shift_logits.transpose(1, 2), shift_labels, ignore_index=-100, reduction="none"
    )
    supervised = (shift_labels != -100).float()
    summed = (per_token * supervised).sum(dim=1)
    counts = (labels != -100).float().sum(dim=1)  # unshifted — the bug
    return torch.where(counts > 0, summed / counts, torch.full_like(summed, float("nan"))).tolist()


VOCAB, SEQ, BATCH = 23, 9, 4


def _logits(seed, batch=BATCH, seq=SEQ, vocab=VOCAB):
    g = torch.Generator().manual_seed(seed)
    return torch.randn(batch, seq, vocab, generator=g)


def _labels(seed, batch=BATCH, seq=SEQ, vocab=VOCAB, mask_frac=0.4):
    g = torch.Generator().manual_seed(seed)
    lab = torch.randint(0, vocab, (batch, seq), generator=g)
    lab[torch.rand(batch, seq, generator=g) < mask_frac] = -100
    return lab


# --------------------------------------------------------------------------
# Parity
# --------------------------------------------------------------------------

@pytest.mark.parametrize("seed", range(6))
def test_matches_validator_reference(seed):
    logits, labels = _logits(seed), _labels(seed + 50)
    got = per_example_losses_from_logits(logits, labels)
    want = validator_reference_per_example(logits, labels)
    assert len(got) == len(want)
    for g, w in zip(got, want):
        if math.isnan(w):
            assert math.isnan(g)
        else:
            assert g == pytest.approx(w, rel=1e-6)


def test_shift_is_applied_unlike_the_kl_term():
    """The KL term deliberately does not shift. This one does. They must differ.

    If these ever agree, someone has unified the two conventions and one of them
    is now wrong against the validator.
    """
    logits, labels = _logits(11), _labels(12)
    shifted = per_example_losses_from_logits(logits, labels)
    unshifted = _unshifted_variant(logits, labels)
    finite = [(a, b) for a, b in zip(shifted, unshifted) if not math.isnan(a) and not math.isnan(b)]
    assert finite, "fixture produced no comparable examples"
    assert any(abs(a - b) > 1e-4 for a, b in finite)


def test_denominator_is_the_shifted_supervised_count():
    """The validator records that an unshifted denominator is wrong by n/(n-1)
    when the first token is supervised. Build exactly that case."""
    logits = _logits(21, batch=1)
    labels = torch.full((1, SEQ), -100)
    labels[0, 0] = 5  # first token supervised — the case that exposes the bug
    labels[0, 3] = 7
    labels[0, 4] = 9

    ours = per_example_losses_from_logits(logits, labels)[0]
    buggy = _unshifted_denominator_variant(logits, labels)[0]

    assert ours == pytest.approx(validator_reference_per_example(logits, labels)[0], rel=1e-9)
    assert not math.isnan(ours)
    assert ours != pytest.approx(buggy, rel=1e-6), "unshifted denominator must give a different answer"

    # And the ratio is exactly the documented n/(n-1).
    shifted_n = int((labels[:, 1:] != -100).sum())
    unshifted_n = int((labels != -100).sum())
    assert unshifted_n == shifted_n + 1
    assert buggy == pytest.approx(ours * shifted_n / unshifted_n, rel=1e-6)


def test_example_with_no_supervised_tokens_is_nan_not_zero():
    """NaN drops the example from the pairing. Zero would score it as perfect."""
    logits = _logits(31, batch=2)
    labels = torch.full((2, SEQ), -100)
    labels[1, 4] = 3  # second example has one supervised token
    out = per_example_losses_from_logits(logits, labels)
    assert math.isnan(out[0])
    assert not math.isnan(out[1])


def test_supervision_only_in_first_position_is_nan_after_shift():
    """Label at index 0 alone: after the shift there is nothing supervised left."""
    logits = _logits(41, batch=1)
    labels = torch.full((1, SEQ), -100)
    labels[0, 0] = 11
    assert math.isnan(per_example_losses_from_logits(logits, labels)[0])


def test_losses_are_non_negative_and_finite_where_supervised():
    for seed in range(5):
        out = per_example_losses_from_logits(_logits(seed), _labels(seed + 70))
        for x in out:
            if not math.isnan(x):
                assert x >= 0 and math.isfinite(x)


def test_perfect_prediction_gives_near_zero_loss():
    labels = torch.randint(0, VOCAB, (1, SEQ))
    logits = torch.zeros(1, SEQ, VOCAB)
    # position t predicts label t+1
    for t in range(SEQ - 1):
        logits[0, t, labels[0, t + 1]] = 50.0
    assert per_example_losses_from_logits(logits, labels)[0] == pytest.approx(0.0, abs=1e-4)


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def test_fingerprint_is_stable_and_order_sensitive():
    v = [1.0, 2.0, 3.0]
    assert vector_fingerprint(v) == vector_fingerprint([1.0, 2.0, 3.0])
    assert vector_fingerprint(v) != vector_fingerprint([3.0, 2.0, 1.0])
    assert vector_fingerprint(v) != vector_fingerprint([1.0, 2.0])


def test_fingerprint_handles_nan_without_raising():
    assert isinstance(vector_fingerprint([1.0, float("nan"), 2.0]), str)


def test_summarise_ignores_non_finite():
    s = summarise([1.0, 2.0, float("nan"), 3.0, float("inf")])
    assert s["n"] == 5 and s["n_finite"] == 3
    assert s["mean"] == pytest.approx(2.0)


def test_summarise_on_all_nan():
    s = summarise([float("nan"), float("nan")])
    assert s["n_finite"] == 0 and "mean" not in s


# --------------------------------------------------------------------------
# The analysis comparator (not wired to selection)
# --------------------------------------------------------------------------

def test_deadzone_excludes_hairline_differences():
    """Fable's correction: hairline losses cost nothing — they are undecided,
    not counted against the candidate."""
    baseline = [1.000] * 100
    candidate = [0.995] * 100  # better by 0.005, under the 0.01 dead zone
    r = compare_paired(baseline, candidate)
    assert r["n_decided"] == 0
    assert r["mean_gap"] == pytest.approx(0.005)


def test_uniform_small_improvement_is_invisible_in_win_rate_but_shows_in_mean():
    """The profile that draws at the boss round but wins a knockout on tie-break."""
    baseline = [1.0] * 200
    candidate = [1.0 - 0.008] * 200
    r = compare_paired(baseline, candidate)
    assert r["n_decided"] == 0
    assert r["win_rate"] == 0.0
    assert r["mean_gap"] > 0


def test_broad_consistent_improvement_wins_on_rate():
    baseline = [1.0] * 100
    candidate = [1.0 - 0.05] * 100
    r = compare_paired(baseline, candidate)
    assert r["n_decided"] == 100
    assert r["win_rate"] == pytest.approx(1.0)


def test_spiky_improvement_can_lose_the_rate_while_winning_the_mean():
    """Wins huge on a few, loses moderately on many — the profile the new rule punishes."""
    baseline = [1.0] * 100
    candidate = [1.0] * 100
    for i in range(10):
        candidate[i] = 0.0          # ten enormous wins
    for i in range(10, 100):
        candidate[i] = 1.05         # ninety moderate losses
    r = compare_paired(baseline, candidate)
    assert r["mean_gap"] > 0, "mean still favours the candidate"
    assert r["win_rate"] < 0.5, "but it loses the example count"


def test_nan_examples_are_dropped_from_both_sides():
    baseline = [1.0, float("nan"), 1.0]
    candidate = [0.5, 0.5, float("nan")]
    r = compare_paired(baseline, candidate)
    assert r["n_examples"] == 1


def test_empty_and_mismatched_lengths_do_not_raise():
    assert compare_paired([], [])["n_examples"] == 0
    assert compare_paired([1.0, 2.0, 3.0], [0.5])["n_examples"] == 1
