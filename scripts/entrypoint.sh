#!/bin/bash
set -e
# redis-server best-effort. state_manager.py has in-memory fallback if redis unavailable.
redis-server --daemonize yes 2>/dev/null || echo "[entrypoint] redis-server unavailable, state will use in-memory fallback"
sleep 2  # Give Redis a moment to start up
# Reduce VRAM fragmentation on multi-GPU + gradient_checkpointing (Qwen 7B 2-GPU).
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
echo "*****Running text trainer"
# Image variants differ — try .grpo_env first, then axo_py, else system python.
if [ -f /workspace/.grpo_env/bin/activate ]; then
    source /workspace/.grpo_env/bin/activate
    # Symlink axo_py → .grpo_env if missing (text_trainer hardcodes axo_py for tokenize).
    [ -d /workspace/axo_py ] || ln -s /workspace/.grpo_env /workspace/axo_py
elif [ -f /workspace/axo_py/bin/activate ]; then
    source /workspace/axo_py/bin/activate
fi
# Lazy install missing deps (some image rebuilds drop these). Don't mask install errors.
python3 -c "import colorama, loguru, fastapi, redis, pydantic_settings, textstat" 2>/dev/null \
  || pip install -q colorama loguru fastapi redis pydantic-settings python-dotenv toml textstat langcheck detoxify \
  || echo "[entrypoint] some deps failed to install — relying on fallbacks"
# Verify redis Python module (state_manager has in-memory fallback if missing)
python3 -c "import redis" 2>/dev/null \
  || echo "[entrypoint] redis Python module missing — state_manager will use in-memory fallback"
python3 /workspace/scripts/text_trainer.py "$@"