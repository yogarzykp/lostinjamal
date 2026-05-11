"""General HP Resolver — dynamic rule-based, NOT per-model catalog.

Philosophy (per user 2026-05-09):
  - Repo general (bisa digunakan di situasi apapun/model manapun/bucket manapun)
  - Sistematis yang dinamis, menyesuaikan diri dengan model atau dataset baru
  - Config dynamic untuk siap bertemu model anonim lainnya
  - Dataset isi berbeda + augmentasi tidak punya data validasi 100% — jadi
    rule-based DENGAN dataset profile + augmentation detection adalah
    fallback safest

Pipeline:
  Input  : (model_dir, dataset_path, task_type, hours_to_complete,
            baseline_stats_optional)
  Output : run_config dict (matches legacy instruct/dpo/grpo schema)

Tier cascade (no per-model lookup):
  T1. Architecture+size empirical (empirical_hp_rules.json) — winner-derived
      median LR per (family, size_bucket, task_type)
  T1.5 Task character adjustment (translation/reasoning/code/skill) from
      dataset profile (io_jaccard, lang_ratio, cot/math/code flags)
  T1.7 Dataset size adjustment (small <3K / medium 3-50K / large >50K)
  T1.8 Augmentation compensator (from BASELINE_STATS weight_rms vs canonical)
  T2.  Scaling-law fallback when empirical table miss (Chinchilla-inspired
       size scaling: LR ~ 1/sqrt(param_count) × family multiplier)
  T3.  Generic safe default (very last resort)

NO per-model entries. Each task fingerprint resolves DYNAMICALLY.
"""

from __future__ import annotations

import json
import math
import os
from pathlib import Path
from typing import Any, Dict, Optional


# ── Static catalog (loaded once) ──────────────────────────────────────
_RULES: Optional[Dict] = None


def _load_rules() -> Dict:
    """Lazy-load empirical_hp_rules.json. Cached after first call."""
    global _RULES
    if _RULES is not None:
        return _RULES
    rules_path = Path(__file__).parent / "empirical_hp_rules.json"
    if rules_path.exists():
        try:
            _RULES = json.loads(rules_path.read_text())
        except Exception as exc:
            print(f"[resolver] empirical_hp_rules.json parse fail: {exc}", flush=True)
            _RULES = {"cells": {}}
    else:
        _RULES = {"cells": {}}
    return _RULES


# ── Architecture → family map (same as research_aggregate) ────────────
_ARCH_TO_FAMILY = {
    "qwen2forcausallm": "qwen",
    "qwen3forcausallm": "qwen",
    "llamaforcausallm": "llama",
    "mistralforcausallm": "mistral",
    "mixtralforcausallm": "mixtral",
    "phi3forcausallm": "phi",
    "phiforcausallm": "phi",
    "phimoeforcausallm": "phi",
    "gemma2forcausallm": "gemma",
    "gemmaforcausallm": "gemma",
    "gemma3forcausallm": "gemma",
    "gptneoxforcausallm": "gpt_neox",
    "gptneoforcausallm": "gpt_neo",
    "bloomforcausallm": "bloom",
    "falconforcausallm": "falcon",
    "optforcausallm": "opt",
    "starcoder2forcausallm": "starcoder",
    "gptbigcodeforcausallm": "starcoder",
    "gptossforcausallm": "gpt_oss",
}


def detect_family(arch: Optional[str], hidden_size: Optional[int] = None,
                  vocab_size: Optional[int] = None) -> str:
    """Family from `architectures[0]` + optional size hints.

    Anonymization-safe: only uses fields preserved by validator's scrub.
    """
    if not arch:
        return "unknown"
    a = arch.strip().lower()
    family = _ARCH_TO_FAMILY.get(a)
    if not family:
        # Heuristic from arch substring
        if "qwen" in a: return "qwen"
        if "llama" in a: return "llama"
        if "gemma" in a: return "gemma"
        if "phi" in a: return "phi"
        return "unknown"

    # Refine via vocab+hidden signature (without model name):
    # SmolLM: vocab 49152
    # TinyLlama: vocab 32000 + hidden 2048 layers 22
    # Sheared-LLaMA: vocab 32000 + hidden 2048 layers 24
    if family == "llama" and vocab_size == 49152:
        return "smollm"
    if family == "llama" and vocab_size == 32000 and hidden_size == 2048:
        return "tinyllama"  # TinyLlama, Sheared-LLaMA cluster
    return family


def size_bucket(param_count_billions: Optional[float]) -> str:
    """Convert param count (billions) to bucket. Matches research_aggregate."""
    if param_count_billions is None:
        return "unknown"
    b = param_count_billions
    if b < 0.3: return "0_03b"
    if b < 0.6: return "0_06b"
    if b < 1.0: return "0_1b"
    if b < 2.0: return "1_2b"
    if b < 4.0: return "2_4b"
    if b < 5.0: return "4_5b"
    if b < 9.0: return "5_9b"
    if b < 12.0: return "9_12b"
    if b < 15.0: return "12_15b"
    if b < 35.0: return "15_35b"
    return "35b+"


def _estimate_param_count(config: Dict) -> Optional[float]:
    """Rough param count in billions from config.json fields."""
    h = config.get("hidden_size")
    layers = config.get("num_hidden_layers")
    vocab = config.get("vocab_size")
    inter = config.get("intermediate_size") or (h * 4 if h else None)
    if not all([h, layers, vocab, inter]):
        return None
    embed = 2 * vocab * h
    per_layer = 4 * h * h + 3 * h * inter
    return (embed + per_layer * layers) / 1e9


def _read_config(model_dir: str) -> Optional[Dict]:
    """Read config.json from model_dir. Returns None on fail (anonymization-safe path)."""
    if not model_dir:
        return None
    cfg_path = Path(model_dir) / "config.json"
    if not cfg_path.exists():
        return None
    try:
        return json.loads(cfg_path.read_text())
    except Exception:
        return None


# ── Tier 1: empirical lookup ───────────────────────────────────────────
def _lookup_empirical(family: str, bucket: str, task_type: str) -> Optional[Dict]:
    """Find empirical HP for (family, bucket, task_type) cell.
    Fallback chain: exact → adjacent bucket → same family any bucket → None.
    """
    rules = _load_rules()
    cells = rules.get("cells", {})

    key = f"{family}|{bucket}|{task_type}"
    if key in cells:
        return cells[key]

    # Adjacent bucket fallback (within same family + task)
    ORDER = ["0_03b", "0_06b", "0_1b", "1_2b", "2_4b", "4_5b", "5_9b",
             "9_12b", "12_15b", "15_35b", "35b+"]
    if bucket in ORDER:
        idx = ORDER.index(bucket)
        for delta in [-1, +1, -2, +2]:
            adj_idx = idx + delta
            if 0 <= adj_idx < len(ORDER):
                adj_key = f"{family}|{ORDER[adj_idx]}|{task_type}"
                if adj_key in cells:
                    return cells[adj_key]

    # Same family, any bucket, same task
    family_matches = [
        v for k, v in cells.items()
        if k.startswith(f"{family}|") and k.endswith(f"|{task_type}")
    ]
    if family_matches:
        # Aggregate medians weighted by n
        return _weighted_median(family_matches)

    return None


def _weighted_median(cells: list[Dict]) -> Dict:
    """Combine multiple cells by n-weighted median per field."""
    agg = {}
    for field in ("learning_rate", "weight_decay", "warmup_steps",
                  "num_train_epochs", "per_device_train_batch_size",
                  "neftune_noise_alpha", "min_lr_rate"):
        vals = []
        ns = []
        for c in cells:
            d = c.get(field)
            if isinstance(d, dict) and d.get("median") is not None:
                vals.append(d["median"])
                ns.append(d.get("n", 1))
        if vals:
            total_n = sum(ns)
            if total_n > 0:
                agg[field] = {"median": sum(v * n for v, n in zip(vals, ns)) / total_n,
                              "n": total_n, "_source": "weighted_family"}
    return agg


# ── Tier 1.5: task character ───────────────────────────────────────────
def _classify_task_character(dataset_profile: Optional[Dict]) -> str:
    """Mirror adaptive_config.classify_task_character logic.
    Returns: memorization | translation | code | reasoning | skill (default)
    """
    if not dataset_profile:
        return "skill"
    flags = dataset_profile.get("heuristic_flags", {})
    cot = flags.get("cot", 0.0)
    math = flags.get("math", 0.0)
    code = flags.get("code", 0.0)
    io_j = dataset_profile.get("io_jaccard_p50", 0.0)
    lang_ratio = dataset_profile.get("lang_ratio", 1.0)
    script = dataset_profile.get("script_overall", "unknown")

    if code > 0.3:
        return "code"
    if cot > 0.3 or math > 0.2:
        return "reasoning"
    if lang_ratio < 0.6 or script in ("cjk", "arabic", "cyrillic", "mixed"):
        return "translation"
    if io_j > 0.5:
        return "translation"  # parallel pairs
    if 0.05 < io_j < 0.3:
        return "memorization"
    return "skill"


# Multipliers per task_class (derived from empirical observations)
_TASK_CLASS_LR_MULT = {
    "translation": 1.0,
    "reasoning":   0.85,    # slightly lower LR; needs longer convergence
    "code":        0.7,     # code tasks tend to use lower LR (winner data shows ~3e-5 for 4B+)
    "memorization": 0.5,    # memorization needs lower LR (TOFU-like)
    "skill":       1.0,     # default
}


# ── Tier 1.7: dataset size scaling ─────────────────────────────────────
def _dataset_size_mult(num_samples: int, task_type: str) -> float:
    """LR multiplier based on dataset size. Smaller dataset → lower LR (regularization)."""
    if num_samples is None:
        return 1.0
    if num_samples < 1000:   return 0.7
    if num_samples < 5000:   return 0.85
    if num_samples < 30000:  return 1.0
    if num_samples < 100000: return 1.1
    return 1.15


# ── Tier 1.8: augmentation compensator ─────────────────────────────────
_AUG_LR_MULT = {
    "WEIGHT_SCALING":     1.0,   # model just rescaled, dynamics intact
    "GAUSSIAN_NOISE":     1.0,   # noise already there, no LR change
    "MAGNITUDE_PRUNING":  1.15,  # rebuild zeroed weights
    "LAYER_REINIT":       1.05,  # mild bump for reinit'd layer
}


# ── Tier 2: scaling-law fallback ───────────────────────────────────────
def _scaling_law_lr(param_count_b: float, task_type: str) -> float:
    """Chinchilla-inspired LR scaling when empirical table miss.

    Base anchor: 1e-4 at ~1B params for instruct.
    LR scales ~ 1/sqrt(params/anchor).
    Per-task multipliers from observed winner clusters.
    """
    if param_count_b is None or param_count_b <= 0:
        return 5e-5  # very conservative

    anchor_b = 1.0
    anchor_lr = 1e-4
    scaling = math.sqrt(anchor_b / param_count_b)
    lr = anchor_lr * scaling

    task_mult = {
        "instruct":     1.0,
        "dpo":          0.1,   # DPO uses 10× lower LR typically
        "grpo":         0.2,
        "grpo_python":  0.2,
    }.get(task_type, 1.0)
    return lr * task_mult


# ── Main entry ─────────────────────────────────────────────────────────
def resolve_hp(
    model_dir: str,
    task_type: str,
    num_dataset_samples: Optional[int] = None,
    dataset_profile: Optional[Dict] = None,
    baseline_stats: Optional[Dict] = None,
    augmentation_info: Optional[Dict] = None,
) -> Dict:
    """Resolve HP dynamically from model + dataset signals.

    Returns dict with HP fields ready to merge into run_config:
        learning_rate, weight_decay, warmup_steps, num_train_epochs,
        per_device_train_batch_size, neftune_noise_alpha, min_lr_rate
        + meta keys (family, bucket, source_tier, ...)

    All fields are SUGGESTIONS — caller may override based on its own policy.
    """
    cfg = _read_config(model_dir) or {}
    arch = (cfg.get("architectures") or [""])[0]
    family = detect_family(arch, cfg.get("hidden_size"), cfg.get("vocab_size"))
    param_b = _estimate_param_count(cfg)
    bucket = size_bucket(param_b)
    task_norm = task_type.lower().replace("task", "").replace("text", "").strip("_")

    out = {
        "_family": family,
        "_size_bucket": bucket,
        "_param_count_b": param_b,
        "_task_type": task_norm,
        "_source_tier": None,
    }

    # Tier 1: empirical lookup
    cell = _lookup_empirical(family, bucket, task_norm)
    if cell:
        for f in ("learning_rate", "weight_decay", "warmup_steps",
                  "num_train_epochs", "per_device_train_batch_size",
                  "neftune_noise_alpha", "min_lr_rate"):
            if f in cell and isinstance(cell[f], dict) and cell[f].get("median") is not None:
                out[f] = cell[f]["median"]
        if "_source" in cell or any(f in out for f in ("learning_rate",)):
            out["_source_tier"] = "T1_empirical" if "_source" not in cell else cell.get("_source")
            out["_empirical_n"] = cell.get("learning_rate", {}).get("n")

    # Tier 2: scaling-law fallback for LR
    if "learning_rate" not in out:
        out["learning_rate"] = _scaling_law_lr(param_b, task_norm)
        out["_source_tier"] = "T2_scaling_law"

    # Tier 1.5: task character adjustment (LR multiplier)
    task_class = _classify_task_character(dataset_profile)
    out["_task_class"] = task_class
    task_mult = _TASK_CLASS_LR_MULT.get(task_class, 1.0)
    if task_mult != 1.0:
        out["learning_rate"] *= task_mult
        out["_task_class_lr_mult"] = task_mult

    # Tier 1.7: dataset size adjustment
    ds_mult = _dataset_size_mult(num_dataset_samples, task_norm)
    if ds_mult != 1.0:
        out["learning_rate"] *= ds_mult
        out["_dataset_size_lr_mult"] = ds_mult

    # Tier 1.8: augmentation compensator
    if augmentation_info and augmentation_info.get("detected_type"):
        aug_type = augmentation_info["detected_type"]
        aug_mult = _AUG_LR_MULT.get(aug_type, 1.0)
        if aug_mult != 1.0:
            out["learning_rate"] *= aug_mult
            out["_aug_lr_mult"] = aug_mult
        out["_aug_type"] = aug_type

    return out


# Convenience CLI
if __name__ == "__main__":
    import argparse, sys
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", required=True)
    ap.add_argument("--task-type", required=True, choices=["instruct", "dpo", "grpo"])
    ap.add_argument("--samples", type=int, default=None)
    args = ap.parse_args()

    result = resolve_hp(args.model_dir, args.task_type, args.samples)
    print(json.dumps(result, indent=2, default=str))
