"""A LoRA target that names a decoder layer kills the run before step one.

PEFT matches `target_modules` by name suffix. A Linear sitting directly inside an
nn.Sequential has a bare numeric leaf — `...gla.gk_proj.0` — and the bare `"0"` is a
suffix of `model.layers.0`, an entire decoder layer. get_peft_model then tries to wrap a
layer and dies. Our three trainers each carried the same `names[-1]` version.

These tests are written against `qualified_target` directly rather than through a model,
because the whole bug is a string-suffix question and a real nn.Module would add nothing
except a torch dependency this suite does not need.
"""

from __future__ import annotations

import ast
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
MODULE = os.path.join(SCRIPTS, "lora_targets.py")
TRAINERS = ("train_instruct.py", "train_dpo.py", "train_grpo.py")


def _source(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


@pytest.fixture(scope="module")
def mod():
    ns = {}
    exec(compile(_source(MODULE), MODULE, "exec"), ns)  # noqa: S102
    return ns


# --- the bug itself ----------------------------------------------------------------


def test_a_numeric_leaf_is_never_returned_bare(mod):
    """The one output that must never appear: PEFT would match whole decoder layers."""
    got = mod["qualified_target"]("model.layers.5.self_attn.gla.gk_proj.0")
    assert got != "0"
    assert got == "gk_proj.0"


def test_the_sibling_in_the_same_sequential_qualifies_too(mod):
    assert mod["qualified_target"]("model.layers.5.self_attn.gla.gk_proj.1") == "gk_proj.1"


def test_nested_numeric_components_walk_back_to_a_real_name(mod):
    """A Linear two ModuleLists deep still has to anchor on something non-numeric."""
    assert mod["qualified_target"]("block.seq.3.0") == "seq.3.0"


@pytest.mark.parametrize("name,want", [
    ("model.layers.0.self_attn.q_proj", "q_proj"),
    ("model.layers.31.mlp.down_proj", "down_proj"),
    ("lm_head", "lm_head"),
    ("model.embed_tokens", "embed_tokens"),
])
def test_ordinary_names_are_unchanged(mod, name, want):
    """The fix must not perturb the normal case, which is every model we have run."""
    assert mod["qualified_target"](name) == want


def test_a_single_component_name_survives(mod):
    assert mod["qualified_target"]("classifier") == "classifier"


def test_an_all_numeric_path_does_not_collapse_to_a_digit(mod):
    """Should not occur on a real module, but returning "0" is the one forbidden output."""
    got = mod["qualified_target"]("0.1")
    assert got != "0" and got != "1"


# --- and the collection built from it ------------------------------------------------


class _FakeLinear:
    pass


class _FakeModel:
    def __init__(self, names):
        self._names = names

    def named_modules(self):
        return [(n, _FakeLinear()) for n in self._names]


def test_lm_head_is_dropped(mod):
    got = mod["find_all_linear_names"](
        _FakeModel(["model.layers.0.mlp.up_proj", "lm_head"]), (_FakeLinear,))
    assert "lm_head" not in got and "up_proj" in got


def test_a_sequential_gate_does_not_poison_the_target_list(mod):
    """The end-to-end shape of the bug: one Sequential Linear used to add "0"."""
    got = mod["find_all_linear_names"](_FakeModel([
        "model.layers.0.self_attn.q_proj",
        "model.layers.0.self_attn.gla.gk_proj.0",
        "model.layers.0.self_attn.gla.gk_proj.1",
    ]), (_FakeLinear,))
    assert "0" not in got and "1" not in got
    assert set(got) == {"q_proj", "gk_proj.0", "gk_proj.1"}


def test_duplicate_leaves_collapse(mod):
    """Every layer contributes q_proj; the list is a set of names, not of modules."""
    got = mod["find_all_linear_names"](_FakeModel(
        ["model.layers.%d.self_attn.q_proj" % i for i in range(8)]), (_FakeLinear,))
    assert got == ["q_proj"]


# --- and it has to reach all three trainers -----------------------------------------


@pytest.mark.parametrize("trainer", TRAINERS)
def test_every_trainer_uses_the_shared_implementation(trainer):
    """It was three byte-identical copies. A fix in one is a fix in one."""
    src = _source(os.path.join(SCRIPTS, trainer))
    assert "from lora_targets import" in src, (
        "%s still has its own copy, so the decoder-layer crash survives there" % trainer
    )


@pytest.mark.parametrize("trainer", TRAINERS)
def test_no_trainer_still_takes_the_bare_leaf(trainer):
    """The exact expression that caused it, in the file it caused it in."""
    src = _source(os.path.join(SCRIPTS, trainer))
    assert "names[0] if len(names) == 1 else names[-1]" not in src


def test_the_shared_module_is_importable_without_torch():
    """The trainers pass their own linear types, so this file needs no torch at import.

    If it grew a module-level torch import, every test here would still pass on a GPU box
    and fail on a laptop — and the failure would look like a missing dependency rather
    than a design change.
    """
    tree = ast.parse(_source(MODULE))
    top = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    names = [a.name for n in top if isinstance(n, ast.Import) for a in n.names]
    names += [n.module for n in top if isinstance(n, ast.ImportFrom)]
    assert "torch" not in names, names


# --- against real nn.Modules, not stand-ins ------------------------------------------
#
# Everything above uses fake objects, and the gate never reaches the branch this file
# exists for: it only fires on a model whose Linears sit inside an nn.Sequential, and no
# model the gate runs has one. So the fixed branch had never met a real PyTorch module.

try:
    import torch
    import torch.nn as nn
    HAVE_TORCH = True
except Exception:  # pragma: no cover - depends on the machine
    HAVE_TORCH = False

needs_torch = pytest.mark.skipif(not HAVE_TORCH, reason="builds real nn.Modules")


@needs_torch
def test_a_real_sequential_gate_never_yields_a_bare_digit(mod):
    """The quasar GLA shape the challenger's comment describes, built for real.

    A Linear inside nn.Sequential is named `...gk_proj.0`. Taking the leaf gives "0",
    which PEFT suffix-matches against `model.layers.0` — a whole decoder layer — and
    get_peft_model dies on it.
    """
    class Attn(nn.Module):
        def __init__(self):
            super().__init__()
            self.q_proj = nn.Linear(8, 8)
            self.gk_proj = nn.Sequential(nn.Linear(8, 4), nn.Linear(4, 8))

    class Model(nn.Module):
        def __init__(self):
            super().__init__()
            self.layers = nn.ModuleList([Attn() for _ in range(3)])
            self.lm_head = nn.Linear(8, 32)

    got = mod["find_all_linear_names"](Model(), (nn.Linear,))
    assert "0" not in got and "1" not in got, got
    assert set(got) == {"q_proj", "gk_proj.0", "gk_proj.1"}, got


@needs_torch
def test_an_ordinary_model_is_unaffected(mod):
    """The case every real run takes: plain Linears, plain leaf names."""
    class Block(nn.Module):
        def __init__(self):
            super().__init__()
            self.q_proj, self.k_proj = nn.Linear(8, 8), nn.Linear(8, 8)

    class Model(nn.Module):
        def __init__(self):
            super().__init__()
            self.layers = nn.ModuleList([Block() for _ in range(4)])
            self.lm_head = nn.Linear(8, 32)

    got = mod["find_all_linear_names"](Model(), (nn.Linear,))
    assert set(got) == {"q_proj", "k_proj"}, got


@needs_torch
def test_every_returned_name_matches_a_module_that_exists(mod):
    """The property PEFT actually needs: each target is a suffix of a real module path,
    and of a module that is a Linear rather than a container."""
    class Attn(nn.Module):
        def __init__(self):
            super().__init__()
            self.o_proj = nn.Linear(8, 8)
            self.gate = nn.Sequential(nn.Linear(8, 8))

    class Model(nn.Module):
        def __init__(self):
            super().__init__()
            self.layers = nn.ModuleList([Attn() for _ in range(2)])

    m = Model()
    names = {n: type(x) for n, x in m.named_modules()}
    for target in mod["find_all_linear_names"](m, (nn.Linear,)):
        hits = [n for n in names if n.endswith(target)]
        assert hits, "target %r matches no module" % target
        assert all(names[h] is nn.Linear for h in hits), \
            "target %r also matches non-Linear modules: %s" % (target, hits)
