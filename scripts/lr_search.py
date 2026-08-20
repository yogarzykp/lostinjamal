"""Learning-rate candidates from an LR range test, fenced by held-out confirmation.

Replaces the geometric ladder for candidate GENERATION. The ladder built candidates
with `lr_utils.extend_learning_rates(lr, n, log_range=0.18)` — a span of x0.66..x1.51
around whatever the family table suggested. That is fine tuning around a prior assumed
close, and it is exactly what fails when the prior is not close.

Measured on 2026-08-20 with `ops/smoke/lr_recovery.sh`, prior poisoned 10x high:

    candidates     8.070e-04  5.332e-04  1.221e-03
    held-out probe 3.4228     3.1281     7.7938
    selected       5.332e-04       true LR 8.07e-05  ->  still 6.6x too high

Two things in that result shaped this module. The selection was CORRECT — the probe
scored the 1.221e-03 candidate at 7.79 and rejected it, so held-out probe scoring
reliably kills a bad learning rate. And the search chose its own LOWEST candidate,
the signature of a range that wants to extend and cannot. So the fix is reach, not
scoring: `lr_finder.find_lr_lrrt` sweeps 1e-7..1e-2, five decades, and the true LR in
that experiment sits inside it.

WHAT FENCES A WILD SUGGESTION. Not a clip around the prior — that re-anchors the
answer to the thing we just decided we cannot trust, and at the ratios that matter it
re-poisons it (a x5 clip on a 10x-wrong prior still lands 2x high). The fence is the
confirmation probe: the LRRT suggestion runs against the incumbent table LR and the
held-out loss picks the winner. A bad suggestion loses, as 1.221e-03 did.

The bounds below are therefore a LAST RESORT, not the mechanism. They exist because
`find_lr_lrrt` has two branches that return something arbitrary rather than measured —
it returns `lr_min * 10` when it gathers fewer than five points, and a mid-range LR
when it sees no descent at all — and neither deserves to reach a probe.
"""

import math
from typing import List

# Per task type, because DPO's workable band sits about a decade below SFT's; one pair
# of bounds would silently clip legitimate DPO suggestions at the instruct floor.
ABSOLUTE_BOUNDS = {
    "instruct": (1e-6, 1e-3),
    "chat": (1e-6, 1e-3),
    "dpo": (1e-7, 1e-4),
    "grpo": (1e-7, 1e-4),
}
DEFAULT_BOUNDS = (1e-6, 1e-3)

# Beyond this much disagreement one of the two is badly wrong, and a midpoint buys real
# resolution for one extra probe. Below it the two are close enough that a third probe
# is 6 minutes for nothing.
MIDPOINT_DECADES = 1.0


def bounds_for(task_type: str) -> tuple:
    key = (task_type or "").lower().replace("task", "").replace("text", "").strip("_")
    return ABSOLUTE_BOUNDS.get(key, DEFAULT_BOUNDS)


def clamp(lr: float, task_type: str) -> float:
    lo, hi = bounds_for(task_type)
    if lr != lr or lr <= 0:  # NaN or nonsense from a degenerate sweep
        return lo
    return max(lo, min(hi, lr))


def confirmation_candidates(lrrt_lr: float, table_lr: float, task_type: str) -> List[float]:
    """Learning rates to probe, EXCLUDING the incumbent that the probe run already ran.

    The probe run trains at `table_lr` and records its held-out score, so that arm is
    already paid for. What is left is the LRRT suggestion, plus a midpoint when the two
    disagree enough to make the space between them worth resolving.
    """
    suggestion = clamp(float(lrrt_lr), task_type)
    incumbent = float(table_lr)

    # A suggestion that lands on the incumbent adds nothing: the probe already has it.
    if incumbent > 0 and abs(math.log10(suggestion / incumbent)) < 0.05:
        return []

    out = [suggestion]
    # >= not >: a full decade of disagreement is already "one of these is badly wrong",
    # and 10x is the canonical poisoned-prior case the recovery gate uses. A strict >
    # would skip the midpoint at exactly the operating point we most want resolved.
    if incumbent > 0 and abs(math.log10(suggestion / incumbent)) >= MIDPOINT_DECADES:
        midpoint = clamp(math.sqrt(suggestion * incumbent), task_type)
        # Geometric, not arithmetic: learning rates are compared on a log scale, and an
        # arithmetic midpoint between 8e-5 and 8e-4 sits at 4.4e-4, which is not the
        # middle of anything that matters.
        if all(abs(math.log10(midpoint / x)) > 0.05 for x in (suggestion, incumbent)):
            out.append(midpoint)
    return out


def describe(lrrt_lr: float, table_lr: float, task_type: str) -> str:
    lo, hi = bounds_for(task_type)
    clamped = clamp(float(lrrt_lr), task_type)
    note = "" if abs(clamped - float(lrrt_lr)) < 1e-12 else f" (clamped from {float(lrrt_lr):.3e})"
    cands = confirmation_candidates(lrrt_lr, table_lr, task_type)
    return (
        f"[lr-search] task={task_type} bounds=[{lo:.1e},{hi:.1e}] "
        f"lrrt={clamped:.3e}{note} incumbent={float(table_lr):.3e} "
        f"-> probe {[f'{c:.3e}' for c in cands] or 'nothing new'}"
    )
