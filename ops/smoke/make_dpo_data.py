#!/usr/bin/env python3
"""Build a DPO preference set out of the GossipCop instruct task, for a smoke run.

WHAT THIS IS FOR
    R1 handed us an instruct task (865ff4ab, GossipCop) and no DPO task at all, so
    there is nothing to replay and nothing to place on a leaderboard. The DPO path
    still has to be exercised: tokenize_dpo's split and column rename, dpo_config's
    run_cmd, train_dpo's max_length override and the LR-probe state machine have all
    been edited since the last time a DPO task actually trained on this code. That
    path needs one input it does not currently have anywhere on the box — a
    prompt/chosen/rejected file at the cache path text_trainer keys off. This makes it.

WHY THE PAIRING IS WHAT IT IS
    chosen   = the answer written for this row.
    rejected = the answer written for a different row.

    That is a real preference, not noise. The matching answer genuinely is the better
    continuation of its own prompt, so the gradient points somewhere and a run that
    trains looks different from a run that has been quietly no-op'd. Shuffling the
    answers instead — or pairing a row against itself — would give a dataset where
    every configuration scores the same, which proves nothing about anything.

WHAT IT IS NOT
    Not a quality measurement, and no number out of it means anything on its own.
    The model is 135M, the row count is capped to fit a quarter-hour, and the
    discrimination being learned (is this answer about this article, or some other
    article?) is far easier than the tournament's. Losses from this run are the
    pass/fail of a code path.

THE IDENTICAL-TEXT GUARD
    If chosen and rejected carry the same string, DPO's two log-prob terms cancel and
    the pair contributes exactly zero gradient — it is a dead row that still costs a
    forward pass. On a veracity dataset, where many answers can be near-duplicates of
    each other, a naive shuffle produces a lot of those; tokenize_dpo._adapt_dpo_columns_to_trl
    samples ten rows and prints CRITICAL when it sees any. So the partner search walks
    the shuffled order until it finds a row whose answer text actually differs, and
    reports how many rows it had to drop.

FIELD NAMES
    Deliberately not TRL's own prompt/chosen/rejected. The rename in
    _adapt_dpo_columns_to_trl is part of what we are testing, and with matching names
    it is a no-op that would never fail. `question` is one of split_policy.DPO_KEYS,
    so the leak-safe split still buckets rows by their prompt side; a name outside
    that tuple silently degrades leak_key to the per-row identity fallback and we
    would learn nothing about the guard.

    Whatever these are, --dataset-type on the trainer command line has to agree with
    them. run_dpo_smoke.sh holds the matching JSON.

Usage:
    python3 make_dpo_data.py --task-id <new-task-id> [--rows N] [--seed N]
"""

import argparse
import json
import os
import sys

# Column names written into the file. See FIELD NAMES above before changing these —
# run_dpo_smoke.sh's --dataset-type must be edited in the same commit.
PROMPT_FIELD = "question"
CHOSEN_FIELD = "chosen_response"
REJECTED_FIELD = "rejected_response"

# train_cst.CACHE_DATASETS_DIR, and training_paths.get_text_dataset_path's filename
# pattern. text_trainer ignores --dataset and reads this, so the name is the contract.
CACHE_DATASETS_DIR = "/cache/datasets"
DATASET_FILENAME = "{task_id}_train_data.json"

# The instruct replay's task: 19,505 rows of GossipCop with instruct/input/output.
DEFAULT_SOURCE_TASK_ID = "865ff4ab-78f2-454d-9d0b-8be506ef42f8"

# Below this the run breaks for a reason that has nothing to do with DPO:
# train_dpo.py:304 recomputes total_steps_per_epoch with a plain // and no floor, and
# hands the result to WhenToEvalHandler, which takes global_step % steps_per_epoch.
# Fewer rows than one effective batch means that divisor is 0.
MIN_USEFUL_ROWS = 512


def build_prompt(row, max_input_chars):
    """instruction + optional input, formatted exactly as the instruct harness does.

    Same string as ops/smoke/score_against_leaderboard.py:build_prompt, on purpose:
    the two smoke runs then differ in the objective under test and nothing else.

    The input side is truncated because train_dpo.py forces
    max_prompt_length = max_position_embeddings // 2 (1024 tokens on SmolLM-135M) and
    TRL drops the overflow. A prompt the trainer silently cuts is not the prompt we
    paired, so cut it here where it is visible instead.
    """
    instruction = str(row.get("instruct", "") or "").strip()
    extra = str(row.get("input", "") or "").strip()
    if extra and 0 < max_input_chars < len(extra):
        extra = extra[:max_input_chars].rstrip()
    return f"{instruction}\n\n{extra}\n\n" if extra else f"{instruction}\n\n"


def load_usable_rows(source_path, max_input_chars):
    """Read the source file and keep the rows that can carry a preference pair."""
    with open(source_path, "r", encoding="utf-8") as fh:
        raw = json.load(fh)
    if not isinstance(raw, list):
        sys.exit(f"{source_path}: expected a JSON array, got {type(raw).__name__}")

    usable, skipped = [], 0
    for row in raw:
        if not isinstance(row, dict):
            skipped += 1
            continue
        answer = str(row.get("output", "") or "").strip()
        prompt = build_prompt(row, max_input_chars)
        # tokenize_dpo.remove_empty_items would drop these anyway; dropping them here
        # keeps the row count printed below equal to the row count that trains.
        if not answer or not prompt.strip():
            skipped += 1
            continue
        usable.append({"prompt": prompt, "answer": answer})
    return raw, usable, skipped


def pair_rows(rows, seed):
    """Pair every row with a different row's answer. Returns (pairs, dropped).

    The seeded shuffle fixes both which rows survive the cap and who partners whom,
    so two runs of this script produce byte-identical files and a difference between
    two smoke runs is never the data.
    """
    import random

    order = list(range(len(rows)))
    random.Random(seed).shuffle(order)

    pairs, dropped = [], 0
    for position, i in enumerate(order):
        chosen = rows[i]["answer"]
        partner = None
        # Walk forward through the shuffled order rather than resampling: it
        # terminates, it is deterministic, and a dataset whose answers are all one
        # string exits the loop instead of spinning.
        for step in range(1, len(order)):
            candidate = order[(position + step) % len(order)]
            if rows[candidate]["answer"] != chosen:
                partner = candidate
                break
        if partner is None:
            dropped += 1
            continue
        pairs.append(
            {
                PROMPT_FIELD: rows[i]["prompt"],
                CHOSEN_FIELD: chosen,
                REJECTED_FIELD: rows[partner]["answer"],
            }
        )
    return pairs, dropped


def truncate(text, limit=160):
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[:limit] + "…"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--task-id", required=True, help="task id of the smoke run (NOT the source task)")
    ap.add_argument("--source-task-id", default=DEFAULT_SOURCE_TASK_ID, help="task id whose cached instruct data to convert")
    ap.add_argument("--cache-dir", default=CACHE_DATASETS_DIR, help="train_cst.CACHE_DATASETS_DIR")
    ap.add_argument("--source", default=None, help="override the source path entirely")
    ap.add_argument("--out", default=None, help="override the output path entirely")
    ap.add_argument("--rows", type=int, default=3000, help="cap on preference pairs written")
    ap.add_argument("--seed", type=int, default=42, help="seed for the shuffle and the pairing")
    ap.add_argument("--max-input-chars", type=int, default=2000, help="truncate the input side of the prompt here (0 = never)")
    args = ap.parse_args()

    source_path = args.source or os.path.join(
        args.cache_dir, DATASET_FILENAME.format(task_id=args.source_task_id)
    )
    out_path = args.out or os.path.join(
        args.cache_dir, DATASET_FILENAME.format(task_id=args.task_id)
    )

    if not os.path.isfile(source_path):
        sys.exit(f"source not found: {source_path}")
    # Both files live in the same cache directory and are named by task id alone, so a
    # copy-pasted task id would overwrite the real replay data with synthesised pairs.
    if os.path.abspath(source_path) == os.path.abspath(out_path):
        sys.exit(f"refusing to overwrite the source dataset: {source_path} (--task-id must be a NEW id)")

    raw, usable, skipped = load_usable_rows(source_path, args.max_input_chars)

    import random

    selection = list(range(len(usable)))
    random.Random(args.seed).shuffle(selection)
    if args.rows > 0:
        selection = selection[: args.rows]
    subset = [usable[i] for i in selection]

    pairs, dropped = pair_rows(subset, args.seed)

    if not pairs:
        sys.exit("no usable preference pairs — every answer in the sample is identical")

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    tmp_path = out_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as fh:
        json.dump(pairs, fh, ensure_ascii=False)
    os.replace(tmp_path, out_path)

    distinct_answers = len({p[CHOSEN_FIELD] for p in pairs})
    identical = sum(1 for p in pairs if p[CHOSEN_FIELD] == p[REJECTED_FIELD])
    mean_prompt = sum(len(p[PROMPT_FIELD]) for p in pairs) / len(pairs)
    mean_answer = sum(len(p[CHOSEN_FIELD]) for p in pairs) / len(pairs)
    example = pairs[0]

    print(f"source            {source_path}")
    print(f"                  {len(raw):,} rows read, {skipped:,} unusable, {len(usable):,} usable")
    print(f"wrote             {out_path}")
    print(f"                  {len(pairs):,} preference pairs (cap {args.rows:,}, seed {args.seed})")
    print(f"fields            {PROMPT_FIELD} / {CHOSEN_FIELD} / {REJECTED_FIELD}")
    print(f"distinct answers  {distinct_answers:,} of {len(pairs):,}")
    print(f"identical pairs   {identical}  (must be 0 — a matched pair trains on nothing)")
    print(f"dropped, no partner {dropped}")
    print(f"mean chars        prompt {mean_prompt:,.0f} · answer {mean_answer:,.0f}")
    print()
    print("example row:")
    print(f"  {PROMPT_FIELD}   {truncate(example[PROMPT_FIELD])}")
    print(f"  {CHOSEN_FIELD}   {truncate(example[CHOSEN_FIELD])}")
    print(f"  {REJECTED_FIELD} {truncate(example[REJECTED_FIELD])}")

    if identical:
        print()
        print("WARNING: identical chosen/rejected got through — the pairing guard is broken.")
    if len(pairs) < MIN_USEFUL_ROWS:
        print()
        print(
            f"WARNING: {len(pairs)} rows is below {MIN_USEFUL_ROWS}. train_dpo.py computes "
            f"steps_per_epoch as len(train)//effective_batch with no floor and hands it to "
            f"WhenToEvalHandler, which takes a modulo by it — fewer rows than one batch is a "
            f"ZeroDivisionError, not a short run."
        )


if __name__ == "__main__":
    main()
