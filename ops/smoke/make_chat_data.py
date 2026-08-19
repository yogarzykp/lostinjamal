#!/usr/bin/env python3
"""Turn a cached instruct file into the conversations shape a ChatTask expects.

ChatTask is the one text task type we had never exercised. It shares the instruct
trainer — `text_trainer.py:711` routes InstructTextTask and ChatTask down the same
path — so what is untested is not the training loop but the tokenisation branch:
`tokenize_instruct._process_chat_template_dataset_fields` fires only when the
dataset_type carries a `chat_template` key, and it maps a completely different set
of fields than the instruct branch.

The shape is dictated by ChatTemplateDatasetType (G.O.D core/models/dataset_models.py:49):

    chat_column           "conversations"   the column holding the turn list
    chat_role_field       "from"            key naming the speaker inside a turn
    chat_content_field    "value"           key holding that turn's text
    chat_user_reference   "user"
    chat_assistant_reference "assistant"

so each row becomes {"conversations": [{"from": "user", ...}, {"from": "assistant", ...}]}.

A grammar Q&A pair is a single-turn conversation, which is the honest conversion: it
exercises the template, the role mapping and the assistant-span loss mask without
inventing multi-turn structure that the source data does not contain. What this does
NOT cover is multi-turn masking — worth a separate fixture if a tournament ever
serves one.
"""
import argparse
import json
import os
import random
import sys

CACHE_DATASETS_DIR = "/cache/datasets"


def load_rows(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise SystemExit(f"expected a JSON array in {path}, got {type(data).__name__}")
    return data


def build_prompt(row: dict, max_input_chars: int) -> str:
    """Same join the instruct path uses: instruction, then the input when present."""
    instruct = str(row.get("instruct") or "").strip()
    inp = str(row.get("input") or "").strip()
    if max_input_chars > 0 and len(inp) > max_input_chars:
        inp = inp[:max_input_chars]
    return f"{instruct}\n\n{inp}".strip() if inp else instruct


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task-id", required=True, help="task id of the smoke run")
    ap.add_argument("--source-task-id", required=True, help="task id whose cached instruct data to convert")
    ap.add_argument("--cache-dir", default=CACHE_DATASETS_DIR)
    ap.add_argument("--source", default=None, help="override the source path entirely")
    ap.add_argument("--rows", type=int, default=3000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--max-input-chars", type=int, default=2000)
    args = ap.parse_args()

    src = args.source or os.path.join(args.cache_dir, f"{args.source_task_id}_train_data.json")
    out = os.path.join(args.cache_dir, f"{args.task_id}_train_data.json")
    if os.path.abspath(src) == os.path.abspath(out):
        raise SystemExit("refusing to overwrite the source file")

    rows = load_rows(src)
    random.Random(args.seed).shuffle(rows)

    convs = []
    skipped = 0
    for row in rows:
        prompt = build_prompt(row, args.max_input_chars)
        answer = str(row.get("output") or "").strip()
        # A turn with no text trains nothing and the validator filters such rows out
        # of its own eval set, so dropping them here keeps the two sides comparable.
        if not prompt or not answer:
            skipped += 1
            continue
        convs.append({"conversations": [
            {"from": "user", "value": prompt},
            {"from": "assistant", "value": answer},
        ]})
        if len(convs) >= args.rows:
            break

    if not convs:
        raise SystemExit("no usable rows: every source row had an empty prompt or output")

    os.makedirs(args.cache_dir, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(convs, f, ensure_ascii=False)

    print(f"source        : {src} ({len(rows)} rows)")
    print(f"conversations : {len(convs)} written -> {out}")
    print(f"skipped       : {skipped} (empty prompt or answer)")
    print(f"example       : {json.dumps(convs[0], ensure_ascii=False)[:220]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
