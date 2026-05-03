import math

def _suggest_learning_rates(
    best_lr: float,
    n: int,
    log_range: float = 0.4
) -> list[float]:
    if n < 0:
        raise ValueError("Number of tries (n) cannot be negative.")
    if n == 0:
        return []
    if n == 1:
        return [best_lr]

    # print("best_lr: ", best_lr)
    # Calculate the lower and upper bounds for the learning rate search
    # on a logarithmic scale.
    lower_bound = best_lr / (10 ** log_range)
    upper_bound = best_lr * (10 ** log_range)

    # Convert bounds to log scale
    log_lower = math.log10(lower_bound)
    log_upper = math.log10(upper_bound)

    # Generate n logarithmically spaced values
    log_spaced_values = [
        log_lower + i * (log_upper - log_lower) / (n - 1)
        for i in range(n)
    ]

    # Convert the log-spaced values back to the original scale
    learning_rates = [10 ** val for val in log_spaced_values]

    return sorted(learning_rates)


def suggest_learning_rates(
    best_lr: float,
    n: int,
    log_range: float = 0.2
) -> list[float]:
    lrs = _suggest_learning_rates(best_lr, n, log_range)
    if n % 2 == 1:
        return lrs
    else: # exclude one and add best_lr to the middle
        lrs = lrs[1:] + [best_lr]
        lrs = sorted(lrs)
        return lrs


def extend_learning_rates(
    lr: float,
    n: int,
    log_range: float = 0.2
) -> list[float]:
    lrs = _suggest_learning_rates(lr, n, log_range)
    # loop over lrs to find the item that is the closest to lr (should be the same) and replace it with lr and move that item to the left (index = 0)
    # Find the index of the learning rate in lrs that is closest to lr
    closest_idx = min(range(len(lrs)), key=lambda i: abs(lrs[i] - lr))
    # Replace that value with the actual lr to ensure precision
    lrs[closest_idx] = lr
    # Move that lr to the first position (index 0)
    if closest_idx != 0:
        lrs.insert(0, lrs.pop(closest_idx))
    return lrs


def lr_guardrail_interpolate(
    candidate_lr: float,
    tested_lrs: list[float],
    best_lr: float,
    second_best_lr: float = None,
    tolerance: float = 0.05,
) -> float:
    """LR Guardrail (Plan D 2026-05-03): avoid duplicate LR sweeps.

    Pulled from hyper-text winner log:
      [LR Guardrail] duplicate LR 1.4281e-04 already tested
                     - interpolating to 1.3402e-04
                     (midpoint of best 1.4651e-04 and #2 1.2153e-04)

    If `candidate_lr` is within `tolerance` (relative) of any `tested_lrs`,
    interpolate to midpoint of best + 2nd-best (in log space) instead.
    """
    if not tested_lrs:
        return candidate_lr
    # Check duplicate (relative tolerance in log space)
    log_cand = math.log10(candidate_lr) if candidate_lr > 0 else -10
    for tested in tested_lrs:
        if tested <= 0:
            continue
        log_tested = math.log10(tested)
        if abs(log_cand - log_tested) < tolerance:
            # Duplicate detected — interpolate
            if second_best_lr is None or second_best_lr <= 0:
                # No 2nd-best: nudge by tolerance
                return candidate_lr * (10 ** tolerance)
            log_best = math.log10(best_lr) if best_lr > 0 else log_cand
            log_2nd = math.log10(second_best_lr)
            interpolated = 10 ** ((log_best + log_2nd) / 2)
            return interpolated
    return candidate_lr


def test():
    lr = 0.00014523947500000002
    for n in [3,4,5, 6]:
        lrs = extend_learning_rates(lr, n)
        print(lrs)
        assert lrs[0] == lr

if __name__ == "__main__":
    test()