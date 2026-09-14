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
TASK_ID="${TASK_ID:-dd558022-496c-4779-8fef-118689e7a227}"
MODEL="${MODEL:-unsloth/Qwen2-1.5B-Instruct}"
HOURS="${HOURS:-1.3}"
RECOVERY_TOLERANCE="${RECOVERY_TOLERANCE:-2.0}"
FACTORS=("$@"); [ ${#FACTORS[@]} -eq 0 ] && FACTORS=(10 0.1)
mkdir -p "$WORK/logs" "$WORK/lr"

# The LR a run actually settled on: the ladder's own selection line if the search ran,
# otherwise the planned LR (which is what a run without a search trains at).
# The LR a run actually settled on.
#
# One gate run produces ONE log, but that log holds EVERY sub-run of the ladder — the
# probe, each confirmation, and the final run — because text_trainer streams all of its
# children into a single stream that run_instruct_replay tees to b.log. So "the peak
# learning rate in the file" is the highest rate the search ever TRIED, not the one it
# chose. That distinction is not academic: the probe trains at the poisoned prior itself
# (the incumbent check below proves it), so a whole-file peak is >= the poison for any
# upward poison, and the gate would score STUCK at exactly the poison factor no matter
# how well the selector recovered. Measured on a real log: whole-file peak said
# 8.069e-04 (STUCK, x10.0) where the final run had actually settled on 2.840e-05
# (x2.84) — a confident, precisely wrong verdict.
#
# So: the peak of the LAST run only. "Training attempt" marks the start of each real
# training launch (including OOM retries, where the last attempt is still the one that
# trained), which makes it the right boundary in both cases.
#
# The BL; line is the ladder's record of what it SELECTED, kept only as a cross-check.
# It is not authoritative: text_trainer prints state["lrs"][index] while the run trains
# at current_lr, which the BO-augment block can override, so BL can name a rate that was
# never trained. Disagreement is worth a warning, not a silent preference.
#
# The earlier fallback here — a bare `lr=` grep — also matched the tail of `safe_lr=` on
# the range test's own log line, and so reported the sweep's SUGGESTION as the settled
# rate (4.13e-07 for a run that trained at 8.069e-04).
extract_lr() {
  local log="$1"
  local sel peak last
  sel=$(grep -ao "BL;[0-9]*;[0-9.e+-]*; *[0-9.e+-]*" "$log" 2>/dev/null | tail -1 | awk -F';' '{print $4}' | tr -d ' ')

  last=$(grep -an "Training attempt" "$log" 2>/dev/null | tail -1 | cut -d: -f1)
  if [ -n "$last" ]; then
    peak=$(tail -n +"$last" "$log" 2>/dev/null | grep -aoE "'learning_rate': [0-9.e-]+" | awk '{print $2}' | sort -g | tail -1)
  else
    peak=$(grep -aoE "'learning_rate': [0-9.e-]+" "$log" 2>/dev/null | awk '{print $2}' | sort -g | tail -1)
  fi

  if [ -n "$sel" ] && [ -n "$peak" ]; then
    python3 -c 'import sys
a, b = float(sys.argv[1]), float(sys.argv[2])
if a > 0 and b > 0 and max(a/b, b/a) > 1.05:
    sys.stderr.write("    !! ladder selected %s but the final run trained at %s\n" % (sys.argv[1], sys.argv[2]))' "$sel" "$peak" >&2
  fi

  if [ -n "$peak" ]; then echo "$peak"; return; fi
  if [ -n "$sel" ];  then echo "$sel";  return; fi
  # Nothing usable. Emit nothing: the caller scores an empty result UNKNOWN, which is the
  # honest outcome. It must never fall through to a pattern that happens to match.
  return 0
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

# A rerun does not need to re-measure the baseline: it is 1.3h of GPU for a number that
# does not change while the selector and task are fixed. Pass BASELINE_LR to reuse one.
if [ -n "${BASELINE_LR:-}" ]; then
  BASE_LR="$BASELINE_LR"
  echo "--- baseline (reused, not re-run) ---"
  echo "    LR = $BASE_LR"
else
  echo "--- baseline (prior untouched) ---"
  BASE_LR="$(run_one baseline "")"
  echo "    settled on LR = ${BASE_LR:-?}"
fi
[ -n "$BASE_LR" ] || { echo "baseline produced no LR — cannot judge recovery" >&2; exit 3; }
echo

RESULTS=()
for f in "${FACTORS[@]}"; do
  # Values go in as ARGV, not interpolated into the source. The previous form nested
  # single quotes inside an f-string, which only became legal in Python 3.12 (PEP 701) —
  # on this box's 3.10 it is a SyntaxError, so POISON came back EMPTY, the
  # ${override:+...} expansion vanished, and every "poisoned" run silently trained on the
  # untouched prior. That reports RECOVERED at ~1.0x for any selector, including one that
  # cannot recover at all. A gate that cannot fail is worse than no gate.
  POISON=$(python3 -c 'import sys; print("%.6e" % (float(sys.argv[1]) * float(sys.argv[2])))' \
           "${BASE_LR:-1e-4}" "$f") || { echo "could not compute poison for factor $f" >&2; exit 3; }
  [ -n "$POISON" ] || { echo "poison came back empty for factor $f — refusing to run" >&2; exit 3; }
  echo "--- prior poisoned x$f  (forced LR = $POISON) ---"
  GOT="$(run_one "x$f" "$POISON")"
  echo "    settled on LR = ${GOT:-?}"

  # PROVE the prior was actually poisoned, rather than trusting that it was. The override
  # path in adaptive_config logs nothing, so the evidence is the planned LR that the LR
  # search reports as its incumbent: with the poison applied that is POISON, not the
  # family-table value. Checking this is not paranoia — the poison expression silently
  # produced an empty string on Python 3.10 for the whole life of this gate, and every
  # "poisoned" run trained on the untouched prior and was scored RECOVERED at ~1.0x.
  # A recovery gate that cannot distinguish a poisoned run from a clean one is worthless,
  # so this aborts rather than reporting a verdict it cannot support.
  SEEN_INC=$(grep -aoE "incumbent=[0-9.e+-]+" "$WORK/logs/lrrec_x${f}.log" 2>/dev/null | tail -1 | cut -d= -f2)
  if [ -z "$SEEN_INC" ]; then
    echo "    !! no incumbent= line in the log — cannot confirm the prior was poisoned" >&2
    exit 4
  fi
  python3 -c 'import sys
want, got = float(sys.argv[1]), float(sys.argv[2])
if abs(got - want) / want > 0.02:
    sys.stderr.write("    !! prior was NOT poisoned: planned incumbent=%s, expected %s\n" % (sys.argv[2], sys.argv[1]))
    sys.exit(4)
print("    confirmed poisoned: planned incumbent = %s" % sys.argv[2])' "$POISON" "$SEEN_INC" || exit 4
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
