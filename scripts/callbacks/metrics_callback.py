"""MetricsCallback — push per-step training metrics to Redis for MCP / dashboards.

Design:
- Wrap all Redis calls in try/except. Training MUST NOT crash on Redis outage.
- Use key prefix `metrics:{task_id}` (list). LPUSH + LTRIM 1000 to cap size.
- Push on `on_log` (HF Trainer emits logs at `logging_steps` cadence).
- Metrics captured: step, loss, lr, grad_norm, epoch, gpu_mem_allocated_mb,
  gpu_mem_reserved_mb, samples_per_sec, ts (iso utc).

Feature flag: INSTRUCT_METRICS_REDIS=1 (opt-in). Default off for safety.

Register from train_instruct.py:
    if os.getenv("INSTRUCT_METRICS_REDIS") == "1":
        callbacks.append(MetricsCallback(task_id, experiment_name))
"""
from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from typing import Optional

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

import torch
from transformers import TrainerCallback

METRICS_MAX_ENTRIES = 1000


def _redis_client() -> Optional["redis.Redis"]:
    if not REDIS_AVAILABLE:
        return None
    try:
        client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            password=os.getenv("REDIS_PASSWORD", None),
            db=int(os.getenv("REDIS_DB", 0)),
            decode_responses=True,
            socket_timeout=2,
            socket_connect_timeout=2,
        )
        client.ping()
        return client
    except Exception as exc:
        print(f"[MetricsCallback] Redis unreachable: {exc}. Disabling metrics push.", flush=True)
        return None


def _gpu_mem_mb() -> tuple[float, float]:
    try:
        if not torch.cuda.is_available():
            return 0.0, 0.0
        allocated = torch.cuda.memory_allocated() / (1024 ** 2)
        reserved = torch.cuda.memory_reserved() / (1024 ** 2)
        return round(allocated, 2), round(reserved, 2)
    except Exception:
        return 0.0, 0.0


class MetricsCallback(TrainerCallback):
    def __init__(self, task_id: str, experiment_name: str = "baseline"):
        self.task_id = task_id
        self.experiment_name = experiment_name
        self.redis_key = f"metrics:{task_id}"
        self.client = _redis_client()
        self.last_step_time = time.time()
        self.last_step = 0

    def _push(self, entry: dict) -> None:
        if self.client is None:
            return
        try:
            self.client.lpush(self.redis_key, json.dumps(entry))
            self.client.ltrim(self.redis_key, 0, METRICS_MAX_ENTRIES - 1)
            self.client.expire(self.redis_key, 60 * 60 * 48)  # 48h TTL
        except Exception as exc:
            print(f"[MetricsCallback] push failed: {exc}", flush=True)

    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs is None:
            return
        if state.global_step == self.last_step:
            return

        alloc_mb, reserved_mb = _gpu_mem_mb()
        now = time.time()
        steps_delta = state.global_step - self.last_step
        time_delta = max(now - self.last_step_time, 1e-6)
        samples_per_sec = steps_delta * args.per_device_train_batch_size * max(torch.cuda.device_count(), 1) / time_delta

        entry = {
            "experiment": self.experiment_name,
            "step": state.global_step,
            "epoch": round(logs.get("epoch", 0.0), 4),
            "loss": logs.get("loss"),
            "eval_loss": logs.get("eval_loss"),
            "lr": logs.get("learning_rate"),
            "grad_norm": logs.get("grad_norm"),
            "gpu_mem_allocated_mb": alloc_mb,
            "gpu_mem_reserved_mb": reserved_mb,
            "samples_per_sec": round(samples_per_sec, 3),
            "ts": datetime.now(timezone.utc).isoformat(),
        }
        # Drop None values for cleaner payload
        entry = {k: v for k, v in entry.items() if v is not None}
        self._push(entry)

        self.last_step = state.global_step
        self.last_step_time = now
