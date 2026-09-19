# Loki — task 059bf721-cca5-4d02-9832-a794cf37074b — hotkey 5CkYizfLyb5hLmcK4WtBGG13WKTQrynHBEV6qC23748g17zC
fetched 2026-09-19T04:59:30+00:00  lines=2653  hit_page_cap=False  containers=['downloader-059bf721-cca5-4d02-9832-a794cf37074b-1d4bce70', 'downloader-059bf721-cca5-4d02-9832-a794cf37074b-c67ca4c2', 'fastapi', 'hf-upload-bcac1c61a6f2439284dee025955d1270', 'text-trainer-1e69b4e3fc644431936bf32591be1506', 'text-trainer-b573bf55157c4d88a7bd29b0a601d73c']

[downloader-0] Downloading datasets to: /cache/datasets
[downloader-0] Downloading models to: /cache/models
[downloader-0] Model already cached at /cache/models/c5159aac10253479.
[downloader-0] Skipping download.
[downloader-0] Model path: /cache/models/c5159aac10253479
[downloader-0] Dataset path: /cache/datasets
[downloader-0] Downloading datasets to: /cache/datasets
[downloader-0] Downloading models to: /cache/models
[downloader-0] /usr/local/lib/python3.10/site-packages/huggingface_hub/utils/_validators.py:205: UserWarning: The `local_dir_use_symlinks` argument is deprecated and ignored in `snapshot_download`. Downloading to a local directory does not use symlinks anymore.
[downloader-0]   warnings.warn(
[downloader-0] Model path: /cache/models/c5159aac10253479
[downloader-0] Dataset path: /cache/datasets
[fastapi] Repository cloned successfully
[fastapi] Running Cache Download Container
[fastapi] Starting downloader container: downloader-059bf721-cca5-4d02-9832-a794cf37074b-c67ca4c2
[fastapi] Download completed successfully for task 059bf721-cca5-4d02-9832-a794cf37074b
[fastapi] Building Docker image 'standalone-text-trainer:d64c09cd-6e06-4a17-b949-43905edc47e2' (timeout=1800s)...
[fastapi] Step 1/13 : FROM runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04
[fastapi] ---> d451fe72f137
[fastapi] Step 2/13 : RUN apt-get update && apt-get install -y     vim zip tmux iotop nvtop bmon wget nano zsh htop     && rm -rf /var/lib/apt/lists/*
[fastapi] ---> Running in 1ed36ee67fd3
[fastapi] Get:1 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  InRelease [1578 B]
[fastapi] Get:2 http://archive.ubuntu.com/ubuntu jammy InRelease [270 kB]
[fastapi] Get:3 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  Packages [3011 kB]
[fastapi] Get:4 http://security.ubuntu.com/ubuntu jammy-security InRelease [129 kB]
[fastapi] Get:5 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [128 kB]
[fastapi] Get:6 http://archive.ubuntu.com/ubuntu jammy-backports InRelease [127 kB]
[fastapi] Get:7 http://archive.ubuntu.com/ubuntu jammy/multiverse amd64 Packages [266 kB]
[fastapi] Get:8 http://archive.ubuntu.com/ubuntu jammy/restricted amd64 Packages [164 kB]
[fastapi] Get:9 http://archive.ubuntu.com/ubuntu jammy/main amd64 Packages [1792 kB]
[fastapi] Get:10 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy InRelease [18.1 kB]
[fastapi] Get:11 http://archive.ubuntu.com/ubuntu jammy/universe amd64 Packages [17.5 MB]
[fastapi] Get:12 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 Packages [4624 kB]
[fastapi] Get:13 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy/main amd64 Packages [44.3 kB]
[fastapi] Get:14 http://archive.ubuntu.com/ubuntu jammy-updates/multiverse amd64 Packages [93.2 kB]
[fastapi] Get:15 http://archive.ubuntu.com/ubuntu jammy-updates/restricted amd64 Packages [8007 kB]
[fastapi] Get:16 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 Packages [1620 kB]
[fastapi] Get:17 http://archive.ubuntu.com/ubuntu jammy-backports/universe amd64 Packages [35.6 kB]
[fastapi] Get:18 http://archive.ubuntu.com/ubuntu jammy-backports/main amd64 Packages [82.8 kB]
[fastapi] Get:19 http://security.ubuntu.com/ubuntu jammy-security/main amd64 Packages [4290 kB]
[fastapi] Get:20 http://security.ubuntu.com/ubuntu jammy-security/multiverse amd64 Packages [84.6 kB]
[fastapi] Get:21 http://security.ubuntu.com/ubuntu jammy-security/restricted amd64 Packages [7717 kB]
[fastapi] Get:22 http://security.ubuntu.com/ubuntu jammy-security/universe amd64 Packages [1317 kB]
[fastapi] Fetched 51.3 MB in 3s (20.2 MB/s)
[fastapi] Reading package lists...
[fastapi] Reading package lists...
[fastapi] Building dependency tree...
[fastapi] Reading state information...
[fastapi] The following additional packages will be installed:
[fastapi] libconfuse-common libconfuse2 libevent-core-2.1-7 libgpm2 libnl-3-200
[fastapi] libnl-genl-3-200 libnl-route-3-200 libpython3.10 libpython3.10-minimal
[fastapi] libpython3.10-stdlib libsodium23 libutempter0 python3.10 python3.10-minimal
[fastapi] unzip vim-common vim-runtime xxd zsh-common
[fastapi] Suggested packages:
[fastapi] lm-sensors lsof strace gpm hunspell python3.10-venv python3.10-doc
[fastapi] binfmt-support ctags vim-doc vim-scripts zsh-doc
[fastapi] The following NEW packages will be installed:
[fastapi] bmon htop iotop libconfuse-common libconfuse2 libevent-core-2.1-7 libgpm2
[fastapi] libnl-3-200 libnl-genl-3-200 libnl-route-3-200 libpython3.10 libsodium23
[fastapi] libutempter0 nano nvtop tmux unzip vim vim-common vim-runtime xxd zip zsh
[fastapi] zsh-common
[fastapi] The following packages will be upgraded:
[fastapi] libpython3.10-minimal libpython3.10-stdlib python3.10 python3.10-minimal
[fastapi] wget
[fastapi] 5 upgraded, 24 newly installed, 0 to remove and 174 not upgraded.
[fastapi] Need to get 23.1 MB of archives.
[fastapi] After this operation, 67.7 MB of additional disk space will be used.
[fastapi] Get:1 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 python3.10 amd64 3.10.12-1~22.04.18 [508 kB]
[fastapi] Get:2 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libpython3.10-stdlib amd64 3.10.12-1~22.04.18 [1850 kB]
[fastapi] Get:3 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 python3.10-minimal amd64 3.10.12-1~22.04.18 [2277 kB]
[fastapi] Get:4 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libpython3.10-minimal amd64 3.10.12-1~22.04.18 [817 kB]
[fastapi] Get:5 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 xxd amd64 2:8.2.3995-1ubuntu2.36 [51.5 kB]
[fastapi] Get:6 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 vim-common all 2:8.2.3995-1ubuntu2.36 [81.5 kB]
[fastapi] Get:7 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 nano amd64 6.2-1ubuntu0.2 [280 kB]
[fastapi] Get:8 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 wget amd64 1.21.2-2ubuntu1.5 [339 kB]
[fastapi] Get:9 http://archive.ubuntu.com/ubuntu jammy/universe amd64 libconfuse-common all 3.3-2 [6004 B]
[fastapi] Get:10 http://archive.ubuntu.com/ubuntu jammy/universe amd64 libconfuse2 amd64 3.3-2 [26.0 kB]
[fastapi] Get:11 http://archive.ubuntu.com/ubuntu jammy/main amd64 libnl-3-200 amd64 3.5.0-0.1 [59.1 kB]
[fastapi] Get:12 http://archive.ubuntu.com/ubuntu jammy/main amd64 libnl-route-3-200 amd64 3.5.0-0.1 [180 kB]
[fastapi] Get:13 http://archive.ubuntu.com/ubuntu jammy/universe amd64 bmon amd64 1:4.0-8 [48.1 kB]
[fastapi] Get:14 http://archive.ubuntu.com/ubuntu jammy/main amd64 libnl-genl-3-200 amd64 3.5.0-0.1 [12.4 kB]
[fastapi] Get:15 http://archive.ubuntu.com/ubuntu jammy/main amd64 htop amd64 3.0.5-7build2 [128 kB]
[fastapi] Get:16 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 iotop amd64 0.6-24-g733f3f8-1.1ubuntu0.1 [23.1 kB]
[fastapi] Get:17 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libevent-core-2.1-7 amd64 2.1.12-stable-1ubuntu0.1 [94.2 kB]
[fastapi] Get:18 http://archive.ubuntu.com/ubuntu jammy/main amd64 libgpm2 amd64 1.20.7-10build1 [15.3 kB]
[fastapi] Get:19 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libpython3.10 amd64 3.10.12-1~22.04.18 [1950 kB]
[fastapi] Get:20 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libsodium23 amd64 1.0.18-1ubuntu0.22.04.1 [164 kB]
[fastapi] Get:21 http://archive.ubuntu.com/ubuntu jammy/main amd64 libutempter0 amd64 1.2.1-2build2 [8848 B]
[fastapi] Get:22 http://archive.ubuntu.com/ubuntu jammy/multiverse amd64 nvtop amd64 1.2.2-1 [43.9 kB]
[fastapi] Get:23 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 tmux amd64 3.2a-4ubuntu0.2 [428 kB]
[fastapi] Get:24 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 unzip amd64 6.0-26ubuntu3.2 [175 kB]
[fastapi] Get:25 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 vim-runtime all 2:8.2.3995-1ubuntu2.36 [6824 kB]
[fastapi] Get:26 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 vim amd64 2:8.2.3995-1ubuntu2.36 [1733 kB]
[fastapi] Get:27 http://archive.ubuntu.com/ubuntu jammy/main amd64 zip amd64 3.0-12build2 [176 kB]
[fastapi] Get:28 http://archive.ubuntu.com/ubuntu jammy/main amd64 zsh-common all 5.8.1-1 [3985 kB]
[fastapi] Get:29 http://archive.ubuntu.com/ubuntu jammy/main amd64 zsh amd64 5.8.1-1 [809 kB]
[fastapi] [91mdebconf: delaying package configuration, since apt-utils is not installed
[fastapi] [0mFetched 23.1 MB in 1s (29.2 MB/s)
[fastapi] (Reading database ... (Reading database ... 5%(Reading database ... 10%(Reading database ... 15%(Reading database ... 20%(Reading database ... 25%(Reading database ... 30%(Reading database ... 35%(Reading database ... 40%(Reading database ... 45%(Reading database ... 50%(Reading database ... 55%(Reading database ... 60%(Reading database ... 65%(Reading database ... 70%(Reading database ... 75%(Reading database ... 80%(Reading database ... 85%(Reading database ... 90%(Reading database ... 95%(Reading database ... 100%(Reading database ... 24286 files and directories currently installed.)
[fastapi] Preparing to unpack .../00-python3.10_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking python3.10 (3.10.12-1~22.04.18) over (3.10.12-1~22.04.9) ...
[fastapi] Preparing to unpack .../01-libpython3.10-stdlib_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking libpython3.10-stdlib:amd64 (3.10.12-1~22.04.18) over (3.10.12-1~22.04.9) ...
[fastapi] Preparing to unpack .../02-python3.10-minimal_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking python3.10-minimal (3.10.12-1~22.04.18) over (3.10.12-1~22.04.9) ...
[fastapi] Preparing to unpack .../03-libpython3.10-minimal_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking libpython3.10-minimal:amd64 (3.10.12-1~22.04.18) over (3.10.12-1~22.04.9) ...
[fastapi] Selecting previously unselected package xxd.
[fastapi] Preparing to unpack .../04-xxd_2%3a8.2.3995-1ubuntu2.36_amd64.deb ...
[fastapi] Unpacking xxd (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Selecting previously unselected package vim-common.
[fastapi] Preparing to unpack .../05-vim-common_2%3a8.2.3995-1ubuntu2.36_all.deb ...
[fastapi] Unpacking vim-common (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Selecting previously unselected package nano.
[fastapi] Preparing to unpack .../06-nano_6.2-1ubuntu0.2_amd64.deb ...
[fastapi] Unpacking nano (6.2-1ubuntu0.2) ...
[fastapi] Preparing to unpack .../07-wget_1.21.2-2ubuntu1.5_amd64.deb ...
[fastapi] Unpacking wget (1.21.2-2ubuntu1.5) over (1.21.2-2ubuntu1.1) ...
[fastapi] Selecting previously unselected package libconfuse-common.
[fastapi] Preparing to unpack .../08-libconfuse-common_3.3-2_all.deb ...
[fastapi] Unpacking libconfuse-common (3.3-2) ...
[fastapi] Selecting previously unselected package libconfuse2:amd64.
[fastapi] Preparing to unpack .../09-libconfuse2_3.3-2_amd64.deb ...
[fastapi] Unpacking libconfuse2:amd64 (3.3-2) ...
[fastapi] Selecting previously unselected package libnl-3-200:amd64.
[fastapi] Preparing to unpack .../10-libnl-3-200_3.5.0-0.1_amd64.deb ...
[fastapi] Unpacking libnl-3-200:amd64 (3.5.0-0.1) ...
[fastapi] Selecting previously unselected package libnl-route-3-200:amd64.
[fastapi] Preparing to unpack .../11-libnl-route-3-200_3.5.0-0.1_amd64.deb ...
[fastapi] Unpacking libnl-route-3-200:amd64 (3.5.0-0.1) ...
[fastapi] Selecting previously unselected package bmon.
[fastapi] Preparing to unpack .../12-bmon_1%3a4.0-8_amd64.deb ...
[fastapi] Unpacking bmon (1:4.0-8) ...
[fastapi] Selecting previously unselected package libnl-genl-3-200:amd64.
[fastapi] Preparing to unpack .../13-libnl-genl-3-200_3.5.0-0.1_amd64.deb ...
[fastapi] Unpacking libnl-genl-3-200:amd64 (3.5.0-0.1) ...
[fastapi] Selecting previously unselected package htop.
[fastapi] Preparing to unpack .../14-htop_3.0.5-7build2_amd64.deb ...
[fastapi] Unpacking htop (3.0.5-7build2) ...
[fastapi] Selecting previously unselected package iotop.
[fastapi] Preparing to unpack .../15-iotop_0.6-24-g733f3f8-1.1ubuntu0.1_amd64.deb ...
[fastapi] Unpacking iotop (0.6-24-g733f3f8-1.1ubuntu0.1) ...
[fastapi] Selecting previously unselected package libevent-core-2.1-7:amd64.
[fastapi] Preparing to unpack .../16-libevent-core-2.1-7_2.1.12-stable-1ubuntu0.1_amd64.deb ...
[fastapi] Unpacking libevent-core-2.1-7:amd64 (2.1.12-stable-1ubuntu0.1) ...
[fastapi] Selecting previously unselected package libgpm2:amd64.
[fastapi] Preparing to unpack .../17-libgpm2_1.20.7-10build1_amd64.deb ...
[fastapi] Unpacking libgpm2:amd64 (1.20.7-10build1) ...
[fastapi] Selecting previously unselected package libpython3.10:amd64.
[fastapi] Preparing to unpack .../18-libpython3.10_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking libpython3.10:amd64 (3.10.12-1~22.04.18) ...
[fastapi] Selecting previously unselected package libsodium23:amd64.
[fastapi] Preparing to unpack .../19-libsodium23_1.0.18-1ubuntu0.22.04.1_amd64.deb ...
[fastapi] Unpacking libsodium23:amd64 (1.0.18-1ubuntu0.22.04.1) ...
[fastapi] Selecting previously unselected package libutempter0:amd64.
[fastapi] Preparing to unpack .../20-libutempter0_1.2.1-2build2_amd64.deb ...
[fastapi] Unpacking libutempter0:amd64 (1.2.1-2build2) ...
[fastapi] Selecting previously unselected package nvtop.
[fastapi] Preparing to unpack .../21-nvtop_1.2.2-1_amd64.deb ...
[fastapi] Unpacking nvtop (1.2.2-1) ...
[fastapi] Selecting previously unselected package tmux.
[fastapi] Preparing to unpack .../22-tmux_3.2a-4ubuntu0.2_amd64.deb ...
[fastapi] Unpacking tmux (3.2a-4ubuntu0.2) ...
[fastapi] Selecting previously unselected package unzip.
[fastapi] Preparing to unpack .../23-unzip_6.0-26ubuntu3.2_amd64.deb ...
[fastapi] Unpacking unzip (6.0-26ubuntu3.2) ...
[fastapi] Selecting previously unselected package vim-runtime.
[fastapi] Preparing to unpack .../24-vim-runtime_2%3a8.2.3995-1ubuntu2.36_all.deb ...
[fastapi] Adding 'diversion of /usr/share/vim/vim82/doc/help.txt to /usr/share/vim/vim82/doc/help.txt.vim-tiny by vim-runtime'
[fastapi] Adding 'diversion of /usr/share/vim/vim82/doc/tags to /usr/share/vim/vim82/doc/tags.vim-tiny by vim-runtime'
[fastapi] Unpacking vim-runtime (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Selecting previously unselected package vim.
[fastapi] Preparing to unpack .../25-vim_2%3a8.2.3995-1ubuntu2.36_amd64.deb ...
[fastapi] Unpacking vim (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Selecting previously unselected package zip.
[fastapi] Preparing to unpack .../26-zip_3.0-12build2_amd64.deb ...
[fastapi] Unpacking zip (3.0-12build2) ...
[fastapi] Selecting previously unselected package zsh-common.
[fastapi] Preparing to unpack .../27-zsh-common_5.8.1-1_all.deb ...
[fastapi] Unpacking zsh-common (5.8.1-1) ...
[fastapi] Selecting previously unselected package zsh.
[fastapi] Preparing to unpack .../28-zsh_5.8.1-1_amd64.deb ...
[fastapi] Unpacking zsh (5.8.1-1) ...
[fastapi] Setting up nvtop (1.2.2-1) ...
[fastapi] Setting up libsodium23:amd64 (1.0.18-1ubuntu0.22.04.1) ...
[fastapi] Setting up libgpm2:amd64 (1.20.7-10build1) ...
[fastapi] Setting up wget (1.21.2-2ubuntu1.5) ...
[fastapi] Setting up zsh-common (5.8.1-1) ...
[fastapi] Setting up unzip (6.0-26ubuntu3.2) ...
[fastapi] Setting up xxd (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Setting up zip (3.0-12build2) ...
[fastapi] Setting up iotop (0.6-24-g733f3f8-1.1ubuntu0.1) ...
[fastapi] update-alternatives: using /usr/sbin/iotop-py to provide /usr/sbin/iotop (iotop) in auto mode
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/man8/iotop.8.gz because associated file /usr/share/man/man8/iotop-py.8.gz (of link group iotop) doesn't exist
[fastapi] Setting up vim-common (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Setting up libevent-core-2.1-7:amd64 (2.1.12-stable-1ubuntu0.1) ...
[fastapi] Setting up libpython3.10-minimal:amd64 (3.10.12-1~22.04.18) ...
[fastapi] Setting up libutempter0:amd64 (1.2.1-2build2) ...
[fastapi] Setting up nano (6.2-1ubuntu0.2) ...
[fastapi] update-alternatives: using /bin/nano to provide /usr/bin/editor (editor) in auto mode
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/man1/editor.1.gz because associated file /usr/share/man/man1/nano.1.gz (of link group editor) doesn't exist
[fastapi] update-alternatives: using /bin/nano to provide /usr/bin/pico (pico) in auto mode
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/man1/pico.1.gz because associated file /usr/share/man/man1/nano.1.gz (of link group pico) doesn't exist
[fastapi] Setting up libconfuse-common (3.3-2) ...
[fastapi] Setting up libnl-3-200:amd64 (3.5.0-0.1) ...
[fastapi] Setting up zsh (5.8.1-1) ...
[fastapi] Setting up vim-runtime (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Setting up libconfuse2:amd64 (3.3-2) ...
[fastapi] Setting up tmux (3.2a-4ubuntu0.2) ...
[fastapi] Setting up python3.10-minimal (3.10.12-1~22.04.18) ...
[fastapi] Setting up libnl-route-3-200:amd64 (3.5.0-0.1) ...
[fastapi] Setting up libpython3.10-stdlib:amd64 (3.10.12-1~22.04.18) ...
[fastapi] Setting up bmon (1:4.0-8) ...
[fastapi] Setting up libnl-genl-3-200:amd64 (3.5.0-0.1) ...
[fastapi] Setting up libpython3.10:amd64 (3.10.12-1~22.04.18) ...
[fastapi] Setting up vim (2:8.2.3995-1ubuntu2.36) ...
[fastapi] update-alternatives: using /usr/bin/vim.basic to provide /usr/bin/vim (vim) in auto mode
[fastapi] update-alternatives: using /usr/bin/vim.basic to provide /usr/bin/vimdiff (vimdiff) in auto mode
[fastapi] update-alternatives: using /usr/bin/vim.basic to provide /usr/bin/rvim (rvim) in auto mode
[fastapi] update-alternatives: using /usr/bin/vim.basic to provide /usr/bin/rview (rview) in auto mode
[fastapi] update-alternatives: using /usr/bin/vim.basic to provide /usr/bin/vi (vi) in auto mode
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/da/man1/vi.1.gz because associated file /usr/share/man/da/man1/vim.1.gz (of link group vi) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/de/man1/vi.1.gz because associated file /usr/share/man/de/man1/vim.1.gz (of link group vi) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/fr/man1/vi.1.gz because associated file /usr/share/man/fr/man1/vim.1.gz (of link group vi) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/it/man1/vi.1.gz because associated file /usr/share/man/it/man1/vim.1.gz (of link group vi) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/ja/man1/vi.1.gz because associated file /usr/share/man/ja/man1/vim.1.gz (of link group vi) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/pl/man1/vi.1.gz because associated file /usr/share/man/pl/man1/vim.1.gz (of link group vi) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/ru/man1/vi.1.gz because associated file /usr/share/man/ru/man1/vim.1.gz (of link group vi) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/man1/vi.1.gz because associated file /usr/share/man/man1/vim.1.gz (of link group vi) doesn't exist
[fastapi] update-alternatives: using /usr/bin/vim.basic to provide /usr/bin/view (view) in auto mode
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/da/man1/view.1.gz because associated file /usr/share/man/da/man1/vim.1.gz (of link group view) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/de/man1/view.1.gz because associated file /usr/share/man/de/man1/vim.1.gz (of link group view) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/fr/man1/view.1.gz because associated file /usr/share/man/fr/man1/vim.1.gz (of link group view) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/it/man1/view.1.gz because associated file /usr/share/man/it/man1/vim.1.gz (of link group view) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/ja/man1/view.1.gz because associated file /usr/share/man/ja/man1/vim.1.gz (of link group view) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/pl/man1/view.1.gz because associated file /usr/share/man/pl/man1/vim.1.gz (of link group view) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/ru/man1/view.1.gz because associated file /usr/share/man/ru/man1/vim.1.gz (of link group view) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/man1/view.1.gz because associated file /usr/share/man/man1/vim.1.gz (of link group view) doesn't exist
[fastapi] update-alternatives: using /usr/bin/vim.basic to provide /usr/bin/ex (ex) in auto mode
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/da/man1/ex.1.gz because associated file /usr/share/man/da/man1/vim.1.gz (of link group ex) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/de/man1/ex.1.gz because associated file /usr/share/man/de/man1/vim.1.gz (of link group ex) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/fr/man1/ex.1.gz because associated file /usr/share/man/fr/man1/vim.1.gz (of link group ex) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/it/man1/ex.1.gz because associated file /usr/share/man/it/man1/vim.1.gz (of link group ex) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/ja/man1/ex.1.gz because associated file /usr/share/man/ja/man1/vim.1.gz (of link group ex) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/pl/man1/ex.1.gz because associated file /usr/share/man/pl/man1/vim.1.gz (of link group ex) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/ru/man1/ex.1.gz because associated file /usr/share/man/ru/man1/vim.1.gz (of link group ex) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/man1/ex.1.gz because associated file /usr/share/man/man1/vim.1.gz (of link group ex) doesn't exist
[fastapi] Setting up python3.10 (3.10.12-1~22.04.18) ...
[fastapi] Setting up htop (3.0.5-7build2) ...
[fastapi] Processing triggers for mailcap (3.70+nmu1ubuntu1) ...
[fastapi] Processing triggers for libc-bin (2.35-0ubuntu3.9) ...
[fastapi] ---> de54396eae60
[fastapi] Step 3/13 : RUN mkdir -p /workspace /cache /workspace/scripts/datasets /app/checkpoints
[fastapi] ---> Running in 68d07eee7e13
[fastapi] ---> 39147c584d44
[fastapi] Step 4/13 : WORKDIR /workspace/scripts
[fastapi] ---> Running in 8935e7600ae3
[fastapi] ---> d72c20b2a946
[fastapi] Step 5/13 : COPY scripts/training_requirements.txt /workspace/scripts/training_requirements.txt
[fastapi] ---> 582e4c741673
[fastapi] Step 6/13 : COPY scripts/grpo_requirements.txt /workspace/scripts/grpo_requirements.txt
[fastapi] ---> 3fefeaf6e25f
[fastapi] Step 7/13 : RUN pip install uv &&     pip install -U packaging==23.2 setuptools==75.8.0 wheel ninja &&     uv pip install -r /workspace/scripts/training_requirements.txt --system &&     pip install tenacity==9.1.2 tiktoken==0.9.0 &&     pip install https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu12torch2.8cxx11abiTRUE-cp311-cp311-linux_x86_64.whl &&     pip install "fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0"
[fastapi] ---> Running in 54e1cf7fab6f
[fastapi] Collecting uv
[fastapi] Downloading uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] Downloading uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.1 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 20.1/20.1 MB 350.1 MB/s eta 0:00:00
[fastapi] Installing collected packages: uv
[fastapi] Successfully installed uv-0.12.15
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 25.0.1 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0mCollecting packaging==23.2
[fastapi] Downloading packaging-23.2-py3-none-any.whl.metadata (3.2 kB)
[fastapi] Collecting setuptools==75.8.0
[fastapi] Downloading setuptools-75.8.0-py3-none-any.whl.metadata (6.7 kB)
[fastapi] Requirement already satisfied: wheel in /usr/local/lib/python3.11/dist-packages (0.45.1)
[fastapi] Collecting wheel
[fastapi] Downloading wheel-0.48.0-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Collecting ninja
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (5.4 kB)
[fastapi] INFO: pip is looking at multiple versions of wheel to determine which version is compatible with other requirements. This could take a while.
[fastapi] Collecting wheel
[fastapi] Downloading wheel-0.47.0-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Downloading wheel-0.46.3-py3-none-any.whl.metadata (2.4 kB)
[fastapi] Downloading wheel-0.46.2-py3-none-any.whl.metadata (2.4 kB)
[fastapi] Downloading packaging-23.2-py3-none-any.whl (53 kB)
[fastapi] Downloading setuptools-75.8.0-py3-none-any.whl (1.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 123.9 MB/s eta 0:00:00
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (183 kB)
[fastapi] Installing collected packages: setuptools, packaging, ninja
[fastapi] Attempting uninstall: setuptools
[fastapi] Found existing installation: setuptools 77.0.1
[fastapi] Uninstalling setuptools-77.0.1:
[fastapi] Successfully uninstalled setuptools-77.0.1
[fastapi] Attempting uninstall: packaging
[fastapi] Found existing installation: packaging 24.2
[fastapi] Uninstalling packaging-24.2:
[fastapi] Successfully uninstalled packaging-24.2
[fastapi] Successfully installed ninja-1.13.2 packaging-23.2 setuptools-75.8.0
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 25.0.1 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0m[91mUsing Python 3.11.11 environment at: /usr
[fastapi] [0m[91mResolved 191 packages in 1.56s
[fastapi] [0m[91m   Building deepspeed==0.19.2
[fastapi] [0m[91m   Building rouge-score==0.1.2
[fastapi] [0m[91mDownloading scikit-learn (8.9MiB)
[fastapi] [0m[91mDownloading fonttools (5.2MiB)
[fastapi] [0m[91mDownloading hf-xet (4.3MiB)
[fastapi] [0m[91mDownloading sqlalchemy (3.3MiB)
[fastapi] [0m[91mDownloading tokenizers (3.1MiB)
[fastapi] [0m[91mDownloading pycryptodome (2.2MiB)
[fastapi] [0m[91mDownloading pyphen (2.0MiB)
[fastapi] [0m[91mDownloading pydantic-core (2.0MiB)
[fastapi] [0m[91mDownloading openai (1.9MiB)
[fastapi] [0m[91mDownloading nltk (1.7MiB)
[fastapi] [0m[91mDownloading kiwisolver (1.4MiB)
[fastapi] [0m[91mDownloading pyarrow (47.7MiB)
[fastapi] [0m[91mDownloading nvidia-nvjitlink-cu12 (37.4MiB)
[fastapi] [0m[91mDownloading sentencepiece (1.2MiB)
[fastapi] [0m[91mDownloading nvidia-cublas-cu12 (566.8MiB)
[fastapi] [0m[91mDownloading cryptography (4.5MiB)
[fastapi] [0m[91mDownloading mpi4py (1.3MiB)
[fastapi] [0m[91mDownloading matplotlib (9.4MiB)
[fastapi] [0m[91mDownloading nvidia-cudnn-cu12 (674.0MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-cupti-cu12 (9.8MiB)
[fastapi] [0m[91mDownloading mlflow-tracing (1.7MiB)
[fastapi] [0m[91mDownloading pandas (12.5MiB)
[fastapi] [0m[91mDownloading wandb (20.4MiB)
[fastapi] [0m[91mDownloading bitsandbytes (57.8MiB)
[fastapi] [0m[91mDownloading nvidia-cufile-cu12 (1.1MiB)
[fastapi] [0m[91mDownloading triton (148.3MiB)
[fastapi] [0m[91mDownloading nvidia-cusparse-cu12 (274.9MiB)
[fastapi] [0m[91mDownloading mlflow-skinny (3.5MiB)
[fastapi] [0m[91mDownloading dash (8.5MiB)
[fastapi] [0m[91mDownloading aiohttp (1.7MiB)
[fastapi] [0m[91mDownloading scipy (35.9MiB)
[fastapi] [0m[91mDownloading grpcio (6.9MiB)
[fastapi] [0m[91mDownloading transformers (10.6MiB)
[fastapi] [0m[91mDownloading torch (846.9MiB)
[fastapi] [0m[91mDownloading mlflow (11.0MiB)
[fastapi] [0m[91mDownloading tensorboard-data-server (6.3MiB)
[fastapi] [0m[91mDownloading nvidia-cusolver-cu12 (255.1MiB)
[fastapi] [0m[91mDownloading nvidia-cufft-cu12 (184.2MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-nvrtc-cu12 (84.0MiB)
[fastapi] [0m[91mDownloading plotly (9.2MiB)
[fastapi] [0m[91mDownloading nvidia-curand-cu12 (60.7MiB)
[fastapi] [0m[91mDownloading nvidia-cusparselt-cu12 (273.9MiB)
[fastapi] [0m[91mDownloading tensorboard (5.2MiB)
[fastapi] [0m[91mDownloading nvidia-nccl-cu12 (307.4MiB)
[fastapi] [0m[91m Downloaded sentencepiece
[fastapi] Downloaded mpi4py
[fastapi] Downloaded nvidia-cufile-cu12
[fastapi] [0m[91m Downloaded kiwisolver
[fastapi] [0m[91m      Built rouge-score==0.1.2
[fastapi] [0m[91m Downloaded nltk
[fastapi] [0m[91m Downloaded mlflow-tracing
[fastapi] Downloaded aiohttp
[fastapi] [0m[91m Downloaded openai
[fastapi] [0m[91m Downloaded pydantic-core
[fastapi] [0m[91m Downloaded pyphen
[fastapi] [0m[91m Downloaded pycryptodome
[fastapi] [0m[91m   Building antlr4-python3-runtime==4.9.3
[fastapi] [0m[91m Downloaded tokenizers
[fastapi] [0m[91m Downloaded sqlalchemy
[fastapi] [0m[91m Downloaded mlflow-skinny
[fastapi] [0m[91m Downloaded hf-xet
[fastapi] [0m[91m Downloaded cryptography
[fastapi] [0m[91m      Built antlr4-python3-runtime==4.9.3
[fastapi] [0m[91m Downloaded fonttools
[fastapi] [0m[91m Downloaded tensorboard
[fastapi] [0m[91m Downloaded tensorboard-data-server
[fastapi] [0m[91m Downloaded grpcio
[fastapi] [0m[91m Downloaded dash
[fastapi] [0m[91m Downloaded scikit-learn
[fastapi] [0m[91m Downloaded matplotlib
[fastapi] [0m[91m Downloaded plotly
[fastapi] [0m[91m Downloaded nvidia-cuda-cupti-cu12
[fastapi] [0m[91m Downloaded transformers
[fastapi] [0m[91m Downloaded mlflow
[fastapi] [0m[91m Downloaded pandas
[fastapi] [0m[91m Downloaded wandb
[fastapi] [0m[91m Downloaded scipy
[fastapi] [0m[91m      Built deepspeed==0.19.2
[fastapi] [0m[91m Downloaded nvidia-nvjitlink-cu12
[fastapi] [0m[91m Downloaded pyarrow
[fastapi] [0m[91m Downloaded bitsandbytes
[fastapi] [0m[91m Downloaded nvidia-curand-cu12
[fastapi] [0m[91m Downloaded nvidia-cuda-nvrtc-cu12
[fastapi] [0m[91m Downloaded triton
[fastapi] [0m[91m Downloaded nvidia-cufft-cu12
[fastapi] [0m[91m Downloaded nvidia-cusparse-cu12
[fastapi] [0m[91m Downloaded nvidia-cusolver-cu12
[fastapi] [0m[91m Downloaded nvidia-cusparselt-cu12
[fastapi] [0m[91m Downloaded nvidia-nccl-cu12
[fastapi] [0m[91m Downloaded nvidia-cublas-cu12
[fastapi] [0m[91m Downloaded nvidia-cudnn-cu12
[fastapi] [0m[91m Downloaded torch
[fastapi] [0m[91mPrepared 158 packages in 9.57s
[fastapi] [0m[91mUninstalled 22 packages in 1.10s
[fastapi] [0m[91mInstalled 158 packages in 293ms
[fastapi] [0m[91m + absl-py==2.5.0
[fastapi] + accelerate==1.14.0
[fastapi] + aiohappyeyeballs==2.7.1
[fastapi] + aiohttp==3.14.3
[fastapi] + aiosignal==1.4.0
[fastapi] + alembic==1.20.0
[fastapi] +[0m[91m annotated-doc==0.0.5
[fastapi] + annotated-types==0.8.0
[fastapi] + antlr4-python3-runtime==4.9.3[0m[91m
[fastapi] - anyio[0m[91m==4.9.0
[fastapi] [0m[91m + anyio==4.15.1
[fastapi] [0m[91m [0m[91m+ astor==0.8[0m[91m.1
[fastapi] + bitsandbytes==0.49.2
[fastapi] + blinker[0m[91m==1.9.0
[fastapi] + cachetools==7.1.8
[fastapi] - [0m[91mcffi==1.17.1[0m[91m
[fastapi] + cffi==2.1.1[0m[91m
[fastapi] + click==8.5.0[0m[91m
[fastapi] [0m[91m + cloudpickle==[0m[91m3[0m[91m.1[0m[91m.2
[fastapi] + cmudict==1.1.3
[fastapi] + [0m[91mcontourpy==1.3.3
[fastapi] + cryptography[0m[91m==50.0[0m[91m.1
[fastapi] [0m[91m + [0m[91mcycler==0.12.1
[fastapi] + dash==4.4.1
[fastapi] + [0m[91mdatabricks-sdk==0.139.0
[fastapi] + datasets[0m[91m==5.0.[0m[91m1
[fastapi] [0m[91m+ deepspeed[0m[91m==0.19.2
[fastapi] [0m[91m+ detoxify[0m[91m==0.5.[0m[91m2
[fastapi] [0m[91m+ [0m[91mdill==0[0m[91m.4.[0m[91m1
[fastapi] [0m[91m+ [0m[91mdocker==7.2.0
[fastapi] + docker-pycreds==0.[0m[91m4.0
[fastapi] + einops==0[0m[91m.8.1
[fastapi] [0m[91m+ fastapi==0.141.1
[fastapi] + flask[0m[91m==3.1.3
[fastapi] + flask-cors[0m[91m==6.0.[0m[91m5
[fastapi] [0m[91m +[0m[91m fonttools==4.65.0
[fastapi] +[0m[91m frozenlist==1.8.0
[fastapi] [0m[91m+ gdown==6.3.[0m[91m0
[fastapi] [0m[91m+ gitdb[0m[91m==[0m[91m4.0.[0m[91m12
[fastapi] +[0m[91m gitpython[0m[91m==3.1[0m[91m.[0m[91m62
[fastapi] +[0m[91m [0m[91mgoogle-auth==2[0m[91m.58[0m[91m.[0m[91m0
[fastapi] + [0m[91mgraphene[0m[91m==3.[0m[91m4.3
[fastapi] [0m[91m + graphql-core[0m[91m==3.2[0m[91m.12
[fastapi] +[0m[91m graphql-relay[0m[91m==3.2.0
[fastapi] + greenlet==3.5[0m[91m.6
[fastapi] + grpcio==1.[0m[91m84.0
[fastapi] [0m[91m+ [0m[91mgunicorn==26[0m[91m.2[0m[91m.0
[fastapi] [0m[91m- h11==0.14.[0m[91m0
[fastapi] + h11==0.16.0
[fastapi] [0m[91m + hf-xet==1[0m[91m.6.0
[fastapi] [0m[91m + hjson[0m[91m==3.1.0[0m[91m
[fastapi] - httpcore==1.0.7
[fastapi] + httpcore[0m[91m==1.0.9
[fastapi] [0m[91m +[0m[91m httpcore2==[0m[91m2.13.0
[fastapi] + httpx2[0m[91m==2.13.0
[fastapi] [0m[91m +[0m[91m huey[0m[91m==3.4.0[0m[91m
[fastapi] + huggingface-hub==1.31.0
[fastapi] - idna==[0m[91m3.10
[fastapi] + idna==3.19
[fastapi] + importlib-metadata[0m[91m==9.0.1
[fastapi] + importlib-resources==[0m[91m7.1.0
[fastapi] +[0m[91m itsdangerous==2.2.[0m[91m0
[fastapi] +[0m[91m jaconv==[0m[91m0.5.0
[fastapi] +[0m[91m janus==2[0m[91m.0.0
[fastapi] [0m[91m+ jiter==[0m[91m0.17.0
[fastapi] + joblib==1[0m[91m.6.0
[fastapi] + kiwisolver==1.5.1
[fastapi] + langcheck==[0m[91m0.9.0
[fastapi] + liger-kernel[0m[91m==0.8.[0m[91m2[0m[91m
[fastapi] + [0m[91mmako[0m[91m==1.4.[0m[91m1
[fastapi] [0m[91m + markdown==3.10.3
[fastapi] +[0m[91m matplotlib==3.11.2
[fastapi] [0m[91m+ minio==[0m[91m7.2.20[0m[91m
[fastapi] [0m[91m + [0m[91mmlflow==3.16[0m[91m.0
[fastapi] + mlflow-skinny==3.16.0[0m[91m
[fastapi] + mlflow-tracing==3.[0m[91m16.0
[fastapi] [0m[91m+ mpi4py[0m[91m==[0m[91m4.1.2[0m[91m
[fastapi] +[0m[91m msgpack[0m[91m==1.2.2
[fastapi] + multidict[0m[91m==6.8.0
[fastapi] [0m[91m [0m[91m+[0m[91m multiprocess==0.70[0m[91m.19
[fastapi] + narwhals==2.26.0
[fastapi] [0m[91m+ nlpaug==1.1.11[0m[91m
[fastapi] + [0m[91mnltk==3.[0m[91m10[0m[91m.3
[fastapi] [0m[91m- [0m[91mnvidia-cublas-cu12==12[0m[91m.8.[0m[91m3.14
[fastapi] + nvidia-cublas-cu12==12.8.[0m[91m4.1
[fastapi] - nvidia-cuda-cupti-cu12==12.8[0m[91m.57
[fastapi] +[0m[91m nvidia-cuda-cupti-cu12==[0m[91m12.[0m[91m8.90
[fastapi] - nvidia-cuda-nvrtc-cu12==12[0m[91m.8.61
[fastapi] +[0m[91m nvidia-cuda-nvrtc-cu12==12[0m[91m.[0m[91m8.93
[fastapi] [0m[91m- nvidia-cuda-runtime-cu12==12.8.57
[fastapi] + nvidia-cuda-runtime-cu12==12.8[0m[91m.90
[fastapi] - nvidia-cudnn-cu12[0m[91m==9.8.[0m[91m0.[0m[91m87
[fastapi] [0m[91m+[0m[91m nvidia-cudnn-cu12==[0m[91m9.10[0m[91m.2.21[0m[91m
[fastapi] - [0m[91mnvidia-cufft-cu12==11[0m[91m.[0m[91m3.3.[0m[91m41
[fastapi] [0m[91m+ [0m[91mnvidia-cufft-cu12==11.3.[0m[91m3.83
[fastapi] [0m[91m - [0m[91mnvidia-cufile-cu12[0m[91m==[0m[91m1.13.0[0m[91m.[0m[91m11
[fastapi] [0m[91m+ [0m[91mnvidia-cufile-cu12==[0m[91m1[0m[91m.13.1[0m[91m.3[0m[91m
[fastapi] [0m[91m - [0m[91mnvidia-curand-cu12==[0m[91m10.3.[0m[91m9.[0m[91m55
[fastapi] [0m[91m + [0m[91mnvidia-curand-cu12[0m[91m==10.[0m[91m3[0m[91m.9.90[0m[91m
[fastapi] [0m[91m - nvidia-cusolver-cu12[0m[91m==11.[0m[91m7.[0m[91m2.55[0m[91m
[fastapi] [0m[91m+ nvidia-cusolver-cu12[0m[91m==11.7.3.90
[fastapi] - nvidia-cusparse-cu12[0m[91m==12.5.7.53
[fastapi] + nvidia-cusparse-cu12==12.5.8[0m[91m.93
[fastapi] [0m[91m -[0m[91m nvidia-cusparselt-cu12==[0m[91m0.6[0m[91m.3
[fastapi] [0m[91m +[0m[91m nvidia-cusparselt-cu12==0.7[0m[91m.1
[fastapi] - nvidia-nccl-cu12[0m[91m==2.25.1
[fastapi] + nvidia-nccl-cu12==[0m[91m2.27.3
[fastapi] [0m[91m -[0m[91m nvidia-nvjitlink-cu12==12[0m[91m.8.61[0m[91m
[fastapi] [0m[91m+ nvidia-nvjitlink-cu12[0m[91m==12.8.93
[fastapi] [0m[91m- [0m[91mnvidia-nvtx-cu12==[0m[91m12.[0m[91m8.55
[fastapi] [0m[91m +[0m[91m [0m[91mnvidia-nvtx-cu12==12.[0m[91m8.90[0m[91m
[fastapi] + omegaconf==2[0m[91m.3.1[0m[91m
[fastapi] [0m[91m+ openai==3.14.1
[fastapi] + opentelemetry-api[0m[91m==1.44.0
[fastapi] + opentelemetry-proto[0m[91m==1.44.[0m[91m0
[fastapi] [0m[91m + [0m[91mopentelemetry-sdk[0m[91m==1.44.[0m[91m0
[fastapi] + opentelemetry-semantic-conventions[0m[91m==0.65b[0m[91m0
[fastapi] +[0m[91m pandas==2.2.[0m[91m3[0m[91m
[fastapi] [0m[91m+ peft[0m[91m==0.[0m[91m19.[0m[91m1
[fastapi] [0m[91m+ [0m[91mplotly==[0m[91m7.1[0m[91m.0[0m[91m
[fastapi] +[0m[91m prettytable[0m[91m==3[0m[91m.18[0m[91m.0
[fastapi] [0m[91m [0m[91m+ [0m[91mpropcache[0m[91m==0.5[0m[91m.4[0m[91m
[fastapi] [0m[91m+[0m[91m protobuf==6.33.6[0m[91m
[fastapi] + [0m[91mpy-cpuinfo==9.0.0
[fastapi] +[0m[91m pyarrow==25.0[0m[91m.1
[fastapi] + [0m[91mpyasn1[0m[91m==0[0m[91m.6.[0m[91m4
[fastapi] [0m[91m+ [0m[91mpyasn1-modules==[0m[91m0.[0m[91m4.2
[fastapi] [0m[91m +[0m[91m [0m[91mpycryptodome[0m[91m==3.23.[0m[91m0
[fastapi] [0m[91m+[0m[91m pydantic[0m[91m==2[0m[91m.13.5
[fastapi] [0m[91m +[0m[91m pydantic-core==2.46.5
[fastapi] + pyparsing==3.3.2
[fastapi] + pyphen==0.18.1
[fastapi] + pysocks==1.7.1
[fastapi] + python-dotenv==1.2.3
[fastapi] + pytz==2026.3.post1
[fastapi] + regex==2026.9.10
[fastapi] + restrictedpython==8.0
[fastapi] + retrying==1.4.2
[fastapi] + rouge-score==0.1.2
[fastapi] + safetensors==0.8.0
[fastapi] + scikit-learn==1.9.1
[fastapi] + scipy==1.15.2
[fastapi] + sentence-transformers==6.0.1
[fastapi] + sentencepiece==0.2.0
[fastapi] + sentry-sdk==2.69.2
[fastapi] + setproctitle==1.3.7
[fastapi] + six==1.17.0
[fastapi] + skops==0.15.0
[fastapi] + smmap==5.0.3
[fastapi] + sqlalchemy==2.0.54
[fastapi] + sqlparse==0.6.0
[fastapi] + starlette==1.6.0
[fastapi] + tabulate==0.10.0
[fastapi] + tenacity==9.1.4
[fastapi] + tensorboard==2.19.0
[fastapi] + tensorboard-data-server==0.7.2
[fastapi] + textstat==0.7.8
[fastapi] + threadpoolctl==3.7.0
[fastapi] + tokenizers==0.22.2
[fastapi] + toml==0.10.2
[fastapi] - torch==2.8.0.dev20250319+cu128
[fastapi] + torch==2.8.0
[fastapi] + tqdm==4.70.1
[fastapi] + transformers==5.12.1
[fastapi] + triton==3.4.0
[fastapi] + trl==1.10.0
[fastapi] + truststore==0.10.4
[fastapi] + typer==0.9.0
[fastapi] - typing-extensions==4.12.2
[fastapi] + typing-extensions==4.16.0
[fastapi] + typing-inspection==0.4.4
[fastapi] + tzdata==2026.4
[fastapi] + uvicorn==0.53.0
[fastapi] + wandb==0.19.10
[fastapi] - wcwidth==0.2.13
[fastapi] + wcwidth==0.8.3
[fastapi] + werkzeug==3.1.8
[fastapi] + xxhash==4.0.1
[fastapi] + yarl==1.25.1
[fastapi] + zipp==4.1.0
[fastapi] [0mCollecting tenacity==9.1.2
[fastapi] Downloading tenacity-9.1.2-py3-none-any.whl.metadata (1.2 kB)
[fastapi] Collecting tiktoken==0.9.0
[fastapi] Downloading tiktoken-0.9.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.7 kB)
[fastapi] Requirement already satisfied: regex>=2022.1.18 in /usr/local/lib/python3.11/dist-packages (from tiktoken==0.9.0) (2026.9.10)
[fastapi] Requirement already satisfied: requests>=2.26.0 in /usr/local/lib/python3.11/dist-packages (from tiktoken==0.9.0) (2.32.3)
[fastapi] Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.11/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (3.4.1)
[fastapi] Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.11/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (3.19)
[fastapi] Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.11/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (2.3.0)
[fastapi] Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.11/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (2025.1.31)
[fastapi] Downloading tenacity-9.1.2-py3-none-any.whl (28 kB)
[fastapi] Downloading tiktoken-0.9.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (1.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 121.1 MB/s eta 0:00:00
[fastapi] Installing collected packages: tenacity, tiktoken
[fastapi] Attempting uninstall: tenacity
[fastapi] Found existing installation: tenacity 9.1.4
[fastapi] Uninstalling tenacity-9.1.4:
[fastapi] Successfully uninstalled tenacity-9.1.4
[fastapi] Successfully installed tenacity-9.1.2 tiktoken-0.9.0
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 25.0.1 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0mCollecting flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE
[fastapi] Downloading https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu12torch2.8cxx11abiTRUE-cp311-cp311-linux_x86_64.whl (256.0 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 256.0/256.0 MB 123.1 MB/s eta 0:00:00
[fastapi] Requirement already satisfied: torch in /usr/local/lib/python3.11/dist-packages (from flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (2.8.0)
[fastapi] Requirement already satisfied: einops in /usr/local/lib/python3.11/dist-packages (from flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (0.8.1)
[fastapi] Requirement already satisfied: filelock in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (3.16.1)
[fastapi] Requirement already satisfied: typing-extensions>=4.10.0 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (4.16.0)
[fastapi] Requirement already satisfied: sympy>=1.13.3 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (1.13.3)
[fastapi] Requirement already satisfied: networkx in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (3.4.2)
[fastapi] Requirement already satisfied: jinja2 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (3.1.4)
[fastapi] Requirement already satisfied: fsspec in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (2024.10.0)
[fastapi] Requirement already satisfied: nvidia-cuda-nvrtc-cu12==12.8.93 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (12.8.93)
[fastapi] Requirement already satisfied: nvidia-cuda-runtime-cu12==12.8.90 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (12.8.90)
[fastapi] Requirement already satisfied: nvidia-cuda-cupti-cu12==12.8.90 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (12.8.90)
[fastapi] Requirement already satisfied: nvidia-cudnn-cu12==9.10.2.21 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (9.10.2.21)
[fastapi] Requirement already satisfied: nvidia-cublas-cu12==12.8.4.1 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (12.8.4.1)
[fastapi] Requirement already satisfied: nvidia-cufft-cu12==11.3.3.83 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (11.3.3.83)
[fastapi] Requirement already satisfied: nvidia-curand-cu12==10.3.9.90 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (10.3.9.90)
[fastapi] Requirement already satisfied: nvidia-cusolver-cu12==11.7.3.90 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (11.7.3.90)
[fastapi] Requirement already satisfied: nvidia-cusparse-cu12==12.5.8.93 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (12.5.8.93)
[fastapi] Requirement already satisfied: nvidia-cusparselt-cu12==0.7.1 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (0.7.1)
[fastapi] Requirement already satisfied: nvidia-nccl-cu12==2.27.3 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (2.27.3)
[fastapi] Requirement already satisfied: nvidia-nvtx-cu12==12.8.90 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (12.8.90)
[fastapi] Requirement already satisfied: nvidia-nvjitlink-cu12==12.8.93 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (12.8.93)
[fastapi] Requirement already satisfied: nvidia-cufile-cu12==1.13.1.3 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (1.13.1.3)
[fastapi] Requirement already satisfied: triton==3.4.0 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (3.4.0)
[fastapi] Requirement already satisfied: setuptools>=40.8.0 in /usr/local/lib/python3.11/dist-packages (from triton==3.4.0->torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (75.8.0)
[fastapi] Requirement already satisfied: mpmath<1.4,>=1.1.0 in /usr/local/lib/python3.11/dist-packages (from sympy>=1.13.3->torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (1.3.0)
[fastapi] Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.11/dist-packages (from jinja2->torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (2.1.5)
[fastapi] Installing collected packages: flash-attn
[fastapi] Successfully installed flash-attn-2.8.3
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 25.0.1 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0mCollecting fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0
[fastapi] Cloning https://github.com/rayonlabs/fiber.git (to revision 2.4.0) to /tmp/pip-install-g4088w3l/fiber_38cd0d5516b944bda5e251bb9f2af0dc
[fastapi] [91m  Running command git clone --filter=blob:none --quiet https://github.com/rayonlabs/fiber.git /tmp/pip-install-g4088w3l/fiber_38cd0d5516b944bda5e251bb9f2af0dc
[fastapi] [0m[91m  Running command git checkout -q 57a1aa710774015a0b3f84829654e7037f46a2e1
[fastapi] [0m  Resolved https://github.com/rayonlabs/fiber.git to commit 57a1aa710774015a0b3f84829654e7037f46a2e1
[fastapi] Installing build dependencies: started
[fastapi] Installing build dependencies: finished with status 'done'
[fastapi] Getting requirements to build wheel: started
[fastapi] Getting requirements to build wheel: finished with status 'done'
[fastapi] Preparing metadata (pyproject.toml): started
[fastapi] Preparing metadata (pyproject.toml): finished with status 'done'
[fastapi] Collecting async-substrate-interface<2.0.0,>=1.0.0 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading async_substrate_interface-1.6.4-py3-none-any.whl.metadata (8.5 kB)
[fastapi] Collecting bittensor-commit-reveal==0.1.0 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading bittensor_commit_reveal-0.1.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (8.2 kB)
[fastapi] Collecting colorama<=0.4.6,>0.3.0 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading colorama-0.4.6-py2.py3-none-any.whl.metadata (17 kB)
[fastapi] Collecting eth-typing==5.0.0 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading eth_typing-5.0.0-py3-none-any.whl.metadata (5.1 kB)
[fastapi] Collecting netaddr==1.3.0 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading netaddr-1.3.0-py3-none-any.whl.metadata (5.0 kB)
[fastapi] Collecting pydantic<=2.9.2,>2 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading pydantic-2.9.2-py3-none-any.whl.metadata (149 kB)
[fastapi] Collecting python-dotenv==1.0.1 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading python_dotenv-1.0.1-py3-none-any.whl.metadata (23 kB)
[fastapi] Collecting substrate-interface==1.7.10 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading substrate_interface-1.7.10-py3-none-any.whl.metadata (4.5 kB)
[fastapi] Collecting tenacity==9.0.0 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading tenacity-9.0.0-py3-none-any.whl.metadata (1.2 kB)
[fastapi] Requirement already satisfied: typing-extensions>=4.5.0 in /usr/local/lib/python3.11/dist-packages (from eth-typing==5.0.0->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (4.16.0)
[fastapi] Requirement already satisfied: websocket-client<2,>=0.57.0 in /usr/local/lib/python3.11/dist-packages (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (1.8.0)
[fastapi] Collecting base58<3,>=1.0.3 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading base58-2.1.1-py3-none-any.whl.metadata (3.1 kB)
[fastapi] Requirement already satisfied: certifi>=2019.3.9 in /usr/local/lib/python3.11/dist-packages (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2025.1.31)
[fastapi] Requirement already satisfied: idna<4,>=2.1.0 in /usr/local/lib/python3.11/dist-packages (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (3.19)
[fastapi] Requirement already satisfied: requests<3,>=2.21.0 in /usr/local/lib/python3.11/dist-packages (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2.32.3)
[fastapi] Collecting xxhash<4,>=1.3.0 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading xxhash-3.8.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (15 kB)
[fastapi] Collecting ecdsa<1,>=0.17.0 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading ecdsa-0.19.2-py2.py3-none-any.whl.metadata (29 kB)
[fastapi] Collecting eth-keys<1,>=0.2.1 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading eth_keys-0.8.0-py3-none-any.whl.metadata (12 kB)
[fastapi] Collecting eth-utils<3,>=1.3.0 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading eth_utils-2.3.2-py3-none-any.whl.metadata (5.6 kB)
[fastapi] Requirement already satisfied: pycryptodome<4,>=3.11.0 in /usr/local/lib/python3.11/dist-packages (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (3.23.0)
[fastapi] Collecting PyNaCl<2,>=1.0.1 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading pynacl-1.6.2-cp38-abi3-manylinux_2_34_x86_64.whl.metadata (10.0 kB)
[fastapi] Collecting scalecodec<1.3,>=1.2.10 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading scalecodec-1.2.12-py3-none-any.whl.metadata (17 kB)
[fastapi] Collecting py-sr25519-bindings<1,>=0.2.0 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading py_sr25519_bindings-0.2.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.4 kB)
[fastapi] Collecting py-ed25519-zebra-bindings<2,>=1.0 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading py_ed25519_zebra_bindings-1.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.1 kB)
[fastapi] Collecting py-bip39-bindings<1,>=0.1.9 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading py_bip39_bindings-0.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.5 kB)
[fastapi] Requirement already satisfied: wheel in /usr/local/lib/python3.11/dist-packages (from async-substrate-interface<2.0.0,>=1.0.0->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (0.45.1)
[fastapi] Collecting aiosqlite<1.0.0,>=0.21.0 (from async-substrate-interface<2.0.0,>=1.0.0->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading aiosqlite-0.22.1-py3-none-any.whl.metadata (4.3 kB)
[fastapi] Collecting bt-decode==v0.8.0 (from async-substrate-interface<2.0.0,>=1.0.0->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading bt_decode-0.8.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (10 kB)
[fastapi] Collecting websockets>=14.1 (from async-substrate-interface<2.0.0,>=1.0.0->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading websockets-17.1-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (6.3 kB)
[fastapi] Requirement already satisfied: toml>=0.10.0 in /usr/local/lib/python3.11/dist-packages (from bt-decode==v0.8.0->async-substrate-interface<2.0.0,>=1.0.0->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (0.10.2)
[fastapi] Requirement already satisfied: annotated-types>=0.6.0 in /usr/local/lib/python3.11/dist-packages (from pydantic<=2.9.2,>2->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (0.8.0)
[fastapi] Collecting pydantic-core==2.23.4 (from pydantic<=2.9.2,>2->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading pydantic_core-2.23.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.6 kB)
[fastapi] Requirement already satisfied: six>=1.9.0 in /usr/local/lib/python3.11/dist-packages (from ecdsa<1,>=0.17.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (1.17.0)
[fastapi] Collecting eth-hash>=0.3.1 (from eth-utils<3,>=1.3.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading eth_hash-0.8.0-py3-none-any.whl.metadata (4.1 kB)
[fastapi] Collecting cytoolz>=0.10.1 (from eth-utils<3,>=1.3.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading cytoolz-1.1.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (5.2 kB)
[fastapi] Requirement already satisfied: cffi>=2.0.0 in /usr/local/lib/python3.11/dist-packages (from PyNaCl<2,>=1.0.1->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2.1.1)
[fastapi] Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.11/dist-packages (from requests<3,>=2.21.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (3.4.1)
[fastapi] Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.11/dist-packages (from requests<3,>=2.21.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2.3.0)
[fastapi] Requirement already satisfied: more-itertools in /usr/lib/python3/dist-packages (from scalecodec<1.3,>=1.2.10->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (8.10.0)
[fastapi] Requirement already satisfied: pycparser in /usr/local/lib/python3.11/dist-packages (from cffi>=2.0.0->PyNaCl<2,>=1.0.1->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2.22)
[fastapi] Collecting toolz>=0.8.0 (from cytoolz>=0.10.1->eth-utils<3,>=1.3.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading toolz-1.1.0-py3-none-any.whl.metadata (5.1 kB)
[fastapi] Downloading bittensor_commit_reveal-0.1.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (552 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 552.2/552.2 kB 66.4 MB/s eta 0:00:00
[fastapi] Downloading eth_typing-5.0.0-py3-none-any.whl (20 kB)
[fastapi] Downloading netaddr-1.3.0-py3-none-any.whl (2.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.3/2.3 MB 146.3 MB/s eta 0:00:00
[fastapi] Downloading python_dotenv-1.0.1-py3-none-any.whl (19 kB)
[fastapi] Downloading substrate_interface-1.7.10-py3-none-any.whl (60 kB)
[fastapi] Downloading tenacity-9.0.0-py3-none-any.whl (28 kB)
[fastapi] Downloading async_substrate_interface-1.6.4-py3-none-any.whl (97 kB)
[fastapi] Downloading bt_decode-0.8.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (647 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 647.8/647.8 kB 85.5 MB/s eta 0:00:00
[fastapi] Downloading colorama-0.4.6-py2.py3-none-any.whl (25 kB)
[fastapi] Downloading pydantic-2.9.2-py3-none-any.whl (434 kB)
[fastapi] Downloading pydantic_core-2.23.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 147.7 MB/s eta 0:00:00
[fastapi] Downloading aiosqlite-0.22.1-py3-none-any.whl (17 kB)
[fastapi] Downloading base58-2.1.1-py3-none-any.whl (5.6 kB)
[fastapi] Downloading ecdsa-0.19.2-py2.py3-none-any.whl (150 kB)
[fastapi] Downloading eth_keys-0.8.0-py3-none-any.whl (20 kB)
[fastapi] Downloading eth_utils-2.3.2-py3-none-any.whl (77 kB)
[fastapi] Downloading py_bip39_bindings-0.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (432 kB)
[fastapi] Downloading py_ed25519_zebra_bindings-1.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (323 kB)
[fastapi] Downloading py_sr25519_bindings-0.2.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (372 kB)
[fastapi] Downloading pynacl-1.6.2-cp38-abi3-manylinux_2_34_x86_64.whl (1.4 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.4/1.4 MB 147.6 MB/s eta 0:00:00
[fastapi] Downloading scalecodec-1.2.12-py3-none-any.whl (99 kB)
[fastapi] Downloading websockets-17.1-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (224 kB)
[fastapi] Downloading xxhash-3.8.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (220 kB)
[fastapi] Downloading cytoolz-1.1.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (2.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.8/2.8 MB 119.7 MB/s eta 0:00:00
[fastapi] Downloading eth_hash-0.8.0-py3-none-any.whl (8.0 kB)
[fastapi] Downloading toolz-1.1.0-py3-none-any.whl (58 kB)
[fastapi] Building wheels for collected packages: fiber
[fastapi] Building wheel for fiber (pyproject.toml): started
[fastapi] Building wheel for fiber (pyproject.toml): finished with status 'done'
[fastapi] Created wheel for fiber: filename=fiber-2.4.0-py3-none-any.whl size=51790 sha256=c50f803eff2fbcdf01560cfffdc65a3891a75b0b315d61d842fd3861f51b5d73
[fastapi] Stored in directory: /tmp/pip-ephem-wheel-cache-g_zpa20g/wheels/d1/5e/21/2fa1f403cd187996037f04f6328bf11973ce31440a275f6949
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
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 25.0.1 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0m ---> 971040a12fba
[fastapi] Step 8/13 : RUN pip install --index-url https://download.pytorch.org/whl/cu128     torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0
[fastapi] ---> Running in b130857fda31
[fastapi] Looking in indexes: https://download.pytorch.org/whl/cu128
[fastapi] Requirement already satisfied: torch==2.8.0 in /usr/local/lib/python3.11/dist-packages (2.8.0)
[fastapi] Collecting torchvision==0.23.0
[fastapi] Downloading https://download-r2.pytorch.org/whl/cu128/torchvision-0.23.0%2Bcu128-cp311-cp311-manylinux_2_28_x86_64.whl.metadata (6.1 kB)
[fastapi] Collecting torchaudio==2.8.0
[fastapi] Downloading https://download-r2.pytorch.org/whl/cu128/torchaudio-2.8.0%2Bcu128-cp311-cp311-manylinux_2_28_x86_64.whl.metadata (7.2 kB)
[fastapi] Requirement already satisfied: filelock in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (3.16.1)
[fastapi] Requirement already satisfied: typing-extensions>=4.10.0 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (4.16.0)
[fastapi] Requirement already satisfied: sympy>=1.13.3 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (1.13.3)
[fastapi] Requirement already satisfied: networkx in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (3.4.2)
[fastapi] Requirement already satisfied: jinja2 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (3.1.4)
[fastapi] Requirement already satisfied: fsspec in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (2024.10.0)
[fastapi] Requirement already satisfied: nvidia-cuda-nvrtc-cu12==12.8.93 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (12.8.93)
[fastapi] Requirement already satisfied: nvidia-cuda-runtime-cu12==12.8.90 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (12.8.90)
[fastapi] Requirement already satisfied: nvidia-cuda-cupti-cu12==12.8.90 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (12.8.90)
[fastapi] Requirement already satisfied: nvidia-cudnn-cu12==9.10.2.21 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (9.10.2.21)
[fastapi] Requirement already satisfied: nvidia-cublas-cu12==12.8.4.1 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (12.8.4.1)
[fastapi] Requirement already satisfied: nvidia-cufft-cu12==11.3.3.83 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (11.3.3.83)
[fastapi] Requirement already satisfied: nvidia-curand-cu12==10.3.9.90 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (10.3.9.90)
[fastapi] Requirement already satisfied: nvidia-cusolver-cu12==11.7.3.90 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (11.7.3.90)
[fastapi] Requirement already satisfied: nvidia-cusparse-cu12==12.5.8.93 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (12.5.8.93)
[fastapi] Requirement already satisfied: nvidia-cusparselt-cu12==0.7.1 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (0.7.1)
[fastapi] Requirement already satisfied: nvidia-nccl-cu12==2.27.3 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (2.27.3)
[fastapi] Requirement already satisfied: nvidia-nvtx-cu12==12.8.90 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (12.8.90)
[fastapi] Requirement already satisfied: nvidia-nvjitlink-cu12==12.8.93 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (12.8.93)
[fastapi] Requirement already satisfied: nvidia-cufile-cu12==1.13.1.3 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (1.13.1.3)
[fastapi] Requirement already satisfied: triton==3.4.0 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (3.4.0)
[fastapi] Requirement already satisfied: numpy in /usr/local/lib/python3.11/dist-packages (from torchvision==0.23.0) (2.1.2)
[fastapi] Requirement already satisfied: pillow!=8.3.*,>=5.3.0 in /usr/local/lib/python3.11/dist-packages (from torchvision==0.23.0) (11.0.0)
[fastapi] Requirement already satisfied: setuptools>=40.8.0 in /usr/local/lib/python3.11/dist-packages (from triton==3.4.0->torch==2.8.0) (75.8.0)
[fastapi] Requirement already satisfied: mpmath<1.4,>=1.1.0 in /usr/local/lib/python3.11/dist-packages (from sympy>=1.13.3->torch==2.8.0) (1.3.0)
[fastapi] Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.11/dist-packages (from jinja2->torch==2.8.0) (2.1.5)
[fastapi] Downloading https://download-r2.pytorch.org/whl/cu128/torchvision-0.23.0%2Bcu128-cp311-cp311-manylinux_2_28_x86_64.whl (8.6 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.6/8.6 MB 219.8 MB/s eta 0:00:00
[fastapi] Downloading https://download-r2.pytorch.org/whl/cu128/torchaudio-2.8.0%2Bcu128-cp311-cp311-manylinux_2_28_x86_64.whl (3.9 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.9/3.9 MB 166.6 MB/s eta 0:00:00
[fastapi] Installing collected packages: torchvision, torchaudio
[fastapi] Attempting uninstall: torchvision
[fastapi] Found existing installation: torchvision 0.22.0.dev20250319+cu128
[fastapi] Uninstalling torchvision-0.22.0.dev20250319+cu128:
[fastapi] Successfully uninstalled torchvision-0.22.0.dev20250319+cu128
[fastapi] Attempting uninstall: torchaudio
[fastapi] Found existing installation: torchaudio 2.6.0.dev20250319+cu128
[fastapi] Uninstalling torchaudio-2.6.0.dev20250319+cu128:
[fastapi] Successfully uninstalled torchaudio-2.6.0.dev20250319+cu128
[fastapi] Successfully installed torchaudio-2.8.0+cu128 torchvision-0.23.0+cu128
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 25.0.1 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0m ---> 0a3fc4992f9e
[fastapi] Step 9/13 : RUN python -m venv /workspace/grpo_py &&     /workspace/grpo_py/bin/pip install -U pip uv &&     /workspace/grpo_py/bin/python -m uv pip install         --python /workspace/grpo_py/bin/python         -r /workspace/scripts/grpo_requirements.txt &&     /workspace/grpo_py/bin/python -c "import torch, vllm, trl, transformers; print('grpo venv', torch.__version__, vllm.__version__, trl.__version__, transformers.__version__)"
[fastapi] ---> Running in cc06f7473f30
[fastapi] Requirement already satisfied: pip in /workspace/grpo_py/lib/python3.11/site-packages (24.0)
[fastapi] Collecting pip
[fastapi] Downloading pip-26.2.1-py3-none-any.whl.metadata (4.6 kB)
[fastapi] Collecting uv
[fastapi] Using cached uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] Downloading pip-26.2.1-py3-none-any.whl (1.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 34.1 MB/s eta 0:00:00
[fastapi] Using cached uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.1 MB)
[fastapi] Installing collected packages: uv, pip
[fastapi] Attempting uninstall: pip
[fastapi] Found existing installation: pip 24.0
[fastapi] Uninstalling pip-24.0:
[fastapi] Successfully uninstalled pip-24.0
[fastapi] Successfully installed pip-26.2.1 uv-0.12.15
[fastapi] [91mUsing Python 3.11.11 environment at: /workspace/grpo_py
[fastapi] [0m[91mResolved 258 packages in 317ms
[fastapi] [0m[91mDownloading uvloop (3.6MiB)
[fastapi] [0m[91mDownloading networkx (2.0MiB)
[fastapi] [0m[91mDownloading torchaudio (1.7MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-runtime (2.1MiB)
[fastapi] [0m[91mDownloading sympy (6.0MiB)
[fastapi] [0m[91mDownloading nvidia-cusolver (191.6MiB)
[fastapi] [0m[91mDownloading nvidia-cufft (204.2MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-cupti (10.2MiB)
[fastapi] [0m[91mDownloading fastsafetensors (2.0MiB)
[fastapi] [0m[91mDownloading pynvvideocodec (41.2MiB)
[fastapi] [0m[91mDownloading outlines-core (2.2MiB)
[fastapi] [0m[91mDownloading nvidia-cutlass-dsl-libs-cu13 (83.9MiB)
[fastapi] [0m[91mDownloading torchcodec (9.0MiB)
[fastapi] [0m[91mDownloading pillow (6.6MiB)
[fastapi] [0m[91mDownloading openai-harmony (2.8MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-cccl (3.7MiB)
[fastapi] [0m[91mDownloading z3-solver (27.9MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-nvrtc (86.0MiB)
[fastapi] [0m[91mDownloading nvidia-cutlass-dsl-libs-base (2.7MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-nvcc (45.5MiB)
[fastapi] [0m[91mDownloading xgrammar (1.2MiB)
[fastapi] [0m[91mDownloading nvidia-nccl-cu13 (187.4MiB)
[fastapi] [0m[91mDownloading opencv-python-headless (58.4MiB)
[fastapi] [0m[91mDownloading nvidia-nvjitlink (38.8MiB)
[fastapi] [0m[91mDownloading nvidia-cublas (403.5MiB)
[fastapi] [0m[91mDownloading apache-tvm-ffi (2.5MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-nvdisasm (5.0MiB)
[fastapi] [0m[91mDownloading numpy (16.1MiB)
[fastapi] [0m[91mDownloading nvidia-cusparselt-cu13 (162.0MiB)
[fastapi] [0m[91mDownloading tokenspeed-triton (77.9MiB)
[fastapi] [0m[91mDownloading nvidia-cudnn-cu13 (349.1MiB)
[fastapi] [0m[91mDownloading tilelang (43.3MiB)
[fastapi] [0m[91mDownloading triton (179.5MiB)
[fastapi] [0m[91mDownloading torchvision (7.2MiB)
[fastapi] [0m[91mDownloading nvidia-nvvm (69.2MiB)
[fastapi] [0m[91mDownloading mistral-common (6.2MiB)
[fastapi] [0m[91mDownloading flashinfer-python (13.9MiB)
[fastapi] [0m[91mDownloading cuda-core (6.2MiB)
[fastapi] [0m[91mDownloading numba (3.6MiB)
[fastapi] [0m[91mDownloading nvidia-nvshmem-cu13 (57.6MiB)
[fastapi] [0m[91mDownloading llguidance (2.9MiB)
[fastapi] [0m[91mDownloading nvidia-cutlass-dsl-libs-cu12 (84.3MiB)
[fastapi] [0m[91mDownloading pycountry (7.7MiB)
[fastapi] [0m[91mDownloading nvidia-curand (56.8MiB)
[fastapi] [0m[91mDownloading cuda-bindings (6.8MiB)
[fastapi] [0m[91mDownloading nvidia-cudnn-frontend (5.4MiB)
[fastapi] [0m[91mDownloading torch (506.0MiB)
[fastapi] [0m[91mDownloading nvidia-cusparse (139.2MiB)
[fastapi] [0m[91mDownloading llvmlite (53.7MiB)
[fastapi] [0m[91mDownloading vllm (289.6MiB)
[fastapi] [0m[91m Downloaded xgrammar
[fastapi] [0m[91mDownloading pygments (1.2MiB)
[fastapi] [0m[91m Downloaded torchaudio
[fastapi] [0m[91mDownloading anthropic (1.2MiB)
[fastapi] [0m[91m Downloaded networkx
[fastapi] [0m[91m Downloaded fastsafetensors
[fastapi] [0m[91mDownloading nvidia-cufile (1.2MiB)
[fastapi] [0m[91mDownloading tiktoken (1.2MiB)
[fastapi] [0m[91m Downloaded outlines-core
[fastapi] [0m[91m Downloaded nvidia-cuda-runtime
[fastapi] [0m[91m Downloaded pygments
[fastapi] [0m[91m Downloaded apache-tvm-ffi
[fastapi] [0m[91m Downloaded nvidia-cutlass-dsl-libs-base
[fastapi] [0m[91m Downloaded openai-harmony
[fastapi] [0m[91m Downloaded llguidance
[fastapi] [0m[91m Downloaded anthropic
[fastapi] [0m[91m Downloaded nvidia-cufile
[fastapi] [0m[91m Downloaded tiktoken
[fastapi] [0m[91m Downloaded numba
[fastapi] [0m[91m Downloaded uvloop
[fastapi] [0m[91m Downloaded nvidia-cuda-cccl
[fastapi] [0m[91m Downloaded nvidia-cuda-nvdisasm
[fastapi] [0m[91m Downloaded nvidia-cudnn-frontend
[fastapi] [0m[91m Downloaded sympy
[fastapi] [0m[91m Downloaded cuda-core
[fastapi] [0m[91m Downloaded mistral-common
[fastapi] [0m[91m Downloaded pillow
[fastapi] [0m[91m Downloaded cuda-bindings
[fastapi] [0m[91m Downloaded torchvision
[fastapi] [0m[91m Downloaded pycountry
[fastapi] [0m[91m Downloaded torchcodec
[fastapi] [0m[91m Downloaded nvidia-cuda-cupti
[fastapi] [0m[91m Downloaded flashinfer-python
[fastapi] [0m[91m Downloaded numpy
[fastapi] [0m[91m Downloaded z3-solver
[fastapi] [0m[91m Downloaded nvidia-nvjitlink
[fastapi] [0m[91m Downloaded pynvvideocodec
[fastapi] [0m[91m Downloaded tilelang
[fastapi] [0m[91m Downloaded nvidia-cuda-nvcc
[fastapi] [0m[91m Downloaded llvmlite
[fastapi] [0m[91m Downloaded nvidia-curand
[fastapi] [0m[91m Downloaded nvidia-nvshmem-cu13
[fastapi] [0m[91m Downloaded opencv-python-headless
[fastapi] [0m[91m Downloaded nvidia-nvvm
[fastapi] [0m[91m Downloaded tokenspeed-triton
[fastapi] [0m[91m Downloaded nvidia-cutlass-dsl-libs-cu13
[fastapi] [0m[91m Downloaded nvidia-cutlass-dsl-libs-cu12
[fastapi] [0m[91m Downloaded nvidia-cuda-nvrtc
[fastapi] [0m[91m Downloaded nvidia-cusparse
[fastapi] [0m[91m Downloaded nvidia-cusparselt-cu13
[fastapi] [0m[91m Downloaded triton
[fastapi] [0m[91m Downloaded nvidia-cusolver
[fastapi] [0m[91m Downloaded nvidia-cufft
[fastapi] [0m[91m Downloaded nvidia-nccl-cu13
[fastapi] [0m[91m Downloaded vllm
[fastapi] [0m[91m Downloaded nvidia-cudnn-cu13
[fastapi] [0m[91m Downloaded nvidia-cublas
[fastapi] [0m[91m Downloaded torch
[fastapi] [0m[91mPrepared 151 packages in 7.12s
[fastapi] [0m[91mInstalled 257 packages in 6.14s
[fastapi] [0m[91m + absl-py==2.5.0
[fastapi] + accelerate==1.14.0
[fastapi] + agent-detector==2.0.0
[fastapi] + aiohappyeyeballs==2.7.1
[fastapi] + aiohttp[0m[91m==3.14.3
[fastapi] + aiosignal==1.4.0
[fastapi] + annotated-doc==0.0[0m[91m.5
[fastapi] + [0m[91mannotated-types==0.8.0
[fastapi] + anthropic==[0m[91m1.6.0
[fastapi] + antlr4-python3-runtime==4.9.3
[fastapi] + anyio==4.15.[0m[91m1
[fastapi] + [0m[91mapache-tvm-ffi==0.[0m[91m1.10
[fastapi] [0m[91m+ argon2-cffi==[0m[91m25.1.0
[fastapi] [0m[91m + [0m[91margon2-cffi-bindings==26.1.0
[fastapi] + astor==[0m[91m0.8.[0m[91m1
[fastapi] +[0m[91m attrs==[0m[91m26.1.0
[fastapi] + beautifulsoup4==4.15.0
[fastapi] + bitsandbytes==0.49.2[0m[91m
[fastapi] + blake3==1.0.9
[fastapi] + [0m[91mblinker==1.9.0[0m[91m
[fastapi] + cachetools==[0m[91m7.1[0m[91m.8
[fastapi] [0m[91m+ cbor2[0m[91m==6.1[0m[91m.4[0m[91m
[fastapi] + [0m[91mcertifi==2026[0m[91m.7.22[0m[91m
[fastapi] +[0m[91m cffi==2.1.1[0m[91m
[fastapi] + charset-normalizer[0m[91m==[0m[91m3.5.1[0m[91m
[fastapi] [0m[91m + [0m[91mclick==8.5.0
[fastapi] [0m[91m + cloudpickle==3.1.2[0m[91m
[fastapi] + cmudict==1.[0m[91m1.3
[fastapi] + comm[0m[91m==0.2.3[0m[91m
[fastapi] + compressed-tensors[0m[91m==0.17.0
[fastapi] [0m[91m + cryptography==50[0m[91m.0.1
[fastapi] + cuda-bindings[0m[91m==13.4.[0m[91m1
[fastapi] +[0m[91m cuda-core==[0m[91m1.2.0
[fastapi] + cuda-pathfinder==1.8.1
[fastapi] + [0m[91mcuda-python==13.4[0m[91m.1
[fastapi] [0m[91m +[0m[91m [0m[91mcuda-tile==1[0m[91m.6.[0m[91m0[0m[91m
[fastapi] +[0m[91m cuda-toolkit[0m[91m==[0m[91m13.0.[0m[91m2[0m[91m
[fastapi] +[0m[91m dash[0m[91m==[0m[91m4.4.[0m[91m1[0m[91m
[fastapi] +[0m[91m datasets[0m[91m==5.[0m[91m0.1
[fastapi] + deepspeed==[0m[91m0.19.2[0m[91m
[fastapi] + defusedxml==0[0m[91m.7.1
[fastapi] [0m[91m+ depyf==0.[0m[91m20.0
[fastapi] [0m[91m+ detect-installer[0m[91m==0.2.1[0m[91m
[fastapi] + detoxify==[0m[91m0.5.2[0m[91m
[fastapi] + dill[0m[91m==0.4.[0m[91m1
[fastapi] + [0m[91mdnspython==2.[0m[91m8.[0m[91m0
[fastapi] [0m[91m+ [0m[91mdocker-pycreds==[0m[91m0.4.0
[fastapi] + docstring-parser==0.18.0
[fastapi] + [0m[91meinops==0.8.1[0m[91m
[fastapi] + [0m[91memail-validator==2.3.0
[fastapi] [0m[91m + fastapi[0m[91m==0.136[0m[91m.[0m[91m3
[fastapi] [0m[91m+ [0m[91mfastapi-cli[0m[91m==0.0.32
[fastapi] + [0m[91mfastapi-cloud-cli==0.26.0
[fastapi] [0m[91m+ fastar==0.12.0
[fastapi] [0m[91m+ fastsafetensors==[0m[91m0[0m[91m.4.0[0m[91m
[fastapi] +[0m[91m [0m[91mfilelock[0m[91m==3.32.7
[fastapi] + flashinfer-python==0.6[0m[91m.14
[fastapi] + flask==3.1.3[0m[91m
[fastapi] + frozenlist[0m[91m==1.8.0[0m[91m
[fastapi] + [0m[91mfsspec==[0m[91m2026.6[0m[91m.0
[fastapi] +[0m[91m gdown==[0m[91m6.3.0
[fastapi] +[0m[91m gitdb==4.0.[0m[91m12
[fastapi] [0m[91m + gitpython[0m[91m==3.[0m[91m1.62
[fastapi] + googleapis-common-protos==1.75.3
[fastapi] + [0m[91mgrpcio==1.84.[0m[91m0
[fastapi] + [0m[91mh11==0.16.0
[fastapi] + hf-xet==1.6.0
[fastapi] + hjson[0m[91m==3.1.0
[fastapi] +[0m[91m httpcore==1.0.9
[fastapi] [0m[91m+ httpcore2[0m[91m==2.[0m[91m13.0
[fastapi] + httptools==0.8.0
[fastapi] + httpx==0.28[0m[91m.1
[fastapi] + httpx2==2.13[0m[91m.0
[fastapi] + huggingface-hub==1.31.0
[fastapi] + humming-kernels==0.1[0m[91m.10
[fastapi] + idna==3.19
[fastapi] + ijson[0m[91m==3.5.1
[fastapi] [0m[91m [0m[91m+ importlib-metadata[0m[91m==9.[0m[91m0.1[0m[91m
[fastapi] +[0m[91m [0m[91mimportlib-resources==7.1[0m[91m.[0m[91m0
[fastapi] [0m[91m+ [0m[91minteregular==0.[0m[91m3.3[0m[91m
[fastapi] +[0m[91m itsdangerous[0m[91m==2.2.0
[fastapi] + jaconv==0.5.0[0m[91m
[fastapi] + janus==[0m[91m2.0.[0m[91m0
[fastapi] [0m[91m+ [0m[91mjinja2==3.1.6
[fastapi] + jiter==0.17.[0m[91m0
[fastapi] + jmespath==1.1.[0m[91m0
[fastapi] + joblib==1.6.0[0m[91m
[fastapi] + jsonschema==4.[0m[91m26.0
[fastapi] [0m[91m + jsonschema-specifications[0m[91m==2025.9.1[0m[91m
[fastapi] + [0m[91mlangcheck==0.9[0m[91m.0
[fastapi] +[0m[91m lark==1[0m[91m.2.2
[fastapi] [0m[91m + llguidance[0m[91m==1.7.[0m[91m6
[fastapi] +[0m[91m llvmlite==0.47.0[0m[91m
[fastapi] + lm-format-enforcer[0m[91m==0.11[0m[91m.3
[fastapi] [0m[91m [0m[91m+ loguru==0[0m[91m.7.[0m[91m3
[fastapi] [0m[91m+ markdown-it-py[0m[91m==4.[0m[91m2.0
[fastapi] + markupsafe==3.0.3
[fastapi] [0m[91m+ mcp==2.2.0
[fastapi] + mcp-types==[0m[91m2.2.0
[fastapi] + mdurl[0m[91m==0.1.2[0m[91m
[fastapi] [0m[91m + [0m[91mminio[0m[91m==7[0m[91m.2.[0m[91m20
[fastapi] [0m[91m+[0m[91m mistral-common[0m[91m==[0m[91m1.11[0m[91m.7[0m[91m
[fastapi] [0m[91m+ [0m[91mml-dtypes[0m[91m==0.[0m[91m6.0[0m[91m
[fastapi] [0m[91m+ [0m[91mmodel-hosting-container-standards[0m[91m==0.1.16
[fastapi] + mpmath==1.3.0[0m[91m
[fastapi] + msgpack==1.2.2
[fastapi] +[0m[91m msgspec==0.21.[0m[91m1
[fastapi] +[0m[91m multidict[0m[91m==6.8.0
[fastapi] [0m[91m+ multiprocess==0.[0m[91m70.19[0m[91m
[fastapi] + narwhals==2.26.0
[fastapi] + nest-asyncio==1.6.0
[fastapi] [0m[91m+ networkx==3.6.1
[fastapi] [0m[91m + ninja==[0m[91m1.13.2[0m[91m
[fastapi] + nlpaug[0m[91m==1.1[0m[91m.11
[fastapi] + nltk==3.10.3[0m[91m
[fastapi] + numba==0.65.0
[fastapi] + numpy==2[0m[91m.3.5
[fastapi] +[0m[91m nvidia-cublas[0m[91m==13.[0m[91m1.0.[0m[91m3
[fastapi] [0m[91m+ [0m[91mnvidia-cuda-cccl==13.3[0m[91m.4.2.1
[fastapi] + nvidia-cuda-crt==13.4.59[0m[91m
[fastapi] + nvidia-cuda-cupti[0m[91m==[0m[91m13.0[0m[91m.85
[fastapi] [0m[91m+[0m[91m [0m[91mnvidia-cuda-nvcc==13.4.59
[fastapi] + nvidia-cuda-nvdisasm==13.4.49
[fastapi] + nvidia-cuda-nvrtc==13.0[0m[91m.88
[fastapi] +[0m[91m nvidia-cuda-runtime[0m[91m==13.0[0m[91m.[0m[91m96
[fastapi] [0m[91m+ [0m[91mnvidia-cudnn-cu13==[0m[91m9.19[0m[91m.0[0m[91m.[0m[91m56
[fastapi] +[0m[91m nvidia-cudnn-frontend[0m[91m==1.28.0
[fastapi] + [0m[91mnvidia-cufft==12.0[0m[91m.0.61[0m[91m
[fastapi] +[0m[91m nvidia-cufile[0m[91m==1.15.1.6
[fastapi] + nvidia-curand==10.4[0m[91m.0.35
[fastapi] + nvidia-cusolver==[0m[91m12.0.4[0m[91m.66
[fastapi] + nvidia-cusparse==12.6.3.3[0m[91m
[fastapi] +[0m[91m [0m[91mnvidia-cusparselt-cu13==0.8.0
[fastapi] + nvidia-cutlass-dsl==4.[0m[91m6.0
[fastapi] + nvidia-cutlass-dsl-libs-base==4.6.[0m[91m0
[fastapi] +[0m[91m [0m[91mnvidia-cutlass-dsl-libs-core==4.[0m[91m6.0[0m[91m
[fastapi] [0m[91m+ [0m[91mnvidia-cutlass-dsl-libs-cu12[0m[91m==4.[0m[91m6.0[0m[91m
[fastapi] +[0m[91m [0m[91mnvidia-cutlass-dsl-libs-cu13[0m[91m==4.6.[0m[91m0
[fastapi] [0m[91m +[0m[91m nvidia-ml-py==13.610[0m[91m.43
[fastapi] + [0m[91mnvidia-nccl-cu13==2.28.9
[fastapi] [0m[91m + nvidia-nvjitlink[0m[91m==13.0.[0m[91m88
[fastapi] + nvidia-nvshmem-cu13==3[0m[91m.4.5[0m[91m
[fastapi] [0m[91m+ nvidia-nvtx[0m[91m==[0m[91m13.0.85
[fastapi] + nvidia-nvvm==13.4.59
[fastapi] + nvtx==0.2.15
[fastapi] + omegaconf==2.3.1
[fastapi] + openai==3.14.1
[fastapi] + openai-harmony==0.0.8
[fastapi] + opencv-python-headless==5.0.0.93
[fastapi] + opentelemetry-api==1.44.0
[fastapi] + opentelemetry-exporter-otlp==1.44.0
[fastapi] + opentelemetry-exporter-otlp-proto-common==1.44.0
[fastapi] + opentelemetry-exporter-otlp-proto-grpc==1.44.0
[fastapi] + opentelemetry-exporter-otlp-proto-http==1.44.0
[fastapi] + opentelemetry-proto==1.44.0
[fastapi] + opentelemetry-sdk==1.44.0
[fastapi] + opentelemetry-semantic-conventions==0.65b0
[fastapi] + opentelemetry-semantic-conventions-ai==0.5.1
[fastapi] + outlines-core==0.2.14
[fastapi] + packaging==26.3
[fastapi] + pandas==2.2.3
[fastapi] + partial-json-parser==0.2.1.1.post7
[fastapi] + peft==0.19.1
[fastapi] + pillow==12.3.0
[fastapi] + platformdirs==4.11.9
[fastapi] + plotly==7.1.0
[fastapi] + prometheus-client==0.26.0
[fastapi] + prometheus-fastapi-instrumentator==8.1.0
[fastapi] + propcache==0.5.4
[fastapi] + protobuf==6.33.6
[fastapi] + psutil==7.2.2
[fastapi] + py-cpuinfo==9.0.0
[fastapi] + pyarrow==25.0.1
[fastapi] + pybase64==1.5.0
[fastapi] + pycountry==26.2.16
[fastapi] + pycparser==3.0
[fastapi] + pycryptodome==3.23.0
[fastapi] + pydantic==2.13.5
[fastapi] + pydantic-core==2.46.5
[fastapi] + pydantic-extra-types==2.11.1
[fastapi] + pydantic-settings==2.15.0
[fastapi] + pyelftools==0.33
[fastapi] + pygments==2.21.0
[fastapi] + pyjwt==2.14.0
[fastapi] + pynvvideocodec==2.0.4
[fastapi] + pyphen==0.18.1
[fastapi] + pysocks==1.7.1
[fastapi] + python-dateutil==2.9.0.post0
[fastapi] + python-dotenv==1.2.3
[fastapi] + python-json-logger==4.2.0
[fastapi] + python-multipart==0.0.32
[fastapi] + pytz==2026.3.post1
[fastapi] + pyyaml==6.0.3
[fastapi] + pyzmq==27.2.0
[fastapi] + quack-kernels==0.6.3
[fastapi] + referencing==0.37.0
[fastapi] + regex==2026.9.10
[fastapi] + requests==2.34.2
[fastapi] + restrictedpython==8.0
[fastapi] + retrying==1.4.2
[fastapi] + rich==15.0.0
[fastapi] + rich-toolkit==0.20.5
[fastapi] + rignore==0.8.1
[fastapi] + rouge-score==0.1.2
[fastapi] + rpds-py==2026.6.3
[fastapi] + safetensors==0.8.0
[fastapi] + scikit-learn==1.9.1
[fastapi] + scipy==1.15.2
[fastapi] + sentence-transformers==6.0.1
[fastapi] + sentencepiece==0.2.0
[fastapi] + sentry-sdk==2.69.2
[fastapi] + setproctitle==1.3.7
[fastapi] + shellingham==1.5.4
[fastapi] + six==1.17.0
[fastapi] + smmap==5.0.3
[fastapi] + sniffio==1.3.1
[fastapi] + soupsieve==2.9.2
[fastapi] + sse-starlette==3.4.11
[fastapi] + starlette==1.6.0
[fastapi] + supervisor==4.3.0
[fastapi] + sympy==1.14.0
[fastapi] + tabulate==0.10.0
[fastapi] + tenacity==9.1.4
[fastapi] + textstat==0.7.8
[fastapi] + threadpoolctl==3.7.0
[fastapi] + tiktoken==0.14.0
[fastapi] + tilelang==0.1.9
[fastapi] + tokenizers==0.22.2
[fastapi] + tokenspeed-mla==0.1.8
[fastapi] + tokenspeed-triton==3.8.10.post20260906
[fastapi] + torch==2.11.0
[fastapi] + torch-c-dlpack-ext==0.1.5
[fastapi] + torchaudio==2.11.0
[fastapi] + torchcodec==0.16.0
[fastapi] + torchvision==0.26.0
[fastapi] + tqdm==4.70.1
[fastapi] + transformers==5.12.1
[fastapi] + triton==3.6.0
[fastapi] + trl==1.10.0
[fastapi] + truststore==0.10.4
[fastapi] + typer==0.27.2
[fastapi] + typing-extensions==4.16.0
[fastapi] + typing-inspection==0.4.4
[fastapi] + tzdata==2026.4
[fastapi] + urllib3==2.8.0
[fastapi] + uvicorn==0.53.0
[fastapi] + uvloop==0.22.1
[fastapi] + vllm==0.26.0
[fastapi] + wandb==0.19.10
[fastapi] + watchfiles==1.2.0
[fastapi] + websockets==17.1
[fastapi] + werkzeug==3.1.8
[fastapi] + xgrammar==0.2.7
[fastapi] + xxhash==4.0.1
[fastapi] + yarl==1.25.1
[fastapi] + z3-solver==4.15.4.0
[fastapi] + zipp==4.1.0
[fastapi] [0mgrpo venv 2.11.0+cu130 0.26.0 1.10.0 5.12.1
[fastapi] ---> d8d3db6832f0
[fastapi] Step 10/13 : RUN python -c "import transformers; v=transformers.__version__; assert v == '5.12.1', v" &&     python -c "import torch; assert torch.__version__.startswith('2.8.0'), torch.__version__" &&     python -c "import liger_kernel; from liger_kernel.ops.fused_linear_cross_entropy import LigerFusedLinearCrossEntropyFunction as F; assert hasattr(F.forward, '__call__')" &&     python -c "import flash_attn, trl, peft, bitsandbytes" &&     python -c "from deepspeed import DeepSpeedEngine; print('deps ok (deepspeed importable)')"
[fastapi] ---> Running in f1a349bdc357
[fastapi] [91mFailed to load CPU gemm_4bit_forward from kernels-community: No module named 'kernels'. Please make sure you already `pip install kernels` and the kernels >= 0.11.1
[fastapi] [0m[2026-09-16 16:52:57,501] [WARNING] [real_accelerator.py:199:get_accelerator] Setting accelerator to CPU. If you have GPU or other accelerator, we were unable to detect it.
[fastapi] [91m/usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[fastapi] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[fastapi] warnings.warn(
[fastapi] [0mdeps ok (deepspeed importable)
[fastapi] ---> 7bbda57f77e4
[fastapi] Step 11/13 : COPY scripts /workspace/scripts
[fastapi] ---> 744029ea55b4
[fastapi] Step 12/13 : RUN chmod +x /workspace/scripts/entrypoint.sh
[fastapi] ---> Running in 16792127e106
[fastapi] ---> a47ce1d81509
[fastapi] Step 13/13 : ENTRYPOINT ["./entrypoint.sh"]
[fastapi] ---> Running in e59d15ed7e14
[fastapi] ---> a9dc051f51c7
[fastapi] {'aux': {'ID': 'sha256:a9dc051f51c768821936bd4c0841ad2f7b061c77aa4c38d5aebc0d04ad66e882'}}Successfully built a9dc051f51c7
[fastapi] Successfully tagged standalone-text-trainer:d64c09cd-6e06-4a17-b949-43905edc47e2
[fastapi] Docker image built successfully.
[fastapi] Container.wait() returned: {'StatusCode': 0}
[fastapi] Cleaning up
[fastapi] Cleaned up Docker resources.
[fastapi] Starting upload container hf-upload-bcac1c61a6f2439284dee025955d1270 for task 059bf721-cca5-4d02-9832-a794cf37074b...
[fastapi] Unexpected error during upload_repo_to_hf for task 059bf721-cca5-4d02-9832-a794cf37074b: HF upload failed | exit_code=1 | container=hf-upload-bcac1c61a6f2439284dee025955d1270 | last_error=huggingface_hub.errors.HfHubHTTPError: Invalid user token.
[fastapi] Repository cloned successfully
[fastapi] Running Cache Download Container
[fastapi] Starting downloader container: downloader-059bf721-cca5-4d02-9832-a794cf37074b-1d4bce70
[fastapi] Download completed successfully for task 059bf721-cca5-4d02-9832-a794cf37074b
[fastapi] Building Docker image 'standalone-text-trainer:6385764c-f269-4f23-8815-8ad39778f415' (timeout=1800s)...
[fastapi] Step 1/13 : FROM runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04
[fastapi] ---> d451fe72f137
[fastapi] Step 2/13 : RUN apt-get update && apt-get install -y     vim zip tmux iotop nvtop bmon wget nano zsh htop     && rm -rf /var/lib/apt/lists/*
[fastapi] ---> Running in a0fc6294e26e
[fastapi] Get:1 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  InRelease [1578 B]
[fastapi] Get:2 http://security.ubuntu.com/ubuntu jammy-security InRelease [129 kB]
[fastapi] Get:3 http://archive.ubuntu.com/ubuntu jammy InRelease [270 kB]
[fastapi] Get:4 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  Packages [3011 kB]
[fastapi] Get:5 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [128 kB]
[fastapi] Get:6 http://security.ubuntu.com/ubuntu jammy-security/restricted amd64 Packages [7717 kB]
[fastapi] Get:7 http://archive.ubuntu.com/ubuntu jammy-backports InRelease [127 kB]
[fastapi] Get:8 http://archive.ubuntu.com/ubuntu jammy/multiverse amd64 Packages [266 kB]
[fastapi] Get:9 http://archive.ubuntu.com/ubuntu jammy/main amd64 Packages [1792 kB]
[fastapi] Get:10 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy InRelease [18.1 kB]
[fastapi] Get:11 http://archive.ubuntu.com/ubuntu jammy/universe amd64 Packages [17.5 MB]
[fastapi] Get:12 http://security.ubuntu.com/ubuntu jammy-security/universe amd64 Packages [1317 kB]
[fastapi] Get:13 http://security.ubuntu.com/ubuntu jammy-security/multiverse amd64 Packages [84.6 kB]
[fastapi] Get:14 http://security.ubuntu.com/ubuntu jammy-security/main amd64 Packages [4290 kB]
[fastapi] Get:15 http://archive.ubuntu.com/ubuntu jammy/restricted amd64 Packages [164 kB]
[fastapi] Get:16 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 Packages [4624 kB]
[fastapi] Get:17 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy/main amd64 Packages [44.3 kB]
[fastapi] Get:18 http://archive.ubuntu.com/ubuntu jammy-updates/multiverse amd64 Packages [93.2 kB]
[fastapi] Get:19 http://archive.ubuntu.com/ubuntu jammy-updates/restricted amd64 Packages [8007 kB]
[fastapi] Get:20 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 Packages [1620 kB]
[fastapi] Get:21 http://archive.ubuntu.com/ubuntu jammy-backports/main amd64 Packages [82.8 kB]
[fastapi] Get:22 http://archive.ubuntu.com/ubuntu jammy-backports/universe amd64 Packages [35.6 kB]
[fastapi] Fetched 51.3 MB in 2s (21.8 MB/s)
[fastapi] Reading package lists...
[fastapi] Reading package lists...
[fastapi] Building dependency tree...
[fastapi] Reading state information...
[fastapi] The following additional packages will be installed:
[fastapi] libconfuse-common libconfuse2 libevent-core-2.1-7 libgpm2 libnl-3-200
[fastapi] libnl-genl-3-200 libnl-route-3-200 libpython3.10 libpython3.10-minimal
[fastapi] libpython3.10-stdlib libsodium23 libutempter0 python3.10 python3.10-minimal
[fastapi] unzip vim-common vim-runtime xxd zsh-common
[fastapi] Suggested packages:
[fastapi] lm-sensors lsof strace gpm hunspell python3.10-venv python3.10-doc
[fastapi] binfmt-support ctags vim-doc vim-scripts zsh-doc
[fastapi] The following NEW packages will be installed:
[fastapi] bmon htop iotop libconfuse-common libconfuse2 libevent-core-2.1-7 libgpm2
[fastapi] libnl-3-200 libnl-genl-3-200 libnl-route-3-200 libpython3.10 libsodium23
[fastapi] libutempter0 nano nvtop tmux unzip vim vim-common vim-runtime xxd zip zsh
[fastapi] zsh-common
[fastapi] The following packages will be upgraded:
[fastapi] libpython3.10-minimal libpython3.10-stdlib python3.10 python3.10-minimal
[fastapi] wget
[fastapi] 5 upgraded, 24 newly installed, 0 to remove and 174 not upgraded.
[fastapi] Need to get 23.1 MB of archives.
[fastapi] After this operation, 67.7 MB of additional disk space will be used.
[fastapi] Get:1 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 python3.10 amd64 3.10.12-1~22.04.18 [508 kB]
[fastapi] Get:2 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libpython3.10-stdlib amd64 3.10.12-1~22.04.18 [1850 kB]
[fastapi] Get:3 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 python3.10-minimal amd64 3.10.12-1~22.04.18 [2277 kB]
[fastapi] Get:4 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libpython3.10-minimal amd64 3.10.12-1~22.04.18 [817 kB]
[fastapi] Get:5 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 xxd amd64 2:8.2.3995-1ubuntu2.36 [51.5 kB]
[fastapi] Get:6 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 vim-common all 2:8.2.3995-1ubuntu2.36 [81.5 kB]
[fastapi] Get:7 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 nano amd64 6.2-1ubuntu0.2 [280 kB]
[fastapi] Get:8 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 wget amd64 1.21.2-2ubuntu1.5 [339 kB]
[fastapi] Get:9 http://archive.ubuntu.com/ubuntu jammy/universe amd64 libconfuse-common all 3.3-2 [6004 B]
[fastapi] Get:10 http://archive.ubuntu.com/ubuntu jammy/universe amd64 libconfuse2 amd64 3.3-2 [26.0 kB]
[fastapi] Get:11 http://archive.ubuntu.com/ubuntu jammy/main amd64 libnl-3-200 amd64 3.5.0-0.1 [59.1 kB]
[fastapi] Get:12 http://archive.ubuntu.com/ubuntu jammy/main amd64 libnl-route-3-200 amd64 3.5.0-0.1 [180 kB]
[fastapi] Get:13 http://archive.ubuntu.com/ubuntu jammy/universe amd64 bmon amd64 1:4.0-8 [48.1 kB]
[fastapi] Get:14 http://archive.ubuntu.com/ubuntu jammy/main amd64 libnl-genl-3-200 amd64 3.5.0-0.1 [12.4 kB]
[fastapi] Get:15 http://archive.ubuntu.com/ubuntu jammy/main amd64 htop amd64 3.0.5-7build2 [128 kB]
[fastapi] Get:16 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 iotop amd64 0.6-24-g733f3f8-1.1ubuntu0.1 [23.1 kB]
[fastapi] Get:17 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libevent-core-2.1-7 amd64 2.1.12-stable-1ubuntu0.1 [94.2 kB]
[fastapi] Get:18 http://archive.ubuntu.com/ubuntu jammy/main amd64 libgpm2 amd64 1.20.7-10build1 [15.3 kB]
[fastapi] Get:19 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libpython3.10 amd64 3.10.12-1~22.04.18 [1950 kB]
[fastapi] Get:20 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libsodium23 amd64 1.0.18-1ubuntu0.22.04.1 [164 kB]
[fastapi] Get:21 http://archive.ubuntu.com/ubuntu jammy/main amd64 libutempter0 amd64 1.2.1-2build2 [8848 B]
[fastapi] Get:22 http://archive.ubuntu.com/ubuntu jammy/multiverse amd64 nvtop amd64 1.2.2-1 [43.9 kB]
[fastapi] Get:23 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 tmux amd64 3.2a-4ubuntu0.2 [428 kB]
[fastapi] Get:24 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 unzip amd64 6.0-26ubuntu3.2 [175 kB]
[fastapi] Get:25 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 vim-runtime all 2:8.2.3995-1ubuntu2.36 [6824 kB]
[fastapi] Get:26 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 vim amd64 2:8.2.3995-1ubuntu2.36 [1733 kB]
[fastapi] Get:27 http://archive.ubuntu.com/ubuntu jammy/main amd64 zip amd64 3.0-12build2 [176 kB]
[fastapi] Get:28 http://archive.ubuntu.com/ubuntu jammy/main amd64 zsh-common all 5.8.1-1 [3985 kB]
[fastapi] Get:29 http://archive.ubuntu.com/ubuntu jammy/main amd64 zsh amd64 5.8.1-1 [809 kB]
[fastapi] [91mdebconf: delaying package configuration, since apt-utils is not installed
[fastapi] [0mFetched 23.1 MB in 1s (29.1 MB/s)
[fastapi] (Reading database ... (Reading database ... 5%(Reading database ... 10%(Reading database ... 15%(Reading database ... 20%(Reading database ... 25%(Reading database ... 30%(Reading database ... 35%(Reading database ... 40%(Reading database ... 45%(Reading database ... 50%(Reading database ... 55%(Reading database ... 60%(Reading database ... 65%(Reading database ... 70%(Reading database ... 75%(Reading database ... 80%(Reading database ... 85%(Reading database ... 90%(Reading database ... 95%(Reading database ... 100%(Reading database ... 24286 files and directories currently installed.)
[fastapi] Preparing to unpack .../00-python3.10_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking python3.10 (3.10.12-1~22.04.18) over (3.10.12-1~22.04.9) ...
[fastapi] Preparing to unpack .../01-libpython3.10-stdlib_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking libpython3.10-stdlib:amd64 (3.10.12-1~22.04.18) over (3.10.12-1~22.04.9) ...
[fastapi] Preparing to unpack .../02-python3.10-minimal_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking python3.10-minimal (3.10.12-1~22.04.18) over (3.10.12-1~22.04.9) ...
[fastapi] Preparing to unpack .../03-libpython3.10-minimal_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking libpython3.10-minimal:amd64 (3.10.12-1~22.04.18) over (3.10.12-1~22.04.9) ...
[fastapi] Selecting previously unselected package xxd.
[fastapi] Preparing to unpack .../04-xxd_2%3a8.2.3995-1ubuntu2.36_amd64.deb ...
[fastapi] Unpacking xxd (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Selecting previously unselected package vim-common.
[fastapi] Preparing to unpack .../05-vim-common_2%3a8.2.3995-1ubuntu2.36_all.deb ...
[fastapi] Unpacking vim-common (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Selecting previously unselected package nano.
[fastapi] Preparing to unpack .../06-nano_6.2-1ubuntu0.2_amd64.deb ...
[fastapi] Unpacking nano (6.2-1ubuntu0.2) ...
[fastapi] Preparing to unpack .../07-wget_1.21.2-2ubuntu1.5_amd64.deb ...
[fastapi] Unpacking wget (1.21.2-2ubuntu1.5) over (1.21.2-2ubuntu1.1) ...
[fastapi] Selecting previously unselected package libconfuse-common.
[fastapi] Preparing to unpack .../08-libconfuse-common_3.3-2_all.deb ...
[fastapi] Unpacking libconfuse-common (3.3-2) ...
[fastapi] Selecting previously unselected package libconfuse2:amd64.
[fastapi] Preparing to unpack .../09-libconfuse2_3.3-2_amd64.deb ...
[fastapi] Unpacking libconfuse2:amd64 (3.3-2) ...
[fastapi] Selecting previously unselected package libnl-3-200:amd64.
[fastapi] Preparing to unpack .../10-libnl-3-200_3.5.0-0.1_amd64.deb ...
[fastapi] Unpacking libnl-3-200:amd64 (3.5.0-0.1) ...
[fastapi] Selecting previously unselected package libnl-route-3-200:amd64.
[fastapi] Preparing to unpack .../11-libnl-route-3-200_3.5.0-0.1_amd64.deb ...
[fastapi] Unpacking libnl-route-3-200:amd64 (3.5.0-0.1) ...
[fastapi] Selecting previously unselected package bmon.
[fastapi] Preparing to unpack .../12-bmon_1%3a4.0-8_amd64.deb ...
[fastapi] Unpacking bmon (1:4.0-8) ...
[fastapi] Selecting previously unselected package libnl-genl-3-200:amd64.
[fastapi] Preparing to unpack .../13-libnl-genl-3-200_3.5.0-0.1_amd64.deb ...
[fastapi] Unpacking libnl-genl-3-200:amd64 (3.5.0-0.1) ...
[fastapi] Selecting previously unselected package htop.
[fastapi] Preparing to unpack .../14-htop_3.0.5-7build2_amd64.deb ...
[fastapi] Unpacking htop (3.0.5-7build2) ...
[fastapi] Selecting previously unselected package iotop.
[fastapi] Preparing to unpack .../15-iotop_0.6-24-g733f3f8-1.1ubuntu0.1_amd64.deb ...
[fastapi] Unpacking iotop (0.6-24-g733f3f8-1.1ubuntu0.1) ...
[fastapi] Selecting previously unselected package libevent-core-2.1-7:amd64.
[fastapi] Preparing to unpack .../16-libevent-core-2.1-7_2.1.12-stable-1ubuntu0.1_amd64.deb ...
[fastapi] Unpacking libevent-core-2.1-7:amd64 (2.1.12-stable-1ubuntu0.1) ...
[fastapi] Selecting previously unselected package libgpm2:amd64.
[fastapi] Preparing to unpack .../17-libgpm2_1.20.7-10build1_amd64.deb ...
[fastapi] Unpacking libgpm2:amd64 (1.20.7-10build1) ...
[fastapi] Selecting previously unselected package libpython3.10:amd64.
[fastapi] Preparing to unpack .../18-libpython3.10_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking libpython3.10:amd64 (3.10.12-1~22.04.18) ...
[fastapi] Selecting previously unselected package libsodium23:amd64.
[fastapi] Preparing to unpack .../19-libsodium23_1.0.18-1ubuntu0.22.04.1_amd64.deb ...
[fastapi] Unpacking libsodium23:amd64 (1.0.18-1ubuntu0.22.04.1) ...
[fastapi] Selecting previously unselected package libutempter0:amd64.
[fastapi] Preparing to unpack .../20-libutempter0_1.2.1-2build2_amd64.deb ...
[fastapi] Unpacking libutempter0:amd64 (1.2.1-2build2) ...
[fastapi] Selecting previously unselected package nvtop.
[fastapi] Preparing to unpack .../21-nvtop_1.2.2-1_amd64.deb ...
[fastapi] Unpacking nvtop (1.2.2-1) ...
[fastapi] Selecting previously unselected package tmux.
[fastapi] Preparing to unpack .../22-tmux_3.2a-4ubuntu0.2_amd64.deb ...
[fastapi] Unpacking tmux (3.2a-4ubuntu0.2) ...
[fastapi] Selecting previously unselected package unzip.
[fastapi] Preparing to unpack .../23-unzip_6.0-26ubuntu3.2_amd64.deb ...
[fastapi] Unpacking unzip (6.0-26ubuntu3.2) ...
[fastapi] Selecting previously unselected package vim-runtime.
[fastapi] Preparing to unpack .../24-vim-runtime_2%3a8.2.3995-1ubuntu2.36_all.deb ...
[fastapi] Adding 'diversion of /usr/share/vim/vim82/doc/help.txt to /usr/share/vim/vim82/doc/help.txt.vim-tiny by vim-runtime'
[fastapi] Adding 'diversion of /usr/share/vim/vim82/doc/tags to /usr/share/vim/vim82/doc/tags.vim-tiny by vim-runtime'
[fastapi] Unpacking vim-runtime (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Selecting previously unselected package vim.
[fastapi] Preparing to unpack .../25-vim_2%3a8.2.3995-1ubuntu2.36_amd64.deb ...
[fastapi] Unpacking vim (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Selecting previously unselected package zip.
[fastapi] Preparing to unpack .../26-zip_3.0-12build2_amd64.deb ...
[fastapi] Unpacking zip (3.0-12build2) ...
[fastapi] Selecting previously unselected package zsh-common.
[fastapi] Preparing to unpack .../27-zsh-common_5.8.1-1_all.deb ...
[fastapi] Unpacking zsh-common (5.8.1-1) ...
[fastapi] Selecting previously unselected package zsh.
[fastapi] Preparing to unpack .../28-zsh_5.8.1-1_amd64.deb ...
[fastapi] Unpacking zsh (5.8.1-1) ...
[fastapi] Setting up nvtop (1.2.2-1) ...
[fastapi] Setting up libsodium23:amd64 (1.0.18-1ubuntu0.22.04.1) ...
[fastapi] Setting up libgpm2:amd64 (1.20.7-10build1) ...
[fastapi] Setting up wget (1.21.2-2ubuntu1.5) ...
[fastapi] Setting up zsh-common (5.8.1-1) ...
[fastapi] Setting up unzip (6.0-26ubuntu3.2) ...
[fastapi] Setting up xxd (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Setting up zip (3.0-12build2) ...
[fastapi] Setting up iotop (0.6-24-g733f3f8-1.1ubuntu0.1) ...
[fastapi] update-alternatives: using /usr/sbin/iotop-py to provide /usr/sbin/iotop (iotop) in auto mode
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/man8/iotop.8.gz because associated file /usr/share/man/man8/iotop-py.8.gz (of link group iotop) doesn't exist
[fastapi] Setting up vim-common (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Setting up libevent-core-2.1-7:amd64 (2.1.12-stable-1ubuntu0.1) ...
[fastapi] Setting up libpython3.10-minimal:amd64 (3.10.12-1~22.04.18) ...
[fastapi] Setting up libutempter0:amd64 (1.2.1-2build2) ...
[fastapi] Setting up nano (6.2-1ubuntu0.2) ...
[fastapi] update-alternatives: using /bin/nano to provide /usr/bin/editor (editor) in auto mode
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/man1/editor.1.gz because associated file /usr/share/man/man1/nano.1.gz (of link group editor) doesn't exist
[fastapi] update-alternatives: using /bin/nano to provide /usr/bin/pico (pico) in auto mode
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/man1/pico.1.gz because associated file /usr/share/man/man1/nano.1.gz (of link group pico) doesn't exist
[fastapi] Setting up libconfuse-common (3.3-2) ...
[fastapi] Setting up libnl-3-200:amd64 (3.5.0-0.1) ...
[fastapi] Setting up zsh (5.8.1-1) ...
[fastapi] Setting up vim-runtime (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Setting up libconfuse2:amd64 (3.3-2) ...
[fastapi] Setting up tmux (3.2a-4ubuntu0.2) ...
[fastapi] Setting up python3.10-minimal (3.10.12-1~22.04.18) ...
[fastapi] Setting up libnl-route-3-200:amd64 (3.5.0-0.1) ...
[fastapi] Setting up libpython3.10-stdlib:amd64 (3.10.12-1~22.04.18) ...
[fastapi] Setting up bmon (1:4.0-8) ...
[fastapi] Setting up libnl-genl-3-200:amd64 (3.5.0-0.1) ...
[fastapi] Setting up libpython3.10:amd64 (3.10.12-1~22.04.18) ...
[fastapi] Setting up vim (2:8.2.3995-1ubuntu2.36) ...
[fastapi] update-alternatives: using /usr/bin/vim.basic to provide /usr/bin/vim (vim) in auto mode
[fastapi] update-alternatives: using /usr/bin/vim.basic to provide /usr/bin/vimdiff (vimdiff) in auto mode
[fastapi] update-alternatives: using /usr/bin/vim.basic to provide /usr/bin/rvim (rvim) in auto mode
[fastapi] update-alternatives: using /usr/bin/vim.basic to provide /usr/bin/rview (rview) in auto mode
[fastapi] update-alternatives: using /usr/bin/vim.basic to provide /usr/bin/vi (vi) in auto mode
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/da/man1/vi.1.gz because associated file /usr/share/man/da/man1/vim.1.gz (of link group vi) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/de/man1/vi.1.gz because associated file /usr/share/man/de/man1/vim.1.gz (of link group vi) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/fr/man1/vi.1.gz because associated file /usr/share/man/fr/man1/vim.1.gz (of link group vi) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/it/man1/vi.1.gz because associated file /usr/share/man/it/man1/vim.1.gz (of link group vi) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/ja/man1/vi.1.gz because associated file /usr/share/man/ja/man1/vim.1.gz (of link group vi) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/pl/man1/vi.1.gz because associated file /usr/share/man/pl/man1/vim.1.gz (of link group vi) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/ru/man1/vi.1.gz because associated file /usr/share/man/ru/man1/vim.1.gz (of link group vi) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/man1/vi.1.gz because associated file /usr/share/man/man1/vim.1.gz (of link group vi) doesn't exist
[fastapi] update-alternatives: using /usr/bin/vim.basic to provide /usr/bin/view (view) in auto mode
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/da/man1/view.1.gz because associated file /usr/share/man/da/man1/vim.1.gz (of link group view) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/de/man1/view.1.gz because associated file /usr/share/man/de/man1/vim.1.gz (of link group view) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/fr/man1/view.1.gz because associated file /usr/share/man/fr/man1/vim.1.gz (of link group view) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/it/man1/view.1.gz because associated file /usr/share/man/it/man1/vim.1.gz (of link group view) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/ja/man1/view.1.gz because associated file /usr/share/man/ja/man1/vim.1.gz (of link group view) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/pl/man1/view.1.gz because associated file /usr/share/man/pl/man1/vim.1.gz (of link group view) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/ru/man1/view.1.gz because associated file /usr/share/man/ru/man1/vim.1.gz (of link group view) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/man1/view.1.gz because associated file /usr/share/man/man1/vim.1.gz (of link group view) doesn't exist
[fastapi] update-alternatives: using /usr/bin/vim.basic to provide /usr/bin/ex (ex) in auto mode
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/da/man1/ex.1.gz because associated file /usr/share/man/da/man1/vim.1.gz (of link group ex) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/de/man1/ex.1.gz because associated file /usr/share/man/de/man1/vim.1.gz (of link group ex) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/fr/man1/ex.1.gz because associated file /usr/share/man/fr/man1/vim.1.gz (of link group ex) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/it/man1/ex.1.gz because associated file /usr/share/man/it/man1/vim.1.gz (of link group ex) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/ja/man1/ex.1.gz because associated file /usr/share/man/ja/man1/vim.1.gz (of link group ex) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/pl/man1/ex.1.gz because associated file /usr/share/man/pl/man1/vim.1.gz (of link group ex) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/ru/man1/ex.1.gz because associated file /usr/share/man/ru/man1/vim.1.gz (of link group ex) doesn't exist
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/man1/ex.1.gz because associated file /usr/share/man/man1/vim.1.gz (of link group ex) doesn't exist
[fastapi] Setting up python3.10 (3.10.12-1~22.04.18) ...
[fastapi] Setting up htop (3.0.5-7build2) ...
[fastapi] Processing triggers for mailcap (3.70+nmu1ubuntu1) ...
[fastapi] Processing triggers for libc-bin (2.35-0ubuntu3.9) ...
[fastapi] ---> 519a3a23cfce
[fastapi] Step 3/13 : RUN mkdir -p /workspace /cache /workspace/scripts/datasets /app/checkpoints
[fastapi] ---> Running in 5092d9d21c40
[fastapi] ---> 3e211526adab
[fastapi] Step 4/13 : WORKDIR /workspace/scripts
[fastapi] ---> Running in 567a36cba638
[fastapi] ---> cb391120093b
[fastapi] Step 5/13 : COPY scripts/training_requirements.txt /workspace/scripts/training_requirements.txt
[fastapi] ---> c1e4c35da272
[fastapi] Step 6/13 : COPY scripts/grpo_requirements.txt /workspace/scripts/grpo_requirements.txt
[fastapi] ---> 5b83e0926443
[fastapi] Step 7/13 : RUN pip install uv &&     pip install -U packaging==23.2 setuptools==75.8.0 wheel ninja &&     uv pip install -r /workspace/scripts/training_requirements.txt --system &&     pip install tenacity==9.1.2 tiktoken==0.9.0 &&     pip install https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu12torch2.8cxx11abiTRUE-cp311-cp311-linux_x86_64.whl &&     pip install "fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0"
[fastapi] ---> Running in 8ffbfcb76942
[fastapi] Collecting uv
[fastapi] Downloading uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] Downloading uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.1 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 20.1/20.1 MB 331.6 MB/s eta 0:00:00
[fastapi] Installing collected packages: uv
[fastapi] Successfully installed uv-0.12.15
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 25.0.1 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0mCollecting packaging==23.2
[fastapi] Downloading packaging-23.2-py3-none-any.whl.metadata (3.2 kB)
[fastapi] Collecting setuptools==75.8.0
[fastapi] Downloading setuptools-75.8.0-py3-none-any.whl.metadata (6.7 kB)
[fastapi] Requirement already satisfied: wheel in /usr/local/lib/python3.11/dist-packages (0.45.1)
[fastapi] Collecting wheel
[fastapi] Downloading wheel-0.48.0-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Collecting ninja
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (5.4 kB)
[fastapi] INFO: pip is looking at multiple versions of wheel to determine which version is compatible with other requirements. This could take a while.
[fastapi] Collecting wheel
[fastapi] Downloading wheel-0.47.0-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Downloading wheel-0.46.3-py3-none-any.whl.metadata (2.4 kB)
[fastapi] Downloading wheel-0.46.2-py3-none-any.whl.metadata (2.4 kB)
[fastapi] Downloading packaging-23.2-py3-none-any.whl (53 kB)
[fastapi] Downloading setuptools-75.8.0-py3-none-any.whl (1.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 136.5 MB/s eta 0:00:00
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (183 kB)
[fastapi] Installing collected packages: setuptools, packaging, ninja
[fastapi] Attempting uninstall: setuptools
[fastapi] Found existing installation: setuptools 77.0.1
[fastapi] Uninstalling setuptools-77.0.1:
[fastapi] Successfully uninstalled setuptools-77.0.1
[fastapi] Attempting uninstall: packaging
[fastapi] Found existing installation: packaging 24.2
[fastapi] Uninstalling packaging-24.2:
[fastapi] Successfully uninstalled packaging-24.2
[fastapi] Successfully installed ninja-1.13.2 packaging-23.2 setuptools-75.8.0
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 25.0.1 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0m[91mUsing Python 3.11.11 environment at: /usr
[fastapi] [0m[91mResolved 191 packages in 1.56s
[fastapi] [0m[91m   Building deepspeed==0.19.2
[fastapi] [0m[91mDownloading pycryptodome (2.2MiB)
[fastapi] [0m[91mDownloading pydantic-core (2.0MiB)
[fastapi] [0m[91mDownloading nltk (1.7MiB)
[fastapi] [0m[91mDownloading nvidia-cufile-cu12 (1.1MiB)
[fastapi] [0m[91mDownloading sentencepiece (1.2MiB)
[fastapi] [0m[91mDownloading grpcio (6.9MiB)
[fastapi] [0m[91mDownloading openai (1.9MiB)
[fastapi] [0m[91mDownloading mpi4py (1.3MiB)
[fastapi] [0m[91mDownloading tensorboard-data-server (6.3MiB)
[fastapi] [0m[91mDownloading plotly (9.2MiB)
[fastapi] [0m[91mDownloading tokenizers (3.1MiB)
[fastapi] [0m[91mDownloading scikit-learn (8.9MiB)
[fastapi] [0m[91mDownloading aiohttp (1.7MiB)
[fastapi] [0m[91mDownloading sqlalchemy (3.3MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-cupti-cu12 (9.8MiB)
[fastapi] [0m[91mDownloading fonttools (5.2MiB)
[fastapi] [0m[91mDownloading nvidia-cusolver-cu12 (255.1MiB)
[fastapi] [0m[91mDownloading nvidia-cudnn-cu12 (674.0MiB)
[fastapi] [0m[91mDownloading cryptography (4.5MiB)
[fastapi] [0m[91mDownloading dash (8.5MiB)
[fastapi] [0m[91mDownloading kiwisolver (1.4MiB)
[fastapi] [0m[91mDownloading hf-xet (4.3MiB)
[fastapi] [0m[91mDownloading pandas (12.5MiB)
[fastapi] [0m[91mDownloading tensorboard (5.2MiB)
[fastapi] [0m[91mDownloading mlflow-tracing (1.7MiB)
[fastapi] [0m[91mDownloading mlflow-skinny (3.5MiB)
[fastapi] [0m[91mDownloading matplotlib (9.4MiB)
[fastapi] [0m[91mDownloading mlflow (11.0MiB)
[fastapi] [0m[91mDownloading pyarrow (47.7MiB)
[fastapi] [0m[91mDownloading nvidia-nccl-cu12 (307.4MiB)
[fastapi] [0m[91mDownloading nvidia-curand-cu12 (60.7MiB)
[fastapi] [0m[91mDownloading bitsandbytes (57.8MiB)
[fastapi] [0m[91mDownloading torch (846.9MiB)
[fastapi] [0m[91mDownloading nvidia-cufft-cu12 (184.2MiB)
[fastapi] [0m[91mDownloading scipy (35.9MiB)
[fastapi] [0m[91mDownloading nvidia-nvjitlink-cu12 (37.4MiB)
[fastapi] [0m[91mDownloading nvidia-cusparselt-cu12 (273.9MiB)
[fastapi] [0m[91mDownloading wandb (20.4MiB)
[fastapi] [0m[91mDownloading nvidia-cublas-cu12 (566.8MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-nvrtc-cu12 (84.0MiB)
[fastapi] [0m[91mDownloading transformers (10.6MiB)
[fastapi] [0m[91mDownloading nvidia-cusparse-cu12 (274.9MiB)
[fastapi] [0m[91mDownloading pyphen (2.0MiB)
[fastapi] [0m[91mDownloading triton (148.3MiB)
[fastapi] [0m[91m Downloaded nvidia-cufile-cu12
[fastapi] [0m[91m Downloaded mpi4py
[fastapi] [0m[91m Downloaded sentencepiece
[fastapi] [0m[91m Downloaded kiwisolver
[fastapi] [0m[91m Downloaded nltk
[fastapi] [0m[91m Downloaded aiohttp
[fastapi] [0m[91m Downloaded mlflow-tracing
[fastapi] [0m[91m Downloaded openai
[fastapi] [0m[91m Downloaded pydantic-core
[fastapi] [0m[91m Downloaded pycryptodome
[fastapi] [0m[91m Downloaded pyphen
[fastapi] [0m[91m   Building rouge-score==0.1.2
[fastapi] [0m[91m   Building antlr4-python3-runtime==4.9.3
[fastapi] [0m[91m Downloaded tokenizers
[fastapi] [0m[91m Downloaded sqlalchemy
[fastapi] [0m[91m Downloaded mlflow-skinny
[fastapi] [0m[91m Downloaded hf-xet
[fastapi] [0m[91m Downloaded cryptography
[fastapi] [0m[91m      Built rouge-score==0.1.2
[fastapi] [0m[91m Downloaded tensorboard
[fastapi] [0m[91m Downloaded fonttools
[fastapi] [0m[91m Downloaded tensorboard-data-server
[fastapi] [0m[91m      Built antlr4-python3-runtime==4.9.3
[fastapi] [0m[91m Downloaded grpcio
[fastapi] [0m[91m Downloaded dash
[fastapi] [0m[91m Downloaded scikit-learn
[fastapi] [0m[91m Downloaded plotly
[fastapi] [0m[91m Downloaded matplotlib
[fastapi] [0m[91m Downloaded nvidia-cuda-cupti-cu12
[fastapi] [0m[91m Downloaded transformers
[fastapi] [0m[91m Downloaded mlflow
[fastapi] [0m[91m Downloaded pandas
[fastapi] [0m[91m Downloaded wandb
[fastapi] [0m[91m Downloaded scipy
[fastapi] [0m[91m Downloaded nvidia-nvjitlink-cu12
[fastapi] [0m[91m      Built deepspeed==0.19.2
[fastapi] [0m[91m Downloaded pyarrow
[fastapi] [0m[91m Downloaded bitsandbytes
[fastapi] [0m[91m Downloaded nvidia-curand-cu12
[fastapi] [0m[91m Downloaded nvidia-cuda-nvrtc-cu12
[fastapi] [0m[91m Downloaded triton
[fastapi] [0m[91m Downloaded nvidia-cufft-cu12
[fastapi] [0m[91m Downloaded nvidia-cusolver-cu12
[fastapi] [0m[91m Downloaded nvidia-cusparselt-cu12
[fastapi] [0m[91m Downloaded nvidia-cusparse-cu12
[fastapi] [0m[91m Downloaded nvidia-nccl-cu12
[fastapi] [0m[91m Downloaded nvidia-cublas-cu12
[fastapi] [0m[91m Downloaded nvidia-cudnn-cu12
[fastapi] [0m[91m Downloaded torch
[fastapi] [0m[91mPrepared 158 packages in 8.86s
[fastapi] [0m[91mUninstalled 22 packages in 1.10s
[fastapi] [0m[91mInstalled 158 packages in 292ms
[fastapi] [0m[91m + absl-py==2.5.0
[fastapi] + accelerate==1.14.0
[fastapi] + aiohappyeyeballs==2.7.1
[fastapi] + aiohttp==3.14.3
[fastapi] + aiosignal==1.4.0
[fastapi] + alembic==1.20.0
[fastapi] [0m[91m + annotated-doc==0.0.5
[fastapi] + annotated-types==0.8.0
[fastapi] + antlr4-python3-runtime==4.9.3[0m[91m
[fastapi] -[0m[91m anyio==4[0m[91m.9.0
[fastapi] + anyio==4.15.1
[fastapi] + astor==0.8.1
[fastapi] +[0m[91m bitsandbytes==0.49.2
[fastapi] + blinker==1.9.0
[fastapi] [0m[91m+[0m[91m cachetools==7.2[0m[91m.0
[fastapi] [0m[91m-[0m[91m cffi==1.17[0m[91m.1[0m[91m
[fastapi] +[0m[91m cffi[0m[91m==2.[0m[91m1.1
[fastapi] [0m[91m + click==8.5.[0m[91m0
[fastapi] +[0m[91m cloudpickle[0m[91m==3.[0m[91m1.2
[fastapi] [0m[91m [0m[91m+ cmudict[0m[91m==1[0m[91m.1.3[0m[91m
[fastapi] + contourpy==1.3.3
[fastapi] + cryptography[0m[91m==50.0.1
[fastapi] + cycler==0.12.1
[fastapi] + dash==[0m[91m4.4.1
[fastapi] + databricks-sdk[0m[91m==0.139[0m[91m.0
[fastapi] + datasets==5.0.1
[fastapi] [0m[91m + deepspeed==0.19.2
[fastapi] + detoxify==[0m[91m0.5.2
[fastapi] + dill==0.4.1
[fastapi] + docker==7.2[0m[91m.0
[fastapi] + docker-pycreds[0m[91m==0.4.0
[fastapi] +[0m[91m einops==0[0m[91m.8.1
[fastapi] [0m[91m + fastapi==0.141.1
[fastapi] +[0m[91m flask==3.1[0m[91m.3
[fastapi] + [0m[91mflask-cors==6.[0m[91m0.5[0m[91m
[fastapi] +[0m[91m fonttools[0m[91m==[0m[91m4.65.[0m[91m0
[fastapi] [0m[91m+ [0m[91mfrozenlist==[0m[91m1.[0m[91m8.0
[fastapi] [0m[91m [0m[91m+[0m[91m gdown==6.[0m[91m3.0[0m[91m
[fastapi] [0m[91m [0m[91m+ gitdb[0m[91m==[0m[91m4.0.12[0m[91m
[fastapi] [0m[91m+ gitpython==3.1.62
[fastapi] + google-auth[0m[91m==2.58.0
[fastapi] + graphene[0m[91m==3.4[0m[91m.3
[fastapi] [0m[91m+ [0m[91mgraphql-core[0m[91m==3.2.[0m[91m12
[fastapi] + graphql-relay==3.2.0
[fastapi] + greenlet==[0m[91m3.5.6
[fastapi] + grpcio==1[0m[91m.84.0
[fastapi] +[0m[91m gunicorn==26[0m[91m.2.0[0m[91m
[fastapi] - h11==0.14.0
[fastapi] +[0m[91m h11==0.16.0
[fastapi] [0m[91m+ hf-xet==1[0m[91m.6.0
[fastapi] + hjson==3.1.0[0m[91m
[fastapi] [0m[91m- httpcore[0m[91m==1.0.7[0m[91m
[fastapi] + httpcore==1.0.9
[fastapi] + [0m[91mhttpcore2==2.13.0
[fastapi] [0m[91m [0m[91m+ httpx2==2.13.0
[fastapi] [0m[91m + [0m[91mhuey[0m[91m==3.4.[0m[91m0[0m[91m
[fastapi] +[0m[91m huggingface-hub==[0m[91m1.[0m[91m31.[0m[91m0
[fastapi] - [0m[91midna==3.10
[fastapi] + [0m[91midna==3.19
[fastapi] + importlib-metadata==[0m[91m9.0.1
[fastapi] +[0m[91m importlib-resources==7.1.[0m[91m0
[fastapi] +[0m[91m itsdangerous==[0m[91m2.2.0
[fastapi] [0m[91m + jaconv==[0m[91m0.5.[0m[91m0
[fastapi] +[0m[91m janus==2.[0m[91m0.0
[fastapi] + jiter[0m[91m==0.17.0
[fastapi] [0m[91m+ joblib==1.[0m[91m6.0
[fastapi] +[0m[91m kiwisolver==1[0m[91m.5.1
[fastapi] +[0m[91m langcheck==0.[0m[91m9.0
[fastapi] [0m[91m+ liger-kernel==0[0m[91m.8.2
[fastapi] [0m[91m+ mako[0m[91m==1.4[0m[91m.1
[fastapi] + [0m[91mmarkdown==3.10.[0m[91m3
[fastapi] + [0m[91mmatplotlib==[0m[91m3[0m[91m.11.2
[fastapi] [0m[91m [0m[91m+ minio==[0m[91m7.2[0m[91m.20
[fastapi] [0m[91m [0m[91m+ mlflow==[0m[91m3.[0m[91m16.0[0m[91m
[fastapi] [0m[91m+[0m[91m mlflow-skinny[0m[91m==3.16.[0m[91m0[0m[91m
[fastapi] +[0m[91m mlflow-tracing[0m[91m==3[0m[91m.16.0
[fastapi] +[0m[91m mpi4py[0m[91m==4.1[0m[91m.2
[fastapi] + msgpack==1[0m[91m.2.2
[fastapi] +[0m[91m multidict[0m[91m==6.8.0[0m[91m
[fastapi] [0m[91m [0m[91m+ multiprocess==0[0m[91m.70.[0m[91m19
[fastapi] [0m[91m+ [0m[91mnarwhals[0m[91m==2.26.[0m[91m0
[fastapi] + [0m[91mnlpaug[0m[91m==1.1.11[0m[91m
[fastapi] + [0m[91mnltk==[0m[91m3.10.3[0m[91m
[fastapi] - nvidia-cublas-cu12[0m[91m==12.8.3.14
[fastapi] + nvidia-cublas-cu12==[0m[91m12.8.4.1
[fastapi] [0m[91m- [0m[91mnvidia-cuda-cupti-cu12==12[0m[91m.8[0m[91m.57
[fastapi] [0m[91m +[0m[91m nvidia-cuda-cupti-cu12==12[0m[91m.8.90
[fastapi] [0m[91m- nvidia-cuda-nvrtc-cu12==12.8.61
[fastapi] +[0m[91m nvidia-cuda-nvrtc-cu12==12.8.93[0m[91m
[fastapi] - nvidia-cuda-runtime-cu12==12.[0m[91m8.57
[fastapi] [0m[91m+[0m[91m nvidia-cuda-runtime-cu12[0m[91m==12.[0m[91m8.[0m[91m90
[fastapi] [0m[91m- [0m[91mnvidia-cudnn-cu12==9.8.0[0m[91m.87
[fastapi] [0m[91m +[0m[91m nvidia-cudnn-cu12==9[0m[91m.10.2.21
[fastapi] - [0m[91mnvidia-cufft-cu12==11.3.[0m[91m3.41
[fastapi] + nvidia-cufft-cu12[0m[91m==11.3.3.83
[fastapi] - [0m[91mnvidia-cufile-cu12==1.13.0.11
[fastapi] [0m[91m +[0m[91m nvidia-cufile-cu12==1.13.1.3[0m[91m
[fastapi] - nvidia-curand-cu12[0m[91m==10.3.9.55
[fastapi] + nvidia-curand-cu12==10.3[0m[91m.9.90
[fastapi] - nvidia-cusolver-cu12==11.7.2.55
[fastapi] [0m[91m+ nvidia-cusolver-cu12==[0m[91m11.7.3[0m[91m.90
[fastapi] - nvidia-cusparse-cu12==12[0m[91m.5.7.[0m[91m53[0m[91m
[fastapi] + nvidia-cusparse-cu12==[0m[91m12.5.[0m[91m8.93
[fastapi] [0m[91m- nvidia-cusparselt-cu12[0m[91m==0.6.3
[fastapi] [0m[91m+ nvidia-cusparselt-cu12==0.7.1
[fastapi] [0m[91m- nvidia-nccl-cu12==[0m[91m2.25.1[0m[91m
[fastapi] + nvidia-nccl-cu12==[0m[91m2.27.3
[fastapi] - nvidia-nvjitlink-cu12==12.[0m[91m8.61
[fastapi] +[0m[91m nvidia-nvjitlink-cu12==12.8[0m[91m.93
[fastapi] [0m[91m- nvidia-nvtx-cu12==12.8.[0m[91m55
[fastapi] + [0m[91mnvidia-nvtx-cu12==12[0m[91m.8.[0m[91m90
[fastapi] + omegaconf==2[0m[91m.3.1[0m[91m
[fastapi] + openai==3.14.1
[fastapi] + opentelemetry-api[0m[91m==1.44.0
[fastapi] + opentelemetry-proto[0m[91m==1.44.[0m[91m0
[fastapi] +[0m[91m opentelemetry-sdk==1.44.0[0m[91m
[fastapi] + opentelemetry-semantic-conventions[0m[91m==0[0m[91m.65b[0m[91m0
[fastapi] [0m[91m+[0m[91m pandas[0m[91m==2.[0m[91m2.3[0m[91m
[fastapi] [0m[91m + [0m[91mpeft==[0m[91m0.[0m[91m19.1[0m[91m
[fastapi] [0m[91m+ plotly[0m[91m==7.1.0
[fastapi] [0m[91m + prettytable==3.18.[0m[91m0
[fastapi] [0m[91m+ [0m[91mpropcache[0m[91m==0.5.[0m[91m4[0m[91m
[fastapi] [0m[91m+ [0m[91mprotobuf[0m[91m==[0m[91m6.33.6[0m[91m
[fastapi] [0m[91m + [0m[91mpy-cpuinfo==9.0.[0m[91m0
[fastapi] + [0m[91mpyarrow==25.[0m[91m0.1
[fastapi] + pyasn1[0m[91m==0.6[0m[91m.4
[fastapi] [0m[91m [0m[91m+ [0m[91mpyasn1-modules[0m[91m==0[0m[91m.4.2[0m[91m
[fastapi] [0m[91m+ [0m[91mpycryptodome[0m[91m==3.23.0
[fastapi] + [0m[91mpydantic==2.13.5[0m[91m
[fastapi] + pydantic-core==[0m[91m2.46.[0m[91m5[0m[91m
[fastapi] + [0m[91mpyparsing==[0m[91m3.[0m[91m3[0m[91m.2
[fastapi] + pyphen==0.18.1
[fastapi] +[0m[91m pysocks==1.7.1[0m[91m
[fastapi] + python-dotenv==1.2.3
[fastapi] +[0m[91m pytz==2026[0m[91m.3.post[0m[91m1
[fastapi] [0m[91m + regex==2026.9.10
[fastapi] + restrictedpython==8.0
[fastapi] + retrying==1.4.2
[fastapi] + rouge-score==0.1.2
[fastapi] + safetensors==0.8.0
[fastapi] + scikit-learn==1.9.1
[fastapi] + scipy==1.15.2
[fastapi] + sentence-transformers==6.0.1
[fastapi] + sentencepiece==0.2.0
[fastapi] + sentry-sdk==2.69.2
[fastapi] + setproctitle==1.3.7
[fastapi] + six==1.17.0
[fastapi] + skops==0.15.0
[fastapi] + smmap==5.0.3
[fastapi] + sqlalchemy==2.0.54
[fastapi] + sqlparse==0.6.0
[fastapi] + starlette==1.6.0
[fastapi] + tabulate==0.10.0
[fastapi] + tenacity==9.1.4
[fastapi] + tensorboard==2.19.0
[fastapi] + tensorboard-data-server==0.7.2
[fastapi] + textstat==0.7.8
[fastapi] + threadpoolctl==3.7.0
[fastapi] + tokenizers==0.22.2
[fastapi] + toml==0.10.2
[fastapi] - torch==2.8.0.dev20250319+cu128
[fastapi] + torch==2.8.0
[fastapi] + tqdm==4.70.1
[fastapi] + transformers==5.12.1
[fastapi] + triton==3.4.0
[fastapi] + trl==1.10.0
[fastapi] + truststore==0.10.4
[fastapi] + typer==0.9.0
[fastapi] - typing-extensions==4.12.2
[fastapi] + typing-extensions==4.16.0
[fastapi] + typing-inspection==0.4.4
[fastapi] + tzdata==2026.4
[fastapi] + uvicorn==0.53.0
[fastapi] + wandb==0.19.10
[fastapi] - wcwidth==0.2.13
[fastapi] + wcwidth==0.8.3
[fastapi] + werkzeug==3.1.8
[fastapi] + xxhash==4.0.1
[fastapi] + yarl==1.25.1
[fastapi] + zipp==4.1.0
[fastapi] [0mCollecting tenacity==9.1.2
[fastapi] Downloading tenacity-9.1.2-py3-none-any.whl.metadata (1.2 kB)
[fastapi] Collecting tiktoken==0.9.0
[fastapi] Downloading tiktoken-0.9.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.7 kB)
[fastapi] Requirement already satisfied: regex>=2022.1.18 in /usr/local/lib/python3.11/dist-packages (from tiktoken==0.9.0) (2026.9.10)
[fastapi] Requirement already satisfied: requests>=2.26.0 in /usr/local/lib/python3.11/dist-packages (from tiktoken==0.9.0) (2.32.3)
[fastapi] Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.11/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (3.4.1)
[fastapi] Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.11/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (3.19)
[fastapi] Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.11/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (2.3.0)
[fastapi] Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.11/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (2025.1.31)
[fastapi] Downloading tenacity-9.1.2-py3-none-any.whl (28 kB)
[fastapi] Downloading tiktoken-0.9.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (1.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 126.2 MB/s eta 0:00:00
[fastapi] Installing collected packages: tenacity, tiktoken
[fastapi] Attempting uninstall: tenacity
[fastapi] Found existing installation: tenacity 9.1.4
[fastapi] Uninstalling tenacity-9.1.4:
[fastapi] Successfully uninstalled tenacity-9.1.4
[fastapi] Successfully installed tenacity-9.1.2 tiktoken-0.9.0
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 25.0.1 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0mCollecting flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE
[fastapi] Downloading https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu12torch2.8cxx11abiTRUE-cp311-cp311-linux_x86_64.whl (256.0 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 256.0/256.0 MB 179.1 MB/s eta 0:00:00
[fastapi] Requirement already satisfied: torch in /usr/local/lib/python3.11/dist-packages (from flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (2.8.0)
[fastapi] Requirement already satisfied: einops in /usr/local/lib/python3.11/dist-packages (from flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (0.8.1)
[fastapi] Requirement already satisfied: filelock in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (3.16.1)
[fastapi] Requirement already satisfied: typing-extensions>=4.10.0 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (4.16.0)
[fastapi] Requirement already satisfied: sympy>=1.13.3 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (1.13.3)
[fastapi] Requirement already satisfied: networkx in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (3.4.2)
[fastapi] Requirement already satisfied: jinja2 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (3.1.4)
[fastapi] Requirement already satisfied: fsspec in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (2024.10.0)
[fastapi] Requirement already satisfied: nvidia-cuda-nvrtc-cu12==12.8.93 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (12.8.93)
[fastapi] Requirement already satisfied: nvidia-cuda-runtime-cu12==12.8.90 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (12.8.90)
[fastapi] Requirement already satisfied: nvidia-cuda-cupti-cu12==12.8.90 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (12.8.90)
[fastapi] Requirement already satisfied: nvidia-cudnn-cu12==9.10.2.21 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (9.10.2.21)
[fastapi] Requirement already satisfied: nvidia-cublas-cu12==12.8.4.1 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (12.8.4.1)
[fastapi] Requirement already satisfied: nvidia-cufft-cu12==11.3.3.83 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (11.3.3.83)
[fastapi] Requirement already satisfied: nvidia-curand-cu12==10.3.9.90 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (10.3.9.90)
[fastapi] Requirement already satisfied: nvidia-cusolver-cu12==11.7.3.90 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (11.7.3.90)
[fastapi] Requirement already satisfied: nvidia-cusparse-cu12==12.5.8.93 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (12.5.8.93)
[fastapi] Requirement already satisfied: nvidia-cusparselt-cu12==0.7.1 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (0.7.1)
[fastapi] Requirement already satisfied: nvidia-nccl-cu12==2.27.3 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (2.27.3)
[fastapi] Requirement already satisfied: nvidia-nvtx-cu12==12.8.90 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (12.8.90)
[fastapi] Requirement already satisfied: nvidia-nvjitlink-cu12==12.8.93 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (12.8.93)
[fastapi] Requirement already satisfied: nvidia-cufile-cu12==1.13.1.3 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (1.13.1.3)
[fastapi] Requirement already satisfied: triton==3.4.0 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (3.4.0)
[fastapi] Requirement already satisfied: setuptools>=40.8.0 in /usr/local/lib/python3.11/dist-packages (from triton==3.4.0->torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (75.8.0)
[fastapi] Requirement already satisfied: mpmath<1.4,>=1.1.0 in /usr/local/lib/python3.11/dist-packages (from sympy>=1.13.3->torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (1.3.0)
[fastapi] Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.11/dist-packages (from jinja2->torch->flash-attn==2.8.3+cu12torch2.8cxx11abiTRUE) (2.1.5)
[fastapi] Installing collected packages: flash-attn
[fastapi] Successfully installed flash-attn-2.8.3
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 25.0.1 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0mCollecting fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0
[fastapi] Cloning https://github.com/rayonlabs/fiber.git (to revision 2.4.0) to /tmp/pip-install-e_5g390j/fiber_4487cb52a4e34ca2b04b7fea05694e65
[fastapi] [91m  Running command git clone --filter=blob:none --quiet https://github.com/rayonlabs/fiber.git /tmp/pip-install-e_5g390j/fiber_4487cb52a4e34ca2b04b7fea05694e65
[fastapi] [0m[91m  Running command git checkout -q 57a1aa710774015a0b3f84829654e7037f46a2e1
[fastapi] [0m  Resolved https://github.com/rayonlabs/fiber.git to commit 57a1aa710774015a0b3f84829654e7037f46a2e1
[fastapi] Installing build dependencies: started
[fastapi] Installing build dependencies: finished with status 'done'
[fastapi] Getting requirements to build wheel: started
[fastapi] Getting requirements to build wheel: finished with status 'done'
[fastapi] Preparing metadata (pyproject.toml): started
[fastapi] Preparing metadata (pyproject.toml): finished with status 'done'
[fastapi] Collecting async-substrate-interface<2.0.0,>=1.0.0 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading async_substrate_interface-1.6.4-py3-none-any.whl.metadata (8.5 kB)
[fastapi] Collecting bittensor-commit-reveal==0.1.0 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading bittensor_commit_reveal-0.1.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (8.2 kB)
[fastapi] Collecting colorama<=0.4.6,>0.3.0 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading colorama-0.4.6-py2.py3-none-any.whl.metadata (17 kB)
[fastapi] Collecting eth-typing==5.0.0 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading eth_typing-5.0.0-py3-none-any.whl.metadata (5.1 kB)
[fastapi] Collecting netaddr==1.3.0 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading netaddr-1.3.0-py3-none-any.whl.metadata (5.0 kB)
[fastapi] Collecting pydantic<=2.9.2,>2 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading pydantic-2.9.2-py3-none-any.whl.metadata (149 kB)
[fastapi] Collecting python-dotenv==1.0.1 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading python_dotenv-1.0.1-py3-none-any.whl.metadata (23 kB)
[fastapi] Collecting substrate-interface==1.7.10 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading substrate_interface-1.7.10-py3-none-any.whl.metadata (4.5 kB)
[fastapi] Collecting tenacity==9.0.0 (from fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading tenacity-9.0.0-py3-none-any.whl.metadata (1.2 kB)
[fastapi] Requirement already satisfied: typing-extensions>=4.5.0 in /usr/local/lib/python3.11/dist-packages (from eth-typing==5.0.0->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (4.16.0)
[fastapi] Requirement already satisfied: websocket-client<2,>=0.57.0 in /usr/local/lib/python3.11/dist-packages (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (1.8.0)
[fastapi] Collecting base58<3,>=1.0.3 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading base58-2.1.1-py3-none-any.whl.metadata (3.1 kB)
[fastapi] Requirement already satisfied: certifi>=2019.3.9 in /usr/local/lib/python3.11/dist-packages (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2025.1.31)
[fastapi] Requirement already satisfied: idna<4,>=2.1.0 in /usr/local/lib/python3.11/dist-packages (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (3.19)
[fastapi] Requirement already satisfied: requests<3,>=2.21.0 in /usr/local/lib/python3.11/dist-packages (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2.32.3)
[fastapi] Collecting xxhash<4,>=1.3.0 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading xxhash-3.8.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (15 kB)
[fastapi] Collecting ecdsa<1,>=0.17.0 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading ecdsa-0.19.2-py2.py3-none-any.whl.metadata (29 kB)
[fastapi] Collecting eth-keys<1,>=0.2.1 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading eth_keys-0.8.0-py3-none-any.whl.metadata (12 kB)
[fastapi] Collecting eth-utils<3,>=1.3.0 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading eth_utils-2.3.2-py3-none-any.whl.metadata (5.6 kB)
[fastapi] Requirement already satisfied: pycryptodome<4,>=3.11.0 in /usr/local/lib/python3.11/dist-packages (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (3.23.0)
[fastapi] Collecting PyNaCl<2,>=1.0.1 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading pynacl-1.6.2-cp38-abi3-manylinux_2_34_x86_64.whl.metadata (10.0 kB)
[fastapi] Collecting scalecodec<1.3,>=1.2.10 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading scalecodec-1.2.12-py3-none-any.whl.metadata (17 kB)
[fastapi] Collecting py-sr25519-bindings<1,>=0.2.0 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading py_sr25519_bindings-0.2.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.4 kB)
[fastapi] Collecting py-ed25519-zebra-bindings<2,>=1.0 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading py_ed25519_zebra_bindings-1.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.1 kB)
[fastapi] Collecting py-bip39-bindings<1,>=0.1.9 (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading py_bip39_bindings-0.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.5 kB)
[fastapi] Requirement already satisfied: wheel in /usr/local/lib/python3.11/dist-packages (from async-substrate-interface<2.0.0,>=1.0.0->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (0.45.1)
[fastapi] Collecting aiosqlite<1.0.0,>=0.21.0 (from async-substrate-interface<2.0.0,>=1.0.0->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading aiosqlite-0.22.1-py3-none-any.whl.metadata (4.3 kB)
[fastapi] Collecting bt-decode==v0.8.0 (from async-substrate-interface<2.0.0,>=1.0.0->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading bt_decode-0.8.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (10 kB)
[fastapi] Collecting websockets>=14.1 (from async-substrate-interface<2.0.0,>=1.0.0->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading websockets-17.1-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (6.3 kB)
[fastapi] Requirement already satisfied: toml>=0.10.0 in /usr/local/lib/python3.11/dist-packages (from bt-decode==v0.8.0->async-substrate-interface<2.0.0,>=1.0.0->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (0.10.2)
[fastapi] Requirement already satisfied: annotated-types>=0.6.0 in /usr/local/lib/python3.11/dist-packages (from pydantic<=2.9.2,>2->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (0.8.0)
[fastapi] Collecting pydantic-core==2.23.4 (from pydantic<=2.9.2,>2->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading pydantic_core-2.23.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.6 kB)
[fastapi] Requirement already satisfied: six>=1.9.0 in /usr/local/lib/python3.11/dist-packages (from ecdsa<1,>=0.17.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (1.17.0)
[fastapi] Collecting eth-hash>=0.3.1 (from eth-utils<3,>=1.3.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading eth_hash-0.8.0-py3-none-any.whl.metadata (4.1 kB)
[fastapi] Collecting cytoolz>=0.10.1 (from eth-utils<3,>=1.3.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading cytoolz-1.1.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (5.2 kB)
[fastapi] Requirement already satisfied: cffi>=2.0.0 in /usr/local/lib/python3.11/dist-packages (from PyNaCl<2,>=1.0.1->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2.1.1)
[fastapi] Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.11/dist-packages (from requests<3,>=2.21.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (3.4.1)
[fastapi] Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.11/dist-packages (from requests<3,>=2.21.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2.3.0)
[fastapi] Requirement already satisfied: more-itertools in /usr/lib/python3/dist-packages (from scalecodec<1.3,>=1.2.10->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (8.10.0)
[fastapi] Requirement already satisfied: pycparser in /usr/local/lib/python3.11/dist-packages (from cffi>=2.0.0->PyNaCl<2,>=1.0.1->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2.22)
[fastapi] Collecting toolz>=0.8.0 (from cytoolz>=0.10.1->eth-utils<3,>=1.3.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading toolz-1.1.0-py3-none-any.whl.metadata (5.1 kB)
[fastapi] Downloading bittensor_commit_reveal-0.1.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (552 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 552.2/552.2 kB 63.8 MB/s eta 0:00:00
[fastapi] Downloading eth_typing-5.0.0-py3-none-any.whl (20 kB)
[fastapi] Downloading netaddr-1.3.0-py3-none-any.whl (2.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.3/2.3 MB 146.0 MB/s eta 0:00:00
[fastapi] Downloading python_dotenv-1.0.1-py3-none-any.whl (19 kB)
[fastapi] Downloading substrate_interface-1.7.10-py3-none-any.whl (60 kB)
[fastapi] Downloading tenacity-9.0.0-py3-none-any.whl (28 kB)
[fastapi] Downloading async_substrate_interface-1.6.4-py3-none-any.whl (97 kB)
[fastapi] Downloading bt_decode-0.8.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (647 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 647.8/647.8 kB 100.3 MB/s eta 0:00:00
[fastapi] Downloading colorama-0.4.6-py2.py3-none-any.whl (25 kB)
[fastapi] Downloading pydantic-2.9.2-py3-none-any.whl (434 kB)
[fastapi] Downloading pydantic_core-2.23.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 113.6 MB/s eta 0:00:00
[fastapi] Downloading aiosqlite-0.22.1-py3-none-any.whl (17 kB)
[fastapi] Downloading base58-2.1.1-py3-none-any.whl (5.6 kB)
[fastapi] Downloading ecdsa-0.19.2-py2.py3-none-any.whl (150 kB)
[fastapi] Downloading eth_keys-0.8.0-py3-none-any.whl (20 kB)
[fastapi] Downloading eth_utils-2.3.2-py3-none-any.whl (77 kB)
[fastapi] Downloading py_bip39_bindings-0.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (432 kB)
[fastapi] Downloading py_ed25519_zebra_bindings-1.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (323 kB)
[fastapi] Downloading py_sr25519_bindings-0.2.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (372 kB)
[fastapi] Downloading pynacl-1.6.2-cp38-abi3-manylinux_2_34_x86_64.whl (1.4 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.4/1.4 MB 105.6 MB/s eta 0:00:00
[fastapi] Downloading scalecodec-1.2.12-py3-none-any.whl (99 kB)
[fastapi] Downloading websockets-17.1-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (224 kB)
[fastapi] Downloading xxhash-3.8.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (220 kB)
[fastapi] Downloading cytoolz-1.1.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (2.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.8/2.8 MB 136.7 MB/s eta 0:00:00
[fastapi] Downloading eth_hash-0.8.0-py3-none-any.whl (8.0 kB)
[fastapi] Downloading toolz-1.1.0-py3-none-any.whl (58 kB)
[fastapi] Building wheels for collected packages: fiber
[fastapi] Building wheel for fiber (pyproject.toml): started
[fastapi] Building wheel for fiber (pyproject.toml): finished with status 'done'
[fastapi] Created wheel for fiber: filename=fiber-2.4.0-py3-none-any.whl size=51790 sha256=c50f803eff2fbcdf01560cfffdc65a3891a75b0b315d61d842fd3861f51b5d73
[fastapi] Stored in directory: /tmp/pip-ephem-wheel-cache-gpvbii_f/wheels/d1/5e/21/2fa1f403cd187996037f04f6328bf11973ce31440a275f6949
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
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 25.0.1 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0m ---> e3f6ed77e42f
[fastapi] Step 8/13 : RUN pip install --index-url https://download.pytorch.org/whl/cu128     torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0
[fastapi] ---> Running in 3cbfda365432
[fastapi] Looking in indexes: https://download.pytorch.org/whl/cu128
[fastapi] Requirement already satisfied: torch==2.8.0 in /usr/local/lib/python3.11/dist-packages (2.8.0)
[fastapi] Collecting torchvision==0.23.0
[fastapi] Downloading https://download-r2.pytorch.org/whl/cu128/torchvision-0.23.0%2Bcu128-cp311-cp311-manylinux_2_28_x86_64.whl.metadata (6.1 kB)
[fastapi] Collecting torchaudio==2.8.0
[fastapi] Downloading https://download-r2.pytorch.org/whl/cu128/torchaudio-2.8.0%2Bcu128-cp311-cp311-manylinux_2_28_x86_64.whl.metadata (7.2 kB)
[fastapi] Requirement already satisfied: filelock in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (3.16.1)
[fastapi] Requirement already satisfied: typing-extensions>=4.10.0 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (4.16.0)
[fastapi] Requirement already satisfied: sympy>=1.13.3 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (1.13.3)
[fastapi] Requirement already satisfied: networkx in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (3.4.2)
[fastapi] Requirement already satisfied: jinja2 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (3.1.4)
[fastapi] Requirement already satisfied: fsspec in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (2024.10.0)
[fastapi] Requirement already satisfied: nvidia-cuda-nvrtc-cu12==12.8.93 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (12.8.93)
[fastapi] Requirement already satisfied: nvidia-cuda-runtime-cu12==12.8.90 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (12.8.90)
[fastapi] Requirement already satisfied: nvidia-cuda-cupti-cu12==12.8.90 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (12.8.90)
[fastapi] Requirement already satisfied: nvidia-cudnn-cu12==9.10.2.21 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (9.10.2.21)
[fastapi] Requirement already satisfied: nvidia-cublas-cu12==12.8.4.1 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (12.8.4.1)
[fastapi] Requirement already satisfied: nvidia-cufft-cu12==11.3.3.83 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (11.3.3.83)
[fastapi] Requirement already satisfied: nvidia-curand-cu12==10.3.9.90 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (10.3.9.90)
[fastapi] Requirement already satisfied: nvidia-cusolver-cu12==11.7.3.90 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (11.7.3.90)
[fastapi] Requirement already satisfied: nvidia-cusparse-cu12==12.5.8.93 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (12.5.8.93)
[fastapi] Requirement already satisfied: nvidia-cusparselt-cu12==0.7.1 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (0.7.1)
[fastapi] Requirement already satisfied: nvidia-nccl-cu12==2.27.3 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (2.27.3)
[fastapi] Requirement already satisfied: nvidia-nvtx-cu12==12.8.90 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (12.8.90)
[fastapi] Requirement already satisfied: nvidia-nvjitlink-cu12==12.8.93 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (12.8.93)
[fastapi] Requirement already satisfied: nvidia-cufile-cu12==1.13.1.3 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (1.13.1.3)
[fastapi] Requirement already satisfied: triton==3.4.0 in /usr/local/lib/python3.11/dist-packages (from torch==2.8.0) (3.4.0)
[fastapi] Requirement already satisfied: numpy in /usr/local/lib/python3.11/dist-packages (from torchvision==0.23.0) (2.1.2)
[fastapi] Requirement already satisfied: pillow!=8.3.*,>=5.3.0 in /usr/local/lib/python3.11/dist-packages (from torchvision==0.23.0) (11.0.0)
[fastapi] Requirement already satisfied: setuptools>=40.8.0 in /usr/local/lib/python3.11/dist-packages (from triton==3.4.0->torch==2.8.0) (75.8.0)
[fastapi] Requirement already satisfied: mpmath<1.4,>=1.1.0 in /usr/local/lib/python3.11/dist-packages (from sympy>=1.13.3->torch==2.8.0) (1.3.0)
[fastapi] Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.11/dist-packages (from jinja2->torch==2.8.0) (2.1.5)
[fastapi] Downloading https://download-r2.pytorch.org/whl/cu128/torchvision-0.23.0%2Bcu128-cp311-cp311-manylinux_2_28_x86_64.whl (8.6 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.6/8.6 MB 177.2 MB/s eta 0:00:00
[fastapi] Downloading https://download-r2.pytorch.org/whl/cu128/torchaudio-2.8.0%2Bcu128-cp311-cp311-manylinux_2_28_x86_64.whl (3.9 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.9/3.9 MB 106.8 MB/s eta 0:00:00
[fastapi] Installing collected packages: torchvision, torchaudio
[fastapi] Attempting uninstall: torchvision
[fastapi] Found existing installation: torchvision 0.22.0.dev20250319+cu128
[fastapi] Uninstalling torchvision-0.22.0.dev20250319+cu128:
[fastapi] Successfully uninstalled torchvision-0.22.0.dev20250319+cu128
[fastapi] Attempting uninstall: torchaudio
[fastapi] Found existing installation: torchaudio 2.6.0.dev20250319+cu128
[fastapi] Uninstalling torchaudio-2.6.0.dev20250319+cu128:
[fastapi] Successfully uninstalled torchaudio-2.6.0.dev20250319+cu128
[fastapi] Successfully installed torchaudio-2.8.0+cu128 torchvision-0.23.0+cu128
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 25.0.1 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0m ---> 37bac079600a
[fastapi] Step 9/13 : RUN python -m venv /workspace/grpo_py &&     /workspace/grpo_py/bin/pip install -U pip uv &&     /workspace/grpo_py/bin/python -m uv pip install         --python /workspace/grpo_py/bin/python         -r /workspace/scripts/grpo_requirements.txt &&     /workspace/grpo_py/bin/python -c "import torch, vllm, trl, transformers; print('grpo venv', torch.__version__, vllm.__version__, trl.__version__, transformers.__version__)"
[fastapi] ---> Running in cc089c181f16
[fastapi] Requirement already satisfied: pip in /workspace/grpo_py/lib/python3.11/site-packages (24.0)
[fastapi] Collecting pip
[fastapi] Downloading pip-26.2.1-py3-none-any.whl.metadata (4.6 kB)
[fastapi] Collecting uv
[fastapi] Using cached uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] Downloading pip-26.2.1-py3-none-any.whl (1.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 27.3 MB/s eta 0:00:00
[fastapi] Using cached uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.1 MB)
[fastapi] Installing collected packages: uv, pip
[fastapi] Attempting uninstall: pip
[fastapi] Found existing installation: pip 24.0
[fastapi] Uninstalling pip-24.0:
[fastapi] Successfully uninstalled pip-24.0
[fastapi] Successfully installed pip-26.2.1 uv-0.12.15
[fastapi] [91mUsing Python 3.11.11 environment at: /workspace/grpo_py
[fastapi] [0m[91mResolved 258 packages in 350ms
[fastapi] [0m[91mDownloading nvidia-cuda-nvrtc (86.0MiB)
[fastapi] [0m[91mDownloading pillow (6.6MiB)
[fastapi] [0m[91mDownloading networkx (2.0MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-runtime (2.1MiB)
[fastapi] [0m[91mDownloading uvloop (3.6MiB)
[fastapi] [0m[91mDownloading pycountry (7.7MiB)
[fastapi] [0m[91mDownloading fastsafetensors (2.0MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-cupti (10.2MiB)
[fastapi] [0m[91mDownloading nvidia-curand (56.8MiB)
[fastapi] [0m[91mDownloading mistral-common (6.2MiB)
[fastapi] [0m[91mDownloading sympy (6.0MiB)
[fastapi] [0m[91mDownloading nvidia-cusparselt-cu13 (162.0MiB)
[fastapi] [0m[91mDownloading nvidia-nvjitlink (38.8MiB)
[fastapi] [0m[91mDownloading nvidia-cusolver (191.6MiB)
[fastapi] [0m[91mDownloading flashinfer-python (13.9MiB)
[fastapi] [0m[91mDownloading torchvision (7.2MiB)
[fastapi] [0m[91mDownloading nvidia-nvshmem-cu13 (57.6MiB)
[fastapi] [0m[91mDownloading tilelang (43.3MiB)
[fastapi] [0m[91mDownloading xgrammar (1.2MiB)
[fastapi] [0m[91mDownloading nvidia-cusparse (139.2MiB)
[fastapi] [0m[91mDownloading vllm (289.6MiB)
[fastapi] [0m[91mDownloading opencv-python-headless (58.4MiB)
[fastapi] [0m[91mDownloading nvidia-cutlass-dsl-libs-base (2.7MiB)
[fastapi] [0m[91mDownloading nvidia-cudnn-cu13 (349.1MiB)
[fastapi] [0m[91mDownloading torchcodec (9.0MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-nvcc (45.5MiB)
[fastapi] [0m[91mDownloading numba (3.6MiB)
[fastapi] [0m[91mDownloading z3-solver (27.9MiB)
[fastapi] [0m[91mDownloading nvidia-cufft (204.2MiB)
[fastapi] [0m[91mDownloading pynvvideocodec (41.2MiB)
[fastapi] [0m[91mDownloading llvmlite (53.7MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-cccl (3.7MiB)
[fastapi] [0m[91mDownloading torchaudio (1.7MiB)
[fastapi] [0m[91mDownloading numpy (16.1MiB)
[fastapi] [0m[91mDownloading cuda-bindings (6.8MiB)
[fastapi] [0m[91mDownloading nvidia-cutlass-dsl-libs-cu12 (84.3MiB)
[fastapi] [0m[91mDownloading nvidia-cublas (403.5MiB)
[fastapi] [0m[91mDownloading nvidia-nccl-cu13 (187.4MiB)
[fastapi] [0m[91mDownloading outlines-core (2.2MiB)
[fastapi] [0m[91mDownloading torch (506.0MiB)
[fastapi] [0m[91mDownloading openai-harmony (2.8MiB)
[fastapi] [0m[91mDownloading nvidia-cutlass-dsl-libs-cu13 (83.9MiB)
[fastapi] [0m[91mDownloading nvidia-nvvm (69.2MiB)
[fastapi] [0m[91mDownloading llguidance (2.9MiB)
[fastapi] [0m[91mDownloading cuda-core (6.2MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-nvdisasm (5.0MiB)
[fastapi] [0m[91mDownloading nvidia-cudnn-frontend (5.4MiB)
[fastapi] [0m[91mDownloading tokenspeed-triton (77.9MiB)
[fastapi] [0m[91mDownloading triton (179.5MiB)
[fastapi] [0m[91mDownloading apache-tvm-ffi (2.5MiB)
[fastapi] [0m[91m Downloaded xgrammar
[fastapi] [0m[91mDownloading pygments (1.2MiB)
[fastapi] [0m[91m Downloaded torchaudio
[fastapi] [0m[91mDownloading anthropic (1.2MiB)
[fastapi] [0m[91m Downloaded fastsafetensors
[fastapi] [0m[91m Downloaded networkx
[fastapi] [0m[91mDownloading nvidia-cufile (1.2MiB)
[fastapi] [0m[91mDownloading tiktoken (1.2MiB)
[fastapi] [0m[91m Downloaded nvidia-cuda-runtime
[fastapi] [0m[91m Downloaded outlines-core
[fastapi] [0m[91m Downloaded nvidia-cutlass-dsl-libs-base
[fastapi] [0m[91m Downloaded pygments
[fastapi] [0m[91m Downloaded apache-tvm-ffi
[fastapi] [0m[91m Downloaded anthropic
[fastapi] [0m[91m Downloaded openai-harmony
[fastapi] [0m[91m Downloaded llguidance
[fastapi] [0m[91m Downloaded nvidia-cufile
[fastapi] [0m[91m Downloaded tiktoken
[fastapi] [0m[91m Downloaded numba
[fastapi] [0m[91m Downloaded uvloop
[fastapi] [0m[91m Downloaded nvidia-cuda-cccl
[fastapi] [0m[91m Downloaded nvidia-cuda-nvdisasm
[fastapi] [0m[91m Downloaded nvidia-cudnn-frontend
[fastapi] [0m[91m Downloaded sympy
[fastapi] [0m[91m Downloaded mistral-common
[fastapi] [0m[91m Downloaded cuda-core
[fastapi] [0m[91m Downloaded pillow
[fastapi] [0m[91m Downloaded cuda-bindings
[fastapi] [0m[91m Downloaded torchvision
[fastapi] [0m[91m Downloaded pycountry
[fastapi] [0m[91m Downloaded torchcodec
[fastapi] [0m[91m Downloaded nvidia-cuda-cupti
[fastapi] [0m[91m Downloaded flashinfer-python
[fastapi] [0m[91m Downloaded numpy
[fastapi] [0m[91m Downloaded z3-solver
[fastapi] [0m[91m Downloaded nvidia-nvjitlink
[fastapi] [0m[91m Downloaded pynvvideocodec
[fastapi] [0m[91m Downloaded tilelang
[fastapi] [0m[91m Downloaded nvidia-cuda-nvcc
[fastapi] [0m[91m Downloaded llvmlite
[fastapi] [0m[91m Downloaded nvidia-curand
[fastapi] [0m[91m Downloaded nvidia-nvshmem-cu13
[fastapi] [0m[91m Downloaded opencv-python-headless
[fastapi] [0m[91m Downloaded nvidia-nvvm
[fastapi] [0m[91m Downloaded tokenspeed-triton
[fastapi] [0m[91m Downloaded nvidia-cutlass-dsl-libs-cu12
[fastapi] [0m[91m Downloaded nvidia-cuda-nvrtc
[fastapi] [0m[91m Downloaded nvidia-cutlass-dsl-libs-cu13
[fastapi] [0m[91m Downloaded nvidia-cusparse
[fastapi] [0m[91m Downloaded nvidia-cusparselt-cu13
[fastapi] [0m[91m Downloaded nvidia-nccl-cu13
[fastapi] [0m[91m Downloaded triton
[fastapi] [0m[91m Downloaded nvidia-cusolver
[fastapi] [0m[91m Downloaded nvidia-cufft
[fastapi] [0m[91m Downloaded nvidia-cudnn-cu13
[fastapi] [0m[91m Downloaded nvidia-cublas
[fastapi] [0m[91m Downloaded vllm
[fastapi] [0m[91m Downloaded torch
[fastapi] [0m[91mPrepared 151 packages in 8.03s
[fastapi] [0m[91mInstalled 257 packages in 6.27s
[fastapi] [0m[91m + absl-py==2.5.0
[fastapi] + accelerate==1.14.0
[fastapi] + agent-detector==2.0.0
[fastapi] + aiohappyeyeballs==2.7.1
[fastapi] + aiohttp==3.14.3
[fastapi] + aiosignal==1.4.0
[fastapi] + annotated-doc[0m[91m==0.0.5
[fastapi] + annotated-types==0.8.0
[fastapi] + anthropic==1.6.0[0m[91m
[fastapi] +[0m[91m antlr4-python3-runtime==4.9.[0m[91m3
[fastapi] + anyio==4.15.1
[fastapi] + apache-tvm-ffi==0.1.10
[fastapi] + argon2-cffi==[0m[91m25.1.0
[fastapi] + argon2-cffi-bindings==26.1.0
[fastapi] + astor[0m[91m==0.8.1[0m[91m
[fastapi] +[0m[91m [0m[91mattrs==26.1[0m[91m.0
[fastapi] + beautifulsoup4==4.15.0
[fastapi] + bitsandbytes==0.49.2
[fastapi] + blake3==1.0.9
[fastapi] + blinker[0m[91m==1.9.0
[fastapi] + cachetools==7.2.[0m[91m0
[fastapi] +[0m[91m cbor2[0m[91m==6.1[0m[91m.4
[fastapi] [0m[91m + certifi==2026.7.22
[fastapi] + cffi[0m[91m==2.1.1
[fastapi] + charset-normalizer[0m[91m==3.5.1
[fastapi] + [0m[91mclick==[0m[91m8.5[0m[91m.0
[fastapi] [0m[91m +[0m[91m [0m[91mcloudpickle==3[0m[91m.1.[0m[91m2
[fastapi] [0m[91m+[0m[91m cmudict[0m[91m==1.[0m[91m1.3[0m[91m
[fastapi] [0m[91m + comm[0m[91m==0.2.3[0m[91m
[fastapi] + compressed-tensors==0[0m[91m.17.0
[fastapi] + cryptography==50.[0m[91m0.1[0m[91m
[fastapi] [0m[91m+ [0m[91mcuda-bindings[0m[91m==13.4.1
[fastapi] + cuda-core==1.2.[0m[91m0
[fastapi] [0m[91m + [0m[91mcuda-pathfinder[0m[91m==1.8.[0m[91m1
[fastapi] [0m[91m+ cuda-python==13.4.1
[fastapi] + cuda-tile[0m[91m==1.6.0
[fastapi] + cuda-toolkit==[0m[91m13.0.2
[fastapi] +[0m[91m [0m[91mdash==4.4.1
[fastapi] + datasets==5.0.1
[fastapi] +[0m[91m deepspeed==0.19.2
[fastapi] [0m[91m+ defusedxml==0.7.1
[fastapi] [0m[91m+ depyf[0m[91m==0.20.0
[fastapi] + detect-installer==0.2.1
[fastapi] [0m[91m+ detoxify==0.5.2
[fastapi] +[0m[91m dill==0.[0m[91m4.1
[fastapi] +[0m[91m dnspython==2.8.0
[fastapi] + docker-pycreds==0.[0m[91m4.0
[fastapi] +[0m[91m docstring-parser[0m[91m==[0m[91m0.18.0[0m[91m
[fastapi] +[0m[91m einops[0m[91m==0.8.1[0m[91m
[fastapi] + email-validator==2.3.0
[fastapi] [0m[91m+ fastapi==0.[0m[91m136.3
[fastapi] + [0m[91mfastapi-cli==0.0.[0m[91m32
[fastapi] +[0m[91m fastapi-cloud-cli==[0m[91m0.26.0
[fastapi] [0m[91m+ fastar[0m[91m==0.12[0m[91m.0
[fastapi] +[0m[91m fastsafetensors==0[0m[91m.4.0
[fastapi] [0m[91m+ filelock==3.32.7[0m[91m
[fastapi] + [0m[91mflashinfer-python==0.6.[0m[91m14
[fastapi] [0m[91m+ flask==3[0m[91m.1.3
[fastapi] [0m[91m + frozenlist==1.8.[0m[91m0
[fastapi] +[0m[91m fsspec==2026.[0m[91m6.0
[fastapi] +[0m[91m gdown[0m[91m==[0m[91m6.3.0[0m[91m
[fastapi] [0m[91m+ [0m[91mgitdb==4[0m[91m.[0m[91m0.12[0m[91m
[fastapi] +[0m[91m gitpython[0m[91m==3.1.62
[fastapi] [0m[91m+ googleapis-common-protos[0m[91m==1.75.3
[fastapi] + grpcio==1.[0m[91m84.0
[fastapi] + h11[0m[91m==0.[0m[91m16.0[0m[91m
[fastapi] +[0m[91m [0m[91mhf-xet==1.6[0m[91m.0
[fastapi] [0m[91m + [0m[91mhjson[0m[91m==3.1.[0m[91m0[0m[91m
[fastapi] [0m[91m+ httpcore==1.0.9
[fastapi] + httpcore2==2.13.0
[fastapi] [0m[91m + httptools==0[0m[91m.8.0
[fastapi] [0m[91m [0m[91m+[0m[91m httpx==0.28[0m[91m.[0m[91m1
[fastapi] [0m[91m+ httpx2[0m[91m==2.13[0m[91m.[0m[91m0
[fastapi] [0m[91m+ huggingface-hub[0m[91m==1.31.0
[fastapi] + humming-kernels[0m[91m==0.1.10
[fastapi] [0m[91m+ idna==[0m[91m3[0m[91m.19
[fastapi] [0m[91m+[0m[91m ijson[0m[91m==3.5.1
[fastapi] [0m[91m + [0m[91mimportlib-metadata[0m[91m==9.0.[0m[91m1[0m[91m
[fastapi] + [0m[91mimportlib-resources==7[0m[91m.1[0m[91m.0
[fastapi] [0m[91m+[0m[91m interegular[0m[91m==0.3.3
[fastapi] +[0m[91m itsdangerous[0m[91m==2.2.0
[fastapi] + jaconv[0m[91m==0.5.0[0m[91m
[fastapi] + janus[0m[91m==2.0.0
[fastapi] [0m[91m+ jinja2==[0m[91m3.1.6
[fastapi] [0m[91m + jiter[0m[91m==0.17.[0m[91m0
[fastapi] +[0m[91m jmespath==1.[0m[91m1.0
[fastapi] [0m[91m+ joblib==1.6.0
[fastapi] + [0m[91mjsonschema==4.26.0[0m[91m
[fastapi] + jsonschema-specifications[0m[91m==2025.9.[0m[91m1
[fastapi] +[0m[91m langcheck==0[0m[91m.9.0[0m[91m
[fastapi] + lark[0m[91m==1.2.[0m[91m2
[fastapi] + llguidance==1.7[0m[91m.6
[fastapi] + llvmlite==0.[0m[91m47.0
[fastapi] [0m[91m+ lm-format-enforcer==0.11.3
[fastapi] [0m[91m+ loguru==0.7.[0m[91m3
[fastapi] + [0m[91mmarkdown-it-py==4.[0m[91m2.0
[fastapi] [0m[91m+ markupsafe[0m[91m==3.0.[0m[91m3
[fastapi] +[0m[91m mcp==2[0m[91m.2.0
[fastapi] [0m[91m+ mcp-types==[0m[91m2.2.0
[fastapi] + mdurl==0[0m[91m.1.2
[fastapi] + [0m[91mminio==7.2.20[0m[91m
[fastapi] + mistral-common==1.11.7
[fastapi] + [0m[91mml-dtypes==0.6.0[0m[91m
[fastapi] + model-hosting-container-standards[0m[91m==0.1.[0m[91m16
[fastapi] +[0m[91m mpmath[0m[91m==1.3.0
[fastapi] + msgpack==1.2.[0m[91m2
[fastapi] + msgspec==0[0m[91m.21.1
[fastapi] + multidict==6[0m[91m.8[0m[91m.0
[fastapi] [0m[91m+ [0m[91mmultiprocess==0[0m[91m.70.[0m[91m19
[fastapi] + narwhals==2.26.0
[fastapi] +[0m[91m nest-asyncio==1.6.0
[fastapi] [0m[91m +[0m[91m [0m[91mnetworkx==3.6.1
[fastapi] + ninja[0m[91m==1.13.[0m[91m2
[fastapi] +[0m[91m nlpaug[0m[91m==1.[0m[91m1.[0m[91m11
[fastapi] + nltk[0m[91m==3.10.[0m[91m3
[fastapi] [0m[91m + [0m[91mnumba[0m[91m==0.65.0
[fastapi] + numpy==[0m[91m2.3.5
[fastapi] + nvidia-cublas==13.1[0m[91m.0.3
[fastapi] + nvidia-cuda-cccl[0m[91m==13.3.[0m[91m4.3[0m[91m.1
[fastapi] [0m[91m [0m[91m+ [0m[91mnvidia-cuda-crt==13.4.92
[fastapi] [0m[91m + nvidia-cuda-cupti[0m[91m==13.0[0m[91m.85[0m[91m
[fastapi] + nvidia-cuda-nvcc==13.4.92
[fastapi] +[0m[91m nvidia-cuda-nvdisasm==13.4.92
[fastapi] [0m[91m + nvidia-cuda-nvrtc[0m[91m==13.[0m[91m0.88[0m[91m
[fastapi] +[0m[91m nvidia-cuda-runtime[0m[91m==13.0.96[0m[91m
[fastapi] + nvidia-cudnn-cu13==9.19.0.56[0m[91m
[fastapi] + nvidia-cudnn-frontend==[0m[91m1.28.[0m[91m0
[fastapi] +[0m[91m nvidia-cufft==12[0m[91m.0.0.61
[fastapi] + nvidia-cufile==[0m[91m1.15.1.6
[fastapi] [0m[91m + nvidia-curand==10.[0m[91m4.0.35
[fastapi] [0m[91m+ nvidia-cusolver==[0m[91m12.0.4[0m[91m.66
[fastapi] +[0m[91m nvidia-cusparse==12[0m[91m.6.3.3[0m[91m
[fastapi] + nvidia-cusparselt-cu13==0.8[0m[91m.0
[fastapi] + [0m[91mnvidia-cutlass-dsl==4.6.[0m[91m0
[fastapi] + [0m[91mnvidia-cutlass-dsl-libs-base[0m[91m==4[0m[91m.6.[0m[91m0
[fastapi] [0m[91m+[0m[91m nvidia-cutlass-dsl-libs-core[0m[91m==4.[0m[91m6.0[0m[91m
[fastapi] [0m[91m+ nvidia-cutlass-dsl-libs-cu12==4.6.0[0m[91m
[fastapi] [0m[91m +[0m[91m nvidia-cutlass-dsl-libs-cu13[0m[91m==4.6[0m[91m.0
[fastapi] + nvidia-ml-py==13.610[0m[91m.43
[fastapi] + nvidia-nccl-cu13==2[0m[91m.28.9
[fastapi] [0m[91m+[0m[91m nvidia-nvjitlink==13[0m[91m.0[0m[91m.88
[fastapi] [0m[91m [0m[91m+ nvidia-nvshmem-cu13==[0m[91m3.4.5
[fastapi] + nvidia-nvtx==13[0m[91m.0.85[0m[91m
[fastapi] +[0m[91m nvidia-nvvm[0m[91m==13.4.92[0m[91m
[fastapi] + nvtx==0.2.15
[fastapi] + omegaconf==2.3.1
[fastapi] + openai==3.14.1
[fastapi] + openai-harmony==0.0.8
[fastapi] + opencv-python-headless==5.0.0.93
[fastapi] + opentelemetry-api==1.44.0
[fastapi] + opentelemetry-exporter-otlp==1.44.0
[fastapi] + opentelemetry-exporter-otlp-proto-common==1.44.0
[fastapi] + opentelemetry-exporter-otlp-proto-grpc==1.44.0
[fastapi] + opentelemetry-exporter-otlp-proto-http==1.44.0
[fastapi] + opentelemetry-proto==1.44.0
[fastapi] + opentelemetry-sdk==1.44.0
[fastapi] + opentelemetry-semantic-conventions==0.65b0
[fastapi] + opentelemetry-semantic-conventions-ai==0.5.1
[fastapi] + outlines-core==0.2.14
[fastapi] + packaging==26.3
[fastapi] + pandas==2.2.3
[fastapi] + partial-json-parser==0.2.1.1.post7
[fastapi] + peft==0.19.1
[fastapi] + pillow==12.3.0
[fastapi] + platformdirs==4.11.9
[fastapi] + plotly==7.1.0
[fastapi] + prometheus-client==0.26.0
[fastapi] + prometheus-fastapi-instrumentator==8.1.0
[fastapi] + propcache==0.5.4
[fastapi] + protobuf==6.33.6
[fastapi] + psutil==7.2.2
[fastapi] + py-cpuinfo==9.0.0
[fastapi] + pyarrow==25.0.1
[fastapi] + pybase64==1.5.0
[fastapi] + pycountry==26.2.16
[fastapi] + pycparser==3.0
[fastapi] + pycryptodome==3.23.0
[fastapi] + pydantic==2.13.5
[fastapi] + pydantic-core==2.46.5
[fastapi] + pydantic-extra-types==2.11.1
[fastapi] + pydantic-settings==2.15.0
[fastapi] + pyelftools==0.33
[fastapi] + pygments==2.21.0
[fastapi] + pyjwt==2.14.0
[fastapi] + pynvvideocodec==2.0.4
[fastapi] + pyphen==0.18.1
[fastapi] + pysocks==1.7.1
[fastapi] + python-dateutil==2.9.0.post0
[fastapi] + python-dotenv==1.2.3
[fastapi] + python-json-logger==4.2.0
[fastapi] + python-multipart==0.0.32
[fastapi] + pytz==2026.3.post1
[fastapi] + pyyaml==6.0.3
[fastapi] + pyzmq==27.2.0
[fastapi] + quack-kernels==0.6.3
[fastapi] + referencing==0.37.0
[fastapi] + regex==2026.9.10
[fastapi] + requests==2.34.2
[fastapi] + restrictedpython==8.0
[fastapi] + retrying==1.4.2
[fastapi] + rich==15.0.0
[fastapi] + rich-toolkit==0.20.5
[fastapi] + rignore==0.8.1
[fastapi] + rouge-score==0.1.2
[fastapi] + rpds-py==2026.6.3
[fastapi] + safetensors==0.8.0
[fastapi] + scikit-learn==1.9.1
[fastapi] + scipy==1.15.2
[fastapi] + sentence-transformers==6.0.1
[fastapi] + sentencepiece==0.2.0
[fastapi] + sentry-sdk==2.69.2
[fastapi] + setproctitle==1.3.7
[fastapi] + shellingham==1.5.4
[fastapi] + six==1.17.0
[fastapi] + smmap==5.0.3
[fastapi] + sniffio==1.3.1
[fastapi] + soupsieve==2.9.2
[fastapi] + sse-starlette==3.4.11
[fastapi] + starlette==1.6.0
[fastapi] + supervisor==4.3.0
[fastapi] + sympy==1.14.0
[fastapi] + tabulate==0.10.0
[fastapi] + tenacity==9.1.4
[fastapi] + textstat==0.7.8
[fastapi] + threadpoolctl==3.7.0
[fastapi] + tiktoken==0.14.0
[fastapi] + tilelang==0.1.9
[fastapi] + tokenizers==0.22.2
[fastapi] + tokenspeed-mla==0.1.8
[fastapi] + tokenspeed-triton==3.8.10.post20260906
[fastapi] + torch==2.11.0
[fastapi] + torch-c-dlpack-ext==0.1.5
[fastapi] + torchaudio==2.11.0
[fastapi] + torchcodec==0.16.0
[fastapi] + torchvision==0.26.0
[fastapi] + tqdm==4.70.1
[fastapi] + transformers==5.12.1
[fastapi] + triton==3.6.0
[fastapi] + trl==1.10.0
[fastapi] + truststore==0.10.4
[fastapi] + typer==0.27.2
[fastapi] + typing-extensions==4.16.0
[fastapi] + typing-inspection==0.4.4
[fastapi] + tzdata==2026.4
[fastapi] + urllib3==2.8.0
[fastapi] + uvicorn==0.53.0
[fastapi] + uvloop==0.22.1
[fastapi] + vllm==0.26.0
[fastapi] + wandb==0.19.10
[fastapi] + watchfiles==1.2.0
[fastapi] + websockets==17.1
[fastapi] + werkzeug==3.1.8
[fastapi] + xgrammar==0.2.7
[fastapi] + xxhash==4.0.1
[fastapi] + yarl==1.25.1
[fastapi] + z3-solver==4.15.4.0
[fastapi] + zipp==4.1.0
[fastapi] [0mgrpo venv 2.11.0+cu130 0.26.0 1.10.0 5.12.1
[fastapi] ---> 4c863acafd3d
[fastapi] Step 10/13 : RUN python -c "import transformers; v=transformers.__version__; assert v == '5.12.1', v" &&     python -c "import torch; assert torch.__version__.startswith('2.8.0'), torch.__version__" &&     python -c "import liger_kernel; from liger_kernel.ops.fused_linear_cross_entropy import LigerFusedLinearCrossEntropyFunction as F; assert hasattr(F.forward, '__call__')" &&     python -c "import flash_attn, trl, peft, bitsandbytes" &&     python -c "from deepspeed import DeepSpeedEngine; print('deps ok (deepspeed importable)')"
[fastapi] ---> Running in 8e5dc8d141d1
[fastapi] [91mFailed to load CPU gemm_4bit_forward from kernels-community: No module named 'kernels'. Please make sure you already `pip install kernels` and the kernels >= 0.11.1
[fastapi] [0m[2026-09-16 22:02:09,722] [WARNING] [real_accelerator.py:199:get_accelerator] Setting accelerator to CPU. If you have GPU or other accelerator, we were unable to detect it.
[fastapi] [91m/usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[fastapi] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[fastapi] warnings.warn(
[fastapi] [0mdeps ok (deepspeed importable)
[fastapi] ---> bc24f4b08d23
[fastapi] Step 11/13 : COPY scripts /workspace/scripts
[fastapi] ---> 7a6af837e4a1
[fastapi] Step 12/13 : RUN chmod +x /workspace/scripts/entrypoint.sh
[fastapi] ---> Running in 85a3eef07de3
[fastapi] ---> 11683c3f21b3
[fastapi] Step 13/13 : ENTRYPOINT ["./entrypoint.sh"]
[fastapi] ---> Running in cfb0904653b3
[fastapi] ---> e752141e52c1
[fastapi] {'aux': {'ID': 'sha256:e752141e52c114292ecfaf1a5ce1f0d4395213c85b4c42ec5f3f88e693cf067e'}}Successfully built e752141e52c1
[fastapi] Successfully tagged standalone-text-trainer:6385764c-f269-4f23-8815-8ad39778f415
[fastapi] Docker image built successfully.
[fastapi] Training cancelled
[hf-upload-bc] Traceback (most recent call last):
[hf-upload-bc]   File "/usr/local/lib/python3.10/site-packages/huggingface_hub/utils/_http.py", line 808, in hf_raise_for_status
[hf-upload-bc]     response.raise_for_status()
[hf-upload-bc]   File "/usr/local/lib/python3.10/site-packages/httpx/_models.py", line 829, in raise_for_status
[hf-upload-bc]     raise HTTPStatusError(message, request=request, response=self)
[hf-upload-bc] httpx.HTTPStatusError: Client error '401 Unauthorized' for url 'https://huggingface.co/api/whoami-v2'
[hf-upload-bc] For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/401
[hf-upload-bc] 
[hf-upload-bc] The above exception was the direct cause of the following exception:
[hf-upload-bc] 
[hf-upload-bc] Traceback (most recent call last):
[hf-upload-bc]   File "/usr/local/lib/python3.10/site-packages/huggingface_hub/hf_api.py", line 2388, in _inner_whoami
[hf-upload-bc]     hf_raise_for_status(r)
[hf-upload-bc]   File "/usr/local/lib/python3.10/site-packages/huggingface_hub/utils/_http.py", line 938, in hf_raise_for_status
[hf-upload-bc]     raise _format(HfHubHTTPError, str(e), response) from e
[hf-upload-bc] huggingface_hub.errors.HfHubHTTPError: Client error '401 Unauthorized' for url 'https://huggingface.co/api/whoami-v2' (Request ID: Root=1-6aab0ed9-0ca862d512c9dd22771e8e69;b70ba232-e7db-47c6-8fda-a8e7130e240e)
[hf-upload-bc] For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/401
[hf-upload-bc] 
[hf-upload-bc] User Access Token "grads2026" is expired
[hf-upload-bc] 
[hf-upload-bc] The above exception was the direct cause of the following exception:
[hf-upload-bc] 
[hf-upload-bc] Traceback (most recent call last):
[hf-upload-bc]   File "/app/trainer/containers/uploader.py", line 246, in <module>
[hf-upload-bc]     main()
[hf-upload-bc]   File "/app/trainer/containers/uploader.py", line 172, in main
[hf-upload-bc]     login(token=hf_token)
[hf-upload-bc]   File "/usr/local/lib/python3.10/site-packages/huggingface_hub/_login.py", line 107, in login
[hf-upload-bc]     _validate_and_save_token(token, add_to_git_credential=add_to_git_credential)
[hf-upload-bc]   File "/usr/local/lib/python3.10/site-packages/huggingface_hub/_login.py", line 429, in _validate_and_save_token
[hf-upload-bc]     token_info = whoami(token)
[hf-upload-bc]   File "/usr/local/lib/python3.10/site-packages/huggingface_hub/utils/_validators.py", line 88, in _inner_fn
[hf-upload-bc]     return fn(*args, **kwargs)
[hf-upload-bc]   File "/usr/local/lib/python3.10/site-packages/huggingface_hub/hf_api.py", line 2375, in whoami
[hf-upload-bc]     output = self._inner_whoami(token=token)
[hf-upload-bc]   File "/usr/local/lib/python3.10/site-packages/huggingface_hub/hf_api.py", line 2404, in _inner_whoami
[hf-upload-bc]     raise HfHubHTTPError(error_message, response=e.response) from e
[hf-upload-bc] huggingface_hub.errors.HfHubHTTPError: Invalid user token.
[text-trainer] *****Running text trainer
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_hash" in MinerSubmission has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] [2026-09-16 17:25:51,282] [WARNING] [runner.py:232:fetch_hostfile] Unable to find hostfile, will proceed with training with local resources only.
[text-trainer] [2026-09-16 17:25:51,282] [INFO] [runner.py:630:main] cmd = /usr/bin/python -u -m deepspeed.launcher.launch --world_info=eyJsb2NhbGhvc3QiOiBbMCwgMSwgMiwgM119 --master_addr=127.0.0.1 --master_port=29500 --enable_each_rank_log=None --log_level=info train_instruct.py --request_path datasets/training_request_059bf721-cca5-4d02-9832-a794cf37074b.json --bf16 True --report_to wandb --output_dir /workspace/scripts/soutputs/059bf721-cca5-4d02-9832-a794cf37074b --num_train_epochs 3 --per_device_train_batch_size 1 --per_device_eval_batch_size 1 --gradient_accumulation_steps 1 --eval_accumulation_steps 1 --eval_strategy no --save_strategy epoch --logging_steps 1 --learning_rate 1.8790606746021028e-05 --weight_decay 0. --warmup_steps 200 --lr_scheduler_type cosine_with_min_lr --lr_scheduler_kwargs {"min_lr_rate": 0.25} --tf32 True --gradient_checkpointing True --optim paged_adamw_8bit --use_liger True --packing True --disable_fa False --dataloader_pin_memory True --deepspeed ds_config/zero2.json --use_lora True
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] [2026-09-16 17:25:57,382] [INFO] [launch.py:155:main] 0 NV_LIBNCCL_PACKAGE_VERSION=2.25.1-1
[text-trainer] [2026-09-16 17:25:57,382] [INFO] [launch.py:155:main] 0 NV_LIBNCCL_DEV_PACKAGE_VERSION=2.25.1-1
[text-trainer] [2026-09-16 17:25:57,382] [INFO] [launch.py:155:main] 0 NV_LIBNCCL_PACKAGE_NAME=libnccl2
[text-trainer] [2026-09-16 17:25:57,382] [INFO] [launch.py:155:main] 0 NV_LIBNCCL_DEV_PACKAGE_NAME=libnccl-dev
[text-trainer] [2026-09-16 17:25:57,383] [INFO] [launch.py:155:main] 0 NV_LIBNCCL_PACKAGE=libnccl2=2.25.1-1+cuda12.8
[text-trainer] [2026-09-16 17:25:57,383] [INFO] [launch.py:155:main] 0 NV_LIBNCCL_DEV_PACKAGE=libnccl-dev=2.25.1-1+cuda12.8
[text-trainer] [2026-09-16 17:25:57,383] [INFO] [launch.py:155:main] 0 NCCL_VERSION=2.25.1-1
[text-trainer] [2026-09-16 17:25:57,383] [INFO] [launch.py:162:main] WORLD INFO DICT: {'localhost': [0, 1, 2, 3]}
[text-trainer] [2026-09-16 17:25:57,383] [INFO] [launch.py:168:main] nnodes=1, num_local_procs=4, node_rank=0
[text-trainer] [2026-09-16 17:25:57,383] [INFO] [launch.py:179:main] global_rank_mapping=defaultdict(<class 'list'>, {'localhost': [0, 1, 2, 3]})
[text-trainer] [2026-09-16 17:25:57,383] [INFO] [launch.py:180:main] dist_world_size=4
[text-trainer] [2026-09-16 17:25:57,383] [INFO] [launch.py:184:main] Setting CUDA_VISIBLE_DEVICES=0,1,2,3
[text-trainer] [2026-09-16 17:25:57,383] [INFO] [launch.py:272:main] process 848 spawned with command: ['/usr/bin/python', '-u', 'train_instruct.py', '--local_rank=0', '--request_path', 'datasets/training_request_059bf721-cca5-4d02-9832-a794cf37074b.json', '--bf16', 'True', '--report_to', 'wandb', '--output_dir', '/workspace/scripts/soutputs/059bf721-cca5-4d02-9832-a794cf37074b', '--num_train_epochs', '3', '--per_device_train_batch_size', '1', '--per_device_eval_batch_size', '1', '--gradient_accumulation_steps', '1', '--eval_accumulation_steps', '1', '--eval_strategy', 'no', '--save_strategy', 'epoch', '--logging_steps', '1', '--learning_rate', '1.8790606746021028e-05', '--weight_decay', '0.', '--warmup_steps', '200', '--lr_scheduler_type', 'cosine_with_min_lr', '--lr_scheduler_kwargs', '{"min_lr_rate": 0.25}', '--tf32', 'True', '--gradient_checkpointing', 'True', '--optim', 'paged_adamw_8bit', '--use_liger', 'True', '--packing', 'True', '--disable_fa', 'False', '--dataloader_pin_memory', 'True', '--deepspeed', 'ds_config/zero2.json', '--use_lora', 'True']
[text-trainer] [2026-09-16 17:25:57,384] [INFO] [launch.py:272:main] process 849 spawned with command: ['/usr/bin/python', '-u', 'train_instruct.py', '--local_rank=1', '--request_path', 'datasets/training_request_059bf721-cca5-4d02-9832-a794cf37074b.json', '--bf16', 'True', '--report_to', 'wandb', '--output_dir', '/workspace/scripts/soutputs/059bf721-cca5-4d02-9832-a794cf37074b', '--num_train_epochs', '3', '--per_device_train_batch_size', '1', '--per_device_eval_batch_size', '1', '--gradient_accumulation_steps', '1', '--eval_accumulation_steps', '1', '--eval_strategy', 'no', '--save_strategy', 'epoch', '--logging_steps', '1', '--learning_rate', '1.8790606746021028e-05', '--weight_decay', '0.', '--warmup_steps', '200', '--lr_scheduler_type', 'cosine_with_min_lr', '--lr_scheduler_kwargs', '{"min_lr_rate": 0.25}', '--tf32', 'True', '--gradient_checkpointing', 'True', '--optim', 'paged_adamw_8bit', '--use_liger', 'True', '--packing', 'True', '--disable_fa', 'False', '--dataloader_pin_memory', 'True', '--deepspeed', 'ds_config/zero2.json', '--use_lora', 'True']
[text-trainer] [2026-09-16 17:25:57,384] [INFO] [launch.py:272:main] process 850 spawned with command: ['/usr/bin/python', '-u', 'train_instruct.py', '--local_rank=2', '--request_path', 'datasets/training_request_059bf721-cca5-4d02-9832-a794cf37074b.json', '--bf16', 'True', '--report_to', 'wandb', '--output_dir', '/workspace/scripts/soutputs/059bf721-cca5-4d02-9832-a794cf37074b', '--num_train_epochs', '3', '--per_device_train_batch_size', '1', '--per_device_eval_batch_size', '1', '--gradient_accumulation_steps', '1', '--eval_accumulation_steps', '1', '--eval_strategy', 'no', '--save_strategy', 'epoch', '--logging_steps', '1', '--learning_rate', '1.8790606746021028e-05', '--weight_decay', '0.', '--warmup_steps', '200', '--lr_scheduler_type', 'cosine_with_min_lr', '--lr_scheduler_kwargs', '{"min_lr_rate": 0.25}', '--tf32', 'True', '--gradient_checkpointing', 'True', '--optim', 'paged_adamw_8bit', '--use_liger', 'True', '--packing', 'True', '--disable_fa', 'False', '--dataloader_pin_memory', 'True', '--deepspeed', 'ds_config/zero2.json', '--use_lora', 'True']
[text-trainer] [2026-09-16 17:25:57,384] [INFO] [launch.py:272:main] process 851 spawned with command: ['/usr/bin/python', '-u', 'train_instruct.py', '--local_rank=3', '--request_path', 'datasets/training_request_059bf721-cca5-4d02-9832-a794cf37074b.json', '--bf16', 'True', '--report_to', 'wandb', '--output_dir', '/workspace/scripts/soutputs/059bf721-cca5-4d02-9832-a794cf37074b', '--num_train_epochs', '3', '--per_device_train_batch_size', '1', '--per_device_eval_batch_size', '1', '--gradient_accumulation_steps', '1', '--eval_accumulation_steps', '1', '--eval_strategy', 'no', '--save_strategy', 'epoch', '--logging_steps', '1', '--learning_rate', '1.8790606746021028e-05', '--weight_decay', '0.', '--warmup_steps', '200', '--lr_scheduler_type', 'cosine_with_min_lr', '--lr_scheduler_kwargs', '{"min_lr_rate": 0.25}', '--tf32', 'True', '--gradient_checkpointing', 'True', '--optim', 'paged_adamw_8bit', '--use_liger', 'True', '--packing', 'True', '--disable_fa', 'False', '--dataloader_pin_memory', 'True', '--deepspeed', 'ds_config/zero2.json', '--use_lora', 'True']
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] [W916 17:26:06.041205817 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W916 17:26:06.041644906 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W916 17:26:06.041634231 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W916 17:26:06.041851800 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W916 17:26:06.044543896 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W916 17:26:06.044763753 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W916 17:26:06.054486875 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W916 17:26:06.067168215 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] wandb: Tracking run with wandb version 0.19.10
[text-trainer] wandb: W&B syncing is set to `offline` in this directory. Run `wandb online` or set WANDB_MODE=online to enable cloud syncing.
[text-trainer] [1;34mwandb[0m: 
[text-trainer] [1;34mwandb[0m: You can sync this run to the cloud by running:
[text-trainer] [1;34mwandb[0m: [1mwandb sync /app/checkpoints/wandb_logs/059bf721-cca5-4d02-9832-a794cf37074b_5CkYizfLyb5hLmcK4WtBGG13WKTQrynHBEV6qC23748g17zC/wandb/offline-run-20260916_172853-059bf721-cca5-4d02-9832-a794cf37074b_tournament-tourn_5c64e784a087074a_20260914-059bf721-cca5-4d02-9832-a794cf37074b-5CkYizfL[0m
[text-trainer] [1;34mwandb[0m: Find logs at: [1;35m../../app/checkpoints/wandb_logs/059bf721-cca5-4d02-9832-a794cf37074b_5CkYizfLyb5hLmcK4WtBGG13WKTQrynHBEV6qC23748g17zC/wandb/offline-run-20260916_172853-059bf721-cca5-4d02-9832-a794cf37074b_tournament-tourn_5c64e784a087074a_20260914-059bf721-cca5-4d02-9832-a794cf37074b-5CkYizfL/logs[0m
[text-trainer] [rank0]:[W916 21:48:56.794451561 ProcessGroupNCCL.cpp:1538] Warning: WARNING: destroy_process_group() was not called before program exit, which can leak resources. For more info, please see https://pytorch.org/docs/stable/distributed.html#shutdown (function operator())
[text-trainer] [2026-09-16 21:48:57,976] [INFO] [launch.py:367:main] Process 850 exits successfully.
[text-trainer] [2026-09-16 21:48:57,976] [INFO] [launch.py:367:main] Process 849 exits successfully.
[text-trainer] [2026-09-16 21:48:58,976] [INFO] [launch.py:367:main] Process 851 exits successfully.
[text-trainer] [2026-09-16 21:48:59,977] [INFO] [launch.py:367:main] Process 848 exits successfully.
[text-trainer] *****Running text trainer
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_hash" in MinerSubmission has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] [2026-09-16 22:35:18,605] [WARNING] [runner.py:232:fetch_hostfile] Unable to find hostfile, will proceed with training with local resources only.
[text-trainer] [2026-09-16 22:35:18,605] [INFO] [runner.py:630:main] cmd = /usr/bin/python -u -m deepspeed.launcher.launch --world_info=eyJsb2NhbGhvc3QiOiBbMCwgMSwgMiwgM119 --master_addr=127.0.0.1 --master_port=29500 --enable_each_rank_log=None --log_level=info train_instruct.py --request_path datasets/training_request_059bf721-cca5-4d02-9832-a794cf37074b.json --bf16 True --report_to wandb --output_dir /workspace/scripts/soutputs/059bf721-cca5-4d02-9832-a794cf37074b --num_train_epochs 3 --per_device_train_batch_size 1 --per_device_eval_batch_size 1 --gradient_accumulation_steps 1 --eval_accumulation_steps 1 --eval_strategy no --save_strategy epoch --logging_steps 1 --learning_rate 1.8790606746021028e-05 --weight_decay 0. --warmup_steps 200 --lr_scheduler_type cosine_with_min_lr --lr_scheduler_kwargs {"min_lr_rate": 0.25} --tf32 True --gradient_checkpointing True --optim paged_adamw_8bit --use_liger True --packing True --disable_fa False --dataloader_pin_memory True --deepspeed ds_config/zero2.json --use_lora True
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] [2026-09-16 22:35:24,890] [INFO] [launch.py:155:main] 0 NV_LIBNCCL_PACKAGE_VERSION=2.25.1-1
[text-trainer] [2026-09-16 22:35:24,890] [INFO] [launch.py:155:main] 0 NV_LIBNCCL_DEV_PACKAGE_VERSION=2.25.1-1
[text-trainer] [2026-09-16 22:35:24,890] [INFO] [launch.py:155:main] 0 NV_LIBNCCL_PACKAGE_NAME=libnccl2
[text-trainer] [2026-09-16 22:35:24,890] [INFO] [launch.py:155:main] 0 NV_LIBNCCL_DEV_PACKAGE_NAME=libnccl-dev
[text-trainer] [2026-09-16 22:35:24,890] [INFO] [launch.py:155:main] 0 NV_LIBNCCL_PACKAGE=libnccl2=2.25.1-1+cuda12.8
[text-trainer] [2026-09-16 22:35:24,890] [INFO] [launch.py:155:main] 0 NV_LIBNCCL_DEV_PACKAGE=libnccl-dev=2.25.1-1+cuda12.8
[text-trainer] [2026-09-16 22:35:24,890] [INFO] [launch.py:155:main] 0 NCCL_VERSION=2.25.1-1
[text-trainer] [2026-09-16 22:35:24,890] [INFO] [launch.py:162:main] WORLD INFO DICT: {'localhost': [0, 1, 2, 3]}
[text-trainer] [2026-09-16 22:35:24,890] [INFO] [launch.py:168:main] nnodes=1, num_local_procs=4, node_rank=0
[text-trainer] [2026-09-16 22:35:24,890] [INFO] [launch.py:179:main] global_rank_mapping=defaultdict(<class 'list'>, {'localhost': [0, 1, 2, 3]})
[text-trainer] [2026-09-16 22:35:24,890] [INFO] [launch.py:180:main] dist_world_size=4
[text-trainer] [2026-09-16 22:35:24,890] [INFO] [launch.py:184:main] Setting CUDA_VISIBLE_DEVICES=0,1,2,3
[text-trainer] [2026-09-16 22:35:24,891] [INFO] [launch.py:272:main] process 848 spawned with command: ['/usr/bin/python', '-u', 'train_instruct.py', '--local_rank=0', '--request_path', 'datasets/training_request_059bf721-cca5-4d02-9832-a794cf37074b.json', '--bf16', 'True', '--report_to', 'wandb', '--output_dir', '/workspace/scripts/soutputs/059bf721-cca5-4d02-9832-a794cf37074b', '--num_train_epochs', '3', '--per_device_train_batch_size', '1', '--per_device_eval_batch_size', '1', '--gradient_accumulation_steps', '1', '--eval_accumulation_steps', '1', '--eval_strategy', 'no', '--save_strategy', 'epoch', '--logging_steps', '1', '--learning_rate', '1.8790606746021028e-05', '--weight_decay', '0.', '--warmup_steps', '200', '--lr_scheduler_type', 'cosine_with_min_lr', '--lr_scheduler_kwargs', '{"min_lr_rate": 0.25}', '--tf32', 'True', '--gradient_checkpointing', 'True', '--optim', 'paged_adamw_8bit', '--use_liger', 'True', '--packing', 'True', '--disable_fa', 'False', '--dataloader_pin_memory', 'True', '--deepspeed', 'ds_config/zero2.json', '--use_lora', 'True']
[text-trainer] [2026-09-16 22:35:24,891] [INFO] [launch.py:272:main] process 849 spawned with command: ['/usr/bin/python', '-u', 'train_instruct.py', '--local_rank=1', '--request_path', 'datasets/training_request_059bf721-cca5-4d02-9832-a794cf37074b.json', '--bf16', 'True', '--report_to', 'wandb', '--output_dir', '/workspace/scripts/soutputs/059bf721-cca5-4d02-9832-a794cf37074b', '--num_train_epochs', '3', '--per_device_train_batch_size', '1', '--per_device_eval_batch_size', '1', '--gradient_accumulation_steps', '1', '--eval_accumulation_steps', '1', '--eval_strategy', 'no', '--save_strategy', 'epoch', '--logging_steps', '1', '--learning_rate', '1.8790606746021028e-05', '--weight_decay', '0.', '--warmup_steps', '200', '--lr_scheduler_type', 'cosine_with_min_lr', '--lr_scheduler_kwargs', '{"min_lr_rate": 0.25}', '--tf32', 'True', '--gradient_checkpointing', 'True', '--optim', 'paged_adamw_8bit', '--use_liger', 'True', '--packing', 'True', '--disable_fa', 'False', '--dataloader_pin_memory', 'True', '--deepspeed', 'ds_config/zero2.json', '--use_lora', 'True']
[text-trainer] [2026-09-16 22:35:24,891] [INFO] [launch.py:272:main] process 850 spawned with command: ['/usr/bin/python', '-u', 'train_instruct.py', '--local_rank=2', '--request_path', 'datasets/training_request_059bf721-cca5-4d02-9832-a794cf37074b.json', '--bf16', 'True', '--report_to', 'wandb', '--output_dir', '/workspace/scripts/soutputs/059bf721-cca5-4d02-9832-a794cf37074b', '--num_train_epochs', '3', '--per_device_train_batch_size', '1', '--per_device_eval_batch_size', '1', '--gradient_accumulation_steps', '1', '--eval_accumulation_steps', '1', '--eval_strategy', 'no', '--save_strategy', 'epoch', '--logging_steps', '1', '--learning_rate', '1.8790606746021028e-05', '--weight_decay', '0.', '--warmup_steps', '200', '--lr_scheduler_type', 'cosine_with_min_lr', '--lr_scheduler_kwargs', '{"min_lr_rate": 0.25}', '--tf32', 'True', '--gradient_checkpointing', 'True', '--optim', 'paged_adamw_8bit', '--use_liger', 'True', '--packing', 'True', '--disable_fa', 'False', '--dataloader_pin_memory', 'True', '--deepspeed', 'ds_config/zero2.json', '--use_lora', 'True']
[text-trainer] [2026-09-16 22:35:24,891] [INFO] [launch.py:272:main] process 851 spawned with command: ['/usr/bin/python', '-u', 'train_instruct.py', '--local_rank=3', '--request_path', 'datasets/training_request_059bf721-cca5-4d02-9832-a794cf37074b.json', '--bf16', 'True', '--report_to', 'wandb', '--output_dir', '/workspace/scripts/soutputs/059bf721-cca5-4d02-9832-a794cf37074b', '--num_train_epochs', '3', '--per_device_train_batch_size', '1', '--per_device_eval_batch_size', '1', '--gradient_accumulation_steps', '1', '--eval_accumulation_steps', '1', '--eval_strategy', 'no', '--save_strategy', 'epoch', '--logging_steps', '1', '--learning_rate', '1.8790606746021028e-05', '--weight_decay', '0.', '--warmup_steps', '200', '--lr_scheduler_type', 'cosine_with_min_lr', '--lr_scheduler_kwargs', '{"min_lr_rate": 0.25}', '--tf32', 'True', '--gradient_checkpointing', 'True', '--optim', 'paged_adamw_8bit', '--use_liger', 'True', '--packing', 'True', '--disable_fa', 'False', '--dataloader_pin_memory', 'True', '--deepspeed', 'ds_config/zero2.json', '--use_lora', 'True']
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] [W916 22:35:33.114218053 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W916 22:35:34.141934212 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W916 22:35:34.142325818 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W916 22:35:34.168163943 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W916 22:35:34.168448677 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W916 22:35:34.184037381 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W916 22:35:34.184250412 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W916 22:35:34.753869563 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W916 22:35:34.765252347 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] wandb: Tracking run with wandb version 0.19.10
[text-trainer] wandb: W&B syncing is set to `offline` in this directory. Run `wandb online` or set WANDB_MODE=online to enable cloud syncing.