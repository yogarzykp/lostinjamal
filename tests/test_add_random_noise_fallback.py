"""The last-resort submission must work on models this container cannot train.

That is the whole point of the file, and the previous version failed it: it called
`AutoModelForCausalLM.from_pretrained`, so for any architecture the pinned transformers
does not know, training died AND the fallback died. `submission_dir` stayed empty, the
uploader raised "Nothing to upload", and no repo was created — losing even the
base-model score a failed run normally earns.

Measured 2026-08-22 against G.O.D's 2026+ model pool: transformers 4.51.3 does not
recognise `qwen3_5`, `gemma4`, `lfm2` or `lfm2_moe` — 9 of the 12 models a tournament
now draws from.

These tests build a model directory whose `model_type` is deliberately nonsense, so the
architecture is unknown to any transformers version, past or future. If the fallback
ever regains an architecture-aware dependency, that fixture stops working and these
fail.
"""

import json
import os
import subprocess
import sys
import tempfile

import pytest

torch = pytest.importorskip("torch")
safetensors_torch = pytest.importorskip("safetensors.torch")

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "add_random_noise.py")

VOCAB, HIDDEN = 64, 8


def _make_base_model(root, embed_key="model.embed_tokens.weight", sharded=False):
    """A model directory that no transformers release can build a model class for."""
    os.makedirs(root, exist_ok=True)
    config = {
        "architectures": ["TotallyUnknownForCausalLM"],
        "model_type": "not_a_real_architecture_v9",
        "hidden_size": HIDDEN,
        "num_hidden_layers": 2,
        "num_attention_heads": 2,
        "num_key_value_heads": 2,
        "max_position_embeddings": 2048,
        "vocab_size": VOCAB,
    }
    with open(os.path.join(root, "config.json"), "w") as fh:
        json.dump(config, fh)
    with open(os.path.join(root, "tokenizer_config.json"), "w") as fh:
        json.dump({"model_max_length": 2048}, fh)

    embed = torch.arange(VOCAB * HIDDEN, dtype=torch.float32).reshape(VOCAB, HIDDEN)
    embed = embed.to(torch.bfloat16)
    other = torch.ones(HIDDEN, HIDDEN, dtype=torch.bfloat16)

    if sharded:
        safetensors_torch.save_file(
            {embed_key: embed}, os.path.join(root, "model-00001-of-00002.safetensors"),
            metadata={"format": "pt"})
        safetensors_torch.save_file(
            {"model.layers.0.mlp.weight": other},
            os.path.join(root, "model-00002-of-00002.safetensors"), metadata={"format": "pt"})
        with open(os.path.join(root, "model.safetensors.index.json"), "w") as fh:
            json.dump({"metadata": {"total_size": 1},
                       "weight_map": {embed_key: "model-00001-of-00002.safetensors",
                                      "model.layers.0.mlp.weight": "model-00002-of-00002.safetensors"}}, fh)
    else:
        safetensors_torch.save_file(
            {embed_key: embed, "model.layers.0.mlp.weight": other},
            os.path.join(root, "model.safetensors"), metadata={"format": "pt"})
    return embed


def _run(base, out):
    return subprocess.run([sys.executable, SCRIPT, base, out],
                          capture_output=True, text=True, timeout=300)


def _load_embed(folder, embed_key):
    for name in os.listdir(folder):
        if not name.endswith(".safetensors"):
            continue
        t = safetensors_torch.load_file(os.path.join(folder, name))
        if embed_key in t:
            return t[embed_key]
    raise AssertionError(f"{embed_key} not found in {folder}")


def test_produces_a_submission_for_an_architecture_transformers_cannot_build():
    with tempfile.TemporaryDirectory() as tmp:
        base, out = os.path.join(tmp, "base"), os.path.join(tmp, "sub")
        _make_base_model(base)
        r = _run(base, out)
        assert r.returncode == 0, f"fallback failed on an unknown architecture:\n{r.stderr}"
        assert os.listdir(out), "submission dir is empty — the upload would fail"
        assert os.path.isfile(os.path.join(out, "config.json"))


def test_config_is_preserved_byte_for_byte():
    """model_is_a_finetune compares config attributes; a verbatim copy satisfies it."""
    with tempfile.TemporaryDirectory() as tmp:
        base, out = os.path.join(tmp, "base"), os.path.join(tmp, "sub")
        _make_base_model(base)
        assert _run(base, out).returncode == 0
        with open(os.path.join(base, "config.json"), "rb") as a, \
             open(os.path.join(out, "config.json"), "rb") as b:
            assert a.read() == b.read(), "config.json was rewritten; architecture attrs may drift"


def test_embeddings_are_actually_perturbed():
    with tempfile.TemporaryDirectory() as tmp:
        base, out = os.path.join(tmp, "base"), os.path.join(tmp, "sub")
        original = _make_base_model(base)
        assert _run(base, out).returncode == 0
        got = _load_embed(out, "model.embed_tokens.weight")
        assert got.shape == original.shape and got.dtype == original.dtype
        assert not torch.equal(got, original), "embeddings identical — no noise was added"
        delta = (got.to(torch.float32) - original.to(torch.float32)).abs().mean().item()
        assert delta < 1.0, f"noise far larger than NOISE_STD=0.01 suggests: {delta}"


def test_only_the_embedding_shard_is_rewritten():
    """A 32B model must not be rewritten wholesale to change one tensor."""
    with tempfile.TemporaryDirectory() as tmp:
        base, out = os.path.join(tmp, "base"), os.path.join(tmp, "sub")
        _make_base_model(base, sharded=True)
        assert _run(base, out).returncode == 0
        other = safetensors_torch.load_file(
            os.path.join(out, "model-00002-of-00002.safetensors"))
        assert torch.equal(other["model.layers.0.mlp.weight"],
                           torch.ones(HIDDEN, HIDDEN, dtype=torch.bfloat16))
        got = _load_embed(out, "model.embed_tokens.weight")
        assert not torch.equal(got, _make_base_model(os.path.join(tmp, "ref"), sharded=True))


def test_finds_a_nested_embedding_key():
    """Wrapper models nest the decoder — the shape every text_config pool model uses."""
    key = "model.language_model.embed_tokens.weight"
    with tempfile.TemporaryDirectory() as tmp:
        base, out = os.path.join(tmp, "base"), os.path.join(tmp, "sub")
        original = _make_base_model(base, embed_key=key)
        r = _run(base, out)
        assert r.returncode == 0
        assert "could not perturb" not in r.stdout, r.stdout
        assert not torch.equal(_load_embed(out, key), original)


def test_leftovers_from_a_failed_run_do_not_survive():
    with tempfile.TemporaryDirectory() as tmp:
        base, out = os.path.join(tmp, "base"), os.path.join(tmp, "sub")
        _make_base_model(base)
        os.makedirs(out)
        with open(os.path.join(out, "half_written.safetensors"), "w") as fh:
            fh.write("garbage")
        assert _run(base, out).returncode == 0
        assert not os.path.exists(os.path.join(out, "half_written.safetensors")), (
            "a partial checkpoint survived into the submission alongside base weights"
        )


def test_ships_the_copy_even_when_the_embedding_cannot_be_found():
    """A copy the validator accepts beats no submission; perturbation is best-effort."""
    with tempfile.TemporaryDirectory() as tmp:
        base, out = os.path.join(tmp, "base"), os.path.join(tmp, "sub")
        _make_base_model(base, embed_key="some.completely.unrecognised.tensor")
        r = _run(base, out)
        assert r.returncode == 0, r.stderr
        assert os.path.isfile(os.path.join(out, "config.json"))
        assert "could not perturb" in r.stdout or "perturbed" in r.stdout


def test_imports_no_transformers():
    """The defect was an architecture-aware dependency in the one path that must not have one.

    Checked through the AST, not the text. The file's own docstring explains the bug and
    therefore contains the word "transformers"; a substring search would fail on the
    prose while a real re-introduced import elsewhere could still slip past a careless
    pattern. Only actual import statements count — including ones nested inside functions,
    which is where the perturbation helper puts its own imports.
    """
    import ast

    with open(SCRIPT) as fh:
        tree = ast.parse(fh.read())

    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])

    assert "transformers" not in imported, (
        f"add_random_noise imports transformers again (imports: {sorted(imported)}) — it "
        f"will die on exactly the models it exists to rescue"
    )
    # The two it legitimately needs are architecture-agnostic; anything else is a smell.
    assert imported <= {"json", "os", "shutil", "sys", "typer", "torch", "safetensors", "ast"}, (
        f"unexpected dependency in the last-resort path: {sorted(imported)}"
    )


def test_the_base_model_on_disk_is_never_modified():
    """The clone may hardlink, and a hardlink is the same inode — not a snapshot.

    If the shard were perturbed without breaking the link first, this would rewrite the
    BASE model's own file: corrupting the cached base for every later task on the box,
    and silently changing what the validator compares the submission against. That is a
    far worse outcome than the failure this whole file exists to prevent, so it gets its
    own test rather than riding on the others.
    """
    with tempfile.TemporaryDirectory() as tmp:
        base, out = os.path.join(tmp, "base"), os.path.join(tmp, "sub")
        original = _make_base_model(base)
        base_shard = os.path.join(base, "model.safetensors")
        with open(base_shard, "rb") as fh:
            before = fh.read()

        assert _run(base, out).returncode == 0

        with open(base_shard, "rb") as fh:
            after = fh.read()
        assert before == after, (
            "the base model's own weights file was rewritten — the clone hardlinked and "
            "the perturbation landed on the shared inode"
        )
        # And the base tensor itself still reads back unchanged.
        assert torch.equal(
            safetensors_torch.load_file(base_shard)["model.embed_tokens.weight"], original
        )
        # ...while the submission genuinely differs.
        assert not torch.equal(_load_embed(out, "model.embed_tokens.weight"), original)


def test_the_submission_shard_is_not_left_hardlinked_to_the_base():
    """Even on the no-op path, the file we may edit must be private to the submission."""
    with tempfile.TemporaryDirectory() as tmp:
        base, out = os.path.join(tmp, "base"), os.path.join(tmp, "sub")
        _make_base_model(base)
        assert _run(base, out).returncode == 0
        sub_shard = os.path.join(out, "model.safetensors")
        assert os.stat(sub_shard).st_ino != os.stat(os.path.join(base, "model.safetensors")).st_ino, (
            "submission shard shares an inode with the base model"
        )
