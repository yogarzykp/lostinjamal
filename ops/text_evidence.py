#!/usr/bin/env python3
"""text-evidence: what did every participant ACTUALLY run on one text task — the text-side
counterpart of the plugin's image-evidence agent.

  python3 ops/text_evidence.py recon/<tourn_id>/<task_id> [--ours <hotkey>]

Reads only what the recon sweep wrote (api.json, hf_*.json, participant_*.md, augmented.json)
and tabulates, per hotkey: rank, test_loss, method (LoRA / full), lora rank + alpha + targets,
dtype, base repo (augmented?), and — from the Loki log — training wall time, steps, epochs,
learning rate(s), batch, eval count, first-eval time, tracebacks, ladder rungs, fallback. Every
cell is either a value read from a file or UNAVAILABLE with the reason. Nothing is inferred.
Prints a markdown table and writes RECIPES.json next to the inputs.
"""
import argparse, glob, json, os, re, sys

ap = argparse.ArgumentParser(); ap.add_argument("task_dir"); ap.add_argument("--ours", default="5HBgDWKxNX3333Yit3qMokkYY4Guz1r8Qfons2UJTSU5oqjV")
a = ap.parse_args(); D = a.task_dir.rstrip("/")
api = json.load(open(os.path.join(D, "api.json")))
try: aug = json.load(open(os.path.join(D, "augmented.json")))
except Exception: aug = {}

def U(reason): return {"UNAVAILABLE": reason}
def num(s):
    try: return float(s)
    except Exception: return None

def read_hf(short):
    p = os.path.join(D, f"hf_{short}.json")
    if not os.path.exists(p): return U("no hf record (no repo or fetch failed)")
    d = json.load(open(p)); files = d.get("files") or {}
    ac = files.get("adapter_config.json") if isinstance(files, dict) else None
    hdr = d.get("safetensors_header") or {}
    out = {"method": d.get("method"), "file_count": d.get("file_count"), "base": d.get("base_model_name_or_path")}
    if isinstance(ac, dict):
        out.update({"lora_r": ac.get("r"), "lora_alpha": ac.get("lora_alpha"), "targets": ac.get("target_modules"),
                    "dropout": ac.get("lora_dropout"), "use_rslora": ac.get("use_rslora"), "use_dora": ac.get("use_dora"),
                    "init": ac.get("init_lora_weights")})
    if isinstance(hdr, dict):
        out.update({"hdr_rank": hdr.get("lora_rank"), "dtype": hdr.get("dtype"), "tensors": hdr.get("tensor_count")})
    tree = d.get("tree") or []
    names = [t.get("path") for t in tree if isinstance(t, dict)]
    out["has_training_args"] = any(n and "training_args" in n for n in names)
    out["has_loss_txt"] = any(n == "loss.txt" for n in names)
    out["weights_bytes"] = sum((t.get("size") or 0) for t in tree if isinstance(t, dict) and str(t.get("path","")).endswith((".safetensors", ".bin")))
    return out

RE = {
  "lr": re.compile(r"'learning_rate': ([0-9.e+-]+)"),
  "loss": re.compile(r"'loss': ([0-9.]+)"),
  "epoch": re.compile(r"'epoch': ([0-9.]+)"),
  "eval": re.compile(r"'eval_loss': ([0-9.]+)"),
  "step_bar": re.compile(r"(\d+)/(\d+) \[(\d+):(\d+)(?::(\d+))?<"),
  "tb": re.compile(r"Traceback \(most recent call last\)"),
  "oom": re.compile(r"OutOfMemoryError|CUDA out of memory"),
  "ladder": re.compile(r"batch size from (\d+) to (\d+)|halv|ladder", re.I),
  "fallback": re.compile(r"falling back to noise|noise fallback|clean copy of the base|add_random_noise", re.I),
  "batch": re.compile(r"per_device_train_batch_size[=: ]+(\d+)|batch_size[=: ]+(\d+)|batch=(\d+)"),
  "ga": re.compile(r"gradient_accumulation_steps[=: ]+(\d+)|grad_accum=(\d+)"),
  "epochs": re.compile(r"num_train_epochs[=: ]+([0-9.]+)|epochs=(\d+)"),
  "lora_r": re.compile(r"lora_r[=: ]+(\d+)|\br=(\d+)\b|lora_rank[=: ]+(\d+)"),
  "maxlen": re.compile(r"max_length[=: ]+(\d+)|max_len=(\d+)|sequence_len[=: ]+(\d+)"),
  "done": re.compile(r"Training successfully done|training completed|Saving model|Upload(ed)? .*model|push.*hub", re.I),
  "kl": re.compile(r"\bKL\b|kl_coef|use_kl", re.I),
}

def read_loki(short):
    p = os.path.join(D, f"participant_{short}.md")
    if not os.path.exists(p): return U("no Loki record")
    txt = open(p, errors="ignore").read(); head = txt.split("\n", 3)
    m = re.search(r"lines=(\d+)\s+hit_page_cap=(\w+)", head[1] if len(head) > 1 else "")
    out = {"lines": int(m.group(1)) if m else None, "capped": (m.group(2) == "True") if m else None}
    if out["lines"] == 0: return U("Loki stream empty for this hotkey/task")
    lrs = [num(x) for x in RE["lr"].findall(txt)]; lrs = [x for x in lrs if x]
    out["lr_max"] = max(lrs) if lrs else U("no learning_rate lines")
    out["lr_first"] = lrs[0] if lrs else None
    out["log_steps"] = len(lrs)
    evs = [num(x) for x in RE["eval"].findall(txt)]
    out["evals"] = len(evs); out["eval_losses"] = evs[:12]
    ep = [num(x) for x in RE["epoch"].findall(txt)]; out["epoch_max"] = max(ep) if ep else None
    bars = RE["step_bar"].findall(txt)
    if bars:
        tot = max(int(b[1]) for b in bars); out["planned_steps"] = tot
        last = bars[-1]; out["last_step"] = int(last[0])
        # elapsed of the last bar h:m:s or m:s
        h, m_, s_ = (int(last[2]), int(last[3]), int(last[4] or 0)) if last[4] else (0, int(last[2]), int(last[3]))
        out["last_bar_elapsed_s"] = h*3600 + m_*60 + s_
    out["tracebacks"] = len(RE["tb"].findall(txt)); out["oom"] = len(RE["oom"].findall(txt))
    out["ladder_rungs"] = [x for x in RE["ladder"].findall(txt) if any(x)][:6]
    out["fallback"] = bool(RE["fallback"].search(txt))
    for k in ("batch", "ga", "epochs", "lora_r", "maxlen"):
        ms = RE[k].findall(txt)
        vals = sorted({v for tup in ms for v in (tup if isinstance(tup, tuple) else (tup,)) if v})
        out[k] = vals[:6] if vals else None
    out["kl_mentions"] = len(RE["kl"].findall(txt))
    out["finished"] = bool(RE["done"].search(txt))
    # wall time from first to last timestamped line
    ts = re.findall(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", txt)
    out["first_ts"], out["last_ts"] = (ts[0], ts[-1]) if ts else (None, None)
    return out

rows = []
for x in sorted(api.get("hotkey_details") or [], key=lambda r: (r.get("rank") or 99, r.get("test_loss") or 9)):
    hk = x.get("hotkey") or ""; short = hk[:8]
    r = {"hotkey": hk, "ours": hk == a.ours, "rank": x.get("rank"), "test_loss": x.get("test_loss"),
         "reason": x.get("score_reason"), "submitted": bool(x.get("submission_id")),
         "hf": read_hf(short), "loki": read_loki(short)}
    rows.append(r)

out = {"task_id": api.get("task_id"), "model": api.get("model_id"), "type": api.get("task_type"),
       "hours": api.get("hours_to_complete"), "status": api.get("status"), "augmented": aug, "rows": rows}
json.dump(out, open(os.path.join(D, "RECIPES.json"), "w"), indent=1)

def c(v, w=9):
    if isinstance(v, dict) and "UNAVAILABLE" in v: return "n/a".ljust(w)
    if v is None: return "-".ljust(w)
    s = f"{v:.4g}" if isinstance(v, float) else str(v)
    return s[:w].ljust(w)
print(f"# {out['task_id'][:8]} {out['model']} ({out['type']}, {out['hours']}h) — {out['status']}")
print(f"{'rk':3s} {'hotkey':9s} {'loss':9s} {'meth':5s} {'r':4s} {'alpha':5s} {'lr_max':9s} {'ep':5s} {'steps':11s} {'evals':5s} {'batch':9s} {'tb':3s} {'fb':2s} note")
for r in rows:
    if not r["submitted"] and not r["test_loss"]: continue
    h, l = r["hf"], r["loki"]
    g = lambda d, k: (d.get(k) if isinstance(d, dict) and "UNAVAILABLE" not in d else None)
    steps = f"{g(l,'last_step')}/{g(l,'planned_steps')}" if g(l, "planned_steps") else "-"
    print(f"{c(r['rank'],3)}{c(r['hotkey'][:8])} {c(r['test_loss'])} {c(g(h,'method'),5)} {c(g(h,'lora_r'),4)} {c(g(h,'lora_alpha'),5)} {c(g(l,'lr_max'))} {c(g(l,'epoch_max'),5)} {steps:11s} {c(g(l,'evals'),5)} {c(','.join(g(l,'batch') or []) if g(l,'batch') else None)} {c(g(l,'tracebacks'),3)}{'Y ' if g(l,'fallback') else '- '} {'<== OURS' if r['ours'] else ''}")
