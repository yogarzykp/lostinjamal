#!/usr/bin/env bash
# Exercise the DPO training path on a preference set we synthesise ourselves.
#
# Unlike run_instruct_replay.sh this is NOT a replay. R1 gave us an instruct task and
# no DPO task, so there is no held-out set, no leaderboard, and no number here that
# can be compared with anyone. The question is narrower and, right now, more urgent:
# does the DPO path in this repo still run? Since the last time a DPO task trained on
# this code we have changed tokenize_dpo's split (data/split_policy.leak_safe_split),
# train_dpo's max_length override, the LR-probe scoring (DPO_PROBE_EVAL), the
# per-layer LR hook and the adaptive batch buckets. All of it is unit-tested. None of
# it has executed on a GPU against a real chosen/rejected file.
#
# What a green run proves: the dataset lands where text_trainer looks for it, the
# column rename produces TRL's three columns, dpo_config's template builds a command
# train_dpo accepts, DPOTrainer trains under CustomEvalSaveCallback, the LR state
# machine (initial → continue → finish) completes, and a submission is written to
# /app/checkpoints/<task>/<repo>.
#
# What it does not prove: anything about DPO quality. 135M model, a few thousand rows,
# and a preference task (match the answer to its own article) whose ceiling is far
# below a tournament one. Read the losses as pass/fail for a code path, never as a
# score. make_dpo_data.py explains why the pairs are still a real signal rather than
# noise — that is what makes a broken run distinguishable from a working one, and it
# is the whole of what the numbers are good for.
#
# Stages exist so a failure is attributable, same as the instruct replay:
#
#   a    Pre-2026-08-05 behaviour wherever it is still reachable: LR probes scored on
#        training loss, no validator-baseline signals. This is the code as it ran the
#        last time a DPO task was scored.
#   b    Everything on. Anything that moves between a and b is ours.
#   gap  Stage b plus a synthetic validator baseline_stats carrying a wide
#        implicit_reward_gap. No DPO task has ever handed us that file, so
#        baseline_signals.dpo_epoch_guard has never executed against a live number;
#        this stage makes it, and the log line it prints is the deliverable. Not
#        comparable with a or b — it deliberately changes the training plan.
#
# Two honest limits on stage a. tokenize_dpo.py has no equivalent of
# INSTRUCT_SPLIT_POLICY, so the leak-safe split runs in every stage and cannot be
# switched off from here. And with no BASELINE_STATS_PATH set, the BASELINE_USE_*
# switches in stages a and b are reads that find nothing — which is why the gap stage
# exists at all.
#
# Usage:  ./run_dpo_smoke.sh <stage>     stage = a | b | gap
set -euo pipefail

STAGE="${1:-a}"

# A NEW task id, not the instruct replay's. The dataset file, the checkpoint dir and
# the request JSON are all keyed by it, and make_dpo_data.py refuses to write over the
# source file if this is ever pasted wrong.
TASK_ID="${TASK_ID:-2f7c1a90-5b3e-4a41-9c2f-7d1b6e0a48c3}"
SOURCE_TASK_ID="${SOURCE_TASK_ID:-865ff4ab-78f2-454d-9d0b-8be506ef42f8}"
MODEL="${MODEL:-unsloth/SmolLM-135M-Instruct}"
HOURS="${HOURS:-0.25}"
REPO_NAME="${REPO_NAME:-dpo-smoke-${STAGE}}"

# Row cap. Sized for the quarter-hour budget, with room above the effective batch —
# a 135M DPO task takes the batch=64 bucket, and train_dpo.py:304 divides by that with
# no floor before the eval handler takes a modulo of the result.
ROWS="${ROWS:-3000}"
SEED="${SEED:-42}"

WORK="${WORK:-$HOME/smoke}"
OUT_DIR="$WORK/out/dpo-$STAGE"
LOG="$WORK/logs/dpo-${STAGE}.log"

mkdir -p "$OUT_DIR" "$WORK/logs"

SMOKE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="${REPO_DIR:-$HOME/lostinjamal}"

# Same fixed cache path the instruct replay relies on (train_cst.CACHE_DATASETS_DIR +
# training_paths.get_text_dataset_path). --dataset below is passed for the record;
# text_trainer derives this path from the task id and reads that instead.
TRAIN_JSON="/cache/datasets/${TASK_ID}_train_data.json"

# Must agree with the column constants in make_dpo_data.py. Names that are not TRL's
# own, so tokenize_dpo._adapt_dpo_columns_to_trl actually has a rename to perform.
# field_system / prompt_format / chosen_format / rejected_format exist on
# DpoDatasetType but nothing on this path reads them, so they are left out.
DATASET_TYPE='{"field_prompt":"question","field_chosen":"chosen_response","field_rejected":"rejected_response"}'

# ---------------------------------------------------------------------------
# Stage switches, resolved before anything is written — a typo'd stage should not
# leave a synthesised dataset behind.
#
# Only switches that a DPO run actually reads appear here. Left out on purpose:
# the instruct-only ones (INSTRUCT_DEDUP, INSTRUCT_SPLIT_POLICY, TRAINING_WSM_GATE,
# BASELINE_USE_COMPLETION_LOSS, BASELINE_USE_NEARDUP, EMIT_PER_EXAMPLE_LOSSES),
# which nothing on the way to train_dpo.py reads, and TRAINING_BO_AUGMENT, which
# predates the work under test and is therefore left at its default in every stage.
# Setting any of them here would only suggest this run had tested them.
# ---------------------------------------------------------------------------
STATS_JSON=""

case "$STAGE" in
  a)
    export ADAPTIVE_MODE=1
    export DPO_PROBE_EVAL=0            # probes scored on training loss, as before
    export BASELINE_USE_SEQLEN=0
    export BASELINE_USE_DPO_GAP=0
    # Per-layer LR reads as a default-off feature today, but per_layer_optimizer.py's
    # own docstring dates that default to 2026-08-05 — before then it applied unasked.
    # Stage a therefore has to turn it ON to reproduce what ran last. Its size gate
    # does not save us on a 135M model either: the gate only fires when
    # PER_LAYER_LR_PARAM_NUMS is set, and nothing in this repo sets it.
    export PER_LAYER_LR_ENABLED=1
    export REG_RATIO_ARG="--reg-ratio 1.1874"   # the value that was live before 2026-08-05
    unset BASELINE_STATS_PATH || true
    ;;
  b)
    export ADAPTIVE_MODE=1
    export DPO_PROBE_EVAL=1
    export BASELINE_USE_SEQLEN=1
    export BASELINE_USE_DPO_GAP=1
    export PER_LAYER_LR_ENABLED=0      # current default
    export REG_RATIO_ARG=""            # defaults to 1.0
    unset BASELINE_STATS_PATH || true
    ;;
  gap)
    export ADAPTIVE_MODE=1
    export DPO_PROBE_EVAL=1
    export BASELINE_USE_SEQLEN=1
    export BASELINE_USE_DPO_GAP=1
    export PER_LAYER_LR_ENABLED=0
    export REG_RATIO_ARG=""
    # Only implicit_reward_gap, so the epoch guard is the one thing that moves:
    # init_loss would change the epoch count by itself, and dataset stats would pull
    # correct_seq_len_p95 in too. 3.0 is above baseline_signals.DPO_GAP_WIDE, so the
    # guard should log a cap of epochs-1. task_type is spelled the way
    # baseline_stats_reader.suggest_dpo_beta_from_baseline expects — that β override
    # will also fire, and will change nothing, because dpo_config's run_cmd template
    # has no {beta} placeholder to substitute into.
    STATS_JSON="$OUT_DIR/baseline_stats_${TASK_ID}.json"
    printf '{"task_type":"DpoTask","training":{"implicit_reward_gap":3.0}}\n' > "$STATS_JSON"
    export BASELINE_STATS_PATH="$STATS_JSON"
    ;;
  *)
    echo "unknown stage '$STAGE' (want: a | b | gap)" >&2
    exit 2
    ;;
esac

export TRAINING_TELEMETRY_PATH="$OUT_DIR/run_telemetry.jsonl"

# ---------------------------------------------------------------------------
# Build the dataset. Nothing downstream can start without it, and it is written to
# the cache path text_trainer derives from the task id, not to --dataset. stdlib
# only, so the system python3 is fine; it does not need the training env.
# ---------------------------------------------------------------------------
echo "=== synthesising preference data ==="
"${PYTHON:-python3}" "$SMOKE_DIR/make_dpo_data.py" \
  --task-id "$TASK_ID" \
  --source-task-id "$SOURCE_TASK_ID" \
  --rows "$ROWS" \
  --seed "$SEED"
echo

echo "=== stage $STAGE · task $TASK_ID · model $MODEL · ${HOURS}h · ${ROWS} pairs ==="
env | grep -E "^(ADAPTIVE_MODE|DPO_PROBE_EVAL|BASELINE_USE_|BASELINE_STATS_PATH|PER_LAYER_LR_ENABLED)" | sort | sed 's/^/  /'
echo

cd "$REPO_DIR/scripts"

# shellcheck disable=SC2086
python -m text_trainer \
  --task-id "$TASK_ID" \
  --model "$MODEL" \
  --dataset "$TRAIN_JSON" \
  --dataset-type "$DATASET_TYPE" \
  --task-type DpoTask \
  --file-format json \
  --hours-to-complete "$HOURS" \
  --expected-repo-name "$REPO_NAME" \
  $REG_RATIO_ARG \
  2>&1 | tee "$LOG"

echo
echo "=== dataset: $TRAIN_JSON"
if [ -n "$STATS_JSON" ]; then
  echo "=== baseline stats: $STATS_JSON"
fi
echo "=== log: $LOG"
echo "=== telemetry: $TRAINING_TELEMETRY_PATH"
echo "=== submission: /app/checkpoints/$TASK_ID/$REPO_NAME"
