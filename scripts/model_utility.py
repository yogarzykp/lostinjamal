DPO = "dpo"
GRPO = "grpo"
INSTRUCT = "instruct"
import re
from huggingface_hub import HfApi
from transformers import AutoConfig
import glob
from safetensors.torch import load_file
from pathlib import Path
import torch
import os
import json
import torch

MODEL_CONFIG = {
    "facebook/opt-1.3b": {"model_size": 1_300_000_000},
    "facebook/opt-3b": {"model_size": 3_000_000_000},
    "facebook/opt-6.7b": {"model_size": 6_700_000_000},
    "facebook/opt-13b": {"model_size": 13_000_000_000},
    "EleutherAI/gpt-neo-1.3B": {"model_size": 1_300_000_000},
    "EleutherAI/gpt-neo-125m": {"model_size": 125_000_000},
    "bigscience/bloom-560m": {"model_size": 560_000_000},
    "TinyLlama/TinyLlama_v1.1": {"model_size": 1_100_000_000},
}

hf_api = HfApi()


def get_model_architecture(model_path: str) -> str:
    try:
        config = AutoConfig.from_pretrained(model_path)
        architectures = config.architectures
        if len(architectures) > 1:
            return "Multiple architectures"
        return architectures[0].strip().lower()
    except:
        return "Unknown"


def get_use_liger(architecture: str) -> str:
    if architecture.lower() in [
        "qwen2forcausallm",
        "llamaforcausallm",
        "gemma2forcausallm",
        "mixtralforcausallm",
        "mistralforcausallm",
        "qwen3forcausallm",
        "phi3forcausallm",
        "gemmaforcausallm",
    ]:
        return "True"
    else:
        return "False"


def count_params_from_safetensors(model_dir):
    total_params = 0
    shards = glob.glob(os.path.join(model_dir, "*.safetensors"))
    if not shards:
        return None

    for shard_path in shards:
        print(f"Loading shard: {shard_path}")
        tensors = load_file(shard_path)
        total_params += sum(v.numel() for v in tensors.values())

    return total_params


def count_params_from_bin(model_dir):
    total_params = 0
    shards = glob.glob(os.path.join(model_dir, "*.bin"))
    if not shards:
        return None

    for shard_path in shards:
        print(f"Loading shard: {shard_path}")
        try:
            state_dict = torch.load(shard_path, map_location="cpu")
            total_params += sum(v.numel() for v in state_dict.values())
        except Exception as e:
            print(f"cannot load {shard_path}: {e}")
            continue

    return total_params


def get_model_size_from_local_path(model_path: str) -> int:
    size = count_params_from_safetensors(model_path)
    if size is not None and size > 1000:
        print(f"Model size from safetensors: {size}")
        return size
    size = count_params_from_bin(model_path)
    if size is not None and size > 1000:
        print(f"Model size from bin: {size}")
        return size
    return None


def get_gpu_count():
    return torch.cuda.device_count()


def get_model_num_params(model_id: str, model_path: str) -> int:
    if model_id in MODEL_CONFIG:
        return MODEL_CONFIG[model_id]["model_size"]
    try:
        size = get_model_size_from_local_path(model_path)
        if size is not None:
            return size
        raise Exception(f"Cannot get model size from {model_path}")

    except Exception as e:
        print(f"Error getting model size from safetensors: {e}")
        try:
            model_size = re.search(r"(\d+)(?=[bB])", model_id)
            model_size = (
                int(model_size.group(1)) * 1_000_000_000 if model_size else None
            )
            print(f"Model size from regex: {model_size}")
            return model_size
        except Exception as e:
            print(f"Error getting model size from regex: {e}")
            return None


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


def disable_flash_attention(architecture: str, model: str, model_dir: str = None) -> str:
    # Config-based (anonymization-safe) — preferred when model_dir available
    cfg = _read_config_safe(model_dir)
    if cfg is not None:
        arch_field = (cfg.get("architectures") or [""])[0]
        # Phi-2: PhiForCausalLM + hidden_size=2560 (distinct from Phi-3)
        if arch_field == "PhiForCausalLM" and cfg.get("hidden_size") == 2560:
            return "True"
        # Falcon-RW: model_type=falcon + parallel_attn flag
        if cfg.get("model_type") == "falcon" and cfg.get("parallel_attn"):
            return "True"

    # Legacy name-based (works pre-merge / when model_dir unavailable)
    if model == "microsoft/phi-2":
        return "True"
    if "falcon-rw" in model.lower():  # ex, tiiuae/falcon-rw-1b
        return "True"

    # Architecture string — already anonymization-safe (comes from config)
    if architecture.strip().lower() in ["gptneoforcausallm", "bloomforcausallm", "gptossforcausallm"]:
        return "True"
    else:
        return "False"


# Fingerprint catalog for vllm blocklist (anonymization-safe lookup).
# Source: hand-curated from main branch's get_use_vllm string blocklist.
# Format: "(hidden_size,num_hidden_layers,vocab_size,intermediate_size)" → True/False
_VLLM_BLOCKLIST_FINGERPRINTS = {
    # microsoft/phi-2: PhiForCausalLM, hidden=2560, layers=32, vocab=51200
    "2560,32,51200,10240": False,
    # databricks/dolly-v2-3b: GPTNeoXForCausalLM, hidden=2560, layers=32, vocab=50280
    "2560,32,50280,10240": False,
    # openlm-research/open_llama_3b: LlamaForCausalLM, hidden=3200, layers=26, vocab=32000
    "3200,26,32000,8640": False,
}


def get_use_vllm(architecture: str, model: str, model_dir: str = None) -> str:
    # Config-based check (anonymization-safe)
    cfg = _read_config_safe(model_dir)
    if cfg is not None:
        fp_key = ",".join(str(cfg.get(k, "")) for k in
                          ("hidden_size", "num_hidden_layers", "vocab_size", "intermediate_size"))
        if fp_key in _VLLM_BLOCKLIST_FINGERPRINTS:
            return _VLLM_BLOCKLIST_FINGERPRINTS[fp_key]
        # Falcon-RW pattern
        if cfg.get("model_type") == "falcon" and cfg.get("parallel_attn"):
            return False

    # Legacy name-based blocklist (works pre-merge)
    if model in [
        "Eurdem/Defne_llama3_2x8B",
        "heegyu/WizardVicuna-open-llama-3b-v2",
        "openlm-research/open_llama_3b",
        "TitanML/tiny-mixtral",
        "dunzhang/stella_en_1.5B_v5",
        "oopsung/llama2-7b-n-ox-test-v1",
        "microsoft/phi-2",
        "databricks/dolly-v2-3b",
    ]:
        return False
    if "falcon-rw" in model.lower():
        return False

    if architecture in ["gptneoforcausallm", "bloomforcausallm"]:
        return False
    else:
        return True


def get_gradient_checkpointing(model: str, model_dir: str = None) -> str:
    # Config-based: Falcon-RW has parallel_attn=True
    cfg = _read_config_safe(model_dir)
    if cfg is not None and cfg.get("model_type") == "falcon" and cfg.get("parallel_attn"):
        return "False"

    # Legacy name-based
    if "falcon-rw" in model.lower():
        return "False"
    return "True"


def get_data_size(data_path: str) -> int:
    with open(data_path, "r") as f:
        data = json.load(f)
    return len(data)
