# Rope shim A/B — dd558022 (sea-lion 8B, augmented mirror), 1xH100, 2026-09-13

One task, one arm (`b`, every feature on), one seed (42), one budget (1.25 h), two commits:
`4944667` (before `config_shim`) and `e73fc49` (with it). Base: the task's real augmented
mirror `gradients-io-tournaments/augmented-8bc5002e812b62b4` (config written by 5.12.1:
`rope_parameters{500000}`, no top-level `rope_theta`). Both arms LoRA r=128. Scored on the
validator's own 1,000-row held-out set from the auditing API.

## Scored under transformers 5.12.1 — what the validator runs

| arm | trained at theta | held-out mean CE |
|---|---|---|
| `4944667` pre-shim | 10000 (misread) | **0.9576** |
| `e73fc49` shim | 500000 (true) | **0.7989** |

mean gap **+0.1587 nats** (bootstrap lower bound +0.1328); per-example win rate **0.833**
(lower bound 0.805). Both clear the validator's dethrone bars (0.55 / 0.01) many times over.

Anchors on this exact task and test set: retained boss `5GU4Xkd3` (4.51.3, saved
`rope_theta=10000` beside `rope_parameters{500000}`) **0.8250**; challenger `5GcAxvH7`
(5.12.1) **0.7420**. The shim arm beats the boss on the task the boss lost; the pre-shim arm
is 0.13 worse than the boss.

## Scored under our pinned 4.51.3 — INVERTED, and why

| arm | local 4.51.3 scorer |
|---|---|
| pre-shim | 0.8850 |
| shim | 1.0174 |

`score_against_leaderboard.py` loaded each LoRA arm on its base through 4.51.3, i.e. at
theta 10000 — the same misread. The arm trained at 10000 was scored consistently and looked
good; the arm trained at 500000 was scored at 10000 and looked terrible. The validator does
the mirror image. The scorer now loads through `config_shim` (`ops/smoke/score_against_leaderboard.py`);
a 5.12.x venv (`/root/score512` on the box) remains the faithful reference.

## Also measured

Both arms overran their own `end_time`: −196 s (pre-shim) and −185 s (shim) at
`restore_submission_architectures`. With the validator's ~173 s grace past end_time, a
1.25 h task of this shape would be killed 10–20 s before its post-training finished.

Files: `v512_*.json` (5.12.1 per-example vectors), `b_rope-*.json` (4.51.3 vectors),
`logs/ab_b_rope-*.out` (full run logs; `[config-shim]` present only in the shim arm),
`gate_e73fc49.out` + stage logs (49/49).
