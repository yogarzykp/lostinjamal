#!/usr/bin/env bash
# Wait for a long run to finish, and be able to conclude that it DIED.
#
# Every waiter we wrote before this one waited for a success marker:
#
#     until grep -q "driver end" "$log"; do sleep 60; done
#
# A marker only ever proves success, never failure. A run killed at minute 20 stops
# writing, never writes the marker, and the waiter spins forever — and that silence is
# indistinguishable from a healthy run. We used exactly that shape all day on a box that
# has thrown 162 contained Xid 94, which kill processes in precisely that way. A
# 77-minute gate that died at minute 20 would have looked identical to one that was
# working, until someone got bored and checked by hand.
#
# It replaced an earlier bug of the same family — `pgrep -f` matching the waiter's own
# command line, which spun two waiters for ten hours — so this is the second swap. That
# is why identity here comes from a PID FILE rather than a process pattern: a pattern can
# match the watcher, a pid cannot.
#
# Exit codes, and what each is worth:
#
#   0  the marker appeared. Clean.
#   3  bad usage, or the run never started.
#   4  the process is GONE and the marker was never written. This is the case the old
#      waiter could not see at all.
#   6  the marker appeared, but the Xid count ROSE during the run. The result may be
#      complete-looking and still be missing a path that died — so it is reported, not
#      silently accepted.
#   7  the deadline passed while the process was still alive.
#
# There is deliberately NO stall verdict. Detecting a hang needs a threshold, and we
# cannot yet justify one: measured against 34 stored gate logs, the longest gap between
# timestamped lines was 4668s, and that number is meaningless — poison.log holds 7657
# lines of which 22 carry timestamps, so the file grew continuously through the supposed
# quiet. Write times for unstamped lines are recorded nowhere, so no finished log can
# answer it. Instead this REPORTS the longest span without log growth it observed, so the
# first healthy run produces the number. The measuring instrument is this script, so
# there is no second instrument to be wrong.
#
# Read that reported span as an UPPER BOUND on real silence, never as a measurement: a
# file also stops growing when output is buffered rather than when work stops. Anyone
# setting a threshold from it needs that condition, which is why it is written here
# beside the number and not only in a note.
#
# Usage: wait_gate.sh <log> <end-marker> <pidfile> [timeout_s]
set -uo pipefail

LOG="${1:?usage: wait_gate.sh <log> <end-marker> <pidfile> [timeout_s]}"
MARKER="${2:?}"
PIDFILE="${3:?}"
TIMEOUT="${4:-14400}"
POLL="${WAIT_GATE_POLL:-30}"

# Overridable so the tests can inject a dmesg stub that actually increments. A stub that
# returns a constant would let the Xid path pass without ever running.
DMESG_CMD="${WAIT_GATE_DMESG_CMD:-dmesg -T}"

xid_count() {
  # UNKNOWN, not 0, when dmesg cannot be read. A zero here would read exactly like
  # "no faults" — the same shape as an error string that fails to contain a UUID.
  local out
  out=$($DMESG_CMD 2>/dev/null) || { echo "UNKNOWN"; return; }
  [ -z "$out" ] && { echo "UNKNOWN"; return; }
  printf '%s\n' "$out" | grep -c "Xid" || true
}

log_size() { [ -f "$LOG" ] && wc -c < "$LOG" | tr -d ' ' || echo 0; }

[ -f "$PIDFILE" ] || { echo "[wait] no pidfile at $PIDFILE — did the run start?" >&2; exit 3; }
PID=$(tr -d ' \n' < "$PIDFILE")
[ -n "$PID" ] || { echo "[wait] pidfile is empty" >&2; exit 3; }

XID_START=$(xid_count)
echo "[wait] watching pid=$PID log=$LOG marker='$MARKER'"
echo "[wait] xid at start: $XID_START"

start=$(date +%s)
last_size=$(log_size)
last_growth=$start
longest_quiet=0

finish() {   # verdict, message
  local code="$1"; shift
  echo "[wait] longest span without log growth: ${longest_quiet}s"
  echo "[wait]   upper bound on true silence — a buffered writer also stops growing"
  echo "[wait] $*"
  exit "$code"
}

while true; do
  now=$(date +%s)

  size=$(log_size)
  if [ "$size" != "$last_size" ]; then
    last_size=$size
    last_growth=$now
  else
    quiet=$((now - last_growth))
    [ "$quiet" -gt "$longest_quiet" ] && longest_quiet=$quiet
  fi

  if [ -f "$LOG" ] && grep -qa -- "$MARKER" "$LOG"; then
    XID_END=$(xid_count)
    if [ "$XID_START" != "UNKNOWN" ] && [ "$XID_END" != "UNKNOWN" ] \
       && [ "$XID_END" -gt "$XID_START" ]; then
      finish 6 "FINISHED, but Xid rose ${XID_START} -> ${XID_END} during the run. A path may have died without a trace in the summary — check before trusting the result."
    fi
    finish 0 "finished cleanly (xid ${XID_START} -> ${XID_END})"
  fi

  # Order matters: the marker is checked FIRST, so a process that wrote it and exited in
  # the same poll window is not misreported as having vanished.
  #
  # `kill -0` alone is not enough, and the tests caught it: it SUCCEEDS on a zombie. A
  # process whose parent has not reaped it is finished — it has stopped doing work and
  # will never write the marker — but its pid still answers. Left at `kill -0` this
  # waiter reports "still alive" for a run that died, which is the exact silence it
  # exists to break. So the state is checked too, and Z counts as gone.
  if ! kill -0 "$PID" 2>/dev/null; then
    finish 4 "process $PID is GONE and '$MARKER' was never written — the run died. This is the case a marker-only waiter cannot see."
  fi
  pstate=$(ps -o state= -p "$PID" 2>/dev/null | tr -d ' ')
  case "$pstate" in
    Z*) finish 4 "process $PID is a ZOMBIE (state=$pstate) and '$MARKER' was never written — it has stopped working; its pid answering is not the same as it running." ;;
  esac

  if [ $((now - start)) -ge "$TIMEOUT" ]; then
    finish 7 "deadline ${TIMEOUT}s passed with pid $PID still alive"
  fi

  sleep "$POLL"
done
