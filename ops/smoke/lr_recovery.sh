#!/usr/bin/env bash
# Recovery gate: poison the LR prior and see where the mechanism actually lands.
#
# LR selection exists for one case — the prior is wrong. On a normal task the family LR
# table is already close, so every selector looks fine and an on-distribution A/B
# measures nothing. This deliberately breaks the prior by a known factor and asks
# whether the search finds its way back.
#
# What "pass" means: the LR actually trained at is within RECOVERY_TOLERANCE of the LR
# the unpoisoned run chose. Not "the loss got better" — that hides inside run-to-run
# noise (measured at 0.017 nats on this box, against effects around 0.009). Recovery is
# a property of the search, and it is directly observable.
#
# The current ladder is expected to FAIL this, and the arithmetic says why:
# lr_utils.extend_learning_rates with text_trainer.get_log_scale's 0.18 spans only
# x0.66..x1.51 around the prior, so a prior wrong by 10x puts the truth far outside
# every candidate. tests/test_lr_recovery_reach.py states that as executable bounds and
# runs in milliseconds. This script is the empirical counterpart, and its real job is to
# gate a FUTURE change that claims to recover — an LR range test, a widened span —
# rather than to re-confirm arithmetic we already have.
#
# Usage:  ./lr_recovery.sh [factor ...]     default: 10 0.1
#         HOURS must be >= ~1.3 or the ladder never engages (see the n<=0 branch in
#         customized_trainer.py: at 1.0h it sets mode=finish and the probe becomes the
#         final run, so there is no search to test).
set -uo pipefail

SMOKE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="${REPO_DIR:-$(cd "$SMOKE_DIR/../.." && pwd)}"
WORK="${WORK:-$HOME/smoke}"
TASK_ID="${TASK_ID:-6d8b2af6-9715-4a60-bc19-b7e8023b57a2}"
MODEL="${MODEL:-unsloth/Qwen2-1.5B-Instruct}"
HOURS="${HOURS:-1.3}"
RECOVERY_TOLERANCE="${RECOVERY_TOLERANCE:-2.0}"
FACTORS=("$@"); [ ${#FACTORS[@]} -eq 0 ] && FACTORS=(10 0.1)
mkdir -p "$WORK/logs" "$WORK/lr"

# The LR a run actually settled on: the ladder's own selection line if the search ran,
# otherwise the planned LR (which is what a run without a search trains at).
extract_lr() {
  local log="$1"
  local sel; sel=$(grep -ao "BL;[0-9]*;[0-9.e+-]*; *[0-9.e+-]*" "$log" 2>/dev/null | tail -1 | awk -F';' '{print $4}' | tr -d ' ')
  if [ -n "$sel" ]; then echo "$sel"; return; fi
  grep -ao "lr=[0-9.e+-]*" "$log" 2>/dev/null | tail -1 | cut -d= -f2
}

run_one() {  # name, override_or_empty
  local name="$1" override="$2"
  local log="$WORK/logs/lrrec_${name}.log"
  rm -rf /workspace/scripts/soutputs/* 2>/dev/null
  redis-cli del state >/dev/null 2>&1
  # Batch size is planned from live free VRAM; starting before the previous run has
  # released produces a different experiment, not a noisier one.
  "$SMOKE_DIR/wait_gpu.sh" >&2
  env TASK_ID="$TASK_ID" MODEL="$MODEL" HOURS="$HOURS" REPO_NAME="lrrec-$name" REPO_DIR="$REPO_DIR" \
      ${override:+ADAPTIVE_LR_OVERRIDE="$override"} \
      "$SMOKE_DIR/run_instruct_replay.sh" b > "$WORK/logs/lrrec_${name}.out" 2>&1
  cp "$WORK/logs/b.log" "$log" 2>/dev/null
  extract_lr "$log"
}

echo "=== LR recovery gate · $MODEL · ${HOURS}h per run · tolerance x${RECOVERY_TOLERANCE} ==="
echo

echo "--- baseline (prior untouched) ---"
BASE_LR="$(run_one baseline "")"
echo "    settled on LR = ${BASE_LR:-?}"
echo

RESULTS=()
for f in "${FACTORS[@]}"; do
  POISON=$(python3 -c "print(f'{float('${BASE_LR:-1e-4}') * float('$f'):.6e}')")
  echo "--- prior poisoned x$f  (forced LR = $POISON) ---"
  GOT="$(run_one "x$f" "$POISON")"
  echo "    settled on LR = ${GOT:-?}"
  RESULTS+=("$f|$POISON|${GOT:-nan}")
  echo
done

echo "════════════════ RECOVERY RESULT ════════════════"
printf '%-8s %-14s %-14s %-10s %s\n' FACTOR POISONED SETTLED "OFF-BY" VERDICT
FAILED=0
for r in "${RESULTS[@]}"; do
  IFS='|' read -r f poison got <<<"$r"
  read -r off verdict <<<"$(python3 -c "
import sys
base, got, tol = float('${BASE_LR:-nan}'), float('$got'), float('$RECOVERY_TOLERANCE')
if got != got or base != base:
    print('nan UNKNOWN'); sys.exit()
off = max(got/base, base/got)
print(f'{off:.2f} {\"RECOVERED\" if off <= tol else \"STUCK\"}')")"
  [ "$verdict" != "RECOVERED" ] && FAILED=1
  printf '%-8s %-14s %-14s x%-9s %s\n' "$f" "$poison" "$got" "$off" "$verdict"
done
echo "═════════════════════════════════════════════════"
echo "baseline LR: ${BASE_LR:-?}   tolerance: x$RECOVERY_TOLERANCE"
if [ $FAILED -eq 0 ]; then
  echo "RECOVERED from every poisoned prior."
else
  echo "STUCK on at least one poisoned prior — the search cannot leave a wrong prior's"
  echo "neighbourhood. Expected for the current ladder; see tests/test_lr_recovery_reach.py."
fi
exit $FAILED
