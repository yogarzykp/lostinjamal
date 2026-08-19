"""Dedup must not collapse a dataset whose text lives outside the configured fields.

`_canonical_text` picks the first non-empty STRING among the instruct keys and the
output keys. A ChatTask row carries only `conversations` — a list of turn dicts — so
both loops found nothing and every row canonicalised to the same empty string. Exact
hashing then declared them all duplicates.

Measured on a real chat fixture before the fix: 3000 rows in, 1 row out, and the split
that followed produced zero training rows, so the task died at tokenisation. Not a
degraded run — no run at all, on a task type that appears in tournament boss rounds.

The rule the fix encodes: finding no text in the fields we know about is evidence that
we are looking in the wrong place, never evidence that the rows are alike.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from data.dedup_knn import dedup_from_env  # noqa: E402


def _chat_rows(n, distinct=True):
    return [
        {"conversations": [
            {"from": "user", "value": f"question {i if distinct else 0}"},
            {"from": "assistant", "value": f"answer {i if distinct else 0}"},
        ]}
        for i in range(n)
    ]


def test_distinct_chat_rows_all_survive():
    """The regression: this returned 1 before the fix."""
    kept, stats = dedup_from_env(_chat_rows(500))
    assert len(kept) == 500, f"chat rows were collapsed: {stats}"
    assert stats["exact_removed"] == 0


def test_identical_chat_rows_still_collapse():
    """The fallback must still be a real dedup, not a blanket opt-out."""
    kept, _ = dedup_from_env(_chat_rows(40, distinct=False))
    assert len(kept) == 1


def test_chat_rows_differing_only_in_the_last_turn_are_distinct():
    rows = [
        {"conversations": [{"from": "user", "value": "same"}, {"from": "assistant", "value": "A"}]},
        {"conversations": [{"from": "user", "value": "same"}, {"from": "assistant", "value": "B"}]},
    ]
    kept, _ = dedup_from_env(rows)
    assert len(kept) == 2


def test_instruct_behaviour_is_unchanged():
    """The named-field path must keep working exactly as before."""
    rows = [{"instruct": f"i{i}", "input": "", "output": f"o{i}"} for i in range(50)]
    kept, _ = dedup_from_env(rows)
    assert len(kept) == 50

    dupes = [{"instruct": "same", "input": "", "output": "same"} for _ in range(10)]
    kept2, _ = dedup_from_env(dupes)
    assert len(kept2) == 1


def test_instruct_rows_still_dedup_on_fields_not_on_whole_row():
    """Two rows equal on instruct+output are duplicates even if other keys differ.

    This is what stops the whole-row fallback from silently taking over the named-field
    path — the fallback must only apply when the named fields yield nothing at all.
    """
    rows = [
        {"instruct": "q", "input": "", "output": "a", "row_id": 1},
        {"instruct": "q", "input": "", "output": "a", "row_id": 2},
    ]
    kept, _ = dedup_from_env(rows)
    assert len(kept) == 1, "named-field dedup must ignore incidental extra columns"


def test_rows_with_unserialisable_values_do_not_crash():
    rows = [{"conversations": [{"from": "user", "value": "x"}], "weird": object()} for _ in range(3)]
    kept, _ = dedup_from_env(rows)
    assert len(kept) >= 1
