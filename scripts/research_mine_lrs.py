"""
Mine scripts/lrs/*.json hash → LR entries by reverse-mapping hash → model_id.

lrs/*.json contains 783 entries of form {h: sha256(model_name), lr: value}.
We don't know which model_name produced each hash. To enrich our family×size×task
table, we need to figure out the model_id for each hash.

Strategy:
  1. Build candidate model_id list from MULTIPLE sources:
     - Gradients API: list all tasks → unique model_ids
     - HF popular models (Qwen, Llama, etc. — known family tree)
     - master-text inventory (.agents/context/models_and_tasks.md if structured)
  2. For each candidate model_id, compute SHA256 hash
  3. Check if hash exists in any lrs/*.json
  4. If match → record (model_id, task_type, lr) tuple
  5. Aggregate into family×size×task cells (using same buckets as research_aggregate)

Output: scripts/lrs_reverse_map.json — extends winner_data with these matched entries
Plus refresh empirical_hp_rules.json with combined data.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
import time
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
LRS_DIR = SCRIPT_DIR / "lrs"
OUT_REVERSE = SCRIPT_DIR / "lrs_reverse_map.json"

# Candidate model IDs — combine all known sources we have access to
# 1. Common HF tournament models (manual list, expand as needed)
HF_TOURNAMENT_MODELS = [
    # Qwen family
    "Qwen/Qwen2.5-0.5B", "Qwen/Qwen2.5-1.5B", "Qwen/Qwen2.5-3B",
    "Qwen/Qwen2.5-7B", "Qwen/Qwen2.5-14B", "Qwen/Qwen2.5-32B", "Qwen/Qwen2.5-72B",
    "Qwen/Qwen2.5-0.5B-Instruct", "Qwen/Qwen2.5-1.5B-Instruct", "Qwen/Qwen2.5-3B-Instruct",
    "Qwen/Qwen2.5-7B-Instruct", "Qwen/Qwen2.5-14B-Instruct", "Qwen/Qwen2.5-32B-Instruct",
    "Qwen/Qwen2.5-72B-Instruct",
    "Qwen/Qwen2.5-Coder-1.5B", "Qwen/Qwen2.5-Coder-3B", "Qwen/Qwen2.5-Coder-7B",
    "Qwen/Qwen2.5-Coder-14B", "Qwen/Qwen2.5-Coder-32B",
    "Qwen/Qwen2.5-Coder-1.5B-Instruct", "Qwen/Qwen2.5-Coder-3B-Instruct",
    "Qwen/Qwen2.5-Coder-7B-Instruct", "Qwen/Qwen2.5-Coder-14B-Instruct",
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    "Qwen/Qwen2.5-Math-1.5B", "Qwen/Qwen2.5-Math-7B", "Qwen/Qwen2.5-Math-72B",
    "Qwen/Qwen3-0.6B", "Qwen/Qwen3-1.7B", "Qwen/Qwen3-4B", "Qwen/Qwen3-8B",
    "Qwen/Qwen3-14B", "Qwen/Qwen3-32B",
    # unsloth variants
    "unsloth/Qwen2.5-0.5B", "unsloth/Qwen2.5-1.5B", "unsloth/Qwen2.5-3B",
    "unsloth/Qwen2.5-7B", "unsloth/Qwen2.5-14B",
    "unsloth/Qwen2.5-0.5B-Instruct", "unsloth/Qwen2.5-1.5B-Instruct",
    "unsloth/Qwen2.5-3B-Instruct", "unsloth/Qwen2.5-7B-Instruct",
    "unsloth/Qwen2.5-Coder-7B-Instruct",
    # Llama family
    "meta-llama/Llama-3.2-1B", "meta-llama/Llama-3.2-3B",
    "meta-llama/Llama-3.2-1B-Instruct", "meta-llama/Llama-3.2-3B-Instruct",
    "meta-llama/Meta-Llama-3.1-8B", "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "meta-llama/Meta-Llama-3.1-70B", "meta-llama/Meta-Llama-3.1-70B-Instruct",
    "meta-llama/Llama-3.1-8B", "meta-llama/Llama-3.1-8B-Instruct",
    "meta-llama/Meta-Llama-3-8B", "meta-llama/Meta-Llama-3-8B-Instruct",
    "meta-llama/Llama-2-7b-hf", "meta-llama/Llama-2-7b-chat-hf",
    "meta-llama/Llama-2-13b-hf", "meta-llama/Llama-2-13b-chat-hf",
    "unsloth/Llama-3.2-1B", "unsloth/Llama-3.2-1B-Instruct",
    "unsloth/Llama-3.2-3B", "unsloth/Llama-3.2-3B-Instruct",
    "unsloth/Meta-Llama-3.1-8B", "unsloth/Meta-Llama-3.1-8B-Instruct",
    "unsloth/Llama-3.1-8B", "unsloth/Llama-3.1-8B-Instruct",
    # TinyLlama / Sheared
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0", "TinyLlama/TinyLlama_v1.1",
    "TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T",
    "unsloth/tinyllama", "unsloth/tinyllama-chat",
    "princeton-nlp/Sheared-LLaMA-1.3B", "princeton-nlp/Sheared-LLaMA-2.7B",
    # SmolLM family
    "HuggingFaceTB/SmolLM-135M", "HuggingFaceTB/SmolLM-360M", "HuggingFaceTB/SmolLM-1.7B",
    "HuggingFaceTB/SmolLM2-135M", "HuggingFaceTB/SmolLM2-360M", "HuggingFaceTB/SmolLM2-1.7B",
    "HuggingFaceTB/SmolLM2-135M-Instruct", "HuggingFaceTB/SmolLM2-360M-Instruct",
    "HuggingFaceTB/SmolLM2-1.7B-Instruct",
    "unsloth/SmolLM-135M", "unsloth/SmolLM-360M", "unsloth/SmolLM-1.7B",
    "unsloth/SmolLM2-135M", "unsloth/SmolLM2-360M", "unsloth/SmolLM2-1.7B",
    "unsloth/SmolLM2-135M-Instruct", "unsloth/SmolLM2-360M-Instruct",
    "unsloth/SmolLM2-1.7B-Instruct",
    # Phi family
    "microsoft/phi-1", "microsoft/phi-1_5", "microsoft/phi-2",
    "microsoft/Phi-3-mini-4k-instruct", "microsoft/Phi-3-mini-128k-instruct",
    "microsoft/Phi-3-small-8k-instruct", "microsoft/Phi-3.5-mini-instruct",
    "microsoft/Phi-3.5-MoE-instruct", "microsoft/Phi-4",
    "unsloth/Phi-3-mini-4k-instruct", "unsloth/Phi-3-medium-4k-instruct",
    "unsloth/Phi-3.5-mini-instruct", "unsloth/phi-4",
    # Gemma family
    "google/gemma-2b", "google/gemma-2b-it", "google/gemma-7b", "google/gemma-7b-it",
    "google/gemma-2-2b", "google/gemma-2-2b-it",
    "google/gemma-2-9b", "google/gemma-2-9b-it",
    "google/gemma-2-27b", "google/gemma-2-27b-it",
    "google/gemma-3-1b-it", "google/gemma-3-4b-it", "google/gemma-3-12b-it",
    "google/gemma-3-27b-it",
    "unsloth/gemma-2b-it", "unsloth/gemma-7b-it",
    "unsloth/gemma-2-2b-it", "unsloth/gemma-2-9b-it", "unsloth/gemma-2-27b-it",
    "unsloth/gemma-3-1b-it", "unsloth/gemma-3-4b-it", "unsloth/gemma-3-12b-it",
    # Mistral family
    "mistralai/Mistral-7B-v0.1", "mistralai/Mistral-7B-v0.3",
    "mistralai/Mistral-7B-Instruct-v0.1", "mistralai/Mistral-7B-Instruct-v0.2",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "mistralai/Mixtral-8x7B-v0.1", "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "NousResearch/Nous-Hermes-2-Mistral-7B-DPO",
    "scb10x/llama-3-typhoon-v1.5-8b-instruct",
    # OPT family
    "facebook/opt-125m", "facebook/opt-350m", "facebook/opt-1.3b",
    "facebook/opt-2.7b", "facebook/opt-6.7b", "facebook/opt-13b", "facebook/opt-30b",
    # GPT-Neo family
    "EleutherAI/gpt-neo-125m", "EleutherAI/gpt-neo-1.3B", "EleutherAI/gpt-neo-2.7B",
    "EleutherAI/gpt-neox-20b", "EleutherAI/pythia-160m", "EleutherAI/pythia-410m",
    "EleutherAI/pythia-1b", "EleutherAI/pythia-1.4b", "EleutherAI/pythia-2.8b",
    "EleutherAI/pythia-6.9b", "EleutherAI/pythia-12b",
    # Bloom family
    "bigscience/bloom-560m", "bigscience/bloom-1b1", "bigscience/bloom-1b7",
    "bigscience/bloom-3b", "bigscience/bloom-7b1",
    "bigscience/bloomz-560m", "bigscience/bloomz-1b1", "bigscience/bloomz-1b7",
    "bigscience/bloomz-3b", "bigscience/bloomz-7b1",
    # Falcon family
    "tiiuae/falcon-rw-1b", "tiiuae/falcon-7b", "tiiuae/falcon-7b-instruct",
    "tiiuae/falcon-40b", "tiiuae/falcon-40b-instruct",
    # CodeLlama / Code-specific
    "codellama/CodeLlama-7b-hf", "codellama/CodeLlama-7b-Instruct-hf",
    "codellama/CodeLlama-13b-hf", "codellama/CodeLlama-13b-Instruct-hf",
    "codellama/CodeLlama-34b-hf", "codellama/CodeLlama-34b-Instruct-hf",
    "codellama/CodeLlama-70b-hf", "codellama/CodeLlama-70b-Instruct-hf",
    # Starcoder
    "bigcode/starcoder", "bigcode/starcoder2-3b", "bigcode/starcoder2-7b",
    "bigcode/starcoder2-15b",
    # Smaller models (Jackfram, etc.)
    "JackFram/llama-160m", "JackFram/llama-68m",
    "heegyu/WizardVicuna-open-llama-3b-v2", "openlm-research/open_llama_3b",
    "Eurdem/Defne_llama3_2x8B", "TitanML/tiny-mixtral",
    "dunzhang/stella_en_1.5B_v5", "oopsung/llama2-7b-n-ox-test-v1",
    "databricks/dolly-v2-3b", "databricks/dolly-v2-7b",
]


def sha256_hash(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def load_lrs() -> dict[str, dict[str, float]]:
    """Load all lrs/*.json → {task_type: {hash: lr}}."""
    out = {}
    for task_file, task_name in [
        ("instruct.json", "instruct"),
        ("dpo.json", "dpo"),
        ("grpo.json", "grpo"),
        ("grpo_python.json", "grpo_python"),
    ]:
        path = LRS_DIR / task_file
        if not path.exists():
            continue
        entries = json.loads(path.read_text())
        out[task_name] = {e["h"]: e["lr"] for e in entries if "h" in e and "lr" in e}
    return out


def fetch_more_model_ids_from_api(limit_total: int = 300) -> set[str]:
    """Query Gradients API for additional model_ids."""
    found = set()
    for offset in [0, 50, 100, 150, 200, 250]:
        url = f"https://api.gradients.io/auditing/tasks?limit=50&offset={offset}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "research-mine/1.0"})
            data = json.loads(urllib.request.urlopen(req, timeout=15).read())
            if not isinstance(data, list) or not data:
                break
            for t in data:
                mid = t.get("model_id")
                if mid and not mid.startswith("gradients-io-"):  # skip augmented/merged
                    found.add(mid)
            time.sleep(0.5)
        except Exception:
            break
        if len(found) >= limit_total:
            break
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-api", action="store_true", help="Skip Gradients API discovery")
    args = ap.parse_args()

    print("=" * 70)
    print("MINE LRS — reverse-map hash → model_id")
    print("=" * 70)

    # Load lrs/*.json
    lrs = load_lrs()
    total_entries = sum(len(v) for v in lrs.values())
    print(f"\nLoaded {total_entries} hash entries across {len(lrs)} task types:")
    for tn, d in lrs.items():
        print(f"  {tn}: {len(d)} entries")

    # Candidate model_ids
    candidates = set(HF_TOURNAMENT_MODELS)
    print(f"\nHF tournament catalog: {len(candidates)} model_ids")

    if not args.no_api:
        api_models = fetch_more_model_ids_from_api()
        new_from_api = api_models - candidates
        candidates |= api_models
        print(f"Gradients API: +{len(new_from_api)} new, total {len(candidates)}")

    # Match
    matches = []
    for mid in sorted(candidates):
        h = sha256_hash(mid)
        for task_name, hash_map in lrs.items():
            if h in hash_map:
                matches.append({
                    "model_id": mid,
                    "task_type": task_name,
                    "lr": hash_map[h],
                    "_source": "lrs_reverse",
                })

    # Summary
    print(f"\n=== Matches: {len(matches)} ({len(matches)/total_entries*100:.1f}% coverage) ===")
    by_task = Counter(m["task_type"] for m in matches)
    print(f"By task: {dict(by_task)}")
    by_family = Counter()
    for m in matches:
        mid = m["model_id"].lower()
        if "qwen" in mid: by_family["qwen"] += 1
        elif "llama" in mid and ("sheared" in mid or "tinyllama" in mid): by_family["tinyllama"] += 1
        elif "llama" in mid: by_family["llama"] += 1
        elif "smollm" in mid: by_family["smollm"] += 1
        elif "phi" in mid: by_family["phi"] += 1
        elif "gemma" in mid: by_family["gemma"] += 1
        elif "mistral" in mid: by_family["mistral"] += 1
        elif "opt" in mid: by_family["opt"] += 1
        elif "neo" in mid or "pythia" in mid: by_family["gpt_neo"] += 1
        elif "bloom" in mid: by_family["bloom"] += 1
        elif "falcon" in mid: by_family["falcon"] += 1
        elif "codellama" in mid: by_family["codellama"] += 1
        elif "starcoder" in mid: by_family["starcoder"] += 1
        else: by_family["other"] += 1
    print(f"By family: {dict(by_family)}")

    # Save
    OUT_REVERSE.write_text(json.dumps({
        "_meta": {
            "lrs_total": total_entries,
            "candidates_tried": len(candidates),
            "matched": len(matches),
            "coverage_pct": round(len(matches) / total_entries * 100, 1),
            "by_task": dict(by_task),
            "by_family": dict(by_family),
        },
        "matches": matches,
    }, indent=2))
    print(f"\nSaved → {OUT_REVERSE}")
    print(f"Unmatched lrs entries: {total_entries - len(matches)} ({100 - len(matches)/total_entries*100:.1f}%)")


if __name__ == "__main__":
    main()
