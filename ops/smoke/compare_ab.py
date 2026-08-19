#!/usr/bin/env python3
"""Compare two A/B arms the way the validator compares two submissions.

A single mean loss per arm is not enough to call a winner at the margins that decide
this tournament. The whole 8-miner field fit inside 1.84% on one real task, and the
gap we are trying to close is 0.01-0.06 nats — comfortably inside the run-to-run noise
of a single training run. So this reports the same statistics the boss round uses
(validator/tournament/constants.py): a paired per-example win rate and a mean gap, each
with a one-sided bootstrap lower bound, rather than a bare difference of means.

Pairing matters: both arms are scored on the SAME held-out examples in the same order,
so example i is directly comparable between arms. A paired test removes the variance
that comes from some examples simply being harder than others, which is most of it.

The bars quoted for reference are the validator's own dethrone thresholds
(BOSS_ROUND_MIN_WIN_RATE = 0.55, BOSS_ROUND_MIN_MEAN_GAP_NATS = 0.01). They are not
the bar for "is this change worth keeping" — a smaller, real improvement is still
worth keeping — but they are the scale that decides tournaments, so they are the right
thing to measure against.

Usage:  compare_ab.py --a <a0.json> --b <b.json> [--label-a ...] [--label-b ...]
"""
import argparse
import json
import random
import statistics


def load_vector(path):
    with open(path) as f:
        d = json.load(f)
    for key in ("losses", "per_example", "vector"):
        if isinstance(d, dict) and key in d:
            return [float(x) for x in d[key]]
    if isinstance(d, list):
        return [float(x) for x in d]
    raise SystemExit(f"{path}: could not find a per-example vector (keys: {list(d)[:8]})")


def bootstrap_lower_bound(diffs, confidence=0.99, resamples=10000, seed=0, stat=statistics.mean):
    """One-sided lower bound on `stat`, matching the validator's approach."""
    rng = random.Random(seed)
    n = len(diffs)
    vals = []
    for _ in range(resamples):
        vals.append(stat([diffs[rng.randrange(n)] for _ in range(n)]))
    vals.sort()
    return vals[int((1.0 - confidence) * resamples)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True, help="control arm vector")
    ap.add_argument("--b", required=True, help="treatment arm vector")
    ap.add_argument("--label-a", default="control")
    ap.add_argument("--label-b", default="ours")
    ap.add_argument("--resamples", type=int, default=10000)
    args = ap.parse_args()

    a, b = load_vector(args.a), load_vector(args.b)
    if len(a) != len(b):
        raise SystemExit(f"vectors differ in length ({len(a)} vs {len(b)}); the arms were "
                         f"not scored on the same held-out set, so they cannot be compared")

    # Positive diff = b is better (lower loss) on that example.
    diffs = [x - y for x, y in zip(a, b)]
    decided = [d for d in diffs if abs(d) > 1e-9]
    wins = sum(1 for d in decided if d > 0)

    mean_a, mean_b = statistics.mean(a), statistics.mean(b)
    mean_gap = statistics.mean(diffs)
    win_rate = wins / len(decided) if decided else 0.0

    gap_lb = bootstrap_lower_bound(diffs, resamples=args.resamples)
    wr_lb = bootstrap_lower_bound(
        [1.0 if d > 0 else 0.0 for d in decided], resamples=args.resamples
    ) if decided else 0.0

    print(f"examples            : {len(a)} ({len(decided)} decided)")
    print(f"{args.label_a:<20}: {mean_a:.6f}")
    print(f"{args.label_b:<20}: {mean_b:.6f}")
    print()
    print(f"mean gap (a - b)    : {mean_gap:+.6f} nats   lower bound {gap_lb:+.6f}")
    print(f"per-example win rate: {win_rate:.4f}          lower bound {wr_lb:.4f}")
    print()
    print(f"validator dethrone bars, for scale: win rate >= 0.55 AND mean gap >= 0.01 nats")
    print()

    # The honest verdict is about whether the sign is established, not about magnitude.
    if gap_lb > 0 and wr_lb > 0.5:
        verdict = f"{args.label_b} is better, and the bootstrap bound clears zero on both statistics"
    elif mean_gap > 0 and gap_lb <= 0:
        verdict = (f"{args.label_b} looks better on the point estimate, but the bound does not "
                   f"clear zero — this is not distinguishable from noise on one run per arm")
    elif mean_gap < 0 and bootstrap_lower_bound([-d for d in diffs], resamples=args.resamples) > 0:
        verdict = f"{args.label_a} is better, and the bound clears zero — the features COST us here"
    else:
        verdict = "no separation either way on this evidence"
    print(f"verdict: {verdict}")

    if len(a) < 500:
        print("\nnote: fewer than 500 examples — the bound is wide and one run per arm is one "
              "sample of training noise. Treat a narrow result as provisional.")


if __name__ == "__main__":
    main()
