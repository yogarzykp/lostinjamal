"""d91101f on a REAL sharded checkpoint: torch 2.14 CPU, transformers 4.51.3, safetensors.

tests/test_dev_absorption.py proves the staging-clear predicate on a fake stack whose
save_pretrained is a lambda writing bytes. That cannot answer the three questions that
decide what the commit is worth: does a real save_pretrained really leave the old index
behind, does a real from_pretrained really refuse the result, and can our own pipeline
ever produce the layout change the defect needs. This file drives the real thing.

What every test here uses: a random-init LlamaForCausalLM (24,736 params, 49,472 bytes
in bf16), saved sharded by the real save_pretrained with a tiny max_shard_size so the
directory holds a genuine model.safetensors.index.json; a real tokenizer (WordLevel,
saved by PreTrainedTokenizerFast); a dev_tokenized json in the row schema
absorb_dev_split reads (dev_absorption.py:209-221: `input_ids`, optional `labels`); a
loss.txt in the `<step>,<eval_loss>` shape customized_trainer.on_save writes
(customized_trainer.py:977-978), so the too-hot guard (dev_absorption.py:278-286) is
ARMED and passes on the measured number rather than being silently unarmed.

Measured, HEAD vs `git show 12b16b5:scripts/dev_absorption.py`:

    scenario                                 12b16b5                     HEAD
    ---------------------------------------  --------------------------  ---------------
    3 shards in (20KB), 5GB default out      model.safetensors + STALE   model.safetensors,
                                             index naming 3 deleted      no index
                                             shards
    from_pretrained on that result           LOADS (absorbed weights)    LOADS
    real Trainer bf16 ckpt -> absorb, 20KB   3 shards -> 3 shards,       identical
                                             identical weight_map,
                                             index rewritten, no stale
    real Trainer FP32 ckpt -> absorb, 60KB   2 shards -> 1 file, STALE   1 file, clean
                                             index

Two facts follow, and the second is the one the commit message gets wrong.

1. The stale index is real and d91101f removes it (test 1, test 4 fail on 12b16b5).

2. It is not a forfeit. transformers resolves a local directory by checking
   model.safetensors BEFORE model.safetensors.index.json (4.51.3
   modeling_utils._get_resolved_checkpoint_files: SAFE_WEIGHTS_NAME at the `elif`
   before SAFE_WEIGHTS_INDEX_NAME; the hub branch tries SAFE_WEIGHTS_NAME first and
   falls back to the index only when that file is absent). The validator's evaluator
   runs transformers 5.12.x and its _get_resolved_checkpoint_files has the same order.
   So "from_pretrained prefers the index whenever it is present" is false on both
   stacks, and test 2 pins the fact: a stale index beside model.safetensors is inert.
   If that test ever fails after a transformers upgrade, the hygiene in d91101f has
   become load-bearing.

And the layout question (test 3, test 4): both sides use the same policy. The Trainer
saves bf16 weights at save_pretrained's default max_shard_size (trainer.py `_save`:
`self.model.save_pretrained(output_dir, state_dict=state_dict,
safe_serialization=self.args.save_safetensors)`, no max_shard_size; the model is loaded
bf16 at train_instruct.py:131,203 / train_dpo.py:265 / train_grpo.py:403);
customized_trainer.on_save copies that checkpoint directory verbatim (971-974);
absorb_dev_split reloads bf16 (dev_absorption.py:201-203) and saves at the same default
(298). Same dtype, same key set, same boundary -> the same shards, measured to the
weight_map. The only way the layouts diverge is a dtype or key-set change between the
two saves; test 4 constructs the dtype one (fp32 checkpoint, bf16 reload) and that is
where the stale index appears. Our trainers never save fp32, so on the 1xH100 path D8
cannot fire on our own artefacts: gemma-2-2b (5.23e9 bytes bf16 > the 5e9 boundary) is
2 shards in and 2 shards out, SmolLM2-360M (7.2e8) is one file both ways.

Running against 12b16b5 — point DEV_ABSORPTION_UNDER_TEST at that commit's file:

    mkdir -p /tmp/old && git show 12b16b5:scripts/dev_absorption.py > /tmp/old/dev_absorption.py
    DEV_ABSORPTION_UNDER_TEST=/tmp/old/dev_absorption.py .venv-cpu-pinned/bin/python -m pytest \
      tests/test_absorption_on_a_real_sharded_model.py -p no:cacheprovider

Tests 1 and 4 fail that way. The other three guard properties that are not code changes,
so each carries a deliberate mutation, selected with ABSORB_TEST_MUTATION:

    drop_single_file    test 2: remove model.safetensors so the loader falls through to
                        the stale index -> from_pretrained raises
    fp32_checkpoint     test 3: the Trainer side saves fp32 -> the layouts diverge
    widen_weights_only  test 5: fold the index into _weights_only (the alternative fix
                        the commit rejected) -> an index-only save passes the guard and
                        the swap ships a submission with no weights
"""

from __future__ import annotations

import hashlib
import importlib.machinery
import importlib.util
import inspect
import json
import os
import random
import shutil
import sys
import types

import pytest

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MODULE = os.environ.get("DEV_ABSORPTION_UNDER_TEST") or os.path.join(
    _REPO, "scripts", "dev_absorption.py"
)
_MUTATION = os.environ.get("ABSORB_TEST_MUTATION", "")

# transformers probes integrations with importlib.util.find_spec("wandb"), which raises
# on a spec-less stub left in sys.modules by an earlier test file. The real package is
# installed in the pinned env but slow to import; a stub with a spec keeps it out.
_wandb = sys.modules.setdefault("wandb", types.ModuleType("wandb"))
if getattr(_wandb, "__spec__", None) is None:
    _wandb.__spec__ = importlib.machinery.ModuleSpec("wandb", None)

import torch  # noqa: E402
from safetensors import safe_open  # noqa: E402
from tokenizers import Tokenizer, models, pre_tokenizers  # noqa: E402
from torch.utils.data import Dataset  # noqa: E402
from transformers import (  # noqa: E402
    AutoModelForCausalLM,
    LlamaConfig,
    LlamaForCausalLM,
    PreTrainedModel,
    PreTrainedTokenizerFast,
    Trainer,
    TrainingArguments,
    default_data_collator,
)

INDEX = "model.safetensors.index.json"
SINGLE = "model.safetensors"
FAR_FUTURE = "2099-01-01 00:00:00"
VOCAB = 64
WIDTH = 24  # every dev row padded to this for the Trainer's default collator


@pytest.fixture
def absorb_module():
    """The real dev_absorption module, from the repo or from DEV_ABSORPTION_UNDER_TEST.

    Loaded under its own name so a `dev_absorption` imported by another test file can
    never shadow the copy this file was told to test.
    """
    spec = importlib.util.spec_from_file_location("dev_absorption_real_sharded", _MODULE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _tiny_config():
    return LlamaConfig(
        vocab_size=VOCAB, hidden_size=32, intermediate_size=64, num_hidden_layers=2,
        num_attention_heads=4, num_key_value_heads=4, max_position_embeddings=64,
        tie_word_embeddings=False, pad_token_id=0, bos_token_id=1, eos_token_id=2,
    )


def _tiny_model(dtype=torch.bfloat16):
    torch.manual_seed(0)
    return LlamaForCausalLM(_tiny_config()).to(dtype)


def _save_tokenizer(directory):
    """A real tokenizer.json / tokenizer_config.json / special_tokens_map.json."""
    vocab = {f"<{i}>": i for i in range(VOCAB)}
    vocab.update({"<pad>": 0, "<s>": 1, "</s>": 2})
    tok = Tokenizer(models.WordLevel(vocab=vocab, unk_token="<3>"))
    tok.pre_tokenizer = pre_tokenizers.Whitespace()
    PreTrainedTokenizerFast(
        tokenizer_object=tok, pad_token="<pad>", bos_token="<s>", eos_token="</s>",
        unk_token="<3>",
    ).save_pretrained(directory)


def _dev_rows(n=12):
    """The schema absorb_dev_split reads: input_ids, and labels alongside (209-221)."""
    rng = random.Random(0)
    rows = []
    for _ in range(n):
        ids = [1] + [rng.randint(3, VOCAB - 1) for _ in range(rng.randint(6, WIDTH - 4))] + [2]
        rows.append({"input_ids": ids, "labels": list(ids)})
    return rows


def _write_dev(tmp_path, rows):
    path = tmp_path / "dev_tokenized.json"
    path.write_text(json.dumps(rows), encoding="utf-8")
    return str(path)


def _mean_loss(model, rows):
    model.eval()
    with torch.no_grad():
        losses = []
        for r in rows:
            ids = torch.tensor([r["input_ids"]])
            losses.append(float(model(input_ids=ids, labels=ids).loss))
    return sum(losses) / len(losses)


def _arm_guard(submission, prior):
    """loss.txt in on_save's best-checkpoint shape, one nat above the measured dev loss.

    At lr = base_lr x 0.1 the pass cannot move the loss by anything like a nat, so the
    guard is armed, reads a number in the right format, and passes on the merits.
    """
    with open(os.path.join(submission, "loss.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"7,{prior + 1.0}")


def _layout(directory):
    """(sorted weight files, index weight_map or None) — what a loader sees."""
    files = sorted(f for f in os.listdir(directory) if f.endswith(".safetensors"))
    index = os.path.join(directory, INDEX)
    weight_map = None
    if os.path.isfile(index):
        with open(index, "r", encoding="utf-8") as fh:
            weight_map = json.load(fh)["weight_map"]
    return files, weight_map


def _dangling(directory):
    """Shards named by an index in this directory that do not exist in it."""
    _, weight_map = _layout(directory)
    if weight_map is None:
        return []
    return sorted({f for f in set(weight_map.values())
                   if not os.path.isfile(os.path.join(directory, f))})


def _tensors(directory):
    out = {}
    for name in sorted(os.listdir(directory)):
        if name.endswith(".safetensors"):
            with safe_open(os.path.join(directory, name), "pt") as fh:
                for key in fh.keys():
                    out[key] = fh.get_tensor(key).clone()
    return out


def _fingerprint(directory):
    h = hashlib.sha256()
    for root, dirs, files in os.walk(directory):
        dirs.sort()
        for name in sorted(files):
            full = os.path.join(root, name)
            h.update(os.path.relpath(full, directory).encode())
            with open(full, "rb") as fh:
                h.update(fh.read())
    return h.hexdigest()


def _absorb(mod, submission, dev_path, log):
    return mod.absorb_dev_split(
        submission_dir=submission, dev_tokenized_path=dev_path, base_lr=1e-3,
        end_time=FAR_FUTURE, log=log.append,
    )


@pytest.fixture
def shard_boundary(monkeypatch):
    """Scale save_pretrained's DEFAULT max_shard_size down to what a 49KB model can cross.

    This is the one departure from the real thing, and it is a scale factor, not a
    fake: both the Trainer's save (trainer.py _save passes no max_shard_size) and
    absorption's (dev_absorption.py:298 passes none) fall through to the same default,
    so patching that default keeps the property under test — one policy on both sides
    — and only moves the 5e9-byte boundary to where the tiny model can straddle it.
    Callers that pass max_shard_size explicitly are untouched.
    """
    original = PreTrainedModel.save_pretrained

    def set_to(boundary):
        def patched(self, save_directory, *args, **kwargs):
            kwargs.setdefault("max_shard_size", boundary)
            return original(self, save_directory, *args, **kwargs)
        monkeypatch.setattr(PreTrainedModel, "save_pretrained", patched)

    return set_to


class _Rows(Dataset):
    def __init__(self, rows):
        self.rows = rows

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, i):
        ids = self.rows[i]["input_ids"]
        pad = WIDTH - len(ids)
        return {
            "input_ids": torch.tensor(ids + [0] * pad),
            "labels": torch.tensor(ids + [-100] * pad),
            "attention_mask": torch.tensor([1] * len(ids) + [0] * pad),
        }


def _trainer_checkpoint(tmp_path, rows, dtype):
    """What customized_trainer.on_save finds on disk: the real Trainer's checkpoint dir."""
    model = _tiny_model(dtype)
    out = str(tmp_path / "outputs")
    args = TrainingArguments(
        output_dir=out, max_steps=2, save_steps=2, save_strategy="steps",
        per_device_train_batch_size=2, report_to=[], use_cpu=True, learning_rate=1e-3,
        logging_steps=1, seed=0,
        # save_safetensors is left at its default (True), as it is in instruct_config.py.
    )
    Trainer(model=model, args=args, train_dataset=_Rows(rows),
            data_collator=default_data_collator).train()
    ckpt = os.path.join(out, "checkpoint-2")
    assert os.path.isdir(ckpt)
    return ckpt


def _promote_like_on_save(ckpt, submission):
    """customized_trainer.on_save:966-978 — verbatim copytree, then loss.txt."""
    if os.path.exists(submission):
        shutil.rmtree(submission)
    shutil.copytree(ckpt, submission)
    with open(os.path.join(submission, "loss.txt"), "w", encoding="utf-8") as fh:
        fh.write("2,99.0")


# ── 1. the defect and the fix, on real files ─────────────────────────────────────────


def test_sharded_in_single_out_leaves_no_index_naming_deleted_shards(absorb_module, tmp_path):
    """Fails on 12b16b5: the old predicate leaves model.safetensors.index.json behind,
    naming model-0000N-of-00003.safetensors files that absorption itself deleted."""
    submission = str(tmp_path / "submission")
    model = _tiny_model()
    model.save_pretrained(submission, safe_serialization=True, max_shard_size="20KB")
    _save_tokenizer(submission)
    files_in, weight_map_in = _layout(submission)
    assert weight_map_in is not None and len(files_in) == 3, (files_in, weight_map_in)
    assert set(weight_map_in.values()) == set(files_in)
    rows = _dev_rows()
    _arm_guard(submission, _mean_loss(model, rows))
    before = _tensors(submission)
    log = []

    result = _absorb(absorb_module, submission, _write_dev(tmp_path, rows), log)

    assert result is not None and result["steps"] == len(rows), log
    files_out, weight_map_out = _layout(submission)
    assert files_out == [SINGLE], files_out  # 49KB fits the 5GB default in one file
    assert _dangling(submission) == [], (
        f"index names shards that no longer exist: {_dangling(submission)}; "
        f"directory holds {sorted(os.listdir(submission))}"
    )
    assert weight_map_out is None, "a single-file save must not leave an index at all"
    # The non-weight files rode through the copytree untouched.
    for keep in ("tokenizer.json", "tokenizer_config.json", "special_tokens_map.json",
                 "config.json", "loss.txt"):
        assert os.path.isfile(os.path.join(submission, keep)), keep
    # And the file holds absorbed weights, not a copy of the input.
    after = _tensors(submission)
    assert set(after) == set(before)
    changed = [k for k in before if not torch.equal(before[k], after[k])]
    assert changed, "absorption wrote the input weights back unchanged"
    assert not os.path.isdir(submission + ".absorbing")
    assert not os.path.isdir(submission + ".preabsorb")


# ── 2. what the loader actually does with a stale index ──────────────────────────────


def test_a_stale_index_beside_a_single_file_is_ignored_by_this_transformers(tmp_path):
    """The commit's rationale, tested: "from_pretrained prefers the index whenever it is
    present, so the submission does not load at all". It does not — model.safetensors is
    resolved first (modeling_utils._get_resolved_checkpoint_files, 4.51.3), and the same
    order holds in the validator's transformers 5.12.x. Mutation drop_single_file removes
    model.safetensors so resolution falls through to the stale index and raises."""
    submission = str(tmp_path / "submission")
    model = _tiny_model()
    model.save_pretrained(submission, safe_serialization=True, max_shard_size="20KB")
    _save_tokenizer(submission)
    original = _tensors(submission)
    # The exact directory 12b16b5 leaves: shards deleted, index kept, single file written.
    for name in list(os.listdir(submission)):
        if name.endswith(".safetensors"):
            os.remove(os.path.join(submission, name))
    with torch.no_grad():
        for p in model.parameters():
            p.add_(0.25)  # so the single file is distinguishable from the deleted shards
    model.save_pretrained(submission, safe_serialization=True)  # default 5GB -> one file
    assert os.path.isfile(os.path.join(submission, INDEX)), "setup: the stale index"
    assert _dangling(submission) == sorted(set(_layout(submission)[1].values()))
    if _MUTATION == "drop_single_file":
        os.remove(os.path.join(submission, SINGLE))

    loaded = AutoModelForCausalLM.from_pretrained(submission, torch_dtype=torch.bfloat16)

    state = loaded.state_dict()
    single = _tensors(submission)
    for key, tensor in original.items():
        assert torch.equal(state[key], single[key]), key
        assert not torch.equal(state[key], tensor), (
            f"{key} came back as the deleted shard's value — the loader read the index"
        )


# ── 3/4. can OUR pipeline produce the layout change the defect needs? ────────────────


def test_trainer_checkpoint_and_absorbed_save_shard_identically(absorb_module, shard_boundary,
                                                                tmp_path):
    """The real Trainer's bf16 checkpoint, promoted the way on_save promotes it, then
    absorbed: same shard files, same weight_map, index rewritten in place. This is why
    the stale index cannot appear on our own artefacts — both saves use one dtype and
    one default boundary. Mutation fp32_checkpoint makes the Trainer side fp32, the
    layouts diverge, and the test fails."""
    shard_boundary("20KB")
    rows = _dev_rows()
    dtype = torch.float32 if _MUTATION == "fp32_checkpoint" else torch.bfloat16
    ckpt = _trainer_checkpoint(tmp_path, rows, dtype)
    submission = str(tmp_path / "submission")
    _promote_like_on_save(ckpt, submission)
    files_in, weight_map_in = _layout(submission)
    assert weight_map_in is not None and len(files_in) >= 3, (files_in, weight_map_in)
    log = []

    result = _absorb(absorb_module, submission, _write_dev(tmp_path, rows), log)

    assert result is not None, log
    files_out, weight_map_out = _layout(submission)
    assert files_out == files_in, (files_in, files_out)
    assert weight_map_out == weight_map_in
    assert _dangling(submission) == []
    AutoModelForCausalLM.from_pretrained(submission, torch_dtype=torch.bfloat16)


def test_dtype_divergence_is_where_the_stale_index_comes_from(absorb_module, shard_boundary,
                                                              tmp_path):
    """Fails on 12b16b5. The one condition that makes the layouts differ: the checkpoint
    on disk is bigger than its bf16 reload. An fp32 checkpoint of this model is 98,944
    bytes (2 shards at a 60KB boundary); absorption reloads it bf16 (dev_absorption.py:
    201-203), 49,472 bytes, one file, no index written — and 12b16b5 leaves the fp32
    index pointing at two deleted shards. Our trainers load bf16 (train_instruct.py:131,
    203; train_dpo.py:265; train_grpo.py:403), so this needs a code change to reach a
    real run; the test pins that the fix holds if one ever does."""
    shard_boundary("60KB")
    rows = _dev_rows()
    ckpt = _trainer_checkpoint(tmp_path, rows, torch.float32)
    submission = str(tmp_path / "submission")
    _promote_like_on_save(ckpt, submission)
    files_in, weight_map_in = _layout(submission)
    assert len(files_in) == 2 and weight_map_in is not None, (files_in, weight_map_in)
    log = []

    result = _absorb(absorb_module, submission, _write_dev(tmp_path, rows), log)

    assert result is not None, log
    files_out, _ = _layout(submission)
    assert files_out == [SINGLE], files_out
    assert _dangling(submission) == [], (
        f"stale fp32 index survived the bf16 re-save: {_dangling(submission)}"
    )
    loaded = AutoModelForCausalLM.from_pretrained(submission, torch_dtype=torch.bfloat16)
    assert loaded.dtype == torch.bfloat16


# ── 5. _weights_only kept its second job ─────────────────────────────────────────────


def test_weights_only_unchanged_and_an_index_only_save_is_rejected(absorb_module, monkeypatch,
                                                                    tmp_path):
    """_weights_only is byte-identical to 12b16b5 and still answers "did any weights get
    written" at dev_absorption.py:300: a save_pretrained that produces nothing but an
    index (real file, injected fault) is declined, staging is removed, the submission is
    byte-for-byte untouched. Mutation widen_weights_only folds the index into
    _weights_only — the alternative fix the commit rejected — and the swap ships a
    submission with no weights in it."""
    mod = absorb_module
    src = inspect.getsource(mod._weights_only)
    assert src.strip().splitlines()[-1].strip() == (
        'return name.endswith(".safetensors") or name.endswith(".bin")'
    ), src
    for name, is_weight in (("model.safetensors", True), ("pytorch_model.bin", True),
                            ("model-00001-of-00002.safetensors", True),
                            (INDEX, False), ("pytorch_model.bin.index.json", False),
                            ("config.json", False)):
        assert mod._weights_only(name) is is_weight, name
    if hasattr(mod, "_stale_weight_artefact"):
        assert mod._stale_weight_artefact(INDEX)
        assert mod._stale_weight_artefact("pytorch_model.bin.index.json")
        assert not mod._stale_weight_artefact("config.json")
    if _MUTATION == "widen_weights_only":
        # A standalone widened predicate, not an alias of _stale_weight_artefact —
        # that one calls _weights_only and would recurse instead of widening.
        monkeypatch.setattr(mod, "_weights_only", lambda name: (
            name.endswith(".safetensors") or name.endswith(".bin")
            or name in (INDEX, "pytorch_model.bin.index.json")))

    submission = str(tmp_path / "submission")
    model = _tiny_model()
    model.save_pretrained(submission, safe_serialization=True, max_shard_size="20KB")
    _save_tokenizer(submission)
    rows = _dev_rows()
    _arm_guard(submission, _mean_loss(model, rows))
    fingerprint = _fingerprint(submission)

    def index_only_save(self, save_directory, *args, **kwargs):
        # The failure the guard exists for: an index and no shards. Real file on disk.
        with open(os.path.join(save_directory, INDEX), "w", encoding="utf-8") as fh:
            json.dump({"metadata": {}, "weight_map": {
                k: "model-00001-of-00001.safetensors" for k in self.state_dict()}}, fh)

    monkeypatch.setattr(PreTrainedModel, "save_pretrained", index_only_save)
    log = []

    result = _absorb(mod, submission, _write_dev(tmp_path, rows), log)

    assert result is None, log
    assert any("no weights" in line for line in log), log
    assert not os.path.isdir(submission + ".absorbing")
    assert not os.path.isdir(submission + ".preabsorb")
    assert _fingerprint(submission) == fingerprint, "the submission was touched"
    assert any(mod._weights_only(n) for n in os.listdir(submission))
