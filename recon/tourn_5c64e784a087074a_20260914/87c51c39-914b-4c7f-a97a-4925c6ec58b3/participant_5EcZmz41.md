# Loki — task 87c51c39-914b-4c7f-a97a-4925c6ec58b3 — hotkey 5EcZmz41oFGaJVte8DEzuGd8QyBBxjhTobhrK4A5y4b1Q24Y
fetched 2026-09-19T05:07:22+00:00  lines=375  hit_page_cap=False  containers=['downloader-87c51c39-914b-4c7f-a97a-4925c6ec58b3-f8058d20', 'fastapi', 'hf-upload-c65f8e368fd44ee4844fce1a4e7e865f', 'text-trainer-15e189650a2549ce9dfdb1f7951fc36e']

[downloader-8] Downloading datasets to: /cache/datasets
[downloader-8] Downloading models to: /cache/models
[downloader-8] Model already cached at /cache/models/b254e84a30620233.
[downloader-8] Skipping download.
[downloader-8] Model path: /cache/models/b254e84a30620233
[downloader-8] Dataset path: /cache/datasets
[fastapi] Repository cloned successfully
[fastapi] Running Cache Download Container
[fastapi] Starting downloader container: downloader-87c51c39-914b-4c7f-a97a-4925c6ec58b3-f8058d20
[fastapi] Download completed successfully for task 87c51c39-914b-4c7f-a97a-4925c6ec58b3
[fastapi] Building Docker image 'standalone-text-trainer:0e5c1cb2-1546-4ebe-9593-96d0a0254933' (timeout=1800s)...
[fastapi] Step 1/10 : FROM runpod/pytorch:1.1.0-cu1281-torch291-ubuntu2204@sha256:a9320617b09069038f677ff7dcc2262faba42bc2bfa2125d6c733285946d14ac
[fastapi] ---> 3b600cc49e85
[fastapi] Step 2/10 : ENV PYTHONUNBUFFERED=1     PIP_NO_CACHE_DIR=1     HF_HUB_DISABLE_TELEMETRY=1     HF_HUB_DISABLE_SYMLINKS_WARNING=1     TOKENIZERS_PARALLELISM=false     PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True     HF_HUB_OFFLINE=1     TRANSFORMERS_OFFLINE=1
[fastapi] ---> Running in 478b5b953d99
[fastapi] ---> 83c6b4482485
[fastapi] Step 3/10 : RUN pip install --no-cache-dir uv     && uv pip install --system --no-cache         torch==2.9.1         transformers==5.12.1         tokenizers==0.22.2         peft==0.19.1         trl==1.5.1         liger-kernel==0.8.1         accelerate==1.13.0         datasets==4.8.5         safetensors==0.8.0         sentencepiece==0.2.0         einops==0.8.1         textstat==0.7.8 langcheck==0.9.0 RestrictedPython==8.0
[fastapi] ---> Running in c80a8e0888e9
[fastapi] Collecting uv
[fastapi] Downloading uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] Downloading uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.1 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 20.1/20.1 MB 257.4 MB/s  0:00:00
[fastapi] Installing collected packages: uv
[fastapi] Successfully installed uv-0.12.15
[fastapi] [91mUsing Python 3.12.13 environment at: /usr
[fastapi] [0m[91mResolved 124 packages in 1.27s
[fastapi] [0m[91m   Building antlr4-python3-runtime==4.9.3
[fastapi] [0m[91mDownloading aiohttp (1.7MiB)
[fastapi] [0m[91mDownloading hf-xet (4.3MiB)
[fastapi] [0m[91mDownloading pydantic-core (2.0MiB)
[fastapi] [0m[91mDownloading nltk (1.7MiB)
[fastapi] [0m[91mDownloading dash (8.5MiB)
[fastapi] [0m[91mDownloading openai (1.9MiB)
[fastapi] [0m[91mDownloading tokenizers (3.1MiB)
[fastapi] [0m[91mDownloading pyarrow (47.8MiB)
[fastapi] [0m[91mDownloading sentencepiece (1.2MiB)
[fastapi] [0m[91mDownloading pandas (10.5MiB)
[fastapi] [0m[91mDownloading transformers (10.6MiB)
[fastapi] [0m[91mDownloading scikit-learn (8.7MiB)
[fastapi] [0m[91mDownloading plotly (8.6MiB)
[fastapi] [0m[91mDownloading pyphen (2.0MiB)
[fastapi] [0m[91mDownloading scipy (33.7MiB)
[fastapi] [0m[91mDownloading numpy (15.9MiB)
[fastapi] [0m[91m   Building rouge-score==0.1.2
[fastapi] [0m[91m Downloaded sentencepiece
[fastapi] [0m[91m Downloaded aiohttp
[fastapi] [0m[91m Downloaded nltk
[fastapi] [0m[91m Downloaded pydantic-core
[fastapi] [0m[91m Downloaded pyphen
[fastapi] [0m[91m Downloaded openai
[fastapi] [0m[91m Downloaded tokenizers
[fastapi] [0m[91m Downloaded hf-xet
[fastapi] [0m[91m      Built antlr4-python3-runtime==4.9.3
[fastapi] [0m[91m Downloaded plotly
[fastapi] [0m[91m Downloaded scikit-learn
[fastapi] [0m[91m      Built rouge-score==0.1.2
[fastapi] [0m[91m Downloaded dash
[fastapi] [0m[91m Downloaded pandas
[fastapi] [0m[91m Downloaded transformers
[fastapi] [0m[91m Downloaded numpy
[fastapi] [0m[91m Downloaded scipy
[fastapi] [0m[91m Downloaded pyarrow
[fastapi] [0m[91mPrepared 80 packages in 598ms
[fastapi] [0m[91mUninstalled 1 package in 21ms
[fastapi] [0m[91mInstalled 80 packages in 75ms
[fastapi] + absl-py==2.5.0
[fastapi] +[0m[91m accelerate==1.13.0
[fastapi] + aiohappyeyeballs==2.7.1
[fastapi] + aiohttp==3.14.3
[fastapi] + aiosignal==1.4.0
[fastapi] +[0m[91m annotated-doc==0.0.5
[fastapi] + annotated-types==0.[0m[91m8.0[0m[91m
[fastapi] +[0m[91m antlr4-python3-runtime==4.9.3
[fastapi] + blinker==1.9.0
[fastapi] + click[0m[91m==8.5.0
[fastapi] + cloudpickle==3.1.2
[fastapi] + cmudict==1.1.3[0m[91m
[fastapi] + [0m[91mdash==4.4[0m[91m.1
[fastapi] +[0m[91m datasets[0m[91m==4.8.[0m[91m5
[fastapi] +[0m[91m dill[0m[91m==0.4[0m[91m.1
[fastapi] [0m[91m +[0m[91m einops==0.8.[0m[91m1
[fastapi] + [0m[91mflask==3.[0m[91m1[0m[91m.3
[fastapi] [0m[91m+ frozenlist[0m[91m==1.[0m[91m8.0
[fastapi] [0m[91m - fsspec==2026.7.0
[fastapi] + fsspec[0m[91m==2026.2.0[0m[91m
[fastapi] + [0m[91mgdown==6.2.0
[fastapi] [0m[91m+ hf-xet==1[0m[91m.6.0[0m[91m
[fastapi] [0m[91m + [0m[91mhttpcore2==[0m[91m2.[0m[91m13.0
[fastapi] + httpx2[0m[91m==2.13.0
[fastapi] + huggingface-hub==1.31.0[0m[91m
[fastapi] + [0m[91mimportlib-metadata==9[0m[91m.[0m[91m0.1
[fastapi] [0m[91m +[0m[91m importlib-resources[0m[91m==[0m[91m7.[0m[91m1.0[0m[91m
[fastapi] + [0m[91mitsdangerous==2.2.0
[fastapi] [0m[91m+ jaconv==0.5.0
[fastapi] [0m[91m+ janus==2.0.0
[fastapi] [0m[91m+ jiter==0[0m[91m.17.0[0m[91m
[fastapi] +[0m[91m [0m[91mjoblib[0m[91m==1.[0m[91m6.0[0m[91m
[fastapi] [0m[91m+ [0m[91mlangcheck==0.9[0m[91m.0[0m[91m
[fastapi] [0m[91m+[0m[91m liger-kernel[0m[91m==0.[0m[91m8.1[0m[91m
[fastapi] [0m[91m+ [0m[91mmarkdown-it-py[0m[91m==4.2.0
[fastapi] + mdurl==0.1.2
[fastapi] [0m[91m + multidict==6.8.0
[fastapi] [0m[91m+ multiprocess[0m[91m==[0m[91m0.70.19[0m[91m
[fastapi] [0m[91m + narwhals[0m[91m==2.26.0
[fastapi] + nest-asyncio==[0m[91m1.6.0
[fastapi] +[0m[91m nlpaug==1.1.[0m[91m11
[fastapi] +[0m[91m nltk==3.[0m[91m10.3
[fastapi] [0m[91m+ numpy==[0m[91m2.5.3[0m[91m
[fastapi] + [0m[91momegaconf==2.3[0m[91m.1
[fastapi] +[0m[91m openai==[0m[91m3.14.0[0m[91m
[fastapi] + [0m[91mpandas==3.0.5
[fastapi] + peft==0.19.1
[fastapi] [0m[91m + plotly==7.0[0m[91m.0
[fastapi] [0m[91m+[0m[91m propcache[0m[91m==0.5[0m[91m.2[0m[91m
[fastapi] [0m[91m + pyarrow==25.0.1
[fastapi] + pydantic[0m[91m==2.13.5
[fastapi] [0m[91m + pydantic-core[0m[91m==2.[0m[91m46.5
[fastapi] + pyphen==0.18.1[0m[91m
[fastapi] + [0m[91mpysocks==1.7.1
[fastapi] + regex[0m[91m==2026.[0m[91m9.10[0m[91m
[fastapi] +[0m[91m restrictedpython[0m[91m==[0m[91m8.0[0m[91m
[fastapi] [0m[91m+ [0m[91mretrying==[0m[91m1.[0m[91m4.2[0m[91m
[fastapi] [0m[91m+ rich[0m[91m==[0m[91m15.0.[0m[91m0
[fastapi] [0m[91m [0m[91m+ [0m[91mrouge-score[0m[91m==0.[0m[91m1.[0m[91m2
[fastapi] [0m[91m+ [0m[91msafetensors[0m[91m==0.[0m[91m8.0[0m[91m
[fastapi] [0m[91m+ scikit-learn==1.9.1[0m[91m
[fastapi] + scipy==1.18.1
[fastapi] + sentence-transformers==6.0.1[0m[91m
[fastapi] + sentencepiece==0[0m[91m.2.0
[fastapi] + shellingham[0m[91m==1.[0m[91m5.4[0m[91m
[fastapi] +[0m[91m six[0m[91m==1[0m[91m.17.[0m[91m0
[fastapi] + sniffio==1.3.[0m[91m1
[fastapi] +[0m[91m tabulate[0m[91m==0.10.[0m[91m0
[fastapi] [0m[91m+ textstat[0m[91m==0.[0m[91m7.8[0m[91m
[fastapi] [0m[91m+ threadpoolctl[0m[91m==3.6.0
[fastapi] + tokenizers==0.22.2
[fastapi] + tqdm==4.70.[0m[91m1
[fastapi] + transformers==5.12.1
[fastapi] + trl==1.5.1
[fastapi] + truststore==[0m[91m0.10.4[0m[91m
[fastapi] +[0m[91m typer[0m[91m==0[0m[91m.27.[0m[91m2
[fastapi] [0m[91m+ [0m[91mtyping-inspection==[0m[91m0.4.[0m[91m4[0m[91m
[fastapi] [0m[91m+ [0m[91mwerkzeug[0m[91m==3.[0m[91m1.8[0m[91m
[fastapi] [0m[91m + xxhash[0m[91m==4.[0m[91m0.[0m[91m1
[fastapi] [0m[91m [0m[91m+ [0m[91myarl==[0m[91m1.24[0m[91m.5[0m[91m
[fastapi] [0m[91m +[0m[91m zipp[0m[91m==[0m[91m4.1.[0m[91m0
[fastapi] [0m ---> ff666fc88b03
[fastapi] Step 4/10 : RUN ABI=$(python -c "import torch; print('TRUE' if torch._C._GLIBCXX_USE_CXX11_ABI else 'FALSE')")     && echo "torch cxx11 ABI: ${ABI}"     && uv pip install --system --no-cache         "https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu12torch2.9cxx11abi${ABI}-cp312-cp312-linux_x86_64.whl"     && python -c "import flash_attn; from flash_attn import flash_attn_func, flash_attn_varlen_func; print('flash-attn:', flash_attn.__version__)"
[fastapi] ---> Running in a4b0e7f66007
[fastapi] [91m[W915 12:19:39.152645045 AllocatorConfig.cpp:28] Warning: PYTORCH_CUDA_ALLOC_CONF is deprecated, use PYTORCH_ALLOC_CONF instead (function operator())
[fastapi] [0mtorch cxx11 ABI: TRUE
[fastapi] [91mUsing Python 3.12.13 environment at: /usr
[fastapi] [0m[91mResolved 28 packages in 3.19s
[fastapi] [0m[91mDownloading flash-attn (242.0MiB)
[fastapi] [0m[91m Downloaded flash-attn
[fastapi] [0m[91mPrepared 1 package in 2.35s
[fastapi] [0m[91mInstalled 1 package in 11ms
[fastapi] + flash-attn==2.8.3+cu12torch2.[0m[91m9cxx11abitrue (from https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu12torch2.9cxx11abiTRUE-cp312-cp312-linux_x86_64.whl)
[fastapi] [0mflash-attn: 2.8.3
[fastapi] [91m[W915 12:19:46.202294818 AllocatorConfig.cpp:28] Warning: PYTORCH_CUDA_ALLOC_CONF is deprecated, use PYTORCH_ALLOC_CONF instead (function operator())
[fastapi] [0m ---> cbe835ba256c
[fastapi] Step 5/10 : RUN TORCH_CUDA_ARCH_LIST="8.0;9.0+PTX" MAX_JOBS=4     pip install --no-cache-dir --no-build-isolation     causal-conv1d==1.6.2.post1 mamba-ssm==2.3.2.post1
[fastapi] ---> Running in 796da35b1272
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
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 43.5/43.5 MB 250.6 MB/s  0:00:00
[fastapi] Downloading apache_tvm_ffi-0.1.9-cp312-abi3-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (2.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.3/2.3 MB 287.8 MB/s  0:00:00
[fastapi] Downloading z3_solver-4.15.4.0-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (29.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 29.3/29.3 MB 213.1 MB/s  0:00:00
[fastapi] Downloading quack_kernels-0.6.5-py3-none-any.whl (729 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 729.6/729.6 kB 819.7 MB/s  0:00:00
[fastapi] Downloading nvidia_cutlass_dsl-4.7.1-py3-none-any.whl (10 kB)
[fastapi] Downloading nvidia_cutlass_dsl_libs_base-4.7.1-cp312-cp312-manylinux_2_28_x86_64.whl (2.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.8/2.8 MB 267.2 MB/s  0:00:00
[fastapi] Downloading nvidia_cutlass_dsl_libs_core-4.7.1-py3-none-any.whl (1.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 492.3 MB/s  0:00:00
[fastapi] Downloading nvidia_cutlass_dsl_libs_cu12-4.7.1-cp312-cp312-manylinux_2_28_x86_64.whl (88.7 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 88.7/88.7 MB 250.0 MB/s  0:00:00
[fastapi] Downloading nvidia_cuda_nvdisasm-13.4.49-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (5.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.2/5.2 MB 277.4 MB/s  0:00:00
[fastapi] Downloading cuda_python-13.4.1-py3-none-any.whl (7.6 kB)
[fastapi] Downloading cuda_bindings-13.4.1-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (7.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.2/7.2 MB 358.7 MB/s  0:00:00
[fastapi] Downloading cuda_core-1.2.0-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (6.6 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.6/6.6 MB 288.0 MB/s  0:00:00
[fastapi] Downloading cuda_pathfinder-1.8.1-py3-none-any.whl (62 kB)
[fastapi] Downloading protobuf-7.36.1-cp310-abi3-manylinux2014_x86_64.whl (343 kB)
[fastapi] Downloading ml_dtypes-0.6.0-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (409 kB)
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (183 kB)
[fastapi] Downloading torch_c_dlpack_ext-0.1.5-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (897 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 897.8/897.8 kB 805.8 MB/s  0:00:00
[fastapi] Building wheels for collected packages: causal-conv1d, mamba-ssm
[fastapi] Building wheel for causal-conv1d (pyproject.toml): started
[fastapi] Building wheel for causal-conv1d (pyproject.toml): finished with status 'done'
[fastapi] Created wheel for causal-conv1d: filename=causal_conv1d-1.6.2.post1-cp312-cp312-linux_x86_64.whl size=193795077 sha256=3d09789a5df2760a59c2064c4570a4ccd30315943581e9553eb1f412cd9e25a6
[fastapi] Stored in directory: /tmp/pip-ephem-wheel-cache-j3z1rxm4/wheels/ea/f0/26/5d87ae05a302e6dc8016c50cd8c7ee779585f593b9580e7cf8
[fastapi] Building wheel for mamba-ssm (pyproject.toml): started
[fastapi] Building wheel for mamba-ssm (pyproject.toml): finished with status 'done'
[fastapi] Created wheel for mamba-ssm: filename=mamba_ssm-2.3.2.post1-cp312-cp312-linux_x86_64.whl size=322246976 sha256=8fd21085d668a3bdbb1f7903c81f64434d7ed2c763240f8328a465a42370a7b6
[fastapi] Stored in directory: /tmp/pip-ephem-wheel-cache-j3z1rxm4/wheels/da/67/03/99148d6eeaa4ec2855d71295ac83bcbc8ba7b41a2982992c63
[fastapi] Successfully built causal-conv1d mamba-ssm
[fastapi] Installing collected packages: z3-solver, protobuf, nvidia-cuda-nvdisasm, ninja, ml-dtypes, cuda-pathfinder, apache-tvm-ffi, cuda-core, cuda-bindings, cuda-python, torch-c-dlpack-ext, nvidia-cutlass-dsl-libs-core, causal-conv1d, tilelang, nvidia-cutlass-dsl-libs-base, nvidia-cutlass-dsl-libs-cu12, nvidia-cutlass-dsl, quack-kernels, mamba-ssm
[fastapi] Successfully installed apache-tvm-ffi-0.1.9 causal-conv1d-1.6.2.post1 cuda-bindings-13.4.1 cuda-core-1.2.0 cuda-pathfinder-1.8.1 cuda-python-13.4.1 mamba-ssm-2.3.2.post1 ml-dtypes-0.6.0 ninja-1.13.2 nvidia-cuda-nvdisasm-13.4.49 nvidia-cutlass-dsl-4.7.1 nvidia-cutlass-dsl-libs-base-4.7.1 nvidia-cutlass-dsl-libs-core-4.7.1 nvidia-cutlass-dsl-libs-cu12-4.7.1 protobuf-7.36.1 quack-kernels-0.6.5 tilelang-0.1.8 torch-c-dlpack-ext-0.1.5 z3-solver-4.15.4.0
[fastapi] ---> a7c1112c418c
[fastapi] Step 6/10 : RUN uv pip install --system --no-cache --no-deps         flash-linear-attention==0.5.1 fla-core==0.5.1     && python -c "from fla.modules import FusedRMSNormGated; from fla.ops.gated_delta_rule import chunk_gated_delta_rule, fused_recurrent_gated_delta_rule"     && python -c "import torch; assert torch.__version__.startswith('2.9'), torch.__version__"
[fastapi] ---> Running in 82b6060dd78f
[fastapi] [91mUsing Python 3.12.13 environment at: /usr
[fastapi] [0m[91mResolved 2 packages in 46ms
[fastapi] [0m[91mPrepared 2 packages in 29ms
[fastapi] [0m[91mInstalled 2 packages in 19ms
[fastapi] + fla-core==0.5.1
[fastapi] + flash-linear-attention==0.5.1
[fastapi] [0m[91m/usr/local/lib/python3.12/dist-packages/fla/utils/_device.py:100: UserWarning: Triton is not supported on current platform, roll back to CPU.
[fastapi] _cpu_device_warning()
[fastapi] [0m[91m[W915 12:20:36.665356623 AllocatorConfig.cpp:28] Warning: PYTORCH_CUDA_ALLOC_CONF is deprecated, use PYTORCH_ALLOC_CONF instead (function operator())
[fastapi] [0m[91m[W915 12:20:37.110992332 AllocatorConfig.cpp:28] Warning: PYTORCH_CUDA_ALLOC_CONF is deprecated, use PYTORCH_ALLOC_CONF instead (function operator())
[fastapi] [0m ---> 1921d3de8472
[fastapi] Step 7/10 : WORKDIR /app
[fastapi] ---> Running in 7e8b2d9e4787
[fastapi] ---> d6f1e3e9fa75
[fastapi] Step 8/10 : COPY src /app/tenun
[fastapi] ---> 06c76c39b067
[fastapi] Step 9/10 : COPY pyproject.toml LICENSE.md NOTICE /app/
[fastapi] ---> dad271b7ebd3
[fastapi] Step 10/10 : ENTRYPOINT ["python", "-m", "tenun.cli"]
[fastapi] ---> Running in 23fee0e446a9
[fastapi] ---> fdff2813837e
[fastapi] {'aux': {'ID': 'sha256:fdff2813837eb1699f2cfe8802c57e9eb7437f1b5a320260ed2466d0f327f971'}}Successfully built fdff2813837e
[fastapi] Successfully tagged standalone-text-trainer:0e5c1cb2-1546-4ebe-9593-96d0a0254933
[fastapi] Docker image built successfully.
[fastapi] Container.wait() returned: {'StatusCode': 0}
[fastapi] Cleaning up
[fastapi] Cleaned up Docker resources.
[fastapi] Starting upload container hf-upload-c65f8e368fd44ee4844fce1a4e7e865f for task 87c51c39-914b-4c7f-a97a-4925c6ec58b3...
[hf-upload-c6] Updated adapter_config.json with base_model: unsloth/Qwen2.5-0.5B-Instruct
[hf-upload-c6] Updated README.md with base_model: unsloth/Qwen2.5-0.5B-Instruct
[hf-upload-c6] Creating repo gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5EcZmz41...
[hf-upload-c6] Uploading contents of /app/checkpoints/87c51c39-914b-4c7f-a97a-4925c6ec58b3/tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5EcZmz41 to gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5EcZmz41
[hf-upload-c6] Uploaded successfully to https://huggingface.co/gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5EcZmz41
[hf-upload-c6] Deleted local folder: /app/checkpoints/87c51c39-914b-4c7f-a97a-4925c6ec58b3/tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5EcZmz41
[text-trainer] [logs] init task_id='87c51c39-914b-4c7f-a97a-4925c6ec58b3' task_type='InstructTextTask' model='b254e84a30620233' hours=1.0 file_format='s3' use_kl=False kl_coef=0.0
[text-trainer] [logs] rows_loaded count=29022 source='/cache/datasets/87c51c39-914b-4c7f-a97a-4925c6ec58b3_train_data.json'
[text-trainer] [logs] attention_preflight eligible=True reason='supported'
[text-trainer] [logs] liger_preflight eligible=True reason='supported'
[text-trainer] [logs] model_loaded dir='/cache/models/b254e84a30620233' dtype='torch.bfloat16' tokenizer_rung='trc=False' model_rung='trc=False,attn=flash_attention_2' attn='flash_attention_2' liger=True fused_linear_cross_entropy=True
[text-trainer] [logs] baseline_stats keys=['dataset', 'task_type', 'throughput', 'training', 'weights']
[text-trainer] [logs] plan strategy='lora' kl=False rows=29022 lora_r=128 lr=0.0001 batch=70 grad_accum=1 epochs=3 params_b=0.494 n_gpus=1 per_gpu_gb=85.0
[text-trainer] [logs] floor_written rung='untrained_adapter'
[text-trainer] [logs] dev_split train=28143 dev=879 dup_groups=417
[text-trainer] [logs] rows_dropped_length kept=27924 dropped_overlong=219 dropped_unsupervised=0 max_len=4096
[text-trainer] [logs] rows_dropped_length kept=876 dropped_overlong=3 dropped_unsupervised=0 max_len=4096
[text-trainer] [logs] tokenized n=27924 seq_len=4096 ladder=[4096, 8192, 16384, 32768]
[text-trainer] [logs] rows_packed rows=27924 blocks=3202 gain=8.72 block_len=4096
[text-trainer] [logs] split train_n=3202 val_n=876 steps_per_epoch=45
[text-trainer] [logs] packing_mode packed=True attn='flash_attention_2' isolated=True block_len=4096
[text-trainer] [logs] lr_seed is_augment=False source='model_weight_rms' law=8.539239407063443e-05 bucket=0.0001
[text-trainer] [logs] lr_probe per_step=4.526 steps=8 batch=70 curvature=1.524 rel_drop=0.1711 lr='1.302e-04'
[text-trainer] [logs] lr_search_aborted reason='S1 too shallow (35st) to refine'
[text-trainer] [logs] lr_search mode='two_stage' candidates=3 scores={'6.524e-05': 1.21173, '1.034e-04': 1.20613, '1.639e-04': 1.2121} chosen='1.034e-04' batch=70 budget_s=641.2 tier='coarse' pruned=None skipped=1 dev_scored=False reason='142 probe-steps within 20%: S1 + refine on the surplus'
[text-trainer] [logs] lr_search_memory_released
[text-trainer] [logs] schedule lr=0.00010339997983682164 searched=True per_step_s=4.5098 epochs=4.0
[text-trainer] [logs] mirror_export ok=True
[text-trainer] [logs] mirror_export step=25 ok=True
[text-trainer] [logs] eval_skip_early skipped=2 until_epoch=0.75
[text-trainer] [logs] eval_cadence_widened eval_steps=26 eval_spent_s=48.8 elapsed_s=224.7
[text-trainer] [logs] best_export step=39 metric='eval_loss' value=1.33832
[text-trainer] [logs] eval_cadence_widened eval_steps=52 eval_spent_s=92.3 elapsed_s=327.0
[text-trainer] [logs] eval_cadence_widened eval_steps=104 eval_spent_s=135.8 elapsed_s=604.1
[text-trainer] [logs] eval_cadence_widened eval_steps=208 eval_spent_s=180.6 elapsed_s=1008.8
[text-trainer] [logs] soup_pool size=4
[text-trainer] [logs] best_export step=184 metric='eval_loss' value=1.32466
[text-trainer] [logs] soup_accept step=52 score=1.32466 members=2
[text-trainer] [logs] best_export step=184 metric='eval_loss' value=1.32093
[text-trainer] [logs] soup_accept step=104 score=1.32093 members=3
[text-trainer] [logs] soup_reject step=184 score=1.32718 best=1.32093
[text-trainer] [logs] soup_result verdict='soup' evals=3 final_loss=1.32093 members=3
[text-trainer] [logs] final_save ok=True source='soup'
[text-trainer] [logs] dev_pass ok=True steps=12
[text-trainer] [logs] run_complete
[text-trainer] [W915 12:51:34.599349841 AllocatorConfig.cpp:28] Warning: PYTORCH_CUDA_ALLOC_CONF is deprecated, use PYTORCH_ALLOC_CONF instead (function operator())