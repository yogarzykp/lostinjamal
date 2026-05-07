#!/bin/bash
# Pre-submit smoke test (lesson learned from 2026-05-07 tournament loss).
# REQUIRED to run before submitting any commit hash to G.O.D miner endpoint.
# Validates that the dockerfile + entrypoint + scripts work in a FRESH validator-style environment.
#
# Usage: bash examples/pre-submit-smoke-test.sh [commit_hash]
#
# Exit code 0 = safe to submit; non-zero = DO NOT submit.

set -e

COMMIT_HASH="${1:-HEAD}"
TAG="text-jagger-smoke:$(echo $COMMIT_HASH | cut -c1-8)"

echo "===== Pre-submit smoke test: $COMMIT_HASH ====="

# 1. Build image FRESH from miner repo at given commit (no cache, no mount).
echo ""
echo "[1/5] Build image fresh (no cache, mimics validator)"
git stash 2>/dev/null || true
git checkout "$COMMIT_HASH" 2>&1 | tail -1
docker build --no-cache -t "$TAG" -f dockerfiles/standalone-text-trainer.dockerfile . 2>&1 | tail -20
git checkout - 2>&1 | tail -1
git stash pop 2>/dev/null || true

# 2. Verify ENTRYPOINT exists
echo ""
echo "[2/5] Verify ENTRYPOINT script"
docker run --rm --entrypoint cat "$TAG" /workspace/scripts/entrypoint.sh > /dev/null
echo "  entrypoint.sh present in image"

# 3. Activate venv + import state_manager (the bug that killed us)
echo ""
echo "[3/5] axo_py venv import smoke test"
docker run --rm --entrypoint bash "$TAG" -c "
source /workspace/axo_py/bin/activate
python3 -c '
import sys; sys.path.insert(0, \"/workspace/scripts\")
from state_manager import get_state, set_state
print(\"  state_manager OK\")
import redis
print(f\"  redis OK (v={redis.__version__})\")
'
"

# 4. Critical-path imports test (text_trainer.py imports)
echo ""
echo "[4/5] text_trainer.py critical imports"
docker run --rm --entrypoint bash "$TAG" -c "
source /workspace/axo_py/bin/activate
python3 -c '
import sys; sys.path.insert(0, \"/workspace/scripts\")
import torch, transformers, datasets, trl, peft, bitsandbytes
print(f\"  torch={torch.__version__} transformers={transformers.__version__}\")
print(f\"  trl={trl.__version__} peft={peft.__version__}\")
import redis, wandb, loguru, fastapi, textstat
print(\"  entrypoint-lazy deps OK\")
from huggingface_hub import HfApi
print(\"  huggingface_hub OK\")
'
"

# 5. Dry-run text_trainer.py argparse (should print help, not crash)
echo ""
echo "[5/5] text_trainer.py --help"
docker run --rm --entrypoint bash "$TAG" -c "
source /workspace/axo_py/bin/activate
cd /workspace/scripts && python3 text_trainer.py --help 2>&1 | head -5
"

echo ""
echo "===== ALL CHECKS PASSED — safe to submit $COMMIT_HASH ====="
docker rmi "$TAG" 2>&1 | tail -1
