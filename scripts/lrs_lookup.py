"""Hash-based LR lookup with anonymization-safe fallback.

Pre-merge (model name legible): direct hash → lookup table.
Post-merge (model anonymized as gradients-io/augmented-<sha16>): the direct
hash misses, so we attempt to recover the original model_id via fingerprint
(scripts/model_detection.identify_base_model) using the model directory's
config.json, then retry the hash lookup with the recovered name.

All functions FAIL-SOFT — return None when no match (caller falls back to
family profile in adaptive_config or per-bucket default in instruct_config).
"""

import hashlib
import json
import os
from typing import Optional

current_dir = os.path.dirname(os.path.abspath(__file__))


with open(os.path.join(current_dir, "lrs/dpo.json"), "r") as f:
    dpo_lrs = json.load(f)

with open(os.path.join(current_dir, "lrs/grpo.json"), "r") as f:
    grpo_lrs = json.load(f)

with open(os.path.join(current_dir, "lrs/instruct.json"), "r") as f:
    instruct_lrs = json.load(f)

with open(os.path.join(current_dir, "lrs/grpo_python.json"), "r") as f:
    grpo_python_lrs = json.load(f)


def hash_model(model: str) -> str:
    model_bytes = model.encode('utf-8')
    hashed = hashlib.sha256(model_bytes).hexdigest()
    return hashed


def _detect_and_recover(model_dir: Optional[str]) -> Optional[str]:
    """Try to recover original model_id from anonymized model directory.
    Returns base_model name on high-confidence match, else None.
    """
    if not model_dir or not os.path.exists(model_dir):
        return None
    try:
        from model_detection import identify_base_model
        det = identify_base_model(model_dir)
        if det.get("base_model") and det.get("confidence", 0.0) >= 0.9:
            return det["base_model"]
    except Exception as exc:
        print(f"[lrs_lookup] detection failed (skipped): {exc}", flush=True)
    return None


def get_dpo_lr(model: str, model_dir: Optional[str] = None):
    # Tier 1: direct hash on provided model name (works pre-merge)
    hashed_model = hash_model(model)
    for lr in dpo_lrs:
        if lr["h"] == hashed_model:
            return lr["lr"]
    # Tier 2: detect base model from config + retry hash (post-merge)
    recovered = _detect_and_recover(model_dir)
    if recovered and recovered != model:
        for lr in dpo_lrs:
            if lr["h"] == hash_model(recovered):
                return lr["lr"]
    return None


def get_grpo_lr(model: str, model_dir: Optional[str] = None):
    hashed_model = hash_model(model)
    for lr in grpo_lrs:
        if lr["h"] == hashed_model:
            return lr["lr"]
    recovered = _detect_and_recover(model_dir)
    if recovered and recovered != model:
        for lr in grpo_lrs:
            if lr["h"] == hash_model(recovered):
                return lr["lr"]
    return None


def get_instruct_lr(model: str, model_dir: Optional[str] = None):
    hashed_model = hash_model(model)
    for lr in instruct_lrs:
        if lr["h"] == hashed_model:
            return lr["lr"]
    recovered = _detect_and_recover(model_dir)
    if recovered and recovered != model:
        for lr in instruct_lrs:
            if lr["h"] == hash_model(recovered):
                return lr["lr"]
    return None


def get_grpo_python_lr(model: str, model_dir: Optional[str] = None):
    hashed_model = hash_model(model)
    for lr in grpo_python_lrs:
        if lr["h"] == hashed_model:
            return lr["lr"]
    recovered = _detect_and_recover(model_dir)
    if recovered and recovered != model:
        for lr in grpo_python_lrs:
            if lr["h"] == hash_model(recovered):
                return lr["lr"]
    return None
