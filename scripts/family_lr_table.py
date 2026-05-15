"""Family-level LR lookup table — EMPIRICAL from 783 prior tournament winners.

Ported 2026-05-15 from hyper-text/scripts/family_lr_table.py (friend's R&D
repo, develop-llambo branch). Adopted because their derivation methodology
gives anonymization-resilient LR priors keyed by (family, size_bucket, task)
— exactly what KITA needs to replace hardcoded lr_size_buckets that proved
too aggressive in round 2 (KITA lr=1.4e-4 vs empirical 8.07e-5 for Qwen-1.5B
Instruct = 73% TOO HIGH).

Derivation methodology (per hyper-text v0, 2026-05-03):
  - Source 1: 783 hash-keyed empirical LRs from prior winner training_args
  - Source 2: validator_models.json catalog (model_id → arch + size + tier)
  - Process: hash model_id → match against lrs cache → group by
    (model_type, size_bucket, task) → take median LR per cell
  - Match rate: 169/172 DPO (98.3%), 171/174 GRPO (98.3%), 191/370 Instruct
    (51.6% — many private fine-tunes), 67/67 GRPO-python (100%) → 598 total
    matched records → 140 unique (family, size, task) cells

Confidence levels:
  HIGH    : n>=8, max/min spread <5x  (12 cells, strongest signal)
  MED     : n>=4, spread <10x         (21 cells, decent signal)
  MED-low : n>=4, spread >=10x        (6 cells, real but noisy)
  LOW-ok  : n in {2,3}, spread <3x    (29 cells, small sample but consistent)
  LOW     : everything else           (72 cells, single sample or wild variance)

All cells pre-aug (cache predates G.O.D augmentation feature). Post-aug
effective LR may shift ~10-20% — fingerprint + fail-soft tier chain handles.

Integration in adaptive_config.py:
  Tier 1: family_lr_table.lookup_lr() — empirical winner LR
  Tier 2: _FAMILY_PROFILES.lr_default — our hardcoded family default
  Tier 3: param-based init_lr heuristic — generic fallback

Only apply Tier 1 if confidence >= MED-low (skip single-shot LOW data).
"""
from __future__ import annotations

from typing import Optional, Tuple


# ── Architecture normalization ───────────────────────────────────────────
# Maps `config.architectures[0].lower()` (transformers AutoConfig output)
# to the model_type strings used in HF API + validator_models.json.

ARCHITECTURE_TO_FAMILY = {
    "llamaforcausallm":       "llama",
    "qwen2forcausallm":       "qwen2",
    "qwen3forcausallm":       "qwen3",
    "mistralforcausallm":     "mistral",
    "phi3forcausallm":        "phi3",
    "phiforcausallm":         "phi",
    "gemma2forcausallm":      "gemma2",
    "gemmaforcausallm":       "gemma",
    "gptneoxforcausallm":     "gpt_neox",
    "gptneoforcausallm":      "gpt_neo",
    "bloomforcausallm":       "bloom",
    "falconforcausallm":      "falcon",
    "optforcausallm":         "opt",
    "mixtralforcausallm":     "mixtral",
    "starcoder2forcausallm":  "starcoder2",
    "gptossforcausallm":      "gpt_oss",
}


def family_from_architecture(architecture: str) -> Optional[str]:
    """Map AutoConfig.architectures[0] string to family key.

    Returns None for architectures not in the catalog (caller should
    fall back to tier-config default).
    """
    if not architecture:
        return None
    key = architecture.strip().lower()
    return ARCHITECTURE_TO_FAMILY.get(key)


def size_bucket(size_b: Optional[float]) -> Optional[str]:
    """Convert param count in billions to bucket string.

    None / negative size returns None (caller falls back to tier-config).
    """
    if size_b is None or size_b < 0:
        return None
    if size_b < 1: return "0_1b"
    if size_b < 2: return "1_2b"
    if size_b < 4: return "2_4b"
    if size_b < 5: return "4_5b"
    if size_b < 9: return "5_9b"
    if size_b < 12: return "9_12b"
    if size_b < 15: return "12_15b"
    if size_b < 35: return "15_35b"
    if size_b < 80: return "35_80b"
    return "80b+"


# ── Empirical LR table ───────────────────────────────────────────────────
# Format: (family, size_bucket, task) → (lr, confidence, n_samples)
# task ∈ {"dpo", "grpo", "grpo_python", "instruct"}

FAMILY_LR_TABLE = {
    # --- bloom ---
    ('bloom',      '0_1b', 'dpo'):         (9.08e-06, 'LOW-ok', 2),
    ('bloom',      '0_1b', 'instruct'):    (5.67e-05, 'LOW-ok', 2),

    # --- falcon ---
    ('falcon',     '1_2b', 'dpo'):         (8.00e-06, 'LOW', 1),
    ('falcon',     '1_2b', 'grpo'):        (1.00e-04, 'LOW', 1),
    ('falcon',     '1_2b', 'grpo_python'): (1.00e-05, 'LOW', 1),
    ('falcon',     '1_2b', 'instruct'):    (3.50e-05, 'LOW', 1),
    ('falcon',     '5_9b', 'dpo'):         (1.82e-05, 'LOW', 1),
    ('falcon',     '5_9b', 'grpo'):        (1.25e-04, 'LOW', 1),
    ('falcon',     '5_9b', 'grpo_python'): (9.00e-05, 'LOW', 1),
    ('falcon',     '5_9b', 'instruct'):    (5.66e-05, 'LOW', 1),

    # --- gemma ---
    ('gemma',      '2_4b', 'dpo'):         (4.17e-06, 'LOW-ok', 2),
    ('gemma',      '2_4b', 'grpo'):        (3.38e-05, 'LOW-ok', 2),
    ('gemma',      '2_4b', 'instruct'):    (6.01e-05, 'LOW', 2),
    ('gemma',      '5_9b', 'dpo'):         (3.80e-06, 'LOW', 3),
    ('gemma',      '5_9b', 'grpo'):        (2.40e-05, 'LOW-ok', 3),
    ('gemma',      '5_9b', 'grpo_python'): (6.00e-06, 'LOW', 1),
    ('gemma',      '5_9b', 'instruct'):    (2.00e-05, 'LOW-ok', 3),

    # --- gemma2 ---
    ('gemma2',     '2_4b', 'dpo'):         (4.79e-06, 'LOW', 3),
    ('gemma2',     '2_4b', 'grpo'):        (1.04e-04, 'LOW-ok', 3),
    ('gemma2',     '2_4b', 'grpo_python'): (9.71e-05, 'LOW-ok', 2),
    ('gemma2',     '2_4b', 'instruct'):    (2.86e-05, 'LOW-ok', 3),
    ('gemma2',     '9_12b', 'dpo'):        (1.93e-06, 'LOW', 3),
    ('gemma2',     '9_12b', 'grpo'):       (6.27e-05, 'MED', 4),
    ('gemma2',     '9_12b', 'grpo_python'):(5.00e-06, 'LOW', 1),
    ('gemma2',     '9_12b', 'instruct'):   (1.31e-05, 'MED', 4),

    # --- gpt_neo ---
    ('gpt_neo',    '0_1b', 'dpo'):         (2.30e-05, 'LOW', 1),
    ('gpt_neo',    '0_1b', 'grpo'):        (2.46e-04, 'LOW', 1),
    ('gpt_neo',    '0_1b', 'grpo_python'): (8.00e-04, 'LOW', 1),
    ('gpt_neo',    '0_1b', 'instruct'):    (3.00e-04, 'LOW', 1),
    ('gpt_neo',    '1_2b', 'dpo'):         (2.18e-05, 'LOW', 1),
    ('gpt_neo',    '1_2b', 'grpo'):        (1.00e-04, 'LOW', 1),
    ('gpt_neo',    '1_2b', 'instruct'):    (9.29e-05, 'LOW', 1),

    # --- gpt_neox ---
    ('gpt_neox',   '0_1b', 'dpo'):         (1.94e-05, 'LOW-ok', 3),
    ('gpt_neox',   '0_1b', 'grpo'):        (1.52e-04, 'LOW', 3),
    ('gpt_neox',   '0_1b', 'instruct'):    (8.00e-05, 'LOW-ok', 3),
    ('gpt_neox',   '9_12b', 'dpo'):        (8.80e-06, 'LOW', 1),
    ('gpt_neox',   '9_12b', 'grpo'):       (9.47e-05, 'LOW', 1),
    ('gpt_neox',   '9_12b', 'instruct'):   (3.34e-05, 'LOW', 1),
    ('gpt_neox',   '12_15b', 'dpo'):       (2.00e-05, 'LOW', 1),
    ('gpt_neox',   '12_15b', 'grpo'):      (9.00e-05, 'LOW', 1),
    ('gpt_neox',   '12_15b', 'instruct'):  (4.00e-05, 'LOW', 1),

    # --- gpt_oss ---
    ('gpt_oss',    '15_35b', 'dpo'):       (6.11e-06, 'LOW', 1),
    ('gpt_oss',    '15_35b', 'instruct'):  (6.25e-06, 'LOW', 1),

    # --- llama ---
    ('llama',      '0_1b', 'dpo'):         (1.08e-04, 'MED', 6),
    ('llama',      '0_1b', 'grpo'):        (3.92e-04, 'MED', 6),
    ('llama',      '0_1b', 'grpo_python'): (1.60e-03, 'LOW', 1),
    ('llama',      '0_1b', 'instruct'):    (8.03e-04, 'MED', 6),
    ('llama',      '1_2b', 'dpo'):         (1.38e-05, 'HIGH', 12),
    ('llama',      '1_2b', 'grpo'):        (1.89e-04, 'MED', 13),
    ('llama',      '1_2b', 'grpo_python'): (2.00e-04, 'MED', 7),
    ('llama',      '1_2b', 'instruct'):    (9.18e-05, 'MED-low', 13),
    ('llama',      '2_4b', 'dpo'):         (1.22e-05, 'MED', 5),
    ('llama',      '2_4b', 'grpo'):        (1.00e-04, 'MED', 5),
    ('llama',      '2_4b', 'grpo_python'): (8.92e-05, 'LOW', 2),
    ('llama',      '2_4b', 'instruct'):    (8.07e-05, 'MED', 5),
    ('llama',      '5_9b', 'dpo'):         (1.20e-05, 'MED', 39),
    ('llama',      '5_9b', 'grpo'):        (7.67e-05, 'HIGH', 43),
    ('llama',      '5_9b', 'grpo_python'): (5.53e-05, 'MED-low', 19),
    ('llama',      '5_9b', 'instruct'):    (2.94e-05, 'MED', 43),
    ('llama',      '9_12b', 'dpo'):        (8.03e-06, 'MED', 4),
    ('llama',      '9_12b', 'grpo'):       (6.51e-05, 'MED', 4),
    ('llama',      '9_12b', 'grpo_python'):(2.30e-05, 'LOW', 2),
    ('llama',      '9_12b', 'instruct'):   (7.90e-06, 'MED', 4),
    ('llama',      '12_15b', 'dpo'):       (1.00e-05, 'LOW', 3),
    ('llama',      '12_15b', 'grpo'):      (9.90e-05, 'LOW-ok', 2),
    ('llama',      '12_15b', 'instruct'):  (3.42e-05, 'LOW-ok', 2),
    ('llama',      '35_80b', 'dpo'):       (2.00e-05, 'MED', 11),
    ('llama',      '35_80b', 'instruct'):  (1.00e-04, 'HIGH', 19),

    # --- mistral ---
    ('mistral',    '2_4b', 'dpo'):         (2.12e-05, 'LOW', 1),
    ('mistral',    '2_4b', 'grpo'):        (1.29e-04, 'LOW', 1),
    ('mistral',    '2_4b', 'grpo_python'): (1.37e-04, 'LOW', 1),
    ('mistral',    '2_4b', 'instruct'):    (1.09e-04, 'LOW', 1),
    ('mistral',    '5_9b', 'dpo'):         (6.43e-06, 'HIGH', 14),
    ('mistral',    '5_9b', 'grpo'):        (5.80e-05, 'MED-low', 17),
    ('mistral',    '5_9b', 'grpo_python'): (9.25e-06, 'HIGH', 8),
    ('mistral',    '5_9b', 'instruct'):    (7.49e-06, 'HIGH', 17),
    ('mistral',    '9_12b', 'dpo'):        (8.00e-06, 'LOW', 1),
    ('mistral',    '9_12b', 'instruct'):   (1.40e-05, 'LOW', 1),
    ('mistral',    '12_15b', 'grpo'):      (9.00e-05, 'LOW', 1),
    ('mistral',    '12_15b', 'instruct'):  (4.00e-05, 'LOW', 1),

    # --- mixtral ---
    ('mixtral',    '0_1b', 'dpo'):         (2.81e-05, 'LOW', 1),
    ('mixtral',    '0_1b', 'grpo'):        (6.51e-04, 'LOW', 1),
    ('mixtral',    '0_1b', 'instruct'):    (1.00e-03, 'LOW', 1),
    ('mixtral',    '12_15b', 'grpo'):      (5.50e-05, 'LOW', 1),
    ('mixtral',    '12_15b', 'instruct'):  (2.83e-05, 'LOW', 1),

    # --- opt ---
    ('opt',        '0_1b', 'dpo'):         (2.90e-05, 'LOW-ok', 2),
    ('opt',        '0_1b', 'grpo'):        (4.30e-04, 'LOW-ok', 2),
    ('opt',        '0_1b', 'instruct'):    (9.10e-05, 'LOW-ok', 2),
    ('opt',        '1_2b', 'grpo'):        (2.00e-04, 'LOW', 1),
    ('opt',        '1_2b', 'instruct'):    (6.40e-05, 'LOW', 1),

    # --- phi ---
    ('phi',        '1_2b', 'dpo'):         (9.47e-06, 'LOW', 1),
    ('phi',        '1_2b', 'grpo'):        (7.75e-05, 'LOW', 1),
    ('phi',        '1_2b', 'grpo_python'): (2.94e-04, 'LOW', 1),
    ('phi',        '1_2b', 'instruct'):    (1.69e-04, 'LOW', 1),
    ('phi',        '2_4b', 'dpo'):         (1.28e-05, 'LOW', 1),
    ('phi',        '2_4b', 'grpo'):        (8.80e-05, 'LOW', 1),
    ('phi',        '2_4b', 'grpo_python'): (4.63e-05, 'LOW', 1),
    ('phi',        '2_4b', 'instruct'):    (5.60e-05, 'LOW', 1),

    # --- phi3 ---
    ('phi3',       '2_4b', 'dpo'):         (1.71e-05, 'LOW-ok', 3),
    ('phi3',       '2_4b', 'grpo'):        (1.06e-04, 'MED', 4),
    ('phi3',       '2_4b', 'instruct'):    (1.26e-04, 'MED', 4),
    ('phi3',       '12_15b', 'dpo'):       (8.00e-05, 'LOW', 1),
    ('phi3',       '12_15b', 'grpo'):      (9.00e-05, 'LOW', 1),

    # --- qwen2 ---
    ('qwen2',      '0_1b', 'dpo'):         (1.80e-05, 'HIGH', 8),
    ('qwen2',      '0_1b', 'grpo'):        (2.13e-04, 'MED-low', 10),
    ('qwen2',      '0_1b', 'grpo_python'): (1.92e-04, 'LOW', 1),
    ('qwen2',      '0_1b', 'instruct'):    (8.65e-05, 'HIGH', 10),
    ('qwen2',      '1_2b', 'dpo'):         (1.89e-05, 'HIGH', 10),
    ('qwen2',      '1_2b', 'grpo'):        (1.59e-04, 'HIGH', 11),
    ('qwen2',      '1_2b', 'grpo_python'): (1.11e-04, 'MED-low', 5),
    ('qwen2',      '1_2b', 'instruct'):    (8.07e-05, 'MED', 11),
    ('qwen2',      '2_4b', 'dpo'):         (1.77e-05, 'LOW', 2),
    ('qwen2',      '2_4b', 'grpo'):        (1.39e-04, 'LOW-ok', 3),
    ('qwen2',      '2_4b', 'grpo_python'): (1.11e-04, 'LOW-ok', 2),
    ('qwen2',      '2_4b', 'instruct'):    (6.29e-05, 'LOW-ok', 3),
    ('qwen2',      '5_9b', 'dpo'):         (1.95e-05, 'MED', 8),
    ('qwen2',      '5_9b', 'grpo'):        (7.20e-05, 'HIGH', 10),
    ('qwen2',      '5_9b', 'grpo_python'): (4.96e-05, 'MED-low', 6),
    ('qwen2',      '5_9b', 'instruct'):    (3.96e-05, 'HIGH', 10),
    ('qwen2',      '12_15b', 'dpo'):       (1.40e-05, 'LOW-ok', 3),
    ('qwen2',      '12_15b', 'grpo'):      (1.21e-04, 'MED', 4),
    ('qwen2',      '12_15b', 'grpo_python'):(2.70e-05, 'LOW', 1),
    ('qwen2',      '12_15b', 'instruct'):  (2.83e-05, 'LOW-ok', 3),

    # --- qwen3 ---
    ('qwen3',      '0_1b', 'dpo'):         (1.65e-05, 'LOW-ok', 3),
    ('qwen3',      '0_1b', 'grpo'):        (1.06e-04, 'LOW-ok', 3),
    ('qwen3',      '0_1b', 'grpo_python'): (7.00e-05, 'LOW', 1),
    ('qwen3',      '0_1b', 'instruct'):    (5.50e-05, 'LOW-ok', 3),
    ('qwen3',      '1_2b', 'dpo'):         (8.00e-06, 'LOW', 1),
    ('qwen3',      '1_2b', 'grpo'):        (1.36e-04, 'LOW', 1),
    ('qwen3',      '1_2b', 'grpo_python'): (1.40e-04, 'LOW', 1),
    ('qwen3',      '5_9b', 'dpo'):         (1.99e-05, 'LOW-ok', 2),
    ('qwen3',      '5_9b', 'grpo'):        (6.33e-05, 'LOW-ok', 2),
    ('qwen3',      '5_9b', 'grpo_python'): (5.53e-05, 'LOW', 1),
    ('qwen3',      '5_9b', 'instruct'):    (4.95e-05, 'LOW-ok', 2),
    ('qwen3',      '12_15b', 'dpo'):       (1.90e-05, 'LOW-ok', 2),
    ('qwen3',      '12_15b', 'grpo'):      (1.08e-04, 'LOW', 1),
    ('qwen3',      '15_35b', 'dpo'):       (2.25e-05, 'LOW', 1),
    ('qwen3',      '15_35b', 'instruct'):  (2.01e-04, 'LOW', 1),

    # --- starcoder2 ---
    ('starcoder2', '2_4b', 'dpo'):         (7.97e-06, 'LOW', 1),
    ('starcoder2', '2_4b', 'grpo'):        (1.03e-04, 'LOW', 1),
}


# ── Lookup ───────────────────────────────────────────────────────────────

# Adjacent-bucket fallback order for missing exact bucket.
SIZE_BUCKET_ORDER = [
    "0_1b", "1_2b", "2_4b", "4_5b", "5_9b",
    "9_12b", "12_15b", "15_35b", "35_80b", "80b+",
]


# Confidence ordering for filtering at call-site.
CONFIDENCE_RANK = {
    "HIGH": 5,
    "MED": 4,
    "MED-low": 3,
    "LOW-ok": 2,
    "LOW": 1,
}


def confidence_meets(conf: str, min_conf: str = "LOW-ok") -> bool:
    """Return True if `conf` is at-least `min_conf` (including -ADJ suffix)."""
    if not conf:
        return False
    base = conf.split("-ADJ")[0]  # strip adjacent-bucket suffix
    if base == "FAMILY-FALLBACK":
        return False  # never trust geomean fallback as anchor
    return CONFIDENCE_RANK.get(base, 0) >= CONFIDENCE_RANK.get(min_conf, 0)


def lookup_lr(
    *,
    architecture: str,
    size_b: Optional[float],
    task: str,
) -> Optional[Tuple[float, str, int]]:
    """Return (lr, confidence, n) from family table, or None when miss.

    Caller treats None as "fall back to next tier".

    Lookup order:
      1. Exact (family, bucket, task)
      2. Adjacent bucket (±1, ±2) within same (family, task)
      3. Same family + task across all buckets → geomean (last resort, conf=FAMILY-FALLBACK)
      4. None — caller falls back

    `task` must be one of {"dpo", "grpo", "grpo_python", "instruct"};
    pass it lowercased and underscored from caller.
    """
    family = family_from_architecture(architecture)
    if family is None:
        return None

    bucket = size_bucket(size_b)
    if bucket is None:
        return None

    # 1. Exact hit
    key = (family, bucket, task)
    if key in FAMILY_LR_TABLE:
        return FAMILY_LR_TABLE[key]

    # 2. Adjacent bucket (±1, ±2 step)
    if bucket in SIZE_BUCKET_ORDER:
        idx = SIZE_BUCKET_ORDER.index(bucket)
        for offset in (1, -1, 2, -2):
            adj_idx = idx + offset
            if 0 <= adj_idx < len(SIZE_BUCKET_ORDER):
                adj_bucket = SIZE_BUCKET_ORDER[adj_idx]
                key = (family, adj_bucket, task)
                if key in FAMILY_LR_TABLE:
                    lr, conf, n = FAMILY_LR_TABLE[key]
                    return (lr, f"{conf}-ADJ", n)

    # 3. Family+task across all buckets (geomean fallback)
    family_lrs = [
        v[0] for k, v in FAMILY_LR_TABLE.items()
        if k[0] == family and k[2] == task
    ]
    if family_lrs:
        import math
        log_mean = sum(math.log(x) for x in family_lrs) / len(family_lrs)
        return (math.exp(log_mean), "FAMILY-FALLBACK", len(family_lrs))

    return None


def stats() -> dict:
    """Return summary stats for the table."""
    from collections import Counter
    conf_counts = Counter(v[1] for v in FAMILY_LR_TABLE.values())
    family_counts = Counter(k[0] for k in FAMILY_LR_TABLE.keys())
    return {
        "total_cells": len(FAMILY_LR_TABLE),
        "by_confidence": dict(conf_counts),
        "by_family": dict(family_counts),
    }


if __name__ == "__main__":
    print("FAMILY_LR_TABLE stats:", stats())
    print()
    cases = [
        ("LlamaForCausalLM",  7.0, "dpo"),
        ("Qwen2ForCausalLM",  1.5, "instruct"),    # Round 2 KITA fail case
        ("Qwen3ForCausalLM",  1.7, "instruct"),    # Round 3 task 0f26c1d3
        ("OPTForCausalLM",    0.35, "instruct"),   # Round 1 KITA crash case
        ("Phi3ForCausalLM",   3.8, "instruct"),
        ("MysteryArch",       7.0, "dpo"),
    ]
    for arch, size, task in cases:
        result = lookup_lr(architecture=arch, size_b=size, task=task)
        print(f"  {arch:25s} {str(size):>6s}b {task:14s} → {result}")
