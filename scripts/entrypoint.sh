#!/bin/bash
set -e
redis-server --daemonize yes
sleep 2  # Give Redis a moment to start up
# Reduce VRAM fragmentation on multi-GPU + gradient_checkpointing (Qwen 7B 2-GPU).
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
echo "*****Running text trainer"
# Activate the GRPO env (has transformers etc) — match run_text_trainer.sh path.
if [ -f /workspace/.grpo_env/bin/activate ]; then
    source /workspace/.grpo_env/bin/activate
fi
python3 /workspace/scripts/text_trainer.py "$@"