"""
EXP-HYPER-PORT-E 2026-05-20 — minimal weight-stats extraction (CPU-only).

Source slice from model_features.py.
Only includes the parts needed for per-layer LR multiplier computation
(extract_weight_stats + helpers). Skips arch/shape extraction since adaptive_config
already pulls those via AutoConfig.

Iterates safetensors (preferred) / .bin (fallback), aggregates per layer group:
  - weight_rms  = sqrt(sum(w^2) / n_elem)   (per-element scale)
  - weight_norm = sqrt(sum(w^2))            (Frobenius norm — used for LARS)
  - max_abs                                  (saturation indicator)
  - n_tensors, n_elem                        (sanity)

Returns dict shaped like hyper-text's model_features["weights"] sub-dict so
the per-layer LR pipeline can consume it as-is:
  {"by_group": {group_name: {weight_rms, weight_norm, max_abs, n_tensors, n_elem}},
   "iter_error": str | None,
   "source": "safetensors" | "pytorch_bin" | None}

Cost: ~5-15s for 7B, ~30-60s for 70B. CPU only, no GPU/no torch model load.
"""

from __future__ import annotations

import os
import re
from collections import defaultdict
from typing import Any, Optional


# Layer-group classification — covers most modern decoder transformers
# (Llama, Qwen, Mistral, Gemma, Phi, GPT-style). Matched against safetensors
# parameter keys via regex. Grouping lets us aggregate stats per role
# (q/k/v/o for attention, gate/up/down for MLP).
LAYER_GROUP_PATTERNS = {
    # Self-attention projections
    "attn.q_proj":   r"\.q_proj\.weight$",
    "attn.k_proj":   r"\.k_proj\.weight$",
    "attn.v_proj":   r"\.v_proj\.weight$",
    "attn.o_proj":   r"\.o_proj\.weight$",
    "attn.qkv_proj": r"\.qkv_proj\.weight$",  # combined Wqkv (some Phi/Qwen variants)
    "attn.Wqkv":     r"\.Wqkv\.weight$",
    "attn.dense":    r"\.dense\.weight$",      # falcon-rw
    # MLP (Llama-style: gate + up + down)
    "mlp.gate_proj": r"\.gate_proj\.weight$",
    "mlp.up_proj":   r"\.up_proj\.weight$",
    "mlp.down_proj": r"\.down_proj\.weight$",
    "mlp.gate_up_proj": r"\.gate_up_proj\.weight$",  # combined (some)
    # MLP (GPT-style: fc1 + fc2)
    "mlp.fc1":       r"\.fc1\.weight$",
    "mlp.fc2":       r"\.fc2\.weight$",
    # Norms (LayerNorm / RMSNorm)
    "norm.input":              r"\.input_layernorm\.weight$",
    "norm.post_attention":     r"\.post_attention_layernorm\.weight$",
    "norm.final":              r"^model\.norm\.weight$",
    "norm.ln":                 r"\.ln\.weight$",   # generic
    # Embeddings / output head
    "embed_tokens":   r"^model\.embed_tokens\.weight$",
    "lm_head":        r"^lm_head\.weight$",
}


def _classify_layer(key: str) -> Optional[str]:
    for g, p in LAYER_GROUP_PATTERNS.items():
        if re.search(p, key):
            return g
    return None


def _accumulate_tensor(by_group: dict, group: str, tensor) -> None:
    """Update aggregates for a tensor in a layer group. Tensor must be
    a torch.Tensor or compatible with .float() / .sum() / .abs() / .max() /
    .numel() methods."""
    bg = by_group[group]
    t = tensor.float()
    bg["rms_sq_sum"] += float((t ** 2).sum().item())
    bg["n_elem"]     += int(t.numel())
    bg["max_abs"]     = max(bg["max_abs"], float(t.abs().max().item()))
    bg["n_tensors"]  += 1


def extract_weight_stats(model_path: str, max_layers_per_group: int = 0) -> dict:
    """Iterate weight files (.safetensors preferred, .bin fallback), compute
    weight_rms / weight_norm / max_abs per layer group. CPU only.

    Args:
      model_path: directory with config.json + weight files
      max_layers_per_group: 0 = all. >0 = sample first N tensors per group.

    Returns:
      {"by_group": {group_name: {weight_rms, weight_norm, max_abs, n_tensors,
                                  n_elem}}, "iter_error": str | None,
       "source": "safetensors" | "pytorch_bin" | None}
    """
    out: dict = {"by_group": {}, "iter_error": None, "source": None}

    if not os.path.isdir(model_path):
        out["iter_error"] = f"model_path not a dir: {model_path}"
        return out

    safetensors_files = sorted(
        f for f in os.listdir(model_path) if f.endswith(".safetensors")
    )
    bin_files = sorted(
        f for f in os.listdir(model_path) if f.endswith(".bin")
    )

    if not safetensors_files and not bin_files:
        out["iter_error"] = "no weight files (.safetensors / .bin) found"
        return out

    # Per-group aggregates
    by_group = defaultdict(lambda: {
        "rms_sq_sum": 0.0, "n_elem": 0, "max_abs": 0.0, "n_tensors": 0,
    })

    try:
        if safetensors_files:
            from safetensors import safe_open
            out["source"] = "safetensors"
            for sf in safetensors_files:
                full = os.path.join(model_path, sf)
                with safe_open(full, framework="pt") as st:
                    for key in st.keys():
                        group = _classify_layer(key)
                        if group is None:
                            continue
                        if (max_layers_per_group and
                                by_group[group]["n_tensors"] >= max_layers_per_group):
                            continue
                        t = st.get_tensor(key)
                        _accumulate_tensor(by_group, group, t)
        else:
            # .bin fallback (older models like Sheared-LLaMA-1.3B)
            import torch
            out["source"] = "pytorch_bin"
            for bf in bin_files:
                full = os.path.join(model_path, bf)
                state_dict = torch.load(full, map_location="cpu", weights_only=True)
                for key, t in state_dict.items():
                    group = _classify_layer(key)
                    if group is None:
                        continue
                    if (max_layers_per_group and
                            by_group[group]["n_tensors"] >= max_layers_per_group):
                        continue
                    _accumulate_tensor(by_group, group, t)
                del state_dict  # free memory between shards
    except Exception as exc:
        out["iter_error"] = f"{type(exc).__name__}: {exc}"
        return out

    for group, st in by_group.items():
        if st["n_elem"] == 0:
            continue
        out["by_group"][group] = {
            "weight_rms":  (st["rms_sq_sum"] / st["n_elem"]) ** 0.5,
            "weight_norm": st["rms_sq_sum"] ** 0.5,
            "max_abs":     st["max_abs"],
            "n_tensors":   st["n_tensors"],
            "n_elem":      st["n_elem"],
        }

    return out
