"""Identify base model + detect augmentation from config + baseline_stats.

Post G.O.D feature/model-prep-container merge (2026-05-13), the validator
sends miner an anonymized model_id (gradients-io/augmented-<sha16>) plus
optional BASELINE_STATS env var. Validator's scrub_model_identity() removes
`_name_or_path` from config.json BUT preserves architecture-defining fields
(hidden_size, num_hidden_layers, vocab_size, intermediate_size, architectures).

This module:
1. identify_base_model(model_dir): match config fingerprint → original model_id
2. detect_augmentation(baseline_stats, base_model): infer augmentation type
   from observed weight_rms vs canonical reference

Both are FAIL-SOFT: missing data → confidence=0.0 → caller falls back to
existing flow (e.g. _FAMILY_PROFILES[arch_family] in adaptive_config.py).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional


_CATALOG: Optional[dict] = None
_CANONICAL: Optional[dict] = None


def _load_catalog() -> tuple[dict, dict]:
    """Lazy-load catalog + canonical RMS. Cached after first call."""
    global _CATALOG, _CANONICAL
    if _CATALOG is not None and _CANONICAL is not None:
        return _CATALOG, _CANONICAL

    d = Path(__file__).parent
    cat_path = d / "model_fingerprint_catalog.json"
    can_path = d / "canonical_weight_rms.json"

    _CATALOG = {}
    _CANONICAL = {}
    try:
        if cat_path.exists():
            _CATALOG = json.load(open(cat_path))
        if can_path.exists():
            _CANONICAL = json.load(open(can_path))
    except Exception as exc:
        print(f"[model_detection] catalog load failed (skipped): {exc}", flush=True)

    return _CATALOG, _CANONICAL


def _fingerprint_from_config(cfg: dict) -> str:
    """Build fingerprint key from config dict — matches build_fingerprint_catalog.py."""
    return ",".join(
        str(cfg.get(k, "")) for k in (
            "hidden_size", "num_hidden_layers", "vocab_size", "intermediate_size",
        )
    )


def _arch_to_family(arch: str) -> str:
    """Mirror scripts/dynamics_utils.py family naming. Used as fallback when
    catalog has no fingerprint match — we can still identify the family from
    `architectures` field (NOT scrubbed by validator)."""
    a = (arch or "").lower()
    if "qwen" in a:
        return "qwen"
    if "llama" in a:
        if "shear" in a or "tinyllama" in a:
            return "tinyllama"
        return "llama"
    if "gemma" in a:
        return "gemma"
    if "phi" in a:
        return "phi"
    if "smollm" in a:
        return "smollm"
    if "mistral" in a:
        return "mistral"
    return "unknown"


def identify_base_model(model_dir: str) -> dict:
    """Recover original base_model_id from anonymized model directory.

    Reads config.json (preserved fields after _name_or_path scrub) and matches
    against fingerprint catalog.

    Returns dict with keys:
      base_model: str | None     — original HF model_id if matched (None if catalog miss)
      family: str                — arch family ("qwen", "llama", "smollm", ..., "unknown")
      arch: str                  — architectures[0] field (e.g., "Qwen2ForCausalLM")
      confidence: float          — 1.0 (fingerprint match), 0.5 (arch family only), 0.0 (no info)
      fingerprint_key: str       — for diagnostics
    """
    catalog, _ = _load_catalog()

    cfg_path = Path(model_dir) / "config.json"
    if not cfg_path.exists():
        return {"base_model": None, "family": "unknown", "arch": "",
                "confidence": 0.0, "fingerprint_key": ""}

    try:
        with open(cfg_path) as f:
            cfg = json.load(f)
    except Exception as exc:
        print(f"[model_detection] config.json read failed (skipped): {exc}", flush=True)
        return {"base_model": None, "family": "unknown", "arch": "",
                "confidence": 0.0, "fingerprint_key": ""}

    fp_key = _fingerprint_from_config(cfg)
    arch = (cfg.get("architectures") or [""])[0]

    # Tier 1: exact fingerprint match
    entry = catalog.get(fp_key)
    if entry:
        return {
            "base_model": entry.get("base_model"),
            "family": entry.get("family", _arch_to_family(arch)),
            "arch": entry.get("arch", arch),
            "confidence": 1.0,
            "fingerprint_key": fp_key,
        }

    # Tier 2: family-only fallback (arch known but specific model unrecognized)
    family = _arch_to_family(arch)
    return {
        "base_model": None,
        "family": family,
        "arch": arch,
        "confidence": 0.5 if family != "unknown" else 0.0,
        "fingerprint_key": fp_key,
    }


# Augmentation detection thresholds (data-driven from G.O.D constants)
# Source: validator/core/constants.py:AUGMENTATION_INTENSITY_RANGES
#   weight_scaling: (0.8, 1.2)
#   gaussian_noise: (0.005, 0.02)
#   magnitude_pruning: (0.05, 0.15)
#   layer_reinit: (0.01, 0.05)

# WEIGHT_SCALING: rms ratio = scale_factor (linear)
_SCALE_LO_RANGE = (0.78, 0.82)   # intensity ~0.8 with small slack
_SCALE_HI_RANGE = (1.18, 1.22)   # intensity ~1.2 with small slack

# GAUSSIAN_NOISE: rms ratio = sqrt(1 + intensity^2 * (std/mean)^2) ≈ 1 + tiny
# For typical layer std/mean ratio, expect ratio in (1.0001, 1.005) for 0.5-2% noise
_NOISE_RANGE = (1.0001, 1.005)

# LAYER_REINIT: most groups untouched; affected group's rms changes drastically
_REINIT_OUTLIER_THRESHOLD = 0.3   # |ratio - 1.0| > 0.3 considered outlier

# MAGNITUDE_PRUNING: rms drops as small weights zeroed (no scale uniformity)
_PRUNE_RANGE = (0.85, 0.99)


def detect_augmentation(baseline_stats: dict, base_model: str) -> dict:
    """Infer augmentation type from observed weight_rms vs canonical reference.

    Args:
        baseline_stats: BASELINE_STATS env JSON. Expected schema:
            baseline_stats["weights"]["by_group"][<group>] = {weight_rms, weight_norm, max_abs}
            (per core/models/model_prep_models.py LayerGroupWeightStats)
        base_model: base model_id to look up canonical reference

    Returns dict with keys:
        detected_type: str | None  — one of WEIGHT_SCALING, GAUSSIAN_NOISE,
                                     MAGNITUDE_PRUNING, LAYER_REINIT, or None
        intensity: float | None    — estimated intensity (only for WEIGHT_SCALING)
        confidence: float          — 0.0 (no detection) to ~0.85 (high)
        affected_groups: list[str] — layer groups showing the pattern
        ratios: dict               — observed/canonical ratio per group (diagnostic)

    Fail-soft: missing canonical reference, missing baseline_stats, or
    unparseable structure → all return {detected_type: None, confidence: 0.0}.
    """
    _, canonical_db = _load_catalog()

    canonical = canonical_db.get(base_model) if base_model else None
    if not canonical:
        return {"detected_type": None, "intensity": None, "confidence": 0.0,
                "affected_groups": [], "ratios": {}}

    try:
        observed = baseline_stats.get("weights", {}).get("by_group", {})
    except Exception:
        return {"detected_type": None, "intensity": None, "confidence": 0.0,
                "affected_groups": [], "ratios": {}}

    if not observed:
        return {"detected_type": None, "intensity": None, "confidence": 0.0,
                "affected_groups": [], "ratios": {}}

    # Compute per-group ratios = observed_rms / canonical_rms
    ratios: dict[str, float] = {}
    for group, ref_rms in canonical.items():
        if ref_rms <= 0:
            continue
        obs_entry = observed.get(group)
        if not obs_entry:
            continue
        obs_rms = obs_entry.get("weight_rms")
        if obs_rms is None:
            continue
        ratios[group] = obs_rms / ref_rms

    if not ratios:
        return {"detected_type": None, "intensity": None, "confidence": 0.0,
                "affected_groups": [], "ratios": {}}

    half_threshold = max(1, len(ratios) // 2)

    # Helper: is r within unity tolerance (untouched layer)?
    def _is_unity(r: float, tol: float = 0.02) -> bool:
        return abs(r - 1.0) < tol

    # Pattern 1: WEIGHT_SCALING (all_layers / multi_layer / layer_type_group scopes)
    # All non-unity ratios should cluster around a SINGLE value in [0.8, 1.2].
    # This handles intensity beyond exact 0.8/1.2 by checking ratio uniformity
    # (variance check) AND that values are within validator range.
    non_unity = [(g, r) for g, r in ratios.items() if not _is_unity(r)]
    if len(non_unity) >= half_threshold:
        rs = [r for _, r in non_unity]
        in_scale_range = all(0.78 <= r <= 1.22 for r in rs) and not any(_is_unity(r) for r in rs)
        if in_scale_range:
            mean_r = sum(rs) / len(rs)
            # Check uniformity: all non-unity ratios within tight band of each other
            max_dev = max(abs(r - mean_r) for r in rs)
            if max_dev < 0.03:  # tight cluster → WEIGHT_SCALING
                return {
                    "detected_type": "WEIGHT_SCALING",
                    "intensity": float(mean_r),
                    "confidence": 0.85,
                    "affected_groups": [g for g, _ in non_unity],
                    "ratios": ratios,
                }

    # Pattern 2: WEIGHT_SCALING single_layer scope
    # Exactly 1 group in scale range [0.8, 1.2] (excluding unity), others ~1.0.
    single_scaled = [g for g, r in ratios.items() if (0.78 <= r <= 1.22) and not _is_unity(r)]
    others_unity = sum(1 for r in ratios.values() if _is_unity(r))
    if len(single_scaled) == 1 and others_unity >= len(ratios) - 1:
        g = single_scaled[0]
        return {
            "detected_type": "WEIGHT_SCALING",
            "intensity": float(ratios[g]),
            "confidence": 0.7,  # lower than uniform since ambiguous with LAYER_REINIT
            "affected_groups": single_scaled,
            "ratios": ratios,
        }

    # Pattern 3: GAUSSIAN_NOISE — most groups slightly elevated
    noisy = [g for g, r in ratios.items() if _NOISE_RANGE[0] < r < _NOISE_RANGE[1]]
    if len(noisy) >= half_threshold:
        return {
            "detected_type": "GAUSSIAN_NOISE",
            "intensity": None,  # cannot reliably back out from rms alone
            "confidence": 0.6,
            "affected_groups": noisy,
            "ratios": ratios,
        }

    # Pattern 4: LAYER_REINIT — exactly 1 group is wildly off (|r-1| > 0.3)
    # AND outside scale range (rules out WEIGHT_SCALING single_layer).
    outliers = [g for g, r in ratios.items()
                if abs(r - 1.0) > _REINIT_OUTLIER_THRESHOLD
                and not (0.78 <= r <= 1.22)]
    if len(outliers) == 1 and len(ratios) > 1:
        return {
            "detected_type": "LAYER_REINIT",
            "intensity": None,
            "confidence": 0.5,
            "affected_groups": outliers,
            "ratios": ratios,
        }

    # Pattern 5: MAGNITUDE_PRUNING — most groups show small drop, NOT uniform
    # (rules out WEIGHT_SCALING which would be uniform).
    drops = [g for g, r in ratios.items() if _PRUNE_RANGE[0] < r < _PRUNE_RANGE[1]]
    if len(drops) >= half_threshold:
        drop_rs = [ratios[g] for g in drops]
        max_dev = max(abs(r - sum(drop_rs)/len(drop_rs)) for r in drop_rs)
        if max_dev > 0.03:  # high variance in drops → likely PRUNING (sparsity-driven)
            return {
                "detected_type": "MAGNITUDE_PRUNING",
                "intensity": None,
                "confidence": 0.4,
                "affected_groups": drops,
                "ratios": ratios,
            }

    # No clear pattern
    return {"detected_type": None, "intensity": None, "confidence": 0.0,
            "affected_groups": [], "ratios": ratios}
