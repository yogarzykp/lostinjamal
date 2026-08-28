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
    """exec the function alone — the module reaches for torch only inside the try."""
    ns = {"os": os, "json": json, "shutil": __import__("shutil")}
    flag = annotations.compiler_flag
    tree = ast.parse(_source(MODULE))
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.Assign)):
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


def test_it_is_gated_and_defaults_off():
    """+0.0183 is the champion's number on the champion's stack, not ours.

    It stays off until an A/B on our own harness produces our figure — the same rule
    that governs AUG_PRUNING_LR_FACTOR and the GAUSSIAN_NOISE branch.
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
    assert found[0] == "0", f"the gate defaults to {found[0]!r}; an unmeasured action must default off"


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
    def __init__(self, loss=2.0, on_save=None):
        self.loss, self.on_save = loss, on_save
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
