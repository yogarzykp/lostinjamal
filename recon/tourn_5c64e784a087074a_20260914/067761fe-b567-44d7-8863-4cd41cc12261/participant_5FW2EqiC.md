# Loki — task 067761fe-b567-44d7-8863-4cd41cc12261 — hotkey 5FW2EqiCeLknueng7Bp9rj4JrPNv5F6nxNg7yUtART6U1odT
fetched 2026-09-19T05:01:56+00:00  lines=1783  hit_page_cap=False  containers=['downloader-067761fe-b567-44d7-8863-4cd41cc12261-34fb4998', 'fastapi', 'hf-upload-56c47b8afac14f2aaa0d962f77b07369', 'text-trainer-263fb1e01b4d49c98b25bfd6b0871a37']

[downloader-0] Downloading datasets to: /cache/datasets
[downloader-0] Downloading models to: /cache/models
[downloader-0] Model already cached at /cache/models/c53e93d87a4fe77f.
[downloader-0] Skipping download.
[downloader-0] Model path: /cache/models/c53e93d87a4fe77f
[downloader-0] Dataset path: /cache/datasets
[fastapi] Repository cloned successfully
[fastapi] Running Cache Download Container
[fastapi] Starting downloader container: downloader-067761fe-b567-44d7-8863-4cd41cc12261-34fb4998
[fastapi] Download completed successfully for task 067761fe-b567-44d7-8863-4cd41cc12261
[fastapi] Building Docker image 'standalone-text-trainer:f03e89e6-82d3-4b16-ac07-049aaf278606' (timeout=1800s)...
[fastapi] Step 1/20 : FROM runpod/pytorch:1.1.0-cu1281-torch291-ubuntu2204
[fastapi] ---> 3b600cc49e85
[fastapi] Step 2/20 : ARG FLASH_ATTN_WHEEL=https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu12torch2.9cxx11abiTRUE-cp312-cp312-linux_x86_64.whl
[fastapi] ---> Running in c1ab7c79bcf5
[fastapi] ---> e764a5d69c7d
[fastapi] Step 3/20 : ARG BUILD_MAX_JOBS=4
[fastapi] ---> Running in fae171a09cf4
[fastapi] ---> b7141ad0e15a
[fastapi] Step 4/20 : RUN apt-get update && apt-get install -y     vim     zip     tmux     iotop     nvtop     bmon     wget     nano     zsh     htop     && rm -rf /var/lib/apt/lists/*
[fastapi] ---> Running in d85bd22bb5cf
[fastapi] Get:1 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  InRelease [1578 B]
[fastapi] Get:2 http://security.ubuntu.com/ubuntu jammy-security InRelease [129 kB]
[fastapi] Get:3 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  Packages [3009 kB]
[fastapi] Get:4 http://archive.ubuntu.com/ubuntu jammy InRelease [270 kB]
[fastapi] Get:5 http://security.ubuntu.com/ubuntu jammy-security/restricted amd64 Packages [7717 kB]
[fastapi] Get:6 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy InRelease [18.1 kB]
[fastapi] Get:7 http://security.ubuntu.com/ubuntu jammy-security/multiverse amd64 Packages [84.6 kB]
[fastapi] Get:8 http://security.ubuntu.com/ubuntu jammy-security/universe amd64 Packages [1317 kB]
[fastapi] Get:9 http://security.ubuntu.com/ubuntu jammy-security/main amd64 Packages [4290 kB]
[fastapi] Get:10 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy/main amd64 Packages [44.3 kB]
[fastapi] Get:11 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [128 kB]
[fastapi] Get:12 http://archive.ubuntu.com/ubuntu jammy-backports InRelease [127 kB]
[fastapi] Get:13 http://archive.ubuntu.com/ubuntu jammy/restricted amd64 Packages [164 kB]
[fastapi] Get:14 http://archive.ubuntu.com/ubuntu jammy/main amd64 Packages [1792 kB]
[fastapi] Get:15 http://archive.ubuntu.com/ubuntu jammy/universe amd64 Packages [17.5 MB]
[fastapi] Get:16 http://archive.ubuntu.com/ubuntu jammy/multiverse amd64 Packages [266 kB]
[fastapi] Get:17 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 Packages [1620 kB]
[fastapi] Get:18 http://archive.ubuntu.com/ubuntu jammy-updates/multiverse amd64 Packages [93.2 kB]
[fastapi] Get:19 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 Packages [4624 kB]
[fastapi] Get:20 http://archive.ubuntu.com/ubuntu jammy-updates/restricted amd64 Packages [8007 kB]
[fastapi] Get:21 http://archive.ubuntu.com/ubuntu jammy-backports/main amd64 Packages [82.8 kB]
[fastapi] Get:22 http://archive.ubuntu.com/ubuntu jammy-backports/universe amd64 Packages [35.6 kB]
[fastapi] Fetched 51.3 MB in 4s (13.2 MB/s)
[fastapi] Reading package lists...
[fastapi] Reading package lists...
[fastapi] Building dependency tree...
[fastapi] Reading state information...
[fastapi] zip is already the newest version (3.0-12build2).
[fastapi] nano is already the newest version (6.2-1ubuntu0.2).
[fastapi] tmux is already the newest version (3.2a-4ubuntu0.2).
[fastapi] The following additional packages will be installed:
[fastapi] libconfuse-common libconfuse2 libnl-3-200 libnl-genl-3-200 libnl-route-3-200
[fastapi] vim-common vim-runtime zsh-common
[fastapi] Suggested packages:
[fastapi] lm-sensors strace ctags vim-doc vim-scripts zsh-doc
[fastapi] The following NEW packages will be installed:
[fastapi] bmon htop iotop libconfuse-common libconfuse2 libnl-3-200 libnl-genl-3-200
[fastapi] libnl-route-3-200 nvtop zsh zsh-common
[fastapi] The following packages will be upgraded:
[fastapi] vim vim-common vim-runtime wget
[fastapi] 4 upgraded, 11 newly installed, 0 to remove and 82 not upgraded.
[fastapi] Need to get 14.3 MB of archives.
[fastapi] After this operation, 19.8 MB of additional disk space will be used.
[fastapi] Get:1 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 vim amd64 2:8.2.3995-1ubuntu2.36 [1733 kB]
[fastapi] Get:2 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 vim-runtime all 2:8.2.3995-1ubuntu2.36 [6824 kB]
[fastapi] Get:3 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 vim-common all 2:8.2.3995-1ubuntu2.36 [81.5 kB]
[fastapi] Get:4 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 wget amd64 1.21.2-2ubuntu1.5 [339 kB]
[fastapi] Get:5 http://archive.ubuntu.com/ubuntu jammy/universe amd64 libconfuse-common all 3.3-2 [6004 B]
[fastapi] Get:6 http://archive.ubuntu.com/ubuntu jammy/universe amd64 libconfuse2 amd64 3.3-2 [26.0 kB]
[fastapi] Get:7 http://archive.ubuntu.com/ubuntu jammy/main amd64 libnl-3-200 amd64 3.5.0-0.1 [59.1 kB]
[fastapi] Get:8 http://archive.ubuntu.com/ubuntu jammy/main amd64 libnl-route-3-200 amd64 3.5.0-0.1 [180 kB]
[fastapi] Get:9 http://archive.ubuntu.com/ubuntu jammy/universe amd64 bmon amd64 1:4.0-8 [48.1 kB]
[fastapi] Get:10 http://archive.ubuntu.com/ubuntu jammy/main amd64 libnl-genl-3-200 amd64 3.5.0-0.1 [12.4 kB]
[fastapi] Get:11 http://archive.ubuntu.com/ubuntu jammy/main amd64 htop amd64 3.0.5-7build2 [128 kB]
[fastapi] Get:12 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 iotop amd64 0.6-24-g733f3f8-1.1ubuntu0.1 [23.1 kB]
[fastapi] Get:13 http://archive.ubuntu.com/ubuntu jammy/multiverse amd64 nvtop amd64 1.2.2-1 [43.9 kB]
[fastapi] Get:14 http://archive.ubuntu.com/ubuntu jammy/main amd64 zsh-common all 5.8.1-1 [3985 kB]
[fastapi] Get:15 http://archive.ubuntu.com/ubuntu jammy/main amd64 zsh amd64 5.8.1-1 [809 kB]
[fastapi] [91mdebconf: delaying package configuration, since apt-utils is not installed
[fastapi] [0mFetched 14.3 MB in 2s (6150 kB/s)
[fastapi] (Reading database ... (Reading database ... 5%(Reading database ... 10%(Reading database ... 15%(Reading database ... 20%(Reading database ... 25%(Reading database ... 30%(Reading database ... 35%(Reading database ... 40%(Reading database ... 45%(Reading database ... 50%(Reading database ... 55%(Reading database ... 60%(Reading database ... 65%(Reading database ... 70%(Reading database ... 75%(Reading database ... 80%(Reading database ... 85%(Reading database ... 90%(Reading database ... 95%(Reading database ... 100%(Reading database ... 50269 files and directories currently installed.)
[fastapi] Preparing to unpack .../00-vim_2%3a8.2.3995-1ubuntu2.36_amd64.deb ...
[fastapi] Unpacking vim (2:8.2.3995-1ubuntu2.36) over (2:8.2.3995-1ubuntu2.34) ...
[fastapi] Preparing to unpack .../01-vim-runtime_2%3a8.2.3995-1ubuntu2.36_all.deb ...
[fastapi] Unpacking vim-runtime (2:8.2.3995-1ubuntu2.36) over (2:8.2.3995-1ubuntu2.34) ...
[fastapi] Preparing to unpack .../02-vim-common_2%3a8.2.3995-1ubuntu2.36_all.deb ...
[fastapi] Unpacking vim-common (2:8.2.3995-1ubuntu2.36) over (2:8.2.3995-1ubuntu2.34) ...
[fastapi] Preparing to unpack .../03-wget_1.21.2-2ubuntu1.5_amd64.deb ...
[fastapi] Unpacking wget (1.21.2-2ubuntu1.5) over (1.21.2-2ubuntu1.4) ...
[fastapi] Selecting previously unselected package libconfuse-common.
[fastapi] Preparing to unpack .../04-libconfuse-common_3.3-2_all.deb ...
[fastapi] Unpacking libconfuse-common (3.3-2) ...
[fastapi] Selecting previously unselected package libconfuse2:amd64.
[fastapi] Preparing to unpack .../05-libconfuse2_3.3-2_amd64.deb ...
[fastapi] Unpacking libconfuse2:amd64 (3.3-2) ...
[fastapi] Selecting previously unselected package libnl-3-200:amd64.
[fastapi] Preparing to unpack .../06-libnl-3-200_3.5.0-0.1_amd64.deb ...
[fastapi] Unpacking libnl-3-200:amd64 (3.5.0-0.1) ...
[fastapi] Selecting previously unselected package libnl-route-3-200:amd64.
[fastapi] Preparing to unpack .../07-libnl-route-3-200_3.5.0-0.1_amd64.deb ...
[fastapi] Unpacking libnl-route-3-200:amd64 (3.5.0-0.1) ...
[fastapi] Selecting previously unselected package bmon.
[fastapi] Preparing to unpack .../08-bmon_1%3a4.0-8_amd64.deb ...
[fastapi] Unpacking bmon (1:4.0-8) ...
[fastapi] Selecting previously unselected package libnl-genl-3-200:amd64.
[fastapi] Preparing to unpack .../09-libnl-genl-3-200_3.5.0-0.1_amd64.deb ...
[fastapi] Unpacking libnl-genl-3-200:amd64 (3.5.0-0.1) ...
[fastapi] Selecting previously unselected package htop.
[fastapi] Preparing to unpack .../10-htop_3.0.5-7build2_amd64.deb ...
[fastapi] Unpacking htop (3.0.5-7build2) ...
[fastapi] Selecting previously unselected package iotop.
[fastapi] Preparing to unpack .../11-iotop_0.6-24-g733f3f8-1.1ubuntu0.1_amd64.deb ...
[fastapi] Unpacking iotop (0.6-24-g733f3f8-1.1ubuntu0.1) ...
[fastapi] Selecting previously unselected package nvtop.
[fastapi] Preparing to unpack .../12-nvtop_1.2.2-1_amd64.deb ...
[fastapi] Unpacking nvtop (1.2.2-1) ...
[fastapi] Selecting previously unselected package zsh-common.
[fastapi] Preparing to unpack .../13-zsh-common_5.8.1-1_all.deb ...
[fastapi] Unpacking zsh-common (5.8.1-1) ...
[fastapi] Selecting previously unselected package zsh.
[fastapi] Preparing to unpack .../14-zsh_5.8.1-1_amd64.deb ...
[fastapi] Unpacking zsh (5.8.1-1) ...
[fastapi] Setting up nvtop (1.2.2-1) ...
[fastapi] Setting up wget (1.21.2-2ubuntu1.5) ...
[fastapi] Setting up zsh-common (5.8.1-1) ...
[fastapi] Setting up iotop (0.6-24-g733f3f8-1.1ubuntu0.1) ...
[fastapi] update-alternatives: using /usr/sbin/iotop-py to provide /usr/sbin/iotop (iotop) in auto mode
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/man8/iotop.8.gz because associated file /usr/share/man/man8/iotop-py.8.gz (of link group iotop) doesn't exist
[fastapi] Setting up vim-common (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Setting up libconfuse-common (3.3-2) ...
[fastapi] Setting up libnl-3-200:amd64 (3.5.0-0.1) ...
[fastapi] Setting up zsh (5.8.1-1) ...
[fastapi] Setting up vim-runtime (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Setting up libconfuse2:amd64 (3.3-2) ...
[fastapi] Setting up vim (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Setting up libnl-route-3-200:amd64 (3.5.0-0.1) ...
[fastapi] Setting up bmon (1:4.0-8) ...
[fastapi] Setting up libnl-genl-3-200:amd64 (3.5.0-0.1) ...
[fastapi] Setting up htop (3.0.5-7build2) ...
[fastapi] Processing triggers for mailcap (3.70+nmu1ubuntu1.22.04.1) ...
[fastapi] Processing triggers for hicolor-icon-theme (0.17-2) ...
[fastapi] Processing triggers for libc-bin (2.35-0ubuntu3.14) ...
[fastapi] ---> 90d3102bda14
[fastapi] Step 5/20 : RUN mkdir -p /workspace
[fastapi] ---> Running in 1b5b77d96047
[fastapi] ---> 57fd07ed7ab1
[fastapi] Step 6/20 : RUN mkdir -p /cache
[fastapi] ---> Running in f44a9dc50417
[fastapi] ---> a2676c0f7a04
[fastapi] Step 7/20 : RUN mkdir -p /workspace/scripts/datasets
[fastapi] ---> Running in 5d00c4007ce8
[fastapi] ---> f935811d40cb
[fastapi] Step 8/20 : RUN mkdir -p /app/checkpoints
[fastapi] ---> Running in 501a8a21a127
[fastapi] ---> eb3c1590f96b
[fastapi] Step 9/20 : WORKDIR /workspace/scripts
[fastapi] ---> Running in cf2534f04536
[fastapi] ---> 473b7371abcd
[fastapi] Step 10/20 : COPY scripts/training_requirements.txt /workspace/scripts/training_requirements.txt
[fastapi] ---> 43a92903486a
[fastapi] Step 11/20 : RUN python -m venv /workspace/axo_py
[fastapi] ---> Running in f2abc6d19564
[fastapi] ---> af45b33e887f
[fastapi] Step 12/20 : RUN bash -c "source /workspace/axo_py/bin/activate &&     pip install uv &&     pip install -U packaging==23.2 setuptools==75.8.0 wheel ninja &&     uv pip install --no-build-isolation axolotl==0.9.1 &&     pip install requests==2.32.3 &&     deactivate"
[fastapi] ---> Running in 6f6bec9aedce
[fastapi] Collecting uv
[fastapi] Downloading uv-0.12.14-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] Downloading uv-0.12.14-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.0 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 20.0/20.0 MB 212.9 MB/s eta 0:00:00
[fastapi] Installing collected packages: uv
[fastapi] Successfully installed uv-0.12.14
[fastapi] [91m
[fastapi] [notice] A new release of pip is available: 25.0.1 -> 26.2.1
[fastapi] [notice] To update, run: pip install --upgrade pip
[fastapi] [0mCollecting packaging==23.2
[fastapi] Downloading packaging-23.2-py3-none-any.whl.metadata (3.2 kB)
[fastapi] Collecting setuptools==75.8.0
[fastapi] Downloading setuptools-75.8.0-py3-none-any.whl.metadata (6.7 kB)
[fastapi] Collecting wheel
[fastapi] Using cached wheel-0.48.0-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Collecting ninja
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (5.4 kB)
[fastapi] INFO: pip is looking at multiple versions of wheel to determine which version is compatible with other requirements. This could take a while.
[fastapi] Collecting wheel
[fastapi] Downloading wheel-0.47.0-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Downloading wheel-0.46.3-py3-none-any.whl.metadata (2.4 kB)
[fastapi] Downloading wheel-0.46.2-py3-none-any.whl.metadata (2.4 kB)
[fastapi] Downloading wheel-0.45.1-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Downloading packaging-23.2-py3-none-any.whl (53 kB)
[fastapi] Downloading setuptools-75.8.0-py3-none-any.whl (1.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 122.1 MB/s eta 0:00:00
[fastapi] Downloading wheel-0.45.1-py3-none-any.whl (72 kB)
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (183 kB)
[fastapi] Installing collected packages: wheel, setuptools, packaging, ninja
[fastapi] Successfully installed ninja-1.13.2 packaging-23.2 setuptools-75.8.0 wheel-0.45.1
[fastapi] [91m
[fastapi] [notice] A new release of pip is available: 25.0.1 -> 26.2.1
[fastapi] [notice] To update, run: pip install --upgrade pip
[fastapi] [0m[91mUsing Python 3.12.13 environment at: /workspace/axo_py
[fastapi] [0m[91mResolved 217 packages in 1.37s
[fastapi] [0m[91mDownloading pygments (1.2MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-cupti-cu12 (13.2MiB)
[fastapi] [0m[91mDownloading cryptography (4.5MiB)
[fastapi] [0m[91mDownloading botocore (13.7MiB)
[fastapi] [0m[91mDownloading numba (3.7MiB)
[fastapi] [0m[91mDownloading pydantic-core (1.9MiB)
[fastapi] [0m[91mDownloading nvidia-nvjitlink-cu12 (20.1MiB)
[fastapi] [0m[91mDownloading pyarrow (47.8MiB)
[fastapi] [0m[91mDownloading nvidia-nccl-cu12 (179.9MiB)
[fastapi] [0m[91mDownloading networkx (2.0MiB)
[fastapi] [0m[91mDownloading llvmlite (57.1MiB)
[fastapi] [0m[91mDownloading bitsandbytes (72.5MiB)
[fastapi] [0m[91mDownloading nvidia-cusparse-cu12 (197.8MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-nvrtc-cu12 (23.5MiB)
[fastapi] [0m[91mDownloading hf-xet (51.1MiB)
[fastapi] [0m[91mDownloading scipy (33.7MiB)
[fastapi] [0m[91mDownloading nvidia-cufft-cu12 (201.7MiB)
[fastapi] [0m[91mDownloading nvidia-cusolver-cu12 (122.0MiB)
[fastapi] [0m[91mDownloading oci (35.2MiB)
[fastapi] [0m[91mDownloading xformers (42.2MiB)
[fastapi] [0m[91mDownloading tensorboard (5.3MiB)
[fastapi] [0m[91mDownloading nvidia-cudnn-cu12 (634.0MiB)
[fastapi] [0m[91mDownloading transformers (9.9MiB)
[fastapi] [0m[91mDownloading tokenizers (3.0MiB)
[fastapi] [0m[91mDownloading hf-transfer (3.4MiB)
[fastapi] [0m[91mDownloading triton (241.4MiB)
[fastapi] [0m[91mDownloading numpy (18.4MiB)
[fastapi] [0m[91mDownloading pandas (11.8MiB)
[fastapi] [0m[91mDownloading pillow (6.3MiB)
[fastapi] [0m[91mDownloading nvidia-cusparselt-cu12 (143.1MiB)
[fastapi] [0m[91mDownloading tensorboard-data-server (6.3MiB)
[fastapi] [0m[91mDownloading aiohttp (1.7MiB)
[fastapi] [0m[91mDownloading wandb (24.9MiB)
[fastapi] [0m[91mDownloading gradio (44.3MiB)
[fastapi] [0m[91mDownloading torch (731.1MiB)
[fastapi] [0m[91mDownloading grpcio (6.8MiB)
[fastapi] [0m[91mDownloading torchao (5.4MiB)
[fastapi] [0m[91mDownloading lxml (5.0MiB)
[fastapi] [0m[91mDownloading ruff (9.9MiB)
[fastapi] [0m[91mDownloading nvidia-curand-cu12 (53.7MiB)
[fastapi] [0m[91mDownloading scikit-learn (11.7MiB)
[fastapi] [0m[91mDownloading nltk (1.7MiB)
[fastapi] [0m[91mDownloading zstandard (5.2MiB)
[fastapi] [0m[91mDownloading lm-eval (2.4MiB)
[fastapi] [0m[91mDownloading nvidia-cublas-cu12 (346.6MiB)
[fastapi] [0m[91mDownloading sympy (5.9MiB)
[fastapi] [0m[91mDownloading sentencepiece (1.3MiB)
[fastapi] [0m[91m Downloaded pygments
[fastapi] [0m[91m Downloaded sentencepiece
[fastapi] [0m[91m Downloaded nltk
[fastapi] [0m[91m Downloaded pydantic-core
[fastapi] [0m[91m Downloaded aiohttp
[fastapi] [0m[91m Downloaded networkx
[fastapi] [0m[91m Downloaded lm-eval
[fastapi] [0m[91m   Building langdetect==1.0.9
[fastapi] [0m[91m   Building axolotl==0.9.1
[fastapi] [0m[91m   Building axolotl-contribs-mit==0.0.3
[fastapi] [0m[91m Downloaded tokenizers
[fastapi] [0m[91m   Building word2number==1.1
[fastapi] [0m[91m   Building axolotl-contribs-lgpl==0.0.6
[fastapi] [0m[91m Downloaded hf-transfer
[fastapi] [0m[91m   Building rouge-score==0.1.2
[fastapi] [0m[91m   Building sqlitedict==2.1.0
[fastapi] [0m[91m Downloaded numba
[fastapi] [0m[91m   Building grpclib==0.4.7
[fastapi] [0m[91m   Building hqq==0.2.5
[fastapi] [0m[91m Downloaded cryptography
[fastapi] [0m[91m      Built word2number==1.1
[fastapi] [0m[91m      Built rouge-score==0.1.2
[fastapi] [0m[91m      Built axolotl-contribs-mit==0.0.3
[fastapi] Built axolotl-contribs-lgpl==0.0.6
[fastapi] [0m[91m Downloaded lxml
[fastapi] [0m[91m      Built sqlitedict==2.1.0
[fastapi] [0m[91m Downloaded zstandard
[fastapi] Downloaded tensorboard
[fastapi] [0m[91m Downloaded torchao
[fastapi] [0m[91m Downloaded sympy
[fastapi] [0m[91m Downloaded pillow
[fastapi] [0m[91m Downloaded tensorboard-data-server
[fastapi] [0m[91m      Built axolotl==0.9.1
[fastapi] [0m[91m      Built grpclib==0.4.7
[fastapi] [0m[91m Downloaded grpcio
[fastapi] [0m[91m      Built langdetect==1.0.9
[fastapi] [0m[91m Downloaded transformers
[fastapi] [0m[91m Downloaded ruff
[fastapi] [0m[91m Downloaded scikit-learn
[fastapi] [0m[91m Downloaded pandas
[fastapi] Built hqq==0.2.5
[fastapi] [0m[91m Downloaded nvidia-cuda-cupti-cu12
[fastapi] [0m[91m Downloaded botocore
[fastapi] [0m[91m Downloaded numpy
[fastapi] [0m[91m Downloaded nvidia-nvjitlink-cu12
[fastapi] [0m[91m Downloaded nvidia-cuda-nvrtc-cu12
[fastapi] [0m[91m Downloaded wandb
[fastapi] [0m[91m Downloaded scipy
[fastapi] [0m[91m Downloaded oci
[fastapi] [0m[91m Downloaded xformers
[fastapi] [0m[91m Downloaded gradio
[fastapi] [0m[91m Downloaded pyarrow
[fastapi] [0m[91m Downloaded hf-xet
[fastapi] [0m[91m Downloaded nvidia-curand-cu12
[fastapi] [0m[91m Downloaded llvmlite
[fastapi] [0m[91m Downloaded bitsandbytes
[fastapi] [0m[91m Downloaded nvidia-cusolver-cu12
[fastapi] [0m[91m Downloaded nvidia-cusparselt-cu12
[fastapi] [0m[91m Downloaded nvidia-nccl-cu12
[fastapi] [0m[91m Downloaded nvidia-cusparse-cu12
[fastapi] [0m[91m Downloaded nvidia-cufft-cu12
[fastapi] [0m[91m Downloaded triton
[fastapi] [0m[91m Downloaded nvidia-cublas-cu12
[fastapi] [0m[91m Downloaded nvidia-cudnn-cu12
[fastapi] [0m[91m Downloaded torch
[fastapi] [0m[91mPrepared 215 packages in 8.54s
[fastapi] [0m[91mInstalled 215 packages in 409ms
[fastapi] [0m[91m + absl-py==2.5.0
[fastapi] + accelerate==1.6.0
[fastapi] + addict==2.4.0
[fastapi] + adlfs==2026.8.0
[fastapi] + aiobotocore==2.26.0
[fastapi] + aiofiles==23.2.1
[fastapi] [0m[91m + aiohappyeyeballs==2.7.1
[fastapi] + aiohttp==3.14.3
[fastapi] + aioitertools[0m[91m==0.13.0[0m[91m
[fastapi] [0m[91m+ aiosignal==1.4.0
[fastapi] + annotated-doc==0.0.5
[fastapi] + annotated-types==[0m[91m0.8.0
[fastapi] + antlr4-python3-runtime==4.13.2
[fastapi] +[0m[91m anyio==4[0m[91m.15.1[0m[91m
[fastapi] [0m[91m+ art==6.[0m[91m5
[fastapi] + attrs[0m[91m==26.1[0m[91m.0[0m[91m
[fastapi] +[0m[91m autoawq[0m[91m==0.2.7[0m[91m.post3
[fastapi] + axolotl[0m[91m==0.9[0m[91m.1
[fastapi] +[0m[91m axolotl-contribs-lgpl[0m[91m==0.0.[0m[91m6
[fastapi] + axolotl-contribs-mit==0.0[0m[91m.3
[fastapi] [0m[91m+ [0m[91mazure-core==1.[0m[91m41.0[0m[91m
[fastapi] [0m[91m +[0m[91m azure-identity[0m[91m==1.25.3
[fastapi] + azure-storage-blob==12.30.[0m[91m1
[fastapi] + bitsandbytes[0m[91m==0[0m[91m.45[0m[91m.4
[fastapi] +[0m[91m [0m[91mbotocore==1.41.5
[fastapi] + certifi==2026.[0m[91m7.22
[fastapi] + cffi[0m[91m==2.1[0m[91m.1
[fastapi] [0m[91m+ [0m[91mchardet==[0m[91m6.0[0m[91m.0.post[0m[91m1
[fastapi] [0m[91m+[0m[91m charset-normalizer[0m[91m==3.5.[0m[91m1
[fastapi] + circuitbreaker==2.1.[0m[91m3
[fastapi] + click[0m[91m==8.5[0m[91m.0
[fastapi] + cloudpickle==3[0m[91m.1.2
[fastapi] + [0m[91mcolorama==0.4.6[0m[91m
[fastapi] + coloredlogs==15[0m[91m.0.1
[fastapi] + [0m[91mcrc32c==2.[0m[91m8
[fastapi] + [0m[91mcryptography==50.[0m[91m0.1
[fastapi] [0m[91m+ dataproperty[0m[91m==1.1.1
[fastapi] [0m[91m + datasets==3.5[0m[91m.1
[fastapi] +[0m[91m decorator==5.3.1
[fastapi] + defusedxml==0.[0m[91m7.1
[fastapi] + dill[0m[91m==0.3[0m[91m.8
[fastapi] [0m[91m + einops==0.8.2[0m[91m
[fastapi] + evaluate[0m[91m==0.4.1
[fastapi] + [0m[91mfastapi==0.141.1
[fastapi] + [0m[91mfastcore==2[0m[91m.2.[0m[91m27
[fastapi] [0m[91m+ [0m[91mffmpy==[0m[91m1.0.0
[fastapi] + filelock[0m[91m==3.32.6
[fastapi] + fire==0.7.1
[fastapi] [0m[91m+ frozenlist==1.8.0
[fastapi] + fsspec==2025.3.0
[fastapi] + gcsfs[0m[91m==2025.3.0
[fastapi] [0m[91m+ [0m[91mgoogle-api-core==2.[0m[91m33.0[0m[91m
[fastapi] [0m[91m+ google-auth[0m[91m==[0m[91m2.58.[0m[91m0
[fastapi] [0m[91m+ [0m[91mgoogle-auth-oauthlib==1.4.1
[fastapi] + [0m[91mgoogle-cloud-core==2.7[0m[91m.0
[fastapi] [0m[91m+ [0m[91mgoogle-cloud-storage==[0m[91m3.14[0m[91m.1
[fastapi] [0m[91m + google-crc32c==1.8.0
[fastapi] [0m[91m+ google-resumable-media==2.10.2
[fastapi] +[0m[91m googleapis-common-protos==[0m[91m1.75.0[0m[91m
[fastapi] + gradio==5.23.3
[fastapi] + gradio-client==1.8.[0m[91m0
[fastapi] + groovy==[0m[91m0.1.2[0m[91m
[fastapi] [0m[91m+ grpcio==1[0m[91m.84.0
[fastapi] + grpclib==0.4.7[0m[91m
[fastapi] [0m[91m+ h11==[0m[91m0.16.0
[fastapi] +[0m[91m h2==4.4[0m[91m.1[0m[91m
[fastapi] +[0m[91m hf-transfer[0m[91m==0.[0m[91m1.9[0m[91m
[fastapi] [0m[91m+ hf-xet==1.1.0
[fastapi] +[0m[91m hpack==4.2.0
[fastapi] +[0m[91m hqq==0.2.5
[fastapi] [0m[91m+ httpcore[0m[91m==1.[0m[91m0.9[0m[91m
[fastapi] + httpx==0.28.1
[fastapi] + [0m[91mhuggingface-hub==0.31.0
[fastapi] [0m[91m+ [0m[91mhumanfriendly==[0m[91m10.0
[fastapi] [0m[91m+ hyperframe==6.1[0m[91m.0[0m[91m
[fastapi] [0m[91m + [0m[91midna==3.19
[fastapi] + immutabledict[0m[91m==4.2.0[0m[91m
[fastapi] + isodate[0m[91m==0.7.2
[fastapi] + jinja2[0m[91m==3.1.[0m[91m6
[fastapi] + [0m[91mjmespath==1.1.[0m[91m0
[fastapi] + [0m[91mjoblib==1.[0m[91m6.0
[fastapi] [0m[91m+ jsonlines==[0m[91m4.[0m[91m0.0
[fastapi] [0m[91m [0m[91m+ langdetect[0m[91m==[0m[91m1.0[0m[91m.9[0m[91m
[fastapi] [0m[91m+ [0m[91mliger-kernel==0[0m[91m.5.[0m[91m9
[fastapi] [0m[91m + [0m[91mllvmlite[0m[91m==0.49.[0m[91m0
[fastapi] + lm-eval==0[0m[91m.4.7
[fastapi] +[0m[91m lxml==6[0m[91m.1.[0m[91m3
[fastapi] [0m[91m+ [0m[91mmarkdown[0m[91m==3.[0m[91m10.3
[fastapi] [0m[91m+ markdown-it-py[0m[91m==4.2.[0m[91m0[0m[91m
[fastapi] [0m[91m + markupsafe[0m[91m==3.0.3[0m[91m
[fastapi] [0m[91m+ mbstrdecoder[0m[91m==1.1.5
[fastapi] + [0m[91mmdurl==0[0m[91m.1.2
[fastapi] [0m[91m [0m[91m+ [0m[91mmodal==0[0m[91m.70.[0m[91m5
[fastapi] [0m[91m+ [0m[91mmore-itertools[0m[91m==11.1[0m[91m.0
[fastapi] [0m[91m [0m[91m+ mpmath[0m[91m==1[0m[91m.3[0m[91m.0
[fastapi] [0m[91m +[0m[91m msal[0m[91m==1[0m[91m.38.0[0m[91m
[fastapi] [0m[91m+ msal-extensions[0m[91m==1.3.1
[fastapi] + multidict[0m[91m==6.8.0[0m[91m
[fastapi] + [0m[91mmultiprocess==0[0m[91m.70.16
[fastapi] [0m[91m+[0m[91m networkx==[0m[91m3.[0m[91m6.1[0m[91m
[fastapi] [0m[91m+ [0m[91mnltk[0m[91m==3.[0m[91m10.3[0m[91m
[fastapi] +[0m[91m [0m[91mnumba==[0m[91m0[0m[91m.67.0[0m[91m
[fastapi] +[0m[91m numexpr[0m[91m==[0m[91m2.14[0m[91m.2[0m[91m
[fastapi] + numpy[0m[91m==2.0.1
[fastapi] [0m[91m+ nvidia-cublas-cu12==12.4.5.8[0m[91m
[fastapi] + nvidia-cuda-cupti-cu12[0m[91m==12.4[0m[91m.127
[fastapi] [0m[91m+ [0m[91mnvidia-cuda-nvrtc-cu12[0m[91m==12.4.127
[fastapi] [0m[91m+ [0m[91mnvidia-cuda-runtime-cu12[0m[91m==12.4.127
[fastapi] +[0m[91m [0m[91mnvidia-cudnn-cu12==[0m[91m9.1[0m[91m.0.[0m[91m70[0m[91m
[fastapi] +[0m[91m [0m[91mnvidia-cufft-cu12[0m[91m==11.[0m[91m2.1[0m[91m.3[0m[91m
[fastapi] +[0m[91m nvidia-curand-cu12==10.3.5.147
[fastapi] + [0m[91mnvidia-cusolver-cu12==11.6.1.[0m[91m9
[fastapi] + nvidia-cusparse-cu12[0m[91m==12.3.1.170
[fastapi] +[0m[91m nvidia-cusparselt-cu12==0.6.2
[fastapi] [0m[91m+ nvidia-ml-py==12.560[0m[91m.30
[fastapi] + nvidia-nccl-cu12[0m[91m==2.21.[0m[91m5
[fastapi] [0m[91m+ nvidia-nvjitlink-cu12==[0m[91m12.4.[0m[91m127
[fastapi] +[0m[91m nvidia-nvtx-cu12==[0m[91m12.4.127[0m[91m
[fastapi] + [0m[91moauthlib[0m[91m==3.3[0m[91m.1
[fastapi] [0m[91m+[0m[91m oci==[0m[91m2.186.0[0m[91m
[fastapi] + [0m[91mocifs[0m[91m==1.[0m[91m3.2[0m[91m
[fastapi] [0m[91m+ [0m[91mopentelemetry-api[0m[91m==1.[0m[91m44[0m[91m.0
[fastapi] [0m[91m +[0m[91m opentelemetry-exporter-otlp-proto-common==[0m[91m1.44.0[0m[91m
[fastapi] + opentelemetry-exporter-otlp-proto-http==1.44.0
[fastapi] + opentelemetry-proto==1.44.0
[fastapi] + opentelemetry-sdk==1.44.0
[fastapi] + opentelemetry-semantic-conventions==0.65b0
[fastapi] + optimum==1.16.2
[fastapi] + orjson==3.12.0
[fastapi] + pandas==2.3.3
[fastapi] + pathvalidate==3.3.1
[fastapi] + peft==0.15.2
[fastapi] + pillow==11.3.0
[fastapi] + platformdirs==4.11.8
[fastapi] + portalocker==4.3.2
[fastapi] + propcache==0.5.2
[fastapi] + proto-plus==1.28.2
[fastapi] + protobuf==5.29.6
[fastapi] + psutil==7.2.2
[fastapi] + pyarrow==25.0.1
[fastapi] + pyasn1==0.6.4
[fastapi] + pyasn1-modules==0.4.2
[fastapi] + pybind11==3.1.0
[fastapi] + pycparser==3.0
[fastapi] + pydantic==2.10.6
[fastapi] + pydantic-core==2.27.2
[fastapi] + pydub==0.25.1
[fastapi] + pygments==2.21.0
[fastapi] + pyjwt==2.14.0
[fastapi] + pyopenssl==26.4.0
[fastapi] + pytablewriter==1.2.1
[fastapi] + python-dateutil==2.9.0.post0
[fastapi] + python-dotenv==1.0.1
[fastapi] + python-multipart==0.0.32
[fastapi] + pytz==2026.3.post1
[fastapi] + pyyaml==6.0.3
[fastapi] + regex==2026.9.10
[fastapi] + requests==2.34.2
[fastapi] + requests-oauthlib==2.0.0
[fastapi] + responses==0.18.0
[fastapi] + rich==15.0.0
[fastapi] + rouge-score==0.1.2
[fastapi] + ruff==0.16.7
[fastapi] + s3fs==2025.3.0
[fastapi] + sacrebleu==2.6.0
[fastapi] + safehttpx==0.1.7
[fastapi] + safetensors==0.8.0
[fastapi] + schedulefree==1.4.1
[fastapi] + scikit-learn==1.4.2
[fastapi] + scipy==1.18.1
[fastapi] + semantic-version==2.10.0
[fastapi] + sentencepiece==0.2.2
[fastapi] + shellingham==1.5.4
[fastapi] + sigtools==4.0.1
[fastapi] + six==1.17.0
[fastapi] + sqlitedict==2.1.0
[fastapi] + starlette==0.52.1
[fastapi] + sympy==1.13.1
[fastapi] + synchronicity==0.9.16
[fastapi] + tabledata==1.3.5
[fastapi] + tabulate==0.10.0
[fastapi] + tcolorpy==0.1.7
[fastapi] + tensorboard==2.20.0
[fastapi] + tensorboard-data-server==0.7.2
[fastapi] + termcolor==3.3.0
[fastapi] + threadpoolctl==3.6.0
[fastapi] + tokenizers==0.21.4
[fastapi] + toml==0.10.2
[fastapi] + tomlkit==0.13.3
[fastapi] + torch==2.6.0
[fastapi] + torchao==0.9.0
[fastapi] + tqdm==4.70.1
[fastapi] + tqdm-multiprocess==0.0.11
[fastapi] + transformers==4.51.3
[fastapi] + triton==3.2.0
[fastapi] + trl==0.17.0
[fastapi] + typepy==1.3.5
[fastapi] + typer==0.27.2
[fastapi] + types-certifi==2021.10.8.3
[fastapi] + types-toml==0.10.8.20260518
[fastapi] + typing-extensions==4.16.0
[fastapi] + typing-inspection==0.4.4
[fastapi] + tzdata==2026.4
[fastapi] + urllib3==2.7.0
[fastapi] + uvicorn==0.53.0
[fastapi] + wandb==0.30.0
[fastapi] + watchfiles==1.2.0
[fastapi] + websockets==15.0.1
[fastapi] + werkzeug==3.1.8
[fastapi] + word2number==1.1
[fastapi] + wrapt==1.17.3
[fastapi] + xformers==0.0.29.post2
[fastapi] + xxhash==4.0.1
[fastapi] + yarl==1.24.5
[fastapi] + zstandard==0.22.0
[fastapi] [0mCollecting requests==2.32.3
[fastapi] Downloading requests-2.32.3-py3-none-any.whl.metadata (4.6 kB)
[fastapi] Requirement already satisfied: charset-normalizer<4,>=2 in /workspace/axo_py/lib/python3.12/site-packages (from requests==2.32.3) (3.5.1)
[fastapi] Requirement already satisfied: idna<4,>=2.5 in /workspace/axo_py/lib/python3.12/site-packages (from requests==2.32.3) (3.19)
[fastapi] Requirement already satisfied: urllib3<3,>=1.21.1 in /workspace/axo_py/lib/python3.12/site-packages (from requests==2.32.3) (2.7.0)
[fastapi] Requirement already satisfied: certifi>=2017.4.17 in /workspace/axo_py/lib/python3.12/site-packages (from requests==2.32.3) (2026.7.22)
[fastapi] Downloading requests-2.32.3-py3-none-any.whl (64 kB)
[fastapi] Installing collected packages: requests
[fastapi] Attempting uninstall: requests
[fastapi] Found existing installation: requests 2.34.2
[fastapi] Uninstalling requests-2.34.2:
[fastapi] Successfully uninstalled requests-2.34.2
[fastapi] [91mERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
[fastapi] google-api-core 2.33.0 requires requests<3.0.0,>=2.33.0, but you have requests 2.32.3 which is incompatible.
[fastapi] [0mSuccessfully installed requests-2.32.3
[fastapi] [91m
[fastapi] [notice] A new release of pip is available: 25.0.1 -> 26.2.1
[fastapi] [notice] To update, run: pip install --upgrade pip
[fastapi] [0m ---> 49a0912c787d
[fastapi] Step 13/20 : RUN pip install uv &&     pip install -U packaging==23.2 setuptools==75.8.0 wheel ninja &&     uv pip install torch==2.9.1 --system &&     uv pip install -r /workspace/scripts/training_requirements.txt --system &&     pip install hf_transfer==0.1.9 &&     pip install tenacity==9.1.2 &&     pip install tiktoken==0.9.0 &&     pip install "$FLASH_ATTN_WHEEL" &&     pip install "fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0"
[fastapi] ---> Running in f5a2676517c0
[fastapi] Collecting uv
[fastapi] Using cached uv-0.12.14-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] Using cached uv-0.12.14-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.0 MB)
[fastapi] Installing collected packages: uv
[fastapi] Successfully installed uv-0.12.14
[fastapi] Collecting packaging==23.2
[fastapi] Using cached packaging-23.2-py3-none-any.whl.metadata (3.2 kB)
[fastapi] Collecting setuptools==75.8.0
[fastapi] Using cached setuptools-75.8.0-py3-none-any.whl.metadata (6.7 kB)
[fastapi] Collecting wheel
[fastapi] Using cached wheel-0.48.0-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Collecting ninja
[fastapi] Using cached ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (5.4 kB)
[fastapi] INFO: pip is looking at multiple versions of wheel to determine which version is compatible with other requirements. This could take a while.
[fastapi] Collecting wheel
[fastapi] Using cached wheel-0.47.0-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Using cached wheel-0.46.3-py3-none-any.whl.metadata (2.4 kB)
[fastapi] Using cached wheel-0.46.2-py3-none-any.whl.metadata (2.4 kB)
[fastapi] Using cached wheel-0.45.1-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Using cached packaging-23.2-py3-none-any.whl (53 kB)
[fastapi] Using cached setuptools-75.8.0-py3-none-any.whl (1.2 MB)
[fastapi] Using cached wheel-0.45.1-py3-none-any.whl (72 kB)
[fastapi] Using cached ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (183 kB)
[fastapi] Installing collected packages: wheel, setuptools, packaging, ninja
[fastapi] Attempting uninstall: setuptools
[fastapi] Found existing installation: setuptools 84.0.0
[fastapi] Uninstalling setuptools-84.0.0:
[fastapi] Successfully uninstalled setuptools-84.0.0
[fastapi] Attempting uninstall: packaging
[fastapi] Found existing installation: packaging 26.3
[fastapi] Uninstalling packaging-26.3:
[fastapi] Successfully uninstalled packaging-26.3
[fastapi] Successfully installed ninja-1.13.2 packaging-23.2 setuptools-75.8.0 wheel-0.45.1
[fastapi] [91mUsing Python 3.12.13 environment at: /usr
[fastapi] [0m[91mChecked 1 package in 43ms
[fastapi] [0m[91mUsing Python 3.12.13 environment at: /usr
[fastapi] [0m[91mResolved 191 packages in 860ms
[fastapi] [0m[91m   Building antlr4-python3-runtime==4.9.3
[fastapi] [0m[91m   Building deepspeed==0.19.5
[fastapi] [0m[91mDownloading pillow (6.6MiB)
[fastapi] [0m[91mDownloading sentencepiece (1.2MiB)
[fastapi] [0m[91mDownloading pandas (12.1MiB)
[fastapi] [0m[91mDownloading pydantic-core (2.0MiB)
[fastapi] [0m[91mDownloading bitsandbytes (39.1MiB)
[fastapi] [0m[91mDownloading tokenizers (3.1MiB)
[fastapi] [0m[91mDownloading kiwisolver (1.4MiB)
[fastapi] [0m[91mDownloading pycryptodome (2.2MiB)
[fastapi] [0m[91mDownloading mlflow-skinny (3.5MiB)
[fastapi] [0m[91mDownloading wandb (20.4MiB)
[fastapi] [0m[91mDownloading sqlalchemy (3.3MiB)
[fastapi] [0m[91mDownloading hf-xet (4.3MiB)
[fastapi] [0m[91mDownloading transformers (10.6MiB)
[fastapi] [0m[91mDownloading pyphen (2.0MiB)
[fastapi] [0m[91mDownloading fonttools (5.2MiB)
[fastapi] [0m[91mDownloading tensorboard (5.2MiB)
[fastapi] [0m[91mDownloading numpy (15.9MiB)
[fastapi] [0m[91mDownloading scipy (35.6MiB)
[fastapi] [0m[91mDownloading plotly (8.6MiB)
[fastapi] [0m[91mDownloading dash (8.5MiB)
[fastapi] [0m[91mDownloading mpi4py (1.3MiB)
[fastapi] [0m[91mDownloading mlflow-tracing (1.7MiB)
[fastapi] [0m[91mDownloading openai (1.9MiB)
[fastapi] [0m[91mDownloading matplotlib (9.4MiB)
[fastapi] [0m[91mDownloading mlflow (11.0MiB)
[fastapi] [0m[91mDownloading scikit-learn (8.7MiB)
[fastapi] [0m[91m Downloaded sentencepiece
[fastapi] [0m[91m Downloaded mpi4py
[fastapi] [0m[91m Downloaded kiwisolver
[fastapi] [0m[91m Downloaded mlflow-tracing
[fastapi] [0m[91m Downloaded pydantic-core
[fastapi] [0m[91m Downloaded pyphen
[fastapi] [0m[91m Downloaded openai
[fastapi] [0m[91m Downloaded pycryptodome
[fastapi] [0m[91m Downloaded tokenizers
[fastapi] [0m[91m Downloaded sqlalchemy
[fastapi] [0m[91m Downloaded mlflow-skinny
[fastapi] [0m[91m      Built antlr4-python3-runtime==4.9.3
[fastapi] [0m[91m Downloaded hf-xet
[fastapi] [0m[91m Downloaded fonttools
[fastapi] [0m[91m Downloaded tensorboard
[fastapi] [0m[91m Downloaded pillow
[fastapi] [0m[91m Downloaded plotly
[fastapi] Downloaded dash
[fastapi] [0m[91m Downloaded scikit-learn
[fastapi] [0m[91m Downloaded matplotlib
[fastapi] [0m[91m Downloaded mlflow
[fastapi] [0m[91m Downloaded transformers
[fastapi] [0m[91m Downloaded pandas
[fastapi] [0m[91m Downloaded numpy
[fastapi] [0m[91m Downloaded wandb
[fastapi] [0m[91m Downloaded bitsandbytes
[fastapi] [0m[91m Downloaded scipy
[fastapi] [0m[91m      Built deepspeed==0.19.5
[fastapi] [0m[91mPrepared 99 packages in 1.58s
[fastapi] [0m[91mUninstalled 1 package in 19ms
[fastapi] [0m[91mInstalled 139 packages in 1.49s
[fastapi] [0m[91m + absl-py==2.5.0
[fastapi] + accelerate==1.13.0
[fastapi] + aiohappyeyeballs==2.7.1
[fastapi] + aiohttp[0m[91m==3.14.3
[fastapi] + aiosignal==1.4.[0m[91m0
[fastapi] + alembic==1.20[0m[91m.0[0m[91m
[fastapi] + [0m[91mannotated-doc==[0m[91m0.0.[0m[91m5[0m[91m
[fastapi] +[0m[91m annotated-types[0m[91m==0.[0m[91m8[0m[91m.0
[fastapi] [0m[91m [0m[91m+ antlr4-python3-runtime==4.9.3
[fastapi] + astor==0.8[0m[91m.1
[fastapi] + bitsandbytes==0.50.1
[fastapi] + blinker==1.[0m[91m9.0
[fastapi] + [0m[91mcachetools==7.[0m[91m1.8
[fastapi] [0m[91m+ click==[0m[91m8.5.0[0m[91m
[fastapi] + [0m[91mcloudpickle==3.1.2
[fastapi] + cmudict==1.1[0m[91m.3
[fastapi] + contourpy==1.4.0
[fastapi] + cryptography==50[0m[91m.0.1
[fastapi] + cycler==[0m[91m0.12.1
[fastapi] + [0m[91mdash==4.4.1[0m[91m
[fastapi] + databricks-sdk==[0m[91m0.139.0
[fastapi] [0m[91m+ datasets==4.[0m[91m8.5
[fastapi] + deepspeed[0m[91m==0.19.5[0m[91m
[fastapi] + detoxify[0m[91m==[0m[91m0.5.2[0m[91m
[fastapi] +[0m[91m dill[0m[91m==0.[0m[91m4.1[0m[91m
[fastapi] [0m[91m+ [0m[91mdocker==7.[0m[91m2.0[0m[91m
[fastapi] + [0m[91mdocker-pycreds==0.4.0
[fastapi] [0m[91m + [0m[91meinops==0[0m[91m.8.1[0m[91m
[fastapi] + [0m[91mfastapi==0[0m[91m.141.1[0m[91m
[fastapi] +[0m[91m flask[0m[91m==3.1.3[0m[91m
[fastapi] + [0m[91mflask-cors[0m[91m==6.0.5[0m[91m
[fastapi] +[0m[91m fonttools[0m[91m==4.65.[0m[91m0
[fastapi] [0m[91m+ frozenlist[0m[91m==1.8[0m[91m.0
[fastapi] [0m[91m -[0m[91m fsspec[0m[91m==2026.[0m[91m7.0
[fastapi] [0m[91m+ [0m[91mfsspec==[0m[91m2026.2.[0m[91m0
[fastapi] + gdown==[0m[91m6.2.0
[fastapi] [0m[91m+ gitdb==4.0[0m[91m.12
[fastapi] + gitpython==3.1.62
[fastapi] [0m[91m + google-auth[0m[91m==2.58[0m[91m.0[0m[91m
[fastapi] +[0m[91m graphene==[0m[91m3[0m[91m.4.3[0m[91m
[fastapi] +[0m[91m [0m[91mgraphql-core[0m[91m==3.2.12[0m[91m
[fastapi] + graphql-relay==3.2.0[0m[91m
[fastapi] + greenlet==3.5.6[0m[91m
[fastapi] + grpcio[0m[91m==1.84.0[0m[91m
[fastapi] + gunicorn[0m[91m==26.2.0
[fastapi] +[0m[91m hf-xet==1.6.[0m[91m0
[fastapi] + [0m[91mhjson==3.1.0
[fastapi] + [0m[91mhttpcore2==2[0m[91m.13.0[0m[91m
[fastapi] + [0m[91mhttpx2==2.[0m[91m13.0
[fastapi] + huey==3.4.[0m[91m0
[fastapi] + huggingface-hub==1.31.0[0m[91m
[fastapi] [0m[91m+[0m[91m importlib-metadata[0m[91m==9.[0m[91m0.[0m[91m1
[fastapi] [0m[91m+ [0m[91mimportlib-resources[0m[91m==7.[0m[91m1.0[0m[91m
[fastapi] [0m[91m + [0m[91mitsdangerous[0m[91m==2.[0m[91m2.0[0m[91m
[fastapi] [0m[91m + jaconv==0.[0m[91m5.0
[fastapi] [0m[91m+ janus==2[0m[91m.0.0
[fastapi] [0m[91m + jiter[0m[91m==0.17.0[0m[91m
[fastapi] +[0m[91m joblib==1[0m[91m.6.0
[fastapi] [0m[91m + [0m[91mkiwisolver==1.5.1[0m[91m
[fastapi] + langcheck[0m[91m==0.9.0
[fastapi] [0m[91m + liger-kernel==0.8.[0m[91m1
[fastapi] + mako==1.4[0m[91m.1
[fastapi] + markdown[0m[91m==3.10.[0m[91m3
[fastapi] + [0m[91mmatplotlib==3[0m[91m.11.2
[fastapi] [0m[91m + minio[0m[91m==7.2.[0m[91m20
[fastapi] + [0m[91mmlflow==3[0m[91m.16.0[0m[91m
[fastapi] + mlflow-skinny[0m[91m==3.16.[0m[91m0
[fastapi] +[0m[91m mlflow-tracing==3[0m[91m.16.0
[fastapi] +[0m[91m mpi4py==4.1.2
[fastapi] + [0m[91mmsgpack==1.2[0m[91m.2
[fastapi] +[0m[91m multidict==6.[0m[91m8.0
[fastapi] [0m[91m+ multiprocess==[0m[91m0.70.19
[fastapi] [0m[91m+ narwhals==[0m[91m2.26.0
[fastapi] +[0m[91m nest-asyncio==1.[0m[91m6.0
[fastapi] +[0m[91m [0m[91mnlpaug==1.[0m[91m1.11[0m[91m
[fastapi] [0m[91m + nltk[0m[91m==3.10.3[0m[91m
[fastapi] + numpy[0m[91m==2.4.[0m[91m6
[fastapi] +[0m[91m [0m[91momegaconf[0m[91m==2[0m[91m.[0m[91m3.1
[fastapi] + [0m[91mopenai==[0m[91m3.14.0
[fastapi] + [0m[91mopentelemetry-api==1.44.0
[fastapi] + [0m[91mopentelemetry-proto==1.44.0[0m[91m
[fastapi] + opentelemetry-sdk==1[0m[91m.44.0
[fastapi] +[0m[91m opentelemetry-semantic-conventions==0.65b0[0m[91m
[fastapi] + pandas==2[0m[91m.2.3
[fastapi] [0m[91m+[0m[91m peft[0m[91m==0.19[0m[91m.[0m[91m1[0m[91m
[fastapi] + [0m[91mpillow[0m[91m==12.[0m[91m3.0[0m[91m
[fastapi] [0m[91m+ plotly[0m[91m==7.0.0
[fastapi] [0m[91m+ prettytable==3.18.0
[fastapi] [0m[91m + [0m[91mpropcache==[0m[91m0.5.[0m[91m2
[fastapi] +[0m[91m protobuf==6.33.[0m[91m6
[fastapi] + py-cpuinfo==[0m[91m9.0.0
[fastapi] [0m[91m+ pyarrow==[0m[91m25.0.1
[fastapi] + pyasn1==[0m[91m0.6.4[0m[91m
[fastapi] + [0m[91mpyasn1-modules==[0m[91m0.4.[0m[91m2
[fastapi] [0m[91m+ [0m[91mpycryptodome==3.[0m[91m23.0[0m[91m
[fastapi] +[0m[91m pydantic==[0m[91m2.13.5[0m[91m
[fastapi] [0m[91m+ pydantic-core[0m[91m==2.46[0m[91m.5[0m[91m
[fastapi] + [0m[91mpyparsing==[0m[91m3.3.[0m[91m2
[fastapi] [0m[91m +[0m[91m pyphen[0m[91m==0.[0m[91m18.1[0m[91m
[fastapi] [0m[91m+ pysocks==1.7.1
[fastapi] + [0m[91mpython-dotenv==1.2.3
[fastapi] [0m[91m + pytz==2026.3[0m[91m.post1
[fastapi] + [0m[91mregex==2026.[0m[91m9.10
[fastapi] [0m[91m+ restrictedpython==[0m[91m8.0
[fastapi] [0m[91m+ retrying==1[0m[91m.4.2
[fastapi] [0m[91m+ rouge-score[0m[91m==0.1.2
[fastapi] + [0m[91msafetensors==0.[0m[91m8.0[0m[91m
[fastapi] + [0m[91mscikit-learn[0m[91m==1.9[0m[91m.[0m[91m1
[fastapi] [0m[91m+ [0m[91mscipy==[0m[91m1.15.2
[fastapi] [0m[91m +[0m[91m sentence-transformers[0m[91m==6.0[0m[91m.1
[fastapi] [0m[91m+[0m[91m sentencepiece==0.[0m[91m2[0m[91m.0[0m[91m
[fastapi] [0m[91m + [0m[91msentry-sdk==[0m[91m2.69[0m[91m.1
[fastapi] [0m[91m +[0m[91m [0m[91msetproctitle==1[0m[91m.3.7[0m[91m
[fastapi] [0m[91m [0m[91m+ [0m[91msix==[0m[91m1.17[0m[91m.0[0m[91m
[fastapi] [0m[91m+ [0m[91mskops==[0m[91m0.14[0m[91m.0[0m[91m
[fastapi] +[0m[91m [0m[91msmmap==5.0.3
[fastapi] + sniffio==1.3.1
[fastapi] + sqlalchemy==2.0.53
[fastapi] + sqlparse==0.6.0
[fastapi] + starlette==1.6.0
[fastapi] + tabulate==0.10.0
[fastapi] + tenacity==9.1.4
[fastapi] + tensorboard==2.19.0
[fastapi] + tensorboard-data-server==0.7.2
[fastapi] + textstat==0.7.8
[fastapi] + threadpoolctl==3.6.0
[fastapi] + tokenizers==0.22.2
[fastapi] + toml==0.10.2
[fastapi] + tqdm==4.70.1
[fastapi] + transformers==5.12.1
[fastapi] + trl==1.5.1
[fastapi] + truststore==0.10.4
[fastapi] + typer==0.9.0
[fastapi] + typing-inspection==0.4.4
[fastapi] + uvicorn==0.53.0
[fastapi] + wandb==0.19.10
[fastapi] + werkzeug==3.1.8
[fastapi] + xxhash==4.0.1
[fastapi] + yarl==1.24.5
[fastapi] + zipp==4.1.0
[fastapi] [0mRequirement already satisfied: hf_transfer==0.1.9 in /usr/local/lib/python3.12/dist-packages (0.1.9)
[fastapi] Collecting tenacity==9.1.2
[fastapi] Downloading tenacity-9.1.2-py3-none-any.whl.metadata (1.2 kB)
[fastapi] Downloading tenacity-9.1.2-py3-none-any.whl (28 kB)
[fastapi] Installing collected packages: tenacity
[fastapi] Attempting uninstall: tenacity
[fastapi] Found existing installation: tenacity 9.1.4
[fastapi] Uninstalling tenacity-9.1.4:
[fastapi] Successfully uninstalled tenacity-9.1.4
[fastapi] Successfully installed tenacity-9.1.2
[fastapi] Collecting tiktoken==0.9.0
[fastapi] Downloading tiktoken-0.9.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.7 kB)
[fastapi] Requirement already satisfied: regex>=2022.1.18 in /usr/local/lib/python3.12/dist-packages (from tiktoken==0.9.0) (2026.9.10)
[fastapi] Requirement already satisfied: requests>=2.26.0 in /usr/local/lib/python3.12/dist-packages (from tiktoken==0.9.0) (2.34.2)
[fastapi] Requirement already satisfied: charset_normalizer<4,>=2 in /usr/local/lib/python3.12/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (3.5.1)
[fastapi] Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.12/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (3.19)
[fastapi] Requirement already satisfied: urllib3<3,>=1.26 in /usr/local/lib/python3.12/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (2.7.0)
[fastapi] Requirement already satisfied: certifi>=2023.5.7 in /usr/local/lib/python3.12/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (2026.7.22)
[fastapi] Downloading tiktoken-0.9.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (1.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 42.8 MB/s  0:00:00
[fastapi] Installing collected packages: tiktoken
[fastapi] Successfully installed tiktoken-0.9.0
[fastapi] Collecting flash-attn==2.8.3+cu12torch2.9cxx11abitrue
[fastapi] Downloading flash_attn-2.8.3+cu12torch2.9cxx11abiTRUE-cp312-cp312-linux_x86_64.whl (253.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 253.8/253.8 MB 150.3 MB/s  0:00:01
[fastapi] Requirement already satisfied: torch in /usr/local/lib/python3.12/dist-packages (from flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (2.9.1+cu128)
[fastapi] Requirement already satisfied: einops in /usr/local/lib/python3.12/dist-packages (from flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (0.8.1)
[fastapi] Requirement already satisfied: filelock in /usr/local/lib/python3.12/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (3.32.3)
[fastapi] Requirement already satisfied: typing-extensions>=4.10.0 in /usr/local/lib/python3.12/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (4.16.0)
[fastapi] Requirement already satisfied: setuptools in /usr/local/lib/python3.12/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (75.8.0)
[fastapi] Requirement already satisfied: sympy>=1.13.3 in /usr/local/lib/python3.12/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (1.14.0)
[fastapi] Requirement already satisfied: networkx>=2.5.1 in /usr/local/lib/python3.12/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (3.6.1)
[fastapi] Requirement already satisfied: jinja2 in /usr/local/lib/python3.12/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (3.1.6)
[fastapi] Requirement already satisfied: fsspec>=0.8.5 in /usr/local/lib/python3.12/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (2026.2.0)
[fastapi] Requirement already satisfied: nvidia-cuda-nvrtc-cu12==12.8.93 in /usr/local/lib/python3.12/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (12.8.93)
[fastapi] Requirement already satisfied: nvidia-cuda-runtime-cu12==12.8.90 in /usr/local/lib/python3.12/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (12.8.90)
[fastapi] Requirement already satisfied: nvidia-cuda-cupti-cu12==12.8.90 in /usr/local/lib/python3.12/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (12.8.90)
[fastapi] Requirement already satisfied: nvidia-cudnn-cu12==9.10.2.21 in /usr/local/lib/python3.12/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (9.10.2.21)
[fastapi] Requirement already satisfied: nvidia-cublas-cu12==12.8.4.1 in /usr/local/lib/python3.12/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (12.8.4.1)
[fastapi] Requirement already satisfied: nvidia-cufft-cu12==11.3.3.83 in /usr/local/lib/python3.12/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (11.3.3.83)
[fastapi] Requirement already satisfied: nvidia-curand-cu12==10.3.9.90 in /usr/local/lib/python3.12/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (10.3.9.90)
[fastapi] Requirement already satisfied: nvidia-cusolver-cu12==11.7.3.90 in /usr/local/lib/python3.12/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (11.7.3.90)
[fastapi] Requirement already satisfied: nvidia-cusparse-cu12==12.5.8.93 in /usr/local/lib/python3.12/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (12.5.8.93)
[fastapi] Requirement already satisfied: nvidia-cusparselt-cu12==0.7.1 in /usr/local/lib/python3.12/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (0.7.1)
[fastapi] Requirement already satisfied: nvidia-nccl-cu12==2.27.5 in /usr/local/lib/python3.12/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (2.27.5)
[fastapi] Requirement already satisfied: nvidia-nvshmem-cu12==3.3.20 in /usr/local/lib/python3.12/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (3.3.20)
[fastapi] Requirement already satisfied: nvidia-nvtx-cu12==12.8.90 in /usr/local/lib/python3.12/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (12.8.90)
[fastapi] Requirement already satisfied: nvidia-nvjitlink-cu12==12.8.93 in /usr/local/lib/python3.12/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (12.8.93)
[fastapi] Requirement already satisfied: nvidia-cufile-cu12==1.13.1.3 in /usr/local/lib/python3.12/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (1.13.1.3)
[fastapi] Requirement already satisfied: triton==3.5.1 in /usr/local/lib/python3.12/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (3.5.1)
[fastapi] Requirement already satisfied: mpmath<1.4,>=1.1.0 in /usr/local/lib/python3.12/dist-packages (from sympy>=1.13.3->torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (1.3.0)
[fastapi] Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.12/dist-packages (from jinja2->torch->flash-attn==2.8.3+cu12torch2.9cxx11abitrue) (3.0.3)
[fastapi] Installing collected packages: flash-attn
[fastapi] Successfully installed flash-attn-2.8.3
[fastapi] Collecting fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0
[fastapi] Cloning https://github.com/rayonlabs/fiber.git (to revision 2.4.0) to /tmp/pip-install-zz0ocir_/fiber_84e2e014fc4945b9a7d39e91b290ca4f
[fastapi] [91m  Running command git clone --filter=blob:none --quiet https://github.com/rayonlabs/fiber.git /tmp/pip-install-zz0ocir_/fiber_84e2e014fc4945b9a7d39e91b290ca4f
[fastapi] [0m[91m  Running command git checkout -q 57a1aa710774015a0b3f84829654e7037f46a2e1
[fastapi] [0m  Resolved https://github.com/rayonlabs/fiber.git to commit 57a1aa710774015a0b3f84829654e7037f46a2e1
[fastapi] Installing build dependencies: started
[fastapi] Installing build dependencies: finished with status 'done'
[fastapi] Getting requirements to build wheel: started
[fastapi] Getting requirements to build wheel: finished with status 'done'
[fastapi] Preparing metadata (pyproject.toml): started
[fastapi] Preparing metadata (pyproject.toml): finished with status 'done'
[fastapi] Collecting async-substrate-interface<2.0.0,>=1.0.0 (from fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading async_substrate_interface-1.6.4-py3-none-any.whl.metadata (8.5 kB)
[fastapi] Collecting bittensor-commit-reveal==0.1.0 (from fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading bittensor_commit_reveal-0.1.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (8.2 kB)
[fastapi] Collecting colorama<=0.4.6,>0.3.0 (from fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading colorama-0.4.6-py2.py3-none-any.whl.metadata (17 kB)
[fastapi] Collecting eth-typing==5.0.0 (from fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading eth_typing-5.0.0-py3-none-any.whl.metadata (5.1 kB)
[fastapi] Collecting netaddr==1.3.0 (from fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading netaddr-1.3.0-py3-none-any.whl.metadata (5.0 kB)
[fastapi] Collecting pydantic<=2.9.2,>2 (from fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading pydantic-2.9.2-py3-none-any.whl.metadata (149 kB)
[fastapi] Collecting python-dotenv==1.0.1 (from fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading python_dotenv-1.0.1-py3-none-any.whl.metadata (23 kB)
[fastapi] Collecting substrate-interface==1.7.10 (from fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading substrate_interface-1.7.10-py3-none-any.whl.metadata (4.5 kB)
[fastapi] Collecting tenacity==9.0.0 (from fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading tenacity-9.0.0-py3-none-any.whl.metadata (1.2 kB)
[fastapi] Requirement already satisfied: typing-extensions>=4.5.0 in /usr/local/lib/python3.12/dist-packages (from eth-typing==5.0.0->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0) (4.16.0)
[fastapi] Requirement already satisfied: websocket-client<2,>=0.57.0 in /usr/local/lib/python3.12/dist-packages (from substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0) (1.9.0)
[fastapi] Collecting base58<3,>=1.0.3 (from substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading base58-2.1.1-py3-none-any.whl.metadata (3.1 kB)
[fastapi] Requirement already satisfied: certifi>=2019.3.9 in /usr/local/lib/python3.12/dist-packages (from substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2026.7.22)
[fastapi] Requirement already satisfied: idna<4,>=2.1.0 in /usr/local/lib/python3.12/dist-packages (from substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0) (3.19)
[fastapi] Requirement already satisfied: requests<3,>=2.21.0 in /usr/local/lib/python3.12/dist-packages (from substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2.34.2)
[fastapi] Collecting xxhash<4,>=1.3.0 (from substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading xxhash-3.8.1-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (15 kB)
[fastapi] Collecting ecdsa<1,>=0.17.0 (from substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading ecdsa-0.19.2-py2.py3-none-any.whl.metadata (29 kB)
[fastapi] Collecting eth-keys<1,>=0.2.1 (from substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading eth_keys-0.8.0-py3-none-any.whl.metadata (12 kB)
[fastapi] Collecting eth-utils<3,>=1.3.0 (from substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading eth_utils-2.3.2-py3-none-any.whl.metadata (5.6 kB)
[fastapi] Requirement already satisfied: pycryptodome<4,>=3.11.0 in /usr/local/lib/python3.12/dist-packages (from substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0) (3.23.0)
[fastapi] Collecting PyNaCl<2,>=1.0.1 (from substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading pynacl-1.6.2-cp38-abi3-manylinux_2_34_x86_64.whl.metadata (10.0 kB)
[fastapi] Collecting scalecodec<1.3,>=1.2.10 (from substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading scalecodec-1.2.12-py3-none-any.whl.metadata (17 kB)
[fastapi] Collecting py-sr25519-bindings<1,>=0.2.0 (from substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading py_sr25519_bindings-0.2.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.4 kB)
[fastapi] Collecting py-ed25519-zebra-bindings<2,>=1.0 (from substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading py_ed25519_zebra_bindings-1.3.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.1 kB)
[fastapi] Collecting py-bip39-bindings<1,>=0.1.9 (from substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading py_bip39_bindings-0.3.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.5 kB)
[fastapi] Requirement already satisfied: wheel in /usr/local/lib/python3.12/dist-packages (from async-substrate-interface<2.0.0,>=1.0.0->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0) (0.45.1)
[fastapi] Collecting aiosqlite<1.0.0,>=0.21.0 (from async-substrate-interface<2.0.0,>=1.0.0->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading aiosqlite-0.22.1-py3-none-any.whl.metadata (4.3 kB)
[fastapi] Collecting bt-decode==v0.8.0 (from async-substrate-interface<2.0.0,>=1.0.0->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading bt_decode-0.8.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (10 kB)
[fastapi] Collecting websockets>=14.1 (from async-substrate-interface<2.0.0,>=1.0.0->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading websockets-17.1-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (6.3 kB)
[fastapi] Requirement already satisfied: toml>=0.10.0 in /usr/local/lib/python3.12/dist-packages (from bt-decode==v0.8.0->async-substrate-interface<2.0.0,>=1.0.0->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0) (0.10.2)
[fastapi] Requirement already satisfied: six>=1.9.0 in /usr/local/lib/python3.12/dist-packages (from ecdsa<1,>=0.17.0->substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0) (1.17.0)
[fastapi] Collecting eth-hash>=0.3.1 (from eth-utils<3,>=1.3.0->substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading eth_hash-0.8.0-py3-none-any.whl.metadata (4.1 kB)
[fastapi] Collecting cytoolz>=0.10.1 (from eth-utils<3,>=1.3.0->substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading cytoolz-1.1.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (5.2 kB)
[fastapi] Requirement already satisfied: annotated-types>=0.6.0 in /usr/local/lib/python3.12/dist-packages (from pydantic<=2.9.2,>2->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0) (0.8.0)
[fastapi] Collecting pydantic-core==2.23.4 (from pydantic<=2.9.2,>2->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading pydantic_core-2.23.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.6 kB)
[fastapi] Requirement already satisfied: cffi>=2.0.0 in /usr/local/lib/python3.12/dist-packages (from PyNaCl<2,>=1.0.1->substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2.1.1)
[fastapi] Requirement already satisfied: charset_normalizer<4,>=2 in /usr/local/lib/python3.12/dist-packages (from requests<3,>=2.21.0->substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0) (3.5.1)
[fastapi] Requirement already satisfied: urllib3<3,>=1.26 in /usr/local/lib/python3.12/dist-packages (from requests<3,>=2.21.0->substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2.7.0)
[fastapi] Requirement already satisfied: more-itertools in /usr/lib/python3/dist-packages (from scalecodec<1.3,>=1.2.10->substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0) (8.10.0)
[fastapi] Requirement already satisfied: pycparser in /usr/local/lib/python3.12/dist-packages (from cffi>=2.0.0->PyNaCl<2,>=1.0.1->substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0) (3.0)
[fastapi] Collecting toolz>=0.8.0 (from cytoolz>=0.10.1->eth-utils<3,>=1.3.0->substrate-interface==1.7.10->fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading toolz-1.1.0-py3-none-any.whl.metadata (5.1 kB)
[fastapi] Downloading bittensor_commit_reveal-0.1.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (551 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 551.2/551.2 kB 7.5 MB/s  0:00:00
[fastapi] Downloading eth_typing-5.0.0-py3-none-any.whl (20 kB)
[fastapi] Downloading netaddr-1.3.0-py3-none-any.whl (2.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.3/2.3 MB 56.9 MB/s  0:00:00
[fastapi] Downloading python_dotenv-1.0.1-py3-none-any.whl (19 kB)
[fastapi] Downloading substrate_interface-1.7.10-py3-none-any.whl (60 kB)
[fastapi] Downloading tenacity-9.0.0-py3-none-any.whl (28 kB)
[fastapi] Downloading async_substrate_interface-1.6.4-py3-none-any.whl (97 kB)
[fastapi] Downloading bt_decode-0.8.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (648 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 648.7/648.7 kB 40.5 MB/s  0:00:00
[fastapi] Downloading aiosqlite-0.22.1-py3-none-any.whl (17 kB)
[fastapi] Downloading base58-2.1.1-py3-none-any.whl (5.6 kB)
[fastapi] Downloading colorama-0.4.6-py2.py3-none-any.whl (25 kB)
[fastapi] Downloading ecdsa-0.19.2-py2.py3-none-any.whl (150 kB)
[fastapi] Downloading eth_keys-0.8.0-py3-none-any.whl (20 kB)
[fastapi] Downloading eth_utils-2.3.2-py3-none-any.whl (77 kB)
[fastapi] Downloading py_bip39_bindings-0.3.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (432 kB)
[fastapi] Downloading py_ed25519_zebra_bindings-1.3.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (322 kB)
[fastapi] Downloading py_sr25519_bindings-0.2.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (369 kB)
[fastapi] Downloading pydantic-2.9.2-py3-none-any.whl (434 kB)
[fastapi] Downloading pydantic_core-2.23.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 41.0 MB/s  0:00:00
[fastapi] Downloading pynacl-1.6.2-cp38-abi3-manylinux_2_34_x86_64.whl (1.4 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.4/1.4 MB 13.8 MB/s  0:00:00
[fastapi] Downloading scalecodec-1.2.12-py3-none-any.whl (99 kB)
[fastapi] Downloading xxhash-3.8.1-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (220 kB)
[fastapi] Downloading cytoolz-1.1.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (2.9 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.9/2.9 MB 193.5 MB/s  0:00:00
[fastapi] Downloading eth_hash-0.8.0-py3-none-any.whl (8.0 kB)
[fastapi] Downloading toolz-1.1.0-py3-none-any.whl (58 kB)
[fastapi] Downloading websockets-17.1-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (224 kB)
[fastapi] Building wheels for collected packages: fiber
[fastapi] Building wheel for fiber (pyproject.toml): started
[fastapi] Building wheel for fiber (pyproject.toml): finished with status 'done'
[fastapi] Created wheel for fiber: filename=fiber-2.4.0-py3-none-any.whl size=51790 sha256=c50f803eff2fbcdf01560cfffdc65a3891a75b0b315d61d842fd3861f51b5d73
[fastapi] Stored in directory: /tmp/pip-ephem-wheel-cache-fapzxlin/wheels/bc/c5/70/7e1ef731c6e774998eeeabdf4f53bd9445f754333ceca4065f
[fastapi] Successfully built fiber
[fastapi] Installing collected packages: xxhash, websockets, toolz, tenacity, python-dotenv, pydantic-core, py-sr25519-bindings, py-ed25519-zebra-bindings, py-bip39-bindings, netaddr, eth-typing, eth-hash, ecdsa, colorama, bt-decode, bittensor-commit-reveal, base58, aiosqlite, scalecodec, PyNaCl, pydantic, cytoolz, eth-utils, async-substrate-interface, eth-keys, substrate-interface, fiber
[fastapi] Attempting uninstall: xxhash
[fastapi] Found existing installation: xxhash 4.0.1
[fastapi] Uninstalling xxhash-4.0.1:
[fastapi] Successfully uninstalled xxhash-4.0.1
[fastapi] Attempting uninstall: tenacity
[fastapi] Found existing installation: tenacity 9.1.2
[fastapi] Uninstalling tenacity-9.1.2:
[fastapi] Successfully uninstalled tenacity-9.1.2
[fastapi] Attempting uninstall: python-dotenv
[fastapi] Found existing installation: python-dotenv 1.2.3
[fastapi] Uninstalling python-dotenv-1.2.3:
[fastapi] Successfully uninstalled python-dotenv-1.2.3
[fastapi] Attempting uninstall: pydantic-core
[fastapi] Found existing installation: pydantic_core 2.46.5
[fastapi] Uninstalling pydantic_core-2.46.5:
[fastapi] Successfully uninstalled pydantic_core-2.46.5
[fastapi] Attempting uninstall: pydantic
[fastapi] Found existing installation: pydantic 2.13.5
[fastapi] Uninstalling pydantic-2.13.5:
[fastapi] Successfully uninstalled pydantic-2.13.5
[fastapi] [91mERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
[fastapi] dash 4.4.1 requires pydantic>=2.10, but you have pydantic 2.9.2 which is incompatible.
[fastapi] [0mSuccessfully installed PyNaCl-1.6.2 aiosqlite-0.22.1 async-substrate-interface-1.6.4 base58-2.1.1 bittensor-commit-reveal-0.1.0 bt-decode-0.8.0 colorama-0.4.6 cytoolz-1.1.0 ecdsa-0.19.2 eth-hash-0.8.0 eth-keys-0.8.0 eth-typing-5.0.0 eth-utils-2.3.2 fiber-2.4.0 netaddr-1.3.0 py-bip39-bindings-0.3.0 py-ed25519-zebra-bindings-1.3.0 py-sr25519-bindings-0.2.4 pydantic-2.9.2 pydantic-core-2.23.4 python-dotenv-1.0.1 scalecodec-1.2.12 substrate-interface-1.7.10 tenacity-9.0.0 toolz-1.1.0 websockets-17.1 xxhash-3.8.1
[fastapi] ---> 5707729b272f
[fastapi] Step 14/20 : RUN TORCH_CUDA_ARCH_LIST="8.0;9.0+PTX" MAX_JOBS=$BUILD_MAX_JOBS     pip install --no-build-isolation     causal-conv1d==1.6.2.post1 mamba-ssm==2.3.2.post1
[fastapi] ---> Running in 07d334c342d5
[fastapi] Collecting causal-conv1d==1.6.2.post1
[fastapi] Downloading causal_conv1d-1.6.2.post1.tar.gz (29 kB)
[fastapi] Preparing metadata (pyproject.toml): started
[fastapi] Preparing metadata (pyproject.toml): finished with status 'done'
[fastapi] Collecting mamba-ssm==2.3.2.post1
[fastapi] Downloading mamba_ssm-2.3.2.post1.tar.gz (216 kB)
[fastapi] Preparing metadata (pyproject.toml): started
[fastapi] Preparing metadata (pyproject.toml): finished with status 'done'
[fastapi] Requirement already satisfied: torch in /usr/local/lib/python3.12/dist-packages (from causal-conv1d==1.6.2.post1) (2.9.1+cu128)
[fastapi] Requirement already satisfied: packaging in /usr/local/lib/python3.12/dist-packages (from causal-conv1d==1.6.2.post1) (23.2)
[fastapi] Requirement already satisfied: ninja in /usr/local/lib/python3.12/dist-packages (from causal-conv1d==1.6.2.post1) (1.13.2)
[fastapi] Collecting tilelang==0.1.8 (from mamba-ssm==2.3.2.post1)
[fastapi] Downloading tilelang-0.1.8-cp38-abi3-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (15 kB)
[fastapi] Collecting apache-tvm-ffi<=0.1.9 (from mamba-ssm==2.3.2.post1)
[fastapi] Downloading apache_tvm_ffi-0.1.9-cp312-abi3-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl.metadata (6.1 kB)
[fastapi] Collecting quack-kernels>=0.3.4 (from mamba-ssm==2.3.2.post1)
[fastapi] Downloading quack_kernels-0.6.5-py3-none-any.whl.metadata (834 bytes)
[fastapi] Requirement already satisfied: triton>=3.5.0 in /usr/local/lib/python3.12/dist-packages (from mamba-ssm==2.3.2.post1) (3.5.1)
[fastapi] Requirement already satisfied: einops in /usr/local/lib/python3.12/dist-packages (from mamba-ssm==2.3.2.post1) (0.8.1)
[fastapi] Requirement already satisfied: transformers in /usr/local/lib/python3.12/dist-packages (from mamba-ssm==2.3.2.post1) (5.12.1)
[fastapi] Requirement already satisfied: setuptools>=61.0.0 in /usr/local/lib/python3.12/dist-packages (from mamba-ssm==2.3.2.post1) (75.8.0)
[fastapi] Collecting torch-c-dlpack-ext (from tilelang==0.1.8->mamba-ssm==2.3.2.post1)
[fastapi] Downloading torch_c_dlpack_ext-0.1.5-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl.metadata (14 kB)
[fastapi] Requirement already satisfied: cloudpickle in /usr/local/lib/python3.12/dist-packages (from tilelang==0.1.8->mamba-ssm==2.3.2.post1) (3.1.2)
[fastapi] Collecting ml-dtypes (from tilelang==0.1.8->mamba-ssm==2.3.2.post1)
[fastapi] Downloading ml_dtypes-0.6.0-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (8.8 kB)
[fastapi] Requirement already satisfied: numpy>=1.23.5 in /usr/local/lib/python3.12/dist-packages (from tilelang==0.1.8->mamba-ssm==2.3.2.post1) (2.4.6)
[fastapi] Requirement already satisfied: psutil in /usr/local/lib/python3.12/dist-packages (from tilelang==0.1.8->mamba-ssm==2.3.2.post1) (7.2.2)
[fastapi] Requirement already satisfied: tqdm>=4.62.3 in /usr/local/lib/python3.12/dist-packages (from tilelang==0.1.8->mamba-ssm==2.3.2.post1) (4.70.1)
[fastapi] Requirement already satisfied: typing-extensions>=4.10.0 in /usr/local/lib/python3.12/dist-packages (from tilelang==0.1.8->mamba-ssm==2.3.2.post1) (4.16.0)
[fastapi] Collecting z3-solver<4.15.5,>=4.13.0 (from tilelang==0.1.8->mamba-ssm==2.3.2.post1)
[fastapi] Downloading z3_solver-4.15.4.0-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (602 bytes)
[fastapi] Collecting nvidia-cutlass-dsl>=4.7 (from quack-kernels>=0.3.4->mamba-ssm==2.3.2.post1)
[fastapi] Downloading nvidia_cutlass_dsl-4.7.1-py3-none-any.whl.metadata (2.8 kB)
[fastapi] Collecting nvidia-cutlass-dsl-libs-base==4.7.1 (from nvidia-cutlass-dsl>=4.7->quack-kernels>=0.3.4->mamba-ssm==2.3.2.post1)
[fastapi] Downloading nvidia_cutlass_dsl_libs_base-4.7.1-cp312-cp312-manylinux_2_28_x86_64.whl.metadata (2.9 kB)
[fastapi] Collecting nvidia-cutlass-dsl-libs-cu12==4.7.1 (from nvidia-cutlass-dsl>=4.7->quack-kernels>=0.3.4->mamba-ssm==2.3.2.post1)
[fastapi] Downloading nvidia_cutlass_dsl_libs_cu12-4.7.1-cp312-cp312-manylinux_2_28_x86_64.whl.metadata (2.9 kB)
[fastapi] Collecting cuda-python>=12.8 (from nvidia-cutlass-dsl-libs-base==4.7.1->nvidia-cutlass-dsl>=4.7->quack-kernels>=0.3.4->mamba-ssm==2.3.2.post1)
[fastapi] Downloading cuda_python-13.4.1-py3-none-any.whl.metadata (6.8 kB)
[fastapi] Requirement already satisfied: protobuf>=4.21.12 in /usr/local/lib/python3.12/dist-packages (from nvidia-cutlass-dsl-libs-base==4.7.1->nvidia-cutlass-dsl>=4.7->quack-kernels>=0.3.4->mamba-ssm==2.3.2.post1) (6.33.6)
[fastapi] Collecting nvidia-cuda-nvdisasm<14,>=13.3 (from nvidia-cutlass-dsl-libs-base==4.7.1->nvidia-cutlass-dsl>=4.7->quack-kernels>=0.3.4->mamba-ssm==2.3.2.post1)
[fastapi] Downloading nvidia_cuda_nvdisasm-13.4.49-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (1.9 kB)
[fastapi] Collecting nvidia-cutlass-dsl-libs-core==4.7.1 (from nvidia-cutlass-dsl-libs-base==4.7.1->nvidia-cutlass-dsl>=4.7->quack-kernels>=0.3.4->mamba-ssm==2.3.2.post1)
[fastapi] Downloading nvidia_cutlass_dsl_libs_core-4.7.1-py3-none-any.whl.metadata (2.8 kB)
[fastapi] Collecting cuda-bindings~=13.4.1 (from cuda-python>=12.8->nvidia-cutlass-dsl-libs-base==4.7.1->nvidia-cutlass-dsl>=4.7->quack-kernels>=0.3.4->mamba-ssm==2.3.2.post1)
[fastapi] Downloading cuda_bindings-13.4.1-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl.metadata (2.4 kB)
[fastapi] Collecting cuda-core~=1.2.0 (from cuda-python>=12.8->nvidia-cutlass-dsl-libs-base==4.7.1->nvidia-cutlass-dsl>=4.7->quack-kernels>=0.3.4->mamba-ssm==2.3.2.post1)
[fastapi] Downloading cuda_core-1.2.0-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl.metadata (3.3 kB)
[fastapi] Collecting cuda-pathfinder~=1.1 (from cuda-python>=12.8->nvidia-cutlass-dsl-libs-base==4.7.1->nvidia-cutlass-dsl>=4.7->quack-kernels>=0.3.4->mamba-ssm==2.3.2.post1)
[fastapi] Downloading cuda_pathfinder-1.8.1-py3-none-any.whl.metadata (1.9 kB)
[fastapi] Requirement already satisfied: filelock in /usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (3.32.3)
[fastapi] Requirement already satisfied: sympy>=1.13.3 in /usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (1.14.0)
[fastapi] Requirement already satisfied: networkx>=2.5.1 in /usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (3.6.1)
[fastapi] Requirement already satisfied: jinja2 in /usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (3.1.6)
[fastapi] Requirement already satisfied: fsspec>=0.8.5 in /usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (2026.2.0)
[fastapi] Requirement already satisfied: nvidia-cuda-nvrtc-cu12==12.8.93 in /usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (12.8.93)
[fastapi] Requirement already satisfied: nvidia-cuda-runtime-cu12==12.8.90 in /usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (12.8.90)
[fastapi] Requirement already satisfied: nvidia-cuda-cupti-cu12==12.8.90 in /usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (12.8.90)
[fastapi] Requirement already satisfied: nvidia-cudnn-cu12==9.10.2.21 in /usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (9.10.2.21)
[fastapi] Requirement already satisfied: nvidia-cublas-cu12==12.8.4.1 in /usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (12.8.4.1)
[fastapi] Requirement already satisfied: nvidia-cufft-cu12==11.3.3.83 in /usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (11.3.3.83)
[fastapi] Requirement already satisfied: nvidia-curand-cu12==10.3.9.90 in /usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (10.3.9.90)
[fastapi] Requirement already satisfied: nvidia-cusolver-cu12==11.7.3.90 in /usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (11.7.3.90)
[fastapi] Requirement already satisfied: nvidia-cusparse-cu12==12.5.8.93 in /usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (12.5.8.93)
[fastapi] Requirement already satisfied: nvidia-cusparselt-cu12==0.7.1 in /usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (0.7.1)
[fastapi] Requirement already satisfied: nvidia-nccl-cu12==2.27.5 in /usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (2.27.5)
[fastapi] Requirement already satisfied: nvidia-nvshmem-cu12==3.3.20 in /usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (3.3.20)
[fastapi] Requirement already satisfied: nvidia-nvtx-cu12==12.8.90 in /usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (12.8.90)
[fastapi] Requirement already satisfied: nvidia-nvjitlink-cu12==12.8.93 in /usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (12.8.93)
[fastapi] Requirement already satisfied: nvidia-cufile-cu12==1.13.1.3 in /usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (1.13.1.3)
[fastapi] Requirement already satisfied: mpmath<1.4,>=1.1.0 in /usr/local/lib/python3.12/dist-packages (from sympy>=1.13.3->torch->causal-conv1d==1.6.2.post1) (1.3.0)
[fastapi] Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.12/dist-packages (from jinja2->torch->causal-conv1d==1.6.2.post1) (3.0.3)
[fastapi] Requirement already satisfied: huggingface-hub<2.0,>=1.5.0 in /usr/local/lib/python3.12/dist-packages (from transformers->mamba-ssm==2.3.2.post1) (1.31.0)
[fastapi] Requirement already satisfied: pyyaml>=5.1 in /usr/local/lib/python3.12/dist-packages (from transformers->mamba-ssm==2.3.2.post1) (6.0.3)
[fastapi] Requirement already satisfied: regex>=2025.10.22 in /usr/local/lib/python3.12/dist-packages (from transformers->mamba-ssm==2.3.2.post1) (2026.9.10)
[fastapi] Requirement already satisfied: tokenizers<=0.23.0,>=0.22.0 in /usr/local/lib/python3.12/dist-packages (from transformers->mamba-ssm==2.3.2.post1) (0.22.2)
[fastapi] Requirement already satisfied: typer in /usr/local/lib/python3.12/dist-packages (from transformers->mamba-ssm==2.3.2.post1) (0.9.0)
[fastapi] Requirement already satisfied: safetensors>=0.4.3 in /usr/local/lib/python3.12/dist-packages (from transformers->mamba-ssm==2.3.2.post1) (0.8.0)
[fastapi] Requirement already satisfied: click<9.0.0,>=8.4.2 in /usr/local/lib/python3.12/dist-packages (from huggingface-hub<2.0,>=1.5.0->transformers->mamba-ssm==2.3.2.post1) (8.5.0)
[fastapi] Requirement already satisfied: hf-xet<2.0.0,>=1.5.2 in /usr/local/lib/python3.12/dist-packages (from huggingface-hub<2.0,>=1.5.0->transformers->mamba-ssm==2.3.2.post1) (1.6.0)
[fastapi] Requirement already satisfied: httpx<1,>=0.23.0 in /usr/local/lib/python3.12/dist-packages (from huggingface-hub<2.0,>=1.5.0->transformers->mamba-ssm==2.3.2.post1) (0.28.1)
[fastapi] Requirement already satisfied: anyio in /usr/local/lib/python3.12/dist-packages (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers->mamba-ssm==2.3.2.post1) (4.14.2)
[fastapi] Requirement already satisfied: certifi in /usr/local/lib/python3.12/dist-packages (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers->mamba-ssm==2.3.2.post1) (2026.7.22)
[fastapi] Requirement already satisfied: httpcore==1.* in /usr/local/lib/python3.12/dist-packages (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers->mamba-ssm==2.3.2.post1) (1.0.9)
[fastapi] Requirement already satisfied: idna in /usr/local/lib/python3.12/dist-packages (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers->mamba-ssm==2.3.2.post1) (3.19)
[fastapi] Requirement already satisfied: h11>=0.16 in /usr/local/lib/python3.12/dist-packages (from httpcore==1.*->httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers->mamba-ssm==2.3.2.post1) (0.16.0)
[fastapi] Downloading tilelang-0.1.8-cp38-abi3-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (43.5 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 43.5/43.5 MB 268.1 MB/s  0:00:00
[fastapi] Downloading apache_tvm_ffi-0.1.9-cp312-abi3-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (2.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.3/2.3 MB 210.5 MB/s  0:00:00
[fastapi] Downloading z3_solver-4.15.4.0-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (29.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 29.3/29.3 MB 235.6 MB/s  0:00:00
[fastapi] Downloading quack_kernels-0.6.5-py3-none-any.whl (729 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 729.6/729.6 kB 89.1 MB/s  0:00:00
[fastapi] Downloading nvidia_cutlass_dsl-4.7.1-py3-none-any.whl (10 kB)
[fastapi] Downloading nvidia_cutlass_dsl_libs_base-4.7.1-cp312-cp312-manylinux_2_28_x86_64.whl (2.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.8/2.8 MB 196.4 MB/s  0:00:00
[fastapi] Downloading nvidia_cutlass_dsl_libs_core-4.7.1-py3-none-any.whl (1.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 172.6 MB/s  0:00:00
[fastapi] Downloading nvidia_cutlass_dsl_libs_cu12-4.7.1-cp312-cp312-manylinux_2_28_x86_64.whl (88.7 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 88.7/88.7 MB 240.1 MB/s  0:00:00
[fastapi] Downloading nvidia_cuda_nvdisasm-13.4.49-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (5.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.2/5.2 MB 236.0 MB/s  0:00:00
[fastapi] Downloading cuda_python-13.4.1-py3-none-any.whl (7.6 kB)
[fastapi] Downloading cuda_bindings-13.4.1-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (7.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.2/7.2 MB 231.2 MB/s  0:00:00
[fastapi] Downloading cuda_core-1.2.0-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (6.6 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.6/6.6 MB 254.3 MB/s  0:00:00
[fastapi] Downloading cuda_pathfinder-1.8.1-py3-none-any.whl (62 kB)
[fastapi] Downloading ml_dtypes-0.6.0-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (409 kB)
[fastapi] Downloading torch_c_dlpack_ext-0.1.5-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (897 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 897.8/897.8 kB 136.3 MB/s  0:00:00
[fastapi] Building wheels for collected packages: causal-conv1d, mamba-ssm
[fastapi] Building wheel for causal-conv1d (pyproject.toml): started
[fastapi] Building wheel for causal-conv1d (pyproject.toml): finished with status 'done'
[fastapi] Created wheel for causal-conv1d: filename=causal_conv1d-1.6.2.post1-cp312-cp312-linux_x86_64.whl size=193795077 sha256=3d09789a5df2760a59c2064c4570a4ccd30315943581e9553eb1f412cd9e25a6
[fastapi] Stored in directory: /workspace/.cache/pip/wheels/ea/f0/26/5d87ae05a302e6dc8016c50cd8c7ee779585f593b9580e7cf8
[fastapi] Building wheel for mamba-ssm (pyproject.toml): started
[fastapi] Building wheel for mamba-ssm (pyproject.toml): finished with status 'done'
[fastapi] Created wheel for mamba-ssm: filename=mamba_ssm-2.3.2.post1-cp312-cp312-linux_x86_64.whl size=322246976 sha256=8fd21085d668a3bdbb1f7903c81f64434d7ed2c763240f8328a465a42370a7b6
[fastapi] Stored in directory: /workspace/.cache/pip/wheels/da/67/03/99148d6eeaa4ec2855d71295ac83bcbc8ba7b41a2982992c63
[fastapi] Successfully built causal-conv1d mamba-ssm
[fastapi] Installing collected packages: z3-solver, nvidia-cuda-nvdisasm, ml-dtypes, cuda-pathfinder, apache-tvm-ffi, cuda-core, cuda-bindings, cuda-python, torch-c-dlpack-ext, nvidia-cutlass-dsl-libs-core, causal-conv1d, tilelang, nvidia-cutlass-dsl-libs-base, nvidia-cutlass-dsl-libs-cu12, nvidia-cutlass-dsl, quack-kernels, mamba-ssm
[fastapi] Successfully installed apache-tvm-ffi-0.1.9 causal-conv1d-1.6.2.post1 cuda-bindings-13.4.1 cuda-core-1.2.0 cuda-pathfinder-1.8.1 cuda-python-13.4.1 mamba-ssm-2.3.2.post1 ml-dtypes-0.6.0 nvidia-cuda-nvdisasm-13.4.49 nvidia-cutlass-dsl-4.7.1 nvidia-cutlass-dsl-libs-base-4.7.1 nvidia-cutlass-dsl-libs-core-4.7.1 nvidia-cutlass-dsl-libs-cu12-4.7.1 quack-kernels-0.6.5 tilelang-0.1.8 torch-c-dlpack-ext-0.1.5 z3-solver-4.15.4.0
[fastapi] ---> 5420e477699f
[fastapi] Step 15/20 : RUN pip install --no-deps flash-linear-attention==0.5.1 fla-core==0.5.1 &&     python -c "from fla.modules import FusedRMSNormGated; from fla.ops.gated_delta_rule import chunk_gated_delta_rule, fused_recurrent_gated_delta_rule" &&     python -c "import torch; assert torch.__version__.startswith('2.9'), torch.__version__"
[fastapi] ---> Running in 37b36c619b57
[fastapi] Collecting flash-linear-attention==0.5.1
[fastapi] Downloading flash_linear_attention-0.5.1-py3-none-any.whl.metadata (44 kB)
[fastapi] Collecting fla-core==0.5.1
[fastapi] Downloading fla_core-0.5.1-py3-none-any.whl.metadata (44 kB)
[fastapi] Downloading flash_linear_attention-0.5.1-py3-none-any.whl (403 kB)
[fastapi] Downloading fla_core-0.5.1-py3-none-any.whl (702 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 703.0/703.0 kB 37.9 MB/s  0:00:00
[fastapi] Installing collected packages: flash-linear-attention, fla-core
[fastapi] Successfully installed fla-core-0.5.1 flash-linear-attention-0.5.1
[fastapi] [91m/usr/local/lib/python3.12/dist-packages/fla/utils/_device.py:100: UserWarning: Triton is not supported on current platform, roll back to CPU.
[fastapi] _cpu_device_warning()
[fastapi] [0m ---> c32e964db4f3
[fastapi] Step 16/20 : RUN python -m venv /workspace/grpo_py
[fastapi] ---> Running in 8333db0cdab6
[fastapi] ---> fa9e9bd45c92
[fastapi] Step 17/20 : RUN bash -c "source /workspace/grpo_py/bin/activate &&     pip install uv &&     pip install -U packaging==23.2 setuptools==75.8.0 wheel ninja &&     uv pip install torch==2.11.0 &&     uv pip install -r /workspace/scripts/training_requirements.txt &&     pip install hf_transfer==0.1.9 tenacity==9.1.2 tiktoken==0.9.0 &&     uv pip install vllm==0.24.0 &&     pip install \"fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0\" &&     deactivate"
[fastapi] ---> Running in ad8a79d18501
[fastapi] Collecting uv
[fastapi] Using cached uv-0.12.14-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] Using cached uv-0.12.14-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.0 MB)
[fastapi] Installing collected packages: uv
[fastapi] Successfully installed uv-0.12.14
[fastapi] [91m
[fastapi] [notice] A new release of pip is available: 25.0.1 -> 26.2.1
[fastapi] [notice] To update, run: pip install --upgrade pip
[fastapi] [0mCollecting packaging==23.2
[fastapi] Using cached packaging-23.2-py3-none-any.whl.metadata (3.2 kB)
[fastapi] Collecting setuptools==75.8.0
[fastapi] Using cached setuptools-75.8.0-py3-none-any.whl.metadata (6.7 kB)
[fastapi] Collecting wheel
[fastapi] Using cached wheel-0.48.0-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Collecting ninja
[fastapi] Using cached ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (5.4 kB)
[fastapi] INFO: pip is looking at multiple versions of wheel to determine which version is compatible with other requirements. This could take a while.
[fastapi] Collecting wheel
[fastapi] Using cached wheel-0.47.0-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Using cached wheel-0.46.3-py3-none-any.whl.metadata (2.4 kB)
[fastapi] Using cached wheel-0.46.2-py3-none-any.whl.metadata (2.4 kB)
[fastapi] Using cached wheel-0.45.1-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Using cached packaging-23.2-py3-none-any.whl (53 kB)
[fastapi] Using cached setuptools-75.8.0-py3-none-any.whl (1.2 MB)
[fastapi] Using cached wheel-0.45.1-py3-none-any.whl (72 kB)
[fastapi] Using cached ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (183 kB)
[fastapi] Installing collected packages: wheel, setuptools, packaging, ninja
[fastapi] Successfully installed ninja-1.13.2 packaging-23.2 setuptools-75.8.0 wheel-0.45.1
[fastapi] [91m
[fastapi] [notice] A new release of pip is available: 25.0.1 -> 26.2.1
[fastapi] [notice] To update, run: pip install --upgrade pip
[fastapi] [0m[91mUsing Python 3.12.13 environment at: /workspace/grpo_py
[fastapi] [0m[91mResolved 29 packages in 88ms
[fastapi] [0m[91mDownloading torch (506.1MiB)
[fastapi] [0m[91mDownloading sympy (6.0MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-nvrtc (86.0MiB)
[fastapi] [0m[91mDownloading nvidia-nvjitlink (38.8MiB)
[fastapi] [0m[91mDownloading nvidia-nvshmem-cu13 (57.6MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-runtime (2.1MiB)
[fastapi] [0m[91mDownloading nvidia-cusparse (139.2MiB)
[fastapi] [0m[91mDownloading nvidia-cusparselt-cu13 (162.0MiB)[0m[91m
[fastapi] [0m[91mDownloading nvidia-curand (56.8MiB)
[fastapi] [0m[91mDownloading nvidia-cufile (1.2MiB)
[fastapi] [0m[91mDownloading nvidia-cudnn-cu13 (349.1MiB)
[fastapi] [0m[91mDownloading triton (179.5MiB)
[fastapi] [0m[91mDownloading nvidia-cusolver (191.6MiB)
[fastapi] [0m[91mDownloading nvidia-nccl-cu13 (187.4MiB)
[fastapi] [0m[91mDownloading nvidia-cufft (204.2MiB)
[fastapi] [0m[91mDownloading cuda-bindings (6.8MiB)
[fastapi] [0m[91mDownloading nvidia-cublas (403.5MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-cupti (10.2MiB)
[fastapi] [0m[91m Downloaded nvidia-cufile
[fastapi] [0m[91m Downloaded nvidia-cuda-runtime
[fastapi] [0m[91m Downloaded sympy
[fastapi] [0m[91m Downloaded cuda-bindings
[fastapi] [0m[91m Downloaded nvidia-cuda-cupti
[fastapi] [0m[91m Downloaded nvidia-nvjitlink
[fastapi] [0m[91m Downloaded nvidia-curand
[fastapi] [0m[91m Downloaded nvidia-nvshmem-cu13
[fastapi] [0m[91m Downloaded nvidia-cuda-nvrtc
[fastapi] [0m[91m Downloaded nvidia-cusparse
[fastapi] [0m[91m Downloaded nvidia-cusparselt-cu13
[fastapi] [0m[91m Downloaded nvidia-nccl-cu13
[fastapi] [0m[91m Downloaded triton
[fastapi] [0m[91m Downloaded nvidia-cusolver
[fastapi] [0m[91m Downloaded nvidia-cufft
[fastapi] [0m[91m Downloaded nvidia-cudnn-cu13
[fastapi] [0m[91m Downloaded nvidia-cublas
[fastapi] [0m[91m Downloaded torch
[fastapi] [0m[91mPrepared 22 packages in 4.81s
[fastapi] [0m[91mInstalled 28 packages in 724ms
[fastapi] + cuda-bindings==13.4.1
[fastapi] + cuda-pathfinder==1.8.1
[fastapi] + cuda-toolkit==13.0.2
[fastapi] + filelock==3.32.6
[fastapi] + fsspec==2026.7.0
[fastapi] + jinja2[0m[91m==3.1.6
[fastapi] + markupsafe==3.0.3
[fastapi] + mpmath==1.3.0
[fastapi] [0m[91m+ networkx[0m[91m==3.6.1
[fastapi] [0m[91m + nvidia-cublas==13.1.0.3
[fastapi] + nvidia-cuda-cupti==13.0.85
[fastapi] + nvidia-cuda-nvrtc==13.0.88
[fastapi] [0m[91m+ nvidia-cuda-runtime==13[0m[91m.0.96
[fastapi] +[0m[91m nvidia-cudnn-cu13==9[0m[91m.19.0.[0m[91m56
[fastapi] +[0m[91m nvidia-cufft==12.[0m[91m0.0.61[0m[91m
[fastapi] + [0m[91mnvidia-cufile==1[0m[91m.15.1.[0m[91m6
[fastapi] +[0m[91m nvidia-curand[0m[91m==10.[0m[91m4.0.35
[fastapi] +[0m[91m nvidia-cusolver==12.0.4[0m[91m.66
[fastapi] + nvidia-cusparse==12.6[0m[91m.3.3
[fastapi] + nvidia-cusparselt-cu13[0m[91m==0.8.0[0m[91m
[fastapi] [0m[91m+ [0m[91mnvidia-nccl-cu13==2.28[0m[91m.9
[fastapi] + nvidia-nvjitlink==13[0m[91m.0.88
[fastapi] + nvidia-nvshmem-cu13==3.4[0m[91m.5
[fastapi] + [0m[91mnvidia-nvtx[0m[91m==13.0.[0m[91m85
[fastapi] +[0m[91m sympy==1.14.0
[fastapi] + torch==2.11.0[0m[91m
[fastapi] + triton==3.6.0
[fastapi] + typing-extensions==4.[0m[91m16.0
[fastapi] [0m[91mUsing Python 3.12.13 environment at: /workspace/grpo_py
[fastapi] [0m[91mResolved 194 packages in 76ms
[fastapi] [0m[91mDownloading debugpy (3.8MiB)
[fastapi] [0m[91m Downloaded debugpy
[fastapi] [0m[91mPrepared 7 packages in 55ms
[fastapi] [0m[91mUninstalled 1 package in 0.88ms
[fastapi] [0m[91mInstalled 164 packages in 9.10s
[fastapi] [0m[91m + absl-py==2.5.0
[fastapi] + accelerate==1.13.0
[fastapi] + aiohappyeyeballs==2.7.1
[fastapi] + aiohttp==3.14.3
[fastapi] + aiosignal==1.4.0
[fastapi] + alembic==1.20.0
[fastapi] +[0m[91m annotated-doc==0.0.5
[fastapi] + annotated-types==0.8.0
[fastapi] + antlr4-python3-runtime==4.9.3[0m[91m
[fastapi] + anyio==4.15.1
[fastapi] + argon2-cffi[0m[91m==25.[0m[91m1.0
[fastapi] + argon2-cffi-bindings==26.1[0m[91m.0
[fastapi] + astor[0m[91m==0.8.1
[fastapi] + attrs==26.1.0
[fastapi] + [0m[91mbeautifulsoup4==4.15.0
[fastapi] + bitsandbytes==0.50.1
[fastapi] +[0m[91m blinker==[0m[91m1.9[0m[91m.0[0m[91m
[fastapi] +[0m[91m cachetools[0m[91m==7.1.[0m[91m8
[fastapi] + certifi[0m[91m==2026.7.22
[fastapi] + cffi==2.1.[0m[91m1
[fastapi] + [0m[91mcharset-normalizer==[0m[91m3.5.[0m[91m1
[fastapi] [0m[91m+ click[0m[91m==8.[0m[91m5.[0m[91m0
[fastapi] [0m[91m+ [0m[91mcloudpickle==[0m[91m3.1.[0m[91m2
[fastapi] [0m[91m+[0m[91m cmudict[0m[91m==1.1.3
[fastapi] [0m[91m+ comm==0[0m[91m.2.3
[fastapi] [0m[91m+ [0m[91mcontourpy==[0m[91m1.4.[0m[91m0[0m[91m
[fastapi] + [0m[91mcryptography[0m[91m==50[0m[91m.0.1[0m[91m
[fastapi] [0m[91m + [0m[91mcycler[0m[91m==0.[0m[91m12[0m[91m.1
[fastapi] +[0m[91m [0m[91mdash==[0m[91m4[0m[91m.4.1[0m[91m
[fastapi] [0m[91m +[0m[91m [0m[91mdatabricks-sdk==0.139[0m[91m.0
[fastapi] [0m[91m+[0m[91m datasets[0m[91m==4.8[0m[91m.[0m[91m5
[fastapi] +[0m[91m [0m[91mdebugpy==[0m[91m1.8.[0m[91m21[0m[91m
[fastapi] +[0m[91m deepspeed[0m[91m==0.19.5[0m[91m
[fastapi] [0m[91m+[0m[91m defusedxml==0[0m[91m.[0m[91m7.[0m[91m1
[fastapi] +[0m[91m detoxify==0.5.2
[fastapi] +[0m[91m dill==0.[0m[91m4.1
[fastapi] [0m[91m + docker[0m[91m==7.2.0
[fastapi] + docker-pycreds==0.4.0
[fastapi] [0m[91m+ einops==0.8.1
[fastapi] +[0m[91m fastapi==[0m[91m0.141.1[0m[91m
[fastapi] [0m[91m +[0m[91m flask==3.1.3
[fastapi] + flask-cors==6.[0m[91m0.5
[fastapi] + fonttools==4[0m[91m.65.0
[fastapi] [0m[91m + [0m[91mfrozenlist[0m[91m==1.[0m[91m8.[0m[91m0
[fastapi] [0m[91m- fsspec==2026.[0m[91m7[0m[91m.0
[fastapi] [0m[91m + [0m[91mfsspec[0m[91m==2026[0m[91m.2.0
[fastapi] [0m[91m+[0m[91m gdown==[0m[91m6.2.0
[fastapi] + gitdb[0m[91m==4.0.12
[fastapi] [0m[91m+ gitpython==3[0m[91m.1.62
[fastapi] [0m[91m [0m[91m+ google-auth==[0m[91m2[0m[91m.58.0[0m[91m
[fastapi] +[0m[91m [0m[91mgraphene==3[0m[91m.4.[0m[91m3
[fastapi] [0m[91m+ [0m[91mgraphql-core[0m[91m==3[0m[91m.[0m[91m2.12
[fastapi] [0m[91m+[0m[91m graphql-relay[0m[91m==3.[0m[91m2[0m[91m.0
[fastapi] +[0m[91m [0m[91mgreenlet==3[0m[91m.5.6
[fastapi] [0m[91m + grpcio==1.84.0
[fastapi] [0m[91m+ gunicorn==26.2.0
[fastapi] [0m[91m + [0m[91mh11==0.[0m[91m16.0[0m[91m
[fastapi] [0m[91m+ hf-xet[0m[91m==1.[0m[91m6.[0m[91m0
[fastapi] [0m[91m+ [0m[91mhjson[0m[91m==3.1.0[0m[91m
[fastapi] [0m[91m + [0m[91mhttpcore[0m[91m==1.0.[0m[91m9
[fastapi] + httpcore2==[0m[91m2.13.0[0m[91m
[fastapi] + httpx==0.28.1
[fastapi] + httpx2[0m[91m==2.13.0
[fastapi] + [0m[91mhuey==3.4[0m[91m.0[0m[91m
[fastapi] [0m[91m+ huggingface-hub[0m[91m==1.31.[0m[91m0
[fastapi] + idna==3[0m[91m.19
[fastapi] + [0m[91mimportlib-metadata==9.0.[0m[91m1
[fastapi] + importlib-resources==7.1.0
[fastapi] + itsdangerous==2.2.0
[fastapi] [0m[91m+ jaconv==[0m[91m0.5.0
[fastapi] + janus==[0m[91m2.0.0[0m[91m
[fastapi] +[0m[91m [0m[91mjiter==0.[0m[91m17.[0m[91m0
[fastapi] [0m[91m +[0m[91m [0m[91mjoblib==1[0m[91m.6.[0m[91m0[0m[91m
[fastapi] +[0m[91m kiwisolver[0m[91m==1.[0m[91m5[0m[91m.1
[fastapi] [0m[91m +[0m[91m [0m[91mlangcheck==[0m[91m0.[0m[91m9.0[0m[91m
[fastapi] [0m[91m+[0m[91m liger-kernel==0[0m[91m.8.1[0m[91m
[fastapi] [0m[91m+[0m[91m mako==[0m[91m1[0m[91m.4.1[0m[91m
[fastapi] [0m[91m +[0m[91m [0m[91mmarkdown==[0m[91m3.[0m[91m10.3[0m[91m
[fastapi] [0m[91m+ [0m[91mmatplotlib[0m[91m==3[0m[91m.11.2[0m[91m
[fastapi] [0m[91m+ minio==7.2.20
[fastapi] +[0m[91m mlflow==3.16.[0m[91m0
[fastapi] + mlflow-skinny[0m[91m==3.16.0[0m[91m
[fastapi] [0m[91m+ mlflow-tracing[0m[91m==[0m[91m3.16.[0m[91m0
[fastapi] [0m[91m+ [0m[91mmpi4py==[0m[91m4.[0m[91m1.2
[fastapi] [0m[91m [0m[91m+ msgpack[0m[91m==1.[0m[91m2.2[0m[91m
[fastapi] [0m[91m+ [0m[91mmultidict==[0m[91m6.8[0m[91m.0
[fastapi] [0m[91m +[0m[91m [0m[91mmultiprocess==0[0m[91m.70.19
[fastapi] + narwhals==[0m[91m2.26.0[0m[91m
[fastapi] [0m[91m + [0m[91mnest-asyncio[0m[91m==1.6.0
[fastapi] + nlpaug[0m[91m==1.1.11
[fastapi] + nltk==3.[0m[91m10.3
[fastapi] [0m[91m+ [0m[91mnumpy==2[0m[91m.4.6
[fastapi] + omegaconf==2.3[0m[91m.1
[fastapi] + openai[0m[91m==3.14.0[0m[91m
[fastapi] + opentelemetry-api[0m[91m==1.[0m[91m44.0
[fastapi] [0m[91m +[0m[91m opentelemetry-proto[0m[91m==1.[0m[91m44.0[0m[91m
[fastapi] [0m[91m+ opentelemetry-sdk[0m[91m==[0m[91m1.44[0m[91m.0
[fastapi] [0m[91m [0m[91m+ opentelemetry-semantic-conventions[0m[91m==0.65b0
[fastapi] [0m[91m+ pandas==2.2[0m[91m.3
[fastapi] +[0m[91m peft==0[0m[91m.19.1
[fastapi] [0m[91m+ pillow==12.3.0
[fastapi] [0m[91m + platformdirs==4.11.8[0m[91m
[fastapi] + plotly==7.0.[0m[91m0[0m[91m
[fastapi] + [0m[91mprettytable==[0m[91m3.18.[0m[91m0
[fastapi] [0m[91m+ [0m[91mpropcache==0[0m[91m.5.[0m[91m2
[fastapi] [0m[91m+ protobuf==6.33.6
[fastapi] +[0m[91m psutil==[0m[91m7.2.[0m[91m2
[fastapi] [0m[91m+[0m[91m py-cpuinfo[0m[91m==9.0[0m[91m.0[0m[91m
[fastapi] [0m[91m+ pyarrow==25.0.1
[fastapi] + pyasn1==0.6.4
[fastapi] + pyasn1-modules==0.4.2
[fastapi] + pycparser==3.0
[fastapi] + pycryptodome==3.23.0
[fastapi] + pydantic==2.13.5
[fastapi] + pydantic-core==2.46.5
[fastapi] + pyparsing==3.3.2
[fastapi] + pyphen==0.18.1
[fastapi] + pysocks==1.7.1
[fastapi] + python-dateutil==2.9.0.post0
[fastapi] + python-dotenv==1.2.3
[fastapi] + pytz==2026.3.post1
[fastapi] + pyyaml==6.0.3
[fastapi] + regex==2026.9.10
[fastapi] + requests==2.34.2
[fastapi] + restrictedpython==8.0
[fastapi] + retrying==1.4.2
[fastapi] + rouge-score==0.1.2
[fastapi] + safetensors==0.8.0
[fastapi] + scikit-learn==1.9.1
[fastapi] + scipy==1.15.2
[fastapi] + sentence-transformers==6.0.1
[fastapi] + sentencepiece==0.2.0
[fastapi] + sentry-sdk==2.69.1
[fastapi] + setproctitle==1.3.7
[fastapi] + six==1.17.0
[fastapi] + skops==0.14.0
[fastapi] + smmap==5.0.3
[fastapi] + sniffio==1.3.1
[fastapi] + soupsieve==2.9.2
[fastapi] + sqlalchemy==2.0.53
[fastapi] + sqlparse==0.6.0
[fastapi] + starlette==1.6.0
[fastapi] + tabulate==0.10.0
[fastapi] + tenacity==9.1.4
[fastapi] + tensorboard==2.19.0
[fastapi] + tensorboard-data-server==0.7.2
[fastapi] + textstat==0.7.8
[fastapi] + threadpoolctl==3.6.0
[fastapi] + tokenizers==0.22.2
[fastapi] + toml==0.10.2
[fastapi] + tqdm==4.70.1
[fastapi] + transformers==5.12.1
[fastapi] + trl==1.5.1
[fastapi] + truststore==0.10.4
[fastapi] + typer==0.9.0
[fastapi] + typing-inspection==0.4.4
[fastapi] + tzdata==2026.4
[fastapi] + urllib3==2.7.0
[fastapi] + uvicorn==0.53.0
[fastapi] + wandb==0.19.10
[fastapi] + wcwidth==0.8.3
[fastapi] + werkzeug==3.1.8
[fastapi] + xxhash==4.0.1
[fastapi] + yarl==1.24.5
[fastapi] + zipp==4.1.0
[fastapi] [0mCollecting hf_transfer==0.1.9
[fastapi] Downloading hf_transfer-0.1.9-cp38-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (1.7 kB)
[fastapi] Collecting tenacity==9.1.2
[fastapi] Using cached tenacity-9.1.2-py3-none-any.whl.metadata (1.2 kB)
[fastapi] Collecting tiktoken==0.9.0
[fastapi] Using cached tiktoken-0.9.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.7 kB)
[fastapi] Requirement already satisfied: regex>=2022.1.18 in /workspace/grpo_py/lib/python3.12/site-packages (from tiktoken==0.9.0) (2026.9.10)
[fastapi] Requirement already satisfied: requests>=2.26.0 in /workspace/grpo_py/lib/python3.12/site-packages (from tiktoken==0.9.0) (2.34.2)
[fastapi] Requirement already satisfied: charset_normalizer<4,>=2 in /workspace/grpo_py/lib/python3.12/site-packages (from requests>=2.26.0->tiktoken==0.9.0) (3.5.1)
[fastapi] Requirement already satisfied: idna<4,>=2.5 in /workspace/grpo_py/lib/python3.12/site-packages (from requests>=2.26.0->tiktoken==0.9.0) (3.19)
[fastapi] Requirement already satisfied: urllib3<3,>=1.26 in /workspace/grpo_py/lib/python3.12/site-packages (from requests>=2.26.0->tiktoken==0.9.0) (2.7.0)
[fastapi] Requirement already satisfied: certifi>=2023.5.7 in /workspace/grpo_py/lib/python3.12/site-packages (from requests>=2.26.0->tiktoken==0.9.0) (2026.7.22)
[fastapi] Downloading hf_transfer-0.1.9-cp38-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.6 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.6/3.6 MB 155.5 MB/s eta 0:00:00
[fastapi] Using cached tenacity-9.1.2-py3-none-any.whl (28 kB)
[fastapi] Using cached tiktoken-0.9.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (1.2 MB)
[fastapi] Installing collected packages: tenacity, hf_transfer, tiktoken
[fastapi] Attempting uninstall: tenacity
[fastapi] Found existing installation: tenacity 9.1.4
[fastapi] Uninstalling tenacity-9.1.4:
[fastapi] Successfully uninstalled tenacity-9.1.4
[fastapi] Successfully installed hf_transfer-0.1.9 tenacity-9.1.2 tiktoken-0.9.0
[fastapi] [91m
[fastapi] [notice] A new release of pip is available: 25.0.1 -> 26.2.1
[fastapi] [notice] To update, run: pip install --upgrade pip
[fastapi] [0m[91mUsing Python 3.12.13 environment at: /workspace/grpo_py
[fastapi] [0m[91mResolved 192 packages in 335ms
[fastapi] [0m[91mDownloading flashinfer-cubin (426.8MiB)
[fastapi] [0m[91mDownloading anthropic (1.2MiB)
[fastapi] [0m[91mDownloading outlines-core (2.2MiB)
[fastapi] [0m[91mDownloading openai-harmony (2.8MiB)
[fastapi] [0m[91mDownloading opencv-python-headless (58.4MiB)
[fastapi] [0m[91mDownloading cuda-core (6.3MiB)
[fastapi] [0m[91mDownloading mistral-common (6.2MiB)
[fastapi] [0m[91mDownloading apache-tvm-ffi (2.2MiB)
[fastapi] [0m[91mDownloading numba (3.6MiB)
[fastapi] [0m[91mDownloading nvidia-nvvm (61.3MiB)
[fastapi] [0m[91mDownloading xgrammar (42.8MiB)
[fastapi] [0m[91mDownloading numpy (15.8MiB)
[fastapi] [0m[91mDownloading z3-solver (27.9MiB)
[fastapi] [0m[91mDownloading torchvision (7.2MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-cccl (3.7MiB)
[fastapi] [0m[91mDownloading fastsafetensors (2.0MiB)
[fastapi] [0m[91mDownloading setuptools (1.0MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-tileiras (35.3MiB)
[fastapi] [0m[91mDownloading pycountry (7.7MiB)
[fastapi] [0m[91mDownloading tilelang (43.3MiB)
[fastapi] [0m[91mDownloading nvidia-cutlass-dsl-libs-cu13 (75.1MiB)
[fastapi] [0m[91mDownloading nvidia-cudnn-frontend (5.4MiB)
[fastapi] [0m[91mDownloading nvidia-cutlass-dsl-libs-base (71.1MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-nvcc (42.0MiB)
[fastapi] [0m[91mDownloading flashinfer-python (13.3MiB)
[fastapi] [0m[91mDownloading vllm (266.3MiB)
[fastapi] [0m[91mDownloading tokenspeed-triton (77.9MiB)
[fastapi] [0m[91mDownloading llguidance (2.9MiB)
[fastapi] [0m[91mDownloading llvmlite (53.7MiB)
[fastapi] [0m[91mDownloading uvloop (4.2MiB)
[fastapi] [0m[91mDownloading torchaudio (1.7MiB)
[fastapi] [0m[91m Downloaded setuptools
[fastapi] Downloaded anthropic
[fastapi] [0m[91m Downloaded torchaudio
[fastapi] [0m[91m Downloaded fastsafetensors
[fastapi] [0m[91m Downloaded apache-tvm-ffi
[fastapi] [0m[91m Downloaded outlines-core
[fastapi] [0m[91m Downloaded openai-harmony
[fastapi] [0m[91m Downloaded llguidance
[fastapi] [0m[91m Downloaded numba
[fastapi] [0m[91m Downloaded nvidia-cuda-cccl
[fastapi] [0m[91m Downloaded uvloop
[fastapi] [0m[91m Downloaded nvidia-cudnn-frontend
[fastapi] [0m[91m Downloaded mistral-common
[fastapi] [0m[91m Downloaded cuda-core
[fastapi] [0m[91m Downloaded torchvision
[fastapi] [0m[91m Downloaded pycountry
[fastapi] [0m[91m Downloaded flashinfer-python
[fastapi] [0m[91m Downloaded numpy
[fastapi] [0m[91m Downloaded z3-solver
[fastapi] [0m[91m Downloaded nvidia-cuda-tileiras
[fastapi] [0m[91m Downloaded nvidia-cuda-nvcc
[fastapi] [0m[91m Downloaded xgrammar
[fastapi] [0m[91m Downloaded tilelang
[fastapi] [0m[91m Downloaded llvmlite
[fastapi] [0m[91m Downloaded opencv-python-headless
[fastapi] [0m[91m Downloaded nvidia-nvvm
[fastapi] [0m[91m Downloaded nvidia-cutlass-dsl-libs-base
[fastapi] [0m[91m Downloaded nvidia-cutlass-dsl-libs-cu13
[fastapi] [0m[91m Downloaded tokenspeed-triton
[fastapi] [0m[91m Downloaded vllm
[fastapi] [0m[91m Downloaded flashinfer-cubin
[fastapi] [0m[91mPrepared 88 packages in 5.27s
[fastapi] [0m[91mUninstalled 5 packages in 30ms
[fastapi] [0m[91mInstalled 100 packages in 689ms
[fastapi] + agent-detector==2.0.0
[fastapi] + [0m[91manthropic==1.5.0
[fastapi] + apache-tvm-ffi==0.1.9
[fastapi] + blake3==1.0.9
[fastapi] + cbor2==6.1.4
[fastapi] [0m[91m+ compressed-tensors==0.17[0m[91m.0
[fastapi] +[0m[91m cuda-core[0m[91m==1.[0m[91m2.0
[fastapi] + cuda-python==13.4.1[0m[91m
[fastapi] + cuda-tile==1.3.0
[fastapi] + depyf==0.20.0
[fastapi] + detect-installer==0.2.[0m[91m1
[fastapi] +[0m[91m diskcache==5[0m[91m.6[0m[91m.3[0m[91m
[fastapi] + dnspython[0m[91m==[0m[91m2.8.0[0m[91m
[fastapi] [0m[91m +[0m[91m docstring-parser==0.18.0
[fastapi] + [0m[91memail-validator==2.3.0
[fastapi] - fastapi==0.141.1
[fastapi] +[0m[91m fastapi==0.[0m[91m136.3[0m[91m
[fastapi] + fastapi-cli==0.0.32
[fastapi] + fastapi-cloud-cli[0m[91m==0.26.0
[fastapi] + fastar[0m[91m==0.12.0
[fastapi] [0m[91m + fastsafetensors==0.4.0[0m[91m
[fastapi] + flashinfer-cubin==0[0m[91m.6.12
[fastapi] +[0m[91m flashinfer-python==0[0m[91m.6.12
[fastapi] + googleapis-common-protos==1.75.3
[fastapi] +[0m[91m httptools==0.8.0[0m[91m
[fastapi] + humming-kernels==0.1.6
[fastapi] [0m[91m+ ijson==3.[0m[91m5.1[0m[91m
[fastapi] + [0m[91minteregular[0m[91m==0.3.[0m[91m3[0m[91m
[fastapi] + [0m[91mjmespath[0m[91m==1.1.[0m[91m0[0m[91m
[fastapi] +[0m[91m jsonschema[0m[91m==4[0m[91m.26.[0m[91m0
[fastapi] [0m[91m +[0m[91m jsonschema-specifications==2025.9.1[0m[91m
[fastapi] + lark==1[0m[91m.2.2
[fastapi] + llguidance[0m[91m==1.7.6[0m[91m
[fastapi] +[0m[91m llvmlite==0.[0m[91m47.0
[fastapi] + lm-format-enforcer==0.11.3
[fastapi] [0m[91m+ loguru==0.7.3
[fastapi] +[0m[91m markdown-it-py==4.2.0
[fastapi] + [0m[91mmcp==2.2.[0m[91m0
[fastapi] [0m[91m + mcp-types==2.2.0
[fastapi] + mdurl[0m[91m==0.1.2
[fastapi] + [0m[91mmistral-common==1.11.7
[fastapi] +[0m[91m ml-dtypes==0.6.0
[fastapi] + model-hosting-container-standards==0.1.[0m[91m16
[fastapi] + msgspec==0.21.1
[fastapi] + numba==0.65.[0m[91m0
[fastapi] - numpy[0m[91m==2.4[0m[91m.6
[fastapi] [0m[91m + [0m[91mnumpy[0m[91m==2.3.[0m[91m5[0m[91m
[fastapi] + nvidia-cuda-cccl[0m[91m==[0m[91m13.3[0m[91m.4.[0m[91m2.[0m[91m1
[fastapi] [0m[91m+ [0m[91mnvidia-cuda-crt[0m[91m==13.[0m[91m4.59[0m[91m
[fastapi] + [0m[91mnvidia-cuda-nvcc[0m[91m==13.[0m[91m2[0m[91m.86
[fastapi] [0m[91m+ [0m[91mnvidia-cuda-tileiras[0m[91m==13.2.[0m[91m86
[fastapi] + nvidia-cudnn-frontend==1.[0m[91m28.0
[fastapi] [0m[91m+ nvidia-cutlass-dsl==4.5.2
[fastapi] [0m[91m +[0m[91m nvidia-cutlass-dsl-libs-base==4.5.2
[fastapi] + [0m[91mnvidia-cutlass-dsl-libs-cu13==4.5.[0m[91m2
[fastapi] + [0m[91mnvidia-ml-py==13.[0m[91m610.43
[fastapi] + nvidia-nvvm==13.2[0m[91m.86
[fastapi] + [0m[91mopenai-harmony==[0m[91m0.0.8[0m[91m
[fastapi] + opencv-python-headless==[0m[91m5.0.0.93[0m[91m
[fastapi] + opentelemetry-exporter-otlp==1[0m[91m.44.0
[fastapi] [0m[91m+ opentelemetry-exporter-otlp-proto-common==[0m[91m1.44.0
[fastapi] [0m[91m + opentelemetry-exporter-otlp-proto-grpc[0m[91m==1.44.0
[fastapi] +[0m[91m opentelemetry-exporter-otlp-proto-http==1.44[0m[91m.0
[fastapi] +[0m[91m opentelemetry-semantic-conventions-ai==0[0m[91m.5.1
[fastapi] +[0m[91m outlines-core==0.2.[0m[91m14
[fastapi] - [0m[91mpackaging==23.2[0m[91m
[fastapi] + packaging[0m[91m==26.3
[fastapi] [0m[91m + partial-json-parser[0m[91m==0.2.1[0m[91m.1.post7
[fastapi] [0m[91m + prometheus-client[0m[91m==0.26.0
[fastapi] [0m[91m + prometheus-fastapi-instrumentator==8[0m[91m.1.0[0m[91m
[fastapi] [0m[91m + [0m[91mpybase64[0m[91m==1.[0m[91m5.[0m[91m0
[fastapi] [0m[91m+ pycountry==26.2.16
[fastapi] + [0m[91mpydantic-extra-types==2.11.1
[fastapi] +[0m[91m pydantic-settings==2.15.0
[fastapi] + [0m[91mpyelftools==0.33[0m[91m
[fastapi] [0m[91m+ [0m[91mpygments==2[0m[91m.21.[0m[91m0[0m[91m
[fastapi] + [0m[91mpyjwt[0m[91m==2.[0m[91m14.0[0m[91m
[fastapi] [0m[91m+[0m[91m python-json-logger[0m[91m==4.2[0m[91m.[0m[91m0
[fastapi] [0m[91m+ [0m[91mpython-multipart==[0m[91m0.0.[0m[91m32[0m[91m
[fastapi] + [0m[91mpyzmq[0m[91m==27.[0m[91m2.0[0m[91m
[fastapi] [0m[91m+ quack-kernels[0m[91m==0.5[0m[91m.0[0m[91m
[fastapi] [0m[91m+ [0m[91mreferencing==[0m[91m0.37.[0m[91m0[0m[91m
[fastapi] +[0m[91m [0m[91mrich==[0m[91m15.0.[0m[91m0[0m[91m
[fastapi] +[0m[91m rich-toolkit[0m[91m==0.20.5
[fastapi] [0m[91m+ rignore==0[0m[91m.8.1
[fastapi] + rpds-py[0m[91m==2026.6.[0m[91m3
[fastapi] [0m[91m -[0m[91m setuptools[0m[91m==75.8.0
[fastapi] + setuptools[0m[91m==80.10.2
[fastapi] + shellingham[0m[91m==1.5.4
[fastapi] +[0m[91m sse-starlette==3.[0m[91m4.11
[fastapi] [0m[91m + supervisor[0m[91m==4.[0m[91m3[0m[91m.0
[fastapi] [0m[91m+ tilelang==0.[0m[91m1.9
[fastapi] + [0m[91mtokenspeed-mla==0.[0m[91m1.2
[fastapi] [0m[91m+ tokenspeed-triton[0m[91m==3.8.10.post[0m[91m20260906
[fastapi] + [0m[91mtorch-c-dlpack-ext==0.1.[0m[91m5
[fastapi] +[0m[91m torchaudio==2[0m[91m.11.0
[fastapi] [0m[91m + [0m[91mtorchvision==0.[0m[91m26.0
[fastapi] [0m[91m - typer[0m[91m==0.9.[0m[91m0
[fastapi] + typer==0.27[0m[91m.2
[fastapi] +[0m[91m uvloop==0[0m[91m.22.1
[fastapi] + vllm[0m[91m==[0m[91m0.24.0
[fastapi] [0m[91m +[0m[91m watchfiles[0m[91m==1[0m[91m.2.[0m[91m0[0m[91m
[fastapi] +[0m[91m websockets[0m[91m==17.[0m[91m1
[fastapi] + xgrammar[0m[91m==0.2.3
[fastapi] +[0m[91m z3-solver==4.15.4.[0m[91m0
[fastapi] [0mCollecting fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0
[fastapi] Cloning https://github.com/rayonlabs/fiber.git (to revision 2.4.0) to /tmp/pip-install-li3d8pxr/fiber_ea8fc86729e248cca7fd23212e71fce8
[fastapi] [91m  Running command git clone --filter=blob:none --quiet https://github.com/rayonlabs/fiber.git /tmp/pip-install-li3d8pxr/fiber_ea8fc86729e248cca7fd23212e71fce8
[fastapi] [0m[91m  Running command git checkout -q 57a1aa710774015a0b3f84829654e7037f46a2e1
[fastapi] [0m  Resolved https://github.com/rayonlabs/fiber.git to commit 57a1aa710774015a0b3f84829654e7037f46a2e1
[fastapi] Installing build dependencies: started
[fastapi] Installing build dependencies: finished with status 'done'
[fastapi] Getting requirements to build wheel: started
[fastapi] Getting requirements to build wheel: finished with status 'done'
[fastapi] Preparing metadata (pyproject.toml): started
[fastapi] Preparing metadata (pyproject.toml): finished with status 'done'
[fastapi] Collecting async-substrate-interface<2.0.0,>=1.0.0 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached async_substrate_interface-1.6.4-py3-none-any.whl.metadata (8.5 kB)
[fastapi] Collecting bittensor-commit-reveal==0.1.0 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached bittensor_commit_reveal-0.1.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (8.2 kB)
[fastapi] Collecting colorama<=0.4.6,>0.3.0 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached colorama-0.4.6-py2.py3-none-any.whl.metadata (17 kB)
[fastapi] Collecting eth-typing==5.0.0 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached eth_typing-5.0.0-py3-none-any.whl.metadata (5.1 kB)
[fastapi] Collecting netaddr==1.3.0 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached netaddr-1.3.0-py3-none-any.whl.metadata (5.0 kB)
[fastapi] Collecting pydantic<=2.9.2,>2 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached pydantic-2.9.2-py3-none-any.whl.metadata (149 kB)
[fastapi] Collecting python-dotenv==1.0.1 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached python_dotenv-1.0.1-py3-none-any.whl.metadata (23 kB)
[fastapi] Collecting substrate-interface==1.7.10 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached substrate_interface-1.7.10-py3-none-any.whl.metadata (4.5 kB)
[fastapi] Collecting tenacity==9.0.0 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached tenacity-9.0.0-py3-none-any.whl.metadata (1.2 kB)
[fastapi] Requirement already satisfied: typing-extensions>=4.5.0 in /workspace/grpo_py/lib/python3.12/site-packages (from eth-typing==5.0.0->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (4.16.0)
[fastapi] Collecting websocket-client<2,>=0.57.0 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading websocket_client-1.9.2-py3-none-any.whl.metadata (8.3 kB)
[fastapi] Collecting base58<3,>=1.0.3 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached base58-2.1.1-py3-none-any.whl.metadata (3.1 kB)
[fastapi] Requirement already satisfied: certifi>=2019.3.9 in /workspace/grpo_py/lib/python3.12/site-packages (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2026.7.22)
[fastapi] Requirement already satisfied: idna<4,>=2.1.0 in /workspace/grpo_py/lib/python3.12/site-packages (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (3.19)
[fastapi] Requirement already satisfied: requests<3,>=2.21.0 in /workspace/grpo_py/lib/python3.12/site-packages (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2.34.2)
[fastapi] Collecting xxhash<4,>=1.3.0 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached xxhash-3.8.1-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (15 kB)
[fastapi] Collecting ecdsa<1,>=0.17.0 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached ecdsa-0.19.2-py2.py3-none-any.whl.metadata (29 kB)
[fastapi] Collecting eth-keys<1,>=0.2.1 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached eth_keys-0.8.0-py3-none-any.whl.metadata (12 kB)
[fastapi] Collecting eth-utils<3,>=1.3.0 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached eth_utils-2.3.2-py3-none-any.whl.metadata (5.6 kB)
[fastapi] Requirement already satisfied: pycryptodome<4,>=3.11.0 in /workspace/grpo_py/lib/python3.12/site-packages (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (3.23.0)
[fastapi] Collecting PyNaCl<2,>=1.0.1 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached pynacl-1.6.2-cp38-abi3-manylinux_2_34_x86_64.whl.metadata (10.0 kB)
[fastapi] Collecting scalecodec<1.3,>=1.2.10 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached scalecodec-1.2.12-py3-none-any.whl.metadata (17 kB)
[fastapi] Collecting py-sr25519-bindings<1,>=0.2.0 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached py_sr25519_bindings-0.2.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.4 kB)
[fastapi] Collecting py-ed25519-zebra-bindings<2,>=1.0 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached py_ed25519_zebra_bindings-1.3.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.1 kB)
[fastapi] Collecting py-bip39-bindings<1,>=0.1.9 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached py_bip39_bindings-0.3.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.5 kB)
[fastapi] Requirement already satisfied: wheel in /workspace/grpo_py/lib/python3.12/site-packages (from async-substrate-interface<2.0.0,>=1.0.0->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (0.45.1)
[fastapi] Collecting aiosqlite<1.0.0,>=0.21.0 (from async-substrate-interface<2.0.0,>=1.0.0->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached aiosqlite-0.22.1-py3-none-any.whl.metadata (4.3 kB)
[fastapi] Collecting bt-decode==v0.8.0 (from async-substrate-interface<2.0.0,>=1.0.0->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached bt_decode-0.8.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (10 kB)
[fastapi] Requirement already satisfied: websockets>=14.1 in /workspace/grpo_py/lib/python3.12/site-packages (from async-substrate-interface<2.0.0,>=1.0.0->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (17.1)
[fastapi] Requirement already satisfied: toml>=0.10.0 in /workspace/grpo_py/lib/python3.12/site-packages (from bt-decode==v0.8.0->async-substrate-interface<2.0.0,>=1.0.0->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (0.10.2)
[fastapi] Requirement already satisfied: annotated-types>=0.6.0 in /workspace/grpo_py/lib/python3.12/site-packages (from pydantic<=2.9.2,>2->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (0.8.0)
[fastapi] Collecting pydantic-core==2.23.4 (from pydantic<=2.9.2,>2->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached pydantic_core-2.23.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.6 kB)
[fastapi] Requirement already satisfied: six>=1.9.0 in /workspace/grpo_py/lib/python3.12/site-packages (from ecdsa<1,>=0.17.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (1.17.0)
[fastapi] Collecting eth-hash>=0.3.1 (from eth-utils<3,>=1.3.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached eth_hash-0.8.0-py3-none-any.whl.metadata (4.1 kB)
[fastapi] Collecting cytoolz>=0.10.1 (from eth-utils<3,>=1.3.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached cytoolz-1.1.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (5.2 kB)
[fastapi] Requirement already satisfied: cffi>=2.0.0 in /workspace/grpo_py/lib/python3.12/site-packages (from PyNaCl<2,>=1.0.1->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2.1.1)
[fastapi] Requirement already satisfied: charset_normalizer<4,>=2 in /workspace/grpo_py/lib/python3.12/site-packages (from requests<3,>=2.21.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (3.5.1)
[fastapi] Requirement already satisfied: urllib3<3,>=1.26 in /workspace/grpo_py/lib/python3.12/site-packages (from requests<3,>=2.21.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2.7.0)
[fastapi] Collecting more-itertools (from scalecodec<1.3,>=1.2.10->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading more_itertools-11.1.0-py3-none-any.whl.metadata (41 kB)
[fastapi] Requirement already satisfied: pycparser in /workspace/grpo_py/lib/python3.12/site-packages (from cffi>=2.0.0->PyNaCl<2,>=1.0.1->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (3.0)
[fastapi] Collecting toolz>=0.8.0 (from cytoolz>=0.10.1->eth-utils<3,>=1.3.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Using cached toolz-1.1.0-py3-none-any.whl.metadata (5.1 kB)
[fastapi] Using cached bittensor_commit_reveal-0.1.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (551 kB)
[fastapi] Using cached eth_typing-5.0.0-py3-none-any.whl (20 kB)
[fastapi] Using cached netaddr-1.3.0-py3-none-any.whl (2.3 MB)
[fastapi] Using cached python_dotenv-1.0.1-py3-none-any.whl (19 kB)
[fastapi] Using cached substrate_interface-1.7.10-py3-none-any.whl (60 kB)
[fastapi] Using cached tenacity-9.0.0-py3-none-any.whl (28 kB)
[fastapi] Using cached async_substrate_interface-1.6.4-py3-none-any.whl (97 kB)
[fastapi] Using cached bt_decode-0.8.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (648 kB)
[fastapi] Using cached colorama-0.4.6-py2.py3-none-any.whl (25 kB)
[fastapi] Using cached pydantic-2.9.2-py3-none-any.whl (434 kB)
[fastapi] Using cached pydantic_core-2.23.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
[fastapi] Using cached aiosqlite-0.22.1-py3-none-any.whl (17 kB)
[fastapi] Using cached base58-2.1.1-py3-none-any.whl (5.6 kB)
[fastapi] Using cached ecdsa-0.19.2-py2.py3-none-any.whl (150 kB)
[fastapi] Using cached eth_keys-0.8.0-py3-none-any.whl (20 kB)
[fastapi] Using cached eth_utils-2.3.2-py3-none-any.whl (77 kB)
[fastapi] Using cached py_bip39_bindings-0.3.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (432 kB)
[fastapi] Using cached py_ed25519_zebra_bindings-1.3.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (322 kB)
[fastapi] Using cached py_sr25519_bindings-0.2.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (369 kB)
[fastapi] Using cached pynacl-1.6.2-cp38-abi3-manylinux_2_34_x86_64.whl (1.4 MB)
[fastapi] Using cached scalecodec-1.2.12-py3-none-any.whl (99 kB)
[fastapi] Downloading websocket_client-1.9.2-py3-none-any.whl (95 kB)
[fastapi] Using cached xxhash-3.8.1-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (220 kB)
[fastapi] Using cached cytoolz-1.1.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (2.9 MB)
[fastapi] Using cached eth_hash-0.8.0-py3-none-any.whl (8.0 kB)
[fastapi] Downloading more_itertools-11.1.0-py3-none-any.whl (72 kB)
[fastapi] Using cached toolz-1.1.0-py3-none-any.whl (58 kB)
[fastapi] Building wheels for collected packages: fiber
[fastapi] Building wheel for fiber (pyproject.toml): started
[fastapi] Building wheel for fiber (pyproject.toml): finished with status 'done'
[fastapi] Created wheel for fiber: filename=fiber-2.4.0-py3-none-any.whl size=51790 sha256=c50f803eff2fbcdf01560cfffdc65a3891a75b0b315d61d842fd3861f51b5d73
[fastapi] Stored in directory: /tmp/pip-ephem-wheel-cache-xmxtypko/wheels/bc/c5/70/7e1ef731c6e774998eeeabdf4f53bd9445f754333ceca4065f
[fastapi] Successfully built fiber
[fastapi] Installing collected packages: xxhash, websocket-client, toolz, tenacity, python-dotenv, pydantic-core, py-sr25519-bindings, py-ed25519-zebra-bindings, py-bip39-bindings, netaddr, more-itertools, eth-typing, eth-hash, ecdsa, colorama, bt-decode, bittensor-commit-reveal, base58, aiosqlite, scalecodec, PyNaCl, pydantic, cytoolz, eth-utils, async-substrate-interface, eth-keys, substrate-interface, fiber
[fastapi] Attempting uninstall: xxhash
[fastapi] Found existing installation: xxhash 4.0.1
[fastapi] Uninstalling xxhash-4.0.1:
[fastapi] Successfully uninstalled xxhash-4.0.1
[fastapi] Attempting uninstall: tenacity
[fastapi] Found existing installation: tenacity 9.1.2
[fastapi] Uninstalling tenacity-9.1.2:
[fastapi] Successfully uninstalled tenacity-9.1.2
[fastapi] Attempting uninstall: python-dotenv
[fastapi] Found existing installation: python-dotenv 1.2.3
[fastapi] Uninstalling python-dotenv-1.2.3:
[fastapi] Successfully uninstalled python-dotenv-1.2.3
[fastapi] Attempting uninstall: pydantic-core
[fastapi] Found existing installation: pydantic_core 2.46.5
[fastapi] Uninstalling pydantic_core-2.46.5:
[fastapi] Successfully uninstalled pydantic_core-2.46.5
[fastapi] Attempting uninstall: pydantic
[fastapi] Found existing installation: pydantic 2.13.5
[fastapi] Uninstalling pydantic-2.13.5:
[fastapi] Successfully uninstalled pydantic-2.13.5
[fastapi] [91mERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
[fastapi] vllm 0.24.0 requires pydantic>=2.12.0, but you have pydantic 2.9.2 which is incompatible.
[fastapi] dash 4.4.1 requires pydantic>=2.10, but you have pydantic 2.9.2 which is incompatible.
[fastapi] openai-harmony 0.0.8 requires pydantic>=2.11.7, but you have pydantic 2.9.2 which is incompatible.
[fastapi] mcp 2.2.0 requires pydantic>=2.12.0, but you have pydantic 2.9.2 which is incompatible.
[fastapi] mcp-types 2.2.0 requires pydantic>=2.12.0, but you have pydantic 2.9.2 which is incompatible.
[fastapi] [0mSuccessfully installed PyNaCl-1.6.2 aiosqlite-0.22.1 async-substrate-interface-1.6.4 base58-2.1.1 bittensor-commit-reveal-0.1.0 bt-decode-0.8.0 colorama-0.4.6 cytoolz-1.1.0 ecdsa-0.19.2 eth-hash-0.8.0 eth-keys-0.8.0 eth-typing-5.0.0 eth-utils-2.3.2 fiber-2.4.0 more-itertools-11.1.0 netaddr-1.3.0 py-bip39-bindings-0.3.0 py-ed25519-zebra-bindings-1.3.0 py-sr25519-bindings-0.2.4 pydantic-2.9.2 pydantic-core-2.23.4 python-dotenv-1.0.1 scalecodec-1.2.12 substrate-interface-1.7.10 tenacity-9.0.0 toolz-1.1.0 websocket-client-1.9.2 xxhash-3.8.1
[fastapi] [91m
[fastapi] [notice] A new release of pip is available: 25.0.1 -> 26.2.1
[fastapi] [notice] To update, run: pip install --upgrade pip
[fastapi] [0m ---> 22ae1cf3b83a
[fastapi] Step 18/20 : COPY scripts /workspace/scripts
[fastapi] ---> 88eb53ddc7d4
[fastapi] Step 19/20 : RUN chmod +x /workspace/scripts/entrypoint.sh
[fastapi] ---> Running in 6084eb6f0b24
[fastapi] ---> 6dc32fb99995
[fastapi] Step 20/20 : ENTRYPOINT ["./entrypoint.sh"]
[fastapi] ---> Running in bc4f4d9f7099
[fastapi] ---> fc27e6254763
[fastapi] {'aux': {'ID': 'sha256:fc27e6254763393177ff5dd5259935c858b7a8c7eafa9d419fc086ccc6297cf1'}}Successfully built fc27e6254763
[fastapi] Successfully tagged standalone-text-trainer:f03e89e6-82d3-4b16-ac07-049aaf278606
[fastapi] Docker image built successfully.
[fastapi] Container.wait() returned: {'StatusCode': 0}
[fastapi] Cleaning up
[fastapi] Cleaned up Docker resources.
[fastapi] Starting upload container hf-upload-56c47b8afac14f2aaa0d962f77b07369 for task 067761fe-b567-44d7-8863-4cd41cc12261...
[hf-upload-56]  adapter_config.json not found
[hf-upload-56] README.md not found
[hf-upload-56] Creating repo gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5FW2EqiC...
[hf-upload-56] Uploading contents of /app/checkpoints/067761fe-b567-44d7-8863-4cd41cc12261/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5FW2EqiC to gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5FW2EqiC
[hf-upload-56] Uploaded successfully to https://huggingface.co/gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5FW2EqiC
[hf-upload-56] Deleted local folder: /app/checkpoints/067761fe-b567-44d7-8863-4cd41cc12261/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5FW2EqiC
[text-trainer] *****Running text trainer
[text-trainer] /workspace/scripts/text_trainer.py:88: SyntaxWarning: invalid escape sequence '\s'
[text-trainer]   match = re.search(f"(?P<p>--{arg_name}(\s+)([^\s]+))(\s+)", cmd)
[text-trainer] /workspace/scripts/text_trainer.py:98: SyntaxWarning: invalid escape sequence '\s'
[text-trainer]   match = re.search(f"(?P<p>--{arg_name}(\s+)(?P<value>[^\s]+))(\s+)", cmd)
[text-trainer] /usr/local/lib/python3.12/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_hash" in MinerSubmission has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] /workspace/axo_py/lib/python3.12/site-packages/requests/__init__.py:113: RequestsDependencyWarning: urllib3 (2.7.0) or chardet (6.0.0.post1)/charset_normalizer (3.5.1) doesn't match a supported version!
[text-trainer]   warnings.warn(
[text-trainer] /usr/local/lib/python3.12/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] wandb: Tracking run with wandb version 0.19.10
[text-trainer] wandb: W&B syncing is set to `offline` in this directory. Run `wandb online` or set WANDB_MODE=online to enable cloud syncing.
[text-trainer] [1;34mwandb[0m: 
[text-trainer] [1;34mwandb[0m: You can sync this run to the cloud by running:
[text-trainer] [1;34mwandb[0m: [1mwandb sync /app/checkpoints/wandb_logs/067761fe-b567-44d7-8863-4cd41cc12261_5FW2EqiCeLknueng7Bp9rj4JrPNv5F6nxNg7yUtART6U1odT/wandb/offline-run-20260915_100850-067761fe-b567-44d7-8863-4cd41cc12261_tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5FW2EqiC[0m
[text-trainer] [1;34mwandb[0m: Find logs at: [1;35m../../app/checkpoints/wandb_logs/067761fe-b567-44d7-8863-4cd41cc12261_5FW2EqiCeLknueng7Bp9rj4JrPNv5F6nxNg7yUtART6U1odT/wandb/offline-run-20260915_100850-067761fe-b567-44d7-8863-4cd41cc12261_tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5FW2EqiC/logs[0m