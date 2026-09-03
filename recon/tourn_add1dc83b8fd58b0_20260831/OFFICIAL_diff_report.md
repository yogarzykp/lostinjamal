# Tournament Code Comparison: Boss Retained vs Challenger

**Challenger Repository:** https://github.com/yeahteam/txt-tombo-maju-jaya  
**Previous Boss Repository:** https://github.com/gradients-opensource/god-text-tourn-e758aac2d861c378-20260824-position-1.git

**Result:** Boss retained; challenger was 5FpdSckwjnAFrShGtKsPn73HxfyDLBDgnermaqctZtZb6i5g.

---

## Thesis

The challenger lost because it introduced **substantial experimental complexity and untested infrastructure** while the boss maintained a **proven, simpler configuration**. The challenger added transformers v5 support, new LR selection strategies (LES/ladder), multiple environment-gated features, and timing-sensitive execution paths—but internal A/B test logs reveal several of these changes **actively regressed performance**. The boss won by avoiding this experimental debt.

---

## Ranked Winning Deltas (Boss Advantages)

### 1. **Simpler, Proven LR Strategy** (HIGH CONFIDENCE)

**Files inspected:**
- `challenger/scripts/instruct_config.py:27` (`LR_STRATEGY = "les"`)
- `challenger/scripts/lr_finder_les.py` (new 200+ line LES implementation)
- `challenger/scripts/lr_ladder.py` (new 500+ line probe ladder)
- `boss/scripts/instruct_config.py` (no LR_STRATEGY constant)

**What changed:**  
Challenger replaced the boss's direct LR selection with:
- **LES (Leslie Smith) range test** as default (`LR_STRATEGY = "les"` in instruct_config.py)
- **LR ladder probing** (`lr_ladder.py`) with empirical dev-CE scoring across multiple LR candidates
- Complex timing gates: `LADDER_PLAN_FRAC`, `LADDER_DEADLINE_FRAC`, probe step floors

**Why it mattered:**  
The LES finder has documented failure modes on low-entropy tasks (lr_ladder.py:5-8: "burned full-FT 0.3-2B live... SmolLM2-1.7B stuck at base loss, pythia-410m cooked"). The ladder adds 35% sweep overhead (`LADDER_SWEEP_FRACTION = 0.35`) and planning complexity. Boss used simpler `lr_finder.py::estimate_starting_lr()` with established weight-RMS scaling—less overhead, fewer failure modes.

**Confidence:** HIGH—the challenger's own logs show phi-1_5 lost +5.4% with planning/timing issues tied to this infrastructure.

---

### 2. **No Transformers v5 Venv Risk** (MEDIUM-HIGH CONFIDENCE)

**Files inspected:**
- `challenger/dockerfiles/standalone-text-trainer.dockerfile:49-95` (new 47-line v5 venv block)
- `challenger/scripts/v5_venv_selfcheck.py` (new validation script)
- `challenger/scripts/train_instruct.py:50-58` (transformers version gating)
- `boss/dockerfiles/standalone-text-trainer.dockerfile:1-49` (no v5 venv)

**What changed:**  
Challenger added a complete second Python environment (`/workspace/quasar_py`) with:
- `transformers==5.12.1` (vs boss's 4.51.3)
- `torch==2.9.1` cu128 (vs boss's 2.4.0 cu124)
- `trl==1.10.0` (vs boss's 0.18.0—API breaking change)
- Conditional routing via `is_v5_family_model()`, `route_launcher_to_v5_venv()`

**Why it mattered:**  
Version jumps introduce breaking changes. The Dockerfile itself warns: "trl 1.x is an API BREAK... leaving it floating meant a rebuild could silently move the API" (line 68-72). The challenger's RUN_20260821_3task.md shows task 45f9a179 ran stats-less (no LR ladder/probe) because tokenizer fallback failed—"lantai" (floor) LR only. Boss avoided this entire class of version-mismatch risk.

**Confidence:** MEDIUM-HIGH—no direct evidence v5 caused the tournament loss, but it's untested infrastructure added days before submission.

---

### 3. **WSD_SMALL_FULLFT Disabled After Losses** (HIGH CONFIDENCE)

**Files inspected:**
- `challenger/scripts/instruct_config.py:132` (`WSD_SMALL_FULLFT = os.environ.get("SN56_WSD_SMALL", "0") == "1"`)
- `challenger/scripts/instruct_config.py:124-131` (forensic comment)
- `boss/scripts/instruct_config.py` (no WSD feature)

**What changed:**  
Challenger added warmup-stable-decay LR schedule for sub-2B models, then **disabled it by default** after tournament losses. The code comment (lines 124-131) states:

> "DEFAULT FLIPPED TO OFF (tourn_20260803 forensics): the merge put this lever live UNVALIDATED and round 1 of 20260803 was its first deployment — all three tasks were <2B cool full-FT, WSD fired on all three, and we lost all three (ranks 3/4/6)"

**Why it mattered:**  
The challenger shipped with a recently-disabled footgun. Boss never had WSD, avoiding the risk entirely. Even disabled, the presence of untested/regressed code paths increases maintenance surface and suggests rushed development.

**Confidence:** HIGH—explicit admission of 3/3 task losses in challenger's own codebase.

---

### 4. **Timing Budget Fragility** (MEDIUM CONFIDENCE)

**Files inspected:**
- `challenger/scripts/lr_ladder.py:30-34` (timing fraction constants)
- `challenger/tools/RUN_20260821_3task.md:96` ("Dev-pass final skipped for 9 seconds")
- `challenger/tools/AB_DEVFIT_RESERVE_20260822.md` (reserve timing failure)

**What changed:**  
Challenger introduced fine-grained wall-clock planning:
- `LADDER_PLAN_FRAC = 0.85`, `LADDER_DEADLINE_FRAC = 0.92` (lr_ladder.py:31-32)
- Dev-pass reserve calculations in `dev_pass.py`
- Multiple time-based gates competing for limited budget

**Why it mattered:**  
RUN_20260821_3task.md documents phi-1_5 task **lost dev-pass final because of 9 second shortage**: "sem janela (205s restantes < ~214s necessários)". The document calls this "the FOURTH time coin" issue—results decided by second-level budget arithmetic, not training quality. Boss's simpler pipeline has fewer time-sensitive gates.

**Confidence:** MEDIUM—documented phi-1_5 loss includes timing issue, but unclear if boss would handle it better without full boss logs.

---

### 5. **Reduced Infrastructure Complexity** (MEDIUM CONFIDENCE)

**Files inspected:**
- Deleted: `challenger/scripts/core/{create_config.py, docker_utils.py, validators.py, manual_reward_funcs.py}` (7 files, ~800 lines)
- Deleted: `challenger/scripts/{job_handler.py, trainer_downloader.py, download_model_only.py, test_args.py}`
- `boss/scripts/core/models/` (all present)

**What changed:**  
Challenger **deleted** extensive infrastructure the boss had:
- Configuration generators (`create_config.py`)
- Job handlers (`job_handler.py`, `docker_utils.py`)
- Tournament/payload models (`tournament_models.py`, `payload_models.py`)
- Manual reward functions (`manual_reward_funcs.py`)

**Why it mattered:**  
Two interpretations: (1) Challenger is leaner and focused on training only—positive. (2) Challenger removed battle-tested scaffolding that boss relied on—negative. The boss's retention suggests the deleted code provided value. However, the deleted files are mostly **orchestration**, not core training logic, so the impact is indirect.

**Confidence:** MEDIUM—deletion is clear, but causal link to tournament loss is speculative.

---

### 6. **LoRA Target Module Logic Correctness** (LOW-MEDIUM CONFIDENCE)

**Files inspected:**
- `challenger/scripts/train_instruct.py:82-101` (`find_all_linear_names()` with numeric-leaf handling)
- `boss/scripts/train_instruct.py:59-68` (`find_all_linear_names()` simple version)

**What changed:**  
Challenger's `find_all_linear_names()` has special logic to qualify numeric module names (lines 88-101):
```python
# A Linear that lives directly inside an nn.Sequential/nn.ModuleList has a bare NUMERIC
# leaf name — quasar's GLA full-attention layers carry a low-rank gate gk_proj = 
# nn.Sequential(Linear, Linear), i.e. Linears at ...self_attn.gla.gk_proj.0/1. Targeting 
# the bare "0"/"1" makes PEFT suffix-match every model.layers.<n> DECODER LAYER and
# get_peft_model dies...
```

Boss uses simple logic: `lora_module_names.add(names[0] if len(names) == 1 else names[-1])`.

**Why it mattered:**  
Boss's simple approach may incorrectly target `"0"/"1"` module names on models with Sequential layers, causing `get_peft_model` to fail. Challenger fixed this. **However**, this is a challenger *advantage*, not a boss advantage—inverse attribution.

**Confidence:** LOW-MEDIUM (inverted)—challenger fix is technically superior, but if the boss never encountered such models in the tournament, it's moot.

---

## Potential Exploits or Cheating Signals

**No credible exploits detected.**

Inspected suspicious patterns:
- **Dockerfile internet access:** Lines 26-47 install from public PyPI/GitHub only—no hidden model downloads, no eval-time networking
- **Seed floor guard (`seed_floor.py`):** Ships base seed when trained adapter doesn't improve—**legitimate optimization** for continuous-SFT tasks, not cheating. The code is transparent (logs decision), respects PEFT architecture gates, and the validator's finetune check is architecture-only (comment line 7-11 explicitly notes this loophole is legal)
- **Submission validity (`submission_validity.py`):** Validates artifacts prevent zero-tensor DeepSpeed bugs—defensive, not exploitative
- **No hardcoded answers:** Grepped dataset/eval paths—all load from task-provided data

The challenger's complexity comes from **over-engineering training hyperparameters**, not circumventing evaluation.

---

## Out of Scope

- **Deleted orchestration files** (`scripts/core/create_config.py`, `job_handler.py`, `docker_utils.py`, `tournament_models.py`, `payload_models.py`, `validators.py`): Configuration and job management—not training behavior
- **Test suite expansion** (60+ new `test_helpers/test_*.py` files): Unit tests for features—doesn't affect runtime
- **Markdown documentation** (`tools/*.md`): A/B test reports, forensics—evidence of experimentation, not training code
- **Logging/quiet mode** (`quiet_mode.py`, `utility.py` log_info changes): Output formatting only
- **`.gitignore` updates:** Development hygiene

---

## Porting Recommendations

**Do NOT port from challenger to boss:**
1. **LES LR strategy default** (`LR_STRATEGY = "les"`)—documented failures on low-entropy tasks
2. **LR ladder probing**—35% sweep overhead, timing fragility
3. **Transformers v5 venv**—unless validator mandates v5-family models, avoid the version risk
4. **WSD_SMALL_FULLFT**—already disabled in challenger after losses

**Consider porting (low risk):**
1. **`submission_validity.py`**—defensive zero-tensor detection for DeepSpeed
2. **Numeric-leaf LoRA fix** (`find_all_linear_names()` in train_instruct.py:88-101)—prevents `get_peft_model` crashes on Sequential layers
3. **`seed_floor.py`** (if continuous-SFT tasks appear)—provably beneficial when seed is already optimal

**Boss should remain stable.** The challenger's internal A/B logs show it was actively testing and **disabling failed experiments**. The boss represents the pre-experiment baseline that won by not taking those risks.
