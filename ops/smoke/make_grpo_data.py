#!/usr/bin/env python3
"""Build a GRPO smoke dataset (prompts only) + its dataset_type, from the R1 GossipCop file.

What the resulting run proves: that our GRPO code path executes end to end on a
real box — dataset_type parse, tokenize_grpo split, prompt-column adaptation,
reward-function exec + validation, TRL group sampling, advantage, backward, the
deadline callback, and a checkpoint landing in the submission dir.

What it does NOT prove: anything about quality. A 135M model generating a few
hundred completions for a few minutes produces a reward number that means
nothing on a leaderboard. There is no GRPO held-out set here the way the
instruct replay has one, and the validator's GRPO score (normalized_reward −
0.5×KL) is not comparable across tasks anyway. Read the exit code and the log,
not the reward.

Why the reward function is what it is
-------------------------------------
train_grpo.validate_reward_function EXECs the source string we ship, grabs the
first callable in the namespace, calls it, and asserts the return is a list of
numbers with one entry per completion. Fail any of that and the run dies before
the first step — so this script re-runs that exact validation locally, on CPU,
in a second, before it writes anything.

The function itself is `reward_specific_word_count`, one of the 13 generic
reward functions the tournament actually ships (scripts/reward_classifier.py:
REWARD_CATALOG), implemented in the sense the catalog records for it: a penalty
proportional to distance from a target word count. Two reasons for that choice
over something invented:

* It has to VARY. GRPO's advantage is (r − mean of group) / std of group. A
  constant reward makes every advantage zero, every gradient zero, and the run
  would pass while proving nothing about the part of the path we care about.
  Completion length from a 135M model at temperature 1.0 varies a lot, so this
  reward varies a lot — the check at the bottom of this file asserts it does.
* Using a catalogued name means the run also exercises the tier-1.5 reward
  classifier in adaptive_config (landscape=single → it becomes authoritative
  for LR and β). An invented name would take the fail-soft "unknown" branch
  instead, which is the branch we exercise least often in production.

It deliberately does not take `extra_data`. train_grpo.supports_extra_data
inspects the signature, and if the parameter is present but no row carries an
`extra_data` column, validate_reward_function skips its assertions entirely —
i.e. it would "pass" without ever calling our function. Keeping the signature
plain forces the real check to run.

Why the prompt column is literally named "prompt"
-------------------------------------------------
tokenize_grpo renames dataset_type["field_prompt"] → "prompt", so any name
works there. But adaptive_config sizes max_completion_length from
dynamics_utils.measure_dataset, whose length probe walks a fixed chain of field
names (text / output / chosen / prompt / instruct / instruction / input). A
prompt column named anything outside that chain measures as nothing, falls back
to a hardcoded [512, 1024, 2048], and max_completion_length lands on 1024
instead of its 512 floor — doubling generation cost per step on a run whose
whole budget is minutes. So: "prompt", and the rename is a no-op on purpose.

Usage (all knobs are env vars; run_grpo_smoke.sh sets them):
    TASK_ID=<new-id> python3 make_grpo_data.py
"""

import argparse
import inspect
import json
import numbers
import os
import random
import sys

# tokenize_grpo.split_dataset takes this many rows off the top for dev, before
# training sees anything. Hardcoded there, not configurable, so the row cap has
# to clear it with room to spare or the train split comes out empty.
TOKENIZE_GRPO_DEV_SIZE = 200

DEFAULT_SRC = "/cache/datasets/865ff4ab-78f2-454d-9d0b-8be506ef42f8_train_data.json"

# Prompt-side field names we accept from the source file, in order.
INSTRUCT_FIELDS = ("instruct", "instruction")
INPUT_FIELDS = ("input", "context")


# Deliberately ASCII-only: this source string is passed to the trainer as a
# command-line argument, and argv decoding depends on the container's locale.
# Keeping it ASCII removes that variable entirely. The check in main() enforces it.
REWARD_SRC_TEMPLATE = '''def reward_specific_word_count(completions, **kwargs):
    """Penalty proportional to distance from a {target}-word completion.

    Generic tournament reward function (see reward_classifier.REWARD_CATALOG:
    direction "-", magnitude "bounded_medium", theme "length"). Deterministic,
    stdlib-only, O(len) per completion. The reward is not the thing under test;
    the path around it is.
    """
    target = {target}
    rewards = []
    for completion in completions:
        if isinstance(completion, str):
            text = completion
        elif isinstance(completion, list) and completion and isinstance(completion[-1], dict):
            text = str(completion[-1].get("content", ""))
        else:
            text = str(completion)
        rewards.append(float(-abs(target - len(text.split()))))
    return rewards
'''


def build_reward_source(target_words: int) -> str:
    return REWARD_SRC_TEMPLATE.format(target=int(target_words))


def selfcheck_reward_source(func_def: str) -> str:
    """Re-run train_grpo.validate_reward_function's checks locally, plus one more.

    Mirrors train_grpo.py:135 exactly — same exec-into-empty-namespace, same
    first-callable pick, same three assertions — so a reward function that would
    kill the run on the GPU dies here instead, on CPU, for free. Returns the
    resolved function name.
    """
    namespace = {}
    exec(func_def, namespace)  # noqa: S102 — this is the behaviour under test
    func = next(v for k, v in namespace.items() if callable(v))

    # train_grpo.supports_extra_data: if this were True with no extra_data column
    # in the data, validate_reward_function would skip every assertion below and
    # pass vacuously. Keep it False so the real check runs.
    if "extra_data" in inspect.signature(func).parameters:
        raise SystemExit(
            "reward function takes extra_data; validate_reward_function would "
            "skip its assertions and 'pass' without ever calling it"
        )

    # Lengths chosen to straddle the target so the rewards must differ.
    test_completions = [
        "short.",
        " ".join(["word"] * 40),
        " ".join(["word"] * 250),
    ]
    rewards = func(test_completions)

    assert isinstance(rewards, list), "rewards must be a list"
    assert len(rewards) == len(test_completions), "one reward per completion"
    assert all(isinstance(r, numbers.Number) for r in rewards), "rewards must be numbers"
    # Not part of the trainer's validation, but the thing that decides whether
    # the test proves anything: constant rewards → zero advantage → zero gradient.
    assert len(set(rewards)) > 1, "rewards are constant; GRPO advantage would be degenerate"

    return getattr(func, "__name__", "reward_func_0")


def load_source_rows(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and isinstance(data.get("data"), list):
        data = data["data"]
    if not isinstance(data, list):
        raise SystemExit(f"{path}: expected a JSON array, got {type(data).__name__}")
    return data


def first_field(row: dict, names) -> str:
    for name in names:
        value = row.get(name)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def build_prompt(row: dict, max_words: int) -> str:
    head = first_field(row, INSTRUCT_FIELDS)
    body = first_field(row, INPUT_FIELDS)
    parts = [p for p in (head, body) if p]
    if not parts:
        return ""
    text = "\n\n".join(parts)
    words = text.split()
    if len(words) > max_words:
        text = " ".join(words[:max_words])
    return text


def env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return int(raw)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Synthesize a GRPO prompt-only dataset for the smoke run.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--task-id", default=os.getenv("TASK_ID"),
                        help="task id the trainer will be told to run (env TASK_ID)")
    parser.add_argument("--src", default=os.getenv("GRPO_SRC", DEFAULT_SRC),
                        help="source instruct dataset to draw prompts from (env GRPO_SRC)")
    parser.add_argument("--cache-dir", default=os.getenv("CACHE_DATASETS_DIR", "/cache/datasets"),
                        help="train_cst.CACHE_DATASETS_DIR (env CACHE_DATASETS_DIR)")
    parser.add_argument("--rows", type=int, default=env_int("GRPO_ROWS", 512),
                        help="rows to write, dev split included (env GRPO_ROWS)")
    parser.add_argument("--prompt-words", type=int, default=env_int("GRPO_PROMPT_WORDS", 120),
                        help="truncate each prompt to this many words (env GRPO_PROMPT_WORDS)")
    parser.add_argument("--target-words", type=int, default=env_int("GRPO_TARGET_WORDS", 60),
                        help="reward function's target completion length (env GRPO_TARGET_WORDS)")
    parser.add_argument("--seed", type=int, default=env_int("GRPO_SEED", 42),
                        help="shuffle seed (env GRPO_SEED)")
    parser.add_argument("--dataset-type-out", default=os.getenv("GRPO_DATASET_TYPE_OUT"),
                        help="where to write the --dataset-type JSON (env GRPO_DATASET_TYPE_OUT)")
    args = parser.parse_args()

    if not args.task_id:
        raise SystemExit("--task-id / TASK_ID is required")

    dest = os.path.join(args.cache_dir, f"{args.task_id}_train_data.json")
    dtype_out = args.dataset_type_out or os.path.join(
        args.cache_dir, f"{args.task_id}_dataset_type.json"
    )

    # The cache path is keyed by task id and the source file IS a cache path for
    # a real replayed task. Same id → we would overwrite 19,505 rows of GossipCop
    # with 512 prompts and silently break the instruct replay.
    if os.path.abspath(dest) == os.path.abspath(args.src):
        raise SystemExit(
            f"refusing to overwrite the source file: TASK_ID={args.task_id} resolves "
            f"to the same cache path as --src ({dest}). Use a NEW task id."
        )

    if args.rows <= TOKENIZE_GRPO_DEV_SIZE + 63:
        raise SystemExit(
            f"--rows {args.rows} is too low: tokenize_grpo.split_dataset removes "
            f"{TOKENIZE_GRPO_DEV_SIZE} rows for dev before training sees any, so this "
            f"would leave {max(0, args.rows - TOKENIZE_GRPO_DEV_SIZE)} train rows. "
            f"Use at least {TOKENIZE_GRPO_DEV_SIZE + 64}."
        )

    reward_src = build_reward_source(args.target_words)
    reward_name = selfcheck_reward_source(reward_src)

    rows = load_source_rows(args.src)
    random.seed(args.seed)
    order = list(range(len(rows)))
    random.shuffle(order)

    seen = set()
    out = []
    skipped_empty = 0
    skipped_dup = 0
    for idx in order:
        if len(out) >= args.rows:
            break
        row = rows[idx]
        if not isinstance(row, dict):
            continue
        prompt = build_prompt(row, args.prompt_words)
        if not prompt:
            skipped_empty += 1
            continue
        if prompt in seen:
            # Identical prompts across groups add generation cost and nothing else.
            skipped_dup += 1
            continue
        seen.add(prompt)
        out.append({"prompt": prompt})

    if not out:
        keys = sorted(rows[0].keys()) if rows and isinstance(rows[0], dict) else []
        raise SystemExit(
            f"no usable prompts built from {args.src}; expected one of "
            f"{INSTRUCT_FIELDS + INPUT_FIELDS}, first row has keys {keys}"
        )
    if len(out) < args.rows:
        print(f"[warn] only {len(out)} usable rows (asked for {args.rows})", flush=True)

    dataset_type = {
        "field_prompt": "prompt",
        "reward_functions": [{"reward_func": reward_src, "reward_weight": 1.0}],
    }

    # The dataset_type is handed to the trainer on the command line, so it must
    # survive argv decoding under any locale. Everything in it is ours, so ASCII
    # is achievable — assert it rather than hope.
    dataset_type_json = json.dumps(dataset_type)
    if not dataset_type_json.isascii():
        raise SystemExit("dataset_type JSON is not ASCII; it is passed via argv, keep it ASCII")

    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    os.makedirs(os.path.dirname(dtype_out) or ".", exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)
    with open(dtype_out, "w", encoding="utf-8") as f:
        f.write(dataset_type_json)

    n_dev = min(TOKENIZE_GRPO_DEV_SIZE, len(out))
    example = out[0]["prompt"]
    if len(example) > 220:
        example = example[:220] + " …"

    print("--- grpo smoke dataset ---")
    print(f"  source        {args.src} ({len(rows)} rows)")
    print(f"  wrote         {dest}")
    print(f"  rows          {len(out)}  (skipped: {skipped_empty} empty, {skipped_dup} duplicate)")
    print(f"  fields        {sorted(out[0].keys())}")
    print(f"  split         {len(out) - n_dev} train / {n_dev} dev "
          f"(tokenize_grpo hardcodes dev={TOKENIZE_GRPO_DEV_SIZE}; dev is never scored — "
          f"the GRPO callback skips eval — it only feeds reward validation)")
    print(f"  prompt words  <= {args.prompt_words}, seed {args.seed}")
    print(f"  example       {example!r}")
    print(f"  dataset_type  {dtype_out}")
    print(f"  reward        {reward_name} (weight 1.0, target {args.target_words} words) "
          f"— validated: list of numbers, one per completion, non-constant")
    return 0


if __name__ == "__main__":
    sys.exit(main())
