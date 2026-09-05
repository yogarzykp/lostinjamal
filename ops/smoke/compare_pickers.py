"""What each LR picker would have chosen, from curves that already exist.

The 2026-08-22 comparison needed four GPU curves to answer a question that is arithmetic
once a curve is saved — and then those curves were lost, so the question had to be re-asked
with fresh GPU time. This reads `lrrt_curve.json` files and reports every candidate against
the incumbent, so the next person spends zero GPU on it.

    python3 compare_pickers.py <dir-of-curves-or-json> [...]

What it deliberately does NOT claim: which picker is BETTER. Distance to the incumbent is
not held-out loss, and our own measurement says the error is asymmetric — a 10x-HIGH prior
cost +36% held-out loss where a 10x-LOW prior cost +2.7%. So a pick that is nearer in
log-distance can still be the more expensive one, and only ops/smoke/lr_recovery.sh can
settle direction. This script exists to say whether that expensive run is warranted at all:
if every candidate lands within the fence the downstream search already absorbs, it is not.
"""

from __future__ import annotations

import json
import os
import sys


def _slope_index(lrs, losses):
    """Reproduce find_lr_lrrt's steepest-descent pick from the saved curve.

    Kept in step with lr_finder deliberately rather than imported: lr_finder needs torch,
    and this has to run on a laptop against a curve fetched from a box.
    """
    import math
    # `slopes` starts at i=1 and carries NO leading zero, so slopes[k] belongs to lrs[k+1].
    # Prepending a zero here shifted every index by one and moved all three of the first
    # curves I ran this against — caught only because the saved suggested_safe_lr is
    # compared back against this reconstruction. Keep that check.
    log_lrs = [math.log10(lr) for lr in lrs]
    slopes = []
    for i in range(1, len(losses)):
        d_loss = losses[i] - losses[i - 1]
        d_loglr = log_lrs[i] - log_lrs[i - 1]
        slopes.append(0 if abs(d_loglr) < 1e-9 else d_loss / d_loglr)
    skip = min(max(5, len(slopes) // 10), max(1, len(slopes) - 1))
    searchable = slopes[skip:]
    if not searchable or all(s >= 0 for s in searchable):
        return len(lrs) // 2
    return min(searchable.index(min(searchable)) + skip + 1, len(lrs) - 1)


def candidates(curve):
    lrs, losses = curve["lrs"], curve["smoothed_losses"]
    si = _slope_index(lrs, losses)
    li = losses.index(min(losses))
    return {
        "slope10": lrs[si] / 10.0,
        "slope": lrs[si],
        "lossmin": lrs[li],
        "lossmin10": lrs[li] / 10.0,
    }, si, li


def _ratio(lr, incumbent):
    """Signed factor: >1 means the pick is that many times ABOVE the incumbent."""
    if not incumbent or not lr:
        return float("nan")
    return lr / incumbent


def main(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            for root, _, names in os.walk(p):
                files += [os.path.join(root, n) for n in names if n == "lrrt_curve.json"]
        else:
            files.append(p)
    if not files:
        print("no lrrt_curve.json found", file=sys.stderr)
        return 2

    names = ("slope10", "slope", "lossmin", "lossmin10")
    per_picker = {n: [] for n in names}

    for f in sorted(files):
        curve = json.load(open(f))
        cands, si, li = candidates(curve)
        inc = curve.get("incumbent") or 0.0
        cell = os.path.basename(os.path.dirname(f))
        print(f"\n{cell}  ({curve.get('points')} points, task={curve.get('task_type')}, "
              f"accepted={curve.get('accepted')})")
        print(f"  incumbent      {inc:.3e}")
        print(f"  slope idx {si}, loss-min idx {li}")
        for n in names:
            r = _ratio(cands[n], inc)
            per_picker[n].append(r)
            side = "above" if r > 1 else "below"
            print(f"  {n:<10} {cands[n]:.3e}   {max(r, 1/r if r else 0):6.1f}x {side}")
        saved = curve.get("suggested_safe_lr")
        if saved is not None:
            match = abs(saved - cands["slope10"]) <= abs(saved) * 1e-6
            print(f"  saved suggested_safe_lr {saved:.3e} — reproduces slope10: {match}")

    print("\n=== across %d curve(s), geometric mean distance from incumbent ===" % len(files))
    import math
    for n in names:
        rs = [r for r in per_picker[n] if r == r and r > 0]
        if not rs:
            continue
        geo = math.exp(sum(math.log(max(r, 1 / r)) for r in rs) / len(rs))
        above = sum(1 for r in rs if r > 1)
        print(f"  {n:<10} {geo:6.1f}x   ({above}/{len(rs)} land above the incumbent)")
    print("\nDirection, not distance, decides this — see the module docstring.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["."]))
