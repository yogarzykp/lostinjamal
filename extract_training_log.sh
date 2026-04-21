#!/bin/bash
# extract_training_log.sh — Extract important training metrics from full log
# Usage: ./extract_training_log.sh <full_log_file> [output_file]
# Or pipe: docker run ... 2>&1 | tee full_log.txt && ./extract_training_log.sh full_log.txt
#
# Covers:
#   - HF Trainer standard: train_runtime, train_loss, eval_loss, samples_per_sec
#   - text-jagger state machine: BL; (LR decision), Checking the model, etc.
#   - Our additions: [dedup], [instruct_config], [init_wandb], [train_instruct],
#     [MetricsCallback], [ExperimentLogger]

INPUT="${1:-/dev/stdin}"
OUTPUT="${2:-training_summary.txt}"

grep -E \
  '\[Adaptive\]|\[Advisor\]|\[dedup\]|\[instruct_config\]|\[init_wandb\]|\[train_instruct\]|\[MetricsCallback\]|\[ExperimentLogger\]|Using lr from|Model size from|split .* into|Dropped .* long|Loaded dataset|original_steps|total_steps_per_epoch|total_steps_all_epochs|^\{.loss|Deleting checkpoint|^BL;|eval_loss|train_runtime|train_loss|train_samples_per_second|Checking the model|Estimated number|Final number|Evaluating the model|Updating the best|Training successfully|current_loss|do not pack|packing the dataset|min_data_size_num|periodic_save_steps|max_steps' \
  "$INPUT" \
  | grep -v "^Tokenizing\|^Dropping\|^Generating\|^Processing\|^Filtered\|^Dumped\|wandb:" \
  > "$OUTPUT"

# Count lines
TOTAL_INPUT=$(wc -l < "$INPUT" 2>/dev/null || echo "?")
TOTAL_OUTPUT=$(wc -l < "$OUTPUT")
echo "Extracted $TOTAL_OUTPUT lines from $TOTAL_INPUT -> $OUTPUT"
