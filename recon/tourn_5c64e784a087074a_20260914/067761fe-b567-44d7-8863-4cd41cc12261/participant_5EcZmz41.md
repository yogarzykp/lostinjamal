# Loki — task 067761fe-b567-44d7-8863-4cd41cc12261 — hotkey 5EcZmz41oFGaJVte8DEzuGd8QyBBxjhTobhrK4A5y4b1Q24Y
fetched 2026-09-19T05:01:30+00:00  lines=377  hit_page_cap=False  containers=['downloader-067761fe-b567-44d7-8863-4cd41cc12261-22e883ea', 'fastapi', 'hf-upload-362e7d993ed141d886982acdfe0e1ee4', 'text-trainer-9818364f88d64715954455c2f3aa70c9']

[downloader-0] Downloading datasets to: /cache/datasets
[downloader-0] Downloading models to: /cache/models
[downloader-0] Model already cached at /cache/models/c53e93d87a4fe77f.
[downloader-0] Skipping download.
[downloader-0] Model path: /cache/models/c53e93d87a4fe77f
[downloader-0] Dataset path: /cache/datasets
[fastapi] Repository cloned successfully
[fastapi] Running Cache Download Container
[fastapi] Starting downloader container: downloader-067761fe-b567-44d7-8863-4cd41cc12261-22e883ea
[fastapi] Download completed successfully for task 067761fe-b567-44d7-8863-4cd41cc12261
[fastapi] Building Docker image 'standalone-text-trainer:fe569850-7e3e-4ac2-a050-28d230475fca' (timeout=1800s)...
[fastapi] Step 1/10 : FROM runpod/pytorch:1.1.0-cu1281-torch291-ubuntu2204@sha256:a9320617b09069038f677ff7dcc2262faba42bc2bfa2125d6c733285946d14ac
[fastapi] ---> 3b600cc49e85
[fastapi] Step 2/10 : ENV PYTHONUNBUFFERED=1     PIP_NO_CACHE_DIR=1     HF_HUB_DISABLE_TELEMETRY=1     HF_HUB_DISABLE_SYMLINKS_WARNING=1     TOKENIZERS_PARALLELISM=false     PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True     HF_HUB_OFFLINE=1     TRANSFORMERS_OFFLINE=1
[fastapi] ---> Running in 29a5a1d1ddcd
[fastapi] ---> 7786d62c1a85
[fastapi] Step 3/10 : RUN pip install --no-cache-dir uv     && uv pip install --system --no-cache         torch==2.9.1         transformers==5.12.1         tokenizers==0.22.2         peft==0.19.1         trl==1.5.1         liger-kernel==0.8.1         accelerate==1.13.0         datasets==4.8.5         safetensors==0.8.0         sentencepiece==0.2.0         einops==0.8.1         textstat==0.7.8 langcheck==0.9.0 RestrictedPython==8.0
[fastapi] ---> Running in ea09bdcabcb5
[fastapi] Collecting uv
[fastapi] Downloading uv-0.12.14-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] Downloading uv-0.12.14-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.0 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 20.0/20.0 MB 219.2 MB/s  0:00:00
[fastapi] Installing collected packages: uv
[fastapi] Successfully installed uv-0.12.14
[fastapi] [91mUsing Python 3.12.13 environment at: /usr
[fastapi] [0m[91mResolved 124 packages in 1.21s
[fastapi] [0m[91m   Building rouge-score==0.1.2
[fastapi] [0m[91m   Building antlr4-python3-runtime==4.9.3
[fastapi] [0m[91mDownloading numpy (15.9MiB)
[fastapi] [0m[91mDownloading aiohttp (1.7MiB)
[fastapi] [0m[91mDownloading sentencepiece (1.2MiB)
[fastapi] [0m[91mDownloading pyphen (2.0MiB)
[fastapi] [0m[91mDownloading transformers (10.6MiB)
[fastapi] [0m[91mDownloading hf-xet (4.3MiB)
[fastapi] [0m[91mDownloading dash (8.5MiB)
[fastapi] [0m[91mDownloading scipy (33.7MiB)
[fastapi] [0m[91mDownloading pyarrow (47.8MiB)
[fastapi] [0m[91mDownloading tokenizers (3.1MiB)
[fastapi] [0m[91mDownloading plotly (8.6MiB)
[fastapi] [0m[91mDownloading pandas (10.5MiB)
[fastapi] [0m[91mDownloading pydantic-core (2.0MiB)
[fastapi] [0m[91mDownloading openai (1.9MiB)
[fastapi] [0m[91mDownloading scikit-learn (8.7MiB)
[fastapi] [0m[91mDownloading nltk (1.7MiB)
[fastapi] [0m[91m Downloaded sentencepiece
[fastapi] [0m[91m Downloaded aiohttp
[fastapi] [0m[91m Downloaded pyphen
[fastapi] [0m[91m Downloaded pydantic-core
[fastapi] [0m[91m Downloaded nltk
[fastapi] [0m[91m Downloaded openai
[fastapi] [0m[91m Downloaded tokenizers
[fastapi] [0m[91m Downloaded hf-xet
[fastapi] [0m[91m      Built rouge-score==0.1.2
[fastapi] [0m[91m      Built antlr4-python3-runtime==4.9.3
[fastapi] [0m[91m Downloaded plotly
[fastapi] [0m[91m Downloaded scikit-learn
[fastapi] [0m[91m Downloaded dash
[fastapi] [0m[91m Downloaded transformers
[fastapi] [0m[91m Downloaded pandas
[fastapi] [0m[91m Downloaded numpy
[fastapi] [0m[91m Downloaded scipy
[fastapi] [0m[91m Downloaded pyarrow
[fastapi] [0m[91mPrepared 80 packages in 605ms
[fastapi] [0m[91mUninstalled 1 package in 30ms
[fastapi] [0m[91mInstalled 80 packages in 78ms
[fastapi] + absl-py==2.5.0
[fastapi] + accelerate==1.13.0
[fastapi] [0m[91m+ aiohappyeyeballs==2.7.1
[fastapi] + aiohttp==3.14.3
[fastapi] + aiosignal==1.4.0
[fastapi] + annotated-doc[0m[91m==0.0.5
[fastapi] +[0m[91m annotated-types==0.8.0
[fastapi] + antlr4-python3-runtime==4.9.3
[fastapi] + [0m[91mblinker==1.9.0
[fastapi] + click==8.5.0
[fastapi] + cloudpickle==3.1.2
[fastapi] + cmudict==1.1.3
[fastapi] [0m[91m+ dash==4.4.[0m[91m1
[fastapi] + datasets==4.8.5[0m[91m
[fastapi] + dill==0.4[0m[91m.1
[fastapi] [0m[91m + [0m[91meinops==0[0m[91m.8.1
[fastapi] + flask==[0m[91m3.1.3
[fastapi] + frozenlist==1.8.0
[fastapi] - fsspec==2026.[0m[91m7.0
[fastapi] + [0m[91mfsspec==2026.2.[0m[91m0
[fastapi] + gdown==[0m[91m6.2.0
[fastapi] [0m[91m + hf-xet==1.6.0
[fastapi] [0m[91m+ httpcore2==2[0m[91m.13.0
[fastapi] +[0m[91m [0m[91mhttpx2==2.13.[0m[91m0
[fastapi] [0m[91m+ [0m[91mhuggingface-hub==1[0m[91m.31.[0m[91m0
[fastapi] +[0m[91m [0m[91mimportlib-metadata==9[0m[91m.0[0m[91m.1
[fastapi] +[0m[91m importlib-resources==[0m[91m7.1.0
[fastapi] + itsdangerous==2.2.0[0m[91m
[fastapi] +[0m[91m jaconv[0m[91m==0.5.0[0m[91m
[fastapi] [0m[91m+[0m[91m janus==[0m[91m2.0[0m[91m.0[0m[91m
[fastapi] + jiter==0.17.0
[fastapi] + joblib==1.6.0
[fastapi] [0m[91m+ langcheck[0m[91m==0.[0m[91m9.0[0m[91m
[fastapi] +[0m[91m liger-kernel[0m[91m==0.8.1[0m[91m
[fastapi] + markdown-it-py==4.2[0m[91m.[0m[91m0
[fastapi] +[0m[91m [0m[91mmdurl==[0m[91m0.1.[0m[91m2[0m[91m
[fastapi] +[0m[91m multidict==6[0m[91m.8.0
[fastapi] + multiprocess[0m[91m==0.[0m[91m70.19[0m[91m
[fastapi] + narwhals[0m[91m==2.26.0
[fastapi] + nest-asyncio==1[0m[91m.6.0
[fastapi] + nlpaug==1[0m[91m.1.11
[fastapi] + nltk==3.10.3
[fastapi] + [0m[91mnumpy==2[0m[91m.5.3
[fastapi] [0m[91m +[0m[91m [0m[91momegaconf==2[0m[91m.3.[0m[91m1
[fastapi] [0m[91m+ [0m[91mopenai[0m[91m==3.14[0m[91m.0[0m[91m
[fastapi] +[0m[91m [0m[91mpandas==[0m[91m3.0.[0m[91m5[0m[91m
[fastapi] +[0m[91m peft[0m[91m==0.[0m[91m19.1
[fastapi] +[0m[91m plotly==7.0.0
[fastapi] + propcache==0.[0m[91m5.2
[fastapi] [0m[91m + pyarrow==25.0.1[0m[91m
[fastapi] + [0m[91mpydantic==2[0m[91m.13.5
[fastapi] [0m[91m + pydantic-core==2.46.5
[fastapi] + pyphen==0.18.1[0m[91m
[fastapi] + pysocks==[0m[91m1.[0m[91m7.1
[fastapi] [0m[91m [0m[91m+ regex==2026.9.10
[fastapi] + [0m[91mrestrictedpython==8[0m[91m.[0m[91m0
[fastapi] + [0m[91mretrying==1[0m[91m.4.2
[fastapi] + rich==15.0.[0m[91m0
[fastapi] + rouge-score==0.1.2
[fastapi] [0m[91m+ safetensors==0.8.0[0m[91m
[fastapi] [0m[91m + [0m[91mscikit-learn==[0m[91m1.9.1[0m[91m
[fastapi] + scipy==1.18.1
[fastapi] + sentence-transformers[0m[91m==6.0[0m[91m.1[0m[91m
[fastapi] + [0m[91msentencepiece[0m[91m==0.2.[0m[91m0
[fastapi] + shellingham==1.5.4
[fastapi] + six[0m[91m==1.17.0
[fastapi] + [0m[91msniffio==[0m[91m1.3.1[0m[91m
[fastapi] +[0m[91m [0m[91mtabulate[0m[91m==0.10.0
[fastapi] + [0m[91mtextstat==[0m[91m0.7.8[0m[91m
[fastapi] +[0m[91m threadpoolctl[0m[91m==3.6[0m[91m.[0m[91m0
[fastapi] [0m[91m+ tokenizers[0m[91m==[0m[91m0.22.[0m[91m2[0m[91m
[fastapi] +[0m[91m [0m[91mtqdm==4[0m[91m.70[0m[91m.1
[fastapi] [0m[91m+[0m[91m transformers[0m[91m==5.12.1
[fastapi] + trl[0m[91m==[0m[91m1.5.[0m[91m1
[fastapi] [0m[91m+[0m[91m [0m[91mtruststore==0[0m[91m.10.4[0m[91m
[fastapi] [0m[91m+[0m[91m [0m[91mtyper==0.27.2
[fastapi] +[0m[91m typing-inspection==0.4.4
[fastapi] +[0m[91m werkzeug==3.1.[0m[91m8
[fastapi] + [0m[91mxxhash==4[0m[91m.0.1[0m[91m
[fastapi] [0m[91m + [0m[91myarl[0m[91m==1.24[0m[91m.5
[fastapi] [0m[91m +[0m[91m zipp[0m[91m==4[0m[91m.1.[0m[91m0
[fastapi] [0m ---> 37604aef2ef9
[fastapi] Step 4/10 : RUN ABI=$(python -c "import torch; print('TRUE' if torch._C._GLIBCXX_USE_CXX11_ABI else 'FALSE')")     && echo "torch cxx11 ABI: ${ABI}"     && uv pip install --system --no-cache         "https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu12torch2.9cxx11abi${ABI}-cp312-cp312-linux_x86_64.whl"     && python -c "import flash_attn; from flash_attn import flash_attn_func, flash_attn_varlen_func; print('flash-attn:', flash_attn.__version__)"
[fastapi] ---> Running in 29d54456b527
[fastapi] [91m[W915 11:04:25.703853964 AllocatorConfig.cpp:28] Warning: PYTORCH_CUDA_ALLOC_CONF is deprecated, use PYTORCH_ALLOC_CONF instead (function operator())
[fastapi] [0mtorch cxx11 ABI: TRUE
[fastapi] [91mUsing Python 3.12.13 environment at: /usr
[fastapi] [0m[91mResolved 28 packages in 3.07s
[fastapi] [0m[91mDownloading flash-attn (242.0MiB)
[fastapi] [0m[91m Downloaded flash-attn
[fastapi] [0m[91mPrepared 1 package in 2.33s
[fastapi] [0m[91mInstalled 1 package in 11ms
[fastapi] + flash-attn==2.8.3+cu12torch2.9cxx11abitrue (from https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu12torch2.9cxx11abiTRUE-cp312-cp312-linux_x86_64.whl)
[fastapi] [0mflash-attn: 2.8.3
[fastapi] [91m[W915 11:04:32.608227695 AllocatorConfig.cpp:28] Warning: PYTORCH_CUDA_ALLOC_CONF is deprecated, use PYTORCH_ALLOC_CONF instead (function operator())
[fastapi] [0m ---> f1c675f00bc2
[fastapi] Step 5/10 : RUN TORCH_CUDA_ARCH_LIST="8.0;9.0+PTX" MAX_JOBS=4     pip install --no-cache-dir --no-build-isolation     causal-conv1d==1.6.2.post1 mamba-ssm==2.3.2.post1
[fastapi] ---> Running in bb6e8843d33f
[fastapi] Collecting causal-conv1d==1.6.2.post1
[fastapi] Downloading causal_conv1d-1.6.2.post1.tar.gz (29 kB)
[fastapi] Preparing metadata (pyproject.toml): started
[fastapi] Preparing metadata (pyproject.toml): finished with status 'done'
[fastapi] Collecting mamba-ssm==2.3.2.post1
[fastapi] Downloading mamba_ssm-2.3.2.post1.tar.gz (216 kB)
[fastapi] Preparing metadata (pyproject.toml): started
[fastapi] Preparing metadata (pyproject.toml): finished with status 'done'
[fastapi] Requirement already satisfied: torch in ./usr/local/lib/python3.12/dist-packages (from causal-conv1d==1.6.2.post1) (2.9.1+cu128)
[fastapi] Requirement already satisfied: packaging in ./usr/local/lib/python3.12/dist-packages (from causal-conv1d==1.6.2.post1) (26.3)
[fastapi] Collecting ninja (from causal-conv1d==1.6.2.post1)
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (5.4 kB)
[fastapi] Collecting tilelang==0.1.8 (from mamba-ssm==2.3.2.post1)
[fastapi] Downloading tilelang-0.1.8-cp38-abi3-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (15 kB)
[fastapi] Collecting apache-tvm-ffi<=0.1.9 (from mamba-ssm==2.3.2.post1)
[fastapi] Downloading apache_tvm_ffi-0.1.9-cp312-abi3-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl.metadata (6.1 kB)
[fastapi] Collecting quack-kernels>=0.3.4 (from mamba-ssm==2.3.2.post1)
[fastapi] Downloading quack_kernels-0.6.5-py3-none-any.whl.metadata (834 bytes)
[fastapi] Requirement already satisfied: triton>=3.5.0 in ./usr/local/lib/python3.12/dist-packages (from mamba-ssm==2.3.2.post1) (3.5.1)
[fastapi] Requirement already satisfied: einops in ./usr/local/lib/python3.12/dist-packages (from mamba-ssm==2.3.2.post1) (0.8.1)
[fastapi] Requirement already satisfied: transformers in ./usr/local/lib/python3.12/dist-packages (from mamba-ssm==2.3.2.post1) (5.12.1)
[fastapi] Requirement already satisfied: setuptools>=61.0.0 in ./usr/local/lib/python3.12/dist-packages (from mamba-ssm==2.3.2.post1) (84.0.0)
[fastapi] Collecting torch-c-dlpack-ext (from tilelang==0.1.8->mamba-ssm==2.3.2.post1)
[fastapi] Downloading torch_c_dlpack_ext-0.1.5-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl.metadata (14 kB)
[fastapi] Requirement already satisfied: cloudpickle in ./usr/local/lib/python3.12/dist-packages (from tilelang==0.1.8->mamba-ssm==2.3.2.post1) (3.1.2)
[fastapi] Collecting ml-dtypes (from tilelang==0.1.8->mamba-ssm==2.3.2.post1)
[fastapi] Downloading ml_dtypes-0.6.0-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (8.8 kB)
[fastapi] Requirement already satisfied: numpy>=1.23.5 in ./usr/local/lib/python3.12/dist-packages (from tilelang==0.1.8->mamba-ssm==2.3.2.post1) (2.5.3)
[fastapi] Requirement already satisfied: psutil in ./usr/local/lib/python3.12/dist-packages (from tilelang==0.1.8->mamba-ssm==2.3.2.post1) (7.2.2)
[fastapi] Requirement already satisfied: tqdm>=4.62.3 in ./usr/local/lib/python3.12/dist-packages (from tilelang==0.1.8->mamba-ssm==2.3.2.post1) (4.70.1)
[fastapi] Requirement already satisfied: typing-extensions>=4.10.0 in ./usr/local/lib/python3.12/dist-packages (from tilelang==0.1.8->mamba-ssm==2.3.2.post1) (4.16.0)
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
[fastapi] Collecting protobuf>=4.21.12 (from nvidia-cutlass-dsl-libs-base==4.7.1->nvidia-cutlass-dsl>=4.7->quack-kernels>=0.3.4->mamba-ssm==2.3.2.post1)
[fastapi] Downloading protobuf-7.36.1-cp310-abi3-manylinux2014_x86_64.whl.metadata (595 bytes)
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
[fastapi] Requirement already satisfied: filelock in ./usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (3.32.3)
[fastapi] Requirement already satisfied: sympy>=1.13.3 in ./usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (1.14.0)
[fastapi] Requirement already satisfied: networkx>=2.5.1 in ./usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (3.6.1)
[fastapi] Requirement already satisfied: jinja2 in ./usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (3.1.6)
[fastapi] Requirement already satisfied: fsspec>=0.8.5 in ./usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (2026.2.0)
[fastapi] Requirement already satisfied: nvidia-cuda-nvrtc-cu12==12.8.93 in ./usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (12.8.93)
[fastapi] Requirement already satisfied: nvidia-cuda-runtime-cu12==12.8.90 in ./usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (12.8.90)
[fastapi] Requirement already satisfied: nvidia-cuda-cupti-cu12==12.8.90 in ./usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (12.8.90)
[fastapi] Requirement already satisfied: nvidia-cudnn-cu12==9.10.2.21 in ./usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (9.10.2.21)
[fastapi] Requirement already satisfied: nvidia-cublas-cu12==12.8.4.1 in ./usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (12.8.4.1)
[fastapi] Requirement already satisfied: nvidia-cufft-cu12==11.3.3.83 in ./usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (11.3.3.83)
[fastapi] Requirement already satisfied: nvidia-curand-cu12==10.3.9.90 in ./usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (10.3.9.90)
[fastapi] Requirement already satisfied: nvidia-cusolver-cu12==11.7.3.90 in ./usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (11.7.3.90)
[fastapi] Requirement already satisfied: nvidia-cusparse-cu12==12.5.8.93 in ./usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (12.5.8.93)
[fastapi] Requirement already satisfied: nvidia-cusparselt-cu12==0.7.1 in ./usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (0.7.1)
[fastapi] Requirement already satisfied: nvidia-nccl-cu12==2.27.5 in ./usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (2.27.5)
[fastapi] Requirement already satisfied: nvidia-nvshmem-cu12==3.3.20 in ./usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (3.3.20)
[fastapi] Requirement already satisfied: nvidia-nvtx-cu12==12.8.90 in ./usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (12.8.90)
[fastapi] Requirement already satisfied: nvidia-nvjitlink-cu12==12.8.93 in ./usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (12.8.93)
[fastapi] Requirement already satisfied: nvidia-cufile-cu12==1.13.1.3 in ./usr/local/lib/python3.12/dist-packages (from torch->causal-conv1d==1.6.2.post1) (1.13.1.3)
[fastapi] Requirement already satisfied: mpmath<1.4,>=1.1.0 in ./usr/local/lib/python3.12/dist-packages (from sympy>=1.13.3->torch->causal-conv1d==1.6.2.post1) (1.3.0)
[fastapi] Requirement already satisfied: MarkupSafe>=2.0 in ./usr/local/lib/python3.12/dist-packages (from jinja2->torch->causal-conv1d==1.6.2.post1) (3.0.3)
[fastapi] Requirement already satisfied: huggingface-hub<2.0,>=1.5.0 in ./usr/local/lib/python3.12/dist-packages (from transformers->mamba-ssm==2.3.2.post1) (1.31.0)
[fastapi] Requirement already satisfied: pyyaml>=5.1 in ./usr/local/lib/python3.12/dist-packages (from transformers->mamba-ssm==2.3.2.post1) (6.0.3)
[fastapi] Requirement already satisfied: regex>=2025.10.22 in ./usr/local/lib/python3.12/dist-packages (from transformers->mamba-ssm==2.3.2.post1) (2026.9.10)
[fastapi] Requirement already satisfied: tokenizers<=0.23.0,>=0.22.0 in ./usr/local/lib/python3.12/dist-packages (from transformers->mamba-ssm==2.3.2.post1) (0.22.2)
[fastapi] Requirement already satisfied: typer in ./usr/local/lib/python3.12/dist-packages (from transformers->mamba-ssm==2.3.2.post1) (0.27.2)
[fastapi] Requirement already satisfied: safetensors>=0.4.3 in ./usr/local/lib/python3.12/dist-packages (from transformers->mamba-ssm==2.3.2.post1) (0.8.0)
[fastapi] Requirement already satisfied: click<9.0.0,>=8.4.2 in ./usr/local/lib/python3.12/dist-packages (from huggingface-hub<2.0,>=1.5.0->transformers->mamba-ssm==2.3.2.post1) (8.5.0)
[fastapi] Requirement already satisfied: hf-xet<2.0.0,>=1.5.2 in ./usr/local/lib/python3.12/dist-packages (from huggingface-hub<2.0,>=1.5.0->transformers->mamba-ssm==2.3.2.post1) (1.6.0)
[fastapi] Requirement already satisfied: httpx<1,>=0.23.0 in ./usr/local/lib/python3.12/dist-packages (from huggingface-hub<2.0,>=1.5.0->transformers->mamba-ssm==2.3.2.post1) (0.28.1)
[fastapi] Requirement already satisfied: anyio in ./usr/local/lib/python3.12/dist-packages (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers->mamba-ssm==2.3.2.post1) (4.14.2)
[fastapi] Requirement already satisfied: certifi in ./usr/local/lib/python3.12/dist-packages (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers->mamba-ssm==2.3.2.post1) (2026.7.22)
[fastapi] Requirement already satisfied: httpcore==1.* in ./usr/local/lib/python3.12/dist-packages (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers->mamba-ssm==2.3.2.post1) (1.0.9)
[fastapi] Requirement already satisfied: idna in ./usr/local/lib/python3.12/dist-packages (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers->mamba-ssm==2.3.2.post1) (3.19)
[fastapi] Requirement already satisfied: h11>=0.16 in ./usr/local/lib/python3.12/dist-packages (from httpcore==1.*->httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers->mamba-ssm==2.3.2.post1) (0.16.0)
[fastapi] Requirement already satisfied: shellingham>=1.3.0 in ./usr/local/lib/python3.12/dist-packages (from typer->transformers->mamba-ssm==2.3.2.post1) (1.5.4)
[fastapi] Requirement already satisfied: rich>=13.8.0 in ./usr/local/lib/python3.12/dist-packages (from typer->transformers->mamba-ssm==2.3.2.post1) (15.0.0)
[fastapi] Requirement already satisfied: annotated-doc>=0.0.2 in ./usr/local/lib/python3.12/dist-packages (from typer->transformers->mamba-ssm==2.3.2.post1) (0.0.5)
[fastapi] Requirement already satisfied: markdown-it-py>=2.2.0 in ./usr/local/lib/python3.12/dist-packages (from rich>=13.8.0->typer->transformers->mamba-ssm==2.3.2.post1) (4.2.0)
[fastapi] Requirement already satisfied: pygments<3.0.0,>=2.13.0 in ./usr/local/lib/python3.12/dist-packages (from rich>=13.8.0->typer->transformers->mamba-ssm==2.3.2.post1) (2.21.0)
[fastapi] Requirement already satisfied: mdurl~=0.1 in ./usr/local/lib/python3.12/dist-packages (from markdown-it-py>=2.2.0->rich>=13.8.0->typer->transformers->mamba-ssm==2.3.2.post1) (0.1.2)
[fastapi] Downloading tilelang-0.1.8-cp38-abi3-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (43.5 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 43.5/43.5 MB 331.2 MB/s  0:00:00
[fastapi] Downloading apache_tvm_ffi-0.1.9-cp312-abi3-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (2.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.3/2.3 MB 669.4 MB/s  0:00:00
[fastapi] Downloading z3_solver-4.15.4.0-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (29.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 29.3/29.3 MB 418.6 MB/s  0:00:00
[fastapi] Downloading quack_kernels-0.6.5-py3-none-any.whl (729 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 729.6/729.6 kB 822.9 MB/s  0:00:00
[fastapi] Downloading nvidia_cutlass_dsl-4.7.1-py3-none-any.whl (10 kB)
[fastapi] Downloading nvidia_cutlass_dsl_libs_base-4.7.1-cp312-cp312-manylinux_2_28_x86_64.whl (2.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.8/2.8 MB 357.1 MB/s  0:00:00
[fastapi] Downloading nvidia_cutlass_dsl_libs_core-4.7.1-py3-none-any.whl (1.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 830.5 MB/s  0:00:00
[fastapi] Downloading nvidia_cutlass_dsl_libs_cu12-4.7.1-cp312-cp312-manylinux_2_28_x86_64.whl (88.7 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 88.7/88.7 MB 299.5 MB/s  0:00:00
[fastapi] Downloading nvidia_cuda_nvdisasm-13.4.49-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (5.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.2/5.2 MB 412.4 MB/s  0:00:00
[fastapi] Downloading cuda_python-13.4.1-py3-none-any.whl (7.6 kB)
[fastapi] Downloading cuda_bindings-13.4.1-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (7.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.2/7.2 MB 364.7 MB/s  0:00:00
[fastapi] Downloading cuda_core-1.2.0-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (6.6 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.6/6.6 MB 296.3 MB/s  0:00:00
[fastapi] Downloading cuda_pathfinder-1.8.1-py3-none-any.whl (62 kB)
[fastapi] Downloading protobuf-7.36.1-cp310-abi3-manylinux2014_x86_64.whl (343 kB)
[fastapi] Downloading ml_dtypes-0.6.0-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (409 kB)
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (183 kB)
[fastapi] Downloading torch_c_dlpack_ext-0.1.5-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (897 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 897.8/897.8 kB 835.7 MB/s  0:00:00
[fastapi] Building wheels for collected packages: causal-conv1d, mamba-ssm
[fastapi] Building wheel for causal-conv1d (pyproject.toml): started
[fastapi] Building wheel for causal-conv1d (pyproject.toml): finished with status 'done'
[fastapi] Created wheel for causal-conv1d: filename=causal_conv1d-1.6.2.post1-cp312-cp312-linux_x86_64.whl size=193795077 sha256=3d09789a5df2760a59c2064c4570a4ccd30315943581e9553eb1f412cd9e25a6
[fastapi] Stored in directory: /tmp/pip-ephem-wheel-cache-hx_tv2db/wheels/ea/f0/26/5d87ae05a302e6dc8016c50cd8c7ee779585f593b9580e7cf8
[fastapi] Building wheel for mamba-ssm (pyproject.toml): started
[fastapi] Building wheel for mamba-ssm (pyproject.toml): finished with status 'done'
[fastapi] Created wheel for mamba-ssm: filename=mamba_ssm-2.3.2.post1-cp312-cp312-linux_x86_64.whl size=322246976 sha256=8fd21085d668a3bdbb1f7903c81f64434d7ed2c763240f8328a465a42370a7b6
[fastapi] Stored in directory: /tmp/pip-ephem-wheel-cache-hx_tv2db/wheels/da/67/03/99148d6eeaa4ec2855d71295ac83bcbc8ba7b41a2982992c63
[fastapi] Successfully built causal-conv1d mamba-ssm
[fastapi] Installing collected packages: z3-solver, protobuf, nvidia-cuda-nvdisasm, ninja, ml-dtypes, cuda-pathfinder, apache-tvm-ffi, cuda-core, cuda-bindings, cuda-python, torch-c-dlpack-ext, nvidia-cutlass-dsl-libs-core, causal-conv1d, tilelang, nvidia-cutlass-dsl-libs-base, nvidia-cutlass-dsl-libs-cu12, nvidia-cutlass-dsl, quack-kernels, mamba-ssm
[fastapi] Successfully installed apache-tvm-ffi-0.1.9 causal-conv1d-1.6.2.post1 cuda-bindings-13.4.1 cuda-core-1.2.0 cuda-pathfinder-1.8.1 cuda-python-13.4.1 mamba-ssm-2.3.2.post1 ml-dtypes-0.6.0 ninja-1.13.2 nvidia-cuda-nvdisasm-13.4.49 nvidia-cutlass-dsl-4.7.1 nvidia-cutlass-dsl-libs-base-4.7.1 nvidia-cutlass-dsl-libs-core-4.7.1 nvidia-cutlass-dsl-libs-cu12-4.7.1 protobuf-7.36.1 quack-kernels-0.6.5 tilelang-0.1.8 torch-c-dlpack-ext-0.1.5 z3-solver-4.15.4.0
[fastapi] ---> 8cd654697367
[fastapi] Step 6/10 : RUN uv pip install --system --no-cache --no-deps         flash-linear-attention==0.5.1 fla-core==0.5.1     && python -c "from fla.modules import FusedRMSNormGated; from fla.ops.gated_delta_rule import chunk_gated_delta_rule, fused_recurrent_gated_delta_rule"     && python -c "import torch; assert torch.__version__.startswith('2.9'), torch.__version__"
[fastapi] ---> Running in ab465e5f78cd
[fastapi] [91mUsing Python 3.12.13 environment at: /usr
[fastapi] [0m[91mResolved 2 packages in 45ms
[fastapi] [0m[91mPrepared 2 packages in 28ms
[fastapi] [0m[91mInstalled 2 packages in 19ms
[fastapi] + fla-core==0.5.1
[fastapi] + flash-linear-attention==0.5.1
[fastapi] [0m[91m/usr/local/lib/python3.12/dist-packages/fla/utils/_device.py:100: UserWarning: Triton is not supported on current platform, roll back to CPU.
[fastapi] _cpu_device_warning()
[fastapi] [0m[91m[W915 11:05:21.959744342 AllocatorConfig.cpp:28] Warning: PYTORCH_CUDA_ALLOC_CONF is deprecated, use PYTORCH_ALLOC_CONF instead (function operator())
[fastapi] [0m[91m[W915 11:05:22.400134903 AllocatorConfig.cpp:28] Warning: PYTORCH_CUDA_ALLOC_CONF is deprecated, use PYTORCH_ALLOC_CONF instead (function operator())
[fastapi] [0m ---> b2bbcaee3d98
[fastapi] Step 7/10 : WORKDIR /app
[fastapi] ---> Running in 178df29aa991
[fastapi] ---> 382cc8695fa0
[fastapi] Step 8/10 : COPY src /app/tenun
[fastapi] ---> 274495038429
[fastapi] Step 9/10 : COPY pyproject.toml LICENSE.md NOTICE /app/
[fastapi] ---> 582e4e79766e
[fastapi] Step 10/10 : ENTRYPOINT ["python", "-m", "tenun.cli"]
[fastapi] ---> Running in f3701593166e
[fastapi] ---> 1f4a60ccafa2
[fastapi] {'aux': {'ID': 'sha256:1f4a60ccafa280280fd6e8af587246fc0f6f213438b67df752cd9ab585bdece0'}}Successfully built 1f4a60ccafa2
[fastapi] Successfully tagged standalone-text-trainer:fe569850-7e3e-4ac2-a050-28d230475fca
[fastapi] Docker image built successfully.
[fastapi] Container.wait() returned: {'StatusCode': 0}
[fastapi] Cleaning up
[fastapi] Cleaned up Docker resources.
[fastapi] Starting upload container hf-upload-362e7d993ed141d886982acdfe0e1ee4 for task 067761fe-b567-44d7-8863-4cd41cc12261...
[hf-upload-36] Updated adapter_config.json with base_model: gradients-io-tournaments/augmented-8a3f84c4cc4a7528
[hf-upload-36] Updated README.md with base_model: gradients-io-tournaments/augmented-8a3f84c4cc4a7528
[hf-upload-36] Creating repo gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5EcZmz41...
[hf-upload-36] Uploading contents of /app/checkpoints/067761fe-b567-44d7-8863-4cd41cc12261/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5EcZmz41 to gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5EcZmz41
[hf-upload-36] Uploaded successfully to https://huggingface.co/gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5EcZmz41
[hf-upload-36] Deleted local folder: /app/checkpoints/067761fe-b567-44d7-8863-4cd41cc12261/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5EcZmz41
[text-trainer] [logs] init task_id='067761fe-b567-44d7-8863-4cd41cc12261' task_type='InstructTextTask' model='c53e93d87a4fe77f' hours=1.0 file_format='s3' use_kl=False kl_coef=0.0
[text-trainer] [logs] rows_loaded count=19505 source='/cache/datasets/067761fe-b567-44d7-8863-4cd41cc12261_train_data.json'
[text-trainer] [logs] attention_preflight eligible=True reason='supported'
[text-trainer] [logs] liger_preflight eligible=True reason='supported'
[text-trainer] [logs] model_loaded dir='/cache/models/c53e93d87a4fe77f' dtype='torch.bfloat16' tokenizer_rung='trc=False' model_rung='trc=False,attn=flash_attention_2' attn='flash_attention_2' liger=True fused_linear_cross_entropy=True
[text-trainer] [logs] baseline_stats keys=['dataset', 'task_type', 'throughput', 'training', 'weights']
[text-trainer] [logs] plan strategy='lora' kl=False rows=19505 lora_r=128 lr=0.0001 batch=50 grad_accum=1 epochs=3 params_b=1.236 n_gpus=1 per_gpu_gb=85.0
[text-trainer] [logs] floor_written rung='untrained_adapter'
[text-trainer] [logs] dev_split train=18914 dev=591 dup_groups=785
[text-trainer] [logs] rows_dropped_length kept=18739 dropped_overlong=175 dropped_unsupervised=0 max_len=4096
[text-trainer] [logs] rows_dropped_length kept=582 dropped_overlong=9 dropped_unsupervised=0 max_len=4096
[text-trainer] [logs] tokenized n=18739 seq_len=4096 ladder=[4096, 8192, 16384, 32768, 65536, 131072]
[text-trainer] [logs] prompt_loss_weight ratio=17.33 fraction=0.0144 unmasked_tokens=129359
[text-trainer] [logs] rows_packed rows=18739 blocks=2791 gain=6.71 block_len=4096
[text-trainer] [logs] split train_n=2791 val_n=582 steps_per_epoch=55
[text-trainer] [logs] packing_mode packed=True attn='flash_attention_2' isolated=True block_len=4096
[text-trainer] [logs] lr_seed is_augment=False source='model_weight_rms' law=4.8360810419379694e-05 bucket=0.0001
[text-trainer] [logs] lr_probe per_step=4.8945 steps=8 batch=50 curvature=1.353 rel_drop=0.1283 lr='6.544e-05'
[text-trainer] [logs] lr_search_aborted reason='S1 too shallow (30st) to refine'
[text-trainer] [logs] lr_search mode='two_stage' candidates=4 scores={'3.280e-05': 1.69828, '5.198e-05': 1.66568, '8.239e-05': 1.63734, '1.306e-04': 1.61954} chosen='1.306e-04' batch=50 budget_s=606.5 tier='coarse' pruned=None skipped=0 dev_scored=False reason='124 probe-steps within 20%: S1 + refine on the surplus'
[text-trainer] [logs] lr_search_memory_released
[text-trainer] [logs] schedule lr=0.00013057710288905038 searched=True per_step_s=4.8904 epochs=4.0
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=25 ok=True
[text-trainer] [logs] eval_skip_early skipped=2 until_epoch=0.75
[text-trainer] [logs] eval_cadence_widened eval_steps=30 eval_spent_s=26.0 elapsed_s=246.9
[text-trainer] [logs] best_export step=45 metric='eval_loss' value=1.50308
[text-trainer] [logs] eval_cadence_widened eval_steps=60 eval_spent_s=45.4 elapsed_s=340.2
[text-trainer] [logs] best_export step=120 metric='eval_loss' value=1.46371
[text-trainer] [logs] soup_pool size=5
[text-trainer] [logs] best_export step=224 metric='eval_loss' value=1.41744
[text-trainer] [logs] soup_accept step=180 score=1.41744 members=2
[text-trainer] [logs] best_export step=224 metric='eval_loss' value=1.36276
[text-trainer] [logs] soup_accept step=45 score=1.36276 members=3
[text-trainer] [logs] best_export step=224 metric='eval_loss' value=1.36152
[text-trainer] [logs] soup_accept step=224 score=1.36152 members=4
[text-trainer] [logs] soup_reject step=60 score=1.37114 best=1.36152
[text-trainer] [logs] soup_result verdict='soup' evals=4 final_loss=1.36152 members=4
[text-trainer] [logs] final_save ok=True source='soup'
[text-trainer] [logs] dev_pass ok=True steps=11
[text-trainer] [logs] run_complete
[text-trainer] [W915 11:43:31.096844503 AllocatorConfig.cpp:28] Warning: PYTORCH_CUDA_ALLOC_CONF is deprecated, use PYTORCH_ALLOC_CONF instead (function operator())