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

# How far above the incumbent to probe when nothing brackets it from above. Sized so the
# canonical 10x-low case lands inside the gate's 3x bar rather than just outside it.
UPWARD_PROBE_DECADES = 0.75

# Below this much explored range, the search has not covered enough ground for the
# incumbent-versus-suggestion comparison to mean much, and an upward probe is added.
MIN_EXPLORED_DECADES = 1.0


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

    # Restore bracketing when every candidate sits at or below the incumbent.
    #
    # The range test reads systematically LOW on a fine-tune: smoothed loss falls fastest
    # where the rate first stops being negligible — format, EOS and easy tokens are learned
    # immediately — and the sweep trains as it goes, so "loss fell" conflates progress with
    # rate. Measured here its raw suggestion was 4.13e-06 against a true 8.07e-05, ~20x low,
    # before any damping.
    #
    # That bias is exactly why a HIGH prior recovers: a low suggestion and a high prior
    # straddle the truth and the midpoint lands on it (measured 2.84x). With a LOW prior both
    # sit on the same side, nothing straddles anything, and the incumbent wins at 10x low.
    # One probe above the incumbent restores the invariant the whole mechanism rests on —
    # that the truth lies BETWEEN two candidates.
    #
    # 10**0.75 (~5.6x) rather than 3x: in the canonical 10x-low case 3x lands 3.33x from
    # true and misses the very bar this gate measures, while 10**0.75 lands 1.79x. The
    # resulting 0.75-decade gap also stays under MIDPOINT_DECADES, so it does not drag an
    # extra midpoint probe along with it.
    # The trigger is how much ground the search has covered, not which side the
    # suggestion fell on. With a HIGH prior the candidates also all sit below the
    # incumbent, but the span from the lowest candidate up to the incumbent is nearly
    # three decades and the truth is inside it — an extra probe there would only re-test
    # a rate the incumbent already proved bad. With a LOW prior that span is under a
    # decade: the search has barely moved, and nothing above it has been tried.
    # Two conditions, and both are needed.
    #
    # A narrow span alone is not enough: when the suggestion AGREES with the incumbent
    # the span is also tiny, but that is two independent methods converging — the most
    # informative outcome available, and the last place to spend another probe.
    #
    # A low suggestion alone is not enough either: with a HIGH prior the suggestion is
    # far below the incumbent too, but the span is then ~3 decades and the truth sits
    # inside it.
    #
    # It is the combination — barely any ground covered AND the suggestion pinned well
    # below the incumbent — that says the sweep gave nothing and the incumbent stands
    # unchallenged from above.
    explored = [c for c in out if c > 0] + ([incumbent] if incumbent > 0 else [])
    span_decades = math.log10(max(explored) / min(explored)) if len(explored) > 1 else 0.0
    suggestion_is_well_below = incumbent > 0 and suggestion < incumbent / 2
    if incumbent > 0 and span_decades < MIN_EXPLORED_DECADES and suggestion_is_well_below:
        upward = clamp(incumbent * (10 ** UPWARD_PROBE_DECADES), task_type)
        if all(abs(math.log10(upward / x)) > 0.05 for x in explored):
            out.append(upward)
    return out


def describe(lrrt_lr: float, table_lr: float, task_type: str) -> str:
    lo, hi = bounds_for(task_type)
    clamped = clamp(float(lrrt_lr), task_type)
    note = "" if abs(clamped - float(lrrt_lr)) < 1e-12 else f" (clamped from {float(lrrt_lr):.3e})"
    cands = confirmation_candidates(lrrt_lr, table_lr, task_type)
    # A kept incumbent must never read as a confirmation when nothing was tested above
    # it — that is the shape in which a half-working search looks like a working one.
    #
    # But the bare warning said only THAT it happened, and it happens on nearly every
    # run, so it read as a standing alarm and stopped being read at all. It is not a
    # false alarm: the condition is genuinely true. It is an unexplained one, and an
    # unexplained alarm that never clears is indistinguishable from noise.
    #
    # So say WHY. The upward probe exists to prevent exactly this, and it is gated on
    # `span_decades < MIN_EXPLORED_DECADES and suggestion < incumbent/2`. Those two can
    # only hold together in a narrow window, because `explored` includes the incumbent —
    # so a suggestion far BELOW it makes the span automatically WIDE and suppresses the
    # probe. The range test reads systematically ~20x low on a fine-tune, i.e. 1.3
    # decades, which is outside the window. Naming the reason turns a permanent alarm
    # into a diagnosis, and makes the suppression visible instead of implied.
    warn = ""
    inc = float(table_lr)
    if cands and inc > 0 and all(c <= inc * 1.05 for c in cands):
        explored = [c for c in cands if c > 0] + [inc]
        span = math.log10(max(explored) / min(explored)) if len(explored) > 1 else 0.0
        suggestion = clamp(float(lrrt_lr), task_type)
        if span >= MIN_EXPLORED_DECADES:
            why = (f"upward probe suppressed: explored span {span:.2f}d >= "
                   f"{MIN_EXPLORED_DECADES}d")
        elif not (suggestion < inc / 2):
            why = "upward probe not applicable: suggestion is not well below the incumbent"
        else:
            why = "upward probe produced nothing new"
        warn = f"  UNBRACKETED(nothing above the incumbent; {why})"
    return (
        f"[lr-search] task={task_type} bounds=[{lo:.1e},{hi:.1e}] "
        f"lrrt={clamped:.3e}{note} incumbent={float(table_lr):.3e} "
        f"-> probe {[f'{c:.3e}' for c in cands] or 'nothing new'}{warn}"
    )
