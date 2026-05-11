"""Phase A — Pull winner training_args.bin from past tournament tasks.

Goal: build empirical (arch_family, size_bucket, task_type) → HP table from
past winners' actual training configurations, derived dynamically from
public sources (Gradients Fast API + HuggingFace Hub).

Strategy:
  1. For each task_id in TASK_LIST → query Fast API → top-3 hotkey repos
  2. For each repo → extract training_args.bin via pickle
  3. Save per-record JSON to /tmp/winner_data/<task_id>__<hotkey>.json
  4. Aggregate later in Phase B

NO per-model lookup logic here — this is pure DATA COLLECTION.
"""

from __future__ import annotations

import argparse
import io
import json
import pickle
import sys
import time
import urllib.request
import urllib.error
import zipfile
from pathlib import Path
from typing import Optional


GRADIENTS_API = "https://api.gradients.io"
HF_BASE = "https://huggingface.co"


# Tasks user provided (16) + recent historical anchors for broader family coverage
DEFAULT_TASKS = [
    # Round of user's prompt 2026-05-09
    "708e03d4-1a55-440a-ad2e-58f1284c5d61",
    "acd597ef-23a9-4713-8e3f-8a1bbbde5648",
    "0bda471b-9209-4778-8587-5e10a46205d7",
    "71e64603-f641-40cb-b0fd-91a13dd117fa",
    "a4e98b56-df24-4ed1-87b3-8283756579d4",
    "6ef76e40-adb3-42e7-b0f1-9739821324b7",
    "45d5ffd1-2744-436d-a1df-42af6d03913a",
    "c789618d-44d7-4183-8ac0-3d2e86f773d4",
    "f2a461ec-3e48-40ce-9274-7d9b411a4f22",
    "e84aca25-ebd0-4afd-af15-e489310011ef",
    "89f19db7-0b8e-42db-b18b-a5bff871a389",
    "0c5c7124-3e21-4487-b31c-0a1d63a2da51",
    "8fbf4273-be63-4b90-8fa3-016b9f12bb1f",
    "020b2f24-3214-461e-a24e-d9f9cf86669c",
    "0d824d73-6a57-4eba-9f90-3a65a1fa5094",
    "a2531680-3421-4156-aa94-736466bc2250",
    # Historical anchors from prior tournaments (memory-recorded)
    "ded7e684-0213-4627-a0d7-dcb407d8f838",  # SmolLM2-1.7B-Instruct (winner 5C5FBvLa)
    "03f6b01c-aa0e-4f6c-94f7-9e6b08d6d12e",  # need to verify exists
    "f5fbe40f-39e2-4593-a44a-7dfa6fb2a233",  # SmolLM-135M GRPO
    "574ded42-37f5-453d-bbeb-7f1ca9b1d4ec",  # DPO task
    "dc568dbe-5b22-422e-b76b-25a9f00fb40e",  # SmolLM2
    "0304997e-9f5a-4afb-9e3f-3c6dc6fae867",  # Qwen 7B CodeMath
    "05933c53-0ab2-4faf-b62e-bd7be1f1a9d0",  # gpt-neo-125m
    "d4456b0f-2a35-4a78-87bf-a08a18a0e6e3",  # DPO Phi-3.5
    "091116b6-5dd9-4f44-925d-d4d6b9c1d8e7",  # GRPO Qwen 1.5B
    "596e8ab3-cc4a-4d59-b8ca-f50f4ce0cb88",  # gemma-2-2b + Magicoder
    "7c8ba003-9b4a-4f4f-86e8-2cc7b8fb1ce5",  # Llama-3.2-1B
]


# Pickle unpickler for HF training_args.bin without importing transformers
class _ArgsUnpickler(pickle.Unpickler):
    """Minimal Unpickler stub. transformers may serialize TrainingArguments
    + enum-ish classes; we shim them as generic objects that capture state."""

    def find_class(self, module, name):
        # Special: torch.device
        if (module, name) == ("torch", "device"):
            return lambda *a: ":".join(str(x) for x in a) if a else "cpu"
        # TrainingArguments + its frozen-dataclass cousins
        if name == "TrainingArguments":
            class StubArgs:
                def __setstate__(self, state):
                    self.__dict__.update(state if isinstance(state, dict) else {})
            return StubArgs
        # Enum-ish (XxxStrategy, XxxNames, XxxType, XxxOption)
        if name.endswith(("Strategy", "Names", "Option", "Type")):
            return lambda *a: ":".join(str(x) for x in a) if a else "unset"
        # Catch-all: define class on the fly that absorbs setstate
        cls = type(name, (), {"__module__": module})
        cls.__setstate__ = lambda self, s: (
            self.__dict__.update(s) if isinstance(s, dict) else None
        )
        return cls


def extract_training_args(repo_id: str, timeout: int = 30) -> Optional[dict]:
    """Pickle-extract training_args.bin from HF repo. Returns dict or None."""
    url = f"{HF_BASE}/{repo_id}/resolve/main/training_args.bin"
    req = urllib.request.Request(url, headers={"User-Agent": "research-pull/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            binary = resp.read()
    except (urllib.error.HTTPError, urllib.error.URLError) as exc:
        return {"_error": f"download: {exc}"}
    except Exception as exc:
        return {"_error": f"download: {exc}"}

    try:
        with zipfile.ZipFile(io.BytesIO(binary)) as zf:
            data = None
            for n in zf.namelist():
                if n.endswith("data.pkl"):
                    data = zf.read(n)
                    break
        if not data:
            return {"_error": "no data.pkl in zip"}
        obj = _ArgsUnpickler(io.BytesIO(data)).load()
        d = obj.__dict__ if hasattr(obj, "__dict__") else dict(obj)
        # Sanitize for JSON
        return {k: _sanitize(v) for k, v in d.items()}
    except Exception as exc:
        return {"_error": f"parse: {exc}"}


def _sanitize(v):
    """Convert non-JSON-serializable to str."""
    if v is None or isinstance(v, (str, int, float, bool)):
        return v
    if isinstance(v, list):
        return [_sanitize(x) for x in v]
    if isinstance(v, tuple):
        return [_sanitize(x) for x in v]
    if isinstance(v, dict):
        return {str(k): _sanitize(x) for k, x in v.items()}
    return str(v)


def fetch_task_details(task_id: str, timeout: int = 8) -> Optional[dict]:
    """Query Gradients Fast API for task details + hotkey leaderboard."""
    url = f"{GRADIENTS_API}/auditing/tasks/{task_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "research-pull/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except Exception as exc:
        print(f"  fetch_task_details({task_id}) ERR: {exc}", flush=True)
        return None


def fetch_trainer_state(repo_id: str, timeout: int = 15) -> Optional[dict]:
    """Fetch trainer_state.json (eval trajectory)."""
    url = f"{HF_BASE}/{repo_id}/resolve/main/trainer_state.json"
    req = urllib.request.Request(url, headers={"User-Agent": "research-pull/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


def fetch_model_config(repo_id: str, timeout: int = 10) -> Optional[dict]:
    """Fetch base model config.json for architecture fingerprint."""
    url = f"{HF_BASE}/{repo_id}/resolve/main/config.json"
    req = urllib.request.Request(url, headers={"User-Agent": "research-pull/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


def fetch_loss_txt(repo_id: str, timeout: int = 10) -> Optional[str]:
    """Fetch loss.txt (text-jagger format: best_step,best_loss)."""
    url = f"{HF_BASE}/{repo_id}/resolve/main/loss.txt"
    req = urllib.request.Request(url, headers={"User-Agent": "research-pull/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode().strip()
    except Exception:
        return None


def process_task(task_id: str, out_dir: Path, top_k: int = 3) -> dict:
    """Pull all winner data for one task. Returns summary."""
    print(f"[task {task_id[:8]}] fetching...", flush=True)
    detail = fetch_task_details(task_id)
    if not detail:
        return {"task_id": task_id, "_error": "no task details"}

    summary = {
        "task_id": task_id,
        "task_type": detail.get("task_type"),
        "model": detail.get("model_id"),
        "dataset": detail.get("ds"),
        "hours_to_complete": detail.get("hours_to_complete"),
        "created_at": detail.get("created_at"),
        "winners": [],
    }

    # Base model config (for arch fingerprint)
    base_model = detail.get("model_id")
    if base_model:
        base_cfg = fetch_model_config(base_model)
        if base_cfg:
            summary["base_arch"] = (base_cfg.get("architectures") or [""])[0]
            summary["base_hidden_size"] = base_cfg.get("hidden_size")
            summary["base_num_layers"] = base_cfg.get("num_hidden_layers")
            summary["base_vocab_size"] = base_cfg.get("vocab_size")
            summary["base_intermediate_size"] = base_cfg.get("intermediate_size")

    hd = detail.get("hotkey_details") or []
    tops = sorted(
        [h for h in hd if (h.get("test_loss") or 0) > 0 and h.get("repo")],
        key=lambda x: x["test_loss"],
    )[:top_k]

    for h in tops:
        repo = h["repo"]
        print(f"  rank {h.get('rank')} hotkey={h.get('hotkey', '')[:8]} repo={repo}", flush=True)
        args = extract_training_args(repo)
        state = fetch_trainer_state(repo)
        loss_txt = fetch_loss_txt(repo)

        record = {
            "hotkey": h.get("hotkey"),
            "rank": h.get("rank"),
            "test_loss": h.get("test_loss"),
            "synth_loss": h.get("synth_loss"),
            "quality_score": h.get("quality_score"),
            "repo": repo,
            "training_args": args,
            "loss_txt": loss_txt,
        }
        if state:
            record["best_global_step"] = state.get("best_global_step")
            record["best_metric"] = state.get("best_metric")
            record["global_step"] = state.get("global_step")
            record["epoch"] = state.get("epoch")
            # Eval trajectory
            log_history = state.get("log_history", [])
            evals = [(h.get("step"), h.get("eval_loss")) for h in log_history
                     if h.get("eval_loss") is not None]
            record["eval_trajectory"] = evals
        summary["winners"].append(record)

        # Save per-record JSON
        out_path = out_dir / f"{task_id}__{h.get('hotkey', 'unknown')[:8]}.json"
        out_path.write_text(json.dumps(record, indent=2, default=str))

    summary_path = out_dir / f"_task_{task_id}_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, default=str))
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", nargs="+", default=None,
                    help="Task IDs to pull (space-separated). Default: 16 user tasks + historical anchors")
    ap.add_argument("--tasks-file", default=None,
                    help="File with one task ID per line (alternative to --tasks). Avoids shell arg-list collapsing.")
    ap.add_argument("--top-k", type=int, default=3,
                    help="Pull top-K winners per task (default 3)")
    ap.add_argument("--out-dir", default="/tmp/winner_data",
                    help="Output directory (default /tmp/winner_data)")
    ap.add_argument("--rate-limit", type=float, default=0.5,
                    help="Sleep seconds between repos (HF rate limit guard)")
    args = ap.parse_args()

    # Resolve tasks: file > --tasks > DEFAULT_TASKS
    if args.tasks_file:
        with open(args.tasks_file) as f:
            args.tasks = [line.strip() for line in f if line.strip()]
    elif args.tasks is None:
        args.tasks = DEFAULT_TASKS

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"[research] Output: {out_dir}", flush=True)
    print(f"[research] Tasks: {len(args.tasks)}, top-K winners each", flush=True)

    summaries = []
    for i, tid in enumerate(args.tasks, 1):
        print(f"\n=== [{i}/{len(args.tasks)}] {tid} ===", flush=True)
        try:
            s = process_task(tid, out_dir, top_k=args.top_k)
            summaries.append(s)
        except Exception as exc:
            print(f"  task error: {exc}", flush=True)
            summaries.append({"task_id": tid, "_error": str(exc)})
        time.sleep(args.rate_limit)

    # Master summary
    master_path = out_dir / "_master_summary.json"
    master_path.write_text(json.dumps(summaries, indent=2, default=str))
    print(f"\n[research] Master summary: {master_path}", flush=True)
    print(f"[research] Total tasks: {len(summaries)}, "
          f"total winner records: {sum(len(s.get('winners', [])) for s in summaries)}", flush=True)


if __name__ == "__main__":
    main()
