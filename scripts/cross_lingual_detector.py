"""Cross-lingual mismatch detection — multi-signal.

Uses THREE independent signals to decide whether a training task is
cross-lingual (dataset language doesn't match base model's training
language), then combines them with a tiered-priority strategy.

Signal 1: Tokenizer fertility (tokens/char on dataset samples)
  High fertility signals tokenizer encodes the text inefficiently, which
  typically correlates with out-of-distribution language.

Signal 2: Dataset dominant script (Unicode range counting)
  Directly identifies the script family (latin/cyrillic/thai/cjk/etc)
  without any library dependency.

Signal 3: Model classification via catalog
  Recognizes known multilingual models (Qwen, Llama-3 base, Mistral-Nemo)
  and known language-specific models (DeepMount00/Llama-3-8b-Ita, etc).
  Catalog derived from .agent/data/validator_models.json scan.

Combination strategy (priority order):
  1. Model is MULTILINGUAL → NOT cross-lingual (it handles diverse data)
  2. Model is LANG_SPECIFIC + dataset script mismatches → cross-lingual
  3. Model is WESTERN_DEFAULT + dataset script is non-Latin → cross-lingual
  4. Otherwise → use fertility threshold as tiebreaker

Library-free. Relies only on the tokenizer training already loads.

Backward compatibility:
  `detect_cross_lingual(tokenizer, samples)` without `model_name` still
  works (falls back to fertility-only).
"""
from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List, Optional, Tuple


# --------------------------------------------------------------------------- #
# Tuning constants
# --------------------------------------------------------------------------- #

DEFAULT_FERTILITY_THRESHOLD = 0.4
DEFAULT_MIN_SAMPLES = 5
DEFAULT_MAX_SAMPLES = 20
MIN_SAMPLE_CHAR_LEN = 10


# --------------------------------------------------------------------------- #
# Signal 3 — vocab-size heuristic (anon-resilient)
# --------------------------------------------------------------------------- #

# Most English-only models have vocab_size ~32k-50k (Llama-2: 32k, Mistral: 32k,
# Phi: 51k). Multilingual models have noticeably larger vocabs to allocate
# tokens for non-Latin scripts (Llama-3: 128k, Qwen2: 151k, Qwen3: 151k).
# Threshold 100k cleanly separates these classes. lang_specific is no longer
# detectable without model_name — folded into "default".
MULTILINGUAL_VOCAB_THRESHOLD = 100_000


def classify_model(
    vocab_size: Optional[int] = None,
) -> Tuple[str, Optional[str]]:
    """Classify base model into one of: multilingual, default.

    vocab_size ≥ 100k → multilingual (Llama-3, Qwen2/3, etc).
    Otherwise default. lang_specific bucket dropped (was name-keyed).

    Returns (category, None).
    """
    if vocab_size and vocab_size >= MULTILINGUAL_VOCAB_THRESHOLD:
        return ("multilingual", None)
    return ("default", None)


# --------------------------------------------------------------------------- #
# Signal 2 — Unicode script detection
# --------------------------------------------------------------------------- #

# Unicode ranges for major scripts. `other` catches anything outside these
# (emojis, CJK symbols, etc).
SCRIPT_RANGES: List[Tuple[str, int, int]] = [
    ("latin",    0x0020, 0x024F),
    ("cyrillic", 0x0400, 0x04FF),
    ("greek",    0x0370, 0x03FF),
    ("arabic",   0x0600, 0x06FF),
    ("hebrew",   0x0590, 0x05FF),
    ("thai",     0x0E00, 0x0E7F),
    ("devanagari", 0x0900, 0x097F),
    # CJK blocks
    ("chinese",  0x4E00, 0x9FFF),   # CJK Unified Ideographs
    ("hiragana", 0x3040, 0x309F),   # Japanese
    ("katakana", 0x30A0, 0x30FF),   # Japanese
    ("hangul",   0xAC00, 0xD7AF),   # Korean
]


def detect_dominant_script(samples: List[str]) -> str:
    """Return the script family that dominates non-whitespace/non-ASCII-punct
    characters in `samples`. Returns 'latin' if majority is Latin (including
    ASCII) — the common default.
    """
    counts: Counter = Counter()
    for text in samples:
        if not isinstance(text, str):
            continue
        for ch in text:
            cp = ord(ch)
            # Skip whitespace and control chars
            if cp < 0x20 or ch.isspace():
                continue
            classified = False
            for name, lo, hi in SCRIPT_RANGES:
                if lo <= cp <= hi:
                    counts[name] += 1
                    classified = True
                    break
            if not classified:
                counts["other"] += 1
    if not counts:
        return "latin"  # safe default
    return counts.most_common(1)[0][0]


# Language code → expected dominant script
LANG_TO_SCRIPT: Dict[str, str] = {
    "en": "latin", "it": "latin", "es": "latin", "fr": "latin",
    "de": "latin", "pt": "latin", "nl": "latin",
    "ja": "hiragana",    # may also have chinese/katakana
    "ko": "hangul",
    "zh": "chinese",
    "th": "thai",
    "ru": "cyrillic", "uk": "cyrillic", "bg": "cyrillic",
    "ar": "arabic",
    "he": "hebrew",
    "hi": "devanagari",
}


def _matches_model_language(model_lang: str, dataset_script: str) -> bool:
    """Does the dataset script match the model's expected language script?"""
    expected = LANG_TO_SCRIPT.get(model_lang)
    if expected is None:
        return False
    # Japanese is a special case — uses multiple scripts
    if model_lang == "ja":
        return dataset_script in ("hiragana", "katakana", "chinese")
    return dataset_script == expected


# --------------------------------------------------------------------------- #
# Signal 1 — tokenizer fertility (unchanged)
# --------------------------------------------------------------------------- #


def _compute_fertility(
    tokenizer: Any, samples: List[str]
) -> Tuple[Optional[float], int]:
    """Returns (fertility_or_None, num_valid_samples)."""
    valid = [s for s in samples if isinstance(s, str) and len(s) >= MIN_SAMPLE_CHAR_LEN]
    valid = valid[:DEFAULT_MAX_SAMPLES]
    if len(valid) < DEFAULT_MIN_SAMPLES:
        return (None, len(valid))
    total_chars = 0
    total_tokens = 0
    try:
        for text in valid:
            total_chars += len(text)
            total_tokens += len(tokenizer.encode(text, add_special_tokens=False))
    except Exception:
        return (None, len(valid))
    if total_chars == 0:
        return (None, len(valid))
    return (total_tokens / total_chars, len(valid))


# --------------------------------------------------------------------------- #
# Main entry point — combines signals
# --------------------------------------------------------------------------- #


def detect_cross_lingual(
    tokenizer: Any,
    samples: Optional[List[str]],
    vocab_size: Optional[int] = None,
    threshold: float = DEFAULT_FERTILITY_THRESHOLD,
) -> Dict[str, Any]:
    """Multi-signal cross-lingual detection (anon-resilient).

    Signals: tokenizer fertility on dataset, dominant Unicode script,
    and vocab_size heuristic for multilingual classification.

    Returns dict with keys:
      is_cross_lingual : bool
      reason           : str (human-readable explanation of decision)
      fertility        : float | None
      dataset_script   : str
      model_category   : str (multilingual | default)
      model_lang       : str | None (always None — lang_specific dropped)
    """
    # Guard: inputs
    if tokenizer is None:
        return {"is_cross_lingual": False, "reason": "no tokenizer",
                "fertility": None, "dataset_script": "unknown",
                "model_category": "default", "model_lang": None}
    if not samples:
        return {"is_cross_lingual": False, "reason": "no samples",
                "fertility": None, "dataset_script": "unknown",
                "model_category": "default", "model_lang": None}

    # Signal 1: fertility
    fertility, n_valid = _compute_fertility(tokenizer, samples)
    if fertility is None:
        return {"is_cross_lingual": False,
                "reason": f"fertility not computable (n_valid={n_valid})",
                "fertility": None, "dataset_script": "unknown",
                "model_category": "default", "model_lang": None}

    # Signal 2: dataset script
    dataset_script = detect_dominant_script(samples[:DEFAULT_MAX_SAMPLES])

    # Signal 3: model classification
    model_cat, model_lang = classify_model(vocab_size=vocab_size)

    # Decision tree (priority order)
    base = {
        "fertility": round(fertility, 3),
        "dataset_script": dataset_script,
        "model_category": model_cat,
        "model_lang": model_lang,
    }

    # Priority 1: MULTILINGUAL models — never flag
    if model_cat == "multilingual":
        return {
            "is_cross_lingual": False,
            "reason": (
                f"multilingual model handles diverse data natively "
                f"(fertility={fertility:.3f}, script={dataset_script})"
            ),
            **base,
        }

    # Priority 2: LANG_SPECIFIC model + mismatched script
    if model_cat == "lang_specific" and model_lang:
        if not _matches_model_language(model_lang, dataset_script):
            return {
                "is_cross_lingual": True,
                "reason": (
                    f"lang-specific model ({model_lang}) trained for "
                    f"{LANG_TO_SCRIPT.get(model_lang, '?')}, but dataset is "
                    f"{dataset_script} (fertility={fertility:.3f})"
                ),
                **base,
            }
        else:
            return {
                "is_cross_lingual": False,
                "reason": (
                    f"lang-specific model ({model_lang}) matches dataset script "
                    f"({dataset_script}), fertility={fertility:.3f}"
                ),
                **base,
            }

    # Priority 3: DEFAULT model (English/Latin-trained) + non-Latin script
    if model_cat == "default" and dataset_script not in ("latin", "unknown"):
        return {
            "is_cross_lingual": True,
            "reason": (
                f"default (Latin-trained) model + non-Latin script "
                f"({dataset_script}), fertility={fertility:.3f}"
            ),
            **base,
        }

    # Priority 4: fallback — fertility-only tiebreaker (catches novel cases)
    is_cross = fertility > threshold
    return {
        "is_cross_lingual": is_cross,
        "reason": (
            f"fallback fertility test: {fertility:.3f} "
            f"{'>' if is_cross else '<='} {threshold} "
            f"(script={dataset_script}, category={model_cat})"
        ),
        **base,
    }


# --------------------------------------------------------------------------- #
# Override spec
# --------------------------------------------------------------------------- #


def get_overrides(fingerprint: Dict[str, Any]) -> Dict[str, Any]:
    """Training overrides when cross-lingual is detected."""
    if not fingerprint.get("is_cross_lingual"):
        return {}
    return {
        "skip_refinement": True,
    }
