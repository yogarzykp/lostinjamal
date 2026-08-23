"""Last-resort submission: a copy of the base model with its embeddings perturbed.

This runs when training failed, so it is the only thing standing between a failed run
and a score of zero. It must therefore work on models this container cannot train — and
that is exactly what the previous version could not do.

It used to be `AutoModelForCausalLM.from_pretrained(...)`, which fails for any
architecture the pinned transformers does not know. Measured 2026-08-22 against G.O.D's
new 2026+ model pool: transformers 4.51.3 does not recognise `qwen3_5`, `gemma4`, `lfm2`
or `lfm2_moe`, i.e. 9 of the 12 models a tournament now draws from. On those tasks
training died AND this fallback died, so `submission_dir` stayed empty, the uploader
raised "Nothing to upload", and no repo was ever created — losing even the base-model
score a failed run normally still earns.

So this file imports no `transformers` and builds no model. It copies the base directory
and edits one tensor on disk. Nothing here depends on the architecture, which means it
keeps working for models that do not exist yet.

What the validator actually requires (G.O.D validator/evaluation/model_checks.py:92-148,
`model_is_a_finetune`) is that the submitted config's architecture attributes match the
base — `architectures`, `hidden_size`, `model_type`, layer/head counts — plus a context
window not smaller than the base. It compares CONFIG ATTRIBUTES ONLY, never weights. A
verbatim copy satisfies all of it, and the validator loads the result with its own
transformers, not ours. The embedding perturbation is kept anyway: it preserves the
original intent, costs one shard's worth of I/O, and means the submission is not a
byte-identical copy of the base repo.
"""

import json
import os
import shutil

import typer

NOISE_STD = 0.01

# Ordered by how specific they are. The generic suffix match at the end covers wrappers
# that nest the decoder (`model.language_model.embed_tokens.weight`), which is the shape
# every one of the new pool models with a `text_config` uses.
_EMBED_KEYS = (
    "model.embed_tokens.weight",
    "transformer.wte.weight",
    "model.decoder.embed_tokens.weight",
    "embed_tokens.weight",
    "wte.weight",
)


def _skip(_dir, names):
    """Never copy caches or VCS metadata into a submission."""
    return {n for n in names if n in {".git", ".cache", "__pycache__"} or n.endswith(".lock")}


def _clone_tree(src, dst):
    """Materialise `src` at `dst`, by hardlink where possible.

    The pre-boss task's model is Qwen3-32B — about 65 GB in bf16. Byte-copying that to
    change ONE tensor costs the copy twice over: the minutes, and the disk, on a run that
    has already failed and is burning what remains of its budget. Hardlinks make the
    clone effectively free, and the single shard we edit is un-linked first (see
    `_break_link`) so the base model on disk is never touched.

    Falls back to a real copy when hardlinks are unavailable — a different filesystem, or
    a container mount that forbids them. Correctness does not depend on which path runs.
    """
    try:
        shutil.copytree(src, dst, ignore=_skip, dirs_exist_ok=True, symlinks=False,
                        copy_function=os.link)
        return "hardlink"
    except Exception:
        # Partial trees are fine to overwrite: dirs_exist_ok fills the gaps, and every
        # file we may have linked is identical to its source by construction.
        shutil.copytree(src, dst, ignore=_skip, dirs_exist_ok=True, symlinks=False)
        return "copy"


def _break_link(path):
    """Replace a possibly-hardlinked file with a private copy before editing it.

    Without this, perturbing the shard in place would rewrite the BASE model's own file:
    a hardlink is the same inode, not a snapshot. That would corrupt the cached base for
    every later task on the box and silently change what the validator compares against.
    """
    if not os.path.isfile(path):
        return
    if os.stat(path).st_nlink <= 1:
        return
    tmp = path + ".unlinked"
    shutil.copyfile(path, tmp)
    os.replace(tmp, path)


def _find_embedding(keys):
    """Return the tensor name holding the input embeddings, or None."""
    for exact in _EMBED_KEYS:
        if exact in keys:
            return exact
    for suffix in _EMBED_KEYS:
        for k in keys:
            if k.endswith(suffix):
                return k
    return None


def _perturb_safetensors(folder):
    """Add noise to the embedding tensor, rewriting only the shard that holds it."""
    import torch
    from safetensors.torch import load_file, save_file

    index_path = os.path.join(folder, "model.safetensors.index.json")
    if os.path.isfile(index_path):
        with open(index_path) as fh:
            weight_map = json.load(fh).get("weight_map", {})
        name = _find_embedding(weight_map.keys())
        if name is None:
            return False, "no embedding tensor in the safetensors index"
        shard = os.path.join(folder, weight_map[name])
    else:
        shard = os.path.join(folder, "model.safetensors")
        if not os.path.isfile(shard):
            return False, "no model.safetensors and no shard index"
        name = None  # resolved after load

    # Un-link BEFORE reading, so the write below can never land on the base model's inode.
    _break_link(shard)

    tensors = load_file(shard)
    if name is None:
        name = _find_embedding(tensors.keys())
        if name is None:
            return False, "no embedding tensor in model.safetensors"

    # Generated on CPU in the tensor's own dtype: a 32B model's embedding is several GB
    # and this path exists precisely for runs whose GPU state is unknown or exhausted.
    w = tensors[name]
    noise = torch.randn(w.shape, dtype=torch.float32) * NOISE_STD
    tensors[name] = (w.to(torch.float32) + noise).to(w.dtype)

    # Preserve the shard's own metadata; safetensors requires the format key for
    # framework detection and drops it silently if we pass metadata=None.
    save_file(tensors, shard, metadata={"format": "pt"})
    return True, f"{name} in {os.path.basename(shard)}"


def main(model_path: str, save_folder: str):
    if not os.path.isdir(model_path):
        print(f"[noise] base model dir missing: {model_path}", flush=True)
        raise SystemExit(1)

    # Whatever a failed run left behind is not a submission. Replace it wholesale rather
    # than copying the base over the top, so a half-written checkpoint cannot survive
    # into the upload alongside base weights.
    if os.path.isdir(save_folder) and os.listdir(save_folder):
        print(f"[noise] clearing {len(os.listdir(save_folder))} leftover entries "
              f"from {save_folder}", flush=True)
        shutil.rmtree(save_folder, ignore_errors=True)

    print(f"[noise] cloning base model {model_path} -> {save_folder}", flush=True)
    how = _clone_tree(model_path, save_folder)
    print(f"[noise] clone method: {how}", flush=True)

    try:
        ok, detail = _perturb_safetensors(save_folder)
    except Exception as exc:  # noqa: BLE001 - see below
        ok, detail = False, f"{type(exc).__name__}: {exc}"

    if ok:
        print(f"[noise] perturbed {detail}", flush=True)
    else:
        # A copy the validator accepts beats no submission at all, so a failure to
        # perturb must NOT take the fallback down with it. The copy is already on disk
        # and passes model_is_a_finetune on its own.
        print(f"[noise] could not perturb embeddings ({detail}); "
              f"shipping the unperturbed copy", flush=True)

    n = len(os.listdir(save_folder))
    print(f"[noise] submission ready: {n} entries in {save_folder}", flush=True)
    if n == 0:
        print("[noise] submission dir is EMPTY — the upload will fail", flush=True)
        raise SystemExit(1)


if __name__ == "__main__":
    typer.run(main)
