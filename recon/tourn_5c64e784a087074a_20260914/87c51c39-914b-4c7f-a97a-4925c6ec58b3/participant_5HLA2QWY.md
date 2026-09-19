# Loki — task 87c51c39-914b-4c7f-a97a-4925c6ec58b3 — hotkey 5HLA2QWYy3GpNwCiBCwMMhGw5hpPosSeZ41my8B3nuFDQHNF
fetched 2026-09-19T05:07:48+00:00  lines=219  hit_page_cap=False  containers=['downloader-87c51c39-914b-4c7f-a97a-4925c6ec58b3-fd57c96f', 'fastapi', 'hf-upload-6d4a6981bf704e359a10360b16cd8e26', 'text-trainer-f12793a3943543e6939c71f33a120a61']

[downloader-8] Downloading datasets to: /cache/datasets
[downloader-8] Downloading models to: /cache/models
[downloader-8] Model already cached at /cache/models/b254e84a30620233.
[downloader-8] Skipping download.
[downloader-8] Model path: /cache/models/b254e84a30620233
[downloader-8] Dataset path: /cache/datasets
[fastapi] Repository cloned successfully
[fastapi] Running Cache Download Container
[fastapi] Starting downloader container: downloader-87c51c39-914b-4c7f-a97a-4925c6ec58b3-fd57c96f
[fastapi] Download completed successfully for task 87c51c39-914b-4c7f-a97a-4925c6ec58b3
[fastapi] Building Docker image 'standalone-text-trainer:60ac8f38-f339-4680-bb27-039e535d5e34' (timeout=3600s)...
[fastapi] Step 1/7 : FROM axolotlai/axolotl:main-20260701-py3.11-cu128-2.9.1@sha256:3aa6403f59f2268bb8f686f6c748d6fad2949580a0048cd25a605eb2de239ee5
[fastapi] Pulling from axolotlai/axolotlAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsDigest: sha256:3aa6403f59f2268bb8f686f6c748d6fad2949580a0048cd25a605eb2de239ee5Status: Downloaded newer image for axolotlai/axolotl:main-20260701-py3.11-cu128-2.9.1@sha256:3aa6403f59f2268bb8f686f6c748d6fad2949580a0048cd25a605eb2de239ee5 ---> 08c3197175de
[fastapi] Step 2/7 : ENV PYTHONUNBUFFERED=1     PIP_NO_CACHE_DIR=1     HF_HUB_DISABLE_TELEMETRY=1     HF_HUB_DISABLE_SYMLINKS_WARNING=1     TOKENIZERS_PARALLELISM=false     HF_HUB_OFFLINE=1     TRANSFORMERS_OFFLINE=1
[fastapi] ---> Running in cd0b36816004
[fastapi] ---> 76d66477e061
[fastapi] Step 3/7 : RUN TORCH_CUDA_ARCH_LIST="8.0;9.0+PTX" uv pip install         --python /workspace/axolotl-venv/bin/python         --no-cache --no-build-isolation causal-conv1d==1.6.2.post1
[fastapi] ---> Running in 3ed800471701
[fastapi] [91mUsing Python 3.11.15 environment at: /workspace/axolotl-venv
[fastapi] [0m[91mResolved 28 packages in 7.63s
[fastapi] [0m[91m   Building causal-conv1d==1.6.2.post1
[fastapi] [0m[91m      Built causal-conv1d==1.6.2.post1
[fastapi] [0m[91mPrepared 1 package in 1m 02s
[fastapi] [0m[91mInstalled 1 package in 6ms
[fastapi] + causal-conv1d==1.6.2.post1
[fastapi] [0m ---> a16a2eea6f0a
[fastapi] Step 4/7 : WORKDIR /app
[fastapi] ---> Running in 52ec9ee4bc67
[fastapi] ---> 07a2510576df
[fastapi] Step 5/7 : COPY forge /app/forge
[fastapi] ---> 29e12fca0c0e
[fastapi] Step 6/7 : COPY pyproject.toml LICENSE.md NOTICE /app/
[fastapi] ---> 768e3f2e667d
[fastapi] Step 7/7 : ENTRYPOINT ["/workspace/axolotl-venv/bin/python", "-m", "forge.cli"]
[fastapi] ---> Running in 2eb57a50feb3
[fastapi] ---> 2e95c37e91bf
[fastapi] {'aux': {'ID': 'sha256:2e95c37e91bfaffa65727fa2d5d09c980953984193fd0700acc9a8b58cea89d2'}}Successfully built 2e95c37e91bf
[fastapi] Successfully tagged standalone-text-trainer:60ac8f38-f339-4680-bb27-039e535d5e34
[fastapi] Docker image built successfully.
[fastapi] Container.wait() returned: {'StatusCode': 0}
[fastapi] Cleaning up
[fastapi] Cleaned up Docker resources.
[fastapi] Starting upload container hf-upload-6d4a6981bf704e359a10360b16cd8e26 for task 87c51c39-914b-4c7f-a97a-4925c6ec58b3...
[hf-upload-6d] Updated adapter_config.json with base_model: unsloth/Qwen2.5-0.5B-Instruct
[hf-upload-6d] Updated README.md with base_model: unsloth/Qwen2.5-0.5B-Instruct
[hf-upload-6d] Creating repo gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5HLA2QWY...
[hf-upload-6d] Uploading contents of /app/checkpoints/87c51c39-914b-4c7f-a97a-4925c6ec58b3/tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5HLA2QWY to gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5HLA2QWY
[hf-upload-6d] Uploaded successfully to https://huggingface.co/gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5HLA2QWY
[hf-upload-6d] Deleted local folder: /app/checkpoints/87c51c39-914b-4c7f-a97a-4925c6ec58b3/tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5HLA2QWY
[text-trainer] Skipping import of cpp extensions due to incompatible torch version. Please upgrade to torch >= 2.11.0 (found 2.9.1+cu128).
[text-trainer] [INFO] Running in WANDB offline mode
[text-trainer] [transformers] warmup_ratio is deprecated and will be removed in v5.2. Use `warmup_steps` instead.
[text-trainer] {'train_runtime': '3.365', 'train_samples_per_second': '4.754', 'train_steps_per_second': '0.297', 'train_loss': '0.3836', 'epoch': '1'}
[text-trainer] [transformers] warmup_ratio is deprecated and will be removed in v5.2. Use `warmup_steps` instead.
[text-trainer] {'train_runtime': '3.84', 'train_samples_per_second': '4.167', 'train_steps_per_second': '0.26', 'train_loss': '0.666', 'epoch': '1'}
[text-trainer] [transformers] warmup_ratio is deprecated and will be removed in v5.2. Use `warmup_steps` instead.
[text-trainer] {'loss': '1.517', 'grad_norm': '1.768', 'learning_rate': '0', 'epoch': '0.25'}
[text-trainer] {'loss': '1.701', 'grad_norm': '1.801', 'learning_rate': '0', 'epoch': '0.5'}
[text-trainer] {'loss': '1.579', 'grad_norm': '1.193', 'learning_rate': '0', 'epoch': '0.75'}
[text-trainer] {'train_runtime': '61.55', 'train_samples_per_second': '9.098', 'train_steps_per_second': '0.569', 'train_loss': '1.599', 'epoch': '0.75'}
[text-trainer] [transformers] warmup_ratio is deprecated and will be removed in v5.2. Use `warmup_steps` instead.
[text-trainer] {'loss': '1.548', 'grad_norm': '1.941', 'learning_rate': '3e-05', 'epoch': '0.005605'}
[text-trainer] {'loss': '1.464', 'grad_norm': '3.32', 'learning_rate': '6.333e-05', 'epoch': '0.01121'}
[text-trainer] {'loss': '1.423', 'grad_norm': '1.715', 'learning_rate': '9.667e-05', 'epoch': '0.01682'}
[text-trainer] {'loss': '1.506', 'grad_norm': '1.588', 'learning_rate': '0.00013', 'epoch': '0.02242'}
[text-trainer] {'loss': '1.473', 'grad_norm': '1.433', 'learning_rate': '0.00015', 'epoch': '0.02803'}
[text-trainer] {'loss': '1.525', 'grad_norm': '1.814', 'learning_rate': '0.00015', 'epoch': '0.03363'}
[text-trainer] {'loss': '1.327', 'grad_norm': '1.008', 'learning_rate': '0.0001499', 'epoch': '0.03924'}
[text-trainer] {'loss': '1.395', 'grad_norm': '1.33', 'learning_rate': '0.0001498', 'epoch': '0.04484'}
[text-trainer] {'loss': '1.44', 'grad_norm': '1.166', 'learning_rate': '0.0001497', 'epoch': '0.05045'}
[text-trainer] {'loss': '1.464', 'grad_norm': '1.043', 'learning_rate': '0.0001496', 'epoch': '0.05605'}
[text-trainer] {'loss': '1.451', 'grad_norm': '1.315', 'learning_rate': '0.0001495', 'epoch': '0.06166'}
[text-trainer] {'loss': '1.25', 'grad_norm': '0.9341', 'learning_rate': '0.0001493', 'epoch': '0.06726'}
[text-trainer] {'loss': '1.348', 'grad_norm': '0.9793', 'learning_rate': '0.0001491', 'epoch': '0.07287'}
[text-trainer] {'loss': '1.331', 'grad_norm': '1.138', 'learning_rate': '0.0001488', 'epoch': '0.07848'}
[text-trainer] {'loss': '1.356', 'grad_norm': '1.028', 'learning_rate': '0.0001486', 'epoch': '0.08408'}
[text-trainer] {'loss': '1.206', 'grad_norm': '1.109', 'learning_rate': '0.0001483', 'epoch': '0.08969'}
[text-trainer] {'loss': '1.282', 'grad_norm': '1.005', 'learning_rate': '0.000148', 'epoch': '0.09529'}
[text-trainer] {'loss': '1.342', 'grad_norm': '1.599', 'learning_rate': '0.0001477', 'epoch': '0.1009'}
[text-trainer] {'loss': '1.45', 'grad_norm': '0.8726', 'learning_rate': '0.0001473', 'epoch': '0.1065'}
[text-trainer] {'loss': '1.333', 'grad_norm': '1.519', 'learning_rate': '0.0001469', 'epoch': '0.1121'}
[text-trainer] {'loss': '1.307', 'grad_norm': '1.273', 'learning_rate': '0.0001465', 'epoch': '0.1177'}
[text-trainer] {'loss': '1.357', 'grad_norm': '0.73', 'learning_rate': '0.0001461', 'epoch': '0.1233'}
[text-trainer] {'loss': '1.282', 'grad_norm': '1.024', 'learning_rate': '0.0001456', 'epoch': '0.1289'}
[text-trainer] {'loss': '1.359', 'grad_norm': '1.548', 'learning_rate': '0.0001451', 'epoch': '0.1345'}
[text-trainer] {'loss': '1.286', 'grad_norm': '0.8545', 'learning_rate': '0.0001446', 'epoch': '0.1401'}
[text-trainer] {'loss': '1.311', 'grad_norm': '1.239', 'learning_rate': '0.0001441', 'epoch': '0.1457'}
[text-trainer] {'loss': '1.276', 'grad_norm': '0.8377', 'learning_rate': '0.0001435', 'epoch': '0.1513'}
[text-trainer] {'loss': '1.211', 'grad_norm': '1.066', 'learning_rate': '0.000143', 'epoch': '0.157'}
[text-trainer] {'loss': '1.445', 'grad_norm': '1.033', 'learning_rate': '0.0001424', 'epoch': '0.1626'}
[text-trainer] {'loss': '1.335', 'grad_norm': '0.6623', 'learning_rate': '0.0001417', 'epoch': '0.1682'}
[text-trainer] {'loss': '1.331', 'grad_norm': '1.012', 'learning_rate': '0.0001411', 'epoch': '0.1738'}
[text-trainer] {'loss': '1.258', 'grad_norm': '0.8436', 'learning_rate': '0.0001404', 'epoch': '0.1794'}
[text-trainer] {'loss': '1.363', 'grad_norm': '1.169', 'learning_rate': '0.0001397', 'epoch': '0.185'}
[text-trainer] {'loss': '1.311', 'grad_norm': '1.518', 'learning_rate': '0.000139', 'epoch': '0.1906'}
[text-trainer] {'loss': '1.342', 'grad_norm': '1.048', 'learning_rate': '0.0001383', 'epoch': '0.1962'}
[text-trainer] {'loss': '1.319', 'grad_norm': '1.015', 'learning_rate': '0.0001375', 'epoch': '0.2018'}
[text-trainer] {'loss': '1.326', 'grad_norm': '0.9709', 'learning_rate': '0.0001368', 'epoch': '0.2074'}
[text-trainer] {'loss': '1.354', 'grad_norm': '0.8749', 'learning_rate': '0.000136', 'epoch': '0.213'}
[text-trainer] {'loss': '1.296', 'grad_norm': '1.017', 'learning_rate': '0.0001352', 'epoch': '0.2186'}
[text-trainer] {'loss': '1.558', 'grad_norm': '0.8461', 'learning_rate': '0.0001343', 'epoch': '0.2242'}
[text-trainer] {'loss': '1.22', 'grad_norm': '0.8464', 'learning_rate': '0.0001335', 'epoch': '0.2298'}
[text-trainer] {'loss': '1.201', 'grad_norm': '0.7342', 'learning_rate': '0.0001326', 'epoch': '0.2354'}
[text-trainer] {'loss': '1.169', 'grad_norm': '1.028', 'learning_rate': '0.0001317', 'epoch': '0.241'}
[text-trainer] {'loss': '1.263', 'grad_norm': '0.9978', 'learning_rate': '0.0001308', 'epoch': '0.2466'}
[text-trainer] {'eval_loss': '1.315', 'eval_runtime': '10.47', 'eval_samples_per_second': '24.45', 'eval_steps_per_second': '6.112', 'epoch': '0.25'}
[text-trainer] {'loss': '1.202', 'grad_norm': '1.073', 'learning_rate': '0.0001299', 'epoch': '0.2522'}
[text-trainer] {'loss': '1.216', 'grad_norm': '1.02', 'learning_rate': '0.000129', 'epoch': '0.2578'}
[text-trainer] {'loss': '1.235', 'grad_norm': '0.8024', 'learning_rate': '0.000128', 'epoch': '0.2635'}
[text-trainer] {'loss': '1.255', 'grad_norm': '1.065', 'learning_rate': '0.000127', 'epoch': '0.2691'}
[text-trainer] {'loss': '1.317', 'grad_norm': '1.03', 'learning_rate': '0.000126', 'epoch': '0.2747'}
[text-trainer] {'loss': '1.3', 'grad_norm': '1.008', 'learning_rate': '0.000125', 'epoch': '0.2803'}
[text-trainer] {'loss': '1.3', 'grad_norm': '0.7017', 'learning_rate': '0.000124', 'epoch': '0.2859'}
[text-trainer] {'loss': '1.327', 'grad_norm': '1.064', 'learning_rate': '0.000123', 'epoch': '0.2915'}
[text-trainer] {'loss': '1.214', 'grad_norm': '0.7693', 'learning_rate': '0.0001219', 'epoch': '0.2971'}
[text-trainer] {'loss': '1.328', 'grad_norm': '1.013', 'learning_rate': '0.0001209', 'epoch': '0.3027'}
[text-trainer] {'loss': '1.154', 'grad_norm': '1.135', 'learning_rate': '0.0001198', 'epoch': '0.3083'}
[text-trainer] {'loss': '1.292', 'grad_norm': '0.7526', 'learning_rate': '0.0001187', 'epoch': '0.3139'}
[text-trainer] {'loss': '1.264', 'grad_norm': '1.045', 'learning_rate': '0.0001176', 'epoch': '0.3195'}
[text-trainer] {'loss': '1.225', 'grad_norm': '0.8109', 'learning_rate': '0.0001165', 'epoch': '0.3251'}
[text-trainer] {'loss': '1.257', 'grad_norm': '0.7007', 'learning_rate': '0.0001154', 'epoch': '0.3307'}
[text-trainer] {'loss': '1.171', 'grad_norm': '0.8992', 'learning_rate': '0.0001143', 'epoch': '0.3363'}
[text-trainer] {'loss': '1.219', 'grad_norm': '0.7291', 'learning_rate': '0.0001132', 'epoch': '0.3419'}
[text-trainer] {'loss': '1.331', 'grad_norm': '0.7011', 'learning_rate': '0.000112', 'epoch': '0.3475'}
[text-trainer] {'loss': '1.271', 'grad_norm': '1.039', 'learning_rate': '0.0001109', 'epoch': '0.3531'}
[text-trainer] {'loss': '1.136', 'grad_norm': '0.7434', 'learning_rate': '0.0001097', 'epoch': '0.3587'}
[text-trainer] {'loss': '1.137', 'grad_norm': '0.68', 'learning_rate': '0.0001085', 'epoch': '0.3643'}
[text-trainer] {'loss': '1.423', 'grad_norm': '0.7118', 'learning_rate': '0.0001073', 'epoch': '0.37'}
[text-trainer] {'loss': '1.444', 'grad_norm': '1.214', 'learning_rate': '0.0001062', 'epoch': '0.3756'}
[text-trainer] {'loss': '1.339', 'grad_norm': '0.8113', 'learning_rate': '0.000105', 'epoch': '0.3812'}
[text-trainer] {'loss': '1.377', 'grad_norm': '0.7581', 'learning_rate': '0.0001038', 'epoch': '0.3868'}
[text-trainer] {'loss': '1.166', 'grad_norm': '1.192', 'learning_rate': '0.0001026', 'epoch': '0.3924'}
[text-trainer] {'loss': '1.168', 'grad_norm': '0.5851', 'learning_rate': '0.0001014', 'epoch': '0.398'}
[text-trainer] {'loss': '1.213', 'grad_norm': '0.8443', 'learning_rate': '0.0001002', 'epoch': '0.4036'}
[text-trainer] {'loss': '1.192', 'grad_norm': '0.8546', 'learning_rate': '9.897e-05', 'epoch': '0.4092'}
[text-trainer] {'loss': '1.185', 'grad_norm': '0.7997', 'learning_rate': '9.776e-05', 'epoch': '0.4148'}
[text-trainer] {'loss': '1.29', 'grad_norm': '0.8813', 'learning_rate': '9.654e-05', 'epoch': '0.4204'}
[text-trainer] {'loss': '1.238', 'grad_norm': '0.9547', 'learning_rate': '9.533e-05', 'epoch': '0.426'}
[text-trainer] {'loss': '1.168', 'grad_norm': '1.05', 'learning_rate': '9.411e-05', 'epoch': '0.4316'}
[text-trainer] {'loss': '1.17', 'grad_norm': '1.129', 'learning_rate': '9.29e-05', 'epoch': '0.4372'}
[text-trainer] {'loss': '1.294', 'grad_norm': '0.7091', 'learning_rate': '9.168e-05', 'epoch': '0.4428'}
[text-trainer] {'loss': '1.146', 'grad_norm': '0.7721', 'learning_rate': '9.047e-05', 'epoch': '0.4484'}
[text-trainer] {'loss': '1.259', 'grad_norm': '0.7098', 'learning_rate': '8.926e-05', 'epoch': '0.454'}
[text-trainer] {'loss': '1.194', 'grad_norm': '1.014', 'learning_rate': '8.805e-05', 'epoch': '0.4596'}
[text-trainer] {'loss': '1.129', 'grad_norm': '0.7271', 'learning_rate': '8.684e-05', 'epoch': '0.4652'}
[text-trainer] {'loss': '1.293', 'grad_norm': '0.6769', 'learning_rate': '8.564e-05', 'epoch': '0.4709'}
[text-trainer] {'loss': '1.157', 'grad_norm': '0.9006', 'learning_rate': '8.443e-05', 'epoch': '0.4765'}
[text-trainer] {'loss': '1.326', 'grad_norm': '0.9052', 'learning_rate': '8.324e-05', 'epoch': '0.4821'}
[text-trainer] {'loss': '1.184', 'grad_norm': '0.8552', 'learning_rate': '8.205e-05', 'epoch': '0.4877'}
[text-trainer] {'loss': '1.39', 'grad_norm': '0.8288', 'learning_rate': '8.086e-05', 'epoch': '0.4933'}
[text-trainer] {'loss': '1.307', 'grad_norm': '1.291', 'learning_rate': '7.968e-05', 'epoch': '0.4989'}
[text-trainer] {'eval_loss': '1.276', 'eval_runtime': '8.554', 'eval_samples_per_second': '29.93', 'eval_steps_per_second': '7.482', 'epoch': '0.5'}
[text-trainer] {'loss': '1.259', 'grad_norm': '1.152', 'learning_rate': '7.851e-05', 'epoch': '0.5045'}
[text-trainer] {'loss': '1.208', 'grad_norm': '0.9028', 'learning_rate': '7.734e-05', 'epoch': '0.5101'}
[text-trainer] {'loss': '1.146', 'grad_norm': '0.9042', 'learning_rate': '7.618e-05', 'epoch': '0.5157'}
[text-trainer] {'loss': '1.264', 'grad_norm': '0.8043', 'learning_rate': '7.503e-05', 'epoch': '0.5213'}
[text-trainer] {'loss': '1.255', 'grad_norm': '1.186', 'learning_rate': '7.389e-05', 'epoch': '0.5269'}
[text-trainer] {'loss': '1.292', 'grad_norm': '0.6892', 'learning_rate': '7.276e-05', 'epoch': '0.5325'}
[text-trainer] {'loss': '1.066', 'grad_norm': '0.8959', 'learning_rate': '7.164e-05', 'epoch': '0.5381'}
[text-trainer] {'loss': '1.28', 'grad_norm': '0.9829', 'learning_rate': '7.052e-05', 'epoch': '0.5437'}
[text-trainer] {'loss': '1.354', 'grad_norm': '0.671', 'learning_rate': '6.942e-05', 'epoch': '0.5493'}
[text-trainer] {'loss': '1.041', 'grad_norm': '0.9016', 'learning_rate': '6.833e-05', 'epoch': '0.5549'}
[text-trainer] {'loss': '1.202', 'grad_norm': '1.161', 'learning_rate': '6.725e-05', 'epoch': '0.5605'}
[text-trainer] {'loss': '1.295', 'grad_norm': '1.066', 'learning_rate': '6.619e-05', 'epoch': '0.5661'}
[text-trainer] {'loss': '1.207', 'grad_norm': '0.8063', 'learning_rate': '6.514e-05', 'epoch': '0.5717'}
[text-trainer] {'loss': '1.19', 'grad_norm': '0.7805', 'learning_rate': '6.41e-05', 'epoch': '0.5774'}
[text-trainer] {'loss': '1.227', 'grad_norm': '0.8098', 'learning_rate': '6.307e-05', 'epoch': '0.583'}
[text-trainer] {'loss': '1.274', 'grad_norm': '0.6667', 'learning_rate': '6.206e-05', 'epoch': '0.5886'}
[text-trainer] {'loss': '1.058', 'grad_norm': '1.212', 'learning_rate': '6.106e-05', 'epoch': '0.5942'}
[text-trainer] {'loss': '1.219', 'grad_norm': '1.273', 'learning_rate': '6.008e-05', 'epoch': '0.5998'}
[text-trainer] {'loss': '1.252', 'grad_norm': '0.8018', 'learning_rate': '5.911e-05', 'epoch': '0.6054'}
[text-trainer] {'loss': '1.259', 'grad_norm': '0.8232', 'learning_rate': '5.817e-05', 'epoch': '0.611'}
[text-trainer] {'loss': '1.274', 'grad_norm': '0.7527', 'learning_rate': '5.723e-05', 'epoch': '0.6166'}
[text-trainer] {'loss': '1.174', 'grad_norm': '0.9725', 'learning_rate': '5.632e-05', 'epoch': '0.6222'}
[text-trainer] {'loss': '1.148', 'grad_norm': '1.094', 'learning_rate': '5.542e-05', 'epoch': '0.6278'}
[text-trainer] {'loss': '1.192', 'grad_norm': '0.8139', 'learning_rate': '5.454e-05', 'epoch': '0.6334'}
[text-trainer] {'loss': '1.216', 'grad_norm': '0.7615', 'learning_rate': '5.368e-05', 'epoch': '0.639'}
[text-trainer] {'loss': '1.203', 'grad_norm': '0.8662', 'learning_rate': '5.283e-05', 'epoch': '0.6446'}
[text-trainer] {'loss': '1.153', 'grad_norm': '0.7572', 'learning_rate': '5.201e-05', 'epoch': '0.6502'}
[text-trainer] {'loss': '1.298', 'grad_norm': '0.859', 'learning_rate': '5.12e-05', 'epoch': '0.6558'}
[text-trainer] {'loss': '1.274', 'grad_norm': '1.219', 'learning_rate': '5.042e-05', 'epoch': '0.6614'}
[text-trainer] {'loss': '1.159', 'grad_norm': '1.593', 'learning_rate': '4.965e-05', 'epoch': '0.667'}
[text-trainer] {'loss': '1.273', 'grad_norm': '1.252', 'learning_rate': '4.891e-05', 'epoch': '0.6726'}
[text-trainer] {'loss': '1.127', 'grad_norm': '1.02', 'learning_rate': '4.819e-05', 'epoch': '0.6783'}
[text-trainer] {'loss': '1.337', 'grad_norm': '1.566', 'learning_rate': '4.748e-05', 'epoch': '0.6839'}
[text-trainer] {'loss': '1.098', 'grad_norm': '0.7148', 'learning_rate': '4.68e-05', 'epoch': '0.6895'}
[text-trainer] {'loss': '1.191', 'grad_norm': '0.9882', 'learning_rate': '4.614e-05', 'epoch': '0.6951'}
[text-trainer] {'loss': '1.213', 'grad_norm': '1.078', 'learning_rate': '4.551e-05', 'epoch': '0.7007'}
[text-trainer] {'loss': '1.155', 'grad_norm': '0.6405', 'learning_rate': '4.489e-05', 'epoch': '0.7063'}
[text-trainer] {'loss': '1.138', 'grad_norm': '1.328', 'learning_rate': '4.43e-05', 'epoch': '0.7119'}
[text-trainer] {'loss': '1.171', 'grad_norm': '1.285', 'learning_rate': '4.374e-05', 'epoch': '0.7175'}
[text-trainer] {'loss': '1.25', 'grad_norm': '0.9613', 'learning_rate': '4.319e-05', 'epoch': '0.7231'}
[text-trainer] {'loss': '1.138', 'grad_norm': '1.011', 'learning_rate': '4.267e-05', 'epoch': '0.7287'}
[text-trainer] {'loss': '1.269', 'grad_norm': '1.014', 'learning_rate': '4.217e-05', 'epoch': '0.7343'}
[text-trainer] {'loss': '1.376', 'grad_norm': '1.555', 'learning_rate': '4.17e-05', 'epoch': '0.7399'}
[text-trainer] {'loss': '1.116', 'grad_norm': '0.7953', 'learning_rate': '4.125e-05', 'epoch': '0.7455'}
[text-trainer] {'eval_loss': '1.253', 'eval_runtime': '6.989', 'eval_samples_per_second': '36.63', 'eval_steps_per_second': '9.157', 'epoch': '0.75'}
[text-trainer] {'loss': '1.125', 'grad_norm': '0.8738', 'learning_rate': '4.083e-05', 'epoch': '0.7511'}
[text-trainer] {'loss': '1.268', 'grad_norm': '0.9615', 'learning_rate': '4.043e-05', 'epoch': '0.7567'}
[text-trainer] {'loss': '1.202', 'grad_norm': '0.8163', 'learning_rate': '4.005e-05', 'epoch': '0.7623'}
[text-trainer] {'loss': '1.342', 'grad_norm': '0.8375', 'learning_rate': '3.97e-05', 'epoch': '0.7679'}
[text-trainer] {'loss': '1.117', 'grad_norm': '0.8073', 'learning_rate': '3.938e-05', 'epoch': '0.7735'}
[text-trainer] {'loss': '1.113', 'grad_norm': '0.8958', 'learning_rate': '3.908e-05', 'epoch': '0.7791'}
[text-trainer] {'loss': '1.361', 'grad_norm': '0.9272', 'learning_rate': '3.881e-05', 'epoch': '0.7848'}
[text-trainer] {'loss': '1.423', 'grad_norm': '1.307', 'learning_rate': '3.856e-05', 'epoch': '0.7904'}
[text-trainer] {'loss': '1.287', 'grad_norm': '0.8824', 'learning_rate': '3.834e-05', 'epoch': '0.796'}
[text-trainer] {'loss': '1.336', 'grad_norm': '0.9668', 'learning_rate': '3.814e-05', 'epoch': '0.8016'}
[text-trainer] {'loss': '1.142', 'grad_norm': '0.7325', 'learning_rate': '3.797e-05', 'epoch': '0.8072'}
[text-trainer] {'loss': '1.294', 'grad_norm': '0.9281', 'learning_rate': '3.783e-05', 'epoch': '0.8128'}
[text-trainer] {'loss': '1.157', 'grad_norm': '1.326', 'learning_rate': '3.771e-05', 'epoch': '0.8184'}
[text-trainer] {'loss': '1.237', 'grad_norm': '0.5309', 'learning_rate': '3.762e-05', 'epoch': '0.824'}
[text-trainer] {'loss': '1.178', 'grad_norm': '1.037', 'learning_rate': '3.755e-05', 'epoch': '0.8296'}
[text-trainer] {'loss': '1.245', 'grad_norm': '0.9281', 'learning_rate': '3.751e-05', 'epoch': '0.8352'}
[text-trainer] {'eval_loss': '1.249', 'eval_runtime': '8.915', 'eval_samples_per_second': '28.71', 'eval_steps_per_second': '7.179', 'epoch': '0.8402'}
[text-trainer] {'train_runtime': '2400', 'train_samples_per_second': '9.992', 'train_steps_per_second': '0.625', 'train_loss': '1.266', 'epoch': '0.8402'}