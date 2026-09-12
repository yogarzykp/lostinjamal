"""Does the ZeRO-3 `use_reentrant` decision actually reach the model?

tests/test_zero3_needs_reentrant_checkpointing.py checks the SOURCE TEXT of the
branch commit 4723787 added to train_dpo.py and train_grpo.py. This file checks the
WIRE: that the value the branch writes into `training_args.gradient_checkpointing_kwargs`
is the value `torch.utils.checkpoint.checkpoint` is called with during a real
training step of the real TRL 0.18.0 DPOTrainer / GRPOTrainer on transformers 4.51.3.

Why the wire is the thing to test here (all line numbers are the pinned venv):

  * transformers/trainer.py:2344-2345 — `_inner_training_loop` re-applies
    `args.gradient_checkpointing_kwargs` to `self.model` on every `train()`, AFTER the
    trainer is built and BEFORE the model is wrapped. Whatever the model carried before
    that line is overwritten. That is what made the old train_dpo.py:291-294 model-level
    `use_reentrant=True` call a dead wire: train_dpo.py@12b16b5:332 then set the args
    value to False unconditionally, and the args value is the one that trains.
  * transformers/modeling_utils.py:3119-3122 — `gradient_checkpointing_enable(None)`
    defaults to `{"use_reentrant": True}` and stores
    `functools.partial(checkpoint, **kwargs)` as `_gradient_checkpointing_func` on every
    module that has a `gradient_checkpointing` attribute. The partial's `.keywords` is the
    inspectable state; the spy below records what the partial actually passes to torch.
  * trl/trainer/dpo_trainer.py:291-334 — DPOTrainer never calls
    `gradient_checkpointing_enable` itself on this path (only `enable_input_require_grads`;
    the `prepare_model_for_kbit_training` branch at :304 is 4/8-bit only and forwards
    `args.gradient_checkpointing_kwargs` anyway).
  * trl/trainer/grpo_trainer.py:430-431 and :802-822 — GRPOTrainer.__init__ calls
    `model.gradient_checkpointing_enable()` with NO kwargs, so the model carries
    `use_reentrant=True` after construction regardless of args; it reads
    `args.gradient_checkpointing_kwargs` only to decide `enable_input_require_grads()`.
    The train-time re-apply at trainer.py:2345 then replaces it with the args value.
    Inspecting the model after `GRPOTrainer(...)` therefore says nothing about what trains.

What is real and what is not:

  REAL   torch 2.14 (CPU), transformers 4.51.3, trl 0.18.0, peft 0.15.1; the trainer module
         under test, imported from its file; its own argument parser fed the literal
         `--gradient_checkpointing True` the launch template emits; the gradient-checkpointing
         `if` blocks of `main()`, extracted by AST and exec'd in the module's own namespace
         so `is_deepspeed_zero3_enabled` and `log_info` resolve exactly as they do in main();
         a two-layer random LlamaForCausalLM; a real fast tokenizer built in-process.
  STUB   `bitsandbytes` (module-scope `import bitsandbytes as bnb` in both trainers). It is
         not installable on macOS CPU. Nothing on this path reads it: the only readers are
         `find_all_linear_names` (never called here) and peft's bnb dispatchers, which
         short-circuit on `loaded_in_8bit/4bit == False`. `--optim` is left at the default
         (adamw_torch) instead of paged_adamw_8bit; the optimizer is not the checkpoint kwarg.
  SPY    `transformers.modeling_utils.checkpoint` is wrapped by a pass-through recorder so
         the test sees the `use_reentrant` value torch is actually called with.
  FLAG   The ZeRO-3 probe is flipped by monkeypatching the trainer module's
         `is_deepspeed_zero3_enabled` binding — the name the seam reads. A separate test
         proves that binding IS transformers' real function reading the global that
         `--deepspeed ds_config/zero3.json` installs, using a stand-in config object with
         only `is_zero3()` (deepspeed cannot be installed here, and flipping the real global
         process-wide makes `from_pretrained`/`create_reference_model` demand deepspeed).
  NOT    ZeRO-3 partitioning itself, hence the CheckpointError the fix exists to avoid;
         `main()`'s straight-line control flow between model load and the seam; the
         CustomEvalSaveCallback; the dataset loaders; bf16 / flash-attention.

Mutation runs: set REENTRANT_WIRE_TRAIN_DPO / REENTRANT_WIRE_TRAIN_GRPO to another copy of
the trainer file (e.g. `git show 12b16b5:scripts/train_dpo.py`) and the same tests run
against it. Against 12b16b5 the zero3=True cases fail with `use_reentrant=False` reaching
torch, which is the measured dead wire.
"""

import ast
import importlib.machinery
import importlib.util
import logging
import os
import sys
import types

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(REPO, "scripts")
sys.path.insert(0, SCRIPTS)

# Compute the optional-backend availability flags against the REAL environment before
# any stub is visible: transformers/peft/accelerate probe `bitsandbytes` at import time
# (and peft lazily, via find_spec + metadata), and a stub must not turn a probe True.
import torch  # noqa: E402
import transformers  # noqa: E402
import transformers.integrations.deepspeed as hf_deepspeed  # noqa: E402
import transformers.modeling_utils as modeling_utils  # noqa: E402
import trl  # noqa: E402
import peft  # noqa: E402
from datasets import Dataset  # noqa: E402


def _ensure_bnb_stub():
    """Make `import bitsandbytes as bnb` succeed without importing bitsandbytes.

    Only the module-scope import in the trainers needs it. `__spec__` is set because
    `importlib.util.find_spec` raises on a spec-less module in sys.modules; `nn` is set
    because peft's cached `is_bnb_4bit_available()` does `hasattr(bnb.nn, "Linear4bit")`
    and must come back False, not raise. Other test modules in this suite install their
    own `nn`-less stub first when collected earlier, and `import` then succeeds on that
    stub — so `nn` is ensured on whatever module is there, real or stub. Idempotent.
    """
    try:
        import bitsandbytes as mod
    except ImportError:
        mod = types.ModuleType("bitsandbytes")
        mod.__spec__ = importlib.machinery.ModuleSpec("bitsandbytes", loader=None)
        mod.__path__ = []
        sys.modules["bitsandbytes"] = mod
    if not hasattr(mod, "nn"):
        mod.nn = types.ModuleType("bitsandbytes.nn")
        sys.modules.setdefault("bitsandbytes.nn", mod.nn)


_ensure_bnb_stub()

TRAINER_SOURCES = {
    "dpo": os.environ.get("REENTRANT_WIRE_TRAIN_DPO", os.path.join(SCRIPTS, "train_dpo.py")),
    "grpo": os.environ.get("REENTRANT_WIRE_TRAIN_GRPO", os.path.join(SCRIPTS, "train_grpo.py")),
}

_GC_ATTRS = {"gradient_checkpointing", "gradient_checkpointing_kwargs", "gradient_checkpointing_enable"}


def _load_trainer_module(kind):
    _ensure_bnb_stub()  # again at fixture time: collection of later modules may have run since
    path = TRAINER_SOURCES[kind]
    name = f"_reentrant_wire_train_{kind}"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod, path


def _gc_blocks(src_path):
    """The top-level `if` statements of main() that touch gradient checkpointing, in order.

    For train_dpo.py that is the model-level ZeRO-3 call (:291) and the args seam (:349);
    for train_grpo.py it is the args seam alone (:477). Extracting rather than re-typing
    means a mutation run against another copy of the file exercises THAT copy's blocks.
    """
    source = open(src_path).read()
    tree = ast.parse(source, filename=src_path)
    main_fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main")

    def touches_gc(node):
        return any(isinstance(s, ast.Attribute) and s.attr in _GC_ATTRS for s in ast.walk(node))

    blocks = [n for n in main_fn.body if isinstance(n, ast.If) and touches_gc(n)]
    assigns_kwargs = any(
        isinstance(s, ast.Assign)
        and any(isinstance(t, ast.Attribute) and t.attr == "gradient_checkpointing_kwargs" for t in s.targets)
        for b in blocks
        for s in ast.walk(b)
    )
    assert blocks and assigns_kwargs, (
        f"{src_path}: main() has no gradient-checkpointing `if` block that assigns "
        "training_args.gradient_checkpointing_kwargs — the seam this file tests is gone"
    )
    return blocks


def _run_gc_blocks(mod, src_path, model, training_args):
    """Exec the extracted blocks with the module's globals: names resolve as in main()."""
    local_ns = {"model": model, "training_args": training_args}
    for block in _gc_blocks(src_path):
        code = compile(ast.fix_missing_locations(ast.Module(body=[block], type_ignores=[])), src_path, "exec")
        exec(code, vars(mod), local_ns)  # noqa: S102 — the trainer's own source, by design
    return local_ns


def _tiny_tokenizer():
    from tokenizers import Tokenizer, models, pre_tokenizers
    from transformers import PreTrainedTokenizerFast

    words = ["<pad>", "<s>", "</s>", "<unk>"] + [f"w{i}" for i in range(40)]
    tok = Tokenizer(models.WordLevel({w: i for i, w in enumerate(words)}, unk_token="<unk>"))
    tok.pre_tokenizer = pre_tokenizers.Whitespace()
    return PreTrainedTokenizerFast(
        tokenizer_object=tok, bos_token="<s>", eos_token="</s>", pad_token="<pad>", unk_token="<unk>"
    ), len(words)


def _tiny_model(vocab_size):
    from transformers import LlamaConfig, LlamaForCausalLM

    torch.manual_seed(0)
    cfg = LlamaConfig(
        vocab_size=vocab_size, hidden_size=16, intermediate_size=32, num_hidden_layers=2,
        num_attention_heads=2, num_key_value_heads=2, max_position_embeddings=64,
        bos_token_id=1, eos_token_id=2, pad_token_id=0,
    )
    model = LlamaForCausalLM(cfg)
    assert model.supports_gradient_checkpointing
    return model


def _checkpoint_spy(monkeypatch):
    """Record the `use_reentrant` each torch checkpoint call carries; delegate to the real one.

    `gradient_checkpointing_enable` binds `transformers.modeling_utils.checkpoint` into its
    partial (modeling_utils.py:3122), so the wrapper has to be in place before that call.
    """
    real = modeling_utils.checkpoint
    calls = []

    def spy(fn, *args, **kwargs):
        calls.append(kwargs.get("use_reentrant", "<absent>"))
        return real(fn, *args, **kwargs)

    monkeypatch.setattr(modeling_utils, "checkpoint", spy)
    return calls


def _gc_state(model):
    """{module name: partial keywords} for every module transformers marks for checkpointing."""
    return {
        name: dict(m._gradient_checkpointing_func.keywords)
        for name, m in model.named_modules()
        if hasattr(m, "gradient_checkpointing") and hasattr(m, "_gradient_checkpointing_func")
    }


def _peft_argv(use_peft):
    # The launch templates append exactly this for LoRA (dpo_config.py:174, grpo_config.py:237);
    # rank shrunk so a 16-wide model can carry it. >9B DPO/GRPO is always LoRA
    # (adaptive_config.py:106-111), and >9B on >1 GPU is what routes to ZeRO-3 (:2203).
    return ["--use_peft", "--lora_r", "4", "--lora_alpha", "8", "--lora_target_modules", "all-linear"] if use_peft else []


_PROOF_LINE = "gradient checkpointing: use_reentrant={r} (deepspeed_zero3={z})"


@pytest.fixture(scope="module")
def dpo_mod():
    return _load_trainer_module("dpo")


@pytest.fixture(scope="module")
def grpo_mod():
    return _load_trainer_module("grpo")


# --------------------------------------------------------------------------------------
# The wire, DPO
# --------------------------------------------------------------------------------------


@pytest.mark.parametrize("use_peft", [True, False], ids=["lora", "full"])
@pytest.mark.parametrize("zero3", [True, False], ids=["zero3", "ddp"])
def test_dpo_seam_value_is_what_torch_checkpoint_receives(dpo_mod, zero3, use_peft, tmp_path, monkeypatch, caplog):
    mod, src_path = dpo_mod
    calls = _checkpoint_spy(monkeypatch)
    monkeypatch.setattr(mod, "is_deepspeed_zero3_enabled", lambda: zero3)
    caplog.set_level(logging.INFO)

    tokenizer, vocab = _tiny_tokenizer()
    model = _tiny_model(vocab)
    rows = {
        "prompt": ["w1 w2", "w3 w4", "w5 w6", "w7 w8"],
        "chosen": ["w9 w10", "w11", "w12 w13", "w14"],
        "rejected": ["w15", "w16 w17", "w18", "w19 w20"],
    }
    train_ds, dev_ds = Dataset.from_dict(rows), Dataset.from_dict(rows)

    # train_dpo.py:172-173 — the module's own TrlParser, fed the launch template's literal.
    argv = [
        "--output_dir", str(tmp_path), "--request_path", "/dev/null",
        "--gradient_checkpointing", "True",
        "--per_device_train_batch_size", "2", "--max_steps", "1", "--learning_rate", "1e-4",
        "--report_to", "none", "--save_strategy", "no", "--eval_strategy", "no", "--logging_steps", "1",
        "--max_length", "32", "--max_prompt_length", "16", "--use_cpu", "True", "--bf16", "False",
    ] + _peft_argv(use_peft)
    training_args, model_args = mod.make_parser().parse_args_and_config(args=argv)
    assert training_args.gradient_checkpointing is True
    assert training_args.gradient_checkpointing_kwargs is None  # nothing has decided yet

    _run_gc_blocks(mod, src_path, model, training_args)
    decided = training_args.gradient_checkpointing_kwargs
    if zero3:
        # train_dpo.py:291-294 — the model-level call fired. It is NOT what trains (below).
        assert _gc_state(model) and all(kw == {"use_reentrant": True} for kw in _gc_state(model).values())

    # The real trainer, built as train_dpo.py:402-411 builds it (callback omitted: not on
    # this path). ref_model=None as when the request carries no "ref_model".
    peft_config = mod.get_peft_config(model_args)
    assert (peft_config is not None) is use_peft
    trainer = trl.DPOTrainer(
        model=model, ref_model=None, args=training_args, train_dataset=train_ds, eval_dataset=dev_ds,
        processing_class=tokenizer, peft_config=peft_config,
    )
    assert not calls, "no forward should have run before train()"
    trainer.train()

    # (1) the wire: what torch.utils.checkpoint was called with during the step
    assert calls, "no checkpoint call was recorded during the training step"
    assert set(calls) == {zero3}, (
        f"torch.utils.checkpoint received use_reentrant={sorted(set(calls), key=str)} "
        f"with deepspeed_zero3={zero3}; the seam had decided {decided}"
    )
    # (2) the state that produced it: trainer.py:2345 applied the args value to every module
    state = _gc_state(trainer.model)
    assert state and all(kw == {"use_reentrant": zero3} for kw in state.values()), state
    # (3) the seam decided it, and said so in the line the GPU run greps for
    assert decided == {"use_reentrant": zero3}
    assert _PROOF_LINE.format(r=zero3, z=zero3) in caplog.text, (
        "the log line the GPU run greps for was not emitted by the branch"
    )


# --------------------------------------------------------------------------------------
# The wire, GRPO
# --------------------------------------------------------------------------------------


@pytest.mark.parametrize("use_peft", [True, False], ids=["lora", "full"])
@pytest.mark.parametrize("zero3", [True, False], ids=["zero3", "ddp"])
def test_grpo_seam_value_is_what_torch_checkpoint_receives(grpo_mod, zero3, use_peft, tmp_path, monkeypatch, caplog):
    mod, src_path = grpo_mod
    calls = _checkpoint_spy(monkeypatch)
    monkeypatch.setattr(mod, "is_deepspeed_zero3_enabled", lambda: zero3)
    caplog.set_level(logging.INFO)

    tokenizer, vocab = _tiny_tokenizer()
    model = _tiny_model(vocab)
    rows = {"prompt": ["w1 w2", "w3 w4", "w5 w6", "w7 w8"]}
    train_ds, dev_ds = Dataset.from_dict(rows), Dataset.from_dict(rows)

    # train_grpo.py:329-330 — the module's own HfArgumentParser over its own dataclasses.
    argv = [
        "--output_dir", str(tmp_path), "--request_path", "/dev/null",
        "--gradient_checkpointing", "True",
        "--per_device_train_batch_size", "2", "--max_steps", "1", "--learning_rate", "1e-4",
        "--report_to", "none", "--save_strategy", "no", "--eval_strategy", "no", "--logging_steps", "1",
        "--max_prompt_length", "8", "--max_completion_length", "4", "--num_generations", "2",
        "--use_vllm", "False", "--use_cpu", "True", "--bf16", "False",
    ] + _peft_argv(use_peft)
    parser = mod.transformers.HfArgumentParser((mod.TrainingArguments, mod.ModelConfig))
    training_args, model_args = parser.parse_args_into_dataclasses(args=argv)
    assert training_args.gradient_checkpointing is True
    assert training_args.gradient_checkpointing_kwargs is None

    _run_gc_blocks(mod, src_path, model, training_args)
    decided = training_args.gradient_checkpointing_kwargs
    assert _gc_state(model) == {}  # train_grpo.py makes no model-level call

    # The real trainer, built as train_grpo.py:503-520 builds it (callback omitted).
    peft_config = mod.get_peft_config(model_args)
    assert (peft_config is not None) is use_peft

    def reward_len(completions, **kwargs):
        return [float(len(c)) for c in completions]

    trainer = trl.GRPOTrainer(
        model=model, reward_funcs=[reward_len], args=training_args, train_dataset=train_ds,
        eval_dataset=dev_ds, processing_class=tokenizer, peft_config=peft_config,
    )
    # grpo_trainer.py:809/812 — TRL's own no-kwarg enable: the model reads True here in EVERY
    # case. This is the state an inspection after construction would report, and it is not
    # the state that trains. Pinned so the next TRL bump that changes it is noticed.
    after_init = _gc_state(trainer.model)
    assert after_init and all(kw == {"use_reentrant": True} for kw in after_init.values()), after_init
    assert not calls
    trainer.train()

    # (1) the wire
    assert calls, "no checkpoint call was recorded during the GRPO step"
    assert set(calls) == {zero3}, (
        f"torch.utils.checkpoint received use_reentrant={sorted(set(calls), key=str)} "
        f"with deepspeed_zero3={zero3}; the seam had decided {decided}"
    )
    # (2) the state that produced it
    state = _gc_state(trainer.model)
    assert state and all(kw == {"use_reentrant": zero3} for kw in state.values()), state
    # (3) the seam decided it, and logged the proof line
    assert decided == {"use_reentrant": zero3}
    assert _PROOF_LINE.format(r=zero3, z=zero3) in caplog.text, (
        "the log line the GPU run greps for was not emitted by the branch"
    )


# --------------------------------------------------------------------------------------
# The probe the seam reads is the flag `--deepspeed ds_config/zero3.json` sets
# --------------------------------------------------------------------------------------


class _Zero3Config:
    """Stand-in for HfTrainerDeepSpeedConfig, which cannot be built without deepspeed.

    `is_deepspeed_zero3_enabled` (integrations/deepspeed.py:292-296) dereferences the
    weakref `TrainingArguments.__post_init__` installs and calls `.is_zero3()` on it —
    that method is the whole surface this test needs.
    """

    def is_zero3(self):
        return True


@pytest.mark.parametrize("kind", ["dpo", "grpo"])
def test_trainer_module_probe_is_the_real_flag(kind, dpo_mod, grpo_mod):
    mod, _ = {"dpo": dpo_mod, "grpo": grpo_mod}[kind]
    probe = mod.is_deepspeed_zero3_enabled
    assert probe is hf_deepspeed.is_deepspeed_zero3_enabled, (
        f"{kind}: the seam's probe is {probe!r}, not transformers' — a local shim would "
        "never see the DeepSpeed config the launch installs"
    )
    assert probe() is False, "no DeepSpeed config is installed in this process"
    cfg = _Zero3Config()  # keep a strong ref: the global holds only a weakref
    hf_deepspeed.set_hf_deepspeed_config(cfg)
    try:
        assert probe() is True
    finally:
        hf_deepspeed.unset_hf_deepspeed_config()
    assert probe() is False
