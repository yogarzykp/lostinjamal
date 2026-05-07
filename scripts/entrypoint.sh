#!/bin/bash
set -e
# Match main's proven pattern: system python (has all deps from training_requirements.txt --system).
# Do NOT activate axo_py venv here — venv is incomplete (only has axolotl) and breaks text_trainer.
# tokenize_*.py subprocess still uses /workspace/axo_py/bin/python explicitly (text_trainer.py:385).
redis-server --daemonize yes 2>/dev/null || echo "[entrypoint] redis-server unavailable, state will use in-memory fallback"
sleep 2  # Give Redis a moment to start up
# Reduce VRAM fragmentation on multi-GPU + gradient_checkpointing.
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
echo "*****Running text trainer"
# Run via system python (matches main branch behavior). System python has full deps.
python -m text_trainer "$@"