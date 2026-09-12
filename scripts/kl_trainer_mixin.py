"""Trainer that optimises the objective a KL-flagged task is actually scored on.

On a task the validator marks USE_KL, our rank comes from

    eval_loss + kl_coef * KL(finetuned || base)

not from eval_loss. Training plain cross-entropy there optimises one thing while
being measured on another, and nothing in the run looks wrong — the loss curve
is healthy, the score is just worse than it should have been.

Two levels of response are possible and they are not equivalent:

* Select checkpoints on the weighted metric. Cheap, but every checkpoint on a
  plain-CE trajectory lies on the same (CE, KL) path, so selection can only pick
  a point on a path it did not choose.
* Train the weighted objective. This moves the path itself, producing
  checkpoints with lower CE at equal KL than selection alone can reach.

We do both; this class is the second half.

Reference logits come from `disable_adapter()`, so the "base model" is the same
weights with the adapter switched off — no second model in memory. That is
standard PEFT practice (TRL's DPOTrainer uses it when no explicit reference is
supplied) and is why adaptive_config forces the LoRA path on KL-flagged tasks
regardless of model size: without an adapter to disable there is no cheap
reference, and the exact objective stops being affordable.

The KL itself lives in kl_objective.py, pinned against a transcription of the
validator's own code in tests/test_kl_validator_parity.py.
"""

import torch

from kl_objective import instruct_kl_tensor


class KLWeightedTrainerMixin:
    """Adds `kl_coef * KL(finetuned || base)` to the training loss.

    Mix in ahead of transformers.Trainer:

        class MyTrainer(KLWeightedTrainerMixin, Trainer):
            pass
        trainer = MyTrainer(..., kl_coef=0.8)

    With `kl_coef` unset or zero the mixin is inert and `compute_loss` is the
    stock implementation, so a non-KL task runs exactly as it does today.
    """

    def __init__(self, *args, kl_coef: float = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.kl_coef = kl_coef
        self._kl_last = None
        self._kl_disabled_reason = None
        # Steps trained on plain CE while KL was requested. A KL-scored task that ran
        # CE-only for most of its steps is a quiet loss; the count makes it a loud one.
        self._kl_off_steps = 0
        self._labels_missing_said = False
        if kl_coef:
            print(f"[kl-trainer] composite objective active, kl_coef={kl_coef}", flush=True)

    def _reference_logits(self, model, inputs):
        """Base-model logits for this batch: same weights, adapter switched off.

        Returns None when the model has no adapter to disable, which is the
        signal to fall back to plain cross-entropy rather than guess a reference.
        """
        base = getattr(model, "module", model)
        disable = getattr(base, "disable_adapter", None)
        if disable is None:
            return None

        forward_inputs = {
            k: v for k, v in inputs.items() if k in ("input_ids", "attention_mask", "position_ids")
        }
        with torch.no_grad():
            with disable():
                return base(**forward_inputs).logits

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        ce_loss, outputs = super().compute_loss(model, inputs, return_outputs=True, **kwargs)

        if not self.kl_coef:
            return (ce_loss, outputs) if return_outputs else ce_loss

        labels = inputs.get("labels")
        if labels is None:
            # Trainer pops `labels` when label_smoothing_factor != 0, and the KL term
            # needs them. Stock CE on a KL-scored task must not be silent.
            self._kl_last = None
            self._kl_off_steps += 1
            if not self._labels_missing_said:
                self._labels_missing_said = True
                print("[kl-trainer] KL term inactive: no labels in the batch (label smoothing on?) — "
                      "training plain CE on a KL-scored task", flush=True)
            return (ce_loss, outputs) if return_outputs else ce_loss

        try:
            ref_logits = self._reference_logits(model, inputs)
            if ref_logits is None:
                self._kl_last = None
                self._kl_off_steps += 1
                if self._kl_disabled_reason is None:
                    self._kl_disabled_reason = "model exposes no disable_adapter()"
                    print(
                        f"[kl-trainer] KL term inactive: {self._kl_disabled_reason} — "
                        f"training plain CE. The scored metric is still weighted.",
                        flush=True,
                    )
                return (ce_loss, outputs) if return_outputs else ce_loss

            kl = instruct_kl_tensor(ref_logits, outputs.logits, labels)
            self._kl_last = float(kl.detach())
            if self._kl_disabled_reason is not None:
                # A transient failure (an OOM on the reference forward, say) that then
                # clears must be visible as a recovery, not read afterwards as "the KL
                # term died at step N" when the log later shows kl values again.
                print(f"[kl-trainer] KL term recovered after {self._kl_off_steps} CE-only step(s) "
                      f"(last failure: {self._kl_disabled_reason})", flush=True)
                self._kl_disabled_reason = None
            total = ce_loss + self.kl_coef * kl.to(ce_loss.dtype)
        except Exception as exc:
            # A failure here must not kill the run: plain CE still trains a usable
            # model, where a crash submits nothing at all. Report once per outage,
            # loudly — a silently CE-only run on a KL-scored task is a quiet loss.
            # And drop the stale value: `log` used to keep injecting the LAST good kl
            # into every CE-only step's line, so a post-run reader saw KL "applied"
            # on steps where it was not.
            self._kl_last = None
            self._kl_off_steps += 1
            if self._kl_disabled_reason is None:
                self._kl_disabled_reason = f"{type(exc).__name__}: {exc}"
                print(f"[kl-trainer] KL term failed ({self._kl_disabled_reason}) — plain CE", flush=True)
            return (ce_loss, outputs) if return_outputs else ce_loss

        return (total, outputs) if return_outputs else total

    def log(self, logs, *args, **kwargs):
        """Surface the KL term alongside the loss so a run can be read afterwards."""
        if self._kl_last is not None or self._kl_off_steps:
            logs = dict(logs)
            if self._kl_last is not None:
                logs["kl"] = round(self._kl_last, 6)
            if self._kl_off_steps:
                # Absence of `kl` says this step was CE-only; the running count says
                # how much of the run was.
                logs["kl_off_steps"] = self._kl_off_steps
        return super().log(logs, *args, **kwargs)
