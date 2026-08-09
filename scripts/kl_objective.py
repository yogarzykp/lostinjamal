"""KL term for instruct tasks the validator flags with USE_KL.

What the validator does
-----------------------
When it creates an instruct task there is a 20% chance it marks the task KL-
weighted and draws a coefficient uniform(0.1, 1.5). It tells our container via
env `USE_KL=1` and `KL_COEF=<float>`, and then ranks us on

    weighted_loss = eval_loss + kl_coef * KL(finetuned || base)

instead of plain eval loss. Both boss-round instruct tasks are KL-eligible, so
this is not a rare corner: roughly a third of boss campaigns contain at least one.

Ignoring the flag means optimising a different objective than the one being
scored, and the failure is silent — training looks healthy and the rank is just
worse. This module is the objective, kept deliberately small and pure so
tests/test_kl_validator_parity.py can pin it against a transcription of the
validator's own code.

Formula, from validator/evaluation/evaluators/instruct_text.py:181-203
---------------------------------------------------------------------
Per position, KL of the finetuned distribution against the base one, summed over
vocab, averaged over positions whose label is not -100:

    kl_per_token = (p_ft * (log p_ft - log p_base)).sum(-1)
    mask         = labels != -100
    kl           = (kl_per_token * mask).sum() / mask.sum()

Two properties of that code are load-bearing and easy to "fix" by accident:

* NO SHIFT. `logits[:, i]` is masked by `labels[:, i]`, even though in a causal
  LM position i predicts token i+1. The textbook alignment would drop the last
  logit and the first label. We reproduce the validator's convention because it
  is the quantity we are ranked on, not the one a paper would define.
* Padding needs no special handling: the collate pads labels with -100
  (instruct_text.py:150), so padded positions fall out of the mask by themselves.

We compute in float32 regardless of model dtype. That is a precision choice, not
a formula change: the sum over a large vocab accumulates error quickly in bf16,
and during training this value carries gradient. The validator's own number is a
lower-precision estimate of the same quantity.
"""

import os

import torch
import torch.nn.functional as F

USE_KL_ENV = "USE_KL"
KL_COEF_ENV = "KL_COEF"

# The validator draws kl_coef from uniform(0.1, 1.5)
# (INSTRUCT_KL_COEFFICIENT_MIN / _MAX). If it tells us KL is active but the
# coefficient is unusable, the midpoint is the least-wrong assumption available.
KL_COEF_MIN = 0.1
KL_COEF_MAX = 1.5
KL_COEF_FALLBACK = 0.8


def kl_per_token(base_logits: torch.Tensor, finetuned_logits: torch.Tensor) -> torch.Tensor:
    """KL(finetuned || base) at every position, summed over vocab.

    Returns a (batch, seq) tensor that carries gradient through finetuned_logits.
    """
    base_log_probs = F.log_softmax(base_logits.float(), dim=-1)
    ft_log_probs = F.log_softmax(finetuned_logits.float(), dim=-1)
    ft_probs = ft_log_probs.exp()
    return (ft_probs * (ft_log_probs - base_log_probs)).sum(dim=-1)


def instruct_kl_tensor(
    base_logits: torch.Tensor,
    finetuned_logits: torch.Tensor,
    labels: torch.Tensor,
) -> torch.Tensor:
    """Mean per-token KL over trainable positions, as a differentiable scalar.

    No shift between logits and labels — see the module docstring.
    Returns a zero tensor when nothing is trainable, matching the validator's
    early return rather than dividing by zero.
    """
    kl = kl_per_token(base_logits, finetuned_logits)
    mask = (labels != -100).to(kl.dtype)
    total = mask.sum()
    if total.item() == 0:
        return torch.zeros((), dtype=kl.dtype, device=kl.device)
    return (kl * mask).sum() / total


def instruct_kl_divergence(
    base_logits: torch.Tensor,
    finetuned_logits: torch.Tensor,
    labels: torch.Tensor,
) -> float:
    """Scalar form of instruct_kl_tensor, for metrics and for parity assertions."""
    with torch.no_grad():
        return float(instruct_kl_tensor(base_logits, finetuned_logits, labels).item())


def weighted_loss(eval_loss: float, kl_coef: float, kl_divergence: float) -> float:
    """The ranked metric on a KL-flagged task (instruct_text.py:263)."""
    return eval_loss + kl_coef * kl_divergence


def read_kl_config(env=None):
    """Resolve (use_kl, kl_coef, reason) from the container environment.

    The important case is the awkward one. If the validator says `USE_KL=1` but
    the coefficient is missing or unparsable, we must NOT quietly fall back to
    plain cross-entropy: that is precisely the failure this whole path exists to
    remove — training blind against a metric we know is weighted. We assume the
    midpoint of the validator's range and log it loudly instead.

    A coefficient outside the validator's published range is clamped rather than
    rejected: it still tells us the direction and rough magnitude, and refusing
    it would put us back on the blind path.
    """
    env = os.environ if env is None else env

    if env.get(USE_KL_ENV) != "1":
        return False, None, "USE_KL not set"

    raw = env.get(KL_COEF_ENV)
    if raw is None or str(raw).strip() == "":
        return True, KL_COEF_FALLBACK, (
            f"USE_KL=1 but {KL_COEF_ENV} absent — assuming midpoint {KL_COEF_FALLBACK} "
            f"rather than training unweighted"
        )

    try:
        coef = float(str(raw).strip())
    except (TypeError, ValueError):
        return True, KL_COEF_FALLBACK, (
            f"USE_KL=1 but {KL_COEF_ENV}={raw!r} unparsable — assuming midpoint "
            f"{KL_COEF_FALLBACK} rather than training unweighted"
        )

    if coef != coef or coef in (float("inf"), float("-inf")):
        return True, KL_COEF_FALLBACK, (
            f"USE_KL=1 but {KL_COEF_ENV}={raw!r} not finite — assuming midpoint {KL_COEF_FALLBACK}"
        )

    if coef < KL_COEF_MIN or coef > KL_COEF_MAX:
        clamped = min(KL_COEF_MAX, max(KL_COEF_MIN, coef))
        return True, clamped, (
            f"{KL_COEF_ENV}={coef} outside validator range "
            f"[{KL_COEF_MIN}, {KL_COEF_MAX}] — clamped to {clamped}"
        )

    return True, coef, f"{KL_COEF_ENV}={coef}"
