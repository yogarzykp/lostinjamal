# Gate 8f1bc00 — 2026-09-14, 1xH100 PCIe 80 GiB, task dd558022 (new default)

Two runs on the same commit, fresh container + `redis-cli flushall` each:
`gate_dpo.out` (DPO stage alone, 12:07–12:12) and `gate_full2.out` (all five, 12:13–13:11).
Both **ALL GATES PASSED**; the full run 49/49. Logs have the progress bars stripped.

| stage | batch | vs end_time | `[vram]` peak alloc | evals | tracebacks |
|---|---|---|---|---|---|
| instruct | 16 | +83s | 15.49 GiB | 0 | 0 |
| kl | 4 | +150s | 32.55 GiB | 1 | 0 |
| **dpo** | **24** | **+444s** | **58.21 GiB** | 1 | **0** |
| grpo | 40 | +159s | 25.42 GiB | 0 | 0 |
| chat | 70 | +612s | 4.04 GiB | 2 | 0 |

No OOM, no noise fallback, anywhere.

## What this run proves

* **DPO** (`8f1bc00`): the measured-peak ceiling planned 35→24 and the ladder never engaged.
  Predicted peak 58.3 GiB, measured **58.21**. Previously 70 → OOM → 35 → OOM → 17, +388s.
* **The `[vram]` line fires on all five stages**, including GRPO — so the subclass does reach
  the parent's `on_train_end`. This is the first time the repo has a *floor* for every stage,
  not only the OOM ceilings the batch buckets were fitted to.
* **The cost envelope (`2fc2028`) still brackets every measured cycle** on this commit.

## What the `[vram]` floors say, for later

instruct at batch 16 used **15.5 of 79 GiB**. That is headroom the planner is not spending. Not
a defect — throughput is a separate question from correctness — but it is the first number
that could size it honestly.
