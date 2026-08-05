# Attribution

This file carries the attribution notices for derivative work in this repository.

It is kept separate from `NOTICE` because the G.O.D tournament validator requires `NOTICE`
to match the upstream Gradients-on-Demand file verbatim
(`validator/tournament/github_validation.py::validate_repo_license` performs an exact
line-by-line comparison and rejects the repository on any difference). Moving the derivative-work
attribution here preserves it in full while keeping `NOTICE` contract-compliant.

The upstream `NOTICE` and `LICENSE.md` remain in the repository root, unmodified.

---

## Upstream work

**Gradients-on-Demand** — Copyright 2025 Grads LLC.
Licensed under the Apache License, Version 2.0. See `LICENSE.md` and `NOTICE`.
Gradients.io (https://gradients.io) is owned by Grads LLC.

## Derivative work

**text-jagger (modifications and derivative work)**
Copyright 2026 Zaydensth <168814481+Zaydensth@users.noreply.github.com>

Source repository: https://github.com/Zaydensth/text-jagger
Authoritative branches:
  - main (= safe-tournament-2026-05-21)
  - experimental-tournament-2026-05-21

Modifications include but are not limited to:
  - Adaptive hyperparameter optimization (scripts/adaptive_config.py)
  - Per-family LR tables and dynamics-driven HP selection
  - Reward classifier port + format-theme LR override (GRPO)
  - Safety layer with cascade-to-legacy on config-builder crash
  - Fast-crash detection in training state machine
  - Vocab-aware and DPO-aware batch bucket caps
  - Bayesian/GP-EI augmentation for LR sweep
  - Per-layer LR optimizer (LARS-style)
  - Model fingerprint + anonymization-resistant detection

These modifications are licensed under the same Apache License, Version 2.0, as the underlying
work. The original copyright notice and license terms remain in effect.

When redistributing, modifying, or deriving work from these modifications, you must preserve this
attribution and credit:

    Zaydensth (https://github.com/Zaydensth/text-jagger)

If you encounter this software in another repository or deployment that does not credit
Zaydensth, it likely constitutes unauthorized redistribution.
