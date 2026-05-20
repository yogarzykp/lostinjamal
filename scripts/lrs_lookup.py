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


# ---------------------------------------------------------------------------
# EXP-BOSS-1 (2026-05-20): Architecture×param-size CSV fallback table.
# Ported from BOSS lion_dance_1 lrs/instruct_ar.csv + dpo_ar.csv (2026-05-14
# commit 249e0e7). Each row: size,architecture,avg_lr.
#
# Anonymization-resistant — uses (architecture, param_count) instead of model
# name hash. Closest-size match within same architecture family.
#
# Layered:
#   Tier 1: hash(model_name) → JSON lookup (legacy)
#   Tier 2: _detect_and_recover → fingerprint-recover original name → retry hash
#   Tier 3: AR-CSV (arch, closest_size) — THIS LAYER (added 2026-05-20)
#   Else: bucket / family-profile default
#
# Forensic: research_adaptive_config_diff_2026_05_20.md +
#            research_lion_dance_1_evolution_2026_05_20.md
# ---------------------------------------------------------------------------

def _read_csv_ar(path: str):
    """Parse arch+size→LR CSV. Format: size,architecture,avg_lr (header L1).
    Returns list of {size:int, ar:str_lower, lr:float}. Fail-soft to [].
    """
    if not os.path.exists(path):
        return []
    rows = []
    try:
        with open(path, "r") as f:
            for i, line in enumerate(f):
                if i == 0:
                    continue  # skip header
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != 3:
                    continue
                try:
                    rows.append({
                        "size": int(parts[0]),
                        "ar": parts[1].strip().lower(),
                        "lr": float(parts[2]),
                    })
                except ValueError:
                    continue
    except Exception as exc:
        print(f"[lrs_lookup] AR CSV load failed (skipped): {exc}", flush=True)
    return rows


_INSTRUCT_AR_CONFIG = _read_csv_ar(os.path.join(current_dir, "lrs/instruct_ar.csv"))
_DPO_AR_CONFIG = _read_csv_ar(os.path.join(current_dir, "lrs/dpo_ar.csv"))


def _get_lr_from_ar(architecture: Optional[str], param_nums: Optional[int],
                    list_config: list) -> Optional[float]:
    """Match by architecture lowercase + closest size. None on miss."""
    if not list_config or not architecture or not param_nums:
        return None
    filtered = [c for c in list_config if c["ar"] == architecture.lower().strip()]
    if not filtered:
        return None
    closest = min(filtered, key=lambda x: abs(x["size"] - param_nums))
    return closest["lr"]


def get_lr_from_ar_dpo(architecture: Optional[str], param_nums: Optional[int]) -> Optional[float]:
    """Tier 3 AR-CSV fallback for DPO. None on miss."""
    return _get_lr_from_ar(architecture, param_nums, _DPO_AR_CONFIG)


def get_lr_from_ar_instruct(architecture: Optional[str], param_nums: Optional[int]) -> Optional[float]:
    """Tier 3 AR-CSV fallback for Instruct. None on miss."""
    return _get_lr_from_ar(architecture, param_nums, _INSTRUCT_AR_CONFIG)


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
