# DECISION LEDGER — lostinjamal vs retained boss 5GU4Xkd3 (tourn 2ba0f79237bffcf7, 20260907)

**Verdict in one line:** we did not lose on method. We lost ~9% of a scored wall clock and one checkpoint promotion to instrumentation that our own source comments say nothing reads, then trained a cosine schedule against 61% of the steps it was drawn for. Our ML pins are byte-identical to the champion's; after deleting two dependencies we did not need, `training_requirements.txt` becomes byte-identical. The 1.8x size is real, but the loss is concentrated in about six lines of statement ordering and two dead wires.

**HARD CLOCK: `recon/.../task_59469903.json` → `dataset_url_expires_at = 2026-09-14T11:10:27Z`.** Today is 2026-09-11. The replay dataset for the only task we hold a full trace for dies in **3 days**. Everything in §5 is gated on that. (Memory's "datasets expire 2026-08-31" note is the *previous* tournament's; this one is still open, barely.)

---

## §0 — CORRECTIONS MADE THIS SESSION (use these, not the ledger's originals)

Six ledger entries changed under verification. All are `MEASURED` from `recon/tourn_2ba0f79237bffcf7_20260907/loki_59469903.txt` and the boss checkout.

| # | Ledger said | Corrected to |
|---|---|---|
| C1 | train-instruct: eval cadence is "highest value-per-line in this subsystem" | **Downgraded.** Boss cadence is `max_evals = max(3, int(hours*4))`, `eval_steps = total // min(10, max_evals)` (BOSS `train_instruct.py:442-443`). The run log says `budget=1.75h`; the auditing record says `hours_to_complete=0.75`. So the boss gets **3 to 7** checkpoint candidates on this task, not 10. We got 2. Real but smaller than claimed — and the discrepancy between 1.75h and 0.75h is itself an open item that sizes this defect. |
| C2 | customized-trainer: telemetry "cost 349.7s and made us ship step 500" | **Upgraded to a closed causal chain, visible in the log.** `GO INTO CUSTOMIZED EVALUATE AT STEP: 500` and `...: 544` both fire; `Updating the best checkpoint info at step: 500` fires **once and only once**. Step 544 evaluated at a better loss and was never promoted. The promotion at `customized_trainer.py:769` never ran for 544 because the process was killed inside the telemetry block at `:729-760`. |
| C3 | dpo-grpo + text-trainer: "porting quiet_mode may break OOM-retry detection — verify first" | **RESOLVED, no risk.** `text_trainer.py:309-317` `get_error_type(log_path)` reads the **log file**, and `run_cmd_with_log` writes it at `:70` (`log_file.write(line)`) independently of the `print(line)` at `:69`. A print shim cannot break OOM detection. What it *does* break is console/Loki visibility of child errors — which is exactly why the boss changed print→`sys.stdout.write` (BOSS `text_trainer.py:70-78`, comment says so verbatim). Port both together. |
| C4 | deps: "whether 59469903 carried USE_KL — I did not open the task json" | **Unresolvable from what we hold, and separately answered.** The json carries its own `kl_note`: *"use_kl and kl_coef are always False/None here even for KL tasks — the config is not persisted once a task finishes."* But the run log contains **zero** `eval_kl` / `USE_KL` / `kl_coef` hits. So the KL grad-accum defect (D8) was **not live on 59469903**. It is a boss-round trap, not a round-1 cost. |
| C5 | config-hp: "epoch_num 2 vs 3 — refuted as live delta" | **Confirmed refuted, with the number.** `[CONFIG-RESOLVED] ... steps_or_epochs=3`. Adaptive ran 3 epochs, matching the boss. Stop spending time here. |
| C6 | lr-subsystem: "the ladder only exists on tasks longer than ~1.3h, and round 1 doesn't give us those" | **Confirmed and worse.** The log shows `attempt 1/5` and `attempt 2/5` with `total_steps_per_epoch: 361` then `722` — the ladder *did* relaunch, at a different batch, and consumed budget on a task that then ran out of it (`budget reached; handing back so the post-training checks can run`). It cost a restart and returned no LR decision. |

Also confirmed unchanged: `NOISE_STD = 0.01` is identical on both sides (ours `add_random_noise.py:35`/`:136`, boss `:17`/`:23`) — a shared problem, not a divergence. And `max_steps: -1` with `max_steps_budget=666` computed and never applied — the memory item "step cap wire dead" is confirmed live in this tournament.

---

## §1 — THE DEFECTS (our code is measurably wrong), ranked by cost

**Tier A — measured cost on the tournament we lost.**

### D1. Per-example telemetry runs before the promotion it preempts — and nothing reads what it writes
- **Ours:** `scripts/customized_trainer.py:698-713` (`record_outcome`), `:729-760` (per-example forward pass), both executing before the promotion at `:769-793`. Guard at `:692`. Pass itself at `scripts/per_example_eval.py:89-122`, wired at `scripts/train_instruct.py:670-681`. The sink says so in its own source: `scripts/telemetry.py:72-73` — *"not used in training"*. Repo-wide grep for `run_telemetry`: only `telemetry.py` and four `ops/smoke/*.sh` lines that export the path.
- **Boss:** `BOSS/scripts/customized_trainer.py:249-267` — `save_only` reset, `compute_loss` dict lookup, two guards, then **PROMOTE**. Nothing between the metric and the promotion. No telemetry module anywhere in the boss tree.
- **Cost — MEASURED:** shipped step 500 (`0.0527852`) instead of step 544 (`0.0517329`) = **0.0010523 nats**, which is **14.6% of our entire 0.0072 gap to rank 1 on gemma**. Plus 349.7s ≈ **40 training steps** at the log's measured `step_time_est=8.7s`, out of a 666-step budget. The log proves the mechanism: step 544 evaluated, step 544 never promoted.
- **Fix (one statement move):** relocate the promotion block `:769-793` to immediately after the `None` guard at `:692`, ahead of every telemetry block — the boss's exact order. Then default `EMIT_PER_EXAMPLE_LOSSES` to `0` at `per_example_eval.py:60` and remove the wiring at `train_instruct.py:670-683`.
- **Why rank 1:** it is the only defect with a nats figure attached to a real ranked task, the fix is a reorder rather than a mechanism, and the block it protects has a documented consumer count of zero.

### D2. Time-aware epoch planning absent — we trained 61% of the schedule we drew
- **Ours:** `scripts/adaptive_config.py:2177` (`"epoch_num": epochs`) and the **proven absence** of any `training_args.num_train_epochs` reassignment in `scripts/train_instruct.py` (grep returns only comments and read-only uses at `:402`, `:502`).
- **Boss:** `BOSS/scripts/train_instruct.py:726-801` — recomputes `optimal_epochs` from measured `t_per_step`, reassigns `num_train_epochs` at `:797` and `warmup_steps` at `:798`, broadcast across ranks.
- **Cost — MEASURED from the log:** `total_steps=1083` planned (3 × 361), `max_steps_budget=666` affordable at the measured `8.7s/step`, `max_steps: -1` so nothing truncated or re-fitted it. We traverse 61% of a cosine drawn for 1083 steps, ending at roughly **43% of peak LR instead of the 15% floor** `min_lr_rate` promises. Every instruct task we run has this shape.
- **Fix:** port BOSS `train_instruct.py:726-801` plus the 3%-warmup clamp at `:433-435`. It needs a real `t_per_step` — and the log proves we already measure one (`step_time_est=8.7s (measured)`), so this does **not** require the full LR-search port.
- **Do not** substitute `EXPT_MAX_STEPS` for it: capping `max_steps` truncates the plan, it does not re-fit the schedule to the budget. That distinction is the whole defect.

### D3. The multi-launch ladder relaunched on a task too short to use it
- **Ours:** `scripts/text_trainer.py:1127-1310` (`while True`), ladder build `:1160-1194`, `MAX_LOOP_RUNS=8` at `:756`; time gate at `scripts/customized_trainer.py:493` (*"Time is not enough so we will finish the training"*).
- **Boss:** `BOSS/scripts/text_trainer.py:487-489` — *"Single training run — no multi-restart LR search"*; one `run_output_dir`, one `set_state`, one `run_training` call at `:500-524`.
- **Cost — MEASURED:** `attempt 1/5` then `attempt 2/5`, with `total_steps_per_epoch` changing 361→722 between them. A relaunch was paid for, the time gate then refused to use the ladder's output, and the second attempt ran out of budget mid-schedule. Both official diff reports named the LR ladder.
- **Fix:** collapse to a single launch (§3 R1 for the full argument). This is listed as a DEFECT rather than only a RISK because on *this* task it demonstrably consumed budget and returned no decision.

**Tier B — structural, every run, cost not yet quantified.**

### D4. Eval/save cadence is never switched on — 2 candidates where the boss gets 3-7
- **Ours:** `scripts/instruct_config.py:227` `--eval_strategy no`, `:228` `--save_strategy epoch`; **zero** `training_args.eval_strategy` / `save_strategy` assignments anywhere in `scripts/` (verified by grep, no hits).
- **Boss:** identical template (`BOSS/scripts/instruct_config.py:160-161`) — the difference is entirely in `BOSS/scripts/train_instruct.py:441-449`, which flips both to `"steps"` at `adaptive_eval_steps` under an `is_final_run` gate.
- **Cost:** log shows exactly two evals (`eval_runtime: 109.1995`, `110.1556`). Boss would get 3 (at 0.75h) to 7 (at 1.75h). Our eval and save are also driven by *different* mechanisms, which is how step 500 and step 544 ended up as an unmatched pair in the first place.
- **Fix:** port BOSS `train_instruct.py:441-449` verbatim — 12 lines, uses only `hours_to_complete` and `total_steps_all_epochs`, which we already compute at `train_instruct.py:502`.
- **Ship it with M3 (§2), not alone.** Our dev set is unpacked at ~110s/eval; going from 2 evals to 7 without the boss's eval-cost governors adds ~550s to a 6300s budget.

### D5. `use_liger` hardcoded `False` — the root of the whole config cascade
- **Ours:** `scripts/adaptive_config.py:2181` — `"use_liger": False,  # arch-dependent, conservative default`.
- **Boss:** `BOSS/scripts/instruct_config.py:209` — `get_use_liger(model_architecture)`; helper at `BOSS/scripts/model_utility.py:40-53`.
- **Cost — INFERRED but mechanically tight:** no fused CE → full `[B,T,V]` logits materialised → on gemma-2-2b `V=256000` that is the memory pressure the vocab-aware batch cap exists to relieve → `batch=8` in the log, down from a bucket of 60. One "conservative default" produces a 7.5x batch reduction on our worst measured task.
- **Fix:** restore `get_use_liger(model_architecture)` at `:2181`, then re-measure whether R2's cap needs to fire at all.

### D6. `gradient_accumulation` capped at `min(4, ...)` — halves the effective batch exactly where it was already starved
- **Ours:** `scripts/adaptive_config.py:2059` — `grad_accum = min(4, max(1, 64 // total_batch))`.
- **Boss:** `BOSS/scripts/instruct_config.py:269-273` — same rule, no cap.
- **Cost:** with the log's `batch=8` and 1 GPU, `64 // 8 = 8`, capped to 4 → effective batch **32 instead of 64**. Compounds D5 multiplicatively.
- **Fix:** drop `min(4, ...)` for instruct. Keep it for DPO/GRPO where the boss also caps.

### D7. FlashAttention decided by a 6-family allow-list instead of the boss's deny-list
- **Ours:** `scripts/adaptive_config.py:2183-2186` — `"False" if arch_supports_fa(arch) else "True"`; family list at `scripts/dynamics_utils.py:40,75-77`.
- **Boss:** `BOSS/scripts/model_utility.py:127-137`, wired at `BOSS/scripts/instruct_config.py:212` — default on, deny known-bad.
- **Cost:** any architecture outside our six silently trains without FA. The log carries `attempting to use Flash Attention 2.0 with a model not in...`. Worse, it is half of R8: our `PackedDataset` has no `use_fa` flag, so packing stays on when FA falls off.
- **Fix:** invert the polarity — keep our anonymisation-resistant arch detection (that part is better than the boss's), deny only the known-bad set.

**Tier C — cheap correctness, forfeit-class blast radius, not live in round 1.**

### D8. `dev_absorption` leaves a stale `model.safetensors.index.json` in the staged submission
- **Ours:** `scripts/dev_absorption.py:79-80` — `return name.endswith(".safetensors") or name.endswith(".bin")`, used at `:265` to decide what to clear from staging.
- **Boss:** `BOSS/scripts/dev_pass.py:154-157` — `_is_weight_file` includes the literal `name == "model.safetensors.index.json"`.
- **Cost:** on any model large enough to shard, the index points at pre-absorption shards. Best case a load failure, worst case silently the wrong weights. Did not bite on gemma-2-2b or SmolLM2-360M; the boss round guarantees 35-71B.
- **Fix — literally one clause:** `or name == "model.safetensors.index.json"`. **Do this first. It costs 30 seconds and it is the only forfeit-class one-liner in the diff.**

### D9. KL term is not divided by gradient-accumulation steps
- **Ours:** `scripts/kl_trainer_mixin.py:50-56` — `__init__` never touches `model_accepts_loss_kwargs`; `:77`/`:100` add `super()` CE and a mean KL.
- **Boss:** `BOSS/scripts/kl_trainer.py:94-103` — `self.model_accepts_loss_kwargs = False`, with the reasoning written out.
- **Cost:** with `grad_accum=4` the KL term carries ~4x its intended weight relative to CE. **Corrected (C4): not live on 59469903** — no `eval_kl` or `USE_KL` in the log. This is a boss-round trap.
- **Fix:** set `model_accepts_loss_kwargs = False` in the mixin's `__init__`, exactly as the boss does. Add a test that accumulates N micro-batches and asserts the summed gradient matches the single-batch equivalent — `tests/test_kl_validator_parity.py` pins the formula but cannot see the scaling.

### D10. GRPO trains at `beta=0.04` against a validator that scores at `0.5`
- **Ours:** `scripts/grpo_config.py:296` — `"beta": 0.04,  # legacy TRL default`; `scripts/adaptive_config.py:2337` (`ADAPTIVE_BETA_OVERRIDE` default 0.04); `scripts/train_grpo.py:72` a dead module constant `BETA_GRPO = 0.04` **carrying the validator's own name with the wrong value**.
- **Boss:** `BOSS/scripts/grpo_config.py:281` — `"beta": 0.5`; `BOSS/scripts/customized_trainer.py:351` — `VALIDATOR_BETA_GRPO = 0.5`.
- **Cost:** the scored metric is `reward − 0.5·KL`. We optimise a KL weight 12.5x weaker than the one we are graded on. Not live in round 1 (three instruct tasks); the boss round spans all four types.
- **Fix:** `0.5` in both `grpo_config.py:296` and `adaptive_config.py:2337`; strip `reward_classifier`'s beta authority entirely (R7); delete or rename `train_grpo.py:72`.

### D11. ZeRO-3 + gradient checkpointing forced together on DPO/GRPO
- **Ours:** `scripts/adaptive_config.py:2203-2204` — emits `distributed="ds"` above 9e9 params on >1 GPU **and** `gradient_checkpointing="True"`.
- **Boss:** `BOSS/scripts/dpo_config.py:46,54,62,70,78` — `gradient_checkpointing` **False on every `ds` bucket**; `BOSS/scripts/grpo_config.py:13-105` — **no bucket selects `ds` at any size**.
- **Cost:** forfeit-class on the boss round's guaranteed 35-71B task. Our HEAD fix (4723787, `use_reentrant=bool(zero3)`) is **unpushed and has never been gate-tested**, and no multi-GPU DPO/GRPO run has ever executed on this repo.
- **Fix:** adopt the boss's shape, not just our flag patch — `adaptive_config.py:2204` must emit `gradient_checkpointing=False` whenever it emits `distributed="ds"`, and stop routing GRPO to `ds` at all until a multi-GPU GRPO run has actually run.

### D12. Disconnected wires on the DPO/GRPO templates (one fix session, four wires)
- `--warmup_steps 35` hardcoded at `scripts/dpo_config.py:163` and `scripts/grpo_config.py:218`, while `adaptive_config.py:2206` computes a value that never arrives. Boss uses `{warmup_steps}` at `BOSS/scripts/dpo_config.py:162`, `grpo_config.py:213`. `scripts/instruct_config.py:234` proves the placeholder form exists in our own repo.
- DPO `max_length` / `max_prompt_length` deleted from the template (`scripts/dpo_config.py:150-170`); boss passes both at `BOSS/scripts/dpo_config.py:163-165`. Our planner's value reaches nothing.
- DPO batch not scaled when `max_length` rises (`scripts/dpo_config.py:197`); boss scales at `BOSS/scripts/dpo_config.py:236-241`.
- KL objective reachable only if `adaptive_config` succeeds (`scripts/train_instruct.py:560` reads `train_request`; the only writer is `adaptive_config.py:2794`; the fallback at `text_trainer.py:991-1014` drops it). Boss reads `os.environ` directly in the trainer at `BOSS/scripts/train_instruct.py:210-221`.
- **This is our named bug class** ("correct code nothing calls on one path"). Before the next submission, grep every template for a literal sitting where a placeholder belongs.

### D13. `tokenize_dpo` warns about identical chosen/rejected pairs instead of removing them
- **Ours:** `scripts/tokenize_dpo.py:122-141` — samples 10 rows and prints.
- **Boss:** `BOSS/scripts/tokenize_dpo.py:122-127` — `dataset.filter(lambda ex: ex[chosen] != ex[rejected])` with a removal count logged.
- **Fix:** two lines, zero interaction with anything else. Identical pairs contribute a zero-gradient term to a preference objective.

### D14. `state["train"]` dereferenced unguarded
- **Ours:** `scripts/train_instruct.py:472-473`. **Boss:** guarded at `BOSS/scripts/train_instruct.py:417-420`.
- Only reachable because our state channel can return empty (R3). Two-line fix; do it with R3.

### D15. `DEV_ABSORPTION` comment says "Default OFF", code says on
- **Ours:** `scripts/text_trainer.py:1345` (*"Default OFF."*) against `:1350` `os.getenv("DEV_ABSORPTION", "1") == "1"`. Identical at the commit that ran (`git show 12b16b5:scripts/text_trainer.py:1351`). **Verified this session.**
- The one mechanism we believe is gated is armed, unmeasured on our harness, inside a post-training window already measured overrunning `end_time` by 29s. Boss's equivalent gate is structural, not env-driven (`BOSS/scripts/train_instruct.py:874`).
- **Fix:** fix the comment (it is armed), then replace the env flag with the boss's structural gate.

### D16. Architecture patch runs once post-training instead of at every checkpoint copy
- **Ours:** `scripts/text_trainer.py:1402` is the sole call; `scripts/customized_trainer.py:583-590` *documents the hazard* and `:917-952` copies without patching.
- **Boss:** `BOSS/scripts/customized_trainer.py:78-96` called at `:319` and `:344`; `BOSS/scripts/text_trainer.py:552-555` explicitly labels the post-training call *"Final safety net … the primary patch runs on every checkpoint copy"*.
- **On 59469903 our single call never executed** — `run_training()` never returned. Port the callback-time patch; keep `:1402` as the net it was always supposed to be.

### D17. GRPO never evaluates — checkpoints selected on a training-log proxy
- **Ours:** `scripts/customized_trainer.py:1314` (`_grpo_no_eval=True`), `:550-562`, selection on `_h3_last_proxy` at `:901-916`.
- **Boss:** `BOSS/scripts/customized_trainer.py:354-394` — reads `eval_reward` and `eval_kl`, returns `-(reward - 0.5*kl)`; `on_step_end:210-229` sets `should_evaluate` for GRPO exactly as for instruct. **Both repos pin `trl==0.18.0`.**
- The claimed TRL 1199 reshape crash is therefore not a version difference. Reproduce it before keeping the workaround; if real, it is a `batch/num_generations` divisibility problem in *our* eval config.

---

## §2 — THE MISSING (boss has a capability we lack), ranked by likely value

### M1. Dev reclaim in the right place, with a computed time reserve — HIGHEST VALUE
- **Boss:** `BOSS/scripts/train_instruct.py:874-899` (the pass, after `trainer.train()` at `:847`, before `success.txt` at `:908-911`), budgeted at `:813-830` (`save_before_remaining_time = base + _extra_min`, sized from measured `_dev_pass_secs`), with a window re-check at `:862-873` that skips cleanly if the remaining window is smaller than the estimate.
- **Ours:** the mechanism exists (`scripts/dev_absorption.py`) but sits **outside the killable path** at `scripts/text_trainer.py:1350-1388`, behind a **hardcoded 3-minute** reserve set at `instruct_config.py:425` / `adaptive_config.py:2728` / `dpo_config.py:249` and raised by nothing (grep confirms three sites, zero adjusters).
- **Value — our own two measurements:** −0.0194 nats on one task, −0.0052 on 3a6658eb. The gemma gap was 0.0072. Either measurement is decisive at that scale.
- **It produced nothing on 59469903 because `run_training()` never returned.** The capability is not missing; the *placement* is.
- **Resolution of the three-way conflict (see §7 K-1):** port the boss's **placement and budgeting**, keep **our rate (r=0.1, twice measured)** and **our hotness guard** (`dev_absorption.py:83-122`, `:248-256` — the boss's `dev_pass.py` has no loss comparison at all). Do **not** port `dev_pass.py` wholesale; its DDP machinery buys nothing at our seam.

### M2. The two eval-cost governors — ship with D4, not after it
- **Boss:** `BOSS/scripts/customized_trainer.py:231-245` (skip evals before 0.75 epochs, never on `reason=='end_time'`) and `:272-295` (measure `eval_runtime`, derive `max_evals` from a 10% budget, widen `eval_steps`/`save_steps`).
- **Ours:** absent — grep for `_eval_timing_adjusted` and `0.75` over `customized_trainer.py` returns nothing; `on_step_end` ends at `:630`, `on_evaluate` at `:877`, neither measures runtime.
- **Value:** our measured `eval_runtime` is **109-110s**. `:272-295` is the block that bounds exactly the cost D1 added, and it is the precondition that makes D4 safe. Self-contained, read-only against the rest of our callback.

### M3. The boss's in-process LR search (`run_lr_search`) — largest structural gap
- **Boss:** `BOSS/scripts/lr_search.py:498` (`run_lr_search`), `:209` (`plan_budget`), `:282` (`select_edge_lr`), `:330` (`_run_trial`), `:921-974` (S1/S2/S3); wired at `BOSS/scripts/train_instruct.py:599`; cross-attempt cache at `:568-578` and `:651-652`.
- **Ours:** none of it. Our `scripts/lr_search.py:1-183` is entirely candidate arithmetic; grep for `select_edge_lr` / `plan_budget` / `_run_trial` over `scripts/` returns zero.
- **Value:** one port delivers a searched LR, a measured `t_per_step` (which D2 needs), **weights that are kept**, an OOM-halving path, and a cross-attempt cache. It also makes D3, R1, the LRRT picker question and the UNBRACKETED problem all disappear rather than needing individual fixes.
- **Conflict named (§7 C-2):** dpo-grpo said *"do not port the whole search blind — the reports twice named LR machinery as harmful."* **That reading is wrong on the facts.** The 20260831 report's "Do NOT port" list names the *challenger's* LES strategy and LR ladder. `run_lr_search` is the **boss's own published code, in the repo that retained the title**. Porting the champion's mechanism is not adopting an experiment. That said: it is ~1100 lines against our 183, so take the **validate-mode subset first** (`BOSS/lr_search.py:897-957` + `plan_budget`), and take D2's `t_per_step` measurement even if you take nothing else.

### M4. Checkpoint averaging on full fine-tunes
- **Boss:** `BOSS/scripts/checkpoint_avg_callback.py:261-332` (greedy soup: seed at best `:277-279`, accept only if `cand_loss < best - 1e-6` at `:305`, **time budget = half the remaining wall clock** at `:287-296`), `:349-455` (disk path for sharded/large), `:757-775` (restore-best + atomic weights-only swap). Wired at `BOSS/scripts/train_instruct.py:484-505`, final run only.
- **Ours:** `scripts/customized_trainer.py:1044-1204` — one-shot equal-weight merge, single accept/reject at `:1187`, **no time check at the `on_train_end` trigger `:1231-1247`**, and a LoRA-only bail at `:984-1002` that switches the whole capability off the moment it sees a full fine-tune.
- **Resolution of the three-way conflict (§7 C-3):** all three subsystems agree our construct is *worse*; they disagree on scope. Port the **averaging half** — greedy accept-if-better, the time bound, the full-FT disk path. It is a post-hoc read of checkpoints already on disk and is gated by our existing `merge_eval_fn` (`customized_trainer.py:124`), so a bad average cannot ship. **Refuse the trajectory half** — rollback, NEFTune escalation, memorized-masking — that is unvalidated machinery in champion clothing.
- **Strictly downstream of D4.** With 2 checkpoints there is nothing to average.

### M5. `baseline_stats` never reaches the training child
- **Ours:** `scripts/text_trainer.py:759-813` has no `--baseline-stats` arg; `train_info` at `:884-908` has no such key. Only reader is `adaptive_config.py:1099-1114`, in the orchestrator.
- **Boss:** CLI arg at `BOSS/scripts/text_trainer.py:358-366`, parsed `:372-384`, injected at `:454`, consumed in the child at `BOSS/scripts/train_instruct.py:272-281`.
- **Cheap, and it unblocks M6.** Caveat: do **not** add a `--baseline-stats` CLI flag blindly — it is unresolved whether the validator ever passes one, and our parser aborts on unrecognised args (a forfeit). Use the env path; `baseline_stats_reader` already implements it.

### M6. Three `utility.py` helpers we deleted that the boss actively uses
- **Boss:** `smart_truncate` at `BOSS/scripts/utility.py:45-80`, wired into `pad_inputs` at `:157`; `apply_prompt_loss_weight` at `:83-112`, called at `BOSS/scripts/train_instruct.py:279-280` when prompt:completion > 5:1; `gaussian_subsample` at `:115-149`, called at `:702-715` when measured coverage < 0.5 on >2000 rows.
- **Ours:** `scripts/utility.py:45-58` `pad_sequence` does `sequence = sequence[-max_length:]`; the other two are absent.
- **Take `smart_truncate` unconditionally** — it trims the *prompt* side and preserves the whole completion, which is strictly better on prompt-heavy rows and is the thing we are scored on. The other two are gated on M5.

### M7. Naive packing fallback for non-FA models
- **Boss:** `BOSS/scripts/monkeypatch.py:119-160` (`pack_data_points_naive`), `:252,:283` (`use_fa` flag and dispatch); `BOSS/scripts/train_instruct.py:304-350` (`packing_mode` switch).
- **Ours:** `scripts/instruct_config.py:347-350` disables packing entirely on non-FA; `scripts/monkeypatch.py:243-253` has no `use_fa`.
- Large mechanical throughput win on a model class we have already drawn, and it is the fix for R8's correctness hole in the same change.

### M8. Stratified dev split
- **Boss:** `BOSS/scripts/val_split.py:163-303` (`stratified_split`), `:151-160` (`_quantile_bins`), wired at `BOSS/scripts/tokenize_instruct.py:188,212`.
- **Ours:** `scripts/data/split_policy.py:88-140` (`leak_key`, `leak_safe_split`), wired at `scripts/tokenize_instruct.py:222-235`.
- **Resolution (§7 C-4):** config-hp said port all ~300 lines; deps said port the stratification half only. **Deps is right** — take `_quantile_bins` + the composite 4x4 stratum sampling, **skip `_near_dedup_groups`**: our `leak_safe_split` plus `dedup_knn` already give the group atomicity MinHash exists to provide, and the LSH pass is O(n · bands) with pairwise verification. Value: variance reduction on the exact signal we select on — memory says our dev-loss gauge is calibrated to 0.009 and the gemma gap was 0.0072, i.e. **our selection signal is currently coarser than the margin we lost by.**

### M9. Full-fine-tune reference model for the KL objective
- **Boss:** `BOSS/scripts/kl_trainer.py:43-69` (`load_base_model`), `:117-125` (lazy co-location), wired at `BOSS/scripts/train_instruct.py:840-844` for the not-`use_lora` case.
- **Ours:** `scripts/kl_trainer_mixin.py:64-67` returns `None` with no `disable_adapter`, then `:88-96` **silently falls back to plain CE**. `adaptive_config.py:106-108` forces LoRA at any size when `use_kl` — i.e. a scoring-critical objective depends on one config decision going right, and fails silent when it doesn't.
- ~30 lines of the boss's own tested code.

### M10. Deny-list FlashAttention head-size guard on vLLM selection
- **Boss:** `_FLASH_ATTN_HEAD_SIZES` + `_has_compatible_head_size` in `BOSS/scripts/model_utility.py`, called from `get_use_vllm`. **Ours:** deleted both; `get_use_vllm` has a fingerprint blocklist and a legacy name list, no head-size computation. ~15 lines, reads a config we already load.

### M11. Lower value, port when convenient
- **Training-data dedup** — `BOSS/scripts/data_filter.py:21-55`, called at `BOSS/scripts/train_instruct.py:262-264`. Unconditionally safe: removing exact duplicates cannot hurt a held-out metric. (Take `deduplicate_samples` only; see §6 for why not `filter_outliers`.)
- **DPO adaptive eval frequency** — `BOSS/scripts/train_dpo.py:296-305`. Self-contained, directly improves DPO checkpoint selection.
- **GRPO `max_prompt_length` derived from data** — ours is pinned at 512 on both paths (`scripts/train_grpo.py:486-491`); boss computes it at `BOSS/scripts/grpo_config.py:293-308` and scales batch with it at `:344-357`.
- **GRPO stratified split** — ours is still `data[:200]` at `scripts/tokenize_grpo.py:34`, no policy import, no gate.
- **3%-of-total warmup clamp** — `BOSS/scripts/train_instruct.py:433-435`. Two lines; ships with D2 since they share the `total_steps` recompute.
- **`quiet_mode`** — `BOSS/scripts/quiet_mode.py` (5020 bytes, verified present), imported first in eight boss modules; we leak `[CONFIG-RESOLVED] path=adaptive ... lr=2.86e-05 batch=8 steps_or_epochs=3` straight into a publicly queryable log. **Corrected (C3): it cannot break our OOM detection** — port it *with* the `print`→`sys.stdout.write` change at `scripts/text_trainer.py:69`. But rank it low on value: the 20260831 report explicitly listed quiet mode among changes that did **not** decide the result. Port for intel hygiene, not as a scoring fix. Route StageClock and `[FAST-CRASH]` to stderr first or you will silence your own diagnostics.

---

## §3 — THE RISKS (we carry it, the boss doesn't, no measurement behind it)

Ranked by how much of a run they can affect.

| # | Mechanism | Verdict | Why |
|---|---|---|---|
| **R1** | **Multi-launch LR ladder** — `text_trainer.py:1127-1310`, `MAX_LOOP_RUNS=8` at `:756`, BO override `:1199-1224`. Boss: `BOSS/text_trainer.py:487-489` one run. | **DELETE** | Affects the entire run *structure*, not a parameter. Named by both official reports. And it is no longer unmeasured — the 59469903 log shows `attempt 1/5`→`2/5` with the step count changing 361→722, then the time gate at `customized_trainer.py:493` refusing to use its output. It cost a relaunch and returned no LR. Replace with M3's in-process search. The runaway guard at `:1287-1296` (written after a 244-launch / 700GB incident) is evidence this mechanism has already failed catastrophically once. |
| **R2** | **Vocab-aware batch ceiling** — `adaptive_config.py:1490-1508`. Boss: absent. | **MEASURE-THEN-DELETE** | Fired hardest on our worst task (bucket 60 → log `batch=8`) and the run **still OOM'd**. It is a static table, not a memory measurement. The measurement is free and is the same run as D5: `use_liger=True` with the cap off. If it does not OOM, the cap was compensating for a defect we introduced at `:2181`. |
| **R3** | **Redis `state_manager` with a silent process-local fallback** — `state_manager.py:10-19, 42-43, 62-63`; `entrypoint.sh:6-7`; `training_requirements.txt:27`; `dockerfiles/standalone-text-trainer.dockerfile:41`. Boss: `BOSS/scripts/state_manager.py:1-20`, a 21-line JSON file. | **DELETE** | It degrades to a *silently wrong answer*, not an error, on the cross-process channel that carries `lrrt_lr` (`train_instruct.py:885-888`) and the best checkpoint (`customized_trainer.py:786-791`). **Four independent subsystems recommended reverting; zero dissented** — the only unanimous item in the ledger. Whether redis even came up in the tournament container is unresolved, which makes a dead channel an alternative explanation for parts of run 59469903. Reverting deletes the pin, the apt package, the daemon and a 2-second sleep in one move, and D14's guard comes with it. |
| **R4** | **Live divergence detector** — `customized_trainer.py:227-243` (default **on** at `:228`), init_loss from `log[0]` at `:654-655`, `logging_steps=5`. Boss: **no `on_log` hook at all**. | **DELETE / default-off** | It can terminate a healthy run off a single step-5 loss reading. The boss's only early stop is dev-loss overfit (`BOSS/checkpoint_avg_callback.py:675-698`, best*1.05, patience 3, DDP-synced) — it measures the thing we are ranked on. Replace, don't tune. |
| **R5** | **WSM one-shot equal-weight merge, unbounded in time** — `customized_trainer.py:1044-1204`, trigger at `:1231-1247` with **no time check**. | **MEASURE-THEN-KEEP**, with an immediate hard time bound | Do *not* delete averaging — the boss ships strictly more of it and retained the title. But ours runs at `on_train_end`, inside a post-training window already measured overrunning by 29s, with no bound. **Add a remaining-time check at `:1044` today**, then replace the merge with M4's greedy accept-if-better loop, which is strictly dominant. |
| **R6** | **Packing enabled with no non-FA path** — `train_instruct.py:309-323` unconditional; `monkeypatch.py:243-253` has no `use_fa`. | **FIX, not measure** | This is a correctness hole, not a tuning risk: under eager attention, packed sequences cross-contaminate. Currently reachable and unguarded. The fix *is* M7. |
| **R7** | **`reward_classifier` overriding GRPO LR and beta unconditionally** — `grpo_config.py:393-441`, `adaptive_config.py:2400-2410`; `allow_find_lk_lr` is permanently False so the Tier-1 gate is dead and the fallback always promotes. Boss: absent; its GRPO LR is the size bucket alone. | **DELETE the beta authority permanently; default the whole thing off** | An unvalidated static catalog silently overriding both knobs, through a gate that can never fire. Never leave a permanently-False flag quietly promoting a fallback. |
| **R8** | **GP-EI Bayesian optimisation + `optuna==4.4.0`** — `text_trainer.py:1200-1226` gated on `len(state["runs"]) >= 3`; `bo_augmentation.py`; pin at `training_requirements.txt:33`. Boss: none. | **DELETE** | The gate needs ≥3 completed runs, which R1's own time gate makes unreachable on a ≤1.3h task — so on our round-1 tasks it almost certainly never fired. Deps wanted to check the Loki log first; that check is a 60-second grep and worth doing, but the default action is removal either way. Deleting it plus R3 makes `training_requirements.txt` **byte-identical to the retained champion's**. |
| **R9** | **`min_lr_rate` family variation** — gemma/phi 0.15 (`adaptive_config.py:604,620`), opt 0.75 (`:648`). Boss: flat 0.25 (`BOSS/instruct_config.py:207`). | **DELETE the variation** | The 0.75 cell is a scheduler rewrite wearing a hyperparameter's clothes. No profile comment cites a measurement for the gemma/phi cells (unlike the smollm cell, which documents its 0.075→0.25 fix — that one has evidence). **Note the interaction with D2:** at 61% of the schedule we never reach the tail, so `min_lr_rate` barely matters today. Revert to 0.25 now; A/B one family at a time *after* the epoch planner lands. |
| **R10** | **`maybe_d2z_scheduler`** — cosine→linear-decay-to-zero override, defaults **on** at `hp_override.py:111,140-142`, and is silently discarded by the template (`instruct_config.py:235-236,257-258`). | **DELETE the mechanism, do not fix the wire** | Both reports explicitly said keep `cosine_with_min_lr`. The only reason we currently comply is that the wire is dead. Delete `maybe_d2z_scheduler` and the call site at `adaptive_config.py:2504-2508`, plus the unconsumed `max_packed_size` profile keys. |
| **R11** | **Cross-instance best-checkpoint persistence** — `customized_trainer.py:252-273` restore. Boss: `BOSS:54-56` sets all three to None, and there is **no read or write of any persisted best-checkpoint key anywhere in `BOSS/scripts`**. | **DELETE the restore** | Can suppress the submission write entirely. Its stated purpose does not hold: probe runs launch with `save_strategy=no` and a per-attempt `output_dir`, so the checkpoint the restored loss refers to is usually not on disk under this run's `output_dir`. INFERRED — no live occurrence confirmed — but the failure mode is "ship nothing" and the mechanism protects against a case that cannot arise. |
| **R12** | **OOM ladder floors** — `MIN_OOM_MAX_LENGTH = 512` (`text_trainer.py:331`), `--retries 5` (`:799`). Boss: floor 2048 (`BOSS/text_trainer.py:222`), retries 8 (`:353`). | **MEASURE-THEN-KEEP**, raise the floor now | A run that survives at 512 reports health while training on truncated rows — the exact gauge-lies pattern that cost us the max_length wire (3a6658eb trained 490 of 27992 rows). Raise to 1024-2048, restore retries to 8, and **log loudly at that rung** so the gauge cannot report health while starved. |
| **R13** | **NEFTune default 5.0 on the fallback path** — `instruct_config.py:307-312`. Boss: no neftune flag in the template at all. | **DELETE** (set 0.0) | A crash path is not the place to run an experiment. |
| **R14** | **Two independent `max_length` sizings** — `instruct_config.py:443` and `adaptive_config._select_max_length`; nobody established which wins on the instruct path. | **MEASURE** (resolve which site wins, first) | §7 C-5: config-hp said port the boss's p99+2·p50 policy; deps said do not port. Both are half right. The policy question (p95 vs p99) is offline-verifiable against archived `baseline_stats` in an afternoon. The *real* finding underneath is deps': two independent sizings of the same quantity is our named bug class. Resolve the duplication before touching the percentile. |
| **R15** | **`BUCKET_REFERENCE_LEN = 1024`** (`adaptive_config.py:188`) vs the boss's `default_max = 2048` (`BOSS/instruct_config.py:310-320`). | **ALIGN to 2048** — not really a risk, a mis-transcription | The buckets are inherited from this exact lineage and the boss's own compensation code names 2048 as the length they were fitted at. That is stronger evidence than our stated guess. |
| **R16** | **`save_total_limit 3`** (`instruct_config.py:229`). Boss: **grep for `save_total_limit` over the entire boss checkout returns nothing** (verified). | **DELETE** | §7 C-6: three subsystems proposed three different fixes and **not one could name which save site it governs**. A retention limit nobody can point at, sitting upstream of checkpoint selection, in a repo whose named bug class is "correct code nothing calls" — and D4 is about to multiply the checkpoint count. Match the boss. |
| **R17** | **`PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`** (`entrypoint.sh:9`). Boss sets no env. | **KEEP, but make it bisectable** | Put it behind an env with the current value as the default so a suspected allocator interaction can be tested in one run without a rebuild, and add it to the standing list of unvalidated global settings. |

---

## §4 — THE KEEPS (strict: a measurement in a comment counts, an intention does not)

1. **`add_random_noise` rewrite** — `scripts/add_random_noise.py:54-74` (`_clone_tree`), `:77-90` (`_break_link`), `:105-142`, `:145-180`. Boss does `AutoModelForCausalLM.from_pretrained` at `BOSS:14`, which **cannot load the models this path exists to rescue**. Task 29fc1a10 was exactly that class. Forfeit-class, strictly ahead of the retained champion. **Keep unchanged.**
   - *Paired free fix:* `NOISE_STD` is `0.01` on **both** sides (ours `:35`/`:136`, boss `:17`/`:23` — verified). Our own file argues at `:19-26` that the clean copy passes the check, and the validator compares config attributes, not weights. Set it to 0 and ship the clean clone. Free rank on every forfeit, and not a divergence risk since the boss has the same problem.
2. **Preflight forfeit path** — `text_trainer.py:256-296` (`detect_unloadable_architecture`, deliberately narrowed to the single *"does not recognize this architecture"* marker so a half-downloaded snapshot is not diverted), `:875-880`, `:177-241` (tokenisation gate). Boss burns eight retries (`BOSS/text_trainer.py:353`). Worth its complexity **only** because of keep #1 — review the two as one mechanism.
3. **Deadline stop + finish-state transition** — `customized_trainer.py:574-599`, `:601-629`. Motivated by a measured 244-launch / 700GB incident, and **validated in this tournament's log**: `budget reached; handing back so the post-training checks can run` and `state set to 'finish' so the outer loop stops relaunching`. The boss has the stop (`BOSS:217-225`, same rationale in its comment) but no state transition. One of the few places our addition has an incident behind it.
4. **Held-out scoring for LR probes** — `customized_trainer.py:365-407` (`_probe_loss`, fail-open at `:402-407`), used at `:486`,`:504`. Boss scores probes on **training** loss (`BOSS:162`, `:180`). Strictly better signal, and the fail-open is the right shape: a probe is never lost to an eval failure.
5. **State-read hardening** — `customized_trainer.py:53-71`, `:74-99`. Boss does a raw `strptime` at `BOSS:114-116` and an unchecked `min()` at `:192`. Keep the hardening; delete the Redis backend under it (R3).
6. **`MAX_TRIES` 3 vs boss 9** — `customized_trainer.py:17-21`, cold-start arithmetic in the comment. Keep at 3 until the LR picker is fixed.
7. **Anonymisation-resistant model detection** — `scripts/model_detection.py`, `instruct_config.py:55-88,360-367`, `grpo_config.py:281-297`. Boss matches name strings only (`BOSS/instruct_config.py:246-266`), which anonymised tasks defeat. Clearest case in the whole diff where we beat the champion and the evidence is in our own run log.
8. **len-check tokenisation instrumentation** — `tokenize_instruct.py:295-345`. Boss: absent. Read-only, one pass over lengths, and it catches the exact bug class we have already shipped (the max_length wire that dropped 98% of rows).
9. **`dedup_knn` placement** — `data/dedup_knn.py:167-187`, wired at `tokenize_instruct.py:194-210`. Better placed than the boss's train-time dedup at `BOSS/train_instruct.py:262`.
10. **axolotl venv transformers pin + build-time import assert** — `dockerfiles/standalone-text-trainer.dockerfile:81,89-95`. Boss has neither (`BOSS:30-35`). This converts a class of failure that only surfaces at tokenisation time in a live task into a **build** failure — and it is the direct fix for the 20260824 TRL import clash that made all three runs submit a noised base model. **Do not "simplify back to the boss" here**; the boss's version is safe only because its venv has nothing that can drag transformers, and the assert is what guarantees that stays true for us.
11. **Core ML pins byte-identical to the boss** — `training_requirements.txt:1-14`: transformers 4.51.3, trl 0.18.0, datasets 3.5.0. **The report's #1 finding, "Dependency Version Explosion (HIGH CONFIDENCE: harmful)", does not apply to us.** Our only two additions are `redis==7.0.1` and `optuna==4.4.0`, both of which R3 and R8 delete — after which the file is byte-identical to the retained champion's. Say this out loud in any future diff-report defence.
12. **`dev_absorption`'s hotness guard** — `dev_absorption.py:83-122` (`_prior_dev_loss`, incl. the `proxy=` discrimination at `:106-108`) and `:248-256` (the refusal). Boss's `dev_pass.py` has **no loss comparison anywhere**. Carry it across when M1 moves the mechanism into the child; reading `loss.txt` works there too.
13. **StageClock + `[FAST-CRASH]` marker** — `text_trainer.py:80-124`, `:465-476`. Cheap, control-flow-free, boss-absent. Keep — but route to **stderr** before porting quiet_mode.
14. **`resolve_dpo_max_length` with its OOM rung** — `train_dpo.py:117-172`. Keep; take only the boss's `max_prompt_length` derivation from `chosen_length_distribution` (`BOSS/dpo_config.py:207-215`), which replaces a guess with a measurement.
15. **ZeRO-3 gradient-checkpointing branch on instruct** — `train_instruct.py:240-251`. No boss counterpart in either direction (verified: the boss's `training_args.*` assignment list contains no `gradient_checkpointing_kwargs`). Keep, but verify our DDP + non-reentrant choice actually beats the default on a single-GPU run — it was adopted to fix a DDP error we may no longer hit.
16. **Build-time network surface identical to the boss's** — `dockerfile:30-42,78-95,99-107` vs `BOSS:4-15,30-35,39-47`, same endpoints including the same fiber git URL. No exploit signal. Make it a standing pre-submission invariant: any new `RUN` reaching a host outside apt / PyPI / the inherited fiber URL is an automatic reject, because that is what the validator's reviewer looks for.

**Rejected from KEEPS** (intention, not measurement): the early-stop CV block (`customized_trainer.py:204-218`, off by default, nothing reads `train_loss_history`), the advisory LR resolver (`adaptive_config.py:2525-2546`, comment says *"advisory only — NOT applied"*), `lr_guardrail_interpolate` and `find_lr_for_task` (`lr_utils.py:68-101`, `lr_finder.py:197` — **zero callers each**). Delete all four.

---

## §5 — THE ONE CHEAPEST EXPERIMENT

**Step 0, today, before anything else (60 seconds):** confirm the 59469903 dataset URL still resolves. `dataset_url_expires_at = 2026-09-14T11:10:27Z`. If it is dead, this experiment cannot be run on the task we have a full trace for, and the whole plan changes.

**The experiment: one replay of 59469903 at a commit carrying exactly four changes and nothing else.**

1. Move the promotion block `customized_trainer.py:769-793` above the telemetry at `:698` (D1).
2. `EMIT_PER_EXAMPLE_LOSSES=0`; remove the wiring at `train_instruct.py:670-683` (D1).
3. Port BOSS `train_instruct.py:441-449` — the eval/save cadence (D4).
4. Port BOSS `customized_trainer.py:231-245` and `:272-295` — the two eval governors (M2).

Same LR (2.86e-05), same batch, same epochs, same everything else. Against the 12b16b5 baseline we already hold a full trace for.

**Why this one, and not the LR question.** The largest remaining uncertainty is not "is our LR wrong" — it is **"is our gap a training-quality problem or a checkpoint-selection problem, and have we ever measured either?"** Memory's own verdict is *"every number we have is the fallback"*: our training quality has never been measured. And the LR question is unanswerable until selection is fixed — with **two** checkpoint candidates, every LR looks the same, which is exactly why 10.5 GPU hours of LRRT arbiter runs returned byte-identical LRs across all three arms and got invalidated.

**What it settles, from one run:**
- The best-of-N vs best-of-2 delta in nats, against a known target (rank 1 at 0.0451274, us at 0.0523470, gap 0.0072). We already know one adjacent-checkpoint pair differs by 0.0010523.
- A real `eval_runtime` under the governors — the number every subsequent sizing decision needs.
- Whether the ~40 steps reclaimed from telemetry move the loss at all, which is the first honest read on our training quality that is not a fallback.
- It costs **zero new mechanisms**: three of the four changes are the boss's own published code, and the fourth is a statement reorder.

**What it deliberately does not touch:** LR, batch, `use_liger`, the ladder, dev absorption. Change one subsystem per run. Shipping forty fixes at once and calling the result an improvement is precisely the pattern the last two reports condemned — the fact that each individual fix is defensible does not make the bundle measured.

**Second run, if the dataset survives and budget allows:** `use_liger=True` with the vocab cap off, everything else at baseline. That single run settles D5, D6, R2 and D-static-batch together, because they are one causal chain.

---

## §6 — WHAT I WOULD NOT TOUCH

1. **The ML pins.** transformers 4.51.3 / trl 0.18.0 / datasets 3.5.0 — byte-identical to the champion. **Specifically: do not bump transformers to rescue LFM2.** The boss cannot build `lfm2` on 4.51.3 either and it **retained the title**; the 29fc1a10 forfeit was shared across the field, not a deficit of ours. The report's verbatim instruction is *"Only upgrade when a specific task requires it, not preemptively."* Bumping here would hand the next reviewer its own #1 finding.
2. **`cosine_with_min_lr`.** Both reports named it. Do not wire d2z; delete it instead (R10).
3. **`add_random_noise` and the preflight forfeit path.** Keeps #1 and #2. Two forfeit-class advantages over the champion.
4. **The docker build-time network surface.** Identical to the boss's; changing it can only create signal.
5. **The rollback / NEFTune-escalation / memorized-masking half of `checkpoint_avg_callback.py`.** It is 34,954 bytes, it mutates the training trajectory, and nobody read its selection logic. This is unvalidated machinery in champion clothing — the fact that the champion carries it is not evidence it helped, and adopting it would reproduce our own losing pattern with better provenance.
6. **`filter_outliers`.** Unvalidated data surgery costing a forward pass, and its only boss consumer is `checkpoint_avg_callback.py:481` behind a `try/except ImportError` — so **it may never execute on the boss either.** Both subsystems that looked at it agreed. Take `deduplicate_samples` alone.
7. **The LRRT picker default.** Do not flip `slope10`→`lossmin` (`lr_finder.py:38`). `recon/lrrt_pickers_20260905/FINDINGS.md` states the two criteria pull opposite directions: `lossmin` brackets better, but training too high costs +36% versus +2.7% for too low. Distance alone does not settle direction, and the arbiter runs meant to settle it were invalidated. If M3 lands, the picker stops existing.
8. **`recon/`.** 74 files tracked at 12b16b5. Deleting it buys no ranks and costs us our own tooling. But before a submission that could actually place, move it out of the tracked tree — the boss's own `.gitignore` carries a *"Local-only experiment/seeding/trainer helpers (never commit — contain IPs, repo URLs, commit hashes, task IDs)"* block, so the champion prunes exactly this.
9. **Our dedup placement, len-check instrumentation, anonymisation-resistant detection, held-out probe scoring.** Four places we are ahead. Leave them.
10. **Anything at once.** The verdict *"Simplicity beats complexity when complexity lacks validation"* is about validation, not line count. A 40-change bundle is unvalidated regardless of how good each change looks.

---

## §7 — CONFLICT REGISTER (named, not smoothed)

| | Conflict | Resolution |
|---|---|---|
| **C-1** | **Dev absorption.** deps: *"keep ours, do not port dev_pass.py."* train-instruct: *"port dev_pass.py and both boss blocks — highest-confidence positive-delta port available."* text-trainer: *"port the placement, keep our r=0.1."* | **text-trainer is right and the other two are each half right.** The mechanism is ours and twice measured (−0.0194, −0.0052); the *placement* and the *computed reserve* are the boss's and we lack both. Port `BOSS/train_instruct.py:874-899` + `:813-830` + `:862-873`; keep our rate and our hotness guard. Do not port `dev_pass.py`'s DDP machinery. |
| **C-2** | **The boss's LR search.** lr-subsystem + train-instruct: *"port `run_lr_search`; it is the champion's own published code, not an experiment."* dpo-grpo: *"do not port blind — the reports twice named LR machinery as harmful."* | **lr-subsystem is right on the facts.** The 20260831 "Do NOT port" list names the *challenger's* LES strategy and LR ladder. `run_lr_search` is what the **boss** shipped while retaining the title. dpo-grpo's caution still buys something: take the validate-mode subset first, not 1100 lines in one commit. |
| **C-3** | **Checkpoint averaging.** customized-trainer: *"do not delete, upgrade to the greedy soup."* deps: *"highest-value item in this subsystem."* train-instruct: *"do not port yet, A/B first."* | **A scope disagreement, not a direction one.** All three agree our one-shot equal-weight merge is worse than the boss's greedy version. Port the averaging half (post-hoc read of on-disk checkpoints, gated by our existing `merge_eval_fn`); refuse the trajectory-mutating half. train-instruct's "not yet" is right about **ordering**: it is strictly downstream of D4, because with 2 checkpoints there is nothing to average. |
| **C-4** | **`family_lr_table` Tier-1 gate.** config-hp: *"fix the gate to MED-low, it contradicts its own docstring."* lr-subsystem: *"do NOT simply flip 1606 — MED-low drops us to the generic 8e-6 bucket, which is worse. That is a regression."* | **lr-subsystem is right, and this is the most dangerous item in the ledger** — the "obvious" fix makes things worse. Decide the tier *chain* first: adopt the boss's computed `estimate_starting_lr` (`BOSS/lr_finder.py:252`) as the fallback, **then** raise the gate to MED-low. Changing `adaptive_config.py:1606` alone is a regression. |
| **C-5** | **`max_length` policy.** config-hp: *"port the boss's p99 + 2·p50."* deps: *"do not port."* | Both half right; the real finding is deps'. **Resolve the duplicate sizing first** (`instruct_config.py:443` vs `adaptive_config._select_max_length` — nobody knows which wins on the instruct path). Then answer p95-vs-p99 offline against archived `baseline_stats`. |
| **C-6** | **`save_total_limit 3`.** customized-trainer: *"raise it to at least the WSM K."* config-hp: *"remove it."* train-instruct: *"raise or remove."* | **Remove.** Verified: the boss has no `save_total_limit` anywhere. Not one subsystem could name which save site it governs, and that question was explicitly logged as unestablished. |
| **C-7** | **Dev-split stratification.** config-hp: port all ~300 lines of `val_split.py`. deps: port the stratification half only. | **deps.** We already have group atomicity from `leak_safe_split` + `dedup_knn`; `_near_dedup_groups` is O(n·bands) duplicating it. |
| **C-8** | **Our skill file contradicts the boss's code.** `.claude/skills/gradient-text-tournament/SKILL.md:177-181` claims *"all 9 winners select on reward alone and ignore the KL penalty"* and lists validator-exact GRPO selection as our differentiator. | **False against this boss:** `BOSS/customized_trainer.py:351-370` selects on `reward − 0.5·kl`. Whether the claim was ever true is unknown. **Fix the skill file** — it is currently steering future decisions off a refuted premise. |

**Unresolved and worth one cheap check each:** (a) `budget=1.75h` in the run log vs `hours_to_complete=0.75` in the auditing record — this discrepancy directly sizes D4; (b) whether `bo_augmentation` ever changed a selected LR (one grep of the archived Loki log); (c) whether the TRL 1199 reshape crash reproduces under `trl==0.18.0`, which decides whether D17 is a workaround or a misdiagnosis; (d) whether redis-server actually came up in the tournament container — a dead channel is an alternative explanation for parts of run 59469903, and R3 removes the question entirely.