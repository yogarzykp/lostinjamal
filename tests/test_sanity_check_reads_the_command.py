"""The adaptive-output sanity check must read where the planner actually writes.

sanity_check_train_info exists to catch a planner that returned nonsense — a NaN
learning rate, batch 0 — before it burns a retry attempt at step 1. It looked for
those values in train_request; the planner puts them in the run_cmd string. So lr
was always None, the guard passed everything, and it had been inert since it was
written. Measured 2026-09-13: --learning_rate 1e3 sailed through.
"""

import importlib.machinery
import os
import sys
import types

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
if "wandb" not in sys.modules:
    _w = types.ModuleType("wandb"); _w.__spec__ = importlib.machinery.ModuleSpec("wandb", None)
    sys.modules["wandb"] = _w

tt = pytest.importorskip("text_trainer", reason="needs the training stack; run on the pinned venv")


def _ti(cmd, request=None):
    return {"run_cmd": cmd, "train_request": request if request is not None else {"model_name": "x"}}


def test_an_absurd_learning_rate_in_the_command_is_rejected():
    ok, why = tt.sanity_check_train_info(_ti("python train_instruct.py --learning_rate 1e3 --per_device_train_batch_size 4"))
    assert ok is False and "learning_rate" in why, (ok, why)


def test_a_zero_batch_in_the_command_is_rejected():
    ok, why = tt.sanity_check_train_info(_ti("python x --learning_rate 2e-5 --per_device_train_batch_size 0"))
    assert ok is False and "batch" in why, (ok, why)


def test_a_sane_command_passes():
    ok, why = tt.sanity_check_train_info(_ti("python x --learning_rate 2e-5 --per_device_train_batch_size 8"))
    assert ok is True, why


def test_the_request_still_wins_when_it_carries_the_value():
    ok, why = tt.sanity_check_train_info(_ti("python x --learning_rate 2e-5", {"learning_rate": "nan"}))
    assert ok is False, why
