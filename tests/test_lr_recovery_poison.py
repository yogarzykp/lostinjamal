"""The recovery gate must be unable to report a verdict it cannot support.

Two defects, both live from the commit that introduced the gate until 2026-08-22:

1. The poison factor was computed by interpolating shell values into Python SOURCE:

       python3 -c "print(f'{float('$BASE_LR') * float('$f'):.6e}')"

   Nested same-type quotes inside an f-string only became legal in Python 3.12
   (PEP 701). On the 3.10 the training box runs it is a SyntaxError, so POISON came
   back EMPTY, `${override:+ADAPTIVE_LR_OVERRIDE=...}` expanded to nothing, and every
   "poisoned" run trained on the untouched prior. The gate then scored it RECOVERED at
   ~1.0x — for any selector, including one that cannot recover at all.

2. Nothing checked that the poison had been applied, so failure mode 1 was invisible.

These tests execute the shipped shell text rather than paraphrasing it, because the
defect WAS the exact quoting: a test that reimplemented the expression would have
passed while the script stayed broken.
"""
import re
import subprocess
import sys
import os

GATE = os.path.join(os.path.dirname(__file__), "..", "ops", "smoke", "lr_recovery.sh")


def _script():
    with open(GATE) as fh:
        return fh.read()


def _extract(pattern, label):
    m = re.search(pattern, _script(), re.S)
    assert m, f"could not locate {label} in lr_recovery.sh"
    return m.group(1)


def test_poison_expression_runs_on_this_interpreter():
    """The exact python invocation the gate uses must produce a number, not a traceback."""
    body = _extract(r"POISON=\$\(python3 -c '([^']+)'", "the POISON computation")
    out = subprocess.run([sys.executable, "-c", body, "8.07e-05", "10"],
                         capture_output=True, text=True)
    assert out.returncode == 0, f"poison expression failed: {out.stderr}"
    assert out.stdout.strip(), "poison expression produced EMPTY output"
    assert abs(float(out.stdout) - 8.07e-04) / 8.07e-04 < 1e-9, out.stdout


def test_poison_expression_handles_a_fractional_factor():
    body = _extract(r"POISON=\$\(python3 -c '([^']+)'", "the POISON computation")
    out = subprocess.run([sys.executable, "-c", body, "8.07e-05", "0.1"],
                         capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    assert abs(float(out.stdout) - 8.07e-06) / 8.07e-06 < 1e-9, out.stdout


def test_values_are_passed_as_argv_not_interpolated_into_source():
    """The specific shape that broke. Interpolating into an f-string is what failed."""
    line = _extract(r"(POISON=\$\(python3 -c .*?\))\n", "the POISON assignment")
    assert "sys.argv" in line, "poison values must arrive as argv"
    assert "f'{" not in line and 'f"{' not in line, (
        "poison is being built by interpolating shell values into an f-string again"
    )


def test_gate_refuses_to_run_on_an_empty_poison():
    s = _script()
    assert re.search(r"\[ -n \"\$POISON\" \]", s), "no guard on an empty poison"
    assert "refusing to run" in s, "an empty poison must abort, not proceed silently"


def test_poison_confirmation_rejects_an_unpoisoned_run():
    """The check must FAIL when the planned incumbent is the untouched prior."""
    body = _extract(r"python3 -c '(import sys\nwant, got.*?)' \"\$POISON\"", "the confirmation check")
    same = subprocess.run([sys.executable, "-c", body, "8.070000e-04", "8.070e-04"],
                          capture_output=True, text=True)
    assert same.returncode == 0, f"a correctly poisoned run was rejected: {same.stderr}"

    unpoisoned = subprocess.run([sys.executable, "-c", body, "8.070000e-04", "8.070e-05"],
                                capture_output=True, text=True)
    assert unpoisoned.returncode != 0, (
        "an UNPOISONED run passed the confirmation check — this is the exact blindness "
        "that let the gate report RECOVERED for runs that were never poisoned"
    )


def test_confirmation_aborts_when_no_incumbent_line_exists():
    s = _script()
    assert "cannot confirm the prior was poisoned" in s, (
        "a run whose log has no incumbent= line must abort rather than be judged"
    )


# ---------------------------------------------------------------------------
# extract_lr: the third defect in this script, and the one that produced a
# confident wrong number rather than a missing one.
# ---------------------------------------------------------------------------

import tempfile

# A log shaped like a real run that produced no BL line: the range test prints its
# SUGGESTION as `safe_lr=`, and the trainer logs the schedule it actually used.
_LOG_NO_BL = """\
INFO:root:print: [lrrt] picker=slope suggested_lr=4.13e-06, safe_lr=4.13e-07 (idx=32/100)
INFO:root:print: [lr-search] task=instruct lrrt=1.000e-06 incumbent=8.070e-04 -> probe ['1.000e-06']
{'loss': 2.31, 'learning_rate': 7.017391304347826e-05, 'epoch': 0.05}
{'loss': 2.20, 'learning_rate': 0.0008068927530662348, 'epoch': 0.5}
{'loss': 2.18, 'learning_rate': 0.0004, 'epoch': 0.9}
"""

_LOG_WITH_BL = _LOG_NO_BL + "BL;1;2.5008; 0.0008068927530662348\n"

_LOG_EMPTY = "nothing useful here at all\n"


def _run_extract_lr(log_text):
    """Source the shipped extract_lr and run it on a log, exactly as the gate does."""
    body = _extract(r"(extract_lr\(\) \{.*?\n\})", "extract_lr")
    with tempfile.NamedTemporaryFile("w", suffix=".log", delete=False) as fh:
        fh.write(log_text)
        path = fh.name
    try:
        out = subprocess.run(
            ["bash", "-c", body + f'\nextract_lr "{path}"'],
            capture_output=True, text=True,
        )
        return out.stdout.strip(), out.stderr, out.returncode
    finally:
        os.unlink(path)


def test_extract_lr_returns_the_trained_rate_not_the_sweep_suggestion():
    """The exact failure of 2026-08-22, which reported 4.13e-07 for a run at 8.07e-04."""
    got, _, rc = _run_extract_lr(_LOG_NO_BL)
    assert rc == 0, "extract_lr failed to run"
    assert got, "extract_lr returned nothing for a log with a usable schedule"
    assert abs(float(got) - 8.068927530662348e-04) / 8.068927530662348e-04 < 1e-9, (
        f"extract_lr returned {got!r}; it is reading the sweep suggestion again, not "
        f"the peak of the schedule the run actually trained on"
    )
    assert abs(float(got) - 4.13e-07) > 1e-12, "returned safe_lr, the value that misled us"


def test_extract_lr_agrees_with_the_ladder_when_a_bl_line_exists():
    got, err, rc = _run_extract_lr(_LOG_WITH_BL)
    assert rc == 0
    assert abs(float(got) - 8.068927530662348e-04) / 8.068927530662348e-04 < 1e-9, got
    assert "should agree" not in err, f"spurious disagreement warning: {err}"


def test_extract_lr_warns_when_selection_and_training_disagree():
    """A ladder that selects one rate while the trainer uses another is a real defect.

    Asserted on the VALUES, not on the sentence: an earlier version of this test matched
    the warning's exact wording and started failing the moment the wording was reworded,
    which says nothing about whether the warning still fires.
    """
    disagreeing = _LOG_NO_BL + "BL;1;2.5008; 1.0e-05\n"
    _, err, _ = _run_extract_lr(disagreeing)
    assert "!!" in err, "a selected LR that differs from the trained LR was reported silently"
    # Compared numerically: the log writes rates in whichever notation the trainer used
    # (0.00080689... here, 8.07e-05 elsewhere), so matching on the printed string tests
    # the formatter rather than the warning.
    nums = [float(x) for x in re.findall(r"[0-9]*\.?[0-9]+(?:[eE][+-]?[0-9]+)?", err)]
    assert any(abs(n - 1.0e-05) / 1.0e-05 < 1e-6 for n in nums), (
        f"the warning does not name the SELECTED rate, so it cannot be acted on: {err!r}"
    )
    assert any(abs(n - 8.068927530662348e-04) / 8.068927530662348e-04 < 1e-6 for n in nums), (
        f"the warning does not name the TRAINED rate, so it cannot be acted on: {err!r}"
    )


def test_extract_lr_stays_quiet_when_they_agree():
    """The warning must be a signal, not noise on every healthy run."""
    _, err, _ = _run_extract_lr(_LOG_WITH_BL)
    assert "!!" not in err, f"spurious disagreement warning on a healthy log: {err!r}"


def test_extract_lr_returns_nothing_rather_than_guessing():
    """An unusable log must produce an UNKNOWN verdict, never a value that merely matched."""
    got, _, rc = _run_extract_lr(_LOG_EMPTY)
    assert rc == 0
    assert got == "", f"extract_lr invented {got!r} from a log with no learning rate in it"


# ---------------------------------------------------------------------------
# The multi-run case. Every fixture above is a SINGLE training run, and that is
# exactly why an earlier version of these tests passed while extract_lr was
# reading the wrong number: one gate run produces one log, but that log holds
# every sub-run of the ladder concatenated — probe, confirmations, final.
# ---------------------------------------------------------------------------

# Shaped like a real recovery run poisoned 10x high. The PROBE trains at the poison
# (8.07e-04); the search then moves and the FINAL run settles on 2.84e-05. A whole-file
# peak reports 8.07e-04 and scores STUCK at exactly the poison factor — the most
# convincing possible wrong answer, since it reads as "the search never moved".
_LOG_LADDER = """\
************* Training attempt 1/5 for task abc *************
INFO:root:print: [lrrt] picker=slope suggested_lr=4.13e-06, safe_lr=4.13e-07 (idx=32/100)
INFO:root:print: [lr-search] task=instruct lrrt=1.000e-06 incumbent=8.070e-04 -> probe ['1.000e-06', '2.841e-05']
{'loss': 2.61, 'learning_rate': 0.0004, 'epoch': 0.2}
{'loss': 2.55, 'learning_rate': 0.0008068927530662348, 'epoch': 0.5}
INFO:root:finish: Training successfully done
************* Training attempt 1/5 for task abc *************
{'loss': 2.49, 'learning_rate': 5.0e-07, 'epoch': 0.2}
{'loss': 2.47, 'learning_rate': 1.0e-06, 'epoch': 0.5}
INFO:root:finish: Training successfully done
************* Training attempt 1/5 for task abc *************
{'loss': 2.44, 'learning_rate': 1.2e-05, 'epoch': 0.2}
{'loss': 2.41, 'learning_rate': 2.8403970151813985e-05, 'epoch': 0.5}
{'loss': 2.40, 'learning_rate': 1.9e-05, 'epoch': 0.9}
INFO:root:finish: Training successfully done
"""


def test_extract_lr_reads_the_final_run_not_the_highest_rate_ever_probed():
    """The regression a whole-file peak introduces, measured on a real log 2026-08-22.

    The probe necessarily trains AT the poison — the incumbent check proves it — so a
    whole-file maximum is >= the poison for any upward poison, and the gate reports
    STUCK at exactly the poison factor however well the selector recovered.
    """
    got, _, rc = _run_extract_lr(_LOG_LADDER)
    assert rc == 0 and got, "extract_lr returned nothing for a multi-run ladder log"
    settled = 2.8403970151813985e-05
    poison = 8.068927530662348e-04
    assert abs(float(got) - settled) / settled < 1e-9, (
        f"extract_lr returned {got!r}. Expected the FINAL run's rate {settled:.4e}; "
        f"{poison:.4e} would mean it is reporting the peak across every ladder run, "
        f"which is the poison the probe trained at."
    )


def test_whole_file_peak_would_have_scored_this_stuck():
    """Pin the consequence, so the cost of regressing is visible in the test name."""
    baseline = 8.067916949497648e-05
    got, _, _ = _run_extract_lr(_LOG_LADDER)
    off_by = max(float(got) / baseline, baseline / float(got))
    assert off_by < 3.0, f"off-by {off_by:.2f}x — extract_lr is reading a probe run again"
    whole_file_peak = 8.068927530662348e-04
    assert max(whole_file_peak / baseline, baseline / whole_file_peak) > 9.0, (
        "sanity: the whole-file peak really would have scored ~10x, i.e. STUCK"
    )


def test_extract_lr_still_works_when_no_attempt_markers_exist():
    """Single-run logs without the marker must keep working — the fallback path."""
    got, _, rc = _run_extract_lr(_LOG_NO_BL)
    assert rc == 0
    assert abs(float(got) - 8.068927530662348e-04) / 8.068927530662348e-04 < 1e-9, got
