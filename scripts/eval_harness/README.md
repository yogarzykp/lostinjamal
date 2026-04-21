# Eval Harness

Local replica of G.O.D validator eval for Instruct task.

Mirrors `/Users/zulist/Documents/text/G.O.D/validator/evaluation/eval_instruct_text.py` — uses axolotl `load_tokenized_prepared_datasets`, filters empty-label samples, sorts by length, runs HF `Trainer.evaluate()` with bf16 + auto batch size.

## Validator config baseline

- `sequence_len: 4096` (from `G.O.D/validator/test_axolotl.yml:5`)
- Auto-halves to `ceil(max_position_embeddings / 2)` if model context too small
- `sample_packing: false`, `eval_sample_packing: false`, `pad_to_sequence_len: true`
- `bf16: True`
- `starting_batch_size: 1` with `find_executable_batch_size`

## Usage

After training produces a checkpoint:

```bash
python scripts/eval_harness/run_eval.py \
  --checkpoint-path /app/checkpoints/<task_id>/<expected_repo_name> \
  --original-model meta-llama/Llama-2-7b-hf \
  --dataset datasets/dev_<task_id>.json \
  --dataset-type '{"field_instruction":"instruct","field_output":"output","field_input":null,"field_system":null,"format":null,"no_input_format":null,"system_format":null}' \
  --file-format json \
  --max-length 4096 \
  --output eval_harness/baseline_<task_id>.json
```

## Environment

Run inside same container that has axolotl installed (standalone-text-trainer image), OR via a venv with:

```
axolotl==0.9.1
transformers (pinned by axolotl)
torch>=2.4
accelerate
peft
pyyaml
```

## Output

JSON file with:
```json
{
  "eval_loss": 1.2345,
  "samples": 200,
  "sequence_len_used": 4096,
  "checkpoint_path": "...",
  "dataset_path": "..."
}
```

## Gotchas

- **LoRA detection**: script auto-detects `adapter_config.json` and loads via `AutoPeftModelForCausalLM`.
- **Base model download**: `--original-model` is fetched from HF (needs network). For `--network=none` container, pre-cache first.
- **Dataset filtering**: samples with all `labels == -100` (empty outputs) dropped. Filter rate at large `sequence_len` should be low if dataset not mostly long-context.
- **This is NOT the validator's real eval dataset** — validator has its own hidden held-out set per task. Use your own dev split (e.g., `datasets/dev_<task_id>.json` produced by `scripts/tokenize_instruct.py:split_dataset`) as proxy for A/B benchmarks.

## Baseline protocol

1. Run training via `run_instruct_local.sh` (produces checkpoint at `/app/checkpoints/<task_id>/<repo>`).
2. Use dev split (produced by tokenizer: `datasets/dev_<task_id>.json`) as eval set.
3. Run `run_eval.py` → get `eval_loss`.
4. Save as `eval_harness/baseline_<task_id>.json`.
5. For each experiment (Phase 3), rerun train with feature flag → rerun eval → compare to baseline.
