"""Per-example eval losses, on the validator's convention.

Why
---
The validator is moving knockout and boss rounds off mean loss and onto an
example-by-example comparison: both models are scored on the identical held-out
set, gaps under 0.01 nats count for neither side, and the challenger needs a
majority of *decided* examples as well as a mean-gap floor
(gradients-ai/G.O.D PR #1345).

We are not changing what we select on yet — group rounds are still mean-ranked,
the PR is unmerged, and the selection stack it would touch has never run on a
GPU. What we can do at no risk is RECORD the vector. Every eval writes its
per-example losses to telemetry, so once the rule lands we can ask, against real
runs, whether win-rate selection would ever have picked a different checkpoint
than mean selection did. That measurement is what should decide adoption — not
the existence of the PR.

There is a second reason that holds regardless. HF's `eval_loss` is pooled over
tokens; the validator token-averages *within* each example and then compares
examples. Long examples therefore carry different weight in the two quantities.
Per-example-then-mean is the correct primitive under the old rule as well as the
new one, so recording it costs nothing and fixes a latent mismatch.

The formula, transcribed from validator/evaluation/evaluators/instruct_text.py
in PR #1345:

    shift_logits = logits[:, :-1, :].float()
    shift_labels = labels[:, 1:]
    per_token    = cross_entropy(..., ignore_index=-100, reduction="none")
    supervised   = shift_labels != -100
    per_example  = (per_token * supervised).sum(1) / supervised.sum(1)

Two details that are easy to get wrong and both matter:

* This DOES shift logits against labels. Note that the KL term in
  kl_objective.py deliberately does NOT — the validator computes the two
  quantities on different conventions, and each must match its own. Do not
  "make them consistent".
* The denominator is the supervised-token count AFTER the shift. The validator's
  own comment records that the unshifted count is wrong by n/(n-1) on any
  example whose first token is supervised, which was enough to make their
  mean-vs-eval_loss consistency check misfire permanently.

An example with no supervised tokens yields NaN rather than 0.0, so the pairing
drops it from both sides instead of scoring it as a perfect prediction.
"""

import hashlib
import os

import torch
import torch.nn.functional as F

EMIT_ENV = "EMIT_PER_EXAMPLE_LOSSES"


def enabled() -> bool:
    """Default on. Set EMIT_PER_EXAMPLE_LOSSES=0 to skip the extra forward pass."""
    return os.getenv(EMIT_ENV, "1") == "1"


def per_example_losses_from_logits(logits: torch.Tensor, labels: torch.Tensor) -> list:
    """Token-averaged cross-entropy for each example in a batch.

    Returns a python list of floats, NaN where an example has no supervised token.
    """
    shift_logits = logits[:, :-1, :].float()
    shift_labels = labels[:, 1:]

    per_token = F.cross_entropy(
        shift_logits.transpose(1, 2),
        shift_labels,
        ignore_index=-100,
        reduction="none",
    )
    supervised = (shift_labels != -100).to(per_token.dtype)
    summed = (per_token * supervised).sum(dim=1)
    token_counts = supervised.sum(dim=1)

    per_example = torch.where(
        token_counts > 0,
        summed / token_counts,
        torch.full_like(summed, float("nan")),
    )
    return per_example.tolist()


def collect_per_example_losses(model, dataloader, device=None, max_batches: int = None) -> list:
    """Run the eval set through the model and return one loss per example, in order.

    Order matters: the comparison is positional, so index i must be the same
    example in every vector we ever compare. The fingerprint below is what lets
    us verify that after the fact.

    Costs one forward pass over the eval set. Caller decides when that is worth
    paying; this function does not decide anything about training.
    """
    was_training = model.training
    model.eval()
    losses: list = []
    try:
        with torch.no_grad():
            for i, batch in enumerate(dataloader):
                if max_batches is not None and i >= max_batches:
                    break
                labels = batch.get("labels")
                if labels is None:
                    continue
                inputs = {
                    k: (v.to(device) if device is not None and hasattr(v, "to") else v)
                    for k, v in batch.items()
                    if k in ("input_ids", "attention_mask", "position_ids")
                }
                if device is not None and hasattr(labels, "to"):
                    labels = labels.to(device)
                logits = model(**inputs).logits
                losses.extend(per_example_losses_from_logits(logits, labels))
    finally:
        if was_training:
            model.train()
    return losses


def summarise(losses: list) -> dict:
    """Compact summary for a log line — the full vector goes to telemetry."""
    finite = [x for x in losses if x == x and x not in (float("inf"), float("-inf"))]
    if not finite:
        return {"n": len(losses), "n_finite": 0}
    finite_sorted = sorted(finite)
    n = len(finite_sorted)

    def q(p):
        return finite_sorted[min(n - 1, int(n * p))]

    return {
        "n": len(losses),
        "n_finite": n,
        "mean": sum(finite) / n,
        "p10": q(0.10),
        "p50": q(0.50),
        "p90": q(0.90),
        "max": finite_sorted[-1],
    }


def vector_fingerprint(losses: list) -> str:
    """Short digest of the vector's length and ordering.

    Two vectors are only comparable if they cover the same examples in the same
    order. This does not prove that, but a mismatch is a cheap early warning that
    something reordered or filtered the eval set between runs.
    """
    h = hashlib.sha256()
    h.update(str(len(losses)).encode())
    for x in losses:
        h.update(b"nan" if x != x else f"{x:.6f}".encode())
        h.update(b",")
    return h.hexdigest()[:16]


def compare_paired(
    baseline: list,
    candidate: list,
    deadzone_nats: float = 0.01,
) -> dict:
    """Win-rate style comparison of two loss vectors. ANALYSIS ONLY.

    Mirrors the shape of the validator's paired comparison so we can ask, offline
    and after the fact, whether this would have picked a different checkpoint
    than the mean did. Deliberately NOT wired into any selection path, and
    deliberately without the bootstrap: the significance bar is the validator's
    problem, and a miner cannot reliably know which round it is in.

    Positive gap = candidate assigned more probability than baseline.
    """
    n = min(len(baseline), len(candidate))
    pairs = [
        (b, c)
        for b, c in zip(baseline[:n], candidate[:n])
        if b == b and c == c and abs(b) != float("inf") and abs(c) != float("inf")
    ]
    if not pairs:
        return {"n_examples": 0, "n_decided": 0, "win_rate": 0.0, "mean_gap": 0.0}

    gaps = [b - c for b, c in pairs]
    cand_wins = sum(1 for g in gaps if g > deadzone_nats)
    base_wins = sum(1 for g in gaps if g < -deadzone_nats)
    decided = cand_wins + base_wins

    return {
        "n_examples": len(pairs),
        "n_decided": decided,
        "candidate_wins": cand_wins,
        "baseline_wins": base_wins,
        "win_rate": (cand_wins / decided) if decided else 0.0,
        "mean_gap": sum(gaps) / len(gaps),
    }
