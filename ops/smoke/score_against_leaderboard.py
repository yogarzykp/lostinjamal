#!/usr/bin/env python3
"""Score a trained checkpoint on the real held-out set and place it on the leaderboard.

The auditing API exposes the held-out test set for completed tasks, so a replay
can end with a number that sits directly next to the miners who actually
competed — rather than a dev-set loss that only means something to us.

The loss here is computed the way the validator computes it: cross-entropy over
completion tokens, token-averaged within each example, then averaged over
examples. That is the same primitive as scripts/per_example_eval.py, and it also
gives the per-example vector for free — which is what tells us whether win-rate
selection would have picked a different checkpoint than the mean did.

Usage:
    python score_against_leaderboard.py --model <path> --test-data <json>
"""

import argparse
import json
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "scripts"))

# Real leaderboard for ONE task — 865ff4ab-78f2-454d-9d0b-8be506ef42f8 — from the
# auditing API. Rank 1 scored 3.0; every other row scored 0.0.
#
# It is only meaningful for THAT task, on THAT task's held-out set. Scoring a replay of a
# different task and printing these ranks compares two unrelated distributions and reads
# as "we are far behind" when it means nothing at all. So the table is printed only when
# --task-id says this is the task it belongs to.
LEADERBOARD_TASK_ID = "865ff4ab-78f2-454d-9d0b-8be506ef42f8"
LEADERBOARD = [
    (1, 1.3862991333007812),
    (2, 1.4351),
    (3, 1.5186),
    (4, 1.5483),
    (5, 1.5585),
    (6, 1.6612),
    (7, 1.6896),
    (8, 3.6580),
]


def build_prompt(row):
    """Mirror the trainer's instruct formatting: instruction + optional input."""
    instruction = str(row.get("instruct", "")).strip()
    extra = str(row.get("input", "")).strip()
    return f"{instruction}\n\n{extra}\n\n" if extra else f"{instruction}\n\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="checkpoint dir or HF id")
    ap.add_argument("--test-data", required=True, help="held-out json from the auditing API")
    ap.add_argument("--max-length", type=int, default=2048)
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--out", default=None, help="write the per-example vector here")
    ap.add_argument("--task-id", default=None,
                    help="task this checkpoint was trained for; the leaderboard table is "
                         "printed only when it matches the task that leaderboard belongs to")
    args = ap.parse_args()

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    from per_example_eval import per_example_losses_from_logits, summarise, vector_fingerprint

    rows = json.load(open(args.test_data))
    print(f"held-out examples: {len(rows):,}")

    tok = AutoTokenizer.from_pretrained(args.model)
    if tok.pad_token_id is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(args.model, torch_dtype=torch.bfloat16, device_map="auto")
    model.eval()

    losses = []
    for start in range(0, len(rows), args.batch_size):
        batch = rows[start : start + args.batch_size]
        input_ids, labels = [], []
        for row in batch:
            prompt = build_prompt(row)
            answer = str(row.get("output", ""))
            p_ids = tok(prompt, add_special_tokens=True)["input_ids"]
            a_ids = tok(answer, add_special_tokens=False)["input_ids"] + [tok.eos_token_id]
            ids = (p_ids + a_ids)[: args.max_length]
            # Prompt tokens are not trained on and are not scored — the validator
            # measures completion tokens only.
            lab = ([-100] * len(p_ids) + a_ids)[: args.max_length]
            input_ids.append(ids)
            labels.append(lab)

        width = max(len(x) for x in input_ids)
        pad = tok.pad_token_id
        ids_t = torch.tensor([x + [pad] * (width - len(x)) for x in input_ids])
        lab_t = torch.tensor([x + [-100] * (width - len(x)) for x in labels])
        att_t = torch.tensor([[1] * len(x) + [0] * (width - len(x)) for x in input_ids])

        with torch.no_grad():
            out = model(input_ids=ids_t.to(model.device), attention_mask=att_t.to(model.device))
        losses.extend(per_example_losses_from_logits(out.logits, lab_t.to(model.device)))

        if (start // args.batch_size) % 20 == 0:
            print(f"  {start + len(batch):>5}/{len(rows)}", flush=True)

    finite = [x for x in losses if not math.isnan(x)]
    mean_loss = sum(finite) / len(finite)

    print()
    print(f"per-example summary: {summarise(losses)}")
    print(f"fingerprint        : {vector_fingerprint(losses)}")
    print()
    print(f"OUR TEST LOSS      : {mean_loss:.4f}")
    print()

    if args.task_id == LEADERBOARD_TASK_ID:
        print("  rank   test_loss   ")
        for rank, loss in LEADERBOARD:
            marker = "  <- winner (scored 3.0)" if rank == 1 else ""
            print(f"  {rank:>4}   {loss:.4f}{marker}")
        print()
        if mean_loss < LEADERBOARD[0][1]:
            print("Would have taken rank 1 on this task.")
        elif mean_loss < LEADERBOARD[1][1]:
            print("Rank 2 — under winner-take-all that still scores 0.0.")
        else:
            print("Outside the top 2.")
    else:
        print("(no leaderboard printed: these ranks belong to task "
              f"{LEADERBOARD_TASK_ID[:8]}; against another task's held-out set they "
              f"compare unrelated distributions and mean nothing)")

    if args.out:
        with open(args.out, "w") as fh:
            json.dump({"mean_loss": mean_loss, "losses": losses}, fh)
        print(f"per-example vector written to {args.out}")


if __name__ == "__main__":
    main()
