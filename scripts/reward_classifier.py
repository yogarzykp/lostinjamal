"""GRPO reward-function classifier → LR range suggestion.

Static analysis of a GRPO task's reward function mix to predict an
appropriate learning rate range. Tournament tasks draw reward functions
from a fixed pool of ~13 generic functions (verified across 38 tasks);
this module catalogs them and derives a "landscape fingerprint" from the
specific mix used in a task.

Why: LLM warmstart sees only model name + task type + data size. It cannot
see the reward function code, so it can misjudge LR for tasks with unusual
reward landscapes (e.g. c989b095 where conflicting length rewards + an
unbounded penalty needed LR 5e-6, but LLM picked 2e-5 → -37% LOSE).

Flow:
  reward_functions (list) → classify_reward_mix() → fingerprint dict
  fingerprint + model_size → suggest_lr_range() → (lr_min, lr_max) or None

None return means an unknown reward function was encountered; caller
should fall back to LLM warmstart in that case.
"""
from __future__ import annotations

import math
import re
from typing import Dict, List, Optional, Tuple


# --------------------------------------------------------------------------- #
# Catalog of known generic reward functions (38 tasks observed, 13 unique)
# --------------------------------------------------------------------------- #

# Each entry describes:
#   direction : "+" (higher reward for more of X) or "-" (penalty for more of X)
#   magnitude : "unbounded" | "bounded" | "bounded_medium" | "small" | "unit" | "binary"
#     - unbounded:   scales with output length (can reach ±1000s)
#     - bounded:     natural cap (e.g. words/sentence usually 5-50)
#     - bounded_medium: target-based penalty (e.g. distance from n=30 words)
#     - small:       per-word metric (~3-10)
#     - unit:        percentage in [0, 1]
#     - binary:      {0, 1}
#   theme     : "length" | "vocab_length" | "vocab" | "content" | "format"
REWARD_CATALOG: Dict[str, Dict] = {
    "reward_long_completions":                {"direction": "+", "magnitude": "unbounded",       "theme": "length"},
    "reward_short_completions":               {"direction": "-", "magnitude": "unbounded",       "theme": "length"},
    "reward_specific_word_count":             {"direction": "-", "magnitude": "bounded_medium",  "theme": "length"},
    "reward_specific_char_count":             {"direction": "-", "magnitude": "bounded_medium",  "theme": "length"},
    "reward_long_words":                      {"direction": "+", "magnitude": "small",           "theme": "vocab_length"},
    "reward_short_words":                     {"direction": "-", "magnitude": "small",           "theme": "vocab_length"},
    "reward_long_sentences":                  {"direction": "+", "magnitude": "bounded",         "theme": "length"},
    "reward_short_sentences":                 {"direction": "-", "magnitude": "bounded",         "theme": "length"},
    "reward_reasoning_keywords":              {"direction": "+", "magnitude": "bounded",         "theme": "content"},
    "reward_think_answer_format":             {"direction": "+", "magnitude": "binary",          "theme": "format"},
    "reward_high_unique_words_percentage":    {"direction": "+", "magnitude": "unit",            "theme": "vocab"},
    "reward_low_unique_words_percentage":     {"direction": "-", "magnitude": "unit",            "theme": "vocab"},
    "reward_high_difficult_words_percentage": {"direction": "+", "magnitude": "unit",            "theme": "vocab"},
}

# Reward functions that directly oppose each other on the same theme.
# Indirect conflicts (e.g. long_completions vs specific_char_count target=100)
# are also included: long rewards verbosity, target-based penalizes deviation
# from a small target.
CONFLICT_PAIRS: List[Tuple[str, str]] = [
    # direct opposites (same theme, opposite direction)
    ("reward_long_completions",              "reward_short_completions"),
    ("reward_long_words",                    "reward_short_words"),
    ("reward_long_sentences",                "reward_short_sentences"),
    ("reward_high_unique_words_percentage",  "reward_low_unique_words_percentage"),
    # indirect: unbounded-length-growth vs target-based length caps
    ("reward_long_completions",              "reward_specific_char_count"),
    ("reward_long_completions",              "reward_specific_word_count"),
    ("reward_long_sentences",                "reward_specific_char_count"),
    ("reward_long_completions",              "reward_short_sentences"),
]


# --------------------------------------------------------------------------- #
# Extraction + classification
# --------------------------------------------------------------------------- #


def extract_function_name(reward_func_code: str) -> Optional[str]:
    """Pull the `def NAME(...)` identifier from a reward-function source."""
    m = re.search(r"def\s+(\w+)\s*\(", reward_func_code or "")
    return m.group(1) if m else None


def classify_reward_mix(reward_functions: List[Dict]) -> Dict:
    """Classify a list of GRPO reward-function configs into a fingerprint.

    Parameters
    ----------
    reward_functions : list of dict
        Each item has keys ``reward_func`` (source code str) and
        ``reward_weight`` (float). Matches the ``reward_functions`` field
        in a GRPO task's ``dataset_type``.

    Returns
    -------
    dict
        Always contains: n_functions, known_functions, unknown_functions,
        coverage, landscape. If coverage == 1.0, also includes
        net_direction, has_unbounded_positive/negative, conflict_pairs,
        dominant_theme, hack_risk.
    """
    known: List[Tuple[str, float]] = []
    unknown: List[Tuple[str, float]] = []
    for rf in reward_functions or []:
        code = rf.get("reward_func", "")
        weight = float(rf.get("reward_weight", 0) or 0)
        name = extract_function_name(code)
        if name and name in REWARD_CATALOG:
            known.append((name, weight))
        else:
            unknown.append((name or "?", weight))

    total_weight = sum(w for _, w in known) + sum(w for _, w in unknown)
    coverage = (sum(w for _, w in known) / total_weight) if total_weight > 0 else 0.0

    # Unknown function present → defer to LLM (safer than guessing)
    if unknown:
        return {
            "n_functions": len(reward_functions or []),
            "known_functions": known,
            "unknown_functions": unknown,
            "coverage": coverage,
            "landscape": "unknown",
        }

    # Direction & magnitude summaries
    names_set = {n for n, _ in known}
    pos_weight = sum(w for n, w in known if REWARD_CATALOG[n]["direction"] == "+")
    neg_weight = sum(w for n, w in known if REWARD_CATALOG[n]["direction"] == "-")
    if pos_weight > 0 and neg_weight == 0:
        net_direction = "+"
    elif neg_weight > 0 and pos_weight == 0:
        net_direction = "-"
    else:
        net_direction = "mixed"

    has_unbounded_pos = any(
        REWARD_CATALOG[n]["magnitude"] == "unbounded"
        and REWARD_CATALOG[n]["direction"] == "+"
        for n, _ in known
    )
    has_unbounded_neg = any(
        REWARD_CATALOG[n]["magnitude"] == "unbounded"
        and REWARD_CATALOG[n]["direction"] == "-"
        for n, _ in known
    )

    # Conflicts present in this task
    conflicts_found: List[Tuple[str, str]] = [
        (a, b) for a, b in CONFLICT_PAIRS
        if a in names_set and b in names_set
    ]

    # Dominant theme by cumulative weight
    theme_weights: Dict[str, float] = {}
    for n, w in known:
        t = REWARD_CATALOG[n]["theme"]
        theme_weights[t] = theme_weights.get(t, 0.0) + w
    dominant_theme = max(theme_weights, key=theme_weights.get) if theme_weights else "none"

    # Reward-hack risk: unbounded-positive contribution without unbounded-negative counter
    pos_unb_weight = sum(
        w for n, w in known
        if REWARD_CATALOG[n]["direction"] == "+"
        and REWARD_CATALOG[n]["magnitude"] == "unbounded"
    )
    neg_unb_weight = sum(
        w for n, w in known
        if REWARD_CATALOG[n]["direction"] == "-"
        and REWARD_CATALOG[n]["magnitude"] == "unbounded"
    )
    if pos_unb_weight > 0.15 and pos_unb_weight > neg_unb_weight * 2:
        hack_risk = "high"
    elif pos_unb_weight > 0:
        hack_risk = "medium"
    else:
        hack_risk = "low"

    # Landscape classification — risk check first, then structural checks.
    # (penalty-dominant mixes don't need their own category: the coherent
    # LR range 1-1.5e-5 is already safer than LLM's tendency to pick 2e-5
    # on such mixes; evidence: 24d4fb42 won at 1e-5 despite heavy unbounded
    # negative penalty.)
    if hack_risk == "high":
        landscape = "reward_hack"
    elif len(known) == 1:
        landscape = "single"
    elif conflicts_found:
        # Balanced if opposing functions have similar magnitude category AND weight
        balanced = True
        for a, b in conflicts_found:
            wa = next((w for n, w in known if n == a), 0)
            wb = next((w for n, w in known if n == b), 0)
            mag_a = REWARD_CATALOG[a]["magnitude"]
            mag_b = REWARD_CATALOG[b]["magnitude"]
            # Categorical magnitude mismatch: unbounded vs anything else
            if (mag_a == "unbounded") != (mag_b == "unbounded"):
                balanced = False
                break
            # Weight ratio too asymmetric
            if max(wa, wb) > 0 and min(wa, wb) / max(wa, wb) < 0.3:
                balanced = False
                break
        landscape = "balanced_conflict" if balanced else "imbalanced_conflict"
    else:
        landscape = "coherent"

    return {
        "n_functions": len(reward_functions or []),
        "known_functions": known,
        "unknown_functions": [],
        "coverage": 1.0,
        "net_direction": net_direction,
        "has_unbounded_positive": has_unbounded_pos,
        "has_unbounded_negative": has_unbounded_neg,
        "conflict_pairs": conflicts_found,
        "dominant_theme": dominant_theme,
        "hack_risk": hack_risk,
        "landscape": landscape,
    }


# --------------------------------------------------------------------------- #
# LR range suggestion
# --------------------------------------------------------------------------- #

# Base LR ranges per landscape (tuned on observed 7B GRPO results where
# LR=1e-5 consistently worked except for imbalanced conflict c989b095).
_BASE_RANGES: Dict[str, Tuple[float, float]] = {
    "single":              (8e-6, 2.0e-5),
    "coherent":            (1.0e-5, 1.5e-5),
    "balanced_conflict":   (1.0e-5, 1.5e-5),
    "imbalanced_conflict": (5.0e-6, 1.0e-5),
    "reward_hack":         (5.0e-6, 8.0e-6),
}


def _size_multiplier(model_size_b: Optional[float]) -> float:
    """Mild LR adjustment by model size.

    Smaller models tolerate slightly higher LR; very large models prefer
    slightly lower. Observed GRPO wins used LR=1e-5 for 2.78B-12B models,
    so the adjustment is subtle (±10-30%).
    """
    if model_size_b is None:
        return 1.0
    if model_size_b < 2:
        return 1.3
    if model_size_b < 5:
        return 1.1
    if model_size_b >= 10:
        return 0.9
    return 1.0


def suggest_lr_range(
    fingerprint: Dict,
    model_size_b: Optional[float] = None,
) -> Optional[Tuple[float, float]]:
    """Return an LR (min, max) range based on the fingerprint.

    ``None`` indicates the classifier cannot make a recommendation
    (unknown reward functions) — caller should fall back to LLM warmstart
    or a default.
    """
    landscape = fingerprint.get("landscape", "unknown")
    base = _BASE_RANGES.get(landscape)
    if base is None:
        return None
    mult = _size_multiplier(model_size_b)
    return (base[0] * mult, base[1] * mult)


def suggest_lr(
    fingerprint: Dict,
    model_size_b: Optional[float] = None,
) -> Optional[float]:
    """Pick a single LR from the suggested range (log-space midpoint).

    Returns ``None`` when the classifier has no opinion (unknown mix).
    """
    rng = suggest_lr_range(fingerprint, model_size_b)
    if rng is None:
        return None
    return math.sqrt(rng[0] * rng[1])


# --------------------------------------------------------------------------- #
# Beta (KL coefficient) suggestion
# --------------------------------------------------------------------------- #

# Training β anchors the policy to the reference model. Validator uses
# β_eval=0.5 in its final-score formula (normalized_reward − 0.5 × KL).
# Training β default is 0.04 — too weak when reward structure pushes the
# model far from base (reward-hack / imbalanced landscapes), producing
# high eval KL and a stiff penalty at scoring time.
#
# Rule: raise training β when hack_risk is elevated or landscape has
# conflict tension; keep default when rewards are bounded and balanced.
#
# UPDATE 2026-05-11 — Wave 1+2 eval finding: task 020b2f24 (opt-350m GRPO,
# single reward "reward_reasoning_keywords") catastrophically diverged →
# eval_loss = −0.0662 (winner +0.9871). Quality score → bottom 25% → −1
# penalty. Root cause: β=0.04 training (12.5× weaker than validator 0.5)
# allowed policy free drift over 2 epochs on tiny 350M model; validator
# KL penalty dominated at scoring. Memory cite (β=0.04 verified) was for
# 1.3B+ models (f5fbe40f, d878f32d) which drift slower.
# Patch: bump "single" + "coherent" → 0.10 (matches reward_hack level).
# Tiny-model rationale: smaller param → faster relative drift → need
# stronger anchor. Matches grpo_config.py:450 floor (β=0.10 for 7B+).
_BASE_BETA: Dict[str, float] = {
    "reward_hack":         0.10,  # unbounded + no counter; strong anchor
    "imbalanced_conflict": 0.06,  # mismatched magnitudes; moderate anchor
    "single":              0.10,  # was 0.04 — Wave 1+2 020b2f24 evidence
    "coherent":            0.10,  # was 0.04 — same rationale
    "balanced_conflict":   0.04,
}

# Additional boost if hack_risk is medium (unbounded+ but < threshold).
_HACK_RISK_MEDIUM_BOOST = 0.01


def suggest_beta(fingerprint: Dict) -> Optional[float]:
    """Suggest training β (KL coefficient) based on landscape.

    Returns ``None`` when classifier has no opinion.
    """
    landscape = fingerprint.get("landscape", "unknown")
    base = _BASE_BETA.get(landscape)
    if base is None:
        return None
    if fingerprint.get("hack_risk") == "medium":
        base += _HACK_RISK_MEDIUM_BOOST
    return base


def suggest_params(
    fingerprint: Dict,
    model_size_b: Optional[float] = None,
) -> Optional[Dict[str, float]]:
    """Full classifier-derived training parameters.

    Returns a dict with keys ``learning_rate`` and ``beta``, or ``None``
    when the classifier has no opinion (unknown reward functions).
    """
    lr = suggest_lr(fingerprint, model_size_b)
    beta = suggest_beta(fingerprint)
    if lr is None or beta is None:
        return None
    return {"learning_rate": lr, "beta": beta}


# --------------------------------------------------------------------------- #
# Diagnostic summary (for logging)
# --------------------------------------------------------------------------- #


def describe(fingerprint: Dict) -> str:
    """One-line human-readable summary for log output."""
    if fingerprint.get("landscape") == "unknown":
        unk = fingerprint.get("unknown_functions", [])
        unk_names = ", ".join(n for n, _ in unk) or "?"
        cov = fingerprint.get("coverage", 0.0)
        return f"unknown (coverage={cov:.0%}, unknown_fns=[{unk_names}])"
    parts = [
        f"landscape={fingerprint.get('landscape')}",
        f"net_dir={fingerprint.get('net_direction')}",
        f"theme={fingerprint.get('dominant_theme')}",
        f"hack_risk={fingerprint.get('hack_risk')}",
    ]
    conflicts = fingerprint.get("conflict_pairs", [])
    if conflicts:
        parts.append(f"conflicts={len(conflicts)}")
    return ", ".join(parts)
