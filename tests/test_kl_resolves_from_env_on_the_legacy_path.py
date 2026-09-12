"""KL must not vanish when the request was built by the legacy config path.

Only adaptive_config writes `use_kl` / `kl_coef` into train_request. When adaptive
crashes or fails its sanity check, text_trainer falls back to the legacy builders,
whose request carries neither key. train_instruct read that absence as "KL off":
plain cross-entropy, and checkpoint selection on the unweighted eval_loss, on a task
the validator scores WITH KL. The container environment still says USE_KL=1 on that
path — the reader for it (kl_objective.read_kl_config) existed and was not called.

Found by the CPU preflight on 2026-09-13 (class 3, computed value never reaches the
trainer). Frequency conditional on the legacy cascade being taken.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from kl_objective import KL_COEF_FALLBACK, resolve_kl_for_request  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_a_request_that_carries_the_flag_wins_over_the_environment():
    req = {"use_kl": True, "kl_coef": 0.7, "kl_reason": "adaptive"}
    use, coef, reason, source = resolve_kl_for_request(req, env={"USE_KL": "0"})
    assert (use, coef, source) == (True, 0.7, "request")


def test_a_request_that_says_off_stays_off_even_if_env_says_on():
    req = {"use_kl": False, "kl_coef": None}
    use, coef, _, source = resolve_kl_for_request(req, env={"USE_KL": "1", "KL_COEF": "0.9"})
    assert use is False and source == "request"


def test_a_legacy_request_without_the_key_reads_the_environment():
    """The defect: this used to resolve to (False, None)."""
    use, coef, reason, source = resolve_kl_for_request({"model_name": "x"}, env={"USE_KL": "1", "KL_COEF": "0.9"})
    assert use is True and coef == 0.9
    assert "legacy" in source


def test_legacy_with_use_kl_but_no_coef_assumes_the_midpoint_loudly():
    use, coef, reason, _ = resolve_kl_for_request({}, env={"USE_KL": "1"})
    assert use is True and coef == KL_COEF_FALLBACK
    assert "assuming midpoint" in reason


def test_legacy_without_the_env_flag_is_off():
    use, coef, _, _ = resolve_kl_for_request({}, env={})
    assert use is False and coef is None


def test_train_instruct_uses_the_resolver():
    """The wire: the helper exists AND the trainer reads through it, not the dict."""
    src = open(os.path.join(ROOT, "scripts", "train_instruct.py"), encoding="utf-8").read()
    assert "resolve_kl_for_request(train_request)" in src
    assert '_use_kl = bool(train_request.get("use_kl"))' not in src, "train_instruct still reads use_kl straight off the request"
