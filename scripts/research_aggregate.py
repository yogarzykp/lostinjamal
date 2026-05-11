"""Phase B — Aggregate winner training_args into empirical HP rules.

Reads /tmp/winner_data/*.json (output of research_pull_winners.py) and
derives:
  1. FAMILY_LR_TABLE: (arch_family, size_bucket, task_type) → {median, p25, p75, n}
  2. TASK_CLASS_MULTIPLIERS: detect translation/reasoning/code/skill bias
  3. DATASET_SIZE_RULES: small/medium/large → epoch/batch correlation
  4. AUGMENTATION_TOLERANCE: (placeholder — needs BASELINE_STATS data)

NO hardcoded per-model entries. All rules derived from EMPIRICAL data.
Output: scripts/empirical_hp_rules.json (consumed by general_hp_resolver.py).
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Optional


# Architecture → family map (mirror dynamics_utils.detect_arch_family + extend)
ARCH_TO_FAMILY = {
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


# Special-case: Sheared-LLaMA, TinyLlama, SmolLM → separate sub-families
def detect_family(arch: Optional[str], model_id: Optional[str] = None) -> str:
    """Derive family from arch + name hint."""
    if not arch:
        arch = ""
    a = arch.strip().lower()
    family = ARCH_TO_FAMILY.get(a)
    if not family:
        # Heuristic from name (when arch lookup misses)
        nm = (model_id or "").lower()
        if "smollm" in nm:
            return "smollm"
        if "qwen" in nm:
            return "qwen"
        if "llama" in nm:
            return "llama"
        return "unknown"
    # Refine: TinyLlama/SmolLM via name hint
    nm = (model_id or "").lower()
    if family == "llama" and ("tinyllama" in nm or "sheared" in nm):
        return "tinyllama"
    if family == "llama" and "smollm" in nm:
        return "smollm"
    return family


def size_bucket(param_count_billions: Optional[float]) -> str:
    """Convert param count to bucket. Buckets mirror existing config."""
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


def normalize_task_type(t: Optional[str]) -> str:
    if not t:
        return "unknown"
    s = t.lower().replace("task", "").replace("text", "").strip("_")
    if s == "instruct": return "instruct"
    if s == "dpo": return "dpo"
    if s == "grpo": return "grpo"
    return s or "unknown"


def estimate_size_from_config(cfg: dict) -> Optional[float]:
    """Rough param count estimate from config fields. Returns billions."""
    h = cfg.get("hidden_size") or cfg.get("base_hidden_size")
    layers = cfg.get("num_hidden_layers") or cfg.get("base_num_layers")
    vocab = cfg.get("vocab_size") or cfg.get("base_vocab_size")
    inter = cfg.get("intermediate_size") or cfg.get("base_intermediate_size") or (h * 4 if h else None)
    if not all([h, layers, vocab, inter]):
        return None
    # Decoder transformer rough: embed (vocab*h) + per_layer (4*h^2 attn + 3*h*inter mlp) * layers + lm_head (vocab*h)
    embed = 2 * vocab * h  # embed + lm_head (often tied, but conservative)
    per_layer = 4 * h * h + 3 * h * inter
    total = embed + per_layer * layers
    return total / 1e9


def summarize_stats(values: list) -> dict:
    """Compute n/min/median/max/p25/p75 for a list of numbers."""
    if not values:
        return {"n": 0}
    vs = sorted(values)
    n = len(vs)
    median = vs[n // 2] if n % 2 == 1 else (vs[n // 2 - 1] + vs[n // 2]) / 2
    p25 = vs[int(n * 0.25)]
    p75 = vs[min(n - 1, int(n * 0.75))]
    return {
        "n": n,
        "min": vs[0],
        "p25": p25,
        "median": median,
        "p75": p75,
        "max": vs[-1],
    }


def aggregate(in_dir: Path) -> dict:
    """Read all task summaries, group by (family, size_bucket, task_type),
    compute HP distribution.
    """
    summaries = sorted(in_dir.glob("_task_*_summary.json"))
    print(f"[aggregate] Found {len(summaries)} task summaries", flush=True)

    by_cell = defaultdict(lambda: defaultdict(list))   # cell → field → values
    task_examples = defaultdict(list)                  # cell → [task_id]
    per_winner_records = []                            # flat list for inspection

    for s_path in summaries:
        try:
            s = json.loads(s_path.read_text())
        except Exception as exc:
            print(f"[aggregate] {s_path.name} parse fail: {exc}", flush=True)
            continue

        task_id = s.get("task_id")
        task_type = normalize_task_type(s.get("task_type"))
        arch = s.get("base_arch")
        model = s.get("model")
        family = detect_family(arch, model)
        size_b = estimate_size_from_config(s)
        bucket = size_bucket(size_b)
        cell = (family, bucket, task_type)

        for w in s.get("winners", []):
            args = w.get("training_args")
            if not isinstance(args, dict):
                continue
            if "_error" in args:
                continue
            # Extract HP fields of interest
            fields = {
                "learning_rate": args.get("learning_rate"),
                "weight_decay": args.get("weight_decay"),
                "warmup_steps": args.get("warmup_steps"),
                "num_train_epochs": args.get("num_train_epochs"),
                "per_device_train_batch_size": args.get("per_device_train_batch_size"),
                "gradient_accumulation_steps": args.get("gradient_accumulation_steps"),
                "neftune_noise_alpha": args.get("neftune_noise_alpha"),
                "test_loss": w.get("test_loss"),
            }
            # min_lr_rate (nested in lr_scheduler_kwargs)
            lrs_kw = args.get("lr_scheduler_kwargs")
            if isinstance(lrs_kw, dict):
                fields["min_lr_rate"] = lrs_kw.get("min_lr_rate")
            elif isinstance(lrs_kw, str):
                try:
                    fields["min_lr_rate"] = json.loads(lrs_kw).get("min_lr_rate")
                except Exception:
                    pass

            for k, v in fields.items():
                if v is not None and isinstance(v, (int, float)):
                    by_cell[cell][k].append(float(v))

            task_examples[cell].append(task_id[:8])
            per_winner_records.append({
                "task_id": task_id,
                "family": family,
                "bucket": bucket,
                "task_type": task_type,
                "model": model,
                "size_b_est": size_b,
                "hotkey": w.get("hotkey"),
                "rank": w.get("rank"),
                "test_loss": w.get("test_loss"),
                **fields,
            })

    # Compute distributions per cell
    cells = {}
    for (family, bucket, task_type), field_values in by_cell.items():
        key = f"{family}|{bucket}|{task_type}"
        cell = {"_tasks_sample": list(set(task_examples[(family, bucket, task_type)]))[:5]}
        for fname, vals in field_values.items():
            cell[fname] = summarize_stats(vals)
        cells[key] = cell

    return {
        "version": "v1-empirical-2026-05-09",
        "cells": cells,
        "_meta": {
            "total_tasks": len(summaries),
            "total_winner_records": len(per_winner_records),
            "families_seen": sorted(set(f for (f, _, _) in by_cell.keys())),
            "buckets_seen": sorted(set(b for (_, b, _) in by_cell.keys())),
            "task_types_seen": sorted(set(t for (_, _, t) in by_cell.keys())),
        },
        "_raw_records": per_winner_records,  # for inspection / debugging
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-dir", default="/tmp/winner_data")
    ap.add_argument("--out", default="scripts/empirical_hp_rules.json")
    ap.add_argument("--keep-raw", action="store_true",
                    help="Keep _raw_records in output (useful for debugging)")
    args = ap.parse_args()

    in_dir = Path(args.in_dir)
    if not in_dir.exists():
        sys.exit(f"Input dir not found: {in_dir}")

    result = aggregate(in_dir)
    if not args.keep_raw:
        result.pop("_raw_records", None)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, default=str))

    meta = result["_meta"]
    print(f"\n[aggregate] DONE", flush=True)
    print(f"  output: {out_path}", flush=True)
    print(f"  tasks: {meta['total_tasks']}", flush=True)
    print(f"  winner records: {meta['total_winner_records']}", flush=True)
    print(f"  cells filled: {len(result['cells'])}", flush=True)
    print(f"  families: {meta['families_seen']}", flush=True)
    print(f"  buckets: {meta['buckets_seen']}", flush=True)
    print(f"  task_types: {meta['task_types_seen']}", flush=True)

    # Quick sample print
    print(f"\n=== Sample cells ===", flush=True)
    for i, (key, cell) in enumerate(list(result["cells"].items())[:10]):
        lr = cell.get("learning_rate", {})
        print(f"  {key:40s} n={lr.get('n','?')} lr_median={lr.get('median',0):.2e}" if lr else f"  {key}", flush=True)


if __name__ == "__main__":
    main()
