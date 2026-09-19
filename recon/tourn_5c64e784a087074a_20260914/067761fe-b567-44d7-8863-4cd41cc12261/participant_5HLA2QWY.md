# Loki — task 067761fe-b567-44d7-8863-4cd41cc12261 — hotkey 5HLA2QWYy3GpNwCiBCwMMhGw5hpPosSeZ41my8B3nuFDQHNF
fetched 2026-09-19T05:02:34+00:00  lines=763  hit_page_cap=False  containers=['downloader-067761fe-b567-44d7-8863-4cd41cc12261-f588ac1a', 'fastapi', 'hf-upload-d57a2cdbf89b4eb19b6308f926e517ba', 'text-trainer-89a5ef9bff7540ebb2fa66a041db0341']

[downloader-0] Downloading datasets to: /cache/datasets
[downloader-0] Downloading models to: /cache/models
[downloader-0] Model already cached at /cache/models/c53e93d87a4fe77f.
[downloader-0] Skipping download.
[downloader-0] Model path: /cache/models/c53e93d87a4fe77f
[downloader-0] Dataset path: /cache/datasets
[fastapi] Repository cloned successfully
[fastapi] Running Cache Download Container
[fastapi] Starting downloader container: downloader-067761fe-b567-44d7-8863-4cd41cc12261-f588ac1a
[fastapi] Download completed successfully for task 067761fe-b567-44d7-8863-4cd41cc12261
[fastapi] Building Docker image 'standalone-text-trainer:7d822049-2622-44f9-b03d-4f9efa0b3a88' (timeout=1800s)...
[fastapi] Step 1/7 : FROM axolotlai/axolotl:main-20260701-py3.11-cu128-2.9.1@sha256:3aa6403f59f2268bb8f686f6c748d6fad2949580a0048cd25a605eb2de239ee5
[fastapi] Pulling from axolotlai/axolotlAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsDigest: sha256:3aa6403f59f2268bb8f686f6c748d6fad2949580a0048cd25a605eb2de239ee5Status: Downloaded newer image for axolotlai/axolotl:main-20260701-py3.11-cu128-2.9.1@sha256:3aa6403f59f2268bb8f686f6c748d6fad2949580a0048cd25a605eb2de239ee5 ---> 08c3197175de
[fastapi] Step 2/7 : ENV PYTHONUNBUFFERED=1     PIP_NO_CACHE_DIR=1     HF_HUB_DISABLE_TELEMETRY=1     HF_HUB_DISABLE_SYMLINKS_WARNING=1     TOKENIZERS_PARALLELISM=false     HF_HUB_OFFLINE=1     TRANSFORMERS_OFFLINE=1
[fastapi] ---> Running in 56e1b7511fa5
[fastapi] ---> 24c212a78f4e
[fastapi] Step 3/7 : RUN TORCH_CUDA_ARCH_LIST="8.0;9.0+PTX" uv pip install         --python /workspace/axolotl-venv/bin/python         --no-cache --no-build-isolation causal-conv1d==1.6.2.post1
[fastapi] ---> Running in 3d40986e7168
[fastapi] [91mUsing Python 3.11.15 environment at: /workspace/axolotl-venv
[fastapi] [0m[91mResolved 28 packages in 116ms
[fastapi] [0m[91m   Building causal-conv1d==1.6.2.post1
[fastapi] [0m[91m      Built causal-conv1d==1.6.2.post1
[fastapi] [0m[91mPrepared 1 package in 4.25s
[fastapi] [0m[91mInstalled 1 package in 0.68ms
[fastapi] + causal-conv1d==1.6.2.post1
[fastapi] [0m ---> 1f66b10588fa
[fastapi] Step 4/7 : WORKDIR /app
[fastapi] ---> Running in b88f40f18761
[fastapi] ---> c2ba92843019
[fastapi] Step 5/7 : COPY forge /app/forge
[fastapi] ---> 6a11ffab84af
[fastapi] Step 6/7 : COPY pyproject.toml LICENSE.md NOTICE /app/
[fastapi] ---> 990c6fa10381
[fastapi] Step 7/7 : ENTRYPOINT ["/workspace/axolotl-venv/bin/python", "-m", "forge.cli"]
[fastapi] ---> Running in 8135ff3aa8a5
[fastapi] ---> 20ab477f905a
[fastapi] {'aux': {'ID': 'sha256:20ab477f905a51c15f4a82b9a35164ee59a4f725190345183e50111ee8bdd193'}}Successfully built 20ab477f905a
[fastapi] Successfully tagged standalone-text-trainer:7d822049-2622-44f9-b03d-4f9efa0b3a88
[fastapi] Docker image built successfully.
[fastapi] Container.wait() returned: {'StatusCode': 0}
[fastapi] Cleaning up
[fastapi] Cleaned up Docker resources.
[fastapi] Starting upload container hf-upload-d57a2cdbf89b4eb19b6308f926e517ba for task 067761fe-b567-44d7-8863-4cd41cc12261...
[hf-upload-d5] Updated adapter_config.json with base_model: gradients-io-tournaments/augmented-8a3f84c4cc4a7528
[hf-upload-d5] Updated README.md with base_model: gradients-io-tournaments/augmented-8a3f84c4cc4a7528
[hf-upload-d5] Creating repo gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5HLA2QWY...
[hf-upload-d5] Uploading contents of /app/checkpoints/067761fe-b567-44d7-8863-4cd41cc12261/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5HLA2QWY to gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5HLA2QWY
[hf-upload-d5] Uploaded successfully to https://huggingface.co/gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5HLA2QWY
[hf-upload-d5] Deleted local folder: /app/checkpoints/067761fe-b567-44d7-8863-4cd41cc12261/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5HLA2QWY
[text-trainer] Skipping import of cpp extensions due to incompatible torch version. Please upgrade to torch >= 2.11.0 (found 2.9.1+cu128).
[text-trainer] [INFO] Running in WANDB offline mode
[text-trainer] [sft_v2] sft_v2_selected {'params_b': 1.236, 'hours_remaining': 0.995}
[text-trainer] [sft_v2] sft_v2_data {'rows': 19505, 'tokenized': 19321, 'deduped': 18538, 'train_n': 18138, 'dev_n': 400, 'max_len': 2944, 'p50': 424, 'p99': 2646}
[text-trainer] [sft_v2] sft_v2_adapter {'r': 32, 'alpha': 64, 'dropout': 0.0}
[text-trainer] [transformers] `use_return_dict` is deprecated! Use `return_dict` instead!
[text-trainer] [sft_v2] sft_v2_memory_probe {'micro': 8, 'gradient_checkpointing': False, 'fits': True}
[text-trainer] [sft_v2] sft_v2_timing {'t_per_step': 0.227, 'eff_batch': 16, 'losses': [1.9797, 2.2254, 1.4303]}
[text-trainer] [sft_v2] sft_v2_sweep_skipped {'strategy': 'lora', 'lr': 0.0002}
[text-trainer] [sft_v2] sft_v2_sweep_gate {'batches': 200, 't_per_step': 0.227, 'lr_override': 0.0002, 'remaining_s': 3542.4}
[text-trainer] [sft_v2] sft_v2_train_start {'elapsed_s': 42.0, 'lr': 0.0002, 'prior_lr': 0.0002, 't_per_step': 0.227029, 'steps_per_epoch': 1133, 'finish_reserve_s': 98.9}
[text-trainer] [sft_v2] sft_v2_plan {'phase': 0, 'lr': 0.0002, 't_per_step': 0.227029, 'epochs': 1.0, 'total_steps': 1133, 'warmup': 33, 'eval_every': 141, 'window_s': 3442.9, 'epochs_done': 0.0}
[text-trainer] {'loss': '2.07', 'grad_norm': '2.921', 'learning_rate': '2.424e-05', 'epoch': '0.004409'}
[text-trainer] {'loss': '1.73', 'grad_norm': '2.928', 'learning_rate': '5.455e-05', 'epoch': '0.008818'}
[text-trainer] {'loss': '1.798', 'grad_norm': '3.952', 'learning_rate': '8.485e-05', 'epoch': '0.01323'}
[text-trainer] {'loss': '1.648', 'grad_norm': '2.478', 'learning_rate': '0.0001152', 'epoch': '0.01764'}
[text-trainer] {'loss': '1.463', 'grad_norm': '1.794', 'learning_rate': '0.0001455', 'epoch': '0.02205'}
[text-trainer] {'loss': '1.703', 'grad_norm': '1.847', 'learning_rate': '0.0001758', 'epoch': '0.02646'}
[text-trainer] {'loss': '2.257', 'grad_norm': '2.295', 'learning_rate': '0.0002', 'epoch': '0.03086'}
[text-trainer] {'loss': '2.079', 'grad_norm': '2.17', 'learning_rate': '0.0002', 'epoch': '0.03527'}
[text-trainer] {'loss': '1.895', 'grad_norm': '2.574', 'learning_rate': '0.0002', 'epoch': '0.03968'}
[text-trainer] {'loss': '2.134', 'grad_norm': '3.702', 'learning_rate': '0.0001999', 'epoch': '0.04409'}
[text-trainer] {'loss': '1.718', 'grad_norm': '2.471', 'learning_rate': '0.0001998', 'epoch': '0.0485'}
[text-trainer] {'loss': '1.415', 'grad_norm': '1.792', 'learning_rate': '0.0001998', 'epoch': '0.05291'}
[text-trainer] {'loss': '1.336', 'grad_norm': '2.076', 'learning_rate': '0.0001996', 'epoch': '0.05732'}
[text-trainer] {'loss': '1.536', 'grad_norm': '1.69', 'learning_rate': '0.0001995', 'epoch': '0.06173'}
[text-trainer] {'loss': '1.796', 'grad_norm': '2.086', 'learning_rate': '0.0001994', 'epoch': '0.06614'}
[text-trainer] {'loss': '1.52', 'grad_norm': '2.035', 'learning_rate': '0.0001992', 'epoch': '0.07055'}
[text-trainer] {'loss': '1.755', 'grad_norm': '2.27', 'learning_rate': '0.000199', 'epoch': '0.07496'}
[text-trainer] {'loss': '2.014', 'grad_norm': '2.965', 'learning_rate': '0.0001989', 'epoch': '0.07937'}
[text-trainer] {'loss': '1.954', 'grad_norm': '1.705', 'learning_rate': '0.0001986', 'epoch': '0.08377'}
[text-trainer] {'loss': '1.646', 'grad_norm': '2.305', 'learning_rate': '0.0001984', 'epoch': '0.08818'}
[text-trainer] {'loss': '1.362', 'grad_norm': '1.845', 'learning_rate': '0.0001982', 'epoch': '0.09259'}
[text-trainer] {'loss': '1.058', 'grad_norm': '1.48', 'learning_rate': '0.0001979', 'epoch': '0.097'}
[text-trainer] {'loss': '1.206', 'grad_norm': '1.493', 'learning_rate': '0.0001976', 'epoch': '0.1014'}
[text-trainer] {'loss': '1.548', 'grad_norm': '1.594', 'learning_rate': '0.0001973', 'epoch': '0.1058'}
[text-trainer] {'loss': '1.389', 'grad_norm': '1.774', 'learning_rate': '0.000197', 'epoch': '0.1102'}
[text-trainer] {'loss': '1.641', 'grad_norm': '1.954', 'learning_rate': '0.0001966', 'epoch': '0.1146'}
[text-trainer] {'loss': '1.765', 'grad_norm': '2.071', 'learning_rate': '0.0001963', 'epoch': '0.119'}
[text-trainer] {'loss': '1.784', 'grad_norm': '2.242', 'learning_rate': '0.0001959', 'epoch': '0.1235'}
[text-trainer] [sft_v2] sft_v2_eval {'step': 141, 'dev_loss': 1.656531, 'best': 1.656531, 'eval_s': 7.8, 'pool': 1, 'improved': True}
[text-trainer] [sft_v2] sft_v2_eval_governor {'eval_every': 579, 'eval_s': 7.8}
[text-trainer] {'loss': '1.776', 'grad_norm': '2.399', 'learning_rate': '0.0001955', 'epoch': '0.1279'}
[text-trainer] {'loss': '2.406', 'grad_norm': '4.57', 'learning_rate': '0.0001951', 'epoch': '0.1323'}
[text-trainer] {'loss': '1.581', 'grad_norm': '1.474', 'learning_rate': '0.0001947', 'epoch': '0.1367'}
[text-trainer] {'loss': '1.187', 'grad_norm': '1.569', 'learning_rate': '0.0001942', 'epoch': '0.1411'}
[text-trainer] {'loss': '1.492', 'grad_norm': '1.434', 'learning_rate': '0.0001938', 'epoch': '0.1455'}
[text-trainer] {'loss': '1.286', 'grad_norm': '2.068', 'learning_rate': '0.0001933', 'epoch': '0.1499'}
[text-trainer] {'loss': '1.521', 'grad_norm': '2.071', 'learning_rate': '0.0001928', 'epoch': '0.1543'}
[text-trainer] {'loss': '1.407', 'grad_norm': '1.778', 'learning_rate': '0.0001923', 'epoch': '0.1587'}
[text-trainer] {'loss': '1.599', 'grad_norm': '2.093', 'learning_rate': '0.0001918', 'epoch': '0.1631'}
[text-trainer] {'loss': '2.044', 'grad_norm': '2.471', 'learning_rate': '0.0001912', 'epoch': '0.1675'}
[text-trainer] {'loss': '1.638', 'grad_norm': '1.98', 'learning_rate': '0.0001907', 'epoch': '0.172'}
[text-trainer] {'loss': '1.514', 'grad_norm': '2.5', 'learning_rate': '0.0001901', 'epoch': '0.1764'}
[text-trainer] {'loss': '1.559', 'grad_norm': '1.455', 'learning_rate': '0.0001895', 'epoch': '0.1808'}
[text-trainer] {'loss': '1.021', 'grad_norm': '1.415', 'learning_rate': '0.0001889', 'epoch': '0.1852'}
[text-trainer] {'loss': '1.167', 'grad_norm': '1.656', 'learning_rate': '0.0001883', 'epoch': '0.1896'}
[text-trainer] {'loss': '1.198', 'grad_norm': '1.557', 'learning_rate': '0.0001876', 'epoch': '0.194'}
[text-trainer] {'loss': '1.592', 'grad_norm': '1.667', 'learning_rate': '0.000187', 'epoch': '0.1984'}
[text-trainer] {'loss': '1.677', 'grad_norm': '1.697', 'learning_rate': '0.0001863', 'epoch': '0.2028'}
[text-trainer] {'loss': '1.79', 'grad_norm': '2.357', 'learning_rate': '0.0001856', 'epoch': '0.2072'}
[text-trainer] {'loss': '1.755', 'grad_norm': '1.778', 'learning_rate': '0.0001849', 'epoch': '0.2116'}
[text-trainer] {'loss': '1.787', 'grad_norm': '2.18', 'learning_rate': '0.0001842', 'epoch': '0.216'}
[text-trainer] {'loss': '1.743', 'grad_norm': '3.132', 'learning_rate': '0.0001834', 'epoch': '0.2205'}
[text-trainer] {'loss': '1.151', 'grad_norm': '1.294', 'learning_rate': '0.0001827', 'epoch': '0.2249'}
[text-trainer] {'loss': '1.114', 'grad_norm': '1.746', 'learning_rate': '0.0001819', 'epoch': '0.2293'}
[text-trainer] {'loss': '1.31', 'grad_norm': '1.964', 'learning_rate': '0.0001811', 'epoch': '0.2337'}
[text-trainer] {'loss': '1.107', 'grad_norm': '1.249', 'learning_rate': '0.0001804', 'epoch': '0.2381'}
[text-trainer] {'loss': '1.507', 'grad_norm': '1.606', 'learning_rate': '0.0001795', 'epoch': '0.2425'}
[text-trainer] {'loss': '1.648', 'grad_norm': '2.188', 'learning_rate': '0.0001787', 'epoch': '0.2469'}
[text-trainer] {'loss': '1.809', 'grad_norm': '1.928', 'learning_rate': '0.0001779', 'epoch': '0.2513'}
[text-trainer] {'loss': '1.747', 'grad_norm': '2.015', 'learning_rate': '0.000177', 'epoch': '0.2557'}
[text-trainer] {'loss': '1.564', 'grad_norm': '1.524', 'learning_rate': '0.0001762', 'epoch': '0.2601'}
[text-trainer] {'loss': '1.653', 'grad_norm': '3.355', 'learning_rate': '0.0001753', 'epoch': '0.2646'}
[text-trainer] {'loss': '1.292', 'grad_norm': '1.322', 'learning_rate': '0.0001744', 'epoch': '0.269'}
[text-trainer] {'loss': '1.362', 'grad_norm': '2.058', 'learning_rate': '0.0001735', 'epoch': '0.2734'}
[text-trainer] {'loss': '1.309', 'grad_norm': '1.878', 'learning_rate': '0.0001726', 'epoch': '0.2778'}
[text-trainer] {'loss': '1.554', 'grad_norm': '1.542', 'learning_rate': '0.0001717', 'epoch': '0.2822'}
[text-trainer] {'loss': '1.403', 'grad_norm': '2.007', 'learning_rate': '0.0001707', 'epoch': '0.2866'}
[text-trainer] {'loss': '1.398', 'grad_norm': '2.109', 'learning_rate': '0.0001698', 'epoch': '0.291'}
[text-trainer] {'loss': '1.735', 'grad_norm': '1.934', 'learning_rate': '0.0001688', 'epoch': '0.2954'}
[text-trainer] {'loss': '1.549', 'grad_norm': '1.683', 'learning_rate': '0.0001678', 'epoch': '0.2998'}
[text-trainer] {'loss': '1.643', 'grad_norm': '1.679', 'learning_rate': '0.0001668', 'epoch': '0.3042'}
[text-trainer] {'loss': '1.759', 'grad_norm': '3.121', 'learning_rate': '0.0001658', 'epoch': '0.3086'}
[text-trainer] {'loss': '1.329', 'grad_norm': '1.509', 'learning_rate': '0.0001648', 'epoch': '0.3131'}
[text-trainer] {'loss': '1.012', 'grad_norm': '1.884', 'learning_rate': '0.0001638', 'epoch': '0.3175'}
[text-trainer] {'loss': '1.318', 'grad_norm': '1.714', 'learning_rate': '0.0001628', 'epoch': '0.3219'}
[text-trainer] {'loss': '1.25', 'grad_norm': '1.765', 'learning_rate': '0.0001617', 'epoch': '0.3263'}
[text-trainer] {'loss': '1.589', 'grad_norm': '1.833', 'learning_rate': '0.0001607', 'epoch': '0.3307'}
[text-trainer] {'loss': '1.443', 'grad_norm': '1.761', 'learning_rate': '0.0001596', 'epoch': '0.3351'}
[text-trainer] {'loss': '1.472', 'grad_norm': '1.82', 'learning_rate': '0.0001585', 'epoch': '0.3395'}
[text-trainer] {'loss': '1.743', 'grad_norm': '2.155', 'learning_rate': '0.0001574', 'epoch': '0.3439'}
[text-trainer] {'loss': '1.836', 'grad_norm': '2.338', 'learning_rate': '0.0001563', 'epoch': '0.3483'}
[text-trainer] {'loss': '1.588', 'grad_norm': '2.639', 'learning_rate': '0.0001552', 'epoch': '0.3527'}
[text-trainer] {'loss': '1.327', 'grad_norm': '1.662', 'learning_rate': '0.0001541', 'epoch': '0.3571'}
[text-trainer] {'loss': '1.213', 'grad_norm': '1.699', 'learning_rate': '0.000153', 'epoch': '0.3616'}
[text-trainer] {'loss': '1.227', 'grad_norm': '1.911', 'learning_rate': '0.0001519', 'epoch': '0.366'}
[text-trainer] {'loss': '1.326', 'grad_norm': '1.373', 'learning_rate': '0.0001507', 'epoch': '0.3704'}
[text-trainer] {'loss': '1.537', 'grad_norm': '1.701', 'learning_rate': '0.0001496', 'epoch': '0.3748'}
[text-trainer] {'loss': '1.536', 'grad_norm': '1.89', 'learning_rate': '0.0001484', 'epoch': '0.3792'}
[text-trainer] {'loss': '1.607', 'grad_norm': '2.05', 'learning_rate': '0.0001472', 'epoch': '0.3836'}
[text-trainer] {'loss': '2.096', 'grad_norm': '2.021', 'learning_rate': '0.0001461', 'epoch': '0.388'}
[text-trainer] {'loss': '1.992', 'grad_norm': '1.664', 'learning_rate': '0.0001449', 'epoch': '0.3924'}
[text-trainer] {'loss': '1.815', 'grad_norm': '3.271', 'learning_rate': '0.0001437', 'epoch': '0.3968'}
[text-trainer] {'loss': '1.519', 'grad_norm': '1.811', 'learning_rate': '0.0001425', 'epoch': '0.4012'}
[text-trainer] {'loss': '0.9218', 'grad_norm': '1.571', 'learning_rate': '0.0001413', 'epoch': '0.4056'}
[text-trainer] {'loss': '1.265', 'grad_norm': '1.976', 'learning_rate': '0.0001401', 'epoch': '0.4101'}
[text-trainer] {'loss': '1.318', 'grad_norm': '1.585', 'learning_rate': '0.0001389', 'epoch': '0.4145'}
[text-trainer] {'loss': '1.496', 'grad_norm': '1.472', 'learning_rate': '0.0001377', 'epoch': '0.4189'}
[text-trainer] {'loss': '1.457', 'grad_norm': '1.817', 'learning_rate': '0.0001364', 'epoch': '0.4233'}
[text-trainer] {'loss': '1.498', 'grad_norm': '1.823', 'learning_rate': '0.0001352', 'epoch': '0.4277'}
[text-trainer] {'loss': '1.485', 'grad_norm': '1.754', 'learning_rate': '0.000134', 'epoch': '0.4321'}
[text-trainer] {'loss': '1.574', 'grad_norm': '1.809', 'learning_rate': '0.0001327', 'epoch': '0.4365'}
[text-trainer] {'loss': '1.414', 'grad_norm': '2.685', 'learning_rate': '0.0001315', 'epoch': '0.4409'}
[text-trainer] {'loss': '1.317', 'grad_norm': '1.417', 'learning_rate': '0.0001302', 'epoch': '0.4453'}
[text-trainer] {'loss': '1.042', 'grad_norm': '1.323', 'learning_rate': '0.000129', 'epoch': '0.4497'}
[text-trainer] {'loss': '1.225', 'grad_norm': '1.891', 'learning_rate': '0.0001277', 'epoch': '0.4541'}
[text-trainer] {'loss': '1.302', 'grad_norm': '1.614', 'learning_rate': '0.0001265', 'epoch': '0.4586'}
[text-trainer] {'loss': '1.253', 'grad_norm': '1.536', 'learning_rate': '0.0001252', 'epoch': '0.463'}
[text-trainer] {'loss': '1.541', 'grad_norm': '1.94', 'learning_rate': '0.0001239', 'epoch': '0.4674'}
[text-trainer] {'loss': '1.828', 'grad_norm': '1.969', 'learning_rate': '0.0001227', 'epoch': '0.4718'}
[text-trainer] {'loss': '1.704', 'grad_norm': '1.534', 'learning_rate': '0.0001214', 'epoch': '0.4762'}
[text-trainer] {'loss': '1.53', 'grad_norm': '1.674', 'learning_rate': '0.0001201', 'epoch': '0.4806'}
[text-trainer] {'loss': '1.716', 'grad_norm': '2.907', 'learning_rate': '0.0001188', 'epoch': '0.485'}
[text-trainer] {'loss': '1.222', 'grad_norm': '1.225', 'learning_rate': '0.0001176', 'epoch': '0.4894'}
[text-trainer] {'loss': '1.102', 'grad_norm': '1.312', 'learning_rate': '0.0001163', 'epoch': '0.4938'}
[text-trainer] {'loss': '1.126', 'grad_norm': '1.7', 'learning_rate': '0.000115', 'epoch': '0.4982'}
[text-trainer] {'loss': '1.213', 'grad_norm': '1.653', 'learning_rate': '0.0001137', 'epoch': '0.5026'}
[text-trainer] {'loss': '1.177', 'grad_norm': '1.506', 'learning_rate': '0.0001124', 'epoch': '0.5071'}
[text-trainer] [sft_v2] sft_v2_eval {'step': 579, 'dev_loss': 1.454955, 'best': 1.454955, 'eval_s': 6.7, 'pool': 2, 'improved': True}
[text-trainer] {'loss': '1.405', 'grad_norm': '1.855', 'learning_rate': '0.0001112', 'epoch': '0.5115'}
[text-trainer] {'loss': '1.817', 'grad_norm': '2.396', 'learning_rate': '0.0001099', 'epoch': '0.5159'}
[text-trainer] {'loss': '1.673', 'grad_norm': '1.629', 'learning_rate': '0.0001086', 'epoch': '0.5203'}
[text-trainer] {'loss': '1.709', 'grad_norm': '2.39', 'learning_rate': '0.0001073', 'epoch': '0.5247'}
[text-trainer] {'loss': '1.874', 'grad_norm': '3.937', 'learning_rate': '0.000106', 'epoch': '0.5291'}
[text-trainer] {'loss': '1.221', 'grad_norm': '1.547', 'learning_rate': '0.0001047', 'epoch': '0.5335'}
[text-trainer] {'loss': '1.149', 'grad_norm': '1.723', 'learning_rate': '0.0001035', 'epoch': '0.5379'}
[text-trainer] {'loss': '1.062', 'grad_norm': '1.559', 'learning_rate': '0.0001022', 'epoch': '0.5423'}
[text-trainer] {'loss': '1.239', 'grad_norm': '1.641', 'learning_rate': '0.0001009', 'epoch': '0.5467'}
[text-trainer] {'loss': '1.129', 'grad_norm': '1.686', 'learning_rate': '9.962e-05', 'epoch': '0.5511'}
[text-trainer] {'loss': '1.475', 'grad_norm': '1.944', 'learning_rate': '9.835e-05', 'epoch': '0.5556'}
[text-trainer] {'loss': '1.571', 'grad_norm': '2.12', 'learning_rate': '9.708e-05', 'epoch': '0.56'}
[text-trainer] {'loss': '1.783', 'grad_norm': '2.091', 'learning_rate': '9.581e-05', 'epoch': '0.5644'}
[text-trainer] {'loss': '1.612', 'grad_norm': '1.882', 'learning_rate': '9.454e-05', 'epoch': '0.5688'}
[text-trainer] {'loss': '1.555', 'grad_norm': '2.659', 'learning_rate': '9.328e-05', 'epoch': '0.5732'}
[text-trainer] {'loss': '1.243', 'grad_norm': '1.744', 'learning_rate': '9.202e-05', 'epoch': '0.5776'}
[text-trainer] {'loss': '1.075', 'grad_norm': '1.739', 'learning_rate': '9.076e-05', 'epoch': '0.582'}
[text-trainer] {'loss': '1.04', 'grad_norm': '1.612', 'learning_rate': '8.951e-05', 'epoch': '0.5864'}
[text-trainer] {'loss': '1.202', 'grad_norm': '1.756', 'learning_rate': '8.826e-05', 'epoch': '0.5908'}
[text-trainer] {'loss': '1.436', 'grad_norm': '1.405', 'learning_rate': '8.702e-05', 'epoch': '0.5952'}
[text-trainer] {'loss': '1.681', 'grad_norm': '1.798', 'learning_rate': '8.578e-05', 'epoch': '0.5996'}
[text-trainer] {'loss': '1.706', 'grad_norm': '1.755', 'learning_rate': '8.454e-05', 'epoch': '0.6041'}
[text-trainer] {'loss': '1.828', 'grad_norm': '2.022', 'learning_rate': '8.331e-05', 'epoch': '0.6085'}
[text-trainer] {'loss': '1.651', 'grad_norm': '2.061', 'learning_rate': '8.209e-05', 'epoch': '0.6129'}
[text-trainer] {'loss': '1.269', 'grad_norm': '2.869', 'learning_rate': '8.087e-05', 'epoch': '0.6173'}
[text-trainer] {'loss': '1.217', 'grad_norm': '1.397', 'learning_rate': '7.966e-05', 'epoch': '0.6217'}
[text-trainer] {'loss': '0.8594', 'grad_norm': '1.093', 'learning_rate': '7.846e-05', 'epoch': '0.6261'}
[text-trainer] {'loss': '1.129', 'grad_norm': '1.413', 'learning_rate': '7.726e-05', 'epoch': '0.6305'}
[text-trainer] {'loss': '1.231', 'grad_norm': '1.382', 'learning_rate': '7.606e-05', 'epoch': '0.6349'}
[text-trainer] {'loss': '1.248', 'grad_norm': '1.435', 'learning_rate': '7.488e-05', 'epoch': '0.6393'}
[text-trainer] {'loss': '1.395', 'grad_norm': '1.684', 'learning_rate': '7.37e-05', 'epoch': '0.6437'}
[text-trainer] {'loss': '1.529', 'grad_norm': '3.334', 'learning_rate': '7.253e-05', 'epoch': '0.6481'}
[text-trainer] {'loss': '1.723', 'grad_norm': '2.129', 'learning_rate': '7.136e-05', 'epoch': '0.6526'}
[text-trainer] {'loss': '1.63', 'grad_norm': '1.776', 'learning_rate': '7.021e-05', 'epoch': '0.657'}
[text-trainer] {'loss': '1.456', 'grad_norm': '3.29', 'learning_rate': '6.906e-05', 'epoch': '0.6614'}
[text-trainer] {'loss': '1.313', 'grad_norm': '1.476', 'learning_rate': '6.792e-05', 'epoch': '0.6658'}
[text-trainer] {'loss': '1.145', 'grad_norm': '2.172', 'learning_rate': '6.679e-05', 'epoch': '0.6702'}
[text-trainer] {'loss': '1.113', 'grad_norm': '1.882', 'learning_rate': '6.567e-05', 'epoch': '0.6746'}
[text-trainer] {'loss': '1.212', 'grad_norm': '1.65', 'learning_rate': '6.456e-05', 'epoch': '0.679'}
[text-trainer] {'loss': '1.344', 'grad_norm': '1.739', 'learning_rate': '6.345e-05', 'epoch': '0.6834'}
[text-trainer] {'loss': '1.529', 'grad_norm': '1.414', 'learning_rate': '6.236e-05', 'epoch': '0.6878'}
[text-trainer] {'loss': '1.624', 'grad_norm': '1.98', 'learning_rate': '6.127e-05', 'epoch': '0.6922'}
[text-trainer] {'loss': '1.605', 'grad_norm': '2.016', 'learning_rate': '6.02e-05', 'epoch': '0.6966'}
[text-trainer] {'loss': '1.382', 'grad_norm': '1.756', 'learning_rate': '5.913e-05', 'epoch': '0.7011'}
[text-trainer] {'loss': '1.701', 'grad_norm': '3.314', 'learning_rate': '5.808e-05', 'epoch': '0.7055'}
[text-trainer] {'loss': '1.236', 'grad_norm': '2.05', 'learning_rate': '5.704e-05', 'epoch': '0.7099'}
[text-trainer] {'loss': '1.011', 'grad_norm': '1.628', 'learning_rate': '5.6e-05', 'epoch': '0.7143'}
[text-trainer] {'loss': '1.137', 'grad_norm': '1.557', 'learning_rate': '5.498e-05', 'epoch': '0.7187'}
[text-trainer] {'loss': '1.054', 'grad_norm': '1.446', 'learning_rate': '5.397e-05', 'epoch': '0.7231'}
[text-trainer] {'loss': '1.231', 'grad_norm': '1.581', 'learning_rate': '5.297e-05', 'epoch': '0.7275'}
[text-trainer] {'loss': '1.375', 'grad_norm': '1.585', 'learning_rate': '5.199e-05', 'epoch': '0.7319'}
[text-trainer] {'loss': '1.605', 'grad_norm': '2.069', 'learning_rate': '5.101e-05', 'epoch': '0.7363'}
[text-trainer] {'loss': '1.721', 'grad_norm': '1.817', 'learning_rate': '5.005e-05', 'epoch': '0.7407'}
[text-trainer] {'loss': '1.48', 'grad_norm': '2.33', 'learning_rate': '4.909e-05', 'epoch': '0.7451'}
[text-trainer] {'loss': '1.599', 'grad_norm': '2.901', 'learning_rate': '4.816e-05', 'epoch': '0.7496'}
[text-trainer] {'loss': '0.997', 'grad_norm': '1.165', 'learning_rate': '4.723e-05', 'epoch': '0.754'}
[text-trainer] {'loss': '1.073', 'grad_norm': '1.654', 'learning_rate': '4.632e-05', 'epoch': '0.7584'}
[text-trainer] {'loss': '1.081', 'grad_norm': '1.578', 'learning_rate': '4.541e-05', 'epoch': '0.7628'}
[text-trainer] {'loss': '1.111', 'grad_norm': '1.804', 'learning_rate': '4.453e-05', 'epoch': '0.7672'}
[text-trainer] {'loss': '1.389', 'grad_norm': '1.891', 'learning_rate': '4.365e-05', 'epoch': '0.7716'}
[text-trainer] {'loss': '1.571', 'grad_norm': '2.083', 'learning_rate': '4.279e-05', 'epoch': '0.776'}
[text-trainer] {'loss': '1.571', 'grad_norm': '2.118', 'learning_rate': '4.194e-05', 'epoch': '0.7804'}
[text-trainer] {'loss': '1.454', 'grad_norm': '1.757', 'learning_rate': '4.111e-05', 'epoch': '0.7848'}
[text-trainer] {'loss': '1.74', 'grad_norm': '1.67', 'learning_rate': '4.029e-05', 'epoch': '0.7892'}
[text-trainer] {'loss': '1.421', 'grad_norm': '2.942', 'learning_rate': '3.949e-05', 'epoch': '0.7937'}
[text-trainer] {'loss': '0.9937', 'grad_norm': '1.305', 'learning_rate': '3.87e-05', 'epoch': '0.7981'}
[text-trainer] {'loss': '0.8693', 'grad_norm': '1.156', 'learning_rate': '3.792e-05', 'epoch': '0.8025'}
[text-trainer] {'loss': '0.9998', 'grad_norm': '1.517', 'learning_rate': '3.716e-05', 'epoch': '0.8069'}
[text-trainer] {'loss': '1.101', 'grad_norm': '1.877', 'learning_rate': '3.641e-05', 'epoch': '0.8113'}
[text-trainer] {'loss': '1.393', 'grad_norm': '2.101', 'learning_rate': '3.568e-05', 'epoch': '0.8157'}
[text-trainer] {'loss': '1.445', 'grad_norm': '2.105', 'learning_rate': '3.496e-05', 'epoch': '0.8201'}
[text-trainer] {'loss': '1.877', 'grad_norm': '2.19', 'learning_rate': '3.426e-05', 'epoch': '0.8245'}
[text-trainer] {'loss': '1.587', 'grad_norm': '2.153', 'learning_rate': '3.358e-05', 'epoch': '0.8289'}
[text-trainer] {'loss': '1.482', 'grad_norm': '1.794', 'learning_rate': '3.291e-05', 'epoch': '0.8333'}
[text-trainer] {'loss': '1.419', 'grad_norm': '2.477', 'learning_rate': '3.225e-05', 'epoch': '0.8377'}
[text-trainer] {'loss': '1.303', 'grad_norm': '1.451', 'learning_rate': '3.161e-05', 'epoch': '0.8422'}
[text-trainer] {'loss': '0.9551', 'grad_norm': '1.365', 'learning_rate': '3.099e-05', 'epoch': '0.8466'}
[text-trainer] {'loss': '0.9804', 'grad_norm': '1.517', 'learning_rate': '3.038e-05', 'epoch': '0.851'}
[text-trainer] {'loss': '1.329', 'grad_norm': '1.59', 'learning_rate': '2.979e-05', 'epoch': '0.8554'}
[text-trainer] {'loss': '1.296', 'grad_norm': '1.717', 'learning_rate': '2.922e-05', 'epoch': '0.8598'}
[text-trainer] {'loss': '1.606', 'grad_norm': '2.094', 'learning_rate': '2.866e-05', 'epoch': '0.8642'}
[text-trainer] {'loss': '1.374', 'grad_norm': '1.894', 'learning_rate': '2.812e-05', 'epoch': '0.8686'}
[text-trainer] {'loss': '1.523', 'grad_norm': '1.952', 'learning_rate': '2.759e-05', 'epoch': '0.873'}
[text-trainer] {'loss': '1.574', 'grad_norm': '2.122', 'learning_rate': '2.709e-05', 'epoch': '0.8774'}
[text-trainer] {'loss': '1.365', 'grad_norm': '2.692', 'learning_rate': '2.66e-05', 'epoch': '0.8818'}
[text-trainer] {'loss': '1.21', 'grad_norm': '1.518', 'learning_rate': '2.612e-05', 'epoch': '0.8862'}
[text-trainer] {'loss': '0.9517', 'grad_norm': '1.549', 'learning_rate': '2.566e-05', 'epoch': '0.8907'}
[text-trainer] {'loss': '1.135', 'grad_norm': '1.531', 'learning_rate': '2.522e-05', 'epoch': '0.8951'}
[text-trainer] {'loss': '1.38', 'grad_norm': '1.758', 'learning_rate': '2.48e-05', 'epoch': '0.8995'}
[text-trainer] {'loss': '1.258', 'grad_norm': '1.848', 'learning_rate': '2.44e-05', 'epoch': '0.9039'}
[text-trainer] {'loss': '1.296', 'grad_norm': '1.896', 'learning_rate': '2.401e-05', 'epoch': '0.9083'}
[text-trainer] {'loss': '1.399', 'grad_norm': '1.758', 'learning_rate': '2.364e-05', 'epoch': '0.9127'}
[text-trainer] {'loss': '1.683', 'grad_norm': '2.421', 'learning_rate': '2.329e-05', 'epoch': '0.9171'}
[text-trainer] {'loss': '1.65', 'grad_norm': '2.098', 'learning_rate': '2.295e-05', 'epoch': '0.9215'}
[text-trainer] {'loss': '1.584', 'grad_norm': '3.363', 'learning_rate': '2.263e-05', 'epoch': '0.9259'}
[text-trainer] {'loss': '1.251', 'grad_norm': '1.254', 'learning_rate': '2.233e-05', 'epoch': '0.9303'}
[text-trainer] {'loss': '0.8941', 'grad_norm': '1.668', 'learning_rate': '2.205e-05', 'epoch': '0.9347'}
[text-trainer] {'loss': '1.109', 'grad_norm': '2.618', 'learning_rate': '2.179e-05', 'epoch': '0.9392'}
[text-trainer] {'loss': '1.162', 'grad_norm': '1.61', 'learning_rate': '2.154e-05', 'epoch': '0.9436'}
[text-trainer] {'loss': '1.161', 'grad_norm': '1.887', 'learning_rate': '2.132e-05', 'epoch': '0.948'}
[text-trainer] {'loss': '1.647', 'grad_norm': '2.124', 'learning_rate': '2.111e-05', 'epoch': '0.9524'}
[text-trainer] {'loss': '1.694', 'grad_norm': '2.027', 'learning_rate': '2.091e-05', 'epoch': '0.9568'}
[text-trainer] {'loss': '1.551', 'grad_norm': '2.15', 'learning_rate': '2.074e-05', 'epoch': '0.9612'}
[text-trainer] {'loss': '1.484', 'grad_norm': '2.4', 'learning_rate': '2.059e-05', 'epoch': '0.9656'}
[text-trainer] {'loss': '1.38', 'grad_norm': '2.971', 'learning_rate': '2.045e-05', 'epoch': '0.97'}
[text-trainer] {'loss': '1.343', 'grad_norm': '1.035', 'learning_rate': '2.033e-05', 'epoch': '0.9744'}
[text-trainer] {'loss': '0.9852', 'grad_norm': '1.587', 'learning_rate': '2.023e-05', 'epoch': '0.9788'}
[text-trainer] {'loss': '1.15', 'grad_norm': '2.05', 'learning_rate': '2.015e-05', 'epoch': '0.9832'}
[text-trainer] {'loss': '1.152', 'grad_norm': '1.717', 'learning_rate': '2.008e-05', 'epoch': '0.9877'}
[text-trainer] {'loss': '1.558', 'grad_norm': '1.68', 'learning_rate': '2.004e-05', 'epoch': '0.9921'}
[text-trainer] {'loss': '1.483', 'grad_norm': '2.034', 'learning_rate': '2.001e-05', 'epoch': '0.9965'}
[text-trainer] [sft_v2] sft_v2_eval {'step': 1134, 'dev_loss': 1.367285, 'best': 1.367285, 'eval_s': 6.8, 'pool': 3, 'improved': True}
[text-trainer] {'train_runtime': '347.6', 'train_samples_per_second': '52.17', 'train_steps_per_second': '3.262', 'train_loss': '1.45', 'epoch': '1'}
[text-trainer] [sft_v2] sft_v2_phase_end {'phase': 0, 'steps': 1134, 'planned': 1134, 'epochs_done': 1.001, 't_per_step_measured': 0.288, 'best': 1.367285, 'best_step': 1134, 'remaining_s': 3192.8}
[text-trainer] [sft_v2] sft_v2_plan {'phase': 1, 'lr': 0.0001, 't_per_step': 0.288255, 'epochs': 1.999, 'total_steps': 2265, 'warmup': 67, 'eval_every': 141, 'window_s': 3094.0, 'epochs_done': 1.001}
[text-trainer] {'loss': '0.9114', 'grad_norm': '0.8527', 'learning_rate': '5.97e-06', 'epoch': '0.004409'}
[text-trainer] {'loss': '0.814', 'grad_norm': '1.304', 'learning_rate': '1.343e-05', 'epoch': '0.008818'}
[text-trainer] {'loss': '0.7208', 'grad_norm': '1.251', 'learning_rate': '2.09e-05', 'epoch': '0.01323'}
[text-trainer] {'loss': '1.178', 'grad_norm': '1.677', 'learning_rate': '2.836e-05', 'epoch': '0.01764'}
[text-trainer] {'loss': '0.9786', 'grad_norm': '1.482', 'learning_rate': '3.582e-05', 'epoch': '0.02205'}
[text-trainer] {'loss': '1.145', 'grad_norm': '2.13', 'learning_rate': '4.328e-05', 'epoch': '0.02646'}
[text-trainer] {'loss': '1.307', 'grad_norm': '1.953', 'learning_rate': '5.075e-05', 'epoch': '0.03086'}
[text-trainer] {'loss': '1.25', 'grad_norm': '1.866', 'learning_rate': '5.821e-05', 'epoch': '0.03527'}
[text-trainer] {'loss': '1.106', 'grad_norm': '2.213', 'learning_rate': '6.567e-05', 'epoch': '0.03968'}
[text-trainer] {'loss': '1.207', 'grad_norm': '2.616', 'learning_rate': '7.313e-05', 'epoch': '0.04409'}
[text-trainer] {'loss': '0.8241', 'grad_norm': '1.685', 'learning_rate': '8.06e-05', 'epoch': '0.0485'}
[text-trainer] {'loss': '0.8186', 'grad_norm': '2.159', 'learning_rate': '8.806e-05', 'epoch': '0.05291'}
[text-trainer] {'loss': '0.7492', 'grad_norm': '1.581', 'learning_rate': '9.552e-05', 'epoch': '0.05732'}
[text-trainer] {'loss': '0.8277', 'grad_norm': '1.862', 'learning_rate': '0.0001', 'epoch': '0.06173'}
[text-trainer] {'loss': '0.804', 'grad_norm': '1.864', 'learning_rate': '0.0001', 'epoch': '0.06614'}
[text-trainer] {'loss': '1.186', 'grad_norm': '2.263', 'learning_rate': '9.999e-05', 'epoch': '0.07055'}
[text-trainer] {'loss': '1.396', 'grad_norm': '2.292', 'learning_rate': '9.999e-05', 'epoch': '0.07496'}
[text-trainer] {'loss': '1.35', 'grad_norm': '2.382', 'learning_rate': '9.998e-05', 'epoch': '0.07937'}
[text-trainer] {'loss': '1.043', 'grad_norm': '1.902', 'learning_rate': '9.997e-05', 'epoch': '0.08377'}
[text-trainer] {'loss': '1.065', 'grad_norm': '3.644', 'learning_rate': '9.995e-05', 'epoch': '0.08818'}
[text-trainer] {'loss': '1.066', 'grad_norm': '1.847', 'learning_rate': '9.994e-05', 'epoch': '0.09259'}
[text-trainer] {'loss': '0.7661', 'grad_norm': '1.513', 'learning_rate': '9.992e-05', 'epoch': '0.097'}
[text-trainer] {'loss': '0.6996', 'grad_norm': '1.871', 'learning_rate': '9.99e-05', 'epoch': '0.1014'}
[text-trainer] {'loss': '0.9249', 'grad_norm': '1.909', 'learning_rate': '9.988e-05', 'epoch': '0.1058'}
[text-trainer] {'loss': '1.004', 'grad_norm': '2.264', 'learning_rate': '9.985e-05', 'epoch': '0.1102'}
[text-trainer] {'loss': '1.31', 'grad_norm': '2.022', 'learning_rate': '9.982e-05', 'epoch': '0.1146'}
[text-trainer] {'loss': '1.148', 'grad_norm': '2.215', 'learning_rate': '9.979e-05', 'epoch': '0.119'}
[text-trainer] {'loss': '1.276', 'grad_norm': '2.554', 'learning_rate': '9.976e-05', 'epoch': '0.1235'}
[text-trainer] [sft_v2] sft_v2_eval {'step': 1275, 'dev_loss': 1.399796, 'best': 1.367285, 'eval_s': 6.5, 'pool': 4, 'improved': False}
[text-trainer] [sft_v2] sft_v2_eval_governor {'eval_every': 380, 'eval_s': 6.5}
[text-trainer] {'loss': '0.9385', 'grad_norm': '2.234', 'learning_rate': '9.973e-05', 'epoch': '0.1279'}
[text-trainer] {'loss': '1.07', 'grad_norm': '2.763', 'learning_rate': '9.969e-05', 'epoch': '0.1323'}
[text-trainer] {'loss': '1.041', 'grad_norm': '1.827', 'learning_rate': '9.965e-05', 'epoch': '0.1367'}
[text-trainer] {'loss': '0.743', 'grad_norm': '1.973', 'learning_rate': '9.961e-05', 'epoch': '0.1411'}
[text-trainer] {'loss': '1.105', 'grad_norm': '5.535', 'learning_rate': '9.957e-05', 'epoch': '0.1455'}
[text-trainer] {'loss': '0.9056', 'grad_norm': '2.224', 'learning_rate': '9.952e-05', 'epoch': '0.1499'}
[text-trainer] {'loss': '0.9107', 'grad_norm': '2.087', 'learning_rate': '9.948e-05', 'epoch': '0.1543'}
[text-trainer] {'loss': '1.094', 'grad_norm': '2.12', 'learning_rate': '9.943e-05', 'epoch': '0.1587'}
[text-trainer] {'loss': '1.335', 'grad_norm': '2.295', 'learning_rate': '9.937e-05', 'epoch': '0.1631'}
[text-trainer] {'loss': '1.183', 'grad_norm': '2.037', 'learning_rate': '9.932e-05', 'epoch': '0.1675'}
[text-trainer] {'loss': '1.073', 'grad_norm': '1.996', 'learning_rate': '9.926e-05', 'epoch': '0.172'}
[text-trainer] {'loss': '1.12', 'grad_norm': '3.379', 'learning_rate': '9.92e-05', 'epoch': '0.1764'}
[text-trainer] {'loss': '0.8448', 'grad_norm': '1.72', 'learning_rate': '9.914e-05', 'epoch': '0.1808'}
[text-trainer] {'loss': '0.6193', 'grad_norm': '1.648', 'learning_rate': '9.908e-05', 'epoch': '0.1852'}
[text-trainer] {'loss': '1.051', 'grad_norm': '2.008', 'learning_rate': '9.901e-05', 'epoch': '0.1896'}
[text-trainer] {'loss': '0.6797', 'grad_norm': '1.589', 'learning_rate': '9.894e-05', 'epoch': '0.194'}
[text-trainer] {'loss': '0.7863', 'grad_norm': '1.403', 'learning_rate': '9.887e-05', 'epoch': '0.1984'}
[text-trainer] {'loss': '0.9972', 'grad_norm': '2.12', 'learning_rate': '9.88e-05', 'epoch': '0.2028'}
[text-trainer] {'loss': '0.9672', 'grad_norm': '2.312', 'learning_rate': '9.873e-05', 'epoch': '0.2072'}
[text-trainer] {'loss': '1.17', 'grad_norm': '2.17', 'learning_rate': '9.865e-05', 'epoch': '0.2116'}
[text-trainer] {'loss': '1.155', 'grad_norm': '2.05', 'learning_rate': '9.857e-05', 'epoch': '0.216'}
[text-trainer] {'loss': '1.136', 'grad_norm': '4.241', 'learning_rate': '9.849e-05', 'epoch': '0.2205'}
[text-trainer] {'loss': '1.018', 'grad_norm': '1.032', 'learning_rate': '9.841e-05', 'epoch': '0.2249'}
[text-trainer] {'loss': '0.6702', 'grad_norm': '1.842', 'learning_rate': '9.832e-05', 'epoch': '0.2293'}
[text-trainer] {'loss': '0.8271', 'grad_norm': '2.376', 'learning_rate': '9.823e-05', 'epoch': '0.2337'}
[text-trainer] {'loss': '0.9217', 'grad_norm': '2.082', 'learning_rate': '9.814e-05', 'epoch': '0.2381'}
[text-trainer] {'loss': '0.8278', 'grad_norm': '2.266', 'learning_rate': '9.805e-05', 'epoch': '0.2425'}
[text-trainer] {'loss': '0.9879', 'grad_norm': '2.067', 'learning_rate': '9.795e-05', 'epoch': '0.2469'}
[text-trainer] {'loss': '1.237', 'grad_norm': '2.347', 'learning_rate': '9.786e-05', 'epoch': '0.2513'}
[text-trainer] {'loss': '1.343', 'grad_norm': '2.411', 'learning_rate': '9.776e-05', 'epoch': '0.2557'}
[text-trainer] {'loss': '1.004', 'grad_norm': '1.849', 'learning_rate': '9.766e-05', 'epoch': '0.2601'}
[text-trainer] {'loss': '1.207', 'grad_norm': '3.298', 'learning_rate': '9.755e-05', 'epoch': '0.2646'}
[text-trainer] {'loss': '0.7918', 'grad_norm': '1.94', 'learning_rate': '9.745e-05', 'epoch': '0.269'}
[text-trainer] {'loss': '0.7922', 'grad_norm': '2.352', 'learning_rate': '9.734e-05', 'epoch': '0.2734'}
[text-trainer] {'loss': '0.9152', 'grad_norm': '2.197', 'learning_rate': '9.723e-05', 'epoch': '0.2778'}
[text-trainer] {'loss': '0.9678', 'grad_norm': '1.804', 'learning_rate': '9.712e-05', 'epoch': '0.2822'}
[text-trainer] {'loss': '0.9925', 'grad_norm': '2.173', 'learning_rate': '9.7e-05', 'epoch': '0.2866'}
[text-trainer] {'loss': '1.113', 'grad_norm': '2.598', 'learning_rate': '9.689e-05', 'epoch': '0.291'}
[text-trainer] {'loss': '1.315', 'grad_norm': '2.512', 'learning_rate': '9.677e-05', 'epoch': '0.2954'}
[text-trainer] {'loss': '1.214', 'grad_norm': '1.979', 'learning_rate': '9.665e-05', 'epoch': '0.2998'}
[text-trainer] {'loss': '1.142', 'grad_norm': '2.113', 'learning_rate': '9.653e-05', 'epoch': '0.3042'}
[text-trainer] {'loss': '1.045', 'grad_norm': '3.342', 'learning_rate': '9.64e-05', 'epoch': '0.3086'}
[text-trainer] {'loss': '0.6968', 'grad_norm': '1.605', 'learning_rate': '9.627e-05', 'epoch': '0.3131'}
[text-trainer] {'loss': '0.6473', 'grad_norm': '1.879', 'learning_rate': '9.614e-05', 'epoch': '0.3175'}
[text-trainer] {'loss': '0.8298', 'grad_norm': '2.214', 'learning_rate': '9.601e-05', 'epoch': '0.3219'}
[text-trainer] {'loss': '0.855', 'grad_norm': '2.323', 'learning_rate': '9.588e-05', 'epoch': '0.3263'}
[text-trainer] {'loss': '0.7999', 'grad_norm': '1.77', 'learning_rate': '9.574e-05', 'epoch': '0.3307'}
[text-trainer] [sft_v2] sft_v2_eval {'step': 1514, 'dev_loss': 1.397483, 'best': 1.367285, 'eval_s': 6.7, 'pool': 5, 'improved': False}
[text-trainer] {'loss': '1.106', 'grad_norm': '2.369', 'learning_rate': '9.561e-05', 'epoch': '0.3351'}
[text-trainer] {'loss': '1.117', 'grad_norm': '2.595', 'learning_rate': '9.547e-05', 'epoch': '0.3395'}
[text-trainer] {'loss': '1.266', 'grad_norm': '2.374', 'learning_rate': '9.533e-05', 'epoch': '0.3439'}
[text-trainer] {'loss': '1.114', 'grad_norm': '2.339', 'learning_rate': '9.518e-05', 'epoch': '0.3483'}
[text-trainer] {'loss': '0.8855', 'grad_norm': '2.858', 'learning_rate': '9.504e-05', 'epoch': '0.3527'}
[text-trainer] {'loss': '1.028', 'grad_norm': '1.984', 'learning_rate': '9.489e-05', 'epoch': '0.3571'}
[text-trainer] {'loss': '0.7486', 'grad_norm': '2.447', 'learning_rate': '9.474e-05', 'epoch': '0.3616'}
[text-trainer] {'loss': '0.8369', 'grad_norm': '2.107', 'learning_rate': '9.459e-05', 'epoch': '0.366'}
[text-trainer] {'loss': '0.923', 'grad_norm': '1.743', 'learning_rate': '9.443e-05', 'epoch': '0.3704'}
[text-trainer] {'loss': '0.9704', 'grad_norm': '2.912', 'learning_rate': '9.428e-05', 'epoch': '0.3748'}
[text-trainer] {'loss': '1.183', 'grad_norm': '2.36', 'learning_rate': '9.412e-05', 'epoch': '0.3792'}
[text-trainer] {'loss': '1.271', 'grad_norm': '3.313', 'learning_rate': '9.396e-05', 'epoch': '0.3836'}
[text-trainer] {'loss': '1.181', 'grad_norm': '2.352', 'learning_rate': '9.38e-05', 'epoch': '0.388'}
[text-trainer] {'loss': '1.338', 'grad_norm': '2.384', 'learning_rate': '9.363e-05', 'epoch': '0.3924'}
[text-trainer] {'loss': '1.291', 'grad_norm': '3.734', 'learning_rate': '9.347e-05', 'epoch': '0.3968'}
[text-trainer] {'loss': '0.8158', 'grad_norm': '1.833', 'learning_rate': '9.33e-05', 'epoch': '0.4012'}
[text-trainer] {'loss': '0.8425', 'grad_norm': '2.324', 'learning_rate': '9.313e-05', 'epoch': '0.4056'}
[text-trainer] {'loss': '0.7122', 'grad_norm': '1.71', 'learning_rate': '9.296e-05', 'epoch': '0.4101'}
[text-trainer] {'loss': '0.8102', 'grad_norm': '2.503', 'learning_rate': '9.279e-05', 'epoch': '0.4145'}
[text-trainer] {'loss': '0.9035', 'grad_norm': '2.807', 'learning_rate': '9.261e-05', 'epoch': '0.4189'}
[text-trainer] {'loss': '0.9766', 'grad_norm': '2.018', 'learning_rate': '9.243e-05', 'epoch': '0.4233'}
[text-trainer] {'loss': '1.268', 'grad_norm': '2.726', 'learning_rate': '9.225e-05', 'epoch': '0.4277'}
[text-trainer] {'loss': '1.299', 'grad_norm': '2.62', 'learning_rate': '9.207e-05', 'epoch': '0.4321'}
[text-trainer] {'loss': '1.194', 'grad_norm': '2.537', 'learning_rate': '9.189e-05', 'epoch': '0.4365'}
[text-trainer] {'loss': '1.065', 'grad_norm': '3.772', 'learning_rate': '9.171e-05', 'epoch': '0.4409'}
[text-trainer] {'loss': '0.8436', 'grad_norm': '1.273', 'learning_rate': '9.152e-05', 'epoch': '0.4453'}
[text-trainer] {'loss': '0.7006', 'grad_norm': '2.169', 'learning_rate': '9.133e-05', 'epoch': '0.4497'}
[text-trainer] {'loss': '0.7517', 'grad_norm': '1.623', 'learning_rate': '9.114e-05', 'epoch': '0.4541'}
[text-trainer] {'loss': '0.9172', 'grad_norm': '2.205', 'learning_rate': '9.095e-05', 'epoch': '0.4586'}
[text-trainer] {'loss': '0.9561', 'grad_norm': '2.664', 'learning_rate': '9.075e-05', 'epoch': '0.463'}
[text-trainer] {'loss': '1.028', 'grad_norm': '2.404', 'learning_rate': '9.056e-05', 'epoch': '0.4674'}
[text-trainer] {'loss': '1.396', 'grad_norm': '2.427', 'learning_rate': '9.036e-05', 'epoch': '0.4718'}
[text-trainer] {'loss': '1.295', 'grad_norm': '2.634', 'learning_rate': '9.016e-05', 'epoch': '0.4762'}
[text-trainer] {'loss': '1.28', 'grad_norm': '2.548', 'learning_rate': '8.996e-05', 'epoch': '0.4806'}
[text-trainer] {'loss': '0.8926', 'grad_norm': '3.416', 'learning_rate': '8.975e-05', 'epoch': '0.485'}
[text-trainer] {'loss': '0.8663', 'grad_norm': '1.765', 'learning_rate': '8.955e-05', 'epoch': '0.4894'}
[text-trainer] {'loss': '0.7161', 'grad_norm': '2.249', 'learning_rate': '8.934e-05', 'epoch': '0.4938'}
[text-trainer] {'loss': '0.816', 'grad_norm': '2.005', 'learning_rate': '8.913e-05', 'epoch': '0.4982'}
[text-trainer] {'loss': '0.9309', 'grad_norm': '2.399', 'learning_rate': '8.892e-05', 'epoch': '0.5026'}
[text-trainer] {'loss': '0.9406', 'grad_norm': '2.111', 'learning_rate': '8.871e-05', 'epoch': '0.5071'}
[text-trainer] {'loss': '0.9384', 'grad_norm': '2.148', 'learning_rate': '8.85e-05', 'epoch': '0.5115'}
[text-trainer] {'loss': '1.218', 'grad_norm': '3.007', 'learning_rate': '8.828e-05', 'epoch': '0.5159'}
[text-trainer] {'loss': '1.216', 'grad_norm': '3.343', 'learning_rate': '8.807e-05', 'epoch': '0.5203'}
[text-trainer] {'loss': '1.064', 'grad_norm': '2.571', 'learning_rate': '8.785e-05', 'epoch': '0.5247'}
[text-trainer] {'loss': '1.079', 'grad_norm': '3.668', 'learning_rate': '8.763e-05', 'epoch': '0.5291'}
[text-trainer] {'loss': '0.8645', 'grad_norm': '1.576', 'learning_rate': '8.74e-05', 'epoch': '0.5335'}
[text-trainer] {'loss': '0.8121', 'grad_norm': '1.708', 'learning_rate': '8.718e-05', 'epoch': '0.5379'}
[text-trainer] {'loss': '0.7811', 'grad_norm': '2.231', 'learning_rate': '8.696e-05', 'epoch': '0.5423'}
[text-trainer] {'loss': '0.769', 'grad_norm': '2.518', 'learning_rate': '8.673e-05', 'epoch': '0.5467'}
[text-trainer] {'loss': '0.907', 'grad_norm': '2.457', 'learning_rate': '8.65e-05', 'epoch': '0.5511'}
[text-trainer] {'loss': '0.9135', 'grad_norm': '2.283', 'learning_rate': '8.627e-05', 'epoch': '0.5556'}
[text-trainer] {'loss': '1.091', 'grad_norm': '2.35', 'learning_rate': '8.604e-05', 'epoch': '0.56'}
[text-trainer] {'loss': '1.017', 'grad_norm': '2.112', 'learning_rate': '8.58e-05', 'epoch': '0.5644'}
[text-trainer] {'loss': '1.19', 'grad_norm': '3.118', 'learning_rate': '8.557e-05', 'epoch': '0.5688'}
[text-trainer] {'loss': '1.149', 'grad_norm': '4.159', 'learning_rate': '8.533e-05', 'epoch': '0.5732'}
[text-trainer] {'loss': '1.093', 'grad_norm': '2.564', 'learning_rate': '8.509e-05', 'epoch': '0.5776'}
[text-trainer] {'loss': '0.6481', 'grad_norm': '1.527', 'learning_rate': '8.486e-05', 'epoch': '0.582'}
[text-trainer] {'loss': '0.7934', 'grad_norm': '2.132', 'learning_rate': '8.461e-05', 'epoch': '0.5864'}
[text-trainer] {'loss': '0.9092', 'grad_norm': '3.084', 'learning_rate': '8.437e-05', 'epoch': '0.5908'}
[text-trainer] {'loss': '0.8932', 'grad_norm': '1.839', 'learning_rate': '8.413e-05', 'epoch': '0.5952'}
[text-trainer] {'loss': '0.8468', 'grad_norm': '1.863', 'learning_rate': '8.388e-05', 'epoch': '0.5996'}
[text-trainer] {'loss': '1.335', 'grad_norm': '2.915', 'learning_rate': '8.363e-05', 'epoch': '0.6041'}
[text-trainer] {'loss': '1.221', 'grad_norm': '2.83', 'learning_rate': '8.339e-05', 'epoch': '0.6085'}
[text-trainer] {'loss': '1.252', 'grad_norm': '3.265', 'learning_rate': '8.314e-05', 'epoch': '0.6129'}
[text-trainer] {'loss': '1.098', 'grad_norm': '4.548', 'learning_rate': '8.288e-05', 'epoch': '0.6173'}
[text-trainer] {'loss': '0.8388', 'grad_norm': '1.945', 'learning_rate': '8.263e-05', 'epoch': '0.6217'}
[text-trainer] {'loss': '0.6181', 'grad_norm': '1.435', 'learning_rate': '8.238e-05', 'epoch': '0.6261'}
[text-trainer] {'loss': '0.7508', 'grad_norm': '2.012', 'learning_rate': '8.212e-05', 'epoch': '0.6305'}
[text-trainer] {'loss': '0.8878', 'grad_norm': '2.073', 'learning_rate': '8.186e-05', 'epoch': '0.6349'}
[text-trainer] {'loss': '1.02', 'grad_norm': '2.664', 'learning_rate': '8.161e-05', 'epoch': '0.6393'}
[text-trainer] {'loss': '1.079', 'grad_norm': '2.102', 'learning_rate': '8.135e-05', 'epoch': '0.6437'}
[text-trainer] {'loss': '1.224', 'grad_norm': '2.806', 'learning_rate': '8.109e-05', 'epoch': '0.6481'}
[text-trainer] {'loss': '1.25', 'grad_norm': '2.756', 'learning_rate': '8.082e-05', 'epoch': '0.6526'}
[text-trainer] {'loss': '1.186', 'grad_norm': '2.722', 'learning_rate': '8.056e-05', 'epoch': '0.657'}
[text-trainer] {'loss': '0.6824', 'grad_norm': '2.459', 'learning_rate': '8.029e-05', 'epoch': '0.6614'}
[text-trainer] {'loss': '1.024', 'grad_norm': '1.856', 'learning_rate': '8.003e-05', 'epoch': '0.6658'}
[text-trainer] [sft_v2] sft_v2_eval {'step': 1894, 'dev_loss': 1.328671, 'best': 1.328671, 'eval_s': 6.7, 'pool': 6, 'improved': True}
[text-trainer] {'loss': '0.7622', 'grad_norm': '2.148', 'learning_rate': '7.976e-05', 'epoch': '0.6702'}
[text-trainer] {'loss': '0.7185', 'grad_norm': '2.119', 'learning_rate': '7.949e-05', 'epoch': '0.6746'}
[text-trainer] {'loss': '0.9567', 'grad_norm': '2.39', 'learning_rate': '7.922e-05', 'epoch': '0.679'}
[text-trainer] {'loss': '1.035', 'grad_norm': '2.314', 'learning_rate': '7.895e-05', 'epoch': '0.6834'}
[text-trainer] {'loss': '1.15', 'grad_norm': '2.65', 'learning_rate': '7.868e-05', 'epoch': '0.6878'}
[text-trainer] {'loss': '1.09', 'grad_norm': '2.015', 'learning_rate': '7.84e-05', 'epoch': '0.6922'}
[text-trainer] {'loss': '1.153', 'grad_norm': '2.593', 'learning_rate': '7.813e-05', 'epoch': '0.6966'}
[text-trainer] {'loss': '1.016', 'grad_norm': '2.376', 'learning_rate': '7.785e-05', 'epoch': '0.7011'}
[text-trainer] {'loss': '0.9384', 'grad_norm': '3.016', 'learning_rate': '7.757e-05', 'epoch': '0.7055'}
[text-trainer] {'loss': '0.9301', 'grad_norm': '2.265', 'learning_rate': '7.73e-05', 'epoch': '0.7099'}
[text-trainer] {'loss': '0.7588', 'grad_norm': '2.402', 'learning_rate': '7.702e-05', 'epoch': '0.7143'}
[text-trainer] {'loss': '0.7994', 'grad_norm': '1.921', 'learning_rate': '7.674e-05', 'epoch': '0.7187'}
[text-trainer] {'loss': '0.8267', 'grad_norm': '1.36', 'learning_rate': '7.645e-05', 'epoch': '0.7231'}
[text-trainer] {'loss': '0.8069', 'grad_norm': '1.982', 'learning_rate': '7.617e-05', 'epoch': '0.7275'}
[text-trainer] {'loss': '1.129', 'grad_norm': '2.81', 'learning_rate': '7.589e-05', 'epoch': '0.7319'}
[text-trainer] {'loss': '1.213', 'grad_norm': '2.648', 'learning_rate': '7.56e-05', 'epoch': '0.7363'}
[text-trainer] {'loss': '1.335', 'grad_norm': '2.249', 'learning_rate': '7.531e-05', 'epoch': '0.7407'}
[text-trainer] {'loss': '1.25', 'grad_norm': '2.938', 'learning_rate': '7.503e-05', 'epoch': '0.7451'}
[text-trainer] {'loss': '1.158', 'grad_norm': '5.098', 'learning_rate': '7.474e-05', 'epoch': '0.7496'}
[text-trainer] {'loss': '0.8459', 'grad_norm': '1.689', 'learning_rate': '7.445e-05', 'epoch': '0.754'}
[text-trainer] {'loss': '0.6267', 'grad_norm': '1.422', 'learning_rate': '7.416e-05', 'epoch': '0.7584'}
[text-trainer] {'loss': '0.7276', 'grad_norm': '2.023', 'learning_rate': '7.387e-05', 'epoch': '0.7628'}
[text-trainer] {'loss': '0.8102', 'grad_norm': '1.769', 'learning_rate': '7.358e-05', 'epoch': '0.7672'}
[text-trainer] {'loss': '0.913', 'grad_norm': '2.082', 'learning_rate': '7.328e-05', 'epoch': '0.7716'}
[text-trainer] {'loss': '1.115', 'grad_norm': '2.973', 'learning_rate': '7.299e-05', 'epoch': '0.776'}
[text-trainer] {'loss': '1.064', 'grad_norm': '2.65', 'learning_rate': '7.269e-05', 'epoch': '0.7804'}
[text-trainer] {'loss': '1.197', 'grad_norm': '2.901', 'learning_rate': '7.24e-05', 'epoch': '0.7848'}
[text-trainer] {'loss': '1.128', 'grad_norm': '2.824', 'learning_rate': '7.21e-05', 'epoch': '0.7892'}
[text-trainer] {'loss': '0.9178', 'grad_norm': '3.156', 'learning_rate': '7.18e-05', 'epoch': '0.7937'}
[text-trainer] {'loss': '0.5497', 'grad_norm': '1.696', 'learning_rate': '7.151e-05', 'epoch': '0.7981'}
[text-trainer] {'loss': '0.6003', 'grad_norm': '1.945', 'learning_rate': '7.121e-05', 'epoch': '0.8025'}
[text-trainer] {'loss': '0.8934', 'grad_norm': '1.731', 'learning_rate': '7.091e-05', 'epoch': '0.8069'}
[text-trainer] {'loss': '0.9664', 'grad_norm': '2.077', 'learning_rate': '7.061e-05', 'epoch': '0.8113'}
[text-trainer] {'loss': '0.9641', 'grad_norm': '2.299', 'learning_rate': '7.03e-05', 'epoch': '0.8157'}
[text-trainer] {'loss': '1.081', 'grad_norm': '2.457', 'learning_rate': '7e-05', 'epoch': '0.8201'}
[text-trainer] {'loss': '1.257', 'grad_norm': '2.926', 'learning_rate': '6.97e-05', 'epoch': '0.8245'}
[text-trainer] {'loss': '1.166', 'grad_norm': '2.679', 'learning_rate': '6.939e-05', 'epoch': '0.8289'}
[text-trainer] {'loss': '1.277', 'grad_norm': '2.262', 'learning_rate': '6.909e-05', 'epoch': '0.8333'}
[text-trainer] {'loss': '1.17', 'grad_norm': '4.206', 'learning_rate': '6.878e-05', 'epoch': '0.8377'}
[text-trainer] {'loss': '1.007', 'grad_norm': '1.807', 'learning_rate': '6.848e-05', 'epoch': '0.8422'}
[text-trainer] {'loss': '0.7326', 'grad_norm': '1.746', 'learning_rate': '6.817e-05', 'epoch': '0.8466'}
[text-trainer] {'loss': '0.6854', 'grad_norm': '1.98', 'learning_rate': '6.786e-05', 'epoch': '0.851'}
[text-trainer] {'loss': '1.05', 'grad_norm': '2.473', 'learning_rate': '6.755e-05', 'epoch': '0.8554'}
[text-trainer] {'loss': '1.014', 'grad_norm': '2.526', 'learning_rate': '6.725e-05', 'epoch': '0.8598'}
[text-trainer] {'loss': '1.024', 'grad_norm': '2.314', 'learning_rate': '6.694e-05', 'epoch': '0.8642'}
[text-trainer] {'loss': '1.004', 'grad_norm': '2.137', 'learning_rate': '6.663e-05', 'epoch': '0.8686'}
[text-trainer] {'loss': '1.247', 'grad_norm': '2.213', 'learning_rate': '6.632e-05', 'epoch': '0.873'}
[text-trainer] {'loss': '1.181', 'grad_norm': '2.896', 'learning_rate': '6.6e-05', 'epoch': '0.8774'}
[text-trainer] {'loss': '1.114', 'grad_norm': '4.979', 'learning_rate': '6.569e-05', 'epoch': '0.8818'}
[text-trainer] {'loss': '1.181', 'grad_norm': '2.685', 'learning_rate': '6.538e-05', 'epoch': '0.8862'}
[text-trainer] {'loss': '0.6436', 'grad_norm': '1.92', 'learning_rate': '6.507e-05', 'epoch': '0.8907'}
[text-trainer] {'loss': '0.7326', 'grad_norm': '1.551', 'learning_rate': '6.475e-05', 'epoch': '0.8951'}
[text-trainer] {'loss': '0.8383', 'grad_norm': '2.353', 'learning_rate': '6.444e-05', 'epoch': '0.8995'}
[text-trainer] {'loss': '0.9479', 'grad_norm': '2.413', 'learning_rate': '6.413e-05', 'epoch': '0.9039'}
[text-trainer] {'loss': '1.005', 'grad_norm': '2.323', 'learning_rate': '6.381e-05', 'epoch': '0.9083'}
[text-trainer] {'loss': '1.219', 'grad_norm': '2.834', 'learning_rate': '6.35e-05', 'epoch': '0.9127'}
[text-trainer] {'loss': '1.238', 'grad_norm': '2.702', 'learning_rate': '6.318e-05', 'epoch': '0.9171'}
[text-trainer] {'loss': '1.155', 'grad_norm': '2.853', 'learning_rate': '6.286e-05', 'epoch': '0.9215'}
[text-trainer] {'loss': '1.121', 'grad_norm': '3.623', 'learning_rate': '6.255e-05', 'epoch': '0.9259'}
[text-trainer] {'loss': '0.9317', 'grad_norm': '2.163', 'learning_rate': '6.223e-05', 'epoch': '0.9303'}
[text-trainer] {'loss': '0.5664', 'grad_norm': '1.579', 'learning_rate': '6.191e-05', 'epoch': '0.9347'}
[text-trainer] {'loss': '0.5544', 'grad_norm': '1.814', 'learning_rate': '6.159e-05', 'epoch': '0.9392'}
[text-trainer] {'loss': '0.925', 'grad_norm': '2.437', 'learning_rate': '6.128e-05', 'epoch': '0.9436'}
[text-trainer] {'loss': '1.007', 'grad_norm': '2.77', 'learning_rate': '6.096e-05', 'epoch': '0.948'}
[text-trainer] {'loss': '0.9473', 'grad_norm': '2.512', 'learning_rate': '6.064e-05', 'epoch': '0.9524'}
[text-trainer] {'loss': '1.241', 'grad_norm': '3.105', 'learning_rate': '6.032e-05', 'epoch': '0.9568'}
[text-trainer] {'loss': '1.146', 'grad_norm': '2.49', 'learning_rate': '6e-05', 'epoch': '0.9612'}
[text-trainer] {'loss': '1.043', 'grad_norm': '2.268', 'learning_rate': '5.968e-05', 'epoch': '0.9656'}
[text-trainer] {'loss': '0.9549', 'grad_norm': '3.09', 'learning_rate': '5.936e-05', 'epoch': '0.97'}
[text-trainer] {'loss': '0.6701', 'grad_norm': '1.707', 'learning_rate': '5.904e-05', 'epoch': '0.9744'}
[text-trainer] {'loss': '0.7686', 'grad_norm': '1.597', 'learning_rate': '5.872e-05', 'epoch': '0.9788'}
[text-trainer] {'loss': '0.8847', 'grad_norm': '3.019', 'learning_rate': '5.84e-05', 'epoch': '0.9832'}
[text-trainer] {'loss': '1.215', 'grad_norm': '2.702', 'learning_rate': '5.808e-05', 'epoch': '0.9877'}
[text-trainer] {'loss': '1.129', 'grad_norm': '2.472', 'learning_rate': '5.776e-05', 'epoch': '0.9921'}
[text-trainer] {'loss': '1.103', 'grad_norm': '2.237', 'learning_rate': '5.744e-05', 'epoch': '0.9965'}
[text-trainer] {'loss': '1.076', 'grad_norm': '2.014', 'learning_rate': '5.712e-05', 'epoch': '1.001'}
[text-trainer] [sft_v2] sft_v2_eval {'step': 2274, 'dev_loss': 1.272726, 'best': 1.272726, 'eval_s': 6.7, 'pool': 7, 'improved': True}
[text-trainer] {'loss': '0.4603', 'grad_norm': '1.633', 'learning_rate': '5.68e-05', 'epoch': '1.005'}
[text-trainer] {'loss': '0.424', 'grad_norm': '1.736', 'learning_rate': '5.648e-05', 'epoch': '1.01'}
[text-trainer] {'loss': '0.5176', 'grad_norm': '2.244', 'learning_rate': '5.616e-05', 'epoch': '1.014'}
[text-trainer] {'loss': '0.5341', 'grad_norm': '4.499', 'learning_rate': '5.584e-05', 'epoch': '1.019'}
[text-trainer] {'loss': '0.5317', 'grad_norm': '2.42', 'learning_rate': '5.551e-05', 'epoch': '1.023'}
[text-trainer] {'loss': '0.637', 'grad_norm': '2.75', 'learning_rate': '5.519e-05', 'epoch': '1.027'}
[text-trainer] {'loss': '0.7098', 'grad_norm': '2.933', 'learning_rate': '5.487e-05', 'epoch': '1.032'}
[text-trainer] {'loss': '0.6608', 'grad_norm': '2.686', 'learning_rate': '5.455e-05', 'epoch': '1.036'}
[text-trainer] {'loss': '0.6703', 'grad_norm': '1.926', 'learning_rate': '5.423e-05', 'epoch': '1.041'}
[text-trainer] {'loss': '0.5757', 'grad_norm': '2.935', 'learning_rate': '5.391e-05', 'epoch': '1.045'}
[text-trainer] {'loss': '0.4662', 'grad_norm': '1.744', 'learning_rate': '5.359e-05', 'epoch': '1.049'}
[text-trainer] {'loss': '0.4256', 'grad_norm': '1.865', 'learning_rate': '5.327e-05', 'epoch': '1.054'}
[text-trainer] {'loss': '0.5847', 'grad_norm': '1.991', 'learning_rate': '5.294e-05', 'epoch': '1.058'}
[text-trainer] {'loss': '0.5566', 'grad_norm': '2.97', 'learning_rate': '5.262e-05', 'epoch': '1.063'}
[text-trainer] {'loss': '0.611', 'grad_norm': '2.356', 'learning_rate': '5.23e-05', 'epoch': '1.067'}
[text-trainer] {'loss': '0.6922', 'grad_norm': '2.649', 'learning_rate': '5.198e-05', 'epoch': '1.071'}
[text-trainer] {'loss': '0.8328', 'grad_norm': '3.315', 'learning_rate': '5.166e-05', 'epoch': '1.076'}
[text-trainer] {'loss': '0.6644', 'grad_norm': '1.747', 'learning_rate': '5.134e-05', 'epoch': '1.08'}
[text-trainer] {'loss': '0.6292', 'grad_norm': '2.722', 'learning_rate': '5.102e-05', 'epoch': '1.085'}
[text-trainer] {'loss': '0.6479', 'grad_norm': '9.399', 'learning_rate': '5.07e-05', 'epoch': '1.089'}
[text-trainer] {'loss': '0.386', 'grad_norm': '1.951', 'learning_rate': '5.038e-05', 'epoch': '1.093'}
[text-trainer] {'loss': '0.4325', 'grad_norm': '1.994', 'learning_rate': '5.006e-05', 'epoch': '1.098'}
[text-trainer] {'loss': '0.4381', 'grad_norm': '1.958', 'learning_rate': '4.974e-05', 'epoch': '1.102'}
[text-trainer] {'loss': '0.4391', 'grad_norm': '2.555', 'learning_rate': '4.942e-05', 'epoch': '1.107'}
[text-trainer] {'loss': '0.3738', 'grad_norm': '2.384', 'learning_rate': '4.911e-05', 'epoch': '1.111'}
[text-trainer] {'loss': '0.7488', 'grad_norm': '2.795', 'learning_rate': '4.879e-05', 'epoch': '1.116'}
[text-trainer] {'loss': '0.7348', 'grad_norm': '3.128', 'learning_rate': '4.847e-05', 'epoch': '1.12'}
[text-trainer] {'loss': '0.7344', 'grad_norm': '2.56', 'learning_rate': '4.815e-05', 'epoch': '1.124'}
[text-trainer] {'loss': '0.6194', 'grad_norm': '2.734', 'learning_rate': '4.783e-05', 'epoch': '1.129'}
[text-trainer] {'loss': '0.4868', 'grad_norm': '2.02', 'learning_rate': '4.752e-05', 'epoch': '1.133'}
[text-trainer] {'loss': '0.3876', 'grad_norm': '2.6', 'learning_rate': '4.72e-05', 'epoch': '1.138'}
[text-trainer] {'loss': '0.3781', 'grad_norm': '2.296', 'learning_rate': '4.688e-05', 'epoch': '1.142'}
[text-trainer] {'loss': '0.401', 'grad_norm': '2.006', 'learning_rate': '4.657e-05', 'epoch': '1.146'}
[text-trainer] {'loss': '0.5601', 'grad_norm': '2.16', 'learning_rate': '4.625e-05', 'epoch': '1.151'}
[text-trainer] {'loss': '0.5049', 'grad_norm': '2.499', 'learning_rate': '4.594e-05', 'epoch': '1.155'}
[text-trainer] {'loss': '0.6632', 'grad_norm': '2.997', 'learning_rate': '4.562e-05', 'epoch': '1.16'}
[text-trainer] {'loss': '0.7277', 'grad_norm': '3.342', 'learning_rate': '4.531e-05', 'epoch': '1.164'}
[text-trainer] {'loss': '0.7189', 'grad_norm': '2.328', 'learning_rate': '4.5e-05', 'epoch': '1.168'}
[text-trainer] {'loss': '0.5674', 'grad_norm': '1.39', 'learning_rate': '4.468e-05', 'epoch': '1.173'}
[text-trainer] {'loss': '0.5346', 'grad_norm': '3.569', 'learning_rate': '4.437e-05', 'epoch': '1.177'}
[text-trainer] {'loss': '0.3632', 'grad_norm': '1.741', 'learning_rate': '4.406e-05', 'epoch': '1.182'}
[text-trainer] {'loss': '0.5242', 'grad_norm': '2.946', 'learning_rate': '4.375e-05', 'epoch': '1.186'}
[text-trainer] {'loss': '0.5732', 'grad_norm': '2.331', 'learning_rate': '4.344e-05', 'epoch': '1.19'}
[text-trainer] {'loss': '0.4379', 'grad_norm': '2.549', 'learning_rate': '4.313e-05', 'epoch': '1.195'}
[text-trainer] {'loss': '0.5492', 'grad_norm': '2.538', 'learning_rate': '4.282e-05', 'epoch': '1.199'}
[text-trainer] {'loss': '0.5957', 'grad_norm': '2.673', 'learning_rate': '4.251e-05', 'epoch': '1.204'}
[text-trainer] {'loss': '0.735', 'grad_norm': '2.773', 'learning_rate': '4.22e-05', 'epoch': '1.208'}
[text-trainer] {'loss': '0.7203', 'grad_norm': '3.032', 'learning_rate': '4.189e-05', 'epoch': '1.213'}
[text-trainer] {'loss': '0.5824', 'grad_norm': '2.962', 'learning_rate': '4.158e-05', 'epoch': '1.217'}
[text-trainer] {'loss': '0.6216', 'grad_norm': '1.884', 'learning_rate': '4.128e-05', 'epoch': '1.221'}
[text-trainer] {'loss': '0.3879', 'grad_norm': '1.635', 'learning_rate': '4.097e-05', 'epoch': '1.226'}
[text-trainer] {'loss': '0.2948', 'grad_norm': '1.862', 'learning_rate': '4.067e-05', 'epoch': '1.23'}
[text-trainer] {'loss': '0.3141', 'grad_norm': '2.26', 'learning_rate': '4.036e-05', 'epoch': '1.235'}
[text-trainer] {'loss': '0.4452', 'grad_norm': '1.832', 'learning_rate': '4.006e-05', 'epoch': '1.239'}
[text-trainer] {'loss': '0.6252', 'grad_norm': '2.789', 'learning_rate': '3.976e-05', 'epoch': '1.243'}
[text-trainer] {'loss': '0.616', 'grad_norm': '2.871', 'learning_rate': '3.945e-05', 'epoch': '1.248'}
[text-trainer] {'loss': '0.6619', 'grad_norm': '2.945', 'learning_rate': '3.915e-05', 'epoch': '1.252'}
[text-trainer] {'loss': '0.7201', 'grad_norm': '3.263', 'learning_rate': '3.885e-05', 'epoch': '1.257'}
[text-trainer] {'loss': '0.5868', 'grad_norm': '2.237', 'learning_rate': '3.855e-05', 'epoch': '1.261'}
[text-trainer] {'loss': '0.611', 'grad_norm': '3.241', 'learning_rate': '3.826e-05', 'epoch': '1.265'}
[text-trainer] {'loss': '0.4587', 'grad_norm': '1.691', 'learning_rate': '3.796e-05', 'epoch': '1.27'}
[text-trainer] {'loss': '0.4494', 'grad_norm': '2.865', 'learning_rate': '3.766e-05', 'epoch': '1.274'}
[text-trainer] {'loss': '0.5234', 'grad_norm': '3.268', 'learning_rate': '3.736e-05', 'epoch': '1.279'}
[text-trainer] {'loss': '0.6043', 'grad_norm': '2.582', 'learning_rate': '3.707e-05', 'epoch': '1.283'}
[text-trainer] {'loss': '0.6018', 'grad_norm': '2.117', 'learning_rate': '3.678e-05', 'epoch': '1.287'}
[text-trainer] {'loss': '0.6086', 'grad_norm': '2.696', 'learning_rate': '3.648e-05', 'epoch': '1.292'}
[text-trainer] {'loss': '0.7169', 'grad_norm': '2.855', 'learning_rate': '3.619e-05', 'epoch': '1.296'}
[text-trainer] {'loss': '0.6888', 'grad_norm': '3.251', 'learning_rate': '3.59e-05', 'epoch': '1.301'}
[text-trainer] {'loss': '0.5069', 'grad_norm': '3.089', 'learning_rate': '3.561e-05', 'epoch': '1.305'}
[text-trainer] {'loss': '0.5648', 'grad_norm': '4.098', 'learning_rate': '3.532e-05', 'epoch': '1.31'}
[text-trainer] {'loss': '0.3708', 'grad_norm': '1.633', 'learning_rate': '3.503e-05', 'epoch': '1.314'}
[text-trainer] {'loss': '0.4664', 'grad_norm': '2.838', 'learning_rate': '3.474e-05', 'epoch': '1.318'}
[text-trainer] {'loss': '0.3593', 'grad_norm': '1.692', 'learning_rate': '3.446e-05', 'epoch': '1.323'}
[text-trainer] {'loss': '0.4274', 'grad_norm': '1.422', 'learning_rate': '3.417e-05', 'epoch': '1.327'}
[text-trainer] {'loss': '0.6028', 'grad_norm': '3.35', 'learning_rate': '3.389e-05', 'epoch': '1.332'}
[text-trainer] {'loss': '0.5585', 'grad_norm': '3.005', 'learning_rate': '3.36e-05', 'epoch': '1.336'}
[text-trainer] [sft_v2] sft_v2_eval {'step': 2654, 'dev_loss': 1.355134, 'best': 1.272726, 'eval_s': 6.7, 'pool': 8, 'improved': False}
[text-trainer] {'loss': '0.7275', 'grad_norm': '4.487', 'learning_rate': '3.332e-05', 'epoch': '1.34'}
[text-trainer] {'loss': '0.6815', 'grad_norm': '2.9', 'learning_rate': '3.304e-05', 'epoch': '1.345'}
[text-trainer] {'loss': '0.4943', 'grad_norm': '2.811', 'learning_rate': '3.276e-05', 'epoch': '1.349'}
[text-trainer] {'loss': '0.6617', 'grad_norm': '3.088', 'learning_rate': '3.248e-05', 'epoch': '1.354'}
[text-trainer] {'loss': '0.3884', 'grad_norm': '1.912', 'learning_rate': '3.22e-05', 'epoch': '1.358'}
[text-trainer] {'loss': '0.3474', 'grad_norm': '1.777', 'learning_rate': '3.193e-05', 'epoch': '1.362'}
[text-trainer] {'loss': '0.4479', 'grad_norm': '1.935', 'learning_rate': '3.165e-05', 'epoch': '1.367'}
[text-trainer] {'loss': '0.504', 'grad_norm': '2.801', 'learning_rate': '3.138e-05', 'epoch': '1.371'}
[text-trainer] {'loss': '0.4935', 'grad_norm': '2.668', 'learning_rate': '3.111e-05', 'epoch': '1.376'}
[text-trainer] {'loss': '0.5063', 'grad_norm': '2.039', 'learning_rate': '3.083e-05', 'epoch': '1.38'}
[text-trainer] {'loss': '0.762', 'grad_norm': '3.642', 'learning_rate': '3.056e-05', 'epoch': '1.384'}
[text-trainer] {'loss': '0.817', 'grad_norm': '3.045', 'learning_rate': '3.029e-05', 'epoch': '1.389'}
[text-trainer] {'loss': '0.7157', 'grad_norm': '2.78', 'learning_rate': '3.003e-05', 'epoch': '1.393'}
[text-trainer] {'loss': '0.5389', 'grad_norm': '3.445', 'learning_rate': '2.976e-05', 'epoch': '1.398'}
[text-trainer] {'loss': '0.4595', 'grad_norm': '2.144', 'learning_rate': '2.949e-05', 'epoch': '1.402'}
[text-trainer] {'loss': '0.3893', 'grad_norm': '2.499', 'learning_rate': '2.923e-05', 'epoch': '1.407'}
[text-trainer] {'loss': '0.3925', 'grad_norm': '1.85', 'learning_rate': '2.897e-05', 'epoch': '1.411'}
[text-trainer] {'loss': '0.4384', 'grad_norm': '2.358', 'learning_rate': '2.871e-05', 'epoch': '1.415'}
[text-trainer] {'loss': '0.6208', 'grad_norm': '2.871', 'learning_rate': '2.845e-05', 'epoch': '1.42'}
[text-trainer] {'loss': '0.5805', 'grad_norm': '4.394', 'learning_rate': '2.819e-05', 'epoch': '1.424'}
[text-trainer] {'loss': '0.7738', 'grad_norm': '3.038', 'learning_rate': '2.793e-05', 'epoch': '1.429'}
[text-trainer] {'loss': '0.694', 'grad_norm': '3.029', 'learning_rate': '2.767e-05', 'epoch': '1.433'}
[text-trainer] {'loss': '0.5811', 'grad_norm': '2.627', 'learning_rate': '2.742e-05', 'epoch': '1.437'}
[text-trainer] {'loss': '0.6496', 'grad_norm': '4.642', 'learning_rate': '2.717e-05', 'epoch': '1.442'}
[text-trainer] {'loss': '0.4994', 'grad_norm': '1.735', 'learning_rate': '2.691e-05', 'epoch': '1.446'}
[text-trainer] {'loss': '0.3557', 'grad_norm': '1.663', 'learning_rate': '2.666e-05', 'epoch': '1.451'}
[text-trainer] {'loss': '0.4105', 'grad_norm': '2.417', 'learning_rate': '2.642e-05', 'epoch': '1.455'}
[text-trainer] {'loss': '0.4534', 'grad_norm': '2.559', 'learning_rate': '2.617e-05', 'epoch': '1.459'}
[text-trainer] {'loss': '0.5758', 'grad_norm': '3.232', 'learning_rate': '2.592e-05', 'epoch': '1.464'}
[text-trainer] {'loss': '0.5889', 'grad_norm': '2.816', 'learning_rate': '2.568e-05', 'epoch': '1.468'}
[text-trainer] {'loss': '0.8249', 'grad_norm': '2.649', 'learning_rate': '2.543e-05', 'epoch': '1.473'}
[text-trainer] {'loss': '0.7686', 'grad_norm': '2.55', 'learning_rate': '2.519e-05', 'epoch': '1.477'}
[text-trainer] {'loss': '0.8238', 'grad_norm': '5.246', 'learning_rate': '2.495e-05', 'epoch': '1.481'}
[text-trainer] {'loss': '0.6357', 'grad_norm': '2.83', 'learning_rate': '2.471e-05', 'epoch': '1.486'}
[text-trainer] {'loss': '0.3192', 'grad_norm': '1.8', 'learning_rate': '2.448e-05', 'epoch': '1.49'}
[text-trainer] {'loss': '0.3272', 'grad_norm': '2.131', 'learning_rate': '2.424e-05', 'epoch': '1.495'}
[text-trainer] {'loss': '0.4309', 'grad_norm': '2.308', 'learning_rate': '2.401e-05', 'epoch': '1.499'}
[text-trainer] {'loss': '0.4711', 'grad_norm': '2.222', 'learning_rate': '2.378e-05', 'epoch': '1.504'}
[text-trainer] {'loss': '0.5977', 'grad_norm': '3.193', 'learning_rate': '2.355e-05', 'epoch': '1.508'}
[text-trainer] {'loss': '0.6096', 'grad_norm': '2.872', 'learning_rate': '2.332e-05', 'epoch': '1.512'}
[text-trainer] {'loss': '0.672', 'grad_norm': '3.169', 'learning_rate': '2.309e-05', 'epoch': '1.517'}
[text-trainer] {'loss': '0.6016', 'grad_norm': '2.823', 'learning_rate': '2.286e-05', 'epoch': '1.521'}
[text-trainer] {'loss': '0.7389', 'grad_norm': '3.299', 'learning_rate': '2.264e-05', 'epoch': '1.526'}
[text-trainer] {'loss': '0.6001', 'grad_norm': '4.076', 'learning_rate': '2.242e-05', 'epoch': '1.53'}
[text-trainer] {'loss': '0.509', 'grad_norm': '2.095', 'learning_rate': '2.22e-05', 'epoch': '1.534'}
[text-trainer] {'loss': '0.3431', 'grad_norm': '2.657', 'learning_rate': '2.198e-05', 'epoch': '1.539'}
[text-trainer] {'loss': '0.3749', 'grad_norm': '2.959', 'learning_rate': '2.176e-05', 'epoch': '1.543'}
[text-trainer] {'loss': '0.4496', 'grad_norm': '2.338', 'learning_rate': '2.154e-05', 'epoch': '1.548'}
[text-trainer] {'loss': '0.5733', 'grad_norm': '2.924', 'learning_rate': '2.133e-05', 'epoch': '1.552'}
[text-trainer] {'loss': '0.7014', 'grad_norm': '3.972', 'learning_rate': '2.112e-05', 'epoch': '1.556'}
[text-trainer] {'loss': '0.7037', 'grad_norm': '3.412', 'learning_rate': '2.091e-05', 'epoch': '1.561'}
[text-trainer] {'loss': '0.5799', 'grad_norm': '2.443', 'learning_rate': '2.07e-05', 'epoch': '1.565'}
[text-trainer] {'loss': '0.7452', 'grad_norm': '2.985', 'learning_rate': '2.049e-05', 'epoch': '1.57'}
[text-trainer] {'loss': '0.5504', 'grad_norm': '3.234', 'learning_rate': '2.029e-05', 'epoch': '1.574'}
[text-trainer] {'loss': '0.4865', 'grad_norm': '1.66', 'learning_rate': '2.008e-05', 'epoch': '1.578'}
[text-trainer] {'loss': '0.4121', 'grad_norm': '2.469', 'learning_rate': '1.988e-05', 'epoch': '1.583'}
[text-trainer] {'loss': '0.3617', 'grad_norm': '2.522', 'learning_rate': '1.968e-05', 'epoch': '1.587'}
[text-trainer] {'loss': '0.6024', 'grad_norm': '3.876', 'learning_rate': '1.948e-05', 'epoch': '1.592'}
[text-trainer] {'loss': '0.6892', 'grad_norm': '3.115', 'learning_rate': '1.929e-05', 'epoch': '1.596'}
[text-trainer] {'loss': '0.6072', 'grad_norm': '2.292', 'learning_rate': '1.909e-05', 'epoch': '1.601'}
[text-trainer] {'loss': '0.8016', 'grad_norm': '2.663', 'learning_rate': '1.89e-05', 'epoch': '1.605'}
[text-trainer] {'loss': '0.7015', 'grad_norm': '3.316', 'learning_rate': '1.871e-05', 'epoch': '1.609'}
[text-trainer] {'loss': '0.7263', 'grad_norm': '2.574', 'learning_rate': '1.852e-05', 'epoch': '1.614'}
[text-trainer] {'loss': '0.6505', 'grad_norm': '3.098', 'learning_rate': '1.833e-05', 'epoch': '1.618'}
[text-trainer] {'loss': '0.4243', 'grad_norm': '1.197', 'learning_rate': '1.815e-05', 'epoch': '1.623'}
[text-trainer] {'loss': '0.4449', 'grad_norm': '2.691', 'learning_rate': '1.796e-05', 'epoch': '1.627'}
[text-trainer] {'loss': '0.3909', 'grad_norm': '2.8', 'learning_rate': '1.778e-05', 'epoch': '1.631'}
[text-trainer] {'loss': '0.3372', 'grad_norm': '2.693', 'learning_rate': '1.76e-05', 'epoch': '1.636'}
[text-trainer] {'loss': '0.5565', 'grad_norm': '2.752', 'learning_rate': '1.742e-05', 'epoch': '1.64'}
[text-trainer] {'loss': '0.6761', 'grad_norm': '3.164', 'learning_rate': '1.725e-05', 'epoch': '1.645'}
[text-trainer] {'loss': '0.755', 'grad_norm': '2.794', 'learning_rate': '1.707e-05', 'epoch': '1.649'}
[text-trainer] {'loss': '0.7462', 'grad_norm': '2.946', 'learning_rate': '1.69e-05', 'epoch': '1.653'}
[text-trainer] {'loss': '0.6279', 'grad_norm': '2.865', 'learning_rate': '1.673e-05', 'epoch': '1.658'}
[text-trainer] {'loss': '0.8057', 'grad_norm': '3.229', 'learning_rate': '1.656e-05', 'epoch': '1.662'}
[text-trainer] {'loss': '0.3797', 'grad_norm': '2.739', 'learning_rate': '1.64e-05', 'epoch': '1.667'}
[text-trainer] {'loss': '0.3303', 'grad_norm': '2.72', 'learning_rate': '1.623e-05', 'epoch': '1.671'}
[text-trainer] [sft_v2] sft_v2_eval {'step': 3034, 'dev_loss': 1.306668, 'best': 1.272726, 'eval_s': 6.8, 'pool': 8, 'improved': False}
[text-trainer] {'loss': '0.4059', 'grad_norm': '2.214', 'learning_rate': '1.607e-05', 'epoch': '1.675'}
[text-trainer] {'loss': '0.3986', 'grad_norm': '1.914', 'learning_rate': '1.591e-05', 'epoch': '1.68'}
[text-trainer] {'loss': '0.4981', 'grad_norm': '2.67', 'learning_rate': '1.575e-05', 'epoch': '1.684'}
[text-trainer] {'loss': '0.5726', 'grad_norm': '2.764', 'learning_rate': '1.56e-05', 'epoch': '1.689'}
[text-trainer] {'loss': '0.6598', 'grad_norm': '3.474', 'learning_rate': '1.544e-05', 'epoch': '1.693'}
[text-trainer] {'loss': '0.6314', 'grad_norm': '2.753', 'learning_rate': '1.529e-05', 'epoch': '1.698'}
[text-trainer] {'loss': '0.7057', 'grad_norm': '2.669', 'learning_rate': '1.514e-05', 'epoch': '1.702'}
[text-trainer] {'loss': '0.596', 'grad_norm': '3.186', 'learning_rate': '1.499e-05', 'epoch': '1.706'}
[text-trainer] {'loss': '0.4265', 'grad_norm': '1.677', 'learning_rate': '1.485e-05', 'epoch': '1.711'}
[text-trainer] {'loss': '0.3692', 'grad_norm': '2.524', 'learning_rate': '1.47e-05', 'epoch': '1.715'}
[text-trainer] {'loss': '0.4055', 'grad_norm': '2.189', 'learning_rate': '1.456e-05', 'epoch': '1.72'}
[text-trainer] {'loss': '0.5054', 'grad_norm': '1.805', 'learning_rate': '1.442e-05', 'epoch': '1.724'}
[text-trainer] {'loss': '0.4804', 'grad_norm': '3.309', 'learning_rate': '1.428e-05', 'epoch': '1.728'}
[text-trainer] {'loss': '0.616', 'grad_norm': '2.581', 'learning_rate': '1.415e-05', 'epoch': '1.733'}
[text-trainer] {'loss': '0.6476', 'grad_norm': '2.874', 'learning_rate': '1.401e-05', 'epoch': '1.737'}
[text-trainer] {'loss': '0.7293', 'grad_norm': '5.358', 'learning_rate': '1.388e-05', 'epoch': '1.742'}
[text-trainer] {'loss': '0.5899', 'grad_norm': '3.547', 'learning_rate': '1.375e-05', 'epoch': '1.746'}
[text-trainer] {'loss': '0.5361', 'grad_norm': '3.586', 'learning_rate': '1.362e-05', 'epoch': '1.75'}
[text-trainer] {'loss': '0.3784', 'grad_norm': '1.908', 'learning_rate': '1.35e-05', 'epoch': '1.755'}
[text-trainer] {'loss': '0.337', 'grad_norm': '2.101', 'learning_rate': '1.338e-05', 'epoch': '1.759'}
[text-trainer] {'loss': '0.4125', 'grad_norm': '2.163', 'learning_rate': '1.326e-05', 'epoch': '1.764'}
[text-trainer] {'loss': '0.5226', 'grad_norm': '2.138', 'learning_rate': '1.314e-05', 'epoch': '1.768'}
[text-trainer] {'loss': '0.5769', 'grad_norm': '3.139', 'learning_rate': '1.302e-05', 'epoch': '1.772'}
[text-trainer] {'loss': '0.597', 'grad_norm': '3.474', 'learning_rate': '1.291e-05', 'epoch': '1.777'}
[text-trainer] {'loss': '0.7575', 'grad_norm': '2.782', 'learning_rate': '1.279e-05', 'epoch': '1.781'}
[text-trainer] {'loss': '0.7849', 'grad_norm': '3.138', 'learning_rate': '1.268e-05', 'epoch': '1.786'}
[text-trainer] {'loss': '0.6702', 'grad_norm': '3.16', 'learning_rate': '1.257e-05', 'epoch': '1.79'}
[text-trainer] {'loss': '0.6024', 'grad_norm': '2.665', 'learning_rate': '1.247e-05', 'epoch': '1.795'}
[text-trainer] {'loss': '0.2998', 'grad_norm': '1.848', 'learning_rate': '1.236e-05', 'epoch': '1.799'}
[text-trainer] {'loss': '0.3356', 'grad_norm': '2.037', 'learning_rate': '1.226e-05', 'epoch': '1.803'}
[text-trainer] {'loss': '0.4792', 'grad_norm': '2.849', 'learning_rate': '1.216e-05', 'epoch': '1.808'}
[text-trainer] {'loss': '0.4649', 'grad_norm': '2.641', 'learning_rate': '1.207e-05', 'epoch': '1.812'}
[text-trainer] {'loss': '0.4986', 'grad_norm': '3.43', 'learning_rate': '1.197e-05', 'epoch': '1.817'}
[text-trainer] {'loss': '0.55', 'grad_norm': '2.619', 'learning_rate': '1.188e-05', 'epoch': '1.821'}
[text-trainer] {'loss': '0.7082', 'grad_norm': '3.349', 'learning_rate': '1.179e-05', 'epoch': '1.825'}
[text-trainer] {'loss': '0.7743', 'grad_norm': '3.186', 'learning_rate': '1.17e-05', 'epoch': '1.83'}
[text-trainer] {'loss': '0.546', 'grad_norm': '2.66', 'learning_rate': '1.161e-05', 'epoch': '1.834'}
[text-trainer] {'loss': '0.6007', 'grad_norm': '3.179', 'learning_rate': '1.153e-05', 'epoch': '1.839'}
[text-trainer] {'loss': '0.4869', 'grad_norm': '2.801', 'learning_rate': '1.145e-05', 'epoch': '1.843'}
[text-trainer] {'loss': '0.3276', 'grad_norm': '2.232', 'learning_rate': '1.137e-05', 'epoch': '1.847'}
[text-trainer] {'loss': '0.3644', 'grad_norm': '2.394', 'learning_rate': '1.129e-05', 'epoch': '1.852'}
[text-trainer] {'loss': '0.4243', 'grad_norm': '2.06', 'learning_rate': '1.121e-05', 'epoch': '1.856'}
[text-trainer] {'loss': '0.4635', 'grad_norm': '2.216', 'learning_rate': '1.114e-05', 'epoch': '1.861'}
[text-trainer] {'loss': '0.6507', 'grad_norm': '3.011', 'learning_rate': '1.107e-05', 'epoch': '1.865'}
[text-trainer] {'loss': '0.7641', 'grad_norm': '3.452', 'learning_rate': '1.1e-05', 'epoch': '1.869'}
[text-trainer] {'loss': '0.6922', 'grad_norm': '1.974', 'learning_rate': '1.093e-05', 'epoch': '1.874'}
[text-trainer] {'loss': '0.7067', 'grad_norm': '2.967', 'learning_rate': '1.087e-05', 'epoch': '1.878'}
[text-trainer] {'loss': '0.7198', 'grad_norm': '5.686', 'learning_rate': '1.081e-05', 'epoch': '1.883'}
[text-trainer] {'loss': '0.3431', 'grad_norm': '1.706', 'learning_rate': '1.075e-05', 'epoch': '1.887'}
[text-trainer] {'loss': '0.4032', 'grad_norm': '2.116', 'learning_rate': '1.069e-05', 'epoch': '1.892'}
[text-trainer] {'loss': '0.4519', 'grad_norm': '2.361', 'learning_rate': '1.064e-05', 'epoch': '1.896'}
[text-trainer] {'loss': '0.5473', 'grad_norm': '2.473', 'learning_rate': '1.058e-05', 'epoch': '1.9'}
[text-trainer] {'loss': '0.454', 'grad_norm': '2.983', 'learning_rate': '1.053e-05', 'epoch': '1.905'}
[text-trainer] {'loss': '0.4732', 'grad_norm': '2.455', 'learning_rate': '1.049e-05', 'epoch': '1.909'}
[text-trainer] {'loss': '0.7207', 'grad_norm': '3.075', 'learning_rate': '1.044e-05', 'epoch': '1.914'}
[text-trainer] {'loss': '0.6576', 'grad_norm': '2.91', 'learning_rate': '1.04e-05', 'epoch': '1.918'}
[text-trainer] {'loss': '0.5404', 'grad_norm': '2.971', 'learning_rate': '1.035e-05', 'epoch': '1.922'}
[text-trainer] {'loss': '0.5201', 'grad_norm': '3.509', 'learning_rate': '1.032e-05', 'epoch': '1.927'}
[text-trainer] {'loss': '0.4142', 'grad_norm': '2.9', 'learning_rate': '1.028e-05', 'epoch': '1.931'}
[text-trainer] {'loss': '0.2838', 'grad_norm': '2.493', 'learning_rate': '1.024e-05', 'epoch': '1.936'}
[text-trainer] {'loss': '0.3143', 'grad_norm': '3.211', 'learning_rate': '1.021e-05', 'epoch': '1.94'}
[text-trainer] {'loss': '0.4812', 'grad_norm': '2.645', 'learning_rate': '1.018e-05', 'epoch': '1.944'}
[text-trainer] {'loss': '0.3831', 'grad_norm': '2.674', 'learning_rate': '1.015e-05', 'epoch': '1.949'}
[text-trainer] {'loss': '0.6244', 'grad_norm': '2.691', 'learning_rate': '1.013e-05', 'epoch': '1.953'}
[text-trainer] {'loss': '0.6996', 'grad_norm': '3.13', 'learning_rate': '1.011e-05', 'epoch': '1.958'}
[text-trainer] {'loss': '0.7252', 'grad_norm': '3.558', 'learning_rate': '1.008e-05', 'epoch': '1.962'}
[text-trainer] {'loss': '0.4872', 'grad_norm': '2.884', 'learning_rate': '1.007e-05', 'epoch': '1.966'}
[text-trainer] {'loss': '0.5751', 'grad_norm': '4.611', 'learning_rate': '1.005e-05', 'epoch': '1.971'}
[text-trainer] {'loss': '0.3234', 'grad_norm': '1.923', 'learning_rate': '1.004e-05', 'epoch': '1.975'}
[text-trainer] {'loss': '0.3602', 'grad_norm': '1.874', 'learning_rate': '1.002e-05', 'epoch': '1.98'}
[text-trainer] {'loss': '0.465', 'grad_norm': '2.41', 'learning_rate': '1.001e-05', 'epoch': '1.984'}
[text-trainer] {'loss': '0.6436', 'grad_norm': '2.464', 'learning_rate': '1.001e-05', 'epoch': '1.989'}
[text-trainer] {'loss': '0.6684', 'grad_norm': '2.87', 'learning_rate': '1e-05', 'epoch': '1.993'}
[text-trainer] {'loss': '0.6173', 'grad_norm': '2.577', 'learning_rate': '1e-05', 'epoch': '1.997'}
[text-trainer] [sft_v2] sft_v2_eval {'step': 3401, 'dev_loss': 1.297585, 'best': 1.272726, 'eval_s': 6.7, 'pool': 8, 'improved': False}
[text-trainer] {'train_runtime': '683.1', 'train_samples_per_second': '53.08', 'train_steps_per_second': '3.319', 'train_loss': '0.7732', 'epoch': '1.999'}
[text-trainer] [sft_v2] sft_v2_phase_end {'phase': 1, 'steps': 2267, 'planned': 2267, 'epochs_done': 3.002, 't_per_step_measured': 0.281, 'best': 1.272726, 'best_step': 2274, 'remaining_s': 2508.5}
[text-trainer] [sft_v2] sft_v2_train_end {'step': 3401, 'best': 1.272726, 'best_step': 2274, 'phases': 2, 'remaining_s': 2508.5}
[text-trainer] [sft_v2] soup_result {'seed_loss': 1.272726, 'soup_loss': 1.266128, 'members': 2, 'pool': 8, 'steps': [2274, 3401]}
[text-trainer] [sft_v2] sft_v2_dev_pass_done {'rows': 400, 'lr': 5e-05, 'pass_index': 1}
[text-trainer] [sft_v2] sft_v2_final {'saved': True, 'chosen_loss': 1.266128, 'chosen_step': 3401, 'truth': 'COMPLETE_BEST', 'remaining_s': 2443.2}