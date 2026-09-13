"""Load a config.json written by transformers 5.x under our pinned 4.51.3 without
losing its positional encoding.

transformers 5.x writes rope settings as one dict —
`rope_parameters: {rope_theta, rope_type, ...scaling fields}` — with no top-level
`rope_theta` or `rope_scaling`, and `dtype` where 4.x wrote `torch_dtype`. Our 4.51.3
knows none of that: `rope_parameters` survives as an unknown attribute and the model is
built from the class defaults, rope_theta 10000 and no scaling.

Measured 2026-09-13 on real files (tests/fixtures/rope/): SmolLM2-360M saved by 5.12.1
loads as theta 10000 instead of 100000; Hermes-3-Llama-3.1-8B re-saved by 5.12.1 loads
as theta 10000 instead of 500000 and loses its llama3 scaling. Where it bites: every
augmented mirror the tournament serves (the base re-saved by the validator's own stack,
~50% of text tasks) and every merged or continuous-SFT base. The retained boss, on our
exact pin, lost both augmented instruct tasks of tourn_2ba0f79237bffcf7 and won both
un-augmented ones.

And it is worse than consistently wrong. 4.51.3's save_pretrained carries the unknown
`rope_parameters` attribute through untouched, and the validator's 5.12.1 honours it over
the top-level value (measured): we TRAINED at 10000 and were SCORED at the true theta.
The weights adapted to one encoding and were judged under another.

The fix is a load-side override only. The legacy keys are handed to `from_pretrained` as
kwargs — the documented way to override config values, which reaches
AutoModelForCausalLM, passes harmlessly through liger's AutoLigerKernelForCausalLM (it
forwards unknown kwargs), and is never given to PeftModel.from_pretrained (whose `config`
means a PeftConfig). Nothing is needed on the save side: 5.12.1 reads a 4.x-shaped
config correctly, also measured, and a shimmed save carries both shapes in agreement.

Wrapper architectures keep the decoder's fields one level down in `text_config`; none
of those load on 4.51.3 at all (the preflight diverts them), so only the top level is
mapped here and a `text_config` is left as it is.
"""

from __future__ import annotations

import json
import os
from typing import Any

_LOG_PREFIX = "[config-shim]"


def legacy_rope_kwargs(raw: Any) -> dict:
    """Legacy (4.x) config kwargs recovered from a 5.x-shaped config dict.

    Returns {} when there is nothing to recover: a 4.x-shaped file, a top-level key
    already present (a caller or a 4.x re-save already decided it), or garbage.
    """
    if not isinstance(raw, dict):
        return {}
    out: dict = {}
    rp = raw.get("rope_parameters")
    if isinstance(rp, dict):
        if raw.get("rope_theta") is None and isinstance(rp.get("rope_theta"), (int, float)):
            out["rope_theta"] = rp["rope_theta"]
        if raw.get("rope_scaling") is None:
            scaling = {k: v for k, v in rp.items() if k != "rope_theta"}
            if scaling.get("rope_type", "default") != "default":
                out["rope_scaling"] = scaling
    # `dtype` (5.x) vs `torch_dtype` (4.x) is deliberately NOT mapped: every load site in
    # this repo passes torch_dtype explicitly, so the misread is inert there, and handing
    # it back as a kwarg would collide with that explicit value.
    return out


def load_kwargs_for(model_path: str, log=print) -> dict:
    """`from_pretrained(model_path, **load_kwargs_for(model_path))` loads it right.

    Reads config.json directly — the shim must not depend on the AutoConfig that
    misreads the file. Fails open to {}: a directory without a readable config is
    someone else's problem to report, not this helper's.
    """
    path = os.path.join(model_path, "config.json") if os.path.isdir(model_path) else None
    if not path or not os.path.isfile(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
    except Exception as exc:
        log(f"{_LOG_PREFIX} could not read {path} ({type(exc).__name__}); loading as-is")
        return {}
    kw = legacy_rope_kwargs(raw)
    if kw:
        shown = {k: (v if k != "rope_scaling" else v.get("rope_type")) for k, v in kw.items()}
        log(f"{_LOG_PREFIX} config written by transformers "
            f"{raw.get('transformers_version', '?')} — restoring {shown} from rope_parameters "
            f"(4.51.3 would have used rope_theta=10000, no scaling)")
    return kw
