"""The legacy parameter count must not load the weights it is counting.

model_utility.count_params_from_safetensors did `load_file(shard)` on every shard
and summed numel — every tensor materialised in RAM. On the boss round's guaranteed
35-71B instruct task (Llama-2-70b-hf: ~130 GB bf16) that exceeds the validator's
110 GB/GPU container limit: SIGKILL before training, no fallback, no upload. The
path is reached whenever the adaptive planner is bypassed (legacy cascade), i.e. on
exactly the runs already having a bad day.

A safetensors file's header carries every tensor's shape. Reading it costs a few KB
per shard and gives the same number, exactly — which is more than the config-based
estimate on the adaptive side can say about MoE or tied embeddings.
"""

import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

torch = pytest.importorskip("torch")
from safetensors.torch import save_file  # noqa: E402

import model_utility as mu  # noqa: E402


def _sharded_model(tmp_path, shapes):
    """Two real safetensors shards with the given shapes; returns exact numel."""
    total = 0
    for i, group in enumerate(shapes):
        tensors = {}
        for j, shape in enumerate(group):
            t = torch.zeros(*shape, dtype=torch.bfloat16)
            tensors[f"model.layers.{i}.w{j}"] = t
            total += t.numel()
        save_file(tensors, str(tmp_path / f"model-0000{i + 1}-of-0000{len(shapes)}.safetensors"))
    return total


def test_count_is_exact(tmp_path):
    want = _sharded_model(tmp_path, [[(64, 32), (32,)], [(16, 16, 4)]])
    assert mu.count_params_from_safetensors(str(tmp_path)) == want


def test_count_never_materialises_a_tensor(tmp_path, monkeypatch):
    """The whole point. If load_file is called, on a 70B this is the SIGKILL."""
    _sharded_model(tmp_path, [[(8, 8)], [(4, 4)]])

    def _boom(*a, **k):
        raise AssertionError("load_file was called: the counter materialised weights")

    monkeypatch.setattr(mu, "load_file", _boom, raising=False)
    import safetensors.torch as st
    monkeypatch.setattr(st, "load_file", _boom)
    assert mu.count_params_from_safetensors(str(tmp_path)) == 64 + 16


def test_count_survives_a_corrupt_shard_without_loading_the_rest(tmp_path):
    """A truncated shard must not raise the way load_file would; count what is
    readable and say so, since a wrong-but-finite count still routes the run."""
    _sharded_model(tmp_path, [[(8, 8)]])
    (tmp_path / "model-00002-of-00002.safetensors").write_bytes(b"\x10\x00\x00\x00\x00\x00\x00\x00garbage")
    got = mu.count_params_from_safetensors(str(tmp_path))
    assert got == 64


def test_no_safetensors_returns_none(tmp_path):
    assert mu.count_params_from_safetensors(str(tmp_path)) is None
