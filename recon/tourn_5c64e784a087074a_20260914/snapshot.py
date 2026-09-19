#!/usr/bin/env python3
"""One OODA observation of a live tournament: page state + every task record, diffed against the
previous snapshot. Derives the task list from the tournament EACH time (a hardcoded watch list hid a
withdrawn task and its replacement in tourn_2ba0f7); diffs both arrivals and withdrawals.

  python3 snapshot.py <tourn_id> <our_hotkey> [out_dir]
Writes <out_dir>/snap_<UTC>.json and prints a compact human diff. Exit 0 always (a monitor must not die).
"""
import json, os, sys, glob, datetime, urllib.request, subprocess

TOURN, OURS = sys.argv[1], sys.argv[2]
OUT = sys.argv[3] if len(sys.argv) > 3 else os.path.dirname(os.path.abspath(__file__))
RECON = "/Users/m1/Documents/project-badut/skills/recon/scripts/recon.py"
API = "https://api.gradients.io/auditing/tasks/"
UA = {"User-Agent": "curl/8.0"}   # the API 403s python's default UA
now = datetime.datetime.now(datetime.timezone.utc)
stamp = now.strftime("%Y%m%dT%H%M%SZ")

def get_json(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
            return json.load(r)
    except Exception as e:
        return {"_error": f"{type(e).__name__}: {str(e)[:120]}"}

# --- page state (participants, task ids, winner) via the plugin's recon.py
try:
    page = json.loads(subprocess.run([sys.executable, RECON, "tournament", TOURN],
                                     capture_output=True, text=True, timeout=120).stdout)
except Exception as e:
    page = {"_error": f"page: {type(e).__name__}: {str(e)[:120]}"}
task_ids = (page.get("tasks") or {}).get("task_ids") or []
field = (page.get("participants") or {}).get("hotkeys") or []

# --- every task record, from the auditing API
tasks = {}
for t in task_ids:
    d = get_json(API + t)
    hd = d.get("hotkey_details") or []
    mine = next((x for x in hd if x.get("hotkey") == OURS), None)
    scored = [x for x in hd if x.get("submission_id") or (x.get("test_loss") or 0) != 0]
    tasks[t] = {
        "model": d.get("model_id"), "type": d.get("task_type"), "status": d.get("status"),
        "hours": d.get("hours_to_complete"), "created": d.get("created_at"), "termination": d.get("termination_at"),
        "delays": d.get("times_delayed"), "rows": len(hd),
        "ours": {k: mine.get(k) for k in ("submission_id", "test_loss", "quality_score", "rank", "score_reason", "repo")} if mine else None,
        "scored": sorted([{"hk": x["hotkey"][:12], "loss": round(x.get("test_loss") or 0, 5), "rank": x.get("rank"),
                           "reason": (x.get("score_reason") or "")[:80]} for x in scored], key=lambda r: (r["rank"] or 99, r["loss"])),
        "_error": d.get("_error"),
    }

snap = {"tourn": TOURN, "at": now.isoformat(), "status": page.get("status"),
        "winner": page.get("winner_hotkey"), "base_winner": page.get("base_winner_hotkey"),
        "field": field, "task_ids": task_ids, "tasks": tasks, "page_error": page.get("_error")}

# --- diff against the previous snapshot
prev_files = sorted(glob.glob(os.path.join(OUT, "snap_*.json")))
prev = json.load(open(prev_files[-1])) if prev_files else None
with open(os.path.join(OUT, f"snap_{stamp}.json"), "w") as fh:
    json.dump(snap, fh, indent=1)

def say(s): print(s, flush=True)
say(f"[{stamp}] {TOURN} status={snap['status']} field={len(field)} tasks={len(task_ids)} ours_in_field={OURS in field}")
if snap.get("page_error"): say(f"  PAGE ERROR: {snap['page_error']}")
if prev:
    old, new = set(prev["task_ids"]), set(task_ids)
    for t in sorted(new - old): say(f"  + NEW TASK {t[:8]} {tasks[t]['model']} {tasks[t]['type']} {tasks[t]['hours']}h status={tasks[t]['status']}")
    for t in sorted(old - new): say(f"  - WITHDRAWN {t[:8]} (was {prev['tasks'].get(t, {}).get('model')})")
    if prev["status"] != snap["status"]: say(f"  ! tournament status {prev['status']} -> {snap['status']}")
    if set(prev["field"]) != set(field): say(f"  ! field changed: {len(prev['field'])} -> {len(field)}")
for t in task_ids:
    x = tasks[t]; p = (prev or {}).get("tasks", {}).get(t) if prev else None
    flag = ""
    if p and p.get("model") != x.get("model"): flag += f"  MODEL SWAPPED IN PLACE {p.get('model')} -> {x.get('model')}"
    if p and p["status"] != x["status"]: flag += f"  status {p['status']}->{x['status']}"
    if p and len(p["scored"]) != len(x["scored"]): flag += f"  scored {len(p['scored'])}->{len(x['scored'])}"
    if p and (p.get("ours") or {}).get("test_loss") != (x.get("ours") or {}).get("test_loss"): flag += "  OUR SCORE CHANGED"
    if x.get("_error"): flag += f"  API ERROR {x['_error']}"
    o = x.get("ours") or {}
    say(f"  {t[:8]} {str(x['model']):32s} {str(x['status']):22s} scored={len(x['scored']):2d}/{x['rows']}  ours: loss={o.get('test_loss')} rank={o.get('rank')} reason={o.get('score_reason')}{flag}")
    for r in x["scored"][:6]: say(f"      #{r['rank']} {r['hk']} loss={r['loss']} {('['+r['reason']+']') if r['reason'] else ''}")
