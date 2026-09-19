# Loki — task 90d361cb-0b97-464a-9fda-36eb34c99261 — hotkey 5EcZmz41oFGaJVte8DEzuGd8QyBBxjhTobhrK4A5y4b1Q24Y
fetched 2026-09-19T05:10:26+00:00  lines=428  hit_page_cap=False  containers=['downloader-90d361cb-0b97-464a-9fda-36eb34c99261-42cd8c82', 'fastapi', 'hf-upload-4d586441093542ec9fabdda742e51966', 'text-trainer-c32f1da95e4848628c1df953b6b13a38']

[downloader-9] Downloading datasets to: /cache/datasets
[downloader-9] Downloading models to: /cache/models
[downloader-9] /usr/local/lib/python3.10/site-packages/huggingface_hub/utils/_validators.py:205: UserWarning: The `local_dir_use_symlinks` argument is deprecated and ignored in `snapshot_download`. Downloading to a local directory does not use symlinks anymore.
[downloader-9]   warnings.warn(
[downloader-9] Model path: /cache/models/a0971600276b8e78
[downloader-9] Dataset path: /cache/datasets
[fastapi] Repository cloned successfully
[fastapi] Running Cache Download Container
[fastapi] Starting downloader container: downloader-90d361cb-0b97-464a-9fda-36eb34c99261-42cd8c82
[fastapi] Download completed successfully for task 90d361cb-0b97-464a-9fda-36eb34c99261
[fastapi] Building Docker image 'standalone-text-trainer:dbe51207-ba6a-4981-96d6-d62bf2c3ec40' (timeout=1800s)...
[fastapi] Step 1/10 : FROM runpod/pytorch:1.1.0-cu1281-torch291-ubuntu2204@sha256:a9320617b09069038f677ff7dcc2262faba42bc2bfa2125d6c733285946d14ac
[fastapi] ---> 3b600cc49e85
[fastapi] Step 2/10 : ENV PYTHONUNBUFFERED=1     PIP_NO_CACHE_DIR=1     HF_HUB_DISABLE_TELEMETRY=1     HF_HUB_DISABLE_SYMLINKS_WARNING=1     TOKENIZERS_PARALLELISM=false     PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True     HF_HUB_OFFLINE=1     TRANSFORMERS_OFFLINE=1
[fastapi] ---> Running in 0b6cb92c669d
[fastapi] ---> 144279bd7b4e
[fastapi] Step 3/10 : RUN pip install --no-cache-dir uv     && uv pip install --system --no-cache         torch==2.9.1         transformers==5.12.1         tokenizers==0.22.2         peft==0.19.1         trl==1.5.1         liger-kernel==0.8.1         accelerate==1.13.0         datasets==4.8.5         safetensors==0.8.0         sentencepiece==0.2.0         einops==0.8.1         textstat==0.7.8 langcheck==0.9.0 RestrictedPython==8.0
[fastapi] ---> Running in 13fa2bbc8181
[fastapi] Collecting uv
[fastapi] Downloading uv-0.12.13-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] Downloading uv-0.12.13-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.0 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 20.0/20.0 MB 136.4 MB/s  0:00:00
[fastapi] Installing collected packages: uv
[fastapi] Successfully installed uv-0.12.13
[fastapi] [91mUsing Python 3.12.13 environment at: /usr
[fastapi] [0m[91mResolved 124 packages in 1.63s
[fastapi] [0m[91m   Building antlr4-python3-runtime==4.9.3
[fastapi] [0m[91mDownloading pyphen (2.0MiB)
[fastapi] [0m[91mDownloading numpy (15.9MiB)
[fastapi] [0m[91mDownloading dash (8.5MiB)
[fastapi] [0m[91mDownloading sentencepiece (1.2MiB)
[fastapi] [0m[91mDownloading pyarrow (47.8MiB)
[fastapi] [0m[91mDownloading hf-xet (4.3MiB)
[fastapi] [0m[91mDownloading aiohttp (1.7MiB)
[fastapi] [0m[91mDownloading pydantic-core (2.0MiB)
[fastapi] [0m[91mDownloading nltk (1.7MiB)
[fastapi] [0m[91mDownloading scikit-learn (8.7MiB)
[fastapi] [0m[91mDownloading transformers (10.6MiB)
[fastapi] [0m[91mDownloading plotly (8.6MiB)
[fastapi] [0m[91mDownloading openai (1.9MiB)
[fastapi] [0m[91mDownloading pandas (10.5MiB)
[fastapi] [0m[91mDownloading tokenizers (3.1MiB)
[fastapi] [0m[91mDownloading scipy (33.7MiB)
[fastapi] [0m[91m   Building rouge-score==0.1.2
[fastapi] [0m[91m Downloaded sentencepiece
[fastapi] [0m[91m Downloaded nltk
[fastapi] [0m[91m Downloaded aiohttp
[fastapi] [0m[91m Downloaded pyphen
[fastapi] [0m[91m Downloaded pydantic-core
[fastapi] [0m[91m Downloaded openai
[fastapi] [0m[91m Downloaded tokenizers
[fastapi] [0m[91m Downloaded hf-xet
[fastapi] [0m[91m      Built antlr4-python3-runtime==4.9.3
[fastapi] [0m[91m      Built rouge-score==0.1.2
[fastapi] [0m[91m Downloaded dash
[fastapi] [0m[91m Downloaded scikit-learn
[fastapi] [0m[91m Downloaded plotly
[fastapi] [0m[91m Downloaded pandas
[fastapi] [0m[91m Downloaded transformers
[fastapi] [0m[91m Downloaded numpy
[fastapi] [0m[91m Downloaded scipy
[fastapi] [0m[91m Downloaded pyarrow
[fastapi] [0m[91mPrepared 80 packages in 683ms
[fastapi] [0m[91mUninstalled 1 package in 22ms
[fastapi] [0m[91mInstalled 80 packages in 74ms
[fastapi] [0m[91m + absl-py==2.5.0
[fastapi] + accelerate==1.13.0
[fastapi] +[0m[91m aiohappyeyeballs==2.7.1
[fastapi] [0m[91m+ aiohttp[0m[91m==3.14.[0m[91m3
[fastapi] [0m[91m+ [0m[91maiosignal==[0m[91m1.4.0[0m[91m
[fastapi] [0m[91m+[0m[91m annotated-doc[0m[91m==0.0[0m[91m.5[0m[91m
[fastapi] [0m[91m+ [0m[91mannotated-types==0.8.0
[fastapi] [0m[91m + [0m[91mantlr4-python3-runtime[0m[91m==4.9[0m[91m.3[0m[91m
[fastapi] [0m[91m+ blinker[0m[91m==1.9.0
[fastapi] [0m[91m+ click==[0m[91m8.5.0[0m[91m
[fastapi] + cloudpickle[0m[91m==3.1[0m[91m.2
[fastapi] + [0m[91mcmudict==1[0m[91m.1.3[0m[91m
[fastapi] +[0m[91m dash==4.[0m[91m4.1[0m[91m
[fastapi] + [0m[91mdatasets==4.8.5
[fastapi] [0m[91m + dill==0.4.1
[fastapi] + einops==0.8.1
[fastapi] + flask[0m[91m==3.1.3
[fastapi] + frozenlist==[0m[91m1.8.0
[fastapi] - fsspec==2026.7.0
[fastapi] + fsspec[0m[91m==2026.2.0[0m[91m
[fastapi] + gdown==6.2[0m[91m.0
[fastapi] + [0m[91mhf-xet==1.[0m[91m6.0
[fastapi] + httpcore2==2.13.0[0m[91m
[fastapi] + httpx2==2[0m[91m.13.0
[fastapi] + huggingface-hub[0m[91m==1.31.0[0m[91m
[fastapi] + [0m[91mimportlib-metadata==9.0[0m[91m.1
[fastapi] + [0m[91mimportlib-resources==7.[0m[91m1.0
[fastapi] [0m[91m+ itsdangerous==2.2.0
[fastapi] [0m[91m + jaconv[0m[91m==0.5.0[0m[91m
[fastapi] [0m[91m + [0m[91mjanus[0m[91m==2.0.0[0m[91m
[fastapi] + jiter==0[0m[91m.17.0[0m[91m
[fastapi] +[0m[91m joblib==1[0m[91m.6[0m[91m.0
[fastapi] [0m[91m +[0m[91m langcheck[0m[91m==0.9.0[0m[91m
[fastapi] +[0m[91m liger-kernel==0[0m[91m.8.[0m[91m1[0m[91m
[fastapi] + [0m[91mmarkdown-it-py==4[0m[91m.[0m[91m2.0[0m[91m
[fastapi] +[0m[91m [0m[91mmdurl==0[0m[91m.1[0m[91m.2
[fastapi] [0m[91m +[0m[91m multidict[0m[91m==6.8.[0m[91m0
[fastapi] + multiprocess==0.70.19
[fastapi] + [0m[91mnarwhals==2.[0m[91m26.0
[fastapi] [0m[91m + nest-asyncio==1.6.0
[fastapi] + [0m[91mnlpaug==1.1.[0m[91m11
[fastapi] [0m[91m +[0m[91m nltk==[0m[91m3.[0m[91m10.3
[fastapi] [0m[91m + numpy==2.5.3
[fastapi] + omegaconf[0m[91m==2.3.1
[fastapi] [0m[91m +[0m[91m openai[0m[91m==3[0m[91m.14.[0m[91m0
[fastapi] + pandas==3.0.5
[fastapi] [0m[91m+ peft==0[0m[91m.19.1
[fastapi] [0m[91m +[0m[91m plotly[0m[91m==7.[0m[91m0.[0m[91m0
[fastapi] [0m[91m +[0m[91m propcache[0m[91m==0[0m[91m.5[0m[91m.2
[fastapi] [0m[91m+[0m[91m [0m[91mpyarrow==25.[0m[91m0[0m[91m.1
[fastapi] [0m[91m +[0m[91m [0m[91mpydantic==2.[0m[91m13.5
[fastapi] + pydantic-core==2.46[0m[91m.5
[fastapi] + pyphen[0m[91m==0[0m[91m.18.[0m[91m1
[fastapi] [0m[91m [0m[91m+ [0m[91mpysocks==1[0m[91m.7[0m[91m.1[0m[91m
[fastapi] +[0m[91m [0m[91mregex==2026.9.10
[fastapi] + restrictedpython==8.[0m[91m0
[fastapi] + retrying==1[0m[91m.4.2
[fastapi] [0m[91m+[0m[91m rich[0m[91m==15.0.[0m[91m0[0m[91m
[fastapi] + [0m[91mrouge-score[0m[91m==0[0m[91m.1.[0m[91m2
[fastapi] [0m[91m+ [0m[91msafetensors==[0m[91m0.8[0m[91m.[0m[91m0
[fastapi] [0m[91m+ [0m[91mscikit-learn[0m[91m==1.9.1[0m[91m
[fastapi] + scipy==1.18.1[0m[91m
[fastapi] + sentence-transformers[0m[91m==6.[0m[91m0.1
[fastapi] [0m[91m + [0m[91msentencepiece[0m[91m==0.2.[0m[91m0[0m[91m
[fastapi] +[0m[91m shellingham[0m[91m==1.5.[0m[91m4
[fastapi] + six==1.17.[0m[91m0
[fastapi] + sniffio==1.3.1
[fastapi] [0m[91m+ tabulate[0m[91m==0.10.0
[fastapi] [0m[91m+ textstat==0.7.8
[fastapi] + threadpoolctl==3[0m[91m.6.0
[fastapi] +[0m[91m tokenizers==0.[0m[91m22.[0m[91m2
[fastapi] +[0m[91m [0m[91mtqdm==[0m[91m4.70[0m[91m.1
[fastapi] [0m[91m +[0m[91m transformers[0m[91m==5.12.1
[fastapi] + [0m[91mtrl==1[0m[91m.5[0m[91m.1
[fastapi] [0m[91m+ truststore[0m[91m==0.10.4
[fastapi] + [0m[91mtyper==0.27.2
[fastapi] + typing-inspection==0.4.4[0m[91m
[fastapi] + werkzeug==3.1.8
[fastapi] + xxhash==4[0m[91m.0.1
[fastapi] [0m[91m+ [0m[91myarl==[0m[91m1.24.[0m[91m5[0m[91m
[fastapi] + [0m[91mzipp[0m[91m==4.[0m[91m1.0[0m[91m
[fastapi] [0m ---> e2cef3ea0ae6
[fastapi] Step 4/10 : RUN ABI=$(python -c "import torch; print('TRUE' if torch._C._GLIBCXX_USE_CXX11_ABI else 'FALSE')")     && echo "torch cxx11 ABI: ${ABI}"     && uv pip install --system --no-cache         "https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu12torch2.9cxx11abi${ABI}-cp312-cp312-linux_x86_64.whl"     && python -c "import flash_attn; from flash_attn import flash_attn_func, flash_attn_varlen_func; print('flash-attn:', flash_attn.__version__)"
[fastapi] ---> Running in ae2e4fc048b8
[fastapi] [91m[W915 00:05:17.596429895 AllocatorConfig.cpp:28] Warning: PYTORCH_CUDA_ALLOC_CONF is deprecated, use PYTORCH_ALLOC_CONF instead (function operator())
[fastapi] [0mtorch cxx11 ABI: TRUE
[fastapi] [91mUsing Python 3.12.13 environment at: /usr
[fastapi] [0m[91mResolved 28 packages in 2.66s
[fastapi] [0m[91mDownloading flash-attn (242.0MiB)
[fastapi] [0m[91m Downloaded flash-attn
[fastapi] [0m[91mPrepared 1 package in 2.85s
[fastapi] [0m[91mInstalled 1 package in 11ms
[fastapi] + flash-attn==2.8.3+cu12torch2.9cxx11abitrue (from https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu12torch2.9cxx11abiTRUE-cp312-cp312-linux_x86_64.whl)
[fastapi] [0mflash-attn: 2.8.3
[fastapi] [91m[W915 00:05:24.619889115 AllocatorConfig.cpp:28] Warning: PYTORCH_CUDA_ALLOC_CONF is deprecated, use PYTORCH_ALLOC_CONF instead (function operator())
[fastapi] [0m ---> 0c37a186b93f
[fastapi] Step 5/10 : RUN TORCH_CUDA_ARCH_LIST="8.0;9.0+PTX" MAX_JOBS=4     pip install --no-cache-dir --no-build-isolation     causal-conv1d==1.6.2.post1 mamba-ssm==2.3.2.post1
[fastapi] ---> Running in f06492fe91da
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
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 43.5/43.5 MB 156.0 MB/s  0:00:00
[fastapi] Downloading apache_tvm_ffi-0.1.9-cp312-abi3-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (2.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.3/2.3 MB 135.0 MB/s  0:00:00
[fastapi] Downloading z3_solver-4.15.4.0-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (29.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 29.3/29.3 MB 133.8 MB/s  0:00:00
[fastapi] Downloading quack_kernels-0.6.5-py3-none-any.whl (729 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 729.6/729.6 kB 859.0 MB/s  0:00:00
[fastapi] Downloading nvidia_cutlass_dsl-4.7.1-py3-none-any.whl (10 kB)
[fastapi] Downloading nvidia_cutlass_dsl_libs_base-4.7.1-cp312-cp312-manylinux_2_28_x86_64.whl (2.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.8/2.8 MB 223.2 MB/s  0:00:00
[fastapi] Downloading nvidia_cutlass_dsl_libs_core-4.7.1-py3-none-any.whl (1.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 173.9 MB/s  0:00:00
[fastapi] Downloading nvidia_cutlass_dsl_libs_cu12-4.7.1-cp312-cp312-manylinux_2_28_x86_64.whl (88.7 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 88.7/88.7 MB 182.3 MB/s  0:00:00
[fastapi] Downloading nvidia_cuda_nvdisasm-13.4.49-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (5.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.2/5.2 MB 162.6 MB/s  0:00:00
[fastapi] Downloading cuda_python-13.4.1-py3-none-any.whl (7.6 kB)
[fastapi] Downloading cuda_bindings-13.4.1-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (7.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.2/7.2 MB 196.7 MB/s  0:00:00
[fastapi] Downloading cuda_core-1.2.0-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (6.6 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.6/6.6 MB 236.8 MB/s  0:00:00
[fastapi] Downloading cuda_pathfinder-1.8.1-py3-none-any.whl (62 kB)
[fastapi] Downloading protobuf-7.36.1-cp310-abi3-manylinux2014_x86_64.whl (343 kB)
[fastapi] Downloading ml_dtypes-0.6.0-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (409 kB)
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (183 kB)
[fastapi] Downloading torch_c_dlpack_ext-0.1.5-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (897 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 897.8/897.8 kB 202.1 MB/s  0:00:00
[fastapi] Building wheels for collected packages: causal-conv1d, mamba-ssm
[fastapi] Building wheel for causal-conv1d (pyproject.toml): started
[fastapi] Building wheel for causal-conv1d (pyproject.toml): finished with status 'done'
[fastapi] Created wheel for causal-conv1d: filename=causal_conv1d-1.6.2.post1-cp312-cp312-linux_x86_64.whl size=193795077 sha256=3d09789a5df2760a59c2064c4570a4ccd30315943581e9553eb1f412cd9e25a6
[fastapi] Stored in directory: /tmp/pip-ephem-wheel-cache-pk19nf3f/wheels/ea/f0/26/5d87ae05a302e6dc8016c50cd8c7ee779585f593b9580e7cf8
[fastapi] Building wheel for mamba-ssm (pyproject.toml): started
[fastapi] Building wheel for mamba-ssm (pyproject.toml): finished with status 'done'
[fastapi] Created wheel for mamba-ssm: filename=mamba_ssm-2.3.2.post1-cp312-cp312-linux_x86_64.whl size=322246976 sha256=8fd21085d668a3bdbb1f7903c81f64434d7ed2c763240f8328a465a42370a7b6
[fastapi] Stored in directory: /tmp/pip-ephem-wheel-cache-pk19nf3f/wheels/da/67/03/99148d6eeaa4ec2855d71295ac83bcbc8ba7b41a2982992c63
[fastapi] Successfully built causal-conv1d mamba-ssm
[fastapi] Installing collected packages: z3-solver, protobuf, nvidia-cuda-nvdisasm, ninja, ml-dtypes, cuda-pathfinder, apache-tvm-ffi, cuda-core, cuda-bindings, cuda-python, torch-c-dlpack-ext, nvidia-cutlass-dsl-libs-core, causal-conv1d, tilelang, nvidia-cutlass-dsl-libs-base, nvidia-cutlass-dsl-libs-cu12, nvidia-cutlass-dsl, quack-kernels, mamba-ssm
[fastapi] Successfully installed apache-tvm-ffi-0.1.9 causal-conv1d-1.6.2.post1 cuda-bindings-13.4.1 cuda-core-1.2.0 cuda-pathfinder-1.8.1 cuda-python-13.4.1 mamba-ssm-2.3.2.post1 ml-dtypes-0.6.0 ninja-1.13.2 nvidia-cuda-nvdisasm-13.4.49 nvidia-cutlass-dsl-4.7.1 nvidia-cutlass-dsl-libs-base-4.7.1 nvidia-cutlass-dsl-libs-core-4.7.1 nvidia-cutlass-dsl-libs-cu12-4.7.1 protobuf-7.36.1 quack-kernels-0.6.5 tilelang-0.1.8 torch-c-dlpack-ext-0.1.5 z3-solver-4.15.4.0
[fastapi] ---> d136c0d6d8fc
[fastapi] Step 6/10 : RUN uv pip install --system --no-cache --no-deps         flash-linear-attention==0.5.1 fla-core==0.5.1     && python -c "from fla.modules import FusedRMSNormGated; from fla.ops.gated_delta_rule import chunk_gated_delta_rule, fused_recurrent_gated_delta_rule"     && python -c "import torch; assert torch.__version__.startswith('2.9'), torch.__version__"
[fastapi] ---> Running in 49905c066540
[fastapi] [91mUsing Python 3.12.13 environment at: /usr
[fastapi] [0m[91mResolved 2 packages in 47ms
[fastapi] [0m[91mPrepared 2 packages in 34ms
[fastapi] [0m[91mInstalled 2 packages in 19ms
[fastapi] + fla-core==0.5.1
[fastapi] + flash-linear-attention==0.5.1
[fastapi] [0m[91m/usr/local/lib/python3.12/dist-packages/fla/utils/_device.py:100: UserWarning: Triton is not supported on current platform, roll back to CPU.
[fastapi] _cpu_device_warning()
[fastapi] [0m[91m[W915 00:06:13.059655956 AllocatorConfig.cpp:28] Warning: PYTORCH_CUDA_ALLOC_CONF is deprecated, use PYTORCH_ALLOC_CONF instead (function operator())
[fastapi] [0m[91m[W915 00:06:14.489290560 AllocatorConfig.cpp:28] Warning: PYTORCH_CUDA_ALLOC_CONF is deprecated, use PYTORCH_ALLOC_CONF instead (function operator())
[fastapi] [0m ---> f0c09c0aefe5
[fastapi] Step 7/10 : WORKDIR /app
[fastapi] ---> Running in 35e8160cedf1
[fastapi] ---> eec36cd82c2b
[fastapi] Step 8/10 : COPY src /app/tenun
[fastapi] ---> 7b2c9a8b5a4f
[fastapi] Step 9/10 : COPY pyproject.toml LICENSE.md NOTICE /app/
[fastapi] ---> e6e5a9d7c07d
[fastapi] Step 10/10 : ENTRYPOINT ["python", "-m", "tenun.cli"]
[fastapi] ---> Running in ede511fd7065
[fastapi] ---> d714d6c3e876
[fastapi] {'aux': {'ID': 'sha256:d714d6c3e876cca34f72baa4b03624f831ddc6842cf6fb3fdab8a70d24a05e95'}}Successfully built d714d6c3e876
[fastapi] Successfully tagged standalone-text-trainer:dbe51207-ba6a-4981-96d6-d62bf2c3ec40
[fastapi] Docker image built successfully.
[fastapi] Container.wait() returned: {'StatusCode': 0}
[fastapi] Cleaning up
[fastapi] Cleaned up Docker resources.
[fastapi] Starting upload container hf-upload-4d586441093542ec9fabdda742e51966 for task 90d361cb-0b97-464a-9fda-36eb34c99261...
[hf-upload-4d] Updated adapter_config.json with base_model: LiquidAI/LFM2.5-2.6B
[hf-upload-4d] Updated README.md with base_model: LiquidAI/LFM2.5-2.6B
[hf-upload-4d] Creating repo gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-90d361cb-0b97-464a-9fda-36eb34c99261-5EcZmz41...
[hf-upload-4d] Uploading contents of /app/checkpoints/90d361cb-0b97-464a-9fda-36eb34c99261/tournament-tourn_5c64e784a087074a_20260914-90d361cb-0b97-464a-9fda-36eb34c99261-5EcZmz41 to gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-90d361cb-0b97-464a-9fda-36eb34c99261-5EcZmz41
[hf-upload-4d] Uploaded successfully to https://huggingface.co/gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-90d361cb-0b97-464a-9fda-36eb34c99261-5EcZmz41
[hf-upload-4d] Deleted local folder: /app/checkpoints/90d361cb-0b97-464a-9fda-36eb34c99261/tournament-tourn_5c64e784a087074a_20260914-90d361cb-0b97-464a-9fda-36eb34c99261-5EcZmz41
[text-trainer] [logs] init task_id='90d361cb-0b97-464a-9fda-36eb34c99261' task_type='InstructTextTask' model='a0971600276b8e78' hours=2.0 file_format='s3' use_kl=False kl_coef=0.0
[text-trainer] [logs] rows_loaded count=58892 source='/cache/datasets/90d361cb-0b97-464a-9fda-36eb34c99261_train_data.json'
[text-trainer] [logs] attention_preflight eligible=True reason='supported'
[text-trainer] [logs] liger_preflight eligible=False reason='unsupported_architecture'
[text-trainer] [logs] model_loaded dir='/cache/models/a0971600276b8e78' dtype='torch.bfloat16' tokenizer_rung='trc=False' model_rung='trc=False,attn=flash_attention_2' attn='flash_attention_2' liger=False fused_linear_cross_entropy=False
[text-trainer] [logs] baseline_stats keys=['dataset', 'task_type', 'throughput', 'training', 'weights']
[text-trainer] [logs] plan strategy='lora' kl=False rows=58892 lora_r=128 lr=7.5e-05 batch=24 grad_accum=2 epochs=3 params_b=2.697 n_gpus=1 per_gpu_gb=85.0
[text-trainer] [logs] floor_written rung='untrained_adapter'
[text-trainer] [logs] dev_split train=57890 dev=1002 dup_groups=34
[text-trainer] [logs] rows_dropped_length kept=57887 dropped_overlong=3 dropped_unsupervised=0 max_len=4096
[text-trainer] [logs] tokenized n=57887 seq_len=4096 ladder=[4096, 8192, 16384, 32768, 65536, 131072]
[text-trainer] [logs] rows_packed rows=57887 blocks=10105 gain=5.73 block_len=4096
[text-trainer] [logs] split train_n=10105 val_n=1002 steps_per_epoch=210
[text-trainer] [logs] packing_mode packed=True attn='flash_attention_2' isolated=True block_len=4096
[text-trainer] [logs] lr_seed is_augment=False source='model_weight_rms' law=2.770870687134153e-05 bucket=7.5e-05
[text-trainer] [logs] lr_oom_halved batch=12 halving=1 lr='2.771e-05' center='1.959e-05'
[text-trainer] [logs] lr_oom_halved batch=6 halving=2 lr='2.771e-05' center='1.385e-05'
[text-trainer] [logs] lr_probe per_step=3.2429 steps=8 batch=6 curvature=1.6 rel_drop=0.4581 lr='2.217e-05'
[text-trainer] [logs] lr_search_aborted reason='no time to refine (263s left)'
[text-trainer] [logs] lr_search mode='two_stage' candidates=3 scores={'1.111e-05': 0.31411, '1.761e-05': 0.30961, '2.791e-05': 0.30662} chosen='2.791e-05' batch=6 budget_s=1200.0 tier='coarse' pruned=None skipped=1 dev_scored=False reason='370 probe-steps within 20%: S1 + refine on the surplus'
[text-trainer] [logs] lr_search_batch_adopted batch=6 grad_accum=2 lr=2.791e-05
[text-trainer] [logs] lr_search_memory_released
[text-trainer] [logs] schedule lr=2.7906556166629983e-05 searched=True per_step_s=3.2365 epochs=2.11
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=25 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=50 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=75 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=100 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=125 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=150 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=175 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=200 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=225 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=250 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=275 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=300 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=325 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=350 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=375 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=400 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=425 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=450 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=475 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=500 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=525 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=550 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=575 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=600 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=625 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=650 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=675 ok=True
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=700 ok=True
[text-trainer] [logs] eval_skip_early skipped=5 until_epoch=0.75
[text-trainer] [logs] soup_pool_clamped cap=24 affordable=20 snapshot_mb=782
[text-trainer] [logs] best_export step=714 metric='eval_loss' value=0.32901
[text-trainer] [logs] best_export step=833 metric='eval_loss' value=0.32713
[text-trainer] [logs] deadline_stop hook='step_end' step=1516 remaining_s=29.3 margin_s=30.0
[text-trainer] [logs] soup_pool size=7
[text-trainer] [logs] best_export step=1516 metric='eval_loss' value=0.32348
[text-trainer] [logs] soup_accept step=1428 score=0.32348 members=2
[text-trainer] [logs] soup_budget_stop evals=1 spent_s=46.8
[text-trainer] [logs] soup_result verdict='soup' evals=1 final_loss=0.32348 members=2
[text-trainer] [logs] final_save ok=True source='soup'
[text-trainer] [logs] run_complete
[text-trainer] [W915 02:03:38.705704579 AllocatorConfig.cpp:28] Warning: PYTORCH_CUDA_ALLOC_CONF is deprecated, use PYTORCH_ALLOC_CONF instead (function operator())