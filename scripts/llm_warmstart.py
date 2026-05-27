"""LLM Warmstart — Tier-2 LR prior for lookup-miss cases.

This module queries the embedded Qwen2.5-14B-AWQ vLLM sidecar to suggest a single
learning rate when the empirical lookup (winner/scripts/lrs/*.json) returns None
for the given model. Purely additive to the existing flow:

  TIER 1: get_xxx_lr()           -> exact-match empirical prior (strongest)
  TIER 2: try_llm_warmstart()    -> LLM reasoning from model/task/size (THIS MODULE)
  TIER 3: config default         -> tier-based generic (weakest, current fallback)

The function returns Optional[float]:
  - float  -> valid LR suggestion to use
  - None   -> skip this tier, caller should fall back to tier default

All failures (network, parse, validation) gracefully return None. Zero risk of
regression: if any step fails, caller keeps its existing `run_config["learning_rate"]`.

Environment variables:
  LLM_WARMSTART_ENABLED           - "0" or "false" to disable (default: enabled)
  LLM_WARMSTART_TIMEOUT_SECONDS   - request timeout (default: 60)
  LLM_WARMSTART_LR_MIN            - absolute safety lower bound (default: 1e-7)
  LLM_WARMSTART_LR_MAX            - absolute safety upper bound (default: 1e-2)

Reuses decision engine endpoint env:
  TRAINING_LLM_DECIDER_BASE_URL
  TRAINING_LLM_DECIDER_MODEL
  TRAINING_LLM_DECIDER_API_KEY
"""

from __future__ import annotations

import json
import math
import os
import re
from typing import Any, Dict, Optional

import requests


# --------------------------------------------------------------------------- #
# Config helpers
# --------------------------------------------------------------------------- #


def _parse_bool(value: Optional[str], default: bool = True) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_float(value: Any, default: float) -> float:
    try:
        return float(value) if value is not None else default
    except (TypeError, ValueError):
        return default


def _parse_int(value: Any, default: int) -> int:
    try:
        return int(value) if value is not None else default
    except (TypeError, ValueError):
        return default


def _normalize_endpoint(base_url: str) -> str:
    base = base_url.rstrip("/")
    if base.endswith("/chat/completions"):
        return base
    if base.endswith("/v1"):
        return base + "/chat/completions"
    return base + "/v1/chat/completions"


# --------------------------------------------------------------------------- #
# Response parsing
# --------------------------------------------------------------------------- #


def _extract_message_content(payload: Dict[str, Any]) -> str:
    try:
        choices = payload.get("choices") or []
        if not choices:
            return ""
        message = choices[0].get("message") or {}
        return str(message.get("content") or "")
    except Exception:
        return ""


def _extract_lr_from_text(text: str) -> Optional[float]:
    """Extract LR float from LLM response. Tries JSON first, falls back to regex."""
    if not text:
        return None

    # Strip markdown code fences
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)

    # Try full JSON parse
    try:
        obj = json.loads(stripped)
        if isinstance(obj, dict):
            lr = obj.get("lr")
            if lr is None:
                lr = obj.get("learning_rate")
            if lr is not None:
                return float(lr)
    except (json.JSONDecodeError, ValueError, TypeError):
        pass

    # Fallback: regex for "lr": <number>
    match = re.search(
        r'"(?:lr|learning_rate)"\s*:\s*([0-9]+\.?[0-9]*(?:[eE][+-]?[0-9]+)?)',
        stripped,
    )
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            pass

    # Last resort: any scientific notation number in response
    match = re.search(r"([0-9]+\.?[0-9]*[eE][+-]?[0-9]+)", stripped)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            pass

    return None


def _validate_lr(lr: Optional[float], lr_min: float, lr_max: float) -> Optional[float]:
    """Reject invalid LR values. Returns None if out of safe range."""
    if lr is None:
        return None
    try:
        value = float(lr)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(value):
        return None
    if value <= 0:
        return None
    if value < lr_min or value > lr_max:
        return None
    return value


# --------------------------------------------------------------------------- #
# Prompt construction
# --------------------------------------------------------------------------- #


def _build_prompt(
    model_name: str,
    task_type: str,
    param_nums: int,
    dataset_size: Optional[int],
    hours_to_complete: Optional[float],
) -> Dict[str, str]:
    """Build (system, user) prompt pair for warmstart LR suggestion."""

    param_b = param_nums / 1e9 if param_nums else None
    size_hint = f"{param_b:.2f}B params" if param_b else "unknown size"

    dataset_hint = (
        f"{dataset_size} samples" if isinstance(dataset_size, int) and dataset_size > 0
        else "unknown size"
    )

    time_hint = (
        f"{hours_to_complete} hours" if hours_to_complete
        else "unknown budget"
    )

    # Task-type aware guidance
    task_guidance = {
        "InstructTextTask": (
            "This is a supervised fine-tuning (SFT) task. Typical LR range for SFT: "
            "1e-5 to 2e-4. Larger models use lower LRs. Small datasets can tolerate "
            "slightly higher LR for faster convergence."
        ),
        "ChatTask": (
            "This is a supervised fine-tuning (SFT) task with chat formatting. "
            "Typical LR range: 1e-5 to 2e-4. Similar to InstructTextTask."
        ),
        "DpoTask": (
            "This is a DPO (Direct Preference Optimization) task. DPO uses much "
            "smaller LRs than SFT, typically 5e-7 to 5e-6. 7B+ models often 1e-6 to 3e-6."
        ),
        "GrpoTask": (
            "This is a GRPO (Group Relative Policy Optimization) task for RL-style "
            "fine-tuning. LR typically 3e-6 to 3e-5, smaller than SFT. Larger models "
            "benefit from LoRA with slightly higher effective LR."
        ),
    }
    guidance = task_guidance.get(
        task_type,
        "Use general ML fine-tuning knowledge to pick a reasonable LR.",
    )

    system_prompt = (
        "You are an ML hyperparameter expert. Given model + task + dataset details, "
        "suggest a single learning rate (LR). "
        "Return strict JSON only: {\"lr\": <float>, \"reason\": \"<under 15 words>\"}. "
        "LR must be positive, typically between 1e-7 and 5e-3. "
        "Consider: model family, model size (larger -> lower LR), task type, dataset size."
    )

    user_prompt = (
        f"Task:\n"
        f"- Model: {model_name} ({size_hint})\n"
        f"- Task type: {task_type}\n"
        f"- Dataset size: {dataset_hint}\n"
        f"- Time budget: {time_hint}\n"
        f"\n"
        f"Guidance: {guidance}\n"
        f"\n"
        f"Return JSON only."
    )

    return {"system": system_prompt, "user": user_prompt}


# --------------------------------------------------------------------------- #
# Main API
# --------------------------------------------------------------------------- #


def try_llm_warmstart(
    *,
    model_name: str,
    task_type: str,
    param_nums: int,
    dataset_size: Optional[int] = None,
    hours_to_complete: Optional[float] = None,
    reward_functions: Optional[list] = None,
) -> Optional[float]:
    """Query LLM for a warmstart learning rate suggestion.

    Returns None on any failure (disabled, endpoint missing, network error,
    parse failure, out-of-range LR). Caller falls back to tier default.

    For GRPO, the caller should run ``reward_classifier.suggest_params()``
    first (Tier 1.5) before this function — the classifier sets LR + β
    together from the reward-function fingerprint, which is more reliable
    than LLM for known mixes. This function is the LLM fallback when the
    classifier can't handle the mix (unknown reward function).

    Parameters
    ----------
    model_name : str
        HuggingFace model ID (e.g. "Qwen/Qwen2.5-7B-Instruct").
    task_type : str
        "InstructTextTask" | "DpoTask" | "GrpoTask" | "ChatTask".
    param_nums : int
        Model parameter count (used for size-aware reasoning).
    dataset_size : int, optional
        Number of training samples if available.
    hours_to_complete : float, optional
        Task time budget in hours.
    reward_functions : list, optional
        Accepted for signature compatibility with the classifier path;
        not used by the LLM prompt itself.

    Returns
    -------
    Optional[float]
        Valid LR in safe range, or None to skip.
    """
    # Feature flag gate
    if not _parse_bool(os.getenv("LLM_WARMSTART_ENABLED"), default=True):
        print("[warmstart] disabled via LLM_WARMSTART_ENABLED", flush=True)
        return None

    # Reuse decision engine endpoint config
    base_url = (os.getenv("TRAINING_LLM_DECIDER_BASE_URL") or "").strip()
    model = (os.getenv("TRAINING_LLM_DECIDER_MODEL") or "").strip()
    if not base_url or not model:
        print(
            "[warmstart] skipped: TRAINING_LLM_DECIDER_BASE_URL or "
            "TRAINING_LLM_DECIDER_MODEL not set",
            flush=True,
        )
        return None

    endpoint = _normalize_endpoint(base_url)
    api_key = (os.getenv("TRAINING_LLM_DECIDER_API_KEY") or "").strip()
    timeout = _parse_int(os.getenv("LLM_WARMSTART_TIMEOUT_SECONDS"), 60)
    lr_min = _parse_float(os.getenv("LLM_WARMSTART_LR_MIN"), 1e-7)
    lr_max = _parse_float(os.getenv("LLM_WARMSTART_LR_MAX"), 1e-2)

    # Build prompt
    prompts = _build_prompt(
        model_name=model_name,
        task_type=task_type,
        param_nums=param_nums,
        dataset_size=dataset_size,
        hours_to_complete=hours_to_complete,
    )

    # Build request
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "model": model,
        "temperature": 0.0,
        "max_tokens": 120,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": prompts["system"]},
            {"role": "user", "content": prompts["user"]},
        ],
    }

    # Execute
    print(
        f"[warmstart] querying LLM for {model_name} ({task_type}, "
        f"{param_nums/1e9:.2f}B, {dataset_size} samples)",
        flush=True,
    )
    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()
        body = response.json()
    except requests.exceptions.RequestException as exc:
        print(f"[warmstart] request failed: {type(exc).__name__}: {exc}", flush=True)
        return None
    except (ValueError, KeyError) as exc:
        print(f"[warmstart] response decode failed: {exc}", flush=True)
        return None

    # Parse
    raw_text = _extract_message_content(body)
    if not raw_text:
        print("[warmstart] empty response content", flush=True)
        return None

    raw_lr = _extract_lr_from_text(raw_text)
    validated = _validate_lr(raw_lr, lr_min=lr_min, lr_max=lr_max)

    if validated is None:
        print(
            f"[warmstart] rejected LR: raw={raw_lr} "
            f"(bounds=[{lr_min:.1e}, {lr_max:.1e}]) "
            f"response={raw_text[:200]!r}",
            flush=True,
        )
        return None

    print(
        f"[warmstart] accepted LR={validated:.2e} "
        f"(raw response: {raw_text[:150]!r})",
        flush=True,
    )
    return validated
