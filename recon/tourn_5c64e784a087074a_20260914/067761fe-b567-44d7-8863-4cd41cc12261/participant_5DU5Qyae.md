# Loki — task 067761fe-b567-44d7-8863-4cd41cc12261 — hotkey 5DU5Qyae6n5c3PCDY7EBidC8FaZZCb1ykTMAF2JCXm63oQcf
fetched 2026-09-19T05:02:11+00:00  lines=2000  hit_page_cap=False  containers=['downloader-067761fe-b567-44d7-8863-4cd41cc12261-7b3f6528', 'fastapi', 'hf-upload-6e657f07b31f4457bf17b5f6f50b8782', 'text-trainer-25909a293c5c42ab8e11615564b3e5ae']

[downloader-0] Downloading datasets to: /cache/datasets
[downloader-0] Downloading models to: /cache/models
[downloader-0] Model already cached at /cache/models/c53e93d87a4fe77f.
[downloader-0] Skipping download.
[downloader-0] Model path: /cache/models/c53e93d87a4fe77f
[downloader-0] Dataset path: /cache/datasets
[fastapi] Repository cloned successfully
[fastapi] Running Cache Download Container
[fastapi] Starting downloader container: downloader-067761fe-b567-44d7-8863-4cd41cc12261-7b3f6528
[fastapi] Download completed successfully for task 067761fe-b567-44d7-8863-4cd41cc12261
[fastapi] Building Docker image 'standalone-text-trainer:9575fdea-bce4-47c8-aeef-9cf8a82704c3' (timeout=1800s)...
[fastapi] Step 1/13 : FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04
[fastapi] ---> ff5fe688608b
[fastapi] Step 2/13 : ENV DEBIAN_FRONTEND=noninteractive     PIP_NO_CACHE_DIR=1     MAX_JOBS=8
[fastapi] ---> Running in 6544eac1f2fd
[fastapi] ---> 3946d24f03f0
[fastapi] Step 3/13 : RUN mkdir -p /app/checkpoints /cache /workspace
[fastapi] ---> Running in 63350b5f7f97
[fastapi] ---> 2772404e51a9
[fastapi] Step 4/13 : WORKDIR /workspace
[fastapi] ---> Running in c387d7081ff8
[fastapi] ---> 1834e4e1a883
[fastapi] Step 5/13 : RUN pip install -U pip packaging==23.2 setuptools==75.8.0 wheel ninja uv &&     uv pip install --system         transformers==4.51.3 trl==0.18.0 peft==0.15.1 accelerate==1.6.0         deepspeed==0.15.4 bitsandbytes==0.45.4 datasets==3.5.0         liger-kernel==0.5.9 sentencepiece tiktoken==0.9.0 tenacity==9.1.2 &&     (pip install https://github.com/Dao-AILab/flash-attention/releases/download/v2.7.4.post1/flash_attn-2.7.4.post1+cu12torch2.4cxx11abiFALSE-cp311-cp311-linux_x86_64.whl      || pip install flash-attn==2.7.4.post1 --no-build-isolation) &&     uv pip install --system vllm==0.8.3 &&     rm -rf /root/.cache/uv /root/.cache/pip
[fastapi] ---> Running in c5507a3f1c38
[fastapi] Requirement already satisfied: pip in /usr/local/lib/python3.11/dist-packages (24.2)
[fastapi] Collecting pip
[fastapi] Downloading pip-26.2.1-py3-none-any.whl.metadata (4.6 kB)
[fastapi] Collecting packaging==23.2
[fastapi] Downloading packaging-23.2-py3-none-any.whl.metadata (3.2 kB)
[fastapi] Collecting setuptools==75.8.0
[fastapi] Downloading setuptools-75.8.0-py3-none-any.whl.metadata (6.7 kB)
[fastapi] Requirement already satisfied: wheel in /usr/local/lib/python3.11/dist-packages (0.44.0)
[fastapi] Collecting wheel
[fastapi] Downloading wheel-0.48.0-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Collecting ninja
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (5.4 kB)
[fastapi] Collecting uv
[fastapi] Downloading uv-0.12.14-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] INFO: pip is looking at multiple versions of wheel to determine which version is compatible with other requirements. This could take a while.
[fastapi] Collecting wheel
[fastapi] Downloading wheel-0.47.0-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Downloading wheel-0.46.3-py3-none-any.whl.metadata (2.4 kB)
[fastapi] Downloading wheel-0.46.2-py3-none-any.whl.metadata (2.4 kB)
[fastapi] Downloading wheel-0.45.1-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Downloading packaging-23.2-py3-none-any.whl (53 kB)
[fastapi] Downloading setuptools-75.8.0-py3-none-any.whl (1.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 261.8 MB/s eta 0:00:00
[fastapi] Downloading pip-26.2.1-py3-none-any.whl (1.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 818.4 MB/s eta 0:00:00
[fastapi] Downloading wheel-0.45.1-py3-none-any.whl (72 kB)
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (183 kB)
[fastapi] Downloading uv-0.12.14-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.0 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 20.0/20.0 MB 826.6 MB/s eta 0:00:00
[fastapi] Installing collected packages: wheel, uv, setuptools, pip, packaging, ninja
[fastapi] Attempting uninstall: wheel
[fastapi] Found existing installation: wheel 0.44.0
[fastapi] Uninstalling wheel-0.44.0:
[fastapi] Successfully uninstalled wheel-0.44.0
[fastapi] Attempting uninstall: setuptools
[fastapi] Found existing installation: setuptools 75.1.0
[fastapi] Uninstalling setuptools-75.1.0:
[fastapi] Successfully uninstalled setuptools-75.1.0
[fastapi] Attempting uninstall: pip
[fastapi] Found existing installation: pip 24.2
[fastapi] Uninstalling pip-24.2:
[fastapi] Successfully uninstalled pip-24.2
[fastapi] Attempting uninstall: packaging
[fastapi] Found existing installation: packaging 24.1
[fastapi] Uninstalling packaging-24.1:
[fastapi] Successfully uninstalled packaging-24.1
[fastapi] Successfully installed ninja-1.13.2 packaging-23.2 pip-26.2.1 setuptools-75.8.0 uv-0.12.14 wheel-0.45.1
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91mUsing Python 3.11.10 environment at: /usr
[fastapi] [0m[91mResolved 71 packages in 1.31s
[fastapi] [0m[91m   Building deepspeed==0.15.4
[fastapi] [0m[91mDownloading sentencepiece (1.3MiB)
[fastapi] [0m[91mDownloading hf-xet (4.3MiB)
[fastapi] [0m[91mDownloading pyarrow (47.7MiB)
[fastapi] [0m[91mDownloading pandas (10.8MiB)
[fastapi] [0m[91mDownloading pydantic-core (2.0MiB)
[fastapi] [0m[91mDownloading bitsandbytes (72.5MiB)
[fastapi] [0m[91mDownloading tiktoken (1.1MiB)
[fastapi] [0m[91mDownloading tokenizers (3.0MiB)
[fastapi] [0m[91mDownloading transformers (9.9MiB)
[fastapi] [0m[91mDownloading aiohttp (1.7MiB)
[fastapi] [0m[91m Downloaded tiktoken
[fastapi] [0m[91m Downloaded sentencepiece
[fastapi] [0m[91m Downloaded aiohttp
[fastapi] [0m[91m Downloaded pydantic-core
[fastapi] [0m[91m Downloaded tokenizers
[fastapi] [0m[91m Downloaded hf-xet
[fastapi] [0m[91m Downloaded transformers
[fastapi] [0m[91m Downloaded pandas
[fastapi] [0m[91m Downloaded pyarrow
[fastapi] [0m[91m Downloaded bitsandbytes
[fastapi] [0m[91m      Built deepspeed==0.15.4
[fastapi] [0m[91mPrepared 38 packages in 813ms
[fastapi] [0m[91mUninstalled 1 package in 17ms
[fastapi] [0m[91mInstalled 38 packages in 40ms
[fastapi] [0m[91m + accelerate==1.6.0
[fastapi] + aiohappyeyeballs==2.7.[0m[91m1
[fastapi] + aiohttp==[0m[91m3.14.3
[fastapi] +[0m[91m [0m[91maiosignal==1[0m[91m.4.0
[fastapi] + annotated-types==0.[0m[91m8.0[0m[91m
[fastapi] [0m[91m+[0m[91m bitsandbytes==0.45.4
[fastapi] + datasets==3[0m[91m.5.0
[fastapi] + deepspeed==0.15.4
[fastapi] [0m[91m+ dill==0.3.[0m[91m8
[fastapi] + frozenlist==[0m[91m1.8.0[0m[91m
[fastapi] + hf-xet[0m[91m==1.6.0
[fastapi] [0m[91m + hjson[0m[91m==3.[0m[91m1.0
[fastapi] +[0m[91m huggingface-hub==0.36.[0m[91m2
[fastapi] +[0m[91m liger-kernel==[0m[91m0.5.9[0m[91m
[fastapi] + [0m[91mmsgpack==1[0m[91m.2.2
[fastapi] + multidict==6.8.[0m[91m0
[fastapi] + multiprocess==0.70.16
[fastapi] + pandas==3.0[0m[91m.5
[fastapi] + peft[0m[91m==0.15.[0m[91m1
[fastapi] + [0m[91mpropcache==0.[0m[91m5.2
[fastapi] + py-cpuinfo==[0m[91m9.0.0[0m[91m
[fastapi] + [0m[91mpyarrow==25.0[0m[91m.1
[fastapi] [0m[91m+ pydantic==[0m[91m2.13.5
[fastapi] + [0m[91mpydantic-core==2.46.5[0m[91m
[fastapi] + [0m[91mregex==2026.9.[0m[91m10
[fastapi] + safetensors[0m[91m==0.8.[0m[91m0
[fastapi] +[0m[91m sentencepiece==0.[0m[91m2.2
[fastapi] [0m[91m + [0m[91msix==1.[0m[91m17.0
[fastapi] [0m[91m+ tenacity[0m[91m==9.[0m[91m1.2
[fastapi] + tiktoken[0m[91m==0.9.0[0m[91m
[fastapi] + [0m[91mtokenizers[0m[91m==0.21.[0m[91m4
[fastapi] + [0m[91mtqdm==4.70.1
[fastapi] + transformers[0m[91m==4.51.3
[fastapi] +[0m[91m trl[0m[91m==0[0m[91m.18.0
[fastapi] -[0m[91m typing-extensions==4.9[0m[91m.0
[fastapi] [0m[91m+ [0m[91mtyping-extensions==4.16.0
[fastapi] [0m[91m+ typing-inspection==0.4.[0m[91m4
[fastapi] [0m[91m + [0m[91mxxhash==4.0.1
[fastapi] + [0m[91myarl[0m[91m==1.[0m[91m24.5[0m[91m
[fastapi] [0mCollecting flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse
[fastapi] Downloading flash_attn-2.7.4.post1+cu12torch2.4cxx11abiFALSE-cp311-cp311-linux_x86_64.whl (187.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 187.8/187.8 MB 475.7 MB/s  0:00:00
[fastapi] Requirement already satisfied: torch in /usr/local/lib/python3.11/dist-packages (from flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse) (2.4.1+cu124)
[fastapi] Collecting einops (from flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse)
[fastapi] Downloading einops-0.8.2-py3-none-any.whl.metadata (13 kB)
[fastapi] Requirement already satisfied: filelock in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse) (3.13.1)
[fastapi] Requirement already satisfied: typing-extensions>=4.8.0 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse) (4.16.0)
[fastapi] Requirement already satisfied: sympy in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse) (1.12)
[fastapi] Requirement already satisfied: networkx in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse) (3.2.1)
[fastapi] Requirement already satisfied: jinja2 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse) (3.1.3)
[fastapi] Requirement already satisfied: fsspec in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse) (2024.2.0)
[fastapi] Requirement already satisfied: nvidia-cuda-nvrtc-cu12==12.4.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse) (12.4.99)
[fastapi] Requirement already satisfied: nvidia-cuda-runtime-cu12==12.4.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse) (12.4.99)
[fastapi] Requirement already satisfied: nvidia-cuda-cupti-cu12==12.4.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse) (12.4.99)
[fastapi] Requirement already satisfied: nvidia-cudnn-cu12==9.1.0.70 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse) (9.1.0.70)
[fastapi] Requirement already satisfied: nvidia-cublas-cu12==12.4.2.65 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse) (12.4.2.65)
[fastapi] Requirement already satisfied: nvidia-cufft-cu12==11.2.0.44 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse) (11.2.0.44)
[fastapi] Requirement already satisfied: nvidia-curand-cu12==10.3.5.119 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse) (10.3.5.119)
[fastapi] Requirement already satisfied: nvidia-cusolver-cu12==11.6.0.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse) (11.6.0.99)
[fastapi] Requirement already satisfied: nvidia-cusparse-cu12==12.3.0.142 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse) (12.3.0.142)
[fastapi] Requirement already satisfied: nvidia-nccl-cu12==2.20.5 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse) (2.20.5)
[fastapi] Requirement already satisfied: nvidia-nvtx-cu12==12.4.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse) (12.4.99)
[fastapi] Requirement already satisfied: nvidia-nvjitlink-cu12==12.4.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse) (12.4.99)
[fastapi] Requirement already satisfied: triton==3.0.0 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse) (3.0.0)
[fastapi] Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.11/dist-packages (from jinja2->torch->flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse) (2.1.5)
[fastapi] Requirement already satisfied: mpmath>=0.19 in /usr/local/lib/python3.11/dist-packages (from sympy->torch->flash-attn==2.7.4.post1+cu12torch2.4cxx11abifalse) (1.3.0)
[fastapi] Downloading einops-0.8.2-py3-none-any.whl (65 kB)
[fastapi] Installing collected packages: einops, flash-attn
[fastapi] Successfully installed einops-0.8.2 flash-attn-2.7.4.post1
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91mUsing Python 3.11.10 environment at: /usr
[fastapi] [0m[91mResolved 142 packages in 307ms
[fastapi] [0m[91mDownloading xformers (42.2MiB)
[fastapi] [0m[91mDownloading torch (731.2MiB)
[fastapi] [0m[91mDownloading scipy (34.2MiB)
[fastapi] [0m[91mDownloading nvidia-cusparse-cu12 (197.8MiB)
[fastapi] [0m[91mDownloading llvmlite (40.4MiB)
[fastapi] [0m[91mDownloading pycountry (7.7MiB)
[fastapi] [0m[91mDownloading opencv-python-headless (47.7MiB)
[fastapi] [0m[91mDownloading nvidia-cusolver-cu12 (122.0MiB)
[fastapi] [0m[91mDownloading nvidia-nccl-cu12 (179.9MiB)
[fastapi] [0m[91mDownloading nvidia-cusparselt-cu12 (143.1MiB)
[fastapi] [0m[91mDownloading triton (241.4MiB)
[fastapi] [0m[91mDownloading nvidia-cublas-cu12 (346.6MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-nvrtc-cu12 (23.5MiB)
[fastapi] [0m[91mDownloading torchvision (6.9MiB)
[fastapi] [0m[91mDownloading xgrammar (4.1MiB)
[fastapi] [0m[91mDownloading torchaudio (3.2MiB)
[fastapi] [0m[91mDownloading llguidance (14.3MiB)
[fastapi] [0m[91mDownloading nvidia-cufft-cu12 (201.7MiB)
[fastapi] [0m[91mDownloading ray (74.7MiB)
[fastapi] [0m[91mDownloading mistral-common (6.2MiB)
[fastapi] [0m[91mDownloading[0m[91m pillow (6.6MiB)
[fastapi] [0m[91mDownloading uvloop (3.6MiB)
[fastapi] [0m[91mDownloading openai (1.9MiB)
[fastapi] [0m[91mDownloading vllm (280.4MiB)
[fastapi] [0m[91mDownloading numba (3.6MiB)
[fastapi] [0m[91mDownloading sympy (5.9MiB)
[fastapi] [0m[91mDownloading nvidia-curand-cu12 (53.7MiB)
[fastapi] [0m[91mDownloading nvidia-nvjitlink-cu12 (20.1MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-cupti-cu12 (13.2MiB)
[fastapi] [0m[91mDownloading cupy-cuda12x (107.8MiB)
[fastapi] [0m[91m Downloaded openai
[fastapi] [0m[91m Downloaded torchaudio
[fastapi] [0m[91m Downloaded numba
[fastapi] [0m[91m Downloaded uvloop
[fastapi] [0m[91m Downloaded xgrammar
[fastapi] [0m[91m Downloaded sympy
[fastapi] [0m[91m Downloaded mistral-common
[fastapi] [0m[91m Downloaded pillow
[fastapi] [0m[91m Downloaded torchvision
[fastapi] [0m[91m Downloaded pycountry
[fastapi] [0m[91m Downloaded nvidia-cuda-cupti-cu12
[fastapi] [0m[91m Downloaded llguidance
[fastapi] [0m[91m Downloaded nvidia-nvjitlink-cu12
[fastapi] [0m[91m Downloaded nvidia-cuda-nvrtc-cu12
[fastapi] [0m[91m Downloaded scipy
[fastapi] [0m[91m Downloaded llvmlite
[fastapi] [0m[91m Downloaded xformers
[fastapi] [0m[91m Downloaded opencv-python-headless
[fastapi] [0m[91m Downloaded nvidia-curand-cu12
[fastapi] [0m[91m Downloaded ray
[fastapi] [0m[91m Downloaded cupy-cuda12x
[fastapi] [0m[91m Downloaded nvidia-cusolver-cu12
[fastapi] [0m[91m Downloaded nvidia-cusparselt-cu12
[fastapi] [0m[91m Downloaded nvidia-nccl-cu12
[fastapi] [0m[91m Downloaded nvidia-cusparse-cu12
[fastapi] [0m[91m Downloaded nvidia-cufft-cu12
[fastapi] [0m[91m Downloaded triton
[fastapi] [0m[91m Downloaded vllm
[fastapi] [0m[91m Downloaded nvidia-cublas-cu12
[fastapi] [0m[91m Downloaded torch
[fastapi] [0m[91mPrepared 92 packages in 7.68s
[fastapi] [0m[91mUninstalled 24 packages in 1.35s
[fastapi] [0m[91mInstalled 92 packages in 219ms
[fastapi] [0m[91m + agent-detector==2.0.0
[fastapi] + airportsdata==20260905
[fastapi] + annotated-doc==0.0.5
[fastapi] - anyio==4.6.0
[fastapi] + anyio==4.15.1
[fastapi] + astor[0m[91m==0.8.1
[fastapi] + blake3==1.0.9
[fastapi] + cachetools[0m[91m==7.1.8[0m[91m
[fastapi] [0m[91m + click[0m[91m==8.5.0
[fastapi] + [0m[91mcloudpickle==3.1.[0m[91m2
[fastapi] + [0m[91mcompressed-tensors==0.9.2
[fastapi] + cupy-cuda12x==[0m[91m13.6.0
[fastapi] + depyf==0.18.0
[fastapi] + detect-installer[0m[91m==0.2.[0m[91m1
[fastapi] + diskcache[0m[91m==5.6.3
[fastapi] [0m[91m + dnspython[0m[91m==2.8.0[0m[91m
[fastapi] + email-validator==2[0m[91m.3.0
[fastapi] [0m[91m+ fastapi[0m[91m==0.[0m[91m141.1[0m[91m
[fastapi] [0m[91m+ fastapi-cli[0m[91m==0.0[0m[91m.32[0m[91m
[fastapi] + [0m[91mfastapi-cloud-cli[0m[91m==0.[0m[91m26.0
[fastapi] +[0m[91m [0m[91mfastar==0[0m[91m.12.0[0m[91m
[fastapi] [0m[91m + [0m[91mfastrlock[0m[91m==0.8.3
[fastapi] - [0m[91mfilelock==3[0m[91m.13.1[0m[91m
[fastapi] + [0m[91mfilelock==[0m[91m3.32[0m[91m.6[0m[91m
[fastapi] +[0m[91m [0m[91mgguf==0[0m[91m.[0m[91m10.0
[fastapi] [0m[91m- h11==0.14[0m[91m.0
[fastapi] + [0m[91mh11==0[0m[91m.16.0[0m[91m
[fastapi] [0m[91m - httpcore[0m[91m==1.0.5
[fastapi] + httpcore[0m[91m==1.0[0m[91m.9[0m[91m
[fastapi] +[0m[91m [0m[91mhttpcore2==2[0m[91m.13[0m[91m.0
[fastapi] [0m[91m+ httptools==0.8.0
[fastapi] [0m[91m+ httpx2==2.[0m[91m13[0m[91m.0
[fastapi] [0m[91m - idna==3.10
[fastapi] + idna[0m[91m==3.19[0m[91m
[fastapi] [0m[91m+ importlib-metadata[0m[91m==9.0.1
[fastapi] + interegular==[0m[91m0.3.3
[fastapi] - jinja2==[0m[91m3.1.3
[fastapi] [0m[91m+ jinja2==3.[0m[91m1.6
[fastapi] + jiter[0m[91m==0.17.[0m[91m0
[fastapi] [0m[91m+ [0m[91mlark==1.2.2
[fastapi] + llguidance==0.7[0m[91m.30
[fastapi] +[0m[91m llvmlite[0m[91m==0.44.0
[fastapi] + lm-format-enforcer[0m[91m==0.10.[0m[91m12
[fastapi] +[0m[91m [0m[91mmarkdown-it-py==[0m[91m4.2.[0m[91m0[0m[91m
[fastapi] +[0m[91m mdurl[0m[91m==0.1[0m[91m.[0m[91m2
[fastapi] [0m[91m+ mistral-common[0m[91m==1.11.[0m[91m7
[fastapi] + msgspec==0.21[0m[91m.1
[fastapi] + nanobind[0m[91m==3.0.1
[fastapi] +[0m[91m numba==[0m[91m0.[0m[91m61.0
[fastapi] [0m[91m [0m[91m- [0m[91mnvidia-cublas-cu12==[0m[91m12.4.2.65
[fastapi] + nvidia-cublas-cu12==12.4.[0m[91m5.8
[fastapi] -[0m[91m nvidia-cuda-cupti-cu12[0m[91m==12.4.99
[fastapi] [0m[91m +[0m[91m [0m[91mnvidia-cuda-cupti-cu12==12[0m[91m.4[0m[91m.127[0m[91m
[fastapi] [0m[91m- [0m[91mnvidia-cuda-nvrtc-cu12==[0m[91m12.4[0m[91m.99
[fastapi] [0m[91m [0m[91m+ nvidia-cuda-nvrtc-cu12[0m[91m==12.4[0m[91m.127[0m[91m
[fastapi] [0m[91m- [0m[91mnvidia-cuda-runtime-cu12[0m[91m==12.[0m[91m4.99
[fastapi] [0m[91m +[0m[91m [0m[91mnvidia-cuda-runtime-cu12==[0m[91m12.4.[0m[91m127[0m[91m
[fastapi] [0m[91m- nvidia-cufft-cu12[0m[91m==[0m[91m11[0m[91m.2.0.[0m[91m44[0m[91m
[fastapi] [0m[91m+ nvidia-cufft-cu12[0m[91m==[0m[91m11.2[0m[91m.1.[0m[91m3[0m[91m
[fastapi] [0m[91m-[0m[91m nvidia-curand-cu12[0m[91m==10.3[0m[91m.5[0m[91m.119
[fastapi] [0m[91m+ nvidia-curand-cu12==10.3.5.147[0m[91m
[fastapi] -[0m[91m nvidia-cusolver-cu12==11.6.0[0m[91m.99
[fastapi] + nvidia-cusolver-cu12[0m[91m==11.6.1.9[0m[91m
[fastapi] - nvidia-cusparse-cu12[0m[91m==12.3.0[0m[91m.142
[fastapi] +[0m[91m nvidia-cusparse-cu12==12[0m[91m.3.1.170[0m[91m
[fastapi] + [0m[91mnvidia-cusparselt-cu12==0.[0m[91m6.2
[fastapi] [0m[91m- nvidia-nccl-cu12==[0m[91m2.20.5
[fastapi] + [0m[91mnvidia-nccl-cu12==2.21.5
[fastapi] -[0m[91m nvidia-nvjitlink-cu12[0m[91m==12.4.99[0m[91m
[fastapi] + nvidia-nvjitlink-cu12[0m[91m==12.4.127
[fastapi] - nvidia-nvtx-cu12==12.4[0m[91m.99
[fastapi] +[0m[91m nvidia-nvtx-cu12==12.[0m[91m4.127
[fastapi] + openai==3.14[0m[91m.0
[fastapi] +[0m[91m [0m[91mopencv-python-headless==[0m[91m4.11.[0m[91m0[0m[91m.86
[fastapi] +[0m[91m outlines==0.1.11
[fastapi] + outlines-core==0[0m[91m.1.26
[fastapi] [0m[91m- packaging==23[0m[91m.2
[fastapi] + [0m[91mpackaging==26.3
[fastapi] + partial-json-parser==0.2.[0m[91m1.1.post[0m[91m7
[fastapi] - pillow[0m[91m==10.2.0
[fastapi] + pillow==12.[0m[91m3.0
[fastapi] + prometheus-fastapi-instrumentator==8.1.0
[fastapi] + protobuf[0m[91m==7.36.1
[fastapi] [0m[91m + pycountry[0m[91m==26.2[0m[91m.16
[fastapi] + [0m[91mpydantic-extra-types==2.11.1[0m[91m
[fastapi] + pydantic-settings==[0m[91m2.15.0
[fastapi] [0m[91m + python-dotenv[0m[91m==1.2.3[0m[91m
[fastapi] + [0m[91mpython-multipart==0.0[0m[91m.32
[fastapi] [0m[91m+ ray==[0m[91m2.58.0[0m[91m
[fastapi] + [0m[91mrich==15.0[0m[91m.0
[fastapi] + rich-toolkit==[0m[91m0.20.5
[fastapi] [0m[91m+ [0m[91mrignore==0.8.1[0m[91m
[fastapi] + scipy==1.16.3
[fastapi] [0m[91m + sentry-sdk==2.69.[0m[91m1
[fastapi] [0m[91m [0m[91m+ shellingham==1.5.4
[fastapi] +[0m[91m starlette==1.6[0m[91m.0
[fastapi] -[0m[91m [0m[91msympy==1.12[0m[91m
[fastapi] +[0m[91m sympy[0m[91m==[0m[91m1.13.[0m[91m1[0m[91m
[fastapi] -[0m[91m torch[0m[91m==2.4.1+cu124
[fastapi] [0m[91m+ torch==2.6[0m[91m.0[0m[91m
[fastapi] -[0m[91m torchaudio==2.4.1+cu124
[fastapi] + [0m[91mtorchaudio==2.6.0
[fastapi] - torchvision[0m[91m==0.19[0m[91m.1+cu124[0m[91m
[fastapi] +[0m[91m [0m[91mtorchvision==0[0m[91m.21.[0m[91m0
[fastapi] [0m[91m [0m[91m- triton[0m[91m==[0m[91m3.0[0m[91m.0
[fastapi] [0m[91m+[0m[91m triton[0m[91m==3.[0m[91m2.[0m[91m0
[fastapi] [0m[91m+ [0m[91mtruststore[0m[91m==0.[0m[91m10.4[0m[91m
[fastapi] [0m[91m+[0m[91m typer[0m[91m==0.27.2
[fastapi] [0m[91m+ uvicorn==[0m[91m0.53.[0m[91m0[0m[91m
[fastapi] [0m[91m+ uvloop==0[0m[91m.22.1
[fastapi] + vllm==0.[0m[91m8.3
[fastapi] + watchfiles==1[0m[91m.2.0[0m[91m
[fastapi] [0m[91m+ websockets==17[0m[91m.[0m[91m1
[fastapi] + xformers==0.0.29.post2[0m[91m
[fastapi] + xgrammar==0.1.[0m[91m17
[fastapi] + zipp==[0m[91m4.1.0
[fastapi] [0m ---> 65f471a204b0
[fastapi] Step 6/13 : RUN python -m venv /opt/axo &&     /opt/axo/bin/pip install -U pip packaging==23.2 setuptools==75.8.0 wheel ninja uv &&     /opt/axo/bin/uv pip install --python /opt/axo/bin/python --no-build-isolation axolotl==0.9.1 &&     rm -rf /root/.cache/uv /root/.cache/pip
[fastapi] ---> Running in d187d15fc827
[fastapi] Requirement already satisfied: pip in /opt/axo/lib/python3.11/site-packages (24.0)
[fastapi] Collecting pip
[fastapi] Downloading pip-26.2.1-py3-none-any.whl.metadata (4.6 kB)
[fastapi] Collecting packaging==23.2
[fastapi] Downloading packaging-23.2-py3-none-any.whl.metadata (3.2 kB)
[fastapi] Collecting setuptools==75.8.0
[fastapi] Downloading setuptools-75.8.0-py3-none-any.whl.metadata (6.7 kB)
[fastapi] Collecting wheel
[fastapi] Downloading wheel-0.48.0-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Collecting ninja
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (5.4 kB)
[fastapi] Collecting uv
[fastapi] Downloading uv-0.12.14-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] INFO: pip is looking at multiple versions of wheel to determine which version is compatible with other requirements. This could take a while.
[fastapi] Collecting wheel
[fastapi] Downloading wheel-0.47.0-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Downloading wheel-0.46.3-py3-none-any.whl.metadata (2.4 kB)
[fastapi] Downloading wheel-0.46.2-py3-none-any.whl.metadata (2.4 kB)
[fastapi] Downloading wheel-0.45.1-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Downloading packaging-23.2-py3-none-any.whl (53 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 53.0/53.0 kB 10.1 MB/s eta 0:00:00
[fastapi] Downloading setuptools-75.8.0-py3-none-any.whl (1.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 64.3 MB/s eta 0:00:00
[fastapi] Downloading pip-26.2.1-py3-none-any.whl (1.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 180.1 MB/s eta 0:00:00
[fastapi] Downloading wheel-0.45.1-py3-none-any.whl (72 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 72.5/72.5 kB 399.2 MB/s eta 0:00:00
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (183 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 183.4/183.4 kB 462.5 MB/s eta 0:00:00
[fastapi] Downloading uv-0.12.14-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.0 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 20.0/20.0 MB 324.9 MB/s eta 0:00:00
[fastapi] Installing collected packages: wheel, uv, setuptools, pip, packaging, ninja
[fastapi] Attempting uninstall: setuptools
[fastapi] Found existing installation: setuptools 65.5.0
[fastapi] Uninstalling setuptools-65.5.0:
[fastapi] Successfully uninstalled setuptools-65.5.0
[fastapi] Attempting uninstall: pip
[fastapi] Found existing installation: pip 24.0
[fastapi] Uninstalling pip-24.0:
[fastapi] Successfully uninstalled pip-24.0
[fastapi] Successfully installed ninja-1.13.2 packaging-23.2 pip-26.2.1 setuptools-75.8.0 uv-0.12.14 wheel-0.45.1
[fastapi] [91mUsing Python 3.11.10 environment at: /opt/axo
[fastapi] [0m[91mResolved 217 packages in 1.32s
[fastapi] [0m[91mDownloading pygments (1.2MiB)
[fastapi] [0m[91mDownloading networkx (2.0MiB)
[fastapi] [0m[91mDownloading cryptography (4.5MiB)
[fastapi] [0m[91mDownloading lm-eval (2.4MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-cupti-cu12 (13.2MiB)
[fastapi] [0m[91mDownloading xformers (42.2MiB)
[fastapi] [0m[91mDownloading pillow (6.3MiB)
[fastapi] [0m[91mDownloading numpy (18.6MiB)
[fastapi] [0m[91mDownloading lxml (5.0MiB)
[fastapi] [0m[91mDownloading nvidia-cufft-cu12 (201.7MiB)
[fastapi] [0m[91mDownloading zstandard (5.2MiB)
[fastapi] [0m[91mDownloading transformers (9.9MiB)
[fastapi] [0m[91mDownloading nvidia-nvjitlink-cu12 (20.1MiB)
[fastapi] [0m[91mDownloading pydantic-core (1.9MiB)
[fastapi] [0m[91mDownloading gradio (44.3MiB)
[fastapi] [0m[91mDownloading nltk (1.7MiB)
[fastapi] [0m[91mDownloading botocore (13.7MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-nvrtc-cu12 (23.5MiB)
[fastapi] [0m[91mDownloading nvidia-cusparse-cu12 (197.8MiB)
[fastapi] [0m[91mDownloading tensorboard (5.3MiB)
[fastapi] [0m[91mDownloading torch (731.2MiB)
[fastapi] [0m[91mDownloading nvidia-cusolver-cu12 (122.0MiB)
[fastapi] [0m[91mDownloading aiohttp (1.7MiB)
[fastapi] [0m[91mDownloading grpcio (6.9MiB)
[fastapi] [0m[91mDownloading nvidia-nccl-cu12 (179.9MiB)
[fastapi] [0m[91mDownloading sympy (5.9MiB)
[fastapi] [0m[91mDownloading scikit-learn (11.6MiB)
[fastapi] [0m[91mDownloading oci (35.2MiB)
[fastapi] [0m[91mDownloading bitsandbytes (72.5MiB)
[fastapi] [0m[91mDownloading llvmlite (57.1MiB)
[fastapi] [0m[91mDownloading scipy (33.7MiB)
[fastapi] [0m[91mDownloading pyarrow (47.7MiB)
[fastapi] [0m[91mDownloading tensorboard-data-server (6.3MiB)
[fastapi] [0m[91mDownloading triton (241.4MiB)
[fastapi] [0m[91mDownloading numba (3.6MiB)
[fastapi] [0m[91mDownloading hf-xet (51.1MiB)
[fastapi] [0m[91mDownloading nvidia-curand-cu12 (53.7MiB)
[fastapi] [0m[91mDownloading pandas (12.2MiB)
[fastapi] [0m[91mDownloading ruff (9.9MiB)
[fastapi] [0m[91mDownloading wandb (24.9MiB)
[fastapi] [0m[91mDownloading torchao (5.4MiB)
[fastapi] [0m[91mDownloading nvidia-cusparselt-cu12 (143.1MiB)
[fastapi] [0m[91mDownloading nvidia-cudnn-cu12 (634.0MiB)
[fastapi] [0m[91mDownloading hf-transfer (3.4MiB)
[fastapi] [0m[91mDownloading sentencepiece (1.3MiB)
[fastapi] [0m[91mDownloading tokenizers (3.0MiB)
[fastapi] [0m[91mDownloading nvidia-cublas-cu12 (346.6MiB)
[fastapi] [0m[91m Downloaded pygments
[fastapi] [0m[91m Downloaded nltk
[fastapi] [0m[91m Downloaded sentencepiece
[fastapi] [0m[91m Downloaded aiohttp
[fastapi] [0m[91m Downloaded pydantic-core
[fastapi] [0m[91m Downloaded networkx
[fastapi] [0m[91m Downloaded lm-eval
[fastapi] [0m[91m   Building axolotl==0.9.1
[fastapi] [0m[91m   Building langdetect==1.0.9
[fastapi] [0m[91m   Building axolotl-contribs-mit==0.0.3
[fastapi] [0m[91m   Building word2number==1.1
[fastapi] [0m[91m   Building axolotl-contribs-lgpl==0.0.6
[fastapi] [0m[91m Downloaded tokenizers
[fastapi] [0m[91m   Building rouge-score==0.1.2
[fastapi] [0m[91m   Building sqlitedict==2.1.0
[fastapi] [0m[91m Downloaded hf-transfer
[fastapi] [0m[91m Downloaded numba
[fastapi] [0m[91m   Building grpclib==0.4.7
[fastapi] Building hqq==0.2.5
[fastapi] [0m[91m Downloaded zstandard
[fastapi] [0m[91m Downloaded cryptography
[fastapi] [0m[91m      Built word2number==1.1
[fastapi] [0m[91m      Built axolotl-contribs-mit==0.0.3
[fastapi] [0m[91m Downloaded lxml
[fastapi] [0m[91m      Built rouge-score==0.1.2
[fastapi] [0m[91m      Built axolotl-contribs-lgpl==0.0.6
[fastapi] [0m[91m      Built sqlitedict==2.1.0
[fastapi] [0m[91m Downloaded tensorboard
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
[fastapi] [0m[91m      Built hqq==0.2.5
[fastapi] [0m[91m Downloaded scikit-learn
[fastapi] [0m[91m Downloaded pandas
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
[fastapi] [0m[91mPrepared 215 packages in 8.15s
[fastapi] [0m[91mInstalled 215 packages in 426ms
[fastapi] [0m[91m + absl-py==2.5.0
[fastapi] + accelerate==1.6.0
[fastapi] + addict==2.4.0
[fastapi] + adlfs==2026.8.0
[fastapi] + aiobotocore==2.26.0
[fastapi] + aiofiles==23.2.1
[fastapi] + aiohappyeyeballs==[0m[91m2.7.1
[fastapi] + aiohttp==3.14.3
[fastapi] + aioitertools==0.13.0
[fastapi] [0m[91m+ aiosignal==[0m[91m1.4[0m[91m.0
[fastapi] [0m[91m+ [0m[91mannotated-doc==0.0.5
[fastapi] + annotated-types==0.8.0
[fastapi] [0m[91m+ antlr4-python3-runtime==4.13.2
[fastapi] + anyio==4.15.1[0m[91m
[fastapi] [0m[91m+ art==6.5[0m[91m
[fastapi] [0m[91m+ attrs[0m[91m==26.[0m[91m1.0[0m[91m
[fastapi] [0m[91m+ autoawq[0m[91m==0.[0m[91m2.7[0m[91m.post3[0m[91m
[fastapi] + [0m[91maxolotl==0.9.1
[fastapi] + axolotl-contribs-lgpl==0.[0m[91m0.6
[fastapi] + axolotl-contribs-mit==0.0.3
[fastapi] + [0m[91mazure-core[0m[91m==1.41.0
[fastapi] + [0m[91mazure-identity==[0m[91m1.25.3[0m[91m
[fastapi] + [0m[91mazure-storage-blob[0m[91m==12.30.1
[fastapi] + bitsandbytes[0m[91m==0.45.4
[fastapi] + botocore==1.41.5
[fastapi] + certifi[0m[91m==2026.7.22
[fastapi] + cffi[0m[91m==2.1[0m[91m.1
[fastapi] [0m[91m +[0m[91m chardet==[0m[91m6.0.[0m[91m0.post1
[fastapi] + charset-normalizer==3.5.1
[fastapi] + circuitbreaker[0m[91m==2.1.[0m[91m3
[fastapi] + click==8.5.0
[fastapi] +[0m[91m cloudpickle==3.1.2
[fastapi] +[0m[91m colorama==0[0m[91m.4.6
[fastapi] + coloredlogs[0m[91m==15.0.1
[fastapi] [0m[91m+ crc32c==2[0m[91m.8
[fastapi] +[0m[91m cryptography==50[0m[91m.0.1
[fastapi] [0m[91m+ dataproperty[0m[91m==1.1.1
[fastapi] [0m[91m + datasets[0m[91m==3.5.[0m[91m1
[fastapi] +[0m[91m decorator==5.3.1
[fastapi] [0m[91m+ defusedxml==0[0m[91m.7.1
[fastapi] [0m[91m+ dill==0.3.[0m[91m8
[fastapi] + [0m[91meinops==0.[0m[91m8.2
[fastapi] [0m[91m+ evaluate==0[0m[91m.4.1
[fastapi] [0m[91m+ fastapi==[0m[91m0.141.1[0m[91m
[fastapi] + fastcore==[0m[91m2.2.27[0m[91m
[fastapi] [0m[91m + ffmpy[0m[91m==1.0.[0m[91m0
[fastapi] + filelock==3.32.6
[fastapi] + [0m[91mfire==0.7.[0m[91m1
[fastapi] +[0m[91m frozenlist==1.8.0
[fastapi] + fsspec==2025.[0m[91m3.0
[fastapi] [0m[91m+ gcsfs==2025.3.0
[fastapi] + google-api-core==2.33.0
[fastapi] [0m[91m+ google-auth==2.58.0[0m[91m
[fastapi] +[0m[91m [0m[91mgoogle-auth-oauthlib[0m[91m==1.4.1
[fastapi] + google-cloud-core==2.7.[0m[91m0
[fastapi] + google-cloud-storage[0m[91m==3.14.1
[fastapi] + google-crc32c[0m[91m==1.8.[0m[91m0
[fastapi] [0m[91m +[0m[91m google-resumable-media==[0m[91m2.[0m[91m10.[0m[91m2
[fastapi] +[0m[91m googleapis-common-protos==[0m[91m1.[0m[91m75.0[0m[91m
[fastapi] +[0m[91m gradio[0m[91m==5.23[0m[91m.3
[fastapi] [0m[91m+[0m[91m gradio-client[0m[91m==1.[0m[91m8[0m[91m.0
[fastapi] [0m[91m + [0m[91mgroovy==[0m[91m0.1[0m[91m.2
[fastapi] + grpcio==1.84.[0m[91m0
[fastapi] + grpclib==0.4[0m[91m.7
[fastapi] [0m[91m+ h11==0.16.0
[fastapi] + h2[0m[91m==4.4.1
[fastapi] + hf-transfer[0m[91m==0.1[0m[91m.9[0m[91m
[fastapi] +[0m[91m hf-xet[0m[91m==1.1[0m[91m.0
[fastapi] [0m[91m +[0m[91m hpack==4.2.0
[fastapi] +[0m[91m hqq==0.[0m[91m2.5
[fastapi] + httpcore[0m[91m==1.0.[0m[91m9
[fastapi] [0m[91m + [0m[91mhttpx==0.28.1
[fastapi] + huggingface-hub[0m[91m==0.31[0m[91m.0[0m[91m
[fastapi] + [0m[91mhumanfriendly[0m[91m==10.[0m[91m0
[fastapi] + hyperframe==6.1.0
[fastapi] +[0m[91m idna==3.19
[fastapi] + [0m[91mimmutabledict==4.2[0m[91m.0[0m[91m
[fastapi] + [0m[91misodate==0.7.2
[fastapi] [0m[91m+ jinja2==3.1.6[0m[91m
[fastapi] + jmespath==1.1[0m[91m.0
[fastapi] + joblib[0m[91m==1.6.[0m[91m0
[fastapi] +[0m[91m jsonlines==4.[0m[91m0.0
[fastapi] [0m[91m + langdetect[0m[91m==1.0[0m[91m.9
[fastapi] + [0m[91mliger-kernel==0.5.9
[fastapi] [0m[91m+ llvmlite==0[0m[91m.49.0
[fastapi] [0m[91m + lm-eval[0m[91m==0.4.7[0m[91m
[fastapi] + lxml[0m[91m==6.1.3[0m[91m
[fastapi] + [0m[91mmarkdown==3.10.[0m[91m3
[fastapi] + markdown-it-py[0m[91m==4.2.0
[fastapi] + markupsafe==[0m[91m3.0.3
[fastapi] [0m[91m+ mbstrdecoder==1.1[0m[91m.5[0m[91m
[fastapi] +[0m[91m mdurl[0m[91m==0.1.2[0m[91m
[fastapi] + modal==0.70.[0m[91m5
[fastapi] + more-itertools==11.[0m[91m1.0
[fastapi] + mpmath==1[0m[91m.3.0
[fastapi] [0m[91m+ msal==1.38[0m[91m.[0m[91m0
[fastapi] + [0m[91mmsal-extensions[0m[91m==1.3.[0m[91m1[0m[91m
[fastapi] +[0m[91m multidict==6[0m[91m.8[0m[91m.0
[fastapi] +[0m[91m [0m[91mmultiprocess==0.[0m[91m70[0m[91m.16[0m[91m
[fastapi] + [0m[91mnetworkx==[0m[91m3[0m[91m.6.1
[fastapi] [0m[91m+ nltk==3.10.3
[fastapi] +[0m[91m numba==0.67.0
[fastapi] +[0m[91m numexpr==[0m[91m2.14.2[0m[91m
[fastapi] [0m[91m+ [0m[91mnumpy[0m[91m==2.0.1[0m[91m
[fastapi] [0m[91m +[0m[91m nvidia-cublas-cu12==[0m[91m12.4.5.8
[fastapi] + nvidia-cuda-cupti-cu12[0m[91m==12.4.127[0m[91m
[fastapi] + nvidia-cuda-nvrtc-cu12[0m[91m==12.4[0m[91m.127
[fastapi] + [0m[91mnvidia-cuda-runtime-cu12==12.[0m[91m4.127
[fastapi] +[0m[91m nvidia-cudnn-cu12==9[0m[91m.1.0.70[0m[91m
[fastapi] + nvidia-cufft-cu12[0m[91m==11.2[0m[91m.1.3
[fastapi] + [0m[91mnvidia-curand-cu12==10.3.[0m[91m5.147[0m[91m
[fastapi] +[0m[91m nvidia-cusolver-cu12[0m[91m==11.[0m[91m6.1[0m[91m.9
[fastapi] [0m[91m + [0m[91mnvidia-cusparse-cu12==12.3.1.170
[fastapi] + [0m[91mnvidia-cusparselt-cu12==0.6.2[0m[91m
[fastapi] + [0m[91mnvidia-ml-py==12.560.30[0m[91m
[fastapi] + [0m[91mnvidia-nccl-cu12==2.21[0m[91m.5
[fastapi] [0m[91m + [0m[91mnvidia-nvjitlink-cu12[0m[91m==12.4[0m[91m.127
[fastapi] [0m[91m+ [0m[91mnvidia-nvtx-cu12==[0m[91m12.4.[0m[91m127
[fastapi] [0m[91m + oauthlib==3.3.1
[fastapi] + oci==2.[0m[91m186.0
[fastapi] + ocifs==[0m[91m1.3.2
[fastapi] + opentelemetry-api==1.44[0m[91m.0
[fastapi] +[0m[91m opentelemetry-exporter-otlp-proto-common==1[0m[91m.44.[0m[91m0[0m[91m
[fastapi] +[0m[91m opentelemetry-exporter-otlp-proto-http[0m[91m==1.44.[0m[91m0
[fastapi] [0m[91m +[0m[91m opentelemetry-proto[0m[91m==1.44[0m[91m.0
[fastapi] [0m[91m + [0m[91mopentelemetry-sdk[0m[91m==1.[0m[91m44.[0m[91m0
[fastapi] [0m[91m+ [0m[91mopentelemetry-semantic-conventions==[0m[91m0.[0m[91m65b0[0m[91m
[fastapi] +[0m[91m [0m[91moptimum==1.16.2
[fastapi] + orjson==3.12.0
[fastapi] + pandas[0m[91m==2.3[0m[91m.3
[fastapi] +[0m[91m pathvalidate==3.3.1[0m[91m
[fastapi] + [0m[91mpeft==0.[0m[91m15.2
[fastapi] [0m[91m+ pillow==11[0m[91m.3.0
[fastapi] [0m[91m + platformdirs[0m[91m==4.11.[0m[91m8
[fastapi] + portalocker==4[0m[91m.3.2
[fastapi] +[0m[91m propcache==[0m[91m0.[0m[91m5.2
[fastapi] [0m[91m+ [0m[91mproto-plus[0m[91m==1.28.[0m[91m2[0m[91m
[fastapi] +[0m[91m protobuf[0m[91m==5[0m[91m.[0m[91m29.6
[fastapi] [0m[91m+ psutil==7.2.2
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
[fastapi] + scipy==1.17.1
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
[fastapi] [0m ---> 1f1bfa4e1a9f
[fastapi] Step 7/13 : RUN python -m venv /opt/modern &&     /opt/modern/bin/pip install -U pip wheel ninja packaging setuptools &&     /opt/modern/bin/pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cu126 &&     /opt/modern/bin/pip install         "transformers==5.9.0" "accelerate>=1.8" "datasets>=3.5"         safetensors sentencepiece einops triton &&     /opt/modern/bin/pip install flash-linear-attention &&     (/opt/modern/bin/pip install https://github.com/Dao-AILab/causal-conv1d/releases/download/v1.5.2/causal_conv1d-1.5.2+cu12torch2.7cxx11abiTRUE-cp311-cp311-linux_x86_64.whl      || /opt/modern/bin/pip install causal-conv1d --no-build-isolation) &&     (/opt/modern/bin/pip install cut-cross-entropy || true) &&     rm -rf /root/.cache/uv /root/.cache/pip
[fastapi] ---> Running in 3bc20291eeb0
[fastapi] Requirement already satisfied: pip in /opt/modern/lib/python3.11/site-packages (24.0)
[fastapi] Collecting pip
[fastapi] Downloading pip-26.2.1-py3-none-any.whl.metadata (4.6 kB)
[fastapi] Collecting wheel
[fastapi] Downloading wheel-0.48.0-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Collecting ninja
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (5.4 kB)
[fastapi] Collecting packaging
[fastapi] Downloading packaging-26.3-py3-none-any.whl.metadata (3.5 kB)
[fastapi] Requirement already satisfied: setuptools in /opt/modern/lib/python3.11/site-packages (65.5.0)
[fastapi] Collecting setuptools
[fastapi] Downloading setuptools-84.0.0-py3-none-any.whl.metadata (6.6 kB)
[fastapi] Downloading pip-26.2.1-py3-none-any.whl (1.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 58.7 MB/s eta 0:00:00
[fastapi] Downloading wheel-0.48.0-py3-none-any.whl (33 kB)
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (183 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 183.4/183.4 kB 435.2 MB/s eta 0:00:00
[fastapi] Downloading packaging-26.3-py3-none-any.whl (129 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 130.0/130.0 kB 449.6 MB/s eta 0:00:00
[fastapi] Downloading setuptools-84.0.0-py3-none-any.whl (818 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 818.2/818.2 kB 240.9 MB/s eta 0:00:00
[fastapi] Installing collected packages: setuptools, pip, packaging, ninja, wheel
[fastapi] Attempting uninstall: setuptools
[fastapi] Found existing installation: setuptools 65.5.0
[fastapi] Uninstalling setuptools-65.5.0:
[fastapi] Successfully uninstalled setuptools-65.5.0
[fastapi] Attempting uninstall: pip
[fastapi] Found existing installation: pip 24.0
[fastapi] Uninstalling pip-24.0:
[fastapi] Successfully uninstalled pip-24.0
[fastapi] Successfully installed ninja-1.13.2 packaging-26.3 pip-26.2.1 setuptools-84.0.0 wheel-0.48.0
[fastapi] Looking in indexes: https://download.pytorch.org/whl/cu126
[fastapi] Collecting torch==2.7.1
[fastapi] Downloading torch-2.7.1%2Bcu126-cp311-cp311-manylinux_2_28_x86_64.whl.metadata (29 kB)
[fastapi] Collecting filelock (from torch==2.7.1)
[fastapi] Downloading filelock-3.32.3-py3-none-any.whl.metadata (2.0 kB)
[fastapi] Collecting typing-extensions>=4.10.0 (from torch==2.7.1)
[fastapi] Downloading typing_extensions-4.16.0-py3-none-any.whl.metadata (3.3 kB)
[fastapi] Collecting sympy>=1.13.3 (from torch==2.7.1)
[fastapi] Downloading sympy-1.14.0-py3-none-any.whl.metadata (12 kB)
[fastapi] Collecting networkx (from torch==2.7.1)
[fastapi] Downloading networkx-3.6.1-py3-none-any.whl.metadata (6.8 kB)
[fastapi] Collecting jinja2 (from torch==2.7.1)
[fastapi] Downloading jinja2-3.1.6-py3-none-any.whl.metadata (2.9 kB)
[fastapi] Collecting fsspec (from torch==2.7.1)
[fastapi] Downloading fsspec-2026.7.0-py3-none-any.whl.metadata (10 kB)
[fastapi] Collecting nvidia-cuda-nvrtc-cu12==12.6.77 (from torch==2.7.1)
[fastapi] Downloading nvidia_cuda_nvrtc_cu12-12.6.77-py3-none-manylinux2014_x86_64.whl (23.7 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 23.7/23.7 MB 288.0 MB/s  0:00:00
[fastapi] Collecting nvidia-cuda-runtime-cu12==12.6.77 (from torch==2.7.1)
[fastapi] Downloading nvidia_cuda_runtime_cu12-12.6.77-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (897 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 897.7/897.7 kB 724.3 MB/s  0:00:00
[fastapi] Collecting nvidia-cuda-cupti-cu12==12.6.80 (from torch==2.7.1)
[fastapi] Downloading nvidia_cuda_cupti_cu12-12.6.80-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (8.9 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.9/8.9 MB 338.5 MB/s  0:00:00
[fastapi] Collecting nvidia-cudnn-cu12==9.5.1.17 (from torch==2.7.1)
[fastapi] Downloading nvidia_cudnn_cu12-9.5.1.17-py3-none-manylinux_2_28_x86_64.whl (571.0 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 571.0/571.0 MB 314.4 MB/s  0:00:01
[fastapi] Collecting nvidia-cublas-cu12==12.6.4.1 (from torch==2.7.1)
[fastapi] Downloading nvidia_cublas_cu12-12.6.4.1-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (393.1 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 393.1/393.1 MB 321.1 MB/s  0:00:01
[fastapi] Collecting nvidia-cufft-cu12==11.3.0.4 (from torch==2.7.1)
[fastapi] Downloading nvidia_cufft_cu12-11.3.0.4-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (200.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 200.2/200.2 MB 309.5 MB/s  0:00:00
[fastapi] Collecting nvidia-curand-cu12==10.3.7.77 (from torch==2.7.1)
[fastapi] Downloading nvidia_curand_cu12-10.3.7.77-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (56.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 56.3/56.3 MB 314.3 MB/s  0:00:00
[fastapi] Collecting nvidia-cusolver-cu12==11.7.1.2 (from torch==2.7.1)
[fastapi] Downloading nvidia_cusolver_cu12-11.7.1.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (158.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 158.2/158.2 MB 322.0 MB/s  0:00:00
[fastapi] Collecting nvidia-cusparse-cu12==12.5.4.2 (from torch==2.7.1)
[fastapi] Downloading nvidia_cusparse_cu12-12.5.4.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (216.6 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 216.6/216.6 MB 330.0 MB/s  0:00:00
[fastapi] Collecting nvidia-cusparselt-cu12==0.6.3 (from torch==2.7.1)
[fastapi] Downloading nvidia_cusparselt_cu12-0.6.3-py3-none-manylinux2014_x86_64.whl (156.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 156.8/156.8 MB 344.3 MB/s  0:00:00
[fastapi] Collecting nvidia-nccl-cu12==2.26.2 (from torch==2.7.1)
[fastapi] Downloading nvidia_nccl_cu12-2.26.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (201.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 201.3/201.3 MB 329.3 MB/s  0:00:00
[fastapi] Collecting nvidia-nvtx-cu12==12.6.77 (from torch==2.7.1)
[fastapi] Downloading nvidia_nvtx_cu12-12.6.77-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (89 kB)
[fastapi] Collecting nvidia-nvjitlink-cu12==12.6.85 (from torch==2.7.1)
[fastapi] Downloading nvidia_nvjitlink_cu12-12.6.85-py3-none-manylinux2010_x86_64.manylinux_2_12_x86_64.whl (19.7 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 19.7/19.7 MB 303.2 MB/s  0:00:00
[fastapi] Collecting nvidia-cufile-cu12==1.11.1.6 (from torch==2.7.1)
[fastapi] Downloading nvidia_cufile_cu12-1.11.1.6-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (1.1 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.1/1.1 MB 692.8 MB/s  0:00:00
[fastapi] Collecting triton==3.3.1 (from torch==2.7.1)
[fastapi] Downloading triton-3.3.1-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (1.5 kB)
[fastapi] Requirement already satisfied: setuptools>=40.8.0 in /opt/modern/lib/python3.11/site-packages (from triton==3.3.1->torch==2.7.1) (84.0.0)
[fastapi] Collecting mpmath<1.4,>=1.1.0 (from sympy>=1.13.3->torch==2.7.1)
[fastapi] Downloading mpmath-1.3.0-py3-none-any.whl.metadata (8.6 kB)
[fastapi] Collecting MarkupSafe>=2.0 (from jinja2->torch==2.7.1)
[fastapi] Downloading markupsafe-3.0.3-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (2.7 kB)
[fastapi] Downloading torch-2.7.1%2Bcu126-cp311-cp311-manylinux_2_28_x86_64.whl (822.1 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 822.1/822.1 MB 342.8 MB/s  0:00:02
[fastapi] Downloading triton-3.3.1-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (155.7 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 155.7/155.7 MB 431.0 MB/s  0:00:00
[fastapi] Downloading sympy-1.14.0-py3-none-any.whl (6.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.3/6.3 MB 180.3 MB/s  0:00:00
[fastapi] Downloading mpmath-1.3.0-py3-none-any.whl (536 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 536.2/536.2 kB 190.2 MB/s  0:00:00
[fastapi] Downloading typing_extensions-4.16.0-py3-none-any.whl (45 kB)
[fastapi] Downloading filelock-3.32.3-py3-none-any.whl (98 kB)
[fastapi] Downloading fsspec-2026.7.0-py3-none-any.whl (206 kB)
[fastapi] Downloading jinja2-3.1.6-py3-none-any.whl (134 kB)
[fastapi] Downloading markupsafe-3.0.3-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (22 kB)
[fastapi] Downloading networkx-3.6.1-py3-none-any.whl (2.1 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 387.0 MB/s  0:00:00
[fastapi] Installing collected packages: nvidia-cusparselt-cu12, mpmath, typing-extensions, triton, sympy, nvidia-nvtx-cu12, nvidia-nvjitlink-cu12, nvidia-nccl-cu12, nvidia-curand-cu12, nvidia-cufile-cu12, nvidia-cuda-runtime-cu12, nvidia-cuda-nvrtc-cu12, nvidia-cuda-cupti-cu12, nvidia-cublas-cu12, networkx, MarkupSafe, fsspec, filelock, nvidia-cusparse-cu12, nvidia-cufft-cu12, nvidia-cudnn-cu12, jinja2, nvidia-cusolver-cu12, torch
[fastapi] Successfully installed MarkupSafe-3.0.3 filelock-3.32.3 fsspec-2026.7.0 jinja2-3.1.6 mpmath-1.3.0 networkx-3.6.1 nvidia-cublas-cu12-12.6.4.1 nvidia-cuda-cupti-cu12-12.6.80 nvidia-cuda-nvrtc-cu12-12.6.77 nvidia-cuda-runtime-cu12-12.6.77 nvidia-cudnn-cu12-9.5.1.17 nvidia-cufft-cu12-11.3.0.4 nvidia-cufile-cu12-1.11.1.6 nvidia-curand-cu12-10.3.7.77 nvidia-cusolver-cu12-11.7.1.2 nvidia-cusparse-cu12-12.5.4.2 nvidia-cusparselt-cu12-0.6.3 nvidia-nccl-cu12-2.26.2 nvidia-nvjitlink-cu12-12.6.85 nvidia-nvtx-cu12-12.6.77 sympy-1.14.0 torch-2.7.1+cu126 triton-3.3.1 typing-extensions-4.16.0
[fastapi] Collecting transformers==5.9.0
[fastapi] Downloading transformers-5.9.0-py3-none-any.whl.metadata (33 kB)
[fastapi] Collecting accelerate>=1.8
[fastapi] Downloading accelerate-1.15.0-py3-none-any.whl.metadata (19 kB)
[fastapi] Collecting datasets>=3.5
[fastapi] Downloading datasets-5.0.1-py3-none-any.whl.metadata (23 kB)
[fastapi] Collecting safetensors
[fastapi] Downloading safetensors-0.8.0-cp310-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.2 kB)
[fastapi] Collecting sentencepiece
[fastapi] Downloading sentencepiece-0.2.2-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (33 kB)
[fastapi] Collecting einops
[fastapi] Downloading einops-0.8.2-py3-none-any.whl.metadata (13 kB)
[fastapi] Requirement already satisfied: triton in /opt/modern/lib/python3.11/site-packages (3.3.1)
[fastapi] Collecting huggingface-hub<2.0,>=1.5.0 (from transformers==5.9.0)
[fastapi] Downloading huggingface_hub-1.31.0-py3-none-any.whl.metadata (16 kB)
[fastapi] Collecting numpy>=1.17 (from transformers==5.9.0)
[fastapi] Downloading numpy-2.4.6-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (6.6 kB)
[fastapi] Requirement already satisfied: packaging>=20.0 in /opt/modern/lib/python3.11/site-packages (from transformers==5.9.0) (26.3)
[fastapi] Collecting pyyaml>=5.1 (from transformers==5.9.0)
[fastapi] Downloading pyyaml-6.0.3-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (2.4 kB)
[fastapi] Collecting regex>=2025.10.22 (from transformers==5.9.0)
[fastapi] Downloading regex-2026.9.10-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (40 kB)
[fastapi] Collecting tokenizers<=0.23.0,>=0.22.0 (from transformers==5.9.0)
[fastapi] Downloading tokenizers-0.22.2-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (7.3 kB)
[fastapi] Collecting typer (from transformers==5.9.0)
[fastapi] Downloading typer-0.27.2-py3-none-any.whl.metadata (16 kB)
[fastapi] Collecting tqdm>=4.27 (from transformers==5.9.0)
[fastapi] Downloading tqdm-4.70.1-py3-none-any.whl.metadata (57 kB)
[fastapi] Collecting click<9.0.0,>=8.4.2 (from huggingface-hub<2.0,>=1.5.0->transformers==5.9.0)
[fastapi] Downloading click-8.5.0-py3-none-any.whl.metadata (2.6 kB)
[fastapi] Requirement already satisfied: filelock>=3.10.0 in /opt/modern/lib/python3.11/site-packages (from huggingface-hub<2.0,>=1.5.0->transformers==5.9.0) (3.32.3)
[fastapi] Requirement already satisfied: fsspec>=2023.5.0 in /opt/modern/lib/python3.11/site-packages (from huggingface-hub<2.0,>=1.5.0->transformers==5.9.0) (2026.7.0)
[fastapi] Collecting hf-xet<2.0.0,>=1.5.2 (from huggingface-hub<2.0,>=1.5.0->transformers==5.9.0)
[fastapi] Downloading hf_xet-1.6.0-cp38-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (4.9 kB)
[fastapi] Collecting httpx<1,>=0.23.0 (from huggingface-hub<2.0,>=1.5.0->transformers==5.9.0)
[fastapi] Downloading httpx-0.28.1-py3-none-any.whl.metadata (7.1 kB)
[fastapi] Requirement already satisfied: typing-extensions>=4.1.0 in /opt/modern/lib/python3.11/site-packages (from huggingface-hub<2.0,>=1.5.0->transformers==5.9.0) (4.16.0)
[fastapi] Collecting anyio (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers==5.9.0)
[fastapi] Downloading anyio-4.15.1-py3-none-any.whl.metadata (4.7 kB)
[fastapi] Collecting certifi (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers==5.9.0)
[fastapi] Downloading certifi-2026.7.22-py3-none-any.whl.metadata (2.5 kB)
[fastapi] Collecting httpcore==1.* (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers==5.9.0)
[fastapi] Downloading httpcore-1.0.9-py3-none-any.whl.metadata (21 kB)
[fastapi] Collecting idna (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers==5.9.0)
[fastapi] Downloading idna-3.19-py3-none-any.whl.metadata (9.2 kB)
[fastapi] Collecting h11>=0.16 (from httpcore==1.*->httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers==5.9.0)
[fastapi] Downloading h11-0.16.0-py3-none-any.whl.metadata (8.3 kB)
[fastapi] Collecting psutil (from accelerate>=1.8)
[fastapi] Downloading psutil-7.2.2-cp36-abi3-manylinux2010_x86_64.manylinux_2_12_x86_64.manylinux_2_28_x86_64.whl.metadata (22 kB)
[fastapi] Requirement already satisfied: torch>=2.0.0 in /opt/modern/lib/python3.11/site-packages (from accelerate>=1.8) (2.7.1+cu126)
[fastapi] Collecting pyarrow>=21.0.0 (from datasets>=3.5)
[fastapi] Downloading pyarrow-25.0.1-cp311-cp311-manylinux_2_28_x86_64.whl.metadata (3.0 kB)
[fastapi] Collecting dill<0.4.2,>=0.3.0 (from datasets>=3.5)
[fastapi] Downloading dill-0.4.1-py3-none-any.whl.metadata (10 kB)
[fastapi] Collecting pandas (from datasets>=3.5)
[fastapi] Downloading pandas-3.0.5-cp311-cp311-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl.metadata (79 kB)
[fastapi] Collecting requests>=2.32.2 (from datasets>=3.5)
[fastapi] Downloading requests-2.34.2-py3-none-any.whl.metadata (4.8 kB)
[fastapi] Collecting xxhash (from datasets>=3.5)
[fastapi] Downloading xxhash-4.0.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (17 kB)
[fastapi] Collecting multiprocess<0.70.20 (from datasets>=3.5)
[fastapi] Downloading multiprocess-0.70.19-py311-none-any.whl.metadata (7.5 kB)
[fastapi] Collecting fsspec>=2023.5.0 (from huggingface-hub<2.0,>=1.5.0->transformers==5.9.0)
[fastapi] Downloading fsspec-2026.6.0-py3-none-any.whl.metadata (10 kB)
[fastapi] Collecting aiohttp!=4.0.0a0,!=4.0.0a1 (from fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=3.5)
[fastapi] Downloading aiohttp-3.14.3-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (8.3 kB)
[fastapi] Requirement already satisfied: setuptools>=40.8.0 in /opt/modern/lib/python3.11/site-packages (from triton) (84.0.0)
[fastapi] Collecting aiohappyeyeballs>=2.5.0 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=3.5)
[fastapi] Downloading aiohappyeyeballs-2.7.1-py3-none-any.whl.metadata (5.9 kB)
[fastapi] Collecting aiosignal>=1.4.0 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=3.5)
[fastapi] Downloading aiosignal-1.4.0-py3-none-any.whl.metadata (3.7 kB)
[fastapi] Collecting attrs>=17.3.0 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=3.5)
[fastapi] Downloading attrs-26.1.0-py3-none-any.whl.metadata (8.8 kB)
[fastapi] Collecting frozenlist>=1.1.1 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=3.5)
[fastapi] Downloading frozenlist-1.8.0-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (20 kB)
[fastapi] Collecting multidict<7.0,>=4.5 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=3.5)
[fastapi] Downloading multidict-6.8.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (5.3 kB)
[fastapi] Collecting propcache>=0.2.0 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=3.5)
[fastapi] Downloading propcache-0.5.2-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (16 kB)
[fastapi] Collecting yarl<2.0,>=1.17.0 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=3.5)
[fastapi] Downloading yarl-1.24.5-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (103 kB)
[fastapi] Collecting charset_normalizer<4,>=2 (from requests>=2.32.2->datasets>=3.5)
[fastapi] Downloading charset_normalizer-3.5.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (45 kB)
[fastapi] Collecting urllib3<3,>=1.26 (from requests>=2.32.2->datasets>=3.5)
[fastapi] Downloading urllib3-2.7.0-py3-none-any.whl.metadata (6.9 kB)
[fastapi] Requirement already satisfied: sympy>=1.13.3 in /opt/modern/lib/python3.11/site-packages (from torch>=2.0.0->accelerate>=1.8) (1.14.0)
[fastapi] Requirement already satisfied: networkx in /opt/modern/lib/python3.11/site-packages (from torch>=2.0.0->accelerate>=1.8) (3.6.1)
[fastapi] Requirement already satisfied: jinja2 in /opt/modern/lib/python3.11/site-packages (from torch>=2.0.0->accelerate>=1.8) (3.1.6)
[fastapi] Requirement already satisfied: nvidia-cuda-nvrtc-cu12==12.6.77 in /opt/modern/lib/python3.11/site-packages (from torch>=2.0.0->accelerate>=1.8) (12.6.77)
[fastapi] Requirement already satisfied: nvidia-cuda-runtime-cu12==12.6.77 in /opt/modern/lib/python3.11/site-packages (from torch>=2.0.0->accelerate>=1.8) (12.6.77)
[fastapi] Requirement already satisfied: nvidia-cuda-cupti-cu12==12.6.80 in /opt/modern/lib/python3.11/site-packages (from torch>=2.0.0->accelerate>=1.8) (12.6.80)
[fastapi] Requirement already satisfied: nvidia-cudnn-cu12==9.5.1.17 in /opt/modern/lib/python3.11/site-packages (from torch>=2.0.0->accelerate>=1.8) (9.5.1.17)
[fastapi] Requirement already satisfied: nvidia-cublas-cu12==12.6.4.1 in /opt/modern/lib/python3.11/site-packages (from torch>=2.0.0->accelerate>=1.8) (12.6.4.1)
[fastapi] Requirement already satisfied: nvidia-cufft-cu12==11.3.0.4 in /opt/modern/lib/python3.11/site-packages (from torch>=2.0.0->accelerate>=1.8) (11.3.0.4)
[fastapi] Requirement already satisfied: nvidia-curand-cu12==10.3.7.77 in /opt/modern/lib/python3.11/site-packages (from torch>=2.0.0->accelerate>=1.8) (10.3.7.77)
[fastapi] Requirement already satisfied: nvidia-cusolver-cu12==11.7.1.2 in /opt/modern/lib/python3.11/site-packages (from torch>=2.0.0->accelerate>=1.8) (11.7.1.2)
[fastapi] Requirement already satisfied: nvidia-cusparse-cu12==12.5.4.2 in /opt/modern/lib/python3.11/site-packages (from torch>=2.0.0->accelerate>=1.8) (12.5.4.2)
[fastapi] Requirement already satisfied: nvidia-cusparselt-cu12==0.6.3 in /opt/modern/lib/python3.11/site-packages (from torch>=2.0.0->accelerate>=1.8) (0.6.3)
[fastapi] Requirement already satisfied: nvidia-nccl-cu12==2.26.2 in /opt/modern/lib/python3.11/site-packages (from torch>=2.0.0->accelerate>=1.8) (2.26.2)
[fastapi] Requirement already satisfied: nvidia-nvtx-cu12==12.6.77 in /opt/modern/lib/python3.11/site-packages (from torch>=2.0.0->accelerate>=1.8) (12.6.77)
[fastapi] Requirement already satisfied: nvidia-nvjitlink-cu12==12.6.85 in /opt/modern/lib/python3.11/site-packages (from torch>=2.0.0->accelerate>=1.8) (12.6.85)
[fastapi] Requirement already satisfied: nvidia-cufile-cu12==1.11.1.6 in /opt/modern/lib/python3.11/site-packages (from torch>=2.0.0->accelerate>=1.8) (1.11.1.6)
[fastapi] Requirement already satisfied: mpmath<1.4,>=1.1.0 in /opt/modern/lib/python3.11/site-packages (from sympy>=1.13.3->torch>=2.0.0->accelerate>=1.8) (1.3.0)
[fastapi] Requirement already satisfied: MarkupSafe>=2.0 in /opt/modern/lib/python3.11/site-packages (from jinja2->torch>=2.0.0->accelerate>=1.8) (3.0.3)
[fastapi] Collecting python-dateutil>=2.8.2 (from pandas->datasets>=3.5)
[fastapi] Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl.metadata (8.4 kB)
[fastapi] Collecting six>=1.5 (from python-dateutil>=2.8.2->pandas->datasets>=3.5)
[fastapi] Downloading six-1.17.0-py2.py3-none-any.whl.metadata (1.7 kB)
[fastapi] Collecting shellingham>=1.3.0 (from typer->transformers==5.9.0)
[fastapi] Downloading shellingham-1.5.4-py2.py3-none-any.whl.metadata (3.5 kB)
[fastapi] Collecting rich>=13.8.0 (from typer->transformers==5.9.0)
[fastapi] Downloading rich-15.0.0-py3-none-any.whl.metadata (18 kB)
[fastapi] Collecting annotated-doc>=0.0.2 (from typer->transformers==5.9.0)
[fastapi] Downloading annotated_doc-0.0.5-py3-none-any.whl.metadata (6.5 kB)
[fastapi] Collecting markdown-it-py>=2.2.0 (from rich>=13.8.0->typer->transformers==5.9.0)
[fastapi] Downloading markdown_it_py-4.2.0-py3-none-any.whl.metadata (7.4 kB)
[fastapi] Collecting pygments<3.0.0,>=2.13.0 (from rich>=13.8.0->typer->transformers==5.9.0)
[fastapi] Downloading pygments-2.21.0-py3-none-any.whl.metadata (2.5 kB)
[fastapi] Collecting mdurl~=0.1 (from markdown-it-py>=2.2.0->rich>=13.8.0->typer->transformers==5.9.0)
[fastapi] Downloading mdurl-0.1.2-py3-none-any.whl.metadata (1.6 kB)
[fastapi] Downloading transformers-5.9.0-py3-none-any.whl (10.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 10.8/10.8 MB 342.8 MB/s  0:00:00
[fastapi] Downloading huggingface_hub-1.31.0-py3-none-any.whl (798 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 798.3/798.3 kB 735.2 MB/s  0:00:00
[fastapi] Downloading click-8.5.0-py3-none-any.whl (125 kB)
[fastapi] Downloading hf_xet-1.6.0-cp38-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (4.5 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.5/4.5 MB 440.7 MB/s  0:00:00
[fastapi] Downloading httpx-0.28.1-py3-none-any.whl (73 kB)
[fastapi] Downloading httpcore-1.0.9-py3-none-any.whl (78 kB)
[fastapi] Downloading tokenizers-0.22.2-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.3/3.3 MB 344.8 MB/s  0:00:00
[fastapi] Downloading accelerate-1.15.0-py3-none-any.whl (394 kB)
[fastapi] Downloading datasets-5.0.1-py3-none-any.whl (559 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 559.1/559.1 kB 724.5 MB/s  0:00:00
[fastapi] Downloading dill-0.4.1-py3-none-any.whl (120 kB)
[fastapi] Downloading fsspec-2026.6.0-py3-none-any.whl (203 kB)
[fastapi] Downloading multiprocess-0.70.19-py311-none-any.whl (144 kB)
[fastapi] Downloading safetensors-0.8.0-cp310-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (516 kB)
[fastapi] Downloading sentencepiece-0.2.2-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (1.4 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.4/1.4 MB 804.7 MB/s  0:00:00
[fastapi] Downloading einops-0.8.2-py3-none-any.whl (65 kB)
[fastapi] Downloading aiohttp-3.14.3-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (1.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 393.6 MB/s  0:00:00
[fastapi] Downloading multidict-6.8.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (272 kB)
[fastapi] Downloading yarl-1.24.5-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (111 kB)
[fastapi] Downloading aiohappyeyeballs-2.7.1-py3-none-any.whl (15 kB)
[fastapi] Downloading aiosignal-1.4.0-py3-none-any.whl (7.5 kB)
[fastapi] Downloading attrs-26.1.0-py3-none-any.whl (67 kB)
[fastapi] Downloading frozenlist-1.8.0-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (231 kB)
[fastapi] Downloading h11-0.16.0-py3-none-any.whl (37 kB)
[fastapi] Downloading idna-3.19-py3-none-any.whl (68 kB)
[fastapi] Downloading numpy-2.4.6-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (16.9 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 16.9/16.9 MB 419.7 MB/s  0:00:00
[fastapi] Downloading propcache-0.5.2-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (58 kB)
[fastapi] Downloading pyarrow-25.0.1-cp311-cp311-manylinux_2_28_x86_64.whl (50.1 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 50.1/50.1 MB 284.5 MB/s  0:00:00
[fastapi] Downloading pyyaml-6.0.3-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (806 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 806.6/806.6 kB 795.4 MB/s  0:00:00
[fastapi] Downloading regex-2026.9.10-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (802 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 803.0/803.0 kB 776.7 MB/s  0:00:00
[fastapi] Downloading requests-2.34.2-py3-none-any.whl (73 kB)
[fastapi] Downloading charset_normalizer-3.5.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (262 kB)
[fastapi] Downloading urllib3-2.7.0-py3-none-any.whl (131 kB)
[fastapi] Downloading certifi-2026.7.22-py3-none-any.whl (136 kB)
[fastapi] Downloading tqdm-4.70.1-py3-none-any.whl (80 kB)
[fastapi] Downloading anyio-4.15.1-py3-none-any.whl (132 kB)
[fastapi] Downloading pandas-3.0.5-cp311-cp311-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (11.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 11.3/11.3 MB 350.5 MB/s  0:00:00
[fastapi] Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
[fastapi] Downloading six-1.17.0-py2.py3-none-any.whl (11 kB)
[fastapi] Downloading psutil-7.2.2-cp36-abi3-manylinux2010_x86_64.manylinux_2_12_x86_64.manylinux_2_28_x86_64.whl (155 kB)
[fastapi] Downloading typer-0.27.2-py3-none-any.whl (123 kB)
[fastapi] Downloading annotated_doc-0.0.5-py3-none-any.whl (5.3 kB)
[fastapi] Downloading rich-15.0.0-py3-none-any.whl (310 kB)
[fastapi] Downloading pygments-2.21.0-py3-none-any.whl (1.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.3/1.3 MB 664.7 MB/s  0:00:00
[fastapi] Downloading markdown_it_py-4.2.0-py3-none-any.whl (91 kB)
[fastapi] Downloading mdurl-0.1.2-py3-none-any.whl (10.0 kB)
[fastapi] Downloading shellingham-1.5.4-py2.py3-none-any.whl (9.8 kB)
[fastapi] Downloading xxhash-4.0.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (261 kB)
[fastapi] Installing collected packages: xxhash, urllib3, tqdm, six, shellingham, sentencepiece, safetensors, regex, pyyaml, pygments, pyarrow, psutil, propcache, numpy, multidict, mdurl, idna, hf-xet, h11, fsspec, frozenlist, einops, dill, click, charset_normalizer, certifi, attrs, annotated-doc, aiohappyeyeballs, yarl, requests, python-dateutil, multiprocess, markdown-it-py, httpcore, anyio, aiosignal, rich, pandas, httpx, aiohttp, typer, huggingface-hub, tokenizers, datasets, accelerate, transformers
[fastapi] Attempting uninstall: fsspec
[fastapi] Found existing installation: fsspec 2026.7.0
[fastapi] Uninstalling fsspec-2026.7.0:
[fastapi] Successfully uninstalled fsspec-2026.7.0
[fastapi] Successfully installed accelerate-1.15.0 aiohappyeyeballs-2.7.1 aiohttp-3.14.3 aiosignal-1.4.0 annotated-doc-0.0.5 anyio-4.15.1 attrs-26.1.0 certifi-2026.7.22 charset_normalizer-3.5.1 click-8.5.0 datasets-5.0.1 dill-0.4.1 einops-0.8.2 frozenlist-1.8.0 fsspec-2026.6.0 h11-0.16.0 hf-xet-1.6.0 httpcore-1.0.9 httpx-0.28.1 huggingface-hub-1.31.0 idna-3.19 markdown-it-py-4.2.0 mdurl-0.1.2 multidict-6.8.0 multiprocess-0.70.19 numpy-2.4.6 pandas-3.0.5 propcache-0.5.2 psutil-7.2.2 pyarrow-25.0.1 pygments-2.21.0 python-dateutil-2.9.0.post0 pyyaml-6.0.3 regex-2026.9.10 requests-2.34.2 rich-15.0.0 safetensors-0.8.0 sentencepiece-0.2.2 shellingham-1.5.4 six-1.17.0 tokenizers-0.22.2 tqdm-4.70.1 transformers-5.9.0 typer-0.27.2 urllib3-2.7.0 xxhash-4.0.1 yarl-1.24.5
[fastapi] Collecting flash-linear-attention
[fastapi] Downloading flash_linear_attention-0.5.2-py3-none-any.whl.metadata (45 kB)
[fastapi] Collecting fla-core==0.5.2 (from flash-linear-attention)
[fastapi] Downloading fla_core-0.5.2-py3-none-any.whl.metadata (45 kB)
[fastapi] Requirement already satisfied: transformers>=4.45.0 in /opt/modern/lib/python3.11/site-packages (from flash-linear-attention) (5.9.0)
[fastapi] Requirement already satisfied: einops in /opt/modern/lib/python3.11/site-packages (from fla-core==0.5.2->flash-linear-attention) (0.8.2)
[fastapi] Requirement already satisfied: huggingface-hub<2.0,>=1.5.0 in /opt/modern/lib/python3.11/site-packages (from transformers>=4.45.0->flash-linear-attention) (1.31.0)
[fastapi] Requirement already satisfied: numpy>=1.17 in /opt/modern/lib/python3.11/site-packages (from transformers>=4.45.0->flash-linear-attention) (2.4.6)
[fastapi] Requirement already satisfied: packaging>=20.0 in /opt/modern/lib/python3.11/site-packages (from transformers>=4.45.0->flash-linear-attention) (26.3)
[fastapi] Requirement already satisfied: pyyaml>=5.1 in /opt/modern/lib/python3.11/site-packages (from transformers>=4.45.0->flash-linear-attention) (6.0.3)
[fastapi] Requirement already satisfied: regex>=2025.10.22 in /opt/modern/lib/python3.11/site-packages (from transformers>=4.45.0->flash-linear-attention) (2026.9.10)
[fastapi] Requirement already satisfied: tokenizers<=0.23.0,>=0.22.0 in /opt/modern/lib/python3.11/site-packages (from transformers>=4.45.0->flash-linear-attention) (0.22.2)
[fastapi] Requirement already satisfied: typer in /opt/modern/lib/python3.11/site-packages (from transformers>=4.45.0->flash-linear-attention) (0.27.2)
[fastapi] Requirement already satisfied: safetensors>=0.4.3 in /opt/modern/lib/python3.11/site-packages (from transformers>=4.45.0->flash-linear-attention) (0.8.0)
[fastapi] Requirement already satisfied: tqdm>=4.27 in /opt/modern/lib/python3.11/site-packages (from transformers>=4.45.0->flash-linear-attention) (4.70.1)
[fastapi] Requirement already satisfied: click<9.0.0,>=8.4.2 in /opt/modern/lib/python3.11/site-packages (from huggingface-hub<2.0,>=1.5.0->transformers>=4.45.0->flash-linear-attention) (8.5.0)
[fastapi] Requirement already satisfied: filelock>=3.10.0 in /opt/modern/lib/python3.11/site-packages (from huggingface-hub<2.0,>=1.5.0->transformers>=4.45.0->flash-linear-attention) (3.32.3)
[fastapi] Requirement already satisfied: fsspec>=2023.5.0 in /opt/modern/lib/python3.11/site-packages (from huggingface-hub<2.0,>=1.5.0->transformers>=4.45.0->flash-linear-attention) (2026.6.0)
[fastapi] Requirement already satisfied: hf-xet<2.0.0,>=1.5.2 in /opt/modern/lib/python3.11/site-packages (from huggingface-hub<2.0,>=1.5.0->transformers>=4.45.0->flash-linear-attention) (1.6.0)
[fastapi] Requirement already satisfied: httpx<1,>=0.23.0 in /opt/modern/lib/python3.11/site-packages (from huggingface-hub<2.0,>=1.5.0->transformers>=4.45.0->flash-linear-attention) (0.28.1)
[fastapi] Requirement already satisfied: typing-extensions>=4.1.0 in /opt/modern/lib/python3.11/site-packages (from huggingface-hub<2.0,>=1.5.0->transformers>=4.45.0->flash-linear-attention) (4.16.0)
[fastapi] Requirement already satisfied: anyio in /opt/modern/lib/python3.11/site-packages (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers>=4.45.0->flash-linear-attention) (4.15.1)
[fastapi] Requirement already satisfied: certifi in /opt/modern/lib/python3.11/site-packages (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers>=4.45.0->flash-linear-attention) (2026.7.22)
[fastapi] Requirement already satisfied: httpcore==1.* in /opt/modern/lib/python3.11/site-packages (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers>=4.45.0->flash-linear-attention) (1.0.9)
[fastapi] Requirement already satisfied: idna in /opt/modern/lib/python3.11/site-packages (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers>=4.45.0->flash-linear-attention) (3.19)
[fastapi] Requirement already satisfied: h11>=0.16 in /opt/modern/lib/python3.11/site-packages (from httpcore==1.*->httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers>=4.45.0->flash-linear-attention) (0.16.0)
[fastapi] Requirement already satisfied: shellingham>=1.3.0 in /opt/modern/lib/python3.11/site-packages (from typer->transformers>=4.45.0->flash-linear-attention) (1.5.4)
[fastapi] Requirement already satisfied: rich>=13.8.0 in /opt/modern/lib/python3.11/site-packages (from typer->transformers>=4.45.0->flash-linear-attention) (15.0.0)
[fastapi] Requirement already satisfied: annotated-doc>=0.0.2 in /opt/modern/lib/python3.11/site-packages (from typer->transformers>=4.45.0->flash-linear-attention) (0.0.5)
[fastapi] Requirement already satisfied: markdown-it-py>=2.2.0 in /opt/modern/lib/python3.11/site-packages (from rich>=13.8.0->typer->transformers>=4.45.0->flash-linear-attention) (4.2.0)
[fastapi] Requirement already satisfied: pygments<3.0.0,>=2.13.0 in /opt/modern/lib/python3.11/site-packages (from rich>=13.8.0->typer->transformers>=4.45.0->flash-linear-attention) (2.21.0)
[fastapi] Requirement already satisfied: mdurl~=0.1 in /opt/modern/lib/python3.11/site-packages (from markdown-it-py>=2.2.0->rich>=13.8.0->typer->transformers>=4.45.0->flash-linear-attention) (0.1.2)
[fastapi] Downloading flash_linear_attention-0.5.2-py3-none-any.whl (399 kB)
[fastapi] Downloading fla_core-0.5.2-py3-none-any.whl (819 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 819.2/819.2 kB 93.4 MB/s  0:00:00
[fastapi] Installing collected packages: fla-core, flash-linear-attention
[fastapi] Successfully installed fla-core-0.5.2 flash-linear-attention-0.5.2
[fastapi] Collecting causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue
[fastapi] Downloading causal_conv1d-1.5.2+cu12torch2.7cxx11abiTRUE-cp311-cp311-linux_x86_64.whl (133.0 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 133.0/133.0 MB 123.2 MB/s  0:00:01
[fastapi] Requirement already satisfied: torch in /opt/modern/lib/python3.11/site-packages (from causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (2.7.1+cu126)
[fastapi] Requirement already satisfied: packaging in /opt/modern/lib/python3.11/site-packages (from causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (26.3)
[fastapi] Requirement already satisfied: ninja in /opt/modern/lib/python3.11/site-packages (from causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (1.13.2)
[fastapi] Requirement already satisfied: filelock in /opt/modern/lib/python3.11/site-packages (from torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (3.32.3)
[fastapi] Requirement already satisfied: typing-extensions>=4.10.0 in /opt/modern/lib/python3.11/site-packages (from torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (4.16.0)
[fastapi] Requirement already satisfied: sympy>=1.13.3 in /opt/modern/lib/python3.11/site-packages (from torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (1.14.0)
[fastapi] Requirement already satisfied: networkx in /opt/modern/lib/python3.11/site-packages (from torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (3.6.1)
[fastapi] Requirement already satisfied: jinja2 in /opt/modern/lib/python3.11/site-packages (from torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (3.1.6)
[fastapi] Requirement already satisfied: fsspec in /opt/modern/lib/python3.11/site-packages (from torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (2026.6.0)
[fastapi] Requirement already satisfied: nvidia-cuda-nvrtc-cu12==12.6.77 in /opt/modern/lib/python3.11/site-packages (from torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (12.6.77)
[fastapi] Requirement already satisfied: nvidia-cuda-runtime-cu12==12.6.77 in /opt/modern/lib/python3.11/site-packages (from torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (12.6.77)
[fastapi] Requirement already satisfied: nvidia-cuda-cupti-cu12==12.6.80 in /opt/modern/lib/python3.11/site-packages (from torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (12.6.80)
[fastapi] Requirement already satisfied: nvidia-cudnn-cu12==9.5.1.17 in /opt/modern/lib/python3.11/site-packages (from torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (9.5.1.17)
[fastapi] Requirement already satisfied: nvidia-cublas-cu12==12.6.4.1 in /opt/modern/lib/python3.11/site-packages (from torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (12.6.4.1)
[fastapi] Requirement already satisfied: nvidia-cufft-cu12==11.3.0.4 in /opt/modern/lib/python3.11/site-packages (from torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (11.3.0.4)
[fastapi] Requirement already satisfied: nvidia-curand-cu12==10.3.7.77 in /opt/modern/lib/python3.11/site-packages (from torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (10.3.7.77)
[fastapi] Requirement already satisfied: nvidia-cusolver-cu12==11.7.1.2 in /opt/modern/lib/python3.11/site-packages (from torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (11.7.1.2)
[fastapi] Requirement already satisfied: nvidia-cusparse-cu12==12.5.4.2 in /opt/modern/lib/python3.11/site-packages (from torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (12.5.4.2)
[fastapi] Requirement already satisfied: nvidia-cusparselt-cu12==0.6.3 in /opt/modern/lib/python3.11/site-packages (from torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (0.6.3)
[fastapi] Requirement already satisfied: nvidia-nccl-cu12==2.26.2 in /opt/modern/lib/python3.11/site-packages (from torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (2.26.2)
[fastapi] Requirement already satisfied: nvidia-nvtx-cu12==12.6.77 in /opt/modern/lib/python3.11/site-packages (from torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (12.6.77)
[fastapi] Requirement already satisfied: nvidia-nvjitlink-cu12==12.6.85 in /opt/modern/lib/python3.11/site-packages (from torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (12.6.85)
[fastapi] Requirement already satisfied: nvidia-cufile-cu12==1.11.1.6 in /opt/modern/lib/python3.11/site-packages (from torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (1.11.1.6)
[fastapi] Requirement already satisfied: triton==3.3.1 in /opt/modern/lib/python3.11/site-packages (from torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (3.3.1)
[fastapi] Requirement already satisfied: setuptools>=40.8.0 in /opt/modern/lib/python3.11/site-packages (from triton==3.3.1->torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (84.0.0)
[fastapi] Requirement already satisfied: mpmath<1.4,>=1.1.0 in /opt/modern/lib/python3.11/site-packages (from sympy>=1.13.3->torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (1.3.0)
[fastapi] Requirement already satisfied: MarkupSafe>=2.0 in /opt/modern/lib/python3.11/site-packages (from jinja2->torch->causal-conv1d==1.5.2+cu12torch2.7cxx11abitrue) (3.0.3)
[fastapi] Installing collected packages: causal-conv1d
[fastapi] Successfully installed causal-conv1d-1.5.2
[fastapi] Collecting cut-cross-entropy
[fastapi] Downloading cut_cross_entropy-25.1.1-py3-none-any.whl.metadata (9.3 kB)
[fastapi] Requirement already satisfied: torch in /opt/modern/lib/python3.11/site-packages (from cut-cross-entropy) (2.7.1+cu126)
[fastapi] Requirement already satisfied: triton in /opt/modern/lib/python3.11/site-packages (from cut-cross-entropy) (3.3.1)
[fastapi] Requirement already satisfied: filelock in /opt/modern/lib/python3.11/site-packages (from torch->cut-cross-entropy) (3.32.3)
[fastapi] Requirement already satisfied: typing-extensions>=4.10.0 in /opt/modern/lib/python3.11/site-packages (from torch->cut-cross-entropy) (4.16.0)
[fastapi] Requirement already satisfied: sympy>=1.13.3 in /opt/modern/lib/python3.11/site-packages (from torch->cut-cross-entropy) (1.14.0)
[fastapi] Requirement already satisfied: networkx in /opt/modern/lib/python3.11/site-packages (from torch->cut-cross-entropy) (3.6.1)
[fastapi] Requirement already satisfied: jinja2 in /opt/modern/lib/python3.11/site-packages (from torch->cut-cross-entropy) (3.1.6)
[fastapi] Requirement already satisfied: fsspec in /opt/modern/lib/python3.11/site-packages (from torch->cut-cross-entropy) (2026.6.0)
[fastapi] Requirement already satisfied: nvidia-cuda-nvrtc-cu12==12.6.77 in /opt/modern/lib/python3.11/site-packages (from torch->cut-cross-entropy) (12.6.77)
[fastapi] Requirement already satisfied: nvidia-cuda-runtime-cu12==12.6.77 in /opt/modern/lib/python3.11/site-packages (from torch->cut-cross-entropy) (12.6.77)
[fastapi] Requirement already satisfied: nvidia-cuda-cupti-cu12==12.6.80 in /opt/modern/lib/python3.11/site-packages (from torch->cut-cross-entropy) (12.6.80)
[fastapi] Requirement already satisfied: nvidia-cudnn-cu12==9.5.1.17 in /opt/modern/lib/python3.11/site-packages (from torch->cut-cross-entropy) (9.5.1.17)
[fastapi] Requirement already satisfied: nvidia-cublas-cu12==12.6.4.1 in /opt/modern/lib/python3.11/site-packages (from torch->cut-cross-entropy) (12.6.4.1)
[fastapi] Requirement already satisfied: nvidia-cufft-cu12==11.3.0.4 in /opt/modern/lib/python3.11/site-packages (from torch->cut-cross-entropy) (11.3.0.4)
[fastapi] Requirement already satisfied: nvidia-curand-cu12==10.3.7.77 in /opt/modern/lib/python3.11/site-packages (from torch->cut-cross-entropy) (10.3.7.77)
[fastapi] Requirement already satisfied: nvidia-cusolver-cu12==11.7.1.2 in /opt/modern/lib/python3.11/site-packages (from torch->cut-cross-entropy) (11.7.1.2)
[fastapi] Requirement already satisfied: nvidia-cusparse-cu12==12.5.4.2 in /opt/modern/lib/python3.11/site-packages (from torch->cut-cross-entropy) (12.5.4.2)
[fastapi] Requirement already satisfied: nvidia-cusparselt-cu12==0.6.3 in /opt/modern/lib/python3.11/site-packages (from torch->cut-cross-entropy) (0.6.3)
[fastapi] Requirement already satisfied: nvidia-nccl-cu12==2.26.2 in /opt/modern/lib/python3.11/site-packages (from torch->cut-cross-entropy) (2.26.2)
[fastapi] Requirement already satisfied: nvidia-nvtx-cu12==12.6.77 in /opt/modern/lib/python3.11/site-packages (from torch->cut-cross-entropy) (12.6.77)
[fastapi] Requirement already satisfied: nvidia-nvjitlink-cu12==12.6.85 in /opt/modern/lib/python3.11/site-packages (from torch->cut-cross-entropy) (12.6.85)
[fastapi] Requirement already satisfied: nvidia-cufile-cu12==1.11.1.6 in /opt/modern/lib/python3.11/site-packages (from torch->cut-cross-entropy) (1.11.1.6)
[fastapi] Requirement already satisfied: setuptools>=40.8.0 in /opt/modern/lib/python3.11/site-packages (from triton->cut-cross-entropy) (84.0.0)
[fastapi] Requirement already satisfied: mpmath<1.4,>=1.1.0 in /opt/modern/lib/python3.11/site-packages (from sympy>=1.13.3->torch->cut-cross-entropy) (1.3.0)
[fastapi] Requirement already satisfied: MarkupSafe>=2.0 in /opt/modern/lib/python3.11/site-packages (from jinja2->torch->cut-cross-entropy) (3.0.3)
[fastapi] Downloading cut_cross_entropy-25.1.1-py3-none-any.whl (22 kB)
[fastapi] Installing collected packages: cut-cross-entropy
[fastapi] Successfully installed cut-cross-entropy-25.1.1
[fastapi] ---> 8990460451c0
[fastapi] Step 8/13 : COPY src /workspace/src
[fastapi] ---> db1185be0544
[fastapi] Step 9/13 : COPY ds_config /workspace/ds_config
[fastapi] ---> aeb630dc222d
[fastapi] Step 10/13 : COPY ops/accelerate /workspace/ops/accelerate
[fastapi] ---> aa0e572d5906
[fastapi] Step 11/13 : COPY ops/entrypoint.sh /workspace/entrypoint.sh
[fastapi] ---> 55e1bbd4d3f6
[fastapi] Step 12/13 : RUN chmod +x /workspace/entrypoint.sh
[fastapi] ---> Running in 5fe11eeee2d7
[fastapi] ---> d9252b6c825d
[fastapi] Step 13/13 : ENTRYPOINT ["/workspace/entrypoint.sh"]
[fastapi] ---> Running in b957187fa234
[fastapi] ---> 56199e0044a1
[fastapi] {'aux': {'ID': 'sha256:56199e0044a14d049b97ed33a81a82a45be56d44367252af8571dbe6e9b6092c'}}Successfully built 56199e0044a1
[fastapi] Successfully tagged standalone-text-trainer:9575fdea-bce4-47c8-aeef-9cf8a82704c3
[fastapi] Docker image built successfully.
[fastapi] Container.wait() returned: {'StatusCode': 0}
[fastapi] Cleaning up
[fastapi] Cleaned up Docker resources.
[fastapi] Starting upload container hf-upload-6e657f07b31f4457bf17b5f6f50b8782 for task 067761fe-b567-44d7-8863-4cd41cc12261...
[hf-upload-6e]  adapter_config.json not found
[hf-upload-6e] README.md not found
[hf-upload-6e] Creating repo gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5DU5Qyae...
[hf-upload-6e] Uploading contents of /app/checkpoints/067761fe-b567-44d7-8863-4cd41cc12261/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5DU5Qyae to gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5DU5Qyae
[hf-upload-6e] Uploaded successfully to https://huggingface.co/gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5DU5Qyae
[hf-upload-6e] Deleted local folder: /app/checkpoints/067761fe-b567-44d7-8863-4cd41cc12261/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5DU5Qyae
[text-trainer] [main] task=InstructTextTask model=c53e93d87a4fe77f params~1.2B type=llama gpus=1
[text-trainer] [main] run (timeout 57m): /opt/axo/bin/python /workspace/src/tok_axolotl.py --model-path /cache/models/c53e93d87a4fe77f --data-path /cache/datasets/067761fe-b567-44d7-8863-4cd41cc12261_train_data.json --dataset-type {"system_prompt": "", "system_format": "{system}", "field_system": null, "field_instruction": "instruct", "field_input": "input", "field_output": "output", "format": null, "no_input_format": null, "field": null} --task-type InstructTextTask --seq-len 4096 --out-dir /workspace/run/tokenized/067761fe-b567-44d7-8863-4cd41cc12261
[text-trainer] Processing datasets during training can lead to VRAM instability. Please pre-process your dataset.
[text-trainer] Generating train split: 0 examples [00:00, ? examples/s]Generating train split: 19505 examples [00:00, 33304.29 examples/s]Generating train split: 19505 examples [00:00, 33121.48 examples/s]
[text-trainer] Dropped 184 long samples from dataset
[text-trainer] tokenized: {'n_raw': 19321, 'n_train': 18026, 'n_dev': 512, 'n_empty': 0, 'n_dupes': 783, 'len_p50': 425, 'len_p95': 1371, 'len_p99': 2631, 'len_max': 4070, 'seq_len': 4096}
[text-trainer] [main] run (timeout 56m): /usr/bin/python /workspace/src/train_sft.py --task-id 067761fe-b567-44d7-8863-4cd41cc12261 --model-path /cache/models/c53e93d87a4fe77f --base-model-id c53e93d87a4fe77f --output-dir /app/checkpoints/067761fe-b567-44d7-8863-4cd41cc12261/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5DU5Qyae --end-ts 1789470959.3868966 --num-gpus 1 --state-file /tmp/trainer_state.json --tokenized-dir /workspace/run/tokenized/067761fe-b567-44d7-8863-4cd41cc12261
[text-trainer] [2026-09-15 10:19:54,100] [INFO] [real_accelerator.py:219:get_accelerator] Setting ds_accelerator to cuda (auto detect)
[text-trainer] df: /root/.triton/autotune: No such file or directory
[text-trainer] You are attempting to use Flash Attention 2.0 with a model not initialized on GPU. Make sure to move the model to GPU after initializing it on CPU with `model.to('cuda')`.
[text-trainer] [sft 10:19:58] packing=False (len_p99=2631, attn=flash_attention_2)
[text-trainer] [sft 10:20:25] replan: t/step=1.60s total=834 decay@600 eval_every=69
[text-trainer] {'loss': 37.6454, 'grad_norm': 98.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 0.09}
[text-trainer] {'loss': 24.6757, 'grad_norm': 182.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 0.18}
[text-trainer] {'eval_loss': 2.022145417322463, 'eval_loss_tokw': 1.9116215705871582, 'eval_n': 512, 'eval_runtime': 4.0077, 'eval_samples_per_second': 127.754, 'eval_steps_per_second': 25.7, 'epoch': 0.25}
[text-trainer] [sft 10:21:47] exported (best@69) dev_loss=2.02215
[text-trainer] {'loss': 29.8349, 'grad_norm': 82.5, 'learning_rate': 4.759933806448394e-05, 'epoch': 0.27}
[text-trainer] {'loss': 22.2894, 'grad_norm': 139.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 0.36}
[text-trainer] {'loss': 26.3887, 'grad_norm': 82.5, 'learning_rate': 4.759933806448394e-05, 'epoch': 0.45}
[text-trainer] {'eval_loss': 1.8226945197870918, 'eval_loss_tokw': 1.739483118057251, 'eval_n': 512, 'eval_runtime': 4.0713, 'eval_samples_per_second': 125.757, 'eval_steps_per_second': 25.299, 'epoch': 0.5}
[text-trainer] [sft 10:23:20] exported (best@138) dev_loss=1.82269
[text-trainer] {'loss': 21.7644, 'grad_norm': 139.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 0.54}
[text-trainer] {'loss': 24.0581, 'grad_norm': 90.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 0.63}
[text-trainer] {'loss': 19.8472, 'grad_norm': 125.5, 'learning_rate': 4.759933806448394e-05, 'epoch': 0.72}
[text-trainer]   File "/workspace/src/train_sft.py", line 990, in <module>
[text-trainer]     main()
[text-trainer]   File "/workspace/src/train_sft.py", line 725, in main
[text-trainer]     trainer.train()
[text-trainer]   File "/usr/local/lib/python3.11/dist-packages/transformers/trainer.py", line 2245, in train
[text-trainer]     return inner_training_loop(
[text-trainer]            ^^^^^^^^^^^^^^^^^^^^
[text-trainer]   File "/usr/local/lib/python3.11/dist-packages/transformers/trainer.py", line 2560, in _inner_training_loop
[text-trainer]     tr_loss_step = self.training_step(model, inputs, num_items_in_batch)
[text-trainer]                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[text-trainer]   File "/usr/local/lib/python3.11/dist-packages/transformers/trainer.py", line 3782, in training_step
[text-trainer]     self.accelerator.backward(loss, **kwargs)
[text-trainer]   File "/usr/local/lib/python3.11/dist-packages/accelerate/accelerator.py", line 2454, in backward
[text-trainer]     loss.backward(**kwargs)
[text-trainer]   File "/usr/local/lib/python3.11/dist-packages/torch/_tensor.py", line 626, in backward
[text-trainer]     torch.autograd.backward(
[text-trainer]   File "/usr/local/lib/python3.11/dist-packages/torch/autograd/__init__.py", line 347, in backward
[text-trainer]     _engine_run_backward(
[text-trainer]   File "/usr/local/lib/python3.11/dist-packages/torch/autograd/graph.py", line 823, in _engine_run_backward
[text-trainer]     return Variable._execution_engine.run_backward(  # Calls into the C++ engine to run the backward pass
[text-trainer]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[text-trainer] torch.OutOfMemoryError: CUDA out of memory. Tried to allocate 8.91 GiB. GPU 0 has a total capacity of 79.19 GiB of which 6.56 GiB is free. Process 1 has 516.00 MiB memory in use. Including non-PyTorch memory, this process has 72.11 GiB memory in use. Of the allocated memory 58.62 GiB is allocated by PyTorch, and 12.76 GiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
[text-trainer] [main] attempt 1 rc=1
[text-trainer] [main] run (timeout 51m): /usr/bin/python /workspace/src/train_sft.py --task-id 067761fe-b567-44d7-8863-4cd41cc12261 --model-path /cache/models/c53e93d87a4fe77f --base-model-id c53e93d87a4fe77f --output-dir /app/checkpoints/067761fe-b567-44d7-8863-4cd41cc12261/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5DU5Qyae --end-ts 1789470959.3868966 --num-gpus 1 --state-file /tmp/trainer_state.json --tokenized-dir /workspace/run/tokenized/067761fe-b567-44d7-8863-4cd41cc12261
[text-trainer] [2026-09-15 10:24:36,432] [INFO] [real_accelerator.py:219:get_accelerator] Setting ds_accelerator to cuda (auto detect)
[text-trainer] You are attempting to use Flash Attention 2.0 with a model not initialized on GPU. Make sure to move the model to GPU after initializing it on CPU with `model.to('cuda')`.
[text-trainer] [sft 10:24:37] packing=False (len_p99=2631, attn=flash_attention_2)
[text-trainer] [sft 10:25:10] replan: t/step=2.02s total=846 decay@609 eval_every=70
[text-trainer] {'loss': 95.0279, 'grad_norm': 262.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 0.09}
[text-trainer] {'loss': 61.9572, 'grad_norm': 466.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 0.18}
[text-trainer] {'eval_loss': 2.0094923303877295, 'eval_loss_tokw': 1.927204966545105, 'eval_n': 512, 'eval_runtime': 6.6801, 'eval_samples_per_second': 76.645, 'eval_steps_per_second': 38.323, 'epoch': 0.25}
[text-trainer] [sft 10:27:08] exported (best@70) dev_loss=2.00949
[text-trainer] {'loss': 74.7517, 'grad_norm': 217.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 0.27}
[text-trainer] {'loss': 55.7287, 'grad_norm': 360.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 0.36}
[text-trainer] {'loss': 66.1082, 'grad_norm': 196.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 0.44}
[text-trainer] {'eval_loss': 1.8279655571744797, 'eval_loss_tokw': 1.77685546875, 'eval_n': 512, 'eval_runtime': 6.6468, 'eval_samples_per_second': 77.029, 'eval_steps_per_second': 38.515, 'epoch': 0.5}
[text-trainer] [sft 10:29:22] exported (best@140) dev_loss=1.82797
[text-trainer] {'loss': 54.3773, 'grad_norm': 384.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 0.53}
[text-trainer] {'loss': 60.5489, 'grad_norm': 231.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 0.62}
[text-trainer] {'loss': 49.9579, 'grad_norm': 340.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 0.71}
[text-trainer] {'eval_loss': 1.6952188291305674, 'eval_loss_tokw': 1.6552882194519043, 'eval_n': 512, 'eval_runtime': 6.714, 'eval_samples_per_second': 76.259, 'eval_steps_per_second': 38.129, 'epoch': 0.75}
[text-trainer] [sft 10:31:53] exported (best@210) dev_loss=1.69522
[text-trainer] {'loss': 57.6197, 'grad_norm': 178.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 0.8}
[text-trainer] {'loss': 48.3615, 'grad_norm': 342.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 0.89}
[text-trainer] {'loss': 52.6519, 'grad_norm': 204.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 0.98}
[text-trainer] {'eval_loss': 1.6035339261038644, 'eval_loss_tokw': 1.5568625926971436, 'eval_n': 512, 'eval_runtime': 6.7975, 'eval_samples_per_second': 75.322, 'eval_steps_per_second': 37.661, 'epoch': 0.99}
[text-trainer] [sft 10:34:05] exported (best@280) dev_loss=1.60353
[text-trainer] {'loss': 45.6835, 'grad_norm': 194.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 1.07}
[text-trainer] {'loss': 24.277, 'grad_norm': 221.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 1.16}
[text-trainer] {'loss': 36.8034, 'grad_norm': 173.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 1.24}
[text-trainer] {'eval_loss': 1.5884376393078128, 'eval_loss_tokw': 1.537774920463562, 'eval_n': 512, 'eval_runtime': 6.7289, 'eval_samples_per_second': 76.089, 'eval_steps_per_second': 38.045, 'epoch': 1.24}
[text-trainer] [sft 10:36:35] exported (best@350) dev_loss=1.58844
[text-trainer] {'loss': 23.595, 'grad_norm': 234.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 1.33}
[text-trainer] {'loss': 35.6723, 'grad_norm': 201.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 1.42}
[text-trainer] {'eval_loss': 1.4972235184943088, 'eval_loss_tokw': 1.4596350193023682, 'eval_n': 512, 'eval_runtime': 6.9027, 'eval_samples_per_second': 74.174, 'eval_steps_per_second': 37.087, 'epoch': 1.49}
[text-trainer] [sft 10:38:48] exported (best@420) dev_loss=1.49722
[text-trainer] {'loss': 23.1075, 'grad_norm': 228.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 1.51}
[text-trainer] {'loss': 34.0197, 'grad_norm': 188.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 1.6}
[text-trainer] {'loss': 23.4505, 'grad_norm': 193.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 1.69}
[text-trainer] {'eval_loss': 1.4349711634965274, 'eval_loss_tokw': 1.4079232215881348, 'eval_n': 512, 'eval_runtime': 7.091, 'eval_samples_per_second': 72.204, 'eval_steps_per_second': 36.102, 'epoch': 1.74}
[text-trainer] [sft 10:41:11] exported (best@490) dev_loss=1.43497
[text-trainer] {'loss': 33.9058, 'grad_norm': 202.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 1.78}
[text-trainer] {'loss': 22.9315, 'grad_norm': 195.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 1.87}
[text-trainer] {'loss': 27.9194, 'grad_norm': 209.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 1.96}
[text-trainer] {'eval_loss': 1.3602243839745825, 'eval_loss_tokw': 1.323460340499878, 'eval_n': 512, 'eval_runtime': 6.9443, 'eval_samples_per_second': 73.73, 'eval_steps_per_second': 36.865, 'epoch': 1.99}
[text-trainer] [sft 10:43:33] exported (best@560) dev_loss=1.36022
[text-trainer] {'loss': 25.9822, 'grad_norm': 140.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 2.05}
[text-trainer] {'loss': 6.8201, 'grad_norm': 161.0, 'learning_rate': 4.759933806448394e-05, 'epoch': 2.13}
[text-trainer] {'loss': 19.2278, 'grad_norm': 157.0, 'learning_rate': 4.4887983364608274e-05, 'epoch': 2.22}
[text-trainer] {'eval_loss': 1.4855340539951385, 'eval_loss_tokw': 1.4323979616165161, 'eval_n': 512, 'eval_runtime': 7.26, 'eval_samples_per_second': 70.523, 'eval_steps_per_second': 35.262, 'epoch': 2.24}
[text-trainer] {'loss': 6.4697, 'grad_norm': 216.0, 'learning_rate': 4.0369058864815494e-05, 'epoch': 2.31}
[text-trainer] {'loss': 15.8607, 'grad_norm': 144.0, 'learning_rate': 3.585013436502271e-05, 'epoch': 2.4}
[text-trainer] {'loss': 6.092, 'grad_norm': 200.0, 'learning_rate': 3.133120986522993e-05, 'epoch': 2.49}
[text-trainer] {'eval_loss': 1.415170583646571, 'eval_loss_tokw': 1.3732532262802124, 'eval_n': 512, 'eval_runtime': 7.1449, 'eval_samples_per_second': 71.659, 'eval_steps_per_second': 35.83, 'epoch': 2.49}
[text-trainer] {'loss': 17.5921, 'grad_norm': 163.0, 'learning_rate': 2.6812285365437155e-05, 'epoch': 2.58}
[text-trainer] {'loss': 5.6685, 'grad_norm': 169.0, 'learning_rate': 2.2293360865644375e-05, 'epoch': 2.67}
[text-trainer] {'eval_loss': 1.3486750885903902, 'eval_loss_tokw': 1.3386595249176025, 'eval_n': 512, 'eval_runtime': 7.2484, 'eval_samples_per_second': 70.636, 'eval_steps_per_second': 35.318, 'epoch': 2.74}
[text-trainer] [sft 10:50:40] exported (best@770) dev_loss=1.34868
[text-trainer] {'loss': 15.7819, 'grad_norm': 159.0, 'learning_rate': 1.7774436365851598e-05, 'epoch': 2.76}
[text-trainer] {'loss': 5.1092, 'grad_norm': 169.0, 'learning_rate': 1.325551186605882e-05, 'epoch': 2.85}
[text-trainer] {'loss': 10.2492, 'grad_norm': 134.0, 'learning_rate': 8.736587366266038e-06, 'epoch': 2.93}
[text-trainer] {'eval_loss': 1.3185257067674243, 'eval_loss_tokw': 1.304649829864502, 'eval_n': 512, 'eval_runtime': 7.2403, 'eval_samples_per_second': 70.716, 'eval_steps_per_second': 35.358, 'epoch': 2.99}
[text-trainer] [sft 10:52:51] exported (best@840) dev_loss=1.31853
[text-trainer] {'train_runtime': 1697.349, 'train_samples_per_second': 31.86, 'train_steps_per_second': 0.497, 'train_loss': 34.012657464186915, 'epoch': 3.0}
[text-trainer] [sft 10:53:56] soup: 2/4 ckpts -> dev 1.26004 (best single 1.31853)
[text-trainer] [sft 10:53:56] final: best_ondisk=1.31853 raw=1.31876 ema=1.29645 soup=1.26004 -> pick soup
[text-trainer] [sft 10:53:59] exported (soup-final) dev_loss=1.26004
[text-trainer] [sft 10:53:59] done
[text-trainer] [main] finished ok=True elapsed=35m