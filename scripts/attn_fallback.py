"""Survive a missing flash-attention kernel instead of losing the submission.

We pick ``flash_attention_2`` from the model architecture, but whether that
kernel can actually load is a property of the *container*, not the model: a
missing wheel, a torch/CUDA pair with no prebuilt kernel, or a driver mismatch
all raise at ``from_pretrained`` time. On a tournament task that exception costs
the whole task; sdpa costs some throughput and nothing else.

The downgrade is sticky for the run. A trainer loads the policy, then often a
reference model and/or a PEFT wrapper from the same kwargs dict; once we know
flash attention is unavailable, every later load should skip it too rather than
re-raise and re-catch.
"""

FALLBACK_ATTN = "sdpa"

# Already the fallback, or deliberately eager — a failure here is a real
# problem with the model or the environment and must surface, not be masked.
_NON_FLASH = ("eager", FALLBACK_ATTN)


def load_with_attn_fallback(loader, *args, model_kwargs, log=print, **kwargs):
    """``loader(*args, **model_kwargs, **kwargs)``, retried once without flash attention.

    ``model_kwargs`` is mutated on fallback so subsequent loads from the same
    dict go straight to sdpa.
    """
    requested = model_kwargs.get("attn_implementation")
    try:
        return loader(*args, **model_kwargs, **kwargs)
    except Exception as exc:
        if requested is None or requested in _NON_FLASH:
            raise
        log(
            f"attn_implementation={requested} unavailable "
            f"({type(exc).__name__}: {exc}) — retrying with {FALLBACK_ATTN}"
        )
        model_kwargs["attn_implementation"] = FALLBACK_ATTN
        return loader(*args, **model_kwargs, **kwargs)
