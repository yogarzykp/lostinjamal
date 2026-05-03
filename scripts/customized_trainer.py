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
        if not self.early_stop_disabled:
            print(
                f"[early_stop] dynamic config: patience={self.early_stop_patience} "
                f"(adaptive from total_steps={total_steps_all_epochs}, derived_epochs={derived_epochs}), "
                f"window={self.early_stop_window}, min_delta={self.early_stop_min_delta}",
                flush=True,
            )

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

        if self.best_checkpoint_info is None or eval_loss < self.best_checkpoint_info["loss"] - self.early_stop_min_delta:
            print(f"Updating the best checkpoint info at step: {state.global_step} with eval_loss: {eval_loss}", flush=True)
            self.best_checkpoint_info = {
                "loss": eval_loss,
                "step": state.global_step
            }
            self.update_best_checkpoint = True
            self.no_improve_count = 0
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


class GRPOCustomEvalSaveCallback(CustomEvalSaveCallback):
    def compute_loss(self, state: TrainerState, metrics):
        eval_loss = None
        if state.log_history:
            last_log_entry = state.log_history[-1]
            eval_loss = last_log_entry.get("eval_reward", None)
            print(f"choose eval_loss ({eval_loss}) as eval_reward from: last_log_entry: {last_log_entry}; \n metrics: {metrics}", flush=True)
        else:
            print(f"state.log_history is empty", flush=True)
            
        if eval_loss is not None:
            eval_loss = - eval_loss
            
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