#!/usr/bin/env bash
# Replay a real R1 tournament task and measure where we would have placed.
#
# Task 865ff4ab-78f2-454d-9d0b-8be506ef42f8 (2026-08-03, tourn_79c20b9b66ecda90):
#   base model  unsloth/SmolLM-135M-Instruct
#   dataset     Jinyan1/GossipCop, 19,505 train rows
#   held-out    1,000 rows — the set the validator actually scored on
#   leaderboard 1st 1.3863 · 2nd 1.4351 · 3rd 1.5186 · … · 8th 3.6580
#               rank 1 scored 3.0, everyone else 0.0
#
# This is not a "does it start" check. We have the real held-out set, so the run
# ends with a number that can be placed directly on that leaderboard.
#
# Stages exist so a failure is attributable. Everything committed since
# 2026-08-05 has been unit-tested but never executed on a GPU, so stage A runs
# with all of it switched off and establishes what the code did BEFORE any of
# this work. Stage B turns it on. Anything that moves between them is ours.
#
# Usage:  ./run_instruct_replay.sh <stage>     stage = a | a0 | b | kl
set -euo pipefail

STAGE="${1:-a}"
TASK_ID="${TASK_ID:-865ff4ab-78f2-454d-9d0b-8be506ef42f8}"
MODEL="${MODEL:-unsloth/SmolLM-135M-Instruct}"
HOURS="${HOURS:-0.25}"
REPO_NAME="${REPO_NAME:-smoke-${STAGE}}"

WORK="${WORK:-$HOME/smoke}"
DATA_DIR="$WORK/data"
OUT_DIR="$WORK/out/$STAGE"
LOG="$WORK/logs/${STAGE}.log"

mkdir -p "$DATA_DIR" "$OUT_DIR" "$WORK/logs"

# The trainer reads its dataset from a fixed cache path (train_cst.CACHE_DATASETS_DIR)
# keyed by task id, so the file has to be named for the task we claim to be running.
TRAIN_JSON="/cache/datasets/${TASK_ID}_train_data.json"

DATASET_TYPE='{"field_instruction":"instruct","field_input":"input","field_output":"output"}'

# ---------------------------------------------------------------------------
# Stage switches. Default-on features are forced OFF in stage A so that stage is
# a clean measurement of the pre-existing code path.
# ---------------------------------------------------------------------------
case "$STAGE" in
  a)
    export ADAPTIVE_MODE=1
    export INSTRUCT_DEDUP=0
    export BASELINE_USE_COMPLETION_LOSS=0
    export BASELINE_USE_SEQLEN=0
    export BASELINE_USE_NEARDUP=0
    export BASELINE_USE_DPO_GAP=0
    export TRAINING_WSM_GATE=0
    export INSTRUCT_SPLIT_POLICY=0
    export EMIT_PER_EXAMPLE_LOSSES=1   # observational, safe in every stage
    export REG_RATIO_ARG="--reg-ratio 1.1874"   # the value that was live before 2026-08-05
    unset USE_KL KL_COEF || true
    ;;
  a0)
    # Control arm for the A/B: every feature OFF, but reg_ratio left at the neutral
    # 1.0 that stage b uses. Stage `a` also carries the historical reg_ratio 1.1874,
    # so an a-vs-b comparison confounds "our features" with a 19% learning-rate
    # change and cannot answer which one moved the number. This arm isolates the
    # features; `a` vs `a0` isolates the learning rate.
    export ADAPTIVE_MODE=1
    export INSTRUCT_DEDUP=0
    export BASELINE_USE_COMPLETION_LOSS=0
    export BASELINE_USE_SEQLEN=0
    export BASELINE_USE_NEARDUP=0
    export BASELINE_USE_DPO_GAP=0
    export TRAINING_WSM_GATE=0
    export INSTRUCT_SPLIT_POLICY=0
    export EMIT_PER_EXAMPLE_LOSSES=1
    export REG_RATIO_ARG=""            # neutral 1.0, same as stage b
    unset USE_KL KL_COEF || true
    ;;
  b)
    export ADAPTIVE_MODE=1
    export INSTRUCT_DEDUP=1
    export BASELINE_USE_COMPLETION_LOSS=1
    export BASELINE_USE_SEQLEN=1
    export BASELINE_USE_NEARDUP=1
    export BASELINE_USE_DPO_GAP=1
    export TRAINING_WSM_GATE=1
    export EMIT_PER_EXAMPLE_LOSSES=1
    export REG_RATIO_ARG=""            # defaults to 1.0
    unset USE_KL KL_COEF || true
    ;;
  kl)
    export ADAPTIVE_MODE=1
    export INSTRUCT_DEDUP=1
    export BASELINE_USE_COMPLETION_LOSS=1
    export BASELINE_USE_SEQLEN=1
    export BASELINE_USE_NEARDUP=1
    export BASELINE_USE_DPO_GAP=1
    export TRAINING_WSM_GATE=1
    export EMIT_PER_EXAMPLE_LOSSES=1
    export REG_RATIO_ARG=""
    # KL is disabled in R1, so this stage cannot be ranked against the
    # leaderboard. It exists to prove the path executes at the top of the
    # validator's coefficient range.
    export USE_KL=1
    export KL_COEF=1.5
    ;;
  sb0|sb1)
    # Step-budget A/B (2026-09-04). Both arms are stage `b` — our full shipping config —
    # because the question is not "do our features help" but "does the LR schedule finishing
    # inside the budget beat one the deadline truncates". Everything except the step plan is
    # held identical.
    #
    #   sb0  control    max_steps=-1, schedule laid over the full epoch plan, cut by the
    #                   deadline callback partway down the cosine.
    #   sb1  treatment  max_steps=EXPT_MAX_STEPS, measured from sb0's actual stopping point,
    #                   so the same number of steps carries a schedule that reaches its floor.
    export ADAPTIVE_MODE=1
    export INSTRUCT_DEDUP=1
    export BASELINE_USE_COMPLETION_LOSS=1
    export BASELINE_USE_SEQLEN=1
    export BASELINE_USE_NEARDUP=1
    export BASELINE_USE_DPO_GAP=1
    export TRAINING_WSM_GATE=1
    export EMIT_PER_EXAMPLE_LOSSES=1
    export REG_RATIO_ARG=""
    unset USE_KL KL_COEF || true
    if [ "$STAGE" = "sb1" ]; then
      # Refuse to run the treatment as a silent copy of the control. An arm that quietly
      # loses its one distinguishing variable still produces a number, and that number
      # reads exactly like a null result.
      [ "${EXPT_MAX_STEPS:-0}" -gt 0 ] 2>/dev/null || {
        echo "stage sb1 needs EXPT_MAX_STEPS=<steps> — without it this is just sb0" >&2
        exit 2
      }
      export EXPT_MAX_STEPS
    else
      unset EXPT_MAX_STEPS || true
    fi
    ;;
  *)
    echo "unknown stage '$STAGE' (want: a | a0 | b | kl | sb0 | sb1)" >&2
    exit 2
    ;;
esac

export TRAINING_TELEMETRY_PATH="$OUT_DIR/run_telemetry.jsonl"

echo "=== stage $STAGE · task $TASK_ID · model $MODEL · ${HOURS}h ==="
env | grep -E "^(ADAPTIVE_MODE|INSTRUCT_DEDUP|BASELINE_USE_|TRAINING_WSM_GATE|EMIT_PER_EXAMPLE|USE_KL|KL_COEF)" | sort | sed 's/^/  /'
echo

cd "${REPO_DIR:-$HOME/lostinjamal}/scripts"

# shellcheck disable=SC2086
python -m text_trainer \
  --task-id "$TASK_ID" \
  --model "$MODEL" \
  --dataset "$TRAIN_JSON" \
  --dataset-type "$DATASET_TYPE" \
  --task-type InstructTextTask \
  --file-format json \
  --hours-to-complete "$HOURS" \
  --expected-repo-name "$REPO_NAME" \
  $REG_RATIO_ARG \
  2>&1 | tee "$LOG"

echo
echo "=== log: $LOG"
echo "=== telemetry: $TRAINING_TELEMETRY_PATH"
echo "=== submission: /app/checkpoints/$TASK_ID/$REPO_NAME"
