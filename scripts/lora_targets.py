"""Pick LoRA target modules without handing PEFT a name that matches whole layers.

NOT a port. The official diff report for tourn_add1dc83b8fd58b0_20260831 recommended
taking this fix from the challenger's repo, but that repo (yeahteam/txt-tombo-maju-jaya)
now 404s while the boss repo still resolves, so there is no source to copy. What follows
is written from the report's description and the one comment it quoted:

    "A Linear that lives directly inside an nn.Sequential/nn.ModuleList has a bare
     NUMERIC leaf name — quasar's GLA full-attention layers carry a low-rank gate
     gk_proj = nn.Sequential(Linear, Linear), i.e. Linears at
     ...self_attn.gla.gk_proj.0/1. Targeting the bare "0"/"1" makes PEFT suffix-match
     every model.layers.<n> DECODER LAYER and get_peft_model dies..."

THE BUG, in our own three copies. `find_all_linear_names` took `names[-1]`, so a Linear at
`model.layers.5.self_attn.gla.gk_proj.0` contributed the target `"0"`. PEFT matches
target_modules by name suffix, and `"0"` is a suffix of `model.layers.0` — an entire
decoder layer, not a Linear. get_peft_model then tries to wrap a whole layer and dies.

WHY IT LIVES HERE RATHER THAN IN A TRAINER. The function existed three times, byte for
byte identical, in train_instruct.py, train_dpo.py and train_grpo.py. Fixing one would
have left the same crash in the other two — the failure this repo keeps paying for is a
correct fix that only reached one of several copies. One definition, three importers.

The fix qualifies a numeric leaf with enough of its parent path to stop being a suffix of
a decoder layer: `gk_proj.0` instead of `0`. It walks back past consecutive numeric
components, so a Linear nested two ModuleLists deep still resolves to something anchored
on a real module name.
"""


def qualified_target(name: str) -> str:
    """The name to hand PEFT for a module at dotted path `name`.

    Normally the leaf. When the leaf is numeric — a Linear sitting directly in an
    nn.Sequential or nn.ModuleList — the leaf alone would suffix-match decoder layers, so
    it is prefixed with the nearest non-numeric ancestor.
    """
    parts = name.split(".")
    if len(parts) == 1:
        return parts[0]
    if not parts[-1].isdigit():
        return parts[-1]
    # Walk back over consecutive numeric components to the first real module name, and
    # keep everything from there down. `a.b.3.0` -> `b.3.0`, never the bare `0`.
    i = len(parts) - 1
    while i > 0 and parts[i - 1].isdigit():
        i -= 1
    if i == 0:
        # Every component is numeric, which should not happen for a real module, but
        # returning the bare digit is the one thing this function exists to prevent.
        return ".".join(parts)
    return ".".join(parts[i - 1:])


def find_all_linear_names(model, linear_types=None):
    """Target names for every Linear in `model`, minus lm_head.

    `linear_types` lets a caller pass the classes it cares about; the trainers pass
    (bnb.nn.Linear4bit, torch.nn.Linear) exactly as they did when each held its own copy.
    """
    if linear_types is None:  # pragma: no cover - trainers always pass their own
        import torch
        linear_types = (torch.nn.Linear,)

    lora_module_names = set()
    for name, module in model.named_modules():
        if isinstance(module, tuple(linear_types)):
            lora_module_names.add(qualified_target(name))

    lora_module_names.discard("lm_head")  # needed for 16-bit
    return list(lora_module_names)
