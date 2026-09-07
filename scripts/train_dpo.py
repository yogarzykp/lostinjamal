# CRITICAL DEFENSIVE FIX (2026-05-21): Disable optional DeepSpeed BEFORE HF imports
# to prevent Triton "0 active drivers" crash. See validator_workflow_postmortem_2026_05_08.md
from transformers_runtime import maybe_disable_optional_deepspeed
maybe_disable_optional_deepspeed()

from typing import Dict, Optional
import requests
import json
import random
import utility
from datasets import Dataset
from utility import log_info
from transformers import AutoTokenizer, BitsAndBytesConfig, AutoConfig
from transformers.trainer_utils import get_last_checkpoint
import transformers
import torch
from transformers.trainer_utils import is_main_process
from dataclasses import dataclass, field
from transformers import Trainer
from trl import DPOTrainer, DPOConfig, ModelConfig, ScriptArguments, TrlParser
from trl import get_kbit_device_map, get_peft_config, get_quantization_config
from peft import (
    LoraConfig,
    PeftModel,
    get_peft_model,
    prepare_model_for_kbit_training,
    PeftModelForCausalLM,
    AutoPeftModelForCausalLM,
)
from transformers import TrainerCallback
import argparse
import os
from customized_trainer import resize_if_needed, set_generation_config, CustomEvalSaveCallback, WhenToEvalHandler, init_wandb
from state_manager import get_state, set_state

# from packing.packed_dataset import PackedDataset
from transformers import (
    Trainer,
    TrainingArguments,
    TrainerCallback,
    TrainerState,
    TrainerControl,
)
import os
import datetime
import shutil
from huggingface_hub import HfApi
from typing import Callable, Optional
import bitsandbytes as bnb
import yaml
from tokenize_dpo import get_dataset
from transformers.modeling_utils import is_deepspeed_zero3_enabled
from attn_fallback import load_with_attn_fallback



try:
    # Module scope: a raise here fails the import, so the trainer subprocess dies
    # before a step runs and the log carries an ImportError rather than a cause.
    # torchrun normally sets an integer, but a launcher that sets the variable to an
    # EMPTY string gets "" back from getenv — not the default — and int("") raises.
    LOCAL_RANK = int(os.getenv("LOCAL_RANK") or 0)
except (TypeError, ValueError):
    print(f"[rank] LOCAL_RANK={os.getenv('LOCAL_RANK')!r} is not a rank — using 0", flush=True)
    LOCAL_RANK = 0


@dataclass
class TrainingArguments(DPOConfig):
    request_path: Optional[str] = field(default=None)
    use_liger: Optional[bool] = field(default=False)
    disable_fa: Optional[bool] = field(default=False)
    use_attn_implementation: Optional[str] = field(default="")


def find_all_linear_names(model):
    # One definition, in lora_targets.py. This was three byte-identical copies, and a
    # Linear inside an nn.Sequential contributed the bare target "0", which PEFT
    # suffix-matches against model.layers.0 — a whole decoder layer — killing
    # get_peft_model. Fixing one copy would have left the crash in the other two.
    from lora_targets import find_all_linear_names as _impl
    return _impl(model, (bnb.nn.Linear4bit, torch.nn.Linear))


def print_trainable_parameters(model):
    """
    Prints the number of trainable parameters in the model.
    """
    lora_param_count = 0
    all_param = 0
    embedding_lm_head_param_count = 0
    for name, param in model.named_parameters():
        num_params = param.numel()
        # if using DS Zero 3 and the weights are initialized empty
        if num_params == 0 and hasattr(param, "ds_numel"):
            num_params = param.ds_numel

        all_param += num_params
        if param.requires_grad:
            log_info(f"trainable: {name}, num_params: {num_params}")
            if "lm_head" in name or "embed_tokens" in name:
                embedding_lm_head_param_count += num_params
            else:
                lora_param_count += num_params
    trainable_params = embedding_lm_head_param_count + lora_param_count
    log_info(
        f"all params: {all_param:,d} || trainable params: {trainable_params:,d} || trainable%: {100 * trainable_params / all_param}"
    )
    log_info(
        f"embedding_lm_head_param_count: {embedding_lm_head_param_count} = {embedding_lm_head_param_count * 100 / all_param} %"
    )
    log_info(
        f"loara_param: {lora_param_count} = {lora_param_count * 100 / all_param} %"
    )


def resolve_dpo_max_length(model_max_length: int, train_request: dict) -> int:
    """Apply the OOM ladder's sequence-length rung to DPO's own max_length.

    `model_max_length` is what DPO would train at on a healthy run: derived from
    the model config to match the validator's DPO evaluator, which reads
    max_position_embeddings with no halving
    (G.O.D/validator/evaluation/eval_dpo.py:155).

    The OOM ladder's final rung fires only after batch size is already 1 and
    writes `oom_max_length` into the request JSON
    (text_trainer.halve_request_max_length). Nothing here read it, so that rung
    was inert for DPO: the ladder ended at batch=1, every remaining retry re-ran
    an identical command, and retries ran out with no checkpoint written at all —
    a scored zero rather than a worse number.

    Only `oom_max_length` is consulted, and only downwards. Plain `max_length`
    carries the planner's value from `_select_max_length`, which mirrors the
    *axolotl* evaluator's halving rule and is routinely lower than what DPO's own
    evaluator uses; honouring that key here would silently shorten every healthy
    DPO run.

    One rung can drop further than strictly needed, because the ladder halves the
    planner's number rather than this one. That is the intended trade: a shorter
    run that finishes beats an identical retry that OOMs again and submits
    nothing.
    """
    cap = train_request.get("oom_max_length") if isinstance(train_request, dict) else None
    if isinstance(cap, bool) or not isinstance(cap, int):
        return model_max_length
    if cap <= 0 or cap >= model_max_length:
        return model_max_length
    log_info(f"DPO max_length capped {model_max_length} -> {cap} by the OOM ladder")
    return cap


def get_max_length_config():
    config_path = "test_axolotl.yml"
    with open(config_path, "r") as file:
        config_dict = yaml.safe_load(file)
    return config_dict["sequence_len"]


def make_parser(subparsers: argparse._SubParsersAction = None):
    dataclass_types = (TrainingArguments, ModelConfig)
    if subparsers is not None:
        parser = subparsers.add_parser(
            "dpo", help="Run the DPO training script", dataclass_types=dataclass_types
        )
    else:
        parser = TrlParser(dataclass_types)
    return parser


def main():
    """Format of training requests"""
    parser = make_parser()
    training_args, model_args = parser.parse_args_and_config()
    train_info = json.load(open(training_args.request_path, "r"))
    train_request = train_info["train_request"]

    # check if need to run early stop or not
    task_id = train_request["task_id"]
    
    # wandb_init_success = init_wandb(train_request)
    # if not wandb_init_success:
    #     log_info("WANDB_API_KEY is not set, do not report to wandb")
    #     training_args.report_to = "none"    
    # else:
    #     log_info("WANDB_API_KEY is provided, we will report to wandb")
    #     training_args.report_to = "wandb"

    # log_info(f"Training request: {train_request}", "start")
    # first download the dataset from the URL, save it as data.json
    output_dir = training_args.output_dir
    tokenizer = AutoTokenizer.from_pretrained(train_request["model_path"])
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Align with validator DPO eval (PR #1160, 2026-05-30): validator now sets
    # max_length = model.config.max_position_embeddings instead of TRL default 1024.
    # Train with matching cap so long DPO samples aren't silently truncated only here.
    try:
        _model_cfg = AutoConfig.from_pretrained(train_request["model_path"], trust_remote_code=False)
        _max_pos = (
            getattr(_model_cfg, "max_position_embeddings", None)
            or getattr(_model_cfg, "n_positions", None)
            or 4096
        )
    except Exception as _e:
        log_info(f"Could not read model config for max_length: {_e}")
        _max_pos = 4096
    _dpo_max_length = resolve_dpo_max_length(min(int(_max_pos), 4096), train_request)
    training_args.max_length = _dpo_max_length
    training_args.max_prompt_length = _dpo_max_length // 2
    log_info(f"DPO max_length={training_args.max_length}, max_prompt_length={training_args.max_prompt_length}")

    train_path = os.path.join("datasets", f"dpo_train_{task_id}.json")
    dev_path = os.path.join("datasets", f"dpo_dev_{task_id}.json")

    train_ds = get_dataset(train_path, train_request["dataset_type"])
    dev_ds = get_dataset(dev_path, train_request["dataset_type"])

    log_info(f"world_size: {training_args.world_size}")
    # EXP-DEFENSIVE 2026-05-21 (hyper-text port): use math.ceil (not //) for steps_per_epoch
    # and enforce MIN_BATCH_FLOOR=4 to prevent off-by-one WhenToEvalHandler triggers and
    # pathological batch=1 SGD on tiny datasets.
    import math as _math
    _MIN_BATCH_FLOOR = 4
    _eff_batch = max(_MIN_BATCH_FLOOR, training_args.per_device_train_batch_size
                     * training_args.gradient_accumulation_steps
                     * training_args.world_size)
    total_steps_per_epoch = _math.ceil(len(train_ds) / _eff_batch)

    log_info(f"total_steps_per_epoch: {total_steps_per_epoch} (eff_batch={_eff_batch}, MIN_BATCH_FLOOR={_MIN_BATCH_FLOOR})")
    # consider reducing the batch_size if it is quite big
    # num_steps = len(train_ds) * training_args.num_train_epochs / (training_args.per_device_train_batch_size * training_args.gradient_accumulation_steps * training_args.world_size)
    # num_steps > min_step ->
    max_batch_size_theory = len(train_ds) / (
        training_args.gradient_accumulation_steps
        * training_args.world_size
        * train_request["min_steps"]
    )
    max_batch_size_theory = int(max_batch_size_theory)
    if max_batch_size_theory == 0:
        max_batch_size_theory = 1

    original_batch_size = training_args.per_device_train_batch_size

    quantization_config = get_quantization_config(model_args)
    device_string = "cuda:" + str(LOCAL_RANK)
    
    device_map=(
            get_kbit_device_map()
            if quantization_config is not None
            else {"": device_string}
        )
    if len(training_args.fsdp) > 0 or is_deepspeed_zero3_enabled():
        device_map = None


    attn_implementation="flash_attention_2" if not training_args.disable_fa else "eager"
    if training_args.use_attn_implementation:
        attn_implementation = training_args.use_attn_implementation
        log_info(f"Using {attn_implementation} as the attention implementation")
        
    model_kwargs = dict(
        revision=model_args.model_revision,
        attn_implementation=attn_implementation,
        torch_dtype=torch.bfloat16,
        use_cache=False if training_args.gradient_checkpointing else True,
        device_map=device_map
    )
    
    # Only add quantization_config if it's not None
    if quantization_config is not None:
        model_kwargs["quantization_config"] = quantization_config

    log_info(f"final training_args: {training_args}")

    if training_args.use_liger:
        from liger_kernel.transformers import AutoLigerKernelForCausalLM

        model_class = AutoLigerKernelForCausalLM
    else:
        model_class = transformers.AutoModelForCausalLM

    # Wrapping only the first load: the helper downgrades model_kwargs in place,
    # so the ref-model and PEFT loads below inherit the working setting.
    model = load_with_attn_fallback(
        model_class.from_pretrained,
        train_request["model_path"],
        model_kwargs=model_kwargs,
        log=log_info,
    )
    if len(training_args.fsdp) > 0 or is_deepspeed_zero3_enabled():
        # set gradient checkpointing to True with use_reentrant=True for deepspeed
        log_info("Setting gradient checkpointing to True with use_reentrant=True for deepspeed")
        model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant': True})


    # some model need to set the generation config or encounter the invalid generation config error
    set_generation_config(train_request["model_name"], model)

    ref_model = None
    if "ref_model" in train_request:
        ref_model = model_class.from_pretrained(
            train_request["ref_model"], **model_kwargs
        )
        # print("load ref_model: ", train_request["ref_model"])

    peft_config = get_peft_config(model_args)
    if "lora_model" in train_request:
        model = PeftModelForCausalLM.from_pretrained(
            model, train_request["lora_model"], is_trainable=True, **model_kwargs
        )

    if peft_config is None:  # this is full-weight training
        # some model need to resize the token embeddings or encounter the size mismatch error; only for full-weight models
        resize_if_needed(train_request["model_name"], model, len(tokenizer))

    # Only resize token embeddings if not using LoRA
    # if peft_config is None:  # full-weights training
    #    model.resize_token_embeddings(len(tokenizer))

    # Check if this is the main process and create the output directory
    if is_main_process(LOCAL_RANK):  # Only create directory on main process
        os.makedirs(training_args.output_dir, exist_ok=True)
        log_info(f"Created output directory: {training_args.output_dir}")

    periodic_save_steps = train_request.get("periodic_save_steps", -1)
    log_info(f"periodic_save_steps: {periodic_save_steps}")

    training_args.save_only_model = True  # only save the model, not the optimizer

    # ZeRO-3 needs the REENTRANT checkpoint variant. The non-reentrant one validates
    # recomputed activation metadata, and ZeRO-3 releases a gathered parameter after the
    # forward pass, so recomputation sees torch.Size([0]) and every rank dies with
    # CheckpointError before step one. Measured on Qwen2.5-14B / 2 GPUs, 2026-09-07.
    #
    # This line used to be unconditional, which made the ZeRO-3 branch forty lines above
    # (model.gradient_checkpointing_enable(..., use_reentrant=True)) a DEAD WIRE: HF's
    # Trainer re-applies args.gradient_checkpointing_kwargs inside _inner_training_loop,
    #   if args.gradient_checkpointing:
    #       self.model.gradient_checkpointing_enable(gradient_checkpointing_kwargs=args.gradient_checkpointing_kwargs)
    # so the args value is what actually reaches training and False won. The model-level
    # call above is kept for the FSDP case it also covers; this is the seam that decides.
    #
    # It became reachable when adaptive_config widened the ds/ddp threshold to gpu_count>1:
    # a >9B DPO task is provisioned x3, so it lands on 3+ GPUs and now takes ZeRO-3.
    # A crash here is not a bad score, it is a forfeit — no checkpoint is written, the
    # relaunch ladder only pattern-matches OOM, and add_random_noise ships a noised base
    # model as the finetune.
    if training_args.gradient_checkpointing:
        _zero3 = is_deepspeed_zero3_enabled()
        training_args.gradient_checkpointing_kwargs = {"use_reentrant": bool(_zero3)}
        log_info(f"gradient checkpointing: use_reentrant={bool(_zero3)} (deepspeed_zero3={_zero3})")
    print("train_ds.column_names: ", train_ds.column_names)

    max_steps = train_request.get("max_steps", -1)
    log_info(f"max_steps: {max_steps}")
    
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    state = get_state()
    state["train"]["start_train_time"] = start_time
    if is_main_process(LOCAL_RANK):
        set_state(state)
    
    # Recomputed here because batch/accum may have moved since the first
    # estimate. Same guarded form as above, not a bare `//`: a dataset smaller
    # than one effective batch floors this to 0, and WhenToEvalHandler then does
    # `global_step % steps_per_epoch` (customized_trainer.py:1509) and dies with
    # ZeroDivisionError on the first step. ceil also stops a partial last batch
    # from being dropped from the count.
    _eff_batch_now = max(_MIN_BATCH_FLOOR, training_args.per_device_train_batch_size
                         * training_args.gradient_accumulation_steps
                         * training_args.world_size)
    total_steps_per_epoch = max(1, _math.ceil(len(train_ds) / _eff_batch_now))


    total_steps_all_epochs = total_steps_per_epoch * training_args.num_train_epochs
    log_info(f"total_steps_per_epoch: {total_steps_per_epoch}; total_steps_all_epochs: {total_steps_all_epochs}")
    
    
    success_file = os.path.join(training_args.output_dir, "success.txt")
    # remove the success file if it exists
    if is_main_process(LOCAL_RANK) and os.path.exists(success_file):
        os.remove(success_file)
    
    checking_step = train_request["checking_step"]
    if checking_step >= total_steps_per_epoch:
        checking_step = total_steps_per_epoch - 2
    

    eval_save_callback = CustomEvalSaveCallback(
        WhenToEvalHandler(train_request["end_time"], train_request["save_before_remaining_time"], periodic_save_steps=periodic_save_steps, steps_per_epoch=total_steps_per_epoch, max_steps=max_steps),
        train_request["submission_dir"],
        training_args.output_dir,
        train_request["model_name"],
        max_steps,
        checking_step=checking_step,
        total_steps_all_epochs=total_steps_all_epochs,
        end_time=train_request["end_time"],
        checking_mode=train_request.get("checking_mode", "none")
    )

    trainer = DPOTrainer(
        model=model,
        ref_model=ref_model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=dev_ds,
        processing_class=tokenizer,
        peft_config=peft_config,
        callbacks=[eval_save_callback],
    )

    # Score LR-probe runs on held-out DPO loss instead of training loss.
    # DPO's degenerate minimiser means a too-high LR collapses the policy's
    # log-probs, inflating the chosen-rejected margin so training loss falls while
    # the model degrades — so training-loss selection prefers the worst LR. The
    # validator scores DPO on held-out loss, so we select the same way.
    # Disable with DPO_PROBE_EVAL=0.
    if os.getenv("DPO_PROBE_EVAL", "1") == "1":
        def _probe_eval():
            metrics = trainer.evaluate()
            return metrics["eval_loss"]

        eval_save_callback.probe_eval_fn = _probe_eval
        log_info("[probe] DPO LR probes will be scored on held-out dev loss")
    else:
        log_info("[probe] DPO_PROBE_EVAL=0 — probes scored on training loss")


    # EXP-HYPER-PORT-E 2026-05-20: per-layer LR optimizer override (LARS-style).
    # Reads multipliers from train_request (computed in adaptive_config), rebuilds
    # optimizer with per-layer param_groups. Fail-soft: any error → default optimizer.
    # Disable via PER_LAYER_LR_ENABLED=0 env.
    try:
        from per_layer_optimizer import apply_per_layer_lr_optimizer
        apply_per_layer_lr_optimizer(
            trainer, train_request.get("per_layer_lr_multipliers")
        )
    except Exception as _exc:
        log_info(f"[per-layer-lr] hook failed (skipped): {type(_exc).__name__}: {_exc}")

    print("Start training ...", flush=True)
    # trainer.train()
    trainer.train()
    
    if is_main_process(LOCAL_RANK):
        with open(os.path.join(training_args.output_dir, "success.txt"), "w") as f:
            f.write("Success")


if __name__ == "__main__":
    main()