"""Local eval harness that replicates validator's eval_instruct_text logic.

Mirrors /Users/zulist/Documents/text/G.O.D/validator/evaluation/eval_instruct_text.py.

Key validator behaviors:
- Loads eval dataset via axolotl's load_tokenized_prepared_datasets
- Filters samples where all labels == -100 (empty outputs)
- Sorts by input_ids length
- Uses HF Trainer.evaluate() with bf16, per-device batch 1-autoscale
- Returns {"eval_loss": float}
- VALI_CONFIG_PATH uses sequence_len: 4096
- Auto-halves sequence_len if model.config.max_position_embeddings < 2 * sequence_len

Usage:
    python scripts/eval_harness/run_eval.py \
        --checkpoint-path /app/checkpoints/<task_id>/<repo> \
        --original-model meta-llama/Llama-2-7b-hf \
        --dataset datasets/dev_<task_id>.json \
        --dataset-type '{"field_instruction":"instruct","field_output":"output",...}' \
        --file-format json \
        [--max-length 4096] \
        [--output eval_result.json]
"""
import argparse
import json
import os
from math import ceil
from pathlib import Path

os.environ.setdefault("TRANSFORMERS_ALLOW_TORCH_LOAD", "true")

import torch
import yaml
from accelerate.utils import find_executable_batch_size
from axolotl.utils.data import load_tokenized_prepared_datasets
from axolotl.utils.dict import DictDefault
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import Dataset
from transformers import AutoConfig
from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer
from transformers import Trainer
from transformers import TrainingArguments

# Validator defaults (mirror G.O.D validator/test_axolotl.yml)
VALIDATOR_SEQUENCE_LEN = 4096
STARTING_BATCH_SIZE = 1
LOG_INTERVAL_SECONDS = 10


def _process_custom_dataset_fields(custom_type_dict: dict) -> dict:
    """Mirror text-jagger scripts/tokenize_instruct.py:_process_custom_dataset_fields."""
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
    """Mirror text-jagger scripts/tokenize_instruct.py:_process_chat_template_dataset_fields."""
    return {
        "chat_template": dataset_dict["chat_template"],
        "type": "chat_template",
        "field_messages": dataset_dict["chat_column"],
        "message_field_role": dataset_dict["chat_role_field"],
        "message_field_content": dataset_dict["chat_content_field"],
        "roles": {
            "assistant": [dataset_dict["chat_assistant_reference"]],
            "user": [dataset_dict["chat_user_reference"]],
        },
        "message_property_mappings": {
            "role": dataset_dict["chat_role_field"],
            "content": dataset_dict["chat_content_field"],
        },
    }


def build_eval_config(
    dataset_path: str,
    dataset_type: dict,
    file_format: str,
    base_axolotl_yml: str,
    sequence_len: int,
    output_dir: str,
) -> DictDefault:
    """Build axolotl DictDefault config for eval dataset."""
    with open(base_axolotl_yml, "r") as f:
        config_dict = yaml.safe_load(f)

    config_dict["sequence_len"] = sequence_len
    config_dict["output_dir"] = output_dir

    custom_type_dict = {k: v for k, v in dataset_type.items() if v is not None}
    entry = {"path": dataset_path}

    if "chat_template" in dataset_type:
        entry.update(_process_chat_template_dataset_fields(dataset_type))
    else:
        entry.update(_process_custom_dataset_fields(custom_type_dict))

    entry["ds_type"] = file_format
    entry["data_files"] = [dataset_path]
    config_dict["datasets"] = [entry]

    return DictDefault(config_dict)


def load_eval_dataset(config: DictDefault, tokenizer) -> Dataset:
    """Load + filter + sort eval dataset (mirror validator logic)."""
    prepared_path = Path(config.output_dir) / "prepared"
    eval_dataset, _ = load_tokenized_prepared_datasets(tokenizer, config, prepared_path)

    original_length = len(eval_dataset)
    eval_dataset = [s for s in eval_dataset if any(label != -100 for label in s["labels"])]
    filtered_length = len(eval_dataset)

    print(f"Filtered out {original_length - filtered_length} samples with empty outputs", flush=True)

    eval_dataset = sorted(eval_dataset, key=lambda x: len(x["input_ids"]))
    print(f"Loaded evaluation dataset with {filtered_length} samples", flush=True)
    return eval_dataset


def collate_batch(batch, tokenizer):
    input_ids = [torch.tensor(item["input_ids"]) for item in batch]
    attention_mask = [torch.tensor(item["attention_mask"]) for item in batch]
    labels = [torch.tensor(item["labels"]) for item in batch]

    input_ids = pad_sequence(input_ids, batch_first=True, padding_value=tokenizer.pad_token_id)
    attention_mask = pad_sequence(attention_mask, batch_first=True, padding_value=0)
    labels = pad_sequence(labels, batch_first=True, padding_value=-100)

    return {"input_ids": input_ids, "attention_mask": attention_mask, "labels": labels}


def load_model_and_tokenizer(checkpoint_path: str, original_model: str):
    """Load finetuned model. Handles LoRA adapter vs full checkpoint."""
    tokenizer = AutoTokenizer.from_pretrained(original_model, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Detect LoRA adapter
    adapter_config = Path(checkpoint_path) / "adapter_config.json"
    if adapter_config.exists():
        from peft import AutoPeftModelForCausalLM

        print(f"LoRA adapter detected at {checkpoint_path}. Loading via PEFT.", flush=True)
        model = AutoPeftModelForCausalLM.from_pretrained(
            checkpoint_path,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            trust_remote_code=True,
        )
    else:
        print(f"Loading full finetuned model from {checkpoint_path}", flush=True)
        model = AutoModelForCausalLM.from_pretrained(
            checkpoint_path,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            trust_remote_code=True,
        )
    model.eval()
    return model, tokenizer


def evaluate(
    checkpoint_path: str,
    original_model: str,
    dataset_path: str,
    dataset_type: dict,
    file_format: str,
    base_axolotl_yml: str,
    max_length: int,
    output_dir: str,
):
    model, tokenizer = load_model_and_tokenizer(checkpoint_path, original_model)

    # Auto-halve sequence_len if model context too small (mirror validator common.py:430)
    base_config = AutoConfig.from_pretrained(original_model, trust_remote_code=True)
    max_emb = getattr(base_config, "max_position_embeddings", None)
    effective_seq = max_length
    if max_emb and max_emb < 2 * max_length:
        effective_seq = ceil(max_emb / 2)
        print(f"Model max_position_embeddings={max_emb} → halving sequence_len to {effective_seq}", flush=True)

    os.makedirs(output_dir, exist_ok=True)
    config = build_eval_config(
        dataset_path=dataset_path,
        dataset_type=dataset_type,
        file_format=file_format,
        base_axolotl_yml=base_axolotl_yml,
        sequence_len=effective_seq,
        output_dir=output_dir,
    )
    config.tokenizer_config = tokenizer.name_or_path

    eval_dataset = load_eval_dataset(config, tokenizer)

    def data_collator(features):
        return collate_batch(features, tokenizer)

    @find_executable_batch_size(starting_batch_size=STARTING_BATCH_SIZE)
    def eval_with_bs(batch_size):
        args = TrainingArguments(
            output_dir=output_dir,
            per_device_eval_batch_size=batch_size,
            report_to="none",
            bf16=True,
        )
        trainer = Trainer(
            model=model,
            args=args,
            tokenizer=tokenizer,
            eval_dataset=eval_dataset,
            data_collator=data_collator,
        )
        return trainer.evaluate()

    results = eval_with_bs()
    out = {
        "eval_loss": float(results["eval_loss"]),
        "samples": len(eval_dataset),
        "sequence_len_used": effective_seq,
        "checkpoint_path": checkpoint_path,
        "dataset_path": dataset_path,
    }
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint-path", required=True, help="Path to finetuned checkpoint (LoRA adapter dir or full model)")
    parser.add_argument("--original-model", required=True, help="HF repo ID of base model (e.g., meta-llama/Llama-2-7b-hf)")
    parser.add_argument("--dataset", required=True, help="Path to eval dataset JSON file")
    parser.add_argument("--dataset-type", required=True, help="JSON string of dataset_type config")
    parser.add_argument("--file-format", default="json", choices=["json", "csv", "hf", "s3"])
    parser.add_argument("--base-axolotl-yml", default="scripts/test_axolotl.yml", help="Base axolotl YAML template")
    parser.add_argument("--max-length", type=int, default=VALIDATOR_SEQUENCE_LEN, help="Sequence length (validator default 4096)")
    parser.add_argument("--output-dir", default="eval_harness/_tmp", help="Temp dir for axolotl prepared cache")
    parser.add_argument("--output", default="eval_result.json", help="Write result JSON to this path")
    args = parser.parse_args()

    dataset_type = json.loads(args.dataset_type)

    result = evaluate(
        checkpoint_path=args.checkpoint_path,
        original_model=args.original_model,
        dataset_path=args.dataset,
        dataset_type=dataset_type,
        file_format=args.file_format,
        base_axolotl_yml=args.base_axolotl_yml,
        max_length=args.max_length,
        output_dir=args.output_dir,
    )

    print("=== EVAL RESULT ===", flush=True)
    print(json.dumps(result, indent=2), flush=True)

    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Result saved to {args.output}", flush=True)


if __name__ == "__main__":
    main()
