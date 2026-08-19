"""pad_sequence must never hand back a row longer than max_length.

Why this file exists: `pad_sequence` padded with `[pad] * (max_length - len(seq))`,
which is `[]` once the row is already longer than the cap — so the row came back
unpadded AND over-length, and the batch collated ragged.

That was survivable only by accident. `max_length` used to be a fixed 2048 that
tokenisation had already enforced, so no row could exceed it. Two changes break that
assumption at once: the adaptive path now plumbs a real `max_length` through, and the
OOM ladder's final rung halves that value inside the request JSON *after*
tokenisation has already run and cannot re-run. The rung that exists to rescue an
OOM would instead have crashed every remaining retry.

The tail is what we keep: in instruct SFT the prompt is masked and every trainable
label lives in the completion at the end of the row.
"""

import importlib.machinery
import os
import sys
import types

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

# utility.py pulls the training extras in at module scope. None of them take part
# in padding, which is list arithmetic, so stub whatever is not installed rather
# than making this suite depend on the full trainer environment.
def _stub(name):
    mod = types.ModuleType(name)
    # importlib refuses a parentless module without a spec, and transformers
    # probes __spec__ when it checks whether an optional backend is available.
    mod.__spec__ = importlib.machinery.ModuleSpec(name, loader=None)
    mod.__path__ = []
    return mod


for _name in ("wandb", "redis", "bitsandbytes", "peft"):
    if _name not in sys.modules:
        try:
            __import__(_name)
        except ImportError:
            sys.modules[_name] = _stub(_name)

from utility import pad_sequence  # noqa: E402

PAD = 0


@pytest.mark.parametrize("side", ["left", "right"])
def test_short_row_is_padded_to_length(side):
    out = pad_sequence([1, 2, 3], PAD, 6, side)
    assert len(out) == 6
    assert sorted(out.count(x) for x in (1, 2, 3)) == [1, 1, 1]


@pytest.mark.parametrize("side", ["left", "right"])
def test_exact_length_row_is_untouched(side):
    row = [1, 2, 3, 4]
    assert pad_sequence(list(row), PAD, 4, side) == row


@pytest.mark.parametrize("side", ["left", "right"])
def test_over_length_row_is_truncated_not_returned_whole(side):
    """The regression. Before the fix this returned all 10 tokens."""
    out = pad_sequence(list(range(10)), PAD, 4, side)
    assert len(out) == 4, "row longer than max_length must not survive at full length"


@pytest.mark.parametrize("side", ["left", "right"])
def test_truncation_keeps_the_tail(side):
    """Labels live at the end; dropping the tail would train on nothing."""
    assert pad_sequence(list(range(10)), PAD, 4, side) == [6, 7, 8, 9]


def test_the_three_streams_stay_aligned_after_truncation():
    """input_ids / attention_mask / labels must be cut at the same place.

    They are padded by three separate calls, so a length-dependent rule has to be
    applied identically to each or the row silently misaligns.
    """
    ids = list(range(10))
    mask = [1] * 10
    labels = [-100] * 6 + [7, 8, 9, 10]

    cut_ids = pad_sequence(list(ids), PAD, 4, "right")
    cut_mask = pad_sequence(list(mask), 0, 4, "right")
    cut_labels = pad_sequence(list(labels), -100, 4, "right")

    assert len(cut_ids) == len(cut_mask) == len(cut_labels) == 4
    assert cut_labels == [7, 8, 9, 10], "the trainable span must survive truncation"


def test_a_batch_of_mixed_lengths_collates_rectangular():
    """The actual failure mode: one long row made the whole batch ragged."""
    rows = [[1, 2], list(range(20)), [3, 4, 5]]
    padded = [pad_sequence(list(r), PAD, 8, "right") for r in rows]
    assert len({len(r) for r in padded}) == 1, "every row in a batch must share one length"
