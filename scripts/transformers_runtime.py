"""Runtime patches applied BEFORE HuggingFace imports.

Ported from hyper-text (2026-05-21). Critical defensive fix for Triton
"0 active drivers" crash that bit our 2026-05-07 tournament (5/5 hotkey
HANGUS per memory `validator_workflow_postmortem_2026_05_08.md`).

Usage: import + call at the very top of training scripts, BEFORE any
HuggingFace imports.
    from transformers_runtime import maybe_disable_optional_deepspeed
    maybe_disable_optional_deepspeed()

Env override: FORCE_DISABLE_OPTIONAL_DEEPSPEED=1 forces disable even when
--deepspeed arg present (useful for debugging).
"""
import os
import sys


def maybe_disable_optional_deepspeed() -> bool:
    """Disable optional DeepSpeed imports when the current run is not a DeepSpeed run.

    Transformers 4.51+ imports `deepspeed` eagerly from `modeling_utils` whenever
    the package is installed. On DDP / single-GPU runs this can crash inside
    Triton driver detection ("0 active drivers") before training even starts —
    typically seen in refinement subprocess after main training consumed Triton
    state.

    We only keep DeepSpeed integration enabled when the current process is
    explicitly launched with a DeepSpeed config (--deepspeed arg or
    ACCELERATE_USE_DEEPSPEED=true env var).

    Returns True if disabled, False if kept enabled.
    """

    force_disable = os.getenv("FORCE_DISABLE_OPTIONAL_DEEPSPEED", "0").lower() in {
        "1",
        "true",
        "yes",
    }
    using_deepspeed = (
        "--deepspeed" in sys.argv
        or os.getenv("ACCELERATE_USE_DEEPSPEED", "false").lower() == "true"
    )

    if using_deepspeed and not force_disable:
        return False

    try:
        import transformers.integrations.deepspeed as hf_deepspeed
        hf_deepspeed.is_deepspeed_available = lambda: False
        print(
            "[Runtime] Disabled optional DeepSpeed import for non-DeepSpeed run",
            flush=True,
        )
        return True
    except Exception as exc:
        # Fail-soft: don't break training if transformers not installed yet
        print(
            f"[Runtime] DeepSpeed disable skipped (fail-soft): {type(exc).__name__}: {exc}",
            flush=True,
        )
        return False
