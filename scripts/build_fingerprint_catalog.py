"""Build model fingerprint catalog + canonical weight_rms reference.

Purpose: post G.O.D feature/model-prep-container merge (2026-05-13), miner
receives anonymized model_id (gradients-io/augmented-<sha16>). To recover
the original base model and look up known-good HP, we match against this
catalog using config.json fingerprint (hidden_size, num_hidden_layers,
vocab_size, intermediate_size — all preserved by validator's scrub).

The canonical_weight_rms.json provides per-layer-group weight RMS reference
so we can detect post-augmentation deviations (4 augmentation types per
G.O.D constants AUGMENTATION_TYPE_WEIGHTS).

Run (on a machine with HF access + ~3GB free for cache):
    python3 scripts/build_fingerprint_catalog.py [model_id ...]

Defaults to Qwen/Qwen2.5-0.5B (1-model demo). Friend has full catalog;
this script lets us extend incrementally as new tournament models appear.

Outputs (idempotent — merges with existing entries):
    scripts/model_fingerprint_catalog.json
    scripts/canonical_weight_rms.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

import torch
from transformers import AutoConfig, AutoModelForCausalLM


_LAYER_GROUP_REGEX = re.compile(
    r"\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj)\.weight$"
)


def _arch_to_family(arch: str) -> str:
    """Mirror scripts/dynamics_utils.py:detect_arch_family family naming."""
    a = arch.lower()
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
    if "smollm" in a or "mistral" in a:
        return "smollm" if "smol" in a else "mistral"
    return "unknown"


def fingerprint_key(cfg) -> str:
    """Compose fingerprint key from architecture-defining fields preserved by scrub."""
    return ",".join(
        str(getattr(cfg, k, "")) for k in (
            "hidden_size", "num_hidden_layers", "vocab_size", "intermediate_size",
        )
    )


def compute_canonical_rms(model_id: str) -> dict[str, float]:
    """Compute mean weight RMS per layer-group (q_proj/k_proj/.../down_proj).
    Excludes embed/norm/lm_head (these are PRESERVED by augmentation per G.O.D
    augmentation.py:select_target_layers — so they make poor signal).
    """
    print(f"  Loading {model_id} (fp16, cpu) ...", flush=True)
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16)

    groups: dict[str, list[float]] = defaultdict(list)
    for name, p in model.named_parameters():
        if "norm" in name.lower() or "embed" in name.lower() or "lm_head" in name:
            continue
        m = _LAYER_GROUP_REGEX.search(name)
        if m:
            rms = p.detach().float().pow(2).mean().sqrt().item()
            groups[m.group(1)].append(rms)

    canonical = {g: float(sum(rms_list) / len(rms_list)) for g, rms_list in groups.items()}
    del model
    return canonical


def build_for(model_id: str) -> dict:
    cfg = AutoConfig.from_pretrained(model_id)
    arch = (cfg.architectures or ["Unknown"])[0]
    family = _arch_to_family(arch)
    fp_key = fingerprint_key(cfg)
    canonical = compute_canonical_rms(model_id)
    return {
        "model_id": model_id,
        "fp_key": fp_key,
        "family": family,
        "arch": arch,
        "fingerprint_dict": {
            "hidden_size": getattr(cfg, "hidden_size", None),
            "num_hidden_layers": getattr(cfg, "num_hidden_layers", None),
            "vocab_size": getattr(cfg, "vocab_size", None),
            "intermediate_size": getattr(cfg, "intermediate_size", None),
            "num_attention_heads": getattr(cfg, "num_attention_heads", None),
            "num_key_value_heads": getattr(cfg, "num_key_value_heads", None),
        },
        "canonical_rms": canonical,
    }


def merge_save(out_dir: Path, entry: dict) -> None:
    catalog_path = out_dir / "model_fingerprint_catalog.json"
    canonical_path = out_dir / "canonical_weight_rms.json"

    catalog = {}
    if catalog_path.exists():
        catalog = json.load(open(catalog_path))
    catalog[entry["fp_key"]] = {
        "base_model": entry["model_id"],
        "family": entry["family"],
        "arch": entry["arch"],
        "fingerprint_dict": entry["fingerprint_dict"],
    }
    with open(catalog_path, "w") as f:
        json.dump(catalog, f, indent=2)
    print(f"  Wrote {len(catalog)} entries to {catalog_path}", flush=True)

    canonical = {}
    if canonical_path.exists():
        canonical = json.load(open(canonical_path))
    canonical[entry["model_id"]] = entry["canonical_rms"]
    with open(canonical_path, "w") as f:
        json.dump(canonical, f, indent=2)
    print(f"  Wrote {len(canonical)} entries to {canonical_path}", flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("models", nargs="*", default=["Qwen/Qwen2.5-0.5B"],
                    help="Model IDs to fingerprint (default: Qwen/Qwen2.5-0.5B)")
    args = ap.parse_args()

    out_dir = Path(__file__).parent
    for model_id in args.models:
        print(f"\n=== Building fingerprint for: {model_id} ===", flush=True)
        try:
            entry = build_for(model_id)
            print(f"  fingerprint key: {entry['fp_key']}", flush=True)
            print(f"  family={entry['family']} arch={entry['arch']}", flush=True)
            print(f"  canonical_rms layer groups: {list(entry['canonical_rms'].keys())}", flush=True)
            merge_save(out_dir, entry)
        except Exception as exc:
            print(f"  FAILED: {exc}", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()
