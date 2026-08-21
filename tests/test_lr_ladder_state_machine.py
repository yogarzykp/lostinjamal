import os
import re
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

# text_trainer's import chain reaches the whole training stack, so this file runs where
# that stack exists — the smoke box — not on a laptop. That is not a compromise: the
# point was never to avoid dependencies, it was to avoid a 70-minute training run. Here
# the same logic is exercised in milliseconds.
tt = pytest.importorskip("text_trainer", reason="needs the training stack; run on the smoke box")

  # noqa: E402


def lr_of(cmd):
    m = re.search(r"--learning_rate\s+([0-9.eE+-]+)", cmd or "")
    return float(m.group(1)) if m else None


def test_substitution_changes_the_rate_when_the_flag_has_a_neighbour():
    cmd = "python train_instruct.py --learning_rate 1e-4 --seed 42 --bf16 True"
    out = tt.replace_args_in_cmd(cmd, "learning_rate", "2.5e-6")
    assert out is not None
    assert lr_of(out) == 2.5e-6


def test_substitution_returns_none_when_the_flag_is_last():
    """The blind spot. `(\\s+)` after the value means a trailing flag never matches.

    The caller does `train_cmd = replace_args_in_cmd(...)` and later `if train_cmd:`,
    so a None here does not raise — it skips the run. A ladder whose candidate runs are
    skipped looks like a ladder that ran and agreed with its prior.
    """
    cmd = "python train_instruct.py --seed 42 --learning_rate 1e-4"
    assert tt.replace_args_in_cmd(cmd, "learning_rate", "2.5e-6") is None


def test_extraction_shares_the_blind_spot():
    """Same regex shape, and `halve_request_max_length` depends on it."""
    assert tt.extract_value_from_cmd("a --request_path r.json --x 1", "request_path") == "r.json"
    assert tt.extract_value_from_cmd("a --x 1 --request_path r.json", "request_path") is None


def test_substituting_every_candidate_rate_yields_distinct_commands():
    """The invariant the last GPU run violated: run i must train at lrs[i].

    Driven through the real substitution helper, so a regression in it shows up here
    rather than 70 minutes into a GPU run.
    """
    base = "python train_instruct.py --learning_rate 8.07e-04 --seed 42 --bf16 True"
    lrs = [8.07e-04, 1.0e-06, 2.841e-05]
    got = [lr_of(tt.replace_args_in_cmd(base, "learning_rate", str(x))) for x in lrs]
    assert got == lrs, f"candidate rates did not survive substitution: {got}"
    assert len(set(got)) == len(lrs), "two candidates would train at the same rate"


def test_the_log_scale_the_ladder_searches_is_the_one_the_recovery_gate_measured():
    """Ties get_log_scale to the reachability bound recorded in the recovery tests."""
    from core.models.utility_models import TaskType

    assert tt.get_log_scale(TaskType.INSTRUCTTEXTTASK.value) == 0.18
    assert tt.get_log_scale(TaskType.CHATTASK.value) == 0.18
    assert tt.get_log_scale(TaskType.DPOTASK.value) == 0.18
    assert tt.get_log_scale(TaskType.GRPOTASK.value) == 0.2
