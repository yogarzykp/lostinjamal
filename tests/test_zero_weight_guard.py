"""A zeroed ZeRO-3 save has no NaN, loads cleanly, and scores at chance.

The NaN/Inf guard cannot see it — zero is a perfectly good float — so the checkpoint
passes every existing check, uploads, and loses the task with nothing in the log that
reads as an error. The official diff report for tourn_add1dc83b8fd58b0_20260831 flagged
this as worth taking from the challenger; that repo now 404s, so this is the property
rewritten rather than the file copied.

The risk that governs the design is the false positive, not the false negative. Sending a
healthy submission to the noise fallback is a certain loss; missing a zeroed shard is a
loss we were going to take anyway. Hence "every sampled weight matrix is zero" rather than
"any tensor is zero" — biases and some gates are legitimately zero, and a guard that
tripped on those would fire on ordinary models.
"""

from __future__ import annotations

import ast
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAINER = os.path.join(ROOT, "scripts", "text_trainer.py")


def _source():
    with open(TRAINER, "r", encoding="utf-8") as fh:
        return fh.read()


@pytest.fixture
def guard():
    """The guard AND the predicate it calls — text_trainer as a whole needs transformers.

    Both, because the first version exec'd only `checkpoint_weights_are_degenerate` and
    the predicate it delegates to was therefore undefined. The guard caught the NameError
    on its own fail-open path and returned False — so eight of the nine tests here passed,
    since eight of them expect False. Only the one case expecting True exposed it.

    A fixture that under-populates its namespace fails exactly like the code being wrong,
    and mostly in the direction that looks like a pass.
    """
    ns = {"os": os}
    tree = ast.parse(_source())
    wanted = ("count_zero_weight_matrices", "checkpoint_weights_are_degenerate")
    for name in wanted:
        node = next(n for n in tree.body
                    if isinstance(n, ast.FunctionDef) and n.name == name)
        exec(compile(ast.Module(body=[node], type_ignores=[]), TRAINER, "exec"), ns)  # noqa: S102
    return ns["checkpoint_weights_are_degenerate"]


# NOT module-level importorskip. That skipped the whole file on a machine without torch —
# including the AST wiring tests below, which need nothing — and pytest reported the lot as
# a single "1 skipped" line that reads like a pass. The tests that can run here must run
# here, because the wiring ones are precisely what catch a guard nothing calls.
try:
    import torch
    from safetensors.torch import save_file
    HAVE_TORCH = True
except Exception:  # pragma: no cover - depends on the machine, not the code
    HAVE_TORCH = False

needs_torch = pytest.mark.skipif(not HAVE_TORCH, reason="reads real tensors")


def _write(tmp_path, tensors, name="model.safetensors"):
    save_file(tensors, str(tmp_path / name))
    return str(tmp_path)


@needs_torch
def test_an_all_zero_checkpoint_is_flagged(guard, tmp_path):
    d = _write(tmp_path, {"a.weight": torch.zeros(8, 8), "b.weight": torch.zeros(4, 4)})
    assert guard(d) is True


@needs_torch
def test_a_healthy_checkpoint_is_not_flagged(guard, tmp_path):
    d = _write(tmp_path, {"a.weight": torch.randn(8, 8), "b.weight": torch.randn(4, 4)})
    assert guard(d) is False


@needs_torch
def test_one_zero_layer_among_healthy_ones_is_not_flagged(guard, tmp_path):
    """The false positive that matters: a legitimately zeroed gate must not divert a run."""
    d = _write(tmp_path, {"a.weight": torch.zeros(8, 8), "b.weight": torch.randn(8, 8)})
    assert guard(d) is False


@needs_torch
def test_zero_biases_alongside_real_weights_are_ignored(guard, tmp_path):
    """Biases initialise to zero on plenty of models; only 2D weights are evidence."""
    d = _write(tmp_path, {"a.weight": torch.randn(8, 8),
                          "a.bias": torch.zeros(8),
                          "norm.weight": torch.zeros(8)})
    assert guard(d) is False


@needs_torch
def test_a_checkpoint_of_only_1d_tensors_is_not_flagged(guard, tmp_path):
    """No weight matrices sampled means no evidence either way — do not guess."""
    d = _write(tmp_path, {"a.bias": torch.zeros(8), "b.bias": torch.zeros(8)})
    assert guard(d) is False


@needs_torch
def test_an_empty_directory_is_not_flagged(guard, tmp_path):
    assert guard(str(tmp_path)) is False


@needs_torch
def test_a_missing_directory_is_not_flagged(guard, tmp_path):
    assert guard(str(tmp_path / "nope")) is False


@needs_torch
def test_an_unreadable_shard_does_not_flag(guard, tmp_path):
    """Fail-open: a corrupt file is not evidence that the weights are zero."""
    (tmp_path / "model.safetensors").write_bytes(b"not a safetensors file")
    assert guard(str(tmp_path)) is False


@needs_torch
def test_integer_tensors_are_not_counted_as_weights(guard, tmp_path):
    """Zeroed int buffers (masks, position ids) are ordinary and carry no signal."""
    d = _write(tmp_path, {"mask": torch.zeros(8, 8, dtype=torch.int64),
                          "a.weight": torch.randn(8, 8)})
    assert guard(d) is False


# --- and it has to be wired, on the same fallback as the NaN guard -------------------


def test_the_guard_is_called_from_the_trainer():
    tree = ast.parse(_source())
    called = [n for n in ast.walk(tree)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
              and n.func.id == "checkpoint_weights_are_degenerate"]
    assert called, "the guard exists but nothing calls it"


def test_it_routes_to_the_same_noise_fallback_as_nan():
    """A degenerate checkpoint is worth no more than a NaN one; both ship the fallback."""
    src = _source()
    assert "if _nan_hit or _zero_hit:" in src, (
        "the zero-weight verdict does not reach the fallback that the NaN verdict uses"
    )


def test_it_only_runs_on_a_successful_train():
    """On the failure path the submission is about to be overwritten with noise anyway."""
    src = _source()
    i = src.index("_zero_hit = ")
    assert "train_success" in src[i:i + 200]


def test_it_does_not_re_scan_when_nan_already_fired():
    """Both verdicts lead to the same fallback, so the second scan would buy nothing —
    and it is spent inside the post-training window that already runs tight."""
    src = _source()
    i = src.index("_zero_hit = ")
    assert "not _nan_hit" in src[i:i + 200]


# --- the decision itself, with no torch anywhere -------------------------------------
#
# These are the tests that matter most and they were the ones being skipped. The predicate
# takes an iterable, so a handful of stand-ins exercise every branch of it on any machine.


class _T:
    """The smallest thing that behaves like a tensor for this predicate."""

    def __init__(self, ndim, zero, floating=True):
        self.ndim, self._zero, self._f = ndim, zero, floating

    def is_floating_point(self):
        return self._f

    def __eq__(self, other):
        return _Cmp(self._zero)


class _Cmp:
    def __init__(self, v):
        self.v = v

    def all(self):
        return self.v


@pytest.fixture
def counter():
    ns = {}
    tree = ast.parse(_source())
    node = next(n for n in tree.body
                if isinstance(n, ast.FunctionDef) and n.name == "count_zero_weight_matrices")
    exec(compile(ast.Module(body=[node], type_ignores=[]), TRAINER, "exec"), ns)  # noqa: S102
    return ns["count_zero_weight_matrices"]


def test_all_zero_weights_count_as_all_zero(counter):
    assert counter([_T(2, True), _T(2, True)]) == (2, 2)


def test_a_single_zero_weight_does_not_make_the_set_zero(counter):
    """The false positive the design exists to avoid."""
    seen, zeros = counter([_T(2, True), _T(2, False)])
    assert seen == 2 and zeros == 1


def test_one_dimensional_tensors_are_not_counted(counter):
    """Biases and norms are legitimately zero and carry no learned signal."""
    assert counter([_T(1, True), _T(1, True)]) == (0, 0)


def test_non_floating_tensors_are_not_counted(counter):
    """Zeroed int masks are ordinary."""
    assert counter([_T(2, True, floating=False)]) == (0, 0)


def test_an_empty_iterable_yields_no_evidence(counter):
    assert counter([]) == (0, 0)


def test_a_tensor_that_raises_is_skipped_not_fatal(counter):
    class _Boom:
        ndim = 2

        def is_floating_point(self):
            raise RuntimeError("unreadable")

    seen, zeros = counter([_Boom(), _T(2, True)])
    assert seen == 1 and zeros == 1


def test_a_tensor_without_the_attributes_is_skipped(counter):
    assert counter([object()]) == (0, 0)


def test_the_predicate_lives_at_module_level():
    """Nested inside the reader, every test of it needed torch — and skipped."""
    tree = ast.parse(_source())
    assert any(isinstance(n, ast.FunctionDef) and n.name == "count_zero_weight_matrices"
               for n in tree.body), "the predicate is not importable on its own"


def test_the_threshold_is_every_matrix_not_any_of_them():
    """The design's whole safety margin, pinned where a laptop can check it.

    The behavioural version of this needs torch and skips here, and a mutation flipping
    `total_zero == total_seen` to `total_zero > 0` survived the entire local suite. That
    mutation turns a guard that almost never misfires into one that diverts any model with
    a single zeroed gate straight to the noise fallback.
    """
    tree = ast.parse(_source())
    fn = next(n for n in ast.walk(tree)
              if isinstance(n, ast.FunctionDef)
              and n.name == "checkpoint_weights_are_degenerate")
    compares = [n for n in ast.walk(fn) if isinstance(n, ast.Compare)]
    equality = [
        c for c in compares
        if isinstance(c.ops[0], ast.Eq)
        and "total_zero" in ast.unparse(c.left)
        and "total_seen" in ast.unparse(c.comparators[0])
    ]
    assert equality, (
        "no `total_zero == total_seen` test — the verdict is not 'every sampled matrix', "
        "so a single legitimately-zero layer can send a healthy submission to the fallback"
    )


# --- the two paths a mutation walked straight through --------------------------------


@needs_torch
def test_a_pytorch_bin_checkpoint_is_read_too(guard, tmp_path):
    """Every other test writes safetensors, so deleting the .bin branch changed nothing.

    Checkpoints in the older format are exactly as capable of being zeroed, and a guard
    that silently only covers one serialisation is a guard with a hole in it.
    """
    torch.save({"a.weight": torch.zeros(8, 8), "b.weight": torch.zeros(4, 4)},
               str(tmp_path / "pytorch_model.bin"))
    assert guard(str(tmp_path)) is True


@needs_torch
def test_a_healthy_bin_checkpoint_is_not_flagged(guard, tmp_path):
    torch.save({"a.weight": torch.randn(8, 8), "b.weight": torch.randn(4, 4)},
               str(tmp_path / "pytorch_model.bin"))
    assert guard(str(tmp_path)) is False


@needs_torch
def test_safetensors_wins_when_both_formats_are_present(guard, tmp_path):
    """The reader prefers safetensors; a stale zeroed .bin beside it must not decide."""
    _write(tmp_path, {"a.weight": torch.randn(8, 8)})
    torch.save({"a.weight": torch.zeros(8, 8)}, str(tmp_path / "pytorch_model.bin"))
    assert guard(str(tmp_path)) is False


def test_an_unexpected_failure_fails_open(guard):
    """The single most damaging change this file can suffer.

    Flipping the outer handler from `return False` to `return True` sent every healthy
    submission to the noise fallback on any unexpected error, and passed the whole suite:
    the corrupt-shard test only reaches the per-shard handler inside the loop. Passing
    something that breaks os.path.join is the shortest route to the outer one.
    """
    assert guard(None) is False


def test_the_scan_stays_bounded():
    """Sampling caps, pinned because no behavioural test can reach them.

    Removing `[:3]` on shards or `[:50]` on tensors leaves the guard correct and slower,
    so both mutations survive a suite whose checkpoints are 8x8. They matter anyway: this
    runs inside the post-training window that already overran its budget by 29 seconds on
    our cheapest task, and an unbounded scan of a 70-shard checkpoint is the kind of cost
    that turns a guard into the thing that loses the submission.
    """
    src = _source()
    body = src[src.index("def checkpoint_weights_are_degenerate"):]
    body = body[:body.index("\n# Keys the validator")]
    # Per branch, not a bare "[:50]" search: the two readers each carry their own cap,
    # so a single substring assertion is satisfied by whichever one the mutation left
    # alone. That is how the safetensors cap survived being deleted.
    assert "shards[:3]" in body, "the safetensors shard scan is unbounded"
    assert 'glob.glob(os.path.join(checkpoint_dir, "*.bin")))[:3]' in body, \
        "the .bin shard scan is unbounded"
    assert "list(f.keys())[:50]" in body, "the safetensors tensor scan is unbounded"
    assert "list(state.items())[:50]" in body, "the .bin tensor scan is unbounded"
