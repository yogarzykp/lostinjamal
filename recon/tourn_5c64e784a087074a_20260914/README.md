# tourn_5c64e784a087074a_20260914 — FINAL 2026-09-19

Our hotkey `5HBgDWKxNX3333Yit3qMokkYY4Guz1r8Qfons2UJTSU5oqjV`, commit `8f1bc00d` (validator-align).

**9th of 16 by mean per-task rank** (advance line: top 2). Winner `5GU4Xkd3dCGT` dethroned the
three-tournament boss `5H9AM1bG`.

| task | model | ours | note |
|---|---|---|---|
| 067761fe | Llama-3.2-1B-Instruct | **9**/16, 1.1402 | three LR probes (~600s of 1h) lost to the incumbent; final 1.1474 → absorbed 1.1217 |
| 87c51c39 | Qwen2.5-0.5B-Instruct | **4**/16, 1.2787 | 0.0085 nats off #1 — best real placing to date |
| 90d361cb | LFM2.5-2.6B | **15**/15, 0.7458 | unloadable on 4.51.3 → base copy in 3.9s; 11 of 17 trained it |

Files: `snap_*.json` first/last state · `task_*.json` records · `configs/` every model seen
(slot 2 cycled seven models in ~80 min) · `loki_*_ours.json` our three runs (progress bars
stripped) · `OFFICIAL_diff_report.md` archived before its 7-day link expiry · `final_state.json`.
`snapshot.py` is the OODA observer (re-derives the task list each tick; diffs model-per-id too).
