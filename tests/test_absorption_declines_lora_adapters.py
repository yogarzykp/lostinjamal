"""Dev absorption must decline a LoRA adapter submission, before it touches anything.

Measured 2026-09-12 on the pinned stack (transformers 4.51.3, peft 0.15.1): loading an
adapter directory through AutoModelForCausalLM.from_pretrained attaches the adapter via
the inference-oriented PEFT path — inference_mode=true, zero trainable parameters. The
absorption pass then runs a full forward+backward over the dev set for nothing, and
save_pretrained re-serialises adapter_model.safetensors in the load dtype (bf16), so a
fp32 adapter comes out quantised. The function reports "submission updated". Nothing
improved; the artefact we are about to be scored on is degraded; the log says success.

Every instruct/chat task with use_lora=True — the >=7B size bands and the boss round's
35-71B — takes this path. None has met absorption live yet, which is the only reason it
has not cost a rank.

Three properties, real stack throughout (no fake torch, no fake transformers):

  1. The mechanism is real: an adapter dir loaded the way absorption loads it has zero
     trainable parameters. If a future transformers/peft changes that, this test says
     so and the guard can be reconsidered.
  2. The pre-fix code really does rewrite the adapter — bytes change, dtype changes,
     and it claims success. This is the defect, pinned.
  3. HEAD declines before any I/O: returns None, logs the reason and "untouched", and
     the directory is byte-for-byte what it was.

Running against the pre-fix file proves 3 can fail:

    git show e656741:scripts/dev_absorption.py > /tmp/old/dev_absorption.py
    DEV_ABSORPTION_UNDER_TEST=/tmp/old/dev_absorption.py \\
      .venv-cpu-pinned/bin/python -m pytest tests/test_absorption_declines_lora_adapters.py -q

Under the old file, test 3 fails (the adapter is rewritten) and test 2 passes — the
same measurement read from the other side. Under HEAD, test 2 is run against the old
file explicitly so the defect stays documented even after the fix.
"""

from __future__ import annotations

import hashlib
import importlib.machinery
import importlib.util
import json
import os
import random
import subprocess
import sys
import types

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
sys.path.insert(0, SCRIPTS)

_MODULE = os.environ.get("DEV_ABSORPTION_UNDER_TEST") or os.path.join(SCRIPTS, "dev_absorption.py")
PRE_FIX_COMMIT = "e656741"

# transformers probes integrations with importlib.util.find_spec("wandb"), which raises
# ValueError on a bare ModuleType stub (__spec__ is None). Give the stub a real spec.
if "wandb" not in sys.modules:
    _wandb = types.ModuleType("wandb")
    _wandb.__spec__ = importlib.machinery.ModuleSpec("wandb", None)
    sys.modules["wandb"] = _wandb

torch = pytest.importorskip("torch")
peft = pytest.importorskip("peft")
from safetensors import safe_open  # noqa: E402
from tokenizers import Tokenizer, models, pre_tokenizers  # noqa: E402
from transformers import (  # noqa: E402
    AutoModelForCausalLM,
    LlamaConfig,
    LlamaForCausalLM,
    PreTrainedTokenizerFast,
)

FAR_FUTURE = "2099-01-01 00:00:00"
VOCAB = 64


def _load(path):
    spec = importlib.util.spec_from_file_location("dev_absorption_lora_" + hashlib.md5(path.encode()).hexdigest()[:8], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def absorb_module():
    return _load(_MODULE)


@pytest.fixture
def pre_fix_module(tmp_path):
    """The file as it was before the guard, straight from git — so test 2 documents the
    defect regardless of which version DEV_ABSORPTION_UNDER_TEST points at."""
    out = tmp_path / "pre_fix_dev_absorption.py"
    src = subprocess.run(
        ["git", "-C", ROOT, "show", f"{PRE_FIX_COMMIT}:scripts/dev_absorption.py"],
        check=True, capture_output=True, text=True,
    ).stdout
    assert "_is_adapter_submission" not in src, "PRE_FIX_COMMIT already carries the guard"
    out.write_text(src, encoding="utf-8")
    return _load(str(out))


def _tiny_config():
    return LlamaConfig(
        vocab_size=VOCAB, hidden_size=32, intermediate_size=64, num_hidden_layers=2,
        num_attention_heads=4, num_key_value_heads=4, max_position_embeddings=64,
        tie_word_embeddings=False, pad_token_id=0, bos_token_id=1, eos_token_id=2,
    )


def _save_tokenizer(directory):
    vocab = {f"<{i}>": i for i in range(VOCAB)}
    vocab.update({"<pad>": 0, "<s>": 1, "</s>": 2})
    tok = Tokenizer(models.WordLevel(vocab=vocab, unk_token="<3>"))
    tok.pre_tokenizer = pre_tokenizers.Whitespace()
    PreTrainedTokenizerFast(
        tokenizer_object=tok, pad_token="<pad>", bos_token="<s>", eos_token="</s>",
        unk_token="<3>",
    ).save_pretrained(directory)


def _adapter_submission(tmp_path):
    """What on_save copies out for a use_lora=True run: a PEFT adapter directory whose
    adapter_config.json names the base by path, saved in fp32 (the trainer's LoRA
    weights are fp32 masters under bf16 autocast)."""
    base_dir = tmp_path / "base"
    torch.manual_seed(0)
    base = LlamaForCausalLM(_tiny_config()).float()
    base.save_pretrained(str(base_dir))
    _save_tokenizer(str(base_dir))

    cfg = peft.LoraConfig(r=2, lora_alpha=4, target_modules=["q_proj", "v_proj"],
                          task_type="CAUSAL_LM")
    wrapped = peft.get_peft_model(base, cfg)
    # Give the adapter non-trivial values so a rewrite is visible, not just a no-op.
    with torch.no_grad():
        for n, p in wrapped.named_parameters():
            if "lora_" in n:
                p.copy_(torch.randn_like(p) * 0.05)

    sub = tmp_path / "submission"
    wrapped.save_pretrained(str(sub))
    _save_tokenizer(str(sub))
    acfg = json.loads((sub / "adapter_config.json").read_text())
    acfg["base_model_name_or_path"] = str(base_dir)
    (sub / "adapter_config.json").write_text(json.dumps(acfg))
    (sub / "loss.txt").write_text("7,99.0")  # arms the hotness guard so it cannot be why we decline
    return str(sub)


def _dev(tmp_path, n=12):
    rng = random.Random(0)
    rows = []
    for _ in range(n):
        ids = [1] + [rng.randint(3, VOCAB - 1) for _ in range(rng.randint(6, 18))] + [2]
        rows.append({"input_ids": ids, "labels": list(ids)})
    p = tmp_path / "dev_tokenized.json"
    p.write_text(json.dumps(rows))
    return str(p)


def _fingerprint(path):
    h = hashlib.sha256()
    for root, dirs, files in os.walk(path):
        dirs.sort()
        for name in sorted(files):
            full = os.path.join(root, name)
            h.update(name.encode())
            with open(full, "rb") as fh:
                h.update(fh.read())
    return h.hexdigest()


def _adapter_tensors(sub):
    with safe_open(os.path.join(sub, "adapter_model.safetensors"), "pt") as f:
        return {k: f.get_tensor(k) for k in f.keys()}


def _absorb(mod, sub, dev, log):
    return mod.absorb_dev_split(
        submission_dir=sub, dev_tokenized_path=dev, base_lr=1e-2,
        end_time=FAR_FUTURE, log=log.append,
    )


# --- 1. the mechanism -----------------------------------------------------------------

def test_the_inference_load_path_has_no_trainable_parameters(tmp_path):
    """Why the guard exists. dev_absorption loads with AutoModelForCausalLM.from_pretrained
    on the submission dir (dev_absorption.py ~:201); on an adapter dir that attaches the
    adapter for inference. If this ever starts returning trainable params, the guard is
    worth revisiting — the feature would then just work."""
    sub = _adapter_submission(tmp_path)
    model = AutoModelForCausalLM.from_pretrained(sub, torch_dtype=torch.bfloat16)
    trainable = [n for n, p in model.named_parameters() if p.requires_grad]
    assert trainable == [], (
        f"adapter load path now yields {len(trainable)} trainable params under "
        f"transformers {__import__('transformers').__version__} / peft {peft.__version__}; "
        "absorption could train it — reconsider the LoRA guard"
    )


# --- 2. the defect, pinned against the pre-fix file ------------------------------------

def test_pre_fix_code_rewrites_the_adapter_and_calls_it_success(tmp_path, pre_fix_module):
    sub = _adapter_submission(tmp_path)
    before = _adapter_tensors(sub)
    before_bytes = os.path.getsize(os.path.join(sub, "adapter_model.safetensors"))
    log = []

    got = _absorb(pre_fix_module, sub, _dev(tmp_path), log)

    assert got is not None, "\n".join(log)
    assert any("submission updated" in m for m in log), log
    after = _adapter_tensors(sub)
    after_bytes = os.path.getsize(os.path.join(sub, "adapter_model.safetensors"))
    assert after_bytes < before_bytes, (
        f"expected the fp32 adapter to be re-serialised smaller (bf16); "
        f"{before_bytes} -> {after_bytes}"
    )
    assert any(t.dtype == torch.bfloat16 for t in after.values()), {k: t.dtype for k, t in after.items()}
    # And it learned nothing: every value is the bf16 rounding of what went in.
    for k, t in before.items():
        assert torch.equal(after[k].float(), t.to(torch.bfloat16).float()), (
            f"{k}: adapter changed by something other than bf16 rounding — "
            "either training worked (great, revisit the guard) or something else moved it"
        )


# --- 3. HEAD declines, before any I/O --------------------------------------------------

def test_head_declines_an_adapter_submission_untouched(tmp_path, absorb_module):
    sub = _adapter_submission(tmp_path)
    fp = _fingerprint(sub)
    log = []

    got = _absorb(absorb_module, sub, _dev(tmp_path), log)

    assert got is None, "\n".join(log)
    assert any("LoRA adapter" in m and "untouched" in m for m in log), log
    assert _fingerprint(sub) == fp, "an adapter submission was modified"
    siblings = os.listdir(os.path.dirname(sub))
    assert not [s for s in siblings if s.endswith((".absorbing", ".preabsorb"))], siblings


def test_the_decline_happens_before_the_dev_split_is_read(tmp_path, absorb_module, monkeypatch):
    """Cheapness matters: on a 35-71B task the load is the cost. The guard sits ahead of
    the dev-split read, so an unreadable dev path must not be what is reported."""
    sub = _adapter_submission(tmp_path)
    log = []
    got = absorb_module.absorb_dev_split(
        submission_dir=sub, dev_tokenized_path=str(tmp_path / "does_not_exist.json"),
        base_lr=1e-2, end_time=FAR_FUTURE, log=log.append,
    )
    assert got is None
    assert any("LoRA adapter" in m for m in log), log
    assert not any("no dev split" in m for m in log), log


@pytest.mark.parametrize("marker", ["adapter_config.json", "adapter_model.safetensors", "adapter_model.bin"])
def test_any_adapter_marker_is_enough(tmp_path, absorb_module, marker):
    sub = tmp_path / "submission"
    sub.mkdir()
    (sub / "config.json").write_text(json.dumps({"architectures": ["LlamaForCausalLM"]}))
    (sub / marker).write_bytes(b"x")
    assert absorb_module._is_adapter_submission(str(sub)) is True


def test_a_full_model_is_not_mistaken_for_an_adapter(tmp_path, absorb_module):
    sub = tmp_path / "submission"
    sub.mkdir()
    (sub / "config.json").write_text(json.dumps({"architectures": ["LlamaForCausalLM"]}))
    (sub / "model.safetensors").write_bytes(b"x")
    (sub / "model.safetensors.index.json").write_text("{}")
    assert absorb_module._is_adapter_submission(str(sub)) is False
