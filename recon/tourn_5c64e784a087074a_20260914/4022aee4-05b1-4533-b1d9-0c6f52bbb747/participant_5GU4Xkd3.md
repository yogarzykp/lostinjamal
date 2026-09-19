# Loki — task 4022aee4-05b1-4533-b1d9-0c6f52bbb747 — hotkey 5GU4Xkd3dCGTU3s8VLcHGc5wsD5M8XyxDca5yDQhYm1mVXFu
fetched 2026-09-19T05:05:10+00:00  lines=3910  hit_page_cap=False  containers=['downloader-4022aee4-05b1-4533-b1d9-0c6f52bbb747-34d845d3', 'downloader-4022aee4-05b1-4533-b1d9-0c6f52bbb747-a444933b', 'downloader-4022aee4-05b1-4533-b1d9-0c6f52bbb747-e1dae3d8', 'fastapi', 'hf-upload-7809eb525ae74f32be76a70d6cb0a1eb', 'text-trainer-2906c63e741046188b0230b08ee4a373', 'text-trainer-3b81f3ed7e7b4a8c952ab6732698fb0a', 'text-trainer-56629ca6ba134ce1b388c23c8cb11b31']

[downloader-4] Downloading datasets to: /cache/datasets
[downloader-4] Downloading models to: /cache/models
[downloader-4] Model already cached at /cache/models/68b85f2f8133b4d3.
[downloader-4] Skipping download.
[downloader-4] Model path: /cache/models/68b85f2f8133b4d3
[downloader-4] Dataset path: /cache/datasets
[downloader-4] Downloading datasets to: /cache/datasets
[downloader-4] Downloading models to: /cache/models
[downloader-4] /usr/local/lib/python3.10/site-packages/huggingface_hub/utils/_validators.py:205: UserWarning: The `local_dir_use_symlinks` argument is deprecated and ignored in `snapshot_download`. Downloading to a local directory does not use symlinks anymore.
[downloader-4]   warnings.warn(
[downloader-4] Model path: /cache/models/68b85f2f8133b4d3
[downloader-4] Dataset path: /cache/datasets
[downloader-4] Downloading datasets to: /cache/datasets
[downloader-4] Downloading models to: /cache/models
[downloader-4] Model already cached at /cache/models/68b85f2f8133b4d3.
[downloader-4] Skipping download.
[downloader-4] Model path: /cache/models/68b85f2f8133b4d3
[downloader-4] Dataset path: /cache/datasets
[fastapi] Repository cloned successfully
[fastapi] Running Cache Download Container
[fastapi] Starting downloader container: downloader-4022aee4-05b1-4533-b1d9-0c6f52bbb747-a444933b
[fastapi] Download completed successfully for task 4022aee4-05b1-4533-b1d9-0c6f52bbb747
[fastapi] Building Docker image 'standalone-text-trainer:80cd203a-46b4-4ac8-9e55-8a7a3f7b8dc5' (timeout=3600s)...
[fastapi] Step 1/13 : FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04
[fastapi] ---> ff5fe688608b
[fastapi] Step 2/13 : RUN apt-get update && apt-get install -y     vim     zip     tmux     iotop     nvtop     bmon     wget     nano     zsh     htop     && rm -rf /var/lib/apt/lists/*
[fastapi] ---> Running in 74d3bbeaec05
[fastapi] Get:1 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  InRelease [1578 B]
[fastapi] Get:2 http://archive.ubuntu.com/ubuntu jammy InRelease [270 kB]
[fastapi] Get:3 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  Packages [3011 kB]
[fastapi] Get:4 http://security.ubuntu.com/ubuntu jammy-security InRelease [129 kB]
[fastapi] Get:5 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy InRelease [18.1 kB]
[fastapi] Get:6 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [128 kB]
[fastapi] Get:7 http://archive.ubuntu.com/ubuntu jammy-backports InRelease [127 kB]
[fastapi] Get:8 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy/main amd64 Packages [44.3 kB]
[fastapi] Get:9 http://archive.ubuntu.com/ubuntu jammy/universe amd64 Packages [17.5 MB]
[fastapi] Get:10 http://security.ubuntu.com/ubuntu jammy-security/universe amd64 Packages [1317 kB]
[fastapi] Get:11 http://security.ubuntu.com/ubuntu jammy-security/restricted amd64 Packages [7717 kB]
[fastapi] Get:12 http://security.ubuntu.com/ubuntu jammy-security/main amd64 Packages [4290 kB]
[fastapi] Get:13 http://archive.ubuntu.com/ubuntu jammy/multiverse amd64 Packages [266 kB]
[fastapi] Get:14 http://archive.ubuntu.com/ubuntu jammy/restricted amd64 Packages [164 kB]
[fastapi] Get:15 http://archive.ubuntu.com/ubuntu jammy/main amd64 Packages [1792 kB]
[fastapi] Get:16 http://security.ubuntu.com/ubuntu jammy-security/multiverse amd64 Packages [84.6 kB]
[fastapi] Get:17 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 Packages [4624 kB]
[fastapi] Get:18 http://archive.ubuntu.com/ubuntu jammy-updates/multiverse amd64 Packages [93.2 kB]
[fastapi] Get:19 http://archive.ubuntu.com/ubuntu jammy-updates/restricted amd64 Packages [8007 kB]
[fastapi] Get:20 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 Packages [1620 kB]
[fastapi] Get:21 http://archive.ubuntu.com/ubuntu jammy-backports/universe amd64 Packages [35.6 kB]
[fastapi] Get:22 http://archive.ubuntu.com/ubuntu jammy-backports/main amd64 Packages [82.8 kB]
[fastapi] Fetched 51.3 MB in 19s (2675 kB/s)
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
[fastapi] 5 upgraded, 24 newly installed, 0 to remove and 170 not upgraded.
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
[fastapi] [0mFetched 23.1 MB in 7s (3489 kB/s)
[fastapi] (Reading database ... (Reading database ... 5%(Reading database ... 10%(Reading database ... 15%(Reading database ... 20%(Reading database ... 25%(Reading database ... 30%(Reading database ... 35%(Reading database ... 40%(Reading database ... 45%(Reading database ... 50%(Reading database ... 55%(Reading database ... 60%(Reading database ... 65%(Reading database ... 70%(Reading database ... 75%(Reading database ... 80%(Reading database ... 85%(Reading database ... 90%(Reading database ... 95%(Reading database ... 100%(Reading database ... 24135 files and directories currently installed.)
[fastapi] Preparing to unpack .../00-python3.10_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking python3.10 (3.10.12-1~22.04.18) over (3.10.12-1~22.04.6) ...
[fastapi] Preparing to unpack .../01-libpython3.10-stdlib_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking libpython3.10-stdlib:amd64 (3.10.12-1~22.04.18) over (3.10.12-1~22.04.6) ...
[fastapi] Preparing to unpack .../02-python3.10-minimal_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking python3.10-minimal (3.10.12-1~22.04.18) over (3.10.12-1~22.04.6) ...
[fastapi] Preparing to unpack .../03-libpython3.10-minimal_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking libpython3.10-minimal:amd64 (3.10.12-1~22.04.18) over (3.10.12-1~22.04.6) ...
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
[fastapi] Processing triggers for libc-bin (2.35-0ubuntu3.8) ...
[fastapi] ---> d1d30e3c0ffd
[fastapi] Step 3/13 : RUN mkdir -p /workspace
[fastapi] ---> Running in 1704eb0320d9
[fastapi] ---> b9a4757026d7
[fastapi] Step 4/13 : RUN mkdir -p /cache
[fastapi] ---> Running in e0f391f14d53
[fastapi] ---> d996cd546157
[fastapi] Step 5/13 : RUN mkdir -p /workspace/scripts/datasets
[fastapi] ---> Running in 7ce28aa8137b
[fastapi] ---> b8c00f60a810
[fastapi] Step 6/13 : RUN mkdir -p /app/checkpoints
[fastapi] ---> Running in 40ff1fc9db7f
[fastapi] ---> a9fe55fbaab1
[fastapi] Step 7/13 : WORKDIR /workspace/scripts
[fastapi] ---> Running in 87f35565692f
[fastapi] ---> 40b7a01a52ca
[fastapi] Step 8/13 : COPY scripts /workspace/scripts
[fastapi] ---> 85b5256f4906
[fastapi] Step 9/13 : RUN chmod +x /workspace/scripts/entrypoint.sh
[fastapi] ---> Running in f5d22f670795
[fastapi] ---> ab14de17f504
[fastapi] Step 10/13 : RUN python -m venv /workspace/axo_py
[fastapi] ---> Running in 9b72c5330e92
[fastapi] ---> 24ef2054a9ef
[fastapi] Step 11/13 : RUN bash -c "source /workspace/axo_py/bin/activate &&     pip install uv &&     pip install -U packaging==23.2 setuptools==75.8.0 wheel ninja &&     uv pip install --no-build-isolation axolotl==0.9.1 &&     pip install requests==2.32.3 &&     deactivate"
[fastapi] ---> Running in d89b56e12c74
[fastapi] Collecting uv
[fastapi] Downloading uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] Downloading uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.1 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 20.1/20.1 MB 35.5 MB/s eta 0:00:00
[fastapi] Installing collected packages: uv
[fastapi] Successfully installed uv-0.12.15
[fastapi] [91m
[fastapi] [notice] A new release of pip is available: 24.0 -> 26.2.1
[fastapi] [notice] To update, run: pip install --upgrade pip
[fastapi] [0mCollecting packaging==23.2
[fastapi] Downloading packaging-23.2-py3-none-any.whl.metadata (3.2 kB)
[fastapi] Collecting setuptools==75.8.0
[fastapi] Downloading setuptools-75.8.0-py3-none-any.whl.metadata (6.7 kB)
[fastapi] Collecting wheel
[fastapi] Downloading wheel-0.48.0-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Collecting ninja
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (5.4 kB)
[fastapi] INFO: pip is looking at multiple versions of wheel to determine which version is compatible with other requirements. This could take a while.
[fastapi] Collecting wheel
[fastapi] Downloading wheel-0.47.0-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Downloading wheel-0.46.3-py3-none-any.whl.metadata (2.4 kB)
[fastapi] Downloading wheel-0.46.2-py3-none-any.whl.metadata (2.4 kB)
[fastapi] Downloading wheel-0.45.1-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Downloading packaging-23.2-py3-none-any.whl (53 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 53.0/53.0 kB 3.2 MB/s eta 0:00:00
[fastapi] Downloading setuptools-75.8.0-py3-none-any.whl (1.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 25.4 MB/s eta 0:00:00
[fastapi] Downloading wheel-0.45.1-py3-none-any.whl (72 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 72.5/72.5 kB 4.2 MB/s eta 0:00:00
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (183 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 183.4/183.4 kB 12.8 MB/s eta 0:00:00
[fastapi] Installing collected packages: wheel, setuptools, packaging, ninja
[fastapi] Attempting uninstall: setuptools
[fastapi] Found existing installation: setuptools 65.5.0
[fastapi] Uninstalling setuptools-65.5.0:
[fastapi] Successfully uninstalled setuptools-65.5.0
[fastapi] Successfully installed ninja-1.13.2 packaging-23.2 setuptools-75.8.0 wheel-0.45.1
[fastapi] [91m
[fastapi] [notice] A new release of pip is available: 24.0 -> 26.2.1
[fastapi] [notice] To update, run: pip install --upgrade pip
[fastapi] [0m[91mUsing Python 3.11.10 environment at: /workspace/axo_py
[fastapi] [0m[91mResolved 217 packages in 2.78s
[fastapi] [0m[91m   Building axolotl-contribs-mit==0.0.3
[fastapi] [0m[91mDownloading wandb (24.9MiB)
[fastapi] [0m[91mDownloading cryptography (4.5MiB)
[fastapi] [0m[91mDownloading tensorboard (5.3MiB)
[fastapi] [0m[91mDownloading oci (35.2MiB)
[fastapi] [0m[91mDownloading numpy (18.6MiB)
[fastapi] [0m[91mDownloading sympy (5.9MiB)
[fastapi] [0m[91mDownloading nvidia-cudnn-cu12 (634.0MiB)
[fastapi] [0m[91mDownloading llvmlite (57.1MiB)
[fastapi] [0m[91mDownloading hf-xet (51.1MiB)
[fastapi] [0m[91mDownloading nvidia-cusolver-cu12 (122.0MiB)
[fastapi] [0m[91mDownloading grpcio (6.9MiB)
[fastapi] [0m[91mDownloading nvidia-cusparselt-cu12 (143.1MiB)
[fastapi] [0m[91mDownloading nvidia-cufft-cu12 (201.7MiB)
[fastapi] [0m[91mDownloading zstandard (5.2MiB)
[fastapi] [0m[91mDownloading torch (731.2MiB)
[fastapi] [0m[91mDownloading xformers (42.2MiB)
[fastapi] [0m[91mDownloading ruff (9.9MiB)
[fastapi] [0m[91mDownloading torchao (5.4MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-cupti-cu12 (13.2MiB)
[fastapi] [0m[91mDownloading lxml (5.0MiB)
[fastapi] [0m[91mDownloading pillow (6.3MiB)
[fastapi] [0m[91mDownloading tensorboard-data-server (6.3MiB)
[fastapi] [0m[91mDownloading pyarrow (47.7MiB)
[fastapi] [0m[91mDownloading scikit-learn (11.6MiB)
[fastapi] [0m[91mDownloading nvidia-curand-cu12 (53.7MiB)
[fastapi] [0m[91mDownloading hf-transfer (3.4MiB)
[fastapi] [0m[91mDownloading bitsandbytes (72.5MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-nvrtc-cu12 (23.5MiB)
[fastapi] [0m[91mDownloading nvidia-cusparse-cu12 (197.8MiB)
[fastapi] [0m[91mDownloading gradio (44.3MiB)
[fastapi] [0m[91mDownloading tokenizers (3.0MiB)
[fastapi] [0m[91mDownloading nvidia-cublas-cu12 (346.6MiB)
[fastapi] [0m[91mDownloading triton (241.4MiB)
[fastapi] [0m[91mDownloading numba (3.6MiB)
[fastapi] [0m[91mDownloading pandas (12.2MiB)
[fastapi] [0m[91mDownloading nvidia-nvjitlink-cu12 (20.1MiB)
[fastapi] [0m[91mDownloading transformers (9.9MiB)
[fastapi] [0m[91mDownloading botocore (13.7MiB)
[fastapi] [0m[91mDownloading scipy (33.7MiB)
[fastapi] [0m[91mDownloading nvidia-nccl-cu12 (179.9MiB)
[fastapi] [0m[91mDownloading lm-eval (2.4MiB)
[fastapi] [0m[91mDownloading networkx (2.0MiB)
[fastapi] [0m[91mDownloading nltk (1.7MiB)
[fastapi] [0m[91mDownloading pydantic-core (1.9MiB)
[fastapi] [0m[91mDownloading aiohttp (1.7MiB)
[fastapi] [0m[91mDownloading sentencepiece (1.3MiB)
[fastapi] [0m[91mDownloading pygments (1.2MiB)
[fastapi] [0m[91m      Built axolotl-contribs-mit==0.0.3
[fastapi] [0m[91m   Building langdetect==1.0.9
[fastapi] [0m[91m Downloaded pygments
[fastapi] [0m[91m Downloaded sentencepiece
[fastapi] [0m[91m Downloaded nltk
[fastapi] [0m[91m Downloaded aiohttp
[fastapi] [0m[91m      Built langdetect==1.0.9
[fastapi] [0m[91m Downloaded pydantic-core
[fastapi] [0m[91m Downloaded networkx
[fastapi] [0m[91m   Building axolotl==0.9.1
[fastapi] [0m[91m Downloaded lm-eval
[fastapi] [0m[91m   Building word2number==1.1
[fastapi] [0m[91m   Building axolotl-contribs-lgpl==0.0.6
[fastapi] [0m[91m   Building rouge-score==0.1.2
[fastapi] [0m[91m   Building sqlitedict==2.1.0
[fastapi] [0m[91m      Built axolotl==0.9.1
[fastapi] [0m[91m Downloaded tokenizers
[fastapi] [0m[91m      Built word2number==1.1
[fastapi] [0m[91m   Building grpclib==0.4.7
[fastapi] [0m[91m   Building hqq==0.2.5
[fastapi] [0m[91m      Built axolotl-contribs-lgpl==0.0.6
[fastapi] [0m[91m      Built rouge-score==0.1.2
[fastapi] [0m[91m      Built sqlitedict==2.1.0
[fastapi] [0m[91m Downloaded hf-transfer
[fastapi] [0m[91m      Built grpclib==0.4.7
[fastapi] [0m[91m Downloaded numba
[fastapi] [0m[91m      Built hqq==0.2.5
[fastapi] [0m[91m Downloaded cryptography
[fastapi] [0m[91m Downloaded lxml
[fastapi] [0m[91m Downloaded zstandard
[fastapi] [0m[91m Downloaded torchao
[fastapi] [0m[91m Downloaded tensorboard
[fastapi] [0m[91m Downloaded sympy
[fastapi] [0m[91m Downloaded tensorboard-data-server
[fastapi] [0m[91m Downloaded pillow
[fastapi] [0m[91m Downloaded grpcio
[fastapi] [0m[91m Downloaded ruff
[fastapi] [0m[91m Downloaded transformers
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
[fastapi] [0m[91mPrepared 215 packages in 1m 09s
[fastapi] [0m[91mInstalled 215 packages in 1.45s
[fastapi] + absl-py==2.5.0
[fastapi] + accelerate==1.6.0
[fastapi] + addict==2.4.0
[fastapi] + adlfs==2026.8.0
[fastapi] + aiobotocore==2.26.0
[fastapi] + aiofiles==23.2.1
[fastapi] +[0m[91m aiohappyeyeballs==2.7.1
[fastapi] + aiohttp==3.14.3
[fastapi] + aioitertools==0.13.0
[fastapi] + aiosignal==1.4.0
[fastapi] + annotated-doc==0.0.5
[fastapi] + annotated-types==0.8.0[0m[91m
[fastapi] + antlr4-python3-runtime==4.13.2
[fastapi] + [0m[91manyio==4.15.1
[fastapi] + art==6.5
[fastapi] + attrs==26.1.0
[fastapi] + autoawq==0.2.7.post3
[fastapi] + axolotl==0.9.1
[fastapi] + axolotl-contribs-lgpl==0.0.6
[fastapi] + axolotl-contribs-mit==0.0.3
[fastapi] + azure-core==1.41.0
[fastapi] + azure-identity==1.25.3
[fastapi] + azure-storage-blob==12.30.1
[fastapi] + bitsandbytes==0.45.4
[fastapi] + botocore==1.41.5
[fastapi] + certifi==2026.7.22
[fastapi] + cffi==2[0m[91m.1.1
[fastapi] + chardet==6.0.0.post1
[fastapi] + charset-normalizer==3.5.1
[fastapi] + circuitbreaker==2.1[0m[91m.3
[fastapi] + click==8[0m[91m.5.0
[fastapi] +[0m[91m cloudpickle==3.[0m[91m1.2
[fastapi] [0m[91m+ colorama==0[0m[91m.4.6
[fastapi] + [0m[91mcoloredlogs==15.0.1
[fastapi] [0m[91m+ crc32c==2.8
[fastapi] [0m[91m+ cryptography==50.[0m[91m0.1
[fastapi] + [0m[91mdataproperty==1.1.1
[fastapi] +[0m[91m datasets==3.5.1
[fastapi] + decorator==5.3.1
[fastapi] + defusedxml==[0m[91m0.7.1
[fastapi] + dill[0m[91m==0.3.8
[fastapi] [0m[91m+ einops==0.[0m[91m8.2[0m[91m
[fastapi] [0m[91m+ [0m[91mevaluate==[0m[91m0.[0m[91m4.1
[fastapi] [0m[91m +[0m[91m [0m[91mfastapi==0.[0m[91m141.1
[fastapi] +[0m[91m fastcore==2[0m[91m.2.28
[fastapi] [0m[91m+ ffmpy[0m[91m==1.0.0
[fastapi] [0m[91m + filelock[0m[91m==3.32.6[0m[91m
[fastapi] + fire[0m[91m==0.7.1
[fastapi] [0m[91m+ frozenlist==[0m[91m1.8.0
[fastapi] [0m[91m + fsspec[0m[91m==2025.3.0[0m[91m
[fastapi] + gcsfs[0m[91m==2025.3.0
[fastapi] [0m[91m+ google-api-core==2.33.[0m[91m0
[fastapi] + google-auth==2.58.0
[fastapi] + google-auth-oauthlib==1.4.1
[fastapi] + [0m[91mgoogle-cloud-core==2.7.0
[fastapi] + google-cloud-storage==3.14.1
[fastapi] + google-crc32c==1.8.0
[fastapi] + google-resumable-media==2.10.2
[fastapi] + googleapis-common-protos==1.75.0
[fastapi] + gradio==5.23.3
[fastapi] + gradio-client==1.8.0
[fastapi] + groovy==0.1.2
[fastapi] + grpcio==1.84.0
[fastapi] + grpclib==0.4.7
[fastapi] + h11==0.16.0
[fastapi] + h2==4.4.1
[fastapi] + hf-transfer==0.1.9
[fastapi] + hf-xet==1.1.0
[fastapi] + hpack==4.2.0
[fastapi] + hqq==0.2.5
[fastapi] + httpcore==1.0.9
[fastapi] + httpx==0.28.1
[fastapi] +[0m[91m huggingface-hub==0.31.0
[fastapi] + humanfriendly==10.0[0m[91m
[fastapi] + hyperframe==6.1.0
[fastapi] + idna==3.19
[fastapi] + immutabledict==[0m[91m4.2.0
[fastapi] + isodate==0.7.[0m[91m2
[fastapi] + jinja2[0m[91m==3.1.6
[fastapi] + jmespath==1.1.0
[fastapi] [0m[91m+ joblib==1.6.0
[fastapi] [0m[91m + jsonlines==4.0.0
[fastapi] + langdetect==1.0.9
[fastapi] + liger-kernel==0.5.9
[fastapi] + llvmlite==0.49.0
[fastapi] + lm-eval==0.4.7
[fastapi] + lxml==6.1.3
[fastapi] + markdown==3.10.3
[fastapi] + markdown-it-py==4.2.0
[fastapi] + markupsafe==3.0.3
[fastapi] + mbstrdecoder==1.1.5
[fastapi] + mdurl==0.1.2
[fastapi] + modal==0.70.5
[fastapi] + more-itertools==11.1.0
[fastapi] + mpmath==1[0m[91m.3.0
[fastapi] + msal==1.38.0
[fastapi] [0m[91m+ [0m[91mmsal-extensions==1.3.1
[fastapi] + multidict==6.8.0
[fastapi] + multiprocess[0m[91m==0.70.16
[fastapi] [0m[91m + networkx==3.6.1
[fastapi] [0m[91m+ nltk==3.10.3
[fastapi] + numba==0.67.0
[fastapi] + numexpr==2.14.2
[fastapi] + numpy==2.0.1
[fastapi] +[0m[91m nvidia-cublas-cu12==12.4.5.8
[fastapi] + nvidia-cuda-cupti-cu12==12.4.127
[fastapi] + nvidia-cuda-nvrtc-cu12==12.4.127
[fastapi] + nvidia-cuda-runtime-cu12==12.4.127
[fastapi] + nvidia-cudnn-cu12==9.1.0.70
[fastapi] + nvidia-cufft-cu12==11.2.1.3
[fastapi] + nvidia-curand-cu12==10.3.5.147
[fastapi] + nvidia-cusolver-cu12==11.6.1.9
[fastapi] + nvidia-cusparse-cu12==12.3.1.170
[fastapi] + nvidia-cusparselt-cu12==0.6.2
[fastapi] + nvidia-ml-py==12.560.30
[fastapi] + nvidia-nccl-cu12==2.21.5
[fastapi] + nvidia-nvjitlink-cu12==12.4.127
[fastapi] + nvidia-nvtx-cu12==12.4.127
[fastapi] + oauthlib==3[0m[91m.3.1
[fastapi] + oci==2.186.0[0m[91m
[fastapi] + ocifs[0m[91m==1.3.2
[fastapi] [0m[91m+ opentelemetry-api==[0m[91m1.44.0
[fastapi] [0m[91m+ opentelemetry-exporter-otlp-proto-common==1[0m[91m.44.0
[fastapi] +[0m[91m opentelemetry-exporter-otlp-proto-http==1.44.[0m[91m0
[fastapi] [0m[91m+ opentelemetry-proto==1.44.0
[fastapi] + opentelemetry-sdk==1.44.0
[fastapi] + opentelemetry-semantic-conventions==0.65b0
[fastapi] + optimum==1.16.2
[fastapi] + orjson==3.12.0
[fastapi] + pandas==2.3.3
[fastapi] + pathvalidate==3.3.1
[fastapi] + peft==0.15.2
[fastapi] +[0m[91m pillow==11.3.0
[fastapi] + [0m[91mplatformdirs==4.11.8
[fastapi] + portalocker==4.3.2
[fastapi] + propcache==0.5.3
[fastapi] + proto-plus==1[0m[91m.28.2
[fastapi] + protobuf==5.29.6
[fastapi] [0m[91m + psutil==7.2.2
[fastapi] [0m[91m+ pyarrow==25.0.1[0m[91m
[fastapi] + pyasn1==0.6[0m[91m.4
[fastapi] + pyasn1-modules==0.4[0m[91m.2
[fastapi] + pybind11==[0m[91m3.1.0
[fastapi] [0m[91m + [0m[91mpycparser==3.0
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
[fastapi] + [0m[91mrouge-score==0.1.2
[fastapi] + ruff[0m[91m==0.16.7
[fastapi] + [0m[91ms3fs==2025.3.0
[fastapi] + sacrebleu==2.6.0
[fastapi] +[0m[91m safehttpx==[0m[91m0.1.[0m[91m7
[fastapi] +[0m[91m safetensors==0.[0m[91m8.0
[fastapi] + schedulefree==1.4.1
[fastapi] + scikit-learn==1.4.2
[fastapi] + scipy==1.17.1
[fastapi] + semantic-version==2.10.0
[fastapi] + sentencepiece==0.[0m[91m2.2
[fastapi] + shellingham[0m[91m==1.5.4
[fastapi] [0m[91m+ sigtools==4.0.[0m[91m1
[fastapi] + six==1.17.0
[fastapi] + sqlitedict==2.1.0
[fastapi] + [0m[91mstarlette==0.52.1[0m[91m
[fastapi] + sympy[0m[91m==1.13.1
[fastapi] [0m[91m+ synchronicity==0.9.16
[fastapi] [0m[91m + tabledata==1.3.[0m[91m5
[fastapi] + tabulate==0.10[0m[91m.0
[fastapi] + tcolorpy==[0m[91m0.1[0m[91m.7
[fastapi] +[0m[91m tensorboard==2.20.0[0m[91m
[fastapi] [0m[91m+ tensorboard-data-server==[0m[91m0.7.2[0m[91m
[fastapi] + termcolor==[0m[91m3.3.0
[fastapi] + threadpoolctl==3[0m[91m.7.0
[fastapi] + tokenizers==[0m[91m0.21.4
[fastapi] + toml[0m[91m==0.10.2
[fastapi] + tomlkit[0m[91m==0.13.3
[fastapi] + torch[0m[91m==2.[0m[91m6.0
[fastapi] + torchao==0.9[0m[91m.0
[fastapi] + tqdm[0m[91m==4.70.1
[fastapi] +[0m[91m tqdm-multiprocess==0.0.11
[fastapi] [0m[91m + transformers==4.51.3[0m[91m
[fastapi] + triton==[0m[91m3.2.0
[fastapi] + [0m[91mtrl==0.17.0
[fastapi] + [0m[91mtypepy==1.3.5
[fastapi] [0m[91m + typer==0.27.2
[fastapi] + types-certifi[0m[91m==2021.10.8.3
[fastapi] + types-toml==0.10.8.20260518
[fastapi] + typing-extensions==4.16.0
[fastapi] + typing-inspection==0.4.4
[fastapi] + tzdata==2026.4
[fastapi] + urllib3==2.8.0
[fastapi] + uvicorn==0.53.0
[fastapi] + wandb==0.30.0
[fastapi] + watchfiles==1.2.0
[fastapi] + websockets==15.0.1
[fastapi] + werkzeug==3.1.8
[fastapi] + word2number==1.1
[fastapi] + wrapt==1.17.3
[fastapi] + xformers==0[0m[91m.0.29.post2
[fastapi] + xxhash[0m[91m==4.0.1
[fastapi] + yarl==1.25.1
[fastapi] + zstandard[0m[91m==0.22.0
[fastapi] [0mCollecting requests==2.32.3
[fastapi] Downloading requests-2.32.3-py3-none-any.whl.metadata (4.6 kB)
[fastapi] Requirement already satisfied: charset-normalizer<4,>=2 in /workspace/axo_py/lib/python3.11/site-packages (from requests==2.32.3) (3.5.1)
[fastapi] Requirement already satisfied: idna<4,>=2.5 in /workspace/axo_py/lib/python3.11/site-packages (from requests==2.32.3) (3.19)
[fastapi] Requirement already satisfied: urllib3<3,>=1.21.1 in /workspace/axo_py/lib/python3.11/site-packages (from requests==2.32.3) (2.8.0)
[fastapi] Requirement already satisfied: certifi>=2017.4.17 in /workspace/axo_py/lib/python3.11/site-packages (from requests==2.32.3) (2026.7.22)
[fastapi] Downloading requests-2.32.3-py3-none-any.whl (64 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 64.9/64.9 kB 2.1 MB/s eta 0:00:00
[fastapi] Installing collected packages: requests
[fastapi] Attempting uninstall: requests
[fastapi] Found existing installation: requests 2.34.2
[fastapi] Uninstalling requests-2.34.2:
[fastapi] Successfully uninstalled requests-2.34.2
[fastapi] [91mERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
[fastapi] google-api-core 2.33.0 requires requests<3.0.0,>=2.33.0, but you have requests 2.32.3 which is incompatible.
[fastapi] [0mSuccessfully installed requests-2.32.3
[fastapi] [91m
[fastapi] [notice] A new release of pip is available: 24.0 -> 26.2.1
[fastapi] [notice] To update, run: pip install --upgrade pip
[fastapi] [0m ---> dc89668149fe
[fastapi] Step 12/13 : RUN pip install uv &&     pip install -U packaging==23.2 setuptools==75.8.0 wheel ninja &&     uv pip install -r /workspace/scripts/training_requirements.txt --system &&     pip install hf_transfer==0.1.9 &&     pip install tenacity==9.1.2 &&     pip install tiktoken==0.9.0 &&     pip install flash-attn==v2.7.4.post1 --no-build-isolation &&     uv pip install vllm==0.8.3 --system &&     pip install "fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0"
[fastapi] ---> Running in ac833d74e679
[fastapi] Collecting uv
[fastapi] Using cached uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] Using cached uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.1 MB)
[fastapi] Installing collected packages: uv
[fastapi] Successfully installed uv-0.12.15
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0mCollecting packaging==23.2
[fastapi] Using cached packaging-23.2-py3-none-any.whl.metadata (3.2 kB)
[fastapi] Collecting setuptools==75.8.0
[fastapi] Using cached setuptools-75.8.0-py3-none-any.whl.metadata (6.7 kB)
[fastapi] Requirement already satisfied: wheel in /usr/local/lib/python3.11/dist-packages (0.44.0)
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
[fastapi] Attempting uninstall: wheel
[fastapi] Found existing installation: wheel 0.44.0
[fastapi] Uninstalling wheel-0.44.0:
[fastapi] Successfully uninstalled wheel-0.44.0
[fastapi] Attempting uninstall: setuptools
[fastapi] Found existing installation: setuptools 75.1.0
[fastapi] Uninstalling setuptools-75.1.0:
[fastapi] Successfully uninstalled setuptools-75.1.0
[fastapi] Attempting uninstall: packaging
[fastapi] Found existing installation: packaging 24.1
[fastapi] Uninstalling packaging-24.1:
[fastapi] Successfully uninstalled packaging-24.1
[fastapi] Successfully installed ninja-1.13.2 packaging-23.2 setuptools-75.8.0 wheel-0.45.1
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0m[91mUsing Python 3.11.10 environment at: /usr
[fastapi] [0m[91mResolved 187 packages in 3.36s
[fastapi] [0m[91m   Building deepspeed==0.15.4
[fastapi] [0m[91m   Building antlr4-python3-runtime==4.9.3
[fastapi] [0m[91mDownloading openai (1.9MiB)
[fastapi] [0m[91mDownloading dash (8.5MiB)
[fastapi] [0m[91mDownloading mpi4py (1.3MiB)
[fastapi] [0m[91mDownloading pydantic-core (2.0MiB)
[fastapi] [0m[91mDownloading plotly (9.2MiB)
[fastapi] [0m[91mDownloading sqlalchemy (3.3MiB)
[fastapi] [0m[91mDownloading mlflow-tracing (1.7MiB)
[fastapi] [0m[91mDownloading hf-xet (4.3MiB)
[fastapi] [0m[91mDownloading mlflow-skinny (3.5MiB)
[fastapi] [0m[91mDownloading scipy (35.9MiB)
[fastapi] [0m[91mDownloading kiwisolver (1.4MiB)
[fastapi] [0m[91mDownloading pyphen (2.0MiB)
[fastapi] [0m[91mDownloading tensorboard (5.2MiB)
[fastapi] [0m[91mDownloading wandb (20.4MiB)
[fastapi] [0m[91mDownloading sentencepiece (1.2MiB)
[fastapi] [0m[91mDownloading scikit-learn (8.9MiB)
[fastapi] [0m[91mDownloading mlflow (11.0MiB)
[fastapi] [0m[91mDownloading fonttools (5.2MiB)
[fastapi] [0m[91mDownloading pycryptodome (2.2MiB)
[fastapi] [0m[91mDownloading matplotlib (9.4MiB)
[fastapi] [0m[91mDownloading pandas (12.5MiB)
[fastapi] [0m[91m      Built antlr4-python3-runtime==4.9.3
[fastapi] [0m[91m Downloaded sentencepiece
[fastapi] [0m[91m Downloaded mpi4py
[fastapi] [0m[91m Downloaded kiwisolver
[fastapi] [0m[91m Downloaded mlflow-tracing
[fastapi] [0m[91m Downloaded pydantic-core
[fastapi] [0m[91m Downloaded openai
[fastapi] [0m[91m Downloaded pyphen
[fastapi] [0m[91m Downloaded pycryptodome
[fastapi] [0m[91m Downloaded sqlalchemy
[fastapi] [0m[91m      Built deepspeed==0.15.4
[fastapi] [0m[91m Downloaded mlflow-skinny
[fastapi] [0m[91m Downloaded hf-xet
[fastapi] [0m[91m Downloaded fonttools
[fastapi] [0m[91m Downloaded tensorboard
[fastapi] [0m[91m Downloaded dash
[fastapi] [0m[91m Downloaded scikit-learn
[fastapi] [0m[91m Downloaded plotly
[fastapi] [0m[91m Downloaded matplotlib
[fastapi] [0m[91m Downloaded mlflow
[fastapi] [0m[91m Downloaded pandas
[fastapi] [0m[91m Downloaded wandb
[fastapi] [0m[91m Downloaded scipy
[fastapi] [0m[91mPrepared 88 packages in 3.20s
[fastapi] [0m[91mUninstalled 6 packages in 231ms
[fastapi] [0m[91mInstalled 141 packages in 46.30s
[fastapi] [0m[91m + absl-py==2.5.0
[fastapi] + accelerate==1.6.0
[fastapi] + aiohappyeyeballs==2.7.1
[fastapi] + aiohttp==3.14.3
[fastapi] + aiosignal==1.4.0
[fastapi] + alembic==1.20.0
[fastapi] + annotated-doc==0.0.5
[fastapi] + annotated-types==0.8.0
[fastapi] [0m[91m+ antlr4-python3-runtime==4.9.3
[fastapi] - anyio==4.6.0
[fastapi] + anyio==[0m[91m4.15.1
[fastapi] + astor==0.8.1
[fastapi] + bitsandbytes==0.45.4
[fastapi] + blinker==1.9.0
[fastapi] + cachetools==7.1.8
[fastapi] - cffi==1.17.1
[fastapi] + cffi==2.1.1
[fastapi] + click==8.5.0
[fastapi] + cloudpickle==3.[0m[91m1.2
[fastapi] + cmudict==1.1.3
[fastapi] [0m[91m+ contourpy[0m[91m==1.3.3
[fastapi] + [0m[91mcryptography==50.0.1
[fastapi] + cycler==0.12.1
[fastapi] + dash==4.4.1
[fastapi] + databricks-sdk==0.139.0
[fastapi] + datasets==3.5.0
[fastapi] + deepspeed==0.15.4
[fastapi] + detoxify==0.5.2
[fastapi] + dill==0.3.8
[fastapi] + docker==7.[0m[91m2.0
[fastapi] + [0m[91mdocker-pycreds==0.4.0[0m[91m
[fastapi] + einops==0.8.1
[fastapi] + fastapi==0.141.1
[fastapi] + flask==3.1.3
[fastapi] + flask-cors==[0m[91m6.0.5
[fastapi] + fonttools==[0m[91m4.65.0
[fastapi] + frozenlist==1.8.0
[fastapi] + gdown==6.2.0
[fastapi] + gitdb==4.0.12
[fastapi] + gitpython==3.1.62
[fastapi] + google-auth==2.58.0
[fastapi] + graphene==3.4.[0m[91m3
[fastapi] [0m[91m+ graphql-core==3.2.12
[fastapi] + graphql-relay==3.2.0
[fastapi] + greenlet==3.5.6
[fastapi] + grpcio==1.84.0
[fastapi] +[0m[91m gunicorn==26.2.[0m[91m0
[fastapi] - h11==0.14.0
[fastapi] + h11==0.16.0
[fastapi] + hf-xet==1.6.0
[fastapi] + hjson[0m[91m==3.1[0m[91m.0
[fastapi] [0m[91m+[0m[91m [0m[91mhttpcore2==2.13.0
[fastapi] + httpx2==2.13.0
[fastapi] + huey==3.4.0
[fastapi] + huggingface-hub==0.36.2
[fastapi] [0m[91m - idna==3.10[0m[91m
[fastapi] + idna==3.19
[fastapi] + importlib-metadata==9.[0m[91m0.1
[fastapi] +[0m[91m [0m[91mimportlib-resources[0m[91m==7.1[0m[91m.0
[fastapi] [0m[91m + itsdangerous==2[0m[91m.2.0
[fastapi] [0m[91m + jaconv==0.5.0[0m[91m
[fastapi] [0m[91m+ janus[0m[91m==2.0.0
[fastapi] [0m[91m [0m[91m+ jiter[0m[91m==0.17.0[0m[91m
[fastapi] + joblib==1.6.0
[fastapi] + kiwisolver==1.5.1
[fastapi] + langcheck==0.9.0
[fastapi] + [0m[91mliger-kernel==0[0m[91m.5.9[0m[91m
[fastapi] +[0m[91m mako==1.[0m[91m4.1
[fastapi] + markdown==3.10.3
[fastapi] + matplotlib==3.11.2
[fastapi] + minio==7.2.20[0m[91m
[fastapi] + mlflow==3.[0m[91m16.0
[fastapi] + [0m[91mmlflow-skinny==3.16.0[0m[91m
[fastapi] + mlflow-tracing[0m[91m==3.16[0m[91m.0
[fastapi] + mpi4py[0m[91m==4.1.2
[fastapi] [0m[91m+ msgpack==1.2.2
[fastapi] + multidict==6.8.0
[fastapi] + multiprocess==0.70.16
[fastapi] + narwhals==2.26.0
[fastapi] + nlpaug==1.1.11
[fastapi] + nltk==[0m[91m3.10.3
[fastapi] [0m[91m+ omegaconf==[0m[91m2.3.1[0m[91m
[fastapi] + openai[0m[91m==3.14.[0m[91m0
[fastapi] [0m[91m+ opentelemetry-api[0m[91m==1.44.[0m[91m0
[fastapi] +[0m[91m opentelemetry-proto==1.44.0
[fastapi] + opentelemetry-sdk==1.44.0
[fastapi] + [0m[91mopentelemetry-semantic-conventions==0.65[0m[91mb0
[fastapi] + pandas[0m[91m==2.2.3
[fastapi] + peft==0.15.1
[fastapi] + plotly==7.1.0[0m[91m
[fastapi] + [0m[91mprettytable==3.18.[0m[91m0
[fastapi] +[0m[91m propcache==[0m[91m0.5.3[0m[91m
[fastapi] + [0m[91mprotobuf==6.[0m[91m33.6
[fastapi] [0m[91m+ py-cpuinfo==9.0.[0m[91m0
[fastapi] + pyarrow==25.0.1
[fastapi] + pyasn1==0.6.4
[fastapi] + pyasn1-modules==0.4.2
[fastapi] + pycryptodome==3.23.0
[fastapi] + pydantic[0m[91m==2.13.5
[fastapi] + pydantic-core==2.46.5
[fastapi] + pyparsing==3.3.2
[fastapi] + pyphen==0.18.1[0m[91m
[fastapi] + pysocks==1.7.1
[fastapi] + python-dotenv==1.2.3
[fastapi] + pytz==2026.3.post1
[fastapi] + regex==2026.[0m[91m9.10
[fastapi] [0m[91m+ restrictedpython==8.0[0m[91m
[fastapi] + retrying==1.4.2
[fastapi] + rouge-score==0.1.2
[fastapi] + safetensors==0.8.0
[fastapi] + scikit-learn[0m[91m==1.9.1
[fastapi] +[0m[91m scipy[0m[91m==1[0m[91m.15.2[0m[91m
[fastapi] + sentence-transformers[0m[91m==5.[0m[91m7.0
[fastapi] [0m[91m+ sentencepiece==0.2[0m[91m.0
[fastapi] + sentry-sdk==2.69.2
[fastapi] + setproctitle==1.3.7
[fastapi] + six==1.17.0
[fastapi] + skops==0.14.[0m[91m0
[fastapi] + [0m[91msmmap[0m[91m==5.0.3
[fastapi] + sqlalchemy==2.0.53
[fastapi] + sqlparse==0.6.0
[fastapi] + starlette==1.6.0
[fastapi] + tabulate==0.10.0
[fastapi] + tenacity==9.1.4
[fastapi] + tensorboard==2.19.0
[fastapi] + tensorboard-data-server==0[0m[91m.7.2
[fastapi] + textstat==0.7.8
[fastapi] + threadpoolctl==3.7.0
[fastapi] + tokenizers[0m[91m==0.21.4
[fastapi] + toml==0.10.2
[fastapi] + tqdm==4.70.1
[fastapi] + transformers==4.51.3
[fastapi] + trl==0.18.0
[fastapi] + [0m[91mtruststore==0.10.4
[fastapi] + typer==0.9.0
[fastapi] - typing-extensions==4.9.0
[fastapi] + typing-extensions==4.16.0
[fastapi] + typing-inspection==0.4[0m[91m.4
[fastapi] + tzdata==2026.4
[fastapi] + [0m[91muvicorn==0.53.0
[fastapi] + wandb==0.19.10
[fastapi] - wcwidth==0.2.13
[fastapi] + wcwidth==0.8.3
[fastapi] + werkzeug==3.1.8
[fastapi] + xxhash==4.0[0m[91m.1
[fastapi] + yarl[0m[91m==1.25[0m[91m.1
[fastapi] + [0m[91mzipp==4.1.0[0m[91m
[fastapi] [0mCollecting hf_transfer==0.1.9
[fastapi] Downloading hf_transfer-0.1.9-cp38-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (1.7 kB)
[fastapi] Downloading hf_transfer-0.1.9-cp38-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.6 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.6/3.6 MB 27.4 MB/s eta 0:00:00
[fastapi] Installing collected packages: hf_transfer
[fastapi] Successfully installed hf_transfer-0.1.9
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0mCollecting tenacity==9.1.2
[fastapi] Downloading tenacity-9.1.2-py3-none-any.whl.metadata (1.2 kB)
[fastapi] Downloading tenacity-9.1.2-py3-none-any.whl (28 kB)
[fastapi] Installing collected packages: tenacity
[fastapi] Attempting uninstall: tenacity
[fastapi] Found existing installation: tenacity 9.1.4
[fastapi] Uninstalling tenacity-9.1.4:
[fastapi] Successfully uninstalled tenacity-9.1.4
[fastapi] Successfully installed tenacity-9.1.2
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0mCollecting tiktoken==0.9.0
[fastapi] Downloading tiktoken-0.9.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.7 kB)
[fastapi] Requirement already satisfied: regex>=2022.1.18 in /usr/local/lib/python3.11/dist-packages (from tiktoken==0.9.0) (2026.9.10)
[fastapi] Requirement already satisfied: requests>=2.26.0 in /usr/local/lib/python3.11/dist-packages (from tiktoken==0.9.0) (2.32.3)
[fastapi] Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.11/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (3.3.2)
[fastapi] Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.11/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (3.19)
[fastapi] Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.11/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (2.2.3)
[fastapi] Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.11/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (2024.8.30)
[fastapi] Downloading tiktoken-0.9.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (1.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 20.7 MB/s eta 0:00:00
[fastapi] Installing collected packages: tiktoken
[fastapi] Successfully installed tiktoken-0.9.0
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0mCollecting flash-attn==v2.7.4.post1
[fastapi] Downloading flash_attn-2.7.4.post1.tar.gz (6.0 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.0/6.0 MB 35.3 MB/s eta 0:00:00
[fastapi] Preparing metadata (setup.py): started
[fastapi] Preparing metadata (setup.py): finished with status 'done'
[fastapi] Requirement already satisfied: torch in /usr/local/lib/python3.11/dist-packages (from flash-attn==v2.7.4.post1) (2.4.1+cu124)
[fastapi] Requirement already satisfied: einops in /usr/local/lib/python3.11/dist-packages (from flash-attn==v2.7.4.post1) (0.8.1)
[fastapi] Requirement already satisfied: filelock in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (3.13.1)
[fastapi] Requirement already satisfied: typing-extensions>=4.8.0 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (4.16.0)
[fastapi] Requirement already satisfied: sympy in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (1.12)
[fastapi] Requirement already satisfied: networkx in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (3.2.1)
[fastapi] Requirement already satisfied: jinja2 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (3.1.3)
[fastapi] Requirement already satisfied: fsspec in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (2024.2.0)
[fastapi] Requirement already satisfied: nvidia-cuda-nvrtc-cu12==12.4.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (12.4.99)
[fastapi] Requirement already satisfied: nvidia-cuda-runtime-cu12==12.4.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (12.4.99)
[fastapi] Requirement already satisfied: nvidia-cuda-cupti-cu12==12.4.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (12.4.99)
[fastapi] Requirement already satisfied: nvidia-cudnn-cu12==9.1.0.70 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (9.1.0.70)
[fastapi] Requirement already satisfied: nvidia-cublas-cu12==12.4.2.65 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (12.4.2.65)
[fastapi] Requirement already satisfied: nvidia-cufft-cu12==11.2.0.44 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (11.2.0.44)
[fastapi] Requirement already satisfied: nvidia-curand-cu12==10.3.5.119 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (10.3.5.119)
[fastapi] Requirement already satisfied: nvidia-cusolver-cu12==11.6.0.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (11.6.0.99)
[fastapi] Requirement already satisfied: nvidia-cusparse-cu12==12.3.0.142 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (12.3.0.142)
[fastapi] Requirement already satisfied: nvidia-nccl-cu12==2.20.5 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (2.20.5)
[fastapi] Requirement already satisfied: nvidia-nvtx-cu12==12.4.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (12.4.99)
[fastapi] Requirement already satisfied: nvidia-nvjitlink-cu12==12.4.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (12.4.99)
[fastapi] Requirement already satisfied: triton==3.0.0 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (3.0.0)
[fastapi] Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.11/dist-packages (from jinja2->torch->flash-attn==v2.7.4.post1) (2.1.5)
[fastapi] Requirement already satisfied: mpmath>=0.19 in /usr/local/lib/python3.11/dist-packages (from sympy->torch->flash-attn==v2.7.4.post1) (1.3.0)
[fastapi] Building wheels for collected packages: flash-attn
[fastapi] Building wheel for flash-attn (setup.py): started
[fastapi] Building wheel for flash-attn (setup.py): finished with status 'done'
[fastapi] Created wheel for flash-attn: filename=flash_attn-2.7.4.post1-cp311-cp311-linux_x86_64.whl size=187805408 sha256=92cf49e6f66795b6934cec0cba526ed6e45d3313de3f905d45df8773f19092a9
[fastapi] Stored in directory: /root/.cache/pip/wheels/3d/88/d8/284b89f56af7d5bf366b10d6b8e251ac8a7c7bf3f04203fb4f
[fastapi] Successfully built flash-attn
[fastapi] Installing collected packages: flash-attn
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0mSuccessfully installed flash-attn-2.7.4.post1
[fastapi] [91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0m[91mUsing Python 3.11.10 environment at: /usr
[fastapi] [0m[91mResolved 142 packages in 1.65s
[fastapi] [0m[91mDownloading torchaudio (3.2MiB)
[fastapi] [0m[91mDownloading torchvision (6.9MiB)
[fastapi] [0m[91mDownloading llguidance (14.3MiB)
[fastapi] [0m[91mDownloading cupy-cuda12x (130.3MiB)
[fastapi] [0m[91mDownloading xgrammar (4.1MiB)
[fastapi] [0m[91mDownloading pillow (6.6MiB)
[fastapi] [0m[91mDownloading numba (3.6MiB)
[fastapi] [0m[91mDownloading vllm (280.4MiB)
[fastapi] [0m[91mDownloading ray (74.7MiB)
[fastapi] [0m[91mDownloading llvmlite (40.4MiB)
[fastapi] [0m[91mDownloading mistral-common (6.2MiB)
[fastapi] [0m[91mDownloading numpy (15.6MiB)
[fastapi] [0m[91mDownloading pycountry (7.7MiB)
[fastapi] [0m[91mDownloading opencv-python-headless (58.4MiB)
[fastapi] [0m[91mDownloading uvloop (3.6MiB)
[fastapi] [0m[91m Downloaded torchaudio
[fastapi] [0m[91m Downloaded numba
[fastapi] [0m[91m Downloaded uvloop
[fastapi] [0m[91m Downloaded xgrammar
[fastapi] [0m[91m Downloaded mistral-common
[fastapi] [0m[91m Downloaded pillow
[fastapi] [0m[91m Downloaded torchvision
[fastapi] [0m[91m Downloaded pycountry
[fastapi] [0m[91m Downloaded llguidance
[fastapi] [0m[91m Downloaded numpy
[fastapi] [0m[91m Downloaded llvmlite
[fastapi] [0m[91m Downloaded opencv-python-headless
[fastapi] [0m[91m Downloaded ray
[fastapi] [0m[91m Downloaded cupy-cuda12x
[fastapi] [0m[91m Downloaded vllm
[fastapi] [0m[91mPrepared 45 packages in 12.46s
[fastapi] [0m[91mUninstalled 23 packages in 13.11s
[fastapi] [0m[91mInstalled 71 packages in 1m 02s
[fastapi] [0m[91m + agent-detector==2.0.0
[fastapi] + airportsdata==20260905
[fastapi] + blake3==1.0.9
[fastapi] + compressed-tensors==0.9.2
[fastapi] + cuda-pathfinder==1.8.1
[fastapi] + cupy-cuda12x==14.2.[0m[91m0
[fastapi] + depyf==0.18.0
[fastapi] + detect-installer==0.2.[0m[91m1
[fastapi] + diskcache==5.6.3
[fastapi] + dnspython==2[0m[91m.8.0
[fastapi] + email-validator==2.3.0
[fastapi] + fastapi-cli==0.0.32
[fastapi] + fastapi-cloud-cli==0.26[0m[91m.0
[fastapi] + fastar[0m[91m==0.12.0
[fastapi] [0m[91m - filelock==3.13.1
[fastapi] + filelock==3.32.6
[fastapi] + gguf==0.10.0
[fastapi] - httpcore==1.0.5
[fastapi] + httpcore==1.0.9
[fastapi] + httptools==0.8.0
[fastapi] + interegular==0.3.3
[fastapi] - jinja2==[0m[91m3.1.3
[fastapi] + jinja2==3.1.6
[fastapi] +[0m[91m lark==1.[0m[91m2.2
[fastapi] + llguidance==0.7.30
[fastapi] [0m[91m+ llvmlite==0.44.0[0m[91m
[fastapi] + lm-format-enforcer==0.10.12
[fastapi] + markdown-it-py==4.2.0
[fastapi] + mdurl==0.1.2[0m[91m
[fastapi] + mistral-common==1[0m[91m.11.7
[fastapi] + msgspec==0.21.[0m[91m1
[fastapi] + nanobind==3.[0m[91m0.1
[fastapi] + numba==[0m[91m0.61.0[0m[91m
[fastapi] -[0m[91m numpy==[0m[91m1.26.3
[fastapi] [0m[91m+ numpy[0m[91m==[0m[91m2.1.[0m[91m3
[fastapi] - nvidia-cublas-cu12==12.4.2.65
[fastapi] + nvidia-cublas-cu12==12.4.5.8
[fastapi] - nvidia-cuda-cupti-cu12==12.4.99
[fastapi] [0m[91m+ nvidia-cuda-cupti-cu12==12.4.127
[fastapi] -[0m[91m nvidia-cuda-nvrtc-cu12==12.4.99
[fastapi] + nvidia-cuda-nvrtc-cu12[0m[91m==12.4.127
[fastapi] [0m[91m- nvidia-cuda-runtime-cu12==12.[0m[91m4.99
[fastapi] +[0m[91m nvidia-cuda-runtime-cu12==12.4.127
[fastapi] - nvidia-cufft-cu12==11.2.0.44
[fastapi] + nvidia-cufft-cu12==11.2.[0m[91m1.3
[fastapi] - [0m[91mnvidia-curand-cu12==10.3.5.119[0m[91m
[fastapi] + nvidia-curand-cu12==10.3[0m[91m.5.147[0m[91m
[fastapi] [0m[91m - [0m[91mnvidia-cusolver-cu12[0m[91m==11.[0m[91m6.0[0m[91m.99
[fastapi] + [0m[91mnvidia-cusolver-cu12==11.6[0m[91m.1.9[0m[91m
[fastapi] -[0m[91m nvidia-cusparse-cu12==12.3.0.142
[fastapi] + nvidia-cusparse-cu12==12.3.1.170
[fastapi] + nvidia-cusparselt-cu12==0.6.2
[fastapi] - nvidia-nccl-cu12==2.20.5
[fastapi] + nvidia-nccl-cu12==2.21.5
[fastapi] - [0m[91mnvidia-nvjitlink-cu12==12.4.99[0m[91m
[fastapi] +[0m[91m nvidia-nvjitlink-cu12==12.4.127
[fastapi] - nvidia-nvtx-cu12==12.4.99
[fastapi] + nvidia-nvtx-cu12==12.4.127
[fastapi] + opencv-python-headless==[0m[91m5.0.0.93
[fastapi] + [0m[91moutlines==0.1[0m[91m.11
[fastapi] + outlines-core==0.1.26
[fastapi] - packaging[0m[91m==23[0m[91m.2
[fastapi] [0m[91m [0m[91m+ packaging==26.3[0m[91m
[fastapi] + [0m[91mpartial-json-parser==0.2.1.1[0m[91m.post7
[fastapi] - pillow[0m[91m==10.2.0
[fastapi] + pillow[0m[91m==12.3.[0m[91m0
[fastapi] +[0m[91m prometheus-fastapi-instrumentator[0m[91m==8.[0m[91m1.0
[fastapi] + pycountry==26.[0m[91m2.16
[fastapi] + [0m[91mpydantic-extra-types==2.11[0m[91m.1
[fastapi] + pydantic-settings==2.15.0
[fastapi] + python-multipart[0m[91m==0.0.32
[fastapi] + ray[0m[91m==2.58.0
[fastapi] +[0m[91m rich==15[0m[91m.0.0[0m[91m
[fastapi] + rich-toolkit[0m[91m==0.20.5[0m[91m
[fastapi] + [0m[91mrignore==0[0m[91m.8.1
[fastapi] + [0m[91mshellingham==1.5.4
[fastapi] [0m[91m- sympy[0m[91m==1.12[0m[91m
[fastapi] + sympy==1.13.1
[fastapi] - torch==2.4.1+[0m[91mcu124
[fastapi] + torch==2.6.0
[fastapi] - torchaudio==2.4.1+[0m[91mcu124
[fastapi] + torchaudio==2.6.0
[fastapi] [0m[91m- torchvision==0.19.1[0m[91m+cu124
[fastapi] + torchvision==0.21.0
[fastapi] - triton==3.0.0
[fastapi] [0m[91m+ triton==3.2.0
[fastapi] - typer==0.9.0
[fastapi] + typer==0.27.2
[fastapi] + uvloop==0.22.1
[fastapi] + vllm==0.8.3
[fastapi] + watchfiles==1.2.0
[fastapi] + websockets==17.1
[fastapi] + xformers==0[0m[91m.0.29.post2
[fastapi] + [0m[91mxgrammar==0.1.[0m[91m17
[fastapi] [0mCollecting fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0
[fastapi] Cloning https://github.com/rayonlabs/fiber.git (to revision 2.4.0) to /tmp/pip-install-l_89e0c2/fiber_d68a3ad9009749fe92a6d38f4f3c2d6e
[fastapi] [91m  Running command git clone --filter=blob:none --quiet https://github.com/rayonlabs/fiber.git /tmp/pip-install-l_89e0c2/fiber_d68a3ad9009749fe92a6d38f4f3c2d6e
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
[fastapi] Requirement already satisfied: certifi>=2019.3.9 in /usr/local/lib/python3.11/dist-packages (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2024.8.30)
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
[fastapi] Requirement already satisfied: websockets>=14.1 in /usr/local/lib/python3.11/dist-packages (from async-substrate-interface<2.0.0,>=1.0.0->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (17.1)
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
[fastapi] Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.11/dist-packages (from requests<3,>=2.21.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (3.3.2)
[fastapi] Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.11/dist-packages (from requests<3,>=2.21.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2.2.3)
[fastapi] Requirement already satisfied: more-itertools in /usr/lib/python3/dist-packages (from scalecodec<1.3,>=1.2.10->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (8.10.0)
[fastapi] Requirement already satisfied: pycparser in /usr/local/lib/python3.11/dist-packages (from cffi>=2.0.0->PyNaCl<2,>=1.0.1->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2.22)
[fastapi] Collecting toolz>=0.8.0 (from cytoolz>=0.10.1->eth-utils<3,>=1.3.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading toolz-1.1.0-py3-none-any.whl.metadata (5.1 kB)
[fastapi] Downloading bittensor_commit_reveal-0.1.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (552 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 552.2/552.2 kB 12.1 MB/s eta 0:00:00
[fastapi] Downloading eth_typing-5.0.0-py3-none-any.whl (20 kB)
[fastapi] Downloading netaddr-1.3.0-py3-none-any.whl (2.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.3/2.3 MB 33.8 MB/s eta 0:00:00
[fastapi] Downloading python_dotenv-1.0.1-py3-none-any.whl (19 kB)
[fastapi] Downloading substrate_interface-1.7.10-py3-none-any.whl (60 kB)
[fastapi] Downloading tenacity-9.0.0-py3-none-any.whl (28 kB)
[fastapi] Downloading async_substrate_interface-1.6.4-py3-none-any.whl (97 kB)
[fastapi] Downloading bt_decode-0.8.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (647 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 647.8/647.8 kB 18.8 MB/s eta 0:00:00
[fastapi] Downloading colorama-0.4.6-py2.py3-none-any.whl (25 kB)
[fastapi] Downloading pydantic-2.9.2-py3-none-any.whl (434 kB)
[fastapi] Downloading pydantic_core-2.23.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 29.0 MB/s eta 0:00:00
[fastapi] Downloading aiosqlite-0.22.1-py3-none-any.whl (17 kB)
[fastapi] Downloading base58-2.1.1-py3-none-any.whl (5.6 kB)
[fastapi] Downloading ecdsa-0.19.2-py2.py3-none-any.whl (150 kB)
[fastapi] Downloading eth_keys-0.8.0-py3-none-any.whl (20 kB)
[fastapi] Downloading eth_utils-2.3.2-py3-none-any.whl (77 kB)
[fastapi] Downloading py_bip39_bindings-0.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (432 kB)
[fastapi] Downloading py_ed25519_zebra_bindings-1.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (323 kB)
[fastapi] Downloading py_sr25519_bindings-0.2.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (372 kB)
[fastapi] Downloading pynacl-1.6.2-cp38-abi3-manylinux_2_34_x86_64.whl (1.4 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.4/1.4 MB 25.7 MB/s eta 0:00:00
[fastapi] Downloading scalecodec-1.2.12-py3-none-any.whl (99 kB)
[fastapi] Downloading xxhash-3.8.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (220 kB)
[fastapi] Downloading cytoolz-1.1.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (2.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.8/2.8 MB 31.9 MB/s eta 0:00:00
[fastapi] Downloading eth_hash-0.8.0-py3-none-any.whl (8.0 kB)
[fastapi] Downloading toolz-1.1.0-py3-none-any.whl (58 kB)
[fastapi] Building wheels for collected packages: fiber
[fastapi] Building wheel for fiber (pyproject.toml): started
[fastapi] Building wheel for fiber (pyproject.toml): finished with status 'done'
[fastapi] Created wheel for fiber: filename=fiber-2.4.0-py3-none-any.whl size=51790 sha256=c50f803eff2fbcdf01560cfffdc65a3891a75b0b315d61d842fd3861f51b5d73
[fastapi] Stored in directory: /tmp/pip-ephem-wheel-cache-zavfo4e7/wheels/d1/5e/21/2fa1f403cd187996037f04f6328bf11973ce31440a275f6949
[fastapi] Successfully built fiber
[fastapi] Installing collected packages: xxhash, toolz, tenacity, python-dotenv, pydantic-core, py-sr25519-bindings, py-ed25519-zebra-bindings, py-bip39-bindings, netaddr, eth-typing, eth-hash, ecdsa, colorama, bt-decode, bittensor-commit-reveal, base58, aiosqlite, scalecodec, PyNaCl, pydantic, cytoolz, eth-utils, async-substrate-interface, eth-keys, substrate-interface, fiber
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
[fastapi] Successfully installed PyNaCl-1.6.2 aiosqlite-0.22.1 async-substrate-interface-1.6.4 base58-2.1.1 bittensor-commit-reveal-0.1.0 bt-decode-0.8.0 colorama-0.4.6 cytoolz-1.1.0 ecdsa-0.19.2 eth-hash-0.8.0 eth-keys-0.8.0 eth-typing-5.0.0 eth-utils-2.3.2 fiber-2.4.0 netaddr-1.3.0 py-bip39-bindings-0.3.0 py-ed25519-zebra-bindings-1.3.0 py-sr25519-bindings-0.2.4 pydantic-2.9.2 pydantic-core-2.23.4 python-dotenv-1.0.1 scalecodec-1.2.12 substrate-interface-1.7.10 tenacity-9.0.0 toolz-1.1.0 xxhash-3.8.1
[fastapi] [91mERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
[fastapi] dash 4.4.1 requires pydantic>=2.10, but you have pydantic 2.9.2 which is incompatible.
[fastapi] [0m[91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0m ---> 5a6b2ede4724
[fastapi] Step 13/13 : ENTRYPOINT ["./entrypoint.sh"]
[fastapi] ---> Running in 55b44cfba55f
[fastapi] ---> 0de1cb2754b1
[fastapi] {'aux': {'ID': 'sha256:0de1cb2754b17e7b06f0763cf90381cc3305e08979d4d0d831d88cdb6d432971'}}Successfully built 0de1cb2754b1
[fastapi] Successfully tagged standalone-text-trainer:80cd203a-46b4-4ac8-9e55-8a7a3f7b8dc5
[fastapi] Docker image built successfully.
[fastapi] Training job failed: 4022aee4-05b1-4533-b1d9-0c6f52bbb747
[fastapi] Cleaning up
[fastapi] Cleaned up Docker resources.
[fastapi] Repository cloned successfully
[fastapi] Running Cache Download Container
[fastapi] Starting downloader container: downloader-4022aee4-05b1-4533-b1d9-0c6f52bbb747-e1dae3d8
[fastapi] Download completed successfully for task 4022aee4-05b1-4533-b1d9-0c6f52bbb747
[fastapi] Building Docker image 'standalone-text-trainer:b15df6f6-e2e8-4c4e-bba4-01503f082fa4' (timeout=1800s)...
[fastapi] Step 1/13 : FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04
[fastapi] Pulling from runpod/pytorchPulling fs layerPulling fs layerPulling fs layerPulling fs layerPulling fs layerPulling fs layerPulling fs layerPulling fs layerPulling fs layerPulling fs layerPulling fs layerPulling fs layerPulling fs layerPulling fs layerPulling fs layerPulling fs layerPulling fs layerPulling fs layerPulling fs layerPulling fs layerPulling fs layerPulling fs layerPulling fs layerPulling fs layerPulling fs layerPulling fs layerPulling fs layerWaitingPulling fs layerWaitingWaitingWaitingWaitingWaitingWaitingWaitingWaitingWaitingWaitingWaitingWaitingWaitingWaitingWaitingWaitingWaitingWaitingWaitingWaitingWaitingWaitingWaitingWaitingDownloadingDownloadingDownloadingVerifying ChecksumDownload completeDownload completeExtractingDownloadingDownloadingDownload completeVerifying ChecksumDownload completeDownloadingDownloadingDownload completeExtractingDownloadingDownloadingDownloadingVerifying ChecksumDownload completeExtractingDownloadingVerifying ChecksumDownload completeDownloadingExtractingDownloadingVerifying ChecksumDownload completeDownloadingDownloadingDownloadingDownloadingVerifying ChecksumDownload completeDownloadingExtractingDownloadingDownloadingDownloadingDownload completeDownloadingExtractingExtractingDownloadingDownloadingDownloadingPull completeExtractingDownloadingDownloadingDownloadingExtractingExtractingPull completeExtractingDownloadingDownloadingDownloadingExtractingDownloadingDownloadingDownloadingExtractingDownloadingDownloadingDownloadingVerifying ChecksumDownload completeExtractingDownloadingDownloadingDownloadingDownloadingExtractingVerifying ChecksumDownload completeDownloadingDownloadingExtractingDownloadingDownloadingVerifying ChecksumDownload completeDownloadingExtractingDownloadingDownloadingExtractingPull completeExtractingExtractingPull completeExtractingExtractingPull completeDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingDownloadingVerifying ChecksumDownload completeExtractingDownloadingDownloadingExtractingDownloadingDownloadingDownloadingExtractingDownloadingDownloadingDownloadingVerifying ChecksumDownload completeExtractingDownloadingDownloadingDownloadingExtractingDownloadingDownloadingVerifying ChecksumDownload completeExtractingDownloadingDownloadingDownloadingExtractingDownloadingDownloadingVerifying ChecksumDownload completeExtractingDownloadingDownloadingDownloadingDownload completeExtractingDownloadingDownloadingExtractingDownloadingDownload completeDownloadingDownloadingExtractingDownloadingDownload completeDownloadingExtractingDownloadingDownloadingDownload completeDownloadingExtractingDownloadingDownloadingDownloadingVerifying ChecksumDownload completeDownloadingExtractingDownloadingDownloadingVerifying ChecksumDownload completeDownloadingExtractingDownloadingDownloadingVerifying ChecksumDownload completeDownloadingExtractingDownloadingDownloadingExtractingDownloadingVerifying ChecksumDownload completeDownloadingDownloadingExtractingDownloadingVerifying ChecksumDownload completeDownloadingDownloadingExtractingDownloadingDownloadingExtractingDownloadingDownloadingExtractingDownloadingDownloadingExtractingDownloadingDownloadingExtractingDownloadingDownloadingExtractingDownloadingDownloadingExtractingDownloadingDownloadingExtractingDownloadingDownloadingExtractingDownloadingDownloadingExtractingDownloadingDownloadingVerifying ChecksumDownload completeExtractingDownloadingExtractingDownloadingExtractingDownloadingExtractingDownloadingExtractingDownloadingExtractingDownloadingExtractingDownloadingExtractingDownloadingExtractingDownloadingExtractingDownloadingExtractingDownloadingExtractingDownloadingExtractingDownloadingExtractingDownloadingExtractingDownloadingExtractingDownloadingVerifying ChecksumDownload completeExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingPull completeExtractingExtractingPull completeExtractingExtractingPull completeExtractingExtractingPull completeExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingPull completeExtractingExtractingExtractingPull completeExtractingExtractingPull completeExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingPull completeExtractingExtractingExtractingExtractingExtractingPull completeExtractingExtractingPull completeExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingPull completeExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingExtractingPull completeExtractingExtractingExtractingExtractingExtractingExtractingPull completeExtractingExtractingExtractingExtractingPull completeExtractingExtractingPull completeExtractingExtractingPull completeExtractingExtractingPull completeExtractingExtractingPull completeExtractingExtractingPull completeExtractingExtractingPull completeExtractingExtractingPull completeExtractingExtractingPull completeExtractingExtractingPull completeDigest: sha256:61a4aafb0094cd773f11eefa378929d5a687bd775febeb78eac62fc824141fb5Status: Downloaded newer image for runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04 ---> ff5fe688608b
[fastapi] Step 2/13 : RUN apt-get update && apt-get install -y     vim     zip     tmux     iotop     nvtop     bmon     wget     nano     zsh     htop     && rm -rf /var/lib/apt/lists/*
[fastapi] ---> Running in cc8892386ca2
[fastapi] Get:1 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  InRelease [1578 B]
[fastapi] Get:2 http://archive.ubuntu.com/ubuntu jammy InRelease [270 kB]
[fastapi] Get:3 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  Packages [3011 kB]
[fastapi] Get:4 http://security.ubuntu.com/ubuntu jammy-security InRelease [129 kB]
[fastapi] Get:5 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [128 kB]
[fastapi] Get:6 http://archive.ubuntu.com/ubuntu jammy-backports InRelease [127 kB]
[fastapi] Get:7 http://archive.ubuntu.com/ubuntu jammy/main amd64 Packages [1792 kB]
[fastapi] Get:8 http://archive.ubuntu.com/ubuntu jammy/restricted amd64 Packages [164 kB]
[fastapi] Get:9 http://archive.ubuntu.com/ubuntu jammy/universe amd64 Packages [17.5 MB]
[fastapi] Get:10 http://security.ubuntu.com/ubuntu jammy-security/multiverse amd64 Packages [84.6 kB]
[fastapi] Get:11 http://archive.ubuntu.com/ubuntu jammy/multiverse amd64 Packages [266 kB]
[fastapi] Get:12 http://archive.ubuntu.com/ubuntu jammy-updates/multiverse amd64 Packages [93.2 kB]
[fastapi] Get:13 http://archive.ubuntu.com/ubuntu jammy-updates/restricted amd64 Packages [8007 kB]
[fastapi] Get:14 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy InRelease [18.1 kB]
[fastapi] Get:15 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 Packages [4624 kB]
[fastapi] Get:16 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 Packages [1620 kB]
[fastapi] Get:17 http://archive.ubuntu.com/ubuntu jammy-backports/main amd64 Packages [82.8 kB]
[fastapi] Get:18 http://archive.ubuntu.com/ubuntu jammy-backports/universe amd64 Packages [35.6 kB]
[fastapi] Get:19 http://security.ubuntu.com/ubuntu jammy-security/main amd64 Packages [4290 kB]
[fastapi] Get:20 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy/main amd64 Packages [44.3 kB]
[fastapi] Get:21 http://security.ubuntu.com/ubuntu jammy-security/restricted amd64 Packages [7717 kB]
[fastapi] Get:22 http://security.ubuntu.com/ubuntu jammy-security/universe amd64 Packages [1317 kB]
[fastapi] Fetched 51.3 MB in 2s (20.9 MB/s)
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
[fastapi] 5 upgraded, 24 newly installed, 0 to remove and 170 not upgraded.
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
[fastapi] [0mFetched 23.1 MB in 2s (11.7 MB/s)
[fastapi] (Reading database ... (Reading database ... 5%(Reading database ... 10%(Reading database ... 15%(Reading database ... 20%(Reading database ... 25%(Reading database ... 30%(Reading database ... 35%(Reading database ... 40%(Reading database ... 45%(Reading database ... 50%(Reading database ... 55%(Reading database ... 60%(Reading database ... 65%(Reading database ... 70%(Reading database ... 75%(Reading database ... 80%(Reading database ... 85%(Reading database ... 90%(Reading database ... 95%(Reading database ... 100%(Reading database ... 24135 files and directories currently installed.)
[fastapi] Preparing to unpack .../00-python3.10_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking python3.10 (3.10.12-1~22.04.18) over (3.10.12-1~22.04.6) ...
[fastapi] Preparing to unpack .../01-libpython3.10-stdlib_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking libpython3.10-stdlib:amd64 (3.10.12-1~22.04.18) over (3.10.12-1~22.04.6) ...
[fastapi] Preparing to unpack .../02-python3.10-minimal_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking python3.10-minimal (3.10.12-1~22.04.18) over (3.10.12-1~22.04.6) ...
[fastapi] Preparing to unpack .../03-libpython3.10-minimal_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking libpython3.10-minimal:amd64 (3.10.12-1~22.04.18) over (3.10.12-1~22.04.6) ...
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
[fastapi] Processing triggers for libc-bin (2.35-0ubuntu3.8) ...
[fastapi] ---> 9aef4fccc76d
[fastapi] Step 3/13 : RUN mkdir -p /workspace
[fastapi] ---> Running in cbcf3d0c5cfd
[fastapi] ---> 806dc322f9cd
[fastapi] Step 4/13 : RUN mkdir -p /cache
[fastapi] ---> Running in 6747a68fb2de
[fastapi] ---> 6228ec431d41
[fastapi] Step 5/13 : RUN mkdir -p /workspace/scripts/datasets
[fastapi] ---> Running in fc3d0abc09bb
[fastapi] ---> 3b87a0bf787d
[fastapi] Step 6/13 : RUN mkdir -p /app/checkpoints
[fastapi] ---> Running in c16275c3a796
[fastapi] ---> 29ca697bd1a5
[fastapi] Step 7/13 : WORKDIR /workspace/scripts
[fastapi] ---> Running in b55992b6b8d7
[fastapi] ---> 276abd15981d
[fastapi] Step 8/13 : COPY scripts /workspace/scripts
[fastapi] ---> 605f21273b82
[fastapi] Step 9/13 : RUN chmod +x /workspace/scripts/entrypoint.sh
[fastapi] ---> Running in 579ba861074e
[fastapi] ---> f1a5e9aa09b0
[fastapi] Step 10/13 : RUN python -m venv /workspace/axo_py
[fastapi] ---> Running in c55902a6cc03
[fastapi] ---> 940835026a4f
[fastapi] Step 11/13 : RUN bash -c "source /workspace/axo_py/bin/activate &&     pip install uv &&     pip install -U packaging==23.2 setuptools==75.8.0 wheel ninja &&     uv pip install --no-build-isolation axolotl==0.9.1 &&     pip install requests==2.32.3 &&     deactivate"
[fastapi] ---> Running in e992b1f4c2a0
[fastapi] Collecting uv
[fastapi] Downloading uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] Downloading uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.1 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 20.1/20.1 MB 191.6 MB/s eta 0:00:00
[fastapi] Installing collected packages: uv
[fastapi] Successfully installed uv-0.12.15
[fastapi] [91m
[fastapi] [notice] A new release of pip is available: 24.0 -> 26.2.1
[fastapi] [notice] To update, run: pip install --upgrade pip
[fastapi] [0mCollecting packaging==23.2
[fastapi] Downloading packaging-23.2-py3-none-any.whl.metadata (3.2 kB)
[fastapi] Collecting setuptools==75.8.0
[fastapi] Downloading setuptools-75.8.0-py3-none-any.whl.metadata (6.7 kB)
[fastapi] Collecting wheel
[fastapi] Downloading wheel-0.48.0-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Collecting ninja
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (5.4 kB)
[fastapi] INFO: pip is looking at multiple versions of wheel to determine which version is compatible with other requirements. This could take a while.
[fastapi] Collecting wheel
[fastapi] Downloading wheel-0.47.0-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Downloading wheel-0.46.3-py3-none-any.whl.metadata (2.4 kB)
[fastapi] Downloading wheel-0.46.2-py3-none-any.whl.metadata (2.4 kB)
[fastapi] Downloading wheel-0.45.1-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Downloading packaging-23.2-py3-none-any.whl (53 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 53.0/53.0 kB 5.2 MB/s eta 0:00:00
[fastapi] Downloading setuptools-75.8.0-py3-none-any.whl (1.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 44.3 MB/s eta 0:00:00
[fastapi] Downloading wheel-0.45.1-py3-none-any.whl (72 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 72.5/72.5 kB 18.7 MB/s eta 0:00:00
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (183 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 183.4/183.4 kB 54.3 MB/s eta 0:00:00
[fastapi] Installing collected packages: wheel, setuptools, packaging, ninja
[fastapi] Attempting uninstall: setuptools
[fastapi] Found existing installation: setuptools 65.5.0
[fastapi] Uninstalling setuptools-65.5.0:
[fastapi] Successfully uninstalled setuptools-65.5.0
[fastapi] Successfully installed ninja-1.13.2 packaging-23.2 setuptools-75.8.0 wheel-0.45.1
[fastapi] [91m
[fastapi] [notice] A new release of pip is available: 24.0 -> 26.2.1
[fastapi] [notice] To update, run: pip install --upgrade pip
[fastapi] [0m[91mUsing Python 3.11.10 environment at: /workspace/axo_py
[fastapi] [0m[91mResolved 217 packages in 1.25s
[fastapi] [0m[91m   Building grpclib==0.4.7
[fastapi] [0m[91mDownloading pandas (12.2MiB)
[fastapi] [0m[91mDownloading ruff (9.9MiB)
[fastapi] [0m[91mDownloading sympy (5.9MiB)
[fastapi] [0m[91mDownloading cryptography (4.5MiB)
[fastapi] [0m[91mDownloading networkx (2.0MiB)
[fastapi] [0m[91mDownloading nltk (1.7MiB)
[fastapi] [0m[91mDownloading aiohttp (1.7MiB)
[fastapi] [0m[91mDownloading pygments (1.2MiB)
[fastapi] [0m[91mDownloading botocore (13.7MiB)
[fastapi] [0m[91mDownloading scipy (33.7MiB)
[fastapi] [0m[91mDownloading lxml (5.0MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-cupti-cu12 (13.2MiB)
[fastapi] [0m[91mDownloading tensorboard-data-server (6.3MiB)
[fastapi] [0m[91mDownloading sentencepiece (1.3MiB)
[fastapi] [0m[91mDownloading pyarrow (47.7MiB)
[fastapi] [0m[91mDownloading lm-eval (2.4MiB)
[fastapi] [0m[91mDownloading triton (241.4MiB)
[fastapi] [0m[91mDownloading grpcio (6.9MiB)
[fastapi] [0m[91mDownloading scikit-learn (11.6MiB)
[fastapi] [0m[91mDownloading torch (731.2MiB)
[fastapi] [0m[91mDownloading nvidia-cufft-cu12 (201.7MiB)
[fastapi] [0m[91mDownloading nvidia-cudnn-cu12 (634.0MiB)
[fastapi] [0m[91mDownloading hf-transfer (3.4MiB)
[fastapi] [0m[91mDownloading numba (3.6MiB)
[fastapi] [0m[91mDownloading nvidia-cublas-cu12 (346.6MiB)
[fastapi] [0m[91mDownloading nvidia-nccl-cu12 (179.9MiB)
[fastapi] [0m[91mDownloading llvmlite (57.1MiB)
[fastapi] [0m[91mDownloading nvidia-cusparselt-cu12 (143.1MiB)
[fastapi] [0m[91mDownloading nvidia-curand-cu12 (53.7MiB)
[fastapi] [0m[91mDownloading nvidia-nvjitlink-cu12 (20.1MiB)
[fastapi] [0m[91mDownloading nvidia-cusparse-cu12 (197.8MiB)
[fastapi] [0m[91mDownloading wandb (24.9MiB)
[fastapi] [0m[91mDownloading pydantic-core (1.9MiB)
[fastapi] [0m[91mDownloading nvidia-cusolver-cu12 (122.0MiB)
[fastapi] [0m[91mDownloading transformers (9.9MiB)
[fastapi] [0m[91mDownloading zstandard (5.2MiB)
[fastapi] [0m[91mDownloading numpy (18.6MiB)
[fastapi] [0m[91mDownloading bitsandbytes (72.5MiB)
[fastapi] [0m[91mDownloading oci (35.2MiB)
[fastapi] [0m[91mDownloading pillow (6.3MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-nvrtc-cu12 (23.5MiB)
[fastapi] [0m[91mDownloading torchao (5.4MiB)
[fastapi] [0m[91mDownloading xformers (42.2MiB)
[fastapi] [0m[91mDownloading hf-xet (51.1MiB)
[fastapi] [0m[91mDownloading gradio (44.3MiB)
[fastapi] [0m[91mDownloading tokenizers (3.0MiB)
[fastapi] [0m[91mDownloading tensorboard (5.3MiB)
[fastapi] [0m[91m Downloaded pygments
[fastapi] [0m[91m Downloaded sentencepiece
[fastapi] [0m[91m Downloaded aiohttp
[fastapi] [0m[91m Downloaded nltk
[fastapi] [0m[91m Downloaded pydantic-core
[fastapi] [0m[91m Downloaded networkx
[fastapi] [0m[91m      Built grpclib==0.4.7
[fastapi] [0m[91m Downloaded lm-eval
[fastapi] [0m[91m Downloaded tokenizers
[fastapi] [0m[91m   Building axolotl==0.9.1
[fastapi] [0m[91m Downloaded hf-transfer
[fastapi] [0m[91m   Building axolotl-contribs-mit==0.0.3
[fastapi] [0m[91m Downloaded numba
[fastapi] [0m[91m   Building word2number==1.1
[fastapi] [0m[91m   Building axolotl-contribs-lgpl==0.0.6
[fastapi] [0m[91m   Building rouge-score==0.1.2
[fastapi] [0m[91m   Building sqlitedict==2.1.0
[fastapi] [0m[91m   Building langdetect==1.0.9
[fastapi] [0m[91m Downloaded cryptography
[fastapi] [0m[91m   Building hqq==0.2.5
[fastapi] [0m[91m Downloaded lxml
[fastapi] [0m[91m      Built axolotl-contribs-mit==0.0.3
[fastapi] [0m[91m Downloaded zstandard
[fastapi] [0m[91m Downloaded tensorboard
[fastapi] [0m[91m      Built word2number==1.1
[fastapi] [0m[91m Downloaded torchao
[fastapi] [0m[91m      Built rouge-score==0.1.2
[fastapi] [0m[91m      Built axolotl-contribs-lgpl==0.0.6
[fastapi] [0m[91m      Built sqlitedict==2.1.0
[fastapi] [0m[91m Downloaded sympy
[fastapi] [0m[91m      Built axolotl==0.9.1
[fastapi] [0m[91m Downloaded tensorboard-data-server
[fastapi] [0m[91m Downloaded pillow
[fastapi] [0m[91m Downloaded grpcio
[fastapi] [0m[91m Downloaded ruff
[fastapi] [0m[91m Downloaded transformers
[fastapi] [0m[91m      Built langdetect==1.0.9
[fastapi] [0m[91m Downloaded scikit-learn
[fastapi] [0m[91m      Built hqq==0.2.5
[fastapi] [0m[91m Downloaded nvidia-cuda-cupti-cu12
[fastapi] [0m[91m Downloaded pandas
[fastapi] [0m[91m Downloaded botocore
[fastapi] [0m[91m Downloaded numpy
[fastapi] [0m[91m Downloaded nvidia-nvjitlink-cu12
[fastapi] [0m[91m Downloaded nvidia-cuda-nvrtc-cu12
[fastapi] [0m[91m Downloaded wandb
[fastapi] [0m[91m Downloaded scipy
[fastapi] [0m[91m Downloaded xformers
[fastapi] [0m[91m Downloaded oci
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
[fastapi] [0m[91mPrepared 215 packages in 8.40s
[fastapi] [0m[91mInstalled 215 packages in 433ms
[fastapi] [0m[91m + absl-py==2.5.0
[fastapi] + accelerate==1.6.0
[fastapi] + addict==2.4.0
[fastapi] + adlfs==2026.8.0
[fastapi] + aiobotocore==2.26.0
[fastapi] + aiofiles==23.2.[0m[91m1
[fastapi] + aiohappyeyeballs==2.7.1
[fastapi] + aiohttp==3.14.3
[fastapi] + aioitertools[0m[91m==0.13.0
[fastapi] + aiosignal==1.4.0
[fastapi] +[0m[91m annotated-doc==0.0.5
[fastapi] + annotated-types==0.[0m[91m8.0
[fastapi] + antlr4-python3-runtime==4.13[0m[91m.2
[fastapi] + anyio==4.15.1
[fastapi] + art[0m[91m==6.[0m[91m5
[fastapi] + [0m[91mattrs==26.1.0[0m[91m
[fastapi] + autoawq==0[0m[91m.2.7.post[0m[91m3
[fastapi] + [0m[91maxolotl==[0m[91m0.9[0m[91m.1
[fastapi] [0m[91m + axolotl-contribs-lgpl==0.0.6
[fastapi] + axolotl-contribs-mit[0m[91m==0.0.3[0m[91m
[fastapi] +[0m[91m azure-core==1.41.0
[fastapi] + azure-identity==1[0m[91m.25.3
[fastapi] [0m[91m + [0m[91mazure-storage-blob==12.30.[0m[91m1
[fastapi] +[0m[91m bitsandbytes[0m[91m==0.45[0m[91m.4
[fastapi] + [0m[91mbotocore==1.[0m[91m41.5
[fastapi] [0m[91m+ certifi[0m[91m==2026.7.[0m[91m22
[fastapi] + [0m[91mcffi==2[0m[91m.1.1[0m[91m
[fastapi] + chardet==6.0.[0m[91m0.post1
[fastapi] + [0m[91mcharset-normalizer==3.5[0m[91m.1[0m[91m
[fastapi] + [0m[91mcircuitbreaker==2.1[0m[91m.3[0m[91m
[fastapi] [0m[91m + click[0m[91m==8.[0m[91m5.0
[fastapi] + cloudpickle[0m[91m==3.[0m[91m1.2
[fastapi] [0m[91m + colorama[0m[91m==0.4.6[0m[91m
[fastapi] + coloredlogs==15.0.1[0m[91m
[fastapi] + crc32c[0m[91m==2.8[0m[91m
[fastapi] + cryptography==[0m[91m50.0.1
[fastapi] [0m[91m + dataproperty[0m[91m==1.1.1
[fastapi] [0m[91m + [0m[91mdatasets[0m[91m==3.[0m[91m5[0m[91m.1
[fastapi] + decorator==5.3.[0m[91m1
[fastapi] [0m[91m+ defusedxml[0m[91m==0[0m[91m.[0m[91m7.1
[fastapi] + dill==0.[0m[91m3.8[0m[91m
[fastapi] + [0m[91meinops==[0m[91m0.8.2
[fastapi] + evaluate[0m[91m==0.4.[0m[91m1
[fastapi] +[0m[91m fastapi==[0m[91m0.141.1
[fastapi] + [0m[91mfastcore==2.2[0m[91m.28
[fastapi] +[0m[91m ffmpy==1[0m[91m.0.0[0m[91m
[fastapi] +[0m[91m filelock==3.32[0m[91m.7
[fastapi] + fire==0.7[0m[91m.1
[fastapi] + frozenlist[0m[91m==1.8[0m[91m.0
[fastapi] [0m[91m + [0m[91mfsspec[0m[91m==2025.[0m[91m3.0[0m[91m
[fastapi] +[0m[91m gcsfs==2025[0m[91m.3.0
[fastapi] +[0m[91m google-api-core==2.33[0m[91m.0
[fastapi] [0m[91m + google-auth[0m[91m==2.58[0m[91m.0
[fastapi] [0m[91m+ google-auth-oauthlib[0m[91m==1.4.[0m[91m1
[fastapi] +[0m[91m [0m[91mgoogle-cloud-core==2.7.0
[fastapi] + google-cloud-storage==3.14.1
[fastapi] + google-crc32c==1.8.0
[fastapi] [0m[91m+ google-resumable-media==2[0m[91m.10.2
[fastapi] + googleapis-common-protos==[0m[91m1.75.0
[fastapi] [0m[91m+ [0m[91mgradio[0m[91m==5.23.3
[fastapi] + gradio-client[0m[91m==1.8.0
[fastapi] +[0m[91m groovy==0.[0m[91m1[0m[91m.2[0m[91m
[fastapi] [0m[91m+[0m[91m [0m[91mgrpcio==1[0m[91m.[0m[91m84[0m[91m.0
[fastapi] + grpclib==0.4.[0m[91m7
[fastapi] + h11==0.[0m[91m16.0
[fastapi] + h2[0m[91m==4.4.1[0m[91m
[fastapi] + hf-transfer==0.1.9
[fastapi] [0m[91m+ hf-xet==1.1.0[0m[91m
[fastapi] [0m[91m+ [0m[91mhpack[0m[91m==4.2.0
[fastapi] + hqq[0m[91m==0.2.5
[fastapi] +[0m[91m httpcore[0m[91m==1.0[0m[91m.9
[fastapi] + httpx==0[0m[91m.28.1
[fastapi] + [0m[91mhuggingface-hub==0.31[0m[91m.0
[fastapi] +[0m[91m humanfriendly==10.0[0m[91m
[fastapi] + hyperframe[0m[91m==6.1.[0m[91m0[0m[91m
[fastapi] [0m[91m+[0m[91m idna==3.19
[fastapi] + [0m[91mimmutabledict==4.[0m[91m2.0
[fastapi] + [0m[91misodate==0.[0m[91m7.2
[fastapi] +[0m[91m jinja2==3.1.6[0m[91m
[fastapi] + [0m[91mjmespath==1.1.0[0m[91m
[fastapi] + [0m[91mjoblib==1.6.0[0m[91m
[fastapi] +[0m[91m jsonlines==[0m[91m4.0.0
[fastapi] [0m[91m+ langdetect[0m[91m==1.0.9[0m[91m
[fastapi] +[0m[91m liger-kernel[0m[91m==0.5.9
[fastapi] + llvmlite==0.49.0[0m[91m
[fastapi] + [0m[91mlm-eval==0.4[0m[91m.7
[fastapi] [0m[91m +[0m[91m lxml==6[0m[91m.1.3
[fastapi] + markdown==3.10.[0m[91m3
[fastapi] + markdown-it-py[0m[91m==4.2.[0m[91m0
[fastapi] + markupsafe==3.0[0m[91m.3
[fastapi] [0m[91m [0m[91m+ mbstrdecoder[0m[91m==1.1.5
[fastapi] + [0m[91mmdurl==0.1.2[0m[91m
[fastapi] [0m[91m+ modal==0.70.[0m[91m5
[fastapi] [0m[91m+[0m[91m more-itertools==11.[0m[91m1.0
[fastapi] + mpmath==[0m[91m1.3.0
[fastapi] [0m[91m+ msal==1[0m[91m.38[0m[91m.0
[fastapi] [0m[91m [0m[91m+ [0m[91mmsal-extensions==1.3.1[0m[91m
[fastapi] + multidict==6.8.[0m[91m0
[fastapi] + multiprocess[0m[91m==0.70[0m[91m.16[0m[91m
[fastapi] +[0m[91m networkx==3.[0m[91m6.1
[fastapi] + nltk==3.10.[0m[91m3
[fastapi] + numba[0m[91m==0.67[0m[91m.0
[fastapi] +[0m[91m numexpr==2[0m[91m.14.2
[fastapi] + numpy==2[0m[91m.0.1
[fastapi] +[0m[91m nvidia-cublas-cu12==12[0m[91m.4.5.8[0m[91m
[fastapi] + nvidia-cuda-cupti-cu12==12.4[0m[91m.127
[fastapi] [0m[91m + [0m[91mnvidia-cuda-nvrtc-cu12[0m[91m==12.4.[0m[91m127
[fastapi] [0m[91m+[0m[91m nvidia-cuda-runtime-cu12==12[0m[91m.4.127
[fastapi] +[0m[91m nvidia-cudnn-cu12[0m[91m==9.1.0.70
[fastapi] + nvidia-cufft-cu12[0m[91m==11.2.1.3[0m[91m
[fastapi] + nvidia-curand-cu12==10[0m[91m.3.5[0m[91m.147
[fastapi] [0m[91m [0m[91m+ nvidia-cusolver-cu12[0m[91m==[0m[91m11.6.[0m[91m1.9
[fastapi] [0m[91m + nvidia-cusparse-cu12==12.3.1.170
[fastapi] + nvidia-cusparselt-cu12==0.6.2
[fastapi] +[0m[91m nvidia-ml-py==12.560.30[0m[91m
[fastapi] + nvidia-nccl-cu12==[0m[91m2.21.5
[fastapi] [0m[91m+ nvidia-nvjitlink-cu12==12.4.[0m[91m127
[fastapi] + [0m[91mnvidia-nvtx-cu12==12[0m[91m.4.127
[fastapi] [0m[91m + oauthlib==[0m[91m3.3.1[0m[91m
[fastapi] +[0m[91m oci==2.186[0m[91m.0
[fastapi] + ocifs[0m[91m==1.3.[0m[91m2
[fastapi] +[0m[91m opentelemetry-api==1[0m[91m.44.0
[fastapi] [0m[91m + opentelemetry-exporter-otlp-proto-common[0m[91m==1.[0m[91m44.0
[fastapi] [0m[91m+ opentelemetry-exporter-otlp-proto-http[0m[91m==1.[0m[91m44.0
[fastapi] + [0m[91mopentelemetry-proto==1[0m[91m.44.0[0m[91m
[fastapi] [0m[91m+[0m[91m opentelemetry-sdk[0m[91m==1.[0m[91m44.0[0m[91m
[fastapi] [0m[91m + [0m[91mopentelemetry-semantic-conventions==0.65b0
[fastapi] +[0m[91m optimum[0m[91m==1.[0m[91m16.2
[fastapi] +[0m[91m orjson[0m[91m==3.[0m[91m12.[0m[91m0
[fastapi] + pandas==2.3.3
[fastapi] +[0m[91m pathvalidate==3.3.1
[fastapi] [0m[91m+ [0m[91mpeft==[0m[91m0.15.[0m[91m2
[fastapi] + pillow==11.3.0
[fastapi] [0m[91m + platformdirs==4[0m[91m.11.8
[fastapi] [0m[91m + portalocker==4[0m[91m.3.2
[fastapi] +[0m[91m propcache==0.5[0m[91m.4
[fastapi] +[0m[91m proto-plus==1.28.2[0m[91m
[fastapi] + protobuf==5.[0m[91m29.[0m[91m6
[fastapi] [0m[91m+[0m[91m psutil[0m[91m==7.2[0m[91m.2
[fastapi] + [0m[91mpyarrow==25.0[0m[91m.1[0m[91m
[fastapi] [0m[91m+ [0m[91mpyasn1==0[0m[91m.[0m[91m6.4
[fastapi] + pyasn1-modules==0.4.2[0m[91m
[fastapi] [0m[91m+ [0m[91mpybind11==3[0m[91m.1[0m[91m.0
[fastapi] [0m[91m+[0m[91m pycparser[0m[91m==3[0m[91m.0
[fastapi] [0m[91m+ [0m[91mpydantic==2[0m[91m.10.6[0m[91m
[fastapi] [0m[91m +[0m[91m pydantic-core==[0m[91m2.[0m[91m27[0m[91m.2
[fastapi] [0m[91m+[0m[91m pydub[0m[91m==0.25.1
[fastapi] + pygments==2.21[0m[91m.0
[fastapi] + pyjwt[0m[91m==2.14[0m[91m.[0m[91m0
[fastapi] +[0m[91m [0m[91mpyopenssl==26[0m[91m.4[0m[91m.[0m[91m0
[fastapi] +[0m[91m pytablewriter[0m[91m==1.2.1
[fastapi] + python-dateutil[0m[91m==2.9.0.post0
[fastapi] [0m[91m+ python-dotenv==1.[0m[91m0.1
[fastapi] [0m[91m+ python-multipart[0m[91m==0.0.[0m[91m32
[fastapi] [0m[91m+ pytz[0m[91m==2026.3.post[0m[91m1
[fastapi] +[0m[91m pyyaml==6.[0m[91m0.3
[fastapi] [0m[91m + regex[0m[91m==2026.9.10
[fastapi] [0m[91m+ requests[0m[91m==2.34.2
[fastapi] + requests-oauthlib==2.0[0m[91m.0
[fastapi] + responses==0[0m[91m.18.0[0m[91m
[fastapi] [0m[91m+[0m[91m rich==[0m[91m15.0.0
[fastapi] [0m[91m+ rouge-score[0m[91m==0.1.2
[fastapi] + [0m[91mruff==0.16.7[0m[91m
[fastapi] +[0m[91m s3fs[0m[91m==2025[0m[91m.3.0[0m[91m
[fastapi] [0m[91m+ [0m[91msacrebleu==2.6.[0m[91m0
[fastapi] + safehttpx[0m[91m==0.1.7
[fastapi] [0m[91m+ safetensors==0.[0m[91m8.0
[fastapi] + schedulefree==[0m[91m1.4.1
[fastapi] + scikit-learn[0m[91m==1.4.[0m[91m2
[fastapi] + scipy==1.17.[0m[91m1
[fastapi] +[0m[91m [0m[91msemantic-version==2.10[0m[91m.[0m[91m0
[fastapi] +[0m[91m sentencepiece[0m[91m==[0m[91m0.2.2[0m[91m
[fastapi] [0m[91m+ shellingham==1.5.4[0m[91m
[fastapi] + sigtools[0m[91m==4.0[0m[91m.1
[fastapi] +[0m[91m six==[0m[91m1.17.[0m[91m0
[fastapi] +[0m[91m sqlitedict==2[0m[91m.1.0[0m[91m
[fastapi] + [0m[91mstarlette==0[0m[91m.52.1
[fastapi] [0m[91m + sympy==1.[0m[91m13.1
[fastapi] [0m[91m + synchronicity==[0m[91m0.9.[0m[91m16
[fastapi] [0m[91m [0m[91m+[0m[91m tabledata==1[0m[91m.3.5
[fastapi] + tabulate[0m[91m==0.10.0[0m[91m
[fastapi] +[0m[91m tcolorpy==0.[0m[91m1.7
[fastapi] [0m[91m + tensorboard==2.[0m[91m20.0
[fastapi] + tensorboard-data-server==[0m[91m0.7.2[0m[91m
[fastapi] +[0m[91m termcolor[0m[91m==3.3[0m[91m.0
[fastapi] + threadpoolctl[0m[91m==3.7.0
[fastapi] [0m[91m +[0m[91m [0m[91mtokenizers==[0m[91m0.[0m[91m21[0m[91m.4[0m[91m
[fastapi] +[0m[91m [0m[91mtoml[0m[91m==[0m[91m0.10[0m[91m.[0m[91m2[0m[91m
[fastapi] [0m[91m + [0m[91mtomlkit==[0m[91m0.13.3[0m[91m
[fastapi] + torch==[0m[91m2.6.[0m[91m0
[fastapi] [0m[91m + torchao[0m[91m==0.9.0
[fastapi] + [0m[91mtqdm==4.70.1[0m[91m
[fastapi] +[0m[91m [0m[91mtqdm-multiprocess==0[0m[91m.0.11[0m[91m
[fastapi] + transformers==4.[0m[91m51.3
[fastapi] [0m[91m+ triton==3.2[0m[91m.0
[fastapi] + [0m[91mtrl==0.17[0m[91m.0
[fastapi] [0m[91m + typepy[0m[91m==1.3[0m[91m.5
[fastapi] +[0m[91m typer==0.27.2
[fastapi] [0m[91m + types-certifi[0m[91m==2021.10[0m[91m.8.3
[fastapi] + types-toml==0.10.8.20260518
[fastapi] + typing-extensions==4.16.0
[fastapi] + typing-inspection==0.4.4
[fastapi] + tzdata==2026.4
[fastapi] + urllib3==2.8.0
[fastapi] + uvicorn==0.53.0
[fastapi] + wandb==0.30.0
[fastapi] + watchfiles==1.2.0
[fastapi] + websockets==15.0.1
[fastapi] + werkzeug==3.1.8
[fastapi] + word2number==1.1
[fastapi] + wrapt==1.17.3
[fastapi] + xformers==0.0.29.post2
[fastapi] + xxhash==4.0.1
[fastapi] + yarl==1.25.1
[fastapi] + zstandard==0.22.0
[fastapi] [0mCollecting requests==2.32.3
[fastapi] Downloading requests-2.32.3-py3-none-any.whl.metadata (4.6 kB)
[fastapi] Requirement already satisfied: charset-normalizer<4,>=2 in /workspace/axo_py/lib/python3.11/site-packages (from requests==2.32.3) (3.5.1)
[fastapi] Requirement already satisfied: idna<4,>=2.5 in /workspace/axo_py/lib/python3.11/site-packages (from requests==2.32.3) (3.19)
[fastapi] Requirement already satisfied: urllib3<3,>=1.21.1 in /workspace/axo_py/lib/python3.11/site-packages (from requests==2.32.3) (2.8.0)
[fastapi] Requirement already satisfied: certifi>=2017.4.17 in /workspace/axo_py/lib/python3.11/site-packages (from requests==2.32.3) (2026.7.22)
[fastapi] Downloading requests-2.32.3-py3-none-any.whl (64 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 64.9/64.9 kB 3.4 MB/s eta 0:00:00
[fastapi] Installing collected packages: requests
[fastapi] Attempting uninstall: requests
[fastapi] Found existing installation: requests 2.34.2
[fastapi] Uninstalling requests-2.34.2:
[fastapi] Successfully uninstalled requests-2.34.2
[fastapi] [91mERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
[fastapi] google-api-core 2.33.0 requires requests<3.0.0,>=2.33.0, but you have requests 2.32.3 which is incompatible.
[fastapi] [0mSuccessfully installed requests-2.32.3
[fastapi] [91m
[fastapi] [notice] A new release of pip is available: 24.0 -> 26.2.1
[fastapi] [notice] To update, run: pip install --upgrade pip
[fastapi] [0m ---> 4fa20d6b783f
[fastapi] Step 12/13 : RUN pip install uv &&     pip install -U packaging==23.2 setuptools==75.8.0 wheel ninja &&     uv pip install -r /workspace/scripts/training_requirements.txt --system &&     pip install hf_transfer==0.1.9 &&     pip install tenacity==9.1.2 &&     pip install tiktoken==0.9.0 &&     pip install flash-attn==v2.7.4.post1 --no-build-isolation &&     uv pip install vllm==0.8.3 --system &&     pip install "fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0"
[fastapi] ---> Running in ece260593556
[fastapi] Collecting uv
[fastapi] Using cached uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] Using cached uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.1 MB)
[fastapi] Installing collected packages: uv
[fastapi] Successfully installed uv-0.12.15
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0mCollecting packaging==23.2
[fastapi] Using cached packaging-23.2-py3-none-any.whl.metadata (3.2 kB)
[fastapi] Collecting setuptools==75.8.0
[fastapi] Using cached setuptools-75.8.0-py3-none-any.whl.metadata (6.7 kB)
[fastapi] Requirement already satisfied: wheel in /usr/local/lib/python3.11/dist-packages (0.44.0)
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
[fastapi] Attempting uninstall: wheel
[fastapi] Found existing installation: wheel 0.44.0
[fastapi] Uninstalling wheel-0.44.0:
[fastapi] Successfully uninstalled wheel-0.44.0
[fastapi] Attempting uninstall: setuptools
[fastapi] Found existing installation: setuptools 75.1.0
[fastapi] Uninstalling setuptools-75.1.0:
[fastapi] Successfully uninstalled setuptools-75.1.0
[fastapi] Attempting uninstall: packaging
[fastapi] Found existing installation: packaging 24.1
[fastapi] Uninstalling packaging-24.1:
[fastapi] Successfully uninstalled packaging-24.1
[fastapi] Successfully installed ninja-1.13.2 packaging-23.2 setuptools-75.8.0 wheel-0.45.1
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0m[91mUsing Python 3.11.10 environment at: /usr
[fastapi] [0m[91mResolved 187 packages in 1.57s
[fastapi] [0m[91m   Building antlr4-python3-runtime==4.9.3
[fastapi] [0m[91m   Building deepspeed==0.15.4
[fastapi] [0m[91mDownloading fonttools (5.2MiB)
[fastapi] [0m[91mDownloading pydantic-core (2.0MiB)
[fastapi] [0m[91mDownloading sqlalchemy (3.3MiB)
[fastapi] [0m[91mDownloading tensorboard (5.2MiB)
[fastapi] [0m[91mDownloading scipy (35.9MiB)
[fastapi] [0m[91mDownloading scikit-learn (8.9MiB)
[fastapi] [0m[91mDownloading plotly (9.2MiB)
[fastapi] [0m[91mDownloading openai (1.9MiB)
[fastapi] [0m[91mDownloading matplotlib (9.4MiB)
[fastapi] [0m[91mDownloading pycryptodome (2.2MiB)
[fastapi] [0m[91mDownloading mlflow (11.0MiB)
[fastapi] [0m[91mDownloading kiwisolver (1.4MiB)
[fastapi] [0m[91mDownloading hf-xet (4.3MiB)
[fastapi] [0m[91mDownloading pyphen (2.0MiB)
[fastapi] [0m[91mDownloading wandb (20.4MiB)
[fastapi] [0m[91mDownloading mlflow-skinny (3.5MiB)
[fastapi] [0m[91mDownloading pandas (12.5MiB)
[fastapi] [0m[91mDownloading sentencepiece (1.2MiB)
[fastapi] [0m[91mDownloading mlflow-tracing (1.7MiB)
[fastapi] [0m[91mDownloading dash (8.5MiB)
[fastapi] [0m[91mDownloading mpi4py (1.3MiB)
[fastapi] [0m[91m Downloaded sentencepiece
[fastapi] [0m[91m Downloaded mpi4py
[fastapi] [0m[91m Downloaded kiwisolver
[fastapi] [0m[91m Downloaded mlflow-tracing
[fastapi] [0m[91m Downloaded pydantic-core
[fastapi] [0m[91m Downloaded pyphen
[fastapi] [0m[91m Downloaded pycryptodome
[fastapi] [0m[91m Downloaded sqlalchemy
[fastapi] [0m[91m Downloaded openai
[fastapi] [0m[91m Downloaded mlflow-skinny
[fastapi] [0m[91m Downloaded hf-xet
[fastapi] [0m[91m      Built antlr4-python3-runtime==4.9.3
[fastapi] [0m[91m Downloaded tensorboard
[fastapi] [0m[91m Downloaded fonttools
[fastapi] [0m[91m Downloaded scikit-learn
[fastapi] [0m[91m Downloaded plotly
[fastapi] [0m[91m Downloaded dash
[fastapi] [0m[91m Downloaded matplotlib
[fastapi] [0m[91m Downloaded pandas
[fastapi] [0m[91m Downloaded mlflow
[fastapi] [0m[91m Downloaded wandb
[fastapi] [0m[91m Downloaded scipy
[fastapi] [0m[91m      Built deepspeed==0.15.4
[fastapi] [0m[91mPrepared 88 packages in 873ms
[fastapi] [0m[91mUninstalled 6 packages in 35ms
[fastapi] [0m[91mInstalled 141 packages in 3.30s
[fastapi] [0m[91m + absl-py==2.5.0
[fastapi] + accelerate==1.6.0
[fastapi] + aiohappyeyeballs==2.7.1
[fastapi] + aiohttp==3.14.3
[fastapi] + aiosignal==1.4.0[0m[91m
[fastapi] + alembic==1.20.0
[fastapi] + annotated-doc==0.[0m[91m0.5
[fastapi] + annotated-types==0.8.0
[fastapi] + antlr4-python3-runtime==4.9[0m[91m.3
[fastapi] - anyio==4.6.0
[fastapi] + anyio==4.[0m[91m15.1
[fastapi] +[0m[91m astor==0.8.[0m[91m1
[fastapi] [0m[91m +[0m[91m bitsandbytes==0.45.[0m[91m4
[fastapi] + [0m[91mblinker==1[0m[91m.9.0
[fastapi] [0m[91m + [0m[91mcachetools==[0m[91m7.1[0m[91m.8
[fastapi] [0m[91m - [0m[91mcffi==[0m[91m1.17[0m[91m.[0m[91m1
[fastapi] +[0m[91m cffi==2.1.1
[fastapi] + [0m[91mclick==8.5.[0m[91m0
[fastapi] + cloudpickle[0m[91m==3.1.2[0m[91m
[fastapi] + cmudict[0m[91m==1.1.[0m[91m3
[fastapi] + contourpy==1.3.3
[fastapi] [0m[91m+ cryptography[0m[91m==[0m[91m50.0.1
[fastapi] [0m[91m +[0m[91m [0m[91mcycler[0m[91m==0.12.1
[fastapi] + dash==4[0m[91m.4.1
[fastapi] [0m[91m+ [0m[91mdatabricks-sdk==0[0m[91m.139.0[0m[91m
[fastapi] [0m[91m + [0m[91mdatasets==3[0m[91m.5.[0m[91m0
[fastapi] + deepspeed==0.15.[0m[91m4
[fastapi] + [0m[91mdetoxify==0[0m[91m.5.2[0m[91m
[fastapi] [0m[91m+ dill==0.3.8
[fastapi] + docker==[0m[91m7.2.0
[fastapi] + docker-pycreds==[0m[91m0.4.0[0m[91m
[fastapi] [0m[91m+ [0m[91meinops==0[0m[91m.8.[0m[91m1[0m[91m
[fastapi] [0m[91m+ fastapi==0.141.1
[fastapi] + flask==3[0m[91m.1.3
[fastapi] + flask-cors==6.0[0m[91m.5
[fastapi] [0m[91m+ fonttools==4.65[0m[91m.0
[fastapi] + frozenlist[0m[91m==1.8.0
[fastapi] + gdown[0m[91m==6.2.0
[fastapi] [0m[91m + gitdb[0m[91m==4.0.12
[fastapi] + gitpython==3[0m[91m.1.62
[fastapi] + google-auth==2.58.0
[fastapi] + graphene==[0m[91m3.4.3
[fastapi] [0m[91m + graphql-core==3.2.12[0m[91m
[fastapi] + graphql-relay==3.2.0
[fastapi] + greenlet==3.5.6
[fastapi] + grpcio==1.84.0
[fastapi] +[0m[91m gunicorn==26.2.0[0m[91m
[fastapi] - h11==0.14[0m[91m.0
[fastapi] [0m[91m+ h11==0.16.0
[fastapi] + hf-xet==1[0m[91m.6.0
[fastapi] [0m[91m+ hjson[0m[91m==3.1.0[0m[91m
[fastapi] + httpcore2==2.13[0m[91m.0
[fastapi] + httpx2[0m[91m==2.13.[0m[91m0
[fastapi] + [0m[91mhuey==3.4[0m[91m.0
[fastapi] [0m[91m+ huggingface-hub==0.36.[0m[91m2
[fastapi] - idna[0m[91m==3.10[0m[91m
[fastapi] + [0m[91midna[0m[91m==3.19[0m[91m
[fastapi] [0m[91m+ importlib-metadata==[0m[91m9.[0m[91m0.1[0m[91m
[fastapi] +[0m[91m importlib-resources[0m[91m==7[0m[91m.1.[0m[91m0
[fastapi] [0m[91m+[0m[91m itsdangerous[0m[91m==2.[0m[91m2.0[0m[91m
[fastapi] [0m[91m +[0m[91m jaconv==0[0m[91m.[0m[91m5.0[0m[91m
[fastapi] [0m[91m + janus[0m[91m==2[0m[91m.0.[0m[91m0[0m[91m
[fastapi] +[0m[91m jiter[0m[91m==0.[0m[91m17[0m[91m.0
[fastapi] [0m[91m+[0m[91m joblib==[0m[91m1.[0m[91m6.0
[fastapi] [0m[91m [0m[91m+ kiwisolver[0m[91m==1.5.1
[fastapi] + langcheck==[0m[91m0.9.0
[fastapi] [0m[91m+ liger-kernel==0.5.[0m[91m9
[fastapi] +[0m[91m mako==[0m[91m1.[0m[91m4.1
[fastapi] [0m[91m+[0m[91m markdown[0m[91m==3.10.3
[fastapi] [0m[91m+ matplotlib==3.[0m[91m11.2
[fastapi] [0m[91m+[0m[91m minio[0m[91m==7.2[0m[91m.20[0m[91m
[fastapi] [0m[91m + mlflow[0m[91m==[0m[91m3.16.0[0m[91m
[fastapi] +[0m[91m mlflow-skinny[0m[91m==3.16[0m[91m.0
[fastapi] [0m[91m + mlflow-tracing[0m[91m==3[0m[91m.[0m[91m16.0
[fastapi] [0m[91m + [0m[91mmpi4py[0m[91m==4[0m[91m.1[0m[91m.2
[fastapi] [0m[91m [0m[91m+ msgpack[0m[91m==1[0m[91m.[0m[91m2.2
[fastapi] [0m[91m+ [0m[91mmultidict==6.[0m[91m8.0[0m[91m
[fastapi] [0m[91m + multiprocess==0.70.16
[fastapi] + narwhals[0m[91m==2.26.0
[fastapi] + [0m[91mnlpaug==1.1.11
[fastapi] [0m[91m + nltk==3.10[0m[91m.3
[fastapi] [0m[91m+ omegaconf[0m[91m==2.3.1
[fastapi] +[0m[91m openai==[0m[91m3.14[0m[91m.1
[fastapi] [0m[91m+ opentelemetry-api==1.44.0
[fastapi] + opentelemetry-proto==[0m[91m1.44.0
[fastapi] [0m[91m+ opentelemetry-sdk==1.44[0m[91m.0
[fastapi] +[0m[91m opentelemetry-semantic-conventions==[0m[91m0[0m[91m.65b[0m[91m0[0m[91m
[fastapi] [0m[91m+ [0m[91mpandas==2.[0m[91m2.[0m[91m3
[fastapi] +[0m[91m [0m[91mpeft[0m[91m==0.15.1
[fastapi] + plotly==7.1[0m[91m.0
[fastapi] + prettytable==[0m[91m3.18.0[0m[91m
[fastapi] + propcache[0m[91m==0.5.4
[fastapi] + protobuf==[0m[91m6.33.6
[fastapi] +[0m[91m [0m[91mpy-cpuinfo==9[0m[91m.0.[0m[91m0[0m[91m
[fastapi] + pyarrow==25[0m[91m.[0m[91m0.1
[fastapi] [0m[91m+[0m[91m pyasn1[0m[91m==[0m[91m0.[0m[91m6.4
[fastapi] [0m[91m+ pyasn1-modules[0m[91m==0.4.2
[fastapi] + pycryptodome==3.23.0
[fastapi] [0m[91m + pydantic==2.[0m[91m13.5
[fastapi] [0m[91m + pydantic-core[0m[91m==[0m[91m2.46.5[0m[91m
[fastapi] [0m[91m+[0m[91m pyparsing[0m[91m==3.3[0m[91m.2
[fastapi] +[0m[91m pyphen==0.18.1
[fastapi] + pysocks==1.7.1
[fastapi] [0m[91m + [0m[91mpython-dotenv==[0m[91m1.2.3
[fastapi] [0m[91m + pytz==2026.3.post1[0m[91m
[fastapi] [0m[91m+ regex[0m[91m==2026.[0m[91m9.[0m[91m10
[fastapi] [0m[91m+ [0m[91mrestrictedpython==[0m[91m8.0
[fastapi] + retrying==1.4.2
[fastapi] [0m[91m + rouge-score==0.1.[0m[91m2
[fastapi] + safetensors==0.8.[0m[91m0
[fastapi] + scikit-learn[0m[91m==1.9.1
[fastapi] [0m[91m [0m[91m+ scipy==[0m[91m1.15.2
[fastapi] [0m[91m + sentence-transformers==5.7.0
[fastapi] [0m[91m + sentencepiece==0[0m[91m.2.0
[fastapi] [0m[91m + sentry-sdk==2.69[0m[91m.2
[fastapi] [0m[91m + setproctitle==1[0m[91m.3[0m[91m.7[0m[91m
[fastapi] [0m[91m+[0m[91m six==1.17.0
[fastapi] +[0m[91m skops==0[0m[91m.14.0
[fastapi] +[0m[91m smmap==5.0.3
[fastapi] + sqlalchemy[0m[91m==2.0.54
[fastapi] [0m[91m + sqlparse[0m[91m==0.6.0
[fastapi] + starlette==1[0m[91m.6.0
[fastapi] +[0m[91m tabulate==0[0m[91m.10.0
[fastapi] [0m[91m+ tenacity==9.1.4
[fastapi] + [0m[91mtensorboard==2.[0m[91m19.[0m[91m0
[fastapi] + tensorboard-data-server[0m[91m==0[0m[91m.7.2[0m[91m
[fastapi] + textstat==0.7.8
[fastapi] + threadpoolctl==[0m[91m3.7.0
[fastapi] + tokenizers[0m[91m==0.21.4
[fastapi] + [0m[91mtoml==0.[0m[91m10.2[0m[91m
[fastapi] +[0m[91m tqdm[0m[91m==[0m[91m4.70.[0m[91m1[0m[91m
[fastapi] +[0m[91m [0m[91mtransformers==4[0m[91m.51.3
[fastapi] + trl==0.18.0
[fastapi] + truststore==0.10.4
[fastapi] + typer==0.9.0
[fastapi] - typing-extensions==4.9.0
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
[fastapi] [0mCollecting hf_transfer==0.1.9
[fastapi] Downloading hf_transfer-0.1.9-cp38-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (1.7 kB)
[fastapi] Downloading hf_transfer-0.1.9-cp38-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.6 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.6/3.6 MB 216.4 MB/s eta 0:00:00
[fastapi] Installing collected packages: hf_transfer
[fastapi] Successfully installed hf_transfer-0.1.9
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0mCollecting tenacity==9.1.2
[fastapi] Downloading tenacity-9.1.2-py3-none-any.whl.metadata (1.2 kB)
[fastapi] Downloading tenacity-9.1.2-py3-none-any.whl (28 kB)
[fastapi] Installing collected packages: tenacity
[fastapi] Attempting uninstall: tenacity
[fastapi] Found existing installation: tenacity 9.1.4
[fastapi] Uninstalling tenacity-9.1.4:
[fastapi] Successfully uninstalled tenacity-9.1.4
[fastapi] Successfully installed tenacity-9.1.2
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0mCollecting tiktoken==0.9.0
[fastapi] Downloading tiktoken-0.9.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.7 kB)
[fastapi] Requirement already satisfied: regex>=2022.1.18 in /usr/local/lib/python3.11/dist-packages (from tiktoken==0.9.0) (2026.9.10)
[fastapi] Requirement already satisfied: requests>=2.26.0 in /usr/local/lib/python3.11/dist-packages (from tiktoken==0.9.0) (2.32.3)
[fastapi] Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.11/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (3.3.2)
[fastapi] Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.11/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (3.19)
[fastapi] Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.11/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (2.2.3)
[fastapi] Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.11/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (2024.8.30)
[fastapi] Downloading tiktoken-0.9.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (1.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 109.0 MB/s eta 0:00:00
[fastapi] Installing collected packages: tiktoken
[fastapi] Successfully installed tiktoken-0.9.0
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0mCollecting flash-attn==v2.7.4.post1
[fastapi] Downloading flash_attn-2.7.4.post1.tar.gz (6.0 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.0/6.0 MB 170.5 MB/s eta 0:00:00
[fastapi] Preparing metadata (setup.py): started
[fastapi] Preparing metadata (setup.py): finished with status 'done'
[fastapi] Requirement already satisfied: torch in /usr/local/lib/python3.11/dist-packages (from flash-attn==v2.7.4.post1) (2.4.1+cu124)
[fastapi] Requirement already satisfied: einops in /usr/local/lib/python3.11/dist-packages (from flash-attn==v2.7.4.post1) (0.8.1)
[fastapi] Requirement already satisfied: filelock in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (3.13.1)
[fastapi] Requirement already satisfied: typing-extensions>=4.8.0 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (4.16.0)
[fastapi] Requirement already satisfied: sympy in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (1.12)
[fastapi] Requirement already satisfied: networkx in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (3.2.1)
[fastapi] Requirement already satisfied: jinja2 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (3.1.3)
[fastapi] Requirement already satisfied: fsspec in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (2024.2.0)
[fastapi] Requirement already satisfied: nvidia-cuda-nvrtc-cu12==12.4.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (12.4.99)
[fastapi] Requirement already satisfied: nvidia-cuda-runtime-cu12==12.4.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (12.4.99)
[fastapi] Requirement already satisfied: nvidia-cuda-cupti-cu12==12.4.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (12.4.99)
[fastapi] Requirement already satisfied: nvidia-cudnn-cu12==9.1.0.70 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (9.1.0.70)
[fastapi] Requirement already satisfied: nvidia-cublas-cu12==12.4.2.65 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (12.4.2.65)
[fastapi] Requirement already satisfied: nvidia-cufft-cu12==11.2.0.44 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (11.2.0.44)
[fastapi] Requirement already satisfied: nvidia-curand-cu12==10.3.5.119 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (10.3.5.119)
[fastapi] Requirement already satisfied: nvidia-cusolver-cu12==11.6.0.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (11.6.0.99)
[fastapi] Requirement already satisfied: nvidia-cusparse-cu12==12.3.0.142 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (12.3.0.142)
[fastapi] Requirement already satisfied: nvidia-nccl-cu12==2.20.5 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (2.20.5)
[fastapi] Requirement already satisfied: nvidia-nvtx-cu12==12.4.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (12.4.99)
[fastapi] Requirement already satisfied: nvidia-nvjitlink-cu12==12.4.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (12.4.99)
[fastapi] Requirement already satisfied: triton==3.0.0 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (3.0.0)
[fastapi] Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.11/dist-packages (from jinja2->torch->flash-attn==v2.7.4.post1) (2.1.5)
[fastapi] Requirement already satisfied: mpmath>=0.19 in /usr/local/lib/python3.11/dist-packages (from sympy->torch->flash-attn==v2.7.4.post1) (1.3.0)
[fastapi] Building wheels for collected packages: flash-attn
[fastapi] Building wheel for flash-attn (setup.py): started
[fastapi] Building wheel for flash-attn (setup.py): finished with status 'done'
[fastapi] Created wheel for flash-attn: filename=flash_attn-2.7.4.post1-cp311-cp311-linux_x86_64.whl size=187805408 sha256=92cf49e6f66795b6934cec0cba526ed6e45d3313de3f905d45df8773f19092a9
[fastapi] Stored in directory: /root/.cache/pip/wheels/3d/88/d8/284b89f56af7d5bf366b10d6b8e251ac8a7c7bf3f04203fb4f
[fastapi] Successfully built flash-attn
[fastapi] Installing collected packages: flash-attn
[fastapi] Successfully installed flash-attn-2.7.4.post1
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0m[91mUsing Python 3.11.10 environment at: /usr
[fastapi] [0m[91mResolved 142 packages in 806ms
[fastapi] [0m[91mDownloading mistral-common (6.2MiB)
[fastapi] [0m[91mDownloading pillow (6.6MiB)
[fastapi] [0m[91mDownloading uvloop (3.6MiB)
[fastapi] [0m[91mDownloading llguidance (14.3MiB)
[fastapi] [0m[91mDownloading numba (3.6MiB)
[fastapi] [0m[91mDownloading pycountry (7.7MiB)
[fastapi] [0m[91mDownloading numpy (15.6MiB)
[fastapi] [0m[91mDownloading xgrammar (4.1MiB)
[fastapi] [0m[91mDownloading opencv-python-headless (58.4MiB)
[fastapi] [0m[91mDownloading torchaudio (3.2MiB)
[fastapi] [0m[91mDownloading llvmlite (40.4MiB)
[fastapi] [0m[91mDownloading ray (74.7MiB)
[fastapi] [0m[91mDownloading torchvision (6.9MiB)
[fastapi] [0m[91mDownloading cupy-cuda12x (130.3MiB)
[fastapi] [0m[91mDownloading vllm (280.4MiB)
[fastapi] [0m[91m Downloaded torchaudio
[fastapi] [0m[91m Downloaded uvloop
[fastapi] [0m[91m Downloaded xgrammar
[fastapi] [0m[91m Downloaded numba
[fastapi] [0m[91m Downloaded mistral-common
[fastapi] [0m[91m Downloaded pillow
[fastapi] [0m[91m Downloaded torchvision
[fastapi] [0m[91m Downloaded pycountry
[fastapi] [0m[91m Downloaded llguidance
[fastapi] [0m[91m Downloaded numpy
[fastapi] [0m[91m Downloaded llvmlite
[fastapi] [0m[91m Downloaded opencv-python-headless
[fastapi] [0m[91m Downloaded ray
[fastapi] [0m[91m Downloaded cupy-cuda12x
[fastapi] [0m[91m Downloaded vllm
[fastapi] [0m[91mPrepared 45 packages in 3.05s
[fastapi] [0m[91mUninstalled 23 packages in 1.75s
[fastapi] [0m[91mInstalled 71 packages in 12.29s
[fastapi] [0m[91m + agent-detector==2.0.0
[fastapi] + airportsdata==20260905
[fastapi] + blake3==1[0m[91m.0.9
[fastapi] + [0m[91mcompressed-tensors==0.9[0m[91m.2
[fastapi] + cuda-pathfinder==[0m[91m1.8.1[0m[91m
[fastapi] + [0m[91mcupy-cuda12x==14.2[0m[91m.0
[fastapi] +[0m[91m depyf==0.[0m[91m18.0
[fastapi] [0m[91m + [0m[91mdetect-installer==0.2[0m[91m.1
[fastapi] [0m[91m+ diskcache==[0m[91m5.6.3
[fastapi] + dnspython==2.8.0
[fastapi] +[0m[91m email-validator==2.3.0
[fastapi] + fastapi-cli==0.0.32
[fastapi] [0m[91m + fastapi-cloud-cli==0.26.0
[fastapi] [0m[91m+ fastar==0.12.0
[fastapi] [0m[91m - filelock==3.13.[0m[91m1
[fastapi] +[0m[91m filelock==3.[0m[91m32.7
[fastapi] +[0m[91m gguf==0[0m[91m.10.0
[fastapi] [0m[91m- httpcore[0m[91m==1.0[0m[91m.5
[fastapi] [0m[91m+ httpcore==[0m[91m1.0.9[0m[91m
[fastapi] +[0m[91m httptools==0[0m[91m.8.0
[fastapi] [0m[91m + [0m[91minteregular==0.[0m[91m3.3
[fastapi] - jinja2[0m[91m==3.1.3
[fastapi] + [0m[91mjinja2==3.1.6
[fastapi] + [0m[91mlark==1.2[0m[91m.2
[fastapi] + [0m[91mllguidance==0.7.30
[fastapi] + llvmlite[0m[91m==0.44.0
[fastapi] + lm-format-enforcer==0.[0m[91m10.12
[fastapi] + markdown-it-py[0m[91m==4.2.0[0m[91m
[fastapi] + mdurl[0m[91m==0.[0m[91m1.2
[fastapi] +[0m[91m mistral-common==1.11[0m[91m.7
[fastapi] +[0m[91m [0m[91mmsgspec[0m[91m==0.21.[0m[91m1[0m[91m
[fastapi] +[0m[91m nanobind[0m[91m==[0m[91m3.0[0m[91m.1
[fastapi] [0m[91m [0m[91m+ [0m[91mnumba==[0m[91m0.61[0m[91m.0
[fastapi] [0m[91m - numpy[0m[91m==1.26.3[0m[91m
[fastapi] + numpy[0m[91m==2.[0m[91m1.3
[fastapi] [0m[91m- nvidia-cublas-cu12[0m[91m==12.4[0m[91m.2.65
[fastapi] [0m[91m+ nvidia-cublas-cu12[0m[91m==12.4.5.[0m[91m8
[fastapi] -[0m[91m nvidia-cuda-cupti-cu12[0m[91m==12.4.99
[fastapi] [0m[91m+ nvidia-cuda-cupti-cu12==12.4[0m[91m.127
[fastapi] - [0m[91mnvidia-cuda-nvrtc-cu12==12.[0m[91m4.99
[fastapi] [0m[91m+ [0m[91mnvidia-cuda-nvrtc-cu12[0m[91m==12.4[0m[91m.127
[fastapi] [0m[91m -[0m[91m [0m[91mnvidia-cuda-runtime-cu12==12.4.99
[fastapi] +[0m[91m nvidia-cuda-runtime-cu12==12.4[0m[91m.127
[fastapi] - [0m[91mnvidia-cufft-cu12==11.[0m[91m2.0.44[0m[91m
[fastapi] + [0m[91mnvidia-cufft-cu12==11[0m[91m.2.1.[0m[91m3
[fastapi] -[0m[91m nvidia-curand-cu12==[0m[91m10.3.[0m[91m5.119
[fastapi] +[0m[91m nvidia-curand-cu12==10[0m[91m.3.5.[0m[91m147
[fastapi] -[0m[91m nvidia-cusolver-cu12==11.[0m[91m6.0.99
[fastapi] + nvidia-cusolver-cu12==11.[0m[91m6.1.9
[fastapi] [0m[91m- nvidia-cusparse-cu12==[0m[91m12.3[0m[91m.[0m[91m0.142
[fastapi] [0m[91m [0m[91m+ nvidia-cusparse-cu12[0m[91m==[0m[91m12.3.1[0m[91m.170
[fastapi] + nvidia-cusparselt-cu12==0.6.2
[fastapi] - nvidia-nccl-cu12==2.20.5
[fastapi] + nvidia-nccl-cu12==2[0m[91m.21.5
[fastapi] [0m[91m- nvidia-nvjitlink-cu12==[0m[91m12.4.99
[fastapi] [0m[91m + nvidia-nvjitlink-cu12[0m[91m==12.4.127
[fastapi] - nvidia-nvtx-cu12==[0m[91m12.4.99
[fastapi] + nvidia-nvtx-cu12[0m[91m==12.4.[0m[91m127
[fastapi] [0m[91m+ opencv-python-headless[0m[91m==5.0[0m[91m.0.93
[fastapi] [0m[91m+ outlines==0.1.11
[fastapi] [0m[91m + outlines-core==0[0m[91m.1.26
[fastapi] [0m[91m - packaging[0m[91m==23.2
[fastapi] [0m[91m + [0m[91mpackaging==26.3[0m[91m
[fastapi] + partial-json-parser[0m[91m==0.2.[0m[91m1.1.post[0m[91m7
[fastapi] - pillow[0m[91m==10.2[0m[91m.[0m[91m0
[fastapi] [0m[91m+ pillow==12.3[0m[91m.0
[fastapi] [0m[91m+[0m[91m prometheus-fastapi-instrumentator==8[0m[91m.[0m[91m1.0
[fastapi] [0m[91m [0m[91m+ pycountry==[0m[91m26[0m[91m.2.16[0m[91m
[fastapi] + [0m[91mpydantic-extra-types[0m[91m==2.11.[0m[91m1[0m[91m
[fastapi] + [0m[91mpydantic-settings[0m[91m==2[0m[91m.15.[0m[91m0[0m[91m
[fastapi] + [0m[91mpython-multipart[0m[91m==0[0m[91m.0.[0m[91m32[0m[91m
[fastapi] +[0m[91m ray[0m[91m==2.58.0
[fastapi] + rich==[0m[91m15.0.0
[fastapi] +[0m[91m rich-toolkit==0[0m[91m.20.5
[fastapi] [0m[91m + rignore[0m[91m==0.8.1
[fastapi] + [0m[91mshellingham==1.[0m[91m5.4
[fastapi] [0m[91m- sympy==[0m[91m1.12
[fastapi] + sympy[0m[91m==1.13.1
[fastapi] [0m[91m- [0m[91mtorch==2[0m[91m.4.[0m[91m1+[0m[91mcu124
[fastapi] + torch==2.6.0
[fastapi] [0m[91m - torchaudio==[0m[91m2.4.1[0m[91m+cu124
[fastapi] +[0m[91m torchaudio==2[0m[91m.6.0
[fastapi] [0m[91m - torchvision[0m[91m==0.19.1+cu124[0m[91m
[fastapi] + torchvision[0m[91m==0.21.0[0m[91m
[fastapi] - triton==[0m[91m3.0.0[0m[91m
[fastapi] + [0m[91mtriton[0m[91m==3.2[0m[91m.0[0m[91m
[fastapi] -[0m[91m [0m[91mtyper==[0m[91m0.9[0m[91m.0[0m[91m
[fastapi] [0m[91m+[0m[91m typer[0m[91m==0[0m[91m.27.[0m[91m2
[fastapi] + [0m[91muvloop==0.22.1
[fastapi] [0m[91m+ vllm==0.8.3[0m[91m
[fastapi] + watchfiles[0m[91m==1.2.0[0m[91m
[fastapi] + [0m[91mwebsockets==17.1[0m[91m
[fastapi] + xformers==0.[0m[91m0.29.post2[0m[91m
[fastapi] + [0m[91mxgrammar==0.[0m[91m1.17
[fastapi] [0mCollecting fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0
[fastapi] Cloning https://github.com/rayonlabs/fiber.git (to revision 2.4.0) to /tmp/pip-install-94u0ddar/fiber_647533016526496a9d777cb5f7c55d81
[fastapi] [91m  Running command git clone --filter=blob:none --quiet https://github.com/rayonlabs/fiber.git /tmp/pip-install-94u0ddar/fiber_647533016526496a9d777cb5f7c55d81
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
[fastapi] Requirement already satisfied: certifi>=2019.3.9 in /usr/local/lib/python3.11/dist-packages (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2024.8.30)
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
[fastapi] Requirement already satisfied: websockets>=14.1 in /usr/local/lib/python3.11/dist-packages (from async-substrate-interface<2.0.0,>=1.0.0->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (17.1)
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
[fastapi] Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.11/dist-packages (from requests<3,>=2.21.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (3.3.2)
[fastapi] Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.11/dist-packages (from requests<3,>=2.21.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2.2.3)
[fastapi] Requirement already satisfied: more-itertools in /usr/lib/python3/dist-packages (from scalecodec<1.3,>=1.2.10->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (8.10.0)
[fastapi] Requirement already satisfied: pycparser in /usr/local/lib/python3.11/dist-packages (from cffi>=2.0.0->PyNaCl<2,>=1.0.1->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2.22)
[fastapi] Collecting toolz>=0.8.0 (from cytoolz>=0.10.1->eth-utils<3,>=1.3.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading toolz-1.1.0-py3-none-any.whl.metadata (5.1 kB)
[fastapi] Downloading bittensor_commit_reveal-0.1.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (552 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 552.2/552.2 kB 51.2 MB/s eta 0:00:00
[fastapi] Downloading eth_typing-5.0.0-py3-none-any.whl (20 kB)
[fastapi] Downloading netaddr-1.3.0-py3-none-any.whl (2.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.3/2.3 MB 192.0 MB/s eta 0:00:00
[fastapi] Downloading python_dotenv-1.0.1-py3-none-any.whl (19 kB)
[fastapi] Downloading substrate_interface-1.7.10-py3-none-any.whl (60 kB)
[fastapi] Downloading tenacity-9.0.0-py3-none-any.whl (28 kB)
[fastapi] Downloading async_substrate_interface-1.6.4-py3-none-any.whl (97 kB)
[fastapi] Downloading bt_decode-0.8.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (647 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 647.8/647.8 kB 100.2 MB/s eta 0:00:00
[fastapi] Downloading colorama-0.4.6-py2.py3-none-any.whl (25 kB)
[fastapi] Downloading pydantic-2.9.2-py3-none-any.whl (434 kB)
[fastapi] Downloading pydantic_core-2.23.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 218.5 MB/s eta 0:00:00
[fastapi] Downloading aiosqlite-0.22.1-py3-none-any.whl (17 kB)
[fastapi] Downloading base58-2.1.1-py3-none-any.whl (5.6 kB)
[fastapi] Downloading ecdsa-0.19.2-py2.py3-none-any.whl (150 kB)
[fastapi] Downloading eth_keys-0.8.0-py3-none-any.whl (20 kB)
[fastapi] Downloading eth_utils-2.3.2-py3-none-any.whl (77 kB)
[fastapi] Downloading py_bip39_bindings-0.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (432 kB)
[fastapi] Downloading py_ed25519_zebra_bindings-1.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (323 kB)
[fastapi] Downloading py_sr25519_bindings-0.2.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (372 kB)
[fastapi] Downloading pynacl-1.6.2-cp38-abi3-manylinux_2_34_x86_64.whl (1.4 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.4/1.4 MB 164.7 MB/s eta 0:00:00
[fastapi] Downloading scalecodec-1.2.12-py3-none-any.whl (99 kB)
[fastapi] Downloading xxhash-3.8.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (220 kB)
[fastapi] Downloading cytoolz-1.1.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (2.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.8/2.8 MB 236.8 MB/s eta 0:00:00
[fastapi] Downloading eth_hash-0.8.0-py3-none-any.whl (8.0 kB)
[fastapi] Downloading toolz-1.1.0-py3-none-any.whl (58 kB)
[fastapi] Building wheels for collected packages: fiber
[fastapi] Building wheel for fiber (pyproject.toml): started
[fastapi] Building wheel for fiber (pyproject.toml): finished with status 'done'
[fastapi] Created wheel for fiber: filename=fiber-2.4.0-py3-none-any.whl size=51790 sha256=c50f803eff2fbcdf01560cfffdc65a3891a75b0b315d61d842fd3861f51b5d73
[fastapi] Stored in directory: /tmp/pip-ephem-wheel-cache-y_9jc8tj/wheels/d1/5e/21/2fa1f403cd187996037f04f6328bf11973ce31440a275f6949
[fastapi] Successfully built fiber
[fastapi] Installing collected packages: xxhash, toolz, tenacity, python-dotenv, pydantic-core, py-sr25519-bindings, py-ed25519-zebra-bindings, py-bip39-bindings, netaddr, eth-typing, eth-hash, ecdsa, colorama, bt-decode, bittensor-commit-reveal, base58, aiosqlite, scalecodec, PyNaCl, pydantic, cytoolz, eth-utils, async-substrate-interface, eth-keys, substrate-interface, fiber
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
[fastapi] [0mSuccessfully installed PyNaCl-1.6.2 aiosqlite-0.22.1 async-substrate-interface-1.6.4 base58-2.1.1 bittensor-commit-reveal-0.1.0 bt-decode-0.8.0 colorama-0.4.6 cytoolz-1.1.0 ecdsa-0.19.2 eth-hash-0.8.0 eth-keys-0.8.0 eth-typing-5.0.0 eth-utils-2.3.2 fiber-2.4.0 netaddr-1.3.0 py-bip39-bindings-0.3.0 py-ed25519-zebra-bindings-1.3.0 py-sr25519-bindings-0.2.4 pydantic-2.9.2 pydantic-core-2.23.4 python-dotenv-1.0.1 scalecodec-1.2.12 substrate-interface-1.7.10 tenacity-9.0.0 toolz-1.1.0 xxhash-3.8.1
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0m ---> c928e178039f
[fastapi] Step 13/13 : ENTRYPOINT ["./entrypoint.sh"]
[fastapi] ---> Running in d634c5ed5bb9
[fastapi] ---> 3a98a0e61623
[fastapi] {'aux': {'ID': 'sha256:3a98a0e61623459492a975bbb00d304bf47f46130c3a81e31a9accbf97ec0fa0'}}Successfully built 3a98a0e61623
[fastapi] Successfully tagged standalone-text-trainer:b15df6f6-e2e8-4c4e-bba4-01503f082fa4
[fastapi] Docker image built successfully.
[fastapi] Repository cloned successfully
[fastapi] Running Cache Download Container
[fastapi] Starting downloader container: downloader-4022aee4-05b1-4533-b1d9-0c6f52bbb747-34d845d3
[fastapi] Download completed successfully for task 4022aee4-05b1-4533-b1d9-0c6f52bbb747
[fastapi] Building Docker image 'standalone-text-trainer:f6e8370f-5756-47c1-bd5a-d0fc03efc8af' (timeout=1800s)...
[fastapi] Step 1/13 : FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04
[fastapi] ---> ff5fe688608b
[fastapi] Step 2/13 : RUN apt-get update && apt-get install -y     vim     zip     tmux     iotop     nvtop     bmon     wget     nano     zsh     htop     && rm -rf /var/lib/apt/lists/*
[fastapi] ---> Running in 32a7ce3a7f06
[fastapi] Get:1 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  InRelease [1578 B]
[fastapi] Get:2 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  Packages [3011 kB]
[fastapi] Get:3 http://archive.ubuntu.com/ubuntu jammy InRelease [270 kB]
[fastapi] Get:4 http://security.ubuntu.com/ubuntu jammy-security InRelease [129 kB]
[fastapi] Get:5 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [128 kB]
[fastapi] Get:6 http://archive.ubuntu.com/ubuntu jammy-backports InRelease [127 kB]
[fastapi] Get:7 http://archive.ubuntu.com/ubuntu jammy/main amd64 Packages [1792 kB]
[fastapi] Get:8 http://archive.ubuntu.com/ubuntu jammy/multiverse amd64 Packages [266 kB]
[fastapi] Get:9 http://archive.ubuntu.com/ubuntu jammy/universe amd64 Packages [17.5 MB]
[fastapi] Get:10 http://security.ubuntu.com/ubuntu jammy-security/multiverse amd64 Packages [84.6 kB]
[fastapi] Get:11 http://archive.ubuntu.com/ubuntu jammy/restricted amd64 Packages [164 kB]
[fastapi] Get:12 http://security.ubuntu.com/ubuntu jammy-security/universe amd64 Packages [1317 kB]
[fastapi] Get:13 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy InRelease [18.1 kB]
[fastapi] Get:14 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 Packages [1620 kB]
[fastapi] Get:15 http://security.ubuntu.com/ubuntu jammy-security/restricted amd64 Packages [7717 kB]
[fastapi] Get:16 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy/main amd64 Packages [44.3 kB]
[fastapi] Get:17 http://security.ubuntu.com/ubuntu jammy-security/main amd64 Packages [4290 kB]
[fastapi] Get:18 http://archive.ubuntu.com/ubuntu jammy-updates/restricted amd64 Packages [8007 kB]
[fastapi] Get:19 http://archive.ubuntu.com/ubuntu jammy-updates/multiverse amd64 Packages [93.2 kB]
[fastapi] Get:20 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 Packages [4624 kB]
[fastapi] Get:21 http://archive.ubuntu.com/ubuntu jammy-backports/main amd64 Packages [82.8 kB]
[fastapi] Get:22 http://archive.ubuntu.com/ubuntu jammy-backports/universe amd64 Packages [35.6 kB]
[fastapi] Fetched 51.3 MB in 3s (14.9 MB/s)
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
[fastapi] 5 upgraded, 24 newly installed, 0 to remove and 170 not upgraded.
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
[fastapi] [0mFetched 23.1 MB in 3s (8573 kB/s)
[fastapi] (Reading database ... (Reading database ... 5%(Reading database ... 10%(Reading database ... 15%(Reading database ... 20%(Reading database ... 25%(Reading database ... 30%(Reading database ... 35%(Reading database ... 40%(Reading database ... 45%(Reading database ... 50%(Reading database ... 55%(Reading database ... 60%(Reading database ... 65%(Reading database ... 70%(Reading database ... 75%(Reading database ... 80%(Reading database ... 85%(Reading database ... 90%(Reading database ... 95%(Reading database ... 100%(Reading database ... 24135 files and directories currently installed.)
[fastapi] Preparing to unpack .../00-python3.10_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking python3.10 (3.10.12-1~22.04.18) over (3.10.12-1~22.04.6) ...
[fastapi] Preparing to unpack .../01-libpython3.10-stdlib_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking libpython3.10-stdlib:amd64 (3.10.12-1~22.04.18) over (3.10.12-1~22.04.6) ...
[fastapi] Preparing to unpack .../02-python3.10-minimal_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking python3.10-minimal (3.10.12-1~22.04.18) over (3.10.12-1~22.04.6) ...
[fastapi] Preparing to unpack .../03-libpython3.10-minimal_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking libpython3.10-minimal:amd64 (3.10.12-1~22.04.18) over (3.10.12-1~22.04.6) ...
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
[fastapi] Processing triggers for libc-bin (2.35-0ubuntu3.8) ...
[fastapi] ---> 9159009424bc
[fastapi] Step 3/13 : RUN mkdir -p /workspace
[fastapi] ---> Running in da381333cc4c
[fastapi] ---> f75eeebc1ee1
[fastapi] Step 4/13 : RUN mkdir -p /cache
[fastapi] ---> Running in 65d38de664a9
[fastapi] ---> 49f9a865bad4
[fastapi] Step 5/13 : RUN mkdir -p /workspace/scripts/datasets
[fastapi] ---> Running in 8b4720f509b2
[fastapi] ---> 218313a4c37a
[fastapi] Step 6/13 : RUN mkdir -p /app/checkpoints
[fastapi] ---> Running in 2f5b9dee5cf9
[fastapi] ---> c14615117256
[fastapi] Step 7/13 : WORKDIR /workspace/scripts
[fastapi] ---> Running in da9e83184c64
[fastapi] ---> 333199d18372
[fastapi] Step 8/13 : COPY scripts /workspace/scripts
[fastapi] ---> 476fd8ad6996
[fastapi] Step 9/13 : RUN chmod +x /workspace/scripts/entrypoint.sh
[fastapi] ---> Running in 489274aadafc
[fastapi] ---> d88af22b6bb8
[fastapi] Step 10/13 : RUN python -m venv /workspace/axo_py
[fastapi] ---> Running in bb9cac26a39b
[fastapi] ---> 6e3bfeed2ed4
[fastapi] Step 11/13 : RUN bash -c "source /workspace/axo_py/bin/activate &&     pip install uv &&     pip install -U packaging==23.2 setuptools==75.8.0 wheel ninja &&     uv pip install --no-build-isolation axolotl==0.9.1 &&     pip install requests==2.32.3 &&     deactivate"
[fastapi] ---> Running in d668cf92d124
[fastapi] Collecting uv
[fastapi] Downloading uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] Downloading uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.1 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 20.1/20.1 MB 194.5 MB/s eta 0:00:00
[fastapi] Installing collected packages: uv
[fastapi] Successfully installed uv-0.12.15
[fastapi] [91m
[fastapi] [notice] A new release of pip is available: 24.0 -> 26.2.1
[fastapi] [notice] To update, run: pip install --upgrade pip
[fastapi] [0mCollecting packaging==23.2
[fastapi] Downloading packaging-23.2-py3-none-any.whl.metadata (3.2 kB)
[fastapi] Collecting setuptools==75.8.0
[fastapi] Downloading setuptools-75.8.0-py3-none-any.whl.metadata (6.7 kB)
[fastapi] Collecting wheel
[fastapi] Downloading wheel-0.48.0-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Collecting ninja
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (5.4 kB)
[fastapi] INFO: pip is looking at multiple versions of wheel to determine which version is compatible with other requirements. This could take a while.
[fastapi] Collecting wheel
[fastapi] Downloading wheel-0.47.0-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Downloading wheel-0.46.3-py3-none-any.whl.metadata (2.4 kB)
[fastapi] Downloading wheel-0.46.2-py3-none-any.whl.metadata (2.4 kB)
[fastapi] Downloading wheel-0.45.1-py3-none-any.whl.metadata (2.3 kB)
[fastapi] Downloading packaging-23.2-py3-none-any.whl (53 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 53.0/53.0 kB 5.2 MB/s eta 0:00:00
[fastapi] Downloading setuptools-75.8.0-py3-none-any.whl (1.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 56.6 MB/s eta 0:00:00
[fastapi] Downloading wheel-0.45.1-py3-none-any.whl (72 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 72.5/72.5 kB 19.5 MB/s eta 0:00:00
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (183 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 183.4/183.4 kB 59.1 MB/s eta 0:00:00
[fastapi] Installing collected packages: wheel, setuptools, packaging, ninja
[fastapi] Attempting uninstall: setuptools
[fastapi] Found existing installation: setuptools 65.5.0
[fastapi] Uninstalling setuptools-65.5.0:
[fastapi] Successfully uninstalled setuptools-65.5.0
[fastapi] Successfully installed ninja-1.13.2 packaging-23.2 setuptools-75.8.0 wheel-0.45.1
[fastapi] [91m
[fastapi] [notice] A new release of pip is available: 24.0 -> 26.2.1
[fastapi] [notice] To update, run: pip install --upgrade pip
[fastapi] [0m[91mUsing Python 3.11.10 environment at: /workspace/axo_py
[fastapi] [0m[91mResolved 217 packages in 1.22s
[fastapi] [0m[91mDownloading networkx (2.0MiB)
[fastapi] [0m[91mDownloading aiohttp (1.7MiB)
[fastapi] [0m[91mDownloading pygments (1.2MiB)
[fastapi] [0m[91mDownloading nltk (1.7MiB)
[fastapi] [0m[91mDownloading ruff (9.9MiB)
[fastapi] [0m[91mDownloading hf-transfer (3.4MiB)
[fastapi] [0m[91mDownloading grpcio (6.9MiB)
[fastapi] [0m[91mDownloading pillow (6.3MiB)
[fastapi] [0m[91mDownloading tensorboard-data-server (6.3MiB)
[fastapi] [0m[91mDownloading scipy (33.7MiB)
[fastapi] [0m[91mDownloading lxml (5.0MiB)
[fastapi] [0m[91mDownloading pandas (12.2MiB)
[fastapi] [0m[91mDownloading pyarrow (47.7MiB)
[fastapi] [0m[91mDownloading numba (3.6MiB)
[fastapi] [0m[91mDownloading sentencepiece (1.3MiB)
[fastapi] [0m[91mDownloading tokenizers (3.0MiB)
[fastapi] [0m[91mDownloading nvidia-nccl-cu12 (179.9MiB)
[fastapi] [0m[91mDownloading oci (35.2MiB)
[fastapi] [0m[91mDownloading botocore (13.7MiB)
[fastapi] [0m[91mDownloading cryptography (4.5MiB)
[fastapi] [0m[91mDownloading hf-xet (51.1MiB)
[fastapi] [0m[91mDownloading llvmlite (57.1MiB)
[fastapi] [0m[91mDownloading triton (241.4MiB)
[fastapi] [0m[91mDownloading nvidia-cusparselt-cu12 (143.1MiB)
[fastapi] [0m[91mDownloading nvidia-cusolver-cu12 (122.0MiB)
[fastapi] [0m[91mDownloading lm-eval (2.4MiB)
[fastapi] [0m[91mDownloading nvidia-cublas-cu12 (346.6MiB)
[fastapi] [0m[91mDownloading tensorboard (5.3MiB)
[fastapi] [0m[91mDownloading zstandard (5.2MiB)
[fastapi] [0m[91mDownloading pydantic-core (1.9MiB)
[fastapi] [0m[91mDownloading scikit-learn (11.6MiB)
[fastapi] [0m[91mDownloading torchao (5.4MiB)
[fastapi] [0m[91mDownloading sympy (5.9MiB)
[fastapi] [0m[91mDownloading numpy (18.6MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-nvrtc-cu12 (23.5MiB)
[fastapi] [0m[91mDownloading transformers (9.9MiB)
[fastapi] [0m[91mDownloading bitsandbytes (72.5MiB)
[fastapi] [0m[91mDownloading nvidia-nvjitlink-cu12 (20.1MiB)
[fastapi] [0m[91mDownloading gradio (44.3MiB)
[fastapi] [0m[91mDownloading nvidia-cufft-cu12 (201.7MiB)
[fastapi] [0m[91mDownloading torch (731.2MiB)
[fastapi] [0m[91mDownloading xformers (42.2MiB)
[fastapi] [0m[91mDownloading nvidia-cusparse-cu12 (197.8MiB)
[fastapi] [0m[91mDownloading wandb (24.9MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-cupti-cu12 (13.2MiB)
[fastapi] [0m[91mDownloading nvidia-cudnn-cu12 (634.0MiB)
[fastapi] [0m[91mDownloading nvidia-curand-cu12 (53.7MiB)
[fastapi] [0m[91m Downloaded pygments
[fastapi] [0m[91m Downloaded sentencepiece
[fastapi] [0m[91m Downloaded nltk
[fastapi] Downloaded aiohttp
[fastapi] [0m[91m Downloaded networkx
[fastapi] [0m[91m Downloaded pydantic-core
[fastapi] [0m[91m Downloaded lm-eval
[fastapi] [0m[91m   Building langdetect==1.0.9
[fastapi] [0m[91m   Building axolotl==0.9.1
[fastapi] [0m[91m Downloaded tokenizers
[fastapi] [0m[91m   Building axolotl-contribs-mit==0.0.3
[fastapi] [0m[91m Downloaded hf-transfer
[fastapi] [0m[91m   Building word2number==1.1
[fastapi] [0m[91m   Building axolotl-contribs-lgpl==0.0.6
[fastapi] [0m[91m   Building rouge-score==0.1.2
[fastapi] [0m[91m Downloaded numba
[fastapi] [0m[91m   Building sqlitedict==2.1.0
[fastapi] [0m[91m   Building hqq==0.2.5
[fastapi] [0m[91m   Building grpclib==0.4.7
[fastapi] [0m[91m Downloaded cryptography
[fastapi] [0m[91m Downloaded lxml
[fastapi] [0m[91m      Built word2number==1.1
[fastapi] [0m[91m Downloaded zstandard
[fastapi] [0m[91m      Built axolotl-contribs-mit==0.0.3
[fastapi] [0m[91m Downloaded tensorboard
[fastapi] [0m[91m Downloaded torchao
[fastapi] [0m[91m      Built axolotl-contribs-lgpl==0.0.6
[fastapi] [0m[91m      Built sqlitedict==2.1.0
[fastapi] [0m[91m Downloaded sympy
[fastapi] [0m[91m      Built rouge-score==0.1.2
[fastapi] [0m[91m Downloaded pillow
[fastapi] [0m[91m Downloaded tensorboard-data-server
[fastapi] [0m[91m      Built grpclib==0.4.7
[fastapi] [0m[91m Downloaded grpcio
[fastapi] [0m[91m      Built axolotl==0.9.1
[fastapi] [0m[91m      Built langdetect==1.0.9
[fastapi] [0m[91m Downloaded ruff
[fastapi] [0m[91m Downloaded transformers
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
[fastapi] [0m[91m Downloaded nvidia-cufft-cu12
[fastapi] [0m[91m Downloaded nvidia-cusparse-cu12
[fastapi] [0m[91m Downloaded triton
[fastapi] [0m[91m Downloaded nvidia-cublas-cu12
[fastapi] [0m[91m Downloaded nvidia-cudnn-cu12
[fastapi] [0m[91m Downloaded torch
[fastapi] [0m[91mPrepared 215 packages in 8.00s
[fastapi] [0m[91mInstalled 215 packages in 479ms
[fastapi] [0m[91m + absl-py==2.5.0
[fastapi] + accelerate==1.6.0
[fastapi] + addict==2.4.0
[fastapi] + adlfs==2026.8.0
[fastapi] + aiobotocore==2.26.[0m[91m0
[fastapi] + aiofiles==23.2.1
[fastapi] + aiohappyeyeballs==2.7.1
[fastapi] + aiohttp[0m[91m==3.14[0m[91m.3
[fastapi] [0m[91m +[0m[91m [0m[91maioitertools==0.13[0m[91m.0
[fastapi] +[0m[91m aiosignal==1.4.0
[fastapi] + [0m[91mannotated-doc[0m[91m==0.0.5[0m[91m
[fastapi] + annotated-types==0.8.0
[fastapi] + antlr4-python3-runtime[0m[91m==4.13.2
[fastapi] + anyio==4[0m[91m.15.1
[fastapi] + art==6.5
[fastapi] + attrs==26[0m[91m.1.0
[fastapi] [0m[91m +[0m[91m autoawq==[0m[91m0.2[0m[91m.7.post[0m[91m3
[fastapi] [0m[91m+[0m[91m axolotl[0m[91m==0.9[0m[91m.1
[fastapi] [0m[91m + [0m[91maxolotl-contribs-lgpl[0m[91m==0.0.6[0m[91m
[fastapi] + axolotl-contribs-mit==0.0.3
[fastapi] [0m[91m+ azure-core==1.41.0
[fastapi] + [0m[91mazure-identity==1.25.3
[fastapi] [0m[91m+ azure-storage-blob==12.30[0m[91m.1
[fastapi] + bitsandbytes[0m[91m==0.45.4
[fastapi] + [0m[91mbotocore==1.41.[0m[91m5
[fastapi] + [0m[91mcertifi==2026[0m[91m.7.22[0m[91m
[fastapi] + cffi==2.1.1[0m[91m
[fastapi] + chardet==6.0[0m[91m.0.post1
[fastapi] [0m[91m+[0m[91m [0m[91mcharset-normalizer==3.5.1
[fastapi] [0m[91m+ circuitbreaker==2.1.3
[fastapi] + click==8[0m[91m.5.0
[fastapi] + [0m[91mcloudpickle==3.1[0m[91m.2
[fastapi] + [0m[91mcolorama==0.4.6
[fastapi] + coloredlogs[0m[91m==15.0.1[0m[91m
[fastapi] [0m[91m + [0m[91mcrc32c==2[0m[91m.[0m[91m8
[fastapi] [0m[91m+ cryptography==50.0.1
[fastapi] + dataproperty==[0m[91m1.1.1
[fastapi] + datasets[0m[91m==3.5.1
[fastapi] + decorator==5.3.1
[fastapi] [0m[91m+ defusedxml==0[0m[91m.7[0m[91m.1
[fastapi] +[0m[91m [0m[91mdill==0.3[0m[91m.8
[fastapi] [0m[91m +[0m[91m [0m[91meinops==0[0m[91m.8.[0m[91m2[0m[91m
[fastapi] +[0m[91m evaluate==0.4.[0m[91m1
[fastapi] + fastapi==0.[0m[91m141.1
[fastapi] + [0m[91mfastcore==2.2.28
[fastapi] [0m[91m + ffmpy==1[0m[91m.0.0
[fastapi] [0m[91m+ filelock==[0m[91m3.32.7
[fastapi] +[0m[91m fire==0[0m[91m.7.1
[fastapi] [0m[91m + frozenlist==1.8.0
[fastapi] +[0m[91m fsspec==2025.3[0m[91m.0
[fastapi] + gcsfs[0m[91m==2025.3.0[0m[91m
[fastapi] + google-api-core==2.33.[0m[91m0
[fastapi] + google-auth[0m[91m==2.58.[0m[91m0
[fastapi] + [0m[91mgoogle-auth-oauthlib==1.4[0m[91m.1
[fastapi] +[0m[91m google-cloud-core==2.[0m[91m7.0
[fastapi] [0m[91m+ google-cloud-storage==[0m[91m3.14.1[0m[91m
[fastapi] + google-crc32c[0m[91m==1.8[0m[91m.0
[fastapi] [0m[91m + google-resumable-media[0m[91m==2.10[0m[91m.2
[fastapi] + googleapis-common-protos==1[0m[91m.75.0
[fastapi] [0m[91m + gradio==[0m[91m5.23.[0m[91m3[0m[91m
[fastapi] + [0m[91mgradio-client[0m[91m==1.8[0m[91m.0
[fastapi] [0m[91m+ groovy[0m[91m==[0m[91m0.1[0m[91m.[0m[91m2
[fastapi] [0m[91m+ [0m[91mgrpcio[0m[91m==1.84[0m[91m.[0m[91m0
[fastapi] +[0m[91m grpclib[0m[91m==0.[0m[91m4[0m[91m.7[0m[91m
[fastapi] + h11==0.16.0
[fastapi] [0m[91m+ h2[0m[91m==[0m[91m4.4[0m[91m.1
[fastapi] [0m[91m + hf-transfer==0.1.9
[fastapi] + [0m[91mhf-xet==1.1.0
[fastapi] [0m[91m+ [0m[91mhpack[0m[91m==4.2[0m[91m.0[0m[91m
[fastapi] + hqq==0.2[0m[91m.5
[fastapi] [0m[91m+ httpcore[0m[91m==1.0.9
[fastapi] [0m[91m+ httpx[0m[91m==0.28.1
[fastapi] [0m[91m + huggingface-hub==0[0m[91m.31.0
[fastapi] [0m[91m+ humanfriendly==[0m[91m10.0
[fastapi] [0m[91m+ hyperframe[0m[91m==6.1[0m[91m.0
[fastapi] +[0m[91m idna==3.[0m[91m19
[fastapi] + [0m[91mimmutabledict==4.[0m[91m2.0
[fastapi] + isodate==0.7[0m[91m.2
[fastapi] + [0m[91mjinja2==3[0m[91m.1.6
[fastapi] + jmespath==[0m[91m1.1.0
[fastapi] + joblib[0m[91m==1.6[0m[91m.0
[fastapi] [0m[91m+ [0m[91mjsonlines[0m[91m==4.0.[0m[91m0[0m[91m
[fastapi] [0m[91m+ [0m[91mlangdetect==[0m[91m1.[0m[91m0.9[0m[91m
[fastapi] [0m[91m + [0m[91mliger-kernel[0m[91m==0.5.9
[fastapi] +[0m[91m llvmlite==0.[0m[91m49.0
[fastapi] [0m[91m+ lm-eval[0m[91m==0.4.[0m[91m7[0m[91m
[fastapi] +[0m[91m lxml[0m[91m==6.[0m[91m1.[0m[91m3
[fastapi] [0m[91m [0m[91m+ markdown==[0m[91m3.10.3
[fastapi] +[0m[91m markdown-it-py[0m[91m==4.2.[0m[91m0
[fastapi] +[0m[91m markupsafe==3.0.3
[fastapi] [0m[91m+ mbstrdecoder==1[0m[91m.1[0m[91m.5
[fastapi] [0m[91m+[0m[91m mdurl==0.1.2
[fastapi] [0m[91m+ modal==[0m[91m0[0m[91m.70.5[0m[91m
[fastapi] [0m[91m + more-itertools[0m[91m==11.[0m[91m1.[0m[91m0[0m[91m
[fastapi] +[0m[91m mpmath[0m[91m==1.3.0[0m[91m
[fastapi] + msal==[0m[91m1.38.0
[fastapi] +[0m[91m msal-extensions==1[0m[91m.3.1
[fastapi] [0m[91m+ multidict==[0m[91m6.8.0[0m[91m
[fastapi] + [0m[91mmultiprocess==0.70[0m[91m.16
[fastapi] +[0m[91m networkx==3.[0m[91m6.1
[fastapi] + nltk==3[0m[91m.10.3
[fastapi] + [0m[91mnumba==0.67.0
[fastapi] [0m[91m+[0m[91m numexpr[0m[91m==2.14[0m[91m.2[0m[91m
[fastapi] + [0m[91mnumpy==2.0.1
[fastapi] + [0m[91mnvidia-cublas-cu12==12.4[0m[91m.5[0m[91m.8
[fastapi] [0m[91m+[0m[91m nvidia-cuda-cupti-cu12[0m[91m==12.[0m[91m4.127[0m[91m
[fastapi] [0m[91m+[0m[91m nvidia-cuda-nvrtc-cu12[0m[91m==[0m[91m12.4[0m[91m.127
[fastapi] [0m[91m [0m[91m+ [0m[91mnvidia-cuda-runtime-cu12[0m[91m==12.4.[0m[91m127[0m[91m
[fastapi] +[0m[91m nvidia-cudnn-cu12[0m[91m==[0m[91m9.1.[0m[91m0.70[0m[91m
[fastapi] [0m[91m +[0m[91m [0m[91mnvidia-cufft-cu12[0m[91m==11.2.[0m[91m1.3
[fastapi] [0m[91m+ [0m[91mnvidia-curand-cu12==10.[0m[91m3[0m[91m.5.147[0m[91m
[fastapi] +[0m[91m [0m[91mnvidia-cusolver-cu12==11[0m[91m.6.[0m[91m1.9[0m[91m
[fastapi] [0m[91m +[0m[91m [0m[91mnvidia-cusparse-cu12==12.[0m[91m3.1.[0m[91m170
[fastapi] [0m[91m+[0m[91m nvidia-cusparselt-cu12[0m[91m==[0m[91m0.6[0m[91m.2
[fastapi] [0m[91m [0m[91m+ nvidia-ml-py[0m[91m==12[0m[91m.560.[0m[91m30
[fastapi] [0m[91m+[0m[91m nvidia-nccl-cu12[0m[91m==[0m[91m2.21[0m[91m.5[0m[91m
[fastapi] + nvidia-nvjitlink-cu12==12.4.127
[fastapi] + nvidia-nvtx-cu12==12.4.127
[fastapi] + oauthlib==3.3.1
[fastapi] + oci==2.186.0
[fastapi] + ocifs==1.3.2
[fastapi] + opentelemetry-api==1.44.0
[fastapi] + opentelemetry-exporter-otlp-proto-common==1.44.0
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
[fastapi] + propcache==0.5.4
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
[fastapi] + threadpoolctl==3.7.0
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
[fastapi] + urllib3==2.8.0
[fastapi] + uvicorn==0.53.0
[fastapi] + wandb==0.30.0
[fastapi] + watchfiles==1.2.0
[fastapi] + websockets==15.0.1
[fastapi] + werkzeug==3.1.8
[fastapi] + word2number==1.1
[fastapi] + wrapt==1.17.3
[fastapi] + xformers==0.0.29.post2
[fastapi] + xxhash==4.0.1
[fastapi] + yarl==1.25.1
[fastapi] + zstandard==0.22.0
[fastapi] [0mCollecting requests==2.32.3
[fastapi] Downloading requests-2.32.3-py3-none-any.whl.metadata (4.6 kB)
[fastapi] Requirement already satisfied: charset-normalizer<4,>=2 in /workspace/axo_py/lib/python3.11/site-packages (from requests==2.32.3) (3.5.1)
[fastapi] Requirement already satisfied: idna<4,>=2.5 in /workspace/axo_py/lib/python3.11/site-packages (from requests==2.32.3) (3.19)
[fastapi] Requirement already satisfied: urllib3<3,>=1.21.1 in /workspace/axo_py/lib/python3.11/site-packages (from requests==2.32.3) (2.8.0)
[fastapi] Requirement already satisfied: certifi>=2017.4.17 in /workspace/axo_py/lib/python3.11/site-packages (from requests==2.32.3) (2026.7.22)
[fastapi] Downloading requests-2.32.3-py3-none-any.whl (64 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 64.9/64.9 kB 2.7 MB/s eta 0:00:00
[fastapi] Installing collected packages: requests
[fastapi] Attempting uninstall: requests
[fastapi] Found existing installation: requests 2.34.2
[fastapi] Uninstalling requests-2.34.2:
[fastapi] Successfully uninstalled requests-2.34.2
[fastapi] [91mERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
[fastapi] google-api-core 2.33.0 requires requests<3.0.0,>=2.33.0, but you have requests 2.32.3 which is incompatible.
[fastapi] [0mSuccessfully installed requests-2.32.3
[fastapi] [91m
[fastapi] [notice] A new release of pip is available: 24.0 -> 26.2.1
[fastapi] [notice] To update, run: pip install --upgrade pip
[fastapi] [0m ---> 27e6fab2c625
[fastapi] Step 12/13 : RUN pip install uv &&     pip install -U packaging==23.2 setuptools==75.8.0 wheel ninja &&     uv pip install -r /workspace/scripts/training_requirements.txt --system &&     pip install hf_transfer==0.1.9 &&     pip install tenacity==9.1.2 &&     pip install tiktoken==0.9.0 &&     pip install flash-attn==v2.7.4.post1 --no-build-isolation &&     uv pip install vllm==0.8.3 --system &&     pip install "fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0"
[fastapi] ---> Running in efa311e7fbc7
[fastapi] Collecting uv
[fastapi] Using cached uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] Using cached uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.1 MB)
[fastapi] Installing collected packages: uv
[fastapi] Successfully installed uv-0.12.15
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0mCollecting packaging==23.2
[fastapi] Using cached packaging-23.2-py3-none-any.whl.metadata (3.2 kB)
[fastapi] Collecting setuptools==75.8.0
[fastapi] Using cached setuptools-75.8.0-py3-none-any.whl.metadata (6.7 kB)
[fastapi] Requirement already satisfied: wheel in /usr/local/lib/python3.11/dist-packages (0.44.0)
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
[fastapi] Attempting uninstall: wheel
[fastapi] Found existing installation: wheel 0.44.0
[fastapi] Uninstalling wheel-0.44.0:
[fastapi] Successfully uninstalled wheel-0.44.0
[fastapi] Attempting uninstall: setuptools
[fastapi] Found existing installation: setuptools 75.1.0
[fastapi] Uninstalling setuptools-75.1.0:
[fastapi] Successfully uninstalled setuptools-75.1.0
[fastapi] Attempting uninstall: packaging
[fastapi] Found existing installation: packaging 24.1
[fastapi] Uninstalling packaging-24.1:
[fastapi] Successfully uninstalled packaging-24.1
[fastapi] Successfully installed ninja-1.13.2 packaging-23.2 setuptools-75.8.0 wheel-0.45.1
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0m[91mUsing Python 3.11.10 environment at: /usr
[fastapi] [0m[91mResolved 187 packages in 1.58s
[fastapi] [0m[91m   Building deepspeed==0.15.4
[fastapi] [0m[91m   Building antlr4-python3-runtime==4.9.3
[fastapi] [0m[91mDownloading openai (1.9MiB)
[fastapi] [0m[91mDownloading mpi4py (1.3MiB)
[fastapi] [0m[91mDownloading hf-xet (4.3MiB)
[fastapi] [0m[91mDownloading pyphen (2.0MiB)
[fastapi] [0m[91mDownloading tensorboard (5.2MiB)
[fastapi] [0m[91mDownloading pycryptodome (2.2MiB)
[fastapi] [0m[91mDownloading matplotlib (9.4MiB)
[fastapi] [0m[91mDownloading mlflow (11.0MiB)
[fastapi] [0m[91mDownloading dash (8.5MiB)
[fastapi] [0m[91mDownloading pandas (12.5MiB)
[fastapi] [0m[91mDownloading pydantic-core (2.0MiB)
[fastapi] [0m[91mDownloading kiwisolver (1.4MiB)
[fastapi] [0m[91mDownloading mlflow-tracing (1.7MiB)
[fastapi] [0m[91mDownloading scipy (35.9MiB)
[fastapi] [0m[91mDownloading fonttools (5.2MiB)
[fastapi] [0m[91mDownloading sentencepiece (1.2MiB)
[fastapi] [0m[91mDownloading plotly (9.2MiB)
[fastapi] [0m[91mDownloading mlflow-skinny (3.5MiB)
[fastapi] [0m[91mDownloading wandb (20.4MiB)
[fastapi] [0m[91mDownloading scikit-learn (8.9MiB)
[fastapi] [0m[91mDownloading sqlalchemy (3.3MiB)
[fastapi] [0m[91m Downloaded sentencepiece
[fastapi] [0m[91m Downloaded mpi4py
[fastapi] [0m[91m Downloaded kiwisolver
[fastapi] [0m[91m Downloaded mlflow-tracing
[fastapi] [0m[91m Downloaded pydantic-core
[fastapi] [0m[91m Downloaded pyphen
[fastapi] [0m[91m Downloaded pycryptodome
[fastapi] [0m[91m Downloaded openai
[fastapi] [0m[91m Downloaded sqlalchemy
[fastapi] [0m[91m Downloaded mlflow-skinny
[fastapi] [0m[91m Downloaded hf-xet
[fastapi] [0m[91m Downloaded tensorboard
[fastapi] [0m[91m Downloaded fonttools
[fastapi] [0m[91m Downloaded plotly
[fastapi] [0m[91m Downloaded scikit-learn
[fastapi] [0m[91m Downloaded dash
[fastapi] [0m[91m Downloaded matplotlib
[fastapi] [0m[91m      Built antlr4-python3-runtime==4.9.3
[fastapi] [0m[91m Downloaded mlflow
[fastapi] [0m[91m Downloaded pandas
[fastapi] [0m[91m Downloaded wandb
[fastapi] [0m[91m Downloaded scipy
[fastapi] [0m[91m      Built deepspeed==0.15.4
[fastapi] [0m[91mPrepared 88 packages in 829ms
[fastapi] [0m[91mUninstalled 6 packages in 29ms
[fastapi] [0m[91mInstalled 141 packages in 3.21s
[fastapi] [0m[91m + absl-py==2.5.0
[fastapi] + accelerate==1.6.0
[fastapi] + aiohappyeyeballs==2.7.1
[fastapi] + aiohttp==3.14.3
[fastapi] + aiosignal==1.4.0
[fastapi] + alembic==1.20.0
[fastapi] [0m[91m+ annotated-doc==0.0.5
[fastapi] + annotated-types==0.8.0
[fastapi] + antlr4-python3-runtime==4.[0m[91m9.3
[fastapi] - anyio[0m[91m==4.6.0
[fastapi] + anyio==4.15.1
[fastapi] +[0m[91m astor==0.8.1
[fastapi] + bitsandbytes==0.45.4[0m[91m
[fastapi] + blinker==[0m[91m1.9.0
[fastapi] [0m[91m+ cachetools[0m[91m==7[0m[91m.1.8[0m[91m
[fastapi] - cffi[0m[91m==1[0m[91m.17[0m[91m.1
[fastapi] +[0m[91m cffi[0m[91m==2.[0m[91m1.1[0m[91m
[fastapi] +[0m[91m [0m[91mclick==8[0m[91m.5[0m[91m.0
[fastapi] [0m[91m+[0m[91m cloudpickle[0m[91m==3.[0m[91m1.2[0m[91m
[fastapi] [0m[91m+ [0m[91mcmudict==[0m[91m1.1[0m[91m.3[0m[91m
[fastapi] +[0m[91m contourpy[0m[91m==1.3[0m[91m.3
[fastapi] [0m[91m+ [0m[91mcryptography==[0m[91m50.0.1[0m[91m
[fastapi] [0m[91m + cycler[0m[91m==[0m[91m0.12.[0m[91m1[0m[91m
[fastapi] + [0m[91mdash==4[0m[91m.[0m[91m4.[0m[91m1
[fastapi] +[0m[91m [0m[91mdatabricks-sdk==0[0m[91m.139.0[0m[91m
[fastapi] [0m[91m+ [0m[91mdatasets[0m[91m==3.[0m[91m5.0[0m[91m
[fastapi] +[0m[91m deepspeed[0m[91m==0.15[0m[91m.[0m[91m4
[fastapi] [0m[91m+ [0m[91mdetoxify==[0m[91m0.5[0m[91m.2
[fastapi] [0m[91m+[0m[91m dill==0[0m[91m.3.8
[fastapi] [0m[91m+ docker[0m[91m==7.2.0
[fastapi] + docker-pycreds==0[0m[91m.4.0
[fastapi] + einops==0.8.1
[fastapi] [0m[91m + fastapi==0[0m[91m.141.[0m[91m1
[fastapi] +[0m[91m flask==3.1.3
[fastapi] + flask-cors==6.0.5[0m[91m
[fastapi] + fonttools==4.65.[0m[91m0
[fastapi] + frozenlist[0m[91m==1.8.0[0m[91m
[fastapi] + gdown[0m[91m==6.[0m[91m3.0
[fastapi] +[0m[91m gitdb==4[0m[91m.0.12
[fastapi] [0m[91m + gitpython[0m[91m==3.1.62[0m[91m
[fastapi] + [0m[91mgoogle-auth==2[0m[91m.58.0
[fastapi] + graphene==[0m[91m3.4.3
[fastapi] [0m[91m + graphql-core[0m[91m==3.2.12
[fastapi] + graphql-relay[0m[91m==3.2.0
[fastapi] + [0m[91mgreenlet==3.[0m[91m5.6
[fastapi] [0m[91m+ [0m[91mgrpcio==[0m[91m1.84.[0m[91m0
[fastapi] [0m[91m+[0m[91m gunicorn==26[0m[91m.2.[0m[91m0
[fastapi] [0m[91m- h11[0m[91m==0.14.0[0m[91m
[fastapi] + h11[0m[91m==0.16.0
[fastapi] + [0m[91mhf-xet==1.6.0
[fastapi] +[0m[91m hjson==3.1.0
[fastapi] [0m[91m + httpcore2==2.13.[0m[91m0
[fastapi] + httpx2[0m[91m==2.13[0m[91m.0
[fastapi] +[0m[91m huey==3.[0m[91m4.0
[fastapi] +[0m[91m huggingface-hub==0.36.2[0m[91m
[fastapi] - idna==3.10
[fastapi] [0m[91m + idna[0m[91m==3.[0m[91m19
[fastapi] [0m[91m+[0m[91m importlib-metadata[0m[91m==[0m[91m9.0.1
[fastapi] + importlib-resources==7.1.0
[fastapi] [0m[91m + itsdangerous==2.[0m[91m2.0
[fastapi] [0m[91m+ jaconv[0m[91m==[0m[91m0.5.0
[fastapi] + janus==2.0.0
[fastapi] [0m[91m+ jiter==0.[0m[91m17.0
[fastapi] [0m[91m + joblib==1[0m[91m.6.0
[fastapi] [0m[91m+[0m[91m [0m[91mkiwisolver==1.5.1
[fastapi] + langcheck==0.9[0m[91m.0
[fastapi] + liger-kernel==0.5.9
[fastapi] + mako==[0m[91m1.4.1
[fastapi] [0m[91m+ [0m[91mmarkdown==3[0m[91m.10.3
[fastapi] [0m[91m+ matplotlib==3.11.2[0m[91m
[fastapi] + minio==7.2.20
[fastapi] + mlflow==3.[0m[91m16.0
[fastapi] [0m[91m + [0m[91mmlflow-skinny==3.16.0
[fastapi] + mlflow-tracing==[0m[91m3.16.0
[fastapi] + mpi4py==4.1.2
[fastapi] + msgpack==1.2.2
[fastapi] + multidict[0m[91m==6.8.0
[fastapi] + multiprocess==0[0m[91m.70.16
[fastapi] + narwhals==2[0m[91m.[0m[91m26.0
[fastapi] + nlpaug==1.1.11
[fastapi] + nltk==3.10.3
[fastapi] [0m[91m + omegaconf==2.3[0m[91m.1
[fastapi] [0m[91m + openai[0m[91m==3.14[0m[91m.1
[fastapi] [0m[91m+ opentelemetry-api==1.44.0
[fastapi] + opentelemetry-proto[0m[91m==1.44.0
[fastapi] + opentelemetry-sdk==[0m[91m1.44.0
[fastapi] + opentelemetry-semantic-conventions==0.65[0m[91mb0
[fastapi] [0m[91m+ pandas[0m[91m==[0m[91m2.[0m[91m2.3
[fastapi] [0m[91m+[0m[91m peft==0[0m[91m.15.[0m[91m1[0m[91m
[fastapi] + [0m[91mplotly[0m[91m==7.[0m[91m1[0m[91m.0[0m[91m
[fastapi] [0m[91m+ [0m[91mprettytable==3[0m[91m.18.0[0m[91m
[fastapi] [0m[91m + propcache[0m[91m==0.5[0m[91m.[0m[91m4
[fastapi] [0m[91m+ protobuf==[0m[91m6.33.6
[fastapi] [0m[91m+ [0m[91mpy-cpuinfo==9[0m[91m.0[0m[91m.0
[fastapi] [0m[91m +[0m[91m pyarrow[0m[91m==25[0m[91m.0.1
[fastapi] + [0m[91mpyasn1[0m[91m==0.[0m[91m6[0m[91m.4[0m[91m
[fastapi] +[0m[91m pyasn1-modules[0m[91m==0[0m[91m.4.2[0m[91m
[fastapi] [0m[91m+[0m[91m pycryptodome[0m[91m==3.[0m[91m23.0
[fastapi] [0m[91m + [0m[91mpydantic==2.13.5
[fastapi] +[0m[91m pydantic-core[0m[91m==[0m[91m2.46.5
[fastapi] + [0m[91mpyparsing==3.3.2[0m[91m
[fastapi] +[0m[91m pyphen[0m[91m==0.18[0m[91m.1
[fastapi] [0m[91m +[0m[91m pysocks[0m[91m==1.[0m[91m7.1
[fastapi] + python-dotenv==1.[0m[91m2.3
[fastapi] + pytz[0m[91m==2026.3.post1
[fastapi] [0m[91m+ regex==2026.9.10
[fastapi] [0m[91m + restrictedpython==8.[0m[91m0
[fastapi] + [0m[91mretrying==1.4.2[0m[91m
[fastapi] + rouge-score[0m[91m==0.1.[0m[91m2
[fastapi] + safetensors==0.8.0
[fastapi] [0m[91m+ scikit-learn==[0m[91m1.9[0m[91m.1[0m[91m
[fastapi] [0m[91m+ [0m[91mscipy==1.15.2
[fastapi] [0m[91m+ [0m[91msentence-transformers==5.7.[0m[91m0
[fastapi] + sentencepiece==0.2.0
[fastapi] + sentry-sdk==2.69.2
[fastapi] [0m[91m + setproctitle==1.[0m[91m3.7[0m[91m
[fastapi] [0m[91m+ six[0m[91m==1.17.0[0m[91m
[fastapi] + skops==0.14[0m[91m.0
[fastapi] + smmap[0m[91m==5.0.3
[fastapi] [0m[91m+ sqlalchemy==2.0[0m[91m.54
[fastapi] +[0m[91m sqlparse==0.6.[0m[91m0
[fastapi] + starlette[0m[91m==1.6.0[0m[91m
[fastapi] [0m[91m + [0m[91mtabulate==0[0m[91m.10.[0m[91m0
[fastapi] [0m[91m +[0m[91m tenacity[0m[91m==[0m[91m9.1.4[0m[91m
[fastapi] +[0m[91m tensorboard[0m[91m==[0m[91m2.19.0[0m[91m
[fastapi] +[0m[91m tensorboard-data-server==0[0m[91m.7.2
[fastapi] +[0m[91m textstat==[0m[91m0.7.8[0m[91m
[fastapi] [0m[91m + threadpoolctl[0m[91m==3[0m[91m.7.0
[fastapi] [0m[91m +[0m[91m tokenizers==0[0m[91m.21[0m[91m.4
[fastapi] + toml==0.10[0m[91m.2
[fastapi] +[0m[91m tqdm[0m[91m==4.70.[0m[91m1[0m[91m
[fastapi] + transformers==4.51.3
[fastapi] + trl==0.18.0
[fastapi] + truststore==0.10.4
[fastapi] + typer==0.9.0
[fastapi] - typing-extensions==4.9.0
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
[fastapi] [0mCollecting hf_transfer==0.1.9
[fastapi] Downloading hf_transfer-0.1.9-cp38-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (1.7 kB)
[fastapi] Downloading hf_transfer-0.1.9-cp38-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.6 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.6/3.6 MB 206.0 MB/s eta 0:00:00
[fastapi] Installing collected packages: hf_transfer
[fastapi] Successfully installed hf_transfer-0.1.9
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0mCollecting tenacity==9.1.2
[fastapi] Downloading tenacity-9.1.2-py3-none-any.whl.metadata (1.2 kB)
[fastapi] Downloading tenacity-9.1.2-py3-none-any.whl (28 kB)
[fastapi] Installing collected packages: tenacity
[fastapi] Attempting uninstall: tenacity
[fastapi] Found existing installation: tenacity 9.1.4
[fastapi] Uninstalling tenacity-9.1.4:
[fastapi] Successfully uninstalled tenacity-9.1.4
[fastapi] Successfully installed tenacity-9.1.2
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0mCollecting tiktoken==0.9.0
[fastapi] Downloading tiktoken-0.9.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.7 kB)
[fastapi] Requirement already satisfied: regex>=2022.1.18 in /usr/local/lib/python3.11/dist-packages (from tiktoken==0.9.0) (2026.9.10)
[fastapi] Requirement already satisfied: requests>=2.26.0 in /usr/local/lib/python3.11/dist-packages (from tiktoken==0.9.0) (2.32.3)
[fastapi] Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.11/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (3.3.2)
[fastapi] Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.11/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (3.19)
[fastapi] Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.11/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (2.2.3)
[fastapi] Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.11/dist-packages (from requests>=2.26.0->tiktoken==0.9.0) (2024.8.30)
[fastapi] Downloading tiktoken-0.9.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (1.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 101.4 MB/s eta 0:00:00
[fastapi] Installing collected packages: tiktoken
[fastapi] Successfully installed tiktoken-0.9.0
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0mCollecting flash-attn==v2.7.4.post1
[fastapi] Downloading flash_attn-2.7.4.post1.tar.gz (6.0 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.0/6.0 MB 147.5 MB/s eta 0:00:00
[fastapi] Preparing metadata (setup.py): started
[fastapi] Preparing metadata (setup.py): finished with status 'done'
[fastapi] Requirement already satisfied: torch in /usr/local/lib/python3.11/dist-packages (from flash-attn==v2.7.4.post1) (2.4.1+cu124)
[fastapi] Requirement already satisfied: einops in /usr/local/lib/python3.11/dist-packages (from flash-attn==v2.7.4.post1) (0.8.1)
[fastapi] Requirement already satisfied: filelock in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (3.13.1)
[fastapi] Requirement already satisfied: typing-extensions>=4.8.0 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (4.16.0)
[fastapi] Requirement already satisfied: sympy in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (1.12)
[fastapi] Requirement already satisfied: networkx in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (3.2.1)
[fastapi] Requirement already satisfied: jinja2 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (3.1.3)
[fastapi] Requirement already satisfied: fsspec in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (2024.2.0)
[fastapi] Requirement already satisfied: nvidia-cuda-nvrtc-cu12==12.4.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (12.4.99)
[fastapi] Requirement already satisfied: nvidia-cuda-runtime-cu12==12.4.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (12.4.99)
[fastapi] Requirement already satisfied: nvidia-cuda-cupti-cu12==12.4.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (12.4.99)
[fastapi] Requirement already satisfied: nvidia-cudnn-cu12==9.1.0.70 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (9.1.0.70)
[fastapi] Requirement already satisfied: nvidia-cublas-cu12==12.4.2.65 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (12.4.2.65)
[fastapi] Requirement already satisfied: nvidia-cufft-cu12==11.2.0.44 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (11.2.0.44)
[fastapi] Requirement already satisfied: nvidia-curand-cu12==10.3.5.119 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (10.3.5.119)
[fastapi] Requirement already satisfied: nvidia-cusolver-cu12==11.6.0.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (11.6.0.99)
[fastapi] Requirement already satisfied: nvidia-cusparse-cu12==12.3.0.142 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (12.3.0.142)
[fastapi] Requirement already satisfied: nvidia-nccl-cu12==2.20.5 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (2.20.5)
[fastapi] Requirement already satisfied: nvidia-nvtx-cu12==12.4.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (12.4.99)
[fastapi] Requirement already satisfied: nvidia-nvjitlink-cu12==12.4.99 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (12.4.99)
[fastapi] Requirement already satisfied: triton==3.0.0 in /usr/local/lib/python3.11/dist-packages (from torch->flash-attn==v2.7.4.post1) (3.0.0)
[fastapi] Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.11/dist-packages (from jinja2->torch->flash-attn==v2.7.4.post1) (2.1.5)
[fastapi] Requirement already satisfied: mpmath>=0.19 in /usr/local/lib/python3.11/dist-packages (from sympy->torch->flash-attn==v2.7.4.post1) (1.3.0)
[fastapi] Building wheels for collected packages: flash-attn
[fastapi] Building wheel for flash-attn (setup.py): started
[fastapi] Building wheel for flash-attn (setup.py): finished with status 'done'
[fastapi] Created wheel for flash-attn: filename=flash_attn-2.7.4.post1-cp311-cp311-linux_x86_64.whl size=187805408 sha256=92cf49e6f66795b6934cec0cba526ed6e45d3313de3f905d45df8773f19092a9
[fastapi] Stored in directory: /root/.cache/pip/wheels/3d/88/d8/284b89f56af7d5bf366b10d6b8e251ac8a7c7bf3f04203fb4f
[fastapi] Successfully built flash-attn
[fastapi] Installing collected packages: flash-attn
[fastapi] Successfully installed flash-attn-2.7.4.post1
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0m[91mUsing Python 3.11.10 environment at: /usr
[fastapi] [0m[91mResolved 142 packages in 222ms
[fastapi] [0m[91mDownloading mistral-common (6.2MiB)
[fastapi] [0m[91mDownloading llvmlite (40.4MiB)
[fastapi] [0m[91mDownloading pycountry (7.7MiB)
[fastapi] [0m[91mDownloading torchvision (6.9MiB)
[fastapi] [0m[91mDownloading opencv-python-headless (58.4MiB)
[fastapi] [0m[91mDownloading vllm (280.4MiB)
[fastapi] [0m[91mDownloading numba (3.6MiB)
[fastapi] [0m[91mDownloading pillow (6.6MiB)
[fastapi] [0m[91mDownloading numpy (15.6MiB)
[fastapi] [0m[91mDownloading llguidance (14.3MiB)
[fastapi] [0m[91mDownloading ray (74.7MiB)
[fastapi] [0m[91mDownloading xgrammar (4.1MiB)
[fastapi] [0m[91mDownloading torchaudio (3.2MiB)
[fastapi] [0m[91mDownloading cupy-cuda12x (130.3MiB)
[fastapi] [0m[91mDownloading uvloop (3.6MiB)
[fastapi] [0m[91m Downloaded torchaudio
[fastapi] [0m[91m Downloaded uvloop
[fastapi] [0m[91m Downloaded numba
[fastapi] [0m[91m Downloaded xgrammar
[fastapi] [0m[91m Downloaded mistral-common
[fastapi] [0m[91m Downloaded pillow
[fastapi] [0m[91m Downloaded torchvision
[fastapi] [0m[91m Downloaded pycountry
[fastapi] [0m[91m Downloaded llguidance
[fastapi] [0m[91m Downloaded numpy
[fastapi] [0m[91m Downloaded llvmlite
[fastapi] [0m[91m Downloaded opencv-python-headless
[fastapi] [0m[91m Downloaded ray
[fastapi] [0m[91m Downloaded cupy-cuda12x
[fastapi] [0m[91m Downloaded vllm
[fastapi] [0m[91mPrepared 45 packages in 2.67s
[fastapi] [0m[91mUninstalled 23 packages in 1.47s
[fastapi] [0m[91mInstalled 71 packages in 11.53s
[fastapi] [0m[91m + agent-detector==2.0.0
[fastapi] + airportsdata==20260905
[fastapi] + blake3==1.0.9
[fastapi] + compressed-tensors==0.9.2
[fastapi] + cuda-pathfinder==1.8.1
[fastapi] + cupy-cuda12x==14.2.0
[fastapi] + depyf==0.18.0
[fastapi] [0m[91m + detect-installer==0.2.1
[fastapi] + diskcache==5.6.3
[fastapi] + dnspython==[0m[91m2.8.0[0m[91m
[fastapi] +[0m[91m [0m[91memail-validator==2.3[0m[91m.[0m[91m0
[fastapi] + [0m[91mfastapi-cli[0m[91m==0.0[0m[91m.32
[fastapi] + fastapi-cloud-cli[0m[91m==0.26.0
[fastapi] + fastar==0.12.0[0m[91m
[fastapi] -[0m[91m [0m[91mfilelock==3[0m[91m.13[0m[91m.1
[fastapi] [0m[91m+ [0m[91mfilelock==[0m[91m3.32[0m[91m.[0m[91m7[0m[91m
[fastapi] + gguf==0.10.0
[fastapi] - httpcore[0m[91m==1.0.5[0m[91m
[fastapi] + httpcore==1.0.9
[fastapi] [0m[91m + httptools==[0m[91m0.8.0
[fastapi] [0m[91m + interegular[0m[91m==0.3.3[0m[91m
[fastapi] - jinja2[0m[91m==3.1[0m[91m.3
[fastapi] +[0m[91m jinja2==3.[0m[91m1.6
[fastapi] + lark==[0m[91m1.2.2[0m[91m
[fastapi] + llguidance[0m[91m==0.7.30
[fastapi] + llvmlite==0.44.0[0m[91m
[fastapi] + [0m[91mlm-format-enforcer==0.10.12
[fastapi] [0m[91m + markdown-it-py[0m[91m==4.[0m[91m2.0
[fastapi] + [0m[91mmdurl==0[0m[91m.[0m[91m1.2
[fastapi] + mistral-common==1.11.7
[fastapi] [0m[91m+ msgspec==0.21.[0m[91m1
[fastapi] + nanobind==3[0m[91m.0.1
[fastapi] + numba==0.61.0
[fastapi] [0m[91m - numpy==1.26.3
[fastapi] + numpy==2.1.[0m[91m3[0m[91m
[fastapi] - nvidia-cublas-cu12[0m[91m==12.4.2.[0m[91m65
[fastapi] [0m[91m+ [0m[91mnvidia-cublas-cu12==12[0m[91m.4.[0m[91m5.[0m[91m8
[fastapi] -[0m[91m nvidia-cuda-cupti-cu12[0m[91m==12.4.99
[fastapi] [0m[91m + nvidia-cuda-cupti-cu12[0m[91m==12.4.[0m[91m127
[fastapi] -[0m[91m nvidia-cuda-nvrtc-cu12==12[0m[91m.4.99
[fastapi] [0m[91m+ nvidia-cuda-nvrtc-cu12==[0m[91m12.4.127
[fastapi] [0m[91m - nvidia-cuda-runtime-cu12[0m[91m==12.4.[0m[91m99
[fastapi] +[0m[91m nvidia-cuda-runtime-cu12==[0m[91m12.4.127
[fastapi] - nvidia-cufft-cu12[0m[91m==11.2.0.[0m[91m44
[fastapi] + [0m[91mnvidia-cufft-cu12[0m[91m==11.[0m[91m2.1.3[0m[91m
[fastapi] -[0m[91m nvidia-curand-cu12==10.3.5.119
[fastapi] + [0m[91mnvidia-curand-cu12==10.3.5[0m[91m.147
[fastapi] [0m[91m- nvidia-cusolver-cu12[0m[91m==11.6.0.99
[fastapi] + nvidia-cusolver-cu12==11.6[0m[91m.1.9
[fastapi] - nvidia-cusparse-cu12==[0m[91m12.3.0.142
[fastapi] [0m[91m + [0m[91mnvidia-cusparse-cu12==[0m[91m12.3[0m[91m.1.170[0m[91m
[fastapi] + [0m[91mnvidia-cusparselt-cu12[0m[91m==0.[0m[91m6.2[0m[91m
[fastapi] -[0m[91m nvidia-nccl-cu12==2.20.5
[fastapi] + nvidia-nccl-cu12==2.21.5
[fastapi] - nvidia-nvjitlink-cu12==12.4.99
[fastapi] + nvidia-nvjitlink-cu12==[0m[91m12.4.127
[fastapi] - nvidia-nvtx-cu12==12.4.99
[fastapi] + [0m[91mnvidia-nvtx-cu12==12[0m[91m.4.127
[fastapi] + opencv-python-headless==5.0.0.93
[fastapi] +[0m[91m outlines==0.1.11
[fastapi] +[0m[91m outlines-core==0.[0m[91m1.26[0m[91m
[fastapi] -[0m[91m packaging==[0m[91m23.[0m[91m2
[fastapi] +[0m[91m [0m[91mpackaging==26.[0m[91m3[0m[91m
[fastapi] +[0m[91m partial-json-parser[0m[91m==0[0m[91m.2.[0m[91m1.1[0m[91m.post[0m[91m7
[fastapi] [0m[91m- [0m[91mpillow[0m[91m==10.[0m[91m2[0m[91m.0
[fastapi] [0m[91m [0m[91m+[0m[91m pillow==12.3.0
[fastapi] +[0m[91m prometheus-fastapi-instrumentator==8.1.0
[fastapi] + pycountry==26.2.16
[fastapi] + pydantic-extra-types==2.11.1
[fastapi] + pydantic-settings[0m[91m==2.15.0
[fastapi] + python-multipart[0m[91m==0.0.32[0m[91m
[fastapi] + ray[0m[91m==2.[0m[91m58.0
[fastapi] [0m[91m + [0m[91mrich==[0m[91m15.0.0
[fastapi] [0m[91m + rich-toolkit==[0m[91m0.20.[0m[91m5
[fastapi] [0m[91m+ rignore[0m[91m==0.8[0m[91m.1
[fastapi] + shellingham[0m[91m==1.[0m[91m5.4[0m[91m
[fastapi] -[0m[91m sympy==1.12
[fastapi] +[0m[91m sympy==1.[0m[91m13.1
[fastapi] [0m[91m - [0m[91mtorch==[0m[91m2.4.[0m[91m1+[0m[91mcu124
[fastapi] + torch==2.6.0
[fastapi] [0m[91m - torchaudio==2.4.[0m[91m1+cu124[0m[91m
[fastapi] + torchaudio==2.6.0[0m[91m
[fastapi] - torchvision==[0m[91m0.19[0m[91m.1+cu124
[fastapi] + torchvision==0.21.[0m[91m0
[fastapi] - triton[0m[91m==3.0.[0m[91m0
[fastapi] + triton[0m[91m==3.2.[0m[91m0
[fastapi] [0m[91m - [0m[91mtyper==0[0m[91m.9.0[0m[91m
[fastapi] + typer==0.[0m[91m27.2[0m[91m
[fastapi] [0m[91m + uvloop[0m[91m==0.22.1
[fastapi] + [0m[91mvllm==0.[0m[91m8.3
[fastapi] [0m[91m+ watchfiles==1.2[0m[91m.0
[fastapi] + websockets[0m[91m==17.1[0m[91m
[fastapi] + xformers[0m[91m==0.0.[0m[91m29.post2
[fastapi] [0m[91m+ xgrammar==0.1[0m[91m.17
[fastapi] [0mCollecting fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0
[fastapi] Cloning https://github.com/rayonlabs/fiber.git (to revision 2.4.0) to /tmp/pip-install-an9oaqpa/fiber_5a11df5ca061433b8b84b9c5caba4754
[fastapi] [91m  Running command git clone --filter=blob:none --quiet https://github.com/rayonlabs/fiber.git /tmp/pip-install-an9oaqpa/fiber_5a11df5ca061433b8b84b9c5caba4754
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
[fastapi] Requirement already satisfied: certifi>=2019.3.9 in /usr/local/lib/python3.11/dist-packages (from substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2024.8.30)
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
[fastapi] Requirement already satisfied: websockets>=14.1 in /usr/local/lib/python3.11/dist-packages (from async-substrate-interface<2.0.0,>=1.0.0->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (17.1)
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
[fastapi] Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.11/dist-packages (from requests<3,>=2.21.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (3.3.2)
[fastapi] Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.11/dist-packages (from requests<3,>=2.21.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2.2.3)
[fastapi] Requirement already satisfied: more-itertools in /usr/lib/python3/dist-packages (from scalecodec<1.3,>=1.2.10->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (8.10.0)
[fastapi] Requirement already satisfied: pycparser in /usr/local/lib/python3.11/dist-packages (from cffi>=2.0.0->PyNaCl<2,>=1.0.1->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0) (2.22)
[fastapi] Collecting toolz>=0.8.0 (from cytoolz>=0.10.1->eth-utils<3,>=1.3.0->substrate-interface==1.7.10->fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0)
[fastapi] Downloading toolz-1.1.0-py3-none-any.whl.metadata (5.1 kB)
[fastapi] Downloading bittensor_commit_reveal-0.1.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (552 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 552.2/552.2 kB 53.8 MB/s eta 0:00:00
[fastapi] Downloading eth_typing-5.0.0-py3-none-any.whl (20 kB)
[fastapi] Downloading netaddr-1.3.0-py3-none-any.whl (2.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.3/2.3 MB 195.1 MB/s eta 0:00:00
[fastapi] Downloading python_dotenv-1.0.1-py3-none-any.whl (19 kB)
[fastapi] Downloading substrate_interface-1.7.10-py3-none-any.whl (60 kB)
[fastapi] Downloading tenacity-9.0.0-py3-none-any.whl (28 kB)
[fastapi] Downloading async_substrate_interface-1.6.4-py3-none-any.whl (97 kB)
[fastapi] Downloading bt_decode-0.8.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (647 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 647.8/647.8 kB 96.0 MB/s eta 0:00:00
[fastapi] Downloading colorama-0.4.6-py2.py3-none-any.whl (25 kB)
[fastapi] Downloading pydantic-2.9.2-py3-none-any.whl (434 kB)
[fastapi] Downloading pydantic_core-2.23.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 188.0 MB/s eta 0:00:00
[fastapi] Downloading aiosqlite-0.22.1-py3-none-any.whl (17 kB)
[fastapi] Downloading base58-2.1.1-py3-none-any.whl (5.6 kB)
[fastapi] Downloading ecdsa-0.19.2-py2.py3-none-any.whl (150 kB)
[fastapi] Downloading eth_keys-0.8.0-py3-none-any.whl (20 kB)
[fastapi] Downloading eth_utils-2.3.2-py3-none-any.whl (77 kB)
[fastapi] Downloading py_bip39_bindings-0.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (432 kB)
[fastapi] Downloading py_ed25519_zebra_bindings-1.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (323 kB)
[fastapi] Downloading py_sr25519_bindings-0.2.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (372 kB)
[fastapi] Downloading pynacl-1.6.2-cp38-abi3-manylinux_2_34_x86_64.whl (1.4 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.4/1.4 MB 173.6 MB/s eta 0:00:00
[fastapi] Downloading scalecodec-1.2.12-py3-none-any.whl (99 kB)
[fastapi] Downloading xxhash-3.8.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (220 kB)
[fastapi] Downloading cytoolz-1.1.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (2.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.8/2.8 MB 200.8 MB/s eta 0:00:00
[fastapi] Downloading eth_hash-0.8.0-py3-none-any.whl (8.0 kB)
[fastapi] Downloading toolz-1.1.0-py3-none-any.whl (58 kB)
[fastapi] Building wheels for collected packages: fiber
[fastapi] Building wheel for fiber (pyproject.toml): started
[fastapi] Building wheel for fiber (pyproject.toml): finished with status 'done'
[fastapi] Created wheel for fiber: filename=fiber-2.4.0-py3-none-any.whl size=51790 sha256=c50f803eff2fbcdf01560cfffdc65a3891a75b0b315d61d842fd3861f51b5d73
[fastapi] Stored in directory: /tmp/pip-ephem-wheel-cache-g6jxve6d/wheels/d1/5e/21/2fa1f403cd187996037f04f6328bf11973ce31440a275f6949
[fastapi] Successfully built fiber
[fastapi] Installing collected packages: xxhash, toolz, tenacity, python-dotenv, pydantic-core, py-sr25519-bindings, py-ed25519-zebra-bindings, py-bip39-bindings, netaddr, eth-typing, eth-hash, ecdsa, colorama, bt-decode, bittensor-commit-reveal, base58, aiosqlite, scalecodec, PyNaCl, pydantic, cytoolz, eth-utils, async-substrate-interface, eth-keys, substrate-interface, fiber
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
[fastapi] [0mSuccessfully installed PyNaCl-1.6.2 aiosqlite-0.22.1 async-substrate-interface-1.6.4 base58-2.1.1 bittensor-commit-reveal-0.1.0 bt-decode-0.8.0 colorama-0.4.6 cytoolz-1.1.0 ecdsa-0.19.2 eth-hash-0.8.0 eth-keys-0.8.0 eth-typing-5.0.0 eth-utils-2.3.2 fiber-2.4.0 netaddr-1.3.0 py-bip39-bindings-0.3.0 py-ed25519-zebra-bindings-1.3.0 py-sr25519-bindings-0.2.4 pydantic-2.9.2 pydantic-core-2.23.4 python-dotenv-1.0.1 scalecodec-1.2.12 substrate-interface-1.7.10 tenacity-9.0.0 toolz-1.1.0 xxhash-3.8.1
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0m ---> a913b1e6a318
[fastapi] Step 13/13 : ENTRYPOINT ["./entrypoint.sh"]
[fastapi] ---> Running in 2bfdd74aca5f
[fastapi] ---> 97213e5ea6d4
[fastapi] {'aux': {'ID': 'sha256:97213e5ea6d4544d95f776fecb53eec3a2c1569463f18e9988d2dab5b2c5cbe3'}}Successfully built 97213e5ea6d4
[fastapi] Successfully tagged standalone-text-trainer:f6e8370f-5756-47c1-bd5a-d0fc03efc8af
[fastapi] Docker image built successfully.
[fastapi] Container.wait() returned: {'StatusCode': 0}
[fastapi] Cleaning up
[fastapi] Cleaned up Docker resources.
[fastapi] Starting upload container hf-upload-7809eb525ae74f32be76a70d6cb0a1eb for task 4022aee4-05b1-4533-b1d9-0c6f52bbb747...
[hf-upload-78]  adapter_config.json not found
[hf-upload-78] README.md not found
[hf-upload-78] Creating repo gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-7b63e4e3-55a6-4035-ae8b-898e676662c6-5GU4Xkd3...
[hf-upload-78] Uploading contents of /app/checkpoints/4022aee4-05b1-4533-b1d9-0c6f52bbb747/tournament-tourn_5c64e784a087074a_20260914-7b63e4e3-55a6-4035-ae8b-898e676662c6-5GU4Xkd3 to gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-7b63e4e3-55a6-4035-ae8b-898e676662c6-5GU4Xkd3
[hf-upload-78] Uploaded successfully to https://huggingface.co/gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-7b63e4e3-55a6-4035-ae8b-898e676662c6-5GU4Xkd3
[hf-upload-78] Deleted local folder: /app/checkpoints/4022aee4-05b1-4533-b1d9-0c6f52bbb747/tournament-tourn_5c64e784a087074a_20260914-7b63e4e3-55a6-4035-ae8b-898e676662c6-5GU4Xkd3
[text-trainer] *****Running text trainer
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_hash" in MinerSubmission has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] /workspace/axo_py/lib/python3.11/site-packages/requests/__init__.py:113: RequestsDependencyWarning: urllib3 (2.8.0) or chardet (6.0.0.post1)/charset_normalizer (3.5.1) doesn't match a supported version!
[text-trainer]   warnings.warn(
[text-trainer] W0916 10:02:01.585000 868 torch/distributed/run.py:792] 
[text-trainer] W0916 10:02:01.585000 868 torch/distributed/run.py:792] *****************************************
[text-trainer] W0916 10:02:01.585000 868 torch/distributed/run.py:792] Setting OMP_NUM_THREADS environment variable for each process to be 1 in default, to avoid your system being overloaded, please further tune the variable for optimal performance in your application as needed. 
[text-trainer] W0916 10:02:01.585000 868 torch/distributed/run.py:792] *****************************************
[text-trainer] [W916 10:02:01.713979183 socket.cpp:204] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W916 10:02:01.714344888 socket.cpp:204] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] df: /root/.triton/autotune: No such file or directory
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] [W916 10:02:12.915953505 socket.cpp:204] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W916 10:02:12.916382608 socket.cpp:204] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W916 10:02:12.091981942 socket.cpp:204] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W916 10:02:12.092322704 socket.cpp:204] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] /workspace/scripts/train_instruct.py:537: FutureWarning: `tokenizer` is deprecated and will be removed in version 5.0.0 for `Trainer.__init__`. Use `processing_class` instead.
[text-trainer]   trainer = _trainer_cls(**_trainer_kwargs)
[text-trainer] /workspace/scripts/train_instruct.py:537: FutureWarning: `tokenizer` is deprecated and will be removed in version 5.0.0 for `Trainer.__init__`. Use `processing_class` instead.
[text-trainer]   trainer = _trainer_cls(**_trainer_kwargs)
[text-trainer] *****Running text trainer
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_hash" in MinerSubmission has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] /workspace/axo_py/lib/python3.11/site-packages/requests/__init__.py:113: RequestsDependencyWarning: urllib3 (2.8.0) or chardet (6.0.0.post1)/charset_normalizer (3.5.1) doesn't match a supported version!
[text-trainer]   warnings.warn(
[text-trainer] W0916 12:21:54.450000 868 torch/distributed/run.py:792] 
[text-trainer] W0916 12:21:54.450000 868 torch/distributed/run.py:792] *****************************************
[text-trainer] W0916 12:21:54.450000 868 torch/distributed/run.py:792] Setting OMP_NUM_THREADS environment variable for each process to be 1 in default, to avoid your system being overloaded, please further tune the variable for optimal performance in your application as needed. 
[text-trainer] W0916 12:21:54.450000 868 torch/distributed/run.py:792] *****************************************
[text-trainer] [W916 12:21:54.579044922 socket.cpp:204] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W916 12:21:54.579439628 socket.cpp:204] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] df: /root/.triton/autotune: No such file or directory
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] [W916 12:22:05.637149086 socket.cpp:204] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W916 12:22:05.637583785 socket.cpp:204] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W916 12:22:05.823521412 socket.cpp:204] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W916 12:22:05.823861820 socket.cpp:204] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] /workspace/scripts/train_instruct.py:537: FutureWarning: `tokenizer` is deprecated and will be removed in version 5.0.0 for `Trainer.__init__`. Use `processing_class` instead.
[text-trainer]   trainer = _trainer_cls(**_trainer_kwargs)
[text-trainer] /workspace/scripts/train_instruct.py:537: FutureWarning: `tokenizer` is deprecated and will be removed in version 5.0.0 for `Trainer.__init__`. Use `processing_class` instead.
[text-trainer]   trainer = _trainer_cls(**_trainer_kwargs)
[text-trainer] wandb: WARNING The `run_name` is currently set to the same value as `TrainingArguments.output_dir`. If this was not intended, please specify a different run name by setting the `TrainingArguments.run_name` parameter.
[text-trainer] wandb: Tracking run with wandb version 0.19.10
[text-trainer] wandb: W&B syncing is set to `offline` in this directory. Run `wandb online` or set WANDB_MODE=online to enable cloud syncing.
[text-trainer] [1;34mwandb[0m: 
[text-trainer] [1;34mwandb[0m: You can sync this run to the cloud by running:
[text-trainer] [1;34mwandb[0m: [1mwandb sync /app/checkpoints/wandb_logs/4022aee4-05b1-4533-b1d9-0c6f52bbb747_5GU4Xkd3dCGTU3s8VLcHGc5wsD5M8XyxDca5yDQhYm1mVXFu/wandb/offline-run-20260916_123754-4022aee4-05b1-4533-b1d9-0c6f52bbb747_tournament-tourn_5c64e784a087074a_20260914-7b63e4e3-55a6-4035-ae8b-898e676662c6-5GU4Xkd3[0m
[text-trainer] [1;34mwandb[0m: Find logs at: [1;35m../../app/checkpoints/wandb_logs/4022aee4-05b1-4533-b1d9-0c6f52bbb747_5GU4Xkd3dCGTU3s8VLcHGc5wsD5M8XyxDca5yDQhYm1mVXFu/wandb/offline-run-20260916_123754-4022aee4-05b1-4533-b1d9-0c6f52bbb747_tournament-tourn_5c64e784a087074a_20260914-7b63e4e3-55a6-4035-ae8b-898e676662c6-5GU4Xkd3/logs[0m
[text-trainer] [rank0]:[W916 13:27:16.074323773 ProcessGroupNCCL.cpp:1496] Warning: WARNING: destroy_process_group() was not called before program exit, which can leak resources. For more info, please see https://pytorch.org/docs/stable/distributed.html#shutdown (function operator())
[text-trainer] *****Running text trainer
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_hash" in MinerSubmission has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] /workspace/axo_py/lib/python3.11/site-packages/requests/__init__.py:113: RequestsDependencyWarning: urllib3 (2.8.0) or chardet (6.0.0.post1)/charset_normalizer (3.5.1) doesn't match a supported version!
[text-trainer]   warnings.warn(
[text-trainer] W0915 20:59:10.412000 924 torch/distributed/run.py:792] 
[text-trainer] W0915 20:59:10.412000 924 torch/distributed/run.py:792] *****************************************
[text-trainer] W0915 20:59:10.412000 924 torch/distributed/run.py:792] Setting OMP_NUM_THREADS environment variable for each process to be 1 in default, to avoid your system being overloaded, please further tune the variable for optimal performance in your application as needed. 
[text-trainer] W0915 20:59:10.412000 924 torch/distributed/run.py:792] *****************************************
[text-trainer] [W915 20:59:10.458734711 socket.cpp:204] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W915 20:59:10.460324098 socket.cpp:204] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] df: /root/.triton/autotune: No such file or directory
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] [W915 21:03:12.911662192 socket.cpp:204] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W915 21:03:12.911887774 socket.cpp:204] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W915 21:03:12.913301817 socket.cpp:204] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W915 21:03:12.914371703 socket.cpp:204] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] /workspace/scripts/train_instruct.py:537: FutureWarning: `tokenizer` is deprecated and will be removed in version 5.0.0 for `Trainer.__init__`. Use `processing_class` instead.
[text-trainer]   trainer = _trainer_cls(**_trainer_kwargs)
[text-trainer] /workspace/scripts/train_instruct.py:537: FutureWarning: `tokenizer` is deprecated and will be removed in version 5.0.0 for `Trainer.__init__`. Use `processing_class` instead.
[text-trainer]   trainer = _trainer_cls(**_trainer_kwargs)
[text-trainer] wandb: WARNING The `run_name` is currently set to the same value as `TrainingArguments.output_dir`. If this was not intended, please specify a different run name by setting the `TrainingArguments.run_name` parameter.
[text-trainer] wandb: Tracking run with wandb version 0.19.10
[text-trainer] wandb: W&B syncing is set to `offline` in this directory. Run `wandb online` or set WANDB_MODE=online to enable cloud syncing.