#!/usr/bin/env bash
# Exercise the GRPO code path end to end on a 135M model, in about 15 minutes.
#
#   base model  unsloth/SmolLM-135M-Instruct (already in the HF cache on the box)
#   prompts     synthesized from the R1 GossipCop file by make_grpo_data.py
#   reward      reward_specific_word_count, weight 1.0 — one of the 13 generic
#               tournament reward functions (reward_classifier.py:REWARD_CATALOG)
#
# Unlike run_instruct_replay.sh, this run does NOT end in a number you can put
# on a leaderboard. There is no held-out GRPO set here, and a 135M model
# generating for nine minutes produces a reward that means nothing about
# quality. What it proves is that the path runs: dataset_type parses, the
# reward function survives train_grpo.validate_reward_function's exec-and-assert,
# tokenize_grpo splits, TRL samples num_generations completions per prompt,
# advantages are non-degenerate, the backward pass lands, the deadline callback
# fires, and a checkpoint reaches the submission dir. Every one of those is a
# thing that has killed a real GRPO task at step 0 or step 500 before.
#
# Read the log for: "Using reward function 0", "supports_extra: False",
# "[classifier] tier 1.5 hit", the reward/kl columns in the training logs
# (reward must MOVE — a flat reward means zero advantage and the run proved
# nothing), "[deadline] stopping at step N", and the copytree into submission.
#
# Stages exist so a failure is attributable, and so the expensive-and-risky
# variant is never the default. Stage a is what a real small-model GRPO task
# takes today. The other two turn vLLM on, which is a 32GB reservation on a
# GPU that is usually already occupied — hence the GPU_IS_FREE gate.
#
# Usage:  ./run_grpo_smoke.sh <stage>     stage = a | legacy | vllm
set -euo pipefail

STAGE="${1:-a}"

# A NEW task id, deliberately not 865ff4ab… — the trainer keys its dataset cache
# path by task id, so reusing the instruct replay's id would overwrite 19,505
# rows of GossipCop with 512 prompts. make_grpo_data.py refuses to do that, but
# the right fix is to not ask.
TASK_ID="${TASK_ID:-9f1c2d3e-4b5a-6c7d-8e9f-0a1b2c3d4e5f}"
MODEL="${MODEL:-unsloth/SmolLM-135M-Instruct}"
HOURS="${HOURS:-0.25}"
REPO_NAME="${REPO_NAME:-grpo-smoke-${STAGE}}"

WORK="${WORK:-$HOME/smoke}"
DATA_DIR="$WORK/data"
OUT_DIR="$WORK/out/grpo-$STAGE"
LOG="$WORK/logs/grpo-${STAGE}.log"

SMOKE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$DATA_DIR" "$OUT_DIR" "$WORK/logs"

# The trainer reads its dataset from a fixed cache path (train_cst.CACHE_DATASETS_DIR
# via train_paths.get_text_dataset_path) keyed by task id — the --dataset argument
# below is required by the parser and then never read. So the file has to be named
# for the task we claim to be running.
TRAIN_JSON="/cache/datasets/${TASK_ID}_train_data.json"

# Only make_grpo_data.py honours this. train_cst.py hardcodes /cache/datasets as a
# module constant with no env read, so pointing this elsewhere lets you dry-run the
# synthesis step off-box but does NOT redirect the trainer.
export CACHE_DATASETS_DIR="${CACHE_DATASETS_DIR:-/cache/datasets}"

# Row cap. GRPO generates num_generations completions for every prompt at every
# step, so a step here costs ~batch x num_gen x max_completion tokens of
# generation — on this config, 40 x 8 x 512. Rows are therefore not what bounds
# the run (the deadline is); the cap keeps adaptive's tiny-model step formula
# — int(max(50, rows / (batch x gpus)) * 1.5) — from setting a target the budget
# cannot reach, and keeps tokenize instant. 200 of these rows are taken for dev
# by tokenize_grpo before training sees any.
export GRPO_ROWS="${GRPO_ROWS:-512}"
export GRPO_PROMPT_WORDS="${GRPO_PROMPT_WORDS:-120}"
export GRPO_TARGET_WORDS="${GRPO_TARGET_WORDS:-60}"
export GRPO_SEED="${GRPO_SEED:-42}"
export GRPO_SRC="${GRPO_SRC:-/cache/datasets/865ff4ab-78f2-454d-9d0b-8be506ef42f8_train_data.json}"
export GRPO_DATASET_TYPE_OUT="${GRPO_DATASET_TYPE_OUT:-$DATA_DIR/${TASK_ID}_dataset_type.json}"
export TASK_ID

# ---------------------------------------------------------------------------
# Stage switches.
#
# vLLM is the whole axis here. Under ADAPTIVE_MODE (the default), GRPO on a
# model below 500M params auto-disables it — adaptive_config's tiny-model rule,
# added after opt-350m hung on vLLM startup — so stage a generates through HF
# and needs no extra GPU memory. Both other stages hand vLLM 0.4 of the card in
# colocate mode: ~32GB on an H100. Do not run them next to another container.
# ---------------------------------------------------------------------------
require_free_gpu() {
  if [ "${GPU_IS_FREE:-0}" != "1" ]; then
    echo "stage '$STAGE' starts vLLM with vllm_gpu_memory_utilization=0.4 (~32GB on an H100)." >&2
    echo "Confirm nothing else holds the GPU, then re-run with GPU_IS_FREE=1." >&2
    exit 2
  fi
}

case "$STAGE" in
  a)
    # The everyday path: adaptive config, HF generation, no vLLM.
    export ADAPTIVE_MODE=1
    unset FORCE_VLLM || true
    unset DISABLE_VLLM_OVERRIDE || true
    ;;
  legacy)
    # grpo_config.py's bucket path (0_1_b: lr 8e-6, batch 40, num_generations 2).
    # No tiny-model rule lives here, and get_use_vllm() says yes for this
    # architecture — so legacy WILL start vLLM. That asymmetry with stage a is
    # the point of running this at all.
    require_free_gpu
    export ADAPTIVE_MODE=0
    unset FORCE_VLLM || true
    ;;
  vllm)
    # Adaptive config with the tiny-model auto-disable overridden. Proves the
    # colocate path comes up on a model small enough that we normally refuse it.
    require_free_gpu
    export ADAPTIVE_MODE=1
    export FORCE_VLLM=1
    ;;
  *)
    echo "unknown stage '$STAGE' (want: a | legacy | vllm)" >&2
    exit 2
    ;;
esac

# Pinned rather than left to default: these two decide whether the advantage is
# normalized per group at all, which is the mechanism the whole test is about.
export TRAINING_GRPO_LOSS_TYPE="${TRAINING_GRPO_LOSS_TYPE:-bnpo}"
export TRAINING_GRPO_SCALE_REWARDS="${TRAINING_GRPO_SCALE_REWARDS:-True}"

export TRAINING_TELEMETRY_PATH="$OUT_DIR/run_telemetry.jsonl"

echo "=== stage $STAGE · task $TASK_ID · model $MODEL · ${HOURS}h ==="
env | grep -E "^(ADAPTIVE_MODE|FORCE_VLLM|DISABLE_VLLM_OVERRIDE|TRAINING_GRPO_|TRAINING_REWARD_CLASSIFIER|GRPO_|CACHE_DATASETS_DIR)" | sort | sed 's/^/  /'
echo

# Synthesize the dataset AND the dataset_type in one place. The reward function
# source lives inside the dataset_type JSON, and make_grpo_data.py runs
# train_grpo.validate_reward_function's own checks against it before writing —
# so what gets validated on CPU is byte-identical to what gets passed below,
# and a broken reward function costs a second instead of a model load.
python3 "$SMOKE_DIR/make_grpo_data.py"
echo

DATASET_TYPE="$(cat "$GRPO_DATASET_TYPE_OUT")"

cd "${REPO_DIR:-$HOME/lostinjamal}/scripts"

# hours-to-complete is the real budget knob: text_trainer sets end_time to
# start + hours − 3min, and the GRPO callback evaluates, saves and stops once
# under save_before_remaining_time (3) minutes remain. 0.25h therefore means
# roughly nine minutes of training, then a checkpoint. The deadline is only
# checked at step boundaries, which is the other reason to keep per-step
# generation small.
python -m text_trainer \
  --task-id "$TASK_ID" \
  --model "$MODEL" \
  --dataset "$TRAIN_JSON" \
  --dataset-type "$DATASET_TYPE" \
  --task-type GrpoTask \
  --file-format json \
  --hours-to-complete "$HOURS" \
  --expected-repo-name "$REPO_NAME" \
  2>&1 | tee "$LOG"

echo
echo "=== log: $LOG"
echo "=== telemetry: $TRAINING_TELEMETRY_PATH"
echo "=== dataset: $TRAIN_JSON"
echo "=== dataset-type: $GRPO_DATASET_TYPE_OUT"
echo "=== submission: /app/checkpoints/$TASK_ID/$REPO_NAME"
