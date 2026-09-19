# Tournament Repository Comparison: Challenger vs Previous Boss

**Challenger:** https://github.com/bodhinaime/fivtytricks  
**Previous Boss:** https://github.com/gradients-opensource/god-text-tourn-5c64e784a087074a-20260914-position-1.git  
**Result:** Boss retained; challenger was 5CkYizfLyb5hLmcK4WtBGG13WKTQrynHBEV6qC23748g17zC.

## Thesis

The challenger lost due to **dramatically reduced effective batch sizes for mid-to-large models (12B-40B)**, coupled with a DeepSpeed ZeRO-3 → ZeRO-2 migration. The batch size reduction (30→16 for 12-15B models, yielding a 47% effective batch size drop from 120→64) introduced noisier gradient estimates and likely degraded training convergence. While the challenger added extensive telemetry infrastructure, improved error handling, and modernized dependencies, these non-training improvements could not compensate for the core hyperparameter regression.

---

## Ranked Winning Deltas (Boss Advantages)

### 1. **Effective Batch Size Reduction for 12-15B Models** ⭐⭐⭐ (HIGH confidence)
**Files:** `scripts/instruct_config.py` lines 64-79 (challenger) vs 64-69 (boss)

**What changed:**
- Boss: `"12_15_b": {"batch_size": 30, "distributed": "ds", "gpu_count": 4}`
- Challenger: `"12_15_b": {"batch_size": 16, "distributed": "ds", "ds_stage": 2, "gpu_count": 4}`
- Effective batch size calculation (both): `data_per_step = batch_size * gpu_count` → `grad_accum = 1 if data_per_step >= 64 else int(64/data_per_step)`
- **Boss effective batch:** 30 × 4 = 120 samples/step (gradient_accumulation_steps=1)
- **Challenger effective batch:** 16 × 4 = 64 samples/step (gradient_accumulation_steps=1)
- **Net impact:** 47% reduction in effective batch size (120 → 64)

**Why it mattered:**  
Smaller effective batch sizes produce noisier gradient estimates, reducing training stability and potentially degrading convergence quality. The 12-15B bucket is a critical model size range, and a 47% batch size cut directly reduces the signal-to-noise ratio in gradient updates. The challenger's inline comment claimed "gradient accumulation restores the 64-example effective batch," but the boss already ran at 120—this was a regression, not a restoration.

**Confidence:** HIGH. Batch size is a first-order hyperparameter. Halving it (or worse) is among the most direct paths to performance degradation in fine-tuning.

---

### 2. **Effective Batch Size Reduction for 15-40B Models** ⭐⭐ (MEDIUM-HIGH confidence)
**Files:** `scripts/instruct_config.py` lines 80-87 (challenger) vs 70-76 (boss)

**What changed:**
- Boss: `"15_40_b": {"batch_size": 18, "distributed": "ds", "gpu_count": 4}`
- Challenger: `"15_40_b": {"batch_size": 4, "distributed": "ds", "ds_stage": 2, "gpu_count": 4}`
- **Boss effective batch:** 18 × 4 = 72 samples/step (gradient_accumulation_steps=1)
- **Challenger effective batch:** 4 × 4 × 4 = 64 samples/step (gradient_accumulation_steps=4)
- **Net impact:** 11% reduction in effective batch size (72 → 64)

**Why it mattered:**  
While the effective batch size reduction is smaller (11%), the per-device micro-batch dropped 78% (18→4). This introduces more gradient accumulation steps, which can interact poorly with batch normalization layers (if present) and increases communication overhead in distributed training. The ZeRO-2 migration (see #3) was justified by claiming a replicated base model, but the aggressive micro-batch cut suggests the memory budget was miscalculated or the batch size was over-conservatively tuned.

**Confidence:** MEDIUM-HIGH. The effective batch size drop is modest, but the micro-batch collapse is severe and likely introduced secondary inefficiencies.

---

### 3. **DeepSpeed ZeRO-3 → ZeRO-2 Migration for 12-40B Models** ⭐ (MEDIUM confidence)
**Files:** `scripts/instruct_config.py` lines 64-87, `scripts/ds_config/zero2.json` (new file)

**What changed:**
- Boss used ZeRO-3 for all DeepSpeed jobs (12B+ models): `--deepspeed ds_config/zero3.json` (hardcoded, line 176 in boss)
- Challenger introduced dynamic stage selection: `ds_stage = int(config.get("ds_stage", 3))` (line 187), explicitly set `"ds_stage": 2` for 12-15B and 15-40B buckets
- ZeRO-2 replicates the full model per GPU (partitions only gradients/optimizer states), while ZeRO-3 partitions model parameters across GPUs

**Why it mattered:**  
The challenger's comment (lines 64-70) claims ZeRO-2 avoids "per-layer param all-gather in forward or backward" for LoRA fine-tuning, where the frozen base is small enough to replicate. This is architecturally sound for memory-fitting models, but:
1. The batch size reductions were still applied, suggesting memory pressure wasn't actually relieved
2. ZeRO-3's parameter sharding can enable *larger* effective batches by freeing memory; the move to ZeRO-2 may have forced the batch size cuts
3. The migration was not A/B tested—if ZeRO-2 had a correctness or convergence bug on this version, it would manifest silently

**Confidence:** MEDIUM. The ZeRO stage change is plausible on paper but was coupled with batch size cuts that negate the claimed benefit. Without telemetry showing ZeRO-2 runs completed faster or with lower memory, this reads as a premature optimization that enabled a regression.

---

### 4. **Logging Overhead Increase** ⭐ (LOW confidence, overhead only)
**Files:** `scripts/instruct_config.py` line 162 (boss) vs 173 (challenger)

**What changed:**
- Boss: `--logging_steps 5`
- Challenger: `--logging_steps 1`

**Why it mattered:**  
Logging every step instead of every 5th step increases I/O and synchronization overhead. On a 4-GPU job, this means 5× more frequent logging events. While the actual cost is small (milliseconds per step), it compounds over thousands of steps and could contribute to slightly slower throughput.

**Confidence:** LOW. This is a minor overhead issue, not a training quality regression. Unlikely to affect loss directly, but could reduce the number of steps completed within the time budget.

---

## Potential Exploits or Cheating Signals

**No credible exploits detected.** The challenger's changes are primarily infrastructure improvements and hyperparameter adjustments. Specific checks:

1. **Dockerfile internet access:** The challenger upgraded dependencies (torch 2.4→2.8, transformers→5.12.1, added native tokenization) but all installs are from public package indices (PyPI, GitHub releases, torch wheels). No hidden downloads of pretrained weights or external data during training detected.

2. **Native tokenization (`scripts/native_tokenize.py`):** Replaces axolotl dependency with a custom implementation. The file includes extensive validation claims: "verified identical to axolotl's output across five tokenizer families (Qwen3, Llama-3, Mistral-v0.3, Gemma-2, Phi-4-mini)" with test harness at `scripts/test_helpers/test_native_tokenize.py`. **No red flags**—this is a legitimate dependency removal to shrink the Docker image (67.3GB→18.2GB claimed).

3. **Telemetry system:** New files `telemetry.py`, `telemetry_callback.py`, `save_guard.py` are read-only instrumentation—no training behavior changes, no external communication. The telemetry is explicitly file-based (writes to `/app/checkpoints/{task_id}/telemetry/events.jsonl`) and survives container destruction for post-run analysis. **Legitimate observability improvement.**

4. **Second trajectory (`scripts/second_trajectory.py`):** Implements a second training pass with annealed LR schedule and model soup. This is a valid advanced technique (references Wortsman et al., model soup paper). The module is explicitly gated (`SN56_SECOND_TRAJECTORY=0` disables it) and only runs after the first trajectory completes. **No exploit—this is a legitimate ensemble method**, though it wasn't enabled by default in the boss and may not have fired in the challenger's losing run.

5. **Attention fallback (`train_instruct.py` lines 109-173):** Adds a flash_attention_2 → sdpa → eager fallback ladder to handle architecture incompatibilities. This prevents crashes on models that reject flash attention, but uses deterministic fallback logic. **No exploit—defensive programming.**

**Conclusion:** The challenger made legitimate infrastructure improvements. The loss is attributable to hyperparameter regressions (batch size cuts), not cheating.

---

## Out of Scope (Infrastructure-Only Changes)

- **Docker base image upgrade:** `runpod/pytorch:2.4.0-py3.11-cuda12.4.1` → `2.8.0-py3.11-cuda12.8.1-cudnn` (line 13 in challenger dockerfile)
- **Axolotl venv removal:** Replaced 7.82GB `/workspace/axo_py` virtualenv with native tokenization implementation
- **Flash-attention wheel:** Switched from source build to prebuilt wheel (v2.7.4→v2.8.3, line 49 in challenger dockerfile)
- **GRPO venv isolation:** New `/workspace/grpo_py` virtualenv for vllm (torch 2.11 compatibility, lines 58-64)
- **Exception tracking improvements:** `text_trainer.py` lines 181-238 (challenger) add `exception_from_log()`, `attempt_end_fields()`, per-attempt log files
- **OOM recovery:** Max-length reduction fallback (lines 392-416 in challenger `text_trainer.py`)
- **Checkpoint save guard:** `save_guard.py` prevents failed saves from ending training attempts
- **Cosine schedule progress clamp:** `customized_trainer.py` lines 25-109 (challenger) prevents LR re-warming on overruns
- **Telemetry emissions:** ~30 new `tm.emit()` calls across training scripts (no training behavior impact)

---

## Porting Recommendations

**To recover boss performance while keeping challenger infrastructure improvements:**

1. **Restore boss batch sizes for 12-40B models** (CRITICAL):
   - `instruct_config.py` line 78: `"batch_size": 16` → `30` (12_15_b)
   - `instruct_config.py` line 86: `"batch_size": 4` → `18` (15_40_b)

2. **Revert to ZeRO-3 for 12-40B buckets** (RECOMMENDED):
   - Remove `"ds_stage": 2` from lines 75, 83 in `instruct_config.py` (falls back to default ZeRO-3)
   - The ZeRO-2 migration's claimed memory benefit didn't materialize (batch sizes were still cut), and ZeRO-3's parameter sharding is more robust for large models

3. **Optional: Revert logging frequency** (MINOR):
   - `instruct_config.py` line 173: `--logging_steps 1` → `5` to reduce overhead
   - Keep `1` if the telemetry system requires per-step granularity for post-hoc analysis

4. **Keep all infrastructure improvements** (SAFE):
   - Telemetry system, save_guard, native_tokenize, second_trajectory, attention fallback, cosine clamp, OOM recovery, exception tracking
   - These are defensive/observability features with no downside

5. **A/B test second trajectory separately:**
   - `second_trajectory.py` is disabled by default (`SN56_SECOND_TRAJECTORY=0`)
   - If enabled, verify it runs only when slack budget exists and doesn't perturb attempt 0
   - Could be a future win, but isolate it from the batch size fix

**Estimated impact:** Restoring batch sizes alone should recover most of the performance gap. The 47% effective batch size cut for 12-15B models is the single largest regression and is trivially reversible.
