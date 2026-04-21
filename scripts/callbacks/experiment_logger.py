"""ExperimentLoggerCallback — emit end-of-training summary to Redis for MCP.

At `on_train_end`, push one JSON blob to `experiments:{experiment_name}` list
so later we can compare runs across experiments without scraping logs.

Captures: task_id, model, experiment_name, final train_loss, last eval_loss,
best eval_loss seen, total steps, total epochs, wallclock seconds, feature
flags active, timestamps.

Fail-closed on Redis errors.

Feature flag: INSTRUCT_EXPERIMENT_LOG=1 (opt-in). Defaults off.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Optional

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from transformers import TrainerCallback

EXPERIMENTS_MAX_ENTRIES = 500

# Env var prefix used by project feature flags — scanned + recorded
# so each experiment run knows which flags were active.
FLAG_PREFIX = "INSTRUCT_"


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
        print(f"[ExperimentLogger] Redis unreachable: {exc}. Disabling.", flush=True)
        return None


def _active_flags() -> dict:
    return {k: v for k, v in os.environ.items() if k.startswith(FLAG_PREFIX)}


class ExperimentLoggerCallback(TrainerCallback):
    def __init__(self, task_id: str, model_name: str, experiment_name: str = "baseline"):
        self.task_id = task_id
        self.model_name = model_name
        self.experiment_name = experiment_name
        self.redis_key = f"experiments:{experiment_name}"
        self.client = _redis_client()
        self.started_at = datetime.now(timezone.utc)
        self.best_eval_loss: Optional[float] = None
        self.last_train_loss: Optional[float] = None
        self.last_eval_loss: Optional[float] = None

    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs is None:
            return
        if "loss" in logs and logs["loss"] is not None:
            self.last_train_loss = float(logs["loss"])
        if "eval_loss" in logs and logs["eval_loss"] is not None:
            eval_loss = float(logs["eval_loss"])
            self.last_eval_loss = eval_loss
            if self.best_eval_loss is None or eval_loss < self.best_eval_loss:
                self.best_eval_loss = eval_loss

    def on_train_end(self, args, state, control, **kwargs):
        if self.client is None:
            return
        ended = datetime.now(timezone.utc)
        entry = {
            "experiment": self.experiment_name,
            "task_id": self.task_id,
            "model": self.model_name,
            "total_steps": state.global_step,
            "total_epochs": round(state.epoch, 3) if state.epoch else None,
            "last_train_loss": self.last_train_loss,
            "last_eval_loss": self.last_eval_loss,
            "best_eval_loss": self.best_eval_loss,
            "wallclock_sec": round((ended - self.started_at).total_seconds(), 1),
            "started_at": self.started_at.isoformat(),
            "ended_at": ended.isoformat(),
            "active_flags": _active_flags(),
        }
        entry = {k: v for k, v in entry.items() if v is not None}
        try:
            self.client.lpush(self.redis_key, json.dumps(entry))
            self.client.ltrim(self.redis_key, 0, EXPERIMENTS_MAX_ENTRIES - 1)
            print(f"[ExperimentLogger] Logged experiment '{self.experiment_name}' to {self.redis_key}", flush=True)
        except Exception as exc:
            print(f"[ExperimentLogger] push failed: {exc}", flush=True)
