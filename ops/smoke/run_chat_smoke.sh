#!/usr/bin/env bash
# Exercise the ChatTask path end to end.
#
# ChatTask shares the instruct trainer (text_trainer.py:711 routes both the same
# way), so this is not a second training loop to validate. What it validates is the
# tokenisation branch nothing else reaches: passing a dataset_type that carries a
# `chat_template` key makes tokenize_instruct call
# _process_chat_template_dataset_fields, which maps an entirely different set of
# fields — chat_column / chat_role_field / chat_content_field / the role references —
# and hands axolotl a chat_template type instead of a custom format string.
#
# What a green run proves: the conversations file lands where text_trainer looks for
# it, the chat branch of create_dataset_entry builds a valid axolotl entry, the
# assistant spans survive as trainable labels, training runs under
# CustomEvalSaveCallback, the deadline stop fires, and a submission is written.
#
# What it does not prove: anything about chat quality, and nothing about MULTI-TURN
# loss masking — the fixture is single-turn because the source data is Q&A pairs.
#
# Usage:  ./run_chat_smoke.sh
set -euo pipefail

TASK_ID="${TASK_ID:-7c4e9b21-3a8d-4f65-9e02-5b7a1c3d8f40}"
SOURCE_TASK_ID="${SOURCE_TASK_ID:-dd558022-496c-4779-8fef-118689e7a227}"
MODEL="${MODEL:-unsloth/SmolLM-135M-Instruct}"
HOURS="${HOURS:-0.25}"
REPO_NAME="${REPO_NAME:-chat-smoke}"
ROWS="${ROWS:-3000}"

WORK="${WORK:-$HOME/smoke}"
OUT_DIR="$WORK/out/chat"
LOG="$WORK/logs/chat.log"
SMOKE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$OUT_DIR" "$WORK/logs"

# The trainer reads its dataset from a fixed cache path keyed by task id, so the file
# has to be named for the task we claim to be running.
python3 "$SMOKE_DIR/make_chat_data.py" \
  --task-id "$TASK_ID" \
  --source-task-id "$SOURCE_TASK_ID" \
  --rows "$ROWS"

TRAIN_JSON="/cache/datasets/${TASK_ID}_train_data.json"

# Field names straight from ChatTemplateDatasetType (dataset_models.py:49). The
# presence of chat_template is what selects the chat branch in tokenize_instruct.
DATASET_TYPE='{"chat_template":"chatml","chat_column":"conversations","chat_role_field":"from","chat_content_field":"value","chat_user_reference":"user","chat_assistant_reference":"assistant"}'

export ADAPTIVE_MODE=1
export EMIT_PER_EXAMPLE_LOSSES=1
export TRAINING_WSM_GATE=1
export TRAINING_TELEMETRY_PATH="$OUT_DIR/run_telemetry.jsonl"

echo "=== chat · task $TASK_ID · model $MODEL · ${HOURS}h · ${ROWS} conversations ==="
echo

cd "${REPO_DIR:-$HOME/lostinjamal}/scripts"

python -m text_trainer \
  --task-id "$TASK_ID" \
  --model "$MODEL" \
  --dataset "$TRAIN_JSON" \
  --dataset-type "$DATASET_TYPE" \
  --task-type ChatTask \
  --file-format json \
  --hours-to-complete "$HOURS" \
  --expected-repo-name "$REPO_NAME" \
  2>&1 | tee "$LOG"

echo
echo "=== log: $LOG"
echo "=== telemetry: $TRAINING_TELEMETRY_PATH"
echo "=== submission: /app/checkpoints/$TASK_ID/$REPO_NAME"
