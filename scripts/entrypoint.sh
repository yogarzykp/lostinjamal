#!/bin/bash
set -e
redis-server --daemonize yes
sleep 2  # Give Redis a moment to start up
# Reduce VRAM fragmentation on multi-GPU + gradient_checkpointing (Qwen 7B 2-GPU).
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
echo "*****Running text trainer"
# Image variants differ — try .grpo_env first, then axo_py, else system python.
if [ -f /workspace/.grpo_env/bin/activate ]; then
    source /workspace/.grpo_env/bin/activate
elif [ -f /workspace/axo_py/bin/activate ]; then
    source /workspace/axo_py/bin/activate
fi
# Lazy install missing deps (some image rebuilds drop these).
python3 -c "import colorama, loguru, fastapi, redis, pydantic_settings" 2>/dev/null || pip install -q colorama loguru fastapi redis pydantic-settings python-dotenv toml 2>&1 | tail -2
python3 /workspace/scripts/text_trainer.py "$@"