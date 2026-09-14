#!/usr/bin/env bash
# Equal-budget A/B: do our features actually lower the scored loss?
#
# This is the question every other measurement so far has dodged. The earlier
# "comparison" was invalid: stage A got 64 minutes because the deadline-overrun bug
# let it run long, stage B got 15 because the fix works. Different compute, so the
# numbers said nothing about quality.
#
# Two things have to be true for a result here to mean anything, and both were wrong
# in the obvious design:
#
# 1. IDENTICAL BUDGET AND TASK. Same model, same data, same HOURS, same box, run back
#    to back so the GPU is in the same state.
#
# 2. ONE COMMON YARDSTICK. The arms build DIFFERENT dev splits — the control has
#    INSTRUCT_SPLIT_POLICY=0 and INSTRUCT_DEDUP=0 — so comparing their own loss.txt
#    values compares two different held-out sets and is meaningless. Both models are
#    therefore scored afterwards on one file neither ever trained on, with the
#    validator's own metric (per-example token-mean CE, then a flat mean over
#    examples) via score_against_leaderboard.py.
#
# Arms (stage definitions live in run_instruct_replay.sh):
#   a0  every feature OFF, reg_ratio 1.0   <- control
#   b   every feature ON,  reg_ratio 1.0   <- ours
# reg_ratio is held at 1.0 in BOTH so the comparison isolates the features. Stage `a`
# additionally carries the historical reg_ratio 1.1874; a-vs-a0 is a separate
# question (what the learning-rate change alone did) and is not what this measures.
#
# Usage:  ./ab.sh [arm ...]      default: a0 b
set -uo pipefail

SMOKE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="${REPO_DIR:-$(cd "$SMOKE_DIR/../.." && pwd)}"
WORK="${WORK:-$HOME/smoke}"
TASK_ID="${TASK_ID:-dd558022-496c-4779-8fef-118689e7a227}"
MODEL="${MODEL:-unsloth/Qwen2-1.5B-Instruct}"
HOURS="${HOURS:-1.0}"
SEED_TAG="${SEED_TAG:-s1}"
# The training seed itself, not just a label. Without varying this a repeat run is the
# same run, so there is no way to separate a real effect from training noise — which is
# the whole reason a second seed is worth an hour of GPU.
export INSTRUCT_SEED="${INSTRUCT_SEED:-42}"
TEST_DATA="${TEST_DATA:-/cache/datasets/${TASK_ID}_test_data.json}"
ARMS=("$@"); [ ${#ARMS[@]} -eq 0 ] && ARMS=(a0 b)

mkdir -p "$WORK/logs" "$WORK/ab"
[ -f "$TEST_DATA" ] || { echo "no held-out file at $TEST_DATA" >&2; exit 2; }

echo "=== A/B · task $TASK_ID · $MODEL · ${HOURS}h per arm · seed $INSTRUCT_SEED (tag $SEED_TAG) ==="
echo "=== common held-out: $TEST_DATA ($(python3 -c "import json;print(len(json.load(open('$TEST_DATA'))))") rows)"
echo

for arm in "${ARMS[@]}"; do
  REPO_NAME="ab-${arm}-${SEED_TAG}"
  echo "--- arm $arm (${HOURS}h) ---"
  # Reclaim first: one arm's per-attempt output dirs must not starve the next.
  rm -rf /workspace/scripts/soutputs/* 2>/dev/null
  # And wait for the GPU to drain: batch size is planned from live free VRAM, so an arm
  # started too early plans a different batch and is no longer the same experiment.
  "$SMOKE_DIR/wait_gpu.sh" >&2
  TASK_ID="$TASK_ID" MODEL="$MODEL" HOURS="$HOURS" REPO_NAME="$REPO_NAME" REPO_DIR="$REPO_DIR" \
    "$SMOKE_DIR/run_instruct_replay.sh" "$arm" > "$WORK/logs/ab_${arm}_${SEED_TAG}.out" 2>&1
  SUB="/app/checkpoints/$TASK_ID/$REPO_NAME"
  echo "    submission: $SUB"
  echo "    own loss.txt (NOT comparable across arms): $(cat "$SUB/loss.txt" 2>/dev/null)"
  echo
done

echo "=== scoring every arm on the one common held-out set ==="
for arm in "${ARMS[@]}"; do
  REPO_NAME="ab-${arm}-${SEED_TAG}"
  SUB="/app/checkpoints/$TASK_ID/$REPO_NAME"
  OUT="$WORK/ab/${arm}_${SEED_TAG}.json"
  if [ -d "$SUB" ]; then
    python3 "$SMOKE_DIR/score_against_leaderboard.py" \
      --model "$SUB" --test-data "$TEST_DATA" --out "$OUT" \
      2>&1 | sed "s/^/  [$arm] /"
  else
    echo "  [$arm] no submission produced — arm failed, see $WORK/logs/ab_${arm}_${SEED_TAG}.out"
  fi
done

echo
echo "=== per-arm vectors written to $WORK/ab/ — compare with compare_ab.py ==="
