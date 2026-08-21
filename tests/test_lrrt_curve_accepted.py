"""The saved sweep curve must say whether its suggestion was actually used.

The curve exists to explain WHY a learning rate was chosen. A truncated sweep is
rejected by the too-few-points guard and its suggestion is thrown away — but the
curve was written before that guard ran, so the file recorded a `suggested_safe_lr`
the run never used, with nothing to say so. For a file whose only job is explaining
a choice, that is worse than not writing it at all.

The fix is an ordering invariant, so these assert on structure: the acceptance
decision is made before the write, the write records it, and the write still happens
for a REJECTED sweep (the truncated case is the one most worth inspecting — an OOM
after a handful of points is how the finder came to return 1.12e-08).

Source text is compared with comments stripped. An earlier test in this repo matched
its own explanatory prose, which passed for the wrong reason.
"""
import io
import os
import re
import tokenize

SRC = os.path.join(os.path.dirname(__file__), "..", "scripts", "train_instruct.py")


def _code_only(path):
    """Return the file's source with COMMENTS removed, strings left intact.

    Only comments are stripped, deliberately. An earlier version of this helper also
    tried to drop docstrings, and its "is this a docstring?" test was "does a STRING
    token follow a NEWLINE/NL?" — which is also true of every string that begins a
    continuation line, so it silently deleted the keys of any multi-line dict literal.
    That made two of these tests fail against correct code. The needles below are all
    code constructs that no docstring in the target file contains, so keeping strings
    costs nothing and removes the moving part.
    """
    with open(path) as fh:
        src = fh.read()
    out = []
    prev_end = (1, 0)
    for ttype, tstr, start, end, _ in tokenize.generate_tokens(io.StringIO(src).readline):
        if ttype == tokenize.COMMENT:
            continue
        if start[0] > prev_end[0]:
            out.append("\n" * (start[0] - prev_end[0]))
            out.append(" " * start[1])
        elif start[1] > prev_end[1]:
            out.append(" " * (start[1] - prev_end[1]))
        out.append(tstr)
        prev_end = end
    return "".join(out)


CODE = _code_only(SRC)


def _pos(needle):
    i = CODE.find(needle)
    assert i != -1, f"not found in code (comments stripped): {needle!r}"
    return i


def test_acceptance_is_decided_before_the_curve_is_written():
    assert _pos("_accepted = len(_swept) >= _min_pts") < _pos("lrrt_curve.json"), (
        "the curve is written before the run knows whether the sweep was accepted, "
        "so it cannot record which way the decision went"
    )


def test_curve_payload_records_acceptance():
    dump = CODE[_pos("json.dump({"):]
    dump = dump[: dump.find("}, _cf)")]
    for key in ('"accepted"', '"points"', '"min_points_required"'):
        assert key in dump, f"{key} missing from the curve payload"


def test_rejected_sweep_still_writes_its_curve():
    """The write must precede the raise, or the truncated case is never recorded."""
    assert _pos("lrrt_curve.json") < _pos("too few to locate a rate"), (
        "the too-few-points raise happens before the curve write, so a rejected "
        "sweep — the case most worth inspecting — leaves no curve at all"
    )


def test_rejection_still_raises():
    """Recording the rejection must not have turned the guard into a warning."""
    assert re.search(
        r"if not _accepted:\s*raise RuntimeError", CODE
    ), "the too-few-points guard no longer raises"


def test_sweep_resources_released_before_file_io():
    assert _pos("del _opt, _loader") < _pos("lrrt_curve.json"), (
        "the sweep optimizer and loader are still held while writing the curve"
    )
