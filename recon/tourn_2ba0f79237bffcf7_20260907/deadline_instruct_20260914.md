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

## Open

On a run that ends before `periodic_save_steps` (500) is reached, nothing is ever evaluated:
`loss.txt` holds `156,proxy=no_eval` and there is no eval-selected checkpoint. Unreachable on
a real multi-hour task. Buying one early eval would cost 259s of a 682s budget — not decided.
