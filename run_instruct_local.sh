#!/bin/bash
# run_instruct_local.sh — Canonical Instruct training harness for text-jagger
# Mirrors master-text/instruct.sh pattern. Used as 1:1 tournament-like local test.
#
# Pattern:
#   1. trainer-downloader → pre-cache model + dataset into /cache
#   2. standalone-text-trainer → training with --network none (G.O.D contract)
#   3. hf-uploader → push checkpoint to HuggingFace
#
# Usage:
#   bash run_instruct_local.sh
#
# Override via env vars:
#   TASK_ID=xxx MODEL=yyy DATASET=zzz bash run_instruct_local.sh
#
# Or edit the defaults below.

set -euo pipefail

# -----------------------------------------------------------------------------
# Source .env if present (gitignored file with task params + secrets)
# -----------------------------------------------------------------------------
if [ -f ".env" ]; then
  echo "==> Sourcing .env"
  # shellcheck disable=SC1091
  source .env
fi

# -----------------------------------------------------------------------------
# USER-PROVIDED PARAMETERS (fill these or override via env / .env)
# -----------------------------------------------------------------------------

TASK_ID="${TASK_ID:-REPLACE_WITH_TASK_ID}"
MODEL="${MODEL:-TinyLlama/TinyLlama-1.1B-Chat-v1.0}"
DATASET="${DATASET:-REPLACE_WITH_DATASET_URL_OR_PATH}"
DATASET_TYPE="${DATASET_TYPE:-'{\"field_system\": null, \"field_instruction\": \"instruct\", \"field_input\": null, \"field_output\": \"output\", \"format\": null, \"no_input_format\": null, \"system_format\": null}'}"
FILE_FORMAT="${FILE_FORMAT:-s3}"
HOURS_TO_COMPLETE="${HOURS_TO_COMPLETE:-6}"

# Upload params (set if you want to push to HF after training)
HUGGINGFACE_TOKEN="${HUGGINGFACE_TOKEN:-}"
WANDB_TOKEN="${WANDB_TOKEN:-}"
HUGGINGFACE_USERNAME="${HUGGINGFACE_USERNAME:-}"
EXPECTED_REPO_NAME="${EXPECTED_REPO_NAME:-text-jagger-instruct-baseline}"

# -----------------------------------------------------------------------------
# DERIVED PATHS
# -----------------------------------------------------------------------------

LOCAL_FOLDER="/app/checkpoints/$TASK_ID/$EXPECTED_REPO_NAME"
CHECKPOINTS_DIR="$(pwd)/secure_checkpoints"
OUTPUTS_DIR="$(pwd)/outputs"
LOG_DIR="$(pwd)/logs"

mkdir -p "$CHECKPOINTS_DIR" && chmod 700 "$CHECKPOINTS_DIR"
mkdir -p "$OUTPUTS_DIR" && chmod 700 "$OUTPUTS_DIR"
mkdir -p "$LOG_DIR"

# -----------------------------------------------------------------------------
# STEP 0: (optional) Build Docker images if not already built
# -----------------------------------------------------------------------------
# Uncomment to force rebuild:
# docker build --no-cache -t trainer-downloader    -f dockerfiles/trainer-downloader.dockerfile .
# docker build --no-cache -t standalone-text-trainer -f dockerfiles/standalone-text-trainer.dockerfile .
# docker build --no-cache -t hf-uploader           -f dockerfiles/hf-uploader.dockerfile .

# -----------------------------------------------------------------------------
# STEP 1: Download model + dataset
# -----------------------------------------------------------------------------
echo "==> Downloading model and dataset..."
docker run --rm \
  --volume "$CHECKPOINTS_DIR:/cache:rw" \
  --name downloader-image \
  trainer-downloader \
  --task-id "$TASK_ID" \
  --model "$MODEL" \
  --dataset "$DATASET" \
  --file-format "$FILE_FORMAT" \
  --task-type "InstructTextTask"

# -----------------------------------------------------------------------------
# STEP 2: Train (network isolated, matches G.O.D validator environment)
# -----------------------------------------------------------------------------
echo "==> Starting training..."
docker run --rm --gpus all \
  --security-opt=no-new-privileges \
  --cap-drop=ALL \
  --memory=64g \
  --cpus=8 \
  --network none \
  --volume "$CHECKPOINTS_DIR:/cache:rw" \
  --volume "$OUTPUTS_DIR:/app/checkpoints/:rw" \
  --name instruct-text-trainer-local \
  standalone-text-trainer \
  --task-id "$TASK_ID" \
  --model "$MODEL" \
  --dataset "$DATASET" \
  --dataset-type "$DATASET_TYPE" \
  --task-type "InstructTextTask" \
  --file-format "$FILE_FORMAT" \
  --hours-to-complete "$HOURS_TO_COMPLETE" \
  --expected-repo-name "$EXPECTED_REPO_NAME" \
  2>&1 | tee "$LOG_DIR/full_log_${EXPECTED_REPO_NAME}.txt"

# -----------------------------------------------------------------------------
# STEP 3: Extract summary lines for quick review
# -----------------------------------------------------------------------------
echo ""
echo "==> Extracting training summary..."
if [ -x "./extract_training_log.sh" ]; then
  ./extract_training_log.sh \
    "$LOG_DIR/full_log_${EXPECTED_REPO_NAME}.txt" \
    "$LOG_DIR/summary_${EXPECTED_REPO_NAME}.txt"
  echo "Summary:  $LOG_DIR/summary_${EXPECTED_REPO_NAME}.txt"
fi

echo ""
echo "Full log: $LOG_DIR/full_log_${EXPECTED_REPO_NAME}.txt"
echo ""

# -----------------------------------------------------------------------------
# STEP 4 (optional): Upload to HuggingFace
# -----------------------------------------------------------------------------
if [ -n "$HUGGINGFACE_TOKEN" ] && [ -n "$HUGGINGFACE_USERNAME" ]; then
  echo "==> Uploading model to HuggingFace..."
  docker run --rm --gpus all \
    --volume "$OUTPUTS_DIR:/app/checkpoints/:rw" \
    --env HUGGINGFACE_TOKEN="$HUGGINGFACE_TOKEN" \
    --env HUGGINGFACE_USERNAME="$HUGGINGFACE_USERNAME" \
    --env WANDB_TOKEN="$WANDB_TOKEN" \
    --env TASK_ID="$TASK_ID" \
    --env EXPECTED_REPO_NAME="$EXPECTED_REPO_NAME" \
    --env LOCAL_FOLDER="$LOCAL_FOLDER" \
    --env MODEL="$MODEL" \
    --name hf-uploader-local \
    hf-uploader
else
  echo "==> Skipping HF upload (HUGGINGFACE_TOKEN or HUGGINGFACE_USERNAME not set)"
fi

echo ""
echo "==> Done."
