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
MAX_TRIES = 9


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

LOCAL_RANK = int(os.getenv("LOCAL_RANK", "0"))

print(f"LOCAL_RANK: {LOCAL_RANK} in customized_trainer.py", flush=True)
    
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
        checking_mode: str = "none"
    ):
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
        return metrics.get("eval_loss", None)

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
            start_time_obj = datetime.datetime.strptime(my_state["train"]["start_time"], "%Y-%m-%d %H:%M:%S")
            start_train_time_obj = datetime.datetime.strptime(my_state["train"]["start_train_time"], "%Y-%m-%d %H:%M:%S")
            
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
                # save the current loss of this step to the state;
                last_log = state.log_history[-1]
                my_state["train"]["current_loss"] = last_log["loss"]
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
            current_loss = state.log_history[-1]["loss"]
            my_state["train"]["current_loss"] = current_loss
                
            control.should_training_stop = True

            # Check if current_loss > current min_loss --> do not save to save time and space
            # 
            # if my_state["train"]["current_loss"] > current_min_loss:
            #     print(f"Current loss: {my_state['train']['current_loss']} is greater than the current min_loss: {current_min_loss}, do not save the checkpoint", flush=True)
            #     control.should_save = False
            # check if this is the last run and the current_loss is the lowest --> keep running the training
            current_is_the_best = False
            current_min_loss = min([run["current_loss"] for run in my_state["runs"]])
            if current_loss <= current_min_loss:
                if len(my_state["runs"]) + 1 == my_state["next_runs"]:
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
            # do not allow the pod to be stopped by any reason 
                # first check if there is at least one checkpoint or not 
            print(f"Evaluating the model at step: {state.global_step} the reason: {when_to_eval['reason']}", flush=True)
            control.should_evaluate = True
            control.should_save = True
            if when_to_eval["reason"] == "end_time":
                if not self.has_checkpoint: # if there is no checkpoint, we just save the model, do not evaluate
                    print(f"No checkpoint found, just save the model at step: {state.global_step}", flush=True)
                    control.should_evaluate = False
                    self.save_only = True
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

        if self.best_checkpoint_info is None or eval_loss < self.best_checkpoint_info["loss"] - self.early_stop_min_delta:
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
        else:
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
                f.write(f"{current_step},no_eval")
            
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

        # Write merged adapter to submission_dir, overwriting the best-only adapter
        dst_path = os.path.join(self.submission_dir, weight_filename)
        try:
            if weight_filename.endswith(".safetensors"):
                from safetensors.torch import save_file
                save_file(merged_sd, dst_path)
            else:
                torch.save(merged_sd, dst_path)
            losses = [f"{e['loss']:.6e}" for e in pool]
            steps = [e["step"] for e in pool]
            print(
                f"[WSM] MERGED top-{len(pool)} adapters to {dst_path}: "
                f"steps={steps} losses={losses}",
                flush=True,
            )
        except Exception as exc:
            print(f"[WSM] save fail (keeping best-only): {exc}", flush=True)

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
        # divergence). Stable runs sit at KL 0.077-0.258. This governor catches
        # runaway drift DURING training (not just checkpoint-select) by throttling
        # LR when rolling-mean KL exceeds ceiling → pulls policy back toward
        # reference → KL stable → LR effectively self-stabilizing → reward safe.
        # Default ceiling 1.0 (4x above stable 0.258, well below disaster 3.196):
        # never fires on healthy runs, only catches genuine drift. 0 = disabled.
        try:
            self._kl_gov_ceiling = float(os.environ.get("TRAINING_GRPO_KL_GOVERNOR", "1.0"))
        except (TypeError, ValueError):
            self._kl_gov_ceiling = 1.0
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
        recent = sum(self._kl_gov_window) / len(self._kl_gov_window)
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
        if logs:
            self._maybe_kl_govern(logs.get("kl"), logs.get("reward"), kwargs)
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
                    f"triggering eval+save+stop",
                    flush=True,
                )
                control.should_evaluate = True
                control.should_save = True
                control.should_training_stop = True
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
                            f"{len(self._h3_kls)}) — triggering eval+save+stop",
                            flush=True,
                        )
                        control.should_evaluate = True
                        control.should_save = True
                        control.should_training_stop = True
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
                            f"eval+save+stop",
                            flush=True,
                        )
                        control.should_evaluate = True
                        control.should_save = True
                        control.should_training_stop = True
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