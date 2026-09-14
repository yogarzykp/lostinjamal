# Instruct end_time overrun: −80s → +83s

Task `dd558022`, Qwen2-1.5B-Instruct, 1xH100, fresh container + `redis-cli flushall` each run.
`ops/smoke/gate.sh instruct`, identical invocation every time; one variable changed per run.

## The measurement

| commit | overrun vs end_time | steps | dev absorption | gate |
|---|---|---|---|---|
| baseline (`91fdaf4`) | **−80s** | 150 | skipped | 12/12 |
| `3fb99d6` | −75s | 150 | skipped | 12/12 |
| `08b0337` | **−94s** | 156 | skipped | 12/12 |
| `be81e18` | **+83s** | 156 | **ran** (519 steps, dev loss 0.8247) | 12/12 |

The gate passed on all four. **It has no overrun assertion**, so it could not tell these
apart — the number comes from the `[stage]` timer line, not from a gate row.

## Cycle decomposition (the reason the first two attempts failed)

Both stages, same model, same 955-row dev split:

| | eval | per-example | save | copy | total |
|---|---|---|---|---|---|
| instruct | 38s (25.0 rows/s) | 53s (18.0/s) | 9s | 159s | 259s |
| KL | 116s (8.2 rows/s) | 178s (5.4/s) | 9s | 159s | 462s |

* the **copy dominates** (35–61%) and scales with the model, not the dev split
* a **KL eval is 3x slower per row** — every row also goes through the frozen base
* `3fb99d6` modelled the cycle as `dev_rows x train-step time`: 702s predicted, 259s real

## What each run proved

1. `3fb99d6` — guard conditioned on `has_checkpoint`, which the first cycle never has.
   Dead code on its only path. 1046 CPU tests passed because the fixture set it True.
2. `08b0337` — guard fires. But `_cycle_t0` is stamped before the guard decides, so the
   6s save it substituted was recorded as a measured cycle; that outranked the 299s
   estimate and the end_time trigger let a 250s eval run on 178s of budget.
3. `be81e18` — a cycle that did not evaluate is not recorded. Clean.

## Open — and the dev absorption is NOT straightforwardly a win

On a run that ends before `periodic_save_steps` (500) is reached, nothing is ever evaluated:
`loss.txt` holds `156,proxy=no_eval` and there is no eval-selected checkpoint. Unreachable on
a real multi-hour task.

Two consequences follow, and the second was nearly reported as a success:

1. no eval-selected checkpoint — the submission is the last save, not the best one;
2. **dev absorption ran with its safety guard UNARMED.** The guard refuses a pass that ran
   hotter than the checkpoint's own dev loss, and it reads that number from `loss.txt`. A
   `proxy=` value is a TRAIN loss, not comparable to a dev pass, so `_prior_dev_loss`
   correctly returns nothing and the run logs `[dev-absorb] guard unarmed`.

Compare the same stage with an eval present:

    with eval (baseline)  pass loss 0.8268 > checkpoint dev loss 0.7964 -> REFUSED, untouched
    no eval  (be81e18)    pass loss 0.8247, nothing to compare -> ABSORBED, submission updated

So "dev absorption finally ran" is not evidence of an improvement. On the one run where the
comparison was possible, a pass of almost exactly this size was **refused as too hot**. The
submission on `be81e18` was modified by a pass the armed guard would plausibly have rejected.

That materially strengthens the case for buying one early affordable eval on short runs: it
would restore checkpoint selection AND re-arm the absorption guard. Cost 259s of a 682s
budget. NOT decided here.

## Correction: the gate's default dataset was never here, not "expired"

`ffdc3f9` says the default task's presigned URL had expired. That was an inference stated as
a measurement, and it is not supported. What IS verified:

* nothing under `ops/smoke/` fetches a dataset — every runner reads a pre-placed file under
  `/cache/datasets` (`run_instruct_replay.sh:37`, `run_dpo_smoke.sh:78`, `run_chat_smoke.sh:43`,
  `run_grpo_smoke.sh:56`, `ab.sh:43`);
* this box was provisioned 2026-09-13 and holds `dd558022` (12:37) plus three others
  (23:25–23:40). `6d8b2af6` was never copied here.

So the file was **absent**, and whether it could still be re-fetched is UNVERIFIED. The default
is now `dd558022`, the task whose data the box actually holds, in `gate.sh`, `ab.sh`,
`lr_recovery.sh` and `run_chat_smoke.sh`.

`tests/test_gate_assertions_have_producers.py` had `6d8b2af6` re-typed under the comment
"gate.sh's INSTRUCT_TASK default". It now parses the value out of `gate.sh` instead: a constant
labelled as another file's default, which is not that file's default, reads as checked and is not.

## The cost model was recalibrated (2fc2028) — the gate-box decomposition did not transfer

The decomposition recorded above ("copy 159s at ~55 s/GiB") is wrong, and was wrong when
written. Reconstructing the real tournament cycle from the `ts` fields of
`loki_59469903.txt` around step 500 (gemma-2-2b, 4.86 GiB, 965 dev rows):

    eval           109.2s    ('eval_runtime': 109.1995, 8.837 samples/s)
    per-example    349.7s    ts 1788793941159686455 minus the eval-end record
    save             5.71s   Updating... -> Copy...
    copy             5.21s   Copy... -> next record
    ------------------------
    cycle          469.8s

Three corrections fall out:

1. **The eval rate does not transfer.** 8.84 rows/s on the tournament box against 25.0 on the
   gate box — the shipped `EVAL_ROWS_PER_SEC = 20.0` was 2.3x optimistic, the dangerous way.
2. **The copy is nearly free.** 5.21s for 4.86 GiB is ~1.1 s/GiB, against a shipped 60.
3. **The "159s copy" was never a copy.** It is `259 - 38 - 53 - 9`, a residual absorbing the
   checkpoint metric, telemetry, the redis persist and the WSM pool copy. The real cycle's
   dominant term is the per-example pass — 74% of it — which the model priced at 64s.

Net effect of 1 and 2 on the gate box: they cancel, so every reading there looked healthy.
Applied to the real run the same model predicts **419s against a measured 470s** — it would
have started an eval it could not finish.

Replaced by an explicit envelope with no per-term claims:

    cycle ~ (dev_rows / world_size) * model_GiB * K + 20s      K = 0.13, 0.18 with KL

| case | rows | GiB | measured | envelope | ratio |
|---|---|---|---|---|---|
| gate instruct | 955 | 2.88 | 259s | 378s | 1.46x |
| gate KL | 955 | 3.43 | 463s | 610s | 1.32x |
| gate DPO | 200 | 0.25 | 15s | 27s | 1.77x |
| gate chat | 104 | 0.25 | 14s | 23s | 1.67x |
| REAL tournament | 965 | 4.86 | 470s | 630s | 1.34x |

Coverage of all five is a parametrized test. The `world_size` divisor is reasoned, not
measured — every cycle here is single-GPU.

## Not implemented: the early-eval scheduling

Three independent designs (last-affordable-moment, adaptive periodic interval, cheapen the
cycle) were each rejected 3/3 by an adversarial panel. The decisive objections:

* widening the lead from the estimate makes the affordability guard **unfalsifiable** —
  the lead is `ceil((1.25*est+45)/60)`, so `remaining > cost` holds by construction and the
  guard that produced +83s becomes dead code;
* a wider lead fires end_time BEFORE the first checkpoint exists, where `has_checkpoint` is
  False and the eval is refused unconditionally — the same `proxy=no_eval` outcome, minus
  ~56 training steps;
* the `checking_mode == "none"` precondition one design relied on is false for every run that
  has ever produced a submission in this repo, including the real tournament run.
