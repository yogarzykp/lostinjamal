# text-jagger MCP Server (read-only)

Live monitoring of text-jagger training runs via Redis + log files. Exposed to Claude Code over stdio.

## Quick start

```bash
cd mcp_server
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Connect from Claude Code

Edit `~/.claude.json`:

```json
{
  "mcpServers": {
    "text-jagger": {
      "command": "/absolute/path/to/text-jagger/mcp_server/.venv/bin/python",
      "args": ["-m", "mcp_server.server"],
      "env": {
        "REDIS_URL": "redis://localhost:6379",
        "LOG_ROOT": "/workspace/scripts"
      }
    }
  }
}
```

For H100 training pod access, SSH-tunnel Redis first:

```bash
ssh -L 6379:localhost:6379 user@h100-host
# now localhost:6379 on your Mac = redis inside the pod
```

## Tools (all read-only)

| Tool | Args | Returns |
|---|---|---|
| `get_job_state` | — | Full Redis `state` dict (mode, train, runs, lrs, check_details) |
| `get_current_loss` | — | `{lr, output_dir, start_time, current_loss, mode}` |
| `list_runs` | — | Array of completed LR search attempts |
| `get_lr_search_history` | — | `{mode, next_runs, lrs_schedule, attempts_done, best, check_details}` |
| `get_metrics` | `task_id`, `n` | Last N per-step metrics (loss, lr, grad_norm, gpu_mem, throughput) |
| `get_experiment_results` | `experiment_name`, `n` | Last N end-of-run summaries |
| `tail_log` | `log_path`, `n` | Last N lines (path must be under LOG_ROOT) |
| `compare_runs` | `experiment_a`, `experiment_b` | Delta eval_loss + flag diff between two experiments |

## Feeding the data

Two sources populate Redis:

1. **text-jagger orchestrator** (`scripts/text_trainer.py`, `scripts/customized_trainer.py`) writes the single `state` key with state machine info.
2. **Optional observability callbacks** (gated by env flags, see `scripts/callbacks/`):
   - `INSTRUCT_METRICS_REDIS=1` → per-step metrics in `metrics:{task_id}`.
   - `INSTRUCT_EXPERIMENT_LOG=1` → end-of-run summary in `experiments:{experiment_name}`.
   - `INSTRUCT_EXPERIMENT_NAME=<str>` → default "baseline".

Without these flags, only `get_job_state`, `get_current_loss`, `list_runs`, `get_lr_search_history` return useful data.

## Safety

- **Read-only**: no tool mutates Redis or filesystem.
- **Path traversal guarded**: `tail_log` enforces `LOG_ROOT` boundary.
- **Fail-closed**: Redis unreachable → each tool returns `{"_error": ...}` instead of crashing.

## Troubleshooting

- `_error: redis error` → check `REDIS_URL` + SSH tunnel is up.
- Empty `list_runs` → training hasn't entered "continue" mode yet (only happens in LR search scenario).
- Empty `get_metrics` → set `INSTRUCT_METRICS_REDIS=1` when spawning `text_trainer.py` and ensure Redis reachable from trainer container.
