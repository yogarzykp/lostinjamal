import json
import os
from math import ceil

from model_utility import (
    get_model_architecture,
    get_model_num_params,
    get_use_liger,
    disable_flash_attention,
    get_data_size,
    get_gpu_count,
)
from copy import deepcopy
from lrs_lookup import get_instruct_lr, get_lr_from_ar_instruct
from llm_warmstart import try_llm_warmstart
from model_utility import get_data_size

# Validator's test_axolotl.yml sets sequence_len: 4096 — mirror exactly.
VALIDATOR_SEQUENCE_LEN = 4096


def _resolve_max_length(model_path: str) -> int | None:
    """Mirror validator's auto-halve logic (G.O.D/validator/evaluation/common.py:430-431).

    If model.config.max_position_embeddings < 2 * 4096, halve sequence_len to
    ceil(max_position_embeddings / 2). Otherwise use 4096. This keeps training
    and eval distributions aligned per-task, zero manual tuning.

    Returns None if detection fails, so caller can fall back to YAML default.
    """
    try:
        from transformers import AutoConfig
        cfg = AutoConfig.from_pretrained(model_path, trust_remote_code=True)
        max_emb = getattr(cfg, "max_position_embeddings", None)
        if max_emb and max_emb < 2 * VALIDATOR_SEQUENCE_LEN:
            return ceil(max_emb / 2)
        return VALIDATOR_SEQUENCE_LEN
    except Exception as exc:
        print(f"[instruct_config] max_length auto-resolve failed: {exc}", flush=True)
        return None


FIXED_BS_CONFIG = {
    "EleutherAI/gpt-neo-1.3B": {"batch_size": 36},
    "EleutherAI/gpt-neo-125m": {"batch_size": 48},
    "bigscience/bloom-560m": {"batch_size": 10},
    "facebook/opt-1.3b": {"batch_size": 38},
    "facebook/opt-350m": {"batch_size": 36},
    "facebook/opt-125m": {"batch_size": 48},
}

# Anonymization-safe parallel: fingerprint → batch_size for the same models.
# Format: "(hidden_size,num_hidden_layers,vocab_size,intermediate_size)" → batch
# Used when model_name is anonymized (post G.O.D feature/model-prep-container
# merge) — config.json fingerprint preserved by validator's scrub.
# Add entries as encountered in tournament.
FIXED_BS_BY_FINGERPRINT = {
    # facebook/opt-350m: hidden=1024, layers=24, vocab=50272, intermediate=4096
    "1024,24,50272,4096": {"batch_size": 36},
    # facebook/opt-125m: hidden=768, layers=12, vocab=50272, intermediate=3072
    "768,12,50272,3072": {"batch_size": 48},
    # facebook/opt-1.3b: hidden=2048, layers=24, vocab=50272, intermediate=8192
    "2048,24,50272,8192": {"batch_size": 38},
    # bigscience/bloom-560m: hidden=1024, layers=24, vocab=250880, intermediate=4096
    "1024,24,250880,4096": {"batch_size": 10},
    # EleutherAI/gpt-neo-125m: hidden=768, layers=12, vocab=50257, intermediate=3072
    "768,12,50257,3072": {"batch_size": 48},
    # EleutherAI/gpt-neo-1.3B: hidden=2048, layers=24, vocab=50257, intermediate=8192
    "2048,24,50257,8192": {"batch_size": 36},
}


def _read_config_safe(model_dir):
    """Read config.json — fail-soft. Returns dict or None."""
    if not model_dir:
        return None
    try:
        cfg_path = os.path.join(model_dir, "config.json")
        if not os.path.exists(cfg_path):
            return None
        with open(cfg_path) as f:
            return json.load(f)
    except Exception:
        return None


def _fingerprint_key(cfg):
    """Build catalog fingerprint key from config dict."""
    return ",".join(str(cfg.get(k, "")) for k in
                    ("hidden_size", "num_hidden_layers", "vocab_size", "intermediate_size"))

INSTRUCT_CONFIG = {
    "0_1_b": {
        "lr": 0.0001,
        "distributed": "ddp",
        "gpu_count": 1,
        "batch_size": 140,
        "use_lora": False,
    },
    "1_2_b": {
        "lr": 0.0001,
        "distributed": "ddp",
        "gpu_count": 1,
        "use_lora": False,
        "batch_size": 100,
    },
    "2_4_b": {
        "lr": 7.5e-5,
        "distributed": "ddp",
        "gpu_count": 1,
        "batch_size": 48,
    },
    "4_5_b": {
        "lr": 7e-5,
        "distributed": "ddp",
        "gpu_count": 2,
        "batch_size": 40,
    },
    "5_9_b": {
        "lr": 3.5e-5,
        "distributed": "ddp",
        "gpu_count": 2,
        "batch_size": 28,
    },
    "9_12_b": {
        "lr": 1e-4,
        "distributed": "ddp",
        "gpu_count": 2,
        "use_lora": True,
        "batch_size": 32,
    },
    "12_15_b": {
        "lr": 1e-4,
        "distributed": "ds",
        "gpu_count": 4,
        "use_lora": True,
        "batch_size": 30,
    },
    "15_40_b": {
        "lr": 8e-5,
        "distributed": "ds",
        "gpu_count": 4,
        "use_lora": True,
        "batch_size": 18,
    },
    "40_80_b": {
        "lr": 8e-5,
        "distributed": "ds",
        "gpu_count": 8,
        "use_lora": True,
        "batch_size": 8,
    },
}

for key in INSTRUCT_CONFIG:
    INSTRUCT_CONFIG[key]["label"] = key


def get_instruct_config(param_nums: int) -> dict:
    result = {
        "lr": 4e-5,
        "distributed": "ds",
        "gpu_count": 8,
        "batch_size": 6,
        "use_lora": True,
    }
    if param_nums < 1_000_000_000:
        result = INSTRUCT_CONFIG["0_1_b"]
    elif param_nums < 2_000_000_000:
        result = INSTRUCT_CONFIG["1_2_b"]
    elif param_nums < 4_000_000_000:
        result = INSTRUCT_CONFIG["2_4_b"]
    elif param_nums < 5_000_000_000:
        result = INSTRUCT_CONFIG["4_5_b"]
    elif param_nums < 9_000_000_000:
        result = INSTRUCT_CONFIG["5_9_b"]
    elif param_nums < 12_000_000_000:
        result = INSTRUCT_CONFIG["9_12_b"]
    elif param_nums < 15_000_000_000:
        result = INSTRUCT_CONFIG["12_15_b"]
    elif param_nums < 35_000_000_000:
        result = INSTRUCT_CONFIG["15_40_b"]
    elif param_nums < 80_000_000_000:
        result = INSTRUCT_CONFIG["40_80_b"]
    else:
        print(f"Model size {param_nums} is not supported")
    result = deepcopy(result)
    if param_nums < 9_000_000_000 and param_nums > 8_000_000_000:
        result["batch_size"] = int(2 * result["batch_size"] / 3)
    return result


def get_run_cmd(config: dict, gpu_nums: int):
    required_keys = [
        "epoch_num",
        "batch_size",
        "learning_rate",
        "min_lr_rate",
        "use_liger",
        "optimizer",
        "use_lora",
        "packing",
        "disable_fa",
    ]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Required key {key} not found in config")

    gpu_nums = get_gpu_count()
    start_cmd = "python"
    run_type = config["distributed"]
    if gpu_nums > 1 and run_type == "ddp":
        start_cmd = f"torchrun --nproc_per_node={gpu_nums}"
    elif run_type == "ds":
        start_cmd = f"deepspeed"

    template = (
        start_cmd
        + """ train_instruct.py \
    --request_path {request_path} \
    --bf16 True \
    --report_to wandb \
    --output_dir {output_dir} \
    --num_train_epochs {epoch_num} \
    --per_device_train_batch_size {batch_size} \
    --per_device_eval_batch_size 1 \
    --gradient_accumulation_steps {gradient_accumulation_steps} \
    --eval_accumulation_steps 1 \
    --eval_strategy no \
    --save_strategy epoch \
    --logging_steps 5 \
    --learning_rate {learning_rate} \
    --weight_decay {weight_decay} \
    --label_smoothing_factor {label_smoothing} \
    --warmup_steps {warmup_steps} \
    --lr_scheduler_type cosine_with_min_lr \
    --lr_scheduler_kwargs "{\\"min_lr_rate\\": {min_lr_rate}}" \
    --tf32 True \
    --gradient_checkpointing {gradient_checkpointing} \
    --optim {optimizer} \
    --use_liger {use_liger} \
    --neftune_noise_alpha {neftune_noise_alpha} \
    --packing {packing} --disable_fa {disable_fa}"""
    )
    if run_type == "ds":
        template = template + """ --deepspeed ds_config/zero3.json"""

    # Multi-GPU DDP + gradient_checkpointing requires find_unused_parameters to
    # avoid the "Expected to mark a variable ready only once" RuntimeError.
    # Use_reentrant=False is set in train_instruct.py (cleaner than JSON via CLI).
    if gpu_nums > 1 and run_type == "ddp":
        template = template + """ --ddp_find_unused_parameters True"""

    if config["use_lora"]:
        template = template + """ --use_lora True"""

    for key, value in config.items():
        template = template.replace("{" + key + "}", str(value))

    if config.get("use_attn_implementation", ""):
        use_attn_implementation = config["use_attn_implementation"]
        template = (
            template + f""" --use_attn_implementation {use_attn_implementation}"""
        )

    return template


def get_training_json(train_info: dict) -> dict:
    model_name = train_info["model_name"]
    model_path = train_info["model_path"]
    model_architecture = get_model_architecture(model_path)
    param_nums = get_model_num_params(model_name, model_path)
    config = get_instruct_config(param_nums)
    # NEW DEFAULTS (proven across 2 tournament tasks — 2026-04-22 experiments):
    #   epoch_num: 3 -> 2   (best checkpoint already at or before epoch 2 in both
    #                        tasks tested; epoch 3 caused +12% overfit on Task B)
    #   weight_decay: 0.0 -> 0.01  (AdamW standard, -0.85% on Task B, neutral
    #                               on Task A, low risk)
    #   label_smoothing: 0.0 (UNCHANGED — large vocab trap for causal LM;
    #                         +4.48% regression on Llama-3 128K vocab)
    # Override via env vars INSTRUCT_EPOCHS, INSTRUCT_WEIGHT_DECAY,
    # INSTRUCT_LABEL_SMOOTHING.
    run_config = {
        "epoch_num": 2,
        "batch_size": config["batch_size"],
        "learning_rate": config["lr"],
        "min_lr_rate": 0.25,
        "use_liger": get_use_liger(model_architecture),
        "optimizer": "paged_adamw_8bit",
        "use_lora": config.get("use_lora", False),
        "disable_fa": disable_flash_attention(model_architecture, model_name, model_dir=model_path),
        "packing": "True",
        "gpu_nums": config["gpu_count"],
        "output_dir": train_info["output_dir"],
        "request_path": train_info["request_path"],
        "distributed": config.get("distributed", "ddp"),
        "gradient_checkpointing": "True",
        "gradient_accumulation_steps": 4,
        "warmup_steps": int(os.getenv("INSTRUCT_WARMUP_STEPS", "35")),
        "weight_decay": 0.01,
        "label_smoothing": 0.0,
        # NEFTune noise (lotob-neftune branch): default 5.0 (paper recommendation
        # for 7B+; smaller models tolerate similar values). Adds noise to input
        # embeddings during forward pass. Source: arxiv 2310.05914 (Jain 2023).
        # Set 0.0 to disable. Env override NEFTUNE_NOISE_ALPHA.
        "neftune_noise_alpha": float(os.getenv("NEFTUNE_NOISE_ALPHA", "5.0")),
        "use_attn_implementation": (
            "kernels-community/vllm-flash-attn3"
            if train_info.get("is_openai", False)
            else ""
        ),
    }

    # Env overrides (for experiments — default values above are the proven
    # tournament config). Kept backward-compat with INSTRUCT_REGULARIZATION
    # flag but no longer gated behind it.
    if os.getenv("INSTRUCT_WEIGHT_DECAY"):
        try:
            run_config["weight_decay"] = float(os.getenv("INSTRUCT_WEIGHT_DECAY"))
        except ValueError:
            pass
    if os.getenv("INSTRUCT_LABEL_SMOOTHING"):
        try:
            run_config["label_smoothing"] = float(os.getenv("INSTRUCT_LABEL_SMOOTHING"))
        except ValueError:
            pass
    if os.getenv("INSTRUCT_EPOCHS"):
        try:
            run_config["epoch_num"] = int(os.getenv("INSTRUCT_EPOCHS"))
        except ValueError:
            pass

    print(
        f"[instruct_config] config: epoch_num={run_config['epoch_num']}, "
        f"weight_decay={run_config['weight_decay']}, "
        f"label_smoothing={run_config['label_smoothing']}",
        flush=True,
    )

    # there are models that do not support packing, so we need to check if the model supports packing
    if run_config["disable_fa"] == "True" or model_architecture.strip().lower() in [
        "optforcausallm"
    ]:
        run_config["packing"] = "False"

    # data_size = get_data_size(train_info["request_path"])

    # if run_config["disable_fa"]: # if FA is not usable
    #     run_config["batch_size"] = run_config["batch_size"] * 2

    # Tier 1: name-based (works pre-merge / direct model_name)
    if model_name in FIXED_BS_CONFIG:
        run_config["batch_size"] = FIXED_BS_CONFIG[model_name]["batch_size"]
    else:
        # Tier 2: fingerprint-based (anonymization-safe). Reads config.json
        # at model_path and matches preserved architecture-defining fields.
        cfg = _read_config_safe(model_path)
        if cfg is not None:
            fp = _fingerprint_key(cfg)
            if fp in FIXED_BS_BY_FINGERPRINT:
                run_config["batch_size"] = FIXED_BS_BY_FINGERPRINT[fp]["batch_size"]

    if model_architecture.strip().lower() in [
        "gptneoxforcausallm",
        "gptjforcausallm",
        "phiforcausallm",
        "falconforcausallm",
    ]:
        run_config["batch_size"] = int(run_config["batch_size"] // 2)
        if model_name == "EleutherAI/pythia-160m":  # reduce more
            run_config["batch_size"] = int(run_config["batch_size"] / 1.5)
        elif "pythia" in model_name.lower():
            run_config["batch_size"] = int(run_config["batch_size"] / 1.8)

    if model_name in ["microsoft/phi-2", "microsoft/phi-1_5"]:
        run_config["batch_size"] = int(run_config["batch_size"] / 4)

    if "bloom-560m" in model_name or "bloomz-560m" in model_name:
        run_config["batch_size"] = 8

    if model_name == "mistralai/Mistral-7B-v0.1":
        run_config["batch_size"] = int(3 * run_config["batch_size"] / 4)

    if "falcon" in model_name.lower():
        run_config["batch_size"] = int(run_config["batch_size"] / 2)

    data_per_step = run_config["batch_size"] * run_config["gpu_nums"]
    if data_per_step >= 64:
        run_config["gradient_accumulation_steps"] = 1
    else:
        run_config["gradient_accumulation_steps"] = int(64 / data_per_step)

    if model_architecture.strip().lower() in ["gptossforcausallm"]:
        run_config["use_lora"] = False  # currently, gptoss does not support lora

    if train_info["find_lk_lr"]:
        # get lr from lrs_lookup.py — pass model_dir for post-anonymization
        # detection fallback (recover original model_id via fingerprint match
        # against model_fingerprint_catalog.json).
        lr = get_instruct_lr(model_name, model_dir=model_path)
        if lr is not None:
            print(f"Using lr from lk (tier 1/2 hash): {lr}", flush=True)
            run_config["learning_rate"] = lr
        else:
            # EXP-LLM-WARMSTART 2026-05-27: Tier 1.7 — LLM advisor (Qwen-14B-AWQ
            # vLLM sidecar) suggests LR from model/task/size context.
            warmstart_lr = None
            try:
                dataset_size = None
                try:
                    dataset_size = get_data_size(train_info["request_path"])
                except Exception as _e:
                    print(f"[warmstart] data size lookup failed: {_e}", flush=True)
                warmstart_lr = try_llm_warmstart(
                    model_name=model_name,
                    task_type="InstructTextTask",
                    param_nums=param_nums,
                    dataset_size=dataset_size,
                    hours_to_complete=train_info.get("hours_to_complete"),
                )
            except Exception as _exc:
                print(f"[warmstart] unexpected error, falling back: {_exc}", flush=True)

            if warmstart_lr is not None:
                print(f"Using lr from LLM warmstart (tier 1.7): {warmstart_lr}", flush=True)
                run_config["learning_rate"] = warmstart_lr
            else:
                # EXP-BOSS-1 (2026-05-20): Tier 3 AR-CSV fallback ported from
                # BOSS lion_dance_1 (commit 249e0e7 2026-05-14). Anonymization-
                # resistant: matches by (architecture, closest_param_size).
                ar_lr = get_lr_from_ar_instruct(model_architecture, param_nums)
                if ar_lr is not None:
                    print(f"Using lr from AR-CSV (tier 3 fallback): {ar_lr} "
                          f"(arch={model_architecture}, params={param_nums})", flush=True)
                    run_config["learning_rate"] = ar_lr
                else:
                    print(f"Using lr from config: {run_config['learning_rate']}", flush=True)

    run_config["learning_rate"] *= train_info["reg_ratio"]
    run_cmd = get_run_cmd(run_config, run_config["gpu_nums"])
    train_request = deepcopy(train_info)
    train_request["save_before_remaining_time"] = 3
    train_request["adjust_batch_size"] = False
    train_request["periodic_save_steps"] = 500
    # BOSS-9 (2026-05-21): Dynamic checking_step per (param, hours).
    # Source: lion_dance_1/scripts/instruct_config.py:191-194.
    # Small models (<=3B) on long runs (>=2h) need more eval frequency (140)
    # for plateau detection; larger models / shorter runs use default 70.
    def _get_checking_step(param_nums: int, hours_to_complete) -> int:
        if param_nums <= 3_000_000_000 and hours_to_complete >= 2:
            return 140
        return 70
    train_request["checking_step"] = _get_checking_step(param_nums, train_info["hours_to_complete"])

    # Native max_length: per-task auto-halve matching validator behavior.
    # Opt out via INSTRUCT_SKIP_MAX_LENGTH=1 (original winner fallback to YAML 2048).
    if os.getenv("INSTRUCT_SKIP_MAX_LENGTH") != "1":
        resolved = _resolve_max_length(model_path)
        if resolved is not None:
            train_request["max_length"] = resolved
            print(
                f"[instruct_config] max_length={resolved} "
                f"(validator-aligned auto-halve)",
                flush=True,
            )

    if param_nums < 1_000_000_000:
        train_request["min_steps"] = max(
            int(train_info["hours_to_complete"] * 100), train_request["min_steps"]
        )

    elif param_nums < 9_000_000_000:
        train_request["min_steps"] = max(
            int(train_info["hours_to_complete"] * 70), train_request["min_steps"]
        )

    return {"train_request": train_request, "run_cmd": run_cmd}
