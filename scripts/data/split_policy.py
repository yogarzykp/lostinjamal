"""Train/dev split policy: proportional sizing + leak-controlled grouping.

Why this exists
---------------
Every selection signal we act on reads dev loss — best-checkpoint selection,
early stopping, the WSM pool, and (since 2026-08-05) DPO learning-rate
selection. Two defects in the inherited split quietly degraded all of them at
once:

1. A fixed `dev_size=200` is wrong at both ends of the range. On a 500-row task
   that is a 40% holdout, starving training. On a 200k-row task it is a sample
   too small to separate candidates whose eval losses differ in the fourth
   decimal — and tournament margins run that thin.

2. A plain `shuffle` + positional slice lets near-duplicate rows straddle the
   split. When that happens dev loss is partly measuring memorisation of rows
   the model already trained on, so it reads better than the model is, and the
   checkpoint/LR we select on it is not the one that generalises.

Design
------
Sizing is proportional with a floor and a ceiling, and never exceeds a quarter
of the data.

Leak control is group-atomic assignment, not similarity search: rows are
bucketed by a normalised key derived from their prompt side, and a bucket is
assigned to exactly one side of the split. Two rows sharing a normalised prompt
can therefore never end up on opposite sides. This is O(n) — no pairwise
comparison, no timeout to babysit — and it composes with the exact-hash dedup
that runs before it (dedup removes identical rows; this stops the *remaining*
templated near-duplicates from leaking).

Buckets larger than the dev target are forced to train: a single bucket that
could swallow the whole dev set is not a dev bucket.

Stdlib only, so it adds no image dependency.
"""

import hashlib
import random
import re
import unicodedata

DEFAULT_FRACTION = 0.05
DEFAULT_FLOOR = 64
DEFAULT_CEILING = 1000
MAX_DEV_SHARE = 0.25

# Prompt-side fields, most specific first, per task type.
INSTRUCT_KEYS = ("instruct", "instruction", "input", "prompt", "question")
DPO_KEYS = ("prompt", "question", "instruction", "input")
GRPO_KEYS = ("prompt", "question", "instruction", "input")

_WS = re.compile(r"\s+")
_PUNCT = re.compile(r"[^\w\s]", re.UNICODE)


def dev_target_size(
    n: int,
    fraction: float = DEFAULT_FRACTION,
    floor: int = DEFAULT_FLOOR,
    ceiling: int = DEFAULT_CEILING,
) -> int:
    """Dev-set size for a dataset of n rows.

    Proportional, clamped to [floor, ceiling], and never more than MAX_DEV_SHARE
    of the data so a small task is not starved of training rows.
    """
    if n <= 0:
        return 0
    target = round(n * fraction)
    target = max(floor, min(ceiling, target))
    hard_cap = max(1, int(n * MAX_DEV_SHARE))
    return min(target, hard_cap)


def normalise_for_grouping(text: str) -> str:
    """Casefold, strip punctuation and accents, collapse whitespace.

    Deliberately lossy: the point is that templated rows differing only by
    surface formatting land in the same bucket.
    """
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.casefold()
    text = _PUNCT.sub(" ", text)
    return _WS.sub(" ", text).strip()


def leak_key(item: dict, keys: tuple[str, ...]) -> str:
    """Bucket key for one row: hash of its normalised prompt side.

    Falls back to the row's own identity when no prompt-side field carries text,
    so such rows are never merged into one giant bucket.
    """
    if not isinstance(item, dict):
        return "id:" + str(id(item))
    parts = []
    for k in keys:
        v = item.get(k)
        if isinstance(v, str) and v.strip():
            parts.append(normalise_for_grouping(v))
    if not parts:
        return "id:" + str(id(item))
    return hashlib.sha1(" | ".join(parts).encode("utf-8", "ignore")).hexdigest()


def leak_safe_split(
    items: list,
    keys: tuple[str, ...],
    seed: int = 42,
    fraction: float = DEFAULT_FRACTION,
    floor: int = DEFAULT_FLOOR,
    ceiling: int = DEFAULT_CEILING,
) -> tuple[list, list, dict]:
    """Split items into (train, dev, stats) with no bucket straddling the split."""
    n = len(items)
    target = dev_target_size(n, fraction, floor, ceiling)
    if target <= 0 or n == 0:
        return list(items), [], {"n": n, "dev": 0, "target": target, "reason": "empty"}

    buckets: dict[str, list] = {}
    for it in items:
        buckets.setdefault(leak_key(it, keys), []).append(it)

    # Deterministic order first, then a seeded shuffle, so the split is
    # reproducible but not correlated with the input ordering.
    keys_sorted = sorted(buckets)
    random.Random(seed).shuffle(keys_sorted)

    dev: list = []
    train: list = []
    oversized = 0
    for k in keys_sorted:
        bucket = buckets[k]
        if len(bucket) > target:
            # A bucket that alone exceeds the dev target belongs in train.
            oversized += 1
            train.extend(bucket)
        elif len(dev) < target:
            dev.extend(bucket)
        else:
            train.extend(bucket)

    # A templated dataset — one instruction repeated over thousands of rows — puts
    # every row in a single oversized bucket, and the loop above sends all of them
    # to train. An empty dev set is not a degraded split, it is a dead run: the
    # packer divides by len(dev) and raises before training starts, so the task
    # scores nothing. A dev set that leaks is strictly better than no submission,
    # so when the leak-free carve comes up empty we take rows anyway and say so.
    forced_leak = 0
    if not dev and train:
        forced_leak = min(target, max(1, len(train) // 2))
        dev = train[:forced_leak]
        train = train[forced_leak:]

    # The mirror case: a tiny dataset can put every bucket in dev and leave
    # nothing to train on. Training is the point, so it wins the last row.
    if not train and len(dev) > 1:
        train, dev = dev[1:], dev[:1]

    stats = {
        "n": n,
        "buckets": len(buckets),
        "collapsed": n - len(buckets),  # rows sharing a bucket with another row
        "oversized_buckets": oversized,
        "target": target,
        "dev": len(dev),
        "train": len(train),
        "forced_leak": forced_leak,
    }
    return train, dev, stats
