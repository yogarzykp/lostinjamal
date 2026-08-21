# CRITICAL DEFENSIVE FIX (2026-05-21): Disable optional DeepSpeed BEFORE HF imports
# to prevent Triton "0 active drivers" crash. See validator_workflow_postmortem_2026_05_08.md
from transformers_runtime import maybe_disable_optional_deepspeed
maybe_disable_optional_deepspeed()

from typing import Dict, Optional
import requests
import json
import random
from utility import log_info, MyDataset
from transformers.trainer_utils import get_last_checkpoint
from transformers import AutoTokenizer, BitsAndBytesConfig
import transformers
import torch
from transformers.trainer_utils import is_main_process
from dataclasses import dataclass, field
from transformers import Trainer
from customized_trainer import resize_if_needed, set_generation_config, CustomEvalSaveCallback, WhenToEvalHandler, init_wandb

# from packing.packed_dataset import PackedDataset
from transformers import (
    Trainer,
    TrainingArguments,
)

import os
import datetime
import shutil
from huggingface_hub import HfApi
from typing import Callable, Optional
import bitsandbytes as bnb
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import yaml
from state_manager import get_state, set_state
from attn_fallback import load_with_attn_fallback

LOCAL_RANK = int(os.getenv("LOCAL_RANK", "0"))


@dataclass
class TrainingArguments(transformers.TrainingArguments):
    request_path: Optional[str] = field(default=None)
    packing: Optional[bool] = field(default=False)
    max_packed_size: Optional[int] = field(default=-1)
    use_liger: Optional[bool] = field(default=False)
    use_lora: Optional[bool] = field(default=False)
    disable_fa: Optional[bool] = field(default=False)
    use_attn_implementation: Optional[str] = field(default="")

@dataclass
class LoraArguments:
    lora_r: int = 128
    lora_alpha: int = 512
    lora_dropout: float = 0.1
    lora_target_modules: str = "all"  # all for all linear; "q_proj v_proj"
    lora_weight_path: str = ""
    lora_bias: str = "none"
    q_lora: bool = False
    
    
def find_all_linear_names(model):
    lora_module_names = set()
    for name, module in model.named_modules():
        if isinstance(module, bnb.nn.Linear4bit) or isinstance(module, torch.nn.Linear):
            names = name.split(".")
            lora_module_names.add(names[0] if len(names) == 1 else names[-1])

    if "lm_head" in lora_module_names:  # needed for 16-bit
        lora_module_names.remove("lm_head")
    return list(lora_module_names)


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
    

def load_lora_model(training_args: TrainingArguments, model_path: str, lora_args: LoraArguments, token_nums: int):
    if training_args.use_liger:
        from liger_kernel.transformers import AutoLigerKernelForCausalLM
        model_class = AutoLigerKernelForCausalLM
    else:
        model_class = transformers.AutoModelForCausalLM

    # Same attention resolution as the full-weight loader below: honour the
    # explicit override, then fall back to sdpa if the kernel will not load.
    # This path is what KL-flagged tasks take (KL forces LoRA), so leaving it
    # unguarded cost the whole task whenever flash-attn was unavailable.
    attn_implementation = "flash_attention_2" if not training_args.disable_fa else "eager"
    if training_args.use_attn_implementation:
        attn_implementation = training_args.use_attn_implementation
    log_info(f"load_lora_model using attn_implementation: {attn_implementation}")

    model = load_with_attn_fallback(
        model_class.from_pretrained,
        model_path,
        model_kwargs=dict(
            attn_implementation=attn_implementation,
            torch_dtype=torch.bfloat16,
            quantization_config=(
                BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.bfloat16,
                )
                if lora_args.q_lora
                else None
            ),
        ),
        log=log_info,
    )
    # do not resize tokem embeddings in LOra --> will encounter size mismatch error in evaluation 
    # model.resize_token_embeddings(token_nums)
    # convert to lora
    if lora_args.lora_target_modules == "all":
        target_modules = find_all_linear_names(model)
    else:
        modules = lora_args.lora_target_modules.split(" ")
        target_modules = [mod.strip() for mod in modules if len(mod.strip()) > 0]

    lora_config = LoraConfig(
        r=lora_args.lora_r,
        lora_alpha=lora_args.lora_alpha,
        target_modules=target_modules,
        lora_dropout=lora_args.lora_dropout,
        bias=lora_args.lora_bias,
        task_type="CAUSAL_LM",
        # modules_to_save=["lm_head", "embed_tokens"],  # because we retrain the embedding
    )

    if lora_args.q_lora:
        model = prepare_model_for_kbit_training(
            model, use_gradient_checkpointing=training_args.gradient_checkpointing
        )

    model = get_peft_model(model, lora_config)

    if training_args.gradient_checkpointing:
        model.enable_input_require_grads()

    model.config.use_cache = False
    # Activate computing load balancing loss iin MixtralForCausalLM
    if hasattr(model.config, "output_router_logits"):
        setattr(model.config, "output_router_logits", True)

    print_trainable_parameters(model)
    return model


def load_model(training_args: TrainingArguments, model_path: str, token_nums: int):
    model_class = transformers.AutoModelForCausalLM
    
    if training_args.use_liger:
        from liger_kernel.transformers import AutoLigerKernelForCausalLM

        log_info("---------------using LIGER------------")
        model_class = AutoLigerKernelForCausalLM
    
    attn_implementation="flash_attention_2" if not training_args.disable_fa else "eager"
    if training_args.use_attn_implementation:
        attn_implementation = training_args.use_attn_implementation
        log_info(f"Using {attn_implementation} as the attention implementation")
    log_info(f"Using attn_implementation: {attn_implementation}")
    
    model = load_with_attn_fallback(
        model_class.from_pretrained,
        model_path,
        model_kwargs=dict(
            # trust_remote_code=True, remove this because we already filter the model architecture, it will not be used with liger-kernel
            torch_dtype=torch.bfloat16,
            attn_implementation=attn_implementation,
        ),
        log=log_info,
    )
    # model.resize_token_embeddings(token_nums)
    return model


def get_max_length_config():
    config_path = "test_axolotl.yml"
    with open(config_path, "r") as file:
        config_dict = yaml.safe_load(file)
    return config_dict["sequence_len"]


def main():
    """Format of training requests"""
    argument_parser = transformers.HfArgumentParser((TrainingArguments, LoraArguments))
    (training_args, lora_args) = argument_parser.parse_args_into_dataclasses()
    # Multi-GPU DDP + gradient_checkpointing reentrant variant raises
    # "Expected to mark a variable ready only once" — switch to non-reentrant.
    # Also slightly lower memory. Safe for single-GPU too.
    if training_args.gradient_checkpointing:
        training_args.gradient_checkpointing_kwargs = {"use_reentrant": False}
    train_info = json.load(open(training_args.request_path, "r"))
    train_request = train_info["train_request"]
    # log_info(f"Training request: {train_request}", "start")
    task_id = train_request["task_id"]

    tokenizer = AutoTokenizer.from_pretrained(train_request["model_path"])
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # wandb_init_success = init_wandb(train_request)
    # if not wandb_init_success:
    #     log_info("WANDB_API_KEY is not set, do not report to wandb")
    #     training_args.report_to = "none"    
    # else:
    #     log_info("WANDB_API_KEY is provided, we will report to wandb")
    #     training_args.report_to = "wandb"
        
    max_length = get_max_length_config()
    if "max_length" in train_request:
        max_length = train_request["max_length"]

    # we already tokenize the data and save it to train_tokenized.json and dev_tokenized.json
    train_ds = MyDataset(
        tokenizer,
       f"datasets/train_tokenized_{task_id}.json",
        max_length
    )

    dev_ds = MyDataset(
        tokenizer,
        f"datasets/dev_tokenized_{task_id}.json",
        max_length
    )
    log_info(f"train_size: {len(train_ds)}; dev_size: {len(dev_ds)}")
    
    
    donot_pack = False
    original_train_size = len(train_ds)
    original_steps = original_train_size // (
        training_args.per_device_train_batch_size
        * training_args.gradient_accumulation_steps
        * training_args.world_size
    )  # number of steps in the original training
    # min_steps here is per epoch
    if original_steps < train_request["min_steps"]:
        donot_pack = True
        log_info(f"original_steps: {original_steps} < min_steps: {train_request['min_steps']}, do not pack the dataset")

    min_data_size_num = (
        train_request["min_steps"]
        * training_args.per_device_train_batch_size
        * training_args.gradient_accumulation_steps
        * training_args.world_size
    )
    
        
    log_info(f"min_data_size_num: {min_data_size_num}; max_length: {max_length}")
    if training_args.packing and not donot_pack:
        from monkeypatch import monkey_patch_packing_for_model, PackedDataset
        log_info("Patching packing for model")

        monkey_patch_packing_for_model(train_request["model_path"])
        t1 = datetime.datetime.now()
        train_ds = PackedDataset(
            train_ds,
            tokenizer,
            max_input_length=max_length,
            max_packed_size=training_args.max_packed_size,
            min_item_num=min_data_size_num,
        )
        t2 = datetime.datetime.now()
        log_info(f"time for packing train_ds: {(t2 - t1).total_seconds()}")
        # dev_ds is deliberately NOT packed. The validator scores a flat mean over
        # EXAMPLES of each example's token-mean CE, with per_device_eval_batch_size
        # pinned to 1 (validator/evaluation/evaluators/instruct_text.py:178-186).
        # A packed dev "example" is many rows glued together, so packing turns our
        # eval_loss into a token-weighted mean — a different functional from the one
        # we are ranked on. We would then be selecting checkpoints, and gating the
        # WSM merge, on a number nobody scores. Leaving dev unpacked costs a few
        # seconds per eval and makes our metric the validator's metric.
        log_info(f"train_ds: {train_ds.stat()}")
        log_info(f"dev_ds left unpacked to match the validator's per-example mean")

    # ── Cross-lingual detection (Instruct only) ──────────────────────────
    # Measures tokenizer fertility (tokens/char) on raw training text +
    # dominant Unicode script + vocab_size (anon-resilient multilingual
    # signal). On detection: signal text_trainer.py via Redis state to
    # skip refinement (low-LR polish hurts cross-lingual: sparse in-lang
    # dev set overfit). Safe-by-default: any failure falls back to normal
    # behavior. Env override TRAINING_CROSS_LINGUAL_DETECTION=false disables.
    if os.getenv("TRAINING_CROSS_LINGUAL_DETECTION", "true").lower() not in (
        "0", "false", "no"
    ):
        try:
            from cross_lingual_detector import detect_cross_lingual

            _raw_path = f"datasets/train_{task_id}.json"
            _text_samples: list = []
            try:
                with open(_raw_path, "r", encoding="utf-8") as _f:
                    _raw = json.load(_f)
                for _item in _raw[:30]:
                    if not isinstance(_item, dict):
                        continue
                    _parts = []
                    for _field in ("instruct", "instruction", "input", "output"):
                        _val = _item.get(_field)
                        if isinstance(_val, str) and len(_val) >= 3:
                            _parts.append(_val)
                    if _parts:
                        _text_samples.append(" ".join(_parts))
            except Exception as _e:
                log_info(f"[CrossLingual] raw data sample skipped: {_e}")

            try:
                _vocab_size = len(tokenizer)
            except Exception:
                _vocab_size = None
            _fp = detect_cross_lingual(
                tokenizer,
                _text_samples,
                vocab_size=_vocab_size,
            )
            log_info(f"[CrossLingual] detection: {_fp['reason']}")

            if _fp.get("is_cross_lingual"):
                try:
                    _s = get_state() or {}
                    _s["cross_lingual_detected"] = True
                    _s["cross_lingual_fertility"] = round(
                        float(_fp.get("fertility", 0.0)), 3
                    )
                    set_state(_s)
                    log_info(
                        f"[CrossLingual] flag set — refinement will be skipped "
                        f"(fertility={_fp.get('fertility'):.3f})"
                    )
                except Exception as _e:
                    log_info(f"[CrossLingual] state write failed: {_e}")
        except Exception as _e:
            log_info(f"[CrossLingual] detection skipped: {_e}")

    log_info(f"world_size: {training_args.world_size}")
    total_steps_per_epoch = len(train_ds) // (
        training_args.per_device_train_batch_size
        * training_args.gradient_accumulation_steps
        * training_args.world_size
    )
    log_info(f"total_steps_per_epoch: {total_steps_per_epoch}")
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
    if training_args.per_device_train_batch_size > max_batch_size_theory:
        # if batch_size is quite big set it to this value to make sure that we have at least min_steps
        if train_request.get("adjust_batch_size", True):
            log_info(
                f"batch_size ({training_args.per_device_train_batch_size}) is quite big, reducing it to {max_batch_size_theory}"
            )
            training_args.per_device_train_batch_size = max_batch_size_theory
            # need to update total_steps_per_epoch
            total_steps_per_epoch = len(train_ds) // (
                training_args.per_device_train_batch_size
                * training_args.gradient_accumulation_steps
                * training_args.world_size
            )
            log_info(f"updated total_steps_per_epoch: {total_steps_per_epoch}")

    if training_args.use_lora:
        model = load_lora_model(training_args, train_request["model_path"], lora_args, len(tokenizer))
    else:
        model = load_model(training_args, train_request["model_path"], len(tokenizer))
        # some model need to resize the token embeddings or encounter the size mismatch error; only for full-weight models
        resize_if_needed(train_request["model_name"], model, len(tokenizer))
    
    try:
        model.config.use_cache = False
    except:
        pass
    
    # some model need to set the generation config or encounter the invalid generation config error
    set_generation_config(train_request["model_name"], model)

    # Check if this is the main process and create the output directory
    if is_main_process(LOCAL_RANK):  # Only create directory on main process
        os.makedirs(training_args.output_dir, exist_ok=True)
        log_info(f"Created output directory: {training_args.output_dir}")
    
    periodic_save_steps = train_request.get("periodic_save_steps", -1)
    log_info(f"periodic_save_steps: {periodic_save_steps}")
    training_args.save_only_model = True  # only save the model, not the optimizer
    
    max_steps = train_request.get("max_steps", -1)
    log_info(f"max_steps: {max_steps}")
    
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    state = get_state()
    state["train"]["start_train_time"] = start_time
    if is_main_process(LOCAL_RANK):
        set_state(state)
        
    total_steps_per_epoch = len(train_ds) // (
                training_args.per_device_train_batch_size
                * training_args.gradient_accumulation_steps
                * training_args.world_size
            )

    # Safety guard: prevent ZeroDivisionError in WhenToEvalHandler when filtered
    # dataset is smaller than batch (e.g. long-context dataset + small-context model).
    if total_steps_per_epoch == 0:
        log_info(
            f"WARNING: total_steps_per_epoch=0 "
            f"(len(train_ds)={len(train_ds)}, batch={training_args.per_device_train_batch_size}, "
            f"world_size={training_args.world_size}). Forcing batch_size=1."
        )
        training_args.per_device_train_batch_size = 1
        total_steps_per_epoch = len(train_ds) // (
            training_args.gradient_accumulation_steps * training_args.world_size
        )
        if total_steps_per_epoch == 0:
            raise RuntimeError(
                f"Dataset empty after filter (len={len(train_ds)}). "
                f"Model context likely too small for this dataset. Cannot train."
            )
        log_info(f"Safety guard active: total_steps_per_epoch={total_steps_per_epoch}")

    total_steps_all_epochs = total_steps_per_epoch * training_args.num_train_epochs
    log_info(f"total_steps_per_epoch: {total_steps_per_epoch}; total_steps_all_epochs: {total_steps_all_epochs}")
    
    success_file = os.path.join(training_args.output_dir, "success.txt")
    # remove the success file if it exists
    if is_main_process(LOCAL_RANK) and os.path.exists(success_file):
        os.remove(success_file)
    
    checking_step = train_request["checking_step"]
    if checking_step >= total_steps_per_epoch:
        checking_step = total_steps_per_epoch - 2

    callbacks_list = [
        CustomEvalSaveCallback(
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
    ]
    # Held by name, not by index: the list is appended to below, so [-1] would
    # stop pointing at this callback.
    _eval_save_callback = callbacks_list[-1]

    # Optional observability callbacks (opt-in, fail-closed on Redis error)
    if os.getenv("INSTRUCT_METRICS_REDIS") == "1":
        try:
            from callbacks.metrics_callback import MetricsCallback
            callbacks_list.append(MetricsCallback(
                task_id=train_request["task_id"],
                experiment_name=os.getenv("INSTRUCT_EXPERIMENT_NAME", "baseline"),
            ))
            print("[train_instruct] MetricsCallback registered", flush=True)
        except Exception as exc:
            print(f"[train_instruct] Failed to load MetricsCallback: {exc}", flush=True)

    if os.getenv("INSTRUCT_EXPERIMENT_LOG") == "1":
        try:
            from callbacks.experiment_logger import ExperimentLoggerCallback
            callbacks_list.append(ExperimentLoggerCallback(
                task_id=train_request["task_id"],
                model_name=train_request["model_name"],
                experiment_name=os.getenv("INSTRUCT_EXPERIMENT_NAME", "baseline"),
            ))
            print("[train_instruct] ExperimentLoggerCallback registered", flush=True)
        except Exception as exc:
            print(f"[train_instruct] Failed to load ExperimentLoggerCallback: {exc}", flush=True)

    # On a KL-flagged task the validator ranks us on eval_loss + kl_coef * KL
    # against the base model, so train that objective rather than plain CE.
    # Reference logits come from disable_adapter() on the same weights, which is
    # why adaptive_config forces the LoRA path for these tasks. Falls back to the
    # stock Trainer whenever the flag is off — see scripts/kl_objective.py.
    _use_kl = bool(train_request.get("use_kl"))
    _kl_coef = train_request.get("kl_coef")
    if _use_kl and _kl_coef:
        from kl_trainer_mixin import KLWeightedTrainerMixin

        class _KLTrainer(KLWeightedTrainerMixin, Trainer):
            pass

        log_info(f"[kl] composite objective: {train_request.get('kl_reason')}")
        trainer = _KLTrainer(
            model=model,
            tokenizer=tokenizer,
            args=training_args,
            train_dataset=train_ds,
            eval_dataset=dev_ds,
            callbacks=callbacks_list,
            kl_coef=float(_kl_coef),
        )
    else:
        trainer = Trainer(
            model=model,
            tokenizer=tokenizer,
            args=training_args,
            train_dataset=train_ds,
            eval_dataset=dev_ds,
            callbacks=callbacks_list,
        )

    trainer.tokenizer = tokenizer

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

    # Gate the WSM merge on measured held-out loss.
    #
    # The merge writes an averaged adapter over the best-only submission. Nothing
    # guaranteed the average was actually better, so souping could silently
    # downgrade the one artefact we are scored on. This hook loads the merged
    # adapter that was just written and evaluates it, so the callback can roll
    # back a merge that does not beat the best single checkpoint.
    #
    # Note it must LOAD from disk: trainer.evaluate() alone scores the in-memory
    # model, which at train end is the final training state, not the merge.
    # Any failure here raises, and the callback treats that as a rejection —
    # failing toward keeping the verified best-only submission.
    # Disable with TRAINING_WSM_GATE=0.
    if os.getenv("TRAINING_WSM_GATE", "1") == "1":
        def _merge_eval():
            from peft import set_peft_model_state_dict
            from safetensors.torch import load_file

            sub = train_request["submission_dir"]
            path = os.path.join(sub, "adapter_model.safetensors")
            if not os.path.isfile(path):
                raise FileNotFoundError(f"no merged adapter at {path}")
            set_peft_model_state_dict(trainer.model, load_file(path))
            # Score the merge with the SAME function that ranked the individual
            # checkpoints, not a raw eval_loss. On a KL task compute_loss returns
            # eval_loss + kl_coef * KL, which runs well above the unweighted
            # number — so comparing a raw eval_loss against a weighted baseline
            # would accept every merge on exactly the tasks where the merge is
            # least understood. Routing both sides through one function means the
            # two can never drift apart again.
            #
            # The adapter is already loaded above, so the KL this computes is the
            # merged model's. state is unused by compute_loss.
            return _eval_save_callback.compute_loss(None, trainer.evaluate())

        _eval_save_callback.merge_eval_fn = _merge_eval
        log_info("[WSM] merge will be gated on held-out loss")
    else:
        log_info("[WSM] TRAINING_WSM_GATE=0 — merge written unverified")

    # Score LR-probe runs on held-out loss, not training loss.
    #
    # The LR sweep picks the probe with the lowest score, and `_probe_loss` already
    # knows how to use a held-out number — but only when probe_eval_fn is wired, and
    # until now the ONLY wiring site was train_dpo.py. So every instruct and chat task
    # chose its learning rate by comparing TRAINING losses, which is the one signal
    # that rewards a learning rate for fitting the training set harder. The validator
    # ranks us on held-out loss; selecting on anything else optimises a different
    # objective than the one we are scored on, and does it at the point where a single
    # decision governs the whole run.
    #
    # Same shape as the max_length bug: the mechanism was correct and simply not
    # connected on this path. Disable with INSTRUCT_PROBE_EVAL=0.
    if os.getenv("INSTRUCT_PROBE_EVAL", "1") == "1":
        def _probe_eval():
            # compute_loss, not a raw eval_loss, so a KL task ranks its probes on the
            # same weighted metric it ranks its checkpoints and its soup on.
            return _eval_save_callback.compute_loss(None, trainer.evaluate())

        _eval_save_callback.probe_eval_fn = _probe_eval
        log_info("[probe] LR probes will be scored on held-out dev loss")
    else:
        log_info("[probe] INSTRUCT_PROBE_EVAL=0 — probes scored on training loss")

    # Per-example eval losses, recorded to telemetry on every eval.
    # Observational only — see the note in customized_trainer.on_evaluate. The
    # vector is what lets us check, after these runs, whether win-rate selection
    # would have chosen differently than the mean did.
    from per_example_eval import collect_per_example_losses, enabled as _pe_enabled

    if _pe_enabled():
        def _per_example_eval():
            return collect_per_example_losses(
                trainer.model,
                trainer.get_eval_dataloader(),
                device=trainer.args.device,
            )

        _eval_save_callback.per_example_eval_fn = _per_example_eval
        log_info("[per-example] recording per-example eval losses to telemetry")

    # Rank checkpoints by the metric the validator ranks by. Training the
    # composite objective is only half the job: without this, we would optimise
    # eval_loss + kl_coef*KL and then submit whichever checkpoint minimised plain
    # eval_loss. The KL here is measured on the dev set the same way the
    # validator measures it on its held-out set.
    if _use_kl and _kl_coef:
        from kl_objective import instruct_kl_tensor

        def _kl_metric():
            base = getattr(trainer.model, "module", trainer.model)
            disable = getattr(base, "disable_adapter", None)
            if disable is None:
                raise RuntimeError("no adapter to disable — cannot measure reference")

            loader = trainer.get_eval_dataloader()
            total, count = 0.0, 0
            base.eval()
            with torch.no_grad():
                for batch in loader:
                    batch = {k: v.to(trainer.args.device) for k, v in batch.items() if hasattr(v, "to")}
                    labels = batch.get("labels")
                    if labels is None:
                        continue
                    fwd = {k: v for k, v in batch.items() if k in ("input_ids", "attention_mask", "position_ids")}
                    ft_logits = base(**fwd).logits
                    with disable():
                        ref_logits = base(**fwd).logits
                    n = int((labels != -100).sum().item())
                    if n:
                        total += float(instruct_kl_tensor(ref_logits, ft_logits, labels)) * n
                        count += n
            return total / count if count else 0.0

        _eval_save_callback.kl_coef = float(_kl_coef)
        _eval_save_callback.kl_metric_fn = _kl_metric
        log_info(f"[kl] checkpoint selection weighted by kl_coef={_kl_coef}")

    # ── LR range test, probe run only ───────────────────────────────────────
    # Measure where loss actually falls fastest across five decades, and hand the
    # answer to text_trainer through the request state so it can build confirmation
    # candidates from it instead of nudging +/-51% around the family table.
    #
    # Why here: the ladder's candidates were generated from the table LR, so a wrong
    # table meant every candidate was wrong. Measured with a prior poisoned 10x high,
    # the ladder selected its own lowest candidate and still landed 6.6x high
    # (ops/smoke/lr_recovery.sh). The sweep below covers 1e-7..1e-2.
    #
    # Only in the probe run: the confirmation runs and the final run must train, not
    # measure. Disable with INSTRUCT_LRRT=0.
    if (train_request.get("checking_mode") == "first_time"
            and os.getenv("INSTRUCT_LRRT", "1") == "1"):
        try:
            import lr_search
            from lr_finder import find_lr_lrrt
            from torch.utils.data import DataLoader

            _n_iter = int(os.getenv("INSTRUCT_LRRT_ITERS", "100"))
            # Sweep at a SMALL batch, not the training batch. The range test needs a
            # usable gradient per step, not throughput, and the training batch is sized
            # to fill the GPU during training — running it again on top of an already
            # resident model and Trainer allocations does not fit. Measured: at batch 16,
            # seq 1024, vocab 151936 the logits alone are 4.98 GB in bf16 and about
            # twice that once the loss upcasts, which is the 9.27 GiB allocation that
            # OOM'd this path twice.
            _sweep_bs = max(1, min(int(os.getenv("INSTRUCT_LRRT_BATCH", "4")),
                                   training_args.per_device_train_batch_size))
            _loader = DataLoader(train_ds, batch_size=_sweep_bs,
                                 shuffle=True, collate_fn=trainer.data_collator)
            log_info(f"[lr-search] sweeping at batch={_sweep_bs} "
                     f"(training batch is {training_args.per_device_train_batch_size})")
            # Sweep with the optimizer production actually trains with, not a plain
            # AdamW. Two reasons, one measured. A full-precision AdamW allocates two
            # fp32 moment tensors per trainable parameter — ~13 GB on a 1.5B full
            # fine-tune — and that is what OOM'd this path on the first real run
            # ("Tried to allocate 9.27 GiB"), leaving a sweep truncated after a handful
            # of points whose "steepest descent" was noise at the bottom of the range
            # (it returned 1.12e-08). The second reason matters even where memory is
            # free: an LR range test measures how loss responds to a step, and a
            # different optimizer takes a different step, so sweeping with AdamW to
            # choose a rate for paged_adamw_8bit measures the wrong thing.
            try:
                import bitsandbytes as _bnb
                _opt = _bnb.optim.PagedAdamW8bit(model.parameters(), lr=1e-7)
            except Exception:
                # SGD holds no moments at all. Less faithful, but a sweep that runs
                # beats a sweep that OOMs, and the confirmation probe judges the answer.
                _opt = torch.optim.SGD(model.parameters(), lr=1e-7)
            _lrrt_lr, _swept, _sweep_losses = find_lr_lrrt(
                model, _opt, _loader, num_iter=_n_iter, device=str(trainer.args.device))

            # Keep the curve. It is the only record of WHY a rate was chosen, and
            # without it the suggestion is a number with no way to audit it — we spent
            # several GPU runs unable to tell an intrinsically-early heuristic from a
            # picker choosing among noise, which the slope profile answers directly.
            # Written beside the telemetry, never into submission_dir.
            try:
                _curve_dir = os.path.dirname(os.getenv("TRAINING_TELEMETRY_PATH", "")) or training_args.output_dir
                os.makedirs(_curve_dir, exist_ok=True)
                with open(os.path.join(_curve_dir, "lrrt_curve.json"), "w") as _cf:
                    json.dump({"lrs": [float(x) for x in _swept],
                               "smoothed_losses": [float(x) for x in _sweep_losses],
                               "suggested_safe_lr": float(_lrrt_lr),
                               "incumbent": float(training_args.learning_rate)}, _cf)
                log_info(f"[lr-search] sweep curve written ({len(_swept)} points)")
            except Exception as _ce:
                log_info(f"[lr-search] could not write sweep curve ({_ce})")
            del _opt, _loader

            # A sweep cut short covers too little of the range for "steepest descent" to
            # mean anything; the bounds would clamp the answer to a floor that was never
            # measured. Refuse it rather than dress it up as a measurement.
            _min_pts = max(20, _n_iter // 4)
            if len(_swept) < _min_pts:
                raise RuntimeError(
                    f"sweep covered only {len(_swept)}/{_n_iter} points; too few to locate a rate")

            _st = get_state()
            _st["lrrt_lr"] = float(_lrrt_lr)
            if is_main_process(LOCAL_RANK):
                set_state(_st)
            log_info(lr_search.describe(_lrrt_lr, training_args.learning_rate,
                                        train_request.get("task_type", "instruct")))
        except Exception as _lrrt_exc:
            # Fail open: without lrrt_lr in the state, text_trainer falls back to the
            # geometric ladder. A failed measurement must never cost the task.
            log_info(f"[lr-search] LRRT skipped ({type(_lrrt_exc).__name__}: {_lrrt_exc})")
        finally:
            # NON-NEGOTIABLE, and the reason this is not left to lr_finder's own
            # restore: the sweep runs ~100 optimizer steps up to 1e-2, including
            # divergent ones, so these weights are ruined. find_lr_for_task does keep
            # an in-VRAM `detach().clone()` of every trainable parameter, which doubles
            # trainable-weight VRAM for the duration — an OOM landmine on exactly the
            # large boss-round models. Reloading from disk costs the 7 s measured on
            # this path and holds no extra memory. Doing it at the CALL SITE makes it a
            # structural invariant rather than a property of the finder, because the
            # failure mode is silent: training continues on damaged weights and the run
            # looks entirely normal.
            log_info("[lr-search] reloading model to discard the sweep's weights")
            _fresh = (load_lora_model(training_args, train_request["model_path"], lora_args, len(tokenizer))
                      if training_args.use_lora
                      else load_model(training_args, train_request["model_path"], len(tokenizer)))
            trainer.model = _fresh
            trainer.model_wrapped = _fresh
            model = _fresh
            # Clear, do not rebuild. Trainer.create_optimizer() returns early when
            # self.optimizer is already set, so calling create_optimizer_and_scheduler
            # here could leave an optimizer still holding the DESTROYED model's
            # parameters. And the step count is not known yet: max_steps is -1 on an
            # epoch-driven run, so the previous `max_steps if > 0 else 1` built a
            # scheduler for a single step, collapsing the learning rate to its minimum
            # immediately after step 1.
            #
            # trainer.train() builds both, from the fresh model and with the real step
            # count. Setting these to None is all that is needed to let it.
            trainer.optimizer = None
            trainer.lr_scheduler = None

    # last_checkpoint = get_last_checkpoint(training_args.output_dir)
    # log_info(f"last_checkpoint: {last_checkpoint}")
    trainer.train()
    
    if is_main_process(LOCAL_RANK):
        success_file = os.path.join(training_args.output_dir, "success.txt")
        with open(success_file, "w") as f:
            f.write("Success")
    log_info("Training successfully done", "finish")

if __name__ == "__main__":
    main()
