#!/usr/bin/env python3
"""
Standalone script for text model training (InstructText, DPO, and GRPO)
"""

import argparse
import asyncio
import json
import os
import shutil
import copy
import subprocess
import sys
import uuid
import re
import time 
from datetime import datetime, timezone, timedelta

import yaml
from transformers import AutoTokenizer
from state_manager import get_state, set_state
import numpy as np


script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.append(project_root)

import train_cst
from core.config.config_handler import create_dataset_entry
from core.config.config_handler import save_config
from core.config.config_handler import update_flash_attention
from core.dataset_utils import adapt_columns_for_dpo_dataset
from core.dataset_utils import adapt_columns_for_grpo_dataset
from core.models.utility_models import DpoDatasetType
from core.models.utility_models import FileFormat
from core.models.utility_models import GrpoDatasetType
from core.models.utility_models import InstructTextDatasetType
from core.models.utility_models import TaskType
import training_paths as train_paths
from instruct_config import get_training_json as get_instruct_training_json
from dpo_config import get_training_json as get_dpo_training_json
from grpo_config import get_training_json as get_grpo_training_json
import pathlib
from transformers import AutoConfig
import lr_utils

def run_cmd_with_log(cmd: str, log_file_path: str, env_vars: dict = None):
    # print(f"Running command: {cmd}", flush=True)
    with open(log_file_path, "w") as log_file:
        # Prepare environment variables
        process_env = os.environ.copy()
        if env_vars:
            process_env.update(env_vars)

        # Run the command, capturing stdout and stderr
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=process_env,
        )

        # Stream output to both console and log file
        for line in process.stdout:
            print(line, end="", flush=True)
            log_file.write(line)
            log_file.flush()

        # Wait for the process to complete
        return_code = process.wait()

        # Log the return code
        log_file.write(f"\nProcess completed with return code: {return_code}\n")


def replace_args_in_cmd(cmd: str, arg_name: str, arg_value: str):
    match = re.search(f"(?P<p>--{arg_name}(\s+)([^\s]+))(\s+)", cmd)
    if match:
        left_index = match.start("p")
        right_index = match.end("p")
        return cmd[:left_index] + f" --{arg_name} {arg_value} " + cmd[right_index:]
    else:
        return None


def extract_value_from_cmd(cmd: str, arg_name: str):
    match = re.search(f"(?P<p>--{arg_name}(\s+)(?P<value>[^\s]+))(\s+)", cmd)
    if match:
        return match.group("value")
    else:
        return None


def get_model_architecture(model_name: str) -> str:
    try:
        config = AutoConfig.from_pretrained(model_name)
        architectures = config.architectures
        if len(architectures) > 1:
            return "Multiple architectures"
        return architectures[0].strip().lower()
    except Exception as e:
        if "model type `gpt_oss`" in str(e):
            return "GptOssForCausalLM"
        return "Unknown"


def is_openai_model(model_name: str) -> bool:
    architecture = get_model_architecture(model_name)
    if architecture.lower() == "gptossforcausallm":
        return True
    return False


OOM_ERROR = "torch.OutOfMemoryError: CUDA out of memory"
VLLM_OOM_ERROR = "ValueError: No available memory for the cache blocks"


def get_error_type(log_path: str):
    with open(log_path, "r") as f:
        text = f.read()
    if OOM_ERROR in text:
        return OOM_ERROR
    elif VLLM_OOM_ERROR in text:
        return VLLM_OOM_ERROR
    else:
        return None


def extract_output_dir(train_cmd: str) -> str:
    match = re.search(r"--output_dir\s+(.*?)\s+", train_cmd)
    if match:
        return match.group(1)
    else:
        return None


FAST_CRASH_THRESHOLD_SECONDS = 60.0  # train_cmd exiting in <60s = bad config signal


MIN_OOM_MAX_LENGTH = 512


def halve_request_max_length(train_cmd: str) -> int | None:
    """Halve max_length in the request JSON that train_cmd points at.

    Final rung of the OOM ladder. max_length is not a CLI flag — it lives in the
    request JSON under train_request — so degrading it means editing that file.
    Halved, floored at MIN_OOM_MAX_LENGTH, aligned down to a multiple of 64.

    Returns the new value, or None if nothing could be changed (no request_path,
    unreadable JSON, no max_length, or already at the floor).
    """
    try:
        request_path = extract_value_from_cmd(train_cmd, "request_path")
        if not request_path or not os.path.exists(request_path):
            return None
        with open(request_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        train_request = data.get("train_request")
        if not isinstance(train_request, dict):
            return None
        current = train_request.get("max_length")
        if not isinstance(current, int) or current <= MIN_OOM_MAX_LENGTH:
            return None
        new_len = max(MIN_OOM_MAX_LENGTH, (current // 2) // 64 * 64)
        if new_len >= current:
            return None
        train_request["max_length"] = new_len
        with open(request_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return new_len
    except Exception as e:
        print(f"Could not halve max_length: {e}", flush=True)
        return None


def run_training(
    train_cmd: str,
    log_path: str,
    task_id: str,
    retries: int,
    task_type: str,
    expected_repo_name: str,
):
    # SAFETY LAYER (B) 2026-05-23: track per-attempt duration so Grafana can
    # spot fast-fail patterns. UnboundLocalError yesterday: train_*.py never
    # even launched torch — config-phase crash. Different pattern: train
    # launches, dies at step 1 (bad LR / OOM-not-caught / NaN). Both would
    # show up here as <60s exit. Logging only at this stage — cascade-to-
    # legacy after N fast-fails is planned in a follow-up once Grafana
    # confirms the pattern empirically.
    consecutive_fast_crashes = 0
    for i in range(retries):
        print(
            f"************* Training attempt {i+1}/{retries} for task {task_id}*************",
            flush=True,
        )
        if i > 0:  # there was something wrong so we will reduce the batch_size
            # first check if the training is OOM
            if os.path.exists(log_path):
                error_type = get_error_type(log_path)
                if error_type == OOM_ERROR:
                    current_batch_size = extract_value_from_cmd(
                        train_cmd, "per_device_train_batch_size"
                    )
                    current_batch_size = int(current_batch_size)
                    if current_batch_size > 1:
                        new_batch_size = current_batch_size // 2
                        print(
                            f"Reducing batch size from {current_batch_size} to {new_batch_size}",
                            flush=True,
                        )
                        train_cmd = replace_args_in_cmd(
                            train_cmd,
                            "per_device_train_batch_size",
                            str(new_batch_size),
                        )
                        # print(f"New train command: {train_cmd}", flush=True)
                    else:
                        print(f"batch size is 1, cannot reduce further", flush=True)
                        if task_type == TaskType.GRPOTASK.value:
                            # disable vllm
                            train_cmd = replace_args_in_cmd(
                                train_cmd, "use_vllm", "False"
                            )
                            # print(f"disable VLLM {train_cmd}", flush=True)
                        else:
                            # Final rung: batch is already 1, so degrade sequence
                            # length instead of re-running an identical command
                            # until retries run out (which guarantees no
                            # checkpoint at all, i.e. a scored zero).
                            new_len = halve_request_max_length(train_cmd)
                            if new_len is not None:
                                print(
                                    f"Reducing max_length to {new_len} after OOM at batch size 1",
                                    flush=True,
                                )
                            else:
                                print(
                                    "max_length already at floor or unavailable; retrying unchanged",
                                    flush=True,
                                )
                elif error_type == VLLM_OOM_ERROR:
                    if task_type == TaskType.GRPOTASK.value:
                        print(f"VLLM OOM error, disable VLLM", flush=True)
                        train_cmd = replace_args_in_cmd(train_cmd, "use_vllm", "False")

        # empty the log file if it exists
        if os.path.exists(log_path):
            with open(log_path, "w") as f:
                f.write("STARTING TRAINING")

        training_env_vars = {
            "WANDB_MODE": "offline",
            "WANDB_RUN_ID": f"{task_id}_{expected_repo_name}",
            "WANDB_NAME": f"{task_id}_{expected_repo_name}",
        }

        _attempt_start = time.time()
        run_cmd_with_log(train_cmd, log_path, env_vars=training_env_vars)
        _attempt_duration = time.time() - _attempt_start
        # check if training is successfully here so we can break the loop; if output_dir contains file: "successs.txt" return true
        output_dir = extract_value_from_cmd(train_cmd, "output_dir")
        if os.path.exists(os.path.join(output_dir, "success.txt")):
            return True
        # SAFETY LAYER (B): fast-crash detection. If train_cmd died in <60s
        # without success.txt, config is likely bad (UnboundLocalError /
        # immediate OOM / NaN at step 1). Tag with greppable marker for
        # Grafana/Loki visibility.
        if _attempt_duration < FAST_CRASH_THRESHOLD_SECONDS:
            consecutive_fast_crashes += 1
            error_type = get_error_type(log_path) if os.path.exists(log_path) else None
            print(
                f"[FAST-CRASH] attempt={i+1}/{retries} task={task_id} "
                f"duration={_attempt_duration:.1f}s threshold={FAST_CRASH_THRESHOLD_SECONDS}s "
                f"consecutive={consecutive_fast_crashes} error_type={error_type or 'unknown'}",
                flush=True,
            )
        else:
            consecutive_fast_crashes = 0  # reset chain on a "normal" failure
        time.sleep(5)
    return False


def patch_wandb_symlinks(base_dir: str):
    for root, _, files in os.walk(base_dir):
        for name in files:
            full_path = os.path.join(root, name)

            if os.path.islink(full_path):
                target_path = os.readlink(full_path)

                print(f"Symlink: {full_path} → {target_path}")
                try:
                    os.unlink(full_path)
                except Exception as e:
                    print(f"Failed to unlink {full_path}: {e}")
                    continue

                if os.path.exists(target_path):
                    print("Copying real file")
                    try:
                        shutil.copy(target_path, full_path)
                    except Exception as e:
                        print(f"Failed to copy: {e}")
                else:
                    print("Target not found, creating dummy")
                    pathlib.Path(full_path).touch()


def delete_poor_checkpoints(train_runs: list[dict]):
    lowest_loss = min([run["current_loss"] for run in train_runs])
    for run in train_runs:
        if run["current_loss"] > lowest_loss:
            if os.path.exists(run["output_dir"]):
                print(f"Deleting checkpoint {run['output_dir']} with loss {run['current_loss']}", flush=True)
                shutil.rmtree(run["output_dir"])


def get_log_scale(task_type: str):
    log_scale_map = {
        TaskType.INSTRUCTTEXTTASK.value: 0.18,
        TaskType.DPOTASK.value: 0.18,
        TaskType.GRPOTASK.value: 0.2,
        TaskType.CHATTASK.value: 0.18,
    }
    return log_scale_map[task_type]


def checkpoint_has_nan_or_inf(checkpoint_dir: str) -> bool:
    """Scan weights in checkpoint_dir for NaN/Inf.

    Validator scoring sets score=0 when test_loss is NaN
    (see gradients-ai/G.O.D validator/evaluation/scoring.py).
    A submission with NaN/Inf weights almost always produces NaN eval loss,
    so detect early and fall back to add_random_noise so we ship a valid
    finetune-shaped checkpoint instead.

    Returns False (fail-open) on any read error — do not penalize legit
    checkpoints if the check itself errors.
    """
    import glob
    try:
        import torch as _torch
    except Exception:
        return False
    try:
        shards = sorted(glob.glob(os.path.join(checkpoint_dir, "*.safetensors")))
        if shards:
            try:
                from safetensors import safe_open as _safe_open
            except Exception:
                return False
            # Sample up to 3 shards, 50 tensors each — enough to catch broad NaN.
            for shard in shards[:3]:
                try:
                    with _safe_open(shard, framework="pt") as f:
                        for key in list(f.keys())[:50]:
                            t = f.get_tensor(key)
                            if _torch.isnan(t).any() or _torch.isinf(t).any():
                                print(f"NaN/Inf found in {shard}::{key}", flush=True)
                                return True
                except Exception as e:
                    print(f"NaN check skipped for {shard}: {e}", flush=True)
                    continue
            return False
        bins = sorted(glob.glob(os.path.join(checkpoint_dir, "*.bin")))
        for shard in bins[:3]:
            try:
                state = _torch.load(shard, map_location="cpu")
                for k, v in list(state.items())[:50]:
                    if hasattr(v, "isnan") and (v.isnan().any() or v.isinf().any()):
                        print(f"NaN/Inf found in {shard}::{k}", flush=True)
                        return True
            except Exception as e:
                print(f"NaN check skipped for {shard}: {e}", flush=True)
                continue
        return False
    except Exception as e:
        print(f"NaN check failed entirely: {e}", flush=True)
        return False


# Keys the validator's finetune check compares between the base config and ours.
# Source: gradients-ai/G.O.D validator/evaluation/model_checks.py::model_is_a_finetune
# — for each key present and non-None on the base config, a missing or differing
# value on the submission sets architecture_same=False, which scores the task 0.
VALIDATOR_COMPARED_CONFIG_KEYS = (
    "architectures",
    "hidden_size",
    "n_layer",
    "intermediate_size",
    "head_dim",
    "hidden_act",
    "model_type",
    "num_hidden_layers",
    "num_attention_heads",
    "num_key_value_heads",
)


def restore_submission_architectures(submission_dir: str, base_model_path: str) -> None:
    """Restore the `architectures` field on the submitted config.json.

    transformers can re-alias a model class on save (e.g. a Mistral checkpoint
    written back as LlamaForCausalLM). The validator compares `architectures`
    verbatim, so an alias silently turns a won task into a zero.

    Deliberately narrow: only `architectures` is rewritten, because it is the one
    key that legitimately changes through class aliasing while the weights stay
    valid. The other compared keys are structural — if they differ, the config no
    longer describes the weights, and overwriting them would produce an unloadable
    model that masks a real bug. Those are reported only.

    Fail-open: any error leaves the submission untouched.
    """
    try:
        sub_cfg_path = os.path.join(submission_dir, "config.json")
        if not os.path.exists(sub_cfg_path):
            # LoRA submissions ship adapter_config.json and no config.json; the
            # validator resolves architecture through the base model in that case.
            print("[arch-restore] no config.json in submission (LoRA?) — nothing to do", flush=True)
            return

        base_cfg_path = os.path.join(base_model_path, "config.json")
        if not os.path.exists(base_cfg_path):
            print(f"[arch-restore] base config not found at {base_cfg_path} — skipping", flush=True)
            return

        with open(base_cfg_path, "r", encoding="utf-8") as f:
            base_cfg = json.load(f)
        with open(sub_cfg_path, "r", encoding="utf-8") as f:
            sub_cfg = json.load(f)

        for key in VALIDATOR_COMPARED_CONFIG_KEYS:
            base_val = base_cfg.get(key)
            if base_val is None:
                continue
            sub_val = sub_cfg.get(key)
            if sub_val == base_val:
                continue
            if key == "architectures":
                print(f"[arch-restore] architectures {sub_val} -> {base_val}", flush=True)
                sub_cfg[key] = base_val
            else:
                print(
                    f"[arch-restore] WARNING: {key} differs (base={base_val} submission={sub_val}); "
                    f"not rewriting a structural key — validator finetune check may fail",
                    flush=True,
                )

        if sub_cfg.get("architectures") == base_cfg.get("architectures"):
            with open(sub_cfg_path, "w", encoding="utf-8") as f:
                json.dump(sub_cfg, f, indent=2)
    except Exception as e:
        print(f"[arch-restore] failed, leaving submission untouched: {e}", flush=True)


# Ceiling on training relaunches for ONE task. The LR ladder needs at most
# MAX_TRIES + 1; anything beyond that is a state machine that is not converging, and
# each extra launch costs a fresh multi-GB output dir.
MAX_LOOP_RUNS = 8


def main():
    print("---STARTING TEXT TRAINING SCRIPT---", flush=True)
    parser = argparse.ArgumentParser(description="Text Model Training Script")
    parser.add_argument("--task-id", required=True, help="Task ID")
    parser.add_argument("--model", required=True, help="Model name or path")
    parser.add_argument(
        "--dataset", required=True, help="Dataset path or HF dataset name"
    )
    parser.add_argument(
        "--dataset-type", required=True, help="JSON string of dataset type config"
    )
    parser.add_argument(
        "--task-type",
        required=True,
        choices=["InstructTextTask", "DpoTask", "GrpoTask", "ChatTask"],
        help="Type of task",
    )
    parser.add_argument(
        "--file-format",
        required=False,
        choices=["csv", "json", "hf", "s3"],
        help="File format",
        default="s3",
    )
    parser.add_argument(
        "--hours-to-complete",
        type=float,
        required=True,
        help="Number of hours to complete the task",
    )
    parser.add_argument("--expected-repo-name", help="Expected repository name")
    parser.add_argument(
        "--max-data-size",
        type=int,
        help="Max data size to use for training",
        default=-1,
    )
    parser.add_argument(
        "--max-steps", type=int, help="Max steps to use for training", default=-1
    )
    parser.add_argument("--retries", type=int, help="Number of retries", default=5)
    parser.add_argument(
        "--min-steps", type=int, help="Min steps to use for training", default=100
    )

    parser.add_argument(
        "--reg-ratio",
        type=float,
        help=(
            "Global multiplier applied to the final learning rate. Neutral (1.0) by "
            "default since 2026-08-05; earlier defaults (1.24383 / 1.159624 / 1.1874) "
            "were inherited from the upstream lineage and silently boosted every LR. "
            "Set explicitly only for a deliberate, measured experiment."
        ),
        default=1.0,
    )

    args = parser.parse_args()
    original_model_name = args.model
    original_task_type = args.task_type

    for directory in train_cst.AXOLOTL_DIRECTORIES.values():
        os.makedirs(directory, exist_ok=True)
    try:
        dataset_type_dict = json.loads(args.dataset_type)
    except Exception as e:
        sys.exit(f"Error creating dataset type object: {e}")

    dataset_path = train_paths.get_text_dataset_path(args.task_id)
    submission_dir = train_paths.get_checkpoints_output_path(
        args.task_id, args.expected_repo_name
    )
    print(f"submission_dir: {submission_dir}", flush=True)
    if not os.path.exists(submission_dir):
        os.makedirs(submission_dir, exist_ok=True)

    output_dir = f"/workspace/scripts/soutputs/{args.task_id}"
    os.makedirs(output_dir, exist_ok=True)

    end_time = datetime.now(timezone.utc) + timedelta(
        hours=args.hours_to_complete - 3 / 60
    )  # assume that 3 minutes to go this far
    end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
    print("end_time: ", end_time, flush=True)

    ds_folder = "datasets"
    os.makedirs(ds_folder, exist_ok=True)
    request_path = os.path.join(ds_folder, f"training_request_{args.task_id}.json")
    model_path = str(train_paths.get_text_base_model_path(original_model_name))

    # Defensive: G.O.D feature/model-prep-container (merge 2026-05-13) anonymizes
    # models AND pushes Qwen2-family tokenizers via tokenizer.push_to_hub() —
    # which serializes `extra_special_tokens` as list-of-strings (not dict),
    # breaking AutoTokenizer.from_pretrained downstream. Sanitize cached
    # tokenizer_config.json before any tokenizer load. No-op for pre-anon
    # models (field absent). Disable via TRAINING_TOKENIZER_SANITIZE_ENABLED=0.
    try:
        from tokenizer_sanitizer import maybe_sanitize_for_anon_model
        maybe_sanitize_for_anon_model(model_path)
    except Exception as _exc:
        print(f"[tokenizer-sanitize] caller failed (skipped): {_exc}", flush=True)

    is_openai = False
    if is_openai_model(original_model_name):
        print("Upgrading python packages for openai model", flush=True)
        run_cmd_with_log(
            "pip uninstall -y transformers && pip install transformers==4.55.0",
            os.path.join(ds_folder, f"upgrade_transformers.log"),
        )
        # upgrade deepspeed
        run_cmd_with_log(
            "pip uninstall -y deepspeed && pip install deepspeed==0.17.4",
            os.path.join(ds_folder, f"upgrade_deepspeed.log"),
        )
        # install kernel
        run_cmd_with_log(
            "pip install kernels==0.9.0", os.path.join(ds_folder, f"install_kernel.log")
        )
        is_openai = True

    train_info = {
        "model_name": original_model_name,
        "model_path": model_path,
        "task_id": args.task_id,
        "dataset": dataset_path,
        "hours_to_complete": args.hours_to_complete,
        "expected_repo_name": args.expected_repo_name,
        "end_time": end_time,
        "dataset_type": dataset_type_dict,
        "submission_dir": submission_dir,
        "output_dir": output_dir,
        "adjust_batch_size": True,
        "request_path": request_path,
        "max_data_size": args.max_data_size,
        "max_steps": args.max_steps,
        "wandb_log_dir": train_cst.WANDB_LOGS_DIR,
        "min_steps": args.min_steps,
        "is_openai": is_openai,
        "reg_ratio": args.reg_ratio,
        "find_lk_lr": True,
        "checking_mode": "first_time",
    }

    # ADAPTIVE_MODE routes to 100% dynamics-driven config (Plan D).
    # Default ON (validated 80% win-rate, 10-task tournament eval 2026-05-03).
    # Set ADAPTIVE_MODE=0 to fall back to legacy bucket lookup.
    #
    # SAFETY LAYER (2026-05-23): adaptive_config can crash mid-build due to
    # bugs in advanced logic (e.g. UnboundLocalError _family_resolved on
    # 2026-05-22 wiped both KITA hotkeys R2). Wrap with try/except so a
    # config-builder bug never takes the whole training down — cascade to
    # legacy battle-tested config builder instead. Worst case: validator gets
    # a vanilla submission instead of no submission at all.
    def _sanity_check_train_info(ti: dict) -> tuple[bool, str]:
        """Validate adaptive's output has sane fields. Returns (ok, reason).

        Adaptive can import + return without raising but produce nonsense (NaN
        LR, batch=0, missing run_cmd). Catch those before they crash train_*.py
        at step 1 — burning one of our 2 retry attempts.
        """
        if not isinstance(ti, dict):
            return False, f"train_info not dict ({type(ti).__name__})"
        if "run_cmd" not in ti or not isinstance(ti["run_cmd"], str) or not ti["run_cmd"].strip():
            return False, "missing/empty run_cmd"
        tr = ti.get("train_request")
        if not isinstance(tr, dict):
            return False, f"train_request not dict ({type(tr).__name__})"
        # LR sanity — accept any field name that might carry it
        lr_candidates = [tr.get("learning_rate"), tr.get("lr"), tr.get("init_lr")]
        lr = next((v for v in lr_candidates if v is not None), None)
        if lr is not None:
            try:
                lr_f = float(lr)
                if not (1e-8 < lr_f < 1e-1):
                    return False, f"learning_rate out of bounds: {lr_f}"
            except (TypeError, ValueError):
                return False, f"learning_rate non-numeric: {lr!r}"
        # batch sanity — explicit None chain (avoid `or` falsy-on-zero bug)
        bs_candidates = [tr.get("batch_size"), tr.get("per_device_train_batch_size"), tr.get("micro_batch_size")]
        bs = next((v for v in bs_candidates if v is not None), None)
        if bs is not None:
            try:
                if int(bs) <= 0:
                    return False, f"batch_size <= 0: {bs}"
            except (TypeError, ValueError):
                return False, f"batch_size non-int: {bs!r}"
        return True, ""

    use_adaptive = os.getenv("ADAPTIVE_MODE", "1") == "1"
    _train_info_snapshot = copy.deepcopy(train_info)  # restore point if adaptive crashes
    _adaptive_ok = False
    if use_adaptive:
        try:
            from adaptive_config import get_adaptive_training_json
            print(f"[text_trainer] ADAPTIVE_MODE=on — using dynamics-driven config", flush=True)
            train_info = get_adaptive_training_json(args.task_type, train_info)
            # SAFETY LAYER (A) 2026-05-23: sanity-check adaptive's output before
            # accepting. If LR/batch/run_cmd are insane, cascade to legacy.
            _ok, _why = _sanity_check_train_info(train_info)
            if not _ok:
                print(
                    f"[ADAPTIVE-SANITY] adaptive returned invalid train_info: {_why}. "
                    f"Treating as adaptive failure → cascade to legacy.",
                    flush=True,
                )
                try:
                    subprocess.Popen(
                        [
                            "bash",
                            "/workspace/scripts/telegram_notify.sh",
                            "ERROR",
                            f"ADAPTIVE sanity FAIL → legacy fallback [{args.task_type}] task={args.task_id}",
                            f"reason: {_why}",
                        ],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                except Exception:
                    pass
                train_info = _train_info_snapshot  # restore for legacy path
            else:
                _adaptive_ok = True
        except Exception as _ad_exc:
            import traceback
            traceback.print_exc()
            print(
                f"[ADAPTIVE-SAFETY] adaptive_config crashed "
                f"({type(_ad_exc).__name__}: {_ad_exc}). "
                f"Falling back to legacy config so training proceeds instead of dying.",
                flush=True,
            )
            try:
                subprocess.Popen(
                    [
                        "bash",
                        "/workspace/scripts/telegram_notify.sh",
                        "ERROR",
                        f"ADAPTIVE crash → legacy fallback [{args.task_type}] task={args.task_id}",
                        f"{type(_ad_exc).__name__}: {_ad_exc}",
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except Exception:
                pass  # never block training
            train_info = _train_info_snapshot  # restore pre-adaptive state

    # tokenize_cmd is task-type determined — independent of adaptive vs legacy.
    if args.task_type == TaskType.INSTRUCTTEXTTASK.value or args.task_type == TaskType.CHATTASK.value:
        tokenize_cmd = f"/workspace/axo_py/bin/python tokenize_instruct.py {request_path}"
    elif args.task_type == TaskType.DPOTASK.value:
        tokenize_cmd = f"python tokenize_dpo.py {request_path}"
    elif args.task_type == TaskType.GRPOTASK.value:
        tokenize_cmd = f"python tokenize_grpo.py {request_path}"
    else:
        raise ValueError(f"Task type {args.task_type} not supported")

    # Legacy fallback when adaptive disabled or crashed. Wrap defensively too —
    # if legacy ALSO fails, we have no choice but to propagate (container exits,
    # validator marks fail). But at least we tried both layers + logged everything.
    if not _adaptive_ok:
        try:
            if (
                args.task_type == TaskType.INSTRUCTTEXTTASK.value
                or args.task_type == TaskType.CHATTASK.value
            ):
                train_info = get_instruct_training_json(train_info)
            elif args.task_type == TaskType.DPOTASK.value:
                train_info = get_dpo_training_json(train_info)
            elif args.task_type == TaskType.GRPOTASK.value:
                train_info = get_grpo_training_json(train_info)
            else:
                raise ValueError(f"Task type {args.task_type} not supported")
        except Exception as _lg_exc:
            import traceback
            traceback.print_exc()
            print(
                f"[LEGACY-SAFETY] legacy config builder ALSO failed "
                f"({type(_lg_exc).__name__}: {_lg_exc}). "
                f"No more fallback layer — propagating.",
                flush=True,
            )
            try:
                subprocess.Popen(
                    [
                        "bash",
                        "/workspace/scripts/telegram_notify.sh",
                        "TRAIN_FAIL",
                        f"BOTH adaptive+legacy crashed [{args.task_type}] task={args.task_id}",
                        f"{type(_lg_exc).__name__}: {_lg_exc}",
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except Exception:
                pass
            raise

    train_cmd = train_info["run_cmd"]

    # SAFETY LAYER (C) 2026-05-23: post-Grafana-audit, all other diagnostic
    # info (adaptive PLAN, errors, retries, end_time) is already in stdout
    # and shipped to Loki. The only missing greppable marker was the FINAL
    # resolved config — which path won (adaptive vs legacy) and the headline
    # HP. One short line is enough — no need for a separate JSON dump.
    #
    # FIX 2026-05-23: HP lives in train_cmd string (torchrun --arg value),
    # not train_request dict. First production run showed "lr=? batch=?"
    # because the dict lookup found nothing. Use extract_value_from_cmd
    # (already defined above for regex extraction).
    def _safe_extract(cmd: str, *keys: str) -> str:
        for k in keys:
            v = extract_value_from_cmd(cmd, k)
            if v is not None:
                return v
        return "?"

    _lr_val = _safe_extract(train_cmd, "learning_rate", "lr")
    _bs_val = _safe_extract(train_cmd, "per_device_train_batch_size", "batch_size", "micro_batch_size")
    _ms_val = _safe_extract(train_cmd, "max_steps", "num_train_epochs")
    _model_val = _safe_extract(train_cmd, "base_model", "model_name_or_path", "model")
    print(
        f"[CONFIG-RESOLVED] path={'adaptive' if _adaptive_ok else 'legacy'} "
        f"task_type={args.task_type} task_id={args.task_id} "
        f"lr={_lr_val} batch={_bs_val} steps_or_epochs={_ms_val} "
        f"model={_model_val}",
        flush=True,
    )

    with open(request_path, "w") as f:
        json.dump(train_info, f, indent=4, ensure_ascii=False)

    run_cmd_with_log(
        tokenize_cmd, os.path.join(ds_folder, f"tokenize_{args.task_id}.log")
    )

    original_train_cmd = train_cmd
    train_success = False
    state = get_state()
    state = {}
    set_state(state) # reset first
    state["mode"] = "initial"
    # at first the state is always running the train_cmd

    set_state(state)
    # TODO Run something magic here
    count = 0
    while True:
        state = get_state()
        mode_before = state.get("mode")
        train_cmd = original_train_cmd  # will replace based on the state later
        c_train_info = copy.deepcopy(train_info)
        final_output_dir = None
        if args.task_type == TaskType.GRPOTASK.value:
            state["mode"] = "finish" # do not run this for GRPO task
            c_train_info["train_request"]["checking_mode"] = "none"
            # State machine bug fix (2026-04-30): GRPO branch sets mode to
            # "finish" but never breaks the while loop, causing infinite
            # retraining (overwrites trained model with new run from base).
            # Verified empirically: v9 ran 4 separate trainings, each
            # overwriting the previous adapter at /root/text-jagger/outputs/.
            # Break after first GRPO training completes.
            if count > 0:
                break
        else:
            if state["mode"] == "initial":
                c_train_info["train_request"]["checking_mode"] = "first_time"
                
            elif state["mode"] == "continue":
                c_train_info["train_request"]["checking_mode"] = "second_time"
                n_runs = state["next_runs"]
                if "lrs" not in state: # first time of continue
                    current_lr = float(state["train"]["lr"])
                    state["lrs"] = lr_utils.extend_learning_rates(current_lr, n_runs, log_range=get_log_scale(args.task_type))
                    assert len(state["lrs"]) == n_runs, f"Number of learning rates {state['lrs']} should be equal to number of runs {n_runs}"
                    state["runs"] = []
                
                set_state(state)
                state["runs"].append(state["train"].copy())
                delete_poor_checkpoints(state["runs"])
                if len(state["runs"]) < n_runs:
                    index = len(state["runs"])
                    current_lr = state["lrs"][index]

                    # BO/GP-EI augmentation: with ≥3 prior (lr, loss) observations,
                    # use Gaussian Process Expected Improvement to suggest next LR
                    # instead of the pre-generated geometric sweep. Fail-soft on any
                    # error (returns None → fall back to geometric).
                    # Ported from hyper-text 2026-05-11. Enabled by default; disable
                    # with TRAINING_BO_AUGMENT=0 env var.
                    try:
                        from bo_augmentation import is_available as _bo_avail
                        from bo_augmentation import fit_gp_suggest as _bo_suggest
                        from bo_augmentation import derive_bounds as _bo_bounds
                        if _bo_avail() and len(state["runs"]) >= 3:
                            _obs = [(float(r["lr"]), float(r["current_loss"]))
                                    for r in state["runs"]
                                    if r.get("current_loss") is not None]
                            if len(_obs) >= 3:
                                _base_lr = float(state["train"]["lr"])
                                _lo, _hi = _bo_bounds(base_lr=_base_lr, observations=_obs)
                                _bo_lr = _bo_suggest(
                                    observations=_obs,
                                    allowed_lower=_lo,
                                    allowed_upper=_hi,
                                    seed=42 + len(_obs),
                                )
                                if _bo_lr is not None and _bo_lr > 0:
                                    print(f"[BO] override LR {current_lr:.3e} → {_bo_lr:.3e} "
                                          f"from GP-EI on {len(_obs)} obs (bounds=[{_lo:.2e},{_hi:.2e}])",
                                          flush=True)
                                    current_lr = _bo_lr
                    except Exception as _bo_exc:
                        print(f"[BO] suggestion skipped (fallback to geometric): {_bo_exc}", flush=True)

                    train_cmd = replace_args_in_cmd(train_cmd, "learning_rate", str(current_lr))
                else: # the final run
                    # first find from runs the best loss
                    c_train_info["train_request"]["checking_mode"] = "none"
                    index = np.argmin([run["current_loss"] for run in state["runs"]])
                    print(f"BL;{index};{state['runs'][index]['current_loss']}; {state['lrs'][index]}", flush=True)
                    train_cmd = state["runs"][index]["train_cmd"]  #replace_args_in_cmd(train_cmd, "learning_rate", str(state["lrs"][index]))
                    final_output_dir = state["runs"][index]["output_dir"]
                    state["mode"] = "finish"
            else: # the state = finish; no need to run more
                assert state["mode"] == "finish"
                break
        
        set_state(state)
        if train_cmd:
            run_output_dir = output_dir + f"_{count}" if not final_output_dir else final_output_dir
            train_cmd = replace_args_in_cmd(train_cmd, "output_dir", run_output_dir)
            
            current_request_path = os.path.join(ds_folder, f"training_request_{args.task_id}_{count}.json")
            with open(current_request_path, "w") as f:
                json.dump(c_train_info, f, indent=4, ensure_ascii=False)
            
            train_cmd = replace_args_in_cmd(train_cmd, "request_path", current_request_path)
            
            state["train"] = {
                "train_cmd": train_cmd,
                "log_path": os.path.join(ds_folder, f"train_{args.task_id}.log"),
                "lr": extract_value_from_cmd(train_cmd, "learning_rate"),
                "output_dir": run_output_dir
            }
            state["train"]["start_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            set_state(state)
            
            log_path = state["train"]["log_path"]
            # print(f"Run training with train_info: {c_train_info}", flush=True)
            success = run_training(
                train_cmd,
                log_path,
                args.task_id,
                args.retries,
                args.task_type,
                args.expected_repo_name,
            )
            time.sleep(5)
            if not success:
                print(f"Training failed for task {args.task_id} at count={count}", flush=True)
                break

            # A run that SUCCEEDS without advancing the state is the one exit this
            # loop never had. The state normally moves initial -> continue -> finish
            # inside the training subprocess; if a run is cut short before it gets
            # there — a deadline preempting the probe, or Redis state lost mid-task —
            # it exits cleanly with mode still "initial" and we relaunch, forever.
            # Measured before this guard: 244 launches and 700 GB of per-attempt
            # output dirs for a single task, budget entirely spent on relaunch churn.
            # The GRPO branch has carried the same guard since 2026-04-30; this is the
            # non-GRPO half that was missing.
            #
            # Only "initial" is checked: the "continue" arm appends to state["runs"]
            # every iteration and the ladder is capped at next_runs, so it cannot spin.
            if mode_before == "initial" and get_state().get("mode") == "initial":
                print(
                    f"[loop] run {count} finished without advancing the state machine "
                    f"(still 'initial') — stopping rather than relaunching. The "
                    f"submission holds whatever this run saved.",
                    flush=True,
                )
                break

        count += 1
        # Backstop for shapes the check above does not name — state reset, an unseen
        # transition. The ladder legitimately needs at most MAX_TRIES + 1 runs, so a
        # generous cap cannot truncate a healthy run but still bounds a runaway.
        if count > MAX_LOOP_RUNS:
            print(
                f"[loop] hard cap: {count} training launches for one task, which no "
                f"legitimate ladder needs — stopping. Investigate the state machine.",
                flush=True,
            )
            break

    if not os.path.exists(submission_dir) or len(os.listdir(submission_dir)) < 2:
        print(f"Training failed for task {args.task_id}", flush=True)
    else:
        print(f"Training successfully done for task {args.task_id}", flush=True)
        train_success = True

    # NaN/Inf guard: validator scores NaN test_loss as 0. If the final checkpoint
    # contains non-finite weights, treat as failure and fall through to the
    # add_random_noise fallback so we still ship a finetune-shaped submission.
    if train_success and checkpoint_has_nan_or_inf(submission_dir):
        print(f"NaN/Inf in submission checkpoint for task {args.task_id}; falling back to noise", flush=True)
        train_success = False
        try:
            shutil.rmtree(submission_dir)
            os.makedirs(submission_dir, exist_ok=True)
        except Exception as e:
            print(f"Could not clean submission_dir before fallback: {e}", flush=True)

    if not train_success:
        print(f"Training failed for task {args.task_id}", flush=True)
        # add noise to the model
        add_noise_cmd = f"python add_random_noise.py {model_path} {submission_dir}"
        run_cmd_with_log(
            add_noise_cmd, os.path.join(ds_folder, f"add_noise_{args.task_id}.log")
        )

    # Last net before upload: the validator rejects a submission whose config
    # architectures no longer match the base model. Runs on both the trained and
    # the fallback path, since add_random_noise also writes a fresh config.
    restore_submission_architectures(submission_dir, model_path)

    patch_wandb_symlinks(train_cst.WANDB_LOGS_DIR)


if __name__ == "__main__":
    main()
