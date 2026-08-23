# Kept at TWO paths on purpose, byte-for-byte identical.
#
# The validator resolves a miner's dockerfile from a tuple and takes the first that
# exists (G.O.D trainer/constants.py, trainer/runtime.py _resolve_dockerfile_path):
#
#     ops/docker/standalone-text-trainer.dockerfile     <- DEFAULT, tried first
#     dockerfiles/standalone-text-trainer.dockerfile    <- LEGACY, tried second
#
# We used to exist only at the legacy path. That resolves today, but the fallback's own
# name announces the intent to drop it, and when neither path exists the resolver raises
# FileNotFoundError — the task never starts. Not a slow build: no build. And the branch
# that selects this tuple is a bare `else`, so it covers every task type that is not an
# image task, not just text.
#
# Shipping BOTH rather than moving: the default path serves validators that already
# prefer it, the legacy path serves any that have not learned it yet. Deleting the legacy
# copy would trade one risk for a different one.
#
# The build context is the repo ROOT for either location (runtime.py passes
# context_path=local_repo_path), so `COPY scripts ...` below resolves the same way from
# both. Verified in G.O.D a2b14db before duplicating.
#
# tests/test_dockerfile_paths.py fails if the two copies drift. They must not: the
# validator would build one while our own tooling reads the other, so a green local dry
# run would say nothing about what production builds.

FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04

# System dependencies
RUN apt-get update && apt-get install -y \
    vim \
    zip \
    tmux \
    iotop \
    nvtop \
    bmon \
    wget \
    nano \
    zsh \
    htop \
    redis-server \
    && rm -rf /var/lib/apt/lists/*
# Default dir
RUN mkdir -p /workspace
RUN mkdir -p /cache
RUN mkdir -p /workspace/scripts/datasets
RUN mkdir -p /app/checkpoints
WORKDIR /workspace/scripts
# Copy current folder to /workspace/auto_ml
COPY scripts /workspace/scripts
# Make entrypoint script executable
RUN chmod +x /workspace/scripts/entrypoint.sh
# Pytorch (Auto-selects backend https://docs.astral.sh/uv/guides/integration/pytorch/#automatic-backend-selection)

# Create a virtual environment for data generation
RUN python -m venv /workspace/axo_py
RUN bash -c "source /workspace/axo_py/bin/activate && \
    pip install uv && \
    pip install -U packaging==23.2 setuptools==75.8.0 wheel ninja && \
    uv pip install --no-build-isolation axolotl==0.9.1 && \
    pip install requests==2.32.3 && \
    pip install redis==7.0.1 colorama loguru fastapi pydantic-settings python-dotenv toml textstat langcheck detoxify wandb && \
    deactivate"


# install the main dependencies
RUN pip install uv && \
    pip install -U packaging==23.2 setuptools==75.8.0 wheel ninja && \
    uv pip install -r /workspace/scripts/training_requirements.txt --system && \
    pip install hf_transfer==0.1.9 && \
    pip install tenacity==9.1.2 && \
    pip install tiktoken==0.9.0 && \
    pip install flash-attn==v2.7.4.post1 --no-build-isolation && \
    uv pip install vllm==0.8.3 --system && \
    pip install "fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0"

ENTRYPOINT ["./entrypoint.sh"]