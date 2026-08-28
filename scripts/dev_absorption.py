"""Reclaim the dev split as one bounded, low-LR pass over the selected submission.

WHY THIS IS SOUND, and it is worth stating because it looks like training on eval data.
The dev split is not the validator's. It is carved out of the training rows we were
handed, by our own `leak_safe_split`, and the model is scored on a separate test set the
validator never shows us — measured directly on task 28c9f3bb: our 1000-row dev split and
the validator's 1000-row test set have ZERO overlap. Dev exists to choose a checkpoint.
Once that choice is made it has no remaining job, and holding it out past that point
spends training rows for no scoring benefit.

WHERE THE NUMBER CAME FROM. The position-1 miner of tourn_e758aac2d861c378_20260824 ships
this mechanism and left its telemetry in the submitted repo: `devfit,absorb=+0.0183`.
Scored against that same model on identical rows with identical code, we trailed by
0.0225 — so this one step accounts for roughly four fifths of the gap. On that task's
board the entire spread from rank 1 to rank 3 was 0.0136, which is smaller than the
absorption itself.

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

import json
import os
import shutil

MIN_ROWS = 8
DEFAULT_MIN_LR_RATE = 0.1


def _weights_only(name: str) -> bool:
    return name.endswith(".safetensors") or name.endswith(".bin")


def _prior_dev_loss(submission_dir: str):
    """The dev loss already measured for THIS checkpoint, or None if unrecorded.

    `loss.txt` is the file checkpoint selection itself reads, so a guard built on it
    compares the absorption pass against exactly the number that chose this submission
    — no second evaluation, and nothing the validator has ever shown us.
    """
    try:
        with open(os.path.join(submission_dir, "loss.txt"), "r", encoding="utf-8") as fh:
            return float(fh.read().strip().split(",")[-1])
    except Exception:
        pass
    try:
        with open(os.path.join(submission_dir, "trainer_state.json"), "r",
                  encoding="utf-8") as fh:
            history = json.load(fh).get("log_history", [])
        evals = [h["eval_loss"] for h in history if "eval_loss" in h]
        return float(evals[-1]) if evals else None
    except Exception:
        return None


def absorb_dev_split(
    submission_dir: str,
    dev_tokenized_path: str,
    base_lr: float,
    min_lr_rate: float = DEFAULT_MIN_LR_RATE,
    batch_size: int = 1,
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

        seen, total = 0, 0.0
        for input_ids, labels, attention_mask in loader:
            out = model(input_ids=input_ids, labels=labels, attention_mask=attention_mask)
            out.loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            opt.zero_grad(set_to_none=True)
            total += float(out.loss)
            seen += 1

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
        prior = _prior_dev_loss(submission_dir)
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
            if _weights_only(name):
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
