#!/usr/bin/env bash
# Check the box can run a faithful smoke BEFORE burning an hour of GPU on it.
#
# Every check here is something that has already cost us a run. The point is to fail
# in ten seconds with a specific message instead of forty minutes into a training run.
set -uo pipefail

REPO_DIR="${REPO_DIR:-$HOME/lostinjamal}"
FAIL=0
ok()   { printf '  \033[32mOK\033[0m    %s\n' "$1"; }
bad()  { printf '  \033[31mFAIL\033[0m  %s\n' "$1"; FAIL=1; }
warn() { printf '  WARN  %s\n' "$1"; }

echo "=== preflight ==="

# The trainer runs under whatever `python` resolves to; container images have it,
# bare Ubuntu images do not.
command -v python >/dev/null 2>&1 && ok "python on PATH ($(python --version 2>&1))" \
  || bad "no \`python\` on PATH — ln -sf \$(which python3) /usr/local/bin/python"

# The pins matter more than they look. Installing axolotl beside the trainer drags
# trl 0.18 -> 0.17, and a smoke on the wrong trl tests a stack the tournament never
# runs: GRPO's scale_rewards is a bool in 0.18 and a string from 0.19 on.
python3 - <<'PY'
import importlib, sys
want = {"torch": None, "transformers": "4.51.3", "trl": "0.18.0", "peft": "0.15.1", "datasets": "3.5.0"}
bad = False
for mod, exp in want.items():
    try:
        v = importlib.import_module(mod).__version__
    except Exception as e:
        print(f"  FAIL  trainer stack: {mod} does not import ({type(e).__name__})"); bad = True; continue
    if exp and not v.startswith(exp):
        print(f"  FAIL  trainer stack: {mod}=={v}, tournament pins {exp}"); bad = True
    else:
        print(f"  OK    {mod}=={v}")
sys.exit(1 if bad else 0)
PY
[ $? -ne 0 ] && FAIL=1

# Tokenisation runs as a SEPARATE process against this interpreter, by absolute path.
# It needs axolotl, and the chat branch additionally needs jinja2 for apply_chat_template.
AXO=/workspace/axo_py/bin/python
if [ -x "$AXO" ]; then
  "$AXO" -c "import axolotl, jinja2; assert tuple(int(x) for x in jinja2.__version__.split('.')[:2]) >= (3,1)" 2>/dev/null \
    && ok "tokenisation stack: axolotl + jinja2>=3.1" \
    || bad "tokenisation stack incomplete — need axolotl and jinja2>=3.1 reachable from $AXO"
else
  bad "no $AXO — the trainer calls this absolute path (see the two-stack note in ops/smoke/README)"
fi

# text_trainer stores cross-process state here; without it train_*.py dies on state["train"].
redis-cli ping >/dev/null 2>&1 && ok "redis responding" || bad "redis not running — redis-server --daemonize yes"

command -v nvidia-smi >/dev/null 2>&1 && {
  FREE=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -1)
  [ "${FREE:-0}" -gt 40000 ] && ok "GPU has ${FREE} MiB free" \
    || warn "only ${FREE} MiB free — another process is holding the GPU, results will be noisy"
} || bad "no nvidia-smi"

# nvidia-smi is not the thing that trains. It talks to the driver directly and answers
# happily inside a container where torch cannot initialise CUDA at all — measured
# 2026-09-07, where nvidia-smi reported two H100s and 81007 MiB free while torch reported
# device_count 0 and every stage of the gate died on
#   ValueError: --tf32 requires Ampere or a newer GPU arch
# on a card that is two generations newer than Ampere. The whole five-path run was spent
# before anything noticed. Ask the library that does the work.
python - <<'PYCHK'
import sys
try:
    import torch
except Exception as exc:
    print(f"TORCH_IMPORT_FAILED {type(exc).__name__}: {exc}"); sys.exit(2)
if not torch.cuda.is_available():
    print("CUDA_UNAVAILABLE"); sys.exit(1)
n = torch.cuda.device_count()
if n < 1:
    print("ZERO_DEVICES"); sys.exit(1)
caps = ",".join(f"{i}:{torch.cuda.get_device_capability(i)[0]}.{torch.cuda.get_device_capability(i)[1]}" for i in range(n))
print(f"OK {n} {caps}")
PYCHK
case $? in
  0) ok "torch sees CUDA ($(python -c "import torch;print(torch.cuda.device_count())" 2>/dev/null) device(s))" ;;
  1) bad "nvidia-smi answers but torch.cuda is unavailable — this box cannot train, and every stage will fail late" ;;
  *) bad "torch could not be imported for the CUDA check" ;;
esac

# Training writes a full checkpoint per save into output_dir and nothing prunes them
# (no save_total_limit anywhere), and the LR ladder gives every attempt its OWN output
# dir. Five paths back to back filled a 969 GB disk on the first real gate run, and the
# failure surfaced three paths later as a confusing "no log" — so check it up front.
FREE_G=$(df -BG --output=avail / 2>/dev/null | tail -1 | tr -dc '0-9')
if [ "${FREE_G:-0}" -ge 100 ]; then
  ok "disk has ${FREE_G}G free"
else
  bad "only ${FREE_G}G free — a five-path gate needs ~100G; clear /workspace/scripts/soutputs"
fi

for d in /cache/datasets /cache/models /app/checkpoints; do
  [ -d "$d" ] || mkdir -p "$d" 2>/dev/null
  [ -d "$d" ] && ok "$d exists" || bad "cannot create $d"
done

echo
[ $FAIL -eq 0 ] && echo "preflight PASSED" || echo "preflight FAILED — fix the above before running the gate"
exit $FAIL
