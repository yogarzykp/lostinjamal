#!/usr/bin/env python3
"""Drive the project-badut recon script over every task and hotkey of one tournament.

  python3 ops/recon_sweep.py <tourn_id> [--plugin DIR] [--only-tasks id8,id8] [--days N]

Follows the plugin's own layout (skills/recon/SKILL.md "Where it goes") and its HARD-GATE:
UNAVAILABLE is written down with a reason, never guessed; signed dataset links are stripped;
MANIFEST.json makes the sweep resumable — a re-run skips what completed and retries only what
failed. Mechanics stay in the plugin's recon.py; this file only loops.
"""
import argparse, json, os, re, subprocess, sys, time, datetime

ap = argparse.ArgumentParser()
ap.add_argument("tourn_id")
ap.add_argument("--plugin", default="/Users/m1/.claude/plugins/cache/project-badut/project-badut/0.12.0")
ap.add_argument("--only-tasks", default="")
ap.add_argument("--days", type=int, default=14)
ap.add_argument("--out", default=None)
a = ap.parse_args()

RECON = os.path.join(a.plugin, "skills", "recon", "scripts", "recon.py")
OUT = a.out or os.path.join("recon", a.tourn_id)
os.makedirs(OUT, exist_ok=True)
MAN = os.path.join(OUT, "MANIFEST.json")
manifest = json.load(open(MAN)) if os.path.exists(MAN) else {"tourn_id": a.tourn_id, "entries": {}}
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")

def run(*args, timeout=300):
    """One recon.py call -> (parsed json or None, error string or None)."""
    try:
        p = subprocess.run([sys.executable, RECON, *args], capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, f"timeout after {timeout}s"
    if p.returncode != 0 and not p.stdout.strip():
        return None, (p.stderr or "non-zero exit").strip()[:300]
    try:
        return json.loads(p.stdout), None
    except Exception as e:
        return None, f"not json: {type(e).__name__}: {p.stdout[:120]!r}"

def done(key): return manifest["entries"].get(key, {}).get("status") == "ok"
def mark(key, status, **extra):
    manifest["entries"][key] = {"status": status, "at": now(), **extra}
    json.dump(manifest, open(MAN, "w"), indent=1)

def log(s): print(f"[{now()[11:19]}] {s}", flush=True)

# --- 1. the tournament page --------------------------------------------------------------
page, err = run("tournament", a.tourn_id, "--diff-report")
if page is None:
    log(f"tournament page UNAVAILABLE: {err}"); sys.exit(2)
dr = page.get("diff_report") or {}
if isinstance(dr, dict) and dr.get("body"):
    open(os.path.join(OUT, "OFFICIAL_diff_report.md"), "w").write(dr["body"])
    dr = {k: v for k, v in dr.items() if k != "body"}
page["diff_report"] = dr
json.dump(page, open(os.path.join(OUT, "tournament.json"), "w"), indent=1)
task_ids = (page.get("tasks") or {}).get("task_ids") or []
field = (page.get("participants") or {}).get("hotkeys") or []
only = {t for t in a.only_tasks.split(",") if t}
if only: task_ids = [t for t in task_ids if any(t.startswith(o) for o in only)]
log(f"{a.tourn_id}: status={page.get('status')} field={len(field)} tasks={len(task_ids)}")

SIGNED = ("training_data", "test_data", "synthetic_data")
for t in task_ids:
    td = os.path.join(OUT, t); os.makedirs(td, exist_ok=True)
    # --- 2. task record, signed links stripped
    key = f"{t}/api"
    if not done(key):
        d, err = run("task", t)
        if d is None: mark(key, "UNAVAILABLE", reason=err); log(f"{t[:8]} api UNAVAILABLE: {err}"); continue
        for k in SIGNED:
            if d.get(k): d[k] = "STRIPPED (presigned)"
        json.dump(d, open(os.path.join(td, "api.json"), "w"), indent=1); mark(key, "ok")
    api = json.load(open(os.path.join(td, "api.json")))
    if api.get("status") != "success":
        log(f"{t[:8]} status={api.get('status')} — nothing to collect yet"); continue
    rows = [x for x in (api.get("hotkey_details") or []) if x.get("hotkey")]
    scored = [x for x in rows if x.get("submission_id") or (x.get("test_loss") or 0)]
    log(f"{t[:8]} {api.get('model_id')} rows={len(rows)} scored={len(scored)}")
    # --- 3. augmentation, off the repo names (free)
    key = f"{t}/augmented"
    if not done(key):
        repos = [x["repo"] for x in scored if x.get("repo")]
        d, err = run("augmented", t, *repos)
        if d is None: mark(key, "UNAVAILABLE", reason=err)
        else: json.dump(d, open(os.path.join(td, "augmented.json"), "w"), indent=1); mark(key, "ok")
    # --- 4. W&B discovery once per task
    key = f"{t}/wandb-find"
    wf = None
    if not done(key):
        wf, err = run("wandb-find", t)
        if wf is None: mark(key, "UNAVAILABLE", reason=err)
        else: json.dump(wf, open(os.path.join(td, "wandb_find.json"), "w"), indent=1); mark(key, "ok")
    else:
        try: wf = json.load(open(os.path.join(td, "wandb_find.json")))
        except Exception: wf = None
    # --- 5. per participant: loki, hf, wandb
    for x in rows:
        hk = x["hotkey"]; short = hk[:8]
        key = f"{t}/loki/{hk}"
        if not done(key):
            d, err = run("loki", t, hk, "--days", str(a.days), "--full", timeout=600)
            if d is None: mark(key, "UNAVAILABLE", reason=err)
            else:
                lines = d.get("lines") or []
                body = [f"# Loki — task {t} — hotkey {hk}", f"fetched {now()}  lines={len(lines)}  hit_page_cap={d.get('hit_page_cap')}  containers={d.get('containers')}", ""]
                for r in lines:
                    l = r.get("line", "")
                    if "it/s]" in l or "%|" in l: continue     # progress bars carry nothing
                    body.append(f"[{r.get('container','')[:12]}] {l}")
                open(os.path.join(td, f"participant_{short}.md"), "w").write("\n".join(body))
                mark(key, "ok" if lines else "EMPTY", lines=len(lines), cap=bool(d.get("hit_page_cap")))
        key = f"{t}/hf/{hk}"
        if not done(key) and x.get("repo"):
            d, err = run("hf", x["repo"])
            if d is None: mark(key, "UNAVAILABLE", reason=err)
            else: json.dump(d, open(os.path.join(td, f"hf_{short}.json"), "w"), indent=1); mark(key, "ok")
        elif not x.get("repo"): mark(key, "NO_REPO")
        # wandb runs discovered for this task that name this hotkey
        key = f"{t}/wandb/{hk}"
        if not done(key) and wf:
            _runs = wf.get("runs")
            if isinstance(_runs, dict) and _runs.get("status") == "UNAVAILABLE":
                mark(key, "UNAVAILABLE", reason=_runs.get("reason", "")[:160]); continue
            runs = [r for r in (_runs or []) if isinstance(r, dict) and hk[:10] in json.dumps(r)]
            if not runs: mark(key, "NO_RUN")
            else:
                name = runs[0].get("name") or runs[0].get("run_name") or runs[0].get("id")
                d, err = run("wandb", str(name), "--history", timeout=300)
                if d is None: mark(key, "UNAVAILABLE", reason=err)
                else: json.dump(d, open(os.path.join(td, f"WANDB_{short}.json"), "w"), indent=1); mark(key, "ok")
    log(f"{t[:8]} done")
log("sweep complete")
