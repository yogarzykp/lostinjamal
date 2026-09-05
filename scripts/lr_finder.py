"""
LR Finder — Leslie Smith LRRT (arxiv 1506.01186).

Single-run LR Range Test. ~100 steps. Returns LR at steepest loss decrease.

Used by adaptive_config.py for runtime LR selection — replaces hardcoded
bucket lookup. Works regardless of model_name (survives anonymization).
"""
import math
import os
from typing import Iterable, List, Tuple

import torch


def pick_lr(lrs, smoothed_losses, slope_idx, picker=None):
    """Turn a swept curve into the rate a run will train at.

    Split out of find_lr_lrrt so the choice can be tested without torch, a GPU or a real
    sweep — the picker comparison of 2026-08-22 needed four GPU curves to answer a question
    that is arithmetic once the curve exists.

    `picker` defaults to $LRRT_PICKER, which defaults to the shipped `slope10`.
    Returns (lr, index_used, picker_name).
    """
    if not lrs:
        raise ValueError("pick_lr needs a non-empty lr sweep")
    slope_idx = max(0, min(slope_idx, len(lrs) - 1))
    loss_idx = (smoothed_losses.index(min(smoothed_losses))
                if smoothed_losses else slope_idx)
    loss_idx = max(0, min(loss_idx, len(lrs) - 1))
    table = {
        "slope10": (lrs[slope_idx] / 10.0, slope_idx),
        "slope": (lrs[slope_idx], slope_idx),
        "lossmin": (lrs[loss_idx], loss_idx),
        "lossmin10": (lrs[loss_idx] / 10.0, loss_idx),
    }
    name = picker if picker is not None else os.getenv("LRRT_PICKER", "slope10")
    if name not in table:
        print(f"[lrrt] unknown LRRT_PICKER={name!r}; using slope10", flush=True)
        name = "slope10"
    lr, idx_used = table[name]
    return lr, idx_used, name


def find_lr_lrrt(
    model,
    optimizer,
    dataloader: Iterable,
    lr_min: float = 1e-7,
    lr_max: float = 1e-2,
    num_iter: int = 100,
    smooth_factor: float = 0.05,
    diverge_factor: float = 4.0,
    device: str = "cuda",
) -> Tuple[float, List[float], List[float]]:
    """Leslie Smith LR Range Test.

    Sweeps LR exponentially from lr_min → lr_max over num_iter steps.
    Tracks loss. Returns:
    - suggested_lr: LR where smoothed loss has steepest negative slope
    - lrs: log-space LR points tested
    - losses: smoothed loss at each step

    Args:
        model: model in train mode
        optimizer: pre-built optimizer (will adjust LR)
        dataloader: streaming dataset
        lr_min/lr_max: bounds
        num_iter: total LR steps
        smooth_factor: EMA factor for loss smoothing (0.05 = slow)
        diverge_factor: stop early if loss > diverge_factor × min_loss

    Heuristic for "best LR":
        Suggest LR at point where d(smoothed_loss) / d(log_lr) is most negative.
        This is where loss is decreasing fastest (steep descent).
    """
    model.train()
    lrs: List[float] = []
    raw_losses: List[float] = []
    smoothed_losses: List[float] = []

    log_lr_min = math.log10(lr_min)
    log_lr_max = math.log10(lr_max)
    step_log_lr = (log_lr_max - log_lr_min) / max(1, num_iter - 1)

    avg_loss = 0.0
    min_smooth = float("inf")

    for step, batch in enumerate(dataloader):
        if step >= num_iter:
            break

        # Set LR for this step (exponential sweep)
        log_lr = log_lr_min + step * step_log_lr
        cur_lr = 10 ** log_lr
        for pg in optimizer.param_groups:
            pg["lr"] = cur_lr

        # Forward + backward
        batch = {k: v.to(device) for k, v in batch.items() if isinstance(v, torch.Tensor)}
        out = model(**batch)
        loss = out.loss if hasattr(out, "loss") else out["loss"]
        if not torch.isfinite(loss):
            print(f"[lrrt] step {step} non-finite loss, stopping", flush=True)
            break

        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)  # safety
        optimizer.step()

        loss_val = loss.item()
        # EMA smoothing, Adam-style: the accumulator starts at ZERO and the bias
        # correction below undoes the resulting cold start.
        #
        # It used to seed avg_loss with the first loss and then divide by the same
        # correction anyway, which inflated the opening points by up to 1/smooth_factor
        # — a factor of 20 here. On a CONSTANT loss of 2.5 the "smoothed" curve fell
        # 50 -> 25.6 -> 17.5 -> 13.5 over four steps, a huge negative slope produced by
        # the smoother rather than by learning. Since the sweep starts at lr_min, that
        # artefact sat exactly where the LR is too small to do anything, and the
        # steepest-descent search below picked it every time: observed idx=1/100,
        # suggested_lr=1.12e-07 on a task whose real rate is 8.07e-05.
        avg_loss = (1 - smooth_factor) * avg_loss + smooth_factor * loss_val
        bias_corrected = avg_loss / (1 - (1 - smooth_factor) ** (step + 1))

        lrs.append(cur_lr)
        raw_losses.append(loss_val)
        smoothed_losses.append(bias_corrected)

        # Early stop on divergence
        if bias_corrected < min_smooth:
            min_smooth = bias_corrected
        elif bias_corrected > diverge_factor * min_smooth:
            print(f"[lrrt] step {step} loss diverging ({bias_corrected:.3f} > {diverge_factor}× min), stopping", flush=True)
            break

    if len(smoothed_losses) < 5:
        # Fallback: not enough data for slope analysis
        print(f"[lrrt] insufficient data ({len(smoothed_losses)} steps), returning lr_min×10", flush=True)
        return lr_min * 10, lrs, smoothed_losses

    # Find steepest descent point
    # d(smoothed_loss)/d(log_lr) — most negative slope
    log_lrs = [math.log10(lr) for lr in lrs]
    slopes = []
    for i in range(1, len(smoothed_losses)):
        d_loss = smoothed_losses[i] - smoothed_losses[i - 1]
        d_loglr = log_lrs[i] - log_lrs[i - 1]
        if abs(d_loglr) < 1e-9:
            slopes.append(0)
        else:
            slopes.append(d_loss / d_loglr)

    # Ignore the opening of the sweep when looking for the steepest descent. Even with
    # the bias correction fixed, the first handful of points carry the smoother's
    # remaining warm-up and sit at learning rates too small to move the model — any
    # slope there is noise, and it is noise at the one end of the range that would
    # produce a catastrophically low suggestion. Standard practice for a range test is
    # to discard both ends; this discards the one that has actually bitten us.
    skip = min(max(5, len(slopes) // 10), max(1, len(slopes) - 1))
    searchable = slopes[skip:]
    if not searchable or all(s >= 0 for s in searchable):
        # No descent observed → suggest mid-range LR
        idx = len(lrs) // 2
    else:
        idx = searchable.index(min(searchable)) + skip + 1  # +1: slopes[i] = lr[i]-lr[i-1]

    slope_idx = idx
    # The loss minimum, the other classic pick. Computed ALWAYS, even when unused, because a
    # log that records a decision without the evidence behind it cannot be re-analysed: the
    # summary line survives in logs long after the curve file is gone, and the 2026-08-22
    # picker comparison had to be redone from scratch for exactly that reason.
    loss_idx = smoothed_losses.index(min(smoothed_losses)) if smoothed_losses else idx

    # Default is the shipped behaviour, byte for byte. The alternatives exist so a picker
    # A/B can move one thing at a time; nothing reads this env on a normal run.
    #   slope10 (default)  steepest descent / 10   — what every tournament run has used
    #   slope              steepest descent
    #   lossmin            the loss minimum        — lands ABOVE the incumbent
    #   lossmin10          loss minimum / 10       — lands BELOW it
    # Direction matters more than distance here: our own measurement puts a 10x-HIGH prior at
    # +36% held-out loss and a 10x-LOW prior at +2.7%, so the nearer pick in log-distance is
    # not automatically the cheaper one.
    safe_lr, chosen_idx, _picker = pick_lr(lrs, smoothed_losses, slope_idx)
    suggested_lr = lrs[slope_idx]

    print(f"[lrrt] suggested_lr={suggested_lr:.2e}, safe_lr={safe_lr:.2e} "
          f"(idx={chosen_idx}/{len(lrs)}) picker={_picker}", flush=True)
    print(f"[lrrt] candidates: slope={lrs[slope_idx]:.3e}@{slope_idx} "
          f"slope10={lrs[slope_idx]/10.0:.3e} lossmin={lrs[loss_idx]:.3e}@{loss_idx} "
          f"lossmin10={lrs[loss_idx]/10.0:.3e}", flush=True)
    return safe_lr, lrs, smoothed_losses


def find_lr_for_task(
    model,
    train_dataset,
    tokenizer,
    task_type: str,
    num_iter: int = 100,
    batch_size: int = 4,
    device: str = "cuda",
) -> float:
    """Convenience wrapper: build minimal dataloader + run LRRT.

    For DPO/GRPO, the chosen-only proxy approach is recommended (caller's
    responsibility — convert preference dataset → SFT-style chosen-only).

    Returns: suggested_lr (float)
    """
    from torch.utils.data import DataLoader
    from torch.optim import AdamW

    # Subset for speed
    subset = train_dataset.select(range(min(num_iter * batch_size, len(train_dataset))))
    loader = DataLoader(subset, batch_size=batch_size, shuffle=True)

    # Bare optimizer at lr_min (will be overridden in sweep)
    optimizer = AdamW(model.parameters(), lr=1e-7)

    # Save initial weights to restore (LRRT shouldn't permanently mutate model)
    init_state = {n: p.detach().clone() for n, p in model.named_parameters() if p.requires_grad}

    try:
        suggested_lr, _, _ = find_lr_lrrt(model, optimizer, loader, num_iter=num_iter, device=device)
    finally:
        # Restore weights — LRRT was just for measurement
        with torch.no_grad():
            for n, p in model.named_parameters():
                if n in init_state and p.requires_grad:
                    p.copy_(init_state[n])

    return suggested_lr
