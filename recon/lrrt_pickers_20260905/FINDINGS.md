# LR picker comparison, 2026-09-05/06

Raw logs here are force-added past `.gitignore`'s `*.log`. That rule exists for transient
output; these are the evidence for a conclusion, and an earlier commit silently dropped
them — the curves landed, the logs did not, and the commit message claimed both.

## Offline comparison, three curves (~25 min GPU)

Qwen2-1.5B / SmolLM-135M / falcon-rw-1b, all instruct on d99ce208.

| picker | raw distance | after `lr_search.clamp()` | direction |
|---|---|---|---|
| `slope10` (ships) | 308.6x | 53.5x | 0/3 above incumbent |
| `slope` | 30.9x | 22.8x | 0/3 above |
| `lossmin` | 4.0x | 2.9x | 3/3 above |
| `lossmin10` | 3.1x | 3.1x | 1/3 above |

The 777x of 2026-08-22 was not stale. Reading two gate logs had suggested ~19x; both of
those cells happened to be well behaved. Sweeps are deterministic — three repeats per cell
picked identical indices, bar one SmolLM `lossmin` point that moved 87->88.

## The structural finding

Under `slope10` every cell logs `UNBRACKETED(nothing above the incumbent; upward probe
suppressed)`. Every candidate sits below the incumbent, so the search can confirm it or go
lower and can never discover that a HIGHER rate is better. `lossmin`/`lossmin10` bracket.
On any task whose family-table rate is too low, the shipped picker makes that undiscoverable.

## The arbiter runs are INVALID — 10.5 GPU hours, no answer

`ops/smoke/lr_recovery.sh`, HOURS=1.3, Qwen2-1.5B, one run per picker. All three arms
returned byte-identical settled LRs and all three read STUCK. The cause is in `arbiter/*/`:

    [deadline] probe preempted by the budget — state set to 'finish' so the outer loop
               stops relaunching

`probe preempted` appears once in every poisoned run of every arm, never in a baseline. The
first training run eats the budget and the probe candidates are never trained, so the
settled LR is the incumbent regardless of picker.

The arms did differ, which is what makes this a diagnosis rather than a guess:

    slope10    lrrt=4.229e-06   probe ['4.229e-06']                UNBRACKETED
    lossmin10  lrrt=1.205e-05   probe ['1.205e-05']                above the poisoned prior
    lossmin    lrrt=1.205e-04   probe ['1.205e-04','3.118e-05']    STRADDLES the true 8.07e-05

`lossmin` bracketed the truth on both sides and still settled on a prior 10x too low.

**Before repeating: pilot for `probe preempted` first.** The script's header says HOURS must
be >= ~1.3 or the ladder never engages; that is necessary, not sufficient.

## Direction has two criteria that pull opposite ways

| criterion | prefers |
|---|---|
| cost of training at a wrong LR (+36% high vs +2.7% low) | miss LOW |
| ability to recover from a too-low prior | candidate HIGH |

`lossmin10` wins the first and therefore loses the second. Distance to the incumbent alone
cannot settle the choice, which is what the earlier note assumed it could.
