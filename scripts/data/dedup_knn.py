"""Dataset dedup: exact hash + optional Jaccard n-gram near-duplicate removal.

Stdlib + numpy only — avoids any Docker image dependency changes
(dockerfiles stay 1:1 with master-text).

Two-stage filter:
  1. Exact hash dedup (MD5 over instruction+output) — always on when enabled.
     O(n), zero false positives, catches copies.
  2. Jaccard n-gram near-duplicate (optional) — opt-in with threshold.
     O(n²) pairwise; fine for typical tournament datasets <100K samples.
     Uses character k-grams of instruction field (default k=5).

Feature flags (read from env by tokenize_instruct.py caller):
  INSTRUCT_DEDUP=1                  → enable (default off, preserves winner behavior)
  INSTRUCT_DEDUP_JACCARD=<float>    → enable near-dup with this threshold
                                      (e.g. 0.85). 0 or unset → exact-only.
  INSTRUCT_DEDUP_NGRAM=<int>        → k for character n-grams (default 5)
  INSTRUCT_DEDUP_FIELD_INSTRUCT=<k> → instruction field name in dataset (default auto)
  INSTRUCT_DEDUP_FIELD_OUTPUT=<k>   → output field name (default auto)
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from typing import Any, Iterable

# Progress + safety knobs for O(n^2) Jaccard stage (overridable via env)
JACCARD_PROGRESS_EVERY = int(os.getenv("INSTRUCT_DEDUP_JACCARD_PROGRESS_EVERY", "500"))
JACCARD_MAX_SECONDS = int(os.getenv("INSTRUCT_DEDUP_JACCARD_MAX_SECONDS", "900"))  # 15 min default


def _canonical_text(sample: dict, instruct_keys: tuple[str, ...], output_keys: tuple[str, ...]) -> str:
    """Concatenate instruction + output with canonical whitespace."""
    instruct = ""
    for k in instruct_keys:
        v = sample.get(k)
        if isinstance(v, str) and v.strip():
            instruct = v
            break
    output = ""
    for k in output_keys:
        v = sample.get(k)
        if isinstance(v, str) and v.strip():
            output = v
            break
    return f"{instruct.strip()}\n---\n{output.strip()}"


def _md5(text: str) -> str:
    return hashlib.md5(text.encode("utf-8", errors="ignore")).hexdigest()


def _char_ngrams(text: str, k: int) -> set[str]:
    if len(text) < k:
        return {text}
    return {text[i : i + k] for i in range(len(text) - k + 1)}


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    intersection = len(a & b)
    union = len(a | b)
    return intersection / union if union else 0.0


def dedup_samples(
    samples: list[dict],
    jaccard_threshold: float | None = None,
    ngram_k: int = 5,
    instruct_keys: tuple[str, ...] = ("instruct", "instruction", "input", "prompt", "question"),
    output_keys: tuple[str, ...] = ("output", "response", "answer", "completion"),
) -> tuple[list[dict], dict]:
    """Return (deduped_samples, stats_dict).

    stats_dict has: {input, after_exact, after_jaccard, exact_removed, jaccard_removed}
    """
    stats: dict[str, Any] = {"input": len(samples), "exact_removed": 0, "jaccard_removed": 0}

    # Stage 1: exact hash dedup (O(n))
    seen_hashes: dict[str, int] = {}
    exact_filtered: list[dict] = []
    for sample in samples:
        canonical = _canonical_text(sample, instruct_keys, output_keys)
        if not canonical.strip():  # skip entirely empty samples
            continue
        h = _md5(canonical)
        if h not in seen_hashes:
            seen_hashes[h] = len(exact_filtered)
            exact_filtered.append(sample)
        else:
            stats["exact_removed"] += 1

    stats["after_exact"] = len(exact_filtered)

    if not jaccard_threshold or jaccard_threshold <= 0:
        stats["after_jaccard"] = len(exact_filtered)
        return exact_filtered, stats

    # Stage 2: Jaccard near-duplicate on instruction (O(n^2))
    # Pre-compute n-gram sets once.
    n = len(exact_filtered)
    print(f"[dedup] Stage 2 Jaccard starting: n={n}, threshold={jaccard_threshold}, ngram_k={ngram_k}, max_seconds={JACCARD_MAX_SECONDS}", flush=True)
    t0 = time.time()

    ngram_sets: list[set[str]] = []
    for sample in exact_filtered:
        instruct = ""
        for k in instruct_keys:
            v = sample.get(k)
            if isinstance(v, str) and v.strip():
                instruct = v.strip().lower()
                break
        ngram_sets.append(_char_ngrams(instruct, ngram_k))
    print(f"[dedup] Stage 2 ngram_sets built in {time.time() - t0:.1f}s. Starting pairwise loop...", flush=True)

    keep_mask = [True] * n
    timeout_hit = False
    for i in range(n):
        if not keep_mask[i]:
            continue
        # Progress log + timeout check
        if i % JACCARD_PROGRESS_EVERY == 0 and i > 0:
            elapsed = time.time() - t0
            pct = 100.0 * i / n
            rate = i / elapsed if elapsed > 0 else 0
            eta = (n - i) / rate if rate > 0 else float("inf")
            print(
                f"[dedup] Jaccard progress: i={i}/{n} ({pct:.1f}%), removed={stats['jaccard_removed']}, elapsed={elapsed:.0f}s, ETA={eta:.0f}s",
                flush=True,
            )
            if elapsed > JACCARD_MAX_SECONDS:
                print(f"[dedup] Jaccard TIMEOUT hit at {elapsed:.0f}s (limit {JACCARD_MAX_SECONDS}s). Aborting stage 2 — returning exact-only result + partial jaccard removals.", flush=True)
                timeout_hit = True
                break
        for j in range(i + 1, n):
            if not keep_mask[j]:
                continue
            if _jaccard(ngram_sets[i], ngram_sets[j]) >= jaccard_threshold:
                keep_mask[j] = False
                stats["jaccard_removed"] += 1

    jaccard_filtered = [s for s, keep in zip(exact_filtered, keep_mask) if keep]
    stats["after_jaccard"] = len(jaccard_filtered)
    stats["jaccard_elapsed_sec"] = round(time.time() - t0, 1)
    stats["jaccard_timeout_hit"] = timeout_hit
    return jaccard_filtered, stats


def dedup_from_env(samples: list[dict]) -> tuple[list[dict], dict]:
    """Read env flags and run dedup.

    Returns (samples, stats). Set INSTRUCT_DEDUP=0 to disable.

    Default ON since 2026-08-05. Previously this was opt-in via INSTRUCT_DEDUP=1
    and the flag was never exported anywhere, so production shipped with no dedup
    at all. Only the exact-hash stage runs by default (O(n), stdlib); the pairwise
    Jaccard stage stays opt-in behind INSTRUCT_DEDUP_JACCARD because it is O(n^2).
    Duplicate rows inflate the apparent size of a dataset, waste a slice of a
    fixed time budget re-learning the same rows, and — together with the split
    policy in data/split_policy.py — are the main route by which dev loss stops
    measuring generalisation.
    """
    if os.getenv("INSTRUCT_DEDUP", "1") != "1":
        return samples, {"enabled": False, "input": len(samples)}

    try:
        jaccard_th_raw = os.getenv("INSTRUCT_DEDUP_JACCARD", "")
        jaccard_threshold = float(jaccard_th_raw) if jaccard_th_raw else None
        if jaccard_threshold is not None and jaccard_threshold <= 0:
            jaccard_threshold = None
    except ValueError:
        jaccard_threshold = None

    try:
        ngram_k = int(os.getenv("INSTRUCT_DEDUP_NGRAM", "5"))
    except ValueError:
        ngram_k = 5

    instruct_key = os.getenv("INSTRUCT_DEDUP_FIELD_INSTRUCT", "")
    output_key = os.getenv("INSTRUCT_DEDUP_FIELD_OUTPUT", "")
    default_instruct = ("instruct", "instruction", "input", "prompt", "question")
    default_output = ("output", "response", "answer", "completion")
    instruct_keys: tuple[str, ...] = (instruct_key,) + default_instruct if instruct_key else default_instruct
    output_keys: tuple[str, ...] = (output_key,) + default_output if output_key else default_output

    result, stats = dedup_samples(
        samples,
        jaccard_threshold=jaccard_threshold,
        ngram_k=ngram_k,
        instruct_keys=instruct_keys,
        output_keys=output_keys,
    )
    stats["enabled"] = True
    stats["jaccard_threshold"] = jaccard_threshold
    stats["ngram_k"] = ngram_k
    return result, stats


def dedup_json_file(path: str, output_path: str | None = None) -> dict:
    """CLI helper: dedup a JSON file in place (or to output_path). Returns stats."""
    with open(path, "r") as f:
        samples = json.load(f)
    if not isinstance(samples, list):
        raise ValueError(f"Expected JSON array, got {type(samples).__name__}")
    result, stats = dedup_from_env(samples)
    target = output_path or path
    with open(target, "w") as f:
        json.dump(result, f, ensure_ascii=False)
    return stats


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Dedup JSON dataset file (stdlib + numpy only)")
    parser.add_argument("input", help="Input JSON file path (list of dicts)")
    parser.add_argument("--output", help="Output JSON path (default: overwrite input)", default=None)
    args = parser.parse_args()
    stats = dedup_json_file(args.input, args.output)
    print(json.dumps(stats, indent=2))
