"""Read-only MCP server for text-jagger training observability.

Exposes Redis-backed state + callback metrics to Claude Code via stdio.

Tools (all read-only — no mutation):
- get_job_state(): full Redis state JSON (mode, train, runs, lrs, check_details)
- get_current_loss(): latest loss/lr/step from state
- list_runs(): array of LR search attempts
- get_metrics(task_id, n): last N per-step metrics entries (from MetricsCallback)
- get_experiment_results(experiment_name, n): end-of-run summaries
- get_lr_search_history(): attempts + best + budget
- tail_log(log_path, n): last N lines of a training log file
- compare_runs(exp_a, exp_b): delta eval_loss + hyperparam diff between 2 runs

Connection:
  ~/.claude.json -> mcpServers["text-jagger"]
  - command: path/to/mcp_server/.venv/bin/python
  - args: ["-m", "mcp_server.server"]
  - env: REDIS_URL, LOG_ROOT

Redis source:
  REDIS_URL=redis://localhost:6379 (default)
  For H100 pod access: `ssh -L 6379:localhost:6379 pod` then localhost works.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Optional

import redis
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("text-jagger")

STATE_KEY = "state"  # matches scripts/state_manager.py
DEFAULT_LOG_ROOT = "/workspace/scripts"
MAX_TAIL_LINES = 500


def _client() -> redis.Redis:
    url = os.environ.get("REDIS_URL", "redis://localhost:6379")
    return redis.from_url(url, decode_responses=True, socket_timeout=3, socket_connect_timeout=3)


def _safe_get_state() -> dict:
    try:
        raw = _client().get(STATE_KEY)
        if not raw:
            return {}
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"_error": "state JSON corrupt"}
    except redis.RedisError as exc:
        return {"_error": f"redis error: {exc}"}


@mcp.tool()
def get_job_state() -> dict:
    """Return full training state from Redis (STATE_KEY='state').

    Includes: mode (initial/continue/finish), train (current run metadata),
    runs (LR search attempts so far), lrs (LR schedule for continue mode),
    next_runs, check_details (timing estimation from CustomEvalSaveCallback).

    Returns {} if no training active. Returns {'_error': ...} if Redis down.
    """
    return _safe_get_state()


@mcp.tool()
def get_current_loss() -> dict:
    """Return latest loss from the in-flight run.

    Pulls from state['train'] — the current training attempt. Returns
    {step, loss, lr, output_dir, start_time} or {'_error': ...}.
    """
    state = _safe_get_state()
    if "_error" in state:
        return state
    train = state.get("train", {})
    if not train:
        return {"_info": "no active run"}
    return {
        "lr": train.get("lr"),
        "output_dir": train.get("output_dir"),
        "start_time": train.get("start_time"),
        "current_loss": train.get("current_loss"),
        "mode": state.get("mode"),
    }


@mcp.tool()
def list_runs() -> list[dict]:
    """Return all completed LR search runs in this training session.

    From state['runs'] — each entry is one "continue" mode attempt with its
    lr + final current_loss. Empty if mode='initial' or no search yet.
    """
    state = _safe_get_state()
    if "_error" in state:
        return [state]
    runs = state.get("runs", [])
    return runs


@mcp.tool()
def get_lr_search_history() -> dict:
    """Return the LR search state: schedule, attempts made, best result so far.

    Summary of state['lrs'] + state['runs'] + state['check_details']. Useful
    to decide whether the current LR ladder is exploring effectively.
    """
    state = _safe_get_state()
    if "_error" in state:
        return state

    runs = state.get("runs", [])
    best = None
    if runs:
        best_run = min(runs, key=lambda r: r.get("current_loss", float("inf")))
        best = {"lr": best_run.get("lr"), "loss": best_run.get("current_loss"), "output_dir": best_run.get("output_dir")}

    return {
        "mode": state.get("mode"),
        "next_runs": state.get("next_runs"),
        "lrs_schedule": state.get("lrs", []),
        "attempts_done": len(runs),
        "best": best,
        "check_details": state.get("check_details", {}),
    }


@mcp.tool()
def get_metrics(task_id: str, n: int = 50) -> list[dict]:
    """Return last N per-step metrics pushed by MetricsCallback.

    Redis key: metrics:{task_id}. Each entry has step, loss, lr, grad_norm,
    gpu_mem_allocated_mb, gpu_mem_reserved_mb, samples_per_sec, epoch, ts.
    Ordered newest-first (LPUSH order).

    n capped at 500.
    """
    n = min(max(1, n), 500)
    try:
        raw = _client().lrange(f"metrics:{task_id}", 0, n - 1)
        return [json.loads(item) for item in raw]
    except redis.RedisError as exc:
        return [{"_error": f"redis error: {exc}"}]
    except json.JSONDecodeError:
        return [{"_error": "corrupt metrics entry"}]


@mcp.tool()
def get_experiment_results(experiment_name: str, n: int = 20) -> list[dict]:
    """Return end-of-run summaries for `experiment_name` (from ExperimentLoggerCallback).

    Redis key: experiments:{experiment_name}. Each entry has best_eval_loss,
    last_train_loss, wallclock_sec, active_flags, etc. Newest first.

    Use this to compare multiple baseline vs variant runs for A/B analysis.
    """
    n = min(max(1, n), 100)
    try:
        raw = _client().lrange(f"experiments:{experiment_name}", 0, n - 1)
        return [json.loads(item) for item in raw]
    except redis.RedisError as exc:
        return [{"_error": f"redis error: {exc}"}]
    except json.JSONDecodeError:
        return [{"_error": "corrupt experiment entry"}]


@mcp.tool()
def tail_log(log_path: str, n: int = 100) -> dict:
    """Return the last N lines of a training log file.

    log_path must be under LOG_ROOT (default /workspace/scripts) to prevent
    path traversal. n capped at 500.
    """
    n = min(max(1, n), MAX_TAIL_LINES)
    root = Path(os.environ.get("LOG_ROOT", DEFAULT_LOG_ROOT)).resolve()
    try:
        path = Path(log_path).resolve()
        # Security: path must be inside root
        path.relative_to(root)
    except ValueError:
        return {"_error": f"log_path must be under {root}"}
    except Exception as exc:
        return {"_error": f"path error: {exc}"}

    if not path.exists():
        return {"_error": f"file not found: {path}"}

    try:
        with open(path, "rb") as f:
            # Naive tail; fine for typical log sizes (a few MB).
            data = f.read()
        lines = data.splitlines()[-n:]
        return {
            "path": str(path),
            "total_lines": len(data.splitlines()),
            "returned": len(lines),
            "lines": [line.decode("utf-8", errors="replace") for line in lines],
        }
    except Exception as exc:
        return {"_error": f"read error: {exc}"}


@mcp.tool()
def compare_runs(experiment_a: str, experiment_b: str) -> dict:
    """Compare two experiments (by name) on best_eval_loss + wallclock + flags.

    Fetches newest entry from each `experiments:{name}` list.
    Returns delta_eval_loss = (b.best - a.best) / a.best (negative means b better).
    """
    try:
        raw_a = _client().lrange(f"experiments:{experiment_a}", 0, 0)
        raw_b = _client().lrange(f"experiments:{experiment_b}", 0, 0)
    except redis.RedisError as exc:
        return {"_error": f"redis error: {exc}"}

    if not raw_a or not raw_b:
        return {
            "_error": "missing entries",
            f"{experiment_a}_count": len(raw_a),
            f"{experiment_b}_count": len(raw_b),
        }

    try:
        a = json.loads(raw_a[0])
        b = json.loads(raw_b[0])
    except json.JSONDecodeError:
        return {"_error": "corrupt experiment JSON"}

    a_loss = a.get("best_eval_loss")
    b_loss = b.get("best_eval_loss")
    delta: Optional[float] = None
    if a_loss and b_loss and a_loss > 0:
        delta = round((b_loss - a_loss) / a_loss, 5)

    # Flag diff
    a_flags = a.get("active_flags", {})
    b_flags = b.get("active_flags", {})
    flags_added_in_b = {k: v for k, v in b_flags.items() if k not in a_flags}
    flags_removed_in_b = {k: v for k, v in a_flags.items() if k not in b_flags}
    flags_changed = {k: {"a": a_flags[k], "b": b_flags[k]} for k in a_flags if k in b_flags and a_flags[k] != b_flags[k]}

    return {
        "experiment_a": experiment_a,
        "experiment_b": experiment_b,
        "a_best_eval_loss": a_loss,
        "b_best_eval_loss": b_loss,
        "delta_eval_loss_rel": delta,
        "delta_eval_loss_abs": (b_loss - a_loss) if (a_loss and b_loss) else None,
        "a_wallclock_sec": a.get("wallclock_sec"),
        "b_wallclock_sec": b.get("wallclock_sec"),
        "a_total_steps": a.get("total_steps"),
        "b_total_steps": b.get("total_steps"),
        "flags_added_in_b": flags_added_in_b,
        "flags_removed_in_b": flags_removed_in_b,
        "flags_changed": flags_changed,
    }


def main():
    mcp.run()


if __name__ == "__main__":
    main()
