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
import shutil
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


def _run(base, out, noise=None):
    """noise=None runs the shipped default (clean copy); a number opts the perturbation in."""
    env = dict(os.environ)
    env.pop("FALLBACK_NOISE_STD", None)
    if noise is not None:
        env["FALLBACK_NOISE_STD"] = str(noise)
    return subprocess.run([sys.executable, SCRIPT, base, out],
                          capture_output=True, text=True, timeout=300, env=env)


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
        assert _run(base, out, noise=0.01).returncode == 0
        got = _load_embed(out, "model.embed_tokens.weight")
        assert got.shape == original.shape and got.dtype == original.dtype
        assert not torch.equal(got, original), "embeddings identical — no noise was added"
        delta = (got.to(torch.float32) - original.to(torch.float32)).abs().mean().item()
        assert delta < 1.0, f"noise far larger than FALLBACK_NOISE_STD=0.01 suggests: {delta}"


def test_only_the_embedding_shard_is_rewritten():
    """A 32B model must not be rewritten wholesale to change one tensor."""
    with tempfile.TemporaryDirectory() as tmp:
        base, out = os.path.join(tmp, "base"), os.path.join(tmp, "sub")
        _make_base_model(base, sharded=True)
        assert _run(base, out, noise=0.01).returncode == 0
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
        r = _run(base, out, noise=0.01)
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

        assert _run(base, out, noise=0.01).returncode == 0

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


# --- the shipped default: a clean copy ------------------------------------------------

def test_the_default_submission_is_a_clean_copy_of_the_base():
    """Settled from G.O.D source on 2026-09-13 (aeb401a9): model_is_a_finetune compares
    config attributes only (validator/evaluation/model_checks.py:98-123) and the one
    identity rule is the repo-id string (validator/scoring/tasks.py:349-353); nothing
    in validator/ hashes weights. A competitor's byte-identical base scored 2.8929 on
    LFM2 while our noised copy scored 3.2921. The noise was a 0.4-nat, two-rank tax on
    every fallback, paid to satisfy a check that does not exist."""
    with tempfile.TemporaryDirectory() as tmp:
        base, out = os.path.join(tmp, "base"), os.path.join(tmp, "sub")
        original = _make_base_model(base)
        r = _run(base, out)
        assert r.returncode == 0, r.stdout + r.stderr
        assert torch.equal(_load_embed(out, "model.embed_tokens.weight"), original)
        assert "noise disabled" in r.stdout, r.stdout


def test_the_perturbation_stays_available_as_an_opt_in():
    with tempfile.TemporaryDirectory() as tmp:
        base, out = os.path.join(tmp, "base"), os.path.join(tmp, "sub")
        original = _make_base_model(base)
        assert _run(base, out, noise=0.01).returncode == 0
        assert not torch.equal(_load_embed(out, "model.embed_tokens.weight"), original)


def test_non_weight_files_are_private_copies_even_when_the_shard_is_hardlinked():
    """restore_submission_architectures rewrites config.json in place after this runs.
    Through a hardlink that would rewrite the BASE model's config — measured on a
    same-mount box. Small files are always copied; only weight shards may share."""
    with tempfile.TemporaryDirectory() as tmp:
        base, out = os.path.join(tmp, "base"), os.path.join(tmp, "sub")
        _make_base_model(base)
        assert _run(base, out).returncode == 0
        for name in ("config.json", "tokenizer_config.json"):
            assert os.stat(os.path.join(out, name)).st_nlink == 1, f"{name} is still hardlinked to the base"


# --- redundant weight formats ----------------------------------------------------------

def test_duplicate_weight_formats_are_not_copied_when_safetensors_exist():
    """NousResearch/Llama-2-70b-hf carries 128.5 GB of safetensors AND 257 GB of
    pytorch_model-*.bin; llama-3 repos carry original/consolidated.*.pth. The
    validator loads safetensors. Copying the rest is 2-3x the disk and the upload
    time on the most expensive task of the round, for nothing."""
    with tempfile.TemporaryDirectory() as tmp:
        base, out = os.path.join(tmp, "base"), os.path.join(tmp, "sub")
        _make_base_model(base)
        for junk in ("pytorch_model-00001-of-00002.bin", "pytorch_model-00002-of-00002.bin",
                     "pytorch_model.bin.index.json", "tf_model.h5", "flax_model.msgpack",
                     "model.gguf"):
            with open(os.path.join(base, junk), "wb") as fh:
                fh.write(b"redundant")
        os.makedirs(os.path.join(base, "original"))
        with open(os.path.join(base, "original", "consolidated.00.pth"), "wb") as fh:
            fh.write(b"redundant")
        assert _run(base, out).returncode == 0
        got = set(os.listdir(out))
        assert "model.safetensors" in got and "config.json" in got
        for junk in ("pytorch_model-00001-of-00002.bin", "pytorch_model.bin.index.json",
                     "tf_model.h5", "flax_model.msgpack", "model.gguf", "original"):
            assert junk not in got, f"{junk} was copied into the submission"


def test_bin_weights_are_still_copied_when_they_are_the_only_weights():
    with tempfile.TemporaryDirectory() as tmp:
        base, out = os.path.join(tmp, "base"), os.path.join(tmp, "sub")
        _make_base_model(base)
        os.remove(os.path.join(base, "model.safetensors"))
        with open(os.path.join(base, "pytorch_model.bin"), "wb") as fh:
            fh.write(b"the only weights there are")
        r = _run(base, out)
        assert r.returncode == 0, r.stdout
        assert "pytorch_model.bin" in os.listdir(out)


# --- a clone that fails halfway --------------------------------------------------------

def test_a_failed_clone_leaves_no_partial_submission(monkeypatch, tmp_path):
    """text_trainer treats any submission dir with >= 2 entries as a success. A clone
    that dies on ENOSPC after config.json and one shard would be uploaded as a model
    and fail to load at scoring. Better no submission and a loud exit."""
    import errno
    import importlib.util
    spec = importlib.util.spec_from_file_location("add_random_noise_under_test", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    base, out = str(tmp_path / "base"), str(tmp_path / "sub")
    _make_base_model(base)

    real_copytree = shutil.copytree

    def _dies_halfway(src, dst, *a, **k):
        os.makedirs(dst, exist_ok=True)
        shutil.copy2(os.path.join(src, "config.json"), os.path.join(dst, "config.json"))
        raise OSError(errno.ENOSPC, "No space left on device")

    monkeypatch.setattr(mod.shutil, "copytree", _dies_halfway)
    with pytest.raises(SystemExit) as e:
        mod.main(base, out)
    assert e.value.code != 0
    assert not os.path.isdir(out) or not os.listdir(out), "a partial submission survived"
    monkeypatch.setattr(mod.shutil, "copytree", real_copytree)
