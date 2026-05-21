import json
import os
from model_utility import (
    get_model_architecture,
    get_model_num_params,
    get_use_liger,
    disable_flash_attention,
    get_use_vllm,
    get_gradient_checkpointing,
    get_gpu_count,
)
from copy import deepcopy
from lrs_lookup import get_grpo_lr, get_grpo_python_lr
allow_find_lk_lr = False

GRPO_CONFIG = {
    "0_1_b": {
        "lr": 8e-6,
        "distributed": "ddp",
        "gpu_count": 1,
        "batch_size": 40,
        "vllm_gpu_memory_utilization": 0.4,
    },
    "1_2_b": {
        "lr": 8e-6,
        "distributed": "ddp",
        "gpu_count": 1,
        "batch_size": 40,
        "vllm_gpu_memory_utilization": 0.4,
    },
    "2_4_b": {
        "lr": 8e-6,
        "distributed": "ddp",
        "gpu_count": 2,
        "batch_size": 42,
        "vllm_gpu_memory_utilization": 0.35,
        "use_lora": True,
    },
    "4_5_b": {
        "lr": 6e-6,
        "distributed": "ddp",
        "gpu_count": 2,
        "batch_size": 42,
        "use_lora": True,
        "vllm_gpu_memory_utilization": 0.4,
    },
    "5_6_b": {
        "lr": 6e-6,
        "distributed": "ddp",
        "gpu_count": 2,
        "batch_size": 42,
        "use_lora": True,
        "vllm_gpu_memory_utilization": 0.4,
    },
    "6_9_b": {
        "lr": 6e-6,
        "distributed": "ddp",
        "gpu_count": 4,
        "batch_size": 24,
        "use_lora": True,
        "vllm_gpu_memory_utilization": 0.5,
    },
    "9_12_b": {
        "lr": 6e-6,
        "distributed": "ddp",
        "gpu_count": 4,
        "use_lora": True,
        "batch_size": 16,
        "vllm_gpu_memory_utilization": 0.6,
    },
    "12_15_b": {
        "lr": 5e-6,
        "distributed": "ddp",
        "gpu_count": 4,
        "use_lora": True,
        "batch_size": 2,
        "vllm_gpu_memory_utilization": 0.8,
    },
    "15_20_b": {
        "lr": 5e-6,
        "distributed": "ddp",
        "gpu_count": 4,
        "use_lora": True,
        "batch_size": 16,
        "vllm_gpu_memory_utilization": 0.6,
        "use_vllm": False,
    },
    "20_40_b": {
        "lr": 4e-6,
        "distributed": "ddp",
        "gpu_count": 8,
        "use_lora": True,
        "batch_size": 16,
        "vllm_gpu_memory_utilization": 0.6,
        "use_vllm": False,
        "use_4bit": True,
    },
    "40_80_b": {
        "lr": 3e-6,
        "distributed": "ddp",
        "gpu_count": 8,
        "use_lora": True,
        "batch_size": 2,
        "vllm_gpu_memory_utilization": 0.7,
        "use_vllm": False,
        "use_4bit": True,
    },
}

for key in GRPO_CONFIG:
    GRPO_CONFIG[key]["label"] = key


def if_contain_slow_reward_function(dataset_type: dict) -> bool:
    reward_functions = dataset_type["reward_functions"]
    for reward_func in reward_functions:
        func_def = reward_func["reward_func"]
        keywords = [
            "import langcheck",
            "from langcheck",
            "import detoxify",
            "from detoxify",
            "import textstat",
            "from textstat",
        ]
        if any(keyword in func_def for keyword in keywords):
            return True
    return False


def get_grpo_config(param_nums: int) -> dict:
    if param_nums < 1_000_000_000:
        return GRPO_CONFIG["0_1_b"]
    elif param_nums < 2_000_000_000:
        return GRPO_CONFIG["1_2_b"]
    elif param_nums < 4_000_000_000:
        return GRPO_CONFIG["2_4_b"]
    elif param_nums < 5_000_000_000:
        return GRPO_CONFIG["4_5_b"]
    elif param_nums < 6_000_000_000:
        return GRPO_CONFIG["5_6_b"]
    elif param_nums < 9_000_000_000:
        return GRPO_CONFIG["6_9_b"]
    elif param_nums < 12_000_000_000:
        return GRPO_CONFIG["9_12_b"]
    elif param_nums < 15_000_000_000:
        return GRPO_CONFIG["12_15_b"]
    elif param_nums < 20_000_000_000:
        return GRPO_CONFIG["15_20_b"]
    elif param_nums < 40_000_000_000:
        return GRPO_CONFIG["20_40_b"]
    elif param_nums < 80_000_000_000:
        return GRPO_CONFIG["40_80_b"]
    else:
        print(f"Model size {param_nums} is not supported")
        return {
            "lr": 4e-5,
            "distributed": "ds",
            "gpu_count": 8,
            "batch_size": 6,
            "use_lora": True,
        }


def contain_python_execution(dataset_type: dict) -> bool:
    reward_functions = dataset_type["reward_functions"]
    for reward_func in reward_functions:
        func_def = reward_func["reward_func"]
        keywords = ["sat_reward_function", "ded_reward_function", "abd_reward_function"]
        if any(keyword in func_def for keyword in keywords):
            return True
    return False


def get_run_cmd(config: dict, gpu_nums: int):
    required_keys = [
        "epoch_num",
        "batch_size",
        "learning_rate",
        "min_lr_rate",
        "use_liger",
        "optimizer",
        "vllm_gpu_memory_utilization",
        "num_generations",
        "disable_fa",
        "loss_type",       # EXPERIMENTAL 2026-05-21 (Dr.GRPO plumbing)
        "scale_rewards",   # EXPERIMENTAL 2026-05-21 (Dr.GRPO plumbing)
    ]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Required key {key} not found in config")

    start_cmd = "python"
    run_type = config["distributed"]
    # if gpu_nums > 1 and run_type == "ddp":
    gpu_nums = get_gpu_count()
    start_cmd = f"torchrun --nproc_per_node={gpu_nums}"
    if run_type == "ds":
        start_cmd = f"deepspeed"

    template = (
        start_cmd
        + """ train_grpo.py \
    --request_path {request_path} \
    --bf16 True \
    --report_to wandb \
    --output_dir /workspace/data/trained_model \
    --num_train_epochs {epoch_num} \
    --per_device_train_batch_size {batch_size} \
    --per_device_eval_batch_size {eval_batch_size} \
    --gradient_accumulation_steps {gradient_accumulation_steps} \
    --eval_accumulation_steps 1 \
    --eval_strategy no \
    --save_strategy no \
    --logging_steps 5 \
    --learning_rate {learning_rate} \
    --weight_decay 0. \
    --warmup_steps 35 \
    --lr_scheduler_type constant \
    --tf32 True \
    --gradient_checkpointing {gradient_checkpointing} \
    --optim {optimizer} \
    --use_liger {use_liger} --num_generations {num_generations} --vllm_gpu_memory_utilization {vllm_gpu_memory_utilization} \
    --max_completion_length {max_completion_length} \
    --max_steps {max_steps} \
    --beta {beta} \
    --temperature {temperature} \
    --top_p {top_p} \
    --auto_find_batch_size False \
    --dataloader_drop_last True \
    --disable_fa {disable_fa}"""
    )

    if config.get("use_lora", False):
        template += (
            # EXP-3 2026-05-21: lora_r 128→64, lora_alpha 256→32. Data: paper 2502.07374
            # (Berkeley + NovaSky-AI) explicit r=64 worked for 32B distillation. Verl
            # handbook (Qwen2.5-3B GRPO) uses r=64, alpha=32. "LoRA Without Regret"
            # (Thinking Machines): rank-1 sufficient for RL, apply to all-linear.
            # Smaller adapter = less parameter capacity = anti-reward-hack natural floor.
            # alpha=32 follows Verl ratio α=0.5r (more conservative scaling vs our previous α=2r).
            " --use_peft --lora_r 64 --lora_alpha 32 --lora_target_modules all-linear"
        )

    if config.get("use_vllm", True):
        # EXPERIMENTAL 2026-05-21: --vllm_mode colocate (single-container, avoids
        # cross-container NCCL crash) + Dr.GRPO loss_type plumbing (TRL 0.18
        # supports loss_type='dr_grpo' + scale_rewards=False per Dr.GRPO paper).
        # Memory ref: exp_trl_dr_grpo_finding_2026_05_20.md
        template += " --use_vllm True --vllm_mode colocate --loss_type {loss_type} --scale_rewards {scale_rewards}"
    else:
        template += " --use_vllm False"

    if run_type == "ds":
        template = template + """ --deepspeed ds_config/zero3.json"""

    for key, value in config.items():
        template = template.replace("{" + key + "}", str(value))

    if config.get("tensor_parallel", False):
        template = template + f" --vllm_tensor_parallel_size {gpu_nums}"

    if config.get("use_4bit", False):
        template = (
            template
            + " --load_in_4bit True --use_bnb_nested_quant True --bnb_4bit_quant_type nf4"
        )
    return template


def get_training_json(train_info: dict) -> dict:
    model_name = train_info["model_name"]
    model_path = train_info["model_path"]
    model_architecture = get_model_architecture(model_path)
    param_nums = get_model_num_params(model_name, model_path)
    config = get_grpo_config(param_nums)
    print(f"config: {config}")
    run_config = {
        "epoch_num": 2,
        "batch_size": config["batch_size"],
        "learning_rate": config["lr"],
        "min_lr_rate": 0.25,
        "use_liger": get_use_liger(model_architecture),
        "optimizer": "paged_adamw_8bit",
        "use_lora": config.get("use_lora", False),
        "disable_fa": disable_flash_attention(model_architecture, model_name, model_dir=model_path),
        "gpu_nums": config["gpu_count"],
        "output_dir": train_info["output_dir"],
        "request_path": train_info["request_path"],
        "distributed": config.get("distributed", "ddp"),
        "gradient_checkpointing": get_gradient_checkpointing(model_name, model_dir=model_path),
        "gradient_accumulation_steps": 4,
        "vllm_gpu_memory_utilization": config.get("vllm_gpu_memory_utilization", 0.4),
        "num_generations": 5,  # EXP-1 2026-05-21: 2→5 per Verl handbook ablation (sweet spot, N=10 marginal +70% cost). Data ref: research_sea_ai_lab_grpo_2026_05_19.md
        "max_completion_length": 256,
        "max_steps": -1,  # legacy: epoch-based, no step cap
        "beta": 0.04,  # legacy TRL default
        "temperature": 1.0,  # TRL default
        "top_p": 1.0,  # TRL default
        "use_vllm": get_use_vllm(model_architecture, model_name, model_dir=model_path),
        "tensor_parallel": config.get("tensor_parallel", False),
        "use_4bit": config.get("use_4bit", False),
        # EXPERIMENTAL 2026-05-21: Dr.GRPO loss correction (Sea AI Lab paper 2503.20783)
        # loss_type='dr_grpo' removes length-bias from GRPO advantage (sum/max_response_length
        # instead of mean/per-completion-len). scale_rewards=False per Dr.GRPO paper
        # (removes per-group std division that biases group baseline).
        # TRL 0.18 supports both natively. Memory ref: exp_trl_dr_grpo_finding_2026_05_20.md
        "loss_type": "dr_grpo",
        "scale_rewards": False,
    }

    if model_name == "OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5":
        run_config["use_lora"] = True

    # starcoder batch reduction. Detection: name match (pre-merge) OR
    # config-based fingerprint (anonymization-safe).
    # StarCoder: GPTBigCodeForCausalLM is the distinctive architectures field.
    _is_starcoder = "starcoder" in model_name.lower()
    if not _is_starcoder:
        try:
            cfg_path = os.path.join(model_path, "config.json") if model_path else None
            if cfg_path and os.path.exists(cfg_path):
                with open(cfg_path) as _f:
                    _cfg = json.load(_f)
                _arch = (_cfg.get("architectures") or [""])[0]
                if _arch == "GPTBigCodeForCausalLM":
                    _is_starcoder = True
        except Exception:
            pass
    if _is_starcoder:
        run_config["batch_size"] = int(run_config["batch_size"] / 1.5)

    train_request = deepcopy(train_info)
    train_request["save_before_remaining_time"] = 3
    train_request["min_steps"] = 100
    train_request["adjust_batch_size"] = False
    train_request["periodic_save_steps"] = 500

    if if_contain_slow_reward_function(train_info["dataset_type"]):
        train_request["save_before_remaining_time"] = 12
        if config["label"] == "0_1_b":
            run_config["batch_size"] = 8
        elif config["label"] == "1_2_b":
            run_config["batch_size"] = 10
        elif config["label"] == "2_4_b":
            run_config["batch_size"] = 16
        elif config["label"] == "4_5_b":
            run_config["batch_size"] = 16
        elif config["label"] == "5_6_b":
            run_config["batch_size"] = 16
        elif config["label"] == "6_9_b":
            run_config["batch_size"] = 16
            # gemma-2-9b-it OOM workaround. Detection: name match (pre-merge)
            # OR fingerprint (anonymization-safe).
            # gemma-2-9b: hidden=3584, layers=42, vocab=256000, intermediate=14336
            _is_gemma2_9b = model_name == "unsloth/gemma-2-9b-it"
            if not _is_gemma2_9b:
                try:
                    cfg_path = os.path.join(model_path, "config.json") if model_path else None
                    if cfg_path and os.path.exists(cfg_path):
                        with open(cfg_path) as _f:
                            _cfg = json.load(_f)
                        if (_cfg.get("hidden_size") == 3584 and _cfg.get("num_hidden_layers") == 42
                                and _cfg.get("vocab_size") == 256000):
                            _is_gemma2_9b = True
                except Exception:
                    pass
            if _is_gemma2_9b:
                run_config["batch_size"] = 8
        elif config["label"] == "9_12_b":
            run_config["batch_size"] = 16
        elif config["label"] == "12_15_b":
            run_config["batch_size"] = 2
        elif config["label"] == "15_20_b":
            run_config["batch_size"] = 2
        elif config["label"] == "20_40_b":
            run_config["batch_size"] = 16  # this is high because we use 4bit
        elif config["label"] == "40_80_b":
            run_config["batch_size"] = 2

        elif config["label"] == "13_15_b":
            run_config["batch_size"] = 12

    total_batch_size = run_config["batch_size"] * run_config["gpu_nums"]
    if total_batch_size < 64:
        run_config["gradient_accumulation_steps"] = min(4, int(64 / total_batch_size))

    run_config["eval_batch_size"] = 4
    if run_config["batch_size"] <= 4:
        run_config["eval_batch_size"] = 2

    if not config.get("use_vllm", True):
        run_config["use_vllm"] = False

    lookup_hit = False
    classifier_hit = False
    if train_info["find_lk_lr"] and allow_find_lk_lr:
        # TIER 1: exact-match empirical lookup from lrs_lookup.py
        has_python_execution = contain_python_execution(train_info["dataset_type"])
        if not has_python_execution:
            lr = get_grpo_lr(model_name, model_dir=model_path)
            print(f"Using lr from lk not python: {lr}", flush=True)
        else:
            lr = get_grpo_python_lr(model_name, model_dir=model_path)
            print(f"Using lr from lk python: {lr}", flush=True)
        if lr is not None:
            print(f"Using lr from lk (tier 1): {lr}", flush=True)
            run_config["learning_rate"] = lr
            lookup_hit = True
        else:
            print(f"Using lr from config: {run_config['learning_rate']}", flush=True)

    # TIER 1.5: GRPO reward-function fingerprint classifier (lotob-grpo-hard).
    # Static analysis of reward_functions list → suggests LR + β by reward
    # mix landscape. Generic 13-function catalog covers ~90% of tournament
    # tasks. Fail-soft + opt-out via TRAINING_REWARD_CLASSIFIER_ENABLED=0.
    if not lookup_hit:
        reward_fns = (train_info.get("dataset_type") or {}).get(
            "reward_functions", []
        )
        if reward_fns and os.getenv(
            "TRAINING_REWARD_CLASSIFIER_ENABLED", "true"
        ).lower() not in ("0", "false", "no"):
            try:
                from reward_classifier import (
                    classify_reward_mix,
                    describe,
                    suggest_params,
                )
                fingerprint = classify_reward_mix(reward_fns)
                classifier_params = suggest_params(
                    fingerprint,
                    model_size_b=(param_nums / 1e9) if param_nums else None,
                )
                if classifier_params is not None:
                    run_config["learning_rate"] = classifier_params["learning_rate"]
                    run_config["beta"] = classifier_params["beta"]
                    print(
                        f"[classifier] tier 1.5 hit: lr="
                        f"{classifier_params['learning_rate']:.2e} "
                        f"beta={classifier_params['beta']:.3f} "
                        f"({describe(fingerprint)})",
                        flush=True,
                    )
                    classifier_hit = True
                else:
                    print(
                        f"[classifier] no match (unknown reward funcs): "
                        f"{describe(fingerprint)}",
                        flush=True,
                    )
            except Exception as exc:
                print(
                    f"[classifier] error, fail-soft: "
                    f"{type(exc).__name__}: {exc}",
                    flush=True,
                )

    # β floor for large GRPO (7B+). Empirical from tournament observation:
    # 0/3 GRPO 7B+ wins on tourn_f4f456bc6d050b8b_20260430 — pattern shows
    # larger models drift faster from reference under the same β.
    # Bumping β → stronger KL anchor → less drift → ckpt closer to ref.
    # Env: TRAINING_GRPO_BETA_FLOOR_LARGE_7B (default 0.10),
    #      TRAINING_GRPO_LARGE_THRESHOLD (default 7e9).
    try:
        _large_threshold = float(os.getenv("TRAINING_GRPO_LARGE_THRESHOLD", "7000000000"))
        if param_nums >= _large_threshold:
            _large_floor = float(os.getenv("TRAINING_GRPO_BETA_FLOOR_LARGE_7B", "0.10"))
            _current_beta = run_config.get("beta", 0.04)
            if _current_beta < _large_floor:
                run_config["beta"] = _large_floor
                print(f"[beta-floor-large] {param_nums/1e9:.1f}B model >= {_large_threshold/1e9:.0f}B threshold: beta {_current_beta:.3f} -> {_large_floor:.3f}", flush=True)
    except (TypeError, ValueError) as exc:
        print(f"[beta-floor-large] skipped (fail-soft): {exc}", flush=True)

    run_config["learning_rate"] *= train_info["reg_ratio"]

    run_cmd = get_run_cmd(run_config, run_config["gpu_nums"])

    return {"train_request": train_request, "run_cmd": run_cmd}
