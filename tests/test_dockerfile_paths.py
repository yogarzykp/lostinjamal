"""The validator must find our dockerfile, and must find the one we think it finds.

It resolves a miner's dockerfile from a tuple, taking the first path that exists
(G.O.D trainer/constants.py, trainer/runtime.py `_resolve_dockerfile_path`):

    ops/docker/standalone-text-trainer.dockerfile     <- DEFAULT, tried first
    dockerfiles/standalone-text-trainer.dockerfile    <- LEGACY, tried second

Two failures are guarded here, and the second is the sneaky one.

Missing entirely: `_resolve_dockerfile_path` raises FileNotFoundError and the task never
starts. Not a slow build — no build, no submission, on every task type that is not an
image task, because the branch selecting this tuple is a bare `else`.

Drifted: the validator builds the DEFAULT copy while `pre-submit-smoke-test.sh` and
`scripts/train_cst.py` read the LEGACY one. A green local dry run would then say nothing
about the image production actually builds — the worst kind of test, one that reports on
something other than what ships.
"""

import os

import pytest

REPO = os.path.join(os.path.dirname(__file__), "..")

# Mirrors G.O.D's TEXT_DOCKERFILE_PATHS, in ITS order. Order matters: it decides which
# copy the validator builds when the two disagree.
CANDIDATES = (
    "ops/docker/standalone-text-trainer.dockerfile",
    "dockerfiles/standalone-text-trainer.dockerfile",
)


def _read(rel):
    with open(os.path.join(REPO, rel), "rb") as fh:
        return fh.read()


def _exists(rel):
    return os.path.isfile(os.path.join(REPO, rel))


def test_the_default_path_exists():
    """Not merely 'some path resolves'. The legacy entry is named for removal."""
    assert _exists(CANDIDATES[0]), (
        f"{CANDIDATES[0]} is missing. It resolves today only because the validator still "
        f"falls back to the legacy path; when that entry goes, no dockerfile is found and "
        f"the task does not start at all."
    )


def test_the_legacy_path_still_exists():
    """Kept deliberately, for validators that do not know the new path yet."""
    assert _exists(CANDIDATES[1]), (
        f"{CANDIDATES[1]} was removed. Older validators resolve only this path, so "
        f"deleting it trades one risk for another rather than closing it."
    )


def test_the_two_copies_have_not_drifted():
    a, b = (_read(c) for c in CANDIDATES)
    assert a == b, (
        "the two dockerfile copies differ. The validator builds "
        f"{CANDIDATES[0]} (tried first) while our own tooling reads {CANDIDATES[1]}, so a "
        "passing local build proves nothing about the image that ships."
    )


def test_resolution_picks_the_same_file_the_validator_would():
    """Resolve exactly as upstream does, rather than assuming a path by its name."""
    resolved = next((c for c in CANDIDATES if _exists(c)), None)
    assert resolved is not None, "no dockerfile would resolve; the task cannot start"
    assert resolved == CANDIDATES[0], (
        "resolution falls through to the legacy path, which means the default copy is "
        "missing"
    )


def test_the_resolved_file_is_a_usable_dockerfile():
    """A copy that exists but is not buildable closes nothing."""
    text = _read(CANDIDATES[0]).decode()
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    directives = [ln for ln in lines if not ln.startswith("#")]
    assert directives, "the file is entirely comments"
    assert directives[0].upper().startswith(("FROM", "ARG")), (
        f"the first instruction is {directives[0]!r}; docker requires FROM (or ARG) first, "
        f"so the header comment block must not have introduced anything before it"
    )
    assert "COPY scripts" in text, (
        "the trainer sources are no longer copied in — the build context is the repo root "
        "for both locations, so this path should not have changed"
    )


@pytest.mark.parametrize("rel", CANDIDATES)
def test_neither_copy_hardcodes_its_own_location(rel):
    """The build context is the repo root wherever the dockerfile sits, so a path that
    reaches out relative to the dockerfile would break on exactly one of the two."""
    text = _read(rel).decode()
    for ln in text.splitlines():
        stripped = ln.strip()
        if stripped.startswith("#"):
            continue
        if stripped.upper().startswith(("COPY", "ADD")):
            assert ".." not in stripped, (
                f"{rel} has a context-relative escape: {stripped!r}. The context is the "
                f"repo root for both locations, so this resolves differently than intended."
            )
