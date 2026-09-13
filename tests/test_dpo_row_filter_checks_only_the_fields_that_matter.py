"""tokenize_dpo must not drop a preference pair because some OTHER column is empty.

is_poor_item dropped a row if ANY column was None or blank. Validator DPO datasets
carry more than prompt/chosen/rejected — a `system` column is the common one, and it
is empty on most rows of most datasets. Measured by the CPU preflight on 2026-09-13:
a 95%-empty system column left 134 train / 44 dev rows of 3600. The run finishes,
on a twentieth of its data, and the log says only "Removed 3422 empty items".

Only the three fields the objective reads can make a row unusable.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

import tokenize_dpo as td  # noqa: E402

FIELDS = ("question", "good", "bad")


def _rows(n, system_blank_every=1):
    return [
        {"question": f"q{i}", "good": f"g{i}", "bad": f"b{i}",
         "system": "" if i % system_blank_every == 0 else "You are helpful.",
         "id": None}
        for i in range(n)
    ]


def test_a_blank_system_column_does_not_drop_the_pair():
    kept = td.remove_empty_items(_rows(100), required=FIELDS)
    assert len(kept) == 100, f"{len(kept)} of 100 survived — a metadata column emptied the dataset"


def test_a_blank_required_field_still_drops_the_pair():
    rows = _rows(10)
    rows[3]["good"] = ""
    rows[7]["bad"] = None
    kept = td.remove_empty_items(rows, required=FIELDS)
    assert len(kept) == 8


def test_a_missing_required_field_drops_the_pair():
    rows = _rows(5)
    del rows[2]["question"]
    assert len(td.remove_empty_items(rows, required=FIELDS)) == 4


def test_the_split_passes_the_task_fields_through(tmp_path):
    """The wire: split_dataset must hand the dataset_type's field names to the filter."""
    import json
    total = tmp_path / "total.json"
    total.write_text(json.dumps(_rows(600)))
    td.split_dataset(str(total), str(tmp_path / "train.json"), str(tmp_path / "dev.json"),
                     dev_size=100, fields=FIELDS)
    n_train = len(json.load(open(tmp_path / "train.json")))
    n_dev = len(json.load(open(tmp_path / "dev.json")))
    assert n_train + n_dev == 600, (n_train, n_dev)


def test_main_passes_the_dataset_type_fields():
    src = open(os.path.join(os.path.dirname(td.__file__), "tokenize_dpo.py"), encoding="utf-8").read()
    assert "fields=" in src.split("def main")[-1] or "fields=(" in src, "split_dataset is called without the task's field names"
