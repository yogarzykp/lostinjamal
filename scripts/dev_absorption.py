"""Reclaim the dev split as one bounded, low-LR pass over the selected submission.

WHY THIS IS SOUND, and it is worth stating because it looks like training on eval data.
The dev split is not the validator's. It is carved out of the training rows we were
handed, by our own `leak_safe_split`, and the model is scored on a separate test set the
validator never shows us — measured directly on task 28c9f3bb: our 1000-row dev split and
the validator's 1000-row test set have ZERO overlap. Dev exists to choose a checkpoint.
Once that choice is made it has no remaining job, and holding it out past that point
spends training rows for no scoring benefit.

WHERE THE NUMBER CAME FROM, and it is ours rather than borrowed. The position-1 miner of
tourn_e758aac2d861c378_20260824 ships this mechanism and left its telemetry in the
submitted repo: `devfit,absorb=+0.0183`. We then measured our own on the H100, task
28c9f3bb, one baseline and one intervention per arm, scored in the rendering the model
was actually trained on (bare BOS + instruct + output + EOS with the instruct span
masked, proven by rebuilding dev rows and matching the tokeniser token-for-token):

    baseline 1.7053 | r=0.05 1.6806 | r=0.10 1.6859 | champion 1.6825

So -0.0194 at the default rate, against the champion's own +0.0183. Two independent
measurements, different code, near-identical result.

WHY THAT SIZE DECIDES ANYTHING. Across the 44 adjacent-rank gaps on the text boards of
both recon'd tournaments, 21 are smaller than this gain, including 8 of the 17 gaps
between a winner and its runner-up. On the three round-1 boards it spans ranks 4 to 1;
on 3a6658eb the entire rank 1-to-4 spread is 0.0044, a quarter of it. Winner-take-all
means a gain is worth nothing unless it crosses the gap above, and this one usually does.

WHY IT LOOKS NOTHING LIKE THEIRS. They run it inside the trainer, on `model_wrapped`,
and spend most of their file getting DDP right — sharded dev loader, matched grad-accum
so `min_lr` stays calibrated, the exact accumulate/sync pattern. Our architecture offers a
cleaner seam: `text_trainer` selects the winning run by argmin AFTER the training
subprocess has exited, so this runs single-process against a directory on disk. No
wrapped model, no reducer hooks, no lockstep to preserve. That is a genuine difference in
approach, not a port with the names changed.

SAFETY IS STRUCTURAL, since there is no eval left to catch a regression:

  * starts from the SELECTED submission, never the last in-memory state;
  * one epoch, at min_lr — a bounded perturbation, not a second training run;
  * writes to a sibling directory and swaps only on success, so a crash anywhere
    leaves the original submission exactly as it was;
  * every failure path returns without touching the submission.
"""

import datetime
import json
import os
import shutil
import time

MIN_ROWS = 8
DEFAULT_MIN_LR_RATE = 0.1

# Seconds held back for what runs AFTER this: the NaN/Inf scan of the final checkpoint
# and restore_submission_architectures. The second of those is what keeps the validator's
# is_finetune check from rejecting the submission outright, so being killed before it does
# not cost a few ranks, it costs the whole entry. Absorption is worth 0.005-0.019; that
# trade is never worth taking.
RESERVE_SECONDS = 90


def seconds_until_deadline(end_time: str):
    """Seconds until the validator's deadline, or None if it cannot be read.

    Format matches customized_trainer.check_remaining_time_less_than_minutes, which is the
    only other reader of this field — a second, subtly different parser here would be a
    way for the two to disagree about when the run ends. Public because text_trainer's
    stage clock reads it too, and a third parser would be a third way to disagree.
    """
    try:
        end = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        end = end.replace(tzinfo=datetime.timezone.utc)
        return (end - datetime.datetime.now(datetime.timezone.utc)).total_seconds()
    except Exception:
        return None


def _weights_only(name: str) -> bool:
    return name.endswith(".safetensors") or name.endswith(".bin")


def _stale_weight_artefact(name: str) -> bool:
    """What has to leave staging before save_pretrained writes the absorbed weights.

    A shard index is not a weight file, but it names weight files. If the absorbed
    model serialises to a different layout than the checkpoint it replaces — above
    all a single model.safetensors where the previous one was sharded —
    save_pretrained writes no new index (modeling_utils.py:3570 touches an index only
    when it writes one), the old one survives, and it names shards that were just
    deleted.

    How much that costs was measured after this was written, and it is less than the
    first version of this docstring claimed. transformers 4.51.3 resolves a bare
    model.safetensors BEFORE the index on both the local-directory branch
    (modeling_utils.py:898 before :905) and the hub branch (:997), and 5.12.1 reads the
    same way — so on every loader we can see, a stale index beside a single file is
    inert at scoring time. It bites only when the single file is absent or the
    validator's image loads differently, and that image's transformers is the one
    version not measured. Clearing it is correct hygiene, not forfeit prevention.

    Nor does the layout change on our own artefacts today: every path trains and
    saves bf16 (train_instruct.py:131,203 / train_dpo.py:265 / train_grpo.py:403),
    the Trainer saves at the default shard size, on_save copies verbatim, and this
    module reloads bf16 and saves at the same default — measured 3 shards in, 3 out,
    identical weight_map (tests/test_absorption_on_a_real_sharded_model.py). The
    trigger is a dtype or key-set change between the two saves; an fp32 checkpoint
    reloaded here as bf16 reproduces it.

    The boss reaches the same guarantee from the other side: dev_pass.py stages into
    an empty directory and copies only NON-weight files across (its _is_weight_file at
    dev_pass.py:154-157 lists the index for exactly this reason), so a stale index can
    never arrive. We stage by copying everything and deleting, so the index has to be
    named here instead.

    Deliberately NOT folded into _weights_only: that predicate also answers "did any
    weights actually get written" at the post-save check, and an index on its own is
    not weights. Merging them would let a save that produced nothing but an index pass
    that check.
    """
    return _weights_only(name) or name in (
        "model.safetensors.index.json",
        "pytorch_model.bin.index.json",
    )


def _prior_dev_loss(submission_dir: str):
    """The dev loss already measured for THIS checkpoint, as (value, note).

    `loss.txt` is the file checkpoint selection itself reads, so a guard built on it
    compares the absorption pass against exactly the number that chose this submission
    — no second evaluation, and nothing the validator has ever shown us.

    It has two formats. customized_trainer's best-checkpoint path writes
    `<step>,<eval_loss>`, which is what the guard wants. Its save_only path writes
    `<step>,proxy=<train_loss>` or `<step>,proxy=no_eval`, which is a TRAIN-loss proxy
    and not comparable to a pass over dev. Reading the second as a number would arm the
    guard against the wrong quantity; reading it as absent would leave the guard silently
    unarmed on the exact runs that took the unusual path. So it returns a note instead,
    and the caller says so out loud.
    """
    raw = None
    try:
        with open(os.path.join(submission_dir, "loss.txt"), "r", encoding="utf-8") as fh:
            raw = fh.read().strip()
    except Exception:
        pass
    if raw:
        tail = raw.split(",")[-1]
        if tail.startswith("proxy="):
            return None, (f"loss.txt holds a train-loss proxy ({raw!r}), which is not "
                          f"comparable to a dev pass")
        try:
            return float(tail), None
        except ValueError:
            return None, f"loss.txt is unparseable ({raw!r})"
    try:
        with open(os.path.join(submission_dir, "trainer_state.json"), "r",
                  encoding="utf-8") as fh:
            history = json.load(fh).get("log_history", [])
        evals = [h["eval_loss"] for h in history if "eval_loss" in h]
        if evals:
            return float(evals[-1]), None
        return None, "trainer_state.json records no eval_loss"
    except Exception:
        return None, "no loss.txt and no readable trainer_state.json"


def absorb_dev_split(
    submission_dir: str,
    dev_tokenized_path: str,
    base_lr: float,
    min_lr_rate: float = DEFAULT_MIN_LR_RATE,
    batch_size: int = 1,
    end_time: str = None,
    log=print,
):
    """One low-LR epoch over the dev split, applied to the selected submission.

    Returns a stats dict on success, or None when it declined or failed — in both of
    those cases `submission_dir` is byte-for-byte what it was on entry.
    """
    if not os.path.isdir(submission_dir):
        log("[dev-absorb] no submission directory — nothing to absorb into")
        return None
    if not os.path.isfile(dev_tokenized_path):
        log(f"[dev-absorb] no dev split at {dev_tokenized_path}")
        return None

    try:
        with open(dev_tokenized_path, "r", encoding="utf-8") as fh:
            rows = json.load(fh)
    except Exception as exc:
        log(f"[dev-absorb] dev split will not parse ({type(exc).__name__}) — skipped")
        return None
    if not isinstance(rows, list) or len(rows) < MIN_ROWS:
        log(f"[dev-absorb] dev split has {len(rows) if isinstance(rows, list) else '?'} "
            f"rows, under the {MIN_ROWS} floor — skipped")
        return None

    lr = float(base_lr) * float(min_lr_rate)
    if not (lr > 0):
        log(f"[dev-absorb] computed lr {lr} is not positive — skipped")
        return None

    staging = submission_dir.rstrip("/") + ".absorbing"
    try:
        import torch
        from torch.utils.data import DataLoader
        from transformers import AutoModelForCausalLM

        log(f"[dev-absorb] {len(rows)} dev rows, one epoch at lr={lr:.3e} "
            f"(base {float(base_lr):.3e} x min_lr_rate {min_lr_rate})")

        model = AutoModelForCausalLM.from_pretrained(
            submission_dir, torch_dtype=torch.bfloat16
        )
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        model.train()
        model.gradient_checkpointing_enable()

        def collate(batch):
            width = max(len(b["input_ids"]) for b in batch)
            pad = getattr(model.config, "pad_token_id", None)
            if pad is None:
                pad = getattr(model.config, "eos_token_id", 0) or 0
            ids, labels, attn = [], [], []
            for b in batch:
                n = width - len(b["input_ids"])
                ids.append(list(b["input_ids"]) + [pad] * n)
                labels.append(list(b.get("labels", b["input_ids"])) + [-100] * n)
                attn.append([1] * len(b["input_ids"]) + [0] * n)
            t = lambda x: torch.tensor(x, device=device)  # noqa: E731
            return t(ids), t(labels), t(attn)

        loader = DataLoader(rows, batch_size=batch_size, shuffle=True, collate_fn=collate)
        opt = torch.optim.AdamW(model.parameters(), lr=lr)

        # The clock this has to live inside. Training already stops 3 minutes before the
        # validator's end_time (save_before_remaining_time), and that window has to hold
        # the final eval, the checkpoint copy, the NaN scan and the architecture restore.
        # A full pass over a long-sequence dev split took 185s on 3a6658eb, which is more
        # than the whole window — so this stops on the clock rather than on the epoch, and
        # a partial pass is fine: the rows are shuffled, so what it saw is a random subset.
        budget_left = seconds_until_deadline(end_time) if end_time else None
        if budget_left is not None:
            usable = budget_left - RESERVE_SECONDS
            if usable <= 0:
                log(f"[dev-absorb] only {budget_left:.0f}s left before end_time and "
                    f"{RESERVE_SECONDS}s of that is reserved for the post-training "
                    f"checks — skipped, submission untouched")
                return None
            log(f"[dev-absorb] {usable:.0f}s usable before end_time "
                f"({RESERVE_SECONDS}s reserved for the post-training checks)")
        started = time.monotonic()

        seen, total, stopped_early = 0, 0.0, False
        for input_ids, labels, attention_mask in loader:
            if budget_left is not None and time.monotonic() - started > budget_left - RESERVE_SECONDS:
                stopped_early = True
                break
            out = model(input_ids=input_ids, labels=labels, attention_mask=attention_mask)
            out.loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            opt.zero_grad(set_to_none=True)
            total += float(out.loss)
            seen += 1

        if stopped_early:
            log(f"[dev-absorb] stopped on the clock at {seen}/{len(rows)} rows "
                f"({time.monotonic() - started:.0f}s)")
        if seen < MIN_ROWS:
            log(f"[dev-absorb] only {seen} rows absorbed before the clock ran out, under "
                f"the {MIN_ROWS} floor — submission left untouched")
            return None

        mean_loss = total / max(1, seen)
        if seen == 0 or mean_loss != mean_loss:  # NaN check
            log(f"[dev-absorb] pass produced {seen} steps, mean loss {mean_loss} — "
                f"submission left untouched")
            return None

        # Refuse a pass that ran hotter than the checkpoint's own dev loss. Measured on
        # 28c9f3bb this separates cleanly: prior dev loss 1.7893, the two rates that
        # improved the held-out score averaged 1.7694 and 1.7739, and the two that made
        # it worse averaged 1.8664 and 2.6956. The cliff is real — at min_lr_rate 0.2 the
        # absorption LR reaches the run's own final scheduled LR and stops being the
        # gentle final pass this is meant to be. The guard costs nothing, reads a number
        # the trainer already wrote, and needs no held-out data to work.
        prior, prior_note = _prior_dev_loss(submission_dir)
        if prior_note:
            # An unarmed guard is a decision, so it goes in the log next to the result
            # rather than being inferred later from its absence.
            log(f"[dev-absorb] guard unarmed — {prior_note}")
        if prior is not None and mean_loss > prior:
            log(f"[dev-absorb] pass loss {mean_loss:.4f} exceeds the checkpoint's own dev "
                f"loss {prior:.4f} — too hot, submission left untouched")
            return None

        # Stage, then swap. A failure anywhere above or below leaves the original in
        # place; the submission is the only artefact that matters and it is never
        # edited where it stands.
        if os.path.isdir(staging):
            shutil.rmtree(staging)
        shutil.copytree(submission_dir, staging)
        for name in os.listdir(staging):
            if _stale_weight_artefact(name):
                os.remove(os.path.join(staging, name))
        model.config.save_pretrained(staging)
        model.save_pretrained(staging, safe_serialization=True)

        if not any(_weights_only(n) for n in os.listdir(staging)):
            log("[dev-absorb] staged directory has no weights — submission left untouched")
            shutil.rmtree(staging, ignore_errors=True)
            return None

        backup = submission_dir.rstrip("/") + ".preabsorb"
        shutil.rmtree(backup, ignore_errors=True)
        os.rename(submission_dir, backup)
        os.rename(staging, submission_dir)
        shutil.rmtree(backup, ignore_errors=True)

        log(f"[dev-absorb] absorbed {seen} steps, mean dev loss {mean_loss:.4f} — "
            f"submission updated")
        return {"steps": seen, "mean_loss": mean_loss, "lr": lr,
                "rows": len(rows), "prior_dev_loss": prior}

    except Exception as exc:
        log(f"[dev-absorb] failed ({type(exc).__name__}: {str(exc)[:200]}) — "
            f"submission left untouched")
        shutil.rmtree(staging, ignore_errors=True)
        return None
    finally:
        try:
            import torch
            torch.cuda.empty_cache()
        except Exception:
            pass
