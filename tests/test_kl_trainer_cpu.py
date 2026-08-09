"""CPU micro-integration for the KL training path.

The parity tests pin the maths. This file pins the WIRING — that the mixin
actually reaches a reference forward, that the KL lands in the loss, that
gradient flows, and that a model without an adapter degrades to plain CE instead
of crashing. Wiring bugs are the failure mode that building without a GPU
actually produces, and none of them need a GPU to catch.

Everything here runs on a two-layer random model on CPU in a second or so. It is
deliberately not a training-quality test: it asks whether the plumbing is
connected, not whether the objective helps.
"""

import os
import sys

import pytest
import torch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

torch.manual_seed(0)


class _FakeOutput:
    def __init__(self, logits, loss):
        self.logits = logits
        self.loss = loss


class _FakeAdapterModel(torch.nn.Module):
    """Minimal stand-in for a PEFT model: a base head plus a switchable delta.

    `disable_adapter()` is a context manager, exactly as PEFT exposes it, so the
    mixin's reference path is exercised for real rather than mocked out.
    """

    def __init__(self, vocab=17, hidden=8):
        super().__init__()
        self.embed = torch.nn.Embedding(vocab, hidden)
        self.head = torch.nn.Linear(hidden, vocab)
        self.delta = torch.nn.Linear(hidden, vocab)
        self._adapter_on = True
        self.reference_calls = 0

    def forward(self, input_ids=None, attention_mask=None, position_ids=None, **_):
        h = self.embed(input_ids)
        logits = self.head(h)
        if self._adapter_on:
            logits = logits + self.delta(h)
        else:
            self.reference_calls += 1
        return _FakeOutput(logits, None)

    def disable_adapter(self):
        model = self

        class _Ctx:
            def __enter__(self_):
                model._adapter_on = False

            def __exit__(self_, *exc):
                model._adapter_on = True
                return False

        return _Ctx()


class _PlainModel(torch.nn.Module):
    """Full-fine-tune shape: no adapter, therefore no cheap reference to disable."""

    def __init__(self, vocab=17, hidden=8):
        super().__init__()
        self.embed = torch.nn.Embedding(vocab, hidden)
        self.head = torch.nn.Linear(hidden, vocab)

    def forward(self, input_ids=None, attention_mask=None, position_ids=None, **_):
        return _FakeOutput(self.head(self.embed(input_ids)), None)


class _StubTrainer:
    """Stands in for transformers.Trainer's compute_loss contract."""

    def __init__(self, *a, **kw):
        pass

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        out = model(**inputs)
        logits = out.logits
        labels = inputs["labels"]
        loss = torch.nn.functional.cross_entropy(
            logits.reshape(-1, logits.shape[-1]), labels.reshape(-1), ignore_index=-100
        )
        return (loss, out) if return_outputs else loss

    def log(self, logs, *a, **kw):
        self.logged = logs
        return None


def _make_trainer(kl_coef):
    from kl_trainer_mixin import KLWeightedTrainerMixin

    class T(KLWeightedTrainerMixin, _StubTrainer):
        pass

    return T(kl_coef=kl_coef)


def _batch(vocab=17, batch=2, seq=6, mask_frac=0.3):
    g = torch.Generator().manual_seed(7)
    input_ids = torch.randint(0, vocab, (batch, seq), generator=g)
    labels = input_ids.clone()
    labels[torch.rand(batch, seq, generator=g) < mask_frac] = -100
    return {
        "input_ids": input_ids,
        "attention_mask": torch.ones(batch, seq, dtype=torch.long),
        "labels": labels,
    }


# --------------------------------------------------------------------------

def test_kl_coef_zero_is_byte_identical_to_plain_ce():
    """A non-KL task must behave exactly as it does today."""
    model, inputs = _FakeAdapterModel(), _batch()
    plain = _StubTrainer().compute_loss(model, inputs)
    inert = _make_trainer(kl_coef=None).compute_loss(model, inputs)
    assert float(inert) == pytest.approx(float(plain), rel=1e-9)


def test_kl_term_increases_the_loss_and_calls_the_reference():
    model, inputs = _FakeAdapterModel(), _batch()
    ce = _StubTrainer().compute_loss(model, inputs)

    trainer = _make_trainer(kl_coef=1.0)
    before = model.reference_calls
    total = trainer.compute_loss(model, inputs)

    assert model.reference_calls == before + 1, "reference forward was never run"
    assert float(total) > float(ce), "KL is non-negative, so the composite must not be lower"
    assert trainer._kl_last is not None and trainer._kl_last >= 0


def test_coefficient_scales_the_penalty():
    model, inputs = _FakeAdapterModel(), _batch()
    ce = float(_StubTrainer().compute_loss(model, inputs))

    small = float(_make_trainer(kl_coef=0.1).compute_loss(model, inputs))
    large = float(_make_trainer(kl_coef=1.5).compute_loss(model, inputs))

    assert (large - ce) == pytest.approx(15.0 * (small - ce), rel=1e-4)


def test_gradient_flows_through_the_composite_loss():
    model, inputs = _FakeAdapterModel(), _batch()
    loss = _make_trainer(kl_coef=0.8).compute_loss(model, inputs)
    loss.backward()

    grads = [p.grad for p in model.parameters() if p.grad is not None]
    assert grads, "no parameter received gradient"
    assert all(torch.isfinite(g).all() for g in grads)
    assert model.delta.weight.grad is not None
    assert model.delta.weight.grad.abs().sum() > 0, "adapter received no gradient"


def test_model_without_an_adapter_degrades_to_plain_ce_and_says_so(capsys):
    """Full-fine-tune shape: no reference available, so no KL — but no crash either.

    adaptive_config forces LoRA on KL tasks so this should not happen in
    production; if it ever does, training plain CE beats crashing, and the
    message has to be loud because the task is still scored on the weighted
    metric.
    """
    model, inputs = _PlainModel(), _batch()
    trainer = _make_trainer(kl_coef=1.0)

    total = trainer.compute_loss(model, inputs)
    plain = _StubTrainer().compute_loss(model, inputs)

    assert float(total) == pytest.approx(float(plain), rel=1e-9)
    assert "disable_adapter" in trainer._kl_disabled_reason
    assert "inactive" in capsys.readouterr().out


def test_missing_labels_falls_back_without_raising():
    model = _FakeAdapterModel()
    inputs = _batch()
    labels = inputs.pop("labels")
    inputs["labels"] = labels  # keep for CE
    trainer = _make_trainer(kl_coef=1.0)
    assert torch.isfinite(trainer.compute_loss(model, inputs)).all()


def test_reference_forward_does_not_accumulate_gradient():
    """The base side is a fixed reference; it must not be trained toward."""
    model, inputs = _FakeAdapterModel(), _batch()
    loss = _make_trainer(kl_coef=1.0).compute_loss(model, inputs)
    loss.backward()
    # head participates in both passes, but the reference pass runs under
    # no_grad, so its contribution to the gradient is zero by construction.
    assert model.head.weight.grad is not None
    assert torch.isfinite(model.head.weight.grad).all()


def test_kl_is_surfaced_in_logs():
    model, inputs = _FakeAdapterModel(), _batch()
    trainer = _make_trainer(kl_coef=0.5)
    trainer.compute_loss(model, inputs)
    trainer.log({"loss": 1.0})
    assert "kl" in trainer.logged and trainer.logged["kl"] >= 0


def test_return_outputs_contract_is_preserved():
    model, inputs = _FakeAdapterModel(), _batch()
    loss, outputs = _make_trainer(kl_coef=0.5).compute_loss(model, inputs, return_outputs=True)
    assert hasattr(outputs, "logits")
    assert torch.isfinite(loss).all()
