#!/usr/bin/env bash
# Block until the GPU has actually released its memory.
#
# adaptive_config sizes the batch from LIVE free VRAM (`estimate_max_batch_size`), so a
# run started before the previous one's memory is reclaimed reads a starved GPU and
# plans a tiny batch. Measured: back-to-back runs on the same task produced
# `1-GPU empirical bucket: batch=100` and `batch=2` — an 8x difference in steps, enough
# to starve the LR ladder of budget and silently void a comparison.
#
# The failure is invisible in the result: both runs "succeed", and only the batch line
# in the log says they were not the same experiment. Any harness that runs two configs
# back to back and compares them has to wait here first.
#
# Usage:  wait_gpu.sh [min_free_mib] [timeout_s]
set -uo pipefail
MIN_FREE="${1:-70000}"
TIMEOUT="${2:-300}"

command -v nvidia-smi >/dev/null 2>&1 || { echo "[gpu] no nvidia-smi; not waiting"; exit 0; }

start=$(date +%s)
while true; do
  free=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -1)
  [ "${free:-0}" -ge "$MIN_FREE" ] && { echo "[gpu] ${free} MiB free — proceeding"; exit 0; }
  now=$(date +%s)
  if [ $((now - start)) -ge "$TIMEOUT" ]; then
    echo "[gpu] WARNING: only ${free} MiB free after ${TIMEOUT}s; proceeding anyway." >&2
    echo "[gpu] the batch this run plans will not be comparable to one planned on a free GPU." >&2
    exit 0
  fi
  sleep 5
done
