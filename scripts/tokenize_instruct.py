from typing import Dict, Any
from axolotl.utils.dict import DictDefault
import yaml
from torch.utils.data import Dataset
from pathlib import Path
from transformers import AutoTokenizer
from typing import Callable
from axolotl.utils.data import load_tokenized_prepared_datasets
import torch
import logging
from datetime import datetime
import sys
import random
import json
import requests
import os
import shutil
import typer


def _process_custom_dataset_fields(custom_type_dict: dict) -> dict:
    if not custom_type_dict.get("field_output"):
        return {
            "type": "completion",
            "field": custom_type_dict.get("field_instruction"),
        }

    processed_dict = custom_type_dict.copy()
    processed_dict.setdefault("no_input_format", "{instruction}")
    if processed_dict.get("field_input"):
        processed_dict.setdefault("format", "{instruction} {input}")
    else:
        processed_dict.setdefault("format", "{instruction}")

    return {"format": "custom", "type": processed_dict}


def _process_chat_template_dataset_fields(dataset_dict: dict) -> dict:
    processed_dict = {}

    processed_dict["chat_template"] = dataset_dict["chat_template"]
    processed_dict["type"] = "chat_template"
    processed_dict["field_messages"] = dataset_dict["chat_column"]
    processed_dict["message_field_role"] = dataset_dict["chat_role_field"]
    processed_dict["message_field_content"] = dataset_dict["chat_content_field"]
    processed_dict["roles"] = {
        "assistant": [dataset_dict["chat_assistant_reference"]],
        "user": [dataset_dict["chat_user_reference"]],
    }

    processed_dict["message_property_mappings"] = {
        "role": dataset_dict["chat_role_field"],
        "content": dataset_dict["chat_content_field"],
    }

    return processed_dict


def create_dataset_entry(
    data_path: str,
    dataset_type: Dict,
    file_format: str,
) -> dict:
    dataset_entry = {"path": data_path}
    custom_type_dict = {
        key: value for key, value in dataset_type.items() if value is not None
    }
    # if data_type is chat_template, use _process_chat_template_dataset_fields
    if "chat_template" in dataset_type:
        print("Processing chat template dataset type")
        dataset_entry.update(_process_chat_template_dataset_fields(dataset_type))
    else:
        print("Processing instruct dataset type")
        dataset_entry.update(_process_custom_dataset_fields(custom_type_dict))

    # if file_format != FileFormat.HF:
    dataset_entry["ds_type"] = file_format
    # Originally: dataset_entry["data_files"] = [os.path.basename(dataset)]
    dataset_entry["data_files"] = [data_path]
    return dataset_entry


def load_and_update_evaluation_config(
    data_path: str,
    dataset_type: Any,
    file_format: str,
    finetuned_model: Any,
    config_path: str,
    max_length: int = -1,
) -> DictDefault:
    with open(config_path, "r") as file:
        config_dict = yaml.safe_load(file)

    if max_length > 0:
        config_dict["sequence_len"] = max_length

    dataset_entry = create_dataset_entry(
        data_path=data_path,
        dataset_type=dataset_type,
        file_format=file_format,
    )
    config_dict["datasets"] = [dataset_entry]

    # max_embeddings = getattr(finetuned_model.config, "max_position_embeddings", None)

    # if max_embeddings and max_embeddings < 2 * config_dict["sequence_len"]:
    #    config_dict["sequence_len"] = ceil(max_embeddings / 2)

    return DictDefault(config_dict)


def _load_evaluation_dataset(
    evaluation_config: DictDefault, tokenizer: AutoTokenizer
) -> Dataset:
    prepared_path = Path(evaluation_config.output_dir) / "prepared"
    eval_dataset, _ = load_tokenized_prepared_datasets(
        tokenizer, evaluation_config, prepared_path
    )

    original_length = len(eval_dataset)
    eval_dataset = [
        sample
        for sample in eval_dataset
        if any(label != -100 for label in sample["labels"])
    ]
    filtered_length = len(eval_dataset)

    print(
        f"Filtered out {original_length - filtered_length} samples with empty outputs"
    )
    print(f"Loaded dataset with {filtered_length} samples")
    return eval_dataset



def remove_empty_output_items(items: list):
    result = []
    for item in items:
        if "output" in item and not item["output"]:
            continue
        if "input" in item and "instruct" in item:
            if not item["instruct"] and not item["input"]:
                continue
        if "output" in item and type(item["output"]) is not str:
            continue

        if (
            "instruct" in item
            and type(item["instruct"]) is not str
            and item["instruct"] is not None
        ):
            continue
        if (
            "input" in item
            and type(item["input"]) is not str
            and item["input"] is not None
        ):
            continue
        result.append(item)
    return result


def replace_wrong_token_in_item(item: dict):
    for key in item:
        if type(item[key]) is str:
            item[key] = item[key].replace("[PAD]", "")
    return item

def split_dataset(
    total_data_path: str,
    train_data_path: str,
    dev_data_path: str,
    seed: int = 42,
    dev_size: int = 200,
    max_data_size: int = -1
):
    """Split the dataset into train and dev"""
    # Load the dataset
    with open(total_data_path, "r") as file:
        data = json.load(file)

    # Pre-split dedup (default on; set INSTRUCT_DEDUP=0 to disable).
    # Exact hash + optional Jaccard n-gram. Stdlib+numpy only, no Docker deps.
    #
    # The validator's model-prep already measured near_duplicate_rate over the
    # whole dataset. When it reports essentially none, the pass has nothing to
    # remove and the time is better spent training. When it does run, we compare
    # our removal rate against that measurement — not to change behaviour, but
    # because a large divergence means one of the two is reading different
    # fields, which otherwise only shows up as unexplained score loss.
    try:
        from baseline_signals import dedup_crosscheck, should_skip_dedup
        from baseline_stats_reader import read_cached
        from data.dedup_knn import dedup_from_env

        _bs = read_cached()
        _skip, _skip_reason = should_skip_dedup(_bs)
        if _skip:
            print(f"[dedup] skipped — {_skip_reason}", flush=True)
        else:
            before = len(data)
            deduped, stats = dedup_from_env(data)
            if stats.get("enabled"):
                print(f"[dedup] {stats}", flush=True)
                data = deduped
                line = dedup_crosscheck(_bs, removed=before - len(data), total=before)
                if line:
                    print(f"[dedup] {line}", flush=True)
    except Exception as exc:
        print(f"[dedup] skipped ({exc}) — continuing without dedup", flush=True)

    random.seed(seed)
    random.shuffle(data)
    if max_data_size > 0:
        data = data[:max_data_size]

    # Proportional, leak-controlled split. Replaces shuffle + fixed 200-row slice:
    # 200 rows is a 40% holdout on a small task and statistically useless on a
    # large one, and a positional slice lets near-duplicate rows straddle the
    # split, which inflates the dev loss that checkpoint selection reads.
    # Falls back to the legacy behaviour if the policy module is unavailable.
    # Gated so a run can be bisected against the legacy behaviour — the split is a
    # behavioural change like the rest, and a baseline measurement is only a
    # baseline if every new mechanism is off. Set INSTRUCT_SPLIT_POLICY=0.
    if os.getenv("INSTRUCT_SPLIT_POLICY", "1") != "1":
        print(f"[split] INSTRUCT_SPLIT_POLICY=0 — legacy shuffle+slice, dev_size={dev_size}", flush=True)
        dev_items = data[:dev_size]
        train_items = data[dev_size:]
    else:
        try:
            from data.split_policy import leak_safe_split, INSTRUCT_KEYS
            train_items, dev_items, split_stats = leak_safe_split(data, INSTRUCT_KEYS, seed=seed)
            print(f"[split] {split_stats}", flush=True)
        except Exception as exc:
            print(f"[split] policy unavailable ({exc}) — legacy slice", flush=True)
            dev_items = data[:dev_size]
            train_items = data[dev_size:]
    # Save the train and dev datasets
    with open(train_data_path, "w") as file:
        before_len = len(train_items)
        train_items = remove_empty_output_items(train_items)
        after_len = len(train_items)
        print(f"Removed {before_len - after_len} empty output items from train_ds")
        json.dump(train_items, file, ensure_ascii=False)

    with open(dev_data_path, "w") as file:
        before_len = len(dev_items)
        dev_items = remove_empty_output_items(dev_items)
        after_len = len(dev_items)
        print(f"Removed {before_len - after_len} empty output items from dev_ds")
        json.dump(dev_items, file, ensure_ascii=False)

    print(
        f"split {total_data_path} ({len(data)} items) into {train_data_path} ({len(train_items)} items) and {dev_data_path} ({len(dev_items)} items)"
    )
    # Returned so the tokeniser can say how many of these rows survived it. Counting
    # them again from disk would mean re-parsing a quarter-gigabyte of JSON for a
    # diagnostic; the numbers are already here.
    return len(train_items), len(dev_items)


def data_stat(items: list):
    lengths = []
    for item in items:
        lengths.append(len(item["input_ids"]))


def tokenize_dataset(
    tokenizer: AutoTokenizer,
    data_path: str,
    dataset_type: Dict,
    config_path: str,
    output_path: str,
    max_length: int = -1,
    input_rows: int = -1,
):
    evaluation_config = load_and_update_evaluation_config(
        data_path, dataset_type, "json", None, config_path, max_length
    )
    evaluation_config.tokenizer_config = tokenizer.name_or_path
    eval_dataset = _load_evaluation_dataset(evaluation_config, tokenizer)
    # now dump this
    result = []
    for i in range(len(eval_dataset)):
        dp = eval_dataset[i]
        result.append(dp)

    print(f"Dumped {len(result)} samples to {output_path}")

    # Ground-truth check on our own length measurement.
    #
    # `measure_dataset` estimates sequence lengths by tokenizing raw fields; this
    # is the tokenized dataset that will actually be trained on, so it is the only
    # place the estimate can be compared against reality. A silent 24x error in
    # that estimate is what sized max_length at 512 on a task whose real p95 was
    # 1513, truncating the tail of nearly half the batches with nothing in the log
    # to show for it.
    #
    # Logs only — never raises, never alters the run. A diagnostic is not worth
    # trading a tournament submission for. Compares against the max_length the
    # plan chose, so it also reveals a cap set below the data it has to hold.
    try:
        # Rows that never reach `result` are the ones this check most needs to see.
        # Axolotl DROPS a sequence longer than max_length instead of truncating it, so
        # an under-sized cap does not show up as a long tail here — it shows up as an
        # absence, and every measurement below is taken over the survivors. On task
        # 3a6658eb this block reported "1.0% reach the cap" while 98.2% of the dataset
        # had already been discarded upstream: an instrument that surveys who is left
        # and concludes nobody was hurt.
        if input_rows > 0:
            dropped = input_rows - len(result)
            pct = dropped / input_rows * 100
            print(
                f"[len-check] tokenised {len(result)}/{input_rows} rows "
                f"({dropped} dropped, {pct:.1f}%) at max_length={max_length}",
                flush=True,
            )
            if pct >= 25.0:
                print(
                    f"[len-check] WARNING: max_length={max_length} discarded {pct:.1f}% "
                    f"of this split. Axolotl drops over-long rows rather than truncating "
                    f"them, so this is training data thrown away, not shortened — check "
                    f"the sequence-length measurement that sized the cap",
                    flush=True,
                )

        realized = sorted(len(dp.get("input_ids", [])) for dp in result)
        if realized:
            r_p95 = realized[min(len(realized) - 1, int(0.95 * len(realized)))]
            over = sum(1 for x in realized if x >= max_length)
            print(
                f"[len-check] tokenized dataset p95={r_p95} max={realized[-1]} "
                f"vs planned max_length={max_length}; "
                f"{over}/{len(realized)} ({over / len(realized) * 100:.1f}%) reach the cap",
                flush=True,
            )
            if over / len(realized) > 0.10:
                print(
                    f"[len-check] WARNING: {over / len(realized) * 100:.1f}% of examples hit "
                    f"max_length={max_length} — the cap is truncating real training "
                    f"signal, check the sequence-length measurement",
                    flush=True,
                )
    except Exception as exc:
        print(f"[len-check] skipped ({type(exc).__name__}: {exc})", flush=True)

    with open(output_path, "w") as file:
        json.dump(result, file, ensure_ascii=False)


def main(training_request_path: str):
    t1 = datetime.now()
    with open(training_request_path, "r") as file:
        training_request = json.load(file)

    # dataset is already downloaded at: training_request["train_request"]["dataset"]
    task_id = training_request["train_request"]["task_id"]
    total_path = training_request["train_request"]["dataset"]
    train_path = f"datasets/train_{task_id}.json"
    dev_path = f"datasets/dev_{task_id}.json"
    max_data_size = training_request["train_request"].get("max_data_size", -1)
    if max_data_size > 0:
        print(
            f"Max data size is {max_data_size}, so we will only extract {max_data_size} samples randomly"
        )

    _n_train, _n_dev = split_dataset(
        total_path,
        train_path,
        dev_path,
        max_data_size=max_data_size,
    )
    
    config_path = "test_axolotl.yml"
    tokenizer = AutoTokenizer.from_pretrained(
        training_request["train_request"]["model_path"]
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    max_length = -1  # default value in test_axolot.yml

    if "max_length" in training_request["train_request"]:
        max_length = training_request["train_request"]["max_length"]

    print(f"max_length={max_length}")

    tokenize_dataset(
        tokenizer,
        train_path,
        training_request["train_request"]["dataset_type"],
        config_path,
        f"datasets/train_tokenized_{task_id}.json",
        max_length=max_length,
        input_rows=_n_train,
    )
    
    tokenize_dataset(
        tokenizer,
        dev_path,
        training_request["train_request"]["dataset_type"],
        config_path,
        f"datasets/dev_tokenized_{task_id}.json",
        max_length=max_length,
        input_rows=_n_dev,
    )

    t2 = datetime.now()
    print(f"Tokenization completed in {(t2 - t1).seconds} seconds")


if __name__ == "__main__":
    typer.run(main)
