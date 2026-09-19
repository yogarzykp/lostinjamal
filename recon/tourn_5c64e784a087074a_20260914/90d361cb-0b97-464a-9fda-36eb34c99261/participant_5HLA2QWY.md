# Loki — task 90d361cb-0b97-464a-9fda-36eb34c99261 — hotkey 5HLA2QWYy3GpNwCiBCwMMhGw5hpPosSeZ41my8B3nuFDQHNF
fetched 2026-09-19T05:10:40+00:00  lines=484  hit_page_cap=False  containers=['downloader-90d361cb-0b97-464a-9fda-36eb34c99261-4ed3a3ce', 'downloader-90d361cb-0b97-464a-9fda-36eb34c99261-92750f9b', 'fastapi', 'hf-upload-85406cbc56d9450ab4cbfd1841150417', 'text-trainer-0db135cb426b4ed5b2baa4b0dde10ae7']

[downloader-9] Downloading datasets to: /cache/datasets
[downloader-9] Downloading models to: /cache/models
[downloader-9] Model already cached at /cache/models/d9f7cf21608bd02c.
[downloader-9] Skipping download.
[downloader-9] Model path: /cache/models/d9f7cf21608bd02c
[downloader-9] Dataset path: /cache/datasets
[downloader-9] Downloading datasets to: /cache/datasets
[downloader-9] Downloading models to: /cache/models
[downloader-9] Model already cached at /cache/models/a0971600276b8e78.
[downloader-9] Skipping download.
[downloader-9] Model path: /cache/models/a0971600276b8e78
[downloader-9] Dataset path: /cache/datasets
[fastapi] Repository cloned successfully
[fastapi] Running Cache Download Container
[fastapi] Starting downloader container: downloader-90d361cb-0b97-464a-9fda-36eb34c99261-4ed3a3ce
[fastapi] Download completed successfully for task 90d361cb-0b97-464a-9fda-36eb34c99261
[fastapi] Building Docker image 'standalone-text-trainer:b7b0001f-0ce7-4b67-9840-3f94d152ef63' (timeout=1800s)...
[fastapi] Step 1/7 : FROM axolotlai/axolotl:main-20260701-py3.11-cu128-2.9.1@sha256:3aa6403f59f2268bb8f686f6c748d6fad2949580a0048cd25a605eb2de239ee5
[fastapi] Pulling from axolotlai/axolotlAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsDigest: sha256:3aa6403f59f2268bb8f686f6c748d6fad2949580a0048cd25a605eb2de239ee5Status: Downloaded newer image for axolotlai/axolotl:main-20260701-py3.11-cu128-2.9.1@sha256:3aa6403f59f2268bb8f686f6c748d6fad2949580a0048cd25a605eb2de239ee5 ---> 08c3197175de
[fastapi] Step 2/7 : ENV PYTHONUNBUFFERED=1     PIP_NO_CACHE_DIR=1     HF_HUB_DISABLE_TELEMETRY=1     HF_HUB_DISABLE_SYMLINKS_WARNING=1     TOKENIZERS_PARALLELISM=false     HF_HUB_OFFLINE=1     TRANSFORMERS_OFFLINE=1
[fastapi] ---> Running in 7b5aa05f21e5
[fastapi] ---> 28e9c70ad3f2
[fastapi] Step 3/7 : RUN TORCH_CUDA_ARCH_LIST="8.0;9.0+PTX" uv pip install         --python /workspace/axolotl-venv/bin/python         --no-cache --no-build-isolation causal-conv1d==1.6.2.post1
[fastapi] ---> Running in 2e4289ffe301
[fastapi] [91mUsing Python 3.11.15 environment at: /workspace/axolotl-venv
[fastapi] [0m[91mResolved 28 packages in 632ms
[fastapi] [0m[91m   Building causal-conv1d==1.6.2.post1
[fastapi] [0m[91m      Built causal-conv1d==1.6.2.post1
[fastapi] [0m[91mPrepared 1 package in 10.27s
[fastapi] [0m[91mInstalled 1 package in 3ms
[fastapi] + causal-conv1d==1.6.2.post1
[fastapi] [0m ---> 67d91b779ffe
[fastapi] Step 4/7 : WORKDIR /app
[fastapi] ---> Running in 0b7391fd177a
[fastapi] ---> 6cb8aa903b05
[fastapi] Step 5/7 : COPY forge /app/forge
[fastapi] ---> 0e3805b32c0c
[fastapi] Step 6/7 : COPY pyproject.toml LICENSE.md NOTICE /app/
[fastapi] ---> 0fd825880bc6
[fastapi] Step 7/7 : ENTRYPOINT ["/workspace/axolotl-venv/bin/python", "-m", "forge.cli"]
[fastapi] ---> Running in 1864c6f11420
[fastapi] ---> f310eaef3b9f
[fastapi] {'aux': {'ID': 'sha256:f310eaef3b9f17eb69021c740df1f501aa08955d7ef848a6811668be2cc771c5'}}Successfully built f310eaef3b9f
[fastapi] Successfully tagged standalone-text-trainer:b7b0001f-0ce7-4b67-9840-3f94d152ef63
[fastapi] Docker image built successfully.
[fastapi] Training job failed: 90d361cb-0b97-464a-9fda-36eb34c99261
[fastapi] Cleaning up
[fastapi] Cleaned up Docker resources.
[fastapi] Repository cloned successfully
[fastapi] Running Cache Download Container
[fastapi] Starting downloader container: downloader-90d361cb-0b97-464a-9fda-36eb34c99261-92750f9b
[fastapi] Download completed successfully for task 90d361cb-0b97-464a-9fda-36eb34c99261
[fastapi] Building Docker image 'standalone-text-trainer:343212c1-8ea6-492e-83fc-69d9e8141c9a' (timeout=1800s)...
[fastapi] Step 1/7 : FROM axolotlai/axolotl:main-20260701-py3.11-cu128-2.9.1@sha256:3aa6403f59f2268bb8f686f6c748d6fad2949580a0048cd25a605eb2de239ee5
[fastapi] Pulling from axolotlai/axolotlAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsAlready existsDigest: sha256:3aa6403f59f2268bb8f686f6c748d6fad2949580a0048cd25a605eb2de239ee5Status: Downloaded newer image for axolotlai/axolotl:main-20260701-py3.11-cu128-2.9.1@sha256:3aa6403f59f2268bb8f686f6c748d6fad2949580a0048cd25a605eb2de239ee5 ---> 08c3197175de
[fastapi] Step 2/7 : ENV PYTHONUNBUFFERED=1     PIP_NO_CACHE_DIR=1     HF_HUB_DISABLE_TELEMETRY=1     HF_HUB_DISABLE_SYMLINKS_WARNING=1     TOKENIZERS_PARALLELISM=false     HF_HUB_OFFLINE=1     TRANSFORMERS_OFFLINE=1
[fastapi] ---> Running in 1a629e02c7bc
[fastapi] ---> 6b6be5cda3a3
[fastapi] Step 3/7 : RUN TORCH_CUDA_ARCH_LIST="8.0;9.0+PTX" uv pip install         --python /workspace/axolotl-venv/bin/python         --no-cache --no-build-isolation causal-conv1d==1.6.2.post1
[fastapi] ---> Running in da397af48157
[fastapi] [91mUsing Python 3.11.15 environment at: /workspace/axolotl-venv
[fastapi] [0m[91mResolved 28 packages in 242ms
[fastapi] [0m[91m   Building causal-conv1d==1.6.2.post1
[fastapi] [0m[91m      Built causal-conv1d==1.6.2.post1
[fastapi] [0m[91mPrepared 1 package in 5.05s
[fastapi] [0m[91mInstalled 1 package in 0.73ms
[fastapi] + causal-conv1d==1.6.2.post1
[fastapi] [0m ---> b53594269a9a
[fastapi] Step 4/7 : WORKDIR /app
[fastapi] ---> Running in 547daff25c8c
[fastapi] ---> 9bbfc890ed23
[fastapi] Step 5/7 : COPY forge /app/forge
[fastapi] ---> c35910f7580d
[fastapi] Step 6/7 : COPY pyproject.toml LICENSE.md NOTICE /app/
[fastapi] ---> ba41d4b7fbce
[fastapi] Step 7/7 : ENTRYPOINT ["/workspace/axolotl-venv/bin/python", "-m", "forge.cli"]
[fastapi] ---> Running in 25b52acd82c9
[fastapi] ---> c5678b8c9b75
[fastapi] {'aux': {'ID': 'sha256:c5678b8c9b75baaf7bc7a85962cfc204e59619be5c7783f1ab622089bfc00bb8'}}Successfully built c5678b8c9b75
[fastapi] Successfully tagged standalone-text-trainer:343212c1-8ea6-492e-83fc-69d9e8141c9a
[fastapi] Docker image built successfully.
[fastapi] Container.wait() returned: {'StatusCode': 0}
[fastapi] Cleaning up
[fastapi] Cleaned up Docker resources.
[fastapi] Starting upload container hf-upload-85406cbc56d9450ab4cbfd1841150417 for task 90d361cb-0b97-464a-9fda-36eb34c99261...
[hf-upload-85] Updated adapter_config.json with base_model: LiquidAI/LFM2.5-2.6B
[hf-upload-85] Updated README.md with base_model: LiquidAI/LFM2.5-2.6B
[hf-upload-85] Creating repo gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-90d361cb-0b97-464a-9fda-36eb34c99261-5HLA2QWY...
[hf-upload-85] Uploading contents of /app/checkpoints/90d361cb-0b97-464a-9fda-36eb34c99261/tournament-tourn_5c64e784a087074a_20260914-90d361cb-0b97-464a-9fda-36eb34c99261-5HLA2QWY to gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-90d361cb-0b97-464a-9fda-36eb34c99261-5HLA2QWY
[hf-upload-85] Uploaded successfully to https://huggingface.co/gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-90d361cb-0b97-464a-9fda-36eb34c99261-5HLA2QWY
[hf-upload-85] Deleted local folder: /app/checkpoints/90d361cb-0b97-464a-9fda-36eb34c99261/tournament-tourn_5c64e784a087074a_20260914-90d361cb-0b97-464a-9fda-36eb34c99261-5HLA2QWY
[text-trainer] Skipping import of cpp extensions due to incompatible torch version. Please upgrade to torch >= 2.11.0 (found 2.9.1+cu128).
[text-trainer] [INFO] Running in WANDB offline mode
[text-trainer] [transformers] warmup_ratio is deprecated and will be removed in v5.2. Use `warmup_steps` instead.
[text-trainer] {'train_runtime': '1.18', 'train_samples_per_second': '13.56', 'train_steps_per_second': '0.848', 'train_loss': '0.3397', 'epoch': '1'}
[text-trainer] [transformers] warmup_ratio is deprecated and will be removed in v5.2. Use `warmup_steps` instead.
[text-trainer] [transformers] warmup_ratio is deprecated and will be removed in v5.2. Use `warmup_steps` instead.
[text-trainer] {'train_runtime': '0.7247', 'train_samples_per_second': '22.08', 'train_steps_per_second': '1.38', 'train_loss': '0.3397', 'epoch': '1'}
[text-trainer] [transformers] warmup_ratio is deprecated and will be removed in v5.2. Use `warmup_steps` instead.
[text-trainer] {'train_runtime': '1.699', 'train_samples_per_second': '9.419', 'train_steps_per_second': '0.589', 'train_loss': '0.1604', 'epoch': '1'}
[text-trainer] [transformers] warmup_ratio is deprecated and will be removed in v5.2. Use `warmup_steps` instead.
[text-trainer] {'loss': '0.5531', 'grad_norm': '1.46', 'learning_rate': '0', 'epoch': '0.25'}
[text-trainer] {'loss': '0.5545', 'grad_norm': '2.081', 'learning_rate': '0', 'epoch': '0.5'}
[text-trainer] {'loss': '0.5467', 'grad_norm': '2.585', 'learning_rate': '0', 'epoch': '0.75'}
[text-trainer] {'train_runtime': '43.69', 'train_samples_per_second': '12.82', 'train_steps_per_second': '0.801', 'train_loss': '0.5514', 'epoch': '0.75'}
[text-trainer] [transformers] warmup_ratio is deprecated and will be removed in v5.2. Use `warmup_steps` instead.
[text-trainer] {'loss': '0.5244', 'grad_norm': '1.325', 'learning_rate': '1.227e-05', 'epoch': '0.002729'}
[text-trainer] {'loss': '0.4434', 'grad_norm': '0.2874', 'learning_rate': '2.591e-05', 'epoch': '0.005457'}
[text-trainer] {'loss': '0.385', 'grad_norm': '0.3004', 'learning_rate': '3.955e-05', 'epoch': '0.008186'}
[text-trainer] {'loss': '0.3679', 'grad_norm': '0.3135', 'learning_rate': '5.318e-05', 'epoch': '0.01091'}
[text-trainer] {'loss': '0.3237', 'grad_norm': '0.2655', 'learning_rate': '6.682e-05', 'epoch': '0.01364'}
[text-trainer] {'loss': '0.3284', 'grad_norm': '0.2447', 'learning_rate': '8.045e-05', 'epoch': '0.01637'}
[text-trainer] {'loss': '0.3307', 'grad_norm': '0.2614', 'learning_rate': '9.409e-05', 'epoch': '0.0191'}
[text-trainer] {'loss': '0.3266', 'grad_norm': '0.3264', 'learning_rate': '0.0001077', 'epoch': '0.02183'}
[text-trainer] {'loss': '0.3318', 'grad_norm': '0.2662', 'learning_rate': '0.0001214', 'epoch': '0.02456'}
[text-trainer] {'loss': '0.295', 'grad_norm': '0.2496', 'learning_rate': '0.000135', 'epoch': '0.02729'}
[text-trainer] {'loss': '0.3309', 'grad_norm': '0.6285', 'learning_rate': '0.0001486', 'epoch': '0.03002'}
[text-trainer] {'loss': '0.3123', 'grad_norm': '0.2337', 'learning_rate': '0.00015', 'epoch': '0.03274'}
[text-trainer] {'loss': '0.2992', 'grad_norm': '0.2208', 'learning_rate': '0.00015', 'epoch': '0.03547'}
[text-trainer] {'loss': '0.2831', 'grad_norm': '0.202', 'learning_rate': '0.00015', 'epoch': '0.0382'}
[text-trainer] {'loss': '0.3165', 'grad_norm': '0.2318', 'learning_rate': '0.00015', 'epoch': '0.04093'}
[text-trainer] {'loss': '0.3102', 'grad_norm': '0.2179', 'learning_rate': '0.0001499', 'epoch': '0.04366'}
[text-trainer] {'loss': '0.3284', 'grad_norm': '0.2485', 'learning_rate': '0.0001499', 'epoch': '0.04639'}
[text-trainer] {'loss': '0.2993', 'grad_norm': '0.1976', 'learning_rate': '0.0001499', 'epoch': '0.04912'}
[text-trainer] {'loss': '0.2956', 'grad_norm': '0.1855', 'learning_rate': '0.0001499', 'epoch': '0.05185'}
[text-trainer] {'loss': '0.3002', 'grad_norm': '0.2033', 'learning_rate': '0.0001498', 'epoch': '0.05457'}
[text-trainer] {'loss': '0.304', 'grad_norm': '0.2208', 'learning_rate': '0.0001498', 'epoch': '0.0573'}
[text-trainer] {'loss': '0.3101', 'grad_norm': '0.2307', 'learning_rate': '0.0001497', 'epoch': '0.06003'}
[text-trainer] {'loss': '0.314', 'grad_norm': '0.2043', 'learning_rate': '0.0001497', 'epoch': '0.06276'}
[text-trainer] {'loss': '0.3059', 'grad_norm': '0.1784', 'learning_rate': '0.0001496', 'epoch': '0.06549'}
[text-trainer] {'loss': '0.3272', 'grad_norm': '0.2255', 'learning_rate': '0.0001496', 'epoch': '0.06822'}
[text-trainer] {'loss': '0.3167', 'grad_norm': '0.2045', 'learning_rate': '0.0001495', 'epoch': '0.07095'}
[text-trainer] {'loss': '0.3003', 'grad_norm': '0.2052', 'learning_rate': '0.0001494', 'epoch': '0.07367'}
[text-trainer] {'loss': '0.2922', 'grad_norm': '0.2279', 'learning_rate': '0.0001494', 'epoch': '0.0764'}
[text-trainer] {'loss': '0.3189', 'grad_norm': '0.2248', 'learning_rate': '0.0001493', 'epoch': '0.07913'}
[text-trainer] {'loss': '0.3239', 'grad_norm': '0.2072', 'learning_rate': '0.0001492', 'epoch': '0.08186'}
[text-trainer] {'loss': '0.2806', 'grad_norm': '0.2383', 'learning_rate': '0.0001491', 'epoch': '0.08459'}
[text-trainer] {'loss': '0.3113', 'grad_norm': '0.2147', 'learning_rate': '0.000149', 'epoch': '0.08732'}
[text-trainer] {'loss': '0.299', 'grad_norm': '0.2677', 'learning_rate': '0.0001489', 'epoch': '0.09005'}
[text-trainer] {'loss': '0.3189', 'grad_norm': '0.2051', 'learning_rate': '0.0001489', 'epoch': '0.09278'}
[text-trainer] {'loss': '0.3046', 'grad_norm': '0.1909', 'learning_rate': '0.0001488', 'epoch': '0.0955'}
[text-trainer] {'loss': '0.3225', 'grad_norm': '0.2163', 'learning_rate': '0.0001486', 'epoch': '0.09823'}
[text-trainer] {'loss': '0.3223', 'grad_norm': '0.1883', 'learning_rate': '0.0001485', 'epoch': '0.101'}
[text-trainer] {'loss': '0.3325', 'grad_norm': '0.1791', 'learning_rate': '0.0001484', 'epoch': '0.1037'}
[text-trainer] {'loss': '0.3017', 'grad_norm': '0.187', 'learning_rate': '0.0001483', 'epoch': '0.1064'}
[text-trainer] {'loss': '0.3222', 'grad_norm': '0.1922', 'learning_rate': '0.0001482', 'epoch': '0.1091'}
[text-trainer] {'loss': '0.3016', 'grad_norm': '0.2025', 'learning_rate': '0.000148', 'epoch': '0.1119'}
[text-trainer] {'loss': '0.2963', 'grad_norm': '0.2241', 'learning_rate': '0.0001479', 'epoch': '0.1146'}
[text-trainer] {'loss': '0.3545', 'grad_norm': '0.2032', 'learning_rate': '0.0001478', 'epoch': '0.1173'}
[text-trainer] {'loss': '0.3066', 'grad_norm': '0.2114', 'learning_rate': '0.0001476', 'epoch': '0.1201'}
[text-trainer] {'loss': '0.3049', 'grad_norm': '0.1889', 'learning_rate': '0.0001475', 'epoch': '0.1228'}
[text-trainer] {'loss': '0.3142', 'grad_norm': '0.1384', 'learning_rate': '0.0001473', 'epoch': '0.1255'}
[text-trainer] {'loss': '0.2889', 'grad_norm': '0.2633', 'learning_rate': '0.0001472', 'epoch': '0.1282'}
[text-trainer] {'loss': '0.2822', 'grad_norm': '0.2133', 'learning_rate': '0.000147', 'epoch': '0.131'}
[text-trainer] {'loss': '0.3085', 'grad_norm': '0.1824', 'learning_rate': '0.0001469', 'epoch': '0.1337'}
[text-trainer] {'loss': '0.2952', 'grad_norm': '0.211', 'learning_rate': '0.0001467', 'epoch': '0.1364'}
[text-trainer] {'loss': '0.3117', 'grad_norm': '0.2521', 'learning_rate': '0.0001465', 'epoch': '0.1392'}
[text-trainer] {'loss': '0.3232', 'grad_norm': '0.1794', 'learning_rate': '0.0001464', 'epoch': '0.1419'}
[text-trainer] {'loss': '0.3081', 'grad_norm': '0.172', 'learning_rate': '0.0001462', 'epoch': '0.1446'}
[text-trainer] {'loss': '0.3011', 'grad_norm': '0.1811', 'learning_rate': '0.000146', 'epoch': '0.1473'}
[text-trainer] {'loss': '0.2983', 'grad_norm': '0.2002', 'learning_rate': '0.0001458', 'epoch': '0.1501'}
[text-trainer] {'loss': '0.2876', 'grad_norm': '0.2025', 'learning_rate': '0.0001456', 'epoch': '0.1528'}
[text-trainer] {'loss': '0.3069', 'grad_norm': '0.2375', 'learning_rate': '0.0001454', 'epoch': '0.1555'}
[text-trainer] {'loss': '0.3009', 'grad_norm': '0.2059', 'learning_rate': '0.0001452', 'epoch': '0.1583'}
[text-trainer] {'loss': '0.2903', 'grad_norm': '0.2232', 'learning_rate': '0.000145', 'epoch': '0.161'}
[text-trainer] {'loss': '0.3137', 'grad_norm': '0.2022', 'learning_rate': '0.0001448', 'epoch': '0.1637'}
[text-trainer] {'loss': '0.3006', 'grad_norm': '0.1715', 'learning_rate': '0.0001446', 'epoch': '0.1665'}
[text-trainer] {'loss': '0.3045', 'grad_norm': '0.1771', 'learning_rate': '0.0001444', 'epoch': '0.1692'}
[text-trainer] {'loss': '0.289', 'grad_norm': '0.2301', 'learning_rate': '0.0001442', 'epoch': '0.1719'}
[text-trainer] {'loss': '0.2913', 'grad_norm': '0.2011', 'learning_rate': '0.000144', 'epoch': '0.1746'}
[text-trainer] {'loss': '0.2791', 'grad_norm': '0.202', 'learning_rate': '0.0001437', 'epoch': '0.1774'}
[text-trainer] {'loss': '0.3131', 'grad_norm': '0.2147', 'learning_rate': '0.0001435', 'epoch': '0.1801'}
[text-trainer] {'loss': '0.2841', 'grad_norm': '0.2192', 'learning_rate': '0.0001433', 'epoch': '0.1828'}
[text-trainer] {'loss': '0.3015', 'grad_norm': '0.1942', 'learning_rate': '0.000143', 'epoch': '0.1856'}
[text-trainer] {'loss': '0.2931', 'grad_norm': '0.2022', 'learning_rate': '0.0001428', 'epoch': '0.1883'}
[text-trainer] {'loss': '0.2915', 'grad_norm': '0.1858', 'learning_rate': '0.0001426', 'epoch': '0.191'}
[text-trainer] {'loss': '0.3261', 'grad_norm': '0.1846', 'learning_rate': '0.0001423', 'epoch': '0.1937'}
[text-trainer] {'loss': '0.2956', 'grad_norm': '0.2159', 'learning_rate': '0.000142', 'epoch': '0.1965'}
[text-trainer] {'loss': '0.2982', 'grad_norm': '0.2184', 'learning_rate': '0.0001418', 'epoch': '0.1992'}
[text-trainer] {'loss': '0.2844', 'grad_norm': '0.1802', 'learning_rate': '0.0001415', 'epoch': '0.2019'}
[text-trainer] {'loss': '0.3021', 'grad_norm': '0.1907', 'learning_rate': '0.0001413', 'epoch': '0.2047'}
[text-trainer] {'loss': '0.313', 'grad_norm': '0.222', 'learning_rate': '0.000141', 'epoch': '0.2074'}
[text-trainer] {'loss': '0.2792', 'grad_norm': '0.1593', 'learning_rate': '0.0001407', 'epoch': '0.2101'}
[text-trainer] {'loss': '0.3101', 'grad_norm': '0.2312', 'learning_rate': '0.0001405', 'epoch': '0.2128'}
[text-trainer] {'loss': '0.2731', 'grad_norm': '0.1771', 'learning_rate': '0.0001402', 'epoch': '0.2156'}
[text-trainer] {'loss': '0.3019', 'grad_norm': '0.1734', 'learning_rate': '0.0001399', 'epoch': '0.2183'}
[text-trainer] {'loss': '0.3016', 'grad_norm': '0.2182', 'learning_rate': '0.0001396', 'epoch': '0.221'}
[text-trainer] {'loss': '0.3214', 'grad_norm': '0.2007', 'learning_rate': '0.0001393', 'epoch': '0.2238'}
[text-trainer] {'loss': '0.3035', 'grad_norm': '0.1887', 'learning_rate': '0.000139', 'epoch': '0.2265'}
[text-trainer] {'loss': '0.2838', 'grad_norm': '0.1869', 'learning_rate': '0.0001387', 'epoch': '0.2292'}
[text-trainer] {'loss': '0.2736', 'grad_norm': '0.1707', 'learning_rate': '0.0001384', 'epoch': '0.2319'}
[text-trainer] {'loss': '0.2994', 'grad_norm': '0.2185', 'learning_rate': '0.0001381', 'epoch': '0.2347'}
[text-trainer] {'loss': '0.2989', 'grad_norm': '0.2232', 'learning_rate': '0.0001378', 'epoch': '0.2374'}
[text-trainer] {'loss': '0.2662', 'grad_norm': '0.1759', 'learning_rate': '0.0001375', 'epoch': '0.2401'}
[text-trainer] {'loss': '0.3295', 'grad_norm': '0.1905', 'learning_rate': '0.0001372', 'epoch': '0.2429'}
[text-trainer] {'loss': '0.2889', 'grad_norm': '0.1777', 'learning_rate': '0.0001369', 'epoch': '0.2456'}
[text-trainer] {'loss': '0.2935', 'grad_norm': '0.2121', 'learning_rate': '0.0001366', 'epoch': '0.2483'}
[text-trainer] {'eval_loss': '0.2912', 'eval_runtime': '6.235', 'eval_samples_per_second': '41.06', 'eval_steps_per_second': '10.26', 'epoch': '0.2499'}
[text-trainer] {'loss': '0.3032', 'grad_norm': '0.2007', 'learning_rate': '0.0001362', 'epoch': '0.251'}
[text-trainer] {'loss': '0.2837', 'grad_norm': '0.1694', 'learning_rate': '0.0001359', 'epoch': '0.2538'}
[text-trainer] {'loss': '0.276', 'grad_norm': '0.1736', 'learning_rate': '0.0001356', 'epoch': '0.2565'}
[text-trainer] {'loss': '0.3108', 'grad_norm': '0.2147', 'learning_rate': '0.0001352', 'epoch': '0.2592'}
[text-trainer] {'loss': '0.3076', 'grad_norm': '0.1956', 'learning_rate': '0.0001349', 'epoch': '0.262'}
[text-trainer] {'loss': '0.3067', 'grad_norm': '0.2387', 'learning_rate': '0.0001346', 'epoch': '0.2647'}
[text-trainer] {'loss': '0.2857', 'grad_norm': '0.2013', 'learning_rate': '0.0001342', 'epoch': '0.2674'}
[text-trainer] {'loss': '0.2796', 'grad_norm': '0.2386', 'learning_rate': '0.0001339', 'epoch': '0.2701'}
[text-trainer] {'loss': '0.3054', 'grad_norm': '0.1938', 'learning_rate': '0.0001335', 'epoch': '0.2729'}
[text-trainer] {'loss': '0.2998', 'grad_norm': '0.2153', 'learning_rate': '0.0001332', 'epoch': '0.2756'}
[text-trainer] {'loss': '0.2702', 'grad_norm': '0.173', 'learning_rate': '0.0001328', 'epoch': '0.2783'}
[text-trainer] {'loss': '0.2868', 'grad_norm': '0.182', 'learning_rate': '0.0001324', 'epoch': '0.2811'}
[text-trainer] {'loss': '0.3099', 'grad_norm': '0.2502', 'learning_rate': '0.0001321', 'epoch': '0.2838'}
[text-trainer] {'loss': '0.2793', 'grad_norm': '0.1787', 'learning_rate': '0.0001317', 'epoch': '0.2865'}
[text-trainer] {'loss': '0.3036', 'grad_norm': '0.1997', 'learning_rate': '0.0001314', 'epoch': '0.2892'}
[text-trainer] {'loss': '0.292', 'grad_norm': '0.2173', 'learning_rate': '0.000131', 'epoch': '0.292'}
[text-trainer] {'loss': '0.3239', 'grad_norm': '0.1965', 'learning_rate': '0.0001306', 'epoch': '0.2947'}
[text-trainer] {'loss': '0.272', 'grad_norm': '0.2114', 'learning_rate': '0.0001302', 'epoch': '0.2974'}
[text-trainer] {'loss': '0.299', 'grad_norm': '0.1693', 'learning_rate': '0.0001298', 'epoch': '0.3002'}
[text-trainer] {'loss': '0.287', 'grad_norm': '0.1887', 'learning_rate': '0.0001295', 'epoch': '0.3029'}
[text-trainer] {'loss': '0.3232', 'grad_norm': '0.1841', 'learning_rate': '0.0001291', 'epoch': '0.3056'}
[text-trainer] {'loss': '0.2915', 'grad_norm': '0.1892', 'learning_rate': '0.0001287', 'epoch': '0.3083'}
[text-trainer] {'loss': '0.3333', 'grad_norm': '0.209', 'learning_rate': '0.0001283', 'epoch': '0.3111'}
[text-trainer] {'loss': '0.29', 'grad_norm': '0.1943', 'learning_rate': '0.0001279', 'epoch': '0.3138'}
[text-trainer] {'loss': '0.2975', 'grad_norm': '0.195', 'learning_rate': '0.0001275', 'epoch': '0.3165'}
[text-trainer] {'loss': '0.295', 'grad_norm': '0.1974', 'learning_rate': '0.0001271', 'epoch': '0.3193'}
[text-trainer] {'loss': '0.3104', 'grad_norm': '0.1697', 'learning_rate': '0.0001267', 'epoch': '0.322'}
[text-trainer] {'loss': '0.2773', 'grad_norm': '0.1664', 'learning_rate': '0.0001263', 'epoch': '0.3247'}
[text-trainer] {'loss': '0.2848', 'grad_norm': '0.1635', 'learning_rate': '0.0001259', 'epoch': '0.3274'}
[text-trainer] {'loss': '0.261', 'grad_norm': '0.1779', 'learning_rate': '0.0001255', 'epoch': '0.3302'}
[text-trainer] {'loss': '0.2794', 'grad_norm': '0.2018', 'learning_rate': '0.0001251', 'epoch': '0.3329'}
[text-trainer] {'loss': '0.3283', 'grad_norm': '0.3087', 'learning_rate': '0.0001247', 'epoch': '0.3356'}
[text-trainer] {'loss': '0.3142', 'grad_norm': '0.2396', 'learning_rate': '0.0001243', 'epoch': '0.3384'}
[text-trainer] {'loss': '0.2738', 'grad_norm': '0.1728', 'learning_rate': '0.0001238', 'epoch': '0.3411'}
[text-trainer] {'loss': '0.2925', 'grad_norm': '0.2059', 'learning_rate': '0.0001234', 'epoch': '0.3438'}
[text-trainer] {'loss': '0.3165', 'grad_norm': '0.2132', 'learning_rate': '0.000123', 'epoch': '0.3465'}
[text-trainer] {'loss': '0.2865', 'grad_norm': '0.1498', 'learning_rate': '0.0001226', 'epoch': '0.3493'}
[text-trainer] {'loss': '0.2808', 'grad_norm': '0.1867', 'learning_rate': '0.0001221', 'epoch': '0.352'}
[text-trainer] {'loss': '0.2751', 'grad_norm': '0.1538', 'learning_rate': '0.0001217', 'epoch': '0.3547'}
[text-trainer] {'loss': '0.3043', 'grad_norm': '0.1876', 'learning_rate': '0.0001213', 'epoch': '0.3575'}
[text-trainer] {'loss': '0.3081', 'grad_norm': '0.2215', 'learning_rate': '0.0001208', 'epoch': '0.3602'}
[text-trainer] {'loss': '0.2882', 'grad_norm': '0.1862', 'learning_rate': '0.0001204', 'epoch': '0.3629'}
[text-trainer] {'loss': '0.2943', 'grad_norm': '0.1761', 'learning_rate': '0.00012', 'epoch': '0.3656'}
[text-trainer] {'loss': '0.3016', 'grad_norm': '0.1952', 'learning_rate': '0.0001195', 'epoch': '0.3684'}
[text-trainer] {'loss': '0.305', 'grad_norm': '0.1682', 'learning_rate': '0.0001191', 'epoch': '0.3711'}
[text-trainer] {'loss': '0.2988', 'grad_norm': '0.2133', 'learning_rate': '0.0001186', 'epoch': '0.3738'}
[text-trainer] {'loss': '0.2919', 'grad_norm': '0.1811', 'learning_rate': '0.0001182', 'epoch': '0.3766'}
[text-trainer] {'loss': '0.2852', 'grad_norm': '0.2426', 'learning_rate': '0.0001177', 'epoch': '0.3793'}
[text-trainer] {'loss': '0.291', 'grad_norm': '0.2128', 'learning_rate': '0.0001173', 'epoch': '0.382'}
[text-trainer] {'loss': '0.2744', 'grad_norm': '0.1637', 'learning_rate': '0.0001168', 'epoch': '0.3847'}
[text-trainer] {'loss': '0.3082', 'grad_norm': '0.1761', 'learning_rate': '0.0001164', 'epoch': '0.3875'}
[text-trainer] {'loss': '0.2961', 'grad_norm': '0.1713', 'learning_rate': '0.0001159', 'epoch': '0.3902'}
[text-trainer] {'loss': '0.289', 'grad_norm': '0.2436', 'learning_rate': '0.0001155', 'epoch': '0.3929'}
[text-trainer] {'loss': '0.3049', 'grad_norm': '0.167', 'learning_rate': '0.000115', 'epoch': '0.3957'}
[text-trainer] {'loss': '0.2704', 'grad_norm': '0.1986', 'learning_rate': '0.0001145', 'epoch': '0.3984'}
[text-trainer] {'loss': '0.2888', 'grad_norm': '0.2076', 'learning_rate': '0.0001141', 'epoch': '0.4011'}
[text-trainer] {'loss': '0.2836', 'grad_norm': '0.1806', 'learning_rate': '0.0001136', 'epoch': '0.4038'}
[text-trainer] {'loss': '0.3021', 'grad_norm': '0.2089', 'learning_rate': '0.0001132', 'epoch': '0.4066'}
[text-trainer] {'loss': '0.2811', 'grad_norm': '0.1907', 'learning_rate': '0.0001127', 'epoch': '0.4093'}
[text-trainer] {'loss': '0.2856', 'grad_norm': '0.1819', 'learning_rate': '0.0001122', 'epoch': '0.412'}
[text-trainer] {'loss': '0.308', 'grad_norm': '0.1965', 'learning_rate': '0.0001117', 'epoch': '0.4148'}
[text-trainer] {'loss': '0.2956', 'grad_norm': '0.2032', 'learning_rate': '0.0001113', 'epoch': '0.4175'}
[text-trainer] {'loss': '0.2742', 'grad_norm': '0.1747', 'learning_rate': '0.0001108', 'epoch': '0.4202'}
[text-trainer] {'loss': '0.2879', 'grad_norm': '0.2035', 'learning_rate': '0.0001103', 'epoch': '0.4229'}
[text-trainer] {'loss': '0.2916', 'grad_norm': '0.1765', 'learning_rate': '0.0001099', 'epoch': '0.4257'}
[text-trainer] {'loss': '0.3108', 'grad_norm': '0.3572', 'learning_rate': '0.0001094', 'epoch': '0.4284'}
[text-trainer] {'loss': '0.3039', 'grad_norm': '0.163', 'learning_rate': '0.0001089', 'epoch': '0.4311'}
[text-trainer] {'loss': '0.2836', 'grad_norm': '0.2281', 'learning_rate': '0.0001084', 'epoch': '0.4339'}
[text-trainer] {'loss': '0.292', 'grad_norm': '0.2366', 'learning_rate': '0.0001079', 'epoch': '0.4366'}
[text-trainer] {'loss': '0.2818', 'grad_norm': '0.1769', 'learning_rate': '0.0001075', 'epoch': '0.4393'}
[text-trainer] {'loss': '0.2822', 'grad_norm': '0.189', 'learning_rate': '0.000107', 'epoch': '0.442'}
[text-trainer] {'loss': '0.3021', 'grad_norm': '0.1768', 'learning_rate': '0.0001065', 'epoch': '0.4448'}
[text-trainer] {'loss': '0.2817', 'grad_norm': '0.1782', 'learning_rate': '0.000106', 'epoch': '0.4475'}
[text-trainer] {'loss': '0.3083', 'grad_norm': '0.1874', 'learning_rate': '0.0001055', 'epoch': '0.4502'}
[text-trainer] {'loss': '0.2941', 'grad_norm': '0.1863', 'learning_rate': '0.000105', 'epoch': '0.453'}
[text-trainer] {'loss': '0.2868', 'grad_norm': '0.2103', 'learning_rate': '0.0001045', 'epoch': '0.4557'}
[text-trainer] {'loss': '0.3076', 'grad_norm': '0.246', 'learning_rate': '0.0001041', 'epoch': '0.4584'}
[text-trainer] {'loss': '0.2976', 'grad_norm': '0.2211', 'learning_rate': '0.0001036', 'epoch': '0.4612'}
[text-trainer] {'loss': '0.2801', 'grad_norm': '0.1877', 'learning_rate': '0.0001031', 'epoch': '0.4639'}
[text-trainer] {'loss': '0.2984', 'grad_norm': '0.1802', 'learning_rate': '0.0001026', 'epoch': '0.4666'}
[text-trainer] {'loss': '0.2959', 'grad_norm': '0.2108', 'learning_rate': '0.0001021', 'epoch': '0.4693'}
[text-trainer] {'loss': '0.2756', 'grad_norm': '0.1786', 'learning_rate': '0.0001016', 'epoch': '0.4721'}
[text-trainer] {'loss': '0.2986', 'grad_norm': '0.1927', 'learning_rate': '0.0001011', 'epoch': '0.4748'}
[text-trainer] {'loss': '0.2725', 'grad_norm': '0.2322', 'learning_rate': '0.0001006', 'epoch': '0.4775'}
[text-trainer] {'loss': '0.292', 'grad_norm': '0.2112', 'learning_rate': '0.0001001', 'epoch': '0.4803'}
[text-trainer] {'loss': '0.3017', 'grad_norm': '0.2018', 'learning_rate': '9.963e-05', 'epoch': '0.483'}
[text-trainer] {'loss': '0.2903', 'grad_norm': '0.2875', 'learning_rate': '9.914e-05', 'epoch': '0.4857'}
[text-trainer] {'loss': '0.2943', 'grad_norm': '0.1498', 'learning_rate': '9.864e-05', 'epoch': '0.4884'}
[text-trainer] {'loss': '0.2929', 'grad_norm': '0.2274', 'learning_rate': '9.814e-05', 'epoch': '0.4912'}
[text-trainer] {'loss': '0.3045', 'grad_norm': '0.193', 'learning_rate': '9.765e-05', 'epoch': '0.4939'}
[text-trainer] {'loss': '0.2938', 'grad_norm': '0.2065', 'learning_rate': '9.715e-05', 'epoch': '0.4966'}
[text-trainer] {'loss': '0.2907', 'grad_norm': '0.1868', 'learning_rate': '9.666e-05', 'epoch': '0.4994'}
[text-trainer] {'eval_loss': '0.2837', 'eval_runtime': '6.182', 'eval_samples_per_second': '41.41', 'eval_steps_per_second': '10.35', 'epoch': '0.4999'}
[text-trainer] {'loss': '0.2643', 'grad_norm': '0.2237', 'learning_rate': '9.616e-05', 'epoch': '0.5021'}
[text-trainer] {'loss': '0.2874', 'grad_norm': '0.1888', 'learning_rate': '9.566e-05', 'epoch': '0.5048'}
[text-trainer] {'loss': '0.3127', 'grad_norm': '0.2091', 'learning_rate': '9.517e-05', 'epoch': '0.5075'}
[text-trainer] {'loss': '0.2974', 'grad_norm': '0.189', 'learning_rate': '9.467e-05', 'epoch': '0.5103'}
[text-trainer] {'loss': '0.284', 'grad_norm': '0.1755', 'learning_rate': '9.417e-05', 'epoch': '0.513'}
[text-trainer] {'loss': '0.2747', 'grad_norm': '0.1693', 'learning_rate': '9.368e-05', 'epoch': '0.5157'}
[text-trainer] {'loss': '0.2985', 'grad_norm': '0.2679', 'learning_rate': '9.318e-05', 'epoch': '0.5185'}
[text-trainer] {'loss': '0.2924', 'grad_norm': '0.1872', 'learning_rate': '9.268e-05', 'epoch': '0.5212'}
[text-trainer] {'loss': '0.2925', 'grad_norm': '0.3106', 'learning_rate': '9.218e-05', 'epoch': '0.5239'}
[text-trainer] {'loss': '0.2842', 'grad_norm': '0.1955', 'learning_rate': '9.169e-05', 'epoch': '0.5266'}
[text-trainer] {'loss': '0.294', 'grad_norm': '0.1917', 'learning_rate': '9.119e-05', 'epoch': '0.5294'}
[text-trainer] {'loss': '0.2935', 'grad_norm': '0.2007', 'learning_rate': '9.069e-05', 'epoch': '0.5321'}
[text-trainer] {'loss': '0.2767', 'grad_norm': '0.1985', 'learning_rate': '9.02e-05', 'epoch': '0.5348'}
[text-trainer] {'loss': '0.2964', 'grad_norm': '0.1663', 'learning_rate': '8.97e-05', 'epoch': '0.5376'}
[text-trainer] {'loss': '0.2731', 'grad_norm': '0.187', 'learning_rate': '8.921e-05', 'epoch': '0.5403'}
[text-trainer] {'loss': '0.2711', 'grad_norm': '0.2217', 'learning_rate': '8.871e-05', 'epoch': '0.543'}
[text-trainer] {'loss': '0.3095', 'grad_norm': '0.1862', 'learning_rate': '8.822e-05', 'epoch': '0.5457'}
[text-trainer] {'loss': '0.2793', 'grad_norm': '0.1974', 'learning_rate': '8.772e-05', 'epoch': '0.5485'}
[text-trainer] {'loss': '0.2725', 'grad_norm': '0.1972', 'learning_rate': '8.723e-05', 'epoch': '0.5512'}
[text-trainer] {'loss': '0.2877', 'grad_norm': '0.1871', 'learning_rate': '8.673e-05', 'epoch': '0.5539'}
[text-trainer] {'loss': '0.3248', 'grad_norm': '0.2933', 'learning_rate': '8.624e-05', 'epoch': '0.5567'}
[text-trainer] {'loss': '0.2871', 'grad_norm': '0.257', 'learning_rate': '8.575e-05', 'epoch': '0.5594'}
[text-trainer] {'loss': '0.2625', 'grad_norm': '0.1725', 'learning_rate': '8.526e-05', 'epoch': '0.5621'}
[text-trainer] {'loss': '0.2715', 'grad_norm': '0.1648', 'learning_rate': '8.477e-05', 'epoch': '0.5648'}
[text-trainer] {'loss': '0.3228', 'grad_norm': '0.2012', 'learning_rate': '8.428e-05', 'epoch': '0.5676'}
[text-trainer] {'loss': '0.3094', 'grad_norm': '0.1921', 'learning_rate': '8.379e-05', 'epoch': '0.5703'}
[text-trainer] {'loss': '0.2785', 'grad_norm': '0.1885', 'learning_rate': '8.33e-05', 'epoch': '0.573'}
[text-trainer] {'loss': '0.2854', 'grad_norm': '0.2324', 'learning_rate': '8.281e-05', 'epoch': '0.5758'}
[text-trainer] {'loss': '0.2717', 'grad_norm': '0.1565', 'learning_rate': '8.232e-05', 'epoch': '0.5785'}
[text-trainer] {'loss': '0.2756', 'grad_norm': '0.1585', 'learning_rate': '8.184e-05', 'epoch': '0.5812'}
[text-trainer] {'loss': '0.3057', 'grad_norm': '0.2042', 'learning_rate': '8.135e-05', 'epoch': '0.5839'}
[text-trainer] {'loss': '0.2977', 'grad_norm': '0.2722', 'learning_rate': '8.087e-05', 'epoch': '0.5867'}
[text-trainer] {'loss': '0.2739', 'grad_norm': '0.1894', 'learning_rate': '8.038e-05', 'epoch': '0.5894'}
[text-trainer] {'loss': '0.2704', 'grad_norm': '0.1869', 'learning_rate': '7.99e-05', 'epoch': '0.5921'}
[text-trainer] {'loss': '0.2862', 'grad_norm': '0.2084', 'learning_rate': '7.942e-05', 'epoch': '0.5949'}
[text-trainer] {'loss': '0.2841', 'grad_norm': '0.1662', 'learning_rate': '7.894e-05', 'epoch': '0.5976'}
[text-trainer] {'loss': '0.2967', 'grad_norm': '0.1914', 'learning_rate': '7.846e-05', 'epoch': '0.6003'}
[text-trainer] {'loss': '0.2687', 'grad_norm': '0.1716', 'learning_rate': '7.798e-05', 'epoch': '0.603'}
[text-trainer] {'loss': '0.2994', 'grad_norm': '0.1797', 'learning_rate': '7.751e-05', 'epoch': '0.6058'}
[text-trainer] {'loss': '0.2988', 'grad_norm': '0.1621', 'learning_rate': '7.703e-05', 'epoch': '0.6085'}
[text-trainer] {'loss': '0.2665', 'grad_norm': '0.2403', 'learning_rate': '7.656e-05', 'epoch': '0.6112'}
[text-trainer] {'loss': '0.293', 'grad_norm': '0.2517', 'learning_rate': '7.608e-05', 'epoch': '0.614'}
[text-trainer] {'loss': '0.2804', 'grad_norm': '0.1758', 'learning_rate': '7.561e-05', 'epoch': '0.6167'}
[text-trainer] {'loss': '0.2888', 'grad_norm': '0.1829', 'learning_rate': '7.514e-05', 'epoch': '0.6194'}
[text-trainer] {'loss': '0.2706', 'grad_norm': '0.1744', 'learning_rate': '7.467e-05', 'epoch': '0.6221'}
[text-trainer] {'loss': '0.2964', 'grad_norm': '0.2099', 'learning_rate': '7.421e-05', 'epoch': '0.6249'}
[text-trainer] {'loss': '0.2876', 'grad_norm': '0.1826', 'learning_rate': '7.374e-05', 'epoch': '0.6276'}
[text-trainer] {'loss': '0.2945', 'grad_norm': '0.1548', 'learning_rate': '7.328e-05', 'epoch': '0.6303'}
[text-trainer] {'loss': '0.2817', 'grad_norm': '0.2084', 'learning_rate': '7.282e-05', 'epoch': '0.6331'}
[text-trainer] {'loss': '0.2875', 'grad_norm': '0.1824', 'learning_rate': '7.236e-05', 'epoch': '0.6358'}
[text-trainer] {'loss': '0.2803', 'grad_norm': '0.1778', 'learning_rate': '7.19e-05', 'epoch': '0.6385'}
[text-trainer] {'loss': '0.2562', 'grad_norm': '0.2686', 'learning_rate': '7.144e-05', 'epoch': '0.6412'}
[text-trainer] {'loss': '0.2829', 'grad_norm': '0.1961', 'learning_rate': '7.098e-05', 'epoch': '0.644'}
[text-trainer] {'loss': '0.304', 'grad_norm': '0.2069', 'learning_rate': '7.053e-05', 'epoch': '0.6467'}
[text-trainer] {'loss': '0.2892', 'grad_norm': '0.1635', 'learning_rate': '7.008e-05', 'epoch': '0.6494'}
[text-trainer] {'loss': '0.2907', 'grad_norm': '0.245', 'learning_rate': '6.963e-05', 'epoch': '0.6522'}
[text-trainer] {'loss': '0.2879', 'grad_norm': '0.1628', 'learning_rate': '6.918e-05', 'epoch': '0.6549'}
[text-trainer] {'loss': '0.3005', 'grad_norm': '0.1683', 'learning_rate': '6.873e-05', 'epoch': '0.6576'}
[text-trainer] {'loss': '0.2734', 'grad_norm': '0.1918', 'learning_rate': '6.829e-05', 'epoch': '0.6603'}
[text-trainer] {'loss': '0.282', 'grad_norm': '0.1692', 'learning_rate': '6.785e-05', 'epoch': '0.6631'}
[text-trainer] {'loss': '0.2861', 'grad_norm': '0.162', 'learning_rate': '6.741e-05', 'epoch': '0.6658'}
[text-trainer] {'loss': '0.2718', 'grad_norm': '0.2145', 'learning_rate': '6.697e-05', 'epoch': '0.6685'}
[text-trainer] {'loss': '0.2861', 'grad_norm': '0.1968', 'learning_rate': '6.653e-05', 'epoch': '0.6713'}
[text-trainer] {'loss': '0.2801', 'grad_norm': '0.2265', 'learning_rate': '6.61e-05', 'epoch': '0.674'}
[text-trainer] {'loss': '0.2974', 'grad_norm': '0.1978', 'learning_rate': '6.567e-05', 'epoch': '0.6767'}
[text-trainer] {'loss': '0.2785', 'grad_norm': '0.1668', 'learning_rate': '6.524e-05', 'epoch': '0.6794'}
[text-trainer] {'loss': '0.2889', 'grad_norm': '0.2363', 'learning_rate': '6.481e-05', 'epoch': '0.6822'}
[text-trainer] {'loss': '0.2852', 'grad_norm': '0.2467', 'learning_rate': '6.439e-05', 'epoch': '0.6849'}
[text-trainer] {'loss': '0.2829', 'grad_norm': '0.2001', 'learning_rate': '6.396e-05', 'epoch': '0.6876'}
[text-trainer] {'loss': '0.2706', 'grad_norm': '0.2535', 'learning_rate': '6.354e-05', 'epoch': '0.6904'}
[text-trainer] {'loss': '0.2782', 'grad_norm': '0.2129', 'learning_rate': '6.312e-05', 'epoch': '0.6931'}
[text-trainer] {'loss': '0.3081', 'grad_norm': '0.2178', 'learning_rate': '6.271e-05', 'epoch': '0.6958'}
[text-trainer] {'loss': '0.2964', 'grad_norm': '0.1783', 'learning_rate': '6.23e-05', 'epoch': '0.6985'}
[text-trainer] {'loss': '0.2417', 'grad_norm': '0.1902', 'learning_rate': '6.188e-05', 'epoch': '0.7013'}
[text-trainer] {'loss': '0.2844', 'grad_norm': '0.2461', 'learning_rate': '6.148e-05', 'epoch': '0.704'}
[text-trainer] {'loss': '0.2932', 'grad_norm': '0.1645', 'learning_rate': '6.107e-05', 'epoch': '0.7067'}
[text-trainer] {'loss': '0.2598', 'grad_norm': '0.1587', 'learning_rate': '6.067e-05', 'epoch': '0.7095'}
[text-trainer] {'loss': '0.3067', 'grad_norm': '0.1995', 'learning_rate': '6.027e-05', 'epoch': '0.7122'}
[text-trainer] {'loss': '0.2823', 'grad_norm': '0.193', 'learning_rate': '5.987e-05', 'epoch': '0.7149'}
[text-trainer] {'loss': '0.3046', 'grad_norm': '0.1678', 'learning_rate': '5.947e-05', 'epoch': '0.7176'}
[text-trainer] {'loss': '0.2944', 'grad_norm': '0.1938', 'learning_rate': '5.908e-05', 'epoch': '0.7204'}
[text-trainer] {'loss': '0.2759', 'grad_norm': '0.1831', 'learning_rate': '5.869e-05', 'epoch': '0.7231'}
[text-trainer] {'loss': '0.2779', 'grad_norm': '0.1659', 'learning_rate': '5.83e-05', 'epoch': '0.7258'}
[text-trainer] {'loss': '0.2827', 'grad_norm': '0.2177', 'learning_rate': '5.792e-05', 'epoch': '0.7286'}
[text-trainer] {'loss': '0.279', 'grad_norm': '0.1649', 'learning_rate': '5.754e-05', 'epoch': '0.7313'}
[text-trainer] {'loss': '0.2813', 'grad_norm': '0.1601', 'learning_rate': '5.716e-05', 'epoch': '0.734'}
[text-trainer] {'loss': '0.2964', 'grad_norm': '0.196', 'learning_rate': '5.678e-05', 'epoch': '0.7367'}
[text-trainer] {'loss': '0.2716', 'grad_norm': '0.1825', 'learning_rate': '5.641e-05', 'epoch': '0.7395'}
[text-trainer] {'loss': '0.2873', 'grad_norm': '0.1693', 'learning_rate': '5.604e-05', 'epoch': '0.7422'}
[text-trainer] {'loss': '0.2787', 'grad_norm': '0.1925', 'learning_rate': '5.567e-05', 'epoch': '0.7449'}
[text-trainer] {'loss': '0.268', 'grad_norm': '0.1569', 'learning_rate': '5.531e-05', 'epoch': '0.7477'}
[text-trainer] {'eval_loss': '0.2786', 'eval_runtime': '6.195', 'eval_samples_per_second': '41.32', 'eval_steps_per_second': '10.33', 'epoch': '0.7498'}
[text-trainer] {'loss': '0.314', 'grad_norm': '0.2439', 'learning_rate': '5.494e-05', 'epoch': '0.7504'}
[text-trainer] {'loss': '0.2899', 'grad_norm': '0.2079', 'learning_rate': '5.459e-05', 'epoch': '0.7531'}
[text-trainer] {'loss': '0.2944', 'grad_norm': '0.1945', 'learning_rate': '5.423e-05', 'epoch': '0.7558'}
[text-trainer] {'loss': '0.2972', 'grad_norm': '0.203', 'learning_rate': '5.388e-05', 'epoch': '0.7586'}
[text-trainer] {'loss': '0.3107', 'grad_norm': '0.268', 'learning_rate': '5.353e-05', 'epoch': '0.7613'}
[text-trainer] {'loss': '0.2707', 'grad_norm': '0.1831', 'learning_rate': '5.318e-05', 'epoch': '0.764'}
[text-trainer] {'loss': '0.2892', 'grad_norm': '0.2132', 'learning_rate': '5.284e-05', 'epoch': '0.7668'}
[text-trainer] {'loss': '0.2855', 'grad_norm': '0.1474', 'learning_rate': '5.25e-05', 'epoch': '0.7695'}
[text-trainer] {'loss': '0.2815', 'grad_norm': '0.1939', 'learning_rate': '5.216e-05', 'epoch': '0.7722'}
[text-trainer] {'loss': '0.2779', 'grad_norm': '0.1725', 'learning_rate': '5.183e-05', 'epoch': '0.775'}
[text-trainer] {'loss': '0.306', 'grad_norm': '0.188', 'learning_rate': '5.15e-05', 'epoch': '0.7777'}
[text-trainer] {'loss': '0.28', 'grad_norm': '0.1897', 'learning_rate': '5.118e-05', 'epoch': '0.7804'}
[text-trainer] {'loss': '0.2635', 'grad_norm': '0.2003', 'learning_rate': '5.085e-05', 'epoch': '0.7831'}
[text-trainer] {'loss': '0.2854', 'grad_norm': '0.1942', 'learning_rate': '5.053e-05', 'epoch': '0.7859'}
[text-trainer] {'loss': '0.254', 'grad_norm': '0.1622', 'learning_rate': '5.022e-05', 'epoch': '0.7886'}
[text-trainer] {'loss': '0.2703', 'grad_norm': '0.156', 'learning_rate': '4.99e-05', 'epoch': '0.7913'}
[text-trainer] {'loss': '0.287', 'grad_norm': '0.1947', 'learning_rate': '4.959e-05', 'epoch': '0.7941'}
[text-trainer] {'loss': '0.3214', 'grad_norm': '0.2813', 'learning_rate': '4.929e-05', 'epoch': '0.7968'}
[text-trainer] {'loss': '0.2704', 'grad_norm': '0.179', 'learning_rate': '4.898e-05', 'epoch': '0.7995'}
[text-trainer] {'loss': '0.2875', 'grad_norm': '0.1597', 'learning_rate': '4.869e-05', 'epoch': '0.8022'}
[text-trainer] {'loss': '0.255', 'grad_norm': '0.2109', 'learning_rate': '4.839e-05', 'epoch': '0.805'}
[text-trainer] {'loss': '0.2828', 'grad_norm': '0.148', 'learning_rate': '4.81e-05', 'epoch': '0.8077'}
[text-trainer] {'loss': '0.2751', 'grad_norm': '0.1914', 'learning_rate': '4.781e-05', 'epoch': '0.8104'}
[text-trainer] {'loss': '0.298', 'grad_norm': '0.173', 'learning_rate': '4.752e-05', 'epoch': '0.8132'}
[text-trainer] {'loss': '0.2951', 'grad_norm': '0.1678', 'learning_rate': '4.724e-05', 'epoch': '0.8159'}
[text-trainer] {'loss': '0.2807', 'grad_norm': '0.2737', 'learning_rate': '4.696e-05', 'epoch': '0.8186'}
[text-trainer] {'loss': '0.2808', 'grad_norm': '0.1817', 'learning_rate': '4.669e-05', 'epoch': '0.8213'}
[text-trainer] {'loss': '0.2877', 'grad_norm': '0.1904', 'learning_rate': '4.642e-05', 'epoch': '0.8241'}
[text-trainer] {'loss': '0.2887', 'grad_norm': '0.211', 'learning_rate': '4.615e-05', 'epoch': '0.8268'}
[text-trainer] {'loss': '0.2929', 'grad_norm': '0.2224', 'learning_rate': '4.589e-05', 'epoch': '0.8295'}
[text-trainer] {'loss': '0.2703', 'grad_norm': '0.2081', 'learning_rate': '4.563e-05', 'epoch': '0.8323'}
[text-trainer] {'loss': '0.2702', 'grad_norm': '0.1798', 'learning_rate': '4.538e-05', 'epoch': '0.835'}
[text-trainer] {'loss': '0.2787', 'grad_norm': '0.1945', 'learning_rate': '4.512e-05', 'epoch': '0.8377'}
[text-trainer] {'loss': '0.3007', 'grad_norm': '0.2051', 'learning_rate': '4.488e-05', 'epoch': '0.8404'}
[text-trainer] {'loss': '0.2745', 'grad_norm': '0.276', 'learning_rate': '4.463e-05', 'epoch': '0.8432'}
[text-trainer] {'loss': '0.2882', 'grad_norm': '0.179', 'learning_rate': '4.439e-05', 'epoch': '0.8459'}
[text-trainer] {'loss': '0.2834', 'grad_norm': '0.162', 'learning_rate': '4.415e-05', 'epoch': '0.8486'}
[text-trainer] {'loss': '0.2904', 'grad_norm': '0.1902', 'learning_rate': '4.392e-05', 'epoch': '0.8514'}
[text-trainer] {'loss': '0.2735', 'grad_norm': '0.1724', 'learning_rate': '4.369e-05', 'epoch': '0.8541'}
[text-trainer] {'loss': '0.2536', 'grad_norm': '0.2165', 'learning_rate': '4.347e-05', 'epoch': '0.8568'}
[text-trainer] {'loss': '0.2863', 'grad_norm': '0.1613', 'learning_rate': '4.325e-05', 'epoch': '0.8595'}
[text-trainer] {'loss': '0.2962', 'grad_norm': '0.1844', 'learning_rate': '4.303e-05', 'epoch': '0.8623'}
[text-trainer] {'loss': '0.2858', 'grad_norm': '0.2029', 'learning_rate': '4.282e-05', 'epoch': '0.865'}
[text-trainer] {'loss': '0.2716', 'grad_norm': '0.1602', 'learning_rate': '4.261e-05', 'epoch': '0.8677'}
[text-trainer] {'loss': '0.3116', 'grad_norm': '0.2211', 'learning_rate': '4.24e-05', 'epoch': '0.8705'}
[text-trainer] {'loss': '0.3006', 'grad_norm': '0.2255', 'learning_rate': '4.22e-05', 'epoch': '0.8732'}
[text-trainer] {'loss': '0.2586', 'grad_norm': '0.1802', 'learning_rate': '4.201e-05', 'epoch': '0.8759'}
[text-trainer] {'loss': '0.2611', 'grad_norm': '0.1705', 'learning_rate': '4.181e-05', 'epoch': '0.8786'}
[text-trainer] {'loss': '0.2882', 'grad_norm': '0.185', 'learning_rate': '4.162e-05', 'epoch': '0.8814'}
[text-trainer] {'loss': '0.2905', 'grad_norm': '0.1902', 'learning_rate': '4.144e-05', 'epoch': '0.8841'}
[text-trainer] {'loss': '0.2811', 'grad_norm': '0.2015', 'learning_rate': '4.126e-05', 'epoch': '0.8868'}
[text-trainer] {'loss': '0.283', 'grad_norm': '0.1785', 'learning_rate': '4.108e-05', 'epoch': '0.8896'}
[text-trainer] {'loss': '0.277', 'grad_norm': '0.2102', 'learning_rate': '4.091e-05', 'epoch': '0.8923'}
[text-trainer] {'loss': '0.264', 'grad_norm': '0.158', 'learning_rate': '4.074e-05', 'epoch': '0.895'}
[text-trainer] {'loss': '0.2523', 'grad_norm': '0.2075', 'learning_rate': '4.058e-05', 'epoch': '0.8977'}
[text-trainer] {'loss': '0.2934', 'grad_norm': '0.1702', 'learning_rate': '4.042e-05', 'epoch': '0.9005'}
[text-trainer] {'loss': '0.2834', 'grad_norm': '0.1779', 'learning_rate': '4.026e-05', 'epoch': '0.9032'}
[text-trainer] {'loss': '0.2678', 'grad_norm': '0.1684', 'learning_rate': '4.011e-05', 'epoch': '0.9059'}
[text-trainer] {'loss': '0.28', 'grad_norm': '0.1629', 'learning_rate': '3.996e-05', 'epoch': '0.9087'}
[text-trainer] {'loss': '0.2654', 'grad_norm': '0.2201', 'learning_rate': '3.982e-05', 'epoch': '0.9114'}
[text-trainer] {'loss': '0.2622', 'grad_norm': '0.184', 'learning_rate': '3.968e-05', 'epoch': '0.9141'}
[text-trainer] {'loss': '0.3066', 'grad_norm': '0.2285', 'learning_rate': '3.954e-05', 'epoch': '0.9168'}
[text-trainer] {'loss': '0.3007', 'grad_norm': '0.2169', 'learning_rate': '3.941e-05', 'epoch': '0.9196'}
[text-trainer] {'loss': '0.2997', 'grad_norm': '0.2104', 'learning_rate': '3.929e-05', 'epoch': '0.9223'}
[text-trainer] {'loss': '0.3111', 'grad_norm': '0.1838', 'learning_rate': '3.916e-05', 'epoch': '0.925'}
[text-trainer] {'loss': '0.2754', 'grad_norm': '0.204', 'learning_rate': '3.905e-05', 'epoch': '0.9278'}
[text-trainer] {'loss': '0.2566', 'grad_norm': '0.165', 'learning_rate': '3.893e-05', 'epoch': '0.9305'}
[text-trainer] {'loss': '0.2814', 'grad_norm': '0.1446', 'learning_rate': '3.882e-05', 'epoch': '0.9332'}
[text-trainer] {'loss': '0.2494', 'grad_norm': '0.1861', 'learning_rate': '3.872e-05', 'epoch': '0.9359'}
[text-trainer] {'loss': '0.2669', 'grad_norm': '0.1873', 'learning_rate': '3.862e-05', 'epoch': '0.9387'}
[text-trainer] {'loss': '0.276', 'grad_norm': '0.2057', 'learning_rate': '3.852e-05', 'epoch': '0.9414'}
[text-trainer] {'loss': '0.2832', 'grad_norm': '0.1871', 'learning_rate': '3.843e-05', 'epoch': '0.9441'}
[text-trainer] {'loss': '0.2847', 'grad_norm': '0.2301', 'learning_rate': '3.834e-05', 'epoch': '0.9469'}
[text-trainer] {'loss': '0.2774', 'grad_norm': '0.2093', 'learning_rate': '3.826e-05', 'epoch': '0.9496'}
[text-trainer] {'loss': '0.2721', 'grad_norm': '0.1841', 'learning_rate': '3.818e-05', 'epoch': '0.9523'}
[text-trainer] {'loss': '0.2786', 'grad_norm': '0.1849', 'learning_rate': '3.81e-05', 'epoch': '0.955'}
[text-trainer] {'loss': '0.2693', 'grad_norm': '0.1948', 'learning_rate': '3.803e-05', 'epoch': '0.9578'}
[text-trainer] {'loss': '0.3201', 'grad_norm': '0.2125', 'learning_rate': '3.797e-05', 'epoch': '0.9605'}
[text-trainer] {'loss': '0.2574', 'grad_norm': '0.1829', 'learning_rate': '3.791e-05', 'epoch': '0.9632'}
[text-trainer] {'loss': '0.2625', 'grad_norm': '0.1962', 'learning_rate': '3.785e-05', 'epoch': '0.966'}
[text-trainer] {'loss': '0.2825', 'grad_norm': '0.2101', 'learning_rate': '3.78e-05', 'epoch': '0.9687'}
[text-trainer] {'loss': '0.2558', 'grad_norm': '0.1779', 'learning_rate': '3.775e-05', 'epoch': '0.9714'}
[text-trainer] {'loss': '0.2826', 'grad_norm': '0.1737', 'learning_rate': '3.77e-05', 'epoch': '0.9741'}
[text-trainer] {'loss': '0.2766', 'grad_norm': '0.2064', 'learning_rate': '3.766e-05', 'epoch': '0.9769'}
[text-trainer] {'loss': '0.277', 'grad_norm': '0.1868', 'learning_rate': '3.763e-05', 'epoch': '0.9796'}
[text-trainer] {'loss': '0.2719', 'grad_norm': '0.1895', 'learning_rate': '3.76e-05', 'epoch': '0.9823'}
[text-trainer] {'loss': '0.2991', 'grad_norm': '0.1939', 'learning_rate': '3.757e-05', 'epoch': '0.9851'}
[text-trainer] {'loss': '0.28', 'grad_norm': '0.1791', 'learning_rate': '3.755e-05', 'epoch': '0.9878'}
[text-trainer] {'loss': '0.2691', 'grad_norm': '0.1836', 'learning_rate': '3.753e-05', 'epoch': '0.9905'}
[text-trainer] {'loss': '0.2653', 'grad_norm': '0.1722', 'learning_rate': '3.751e-05', 'epoch': '0.9932'}
[text-trainer] {'loss': '0.2747', 'grad_norm': '0.1669', 'learning_rate': '3.751e-05', 'epoch': '0.996'}
[text-trainer] {'loss': '0.2836', 'grad_norm': '0.1723', 'learning_rate': '3.75e-05', 'epoch': '0.9987'}
[text-trainer] {'eval_loss': '0.2751', 'eval_runtime': '6.205', 'eval_samples_per_second': '41.26', 'eval_steps_per_second': '10.31', 'epoch': '0.9998'}
[text-trainer] {'eval_loss': '0.2751', 'eval_runtime': '6.165', 'eval_samples_per_second': '41.53', 'eval_steps_per_second': '10.38', 'epoch': '1'}
[text-trainer] {'train_runtime': '5434', 'train_samples_per_second': '10.79', 'train_steps_per_second': '0.675', 'train_loss': '0.2926', 'epoch': '1'}