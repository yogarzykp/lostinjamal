"""Combined aggregator: winner_data (full HP) + lrs_reverse_map (LR-only).

Sources:
  1. /tmp/winner_data/_task_*_summary.json — from research_pull_winners.py.
     Has FULL training_args per winner (64 records with all fields).
  2. scripts/lrs_reverse_map.json — from research_mine_lrs.py.
     Has (model_id, task, lr) tuples only (236 records, LR field only).

Output: scripts/empirical_hp_rules.json — keyed by (family, bucket, task)

For LR aggregation: combine both sources (lots more data).
For other fields (epoch, batch, wd, neftune, min_lr_rate): only winner_data.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
from collections import defaultdict, Counter
from pathlib import Path
from typing import Optional


SCRIPT_DIR = Path(__file__).parent

# Imports from research_aggregate.py (re-use family + bucket logic)
import sys
sys.path.insert(0, str(SCRIPT_DIR))
from research_aggregate import (
    detect_family,
    size_bucket,
    normalize_task_type,
    estimate_size_from_config,
    summarize_stats,
)


# Size estimation from model_id name (when no config available)
_SIZE_RE = re.compile(r"(\d+(?:\.\d+)?)[\s_\-]?b\b", re.IGNORECASE)
_SIZE_M_RE = re.compile(r"(\d+(?:\.\d+)?)[\s_\-]?m\b", re.IGNORECASE)
_SIZE_KNOWN = {
    "llama-160m": 0.16, "jackfram/llama-160m": 0.16, "llama-68m": 0.068,
    "opt-125m": 0.125, "opt-350m": 0.35, "opt-1.3b": 1.3, "opt-2.7b": 2.7,
    "opt-6.7b": 6.7, "opt-13b": 13, "opt-30b": 30,
    "phi-1_5": 1.3, "phi-1": 1.3, "phi-2": 2.7, "phi-3-mini": 3.8, "phi-3-small": 7,
    "phi-3-medium": 14, "phi-3.5-mini": 3.8, "phi-3.5-moe": 41.9, "phi-4": 14,
    "tinyllama_v1.1": 1.1, "tinyllama-1.1b": 1.1, "sheared-llama-1.3b": 1.3,
    "sheared-llama-2.7b": 2.7,
    "gpt-neo-125m": 0.125, "gpt-neo-1.3b": 1.3, "gpt-neo-2.7b": 2.7,
    "gpt-neox-20b": 20, "pythia-160m": 0.16, "pythia-410m": 0.41,
    "pythia-1b": 1.0, "pythia-1.4b": 1.4, "pythia-2.8b": 2.8, "pythia-6.9b": 6.9,
    "pythia-12b": 12,
    "bloom-560m": 0.56, "bloom-1b1": 1.1, "bloom-1b7": 1.7, "bloom-3b": 3,
    "bloom-7b1": 7.1, "bloomz-560m": 0.56, "bloomz-1b1": 1.1, "bloomz-1b7": 1.7,
    "bloomz-3b": 3, "bloomz-7b1": 7.1,
    "falcon-rw-1b": 1.3, "falcon-7b": 7, "falcon-40b": 40,
    "starcoder2-3b": 3, "starcoder2-7b": 7, "starcoder2-15b": 15,
    "codellama-7b": 7, "codellama-13b": 13, "codellama-34b": 34, "codellama-70b": 70,
    "smollm-135m": 0.135, "smollm-360m": 0.36, "smollm-1.7b": 1.7,
    "smollm2-135m": 0.135, "smollm2-360m": 0.36, "smollm2-1.7b": 1.7,
    "qwen2.5-0.5b": 0.5, "qwen2.5-1.5b": 1.5, "qwen2.5-3b": 3, "qwen2.5-7b": 7,
    "qwen2.5-14b": 14, "qwen2.5-32b": 32, "qwen2.5-72b": 72,
    "qwen2.5-coder-1.5b": 1.5, "qwen2.5-coder-3b": 3, "qwen2.5-coder-7b": 7,
    "qwen2.5-coder-14b": 14, "qwen2.5-coder-32b": 32,
    "qwen2.5-math-1.5b": 1.5, "qwen2.5-math-7b": 7, "qwen2.5-math-72b": 72,
    "qwen3-0.6b": 0.6, "qwen3-1.7b": 1.7, "qwen3-4b": 4, "qwen3-8b": 8,
    "qwen3-14b": 14, "qwen3-32b": 32,
    "llama-3.2-1b": 1, "llama-3.2-3b": 3, "llama-3.1-8b": 8, "llama-3.1-70b": 70,
    "meta-llama-3-8b": 8, "meta-llama-3.1-8b": 8, "meta-llama-3.1-70b": 70,
    "llama-2-7b": 7, "llama-2-13b": 13,
    "gemma-2b": 2, "gemma-7b": 7, "gemma-2-2b": 2.6, "gemma-2-9b": 9.2,
    "gemma-2-27b": 27, "gemma-3-1b": 1, "gemma-3-4b": 4, "gemma-3-12b": 12,
    "gemma-3-27b": 27,
    "mistral-7b": 7, "mixtral-8x7b": 47, "nous-hermes-2-mistral-7b": 7,
    "typhoon-v1.5-8b": 8,
    "dolly-v2-3b": 3, "dolly-v2-7b": 7,
}


def estimate_size_from_name(model_id: str) -> Optional[float]:
    """Best-effort size estimate from name only (lrs reverse map has no config)."""
    name = model_id.lower()
    if "/" in name:
        name = name.split("/", 1)[1]
    # Known mappings
    for k, v in _SIZE_KNOWN.items():
        if k in name:
            return v
    # Regex Nb
    m = _SIZE_RE.search(name)
    if m:
        return float(m.group(1))
    # Regex Nm
    m2 = _SIZE_M_RE.search(name)
    if m2:
        return float(m2.group(1)) / 1000.0
    return None


def family_from_name(model_id: str) -> str:
    """Family heuristic from name only (no arch field)."""
    name = model_id.lower()
    if "qwen" in name:
        return "qwen"
    if "sheared" in name or "tinyllama" in name:
        return "tinyllama"
    if "smollm" in name:
        return "smollm"
    if "llama" in name or "typhoon" in name:
        return "llama"
    if "phi" in name:
        return "phi"
    if "gemma" in name:
        return "gemma"
    if "mistral" in name or "mixtral" in name:
        return "mistral"
    if "opt-" in name:
        return "opt"
    if "neo" in name or "pythia" in name:
        return "gpt_neo"
    if "bloom" in name:
        return "bloom"
    if "falcon" in name:
        return "falcon"
    if "codellama" in name:
        return "codellama"
    if "starcoder" in name:
        return "starcoder"
    if "dolly" in name:
        return "gpt_neox"
    return "unknown"


def aggregate_combined(winner_dir: Path, lrs_reverse_path: Path) -> dict:
    """Combine both sources into family×size×task cells."""
    by_cell = defaultdict(lambda: defaultdict(list))   # cell → field → values
    cell_models = defaultdict(set)                     # cell → set of model_ids
    source_counts = defaultdict(int)

    # Source 1: winner_data — full HP per record
    for s_path in sorted(winner_dir.glob("_task_*_summary.json")):
        try:
            s = json.loads(s_path.read_text())
        except Exception:
            continue
        task_id = s.get("task_id")
        task_type = normalize_task_type(s.get("task_type"))
        arch = s.get("base_arch")
        model = s.get("model")
        family = detect_family(arch, model)
        size_b = estimate_size_from_config(s) or estimate_size_from_name(model or "")
        bucket = size_bucket(size_b)
        cell = (family, bucket, task_type)
        cell_models[cell].add(model or "?")

        for w in s.get("winners", []):
            args = w.get("training_args")
            if not isinstance(args, dict) or "_error" in args:
                continue
            fields = {
                "learning_rate": args.get("learning_rate"),
                "weight_decay": args.get("weight_decay"),
                "warmup_steps": args.get("warmup_steps"),
                "num_train_epochs": args.get("num_train_epochs"),
                "per_device_train_batch_size": args.get("per_device_train_batch_size"),
                "gradient_accumulation_steps": args.get("gradient_accumulation_steps"),
                "neftune_noise_alpha": args.get("neftune_noise_alpha"),
            }
            lrs_kw = args.get("lr_scheduler_kwargs")
            if isinstance(lrs_kw, dict):
                fields["min_lr_rate"] = lrs_kw.get("min_lr_rate")

            for k, v in fields.items():
                if v is not None and isinstance(v, (int, float)):
                    by_cell[cell][k].append(float(v))
            source_counts[("winner_data", cell)] += 1

    # Source 2: lrs reverse map — LR only, SUPPLEMENTARY ONLY
    # User clarification 2026-05-11: lrs/*.json is BASE WINNER metadata,
    # not all valid. Priority: winner_data >> lrs_reverse.
    # We add lrs entries ONLY to cells that have FEW or NO winner_data records,
    # to supplement coverage. Skip cells already strong from winner_data.
    if lrs_reverse_path.exists():
        # Determine which cells are already strong from winner_data
        winner_strength = {}
        for k, src in source_counts.items():
            if k[0] == "winner_data":
                winner_strength[k[1]] = src

        rmap = json.loads(lrs_reverse_path.read_text())
        skipped_strong = 0
        for m in rmap.get("matches", []):
            mid = m.get("model_id", "")
            task_type = m.get("task_type")
            if task_type == "grpo_python":
                task_type = "grpo"  # collapse grpo_python into grpo
            lr = m.get("lr")
            if not (mid and task_type and lr):
                continue
            family = family_from_name(mid)
            size_b = estimate_size_from_name(mid)
            bucket = size_bucket(size_b)
            cell = (family, bucket, task_type)

            # Skip if cell already has ≥4 winner_data records (HIGH/MED conf already)
            if winner_strength.get(cell, 0) >= 4:
                skipped_strong += 1
                continue

            cell_models[cell].add(mid)
            by_cell[cell]["learning_rate"].append(float(lr))
            source_counts[("lrs_reverse", cell)] += 1
        print(f"  lrs_reverse: skipped {skipped_strong} entries (cell already strong from winner_data)", flush=True)

    # Build output cells
    cells_out = {}
    for cell, fields in by_cell.items():
        family, bucket, task = cell
        key = f"{family}|{bucket}|{task}"
        cell_data = {"_models_seen": sorted(cell_models[cell])}
        for fname, vals in fields.items():
            cell_data[fname] = summarize_stats(vals)
        cell_data["_source_breakdown"] = {
            "winner_data": source_counts[("winner_data", cell)],
            "lrs_reverse": source_counts[("lrs_reverse", cell)],
        }
        cells_out[key] = cell_data

    return cells_out


def confidence_from_n_spread(stats: dict) -> str:
    if not stats or stats.get("n", 0) == 0:
        return "NONE"
    n = stats["n"]
    if stats["min"] > 0:
        spread = stats["max"] / stats["min"]
    else:
        spread = float("inf")
    if n >= 8 and spread < 5.0: return "HIGH"
    if n >= 4 and spread < 10.0: return "MED"
    if n >= 4: return "MED-low"
    if n >= 2 and spread < 3.0: return "LOW-ok"
    return "LOW"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--winner-dir", default="/tmp/winner_data")
    ap.add_argument("--lrs-reverse", default="scripts/lrs_reverse_map.json")
    ap.add_argument("--out", default="scripts/empirical_hp_rules.json")
    args = ap.parse_args()

    winner_dir = Path(args.winner_dir)
    lrs_path = Path(args.lrs_reverse)
    out_path = Path(args.out)

    print(f"=== Aggregating combined data ===")
    print(f"  winner_data: {winner_dir}")
    print(f"  lrs_reverse: {lrs_path}")
    print()

    cells = aggregate_combined(winner_dir, lrs_path)
    print(f"Total cells: {len(cells)}")

    # Compute coverage stats
    fams = Counter(k.split("|")[0] for k in cells)
    buckets = Counter(k.split("|")[1] for k in cells)
    tasks = Counter(k.split("|")[2] for k in cells)
    print(f"Families: {dict(fams)}")
    print(f"Buckets:  {dict(buckets)}")
    print(f"Tasks:    {dict(tasks)}")

    # Confidence distribution
    conf_dist = Counter()
    for cell in cells.values():
        lr_stats = cell.get("learning_rate")
        conf_dist[confidence_from_n_spread(lr_stats)] += 1
    print(f"Confidence: {dict(conf_dist)}")

    # Save
    output = {
        "version": "v2_combined",
        "cells": cells,
        "_meta": {
            "sources": ["winner_data", "lrs_reverse_map"],
            "total_cells": len(cells),
            "by_family": dict(fams),
            "by_bucket": dict(buckets),
            "by_task": dict(tasks),
            "confidence_dist": dict(conf_dist),
        },
    }
    out_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nSaved → {out_path}")

    # Top cells by sample size
    print("\n=== Top 15 cells by n_samples ===")
    ranked = []
    for k, c in cells.items():
        lr = c.get("learning_rate", {})
        n = lr.get("n", 0)
        if n >= 2:
            ranked.append((k, n, lr.get("median"), confidence_from_n_spread(lr)))
    ranked.sort(key=lambda x: -x[1])
    for k, n, m, conf in ranked[:15]:
        m_str = f"{m:.2e}" if isinstance(m, (int, float)) else "?"
        print(f"  {conf:8s} {k:38s} n={n:3d} lr={m_str}")


if __name__ == "__main__":
    main()
