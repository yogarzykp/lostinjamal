"""Dev absorption must never be the reason a submission gets worse or disappears.

This is the only code in the repo that edits an artefact we are about to be scored on,
after the last evaluation has run. There is nothing downstream to catch a regression, so
the property that matters most is not "does it improve the model" — we cannot know that
here — but "when it declines or fails, is the submission exactly what it was".

Every test below therefore asserts the same invariant on top of its own case: the
submission directory is byte-for-byte unchanged. A test that only checked the return
value would pass while the function had already half-rewritten the weights.

The decline paths are reachable without torch, deliberately: they all sit above the
import, so the guards can be exercised on any machine rather than only where the
training extras happen to be installed.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
MODULE = os.path.join(SCRIPTS, "dev_absorption.py")
TRAINER = os.path.join(SCRIPTS, "text_trainer.py")


def _source(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


@pytest.fixture
def absorb():
    """exec the module's top level — the heavy imports live inside the try, not here.

    The namespace is built from the module's OWN import statements rather than a list
    kept here. A hand-written list has to be updated every time the module imports
    something new, and when it is not, the failure arrives as `NameError: name 'time' is
    not defined` inside the except arm — which the function reports as a decline. So the
    tests would go green-ish and every behavioural assertion would pass for the wrong
    reason. Adding `time` to a literal dict would have fixed today and not next time.
    """
    ns = {}
    flag = annotations.compiler_flag
    tree = ast.parse(_source(MODULE))
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.Assign)):
            exec(compile(ast.Module(body=[node], type_ignores=[]), MODULE, "exec", flags=flag), ns)  # noqa: S102
    assert "absorb_dev_split" in ns, "absorb_dev_split is not defined at module scope"
    return ns["absorb_dev_split"]


def _fingerprint(path):
    """Everything about the directory that a caller could notice changing."""
    if not os.path.isdir(path):
        return None
    h = hashlib.sha256()
    for root, dirs, files in os.walk(path):
        dirs.sort()
        for name in sorted(files):
            full = os.path.join(root, name)
            h.update(os.path.relpath(full, path).encode())
            with open(full, "rb") as fh:
                h.update(fh.read())
    return h.hexdigest()


@pytest.fixture
def submission(tmp_path):
    d = tmp_path / "submission"
    d.mkdir()
    (d / "config.json").write_text(json.dumps({"architectures": ["LlamaForCausalLM"]}))
    (d / "model.safetensors").write_bytes(b"original weights, must survive")
    (d / "tokenizer.json").write_text("{}")
    return str(d)


def _dev(tmp_path, rows):
    p = tmp_path / "dev_tokenized.json"
    if rows is None:
        return str(p)  # deliberately not created
    if isinstance(rows, str):
        p.write_text(rows)
    else:
        p.write_text(json.dumps([{"input_ids": [1, 2, 3], "labels": [1, 2, 3]}] * rows))
    return str(p)


def _call(absorb, submission, dev, **kw):
    """Returns (result, messages).

    The messages matter more than the result here. Removing any guard makes execution
    fall through to `import torch`, which is absent on a dev machine, so the except arm
    returns None too — a test that only checked the return value passed against four
    separate mutations that deleted the guards outright. Asserting WHICH decline fired
    is what makes them testable at all.
    """
    messages = []
    kw.pop("log", None)
    got = absorb(submission_dir=submission, dev_tokenized_path=dev,
                 base_lr=kw.pop("base_lr", 1e-4),
                 log=lambda *a, **k: messages.append(" ".join(map(str, a))), **kw)
    return got, " ".join(messages)


# --- every decline path, and the submission survives all of them ------------------


def test_missing_submission_declines(absorb, tmp_path):
    got, log = _call(absorb, str(tmp_path / "nope"), _dev(tmp_path, 64))
    assert got is None
    assert "no submission directory" in log


def test_missing_dev_split_declines(absorb, tmp_path, submission):
    before = _fingerprint(submission)
    got, log = _call(absorb, submission, _dev(tmp_path, None))
    assert got is None and "no dev split at" in log
    assert _fingerprint(submission) == before


def test_a_lora_adapter_submission_declines_before_anything_is_read(absorb, tmp_path):
    """The inference load path trains nothing and re-serialises the adapter, so an
    adapter directory is declined outright — ahead of the dev-split read, so that this
    torch-free harness can exercise it, and so that on a 35-71B task nothing is loaded.
    The mechanism itself is pinned with real peft in
    tests/test_absorption_declines_lora_adapters.py."""
    d = tmp_path / "submission"
    d.mkdir()
    (d / "adapter_config.json").write_text(json.dumps({"peft_type": "LORA", "r": 16}))
    (d / "adapter_model.safetensors").write_bytes(b"fp32 adapter, must survive")
    (d / "tokenizer.json").write_text("{}")
    before = _fingerprint(str(d))
    got, log = _call(absorb, str(d), _dev(tmp_path, None))  # dev split deliberately absent
    assert got is None and "LoRA adapter" in log and "untouched" in log, log
    assert "no dev split" not in log, "the adapter guard must fire before the dev-split read"
    assert _fingerprint(str(d)) == before


def test_unparseable_dev_split_declines(absorb, tmp_path, submission):
    before = _fingerprint(submission)
    got, log = _call(absorb, submission, _dev(tmp_path, "{not json"))
    assert got is None and "will not parse" in log
    assert _fingerprint(submission) == before


@pytest.mark.parametrize("rows", [0, 1, 7])
def test_a_dev_split_too_small_declines(absorb, tmp_path, submission, rows):
    """A handful of rows cannot be worth perturbing a selected checkpoint for."""
    before = _fingerprint(submission)
    got, log = _call(absorb, submission, _dev(tmp_path, rows))
    assert got is None and "under the" in log and "floor" in log
    assert _fingerprint(submission) == before


def test_a_non_list_dev_split_declines(absorb, tmp_path, submission):
    before = _fingerprint(submission)
    got, log = _call(absorb, submission, _dev(tmp_path, '{"rows": 100}'))
    assert got is None and "floor" in log
    assert _fingerprint(submission) == before


@pytest.mark.parametrize("base_lr,min_rate", [(0.0, 0.1), (1e-4, 0.0), (-1e-4, 0.1)])
def test_a_non_positive_learning_rate_declines(absorb, tmp_path, submission, base_lr, min_rate):
    """lr=0 would be a no-op that still rewrites the weights file for nothing."""
    before = _fingerprint(submission)
    messages = []
    got = absorb(submission_dir=submission, dev_tokenized_path=_dev(tmp_path, 64),
                 base_lr=base_lr, min_lr_rate=min_rate,
                 log=lambda *a, **k: messages.append(" ".join(map(str, a))))
    assert got is None
    assert "is not positive" in " ".join(messages), " ".join(messages)
    assert _fingerprint(submission) == before


def test_torch_absent_is_a_decline_not_a_crash(absorb, tmp_path, submission):
    """The import sits inside the try precisely so a missing extra cannot cost a run."""
    before = _fingerprint(submission)
    got, log = _call(absorb, submission, _dev(tmp_path, 64))
    assert got is None and "failed (" in log, log
    assert _fingerprint(submission) == before


def test_no_staging_directory_is_left_behind(absorb, tmp_path, submission):
    """A crash mid-write must not leave a half-model beside the real one."""
    _call(absorb, submission, _dev(tmp_path, 64))
    siblings = os.listdir(os.path.dirname(submission))
    assert not [s for s in siblings if s.endswith((".absorbing", ".preabsorb"))], siblings


# --- the guard values themselves --------------------------------------------------


def test_the_row_floor_is_stated_not_inlined():
    tree = ast.parse(_source(MODULE))
    names = {
        t.id
        for n in tree.body if isinstance(n, ast.Assign)
        for t in n.targets if isinstance(t, ast.Name)
    }
    assert "MIN_ROWS" in names, "the row floor is a magic number rather than a named constant"


def test_only_weight_files_are_replaced():
    """Tokeniser and config files come from the selected submission, not regenerated."""
    src = _source(MODULE)
    assert "safetensors" in src and ".bin" in src
    tree = ast.parse(src)
    assert any(
        isinstance(n, ast.FunctionDef) and n.name == "_weights_only" for n in tree.body
    ), "no predicate distinguishing weight files from the rest"


# --- and it must be wired, gated, and off by default ------------------------------


def test_the_trainer_calls_it():
    """A correct mechanism nobody calls is the defect class this repo keeps paying for."""
    tree = ast.parse(_source(TRAINER))
    called = [
        n for n in ast.walk(tree)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
        and n.func.id == "absorb_dev_split"
    ]
    assert called, "absorb_dev_split is never called from text_trainer"


def test_it_is_gated_and_defaults_on():
    """It shipped off, and it is on now because two tasks measured it, not one.

        28c9f3bb   -0.0194 at r=0.10
        3a6658eb   -0.0052 at r=0.10, the a-priori default winning outright

    Both above the 0.0003 noise floor taken from two identically-configured arms, with a
    seen-rows control separating in each. The ON branch has also been run end to end
    through the real trainer, not just the module: dev split found, base_lr read from the
    train command, guard armed and passed, submission swapped, model reloaded with zero
    non-finite tensors. The gate stays so a run can still be bisected against it.
    """
    tree = ast.parse(_source(TRAINER))
    envs = {
        (n.args[0].value, n.args[1].value if len(n.args) > 1 and isinstance(n.args[1], ast.Constant) else None)
        for n in ast.walk(tree)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
        and n.func.attr == "getenv" and n.args and isinstance(n.args[0], ast.Constant)
    }
    found = [d for name, d in envs if name == "DEV_ABSORPTION"]
    assert found, "DEV_ABSORPTION gate is absent"
    assert found[0] == "1", (
        f"the gate defaults to {found[0]!r}; it is measured on two tasks now, and a "
        f"default of 0 means no run ever gets the gain"
    )


def test_it_runs_only_after_a_successful_train():
    """Absorbing into the noise fallback would put dev data in a submission that failed."""
    src = _source(TRAINER)
    i = src.index("DEV_ABSORPTION")
    window = src[max(0, i - 200): i]
    assert "train_success" in window, (
        "the gate is not conditioned on train_success, so it could fire on a failed run"
    )


# --- the path that actually touches the submission ---------------------------------
#
# Everything above stops at `import torch`, which is absent here. That left the swap
# itself — the only code that writes to the artefact we get scored on — completely
# unexercised, and it let a mutation deleting the staging cleanup pass untouched: the
# import failed before `copytree` had created anything to clean up. Standing in a torch
# lets the whole function run on any machine, success path included.


class _Loss:
    def __init__(self, v):
        self.v = v

    def backward(self):
        pass

    def __float__(self):
        return self.v


class _FakeModel:
    def __init__(self, loss=2.0, on_save=None, delay=0.0):
        self.loss, self.on_save, self.delay = loss, on_save, delay
        self.config = self
        self.pad_token_id, self.eos_token_id = 0, 0
        self.saved = []

    def to(self, device):
        return self

    def train(self):
        pass

    def gradient_checkpointing_enable(self):
        pass

    def parameters(self):
        return []

    def __call__(self, **kw):
        if self.delay:
            import time as _t
            _t.sleep(self.delay)  # lets a test drive the clock guard
        return type("Out", (), {"loss": _Loss(self.loss)})()

    def save_pretrained(self, d, safe_serialization=None, **kw):
        if safe_serialization is None:  # config.save_pretrained
            return
        if self.on_save:
            self.on_save(d)
        with open(os.path.join(d, "model.safetensors"), "wb") as fh:
            fh.write(b"absorbed weights")
        self.saved.append(d)


@pytest.fixture
def stack(monkeypatch):
    """A torch/transformers pair thin enough to drive absorb_dev_split end to end."""
    import sys
    import types

    handle = types.SimpleNamespace(model=_FakeModel(), emptied=False)

    torch = types.ModuleType("torch")
    torch.bfloat16 = "bf16"
    torch.tensor = lambda x, device=None: x
    torch.cuda = types.SimpleNamespace(
        is_available=lambda: False,
        empty_cache=lambda: setattr(handle, "emptied", True),
    )
    torch.optim = types.SimpleNamespace(
        AdamW=lambda p, lr: types.SimpleNamespace(
            step=lambda: None, zero_grad=lambda **k: None
        )
    )
    torch.nn = types.SimpleNamespace(
        utils=types.SimpleNamespace(clip_grad_norm_=lambda p, n: None)
    )

    data = types.ModuleType("torch.utils.data")

    def _loader(rows, batch_size=1, shuffle=False, collate_fn=None):
        return [collate_fn(rows[i:i + batch_size]) for i in range(0, len(rows), batch_size)]

    data.DataLoader = _loader
    torch.utils = types.SimpleNamespace(data=data)

    tf = types.ModuleType("transformers")
    tf.AutoModelForCausalLM = types.SimpleNamespace(
        from_pretrained=lambda d, **kw: handle.model
    )

    for name, mod in (("torch", torch), ("torch.utils", torch.utils),
                      ("torch.utils.data", data), ("transformers", tf)):
        monkeypatch.setitem(sys.modules, name, mod)
    return handle


def test_the_success_path_swaps_in_the_absorbed_weights(absorb, tmp_path, submission, stack):
    got, log = _call(absorb, submission, _dev(tmp_path, 64))
    assert got is not None, log
    assert got["steps"] == 64 and got["rows"] == 64
    assert got["lr"] == pytest.approx(1e-5)  # base 1e-4 x default min_lr_rate 0.1
    with open(os.path.join(submission, "model.safetensors"), "rb") as fh:
        assert fh.read() == b"absorbed weights"


def test_the_success_path_keeps_the_tokeniser_and_config(absorb, tmp_path, submission, stack):
    """The submission needs its tokeniser to load; absorption replaces weights only."""
    assert _call(absorb, submission, _dev(tmp_path, 16))[0] is not None
    assert os.path.isfile(os.path.join(submission, "tokenizer.json"))
    assert os.path.isfile(os.path.join(submission, "config.json"))


def test_nothing_is_left_beside_the_submission_on_success(absorb, tmp_path, submission, stack):
    _call(absorb, submission, _dev(tmp_path, 16))
    siblings = os.listdir(os.path.dirname(submission))
    assert not [s for s in siblings if s.endswith((".absorbing", ".preabsorb"))], siblings


def test_a_failure_after_staging_cleans_up_and_leaves_the_submission(absorb, tmp_path,
                                                                     submission, stack):
    """The staging directory exists by this point, so the cleanup arm is really run."""
    stack.model = _FakeModel(on_save=lambda d: (_ for _ in ()).throw(OSError("disk full")))
    before = _fingerprint(submission)
    got, log = _call(absorb, submission, _dev(tmp_path, 16))
    assert got is None and "disk full" in log
    assert _fingerprint(submission) == before
    siblings = os.listdir(os.path.dirname(submission))
    assert not [s for s in siblings if s.endswith((".absorbing", ".preabsorb"))], siblings


def test_a_nan_loss_declines_rather_than_shipping_it(absorb, tmp_path, submission, stack):
    """A diverged pass must not be swapped in — there is no eval left to catch it."""
    stack.model = _FakeModel(loss=float("nan"))
    before = _fingerprint(submission)
    got, log = _call(absorb, submission, _dev(tmp_path, 16))
    assert got is None and "untouched" in log
    assert _fingerprint(submission) == before


def _sharded_submission(tmp_path):
    """A submission in the shape every model large enough to shard arrives in."""
    d = tmp_path / "submission"
    d.mkdir()
    (d / "config.json").write_text(json.dumps({"architectures": ["LlamaForCausalLM"]}))
    (d / "tokenizer.json").write_text("{}")
    (d / "model-00001-of-00002.safetensors").write_bytes(b"shard one")
    (d / "model-00002-of-00002.safetensors").write_bytes(b"shard two")
    (d / "model.safetensors.index.json").write_text(json.dumps({
        "metadata": {"total_size": 18},
        "weight_map": {
            "model.embed_tokens.weight": "model-00001-of-00002.safetensors",
            "lm_head.weight": "model-00002-of-00002.safetensors",
        },
    }))
    return str(d)


def test_a_sharded_submission_does_not_keep_an_index_naming_deleted_shards(
        absorb, tmp_path, stack):
    """The forfeit shape: absorption re-serialises to ONE file where the checkpoint
    it replaces was sharded.

    save_pretrained writes no index in that case, so an index left over from the
    previous layout survives the swap and names shards that were just deleted.
    from_pretrained prefers the index whenever it is present, so the submission does
    not load at all — a zero, not a worse score. Nothing in the 2.6B/360M round-1
    draw could surface it; the boss round's 35-71B task guarantees it.

    The champion avoids this from the other side: dev_pass.py stages into an empty
    directory and copies only NON-weight files across, and its _is_weight_file lists
    the index for exactly this reason (dev_pass.py:154-157).
    """
    sub = _sharded_submission(tmp_path)
    got, log = _call(absorb, sub, _dev(tmp_path, 16))
    assert got is not None, log

    left = set(os.listdir(sub))
    assert "model.safetensors" in left, left
    assert not [n for n in left if n.startswith("model-0000")], (
        f"pre-absorption shards survived: {sorted(left)}"
    )
    assert "model.safetensors.index.json" not in left, (
        "a stale shard index survived the swap; it names shards that no longer exist, "
        "so from_pretrained will fail on this submission"
    )


def test_the_bin_shard_index_is_cleared_too(absorb, tmp_path, stack):
    """Same defect, .bin serialisation. The champion's predicate misses this one;
    ours covers it because our shape deletes rather than selectively copies."""
    d = tmp_path / "submission"
    d.mkdir()
    (d / "config.json").write_text(json.dumps({"architectures": ["LlamaForCausalLM"]}))
    (d / "pytorch_model-00001-of-00002.bin").write_bytes(b"shard one")
    (d / "pytorch_model.bin.index.json").write_text(json.dumps({"weight_map": {}}))
    got, log = _call(absorb, str(d), _dev(tmp_path, 16))
    assert got is not None, log
    left = set(os.listdir(str(d)))
    assert "pytorch_model.bin.index.json" not in left, sorted(left)


def test_the_weights_written_check_still_rejects_an_index_alone(absorb, tmp_path, stack):
    """The stale-artefact predicate must not be folded into _weights_only.

    _weights_only also answers "did save_pretrained actually write weights". If the
    index counted as weights, a save that produced nothing but an index would pass
    that check and ship a submission with no model in it.
    """
    src = _source(MODULE)
    tree = ast.parse(src)
    names = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
    assert {"_weights_only", "_stale_weight_artefact"} <= names, names

    ns = {}
    exec(compile(ast.Module(
        body=[n for n in tree.body
              if isinstance(n, ast.FunctionDef) and n.name in
              ("_weights_only", "_stale_weight_artefact")],
        type_ignores=[]), "<dev_absorption>", "exec"), ns)
    assert ns["_weights_only"]("model.safetensors.index.json") is False
    assert ns["_stale_weight_artefact"]("model.safetensors.index.json") is True
    assert ns["_weights_only"]("model.safetensors") is True
    assert ns["_stale_weight_artefact"]("model.safetensors") is True


def test_a_staged_directory_without_weights_is_refused(absorb, tmp_path, submission, stack):
    """save_pretrained can return quietly having written nothing; that is not a success."""
    quiet = _FakeModel()
    quiet.save_pretrained = lambda d, safe_serialization=None, **kw: None
    stack.model = quiet
    before = _fingerprint(submission)
    got, log = _call(absorb, submission, _dev(tmp_path, 16))
    assert got is None and "no weights" in log
    assert _fingerprint(submission) == before


def test_the_dev_rows_are_all_visited_once(absorb, tmp_path, submission, stack):
    """One epoch means one epoch — not a fraction, and not a second training run."""
    got, _ = _call(absorb, submission, _dev(tmp_path, 40), batch_size=4)
    assert got["steps"] == 10, got


def test_min_lr_rate_actually_scales_the_learning_rate(absorb, tmp_path, submission, stack):
    got, _ = _call(absorb, submission, _dev(tmp_path, 16), base_lr=2e-4, min_lr_rate=0.25)
    assert got["lr"] == pytest.approx(5e-5)


def test_the_cache_is_released_afterwards(absorb, tmp_path, submission, stack):
    """This runs while the next task may already be waiting for the GPU."""
    _call(absorb, submission, _dev(tmp_path, 16))
    assert stack.emptied


# --- the guard that came out of the measurement ------------------------------------
#
# Measured on 28c9f3bb: prior dev loss 1.7893; the rates that improved the held-out score
# ran at 1.7694 and 1.7739, the rates that hurt it at 1.8664 and 2.6956. The pass's own
# loss separates them without consulting anything held out, so it is the guard.


def _with_prior(submission, value, as_state=False):
    if as_state:
        if os.path.isfile(os.path.join(submission, "loss.txt")):
            os.remove(os.path.join(submission, "loss.txt"))
        with open(os.path.join(submission, "trainer_state.json"), "w") as fh:
            json.dump({"log_history": [{"eval_loss": 9.9}, {"eval_loss": value}]}, fh)
    else:
        with open(os.path.join(submission, "loss.txt"), "w") as fh:
            fh.write(f"346,{value}")
    return submission


@pytest.fixture
def scored(submission):
    return _with_prior(submission, 1.7893)


def test_a_pass_hotter_than_the_checkpoint_is_refused(absorb, tmp_path, scored, stack):
    """min_lr_rate 0.2 measured 1.8664 against a prior of 1.7893 and lost 0.072."""
    stack.model = _FakeModel(loss=1.8664)
    before = _fingerprint(scored)
    got, log = _call(absorb, scored, _dev(tmp_path, 16))
    assert got is None and "too hot" in log, log
    assert _fingerprint(scored) == before


def test_a_catastrophic_pass_is_refused(absorb, tmp_path, scored, stack):
    """min_lr_rate 0.5 measured 2.6956 and cost nearly a full nat."""
    stack.model = _FakeModel(loss=2.6956)
    got, log = _call(absorb, scored, _dev(tmp_path, 16))
    assert got is None and "too hot" in log


@pytest.mark.parametrize("passloss", [1.7694, 1.7739])
def test_the_rates_that_actually_helped_are_accepted(absorb, tmp_path, scored, stack, passloss):
    """A guard that also rejected the good arms would be worse than no guard."""
    stack.model = _FakeModel(loss=passloss)
    got, log = _call(absorb, scored, _dev(tmp_path, 16))
    assert got is not None, log
    assert got["prior_dev_loss"] == pytest.approx(1.7893)


def test_the_guard_reads_the_file_selection_reads(absorb, tmp_path, submission, stack):
    """loss.txt is what chose this checkpoint; comparing to anything else compares
    against a number that had no say in the submission."""
    ns_source = _source(MODULE)
    assert "loss.txt" in ns_source
    stack.model = _FakeModel(loss=5.0)
    got, log = _call(absorb, _with_prior(submission, 1.0), _dev(tmp_path, 16))
    assert got is None and "too hot" in log


def test_trainer_state_is_the_fallback_when_loss_txt_is_absent(absorb, tmp_path,
                                                               submission, stack):
    stack.model = _FakeModel(loss=5.0)
    got, log = _call(absorb, _with_prior(submission, 1.0, as_state=True),
                     _dev(tmp_path, 16))
    assert got is None and "too hot" in log, log


def test_an_unrecorded_prior_does_not_block_absorption(absorb, tmp_path, submission, stack):
    """No loss.txt and no trainer_state means no basis to refuse — not a refusal."""
    got, log = _call(absorb, submission, _dev(tmp_path, 16))
    assert got is not None, log
    assert got["prior_dev_loss"] is None


# --- the two formats of loss.txt ---------------------------------------------------
#
# customized_trainer writes `<step>,<eval_loss>` from its best-checkpoint path and
# `<step>,proxy=<train_loss>` from its save_only path. The first is what the guard wants.
# The second is a train-loss proxy: reading it as a number would arm the guard against
# the wrong quantity, and reading it as absent would leave the guard silently unarmed on
# exactly the runs that took the unusual path.


def test_a_proxy_prior_does_not_arm_the_guard(absorb, tmp_path, submission, stack):
    """A train-loss proxy is not comparable to a pass over dev."""
    with open(os.path.join(submission, "loss.txt"), "w") as fh:
        fh.write("21,proxy=0.4000")
    stack.model = _FakeModel(loss=5.0)  # would be refused against any real dev loss
    got, log = _call(absorb, submission, _dev(tmp_path, 16))
    assert got is not None, log
    assert got["prior_dev_loss"] is None
    assert "train-loss proxy" in log, (
        "a proxy must be named as one; falling through to the unparseable branch reaches "
        "the same verdict by treating a known format as a broken file")


def test_an_unarmed_guard_says_so(absorb, tmp_path, submission, stack):
    """Silence would leave 'guard passed' and 'guard never ran' looking identical."""
    with open(os.path.join(submission, "loss.txt"), "w") as fh:
        fh.write("21,proxy=no_eval")
    got, log = _call(absorb, submission, _dev(tmp_path, 16))
    # Not `"proxy" in log`: the unparseable branch echoes the raw file, which contains
    # the word, so that assertion passes whether or not the proxy branch exists.
    assert "guard unarmed" in log and "train-loss proxy" in log, log
    assert "unparseable" not in log, log


def test_an_unparseable_prior_is_reported_not_swallowed(absorb, tmp_path, submission, stack):
    with open(os.path.join(submission, "loss.txt"), "w") as fh:
        fh.write("this is not a loss")
    got, log = _call(absorb, submission, _dev(tmp_path, 16))
    assert "guard unarmed" in log and "unparseable" in log, log


def test_a_real_prior_still_arms_it(absorb, tmp_path, submission, stack):
    """The common path must not have been broken by handling the uncommon one."""
    with open(os.path.join(submission, "loss.txt"), "w") as fh:
        fh.write("346,1.7893")
    stack.model = _FakeModel(loss=2.5)
    got, log = _call(absorb, submission, _dev(tmp_path, 16))
    assert got is None and "too hot" in log
    assert "guard unarmed" not in log


# --- the rate the wiring actually passes -------------------------------------------
#
# The first real DEV_ABSORPTION=1 run printed `min_lr_rate 0.1` on a task whose schedule
# floor was 0.25. The wiring had been reading train_request["min_lr_rate"], a key that is
# absent from every training request we have ever written — the value lives in the train
# command's --lr_scheduler_kwargs. So the lookup could never succeed and always fell
# through to the default. Nothing in 542 tests noticed, because a lookup that always
# misses still produces a valid call.


def test_the_wiring_does_not_read_a_key_that_does_not_exist():
    """train_request has no min_lr_rate. Reading it looks like inheritance and is not."""
    tree = ast.parse(_source(TRAINER))
    for n in ast.walk(tree):
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr == "get" and n.args
                and isinstance(n.args[0], ast.Constant)
                and n.args[0].value == "min_lr_rate"):
            raise AssertionError(
                "the trainer reads min_lr_rate from a mapping again; it is not in "
                "train_request, so this can only ever return the fallback"
            )


def test_the_absorption_rate_comes_from_the_module_default():
    """The default is a measured choice, so it belongs in one place, not two.

    Inheriting the run's min_lr_rate would put absorption at the schedule's floor —
    exactly where 28c9f3bb measured a 0.071 loss and where 3a6658eb put r=0.25 behind
    r=0.10.
    """
    tree = ast.parse(_source(TRAINER))
    call = next(n for n in ast.walk(tree)
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                and n.func.id == "absorb_dev_split")
    kw = {k.arg: ast.unparse(k.value) for k in call.keywords}
    assert "DEFAULT_MIN_LR_RATE" in kw.get("min_lr_rate", ""), (
        "min_lr_rate is %s — it should fall back to the module's measured default rather "
        "than a literal repeated here" % kw.get("min_lr_rate")
    )


def test_the_rate_is_overridable_without_editing_code():
    """A measured default still needs a way to run the next A/B against it."""
    tree = ast.parse(_source(TRAINER))
    envs = {n.args[0].value for n in ast.walk(tree)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
            and n.func.attr == "getenv" and n.args
            and isinstance(n.args[0], ast.Constant)}
    assert "DEV_ABSORPTION_RATE" in envs


# --- the clock ---------------------------------------------------------------------
#
# Turning this on by default put it inside a budget it did not know about. Training stops
# 3 minutes before the validator's end_time (save_before_remaining_time=3), and that
# window has to hold the final eval, the checkpoint copy, the NaN scan and
# restore_submission_architectures. A full pass took 185s on 3a6658eb — more than the
# whole window. Being killed before the architecture restore does not cost ranks, it costs
# the submission, so absorption yields the clock rather than competing for it.


def _end_time_in(seconds):
    """The wire format is whole seconds, so a budget cannot be asked for in fractions.

    The first version of these tests asked for RESERVE_SECONDS + 0.4 and got
    RESERVE_SECONDS exactly, which reads as "no time at all" and made the clock tests
    fail against correct code. Budgets here are therefore whole seconds, and the step
    delay is what sets how many iterations fit inside one.
    """
    import datetime
    t = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=seconds)
    return t.strftime("%Y-%m-%d %H:%M:%S")


def test_no_usable_time_means_no_absorption(absorb, tmp_path, submission, stack):
    before = _fingerprint(submission)
    got, log = _call(absorb, submission, _dev(tmp_path, 64), end_time=_end_time_in(20))
    # Not the phrase "reserved for the post-training checks": the informational line
    # printed on the SUCCESS path carries those words too, so asserting on them passed
    # against a mutation that deleted this guard outright. This wording belongs to the
    # refusal alone.
    assert got is None and "s left before end_time and" in log, log
    assert _fingerprint(submission) == before


def test_a_deadline_already_passed_means_no_absorption(absorb, tmp_path, submission, stack):
    before = _fingerprint(submission)
    got, log = _call(absorb, submission, _dev(tmp_path, 64), end_time=_end_time_in(-300))
    assert got is None, log
    assert _fingerprint(submission) == before


def test_ample_time_absorbs_normally(absorb, tmp_path, submission, stack):
    got, log = _call(absorb, submission, _dev(tmp_path, 16), end_time=_end_time_in(3600))
    assert got is not None, log
    assert got["steps"] == 16


def test_an_unreadable_end_time_does_not_block(absorb, tmp_path, submission, stack):
    """A malformed clock is not a reason to skip; it is a reason to ignore the clock."""
    got, log = _call(absorb, submission, _dev(tmp_path, 16), end_time="not a timestamp")
    assert got is not None, log


def test_no_end_time_behaves_as_before(absorb, tmp_path, submission, stack):
    got, log = _call(absorb, submission, _dev(tmp_path, 16))
    assert got is not None and got["steps"] == 16, log


def test_the_pass_stops_on_the_clock_rather_than_overrunning(absorb, tmp_path, submission, stack):
    """A partial pass is fine — the rows are shuffled, so it saw a random subset."""
    stack.model = _FakeModel(delay=0.01)   # ~100-200 steps fit in the 1-2s budget
    got, log = _call(absorb, submission, _dev(tmp_path, 400),
                     end_time=_end_time_in(92))
    assert got is not None, log
    assert got["steps"] < 400, "it ran the whole epoch despite the budget"
    assert "stopped on the clock" in log, log


def test_a_pass_cut_too_short_is_discarded(absorb, tmp_path, submission, stack):
    """Two or three rows of adaptation is not worth rewriting a submission for."""
    stack.model = _FakeModel(delay=0.5)    # at most 2 steps fit, well under MIN_ROWS
    before = _fingerprint(submission)
    got, log = _call(absorb, submission, _dev(tmp_path, 400),
                     end_time=_end_time_in(91))
    assert got is None and "under the" in log, log
    assert _fingerprint(submission) == before


def test_the_reserve_is_named_and_large_enough_to_matter():
    tree = ast.parse(_source(MODULE))
    vals = {t.id: n.value.value
            for n in tree.body if isinstance(n, ast.Assign)
            for t in n.targets
            if isinstance(t, ast.Name) and isinstance(n.value, ast.Constant)}
    assert "RESERVE_SECONDS" in vals, "the reserve is inlined rather than named"
    assert vals["RESERVE_SECONDS"] >= 60, (
        "a reserve of %ss leaves too little for the NaN scan and the architecture "
        "restore, and the restore is what keeps the submission valid" % vals["RESERVE_SECONDS"]
    )


def test_the_trainer_hands_over_the_deadline():
    """The module cannot yield a clock it was never shown."""
    tree = ast.parse(_source(TRAINER))
    call = next(n for n in ast.walk(tree)
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                and n.func.id == "absorb_dev_split")
    kw = {k.arg: ast.unparse(k.value) for k in call.keywords}
    assert "end_time" in kw, "absorb_dev_split is called without end_time"
    assert "end_time" in kw["end_time"], kw["end_time"]
