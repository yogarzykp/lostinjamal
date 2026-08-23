"""The gate waiter must be able to conclude that a run DIED, not just wait for success.

Every waiter before this one waited for a success marker, and a marker only ever proves
success. A run killed at minute 20 stops writing, never writes the marker, and the waiter
spins forever — silence indistinguishable from a healthy run. On a box that has thrown
162 contained Xid 94, which kill processes in exactly that way, a 77-minute gate that
died at minute 20 looked identical to one that was working.

Each test below drives the real script. The mutation test at the end is the one that
makes the rest mean anything: it disables each path in turn and asserts the corresponding
test starts failing. A peer session lost an afternoon to a test that passed because its
stub was static and the path under test never ran at all.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import time

import pytest

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "ops", "smoke", "wait_gate.sh")

# dmesg stubs. The growing one matters: a constant stub lets the Xid path pass without
# ever executing, which is how a test comes to pass for the wrong reason.
GROWING = """#!/usr/bin/env bash
n=$(cat "$COUNTER" 2>/dev/null || echo 1)
echo $((n+1)) > "$COUNTER"
for i in $(seq 1 "$n"); do echo "NVRM: Xid (PCI:0000:00:07): 94, contained"; done
"""
FLAT = """#!/usr/bin/env bash
echo "NVRM: Xid (PCI:0000:00:07): 94, contained"
"""
BROKEN = """#!/usr/bin/env bash
exit 1
"""


@pytest.fixture
def env(tmp_path):
    class E:
        def __init__(self, root):
            self.root = str(root)
            self.counter = os.path.join(self.root, "counter")
            self.procs = []

        def stub(self, name, body):
            p = os.path.join(self.root, name)
            with open(p, "w") as fh:
                fh.write(body)
            os.chmod(p, 0o755)
            return p

        def spawn(self, seconds, marker_into=None, marker="driver end"):
            """A stand-in run: lives `seconds`, optionally writing the marker at the end."""
            if marker_into:
                cmd = f'sleep {seconds}; echo "{marker}" >> "{marker_into}"'
            else:
                cmd = f"sleep {seconds}"
            p = subprocess.Popen(["bash", "-c", cmd])
            self.procs.append(p)
            pidfile = os.path.join(self.root, f"pid_{p.pid}")
            with open(pidfile, "w") as fh:
                fh.write(str(p.pid))
            return pidfile

        def spawn_and_reap(self, seconds=0):
            """A process that is dead AND reaped, so its pid stops answering entirely.

            Distinct from spawn(): an unreaped child is a ZOMBIE whose pid still answers
            `kill -0`. The two are caught by different branches, so each needs its own
            scenario or a mutation can disable one and be masked by the other.
            """
            p = subprocess.Popen(["bash", "-c", f"sleep {seconds}"])
            p.wait()
            pidfile = os.path.join(self.root, f"pid_reaped_{p.pid}")
            with open(pidfile, "w") as fh:
                fh.write(str(p.pid))
            return pidfile

        def run(self, log, pidfile, dmesg, timeout=25, script=SCRIPT):
            e = dict(os.environ, WAIT_GATE_POLL="1", WAIT_GATE_DMESG_CMD=dmesg,
                     COUNTER=self.counter)
            return subprocess.run(["bash", script, log, "driver end", pidfile, str(timeout)],
                                  capture_output=True, text=True, env=e, timeout=120)

        def log(self, name):
            p = os.path.join(self.root, name)
            open(p, "w").close()
            return p

    e = E(tmp_path)
    yield e
    for p in e.procs:
        try:
            p.kill()
        except Exception:
            pass


def test_clean_finish_exits_zero(env):
    log = env.log("a.log")
    pid = env.spawn(2, marker_into=log)
    r = env.run(log, pid, env.stub("flat.sh", FLAT))
    assert r.returncode == 0, r.stdout + r.stderr


def test_a_dead_run_is_reported_instead_of_waited_on_forever(env):
    """The case a marker-only waiter cannot see at all."""
    log = env.log("b.log")
    pid = env.spawn(1)  # dies without ever writing the marker
    r = env.run(log, pid, env.stub("flat.sh", FLAT))
    assert r.returncode == 4, (
        f"expected 4 (process gone, no marker), got {r.returncode}. A marker-only waiter "
        f"would still be spinning here.\n{r.stdout}"
    )
    # Either wording is correct — an unreaped child reports ZOMBIE, a reaped one GONE.
    assert "was never written" in r.stdout


def test_a_reaped_process_is_also_reported(env):
    """The other half of "dead": a pid that has stopped answering at all."""
    log = env.log("b2.log")
    pid = env.spawn_and_reap()
    r = env.run(log, pid, env.stub("flat.sh", FLAT), timeout=5)
    assert r.returncode == 4, f"expected 4, got {r.returncode}\n{r.stdout}"
    assert "GONE" in r.stdout


def test_a_new_xid_during_the_run_is_surfaced(env):
    """Finished-looking output can still be missing a path that died."""
    log = env.log("c.log")
    pid = env.spawn(3, marker_into=log)
    r = env.run(log, pid, env.stub("grow.sh", GROWING))
    assert r.returncode == 6, f"expected 6 (finished but Xid rose), got {r.returncode}\n{r.stdout}"
    assert "Xid rose" in r.stdout


def test_a_run_alive_past_the_deadline_is_reported(env):
    log = env.log("d.log")
    pid = env.spawn(30)
    r = env.run(log, pid, env.stub("flat.sh", FLAT), timeout=3)
    assert r.returncode == 7, f"expected 7 (deadline, still alive), got {r.returncode}"


def test_a_missing_pidfile_is_an_error_not_a_verdict(env):
    r = env.run(env.log("e.log"), os.path.join(env.root, "nope.pid"),
                env.stub("flat.sh", FLAT), timeout=3)
    assert r.returncode == 3


def test_unreadable_dmesg_reports_unknown_rather_than_zero(env):
    """A zero here would read exactly like 'no faults'. It is not the same claim."""
    log = env.log("f.log")
    pid = env.spawn(2, marker_into=log)
    r = env.run(log, pid, env.stub("broken.sh", BROKEN))
    assert r.returncode == 0
    assert "xid at start: UNKNOWN" in r.stdout, (
        f"a count was reported when dmesg could not be read:\n{r.stdout}"
    )


def test_the_quiet_span_is_actually_measured(env):
    """The stall threshold cannot be derived from stored logs, so the waiter measures it.

    Reported as an UPPER BOUND: a file also stops growing when output is buffered rather
    than when work stops.
    """
    log = env.log("g.log")
    pid = env.spawn(4, marker_into=log)
    r = env.run(log, pid, env.stub("flat.sh", FLAT))
    m = re.search(r"without log growth: (\d+)s", r.stdout)
    assert m, f"no quiet span reported:\n{r.stdout}"
    assert int(m.group(1)) >= 2, f"quiet span reported as {m.group(1)}s over a 4s silence"
    assert "upper bound" in r.stdout, "the caveat is missing from the output"


# ---------------------------------------------------------------------------
# The test that makes the others mean something
# ---------------------------------------------------------------------------

MUTATIONS = {
    "reaped-process check": (
        '  if ! kill -0 "$PID" 2>/dev/null; then\n    finish 4 ',
        '  if false; then\n    finish 4 '),
    "zombie check": (
        '    Z*) finish 4 ', '    ZZZNEVER*) finish 4 '),
    "xid comparison": (
        '&& [ "$XID_END" -gt "$XID_START" ]; then', '&& false; then'),
    "unknown-vs-zero on dmesg failure": (
        'out=$($DMESG_CMD 2>/dev/null) || { echo "UNKNOWN"; return; }',
        'out=$($DMESG_CMD 2>/dev/null) || { echo 0; return; }'),
    "quiet-span recording": (
        '    [ "$quiet" -gt "$longest_quiet" ] && longest_quiet=$quiet', '    :'),
}


@pytest.mark.parametrize("name", sorted(MUTATIONS))
def test_disabling_each_path_makes_a_test_fail(name, env, tmp_path):
    """If a path can be removed with every test still green, the tests guard nothing."""
    old, new = MUTATIONS[name]
    with open(SCRIPT) as fh:
        src = fh.read()
    assert old in src, f"mutation anchor for {name!r} no longer matches the script"
    mutant = os.path.join(str(tmp_path), "mutant.sh")
    with open(mutant, "w") as fh:
        fh.write(src.replace(old, new, 1))

    # Drive the state each mutation should break.
    if name == "reaped-process check":
        log = env.log("m1.log"); pid = env.spawn_and_reap()
        r = env.run(log, pid, env.stub("flat.sh", FLAT), timeout=4, script=mutant)
        broke = r.returncode != 4
    elif name == "zombie check":
        log = env.log("m1z.log"); pid = env.spawn(1)
        r = env.run(log, pid, env.stub("flat.sh", FLAT), timeout=4, script=mutant)
        broke = r.returncode != 4
    elif name == "xid comparison":
        log = env.log("m2.log"); pid = env.spawn(2, marker_into=log)
        r = env.run(log, pid, env.stub("grow.sh", GROWING), script=mutant)
        broke = r.returncode != 6
    elif name == "unknown-vs-zero on dmesg failure":
        log = env.log("m3.log"); pid = env.spawn(2, marker_into=log)
        r = env.run(log, pid, env.stub("broken.sh", BROKEN), script=mutant)
        broke = "xid at start: UNKNOWN" not in r.stdout
    else:
        log = env.log("m4.log"); pid = env.spawn(4, marker_into=log)
        r = env.run(log, pid, env.stub("flat.sh", FLAT), script=mutant)
        m = re.search(r"without log growth: (\d+)s", r.stdout)
        broke = not m or int(m.group(1)) < 2

    assert broke, (
        f"the {name} path was disabled and the corresponding check still passed — "
        f"that check is not guarding anything"
    )
