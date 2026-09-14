"""Whether liger was applied must be readable from OUR log, on both loader paths.

`load_model` (full fine-tune) prints `---------------using LIGER------------`.
`load_lora_model` selects AutoLigerKernelForCausalLM the same way and printed nothing.

That is the path most tournament tasks take: adaptive_config forces LoRA above 5e9 for
instruct and for every KL-flagged task. Measured 2026-09-13 on an 8B augmented mirror —
`[adaptive] use_liger=True` in the log, and no trace of liger from us at all. The only
evidence it was applied came from liger's own third-party INFO line
(`liger_kernel.transformers.monkey_patch - INFO - Applying Liger kernels for model type`),
which we neither control nor assert on, and which a version bump can remove.

gate.sh reads logs, not exit codes. A decision this large — fused cross-entropy changes
what `outputs.logits` even contains, which is what made liger and the KL objective mutually
exclusive — has to leave a line we own.
"""

import ast
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = open(os.path.join(ROOT, "scripts", "train_instruct.py"), encoding="utf-8").read()
TREE = ast.parse(SRC)


def _fn(name):
    for node in TREE.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return ast.get_source_segment(SRC, node)
    raise AssertionError(f"{name} not found in train_instruct.py")


def test_both_loaders_select_the_liger_class():
    for name in ("load_model", "load_lora_model"):
        body = _fn(name)
        assert "training_args.use_liger" in body, f"{name} ignores use_liger"
        assert "AutoLigerKernelForCausalLM" in body, f"{name} never selects the liger class"


def test_both_loaders_announce_it():
    for name in ("load_model", "load_lora_model"):
        body = _fn(name)
        i = body.index("training_args.use_liger")
        window = body[i:i + 400]
        assert "LIGER" in window.upper() and ("log_info" in window or "print" in window), (
            f"{name} switches to the liger class without saying so; on the LoRA path that is "
            "every KL task and every instruct task above 5e9"
        )


def test_the_lora_loader_names_the_path_it_is_on():
    """Two loaders printing the identical line would leave a reader unable to tell which
    ran — and they differ in what they do next (PEFT wrap, reference model)."""
    full, lora = _fn("load_model"), _fn("load_lora_model")
    assert "load_lora_model" in lora or "LoRA" in lora, "the LoRA loader's liger line is not distinguishable"
