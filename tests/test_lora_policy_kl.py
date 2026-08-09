"""The adapter-policy decision on KL-flagged tasks.

`adaptive_config.py` cannot be imported here: it pulls in dynamics_utils, which
uses `int | None` annotations requiring Python 3.10+, while this machine has 3.9.
The training container runs 3.11, so that is a local limitation, not a defect.

Rather than copy the rule into the test — where it would quietly drift from the
code it claims to check — we extract the real `_select_lora_config` from the
source with ast and execute that function alone. The test therefore fails if the
shipped logic changes, which is the whole point.
"""

import ast
import os
import sys

import pytest

SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")


def _load_function(module_filename, func_name):
    """Compile a single top-level function out of a module we cannot import."""
    path = os.path.join(SCRIPTS, module_filename)
    with open(path, "r", encoding="utf-8") as fh:
        tree = ast.parse(fh.read(), filename=path)

    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            module = ast.Module(body=[node], type_ignores=[])
            ast.fix_missing_locations(module)
            namespace = {"Dict": dict}
            exec(compile(module, path, "exec"), namespace)  # noqa: S102
            return namespace[func_name]
    raise AssertionError(f"{func_name} not found in {module_filename}")


select_lora = _load_function("adaptive_config.py", "_select_lora_config")


INSTRUCT_FULL_FT_CEILING = 5e9  # below this, instruct normally trains full-FT
DPO_GRPO_CEILING = 1.5e9


# --------------------------------------------------------------------------
# Default path — unchanged when the task is not KL-flagged
# --------------------------------------------------------------------------

@pytest.mark.parametrize("params", [1e8, 5e8, 1e9, 3e9, int(INSTRUCT_FULL_FT_CEILING)])
def test_instruct_below_ceiling_stays_full_ft_without_kl(params):
    assert select_lora(int(params), "instruct", use_kl=False)["use_lora"] is False


@pytest.mark.parametrize("params", [6e9, 8e9, 14e9, 70e9])
def test_instruct_above_ceiling_uses_lora_regardless(params):
    cfg = select_lora(int(params), "instruct", use_kl=False)
    assert cfg["use_lora"] is True
    assert 64 <= cfg["lora_r"] <= 256
    assert cfg["lora_alpha"] == cfg["lora_r"] * 2


def test_use_kl_defaults_to_false_so_existing_callers_are_unaffected():
    """The parameter was added, not required — old call sites keep old behaviour."""
    assert select_lora(int(3e9), "instruct")["use_lora"] is False


@pytest.mark.parametrize("task", ["dpo", "grpo"])
def test_dpo_and_grpo_thresholds_are_untouched(task):
    assert select_lora(int(DPO_GRPO_CEILING), task, use_kl=False)["use_lora"] is False
    assert select_lora(int(2e9), task, use_kl=False)["use_lora"] is True


def test_none_param_count_still_returns_full_ft():
    assert select_lora(None, "instruct", use_kl=True)["use_lora"] is False


# --------------------------------------------------------------------------
# The KL policy shift
# --------------------------------------------------------------------------

@pytest.mark.parametrize("params", [1e8, 5e8, 1e9, 3e9, int(INSTRUCT_FULL_FT_CEILING)])
def test_kl_flagged_instruct_takes_lora_at_any_size(params):
    """Two reasons, same direction: a low-rank adapter structurally limits drift
    from the base model — which is what the KL term penalises — and
    disable_adapter() then provides reference logits at no memory cost, which is
    what makes the exact objective affordable at all."""
    cfg = select_lora(int(params), "instruct", use_kl=True)
    assert cfg["use_lora"] is True
    assert cfg["lora_alpha"] == cfg["lora_r"] * 2


def test_kl_shift_only_affects_models_below_the_ceiling():
    """Above the ceiling LoRA was already chosen, so the flag changes nothing."""
    for params in (6e9, 14e9):
        with_kl = select_lora(int(params), "instruct", use_kl=True)
        without = select_lora(int(params), "instruct", use_kl=False)
        assert with_kl == without


def test_rank_stays_inside_the_documented_band_when_forced():
    """A 100M model forced onto LoRA must still get a sane rank, not r=0."""
    cfg = select_lora(int(1e8), "instruct", use_kl=True)
    assert 64 <= cfg["lora_r"] <= 256


def test_forcing_lora_never_reduces_memory_pressure_assumptions():
    """Sanity on direction: the forced path is LoRA, which uses LESS memory than
    the full fine-tune it replaces — so it cannot trip the batch-size caps that
    were fitted assuming full-FT in this band."""
    forced = select_lora(int(3e9), "instruct", use_kl=True)
    default = select_lora(int(3e9), "instruct", use_kl=False)
    assert forced["use_lora"] is True and default["use_lora"] is False
