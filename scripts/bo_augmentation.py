"""GP-based Bayesian Optimization for LR exploration.

Fits a Gaussian Process to past (lr, eval_loss) observations and suggests
the LR that maximizes Expected Improvement (EI). Used during the explore
loop (text_trainer.py) to refine the geometric extend_learning_rates scan
with empirical signal once enough probe observations exist.

Design properties:
  - Log-space LR (spans 1e-7 to 1e-2 typically) via Optuna FloatDistribution(log=True)
  - Matern 5/2 kernel (Optuna GPSampler default, best-fit for HPO)
  - Cold start bail: return None if < 3 observations (GP posterior too flat)
  - Graceful degradation: return None on any error — never breaks caller
  - Absolute safety via allowed_lower/upper clamp (anchored to base_lr × [1/10, 10])

Public API:
  - is_available()       — Optuna installed + env flag enabled
  - derive_bounds(...)   — compute search trust region from base_lr / observations
  - fit_gp_suggest(...)  — main entry — returns Optional[float] suggested LR

Environment flags:
  TRAINING_BO_AUGMENT            - "1"/"true" to enable (default: true)
  TRAINING_BO_MIN_OBSERVATIONS   - cold start threshold (default: 3)
  TRAINING_BO_SEED               - deterministic for testing (default: 42)
  TRAINING_BO_BOUNDS_EXPANSION   - bounds expansion factor (default: 10.0)
  TRAINING_BO_DUP_LOG_DELTA      - duplicate threshold in log10 space (default: 0.15 ≈ 40% rel)
  TRAINING_BO_RESAMPLE_ATTEMPTS  - resample attempts before Sobol fallback (default: 3)

Duplicate-suppression strategies (research: arXiv:2310.20708 LogEI):
  1. Per-call seed jitter — base_seed + len(obs)*1000 prevents deterministic
     loop when observations don't change between calls.
  2. Adaptive n_startup_trials — force Sobol when <4 obs (GP lengthscale unstable).
  3. Min-distance duplicate filter — reject suggestions within DUP_LOG_DELTA
     log10-distance of any observed LR.
  4. Sobol gap fallback — if all resample attempts duplicate, place LR at the
     midpoint of the largest unexplored log-space gap.
"""

from __future__ import annotations

import math
import os
from typing import Any, Optional

# Optional dependency — graceful import
_OPTUNA_AVAILABLE = False
_OPTUNA_IMPORT_ERROR: Optional[str] = None
try:
    import optuna
    from optuna.samplers import GPSampler
    from optuna.distributions import FloatDistribution
    _OPTUNA_AVAILABLE = True
    # Suppress Optuna's verbose logging (we log our own)
    optuna.logging.set_verbosity(optuna.logging.WARNING)
except ImportError as exc:
    _OPTUNA_IMPORT_ERROR = str(exc)


def _parse_bool(value: Optional[str], default: bool = True) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_int(value: Any, default: int) -> int:
    try:
        return int(value) if value is not None else default
    except (TypeError, ValueError):
        return default


def is_available() -> bool:
    """Return True if GP augmentation is usable (library installed + flag on)."""
    if not _OPTUNA_AVAILABLE:
        return False
    return _parse_bool(os.getenv("TRAINING_BO_AUGMENT"), default=True)


def get_import_error() -> Optional[str]:
    """Return the ImportError message if Optuna failed to load, else None."""
    return _OPTUNA_IMPORT_ERROR


_ABS_LOWER_DEFAULT = 1e-7
_ABS_UPPER_DEFAULT = 1e-1


def _is_duplicate_log10(
    candidate: float,
    observed_lrs: list[float],
    delta: float,
) -> bool:
    """Return True if candidate is within `delta` log10-distance of any observed.

    delta=0.15 ≈ 40% relative (10^0.15 ≈ 1.41). Standard heuristic from BO
    literature for "too close to existing observation."
    """
    if not observed_lrs:
        return False
    cand_log = math.log10(max(candidate, 1e-30))
    return any(
        abs(cand_log - math.log10(max(lr, 1e-30))) < delta
        for lr in observed_lrs
    )


def _largest_log_gap_midpoint(
    observed_lrs: list[float],
    lower: float,
    upper: float,
) -> float:
    """Place a fresh LR at the midpoint (log-space) of the largest unexplored
    gap between sorted observations + bounds.

    Used as fallback when GP keeps suggesting duplicates after multiple
    resample attempts. Guarantees diversity by construction.
    """
    sorted_lrs = sorted(set(lr for lr in observed_lrs if lower <= lr <= upper))
    boundary_points = [lower] + sorted_lrs + [upper]
    log_points = [math.log10(p) for p in boundary_points]

    # Find largest gap
    gaps = [(log_points[i + 1] - log_points[i], i) for i in range(len(log_points) - 1)]
    gaps.sort(reverse=True)  # largest first
    _, idx = gaps[0]

    midpoint_log = (log_points[idx] + log_points[idx + 1]) / 2
    return 10 ** midpoint_log


def _confidence_expansion_factor(family_conf: Optional[str]) -> float:
    """Map family confidence label → bounds expansion factor.

    Wider expansion for less-confident anchors lets BO escape the
    family LR neighborhood when Tier 1 is severely off (10×+).
    Default expansion 10 covers 100× span; LOW conf bumps to 30 (900× span);
    no-hit bumps to 100 (10,000× span — full abs_lower..abs_upper).
    """
    if not family_conf:
        return 10.0  # default
    conf_upper = family_conf.upper()
    if conf_upper.startswith("HIGH") or conf_upper == "CLASSIFIER":
        return 10.0
    if conf_upper.startswith("MED-LOW"):
        return 20.0
    if conf_upper.startswith("MED"):
        return 15.0
    if conf_upper.startswith("LOW-OK"):
        return 25.0
    if conf_upper.startswith("LOW"):
        return 30.0
    if "FAMILY-FALLBACK" in conf_upper:
        return 30.0
    if conf_upper.endswith("-ADJ"):
        return 15.0
    if conf_upper in ("TIER2", "MISS"):
        return 100.0   # 4-decade span — Tier 2 has no signal
    return 10.0


def derive_bounds(
    *,
    base_lr: Optional[float],
    observations: Optional[list[tuple[float, float]]] = None,
    family_conf: Optional[str] = None,
    abs_lower: float = _ABS_LOWER_DEFAULT,
    abs_upper: float = _ABS_UPPER_DEFAULT,
    expansion: Optional[float] = None,
) -> tuple[float, float]:
    """Derive sensible GP search bounds anchored on base_lr (or observation
    range). Prevents boundary-oscillation in GP-EI when bounds span too many
    orders of magnitude with few observations.

    Strategy (in priority order):
      1. base_lr valid → bounds = base_lr × [1/expansion, expansion]
      2. observations available → use min/max LR × [1/expansion, expansion]
      3. fallback → [abs_lower, abs_upper]

    Expansion factor:
      - explicit `expansion` arg     overrides everything
      - else env TRAINING_BO_BOUNDS_EXPANSION  if set
      - else family_conf-derived (HIGH=10, LOW=30, TIER2=100)

    All bounds clamped to [abs_lower, abs_upper] for absolute safety.
    """
    if expansion is None:
        env_val = os.getenv("TRAINING_BO_BOUNDS_EXPANSION")
        if env_val is not None:
            try:
                expansion = float(env_val)
            except (TypeError, ValueError):
                expansion = None
        if expansion is None:
            expansion = _confidence_expansion_factor(family_conf)

    if not math.isfinite(expansion) or expansion <= 1:
        expansion = 10.0

    if (
        base_lr is not None
        and isinstance(base_lr, (int, float))
        and math.isfinite(base_lr)
        and base_lr > 0
    ):
        lower = max(abs_lower, base_lr / expansion)
        upper = min(abs_upper, base_lr * expansion)
        if lower < upper:
            return lower, upper

    if observations:
        valid_lrs = [
            lr for lr, _ in observations
            if isinstance(lr, (int, float)) and math.isfinite(lr) and lr > 0
        ]
        if valid_lrs:
            lower = max(abs_lower, min(valid_lrs) / expansion)
            upper = min(abs_upper, max(valid_lrs) * expansion)
            if lower < upper:
                return lower, upper

    return abs_lower, abs_upper


def expand_bounds_on_boundary_touch(
    *,
    observations: list[tuple[float, float]],
    current_lower: float,
    current_upper: float,
    expand_factor: float = 10.0,
    boundary_threshold: float = 0.15,
    edge_loss_margin: float = 0.05,
    abs_lower: float = _ABS_LOWER_DEFAULT,
    abs_upper: float = _ABS_UPPER_DEFAULT,
) -> tuple[float, float, Optional[str]]:
    """Detect if optimum likely lies BEYOND current search bounds and expand
    the relevant side `expand_factor`× outward. Returns (new_lower,
    new_upper, direction) where direction is 'lower'/'upper'/None.

    Two trigger conditions (TuRBO-inspired):

    1. **Bound-touch**: best observation is within `boundary_threshold`
       log10-distance of a current bound. Expand that bound side.

    2. **Cloud-edge**: best observation IS the lowest (or highest) LR in
       the observation set, AND the loss at that edge is meaningfully
       better (>= `edge_loss_margin` relative) than the loss at the
       opposite-direction observation. This catches the case where the
       geometric scan covers smaller area than bounds, so obs cluster
       inside bounds but the signal trend points outward — optimum likely
       beyond what we've sampled.

    Both checks complementary: bound-touch handles when scan == bounds,
    cloud-edge handles when scan < bounds (e.g., HIGH conf focused scan
    inside MED conf bounds).

    Caps at [abs_lower, abs_upper].
    """
    if not observations:
        return current_lower, current_upper, None

    valid = [(lr, loss) for lr, loss in observations
             if isinstance(lr, (int, float)) and math.isfinite(lr) and lr > 0
             and isinstance(loss, (int, float)) and math.isfinite(loss)]
    if not valid:
        return current_lower, current_upper, None

    best_lr, best_loss = min(valid, key=lambda x: x[1])
    log_best = math.log10(best_lr)
    log_lo = math.log10(max(current_lower, 1e-30))
    log_hi = math.log10(max(current_upper, 1e-30))

    new_lower, new_upper, direction = current_lower, current_upper, None

    # === Trigger 1: Bound-touch ===
    if abs(log_best - log_lo) < boundary_threshold and current_lower > abs_lower:
        new_lower = max(abs_lower, current_lower / expand_factor)
        direction = "lower"
        return new_lower, new_upper, direction

    if abs(log_best - log_hi) < boundary_threshold and current_upper < abs_upper:
        new_upper = min(abs_upper, current_upper * expand_factor)
        direction = "upper"
        return new_lower, new_upper, direction

    # === Trigger 2: Cloud-edge (best at edge of OBSERVATION cloud AND
    #                              near actual bound) ===
    # Stricter than original: requires BOTH conditions, otherwise misfires
    # when best is just-the-lowest-of-2-obs but actually mid-bounds.
    # E.g., obs=[(9e-5, 1.18), (3e-4, 1.32)] → best 9e-5 is "lowest_obs" but
    # NOT near lower bound (e.g., 4e-6) → DON'T expand. Optimum is between.
    cloud_edge_threshold = 0.5  # 0.5 log10 ≈ 3× from bound
    if len(valid) >= 2:
        sorted_by_lr = sorted(valid, key=lambda x: x[0])
        lowest_obs_lr, lowest_loss = sorted_by_lr[0]
        highest_obs_lr, highest_loss = sorted_by_lr[-1]

        # Best at lowest LR AND actually near lower bound (not just middle)
        if (
            best_lr == lowest_obs_lr
            and current_lower > abs_lower
            and abs(log_best - log_lo) < cloud_edge_threshold
        ):
            if highest_loss > best_loss * (1 + edge_loss_margin):
                new_lower = max(abs_lower, current_lower / expand_factor)
                direction = "lower-cloud-edge"
                return new_lower, new_upper, direction

        # Best at highest LR AND actually near upper bound
        if (
            best_lr == highest_obs_lr
            and current_upper < abs_upper
            and abs(log_best - log_hi) < cloud_edge_threshold
        ):
            if lowest_loss > best_loss * (1 + edge_loss_margin):
                new_upper = min(abs_upper, current_upper * expand_factor)
                direction = "upper-cloud-edge"
                return new_lower, new_upper, direction

    return new_lower, new_upper, direction


def fit_gp_suggest(
    *,
    observations: list[tuple[float, float]],
    allowed_lower: float,
    allowed_upper: float,
    min_observations: Optional[int] = None,
    seed: Optional[int] = None,
) -> Optional[float]:
    """Fit GP to (lr, eval_loss) observations, suggest next LR via Expected Improvement.

    Returns None (caller should fall back to tier 3) when:
      - Optuna not installed / not available
      - TRAINING_BO_AUGMENT disabled
      - Fewer than min_observations valid points (cold start)
      - Invalid bounds (allowed_lower >= allowed_upper, non-positive)
      - Optuna raises any exception

    Parameters
    ----------
    observations : list of (lr, eval_loss)
        Past training results. LR in linear scale, loss any scale.
        NaN/non-positive LRs are filtered out.
    allowed_lower, allowed_upper : float
        LR trust region (same as LLM's allowed range).
    min_observations : int, optional
        Cold start threshold. Defaults to env var or 3.
    seed : int, optional
        Deterministic seed. Defaults to env var or 42.

    Returns
    -------
    Optional[float]
        Suggested LR in [allowed_lower, allowed_upper], or None.
    """
    if not is_available():
        if not _OPTUNA_AVAILABLE:
            print(
                f"[bo] skipped: optuna not available ({_OPTUNA_IMPORT_ERROR})",
                flush=True,
            )
        return None

    # MIN_OBS reduced from 3 → 2 (2026-05-09): Tier 1 family table is coarse,
    # so we want BO firing as early as possible. Diversity check below ensures
    # GP only fits when observations span enough log-space for stable lengthscale.
    min_obs = min_observations if min_observations is not None else _parse_int(
        os.getenv("TRAINING_BO_MIN_OBSERVATIONS"), 2
    )
    rng_seed = seed if seed is not None else _parse_int(
        os.getenv("TRAINING_BO_SEED"), 42
    )
    # Diversity gate: require observations span ≥ MIN_LOG_SPAN log10 units.
    # If clustered, GP lengthscale fit is unstable — caller should keep
    # geometric. Default 0.3 (≈2× spread). Auto-disable with min_log_span=0.
    min_log_span = float(os.getenv("TRAINING_BO_MIN_LOG_SPAN", "0.3"))

    # Filter invalid observations
    valid = [
        (lr, loss) for lr, loss in observations
        if isinstance(lr, (int, float))
        and isinstance(loss, (int, float))
        and math.isfinite(lr) and lr > 0
        and math.isfinite(loss)
    ]

    if len(valid) < min_obs:
        print(
            f"[bo] skipped: only {len(valid)} valid obs (need {min_obs})",
            flush=True,
        )
        return None

    # Diversity check: if observations clustered too tightly, GP fit is
    # unstable — return None so caller keeps geometric extension instead.
    if min_log_span > 0 and len(valid) >= 2:
        log_lrs = [math.log10(lr) for lr, _ in valid]
        log_span = max(log_lrs) - min(log_lrs)
        if log_span < min_log_span:
            print(
                f"[bo] skipped: observations cluster too tight "
                f"(log10_span={log_span:.3f} < {min_log_span}); GP fit unstable",
                flush=True,
            )
            return None

    # Bounds sanity
    if not (math.isfinite(allowed_lower) and math.isfinite(allowed_upper)):
        print("[bo] skipped: non-finite bounds", flush=True)
        return None
    if allowed_lower <= 0 or allowed_upper <= allowed_lower:
        print(
            f"[bo] skipped: invalid bounds [{allowed_lower}, {allowed_upper}]",
            flush=True,
        )
        return None

    # Tunables for duplicate suppression
    dup_delta = float(os.getenv("TRAINING_BO_DUP_LOG_DELTA", "0.15"))
    resample_attempts = max(1, _parse_int(os.getenv("TRAINING_BO_RESAMPLE_ATTEMPTS"), 3))

    # Per-call seed jitter — without this, sequential ask() calls with the
    # same observation set return the SAME deterministic LR every time
    # (Optuna issue #5481). Mixing in observation count + scattered hash of
    # latest observation breaks the determinism while keeping reproducibility
    # within a single (obs-set, jitter) pair.
    jittered_seed = rng_seed + len(valid) * 1000

    # Adaptive cold-start: GP needs ≥4 diverse observations for stable
    # lengthscale fit (rule of thumb: 2d+2 with d=1). Force Sobol exploration
    # via n_startup_trials when below that threshold even though we preload.
    cold_obs_threshold = 4
    n_startup = max(0, cold_obs_threshold - len(valid))

    distribution = FloatDistribution(allowed_lower, allowed_upper, log=True)
    observed_lrs = [lr for lr, _ in valid]

    try:
        study = optuna.create_study(
            direction="minimize",
            sampler=GPSampler(
                seed=jittered_seed,
                n_startup_trials=n_startup,
                deterministic_objective=False,  # explicit: eval_loss IS noisy
            ),
        )

        # Pre-load observations (clamp into bounds — GP can't seed OOB values)
        for lr, loss in valid:
            clamped_lr = max(allowed_lower, min(allowed_upper, lr))
            trial = optuna.trial.create_trial(
                params={"lr": clamped_lr},
                distributions={"lr": distribution},
                value=float(loss),
            )
            study.add_trial(trial)

        # Multi-attempt resample loop with duplicate filter.
        # Each resample uses a fresh seed → different QMC starts → different
        # acquisition optimum candidate.
        suggested = None
        for attempt in range(resample_attempts):
            # Mutate sampler seed per attempt (re-instantiate to swap seed)
            if attempt > 0:
                study.sampler = GPSampler(
                    seed=jittered_seed + attempt * 7919,  # prime jitter
                    n_startup_trials=n_startup,
                    deterministic_objective=False,
                )

            asked = study.ask({"lr": distribution})
            candidate = float(asked.params["lr"])

            # Defensive validation
            if not math.isfinite(candidate) or candidate <= 0:
                print(f"[bo] attempt {attempt+1}: rejected non-finite {candidate}", flush=True)
                continue

            candidate = max(allowed_lower, min(allowed_upper, candidate))

            if not _is_duplicate_log10(candidate, observed_lrs, dup_delta):
                suggested = candidate
                if attempt > 0:
                    print(
                        f"[bo] attempt {attempt+1}/{resample_attempts}: GP "
                        f"escaped duplicate region → {candidate:.4e}",
                        flush=True,
                    )
                break

            print(
                f"[bo] attempt {attempt+1}/{resample_attempts}: GP suggested "
                f"{candidate:.4e} duplicate (within Δlog10={dup_delta}); resampling",
                flush=True,
            )

        # Sobol gap fallback — guarantee diversity by construction
        if suggested is None:
            suggested = _largest_log_gap_midpoint(observed_lrs, allowed_lower, allowed_upper)
            print(
                f"[bo] all GP attempts duplicate → Sobol gap fallback {suggested:.4e} "
                f"(midpoint of largest unexplored log-gap)",
                flush=True,
            )

        # Final clamp
        suggested = max(allowed_lower, min(allowed_upper, suggested))

        print(
            f"[bo] suggestion: {suggested:.4e} "
            f"(obs={len(valid)}, n_startup={n_startup}, seed={jittered_seed}, "
            f"range=[{allowed_lower:.2e}, {allowed_upper:.2e}])",
            flush=True,
        )
        return suggested

    except Exception as exc:
        print(f"[bo] GP suggest failed: {type(exc).__name__}: {exc}", flush=True)
        return None
