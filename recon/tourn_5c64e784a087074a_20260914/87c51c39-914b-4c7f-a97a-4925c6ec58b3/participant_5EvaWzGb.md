# Loki — task 87c51c39-914b-4c7f-a97a-4925c6ec58b3 — hotkey 5EvaWzGbtasB2yh6fev3fhdYF6vXzviPPijnh3SLRm2KDP8F
fetched 2026-09-19T05:08:44+00:00  lines=250  hit_page_cap=False  containers=['downloader-87c51c39-914b-4c7f-a97a-4925c6ec58b3-71e9caf7', 'downloader-87c51c39-914b-4c7f-a97a-4925c6ec58b3-a8daffe2', 'fastapi', 'text-trainer-75e417391c654f3b99f3d5b8195d944b', 'text-trainer-d70723f783ce4e93990dd3945b92a1d7']

[downloader-8] Downloading datasets to: /cache/datasets
[downloader-8] Downloading models to: /cache/models
[downloader-8] Model already cached at /cache/models/b254e84a30620233.
[downloader-8] Skipping download.
[downloader-8] Model path: /cache/models/b254e84a30620233
[downloader-8] Dataset path: /cache/datasets
[downloader-8] Downloading datasets to: /cache/datasets
[downloader-8] Downloading models to: /cache/models
[downloader-8] Model already cached at /cache/models/b254e84a30620233.
[downloader-8] Skipping download.
[downloader-8] Model path: /cache/models/b254e84a30620233
[downloader-8] Dataset path: /cache/datasets
[fastapi] Repository cloned successfully
[fastapi] Running Cache Download Container
[fastapi] Starting downloader container: downloader-87c51c39-914b-4c7f-a97a-4925c6ec58b3-a8daffe2
[fastapi] Download completed successfully for task 87c51c39-914b-4c7f-a97a-4925c6ec58b3
[fastapi] Building Docker image 'standalone-text-trainer:02ba51e6-5ec6-48ba-9129-cee2b433e0eb' (timeout=1800s)...
[fastapi] Step 1/9 : FROM axolotlai/axolotl:main-py3.11-cu124-2.5.1
[fastapi] ---> 69535f8df803
[fastapi] Step 2/9 : RUN apt-get update && apt-get install -y --no-install-recommends git curl && rm -rf /var/lib/apt/lists/*
[fastapi] ---> Running in 3f85b259a3be
[fastapi] Get:1 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  InRelease [1578 B]
[fastapi] Get:2 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  Packages [3009 kB]
[fastapi] Get:3 http://security.ubuntu.com/ubuntu jammy-security InRelease [129 kB]
[fastapi] Hit:4 http://archive.ubuntu.com/ubuntu jammy InRelease
[fastapi] Get:5 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [128 kB]
[fastapi] Get:6 http://security.ubuntu.com/ubuntu jammy-security/multiverse amd64 Packages [84.6 kB]
[fastapi] Get:7 http://security.ubuntu.com/ubuntu jammy-security/restricted amd64 Packages [7717 kB]
[fastapi] Get:8 http://archive.ubuntu.com/ubuntu jammy-backports InRelease [127 kB]
[fastapi] Get:9 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 Packages [4624 kB]
[fastapi] Get:10 http://security.ubuntu.com/ubuntu jammy-security/main amd64 Packages [4290 kB]
[fastapi] Get:11 http://security.ubuntu.com/ubuntu jammy-security/universe amd64 Packages [1317 kB]
[fastapi] Get:12 http://archive.ubuntu.com/ubuntu jammy-updates/restricted amd64 Packages [8007 kB]
[fastapi] Get:13 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 Packages [1620 kB]
[fastapi] Get:14 http://archive.ubuntu.com/ubuntu jammy-updates/multiverse amd64 Packages [93.2 kB]
[fastapi] Get:15 http://archive.ubuntu.com/ubuntu jammy-backports/universe amd64 Packages [35.6 kB]
[fastapi] Get:16 http://archive.ubuntu.com/ubuntu jammy-backports/main amd64 Packages [82.8 kB]
[fastapi] Fetched 31.3 MB in 3s (11.9 MB/s)
[fastapi] Reading package lists...
[fastapi] Reading package lists...
[fastapi] Building dependency tree...
[fastapi] Reading state information...
[fastapi] The following additional packages will be installed:
[fastapi] libcurl4
[fastapi] Suggested packages:
[fastapi] gettext-base git-daemon-run | git-daemon-sysvinit git-doc git-email git-gui
[fastapi] gitk gitweb git-cvs git-mediawiki git-svn
[fastapi] The following packages will be upgraded:
[fastapi] curl git libcurl4
[fastapi] 3 upgraded, 0 newly installed, 0 to remove and 127 not upgraded.
[fastapi] Need to get 3659 kB of archives.
[fastapi] After this operation, 2048 B of additional disk space will be used.
[fastapi] Get:1 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 curl amd64 7.81.0-1ubuntu1.27 [194 kB]
[fastapi] Get:2 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libcurl4 amd64 7.81.0-1ubuntu1.27 [292 kB]
[fastapi] Get:3 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 git amd64 1:2.34.1-1ubuntu1.17 [3174 kB]
[fastapi] [91mdebconf: delaying package configuration, since apt-utils is not installed
[fastapi] [0mFetched 3659 kB in 0s (7594 kB/s)
[fastapi] (Reading database ... (Reading database ... 5%(Reading database ... 10%(Reading database ... 15%(Reading database ... 20%(Reading database ... 25%(Reading database ... 30%(Reading database ... 35%(Reading database ... 40%(Reading database ... 45%(Reading database ... 50%(Reading database ... 55%(Reading database ... 60%(Reading database ... 65%(Reading database ... 70%(Reading database ... 75%(Reading database ... 80%(Reading database ... 85%(Reading database ... 90%(Reading database ... 95%(Reading database ... 100%(Reading database ... 19630 files and directories currently installed.)
[fastapi] Preparing to unpack .../curl_7.81.0-1ubuntu1.27_amd64.deb ...
[fastapi] Unpacking curl (7.81.0-1ubuntu1.27) over (7.81.0-1ubuntu1.20) ...
[fastapi] Preparing to unpack .../libcurl4_7.81.0-1ubuntu1.27_amd64.deb ...
[fastapi] Unpacking libcurl4:amd64 (7.81.0-1ubuntu1.27) over (7.81.0-1ubuntu1.20) ...
[fastapi] Preparing to unpack .../git_1%3a2.34.1-1ubuntu1.17_amd64.deb ...
[fastapi] Unpacking git (1:2.34.1-1ubuntu1.17) over (1:2.34.1-1ubuntu1.13) ...
[fastapi] Setting up git (1:2.34.1-1ubuntu1.17) ...
[fastapi] Setting up libcurl4:amd64 (7.81.0-1ubuntu1.27) ...
[fastapi] Setting up curl (7.81.0-1ubuntu1.27) ...
[fastapi] Processing triggers for libc-bin (2.35-0ubuntu3.6) ...
[fastapi] ---> e2fc7f94b747
[fastapi] Step 3/9 : RUN pip install --no-cache-dir huggingface_hub hf_transfer cryptography tenacity python-dotenv
[fastapi] ---> Running in d73878e3b743
[fastapi] Requirement already satisfied: huggingface_hub in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (0.32.2)
[fastapi] Requirement already satisfied: hf_transfer in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (0.1.9)
[fastapi] Requirement already satisfied: cryptography in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (44.0.3)
[fastapi] Collecting tenacity
[fastapi] Downloading tenacity-9.1.4-py3-none-any.whl.metadata (1.2 kB)
[fastapi] Requirement already satisfied: python-dotenv in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (1.0.1)
[fastapi] Requirement already satisfied: filelock in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from huggingface_hub) (3.18.0)
[fastapi] Requirement already satisfied: fsspec>=2023.5.0 in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from huggingface_hub) (2025.3.0)
[fastapi] Requirement already satisfied: packaging>=20.9 in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from huggingface_hub) (23.2)
[fastapi] Requirement already satisfied: pyyaml>=5.1 in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from huggingface_hub) (6.0.2)
[fastapi] Requirement already satisfied: requests in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from huggingface_hub) (2.32.4)
[fastapi] Requirement already satisfied: tqdm>=4.42.1 in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from huggingface_hub) (4.67.1)
[fastapi] Requirement already satisfied: typing-extensions>=3.7.4.3 in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from huggingface_hub) (4.14.1)
[fastapi] Requirement already satisfied: hf-xet<2.0.0,>=1.1.2 in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from huggingface_hub) (1.1.2)
[fastapi] Requirement already satisfied: cffi>=1.12 in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from cryptography) (1.17.1)
[fastapi] Requirement already satisfied: pycparser in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from cffi>=1.12->cryptography) (2.22)
[fastapi] Requirement already satisfied: charset_normalizer<4,>=2 in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from requests->huggingface_hub) (3.4.2)
[fastapi] Requirement already satisfied: idna<4,>=2.5 in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from requests->huggingface_hub) (3.10)
[fastapi] Requirement already satisfied: urllib3<3,>=1.21.1 in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from requests->huggingface_hub) (2.5.0)
[fastapi] Requirement already satisfied: certifi>=2017.4.17 in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from requests->huggingface_hub) (2025.6.15)
[fastapi] Downloading tenacity-9.1.4-py3-none-any.whl (28 kB)
[fastapi] Installing collected packages: tenacity
[fastapi] Successfully installed tenacity-9.1.4
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 25.1.1 -> 26.2.1
[fastapi] [notice] To update, run: pip install --upgrade pip
[fastapi] [0m ---> b34a23f626c2
[fastapi] Step 4/9 : RUN mkdir -p /workspace/scripts /app/checkpoints /cache
[fastapi] ---> Running in 074911033ed9
[fastapi] ---> dc4c3cad2f54
[fastapi] Step 5/9 : WORKDIR /workspace/scripts
[fastapi] ---> Running in d21a3f02b0b2
[fastapi] ---> 9b9430cdc908
[fastapi] Step 6/9 : COPY . /workspace/scripts
[fastapi] ---> 7209b6c55a91
[fastapi] Step 7/9 : RUN chmod +x /workspace/scripts/entrypoint.sh
[fastapi] ---> Running in 1f1bee6195b5
[fastapi] ---> 82994de39f35
[fastapi] Step 8/9 : ENV PYTHONPATH=/workspace/scripts
[fastapi] ---> Running in 7cbaaf2330f0
[fastapi] ---> 339ff6cd6b95
[fastapi] Step 9/9 : ENTRYPOINT ["/workspace/scripts/entrypoint.sh"]
[fastapi] ---> Running in be6fe995eb89
[fastapi] ---> ec77e8efe041
[fastapi] {'aux': {'ID': 'sha256:ec77e8efe04114059483cad583cbe818ffcfe6a6456bd17dc67496874718cf50'}}Successfully built ec77e8efe041
[fastapi] Successfully tagged standalone-text-trainer:02ba51e6-5ec6-48ba-9129-cee2b433e0eb
[fastapi] Docker image built successfully.
[fastapi] Container.wait() returned: {'StatusCode': 1}
[fastapi] Training container failed: OSError: [Errno 30] Read-only file system: '/cache/run'
[fastapi] Cleaning up
[fastapi] Cleaned up Docker resources.
[fastapi] Repository cloned successfully
[fastapi] Running Cache Download Container
[fastapi] Starting downloader container: downloader-87c51c39-914b-4c7f-a97a-4925c6ec58b3-71e9caf7
[fastapi] Download completed successfully for task 87c51c39-914b-4c7f-a97a-4925c6ec58b3
[fastapi] Building Docker image 'standalone-text-trainer:3835cc86-36ce-4d02-a292-09e8a5c3e6b1' (timeout=3600s)...
[fastapi] Step 1/9 : FROM axolotlai/axolotl:main-py3.11-cu124-2.5.1
[fastapi] ---> 69535f8df803
[fastapi] Step 2/9 : RUN apt-get update && apt-get install -y --no-install-recommends git curl && rm -rf /var/lib/apt/lists/*
[fastapi] ---> Running in 7c6b0771dfad
[fastapi] Get:1 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  InRelease [1578 B]
[fastapi] Get:2 http://security.ubuntu.com/ubuntu jammy-security InRelease [129 kB]
[fastapi] Hit:3 http://archive.ubuntu.com/ubuntu jammy InRelease
[fastapi] Get:4 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [128 kB]
[fastapi] Get:5 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  Packages [3009 kB]
[fastapi] Get:6 http://archive.ubuntu.com/ubuntu jammy-backports InRelease [127 kB]
[fastapi] Get:7 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 Packages [1620 kB]
[fastapi] Get:8 http://archive.ubuntu.com/ubuntu jammy-updates/multiverse amd64 Packages [93.2 kB]
[fastapi] Get:9 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 Packages [4624 kB]
[fastapi] Get:10 http://security.ubuntu.com/ubuntu jammy-security/universe amd64 Packages [1317 kB]
[fastapi] Get:11 http://archive.ubuntu.com/ubuntu jammy-updates/restricted amd64 Packages [8007 kB]
[fastapi] Get:12 http://archive.ubuntu.com/ubuntu jammy-backports/main amd64 Packages [82.8 kB]
[fastapi] Get:13 http://archive.ubuntu.com/ubuntu jammy-backports/universe amd64 Packages [35.6 kB]
[fastapi] Get:14 http://security.ubuntu.com/ubuntu jammy-security/main amd64 Packages [4290 kB]
[fastapi] Get:15 http://security.ubuntu.com/ubuntu jammy-security/restricted amd64 Packages [7717 kB]
[fastapi] Get:16 http://security.ubuntu.com/ubuntu jammy-security/multiverse amd64 Packages [84.6 kB]
[fastapi] Fetched 31.3 MB in 9s (3625 kB/s)
[fastapi] Reading package lists...
[fastapi] Reading package lists...
[fastapi] Building dependency tree...
[fastapi] Reading state information...
[fastapi] The following additional packages will be installed:
[fastapi] libcurl4
[fastapi] Suggested packages:
[fastapi] gettext-base git-daemon-run | git-daemon-sysvinit git-doc git-email git-gui
[fastapi] gitk gitweb git-cvs git-mediawiki git-svn
[fastapi] The following packages will be upgraded:
[fastapi] curl git libcurl4
[fastapi] 3 upgraded, 0 newly installed, 0 to remove and 127 not upgraded.
[fastapi] Need to get 3659 kB of archives.
[fastapi] After this operation, 2048 B of additional disk space will be used.
[fastapi] Get:1 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 curl amd64 7.81.0-1ubuntu1.27 [194 kB]
[fastapi] Get:2 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libcurl4 amd64 7.81.0-1ubuntu1.27 [292 kB]
[fastapi] Get:3 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 git amd64 1:2.34.1-1ubuntu1.17 [3174 kB]
[fastapi] [91mdebconf: delaying package configuration, since apt-utils is not installed
[fastapi] [0mFetched 3659 kB in 2s (2162 kB/s)
[fastapi] (Reading database ... (Reading database ... 5%(Reading database ... 10%(Reading database ... 15%(Reading database ... 20%(Reading database ... 25%(Reading database ... 30%(Reading database ... 35%(Reading database ... 40%(Reading database ... 45%(Reading database ... 50%(Reading database ... 55%(Reading database ... 60%(Reading database ... 65%(Reading database ... 70%(Reading database ... 75%(Reading database ... 80%(Reading database ... 85%(Reading database ... 90%(Reading database ... 95%(Reading database ... 100%(Reading database ... 19630 files and directories currently installed.)
[fastapi] Preparing to unpack .../curl_7.81.0-1ubuntu1.27_amd64.deb ...
[fastapi] Unpacking curl (7.81.0-1ubuntu1.27) over (7.81.0-1ubuntu1.20) ...
[fastapi] Preparing to unpack .../libcurl4_7.81.0-1ubuntu1.27_amd64.deb ...
[fastapi] Unpacking libcurl4:amd64 (7.81.0-1ubuntu1.27) over (7.81.0-1ubuntu1.20) ...
[fastapi] Preparing to unpack .../git_1%3a2.34.1-1ubuntu1.17_amd64.deb ...
[fastapi] Unpacking git (1:2.34.1-1ubuntu1.17) over (1:2.34.1-1ubuntu1.13) ...
[fastapi] Setting up git (1:2.34.1-1ubuntu1.17) ...
[fastapi] Setting up libcurl4:amd64 (7.81.0-1ubuntu1.27) ...
[fastapi] Setting up curl (7.81.0-1ubuntu1.27) ...
[fastapi] Processing triggers for libc-bin (2.35-0ubuntu3.6) ...
[fastapi] ---> 94978c218c8b
[fastapi] Step 3/9 : RUN pip install --no-cache-dir huggingface_hub hf_transfer cryptography tenacity python-dotenv
[fastapi] ---> Running in d2c28a330dd7
[fastapi] Requirement already satisfied: huggingface_hub in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (0.32.2)
[fastapi] Requirement already satisfied: hf_transfer in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (0.1.9)
[fastapi] Requirement already satisfied: cryptography in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (44.0.3)
[fastapi] Collecting tenacity
[fastapi] Downloading tenacity-9.1.4-py3-none-any.whl.metadata (1.2 kB)
[fastapi] Requirement already satisfied: python-dotenv in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (1.0.1)
[fastapi] Requirement already satisfied: filelock in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from huggingface_hub) (3.18.0)
[fastapi] Requirement already satisfied: fsspec>=2023.5.0 in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from huggingface_hub) (2025.3.0)
[fastapi] Requirement already satisfied: packaging>=20.9 in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from huggingface_hub) (23.2)
[fastapi] Requirement already satisfied: pyyaml>=5.1 in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from huggingface_hub) (6.0.2)
[fastapi] Requirement already satisfied: requests in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from huggingface_hub) (2.32.4)
[fastapi] Requirement already satisfied: tqdm>=4.42.1 in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from huggingface_hub) (4.67.1)
[fastapi] Requirement already satisfied: typing-extensions>=3.7.4.3 in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from huggingface_hub) (4.14.1)
[fastapi] Requirement already satisfied: hf-xet<2.0.0,>=1.1.2 in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from huggingface_hub) (1.1.2)
[fastapi] Requirement already satisfied: cffi>=1.12 in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from cryptography) (1.17.1)
[fastapi] Requirement already satisfied: pycparser in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from cffi>=1.12->cryptography) (2.22)
[fastapi] Requirement already satisfied: charset_normalizer<4,>=2 in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from requests->huggingface_hub) (3.4.2)
[fastapi] Requirement already satisfied: idna<4,>=2.5 in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from requests->huggingface_hub) (3.10)
[fastapi] Requirement already satisfied: urllib3<3,>=1.21.1 in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from requests->huggingface_hub) (2.5.0)
[fastapi] Requirement already satisfied: certifi>=2017.4.17 in /root/miniconda3/envs/py3.11/lib/python3.11/site-packages (from requests->huggingface_hub) (2025.6.15)
[fastapi] Downloading tenacity-9.1.4-py3-none-any.whl (28 kB)
[fastapi] Installing collected packages: tenacity
[fastapi] Successfully installed tenacity-9.1.4
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 25.1.1 -> 26.2.1
[fastapi] [notice] To update, run: pip install --upgrade pip
[fastapi] [0m ---> 47f64d410727
[fastapi] Step 4/9 : RUN mkdir -p /workspace/scripts /app/checkpoints /cache
[fastapi] ---> Running in 59e60ea15538
[fastapi] ---> a67adaf88469
[fastapi] Step 5/9 : WORKDIR /workspace/scripts
[fastapi] ---> Running in 51955a63cc28
[fastapi] ---> 8a16da28d3a6
[fastapi] Step 6/9 : COPY . /workspace/scripts
[fastapi] ---> c0ff4f2817a4
[fastapi] Step 7/9 : RUN chmod +x /workspace/scripts/entrypoint.sh
[fastapi] ---> Running in 3e3f5faf2ea6
[fastapi] ---> 6159397f74e8
[fastapi] Step 8/9 : ENV PYTHONPATH=/workspace/scripts
[fastapi] ---> Running in 28317a4fc080
[fastapi] ---> 872322664469
[fastapi] Step 9/9 : ENTRYPOINT ["/workspace/scripts/entrypoint.sh"]
[fastapi] ---> Running in d95a4f60c71b
[fastapi] ---> ec9697f7520d
[fastapi] {'aux': {'ID': 'sha256:ec9697f7520d54f32d332354e7ed753827816d0125cea844f9fa59433eb343b9'}}Successfully built ec9697f7520d
[fastapi] Successfully tagged standalone-text-trainer:3835cc86-36ce-4d02-a292-09e8a5c3e6b1
[fastapi] Docker image built successfully.
[fastapi] Container.wait() returned: {'StatusCode': 1}
[fastapi] Training container failed: OSError: [Errno 30] Read-only file system: '/cache/run'
[fastapi] Cleaning up
[fastapi] Cleaned up Docker resources.
[text-trainer] Traceback (most recent call last):
[text-trainer]   File "/workspace/scripts/train_text.py", line 344, in <module>
[text-trainer]     main()
[text-trainer]   File "/workspace/scripts/train_text.py", line 214, in main
[text-trainer]     os.makedirs(workdir, exist_ok=True)
[text-trainer]   File "<frozen os>", line 215, in makedirs
[text-trainer]   File "<frozen os>", line 225, in makedirs
[text-trainer] OSError: [Errno 30] Read-only file system: '/cache/run'
[text-trainer] Traceback (most recent call last):
[text-trainer]   File "/workspace/scripts/train_text.py", line 344, in <module>
[text-trainer]     main()
[text-trainer]   File "/workspace/scripts/train_text.py", line 214, in main
[text-trainer]     os.makedirs(workdir, exist_ok=True)
[text-trainer]   File "<frozen os>", line 215, in makedirs
[text-trainer]   File "<frozen os>", line 225, in makedirs
[text-trainer] OSError: [Errno 30] Read-only file system: '/cache/run'