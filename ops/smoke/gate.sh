#!/usr/bin/env bash
# Mandatory pre-submission gate: run all five text paths and assert on what the logs say.
#
# Exit-code-only checking is not enough here, and that is the whole reason this file
# exists. Every safety net in this codebase is written to keep going rather than die —
# correct for a tournament, and exactly why a green exit code proves very little. Runs
# that "succeeded" while badly broken, all found by reading logs, not exit codes:
#
#   * KL OOM'd, was caught, and the run silently continued on plain cross-entropy —
#     on a task the validator scores WITH the KL term.
#   * Checkpoint selection compared a KL-weighted number against a plain eval_loss, so
#     whichever checkpoint's KL measurement failed always won.
#   * dedup collapsed 3000 chat rows to 1; the split then had zero training rows.
#   * adaptive computed max_length and nothing consumed it; the trainer used a constant.
#
# So each gate below asserts a specific line, and every one of them maps to a bug that
# actually shipped. Add a gate whenever a new one gets through.
#
# Usage:  ./gate.sh [path ...]     default: all five
#         SKIP_PREFLIGHT=1         only if you have already run preflight.sh
set -uo pipefail

SMOKE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="${REPO_DIR:-$(cd "$SMOKE_DIR/../.." && pwd)}"
WORK="${WORK:-$HOME/smoke}"
LOGS="$WORK/logs"
HOURS="${HOURS:-0.25}"
INSTRUCT_TASK="${INSTRUCT_TASK:-6d8b2af6-9715-4a60-bc19-b7e8023b57a2}"
mkdir -p "$LOGS"

PATHS=("$@"); [ ${#PATHS[@]} -eq 0 ] && PATHS=(instruct kl dpo grpo chat)
RESULTS=(); FAILED=0

pass() { RESULTS+=("PASS|$1|$2"); }
fail() { RESULTS+=("FAIL|$1|$2"); FAILED=1; }

# Three tiny python checks, written to temp files rather than inlined. Heredocs inside
# shell conditionals quote badly, and a gate that misreports because of quoting is worse
# than no gate.
PYCHECK_DIR="$(mktemp -d)"
trap 'rm -rf "$PYCHECK_DIR"' EXIT

PYCHECK_ARCH="$PYCHECK_DIR/arch.py"
cat > "$PYCHECK_ARCH" <<'PYEOF'
import json, os, sys
p = os.path.join(sys.argv[1], "config.json")
# A LoRA-only submission legitimately has no config.json; only a present-but-broken one
# is a failure, since that is the shape restore_submission_architectures repairs.
if not os.path.isfile(p):
    sys.exit(0)
try:
    sys.exit(0 if json.load(open(p)).get("architectures") else 1)
except Exception:
    sys.exit(1)
PYEOF

PYCHECK_SPLIT="$PYCHECK_DIR/split.py"
cat > "$PYCHECK_SPLIT" <<'PYEOF'
import ast, re, sys
m = re.search(r"\{.*\}", sys.argv[1])
d = ast.literal_eval(m.group(0)) if m else {}
sys.exit(0 if d.get("train", 0) > 0 and d.get("dev", 0) > 0 else 1)
PYEOF

PYCHECK_DEDUP="$PYCHECK_DIR/dedup.py"
cat > "$PYCHECK_DEDUP" <<'PYEOF'
import ast, re, sys
m = re.search(r"\{.*\}", sys.argv[1])
d = ast.literal_eval(m.group(0)) if m else {}
n = d.get("input", 0)
kept = d.get("after_jaccard", d.get("after_exact", 0))
# Half is a deliberately loose bar: honest dedup on a duplicated corpus can remove a
# lot. What this catches is the collapse-to-nothing shape.
sys.exit(0 if not n or kept >= 0.5 * n else 1)
PYEOF


# --- gates shared by every path ------------------------------------------------
# `Training successfully done` is the only line printed after the post-training NaN
# scan and the architectures restore, so its absence means those never ran even if
# a model file exists on disk.
common_gates() {
  local name="$1" log="$2" sub="$3"
  [ -f "$log" ] || { fail "$name" "no log at $log"; return; }

  grep -aq "Training successfully done" "$log" \
    && pass "$name" "training completed" \
    || fail "$name" "no 'Training successfully done' — post-training checks did not run"

  # Tracebacks alone do not mean failure here: the OOM ladder deliberately crashes an
  # attempt, halves the batch and relaunches, so a recovered OOM leaves a traceback in
  # the log of a perfectly good run. Only an incomplete run makes them damning — and
  # `Training successfully done` above already gates that. So report the count when the
  # run finished, and fail on it only when it did not.
  local tb; tb=$(grep -aci "^Traceback" "$log")
  if [ "$tb" = "0" ]; then
    pass "$name" "no tracebacks"
  elif grep -aq "Training successfully done" "$log"; then
    local retried; retried=$(grep -aco "FAST-CRASH" "$log")
    pass "$name" "$tb traceback(s) from $retried recovered retry/retries, run completed"
  else
    fail "$name" "$tb traceback(s) and the run did not complete"
  fi

  [ -s "$sub/model.safetensors" ] || [ -s "$sub/adapter_model.safetensors" ] \
    && pass "$name" "model artefact written" || fail "$name" "no model artefact in $sub"

  # config.json is rewritten by restore_submission_architectures; a missing
  # `architectures` key is what makes the validator's is_finetune check fail outright.
  if python3 "$PYCHECK_ARCH" "$sub"; then
    pass "$name" "architectures present (or LoRA-only)"
  else
    fail "$name" "config.json has no architectures — validator is_finetune will fail"
  fi
}

# --- gates that only make sense for one path -----------------------------------
instruct_gates() {
  local name="$1" log="$2"
  # The adaptive max_length used to be computed and then dropped on the floor: the
  # command template has no --max_length flag and train_request never carried the key,
  # so tokenisation, the trainer, the VRAM planner and the OOM ladder's last rung all
  # fell back to a constant. These two numbers differing is that bug returning.
  local planned trained
  planned=$(grep -ao "max_len=[0-9]*" "$log" | tail -1 | cut -d= -f2)
  trained=$(grep -ao "max_length: [0-9]*" "$log" | tail -1 | awk '{print $2}')
  if [ -n "$planned" ] && [ -n "$trained" ] && [ "$planned" = "$trained" ]; then
    pass "$name" "max_length plumbed ($planned)"
  else
    fail "$name" "planned max_len=${planned:-?} but trainer used ${trained:-?}"
  fi

  # An empty train or dev split kills the run at the packer before step 1.
  local split; split=$(grep -a "\[split\]" "$log" | tail -1)
  if [ -n "$split" ]; then
    if python3 "$PYCHECK_SPLIT" "$split"; then
      pass "$name" "split has train and dev rows"
    else
      fail "$name" "split produced an empty side: $split"
    fi
  fi

  # dedup wiping a dataset is silent: the run keeps going with whatever survived.
  local ded; ded=$(grep -a "\[dedup\]" "$log" | tail -1)
  if [ -n "$ded" ]; then
    if python3 "$PYCHECK_DEDUP" "$ded"; then
      pass "$name" "dedup kept most rows"
    else
      fail "$name" "dedup removed almost everything: $ded"
    fi
  fi
}

kl_gates() {
  local name="$1" log="$2"
  # The KL term used to OOM, get caught, and let the run continue on plain CE. The
  # run looked fine; the objective was not the one being scored.
  local kf; kf=$(grep -ac "KL term failed" "$log")
  [ "$kf" = "0" ] && pass "$name" "KL term never fell back" || fail "$name" "KL term failed $kf time(s) — trained on the wrong objective"

  local mu; mu=$(grep -ac "checkpoint metric unavailable" "$log")
  [ "$mu" = "0" ] && pass "$name" "checkpoint metric always available" || fail "$name" "KL checkpoint metric unavailable $mu time(s)"

  local mc; mc=$(grep -ac "\[kl\] checkpoint metric:" "$log")
  [ "$mc" -gt 0 ] 2>/dev/null && pass "$name" "$mc weighted checkpoint metric(s)" \
    || fail "$name" "no weighted checkpoint metric was ever computed — the KL path did not run"
}

grpo_gates() {
  local name="$1" log="$2"
  grep -aq "Using reward function" "$log" \
    && pass "$name" "reward function loaded" || fail "$name" "reward function never loaded"
  # A constant reward makes every advantage zero, so the run trains on nothing.
  local n; n=$(grep -ao "reward': [-0-9.]*" "$log" | sort -u | wc -l)
  [ "$n" -gt 1 ] 2>/dev/null && pass "$name" "rewards vary ($n distinct)" \
    || fail "$name" "reward is constant — advantages are degenerate"
}

chat_gates() {
  local name="$1" log="$2"
  # This branch is reached only when dataset_type carries chat_template; if it is
  # missing the row silently trains as instruct text.
  grep -aq "Processing chat template dataset type" "$log" \
    && pass "$name" "chat_template branch taken" || fail "$name" "chat template branch never ran"
  instruct_gates "$name" "$log"   # chat shares the instruct trainer
}


# Reclaim disk between paths. Checkpoints are never pruned (no save_total_limit) and the
# LR ladder creates one output dir per attempt, so five paths in a row will fill a large
# disk. The gates for a path have already been evaluated by the time this runs, so the
# artefacts are spent.
reclaim() {
  rm -rf /workspace/scripts/soutputs/* 2>/dev/null
  rm -rf "$REPO_DIR/scripts/wandb"/* 2>/dev/null
  local free; free=$(df -BG --output=avail / 2>/dev/null | tail -1 | tr -dc '0-9')
  echo "  (reclaimed; ${free:-?}G free)"
}

# --- driver --------------------------------------------------------------------
if [ "${SKIP_PREFLIGHT:-0}" != "1" ]; then
  "$SMOKE_DIR/preflight.sh" || { echo "gate aborted: preflight failed"; exit 2; }
  echo
fi

for p in "${PATHS[@]}"; do
  echo "=== running $p ==="
  case "$p" in
    instruct) TASK_ID=$INSTRUCT_TASK MODEL=unsloth/Qwen2-1.5B-Instruct HOURS=$HOURS REPO_NAME=gate-instruct REPO_DIR=$REPO_DIR \
                "$SMOKE_DIR/run_instruct_replay.sh" b >"$LOGS/gate_instruct.out" 2>&1
              common_gates instruct "$LOGS/b.log" "/app/checkpoints/$INSTRUCT_TASK/gate-instruct"
              instruct_gates instruct "$LOGS/b.log" ;;
    # KL's key assertion is that a WEIGHTED checkpoint metric was computed, and that can
    # only happen at an eval. Too short a budget and the deadline preempts the first eval,
    # so the gate reports "the KL path did not run" when the truth is "the run had no time
    # to get there". Give it its own, longer budget rather than weakening the assertion —
    # the assertion is the whole point of the KL path.
    kl)       TASK_ID=$INSTRUCT_TASK MODEL=unsloth/Qwen2-1.5B-Instruct HOURS=${KL_HOURS:-0.6} REPO_NAME=gate-kl REPO_DIR=$REPO_DIR \
                "$SMOKE_DIR/run_instruct_replay.sh" kl >"$LOGS/gate_kl.out" 2>&1
              common_gates kl "$LOGS/kl.log" "/app/checkpoints/$INSTRUCT_TASK/gate-kl"
              kl_gates kl "$LOGS/kl.log" ;;
    dpo)      SOURCE_TASK_ID=$INSTRUCT_TASK HOURS=$HOURS REPO_DIR=$REPO_DIR \
                "$SMOKE_DIR/run_dpo_smoke.sh" >"$LOGS/gate_dpo.out" 2>&1
              common_gates dpo "$LOGS/dpo-a.log" "$(ls -d /app/checkpoints/*/dpo-smoke-a 2>/dev/null | head -1)" ;;
    grpo)     GRPO_SRC=/cache/datasets/${INSTRUCT_TASK}_train_data.json HOURS=$HOURS REPO_DIR=$REPO_DIR \
                "$SMOKE_DIR/run_grpo_smoke.sh" >"$LOGS/gate_grpo.out" 2>&1
              common_gates grpo "$LOGS/grpo-a.log" "$(ls -d /app/checkpoints/*/grpo-smoke-a 2>/dev/null | head -1)"
              grpo_gates grpo "$LOGS/grpo-a.log" ;;
    chat)     SOURCE_TASK_ID=$INSTRUCT_TASK HOURS=$HOURS REPO_DIR=$REPO_DIR \
                "$SMOKE_DIR/run_chat_smoke.sh" >"$LOGS/gate_chat.out" 2>&1
              common_gates chat "$LOGS/chat.log" "$(ls -d /app/checkpoints/*/chat-smoke 2>/dev/null | head -1)"
              chat_gates chat "$LOGS/chat.log" ;;
    *) echo "unknown path '$p' (want: instruct kl dpo grpo chat)" >&2; exit 2 ;;
  esac
  reclaim
  echo
done

echo "════════════════ GATE RESULT ════════════════"
printf '%-6s %-9s %s\n' STATUS PATH DETAIL
for r in "${RESULTS[@]}"; do
  IFS='|' read -r st nm dt <<<"$r"
  [ -z "$dt" ] && continue
  printf '%-6s %-9s %s\n' "$st" "$nm" "$dt"
done
echo "═════════════════════════════════════════════"
if [ $FAILED -eq 0 ]; then
  echo "ALL GATES PASSED — safe to submit this commit"
else
  echo "GATE FAILED — do not submit. Fix the FAIL rows above."
fi
exit $FAILED
