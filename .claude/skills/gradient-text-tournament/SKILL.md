---
name: gradient-text-tournament
description: Operating knowledge for competing in the Bittensor Gradient (G.O.D, subnet 56) TEXT tournament with this miner codebase. Use when working on training config, learning-rate selection, checkpoint selection, dataset handling, submission packaging, or when deciding whether to adopt a technique seen in a public winner repo. Also use before entering a tournament or pushing miner code.
---

# Gradient TEXT tournament — operating knowledge

Verified against the `gradients-ai/G.O.D` validator source and 9 fingerprinted winner
repos on 2026-08-05. Every claim below marked ✅ was read directly in source. Re-verify
anything load-bearing before betting a tournament entry on it — the validator moves.

## 1. How you are scored (✅ verified)

`validator/scoring/tasks.py::calculate_miner_ranking_and_scores`:

| Placement in a task's miner pool | Score |
|---|---|
| Rank 1 | `FIRST_PLACE_SCORE = 3` |
| Rank 2 .. top 75% | `0.0` |
| Bottom 25% (only when pool > `MIN_IDEAL_NUM_MINERS_IN_POOL = 8`) | `SCORE_PENALTY = -1` |

- Ranking is **ordinal and relative** within the pool. A 0.0001 win scores the same as a 0.5 win.
- Instruct / DPO / Chat: **lowest `eval_loss`** wins. GRPO: **highest reward** wins (the field is
  still called `test_loss` but holds a reward). Env tasks: separate PvP pipeline.
- Invalid repo / non-finetune / NaN loss / duplicate → `0.0`, bumped to `-1` if any valid
  submission exists in that task.
- Validator-side `BETA_DPO = 0.1`; test split `TRAIN_TEST_SPLIT_PERCENTAGE = 0.1`, seed 42,
  fully held out from miners.

**Consequence:** "consistently decent" earns zero. Optimise for outright per-task wins.
A NaN checkpoint scores identically to a crashed run — silent zeros are the most expensive
failure mode, which is why the NaN guard and fallback paths matter.

### Tournament placement pays two positions (✅ verified)

`validator/tournament/performance_utils.py:205-240`:
- **Champion** (dethroned the boss): base weight + emission boost, with champion time-decay.
- **Runner-up** (reached boss round, failed to dethrone): `runner_up_share × base_weight ×
  scale_factor`, **no boost**, only `RUNNER_UP_EMISSION_DAYS = 7` days, then zero.

So reaching the boss round and losing still pays. Realistic target is **rank 2 first**.

## 2. The duplicate detector — read this before adopting anything (✅ verified)

`validator/infrastructure/repo_dedup.py`, `validator/tournament/dedup_gate.py`,
`validator/infrastructure/repo_dedup_config.json`.

| Tier | Trigger | Consequence |
|---|---|---|
| T0 | identical resolved git SHA | auto-eliminate |
| T1 | identical sha256 of **normalised** source | **auto-eliminate, no human review, before training starts, no appeal** |
| T2 | Claude pairwise agentic review at the R1→R2 gate | halts tournament pending human approval; flagged repo **published** to `gradients-opensource` as `dedup-<hotkeyprefix>-<hash>` |

**T1 normalisation drops comments entirely** (`_normalize_text`: skips blank lines and any
line whose stripped form starts with `#`, collapses internal whitespace). Therefore:

> Differentiating submissions only by comments produces **identical T1 digests**.
> Any "marker commit per hotkey slot" scheme is a guaranteed mass auto-elimination.

The live T2 prompt classifies as **COSMETIC** (never makes a pair distinct):
renames / reordering / reformatting / comments; dead code; **parameter tuning — "changing the
value(s) of existing knobs (LR, seed, batch size, ratios, table entries) — however MANY you
change. N cosmetic deltas never sum to one genuine delta"**; **re-parametrisation — "feeding an
existing knob its value a different way … even wrapped in a helper … EVEN IF the two pick
different values"**; **fake differentiators — branches on env vars/config never actually set
inside the locked training container**.

It classifies as **GENUINE** (any one is enough): a confirmed NEW mechanism that actually
executes and changes behaviour — LR finder, model soup, new subsampling/packing/scheduling,
early-stopping or checkpoint-selection policy, a real baseline bug fix.

Policy is explicitly "tolerates false positives … when in doubt, lean duplicate".
The boss/baseline hotkey is permanently exempt from flagging.

### The adoption rule

**A public winner repo is a source of HYPOTHESES, never a source of IMPLEMENTATION.**

For each technique you adopt:
1. Take the *idea* from the winner repo.
2. Find its **public origin** (paper, textbook practice, validator source you read yourself).
3. Implement inside **our** architecture — never mirror their file/function decomposition.
4. Derive every constant from **our own measurements**; keep the calibration that produced it.

**Do not rely on a "many miners converged on this" defence.** A 14-repo audit spanning
2025-08 → 2026-05 found that the public winner repos are not independent families at all — they
are four evolutionary strata (A→B→C→D) of a *single* ancestral codebase. Even the one
same-tournament position-1/position-2 pair (tournament `33c7619a4855ab63`, 2026-04-09) matched on
32 of 33 techniques: two hotkeys running one trainer. Co-occurrence in that corpus is
**inheritance, not convergence**.

The defensible T2 defence is therefore narrower:

> **"This is an upstream framework default, or it is publicly documented (paper / validator
> source I read myself), therefore my implementation is not a port."**

Corollary, and it is the most useful rule here: **the ABSENCE half of that corpus is far more
trustworthy than the presence half.** Shared presence tells you nothing about independent
discovery. But one family declining to adopt a technique for ten months is at least an
unconfounded observation.

## 2b. This repo descends from a PUBLISHED winner — know your exposure (✅ measured)

Measured 2026-08-05 by reimplementing the validator's exact `_normalize_text` and comparing
file-by-file against `gradients-opensource/god-text-tourn-72871bf73ef78976-20260423-position-2`
(Lineage D, public on GitHub):

| | |
|---|---|
| Shared paths | 71 |
| **T1-identical (normalised digest equal)** | **58** |
| Modified by us | 13 |
| Unique to us | 26 files, ~12,600 lines |

The 58 include all of `trainer/`, all of `mcp_server/`, all of `scripts/core/`, `monkeypatch.py`,
all three `tokenize_*.py`, `data/dedup_knn.py`, and all four `lrs/*.json`.

**T1 is safe.** T1 digests the *whole tree*; ours is 97 files with 13 divergences, so the tree
digest cannot collide with theirs.

**T2 is the real surface.** T2 is a *pairwise* judge. Against any entrant who also forked that
public repo, the comparison starts from 58 identical files, and the judge must find a genuine
delta in the remainder. Our delta is real and large — `adaptive_config.py` (2,348 lines),
`dynamics_utils.py` (922), `bo_augmentation.py` (518), `model_detection.py`,
`reward_classifier.py`, `cross_lingual_detector.py`, plus `customized_trainer.py` grown from 366
to 1,270 lines — and `ADAPTIVE_MODE` defaults to `"1"`, so it **actually executes**, which is
exactly what the T2 definition of GENUINE requires.

Practical consequences:
- Never let the unique surface shrink. It is the entire T2 defence.
- Any new mechanism must be **live in the default path**, not env-gated off. A branch that never
  executes inside the locked training container is explicitly a "fake differentiator".
- Two inherited files are named in the audit as the family's loudest fingerprints and are
  T1-identical to the public copy: `scripts/add_random_noise.py` (N(0,0.01) on input embeddings)
  and the `lrs_lookup.py` sha256(model_name) → `lrs/*.json` layout. Replace both mechanisms.

## 3. Tournament structure (✅ verified, one part pending)

- Group/knockout rounds → **pre-boss** knockout (exactly 2 competitors) → **boss round**.
- Boss round on `main` today: **6 tasks** = 2 instruct + 1 DPO + 1 GRPO + one continuous-SFT
  chat task per lineage (2 lineages: `quasar`, `qwen`).
- Win condition (`round_results.py::determine_boss_round_winner`):
  `required_wins = max(1, total_tasks - 1)` **and** the challenger must win **every**
  continuous-SFT task. `BOSS_ROUND_WIN_MARGIN = 0.01` (1%, additive).
- Boss big-model pool is **12B–71B** at `PROBABILITY_OF_A_BIG_TEXT_MODEL = 0.2`.
- Text models are pulled dynamically from a content service, not a static list.

### PR #1342 — OPEN, NOT MERGED as of 2026-08-05

Branch `tournament/pre-boss-qwen3-32b`. Two separate changes, often conflated:
1. `quasar` **removed** from `CONTINUOUS_SFT_LINEAGES` (not replaced) → boss tasks 6→5 →
   `required_wins` → **4 of 5**. Margin stays 1%.
2. `PRE_BOSS_MODEL = "Qwen/Qwen3-32B"` becomes the forced model for the **pre-boss** knockout,
   with augmentation, KL and YaRN **disabled**.

The PR also deletes the remote-code auditing subsystem and forces `trust_remote_code=False`
everywhere — quasar was the only custom-arch lineage, which is the real reason it went.

**Re-check merge status before planning around it.**

## 4. Organic tasks are not a miner lever (✅ verified)

`gradients-text-organic` is G.O.D's own infra repo running paying-customer jobs under
`EMISSION_BURN_HOTKEY`, using **the last tournament winner's code**. Miners cannot opt in and
earn nothing directly. The only lever is winning rounds so your code gets promoted. Do not
build an "organic trainer".

## 5. What this codebase already does better than the winners — DO NOT REBUILD

Verified against all 9 fingerprinted winners:

- **Anonymisation / augmentation handling.** `scripts/model_detection.py` reconstructs the
  original base model from an anonymised dir by fingerprinting config fields the validator's
  `scrub_model_identity()` leaves behind, gated at confidence ≥0.9, backed by
  `model_fingerprint_catalog.json`. `detect_augmentation` infers *which* validator augmentation
  was applied from `weight_rms` vs `canonical_weight_rms.json`, and reacts per type. Only one
  winner has anything here, and only a fallback chain.
- **GRPO.** The meta has been frozen 9 weeks (`num_generations=2`, static `beta=0.5`, no
  adaptive KL). We have adaptive divisor-safe `num_generations`, validator-exact checkpoint
  selection on `reward − 0.5·KL` (all 9 winners select on reward alone and ignore the KL
  penalty), a preventive KL-drift governor, and `reward_classifier.py` reward-mix analysis.
- **Early-stop detection.** Adaptive patience from planned epochs, window smoothing so a cosine
  late-dip is not misread as overfit, training-loss-CV override, divergence at 3×init_loss.
  Theirs is a flat 5%/3-evals rule. (The *recovery* half is a real gap — extend, don't replace.)
- **Dataset semantic profiling.** io_jaccard, train_dev_jaccard, dominant script, lang_ratio,
  cot/math/code flags → task-character classification with per-class LR/epoch/NEFTune overrides,
  plus `cross_lingual_detector.py`. Absent from all 9 winners.
- **GP / Expected-Improvement LR proposal** (`bo_augmentation.py`). Every winner uses a fixed
  log-spaced grid.
- **Submission integrity.** NaN/Inf scan of the final checkpoint before shipping, adaptive→legacy
  config cascade with output sanity checks, FAST-CRASH detection.

## 6. Absence findings — the most trustworthy signal available

Two independent audits: 9 winners 2026-05-28 → 2026-07-27, and 14 winners 2025-08-01 →
2026-05-21. Remember section 2: absence is credible, shared presence is not.

### Absent 14/14 across ten months — OPEN FIELD, not proven dead

These are the openings. None of them carries port risk, because nobody has one to port.

| Technique | Note |
|---|---|
| **Held-out LR selection** | The standout. Nine of the fourteen run multi-LR probes and *all* select on training loss, having already built a dev set. Train-loss selection is biased toward the highest stable / most-overfitting run. Top opportunity. |
| **Derived analytic LR** | Never explored; the family invested in brute-force search instead. Looks unexplored, not tested-and-rejected. |
| **Adaptive epoch count** | `epoch_num` is a literal everywhere — yet Lineage D's own in-code ablation records instruct 3→2 after +12% overfit. They *know* epochs matter and set them by hand offline. |
| **Model soup / weight averaging** | Complete dead zone, though souping is standard in other competitive-ML settings. Best-checkpoint machinery already produces the candidates a soup needs. |
| **DPO-specific LR guard** | Untried in every era, despite DPO's known LR sensitivity. |
| **Stratified / leak-controlled split** | Untried; combined with absent dedup, their dev sets are plausibly contaminated. |
| **Per-sample loss filtering** | Untried. |
| **Prompt-loss-weight** | Untried; cheap to test. |

### Absent and probably genuinely not worth it

- **`label_smoothing`** — the one confidently TESTED-AND-REJECTED item, with a number: Lineage D
  records a **+4.48% regression** on a 128K-vocab Llama-3. Do not spend a cycle.
- **NEFTune** — absent 14/14 despite being a one-line `TrainingArguments` flag. Ten months of
  winners declining a free flag is meaningful. ⚠️ **We default `NEFTUNE_NOISE_ALPHA=5.0` for
  instruct — this needs an A/B before it is trusted.**
- **rsLoRA / DoRA** — one-flag PEFT features, absent 14/14. Evidence the uniform
  `r=128 / all-linear` choice is the load-bearing part.
- **Adaptive GRPO `num_generations`** — fixed at 2 everywhere; generations trade directly against
  wall-clock and 2 is the minimum that makes a group-relative advantage computable. Low value.
- **Overfit early-stop** — never wired, and coherently so: they keep training and rely on
  best-checkpoint selection to absorb overfitting. Plausibly tested-and-rejected.
- **Per-layer / discriminative LR** — absent 14/14 and 9/9. No evidence either way on payoff.
- **Data augmentation, Spectrum / LISA / GaLore** — absent throughout.

### Do not treat as dead

**NaN/Inf guards.** No repo implements its own in Python, but several inherit axolotl's
`max_consecutive_nans` / `max_nan_percentage` via `test_axolotl.yml`. Bespoke guards are absent;
framework-level ones may be silently active.

### Converged (table stakes, present throughout)

LoRA `r=128` all-linear, `cosine_with_min_lr` with `min_lr_rate=0.25`, effective batch 64 via
grad accumulation, instruct full-FT below ~9B and LoRA above, DPO/GRPO LoRA from ~2B,
best-checkpoint-not-last, hard deadline management, an OOM degradation ladder, completion-only
loss masking, sequence packing, left-truncation of prompts.

⚠️ Adopt these as *capabilities via framework flags*, not as their code. Several carry
byte-identical implementations across all 14 repos — e.g. the `truncate_prompts` comment
"Keep the last max_length tokens (left truncation)" is verbatim in all of them, and
`dev_size=200 / seed=42 / shuffle-then-slice` is character-identical in 13. Use
`truncation_side='left'`, `load_best_model_at_end`, `sample_packing`, and your own split policy.

Converged across all 9 (table stakes): LoRA `r=128` all-linear, `cosine_with_min_lr` with
`min_lr_rate=0.25`, effective batch 64 via grad accumulation, instruct full-FT below ~9B and
LoRA above, DPO/GRPO LoRA from ~2B, best-checkpoint-not-last, hard deadline management, an OOM
degradation ladder.

## 7. Known gaps in this codebase

Ranked. Paths are relative to the repo root, branch `validator-align`.

| # | Gap | Where | Impact |
|---|---|---|---|
| 1 | DPO LR selected on **training** loss — walks into DPO's degenerate minimiser | `scripts/customized_trainer.py:275`, `scripts/text_trainer.py:745` | critical |
| 2 | No derived/analytic LR; `gradient_noise_scale` and grad-norm p95 are parsed then never consumed | `scripts/baseline_stats_reader.py:9,106` | critical |
| 3 | Still running the abandoned cross-process Redis LR sweep (full container retrain per probe) | `scripts/text_trainer.py:674-790` | high |
| 4 | Plans from an a-priori step-time guess; real measured step time is discarded | `scripts/adaptive_config.py:1826-1838` vs `customized_trainer.py:237` | high |
| 5 | Dataset dedup **off by default** and never exported → ships with no dedup at all | `scripts/data/dedup_knn.py:158`, `scripts/entrypoint.sh` | high |
| 6 | Instruct switches to LoRA at 5B where all 9 winners full-FT to 9B | `scripts/adaptive_config.py:90` | high |
| 7 | Train/dev split is a plain shuffle with fixed `dev_size=200`, no stratification or leak control | `scripts/tokenize_instruct.py:169-218` | medium |
| 8 | WSM soup has no admission test and is disabled on full-FT | `scripts/customized_trainer.py:640-654,746-755` | medium |
| 9 | No validator-exact KL trainer for instruct (the instinct exists, but only for GRPO) | — | medium |
| 10 | OOM ladder stops one rung short (no max_length halving at batch==1) | `scripts/text_trainer.py:165-197` | medium |
| 11 | No `config.json` `architectures` restoration → validator `is_finetune` can fail → score 0 | — | medium |
| 12 | DPO `max_length` driven by the model, not the data | `scripts/train_dpo.py:155-170` | medium |

⚠️ **Gap 6 is coupled to memory sizing.** The multi-GPU batch cap at
`scripts/adaptive_config.py:1211-1218` assumes LoRA memory in the 5–9B band. Change the
threshold and the cap together or you get OOM cascades.

## 8. Liabilities to remove

- **`KITA_STRATEGY` multi-hotkey diversification** (`scripts/adaptive_config.py:2160-2185`) and
  the **"tournament hotkey slot 1..5 variant" marker stubs** (`:2344-2348`). These are a written
  description of the exact pattern T1 auto-eliminates. Remove the mechanism, not just the comments.
- **`reg_ratio` double application** — family profiles apply their own and the CLI value
  multiplies on top (`scripts/adaptive_config.py:2259`), giving some families a compounded LR
  nobody chose. Fix as a bug. Do **not** tune the constant hoping for edge: it is cosmetic to T2
  and noise to scoring.
- **Orphaned `scripts/lr_finder.py`** (Leslie Smith LRRT, imported by nothing) — occupies the
  name and conceptual slot the derived estimator needs.
- **Dead adaptive LoRA rank** — `scripts/adaptive_config.py:94-95` computes a rank the instruct
  run_cmd never emits, so `LoraArguments` defaults silently win.
- **`llm_warmstart.py`** (on `experimental-tournament-2026-05-21`) — another memorised-prior tier
  with a heavy runtime dependency. Do not merge.
- **Inherited family fingerprints** (see section 2b) — `scripts/add_random_noise.py` and the
  `lrs_lookup.py` sha256(model_name) → `lrs/*.json` layout are T1-identical to a published winner
  repo and are named in the audit as this family's loudest identifying artifacts. Keep the *ideas*
  if they earn their place (always emit something; remember which LR worked) but re-implement both
  mechanisms differently, and never reuse those filenames or constants.
- **`lr_utils.extend_learning_rates` + `state_manager` + `MAX_TRIES=9`** — this probe-loop shape
  exists in exactly one lineage, and we inherited it. Single-lineage provenance plus verbatim
  landmark lines makes it the highest port-risk code we carry.

## 9. Strategy leakage

Winner repos get published — and so do dedup-flagged repos. Two distinct exposures:

1. **Source-level.** Print statements and comments describing strategy are visible in the
   published source regardless of runtime suppression. Log-silencing does *not* protect this.
2. **Runtime artefacts.** The validator's own uploader added `ignore_patterns` for
   `trainer_state.json`, `training_args.bin`, `optimizer.pt`, `scheduler.pt`, `scaler.pt`,
   `rng_state*.pth` — its commit message calls the rest "pure strategy leak". Our
   `trainer/utils/hf_upload.py` has **no such patterns** and also syncs wandb logs.

If adding log suppression, use logging configuration — **not** a `builtins.print` monkeypatch,
which is itself distinctive enough to serve as a fingerprint.

## 10. Pre-entry checklist

Do not enter a tournament unless all of these hold:

- [ ] No `KITA_STRATEGY` / hotkey-slot marker mechanism anywhere in the tree
- [ ] `config.json` `architectures` restoration in place
- [ ] OOM ladder includes the max_length rung
- [ ] Repo contract re-diffed against current upstream (LICENSE/NOTICE verbatim, dockerfile path,
      output path `/app/checkpoints/{task_id}/{expected_repo_name}`, full 40-char SHA served)
- [ ] One end-to-end container run passes locally — at minimum one instruct and one DPO task
- [ ] No `trust_remote_code=True` left in any loader
- [ ] Entry cost accepted: text fee is the highest of the three brackets, plus registration burn,
      and ~85% of text emission is burned

## 11. Working agreements

- **Never** copy a winner repo and retune constants. That is the fastest route to elimination.
- **Always** verify a validator claim against cloned source before acting on it — the tournament
  rules change week to week and second-hand summaries go stale fast.
- Escalate to the `strategist` agent once per task for a genuine strategy call or a go/no-go
  before pushing miner code. Delegate mechanical scanning to `worker-haiku`, code-from-spec and
  parallel subsystem reading to `worker-sonnet`. Verify worker output before trusting it.
- Target repo for this work is `lostinjamal`; current branch is `validator-align`
  (equal to `origin/main`).
