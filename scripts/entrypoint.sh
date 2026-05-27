#!/bin/bash
# Match main's proven pattern: system python (has all deps from training_requirements.txt --system).
# Do NOT activate axo_py venv here — venv is incomplete (only has axolotl) and breaks text_trainer.
# tokenize_*.py subprocess still uses /workspace/axo_py/bin/python explicitly (text_trainer.py:385).
#
# EXP-LLM-WARMSTART 2026-05-27: optional embedded vLLM sidecar serving
# Qwen2.5-14B-Instruct-AWQ (~8GB, ~22% GPU mem) as Tier-2 LR prior fallback.
# Sourced from llm_decider_defaults.env. Fail-safe: if sidecar fails to start,
# training continues (try_llm_warmstart returns None on network/parse error).

set -e

# ── NCCL robustness for constrained Docker environments ──
# Validator may run this container without --shm-size / --ipc=host, leaving
# /dev/shm at default 64MB which is insufficient for NCCL multi-GPU comm.
# Disabling SHM forces NCCL to use CUDA P2P which is typically faster anyway.
export NCCL_SHM_DISABLE="${NCCL_SHM_DISABLE:-1}"
export NCCL_P2P_DISABLE="${NCCL_P2P_DISABLE:-0}"

DEFAULTS_FILE="/workspace/scripts/llm_decider_defaults.env"
if [ -f "${DEFAULTS_FILE}" ]; then
  # shellcheck disable=SC1090
  source "${DEFAULTS_FILE}"
fi

cleanup() {
  if [ -n "${LLM_SERVER_PID:-}" ]; then
    kill "${LLM_SERVER_PID}" 2>/dev/null || true
  fi
}
trap cleanup EXIT

redis-server --daemonize yes 2>/dev/null || echo "[entrypoint] redis-server unavailable, state will use in-memory fallback"
sleep 2  # Give Redis a moment to start up

# Reduce VRAM fragmentation on multi-GPU + gradient_checkpointing.
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

# ── Optional embedded vLLM sidecar for LLM warmstart (EXP only) ──
TASK_TYPE=""
ARGS=("$@")
for ((i = 0; i < ${#ARGS[@]}; i++)); do
  if [ "${ARGS[$i]}" = "--task-type" ] && [ $((i + 1)) -lt ${#ARGS[@]} ]; then
    TASK_TYPE="${ARGS[$((i + 1))]}"
    break
  fi
done

TASK_TYPE_ENABLED=0
if [ -n "${TASK_TYPE}" ] && [ -n "${TRAINING_LLM_DECIDER_TASK_TYPES:-}" ]; then
  IFS=',' read -ra ALLOWED_TASK_TYPES <<< "${TRAINING_LLM_DECIDER_TASK_TYPES}"
  for allowed in "${ALLOWED_TASK_TYPES[@]}"; do
    if [ "${TASK_TYPE}" = "${allowed// /}" ]; then
      TASK_TYPE_ENABLED=1
      break
    fi
  done
fi

if [ "${TRAINING_LLM_DECIDER_ENABLED:-0}" = "1" ] && [ "${TRAINING_LLM_SERVER_EMBEDDED:-0}" = "1" ] && [ "${TASK_TYPE_ENABLED}" = "1" ]; then
  LLM_SERVER_HOST="${TRAINING_LLM_SERVER_HOST:-127.0.0.1}"
  LLM_SERVER_PORT="${TRAINING_LLM_SERVER_PORT:-8000}"
  LLM_SERVER_MODEL="${TRAINING_LLM_SERVER_MODEL:-${TRAINING_LLM_DECIDER_MODEL:-}}"
  LLM_SERVER_GPU_MEMORY_UTILIZATION="${TRAINING_LLM_SERVER_GPU_MEMORY_UTILIZATION:-0.22}"
  LLM_SERVER_MAX_MODEL_LEN="${TRAINING_LLM_SERVER_MAX_MODEL_LEN:-8192}"
  LLM_SERVER_STARTUP_ATTEMPTS="${TRAINING_LLM_SERVER_STARTUP_ATTEMPTS:-90}"
  LLM_SERVER_STARTUP_SLEEP_SECONDS="${TRAINING_LLM_SERVER_STARTUP_SLEEP_SECONDS:-2}"
  LLM_SERVER_USE_V1="${TRAINING_LLM_SERVER_USE_V1:-0}"

  if [ -z "${LLM_SERVER_MODEL}" ]; then
    echo "[entrypoint] Embedded LLM server requested but no model path. Skipping sidecar."
  else
    export TRAINING_LLM_DECIDER_MODEL="${TRAINING_LLM_DECIDER_MODEL:-${LLM_SERVER_MODEL}}"
    export TRAINING_LLM_DECIDER_BASE_URL="http://${LLM_SERVER_HOST}:${LLM_SERVER_PORT}/v1"

    VLLM_CMD=(
      python -m vllm.entrypoints.openai.api_server
      --host "${LLM_SERVER_HOST}"
      --port "${LLM_SERVER_PORT}"
      --model "${LLM_SERVER_MODEL}"
      --gpu-memory-utilization "${LLM_SERVER_GPU_MEMORY_UTILIZATION}"
      --max-model-len "${LLM_SERVER_MAX_MODEL_LEN}"
      --dtype "${TRAINING_LLM_SERVER_DTYPE:-auto}"
    )

    [ -n "${TRAINING_LLM_SERVER_TENSOR_PARALLEL_SIZE:-}" ] && VLLM_CMD+=(--tensor-parallel-size "${TRAINING_LLM_SERVER_TENSOR_PARALLEL_SIZE}")
    [ -n "${TRAINING_LLM_SERVER_QUANTIZATION:-}" ] && VLLM_CMD+=(--quantization "${TRAINING_LLM_SERVER_QUANTIZATION}")
    [ "${TRAINING_LLM_SERVER_TRUST_REMOTE_CODE:-0}" = "1" ] && VLLM_CMD+=(--trust-remote-code)

    echo "*****Starting embedded LLM advisor (Tier-2 LR prior)"
    echo "  Model: ${LLM_SERVER_MODEL}"
    echo "  Base URL: ${TRAINING_LLM_DECIDER_BASE_URL}"

    if [ -n "${TRAINING_LLM_SERVER_CUDA_VISIBLE_DEVICES:-}" ]; then
      VLLM_USE_V1="${LLM_SERVER_USE_V1}" CUDA_VISIBLE_DEVICES="${TRAINING_LLM_SERVER_CUDA_VISIBLE_DEVICES}" "${VLLM_CMD[@]}" &
    else
      VLLM_USE_V1="${LLM_SERVER_USE_V1}" "${VLLM_CMD[@]}" &
    fi
    LLM_SERVER_PID=$!

    for attempt in $(seq 1 "${LLM_SERVER_STARTUP_ATTEMPTS}"); do
      if wget -qO- "${TRAINING_LLM_DECIDER_BASE_URL}/models" >/dev/null 2>&1; then
        echo "*****Embedded LLM advisor READY"
        break
      fi
      if ! kill -0 "${LLM_SERVER_PID}" 2>/dev/null; then
        echo "[entrypoint] LLM advisor exited unexpectedly. Continuing training without warmstart."
        unset LLM_SERVER_PID
        break
      fi
      sleep "${LLM_SERVER_STARTUP_SLEEP_SECONDS}"
      if [ "${attempt}" = "${LLM_SERVER_STARTUP_ATTEMPTS}" ]; then
        echo "[entrypoint] Timed out waiting for LLM advisor. Continuing without warmstart."
        kill "${LLM_SERVER_PID}" 2>/dev/null || true
        unset LLM_SERVER_PID
      fi
    done
  fi
elif [ "${TRAINING_LLM_DECIDER_ENABLED:-0}" = "1" ] && [ "${TASK_TYPE_ENABLED}" = "0" ]; then
  echo "[entrypoint] LLM advisor skipped for task type: ${TASK_TYPE:-unknown}"
fi

echo "*****Running text trainer"
# Run via system python (matches main branch behavior). System python has full deps.
python -m text_trainer "$@"
