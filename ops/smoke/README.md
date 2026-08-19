# Pre-submission gate

**Nothing enters a tournament without `./gate.sh` passing on the exact commit being
submitted.** Not the branch, not "basically the same code" — the commit.

```bash
cd ops/smoke
REPO_DIR=/root/lostinjamal ./gate.sh        # all five paths, ~45 min at HOURS=0.15
./gate.sh instruct kl                       # a subset while iterating
```

Exit 0 means safe to submit. Any other exit means do not.

## Why this exists

Six real defects reached the repo while 318 unit tests were green. Every one lived at a
seam that unit tests structurally cannot reach:

| defect | seam |
|---|---|
| flash-attn fallback wrapped one loader, not `load_lora_model` | two functions doing the same job |
| KL term OOM'd, was caught, run continued on plain CE | a memory limit, only on real hardware |
| checkpoint selection compared a KL-weighted number against a raw `eval_loss` | two code paths, each correct alone |
| `train_dpo` recomputed `steps_per_epoch` with a bare `//` 116 lines after the guarded version | one function, later overwrite |
| adaptive `max_length` computed and never consumed | two OS processes, JSON between them |
| dedup collapsed 3000 chat rows to 1 | one task type's data shape |

Unit tests verify functions. These were all about how functions meet.

## Exit codes prove almost nothing here

Every safety net in this codebase keeps going rather than dying — correct for a
tournament, and the reason a green exit is weak evidence. Four of the six above produced
a *successful* run. So `gate.sh` reads the logs and asserts on specific lines.

Each assertion maps to a defect that actually shipped. **When a new one gets through, add
a gate for it** — that is how this file earns its keep.

| gate | catches |
|---|---|
| `PLAN: max_len=N` equals `trainer: max_length: N` | the plumbing breaking again |
| `[split]` has train > 0 and dev > 0 | an empty split killing the packer before step 1 |
| `[dedup]` kept ≥ 50% of rows | a dataset collapsing to nothing |
| zero `KL term failed` | the objective silently becoming plain CE |
| at least one `[kl] checkpoint metric:` | the KL path never running at all |
| GRPO rewards vary | constant reward, so every advantage is zero |
| `Processing chat template dataset type` | chat rows training as plain instruct text |
| `Training successfully done` | the NaN scan and architectures restore never ran |
| `architectures` present in config.json | the validator's `is_finetune` check failing outright |

## The box needs two Python stacks

`preflight.sh` checks this, but the reason is worth stating: tokenisation runs as a
**separate process** from training, by absolute path, and the two stacks conflict.
Installing axolotl beside the trainer drags `trl` 0.18 → 0.17, and `scale_rewards` is a
bool in 0.18 but a string from 0.19 on — so a smoke on the wrong `trl` tests a stack the
tournament never runs, and reports failures that are not real (or passes that are not
either).

| stack | contents | used by |
|---|---|---|
| system python | torch, transformers 4.51.3, trl 0.18.0, peft 0.15.1, datasets 3.5.0 | `train_*.py` |
| `/workspace/axo_py/bin/python` | axolotl 0.9.1 + jinja2 ≥ 3.1 | `tokenize_*.py` |

On Ubuntu 22.04 GPU images `ensurepip` is broken and the distro `virtualenv` uses the
Debian `local/` layout, so `python3 -m venv` yields a directory whose python reports
`sys.prefix = /usr` — not a venv, and every `pip install` through it lands in the system.
What works:

```bash
pip install --target /opt/axo --no-build-isolation axolotl==0.9.1
pip install --target /opt/axo "jinja2>=3.1.0"
mkdir -p /workspace/axo_py/bin
printf '#!/bin/sh\nexec env PYTHONPATH=/opt/axo /usr/bin/python3 "$@"\n' > /workspace/axo_py/bin/python
chmod +x /workspace/axo_py/bin/python
```

Docker with the repo's own dockerfile is more faithful still and worth using when a
stronger guarantee is wanted.

Also needed: the base model under `/cache/models/<org>--<name>` (the container has a
separate downloader step), `redis-server --daemonize yes`, and `python` on PATH.

## What the numbers do and do not mean

The replay datasets are rebuilt from the public HuggingFace source the task named,
because the validator's presigned S3 URLs expire within days. The row sample and the
held-out split are ours, not the validator's.

**So the losses are not comparable to the leaderboard.** They are for detecting
regressions, crashes and deadline pressure in our own code. A comparison is only ever
valid between two runs of the same harness.
