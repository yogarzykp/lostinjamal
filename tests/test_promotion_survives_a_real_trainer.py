"""523124d under a REAL transformers Trainer: what the reorder saves, and what it cannot.

tests/test_promotion_precedes_telemetry.py proves the ordering on a bare callback with
a fake TrainerState. That is the right test for the statement order, but it cannot
answer the question that decides how the fix should be described: the copy into
submission_dir happens in on_save, which the Trainer calls only AFTER on_evaluate
returns. So when the process dies inside telemetry — the 59469903 timeline — does the
promoted checkpoint reach the submission directory, or is it promoted in memory only?

This file drives the real thing on CPU: a random-init LlamaForCausalLM (147,776
params), a 32-row tokenised dataset, transformers.Trainer with eval_strategy="steps",
and the real CustomEvalSaveCallback fed by the real WhenToEvalHandler, with
per_example_eval_fn wired the way train_instruct.py:672-680 wires it. Three evals at
steps 2, 4, 6; the last is the best (asserted, not assumed).

Measured on transformers 4.51.3 / torch 2.14.0 CPU, HEAD vs `git show 12b16b5`:

    scenario                  code     best_checkpoint_info  checkpoint-6  loss.txt
    ------------------------  -------  --------------------  ------------  --------
    no kill                   both     step 6                on disk       6
    kill in telemetry, EMIT=1 12b16b5  step 4                ABSENT        4
    kill in telemetry, EMIT=1 HEAD     step 6 (memory only)  ABSENT        4
    kill in telemetry, unset  12b16b5  step 4                ABSENT        4
    kill in telemetry, unset  HEAD     step 6                on disk       6

Two facts follow. The reorder promotes step 6 in memory before the kill, and that is
all it does: checkpoint-6 was never written (Trainer._save_checkpoint runs after
_evaluate, trainer.py:3095-3104), on_save never ran, and nothing after trainer.train()
reads best_checkpoint_info (train_instruct.py:928-934). The artefact is identical with
and without the reorder. What lands step 6 is EMIT_PER_EXAMPLE_LOSSES defaulting off:
with no telemetry to die inside, the run reaches _save_checkpoint and on_save.

Every test here is run against the 12b16b5 code by pointing PROMOTION_TEST_SCRIPTS_DIR
at a directory holding that commit's customized_trainer.py AND per_example_eval.py
(the default lives in the second file):

    mkdir -p /tmp/old && for f in customized_trainer per_example_eval; do
      git show 12b16b5:scripts/$f.py > /tmp/old/$f.py; done
    PROMOTION_TEST_SCRIPTS_DIR=/tmp/old .venv-cpu-pinned/bin/python -m pytest \
      tests/test_promotion_survives_a_real_trainer.py -p no:cacheprovider

Run that way, the three tests that guard 523124d fail (the in-memory promotion, the
artefact under default-off, and the default itself) and the four measurements pass;
the file must be run on its own for it, because a customized_trainer already imported
by an earlier test file would shadow the old copy (a check below makes that loud).
"""

import importlib.machinery
import inspect
import os
import re
import sys
import types

import pytest

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SCRIPTS = os.path.join(_REPO, "scripts")
_OLD_SCRIPTS = os.environ.get("PROMOTION_TEST_SCRIPTS_DIR")

sys.path.insert(0, _SCRIPTS)
if _OLD_SCRIPTS:
    # The old copies shadow the repo's; everything they import (state_manager,
    # telemetry) still resolves to the repo, which is what 12b16b5 had too.
    sys.path.insert(0, _OLD_SCRIPTS)

# customized_trainer imports wandb at module scope and uses it only in init_wandb
# (customized_trainer.py:1747). A stub keeps the real package (installed in the pinned
# env, but slow and chatty to import) out of the process. The stub MUST carry a
# ModuleSpec: transformers probes integrations with importlib.util.find_spec("wandb"),
# which raises ValueError on a spec-less module in sys.modules, and that is fatal to
# `from transformers import LlamaForCausalLM`. test_promotion_precedes_telemetry.py
# installs a bare stub first when the suite runs in file order, so patch that one too.
_wandb = sys.modules.setdefault("wandb", types.ModuleType("wandb"))
if getattr(_wandb, "__spec__", None) is None:
    _wandb.__spec__ = importlib.machinery.ModuleSpec("wandb", None)

import torch  # noqa: E402
from torch.utils.data import Dataset  # noqa: E402
from transformers import (  # noqa: E402
    LlamaConfig,
    LlamaForCausalLM,
    Trainer,
    TrainingArguments,
    default_data_collator,
)

import customized_trainer  # noqa: E402
import per_example_eval  # noqa: E402

if _OLD_SCRIPTS:
    for _mod in (customized_trainer, per_example_eval):
        assert os.path.abspath(_mod.__file__).startswith(os.path.abspath(_OLD_SCRIPTS)), (
            f"PROMOTION_TEST_SCRIPTS_DIR is set but {_mod.__name__} was imported from "
            f"{_mod.__file__} — run this file on its own, or the mutation run tests HEAD"
        )


EVAL_EVERY = 2
MAX_STEPS = 6
STEPS = [2, 4, 6]


@pytest.fixture(autouse=True)
def _isolated_env(monkeypatch):
    """One callback per test, telemetry into the tmp dir, no early stop.

    TRAINING_BEST_CKPT_PERSIST=0: __init__ restores best_checkpoint_info from the
    process state store (customized_trainer.py:252-262); the store falls back to a
    process-local dict without a redis server, so a promotion in one test would seed
    the next test's starting best.
    INSTRUCT_EARLY_STOP_DISABLE=1: run length must be a property of max_steps, not
    of the loss trajectory.
    EMIT_PER_EXAMPLE_LOSSES is unset here; each test states its own setting.
    """
    monkeypatch.setenv("TRAINING_BEST_CKPT_PERSIST", "0")
    monkeypatch.setenv("INSTRUCT_EARLY_STOP_DISABLE", "1")
    monkeypatch.delenv("EMIT_PER_EXAMPLE_LOSSES", raising=False)
    monkeypatch.delenv("TRAINING_TELEMETRY_PATH", raising=False)
    monkeypatch.delenv("TRAINING_TELEMETRY_DISABLE", raising=False)


class _TokenRows(Dataset):
    """Fixed random token ids; the model is trained and evaluated on the same rows so
    the eval loss falls at every eval and the LAST eval is the best."""

    def __init__(self, n=32, seq=16, vocab=512, seed=1):
        g = torch.Generator().manual_seed(seed)
        self.ids = torch.randint(0, vocab, (n, seq), generator=g)

    def __len__(self):
        return len(self.ids)

    def __getitem__(self, i):
        x = self.ids[i]
        return {"input_ids": x, "attention_mask": torch.ones_like(x), "labels": x.clone()}


class _Run:
    """A real Trainer + real callback, with the per-example hook wired like production.

    `die_at`: global step at which per_example_eval_fn raises SystemExit AFTER having
    done its real forward pass — the container cleanup in the 59469903 timeline.
    SystemExit, not SIGKILL, so the callback's memory can be inspected afterwards;
    on_save is reached in neither case. The callback's telemetry block catches only
    Exception (customized_trainer.py:817), so a BaseException is what escapes it.
    """

    def __init__(self, tmp_path, die_at=None):
        torch.manual_seed(0)
        cfg = LlamaConfig(
            vocab_size=512, hidden_size=64, intermediate_size=128, num_hidden_layers=2,
            num_attention_heads=4, num_key_value_heads=4, max_position_embeddings=64,
            tie_word_embeddings=False,
        )
        model = LlamaForCausalLM(cfg)
        rows = _TokenRows()
        self.output_dir = str(tmp_path / "out")
        self.submission_dir = str(tmp_path / "submission")
        args = TrainingArguments(
            output_dir=self.output_dir,
            max_steps=MAX_STEPS,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
            eval_strategy="steps",
            eval_steps=EVAL_EVERY,
            save_strategy="steps",
            save_steps=EVAL_EVERY,
            logging_steps=1,
            learning_rate=5e-3,
            report_to=[],
            disable_tqdm=True,
            use_cpu=True,
            seed=0,
        )
        # The real handler, as train_instruct.py:516 builds it: a far-off deadline and
        # a periodic cadence that agrees with the Trainer's own eval/save steps.
        self.cb = customized_trainer.CustomEvalSaveCallback(
            customized_trainer.WhenToEvalHandler(
                "2099-01-01 00:00:00", save_before_remaining_time=3, periodic_save_steps=EVAL_EVERY
            ),
            self.submission_dir,
            self.output_dir,
            "tiny-llama",
            max_steps=-1,
        )
        self.trainer = Trainer(
            model=model, args=args, train_dataset=rows, eval_dataset=rows,
            data_collator=default_data_collator, callbacks=[self.cb],
        )
        self.telemetry_calls = []
        trainer = self.trainer

        def _per_example_eval():
            self.telemetry_calls.append(trainer.state.global_step)
            vec = per_example_eval.collect_per_example_losses(
                trainer.model, trainer.get_eval_dataloader(), device=trainer.args.device
            )
            if die_at is not None and trainer.state.global_step == die_at:
                raise SystemExit("container cleaned up mid-pass")
            return vec

        self.cb.per_example_eval_fn = _per_example_eval

    # -- what happened -------------------------------------------------------
    def evals(self):
        return [(h["step"], h["eval_loss"]) for h in self.trainer.state.log_history if "eval_loss" in h]

    def checkpoints_on_disk(self):
        return sorted(
            int(d.split("-")[1]) for d in os.listdir(self.output_dir) if d.startswith("checkpoint-")
        )

    def loss_txt(self):
        p = os.path.join(self.submission_dir, "loss.txt")
        return open(p).read() if os.path.isfile(p) else None

    def assert_last_eval_is_best(self):
        evals = self.evals()
        assert [s for s, _ in evals] == STEPS, f"expected evals at {STEPS}, got {evals}"
        losses = [l for _, l in evals]
        assert all(b < a for a, b in zip(losses, losses[1:])), (
            f"harness precondition: eval loss must fall at every eval so the last eval is "
            f"the best; got {evals}"
        )
        return evals


# ---------------------------------------------------------------------------
# 1. The harness is real: a full run lands the last (best) checkpoint.
#    Holds on 12b16b5 and on HEAD — this is the baseline, not a guard.
# ---------------------------------------------------------------------------
def test_last_eval_best_lands_in_submission(tmp_path):
    run = _Run(tmp_path)
    run.trainer.train()

    evals = run.assert_last_eval_is_best()
    last_step, last_loss = evals[-1]
    assert run.checkpoints_on_disk() == STEPS
    assert run.cb.best_checkpoint_info == {"loss": last_loss, "step": last_step}
    assert run.loss_txt() == f"{last_step},{last_loss}", (
        f"loss.txt={run.loss_txt()!r} does not name the last, best step {last_step}"
    )
    assert os.path.isfile(os.path.join(run.submission_dir, "model.safetensors"))


# ---------------------------------------------------------------------------
# 2. The 59469903 shape: the process dies inside telemetry on the final eval.
#    GUARDS 523124d's reorder. On 12b16b5 best_checkpoint_info still names step 4.
# ---------------------------------------------------------------------------
def test_kill_inside_telemetry_still_promotes_in_memory(tmp_path, monkeypatch):
    monkeypatch.setenv("EMIT_PER_EXAMPLE_LOSSES", "1")
    run = _Run(tmp_path, die_at=MAX_STEPS)

    with pytest.raises(SystemExit):
        run.trainer.train()

    evals = run.assert_last_eval_is_best()
    last_step, last_loss = evals[-1]
    assert run.telemetry_calls == STEPS, "the per-example pass ran at every eval, including the fatal one"
    assert run.cb.best_checkpoint_info == {"loss": last_loss, "step": last_step}, (
        f"best_checkpoint_info={run.cb.best_checkpoint_info} after a kill inside telemetry at "
        f"step {last_step}: the promotion still sits downstream of the telemetry (12b16b5 ordering)"
    )


# ---------------------------------------------------------------------------
# 3. The subtlety. Same kill, same EMIT=1: what did the submission directory get?
#    Nothing new — on BOTH orderings. checkpoint-6 was never written, on_save never
#    ran, and loss.txt still names step 4. The reorder changes a number in memory
#    that nothing reads after trainer.train() (train_instruct.py:928-934).
#
#    This is a measurement, not a guard: it passes on 12b16b5 and on HEAD. It can
#    fail only if the Trainer saved BEFORE evaluating (then checkpoint-6 would exist)
#    or if the copy moved into on_evaluate ahead of the telemetry (then loss.txt
#    would name 6) — either of which would change what the fix should be called.
# ---------------------------------------------------------------------------
def test_kill_inside_telemetry_leaves_the_artefact_at_the_previous_best(tmp_path, monkeypatch):
    monkeypatch.setenv("EMIT_PER_EXAMPLE_LOSSES", "1")
    run = _Run(tmp_path, die_at=MAX_STEPS)

    with pytest.raises(SystemExit):
        run.trainer.train()

    evals = run.assert_last_eval_is_best()
    last_step, _ = evals[-1]
    prev_step, prev_loss = evals[-2]
    assert run.checkpoints_on_disk() == STEPS[:-1], (
        f"checkpoints on disk {run.checkpoints_on_disk()}: the Trainer saves after it "
        f"evaluates, so a kill inside on_evaluate means checkpoint-{last_step} does not exist"
    )
    assert run.loss_txt() == f"{prev_step},{prev_loss}", (
        f"loss.txt={run.loss_txt()!r}: the submission must still hold the previous best; "
        f"on_save is not reached when on_evaluate raises"
    )


# ---------------------------------------------------------------------------
# 4. Same kill, EMIT unset. GUARDS 523124d's default-off. On 12b16b5 the default
#    is "1", the pass runs, the kill lands, loss.txt names step 4. On HEAD the pass
#    never runs, so nothing dies, on_save runs, and step 6 is the artefact.
#    THIS is the change that would have recovered step 544.
# ---------------------------------------------------------------------------
def test_default_off_is_what_lands_the_artefact(tmp_path, monkeypatch):
    monkeypatch.delenv("EMIT_PER_EXAMPLE_LOSSES", raising=False)
    run = _Run(tmp_path, die_at=MAX_STEPS)

    died = False
    try:
        run.trainer.train()
    except SystemExit:
        died = True

    evals = run.assert_last_eval_is_best()
    last_step, last_loss = evals[-1]
    assert not died and run.telemetry_calls == [], (
        f"per-example pass ran at {run.telemetry_calls} with EMIT_PER_EXAMPLE_LOSSES unset "
        f"(died={died}) — the default is still on (12b16b5), and the 59469903 kill lands"
    )
    assert run.checkpoints_on_disk() == STEPS
    assert run.loss_txt() == f"{last_step},{last_loss}", (
        f"loss.txt={run.loss_txt()!r} does not name step {last_step}"
    )


# ---------------------------------------------------------------------------
# 5. The Trainer fact the above rests on, cited from the pinned transformers rather
#    than assumed. On 4.51.3: trainer.py:3095-3096 evaluates, :3102-3104 saves and
#    calls on_save; evaluate() reaches on_evaluate at :4184. So on_save is entered
#    only after on_evaluate has RETURNED.
# ---------------------------------------------------------------------------
def test_pinned_trainer_saves_and_calls_on_save_after_evaluate():
    src, first = inspect.getsourcelines(Trainer._maybe_log_save_evaluate)
    text = "".join(src)
    i_eval = text.index("self._evaluate(")
    i_ckpt = text.index("self._save_checkpoint(")
    i_save = text.index("on_save(")
    assert i_eval < i_ckpt < i_save, (
        f"transformers {__import__('transformers').__version__}: _maybe_log_save_evaluate "
        f"(trainer.py:{first}) does not evaluate before it saves and calls on_save"
    )
    # on_evaluate fires inside evaluate(), i.e. inside _evaluate above.
    eval_src, eval_first = inspect.getsourcelines(Trainer.evaluate)
    assert "callback_handler.on_evaluate(" in "".join(eval_src), (
        f"Trainer.evaluate (trainer.py:{eval_first}) no longer dispatches on_evaluate"
    )
    # And nothing on the way out of train() saves: the one `finally` in the wrapper
    # only re-enables progress bars (trainer.py:2242).
    train_src = "".join(inspect.getsourcelines(Trainer.train)[0])
    assert "_save_checkpoint" not in train_src and "on_save" not in train_src


# ---------------------------------------------------------------------------
# 6. The gate's log-line contract with the callback, and the smoke scripts keeping
#    the telemetry path exercised now that the default is off.
#    Of everything ops/smoke/gate.sh greps, only two strings come from this callback
#    (compute_loss, reached from on_evaluate): "[kl] checkpoint metric:" and
#    "checkpoint metric unavailable". Nothing greps "Updating the best checkpoint",
#    "Copy the best checkpoint", "[dev-absorb]" or "[per-example]".
# ---------------------------------------------------------------------------
def _read(rel):
    with open(os.path.join(_REPO, rel), encoding="utf-8") as f:
        return f.read()


def test_gate_greps_still_match_the_callbacks_log_lines():
    gate = _read("ops/smoke/gate.sh")
    # Every fixed string gate.sh hands to grep, with the shell's regex escapes undone
    # ("\[kl\] checkpoint metric:" is grepped as the literal "[kl] checkpoint metric:").
    grepped = {
        re.sub(r"\\(.)", r"\1", pat)
        for pat in re.findall(r'grep\s+-a\w*\s+"([^"]+)"', gate)
    }
    callback_src = _read("scripts/customized_trainer.py")
    for needle in ("[kl] checkpoint metric:", "checkpoint metric unavailable"):
        assert needle in grepped, f"gate.sh no longer greps {needle!r}; it greps {sorted(grepped)}"
        assert needle in callback_src, f"customized_trainer.py no longer prints {needle!r}"
    # The strings the callback prints must be printed literally, not built from parts
    # the gate could not match: pin the f-string prefixes at their print sites.
    assert re.search(r'f"\[kl\] checkpoint metric: \{', callback_src)
    assert re.search(r'f"\[kl\] checkpoint metric unavailable after retry', callback_src)
    # Nothing in the gate depends on the promotion or copy lines, so 523124d's reorder
    # cannot have moved a grepped string. Pin that too, or a future grep for one of
    # them silently becomes the only test of this ordering on the smoke box.
    for absent in ("Updating the best checkpoint", "Copy the best checkpoint", "[dev-absorb]", "[per-example]"):
        assert not any(absent in g for g in grepped), f"gate.sh now greps {absent!r}: update this test"


def test_smoke_scripts_export_emit_so_the_telemetry_path_stays_exercised():
    # Every stage of the instruct replay and the chat smoke export the flag; DPO and
    # GRPO do not wire per_example_eval_fn at all (only train_instruct.py:680 does),
    # so the default flip changes nothing on those paths.
    replay = _read("ops/smoke/run_instruct_replay.sh")
    stages = re.findall(r"^\s{2}(\w+(?:\|\w+)*)\)\s*$", replay, flags=re.M)
    exports = replay.count("export EMIT_PER_EXAMPLE_LOSSES=1")
    assert stages, "could not find the stage case arms in run_instruct_replay.sh"
    assert exports >= len(stages), (
        f"{exports} EMIT exports for {len(stages)} stages {stages} — a stage runs with the "
        f"per-example pass off, i.e. the gate no longer covers it"
    )
    assert "export EMIT_PER_EXAMPLE_LOSSES=1" in _read("ops/smoke/run_chat_smoke.sh")
    wired = [
        rel for rel in ("scripts/train_instruct.py", "scripts/train_dpo.py", "scripts/train_grpo.py")
        if "per_example_eval_fn" in _read(rel)
    ]
    assert wired == ["scripts/train_instruct.py"], wired
    # And the current default really is off.
    os.environ.pop("EMIT_PER_EXAMPLE_LOSSES", None)
    assert per_example_eval.enabled() is False
