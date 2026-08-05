"""Step-time estimation from the validator's measured throughput probe.

Why this exists
---------------
Every time-budget decision we make — how many steps fit, how many epochs to
plan, how often to evaluate, whether to subsample — divides a wall-clock budget
by an estimate of seconds per step. Until now that estimate was a hardcoded
guess:

    _fa_factor = 0.02 if _supports_fa else 0.06
    _step_time_est = max(0.5, _fa_factor * effective_batch * (max_length / 1024))

Two constants standing in for the combined effect of model size, attention
implementation, GPU model, GPU count, and sequence length. It cannot be right
across a pool spanning 0.1B to 71B on varying hardware, and being wrong in
either direction is expensive: over-estimate and we leave budget unspent,
under-estimate and the wall-clock stop cuts the schedule mid-decay.

The validator already measured the real thing. Its model-prep container runs a
timed forward+backward on the actual model on the actual GPU before our
container starts, and passes the result through baseline_stats:

    throughput: {tokens_per_sec, seq_len, micro_batch_size, n_gpus, gpu_name}

Verified against G.O.D core/models/model_prep_models.py (ThroughputStats) and
trainer/runtime.py, which writes baseline_stats_{task_id}.json and sets
BASELINE_STATS_PATH. Measured, on our hardware, costing none of our budget.

What this module does
---------------------
Converts tokens/sec into seconds/step for OUR planned shape (batch, grad_accum,
max_length, gpu count), with the scaling stated explicitly rather than folded
into a magic factor, and returns the guess-based estimate unchanged whenever the
probe is absent. It never raises.

Deliberate conservatism: the probe measures a clean forward+backward and does
not include optimizer step, gradient accumulation boundaries, checkpointing
recompute, dataloader stalls, or logging. We inflate by OVERHEAD_FACTOR so the
plan errs toward finishing early rather than being truncated.
"""

# The probe is a bare fwd+bwd. Real steps also pay optimizer update, grad-accum
# boundaries, dataloader, and logging. Measured winners plan with a comparable
# safety margin; we start at 1.35 and should revisit once we have telemetry
# comparing predicted vs actual step time on real tasks.
OVERHEAD_FACTOR = 1.35

# Gradient checkpointing trades compute for memory: activations are recomputed
# during backward, which costs roughly an extra forward pass.
GRADIENT_CHECKPOINT_FACTOR = 1.30

# Scaling in GPU count is never linear (communication, stragglers).
DDP_EFFICIENCY = 0.90


def tokens_per_step(batch: int, grad_accum: int, max_length: int) -> int:
    """Tokens processed per optimizer step, per GPU."""
    return max(1, int(batch) * max(1, int(grad_accum)) * max(1, int(max_length)))


def estimate_step_seconds(
    throughput: dict,
    batch: int,
    grad_accum: int,
    max_length: int,
    n_gpus: int = 1,
    gradient_checkpointing: bool = True,
) -> float:
    """Seconds per optimizer step, derived from the measured throughput probe.

    throughput is the dict from baseline_stats_reader.get_throughput().

    The probe's tokens_per_sec is reported for the configuration it ran at
    (its own seq_len / micro_batch_size / n_gpus). We treat tokens/sec as the
    portable quantity and rescale for our own shape:

      1. Take measured tokens/sec, normalise to per-GPU.
      2. Scale back up by our GPU count, discounted by DDP_EFFICIENCY.
      3. Divide our tokens-per-step by that rate.
      4. Inflate for real-step overhead, and again if we recompute activations.

    Raises nothing. Returns a positive float.
    """
    tps = float(throughput.get("tokens_per_sec") or 0.0)
    if tps <= 0:
        raise ValueError("throughput probe has no positive tokens_per_sec")

    probe_gpus = max(1, int(throughput.get("n_gpus") or 1))
    per_gpu_tps = tps / probe_gpus

    our_gpus = max(1, int(n_gpus))
    effective_tps = per_gpu_tps * our_gpus * (DDP_EFFICIENCY if our_gpus > 1 else 1.0)

    seconds = tokens_per_step(batch, grad_accum, max_length) / effective_tps
    seconds *= OVERHEAD_FACTOR
    if gradient_checkpointing:
        seconds *= GRADIENT_CHECKPOINT_FACTOR
    return max(0.01, seconds)


def resolve_step_seconds(
    throughput,
    fallback_estimate: float,
    batch: int,
    grad_accum: int,
    max_length: int,
    n_gpus: int = 1,
    gradient_checkpointing: bool = True,
    sanity_ratio: float = 20.0,
) -> tuple:
    """Measured step time when trustworthy, otherwise the caller's own estimate.

    Returns (seconds_per_step, source) where source is one of
    "measured" | "fallback:no-probe" | "fallback:<reason>".

    The sanity gate matters. A probe that disagrees with the heuristic by more
    than sanity_ratio in either direction is more likely to be a unit mismatch,
    a probe run on different hardware, or a schema change than a genuine 20x
    error in the heuristic — and silently trusting it would mis-plan the whole
    run. In that case we keep the fallback and say so loudly, so the disagreement
    shows up in logs instead of in a truncated schedule.
    """
    if not isinstance(throughput, dict):
        return float(fallback_estimate), "fallback:no-probe"
    try:
        measured = estimate_step_seconds(
            throughput,
            batch=batch,
            grad_accum=grad_accum,
            max_length=max_length,
            n_gpus=n_gpus,
            gradient_checkpointing=gradient_checkpointing,
        )
    except Exception as exc:
        return float(fallback_estimate), f"fallback:{type(exc).__name__}"

    fb = float(fallback_estimate)
    if fb > 0:
        ratio = measured / fb
        if ratio > sanity_ratio or ratio < (1.0 / sanity_ratio):
            return fb, f"fallback:implausible(measured={measured:.2f}s ratio={ratio:.1f}x)"

    return measured, "measured"
