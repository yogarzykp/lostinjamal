"""Append-only run telemetry: what we knew, what we chose, what it scored.

Purpose
-------
We want a learning-rate estimator driven by the validator's baseline-stats
evidence (weight_rms, init_loss, output_entropy, dataset shape). We cannot build
one yet, because nothing links that evidence to a good learning rate:
family_lr_table.py — our best calibration source, derived from past winners — is
keyed only on (family, size_bucket, task) and carries no evidence columns. An
estimator written today would either copy another entrant's constants (a port,
and tuned for their pipeline) or invent our own (guessing at the most sensitive
hyperparameter we have, in a competition that scores mistakes as zero).

So: collect first. Every run records the evidence that was available, the
configuration we derived from it, and what that configuration actually scored.
After enough runs the estimator can be fitted on our own measurements — which is
also a far better answer to the duplicate judge than a reimplementation of
someone else's formula.

Where it writes
---------------
TRAINING_TELEMETRY_PATH, else <output_dir>/run_telemetry.jsonl.

Deliberately NOT the submission directory. Everything in there is uploaded to
Hugging Face, and this file is a description of our decision process — exactly
the "strategy leak" the validator's own uploader started stripping from its
artifacts (it now excludes trainer_state.json and training_args.bin for that
reason). Keep it out of the submission.

Retrieval is honest about its limits: on validator-run tournament tasks the
container is ephemeral and we do not get the file back. This pays off on runs we
control — our own VPS test trains and A/Bs — which is where the calibration set
will actually come from.

Format: one JSON object per line, each with a "kind" discriminator, so records
can be appended from different stages without coordinating a schema.
"""

import json
import os

_ENV_PATH = "TRAINING_TELEMETRY_PATH"
_DISABLE = "TRAINING_TELEMETRY_DISABLE"


def _resolve_path(output_dir: str = None) -> str:
    explicit = os.getenv(_ENV_PATH)
    if explicit:
        return explicit
    base = output_dir or os.getenv("OUTPUT_DIR") or "."
    return os.path.join(base, "run_telemetry.jsonl")


def record(kind: str, payload: dict, output_dir: str = None) -> None:
    """Append one telemetry record. Never raises, never blocks training."""
    if os.getenv(_DISABLE) == "1":
        return
    try:
        path = _resolve_path(output_dir)
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        row = {"kind": kind}
        row.update(payload or {})
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")
    except Exception as exc:
        print(f"[telemetry] skipped ({type(exc).__name__}: {exc})", flush=True)


def record_config(
    *,
    task_type: str,
    baseline_stats: dict = None,
    run_config: dict = None,
    extra: dict = None,
    output_dir: str = None,
) -> None:
    """Evidence available before training, plus the config we derived from it.

    Records only the scalar evidence fields an estimator could plausibly use —
    not the whole baseline payload, which is large and mostly per-layer detail.
    """
    try:
        from baseline_stats_reader import (
            get_dataset_stat,
            get_init_loss,
            get_init_loss_std,
            get_output_entropy,
            get_seq_len_p95,
            get_throughput,
            get_weight_rms,
        )

        evidence = {
            "weight_rms": get_weight_rms(baseline_stats),
            "init_loss": get_init_loss(baseline_stats),
            "init_loss_std": get_init_loss_std(baseline_stats),
            "output_entropy": get_output_entropy(baseline_stats),
            "seq_len_p95": get_seq_len_p95(baseline_stats),
            "total_tokens": get_dataset_stat(baseline_stats, "total_tokens"),
            "num_records": get_dataset_stat(baseline_stats, "num_records"),
            "near_duplicate_rate": get_dataset_stat(baseline_stats, "near_duplicate_rate"),
            "vocab_coverage_ratio": get_dataset_stat(baseline_stats, "vocab_coverage_ratio"),
            "throughput": get_throughput(baseline_stats),
            "has_baseline": baseline_stats is not None,
        }
    except Exception as exc:
        evidence = {"error": f"{type(exc).__name__}: {exc}", "has_baseline": baseline_stats is not None}

    decision = {}
    if isinstance(run_config, dict):
        for k in (
            "learning_rate",
            "batch_size",
            "epoch_num",
            "gradient_accumulation_steps",
            "max_steps",
            "use_lora",
            "optimizer",
            "min_lr_rate",
            "neftune_noise_alpha",
            "packing",
        ):
            if k in run_config:
                decision[k] = run_config[k]

    record(
        "config",
        {"task_type": task_type, "evidence": evidence, "decision": decision, **(extra or {})},
        output_dir=output_dir,
    )


def record_outcome(
    *,
    task_type: str = None,
    eval_loss: float = None,
    step: int = None,
    learning_rate: float = None,
    note: str = None,
    output_dir: str = None,
    **extra,
) -> None:
    """What a configuration actually scored. The label for the eventual fit."""
    record(
        "outcome",
        {
            "task_type": task_type,
            "eval_loss": eval_loss,
            "step": step,
            "learning_rate": learning_rate,
            "note": note,
            **extra,
        },
        output_dir=output_dir,
    )


def load(path: str) -> list:
    """Read a telemetry file back. For offline analysis, not used in training."""
    rows = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        rows.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    except FileNotFoundError:
        return []
    return rows
