"""
Defensive tokenizer_config.json sanitizer for anonymized models.

Background
==========
Validator's G.O.D `feature/model-prep-container` calls
`tokenizer.push_to_hub()` after weight augmentation. For Qwen2-family
tokenizers, HF transformers serializes `extra_special_tokens` as a
**list of token strings** instead of a **dict** — a known transformers
serialization quirk:

    "extra_special_tokens": [
        "<|im_start|>", "<|im_end|>", "<|object_ref_start|>", ...
    ]

When a downstream consumer calls `AutoTokenizer.from_pretrained()` on
that repo, transformers crashes:

    AttributeError: 'list' object has no attribute 'keys'
    at tokenization_utils_base.py:1190
        self.SPECIAL_TOKENS_ATTRIBUTES + list(special_tokens.keys())

This module repairs the cached `tokenizer_config.json` BEFORE any
tokenizer load, by removing the malformed `extra_special_tokens` field.
The tokenizer rebuilds special tokens from `tokenizer.json` (which has
correctly-formed `added_tokens` data).

Idempotent: safe to call multiple times. Fail-soft: any error logged
and skipped (won't block training).

Trigger: G.O.D anonymized models (post `feature/model-prep-container`).
Pre-anon models pass through unchanged (no `extra_special_tokens` field).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


_SENTINEL_FIELD = "extra_special_tokens"

# 2026-05-14: Known anonymization-placeholder tokenizer_class values that don't
# exist as real transformers tokenizer classes. When found, remove field so
# AutoTokenizer falls back to architecture-based detection (config.json
# `model_type` → matching tokenizer class).
_PLACEHOLDER_TOKENIZER_CLASSES = {
    "TokenizersBackend",  # Llama-3.2-3B-Instruct augmented (task 0d824)
}


def sanitize_tokenizer_config(model_dir: str) -> bool:
    """Repair malformed tokenizer_config.json in place.

    Returns True if any fix was applied, False if no-op (already clean).
    Fail-soft on errors (logs + returns False).

    Handles TWO known anon-related issues:
    1. `extra_special_tokens` serialized as list instead of dict (Qwen2 anon).
    2. `tokenizer_class` set to anon placeholder ("TokenizersBackend" etc) that
       isn't a real transformers class → AutoTokenizer ValueError.
    """
    cfg_path = Path(model_dir) / "tokenizer_config.json"
    if not cfg_path.exists():
        return False

    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except Exception as exc:
        print(f"[tokenizer-sanitize] read fail (skip): {cfg_path}: {exc}", flush=True)
        return False

    if not isinstance(cfg, dict):
        return False

    fixed = False

    # Fix 1: malformed extra_special_tokens (list → drop, rebuilt from tokenizer.json)
    raw = cfg.get(_SENTINEL_FIELD)
    if raw is not None and isinstance(raw, list):
        del cfg[_SENTINEL_FIELD]
        print(
            f"[tokenizer-sanitize] removed malformed `{_SENTINEL_FIELD}` "
            f"(was list of {len(raw)} tokens) from {cfg_path}",
            flush=True,
        )
        fixed = True

    # Fix 2: placeholder tokenizer_class (anon scrubbing). Remove so AutoTokenizer
    # falls back to architecture lookup via config.json model_type.
    tc = cfg.get("tokenizer_class")
    if isinstance(tc, str) and tc in _PLACEHOLDER_TOKENIZER_CLASSES:
        del cfg["tokenizer_class"]
        print(
            f"[tokenizer-sanitize] removed placeholder tokenizer_class='{tc}' "
            f"from {cfg_path} (AutoTokenizer will fall back to model_type)",
            flush=True,
        )
        fixed = True

    if not fixed:
        return False

    try:
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    except Exception as exc:
        print(f"[tokenizer-sanitize] write fail (skip): {cfg_path}: {exc}", flush=True)
        return False

    return True


def maybe_sanitize_for_anon_model(model_path: str) -> None:
    """Best-effort sanitizer entry point — call after model is in cache,
    before any AutoTokenizer.from_pretrained().

    Disable: TRAINING_TOKENIZER_SANITIZE_ENABLED=0

    DDP guard 2026-05-12: defense-in-depth — if invoked from a rank-N
    process (LOCAL_RANK!=0), skip. Currently only called from
    text_trainer.py orchestrator (single-process), but this guard
    prevents race if validator ever invokes from rank entrypoints.
    """
    if os.getenv("TRAINING_TOKENIZER_SANITIZE_ENABLED", "1") != "1":
        return
    # Multi-process safety: rank-0 only writes the shared config file.
    try:
        _local_rank = int(os.getenv("LOCAL_RANK", "0"))
    except (TypeError, ValueError):
        _local_rank = 0
    if _local_rank != 0:
        return
    try:
        sanitize_tokenizer_config(model_path)
    except Exception as exc:
        # Outer fail-soft (sanitize_tokenizer_config already fail-soft, but belt+suspenders)
        print(f"[tokenizer-sanitize] outer fail (skip): {exc}", flush=True)
