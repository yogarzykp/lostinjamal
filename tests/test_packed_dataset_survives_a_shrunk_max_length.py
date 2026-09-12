"""The packed path must survive a max_length that shrank under an already-tokenised row.

The OOM ladder's last rung halves max_length in the request JSON and relaunches
without re-tokenising (text_trainer.py ~:333-375, ~:425-443). The unpacked path copes:
utility.pad_sequence truncates to the tail before padding. The packed path did not —
PackedDataset recorded each row's raw length, a row longer than the cap became its own
group, and pack_data_points_FA asserted `len(input_ids) == model_max_length` after
padding by a negative amount. AssertionError -> run_training False -> the retry loop
breaks -> empty submission -> noise fallback. A forfeit shape, on exactly the run that
had just survived an OOM.

Same keep-the-tail rule as pad_sequence: in instruct SFT the prompt is masked and the
completion carries the labels, so the front is what can be spared.
"""

import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

torch = pytest.importorskip("torch")
mp = pytest.importorskip("monkeypatch")


class _Tok:
    pad_token_id = 0
    padding_side = "right"


class _DS:
    def __init__(self, rows):
        self.eval_dataset = rows


def _row(n):
    ids = list(range(1, n + 1))
    return {"input_ids": ids, "attention_mask": [1] * n, "labels": list(ids)}


def test_over_long_rows_are_tail_truncated_and_every_group_packs(capsys):
    cap = 16
    rows = [_row(8), _row(40), _row(16), _row(23)]  # two rows over the cap
    ds = mp.PackedDataset(_DS(rows), _Tok(), max_input_length=cap, min_item_num=1)
    assert max(ds.lengths) <= cap, ds.lengths
    for i in range(len(ds)):
        batch = ds[i]  # AssertionError today on the group holding a 40- or 23-token row
        assert batch["input_ids"].shape[0] == cap
    out = capsys.readouterr().out
    assert "truncated 2" in out and "16" in out, out


def test_the_tail_is_what_survives():
    """Labels live at the end of the row; dropping the front keeps them."""
    cap = 8
    ds = mp.PackedDataset(_DS([_row(12)]), _Tok(), max_input_length=cap, min_item_num=1)
    kept = ds.data_points[0]
    assert kept["input_ids"] == list(range(5, 13))
    assert kept["labels"] == list(range(5, 13))
    assert kept["attention_mask"] == [1] * 8


def test_rows_within_the_cap_are_untouched():
    rows = [_row(8), _row(16)]
    ds = mp.PackedDataset(_DS(rows), _Tok(), max_input_length=16, min_item_num=1)
    assert ds.data_points[0]["input_ids"] == list(range(1, 9))
    assert ds.data_points[1]["input_ids"] == list(range(1, 17))
