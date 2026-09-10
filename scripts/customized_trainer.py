from transformers import GenerationConfig
import datetime
from datetime import timezone
from transformers import (
    TrainerCallback,
    TrainerState,
    TrainerControl,
)
import os
from typing import Callable, Optional, Dict
import shutil
import json
from transformers.trainer_utils import is_main_process
import wandb
import torch
from state_manager import get_state, set_state
# Capped from 9 on 2026-08-19. Each try relaunches train_instruct.py as a fresh OS
# process and pays model load + dataset load + packing again, for 80 steps that are
# thrown away (save_strategy=no). On a 2-4h budget nine of those is 25-60 minutes of
# training time spent on cold starts. Three still explores; the rest was waste.
MAX_TRIES = 3


MIS_MATCH_VOCAB_SIZE_MODELS = [
    'NousResearch/Nous-Capybara-7B-V1',
    'berkeley-nest/Starling-LM-7B-alpha',
    'NousResearch/Hermes-2-Theta-Llama-3-8B',
    'MNC-Jihun/Mistral-7B-AO-u0.5-b2-ver0.4'
]

ERROR_GENERATION_CONFIG_MODELS = [
    "lmsys/vicuna-7b-v1.5", 
    "lmsys/vicuna-13b-v1.5",
    "NousResearch/Nous-Hermes-llama-2-7b", 
    "defog/llama-3-sqlcoder-8b"
]

try:
    # Module scope: a raise here fails the import, so the trainer subprocess dies
    # before a step runs and the log carries an ImportError rather than a cause.
    # torchrun normally sets an integer, but a launcher that sets the variable to an
    # EMPTY string gets "" back from getenv — not the default — and int("") raises.
    LOCAL_RANK = int(os.getenv("LOCAL_RANK") or 0)
except (TypeError, ValueError):
    print(f"[rank] LOCAL_RANK={os.getenv('LOCAL_RANK')!r} is not a rank — using 0", flush=True)
    LOCAL_RANK = 0

print(f"LOCAL_RANK: {LOCAL_RANK} in customized_trainer.py", flush=True)
    
STATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def parse_state_timestamp(value):
    """A datetime from a state timestamp, or None when it is absent or malformed.

    Same reason min_prior_run_loss exists: this is read inside on_step_end, which runs
    every step and is not wrapped by transformers, so a raise here ends the run rather
    than degrading it. get_state() returns {} on a missing redis key or JSON that will
    not parse, which made `my_state["train"]["start_time"]` a KeyError, and a truncated
    or half-written value made strptime a ValueError.

    None rather than a fabricated default on purpose. These two stamps drive the
    remaining-time estimate that decides how many more runs fit; inventing one would
    produce a confident wrong estimate, which is worse than declining to estimate.
    """
    if not isinstance(value, str):
        return None
    try:
        return datetime.datetime.strptime(value, STATE_TIME_FORMAT)
    except (TypeError, ValueError):
        return None


def min_prior_run_loss(runs) -> float:
    """Lowest current_loss among prior runs, or +inf when there is no usable history.

    Pulled out of on_step_end so it can be tested at all: the callback needs torch,
    transformers and a live TrainerState, and the defect here was never in the
    comparison — it was that the expression could raise inside a hook that runs every
    step and is not wrapped by transformers, ending the run instead of degrading it.

    Three ways the old `min([run["current_loss"] for run in my_state["runs"]])` raised:
    KeyError when state_manager.get_state() returned {} (a missing redis key, or JSON
    that will not parse), KeyError on a run dict written before its loss was known, and
    ValueError from min() over an empty list.

    +inf for "no history" is not a sentinel bolted on: with nothing to compare against,
    the current run IS the best so far, which is the same conclusion the loop reaches
    from a single-entry history.
    """
    if not isinstance(runs, (list, tuple)):
        return float("inf")
    losses = [
        r["current_loss"] for r in runs
        if isinstance(r, dict)
        and isinstance(r.get("current_loss"), (int, float))
        and not isinstance(r.get("current_loss"), bool)
    ]
    return min(losses) if losses else float("inf")


class CustomEvalSaveCallback(TrainerCallback):
    def __init__(
        self,
        function_when_to_evaluate: Callable,
        submission_dir: str,
        output_dir: str,
        original_model_name: str,
        max_steps: int = -1,
        checking_step: int = 100,
        total_steps_all_epochs: int = -1,
        end_time: str = "",
        checking_mode: str = "none",
        probe_eval_fn: Callable = None,
    ):
        # probe_eval_fn: optional () -> float returning held-out loss. When set,
        # LR-probe runs are scored on it instead of the training loss. See
        # _probe_loss() for why that distinction decides DPO runs.
        self.probe_eval_fn = probe_eval_fn
        # Optional () -> float returning held-out loss for the CURRENT contents of
        # submission_dir. Gates the WSM merge: without it the merge is written
        # unverified, with it a merge that does not beat the best single
        # checkpoint is rolled back. Wired by the train_*.py entry points.
        self.merge_eval_fn = None
        # KL-flagged instruct tasks only. kl_coef is the validator's coefficient;
        # kl_metric_fn is a () -> float returning KL(finetuned || base) on the dev
        # set for the current model. Both unset means checkpoint ranking is plain
        # eval loss, i.e. unchanged. Wired by train_instruct.py.
        self.kl_coef = None
        self.kl_metric_fn = None
        # Optional () -> list[float] returning one token-averaged loss per dev
        # example, in scored order. Purely observational: it is written to
        # telemetry and nothing reads it back. Wired by the train_*.py entry
        # points; unset means no per-example record for this run.
        self.per_example_eval_fn = None

        # BUGFIX 2026-08-10, found on the first real GPU run. The best-checkpoint
        # gate in on_save reads self._h3_last_proxy, but only the GRPO subclass
        # ever assigned it — so on instruct and DPO the first save raised
        # AttributeError and killed the run. The gate's own comment says
        # "_h3_last_proxy=None (non-GRPO / no proxy yet) -> always save (legacy)",
        # i.e. None was the intended non-GRPO value; it was simply never set on
        # the base class. Initialising both here restores that intent and leaves
        # the GRPO path unchanged (it overwrites them as before).
        self._h3_last_proxy: Optional[float] = None
        self._submission_proxy: Optional[float] = None
        self.function_when_to_evaluate = function_when_to_evaluate
        self.submission_dir = submission_dir
        self.current_best_loss = None
        self.best_checkpoint_info = None
        self.update_best_checkpoint = False
        self.output_dir = output_dir
        self.original_model_name = original_model_name
        self.max_steps = max_steps
        self.has_checkpoint = False
        self.save_only = False
        self.checking_step = checking_step
        self.total_steps_all_epochs = total_steps_all_epochs
        self.checking_mode = checking_mode
        self.end_time = end_time
        # Phase 1 BUGFIX 2026-05-02: early-stop on plateau/regression.
        # Phase D refinement 2026-05-03: window-smoothed + adaptive patience.
        #
        # Bug found via 0304997e Qwen2-7B CodeM (+31.6% loss vs winner BOSS):
        # winner's eval was non-monotonic: 0.1624 → 0.1664 (rise) → 0.1580 (BEST
        # at epoch 1.99) → 0.1748 (overfit). Our patience=2 stopped at the rise
        # and missed the late-epoch dip. Static patience can't handle cosine
        # schedule late drops.
        #
        # Idea 1 (window smoothing): compare moving-avg of last N evals to
        #   prev-N avg. Stop only when SMOOTHED trend is rising.
        #   Source: Prechelt 1998 "Early stopping — but when?"
        # Idea 2 (adaptive patience): patience scales with planned epochs.
        #   patience = max(2, int(epoch_num * 0.4)) — short runs aggressive,
        #   long runs patient. Counters cosine_with_min_lr late dip.
        #
        # Combined: stop only when (no_improve_count >= patience) AND
        # (smoothed last window worse than prev window). This handles
        # non-monotonic trajectories without missing late minima.
        #
        # Env overrides:
        # - INSTRUCT_EARLY_STOP_PATIENCE: hard patience override (default auto)
        # - INSTRUCT_EARLY_STOP_WINDOW: smoothing window size (default 3)
        # - INSTRUCT_EARLY_STOP_MIN_DELTA: minimum improvement to reset count
        # - INSTRUCT_EARLY_STOP_DISABLE=1: disable entirely
        self.early_stop_disabled = os.getenv("INSTRUCT_EARLY_STOP_DISABLE", "0") == "1"
        # Adaptive patience: derive from total_steps_all_epochs (proxy for epoch_num).
        # Each "epoch" boundary creates one eval (save_strategy=epoch). Patience
        # = max(2, int(epochs * 0.4)) — see Idea 2 in plan.
        # If total_steps_all_epochs unknown, fall back to 2.
        steps_per_epoch_hint = max(1, total_steps_all_epochs // max(1, total_steps_all_epochs // 100))
        derived_epochs = max(1, total_steps_all_epochs // max(1, steps_per_epoch_hint)) if total_steps_all_epochs > 0 else 2
        # Simpler: total_steps_all_epochs / checking_step (approximate)
        if total_steps_all_epochs > 0 and checking_step > 0:
            derived_epochs = max(2, int(total_steps_all_epochs / max(60, checking_step / 0.5)))
        adaptive_patience = max(2, int(derived_epochs * 0.4))
        env_patience = os.getenv("INSTRUCT_EARLY_STOP_PATIENCE")
        self.early_stop_patience = int(env_patience) if env_patience else adaptive_patience
        self.early_stop_window = int(os.getenv("INSTRUCT_EARLY_STOP_WINDOW", "3"))
        self.early_stop_min_delta = float(os.getenv("INSTRUCT_EARLY_STOP_MIN_DELTA", "0.0"))
        self.no_improve_count = 0
        # Track all eval_losses for window smoothing
        self.eval_history: list[float] = []
        # Phase D-v2 (2026-05-03): CV-aware convergence detector
        # Source: arxiv 2502.00089 (ICLR 2025 "Provably tuned LR schedules")
        # Track training_loss CV (std/mean) over rolling window. If CV below
        # threshold (loss has converged numerically) AND no_improve >= K → stop.
        # If CV still high (loss actively descending), keep training even if
        # eval bumps up — late-dip recovery likely.
        #
        # Replaces fixed patience for tasks where eval is non-monotonic but
        # train is still descending (Qwen 7B CodeM signature pattern).
        # Default OFF (env-flag gated). Use INSTRUCT_USE_CV_EARLY_STOP=1.
        self.cv_early_stop_enabled = os.getenv("INSTRUCT_USE_CV_EARLY_STOP", "0") == "1"
        self.cv_window = int(os.getenv("INSTRUCT_CV_WINDOW", "20"))
        # CV threshold: code/reasoning typically 0.05, memorization 0.02
        self.cv_threshold = float(os.getenv("INSTRUCT_CV_THRESHOLD", "0.05"))
        self.train_loss_history: list[float] = []

        # ── Live Divergence Detection (lotob-grpo-hard 2026-05-07) ──
        # Catches catastrophic LR-too-high divergence. When train_loss exceeds
        # threshold × init_loss after warmup, force eval+save+stop to capture
        # the pre-divergence checkpoint. Active for Instruct/DPO; GRPO subclass
        # disables (Hook 3 reward-proxy plateau already covers GRPO).
        # Active in FINAL RUN ONLY (checking_mode=="none") to avoid stalling
        # the orchestrator state machine during exploration probes.
        self._divergence_enabled = (
            os.environ.get("TRAINING_DIVERGENCE_DETECT", "1") == "1"
        )
        try:
            self._divergence_threshold = float(
                os.environ.get("TRAINING_DIVERGENCE_THRESHOLD", "3.0")
            )
        except (TypeError, ValueError):
            self._divergence_threshold = 3.0
        try:
            self._divergence_min_step = int(
                os.environ.get("TRAINING_DIVERGENCE_MIN_STEP", "50")
            )
        except (TypeError, ValueError):
            self._divergence_min_step = 50
        self._divergence_init_loss: Optional[float] = None
        self._divergence_fired: bool = False

        # ── Cross-instance best_ckpt persistence (lotob-grpo-hard) ──
        # Each trainer subprocess (probe Run N → final run) starts with
        # best_checkpoint_info=None. Without persistence, final run can push
        # a WORSE ckpt than what an earlier run produced. Read state_manager
        # global_best_checkpoint on init; comparison at on_evaluate then
        # operates against global best across all subprocess instances.
        # Disabled via env TRAINING_BEST_CKPT_PERSIST=0.
        if os.environ.get("TRAINING_BEST_CKPT_PERSIST", "1") == "1":
            try:
                _state = get_state() or {}
                _persisted = _state.get("global_best_checkpoint")
                if (isinstance(_persisted, dict)
                        and "loss" in _persisted and "step" in _persisted):
                    self.best_checkpoint_info = {
                        "step": int(_persisted["step"]),
                        "loss": float(_persisted["loss"]),
                    }
                    self.current_best_loss = float(_persisted["loss"])
                    print(
                        f"[best_ckpt persist] restored from state: "
                        f"step={self.best_checkpoint_info['step']}, "
                        f"loss={self.best_checkpoint_info['loss']:.6e}",
                        flush=True,
                    )
            except Exception as _exc:
                print(
                    f"[best_ckpt persist] restore skipped: {_exc}",
                    flush=True,
                )

        if not self.early_stop_disabled:
            print(
                f"[early_stop] dynamic config: patience={self.early_stop_patience} "
                f"(adaptive from total_steps={total_steps_all_epochs}, derived_epochs={derived_epochs}), "
                f"window={self.early_stop_window}, min_delta={self.early_stop_min_delta}, "
                f"cv_enabled={self.cv_early_stop_enabled} cv_window={self.cv_window} cv_thresh={self.cv_threshold}",
                flush=True,
            )

        # ── WSM (Weight-Space Merging) — top-K ckpt averaging ──
        # Research: LCSC (arxiv 2403.04694) / WSM (arxiv 2507.17634) / Khalifa.
        # Linear-average top-K best LoRA adapters at end of training. Empirical:
        # 0.5-2% SFT eval improvement via ensemble smoothing. Risk: catastrophic
        # if loss spread tight (equal weights work better than loss-weighted
        # per WSM paper finding).
        # LoRA-only currently (full-FT averaging requires per-shard handling
        # for 7B+ models, disabled to avoid OOM + disk cost 3× model size).
        # Disabled in GRPO subclass (mode collapse risk per LCSC paper §3.2).
        # Only fires in FINAL run (checking_mode="none") to avoid interference
        # with state machine probe runs.
        # Env: TRAINING_WSM_ENABLED (default 1), TRAINING_WSM_TOP_K (default 3).
        self._wsm_enabled = (
            os.environ.get("TRAINING_WSM_ENABLED", "1") == "1"
        )
        try:
            self._wsm_top_k = int(os.environ.get("TRAINING_WSM_TOP_K", "3"))
        except (TypeError, ValueError):
            self._wsm_top_k = 3
        self._wsm_pool: list = []   # list of {loss, step, path}, sorted ascending by loss
        # Track every eval (not just NEW BEST) — top-K filter handles spikes.
        # Stored by on_evaluate, consumed by on_save when save event step
        # matches the eval step (avoids stale data when save fires
        # asynchronously from eval).
        self._wsm_last_eval_loss: Optional[float] = None
        self._wsm_last_eval_step: int = -1

    def compute_loss(self, state: TrainerState, metrics):
        """Metric this callback ranks checkpoints by.

        Normally the held-out eval loss. On a KL-flagged instruct task the
        validator ranks on `eval_loss + kl_coef * KL(finetuned || base)`, so we
        rank the same way — otherwise we would train the weighted objective and
        then pick the checkpoint that happens to look best on the unweighted one.

        The KL for a given eval is supplied by the trainer through
        `kl_metric_fn`; without it we fall back to plain eval loss, which is
        exactly today's behaviour.
        """
        eval_loss = metrics.get("eval_loss", None)
        if eval_loss is None or not self.kl_coef or self.kl_metric_fn is None:
            return eval_loss
        try:
            kl = float(self.kl_metric_fn())
            if kl != kl:  # NaN
                raise ValueError("KL metric is NaN")
            weighted = float(eval_loss) + self.kl_coef * kl
            print(
                f"[kl] checkpoint metric: {eval_loss:.6f} + {self.kl_coef} * {kl:.6f} "
                f"= {weighted:.6f}",
                flush=True,
            )
            return weighted
        except Exception as exc:
            # Never hand back a plain eval_loss here. The weighted metric runs
            # ~1.4x higher than the unweighted one, so a checkpoint whose KL
            # measurement failed would beat every checkpoint whose KL succeeded,
            # and selection would be decided by memory pressure rather than by
            # the model. Retry once with the cache dropped — the failure is
            # nearly always transient OOM — and if it still fails, rank the
            # checkpoint last. Discarding one checkpoint is a small loss;
            # letting it win every comparison corrupts the whole run.
            print(f"[kl] checkpoint metric failed ({exc}) — retrying with cache cleared", flush=True)
            try:
                import torch

                torch.cuda.empty_cache()
                kl = float(self.kl_metric_fn())
                if kl != kl:
                    raise ValueError("KL metric is NaN")
                weighted = float(eval_loss) + self.kl_coef * kl
                print(f"[kl] checkpoint metric (retry): {weighted:.6f}", flush=True)
                return weighted
            except Exception as exc2:
                print(
                    f"[kl] checkpoint metric unavailable after retry ({exc2}) — "
                    f"ranking this checkpoint last rather than on an incomparable number",
                    flush=True,
                )
                return float("inf")

    def _probe_loss(self, state: TrainerState) -> float:
        """Score for the current LR-probe run.

        Uses held-out loss when probe_eval_fn is wired, otherwise the last
        training loss (previous behaviour).

        Why this matters, for DPO especially: the multi-run LR sweep picks the
        run with the lowest score. DPO has a degenerate minimiser — an LR that is
        too high collapses the policy's log-probs, which inflates the
        chosen-minus-rejected margin and drives *training* loss down while the
        model itself degrades. Selecting on training loss therefore actively
        prefers the most destructive LR. The validator scores DPO on held-out
        loss (validator/evaluation/evaluators/dpo.py, BETA_DPO=0.1), so scoring
        probes the same way aligns selection with what we are actually ranked on.

        Fail-open: any error falls back to the training loss so a probe run is
        never lost to an eval failure.
        """
        train_loss = None
        try:
            train_loss = state.log_history[-1]["loss"]
        except Exception:
            pass

        if self.probe_eval_fn is None:
            return train_loss

        try:
            eval_loss = float(self.probe_eval_fn())
            if eval_loss != eval_loss:  # NaN
                raise ValueError("probe eval returned NaN")
            print(
                f"[probe] scoring on held-out loss={eval_loss:.6f} "
                f"(train loss was {train_loss})",
                flush=True,
            )
            return eval_loss
        except Exception as exc:
            print(
                f"[probe] held-out eval failed ({exc}); falling back to train loss {train_loss}",
                flush=True,
            )
            return train_loss

    def on_step_end(self, args, state: TrainerState, control: TrainerControl, **kwargs):
        # Custom logic to decide whether to save or evaluate
        # print(f"************* on_step_end: {state.global_step}, check eval", flush=True)
        # TODO: implement the logic to save the model without evaluating if there is no check points --> avoid evaluating takes too much time
        # Check if the checking_step is reached
        # print(f"Checking the model at step: {state.global_step}, checking_step: {self.checking_step}, checking_mode: {self.checking_mode}", flush=True)
        if state.global_step == self.checking_step and self.checking_mode == "first_time":
            # print(f"Checking the model at step: {state.global_step}", flush=True)
            # check the time so far to estimate the training time in total 
            my_state = get_state()
            # The second_time branch below was hardened against a lost state; this
            # branch carried the identical exposure and was left behind. Both stamps
            # are read straight out of get_state(), which returns {} when the redis
            # key is gone or its JSON will not parse.
            _train_state = my_state.get("train") or {}
            start_time_obj = parse_state_timestamp(_train_state.get("start_time"))
            start_train_time_obj = parse_state_timestamp(_train_state.get("start_train_time"))
            if start_time_obj is None or start_train_time_obj is None:
                # Without both stamps there is no remaining-time estimate to make, so
                # skip the probe and let training run to its normal end. That loses the
                # ladder for this task; raising would have lost the checkpoint entirely.
                print(
                    "[on_step_end] training state has no usable start timestamps "
                    "(state lost or unparseable) — skipping the time estimate, "
                    "training continues",
                    flush=True,
                )
                return control
            
            log_content = f"Checking the model at step: {state.global_step}"
            now = datetime.datetime.now()
            preparation_time = (start_train_time_obj - start_time_obj).total_seconds()
            log_content += f"\nPreparation time: {preparation_time}"
            time_so_far = (now - start_time_obj).total_seconds()
            log_content += f"\nTime so far: {time_so_far}"
            time_for_one_step = (now - start_train_time_obj).total_seconds() / self.checking_step
            log_content += f"\nTime for one step: {time_for_one_step}"
            # Now estimate the total training time for this training
            log_content += f"\nTotal steps all epochs: {self.total_steps_all_epochs}"
            total_remaining_training_time = time_for_one_step * (self.total_steps_all_epochs - state.global_step)
            log_content += f"\nTotal remaining training time: {total_remaining_training_time}"
            # n * time_so_far + total_remaining_training_time = total_remaining_time
            end_time_obj = datetime.datetime.strptime(self.end_time, "%Y-%m-%d %H:%M:%S")
            total_remaining_time = (end_time_obj - now).total_seconds()
            log_content += f"\nTotal remaining time: {total_remaining_time}"
            
            # n * time_so_far + (time_so_far + total_remaining_training_time) = total_remaining_time
            # time_so_far + total_remaining_training_time is the time it takes to finish the training (need to estimate the eval time and save time, assuming this is 15 minutes)
            # assuming time_so_far is + 5 minutes, just in case the checking step takes more time than expected
            max_var_time_sofar = 3 * 60
            n = (total_remaining_time - (time_so_far + total_remaining_training_time + 12 * 60)) / (time_so_far + max_var_time_sofar) # 300 = 5 minutes, assume that it extra time would be more or less 5 minutes
            n = int(n)
            my_state["check_details"] = {
                "now": str(now.strftime("%Y-%m-%d %H:%M:%S")),
                "start_time": str(start_time_obj.strftime("%Y-%m-%d %H:%M:%S")),
                "start_train_time": str(start_train_time_obj.strftime("%Y-%m-%d %H:%M:%S")),
                "checking_step": self.checking_step,
                "checking_mode": self.checking_mode,
                "estimation_of_steps": n,
                "preparation_time": preparation_time,
                "time_so_far": time_so_far,
                "time_for_one_step": time_for_one_step,
                "total_remaining_training_time": total_remaining_training_time,
                "total_remaining_time": total_remaining_time,
                "end_time": self.end_time,
            }
            if n > 0: # we should try more 
                log_content += f"\nEstimated number of steps to complete the training: {n}"
                control.should_training_stop = True
                control.should_save = False
                args.save_strategy = "no"
                # save the score of this probe run to the state; held-out loss when
                # probe_eval_fn is wired, otherwise the training loss (see _probe_loss)
                # Same lost-state exposure as the second_time branch below: a
                # bare double subscript is a KeyError on the {} get_state()
                # returns when the redis key is gone, inside a hook that runs
                # every step.
                my_state.setdefault("train", {})["current_loss"] = self._probe_loss(state)
                my_state["mode"] = "continue"
                if n > MAX_TRIES:
                    n = MAX_TRIES
                log_content += f"\nFinal number: {n + 1}"
                my_state["next_runs"] = n + 1 # including the current run
            else:
                print(f"Time is not enough so we will finish the training", flush=True)
                my_state["mode"] = "finish"
            
            if is_main_process(LOCAL_RANK):
                set_state(my_state)
                print(log_content, flush=True)            
            return control
    
        elif state.global_step == self.checking_step and self.checking_mode == "second_time": # at second time, we don't estimate the training time again, just save the current_loss
            log_content = f"Checking the model at step: {state.global_step} where check_mode=second_time"            
            my_state = get_state()
            current_loss = self._probe_loss(state)
            # get_state() returns {} when the redis key is gone or its JSON will
            # not parse, and "state lost mid-task" is a shape this repo has
            # already had to backstop elsewhere. Subscripting it here raises
            # KeyError inside on_step_end, which runs every step and is not
            # wrapped by transformers — so a lost key would end the run rather
            # than degrade it.
            my_state.setdefault("train", {})["current_loss"] = current_loss

            control.should_training_stop = True

            # Check if current_loss > current min_loss --> do not save to save time and space
            # 
            # if my_state["train"]["current_loss"] > current_min_loss:
            #     print(f"Current loss: {my_state['train']['current_loss']} is greater than the current min_loss: {current_min_loss}, do not save the checkpoint", flush=True)
            #     control.should_save = False
            # check if this is the last run and the current_loss is the lowest --> keep running the training
            current_is_the_best = False
            # min() over an empty list is a ValueError, and "runs" is absent
            # entirely on a lost state. Entries are filtered rather than trusted
            # because a half-written run dict has no current_loss yet. No prior
            # run means this one is the best so far, which is what an infinite
            # floor expresses — the same conclusion the loop would reach on a
            # single-entry history.
            _runs = my_state.get("runs") or []
            current_min_loss = min_prior_run_loss(_runs)
            if current_loss is not None and current_loss <= current_min_loss:
                if len(_runs) + 1 == my_state.get("next_runs"):
                    print(f"Current loss: {my_state['train']['current_loss']} is greater than: {current_min_loss}", flush=True)
                    current_is_the_best = True
                    
            if current_is_the_best:
                control.should_training_stop = False
                my_state["mode"] = "finish"
            else:
                control.should_save = False
                args.save_strategy = "no"
            
            if is_main_process(LOCAL_RANK):
                set_state(my_state)
                # print(log_content, flush=True)
        
            
        when_to_eval = self.function_when_to_evaluate(state.global_step)
        if when_to_eval["eval"]:
            print(f"Evaluating the model at step: {state.global_step} the reason: {when_to_eval['reason']}", flush=True)
            if getattr(self, "_grpo_no_eval", False):
                # GRPO STEP-500 RESHAPE FIX (2026-05-28): GRPO eval generation
                # crashes at trl/grpo_trainer.py:1199 — rewards.view(-1, num_generations)
                # fails when the dev-set generation yields rewards not divisible by
                # num_generations (size-1 batch). GRPO scoring uses reward-proxy from
                # TRAINING logs (Hook 3 on_log), NOT eval_loss — so the eval generation
                # is pure overhead AND a crash. Skip it: save-only for best-ckpt.
                # This is what crashed tournament GRPO at step 500 (validator 4h run).
                control.should_evaluate = False
                control.should_save = True
                self.save_only = True
                print(f"[GRPO] save-only (skip eval gen → avoids step-500 reshape crash) "
                      f"@ step {state.global_step}", flush=True)
            else:
                # do not allow the pod to be stopped by any reason
                # first check if there is at least one checkpoint or not
                control.should_evaluate = True
                control.should_save = True
                if when_to_eval["reason"] == "end_time":
                    if not self.has_checkpoint: # if there is no checkpoint, we just save the model, do not evaluate
                        print(f"No checkpoint found, just save the model at step: {state.global_step}", flush=True)
                        control.should_evaluate = False
                        self.save_only = True

            if when_to_eval["reason"] == "end_time":
                # BUGFIX 2026-08-10: actually stop at the deadline.
                #
                # This branch used to only eval and save. The handler's own
                # end_time check latches (`not self.run_eval`), so it fired
                # once and never again — training then ran on past the budget.
                # Observed on the first real GPU run: end_time 04:29, still
                # training at 05:13, 44 minutes over.
                #
                # That is not merely untidy. text_trainer's post-training
                # safety nets — the NaN/Inf scan of the final checkpoint and
                # restore_submission_architectures — only run after
                # trainer.train() RETURNS. A container killed by the validator
                # at hours_to_complete skips both, and the architectures
                # restore is what keeps the validator's is_finetune check from
                # failing the submission outright. So an overrun does not cost
                # a few ranks; it can cost the whole submission.
                #
                # Stopping here hands control back so those nets run, with the
                # eval and save above already done.
                print(
                    f"[deadline] stopping at step {state.global_step} — budget reached; "
                    f"handing back so the post-training checks can run",
                    flush=True,
                )
                control.should_training_stop = True

                # Ending the run is not enough: the OUTER loop in text_trainer keeps
                # relaunching until the shared state reaches "finish", and that
                # transition normally happens in the checking_mode branch above —
                # which only runs once global_step reaches checking_step. Stopping at
                # the deadline can preempt that, and then the subprocess exits
                # SUCCESSFULLY with the state still "initial", so text_trainer starts
                # another run, and another. Measured: 244 launches for one task and
                # 700 GB of per-attempt output dirs before the disk gave out.
                #
                # Before the deadline stop existed this could not happen — a run
                # always overran far enough to reach checking_step and set the state
                # itself. Fixing the overrun exposed the missing transition, so the
                # deadline has to make it. Same assignment and the same main-process
                # guard the `n <= 0` path above uses.
                if getattr(self, "checking_mode", "none") != "none":
                    try:
                        _st = get_state()
                        _st["mode"] = "finish"
                        if is_main_process(LOCAL_RANK):
                            set_state(_st)
                        print(
                            "[deadline] probe preempted by the budget — state set to "
                            "'finish' so the outer loop stops relaunching",
                            flush=True,
                        )
                    except Exception as _exc:
                        # Never let bookkeeping kill a run that is otherwise done; the
                        # hard cap in text_trainer is the backstop for this path.
                        print(f"[deadline] could not set finish state ({_exc})", flush=True)
        return control


    def on_log(self, args, state: TrainerState, control: TrainerControl, logs=None, **kwargs):
        # Phase D-v2: track training loss for CV convergence detector
        if logs and isinstance(logs, dict) and "loss" in logs:
            try:
                self.train_loss_history.append(float(logs["loss"]))
            except (TypeError, ValueError):
                pass

        # ── Live Divergence Detection (lotob-grpo-hard) ──
        # Catches catastrophic LR-too-high divergence. Active in final run
        # only (checking_mode=="none") to avoid stalling the orchestrator
        # state machine during exploration probes.
        if self._divergence_enabled and not self._divergence_fired \
                and self.checking_mode == "none" \
                and logs and isinstance(logs, dict):
            train_loss = logs.get("loss")
            if train_loss is not None:
                try:
                    train_loss_f = float(train_loss)
                    # Skip non-finite (NaN/Inf transients)
                    if train_loss_f == train_loss_f and train_loss_f != float("inf"):
                        if self._divergence_init_loss is None:
                            self._divergence_init_loss = train_loss_f
                            print(
                                f"[Divergence Detect] init_loss captured: "
                                f"{train_loss_f:.4f} @ step {state.global_step}, "
                                f"threshold={self._divergence_threshold}× = "
                                f"{train_loss_f * self._divergence_threshold:.4f}, "
                                f"min_step={self._divergence_min_step}",
                                flush=True,
                            )
                        elif state.global_step >= self._divergence_min_step:
                            threshold_value = (
                                self._divergence_init_loss * self._divergence_threshold
                            )
                            if train_loss_f > threshold_value:
                                self._divergence_fired = True
                                print(
                                    f"[Divergence Detect] DIVERGENCE @ step "
                                    f"{state.global_step}: train_loss="
                                    f"{train_loss_f:.4f} > "
                                    f"{self._divergence_threshold}× init_loss="
                                    f"{self._divergence_init_loss:.4f} "
                                    f"(threshold={threshold_value:.4f}). "
                                    f"Forcing eval+save+stop.",
                                    flush=True,
                                )
                                control.should_evaluate = True
                                control.should_save = True
                                control.should_training_stop = True
                except (TypeError, ValueError):
                    pass
        return control

    def on_evaluate(
        self, args, state: TrainerState, control: TrainerControl, metrics, **kwargs
    ):
        self.save_only = False
        eval_loss = self.compute_loss(state, metrics)
        if state.global_step < 2 or eval_loss is None:
            return
        print(f"GO INTO CUSTOMIZED EVALUATE AT STEP: {state.global_step}", flush=True)

        # Track for window smoothing
        self.eval_history.append(float(eval_loss))
        # WSM: record latest eval_loss+step pair so on_save can track ckpt to pool.
        # Tracked at EVERY eval (not just NEW BEST) — top-K filter rejects spikes.
        self._wsm_last_eval_loss = float(eval_loss)
        self._wsm_last_eval_step = int(state.global_step)

        improved = (
            self.best_checkpoint_info is None
            or eval_loss < self.best_checkpoint_info["loss"] - self.early_stop_min_delta
        )
        if improved:
            print(f"Updating the best checkpoint info at step: {state.global_step} with eval_loss: {eval_loss}", flush=True)
            self.best_checkpoint_info = {
                "loss": eval_loss,
                "step": state.global_step
            }
            self.update_best_checkpoint = True
            self.no_improve_count = 0
            # ── Cross-instance persist (lotob-grpo-hard) ──
            # Save new best to state_manager so subsequent subprocess
            # instances can compare against it (prevents worse final-run
            # ckpt from overwriting an earlier probe-run best).
            # DDP guard 2026-05-12: only rank-0 writes — multiple ranks
            # racing on shared Redis key produces inconsistent reads. Per
            # multi-GPU audit, this was MED severity (race window real).
            if os.environ.get("TRAINING_BEST_CKPT_PERSIST", "1") == "1" and is_main_process(LOCAL_RANK):
                try:
                    _state = get_state() or {}
                    _state["global_best_checkpoint"] = {
                        "loss": float(eval_loss),
                        "step": int(state.global_step),
                    }
                    set_state(_state)
                except Exception as _exc:
                    print(f"[best_ckpt persist] save skipped: {_exc}", flush=True)
        # Everything below the promotion is observational. It sits HERE, and not
        # where it used to sit — above the promotion — because on 2026-09-07 that
        # ordering cost us a checkpoint in a live tournament. Task 59469903
        # evaluated at step 500 (0.05278521) and again at step 544 (0.05173291),
        # the deadline eval. The step-500 promotion happened; the step-544 one
        # never did, because the container was killed inside the per-example pass
        # below, 242s into it. We shipped the worse of two checkpoints we had
        # already measured, and gave away 0.00105 nats against a 0.0072 gap to
        # rank 1 on that task.
        #
        # The rule this encodes: the one statement that decides which artefact we
        # ship must never sit downstream of work whose own comment says nothing
        # reads it. The boss does the same thing structurally — its on_evaluate
        # promotes with nothing at all between the metric and the promotion
        # (god-text-tourn-2ba0f79237bffcf7-20260907-position-1,
        # scripts/customized_trainer.py:249-267).
        #
        # Placed before the early-stop branch rather than at the end of the method
        # so that it still runs on every path: that branch returns early in several
        # places, and telemetry that only fires on improving evals would be a
        # biased sample of exactly the runs we want to study.
        # Label side of the estimator dataset: what this configuration scored.
        # Paired with the config record adaptive_config wrote before training.
        try:
            from telemetry import record_outcome

            record_outcome(
                eval_loss=float(eval_loss),
                step=int(state.global_step),
                learning_rate=(
                    float(state.log_history[-1].get("learning_rate"))
                    if state.log_history and state.log_history[-1].get("learning_rate") is not None
                    else None
                ),
                epoch=getattr(state, "epoch", None),
                output_dir=self.output_dir,
            )
        except Exception:
            pass

        # Record per-example eval losses. LOGGING ONLY — nothing below reads
        # this, and selection stays on the mean.
        #
        # The validator is moving knockout and boss rounds onto an example-by-
        # example comparison (PR #1345). We are not following yet: group rounds
        # are still mean-ranked, the PR is unmerged, and the selection stack it
        # would touch has not run on a GPU. But the vector is free to capture on
        # runs we are doing anyway, and having it lets us ask afterwards —
        # against real data — whether win-rate selection would ever have picked a
        # different checkpoint than the mean did. That measurement, not the PR,
        # is what should decide adoption.
        #
        # Costs one extra forward pass over the dev set per eval — measured at
        # 349.7s against 109.2s for the batched eval it duplicates. Default OFF as
        # of this change; set EMIT_PER_EXAMPLE_LOSSES=1 to capture it.
        try:
            from per_example_eval import (
                collect_per_example_losses,
                enabled,
                summarise,
                vector_fingerprint,
            )

            if enabled() and self.per_example_eval_fn is not None:
                vec = self.per_example_eval_fn()
                if vec:
                    stats = summarise(vec)
                    print(
                        f"[per-example] step={state.global_step} {stats} "
                        f"fp={vector_fingerprint(vec)}",
                        flush=True,
                    )
                    from telemetry import record

                    record(
                        "per_example_eval",
                        {
                            "step": int(state.global_step),
                            "eval_loss_reported": float(eval_loss),
                            "summary": stats,
                            "fingerprint": vector_fingerprint(vec),
                            "losses": vec,
                        },
                        output_dir=self.output_dir,
                    )
        except Exception as _exc:
            print(f"[per-example] skipped ({type(_exc).__name__}: {_exc})", flush=True)

        if not improved:
            self.no_improve_count += 1
            if self.best_checkpoint_info is not None:
                print(
                    f" At step: {state.global_step} eval_loss={eval_loss:.4f} not < best {self.best_checkpoint_info['loss']:.4f} "
                    f"no_improve={self.no_improve_count}/{self.early_stop_patience}",
                    flush=True,
                )

            # Phase D dynamic early-stop (2026-05-03):
            # Stop only when BOTH conditions:
            #   (1) consecutive_no_improve >= adaptive_patience
            #   (2) WINDOW-SMOOTHED trend is rising (last W avg > prev W avg)
            # This handles non-monotonic cosine schedules where eval temporarily
            # rises before dropping again at epoch boundaries.
            # Source: Prechelt 1998 "Early stopping — but when?" + cosine schedule
            # observation from 0304997e Qwen2-7B winner log (epoch 1→1.36 rises,
            # epoch 1.99 drops to BEST).
            if self.early_stop_disabled:
                return
            if self.early_stop_patience <= 0:
                return

            # Phase D-v2 (2026-05-03): CV-aware convergence override
            # Source: arxiv 2502.00089 (ICLR 2025)
            # If training_loss is still ACTIVELY DESCENDING (CV high), keep
            # training even if eval bumped up — late-dip recovery very likely.
            # Only kicks in when INSTRUCT_USE_CV_EARLY_STOP=1 (env-flag gated).
            if self.cv_early_stop_enabled and len(self.train_loss_history) >= self.cv_window:
                import statistics as _stats
                window_losses = self.train_loss_history[-self.cv_window:]
                mean = _stats.mean(window_losses)
                stdev = _stats.stdev(window_losses) if len(window_losses) > 1 else 0.0
                cv = stdev / max(abs(mean), 1e-9)
                if cv > self.cv_threshold:
                    # Loss still actively varying = still learning. Don't stop yet.
                    print(
                        f"[early_stop CV-override] step {state.global_step}: "
                        f"train_loss CV={cv:.3f} > {self.cv_threshold} → "
                        f"loss actively descending, IGNORE patience hit. "
                        f"Likely cosine-schedule late-dip incoming.",
                        flush=True,
                    )
                    return  # don't even check patience

            if self.no_improve_count < self.early_stop_patience:
                return  # not yet at patience limit

            # Apply window smoothing only if we have enough history
            W = self.early_stop_window
            if len(self.eval_history) < 2 * W:
                # Fall back to old patience-only logic (not enough data yet)
                print(
                    f"[early_stop] patience {self.early_stop_patience} exhausted at step "
                    f"{state.global_step} (history<{2*W}, fallback). Best ckpt step="
                    f"{self.best_checkpoint_info['step']} loss={self.best_checkpoint_info['loss']:.4f}",
                    flush=True,
                )
                control.should_training_stop = True
                return

            recent_avg = sum(self.eval_history[-W:]) / W
            prev_avg = sum(self.eval_history[-2*W:-W]) / W
            # Stop only if smoothed trend is RISING (recent worse than prev by min_delta+0.5%)
            rising = recent_avg > prev_avg * 1.005 + self.early_stop_min_delta
            if rising:
                print(
                    f"[early_stop] STOPPING at step {state.global_step}: "
                    f"patience {self.no_improve_count}/{self.early_stop_patience} + "
                    f"smoothed rising (recent_avg={recent_avg:.4f} > prev_avg={prev_avg:.4f}). "
                    f"Best ckpt step={self.best_checkpoint_info['step']} loss={self.best_checkpoint_info['loss']:.4f}",
                    flush=True,
                )
                control.should_training_stop = True
            else:
                print(
                    f"[early_stop] continue at step {state.global_step}: "
                    f"patience hit but smoothed FALLING/FLAT "
                    f"(recent_avg={recent_avg:.4f} <= prev_avg={prev_avg:.4f}*1.005). "
                    f"Late convergence dip likely (cosine schedule). no_improve reset.",
                    flush=True,
                )
                # Reset counter to allow further training (the smoothed trend is good)
                self.no_improve_count = 0




    def on_save(self, args, state: TrainerState, control: TrainerControl, **kwargs):
        
        if state.global_step == self.max_steps and self.max_steps != -1:
            print(f"Stop training because of max steps: {self.max_steps}", flush=True)
            control.should_training_stop = True
        
        self.has_checkpoint = True
        
        if not is_main_process(LOCAL_RANK): # if not main process, skip this
            return 
            
        if self.save_only: # if only save, do not evaluate 
            print(f"Only save the model at step: {state.global_step}, no evaluation", flush=True)
            current_step = state.global_step
            # ── BEST-CKPT GATE (2026-05-28) — GRPO peak-then-drift fix ──
            # Only update submission_dir if reward-proxy IMPROVED over what's
            # already there. Prevents overwriting the PEAK model with a later
            # drifted one (klstable3: peak ep0.18 reward-proxy, drift by ep0.40).
            # _h3_last_proxy=None (non-GRPO / no proxy yet) → always save (legacy).
            _cur = self._h3_last_proxy
            if _cur is not None:
                if self._submission_proxy is not None and _cur <= self._submission_proxy:
                    print(
                        f"[best-ckpt] step {current_step} proxy={_cur:.4f} <= "
                        f"submission best={self._submission_proxy:.4f} → KEEP prior "
                        f"peak, skip overwrite", flush=True,
                    )
                    self.update_best_checkpoint = False
                    self.save_only = False
                    return
                print(
                    f"[best-ckpt] step {current_step} proxy={_cur:.4f} is new best "
                    f"(prev={self._submission_proxy}) → update submission_dir", flush=True,
                )
                self._submission_proxy = _cur
            # Remove existing directory if it exists
            if os.path.exists(self.submission_dir):
                shutil.rmtree(self.submission_dir)

            shutil.copytree(
                os.path.join(self.output_dir, f"checkpoint-{current_step}"),
                self.submission_dir
            )
            self.update_best_checkpoint = False
            # add a loss.txt file to the submission directory
            with open(os.path.join(self.submission_dir, "loss.txt"), "w") as f:
                f.write(f"{current_step},proxy={_cur if _cur is not None else 'no_eval'}")
            
            # release the flag
            self.save_only = False
            return 
            
        # Custom logic after model is saved
        # You can trigger external services, logs, or backups here
        if (
            self.update_best_checkpoint
            and is_main_process(LOCAL_RANK)
        ):
            print(f"Copy the best checkpoint to the submission directory at step: {state.global_step}", flush=True)
            # Remove existing directory if it exists
            if os.path.exists(self.submission_dir):
                shutil.rmtree(self.submission_dir)
            best_eval_loss = self.best_checkpoint_info["loss"]
            shutil.copytree(
                os.path.join(self.output_dir, f"checkpoint-{self.best_checkpoint_info['step']}"),
                self.submission_dir
            )
            self.update_best_checkpoint = False
            # add a loss.txt file to the submission directory
            with open(os.path.join(self.submission_dir, "loss.txt"), "w") as f:
                f.write(f"{self.best_checkpoint_info['step']},{best_eval_loss}")

        # ── WSM: track current ckpt to pool (Option D — every eval, top-K filter) ──
        # Only track when save step matches latest eval step (avoids stale data
        # from saves not paired with eval). Active in FINAL run only.
        if (self._wsm_enabled
                and self.checking_mode == "none"
                and is_main_process(LOCAL_RANK)
                and self._wsm_last_eval_step == state.global_step
                and self._wsm_last_eval_loss is not None):
            try:
                self._wsm_track_ckpt(
                    state.global_step, self._wsm_last_eval_loss
                )
            except Exception as _exc:
                print(f"[WSM] track skipped: {_exc}", flush=True)

    # ── WSM (Weight-Space Merging) helper methods ──
    def _wsm_pool_dir(self) -> str:
        """Pool dir for top-K ckpt copies (sibling to submission_dir)."""
        return self.submission_dir.rstrip("/") + "_wsm_pool"

    def _wsm_track_ckpt(self, step: int, loss: float):
        """Copy ckpt-{step} to wsm_pool dir, maintain top-K sorted by loss."""
        src = os.path.join(self.output_dir, f"checkpoint-{step}")
        if not os.path.isdir(src):
            return

        # LoRA detection: only adapter files (adapter_model.{safetensors,bin}).
        # Full FT produces model.safetensors (single/sharded) — averaging
        # those requires per-shard handling not implemented (disk 3× cost,
        # OOM risk on 7B+). Disable WSM run-wide if full FT detected.
        is_lora = (
            os.path.isfile(os.path.join(src, "adapter_model.safetensors"))
            or os.path.isfile(os.path.join(src, "adapter_model.bin"))
        )
        if not is_lora:
            print(
                f"[WSM] full fine-tune detected at step {step} — disabling "
                f"WSM run-wide (LoRA-only; full FT averaging not implemented).",
                flush=True,
            )
            self._wsm_enabled = False
            for entry in self._wsm_pool:
                try:
                    if os.path.isdir(entry.get("path", "")):
                        shutil.rmtree(entry["path"])
                except Exception:
                    pass
            self._wsm_pool = []
            return

        pool_dir = self._wsm_pool_dir()
        os.makedirs(pool_dir, exist_ok=True)
        dst = os.path.join(pool_dir, f"step_{step}")

        # Skip if step already pooled
        if any(e["step"] == step for e in self._wsm_pool):
            return

        # Optimization: skip copy if pool full and new loss is worse than worst.
        if len(self._wsm_pool) >= self._wsm_top_k:
            worst_in_pool = self._wsm_pool[-1]["loss"]
            if float(loss) >= worst_in_pool:
                print(
                    f"[WSM] skip step {step} loss={float(loss):.6e} "
                    f">= worst-in-pool {worst_in_pool:.6e} (pool full)",
                    flush=True,
                )
                return

        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        self._wsm_pool.append({"loss": float(loss), "step": int(step), "path": dst})
        self._wsm_pool.sort(key=lambda e: e["loss"])
        while len(self._wsm_pool) > self._wsm_top_k:
            evicted = self._wsm_pool.pop()
            try:
                if os.path.isdir(evicted["path"]):
                    shutil.rmtree(evicted["path"])
            except Exception as _exc:
                print(f"[WSM] evict cleanup skipped: {_exc}", flush=True)

        kept_steps = [e["step"] for e in self._wsm_pool]
        kept_losses = [f"{e['loss']:.6e}" for e in self._wsm_pool]
        print(
            f"[WSM] pool now {len(self._wsm_pool)}/{self._wsm_top_k}: "
            f"steps={kept_steps} losses={kept_losses}",
            flush=True,
        )

    def _perform_wsm_merge(self):
        """Linear-average top-K LoRA adapter weights, write to submission_dir.

        Equal weights — paper finding: simpler than loss-weighted, more robust
        when loss spread is tight. Non-tensor files (adapter_config.json,
        tokenizer*) kept from existing submission_dir (best-only ckpt).
        """
        import torch
        pool = list(self._wsm_pool)
        if len(pool) < 2:
            print(f"[WSM] merge skipped: pool size {len(pool)} < 2", flush=True)
            return
        if not os.path.isdir(self.submission_dir):
            print(f"[WSM] merge skipped: submission_dir missing", flush=True)
            return
        # Require adapter_config.json in submission_dir (sanity check)
        if not os.path.isfile(os.path.join(self.submission_dir, "adapter_config.json")):
            print(
                f"[WSM] merge skipped: adapter_config.json missing in "
                f"submission_dir — keeping current best-only submission",
                flush=True,
            )
            return

        # Pick weight filename
        weight_filename = None
        for cand in ("adapter_model.safetensors", "adapter_model.bin"):
            if os.path.isfile(os.path.join(pool[0]["path"], cand)):
                weight_filename = cand
                break
        if weight_filename is None:
            print(f"[WSM] merge skipped: no adapter_model.* in pool[0]", flush=True)
            return

        # Load top-K state dicts
        state_dicts = []
        try:
            for entry in pool:
                wpath = os.path.join(entry["path"], weight_filename)
                if weight_filename.endswith(".safetensors"):
                    from safetensors.torch import load_file
                    sd = load_file(wpath)
                else:
                    sd = torch.load(wpath, map_location="cpu")
                state_dicts.append(sd)
        except Exception as exc:
            print(f"[WSM] load fail (keeping best-only): {exc}", flush=True)
            return

        # Average
        merged_sd = {}
        try:
            keys = list(state_dicts[0].keys())
            for key in keys:
                tensors = [sd[key].float() for sd in state_dicts if key in sd]
                if not tensors:
                    continue
                avg = sum(tensors) / len(tensors)
                # Cast back to original dtype
                merged_sd[key] = avg.to(state_dicts[0][key].dtype)
        except Exception as exc:
            print(f"[WSM] average fail (keeping best-only): {exc}", flush=True)
            return

        # Write merged adapter to submission_dir, overwriting the best-only adapter.
        #
        # ADMISSION TEST (2026-08-05). Averaging is not free: a merge of top-K
        # checkpoints can land WORSE than the single best one, and this function
        # overwrites the submission either way. That made souping a coin flip on
        # the one artefact we are scored on. Wortsman 2022 ("model soups") admits
        # a candidate only when it measurably improves held-out loss, which makes
        # the result never worse than the best single member.
        #
        # We take the cheap form of that guarantee: back up the best-only adapter,
        # write the merge, evaluate once, and roll back if it did not improve.
        # One extra evaluation instead of K, and the submission can only get
        # better.
        #
        # BUGFIX 2026-08-10: the gate never armed. It read `current_best_loss`,
        # which is only assigned when state is restored from Redis (a PREVIOUS
        # probe run's loss — the wrong baseline anyway) or after an earlier
        # accepted merge. The live best for this run is maintained by on_evaluate
        # in `best_checkpoint_info`. So on an ordinary run best_single was None,
        # the gate was off, the backup was skipped, and the merge overwrote the
        # scored artefact unverified with nothing to roll back to.
        dst_path = os.path.join(self.submission_dir, weight_filename)
        backup_path = dst_path + ".prewsm"

        best_single = None
        if self.best_checkpoint_info is not None:
            best_single = self.best_checkpoint_info.get("loss")
        if best_single is None:
            best_single = self.current_best_loss

        if self.merge_eval_fn is None or best_single is None:
            # No way to measure the merge. Writing it anyway is a coin flip on the
            # one file we are scored on, and the best-only checkpoint in place is
            # already measured, so leave it alone. Previously this branch wrote
            # the merge and printed "ACCEPTED unverified".
            print(
                f"[WSM] SKIPPED: nothing to verify the merge against "
                f"(merge_eval_fn={'wired' if self.merge_eval_fn else 'missing'}, "
                f"best_single={best_single}) — keeping the best-only submission",
                flush=True,
            )
            return

        try:
            shutil.copy2(dst_path, backup_path)
        except Exception as exc:
            print(f"[WSM] could not back up best-only adapter ({exc}) — skipping merge", flush=True)
            return

        try:
            if weight_filename.endswith(".safetensors"):
                from safetensors.torch import save_file
                save_file(merged_sd, dst_path)
            else:
                torch.save(merged_sd, dst_path)
            losses = [f"{e['loss']:.6e}" for e in pool]
            steps = [e["step"] for e in pool]
            print(
                f"[WSM] merged top-{len(pool)} adapters to {dst_path}: "
                f"steps={steps} losses={losses}",
                flush=True,
            )
        except Exception as exc:
            print(f"[WSM] save fail (keeping best-only): {exc}", flush=True)
            self._wsm_restore(backup_path, dst_path)
            return

        try:
            merged_loss = float(self.merge_eval_fn())
        except Exception as exc:
            print(f"[WSM] REJECTED: merged adapter failed to evaluate ({exc})", flush=True)
            self._wsm_restore(backup_path, dst_path)
            return

        if merged_loss != merged_loss:  # NaN
            print("[WSM] REJECTED: merged adapter evaluated to NaN", flush=True)
            self._wsm_restore(backup_path, dst_path)
            return

        if merged_loss < best_single:
            print(
                f"[WSM] ACCEPTED: merged {merged_loss:.6f} < best single "
                f"{best_single:.6f} (improvement {best_single - merged_loss:.6f})",
                flush=True,
            )
            self.current_best_loss = merged_loss
            try:
                os.remove(backup_path)
            except Exception:
                pass
        else:
            print(
                f"[WSM] REJECTED: merged {merged_loss:.6f} >= best single "
                f"{best_single:.6f} — restoring best-only submission",
                flush=True,
            )
            self._wsm_restore(backup_path, dst_path)

    def _wsm_restore(self, backup_path: str, dst_path: str) -> None:
        """Put the pre-merge adapter back. Best effort, loud on failure.

        A failure here is serious — it means the submission holds a merge we
        could not verify — so it is logged rather than swallowed.
        """
        try:
            if os.path.isfile(backup_path):
                shutil.move(backup_path, dst_path)
                print(f"[WSM] restored pre-merge adapter to {dst_path}", flush=True)
        except Exception as exc:
            print(f"[WSM] RESTORE FAILED ({exc}) — submission holds the merged adapter", flush=True)
            # The backup lives inside submission_dir, so a failed move leaves a stray
            # .prewsm beside the adapter and the uploader ships it. Two adapters in one
            # repository is not what a submission should look like, and the one that
            # gets served is not ours to choose. Removing it does not recover the
            # restore — the loud line above is still the finding — it only keeps the
            # failure from travelling.
            try:
                if os.path.isfile(backup_path):
                    os.remove(backup_path)
                    print(f"[WSM] removed the stray backup at {backup_path}", flush=True)
            except Exception as _exc:
                print(f"[WSM] could not remove the stray backup ({_exc})", flush=True)

    def on_train_end(self, args, state, control, **kwargs):
        """End of training — trigger WSM merge if eligible."""
        if (self._wsm_enabled
                and self.checking_mode == "none"
                and is_main_process(LOCAL_RANK)
                and len(self._wsm_pool) >= 2):
            print(f"[WSM] on_train_end: pool size={len(self._wsm_pool)}, performing merge", flush=True)
            try:
                self._perform_wsm_merge()
            except Exception as _exc:
                print(f"[WSM] merge error (keeping best-only): {_exc}", flush=True)
        elif self._wsm_enabled:
            print(
                f"[WSM] on_train_end: pool size {len(self._wsm_pool)} < 2 or "
                f"non-final run (checking_mode={self.checking_mode}), skip merge",
                flush=True,
            )


class GRPOCustomEvalSaveCallback(CustomEvalSaveCallback):
    """GRPO reward-plateau guard — preserves best ckpt before reward saturates.

    Mirrors the validator's eval_loss formula at training time:
      eval_loss = normalized_reward − BETA_GRPO × kl_divergence  (BETA_GRPO=0.5)
    so plateau detection on (reward − 0.5×kl) is a direct early-stop signal.

    Three independent fire mechanisms (all post-warmup, all fail-soft):
      A. Reward proxy plateau (PRIMARY, default ON):
         proxy = mean(reward) − 0.5 × mean(kl)  (mirror of validator formula)
         Fires when proxy fails to improve for `patience` steps.
      B. KL ceiling (mean-based, OPT-IN — default 0):
         Fires when mean(kl_window) > TRAINING_GRPO_KL_CEILING.
         Default disabled — wandb evidence (2c4ccac2-02, mean=0.7) shows
         degraded runs that never fire on threshold 8.0; mean-only smooths
         out transient spikes. Plateau already catches the reward symptom.
      C. KL peak detection (OPT-IN — default 0):
         Fires when max(window) > threshold AND violations >= max(2, len//8).
         Calibrated against noisy-KL traces (peak 52, mean 6.2, threshold 8
         + 2 violations) where mean stayed under ceiling but reward collapsed.

    Env knobs:
      TRAINING_GRPO_PLATEAU_ENABLED          (default 1)
      TRAINING_GRPO_PLATEAU_WINDOW_LOGS      (default 50)
      TRAINING_GRPO_PLATEAU_WARMUP_STEPS     (override scaling 10% total)
      TRAINING_GRPO_PLATEAU_PATIENCE_STEPS   (override scaling 15% post-warmup)
      TRAINING_GRPO_PLATEAU_SNAPSHOT_EVERY   (default 200, telemetry cadence)
      TRAINING_GRPO_KL_CEILING               (mean-based, default 0=disabled)
      TRAINING_GRPO_KL_PEAK_THRESHOLD        (peak-based, default 0=disabled)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Disable Live Divergence Detection for GRPO. GRPO loss is a surrogate
        # (mean(advantage * ratio)) — can be negative or oscillate, making
        # ratio-based divergence detection unreliable. Hook 3 reward-proxy
        # plateau already covers the GRPO failure mode.
        self._divergence_enabled = False
        # Disable WSM for GRPO. LCSC paper §3.2 notes mode collapse risk
        # when averaging RL policies (rewards may saturate at different
        # collapse modes — averaging amplifies the collapse).
        # Hook 3 reward-proxy plateau already preserves best ckpt.
        self._wsm_enabled = False
        from collections import deque
        try:
            _w = int(os.environ.get("TRAINING_GRPO_PLATEAU_WINDOW_LOGS", "50"))
        except (TypeError, ValueError):
            _w = 50
        self._h3_rewards = deque(maxlen=max(1, _w))
        self._h3_kls = deque(maxlen=max(1, _w))
        self._h3_best_proxy: Optional[float] = None
        self._h3_best_step: int = 0
        self._h3_fired: bool = False
        # BEST-CKPT capture (2026-05-28): GRPO peaks early then drifts (klstable3:
        # peak reward-proxy ep0.18 → drift by ep0.40). save_only path copies the
        # CURRENT ckpt each save → submission_dir ends as drifted final. Gate it:
        # only update submission_dir when reward-proxy IMPROVES → submission holds
        # the PEAK, not the drifted end. _h3_last_proxy = proxy at last on_log;
        # _submission_proxy = proxy of what's currently in submission_dir.
        self._h3_last_proxy: Optional[float] = None
        self._submission_proxy: Optional[float] = None
        # GRPO STEP-500 RESHAPE FIX: skip eval generation (crashes at TRL
        # grpo_trainer.py:1199). GRPO uses reward-proxy from training logs, not
        # eval_loss → eval gen is overhead + crash. on_step_end routes to save-only.
        self._grpo_no_eval = True
        # Telemetry state — emit config once, warmup-end once, periodic
        # snapshots, and best-proxy update events for post-hoc verification.
        self._h3_config_logged: bool = False
        self._h3_warmup_announced: bool = False
        self._h3_last_snapshot_step: int = 0
        try:
            self._h3_snapshot_every = int(
                os.environ.get("TRAINING_GRPO_PLATEAU_SNAPSHOT_EVERY", "200")
            )
        except (TypeError, ValueError):
            self._h3_snapshot_every = 200
        # Default 0 = disabled. wandb evidence (2c4ccac2-02 mean=0.7) shows
        # degraded runs that never fire on default 8.0 — mean-based misses
        # transient spikes. Plateau on reward proxy catches the symptom.
        try:
            self._h3_kl_ceiling = float(os.environ.get("TRAINING_GRPO_KL_CEILING", "0"))
        except (TypeError, ValueError):
            self._h3_kl_ceiling = 0.0
        # Peak-based detection — default 0 = disabled. Opt-in for noisy KL
        # tasks. Calibrated against 2c4ccac2-02 trace (peak 52, valley 3-4,
        # mean 6.2): threshold=8.0 + min_violations=2 → fires @ step 210.
        try:
            self._h3_kl_peak_threshold = float(
                os.environ.get("TRAINING_GRPO_KL_PEAK_THRESHOLD", "0")
            )
        except (TypeError, ValueError):
            self._h3_kl_peak_threshold = 0.0
        # ── KL GOVERNOR (2026-05-28) — PREVENTIVE LR throttle on KL drift ──
        # Empirical: Dr.GRPO scale_rewards=False drifted KL to 3.196 (reward -180,
        # divergence). This governor catches runaway drift DURING training by
        # throttling LR when rolling-MEDIAN KL exceeds ceiling AND reward-proxy
        # collapses → pulls policy back → reward safe.
        # CEILING CALIBRATION (validation klstable/klstable2 2026-05-28): TRAINING
        # KL for healthy GRPO sits SUSTAINED ~1.0-1.6 (≠ eval KL 0.077-0.258, which
        # is final-model-vs-base). Ceiling=1.0 FALSELY fired on healthy runs (reward
        # improving, length controlled). Default raised to 2.5: above healthy
        # training KL (~1.6) + transient spikes (median-smoothed), below disaster
        # (EXP 3.196). Clean separation. 0 = disabled.
        try:
            self._kl_gov_ceiling = float(os.environ.get("TRAINING_GRPO_KL_GOVERNOR", "2.5"))
        except (TypeError, ValueError):
            self._kl_gov_ceiling = 2.5
        try:
            self._kl_gov_factor = float(os.environ.get("TRAINING_GRPO_KL_GOVERNOR_FACTOR", "0.5"))
        except (TypeError, ValueError):
            self._kl_gov_factor = 0.5
        self._kl_gov_window = deque(maxlen=3)  # rolling 3-log mean (smooths spikes)
        self._kl_gov_throttles = 0
        self._kl_gov_max_throttles = 4  # floor: don't decay LR to zero
        self._kl_gov_best_proxy = None  # best reward-proxy seen (drift discriminator)

    def _maybe_kl_govern(self, kl, reward, kwargs):
        """Throttle LR ONLY on genuine drift: high KL AND reward-proxy collapsing.
        Returns True if throttled."""
        if self._kl_gov_ceiling <= 0 or kl is None:
            return False
        if self._kl_gov_throttles >= self._kl_gov_max_throttles:
            return False
        try:
            kl_f = float(kl)
            self._kl_gov_window.append(kl_f)
        except (TypeError, ValueError):
            return False
        # Track reward-proxy (validator-style reward - 0.5*kl) to discriminate
        # genuine drift from healthy aggressive learning.
        proxy = None
        if reward is not None:
            try:
                proxy = float(reward) - 0.5 * kl_f
                if self._kl_gov_best_proxy is None or proxy > self._kl_gov_best_proxy:
                    self._kl_gov_best_proxy = proxy
            except (TypeError, ValueError):
                proxy = None
        if len(self._kl_gov_window) < self._kl_gov_window.maxlen:
            return False
        # MEDIAN (not mean) — robust to transient numerical KL spikes.
        # Validation 2026-05-28 (klstable2): a single-step KL spike to 249.8
        # (immediately back to 0.7) inflated rolling-MEAN to 83.7 → false fire.
        # Median of [0.8, 249.8, 0.7] = 0.8 (ignores the spike); sustained drift
        # (EXP [3.0,3.2,3.1]) median 3.1 still exceeds ceiling → fires correctly.
        recent = sorted(self._kl_gov_window)[len(self._kl_gov_window) // 2]
        if recent <= self._kl_gov_ceiling:
            return False
        # ── DRIFT GATE (2026-05-28 validation klstable b68ef8e5) ──
        # High training-KL ALONE is NOT drift: healthy aggressive learning runs
        # KL~1.0-1.6 with reward IMPROVING (-21→-10) + length controlled. KL-only
        # ceiling=1.0 falsely throttled that healthy run 4x. TRUE drift (EXP:
        # KL 3.196, reward -180, length blowup) has COLLAPSING reward-proxy.
        # Only throttle if proxy dropped meaningfully below its best → real divergence.
        if proxy is not None and self._kl_gov_best_proxy is not None:
            margin = abs(self._kl_gov_best_proxy) * 0.15 + 0.5
            if proxy >= self._kl_gov_best_proxy - margin:
                return False  # proxy holding/improving → healthy high-KL, don't touch LR
        # Drift confirmed (high KL + proxy collapse) → throttle LR
        sched = kwargs.get("lr_scheduler")
        opt = kwargs.get("optimizer")
        f = self._kl_gov_factor
        modified = False
        if sched is not None and hasattr(sched, "base_lrs") and sched.base_lrs:
            sched.base_lrs = [b * f for b in sched.base_lrs]
            modified = True
        if opt is not None and getattr(opt, "param_groups", None):
            for pg in opt.param_groups:
                if "lr" in pg:
                    pg["lr"] *= f
            modified = True
        if not modified:
            # Neither scheduler nor optimizer reachable this hook — log once, no count.
            if self._kl_gov_throttles == 0:
                print(f"[KL-governor] DRIFT mean_kl={recent:.4f} > {self._kl_gov_ceiling} "
                      f"but LR handle unavailable in callback kwargs — cannot throttle", flush=True)
            return False
        self._kl_gov_throttles += 1
        self._kl_gov_window.clear()  # reset window so we re-measure post-throttle
        _proxy_str = f"{proxy:.3f}" if proxy is not None else "?"
        _best_str = f"{self._kl_gov_best_proxy:.3f}" if self._kl_gov_best_proxy is not None else "?"
        print(
            f"[KL-governor] DRIFT mean_kl={recent:.4f} > {self._kl_gov_ceiling} "
            f"AND proxy={_proxy_str} collapsed from best={_best_str} "
            f"→ LR x{f} (throttle #{self._kl_gov_throttles}/{self._kl_gov_max_throttles})",
            flush=True,
        )
        return True

    def on_log(self, args, state: TrainerState, control: TrainerControl, logs=None, **kwargs):
        """Track reward + kl, compute plateau proxy, fire when stagnated."""
        # KL governor runs FIRST (preventive) — independent of plateau early-stop.
        # Guarded because it sits OUTSIDE the try that wraps the rest of this
        # callback, and transformers does not wrap callback dispatch: anything
        # raised here propagates through trainer.log() and ends the run. The
        # governor only watches and throttles — purely observational machinery
        # must never be the thing that costs a task its checkpoint. Its float
        # conversions are already guarded internally, but the LR mutation block
        # (sched.base_lrs, pg["lr"] *= f) is not, and neither is attribute access
        # on a partially-initialised instance.
        if logs:
            try:
                self._maybe_kl_govern(logs.get("kl"), logs.get("reward"), kwargs)
            except Exception as _exc:
                if getattr(self, "_kl_gov_ceiling", 0) > 0:
                    print(
                        f"[KL-governor] error — governor disabled for the rest of "
                        f"this run, training continues: {_exc}",
                        flush=True,
                    )
                # Setting the ceiling to 0 is the existing disable path
                # (_maybe_kl_govern returns immediately on it), so one failure
                # cannot turn into per-step log spam.
                self._kl_gov_ceiling = 0
        if self._h3_fired or not logs:
            return
        reward = logs.get("reward")
        kl = logs.get("kl")
        if reward is None or kl is None:
            return
        try:
            self._h3_rewards.append(float(reward))
            self._h3_kls.append(float(kl))
        except (TypeError, ValueError):
            return

        try:
            from dynamics_utils import (
                grpo_proxy_score,
                grpo_plateau_window,
                maybe_grpo_plateau_stop,
            )
            proxy = grpo_proxy_score(list(self._h3_rewards), list(self._h3_kls))
            self._h3_last_proxy = proxy  # BEST-CKPT: latest proxy for save-gate
            _total = max(1, int(getattr(state, "max_steps", 0) or 0))
            _warmup, _patience = grpo_plateau_window(_total)

            # ── Telemetry: log config once at first observation ──
            if not self._h3_config_logged:
                print(
                    f"[Hook 3] config: total_steps={_total}, warmup={_warmup} "
                    f"({_warmup/_total*100:.1f}%), patience={_patience} "
                    f"({_patience/_total*100:.1f}%), window_logs="
                    f"{self._h3_rewards.maxlen}",
                    flush=True,
                )
                self._h3_config_logged = True

            # ── Telemetry: announce warmup completion (first eligible step) ──
            if (not self._h3_warmup_announced
                    and state.global_step >= _warmup):
                print(
                    f"[Hook 3] warmup ended @ step={state.global_step} "
                    f"(warmup_steps={_warmup}); plateau detection now active "
                    f"with patience={_patience}",
                    flush=True,
                )
                self._h3_warmup_announced = True

            _prev_best = self._h3_best_proxy
            _prev_best_step = self._h3_best_step

            new_best, new_best_step, should_stop = maybe_grpo_plateau_stop(
                current_step=state.global_step,
                current_proxy=proxy,
                best_proxy=self._h3_best_proxy,
                best_step=self._h3_best_step,
                warmup_steps=_warmup,
                patience_steps=_patience,
            )
            self._h3_best_proxy = new_best
            self._h3_best_step = new_best_step

            # ── Telemetry: announce best proxy updates (post-warmup only) ──
            if (state.global_step >= _warmup
                    and new_best is not None
                    and (_prev_best is None or new_best > _prev_best)):
                _prev_str = (
                    "None" if _prev_best is None else f"{_prev_best:.4f}"
                )
                print(
                    f"[Hook 3] new best proxy={new_best:.4f} @ "
                    f"step={new_best_step} (prev best={_prev_str} @ "
                    f"{_prev_best_step})",
                    flush=True,
                )

            # ── Telemetry: periodic snapshot of current vs best ──
            if (state.global_step >= _warmup
                    and self._h3_best_proxy is not None
                    and (state.global_step - self._h3_last_snapshot_step)
                        >= self._h3_snapshot_every):
                _gap = state.global_step - self._h3_best_step
                _gap_pct = _gap / max(1, _patience) * 100
                print(
                    f"[Hook 3] snapshot step={state.global_step} "
                    f"current_proxy={proxy:.4f} best_proxy="
                    f"{self._h3_best_proxy:.4f} @ {self._h3_best_step} "
                    f"(no-improve gap={_gap}, {_gap_pct:.0f}% of patience)",
                    flush=True,
                )
                self._h3_last_snapshot_step = state.global_step

            if should_stop:
                self._h3_fired = True
                print(
                    f"[Hook 3 GRPO Plateau] proxy stagnated; best_proxy="
                    f"{self._h3_best_proxy:.4f} @ step={self._h3_best_step}, "
                    f"current_proxy={proxy:.4f} @ step={state.global_step} — "
                    f"triggering SAVE+stop (GRPO no-eval: reshape-crash-safe)",
                    flush=True,
                )
                # GRPO STEP-500 RESHAPE FIX: eval crashes (trl grpo_trainer:1199).
                # save-only + best-ckpt gate preserves peak. NEVER should_evaluate.
                control.should_evaluate = False
                control.should_save = True
                control.should_training_stop = True
                self.save_only = True
                return

            # ── KL ceiling — safety net for runaway drift (post-warmup) ──
            # Two detection modes (independent, both opt-in):
            #   a) Mean-based  (TRAINING_GRPO_KL_CEILING)
            #   b) Peak-based  (TRAINING_GRPO_KL_PEAK_THRESHOLD)
            if (state.global_step >= _warmup
                    and len(self._h3_kls) >= max(5, self._h3_kls.maxlen // 4)):
                if self._h3_kl_ceiling > 0:
                    _mean_kl = sum(self._h3_kls) / len(self._h3_kls)
                    if _mean_kl > self._h3_kl_ceiling:
                        self._h3_fired = True
                        print(
                            f"[Hook 3 KL Ceiling] mean_kl={_mean_kl:.2f} > "
                            f"ceiling={self._h3_kl_ceiling:.2f} @ "
                            f"step={state.global_step} (window="
                            f"{len(self._h3_kls)}) — triggering SAVE+stop (GRPO no-eval)",
                            flush=True,
                        )
                        control.should_evaluate = False  # GRPO eval crashes (reshape) — save-only
                        control.should_save = True
                        control.should_training_stop = True
                        self.save_only = True
                        return
                if self._h3_kl_peak_threshold > 0 and not self._h3_fired:
                    _peak_kl = max(self._h3_kls)
                    _violations = sum(
                        1 for k in self._h3_kls
                        if k > self._h3_kl_peak_threshold
                    )
                    _min_violations = max(2, len(self._h3_kls) // 8)
                    if (_peak_kl > self._h3_kl_peak_threshold
                            and _violations >= _min_violations):
                        self._h3_fired = True
                        print(
                            f"[Hook 3 KL Peak] peak_kl={_peak_kl:.2f} > "
                            f"threshold={self._h3_kl_peak_threshold:.2f} "
                            f"with {_violations}/{len(self._h3_kls)} "
                            f"violations (min={_min_violations}) @ "
                            f"step={state.global_step} — triggering "
                            f"SAVE+stop (GRPO no-eval)",
                            flush=True,
                        )
                        control.should_evaluate = False  # GRPO eval crashes (reshape) — save-only
                        control.should_save = True
                        control.should_training_stop = True
                        self.save_only = True
        except Exception as exc:
            # Fail-soft — Hook 3 must never break training.
            print(f"[Hook 3] skipped (fail-soft): {exc}", flush=True)

    def compute_loss(self, state: TrainerState, metrics):
        # FIX 2026-05-27 (Patch A from GRPO bedah):
        # Validator scores GRPO as `eval_loss = reward − BETA_GRPO × KL_div_full_corpus`
        # (rayonlabs/G.O.D validator/evaluation/eval_grpo.py:206-258, BETA_GRPO=0.5).
        # Previous implementation used `-eval_reward` only → checkpoint selection
        # ignored KL drift penalty. May submit high-reward/high-KL ckpt that
        # scores WORSE than moderate-reward/low-KL ckpt at validator side.
        # Hook 3 plateau guard already uses correct proxy (dynamics_utils.py:807-816),
        # mirror that semantic here. Fail-soft: if KL missing from log, fall back
        # to old behavior with visible warning.
        BETA_GRPO = 0.5  # match validator/core/constants.py:BETA_GRPO
        eval_loss = None
        if state.log_history:
            last_log_entry = state.log_history[-1]
            reward = last_log_entry.get("eval_reward") or last_log_entry.get("reward")
            kl = last_log_entry.get("eval_kl") or last_log_entry.get("kl")
            if reward is not None and kl is not None:
                # Validator-aligned: minimize -(reward - β·KL) for ckpt selection
                proxy = float(reward) - BETA_GRPO * float(kl)
                eval_loss = -proxy
                print(f"[ckpt-select] validator-aligned: reward={reward:.4f} kl={kl:.4f} "
                      f"proxy={proxy:.4f} eval_loss={eval_loss:.4f} (KL-penalized)", flush=True)
            elif reward is not None:
                # KL missing — fail-soft to old behavior with warning
                eval_loss = -float(reward)
                print(f"[ckpt-select] WARN: KL missing from log, fallback to -eval_reward "
                      f"(reward={reward:.4f} eval_loss={eval_loss:.4f}). "
                      f"Checkpoint may not align with validator scoring formula.", flush=True)
            else:
                print(f"[ckpt-select] WARN: no reward in last_log_entry: {last_log_entry}", flush=True)
        else:
            print(f"state.log_history is empty", flush=True)

        return eval_loss

    def penalize_eval_loss(self, eval_loss: float):
        if eval_loss < 0:
            return eval_loss / 3
        else:
            return eval_loss * 3


def check_remaining_time_less_than_minutes(end_time: str, minutes: int) -> bool: 
    end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    end_time = end_time.replace(tzinfo=timezone.utc)  # Make end_time timezone-aware in UTC
    now = datetime.datetime.now(timezone.utc)
    time_diff = end_time - now
    result =  time_diff.total_seconds() < minutes * 60
    if result:
        print(f"*** current time: {now} end_time: {end_time} time_diff: {time_diff}", flush=True)
    return result


class WhenToEvalHandler:
    def __init__(self, end_time: str, save_before_remaining_time: int = 3, periodic_save_steps: int = -1, steps_per_epoch: int = -1, max_steps: int = -1):
        self.save_before_remaining_time = save_before_remaining_time
        self.run_eval = False
        self.end_time = end_time
        self.periodic_save_steps = periodic_save_steps
        self.steps_per_epoch = steps_per_epoch
        self.max_steps = max_steps

    def __call__(self, global_step: int) -> dict:
        
        if self.steps_per_epoch != -1 and global_step % self.steps_per_epoch == 0 and global_step > 1:
            return {"eval": True, "reason": "epoch"}
        
        if self.periodic_save_steps != -1 and global_step % self.periodic_save_steps == 0 and global_step > 1:
            return {"eval": True, "reason": "periodic"}
        
        if self.save_before_remaining_time > 0 and not self.run_eval:
            if check_remaining_time_less_than_minutes(self.end_time, self.save_before_remaining_time):
                print(f"***ALERT: The time is about to run out need to eval & save the model", flush=True)
                # the eval time might be higher than the end_time, so we need to let the pod not stop by setting a flag for this
                self.run_eval = True
                return {"eval": True, "reason": "end_time"}
        
        if self.max_steps != -1 and global_step == self.max_steps:
            print(f"Stop training because of max steps: {self.max_steps}", flush=True)
            return {"eval": True, "reason": "max_step"}

        return {"eval": False, "reason": "none"}


def set_generation_config(model_name, model):
    try:
        if model_name in ERROR_GENERATION_CONFIG_MODELS:
            model.generation_config = GenerationConfig(temperature=None, top_p=None)
    except:
        print(f"Error setting generation config for model {model_name}")
        pass


def resize_if_needed(model_name, model, token_nums):
    try:
        if model_name in MIS_MATCH_VOCAB_SIZE_MODELS:
            model.resize_token_embeddings(token_nums)
    except:
        print(f"Error resizing token embeddings for model {model_name}")
        pass


def init_wandb(train_request: Dict):
    """No-op stub by design.

    W&B env vars (WANDB_MODE, WANDB_RUN_ID, WANDB_NAME, WANDB_DIR) are set at
    the orchestrator level in text_trainer.py:193-197 BEFORE training
    subprocess is spawned, so child processes inherit them. Calling this
    function again inside training would re-apply the same values — pointless
    but not harmful.

    The `return True` prematurely-terminated body below (now removed) used to
    re-assign these env vars. Dead code removed for clarity.

    To toggle online W&B at runtime: export WANDB_MODE=online before calling
    text_trainer.py.

    Kept as a function (not deleted) to preserve the import contract used by
    train_instruct.py / train_dpo.py / train_grpo.py.
    """
    mode = os.environ.get("WANDB_MODE", "offline")
    run_id = os.environ.get("WANDB_RUN_ID", "")
    if is_main_process(LOCAL_RANK):
        print(f"[init_wandb] W&B mode={mode} run_id={run_id} (stub — env set upstream)", flush=True)
    return True