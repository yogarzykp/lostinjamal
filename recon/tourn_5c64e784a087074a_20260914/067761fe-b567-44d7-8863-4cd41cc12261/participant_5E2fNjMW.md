# Loki — task 067761fe-b567-44d7-8863-4cd41cc12261 — hotkey 5E2fNjMWkC7NhjFsobwdDT1ym9R8ws7iDMnaZtE1RcnAsfZf
fetched 2026-09-19T05:00:19+00:00  lines=1534  hit_page_cap=False  containers=['downloader-067761fe-b567-44d7-8863-4cd41cc12261-4da51d52', 'fastapi', 'hf-upload-3230fe6e8b9945ca82a6c4b2d24345ed', 'text-trainer-2c341559108747e49f0653913f89ab77']

[downloader-0] Downloading datasets to: /cache/datasets
[downloader-0] Downloading models to: /cache/models
[downloader-0] Model already cached at /cache/models/c53e93d87a4fe77f.
[downloader-0] Skipping download.
[downloader-0] Model path: /cache/models/c53e93d87a4fe77f
[downloader-0] Dataset path: /cache/datasets
[fastapi] Repository cloned successfully
[fastapi] Running Cache Download Container
[fastapi] Starting downloader container: downloader-067761fe-b567-44d7-8863-4cd41cc12261-4da51d52
[fastapi] Download completed successfully for task 067761fe-b567-44d7-8863-4cd41cc12261
[fastapi] Building Docker image 'standalone-text-trainer:b87ca400-5f50-4b20-a8c8-708f4749c818' (timeout=1800s)...
[fastapi] Step 1/14 : FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04
[fastapi] ---> ff5fe688608b
[fastapi] Step 2/14 : RUN apt-get update && apt-get install -y     vim     zip     tmux     iotop     nvtop     bmon     wget     nano     zsh     htop     && rm -rf /var/lib/apt/lists/*
[fastapi] ---> Running in ba444056b7e2
[fastapi] Get:1 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  InRelease [1578 B]
[fastapi] Get:2 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  Packages [3009 kB]
[fastapi] Get:3 http://security.ubuntu.com/ubuntu jammy-security InRelease [129 kB]
[fastapi] Get:4 http://archive.ubuntu.com/ubuntu jammy InRelease [270 kB]
[fastapi] Get:5 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy InRelease [18.1 kB]
[fastapi] Get:6 http://security.ubuntu.com/ubuntu jammy-security/restricted amd64 Packages [7717 kB]
[fastapi] Get:7 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [128 kB]
[fastapi] Get:8 http://archive.ubuntu.com/ubuntu jammy-backports InRelease [127 kB]
[fastapi] Get:9 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy/main amd64 Packages [44.3 kB]
[fastapi] Get:10 http://archive.ubuntu.com/ubuntu jammy/main amd64 Packages [1792 kB]
[fastapi] Get:11 http://archive.ubuntu.com/ubuntu jammy/multiverse amd64 Packages [266 kB]
[fastapi] Get:12 http://archive.ubuntu.com/ubuntu jammy/restricted amd64 Packages [164 kB]
[fastapi] Get:13 http://archive.ubuntu.com/ubuntu jammy/universe amd64 Packages [17.5 MB]
[fastapi] Get:14 http://security.ubuntu.com/ubuntu jammy-security/universe amd64 Packages [1317 kB]
[fastapi] Get:15 http://security.ubuntu.com/ubuntu jammy-security/main amd64 Packages [4290 kB]
[fastapi] Get:16 http://security.ubuntu.com/ubuntu jammy-security/multiverse amd64 Packages [84.6 kB]
[fastapi] Get:17 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 Packages [4624 kB]
[fastapi] Get:18 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 Packages [1620 kB]
[fastapi] Get:19 http://archive.ubuntu.com/ubuntu jammy-updates/restricted amd64 Packages [8007 kB]
[fastapi] Get:20 http://archive.ubuntu.com/ubuntu jammy-updates/multiverse amd64 Packages [93.2 kB]
[fastapi] Get:21 http://archive.ubuntu.com/ubuntu jammy-backports/universe amd64 Packages [35.6 kB]
[fastapi] Get:22 http://archive.ubuntu.com/ubuntu jammy-backports/main amd64 Packages [82.8 kB]
[fastapi] Fetched 51.3 MB in 3s (16.2 MB/s)
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
[fastapi] [0mFetched 23.1 MB in 1s (29.2 MB/s)
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
[fastapi] ---> 96704055f320
[fastapi] Step 3/14 : RUN mkdir -p /workspace
[fastapi] ---> Running in be72762b6e52
[fastapi] ---> 8e354bb4838a
[fastapi] Step 4/14 : RUN mkdir -p /cache
[fastapi] ---> Running in f088389fb48b
[fastapi] ---> d4364a615491
[fastapi] Step 5/14 : RUN mkdir -p /workspace/scripts/datasets
[fastapi] ---> Running in 30d59330a406
[fastapi] ---> 6fe33c16fd34
[fastapi] Step 6/14 : RUN mkdir -p /app/checkpoints
[fastapi] ---> Running in 5d39b7998387
[fastapi] ---> ef94845fc813
[fastapi] Step 7/14 : WORKDIR /workspace/scripts
[fastapi] ---> Running in 44442504b0bf
[fastapi] ---> c1cf3b1a7e95
[fastapi] Step 8/14 : COPY scripts /workspace/scripts
[fastapi] ---> 379142b339a5
[fastapi] Step 9/14 : RUN chmod +x /workspace/scripts/entrypoint.sh
[fastapi] ---> Running in 06df9f4575cf
[fastapi] ---> fbfff5a081a7
[fastapi] Step 10/14 : RUN python -m venv /workspace/axo_py
[fastapi] ---> Running in e58e1ef7b0ab
[fastapi] ---> 0fdc72da388e
[fastapi] Step 11/14 : RUN bash -c "source /workspace/axo_py/bin/activate &&     pip install uv &&     pip install -U packaging==23.2 setuptools==75.8.0 wheel ninja &&     uv pip install --no-build-isolation axolotl==0.9.1 &&     pip install requests==2.32.3 &&     deactivate"
[fastapi] ---> Running in 2eab6370ffb4
[fastapi] Collecting uv
[fastapi] Downloading uv-0.12.14-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] Downloading uv-0.12.14-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.0 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 20.0/20.0 MB 182.8 MB/s eta 0:00:00
[fastapi] Installing collected packages: uv
[fastapi] Successfully installed uv-0.12.14
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
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 53.0/53.0 kB 6.5 MB/s eta 0:00:00
[fastapi] Downloading setuptools-75.8.0-py3-none-any.whl (1.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 55.3 MB/s eta 0:00:00
[fastapi] Downloading wheel-0.45.1-py3-none-any.whl (72 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 72.5/72.5 kB 19.0 MB/s eta 0:00:00
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (183 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 183.4/183.4 kB 53.3 MB/s eta 0:00:00
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
[fastapi] [0m[91mResolved 217 packages in 1.32s
[fastapi] [0m[91mDownloading cryptography (4.5MiB)
[fastapi] [0m[91mDownloading pygments (1.2MiB)
[fastapi] [0m[91mDownloading scipy (33.7MiB)
[fastapi] [0m[91mDownloading networkx (2.0MiB)
[fastapi] [0m[91mDownloading torchao (5.4MiB)
[fastapi] [0m[91mDownloading botocore (13.7MiB)
[fastapi] [0m[91mDownloading aiohttp (1.7MiB)
[fastapi] [0m[91mDownloading tensorboard (5.3MiB)
[fastapi] [0m[91mDownloading numpy (18.6MiB)
[fastapi] [0m[91mDownloading grpcio (6.9MiB)
[fastapi] [0m[91mDownloading oci (35.2MiB)
[fastapi] [0m[91mDownloading hf-transfer (3.4MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-cupti-cu12 (13.2MiB)
[fastapi] [0m[91mDownloading zstandard (5.2MiB)
[fastapi] [0m[91mDownloading ruff (9.9MiB)
[fastapi] [0m[91mDownloading gradio (44.3MiB)
[fastapi] [0m[91mDownloading lm-eval (2.4MiB)
[fastapi] [0m[91mDownloading tokenizers (3.0MiB)
[fastapi] [0m[91mDownloading nvidia-cusolver-cu12 (122.0MiB)
[fastapi] [0m[91mDownloading bitsandbytes (72.5MiB)
[fastapi] [0m[91mDownloading transformers (9.9MiB)
[fastapi] [0m[91mDownloading lxml (5.0MiB)
[fastapi] [0m[91mDownloading nvidia-nccl-cu12 (179.9MiB)
[fastapi] [0m[91mDownloading nvidia-cudnn-cu12 (634.0MiB)
[fastapi] [0m[91mDownloading triton (241.4MiB)
[fastapi] [0m[91mDownloading pydantic-core (1.9MiB)
[fastapi] [0m[91mDownloading numba (3.6MiB)
[fastapi] [0m[91mDownloading tensorboard-data-server (6.3MiB)
[fastapi] [0m[91mDownloading scikit-learn (11.6MiB)
[fastapi] [0m[91mDownloading pandas (12.2MiB)
[fastapi] [0m[91mDownloading pillow (6.3MiB)
[fastapi] [0m[91mDownloading sympy (5.9MiB)
[fastapi] [0m[91mDownloading nltk (1.7MiB)
[fastapi] [0m[91mDownloading wandb (24.9MiB)
[fastapi] [0m[91mDownloading nvidia-cusparselt-cu12 (143.1MiB)
[fastapi] [0m[91mDownloading nvidia-nvjitlink-cu12 (20.1MiB)
[fastapi] [0m[91mDownloading nvidia-cusparse-cu12 (197.8MiB)
[fastapi] [0m[91mDownloading nvidia-cufft-cu12 (201.7MiB)
[fastapi] [0m[91mDownloading sentencepiece (1.3MiB)
[fastapi] [0m[91mDownloading torch (731.2MiB)
[fastapi] [0m[91mDownloading nvidia-cublas-cu12 (346.6MiB)
[fastapi] [0m[91mDownloading pyarrow (47.7MiB)
[fastapi] [0m[91mDownloading xformers (42.2MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-nvrtc-cu12 (23.5MiB)
[fastapi] [0m[91mDownloading nvidia-curand-cu12 (53.7MiB)
[fastapi] [0m[91mDownloading llvmlite (57.1MiB)
[fastapi] [0m[91mDownloading hf-xet (51.1MiB)
[fastapi] [0m[91m Downloaded pygments
[fastapi] [0m[91m Downloaded aiohttp
[fastapi] [0m[91m Downloaded sentencepiece
[fastapi] [0m[91m Downloaded networkx
[fastapi] [0m[91m Downloaded nltk
[fastapi] [0m[91m Downloaded pydantic-core
[fastapi] [0m[91m Downloaded lm-eval
[fastapi] [0m[91m   Building axolotl==0.9.1
[fastapi] [0m[91m   Building axolotl-contribs-mit==0.0.3
[fastapi] [0m[91m   Building langdetect==1.0.9
[fastapi] [0m[91m Downloaded tokenizers
[fastapi] [0m[91m   Building word2number==1.1
[fastapi] [0m[91m   Building axolotl-contribs-lgpl==0.0.6
[fastapi] [0m[91m Downloaded hf-transfer
[fastapi] [0m[91m   Building rouge-score==0.1.2
[fastapi] [0m[91m   Building sqlitedict==2.1.0
[fastapi] [0m[91m Downloaded numba
[fastapi] [0m[91m   Building hqq==0.2.5
[fastapi] [0m[91m   Building grpclib==0.4.7
[fastapi] [0m[91m      Built axolotl-contribs-mit==0.0.3
[fastapi] [0m[91m Downloaded cryptography
[fastapi] [0m[91m      Built word2number==1.1
[fastapi] [0m[91m      Built axolotl-contribs-lgpl==0.0.6
[fastapi] [0m[91m      Built rouge-score==0.1.2
[fastapi] [0m[91m Downloaded torchao
[fastapi] [0m[91m Downloaded zstandard
[fastapi] [0m[91m Downloaded lxml
[fastapi] [0m[91m      Built sqlitedict==2.1.0
[fastapi] [0m[91m Downloaded tensorboard
[fastapi] [0m[91m Downloaded sympy
[fastapi] [0m[91m      Built axolotl==0.9.1
[fastapi] [0m[91m Downloaded grpcio
[fastapi] [0m[91m      Built grpclib==0.4.7
[fastapi] [0m[91m Downloaded tensorboard-data-server
[fastapi] [0m[91m Downloaded pillow
[fastapi] [0m[91m      Built langdetect==1.0.9
[fastapi] [0m[91m Downloaded transformers
[fastapi] [0m[91m Downloaded ruff
[fastapi] [0m[91m      Built hqq==0.2.5
[fastapi] [0m[91m Downloaded scikit-learn
[fastapi] [0m[91m Downloaded pandas
[fastapi] [0m[91m Downloaded botocore
[fastapi] [0m[91m Downloaded nvidia-cuda-cupti-cu12
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
[fastapi] [0m[91mPrepared 215 packages in 8.35s
[fastapi] [0m[91mInstalled 215 packages in 443ms
[fastapi] [0m[91m + absl-py==2.5.0
[fastapi] + accelerate==1.6.0
[fastapi] + addict==2.4.0
[fastapi] + adlfs==2026.8.0
[fastapi] + aiobotocore==2.26.0
[fastapi] + [0m[91maiofiles==23.2.1
[fastapi] + aiohappyeyeballs==2.7.1
[fastapi] + [0m[91maiohttp==3.[0m[91m14.3
[fastapi] + aioitertools==0.13.0
[fastapi] [0m[91m+ aiosignal==1.4.0
[fastapi] + annotated-doc==0.0.[0m[91m5
[fastapi] + annotated-types[0m[91m==0.8.0[0m[91m
[fastapi] + antlr4-python3-runtime[0m[91m==4.13[0m[91m.2
[fastapi] [0m[91m+ anyio==[0m[91m4.15.1
[fastapi] [0m[91m + art==6.5
[fastapi] [0m[91m + attrs==26.1.0
[fastapi] + autoawq==0.2.[0m[91m7.post3
[fastapi] + axolotl==0.[0m[91m9.1
[fastapi] + axolotl-contribs-lgpl==0.0.[0m[91m6[0m[91m
[fastapi] + [0m[91maxolotl-contribs-mit==0[0m[91m.0.3
[fastapi] [0m[91m + azure-core==1.41.0
[fastapi] + azure-identity[0m[91m==1.25.3
[fastapi] +[0m[91m azure-storage-blob==12.[0m[91m30.1
[fastapi] + bitsandbytes==0.45.4
[fastapi] + botocore==[0m[91m1.41.5
[fastapi] + certifi[0m[91m==2026.7.[0m[91m22
[fastapi] + [0m[91mcffi==2.1.1
[fastapi] + chardet==6.0[0m[91m.0.post1
[fastapi] + charset-normalizer==[0m[91m3.5.1
[fastapi] [0m[91m + circuitbreaker==2.1.3[0m[91m
[fastapi] + click==[0m[91m8.5.0
[fastapi] + cloudpickle[0m[91m==3.1.2[0m[91m
[fastapi] + colorama==0[0m[91m.4.6
[fastapi] [0m[91m+ coloredlogs==[0m[91m15.0.1
[fastapi] [0m[91m + crc32c[0m[91m==2.8
[fastapi] +[0m[91m cryptography==50.0[0m[91m.1
[fastapi] +[0m[91m dataproperty==1[0m[91m.1.1
[fastapi] [0m[91m+ datasets==[0m[91m3.5.1
[fastapi] + decorator==5[0m[91m.3.1
[fastapi] +[0m[91m defusedxml[0m[91m==0.[0m[91m7.[0m[91m1
[fastapi] +[0m[91m dill[0m[91m==0.[0m[91m3.8
[fastapi] [0m[91m+ einops==[0m[91m0.8.2
[fastapi] + evaluate==0.4.[0m[91m1
[fastapi] + fastapi==0.141[0m[91m.1
[fastapi] + fastcore[0m[91m==2.2[0m[91m.27
[fastapi] [0m[91m+ ffmpy==1.0.0[0m[91m
[fastapi] + filelock==3.32.6
[fastapi] [0m[91m + fire==0.[0m[91m7.1
[fastapi] [0m[91m+[0m[91m frozenlist==1[0m[91m.8.[0m[91m0[0m[91m
[fastapi] +[0m[91m fsspec[0m[91m==2025.[0m[91m3.[0m[91m0
[fastapi] [0m[91m+ [0m[91mgcsfs==2025[0m[91m.[0m[91m3.0
[fastapi] [0m[91m+[0m[91m google-api-core[0m[91m==2.33[0m[91m.0
[fastapi] + google-auth==2.58.0
[fastapi] + google-auth-oauthlib[0m[91m==1.4.1[0m[91m
[fastapi] [0m[91m+ google-cloud-core[0m[91m==[0m[91m2.7.0
[fastapi] + google-cloud-storage[0m[91m==3.14[0m[91m.1
[fastapi] [0m[91m +[0m[91m google-crc32c[0m[91m==1.8.0
[fastapi] + google-resumable-media[0m[91m==2.10.2
[fastapi] +[0m[91m googleapis-common-protos==1[0m[91m.75.0
[fastapi] + gradio[0m[91m==5.23[0m[91m.3[0m[91m
[fastapi] [0m[91m+ gradio-client[0m[91m==1.8.[0m[91m0
[fastapi] + groovy[0m[91m==0.[0m[91m1.[0m[91m2
[fastapi] +[0m[91m [0m[91mgrpcio==[0m[91m1.[0m[91m84.0[0m[91m
[fastapi] + [0m[91mgrpclib==[0m[91m0.4.7
[fastapi] + h11==0.16.0[0m[91m
[fastapi] + h2==4[0m[91m.4.1[0m[91m
[fastapi] [0m[91m+ hf-transfer==[0m[91m0.1.[0m[91m9
[fastapi] +[0m[91m [0m[91mhf-xet==1[0m[91m.1.[0m[91m0[0m[91m
[fastapi] + [0m[91mhpack[0m[91m==4.2.0[0m[91m
[fastapi] [0m[91m + [0m[91mhqq[0m[91m==0.2.5
[fastapi] + httpcore==[0m[91m1.0.9
[fastapi] + httpx==[0m[91m0.28.1
[fastapi] + huggingface-hub==[0m[91m0.31.[0m[91m0
[fastapi] [0m[91m+ [0m[91mhumanfriendly[0m[91m==10.[0m[91m0
[fastapi] [0m[91m+ hyperframe==[0m[91m6[0m[91m.1.0[0m[91m
[fastapi] [0m[91m + [0m[91midna[0m[91m==3.19
[fastapi] [0m[91m + immutabledict==4.2.[0m[91m0
[fastapi] [0m[91m+[0m[91m isodate==[0m[91m0[0m[91m.7.2[0m[91m
[fastapi] [0m[91m +[0m[91m jinja2==3.1.6
[fastapi] [0m[91m+ jmespath[0m[91m==1.1[0m[91m.0[0m[91m
[fastapi] [0m[91m + [0m[91mjoblib==[0m[91m1.6.[0m[91m0
[fastapi] [0m[91m+[0m[91m jsonlines[0m[91m==4.[0m[91m0.[0m[91m0
[fastapi] [0m[91m+ langdetect[0m[91m==1.0.9[0m[91m
[fastapi] [0m[91m +[0m[91m liger-kernel[0m[91m==0.5.9
[fastapi] + llvmlite==[0m[91m0.49.0
[fastapi] + lm-eval==0.4.7
[fastapi] [0m[91m+ lxml==6.1[0m[91m.3
[fastapi] [0m[91m+ markdown==3.10.3[0m[91m
[fastapi] + markdown-it-py==4[0m[91m.2.0
[fastapi] [0m[91m + markupsafe[0m[91m==3.[0m[91m0.3
[fastapi] [0m[91m+ mbstrdecoder[0m[91m==1.1.5
[fastapi] + [0m[91mmdurl==0.1.2
[fastapi] + modal==0.70.[0m[91m5
[fastapi] + more-itertools==11.1[0m[91m.0
[fastapi] + mpmath[0m[91m==1.3.[0m[91m0
[fastapi] + msal==1.38.0[0m[91m
[fastapi] + [0m[91mmsal-extensions==[0m[91m1.3.[0m[91m1[0m[91m
[fastapi] +[0m[91m multidict[0m[91m==6[0m[91m.8.0[0m[91m
[fastapi] + multiprocess==0.[0m[91m70.16
[fastapi] +[0m[91m [0m[91mnetworkx==[0m[91m3.6.1[0m[91m
[fastapi] + nltk==3.[0m[91m10.3
[fastapi] [0m[91m+ numba==0[0m[91m.67.0
[fastapi] [0m[91m + numexpr[0m[91m==2.14[0m[91m.2
[fastapi] [0m[91m + [0m[91mnumpy==2.0.[0m[91m1
[fastapi] + nvidia-cublas-cu12==12[0m[91m.4.5.8
[fastapi] + nvidia-cuda-cupti-cu12==12[0m[91m.4.127
[fastapi] + [0m[91mnvidia-cuda-nvrtc-cu12==12.[0m[91m4.127
[fastapi] +[0m[91m nvidia-cuda-runtime-cu12[0m[91m==12.4.[0m[91m127
[fastapi] + [0m[91mnvidia-cudnn-cu12[0m[91m==9.1[0m[91m.0[0m[91m.70
[fastapi] [0m[91m+ [0m[91mnvidia-cufft-cu12[0m[91m==11[0m[91m.2.1[0m[91m.3[0m[91m
[fastapi] +[0m[91m nvidia-curand-cu12==10.3.5.147[0m[91m
[fastapi] + [0m[91mnvidia-cusolver-cu12==[0m[91m11.6[0m[91m.1.9[0m[91m
[fastapi] + nvidia-cusparse-cu12==[0m[91m12.3.1.170[0m[91m
[fastapi] + nvidia-cusparselt-cu12==[0m[91m0.6.2[0m[91m
[fastapi] + nvidia-ml-py[0m[91m==12.560.30
[fastapi] [0m[91m+ nvidia-nccl-cu12==[0m[91m2.21.5
[fastapi] [0m[91m+ nvidia-nvjitlink-cu12==[0m[91m12.4.127
[fastapi] [0m[91m + [0m[91mnvidia-nvtx-cu12==12.4.127
[fastapi] +[0m[91m oauthlib==3.3[0m[91m.1
[fastapi] +[0m[91m oci[0m[91m==2[0m[91m.186.0[0m[91m
[fastapi] +[0m[91m ocifs[0m[91m==1.3[0m[91m.2
[fastapi] [0m[91m [0m[91m+ opentelemetry-api[0m[91m==1.[0m[91m44.0[0m[91m
[fastapi] + [0m[91mopentelemetry-exporter-otlp-proto-common[0m[91m==1.44.[0m[91m0[0m[91m
[fastapi] [0m[91m + opentelemetry-exporter-otlp-proto-http==1.44.0
[fastapi] [0m[91m+ opentelemetry-proto==1.[0m[91m44[0m[91m.0
[fastapi] [0m[91m + [0m[91mopentelemetry-sdk==[0m[91m1.[0m[91m44.0[0m[91m
[fastapi] + [0m[91mopentelemetry-semantic-conventions[0m[91m==0.[0m[91m65[0m[91mb0
[fastapi] [0m[91m + optimum==1.16.2[0m[91m
[fastapi] + orjson[0m[91m==3.12.[0m[91m0
[fastapi] [0m[91m+[0m[91m pandas==2.3.3
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
[fastapi] [0mCollecting requests==2.32.3
[fastapi] Downloading requests-2.32.3-py3-none-any.whl.metadata (4.6 kB)
[fastapi] Requirement already satisfied: charset-normalizer<4,>=2 in /workspace/axo_py/lib/python3.11/site-packages (from requests==2.32.3) (3.5.1)
[fastapi] Requirement already satisfied: idna<4,>=2.5 in /workspace/axo_py/lib/python3.11/site-packages (from requests==2.32.3) (3.19)
[fastapi] Requirement already satisfied: urllib3<3,>=1.21.1 in /workspace/axo_py/lib/python3.11/site-packages (from requests==2.32.3) (2.7.0)
[fastapi] Requirement already satisfied: certifi>=2017.4.17 in /workspace/axo_py/lib/python3.11/site-packages (from requests==2.32.3) (2026.7.22)
[fastapi] Downloading requests-2.32.3-py3-none-any.whl (64 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 64.9/64.9 kB 3.0 MB/s eta 0:00:00
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
[fastapi] [0m ---> 306a015c195d
[fastapi] Step 12/14 : RUN pip install uv &&     pip install -U packaging==23.2 setuptools==75.8.0 wheel ninja &&     uv pip install -r /workspace/scripts/training_requirements.txt --system &&     pip install hf_transfer==0.1.9 &&     pip install tenacity==9.1.2 &&     pip install tiktoken==0.9.0 &&     pip install flash-attn==v2.7.4.post1 --no-build-isolation &&     uv pip install vllm==0.8.3 --system &&     pip install "fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0"
[fastapi] ---> Running in 01943af85558
[fastapi] Collecting uv
[fastapi] Using cached uv-0.12.14-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] Using cached uv-0.12.14-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.0 MB)
[fastapi] Installing collected packages: uv
[fastapi] Successfully installed uv-0.12.14
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
[fastapi] [0m[91mResolved 188 packages in 1.59s
[fastapi] [0m[91m   Building deepspeed==0.15.4
[fastapi] [0m[91m   Building antlr4-python3-runtime==4.9.3
[fastapi] [0m[91mDownloading hf-xet (4.3MiB)
[fastapi] [0m[91mDownloading pydantic-core (2.0MiB)
[fastapi] [0m[91mDownloading tensorboard (5.2MiB)
[fastapi] [0m[91mDownloading pyphen (2.0MiB)
[fastapi] [0m[91mDownloading matplotlib (9.4MiB)
[fastapi] [0m[91mDownloading scikit-learn (8.9MiB)
[fastapi] [0m[91mDownloading pandas (12.5MiB)
[fastapi] [0m[91mDownloading sqlalchemy (3.3MiB)
[fastapi] [0m[91mDownloading wandb (20.4MiB)
[fastapi] [0m[91mDownloading scipy (35.9MiB)
[fastapi] [0m[91mDownloading mpi4py (1.3MiB)
[fastapi] [0m[91mDownloading sentencepiece (1.2MiB)
[fastapi] [0m[91mDownloading mlflow (11.0MiB)
[fastapi] [0m[91mDownloading[0m[91m kiwisolver (1.4MiB)
[fastapi] [0m[91mDownloading mlflow-skinny (3.5MiB)
[fastapi] [0m[91mDownloading openai (1.9MiB)
[fastapi] [0m[91mDownloading plotly (8.6MiB)
[fastapi] [0m[91mDownloading fonttools (5.2MiB)
[fastapi] [0m[91mDownloading mlflow-tracing (1.7MiB)
[fastapi] [0m[91mDownloading dash (8.5MiB)
[fastapi] [0m[91mDownloading pycryptodome (2.2MiB)
[fastapi] [0m[91m Downloaded sentencepiece
[fastapi] [0m[91m Downloaded mpi4py
[fastapi] [0m[91m Downloaded kiwisolver
[fastapi] Downloaded mlflow-tracing
[fastapi] [0m[91m Downloaded pyphen
[fastapi] [0m[91m Downloaded pydantic-core
[fastapi] [0m[91m Downloaded pycryptodome
[fastapi] [0m[91m Downloaded openai
[fastapi] [0m[91m Downloaded sqlalchemy
[fastapi] [0m[91m Downloaded mlflow-skinny
[fastapi] [0m[91m Downloaded hf-xet
[fastapi] [0m[91m      Built antlr4-python3-runtime==4.9.3
[fastapi] [0m[91m Downloaded tensorboard
[fastapi] [0m[91m Downloaded fonttools
[fastapi] [0m[91m Downloaded scikit-learn
[fastapi] Downloaded plotly
[fastapi] [0m[91m Downloaded dash
[fastapi] [0m[91m Downloaded matplotlib
[fastapi] [0m[91m Downloaded pandas
[fastapi] [0m[91m Downloaded mlflow
[fastapi] [0m[91m Downloaded wandb
[fastapi] [0m[91m Downloaded scipy
[fastapi] [0m[91m      Built deepspeed==0.15.4
[fastapi] [0m[91mPrepared 89 packages in 853ms
[fastapi] [0m[91mUninstalled 6 packages in 109ms
[fastapi] [0m[91mInstalled 142 packages in 3.17s
[fastapi] [0m[91m + absl-py==2.5.0
[fastapi] + accelerate==1.6.0
[fastapi] + aiohappyeyeballs==2.7.1
[fastapi] [0m[91m+ aiohttp==3.14.3
[fastapi] + aiosignal==1.4[0m[91m.0
[fastapi] + alembic==[0m[91m1.20.0
[fastapi] +[0m[91m annotated-doc==0.0.[0m[91m5
[fastapi] + annotated-types==0.8.0
[fastapi] + antlr4-python3-runtime==[0m[91m4.9.3
[fastapi] [0m[91m - anyio==4.6.0
[fastapi] + anyio==4.15.1[0m[91m
[fastapi] + astor==0.8[0m[91m.1
[fastapi] + [0m[91mbitsandbytes==0.45.4
[fastapi] [0m[91m + blinker[0m[91m==1[0m[91m.9.0[0m[91m
[fastapi] +[0m[91m cachetools[0m[91m==7.1[0m[91m.8
[fastapi] [0m[91m - [0m[91mcffi[0m[91m==1.17.[0m[91m1
[fastapi] + cffi==2.1.1[0m[91m
[fastapi] + click==8.5.0
[fastapi] + cloudpickle==3.1.[0m[91m2
[fastapi] + cmudict==1[0m[91m.1.3
[fastapi] +[0m[91m contourpy==[0m[91m1[0m[91m.3[0m[91m.3
[fastapi] +[0m[91m cryptography[0m[91m==[0m[91m50.0.1
[fastapi] [0m[91m+ cycler[0m[91m==[0m[91m0.12.1[0m[91m
[fastapi] +[0m[91m [0m[91mdash==4[0m[91m.4.[0m[91m1
[fastapi] [0m[91m+ [0m[91mdatabricks-sdk[0m[91m==0.139.[0m[91m0
[fastapi] [0m[91m [0m[91m+ [0m[91mdatasets==3[0m[91m.5.[0m[91m0[0m[91m
[fastapi] +[0m[91m datasketch[0m[91m==2.[0m[91m0.[0m[91m0
[fastapi] [0m[91m+ deepspeed[0m[91m==0.[0m[91m15.4[0m[91m
[fastapi] [0m[91m+ [0m[91mdetoxify[0m[91m==0.[0m[91m5.2[0m[91m
[fastapi] [0m[91m + [0m[91mdill==[0m[91m0.3[0m[91m.8
[fastapi] [0m[91m+ [0m[91mdocker==[0m[91m7.2[0m[91m.0[0m[91m
[fastapi] [0m[91m+[0m[91m docker-pycreds[0m[91m==0.4.0
[fastapi] + einops==0.[0m[91m8.1
[fastapi] + fastapi==0.141.1
[fastapi] [0m[91m+ flask[0m[91m==3.1[0m[91m.3
[fastapi] + flask-cors[0m[91m==6.0.5
[fastapi] + fonttools[0m[91m==4.65.0
[fastapi] [0m[91m+ frozenlist[0m[91m==[0m[91m1.8.[0m[91m0
[fastapi] [0m[91m+ [0m[91mgdown==[0m[91m6.[0m[91m2.0[0m[91m
[fastapi] [0m[91m+ [0m[91mgitdb[0m[91m==4.[0m[91m0.12[0m[91m
[fastapi] [0m[91m+[0m[91m gitpython==[0m[91m3.1[0m[91m.62[0m[91m
[fastapi] [0m[91m+ google-auth[0m[91m==2.58.0
[fastapi] + graphene==3.[0m[91m4.3
[fastapi] + graphql-core==3.[0m[91m2.12
[fastapi] [0m[91m+ graphql-relay[0m[91m==3.2[0m[91m.0[0m[91m
[fastapi] + greenlet==3.5.6
[fastapi] +[0m[91m grpcio==1.84.0
[fastapi] [0m[91m+ gunicorn==26.2[0m[91m.0
[fastapi] - h11==0.14.0[0m[91m
[fastapi] + h11==0.[0m[91m16.0
[fastapi] [0m[91m+ hf-xet==[0m[91m1.6.0
[fastapi] [0m[91m+ hjson==3.1.0
[fastapi] + httpcore2==2[0m[91m.13.0
[fastapi] + httpx2==2.13.0
[fastapi] + huey==3.[0m[91m4.0
[fastapi] +[0m[91m huggingface-hub==0.36[0m[91m.2
[fastapi] [0m[91m- idna==3[0m[91m.10
[fastapi] + [0m[91midna==3.19
[fastapi] + importlib-metadata==[0m[91m9.0.1
[fastapi] [0m[91m + importlib-resources[0m[91m==7.1.[0m[91m0
[fastapi] + itsdangerous==2.2.0[0m[91m
[fastapi] + jaconv==[0m[91m0.5.0
[fastapi] [0m[91m + janus==[0m[91m2.0.0
[fastapi] + [0m[91mjiter==0.17[0m[91m.0[0m[91m
[fastapi] +[0m[91m joblib[0m[91m==1.[0m[91m6.0[0m[91m
[fastapi] + kiwisolver==1.5.1
[fastapi] [0m[91m + langcheck==0.9.0[0m[91m
[fastapi] [0m[91m+ liger-kernel[0m[91m==0.[0m[91m5.9
[fastapi] + mako==1.[0m[91m4.1
[fastapi] [0m[91m + markdown==3.10[0m[91m.3
[fastapi] [0m[91m+ matplotlib[0m[91m==3.[0m[91m11.[0m[91m2[0m[91m
[fastapi] + [0m[91mminio==7.2.20
[fastapi] +[0m[91m mlflow[0m[91m==3.16[0m[91m.0
[fastapi] [0m[91m +[0m[91m mlflow-skinny==3.16.0
[fastapi] + mlflow-tracing[0m[91m==3.16.0
[fastapi] + mpi4py[0m[91m==4.1.[0m[91m2
[fastapi] [0m[91m+ msgpack==1.2.2
[fastapi] + multidict==6[0m[91m.8.0
[fastapi] + multiprocess==[0m[91m0.70.[0m[91m16
[fastapi] +[0m[91m narwhals==2.26.0
[fastapi] +[0m[91m nlpaug==1.1[0m[91m.11
[fastapi] [0m[91m +[0m[91m nltk==3[0m[91m.10.3
[fastapi] + omegaconf==2.[0m[91m3.1
[fastapi] [0m[91m+ openai==3.14.0
[fastapi] +[0m[91m opentelemetry-api[0m[91m==1.[0m[91m44.0[0m[91m
[fastapi] [0m[91m+ [0m[91mopentelemetry-proto[0m[91m==1.44.[0m[91m0
[fastapi] [0m[91m + opentelemetry-sdk==1.44.0
[fastapi] [0m[91m+ opentelemetry-semantic-conventions==0.65b0[0m[91m
[fastapi] + [0m[91mpandas==2.2[0m[91m.3
[fastapi] + peft==0.15.1[0m[91m
[fastapi] + plotly==7.0.0
[fastapi] [0m[91m+ prettytable==3.18.0
[fastapi] + propcache==0.[0m[91m5.2
[fastapi] + protobuf==[0m[91m6.33.6
[fastapi] +[0m[91m py-cpuinfo==9.0.0
[fastapi] + [0m[91mpyarrow==25.0.[0m[91m1
[fastapi] +[0m[91m pyasn1==0.[0m[91m6.4
[fastapi] [0m[91m+ pyasn1-modules==[0m[91m0.4.2
[fastapi] [0m[91m + pycryptodome[0m[91m==3.23.[0m[91m0
[fastapi] +[0m[91m pydantic==2[0m[91m.13.5
[fastapi] + pydantic-core==2[0m[91m.46.5
[fastapi] +[0m[91m pyparsing==3[0m[91m.3.2[0m[91m
[fastapi] [0m[91m+ pyphen[0m[91m==0.18.[0m[91m1
[fastapi] + pysocks==1[0m[91m.7.1
[fastapi] + [0m[91mpython-dotenv==1.2[0m[91m.3
[fastapi] +[0m[91m pytz==2026[0m[91m.3.post1
[fastapi] + [0m[91mregex==2026.9[0m[91m.[0m[91m10
[fastapi] +[0m[91m restrictedpython[0m[91m==8.[0m[91m0
[fastapi] [0m[91m [0m[91m+ retrying[0m[91m==1.4.2
[fastapi] + rouge-score[0m[91m==0.1.2
[fastapi] +[0m[91m safetensors==0.8.[0m[91m0
[fastapi] +[0m[91m scikit-learn[0m[91m==1.[0m[91m9.1[0m[91m
[fastapi] + scipy==1.15.2
[fastapi] +[0m[91m sentence-transformers==5.7.0
[fastapi] +[0m[91m sentencepiece==0.[0m[91m2.0[0m[91m
[fastapi] + sentry-sdk==2[0m[91m.69.1
[fastapi] + setproctitle[0m[91m==1.3.7
[fastapi] [0m[91m + six==1[0m[91m.[0m[91m17.0[0m[91m
[fastapi] [0m[91m+ [0m[91mskops[0m[91m==0.14.[0m[91m0
[fastapi] + smmap==5.[0m[91m0.3
[fastapi] [0m[91m+ sqlalchemy[0m[91m==2.0[0m[91m.53
[fastapi] [0m[91m+ sqlparse[0m[91m==0.[0m[91m6.0
[fastapi] [0m[91m + starlette[0m[91m==1.6.0
[fastapi] + tabulate[0m[91m==0.10.0[0m[91m
[fastapi] + tenacity[0m[91m==9.1[0m[91m.4
[fastapi] [0m[91m [0m[91m+ tensorboard[0m[91m==2[0m[91m.19.[0m[91m0
[fastapi] [0m[91m+ [0m[91mtensorboard-data-server[0m[91m==0.7.[0m[91m2[0m[91m
[fastapi] +[0m[91m textstat[0m[91m==0.7.[0m[91m8
[fastapi] + [0m[91mthreadpoolctl==3.6.0
[fastapi] [0m[91m +[0m[91m [0m[91mtokenizers==0[0m[91m.21.4
[fastapi] [0m[91m [0m[91m+ toml==0[0m[91m.10.2
[fastapi] + tqdm==4.70.[0m[91m1
[fastapi] + transformers==4.51[0m[91m.3
[fastapi] + trl==0[0m[91m.18.0
[fastapi] + truststore==0.10[0m[91m.4
[fastapi] [0m[91m+ typer==0.9.0
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
[fastapi] + yarl==1.24.5
[fastapi] + zipp==4.1.0
[fastapi] [0mCollecting hf_transfer==0.1.9
[fastapi] Downloading hf_transfer-0.1.9-cp38-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (1.7 kB)
[fastapi] Downloading hf_transfer-0.1.9-cp38-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.6 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.6/3.6 MB 176.8 MB/s eta 0:00:00
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
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 100.2 MB/s eta 0:00:00
[fastapi] Installing collected packages: tiktoken
[fastapi] Successfully installed tiktoken-0.9.0
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0mCollecting flash-attn==v2.7.4.post1
[fastapi] Downloading flash_attn-2.7.4.post1.tar.gz (6.0 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.0/6.0 MB 170.1 MB/s eta 0:00:00
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
[fastapi] [0m[91mResolved 142 packages in 230ms
[fastapi] [0m[91mDownloading torchvision (6.9MiB)
[fastapi] [0m[91mDownloading vllm (280.4MiB)
[fastapi] [0m[91mDownloading numba (3.6MiB)
[fastapi] [0m[91mDownloading cupy-cuda12x (130.3MiB)
[fastapi] [0m[91mDownloading xgrammar (4.1MiB)
[fastapi] [0m[91mDownloading llguidance (14.3MiB)
[fastapi] [0m[91mDownloading llvmlite (40.4MiB)
[fastapi] [0m[91mDownloading torchaudio (3.2MiB)
[fastapi] [0m[91mDownloading uvloop (3.6MiB)
[fastapi] [0m[91mDownloading pycountry (7.7MiB)
[fastapi] [0m[91mDownloading numpy (15.6MiB)
[fastapi] [0m[91mDownloading opencv-python-headless (58.4MiB)
[fastapi] [0m[91mDownloading mistral-common (6.2MiB)
[fastapi] [0m[91mDownloading pillow (6.6MiB)
[fastapi] [0m[91mDownloading ray (74.7MiB)
[fastapi] [0m[91m Downloaded torchaudio
[fastapi] [0m[91m Downloaded numba
[fastapi] Downloaded uvloop
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
[fastapi] [0m[91mPrepared 45 packages in 2.63s
[fastapi] [0m[91mUninstalled 23 packages in 1.60s
[fastapi] [0m[91mInstalled 71 packages in 12.71s
[fastapi] [0m[91m + agent-detector==2.0.0
[fastapi] + airportsdata==20260905
[fastapi] + blake3==1.0.9
[fastapi] + compressed-tensors==0.9.2
[fastapi] + cuda-pathfinder==1[0m[91m.8.1
[fastapi] + cupy-cuda12x==14.2.0
[fastapi] + depyf==0.18.0
[fastapi] [0m[91m [0m[91m+ detect-installer==0.[0m[91m2.1
[fastapi] [0m[91m + [0m[91mdiskcache==5.6.3
[fastapi] + [0m[91mdnspython==2.8.0
[fastapi] + email-validator==2.3.0
[fastapi] + [0m[91mfastapi-cli==0.0.32
[fastapi] + fastapi-cloud-cli==0.[0m[91m26.0
[fastapi] + [0m[91mfastar==0[0m[91m.12.0
[fastapi] [0m[91m - filelock==3.13.1
[fastapi] + filelock==3.32.6
[fastapi] + [0m[91mgguf==0.10.0
[fastapi] - httpcore[0m[91m==1.0[0m[91m.5
[fastapi] [0m[91m+ [0m[91mhttpcore==1.0.9
[fastapi] + httptools==[0m[91m0.8.0
[fastapi] [0m[91m+ interegular[0m[91m==0[0m[91m.3[0m[91m.3
[fastapi] [0m[91m - [0m[91mjinja2[0m[91m==3.1.[0m[91m3
[fastapi] [0m[91m + [0m[91mjinja2[0m[91m==3.[0m[91m1.[0m[91m6
[fastapi] [0m[91m+ [0m[91mlark==[0m[91m1[0m[91m.2.2[0m[91m
[fastapi] [0m[91m +[0m[91m [0m[91mllguidance==0[0m[91m.7.[0m[91m30
[fastapi] + [0m[91mllvmlite==0.44.0
[fastapi] +[0m[91m lm-format-enforcer==0.10.12
[fastapi] [0m[91m + markdown-it-py==[0m[91m4.2.0
[fastapi] + mdurl==0.1.2[0m[91m
[fastapi] + mistral-common==1.11.7
[fastapi] [0m[91m + msgspec[0m[91m==0.21[0m[91m.1[0m[91m
[fastapi] +[0m[91m nanobind[0m[91m==[0m[91m3.0.1[0m[91m
[fastapi] + numba==[0m[91m0.61.0
[fastapi] [0m[91m - numpy==1[0m[91m.26.3
[fastapi] [0m[91m + numpy[0m[91m==2.1[0m[91m.3
[fastapi] -[0m[91m nvidia-cublas-cu12==[0m[91m12.4.2[0m[91m.65
[fastapi] [0m[91m+ nvidia-cublas-cu12==[0m[91m12.4.5.8[0m[91m
[fastapi] - [0m[91mnvidia-cuda-cupti-cu12==12.4[0m[91m.99
[fastapi] + nvidia-cuda-cupti-cu12==12.4[0m[91m.127
[fastapi] - nvidia-cuda-nvrtc-cu12[0m[91m==12.4.99
[fastapi] [0m[91m+ nvidia-cuda-nvrtc-cu12==12.[0m[91m4.127
[fastapi] - nvidia-cuda-runtime-cu12[0m[91m==12.4.[0m[91m99
[fastapi] + [0m[91mnvidia-cuda-runtime-cu12==12.[0m[91m4.127
[fastapi] [0m[91m - nvidia-cufft-cu12==11.2.0[0m[91m.44
[fastapi] [0m[91m + [0m[91mnvidia-cufft-cu12[0m[91m==11.2.1.3
[fastapi] - [0m[91mnvidia-curand-cu12==10.3.[0m[91m5.[0m[91m119
[fastapi] [0m[91m+ [0m[91mnvidia-curand-cu12[0m[91m==10.3[0m[91m.5.147
[fastapi] [0m[91m -[0m[91m [0m[91mnvidia-cusolver-cu12==11[0m[91m.6.0.[0m[91m99
[fastapi] + nvidia-cusolver-cu12==11.6.1.9
[fastapi] [0m[91m- nvidia-cusparse-cu12==12.3.0.142
[fastapi] + nvidia-cusparse-cu12==[0m[91m12.3.1.[0m[91m170[0m[91m
[fastapi] + nvidia-cusparselt-cu12[0m[91m==0[0m[91m.6.2
[fastapi] [0m[91m [0m[91m- nvidia-nccl-cu12[0m[91m==2.[0m[91m20[0m[91m.5
[fastapi] [0m[91m+ [0m[91mnvidia-nccl-cu12[0m[91m==2.21.5
[fastapi] - nvidia-nvjitlink-cu12==12.4.99[0m[91m
[fastapi] + nvidia-nvjitlink-cu12==12.4.127
[fastapi] - nvidia-nvtx-cu12==12.4[0m[91m.99
[fastapi] + nvidia-nvtx-cu12[0m[91m==12.4.127[0m[91m
[fastapi] +[0m[91m opencv-python-headless==[0m[91m5.[0m[91m0.0[0m[91m.93[0m[91m
[fastapi] + outlines==0.1.11
[fastapi] [0m[91m+ outlines-core==0.[0m[91m1.[0m[91m26
[fastapi] [0m[91m-[0m[91m packaging==[0m[91m23.2
[fastapi] + packaging==26.3
[fastapi] +[0m[91m partial-json-parser==0.2.1.[0m[91m1.post7[0m[91m
[fastapi] - [0m[91mpillow[0m[91m==10.2[0m[91m.0[0m[91m
[fastapi] [0m[91m+ [0m[91mpillow[0m[91m==12.3[0m[91m.0
[fastapi] [0m[91m+[0m[91m prometheus-fastapi-instrumentator==[0m[91m8.1.[0m[91m0[0m[91m
[fastapi] +[0m[91m pycountry==26[0m[91m.2[0m[91m.16
[fastapi] [0m[91m [0m[91m+ pydantic-extra-types[0m[91m==2[0m[91m.11.1[0m[91m
[fastapi] [0m[91m + [0m[91mpydantic-settings==2[0m[91m.15.[0m[91m0
[fastapi] [0m[91m+ python-multipart==0.0.32
[fastapi] + [0m[91mray==2.58.0
[fastapi] + [0m[91mrich==15.0.[0m[91m0
[fastapi] +[0m[91m rich-toolkit==[0m[91m0.20.5[0m[91m
[fastapi] + [0m[91mrignore==0.8.1
[fastapi] + shellingham[0m[91m==1.5.4
[fastapi] [0m[91m - sympy==[0m[91m1.12
[fastapi] [0m[91m+ sympy[0m[91m==1.13.1
[fastapi] - [0m[91mtorch[0m[91m==2.4.[0m[91m1+[0m[91mcu124
[fastapi] + torch==2.6.0
[fastapi] - torchaudio==2.4.1+cu124[0m[91m
[fastapi] + torchaudio==2.6.0
[fastapi] - torchvision==[0m[91m0.19.[0m[91m1+[0m[91mcu124
[fastapi] [0m[91m+ torchvision[0m[91m==0.21.[0m[91m0
[fastapi] - triton==[0m[91m3.0.0
[fastapi] [0m[91m+ triton==[0m[91m3.2.[0m[91m0
[fastapi] - [0m[91mtyper==0.[0m[91m9.0
[fastapi] + [0m[91mtyper==0.27.[0m[91m2
[fastapi] + uvloop==0[0m[91m.22.1
[fastapi] [0m[91m+ vllm==[0m[91m0.8.3
[fastapi] [0m[91m+ watchfiles==1.2.0
[fastapi] +[0m[91m websockets==17.1[0m[91m
[fastapi] + [0m[91mxformers==0.0[0m[91m.29.post2
[fastapi] [0m[91m+ xgrammar==0.1.17
[fastapi] [0mCollecting fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0
[fastapi] Cloning https://github.com/rayonlabs/fiber.git (to revision 2.4.0) to /tmp/pip-install-kcuh4cg8/fiber_1d4aeb70829945bb99b2d15424966f97
[fastapi] [91m  Running command git clone --filter=blob:none --quiet https://github.com/rayonlabs/fiber.git /tmp/pip-install-kcuh4cg8/fiber_1d4aeb70829945bb99b2d15424966f97
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
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 552.2/552.2 kB 55.5 MB/s eta 0:00:00
[fastapi] Downloading eth_typing-5.0.0-py3-none-any.whl (20 kB)
[fastapi] Downloading netaddr-1.3.0-py3-none-any.whl (2.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.3/2.3 MB 196.1 MB/s eta 0:00:00
[fastapi] Downloading python_dotenv-1.0.1-py3-none-any.whl (19 kB)
[fastapi] Downloading substrate_interface-1.7.10-py3-none-any.whl (60 kB)
[fastapi] Downloading tenacity-9.0.0-py3-none-any.whl (28 kB)
[fastapi] Downloading async_substrate_interface-1.6.4-py3-none-any.whl (97 kB)
[fastapi] Downloading bt_decode-0.8.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (647 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 647.8/647.8 kB 104.4 MB/s eta 0:00:00
[fastapi] Downloading colorama-0.4.6-py2.py3-none-any.whl (25 kB)
[fastapi] Downloading pydantic-2.9.2-py3-none-any.whl (434 kB)
[fastapi] Downloading pydantic_core-2.23.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 227.5 MB/s eta 0:00:00
[fastapi] Downloading aiosqlite-0.22.1-py3-none-any.whl (17 kB)
[fastapi] Downloading base58-2.1.1-py3-none-any.whl (5.6 kB)
[fastapi] Downloading ecdsa-0.19.2-py2.py3-none-any.whl (150 kB)
[fastapi] Downloading eth_keys-0.8.0-py3-none-any.whl (20 kB)
[fastapi] Downloading eth_utils-2.3.2-py3-none-any.whl (77 kB)
[fastapi] Downloading py_bip39_bindings-0.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (432 kB)
[fastapi] Downloading py_ed25519_zebra_bindings-1.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (323 kB)
[fastapi] Downloading py_sr25519_bindings-0.2.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (372 kB)
[fastapi] Downloading pynacl-1.6.2-cp38-abi3-manylinux_2_34_x86_64.whl (1.4 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.4/1.4 MB 184.5 MB/s eta 0:00:00
[fastapi] Downloading scalecodec-1.2.12-py3-none-any.whl (99 kB)
[fastapi] Downloading xxhash-3.8.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (220 kB)
[fastapi] Downloading cytoolz-1.1.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (2.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.8/2.8 MB 226.4 MB/s eta 0:00:00
[fastapi] Downloading eth_hash-0.8.0-py3-none-any.whl (8.0 kB)
[fastapi] Downloading toolz-1.1.0-py3-none-any.whl (58 kB)
[fastapi] Building wheels for collected packages: fiber
[fastapi] Building wheel for fiber (pyproject.toml): started
[fastapi] Building wheel for fiber (pyproject.toml): finished with status 'done'
[fastapi] Created wheel for fiber: filename=fiber-2.4.0-py3-none-any.whl size=51790 sha256=c50f803eff2fbcdf01560cfffdc65a3891a75b0b315d61d842fd3861f51b5d73
[fastapi] Stored in directory: /tmp/pip-ephem-wheel-cache-g8q693t0/wheels/d1/5e/21/2fa1f403cd187996037f04f6328bf11973ce31440a275f6949
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
[fastapi] [0m ---> 2ddc20805943
[fastapi] Step 13/14 : RUN python -m venv --system-site-packages /workspace/v5_py &&     bash -c "source /workspace/v5_py/bin/activate &&     pip install -U pip &&     pip install --no-cache-dir 'transformers==5.12.1' 'tokenizers>=0.22,<0.24' 'peft==0.19.1' 'bitsandbytes==0.50.1' &&     (pip install --no-cache-dir 'trl>=0.24' || true) &&     pip uninstall -y nvidia-cublas-cu12 nvidia-cuda-cupti-cu12 nvidia-cuda-nvrtc-cu12 nvidia-cuda-runtime-cu12 nvidia-cudnn-cu12 nvidia-cufft-cu12 nvidia-curand-cu12 nvidia-cusolver-cu12 nvidia-cusparse-cu12 &&     python -c 'import torch,transformers,peft,accelerate,bitsandbytes; assert torch.cuda.is_available() or True; print(\"v5 venv:\", transformers.__version__, peft.__version__, accelerate.__version__, torch.__version__, bitsandbytes.__version__)' &&     deactivate"
[fastapi] ---> Running in 69fdc2811a06
[fastapi] Requirement already satisfied: pip in /workspace/v5_py/lib/python3.11/site-packages (24.0)
[fastapi] Collecting pip
[fastapi] Downloading pip-26.2.1-py3-none-any.whl.metadata (4.6 kB)
[fastapi] Downloading pip-26.2.1-py3-none-any.whl (1.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 32.5 MB/s eta 0:00:00
[fastapi] Installing collected packages: pip
[fastapi] Attempting uninstall: pip
[fastapi] Found existing installation: pip 24.0
[fastapi] Uninstalling pip-24.0:
[fastapi] Successfully uninstalled pip-24.0
[fastapi] Successfully installed pip-26.2.1
[fastapi] Collecting transformers==5.12.1
[fastapi] Downloading transformers-5.12.1-py3-none-any.whl.metadata (33 kB)
[fastapi] Collecting tokenizers<0.24,>=0.22
[fastapi] Downloading tokenizers-0.23.2-cp310-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (9.8 kB)
[fastapi] Collecting peft==0.19.1
[fastapi] Downloading peft-0.19.1-py3-none-any.whl.metadata (15 kB)
[fastapi] Collecting bitsandbytes==0.50.1
[fastapi] Downloading bitsandbytes-0.50.1-py3-none-manylinux_2_24_x86_64.whl.metadata (10 kB)
[fastapi] Collecting huggingface-hub<2.0,>=1.5.0 (from transformers==5.12.1)
[fastapi] Downloading huggingface_hub-1.31.0-py3-none-any.whl.metadata (16 kB)
[fastapi] Requirement already satisfied: numpy>=1.17 in /usr/local/lib/python3.11/dist-packages (from transformers==5.12.1) (2.1.3)
[fastapi] Requirement already satisfied: packaging>=20.0 in /usr/local/lib/python3.11/dist-packages (from transformers==5.12.1) (26.3)
[fastapi] Requirement already satisfied: pyyaml>=5.1 in /usr/local/lib/python3.11/dist-packages (from transformers==5.12.1) (6.0.2)
[fastapi] Requirement already satisfied: regex>=2025.10.22 in /usr/local/lib/python3.11/dist-packages (from transformers==5.12.1) (2026.9.10)
[fastapi] Collecting tokenizers<0.24,>=0.22
[fastapi] Downloading tokenizers-0.22.2-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (7.3 kB)
[fastapi] Requirement already satisfied: typer in /usr/local/lib/python3.11/dist-packages (from transformers==5.12.1) (0.27.2)
[fastapi] Requirement already satisfied: safetensors>=0.4.3 in /usr/local/lib/python3.11/dist-packages (from transformers==5.12.1) (0.8.0)
[fastapi] Requirement already satisfied: tqdm>=4.60 in /usr/local/lib/python3.11/dist-packages (from transformers==5.12.1) (4.70.1)
[fastapi] Requirement already satisfied: psutil in /usr/local/lib/python3.11/dist-packages (from peft==0.19.1) (6.0.0)
[fastapi] Requirement already satisfied: torch>=1.13.0 in /usr/local/lib/python3.11/dist-packages (from peft==0.19.1) (2.6.0)
[fastapi] Requirement already satisfied: accelerate>=0.21.0 in /usr/local/lib/python3.11/dist-packages (from peft==0.19.1) (1.6.0)
[fastapi] Requirement already satisfied: click<9.0.0,>=8.4.2 in /usr/local/lib/python3.11/dist-packages (from huggingface-hub<2.0,>=1.5.0->transformers==5.12.1) (8.5.0)
[fastapi] Requirement already satisfied: filelock>=3.10.0 in /usr/local/lib/python3.11/dist-packages (from huggingface-hub<2.0,>=1.5.0->transformers==5.12.1) (3.32.6)
[fastapi] Requirement already satisfied: fsspec>=2023.5.0 in /usr/local/lib/python3.11/dist-packages (from huggingface-hub<2.0,>=1.5.0->transformers==5.12.1) (2024.2.0)
[fastapi] Requirement already satisfied: hf-xet<2.0.0,>=1.5.2 in /usr/local/lib/python3.11/dist-packages (from huggingface-hub<2.0,>=1.5.0->transformers==5.12.1) (1.6.0)
[fastapi] Requirement already satisfied: httpx<1,>=0.23.0 in /usr/local/lib/python3.11/dist-packages (from huggingface-hub<2.0,>=1.5.0->transformers==5.12.1) (0.27.2)
[fastapi] Requirement already satisfied: typing-extensions>=4.1.0 in /usr/local/lib/python3.11/dist-packages (from huggingface-hub<2.0,>=1.5.0->transformers==5.12.1) (4.16.0)
[fastapi] Requirement already satisfied: anyio in /usr/local/lib/python3.11/dist-packages (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers==5.12.1) (4.15.1)
[fastapi] Requirement already satisfied: certifi in /usr/local/lib/python3.11/dist-packages (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers==5.12.1) (2024.8.30)
[fastapi] Requirement already satisfied: httpcore==1.* in /usr/local/lib/python3.11/dist-packages (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers==5.12.1) (1.0.9)
[fastapi] Requirement already satisfied: idna in /usr/local/lib/python3.11/dist-packages (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers==5.12.1) (3.19)
[fastapi] Requirement already satisfied: sniffio in /usr/local/lib/python3.11/dist-packages (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers==5.12.1) (1.3.1)
[fastapi] Requirement already satisfied: h11>=0.16 in /usr/local/lib/python3.11/dist-packages (from httpcore==1.*->httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers==5.12.1) (0.16.0)
[fastapi] Requirement already satisfied: networkx in /usr/local/lib/python3.11/dist-packages (from torch>=1.13.0->peft==0.19.1) (3.2.1)
[fastapi] Requirement already satisfied: jinja2 in /usr/local/lib/python3.11/dist-packages (from torch>=1.13.0->peft==0.19.1) (3.1.6)
[fastapi] Requirement already satisfied: nvidia-cuda-nvrtc-cu12==12.4.127 in /usr/local/lib/python3.11/dist-packages (from torch>=1.13.0->peft==0.19.1) (12.4.127)
[fastapi] Requirement already satisfied: nvidia-cuda-runtime-cu12==12.4.127 in /usr/local/lib/python3.11/dist-packages (from torch>=1.13.0->peft==0.19.1) (12.4.127)
[fastapi] Requirement already satisfied: nvidia-cuda-cupti-cu12==12.4.127 in /usr/local/lib/python3.11/dist-packages (from torch>=1.13.0->peft==0.19.1) (12.4.127)
[fastapi] Requirement already satisfied: nvidia-cudnn-cu12==9.1.0.70 in /usr/local/lib/python3.11/dist-packages (from torch>=1.13.0->peft==0.19.1) (9.1.0.70)
[fastapi] Requirement already satisfied: nvidia-cublas-cu12==12.4.5.8 in /usr/local/lib/python3.11/dist-packages (from torch>=1.13.0->peft==0.19.1) (12.4.5.8)
[fastapi] Requirement already satisfied: nvidia-cufft-cu12==11.2.1.3 in /usr/local/lib/python3.11/dist-packages (from torch>=1.13.0->peft==0.19.1) (11.2.1.3)
[fastapi] Requirement already satisfied: nvidia-curand-cu12==10.3.5.147 in /usr/local/lib/python3.11/dist-packages (from torch>=1.13.0->peft==0.19.1) (10.3.5.147)
[fastapi] Requirement already satisfied: nvidia-cusolver-cu12==11.6.1.9 in /usr/local/lib/python3.11/dist-packages (from torch>=1.13.0->peft==0.19.1) (11.6.1.9)
[fastapi] Requirement already satisfied: nvidia-cusparse-cu12==12.3.1.170 in /usr/local/lib/python3.11/dist-packages (from torch>=1.13.0->peft==0.19.1) (12.3.1.170)
[fastapi] Requirement already satisfied: nvidia-cusparselt-cu12==0.6.2 in /usr/local/lib/python3.11/dist-packages (from torch>=1.13.0->peft==0.19.1) (0.6.2)
[fastapi] Requirement already satisfied: nvidia-nccl-cu12==2.21.5 in /usr/local/lib/python3.11/dist-packages (from torch>=1.13.0->peft==0.19.1) (2.21.5)
[fastapi] Requirement already satisfied: nvidia-nvtx-cu12==12.4.127 in /usr/local/lib/python3.11/dist-packages (from torch>=1.13.0->peft==0.19.1) (12.4.127)
[fastapi] Requirement already satisfied: nvidia-nvjitlink-cu12==12.4.127 in /usr/local/lib/python3.11/dist-packages (from torch>=1.13.0->peft==0.19.1) (12.4.127)
[fastapi] Requirement already satisfied: triton==3.2.0 in /usr/local/lib/python3.11/dist-packages (from torch>=1.13.0->peft==0.19.1) (3.2.0)
[fastapi] Requirement already satisfied: sympy==1.13.1 in /usr/local/lib/python3.11/dist-packages (from torch>=1.13.0->peft==0.19.1) (1.13.1)
[fastapi] Requirement already satisfied: mpmath<1.4,>=1.1.0 in /usr/local/lib/python3.11/dist-packages (from sympy==1.13.1->torch>=1.13.0->peft==0.19.1) (1.3.0)
[fastapi] Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.11/dist-packages (from jinja2->torch>=1.13.0->peft==0.19.1) (2.1.5)
[fastapi] Requirement already satisfied: shellingham>=1.3.0 in /usr/local/lib/python3.11/dist-packages (from typer->transformers==5.12.1) (1.5.4)
[fastapi] Requirement already satisfied: rich>=13.8.0 in /usr/local/lib/python3.11/dist-packages (from typer->transformers==5.12.1) (15.0.0)
[fastapi] Requirement already satisfied: annotated-doc>=0.0.2 in /usr/local/lib/python3.11/dist-packages (from typer->transformers==5.12.1) (0.0.5)
[fastapi] Requirement already satisfied: markdown-it-py>=2.2.0 in /usr/local/lib/python3.11/dist-packages (from rich>=13.8.0->typer->transformers==5.12.1) (4.2.0)
[fastapi] Requirement already satisfied: pygments<3.0.0,>=2.13.0 in /usr/local/lib/python3.11/dist-packages (from rich>=13.8.0->typer->transformers==5.12.1) (2.18.0)
[fastapi] Requirement already satisfied: mdurl~=0.1 in /usr/local/lib/python3.11/dist-packages (from markdown-it-py>=2.2.0->rich>=13.8.0->typer->transformers==5.12.1) (0.1.2)
[fastapi] Downloading transformers-5.12.1-py3-none-any.whl (11.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 11.2/11.2 MB 183.3 MB/s  0:00:00
[fastapi] Downloading peft-0.19.1-py3-none-any.whl (680 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 680.7/680.7 kB 562.3 MB/s  0:00:00
[fastapi] Downloading bitsandbytes-0.50.1-py3-none-manylinux_2_24_x86_64.whl (41.0 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 41.0/41.0 MB 228.9 MB/s  0:00:00
[fastapi] Downloading tokenizers-0.22.2-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.3/3.3 MB 330.8 MB/s  0:00:00
[fastapi] Downloading huggingface_hub-1.31.0-py3-none-any.whl (798 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 798.3/798.3 kB 692.2 MB/s  0:00:00
[fastapi] Installing collected packages: huggingface-hub, tokenizers, bitsandbytes, transformers, peft
[fastapi] Attempting uninstall: huggingface-hub
[fastapi] Found existing installation: huggingface_hub 0.36.2
[fastapi] Not uninstalling huggingface-hub at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'huggingface_hub'. No files were found to uninstall.
[fastapi] Attempting uninstall: tokenizers
[fastapi] Found existing installation: tokenizers 0.21.4
[fastapi] Not uninstalling tokenizers at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'tokenizers'. No files were found to uninstall.
[fastapi] Attempting uninstall: bitsandbytes
[fastapi] Found existing installation: bitsandbytes 0.45.4
[fastapi] Not uninstalling bitsandbytes at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'bitsandbytes'. No files were found to uninstall.
[fastapi] Attempting uninstall: transformers
[fastapi] Found existing installation: transformers 4.51.3
[fastapi] Not uninstalling transformers at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'transformers'. No files were found to uninstall.
[fastapi] Attempting uninstall: peft
[fastapi] Found existing installation: peft 0.15.1
[fastapi] Not uninstalling peft at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'peft'. No files were found to uninstall.
[fastapi] Successfully installed bitsandbytes-0.50.1 huggingface-hub-1.31.0 peft-0.19.1 tokenizers-0.22.2 transformers-5.12.1
[fastapi] Collecting trl>=0.24
[fastapi] Downloading trl-1.13.0-py3-none-any.whl.metadata (12 kB)
[fastapi] Requirement already satisfied: accelerate>=1.4.0 in /usr/local/lib/python3.11/dist-packages (from trl>=0.24) (1.6.0)
[fastapi] Collecting datasets>=4.7.0 (from trl>=0.24)
[fastapi] Downloading datasets-5.0.1-py3-none-any.whl.metadata (23 kB)
[fastapi] Requirement already satisfied: jinja2 in /usr/local/lib/python3.11/dist-packages (from trl>=0.24) (3.1.6)
[fastapi] Requirement already satisfied: packaging>20.0 in /usr/local/lib/python3.11/dist-packages (from trl>=0.24) (26.3)
[fastapi] Requirement already satisfied: transformers>=4.56.2 in /workspace/v5_py/lib/python3.11/site-packages (from trl>=0.24) (5.12.1)
[fastapi] Requirement already satisfied: numpy<3.0.0,>=1.17 in /usr/local/lib/python3.11/dist-packages (from accelerate>=1.4.0->trl>=0.24) (2.1.3)
[fastapi] Requirement already satisfied: psutil in /usr/local/lib/python3.11/dist-packages (from accelerate>=1.4.0->trl>=0.24) (6.0.0)
[fastapi] Requirement already satisfied: pyyaml in /usr/local/lib/python3.11/dist-packages (from accelerate>=1.4.0->trl>=0.24) (6.0.2)
[fastapi] Requirement already satisfied: torch>=2.0.0 in /usr/local/lib/python3.11/dist-packages (from accelerate>=1.4.0->trl>=0.24) (2.6.0)
[fastapi] Requirement already satisfied: huggingface-hub>=0.21.0 in /workspace/v5_py/lib/python3.11/site-packages (from accelerate>=1.4.0->trl>=0.24) (1.31.0)
[fastapi] Requirement already satisfied: safetensors>=0.4.3 in /usr/local/lib/python3.11/dist-packages (from accelerate>=1.4.0->trl>=0.24) (0.8.0)
[fastapi] Requirement already satisfied: filelock in /usr/local/lib/python3.11/dist-packages (from datasets>=4.7.0->trl>=0.24) (3.32.6)
[fastapi] Requirement already satisfied: pyarrow>=21.0.0 in /usr/local/lib/python3.11/dist-packages (from datasets>=4.7.0->trl>=0.24) (25.0.1)
[fastapi] Requirement already satisfied: dill<0.4.2,>=0.3.0 in /usr/local/lib/python3.11/dist-packages (from datasets>=4.7.0->trl>=0.24) (0.3.8)
[fastapi] Requirement already satisfied: pandas in /usr/local/lib/python3.11/dist-packages (from datasets>=4.7.0->trl>=0.24) (2.2.3)
[fastapi] Requirement already satisfied: requests>=2.32.2 in /usr/local/lib/python3.11/dist-packages (from datasets>=4.7.0->trl>=0.24) (2.32.3)
[fastapi] Requirement already satisfied: httpx<1.0.0 in /usr/local/lib/python3.11/dist-packages (from datasets>=4.7.0->trl>=0.24) (0.27.2)
[fastapi] Requirement already satisfied: tqdm>=4.66.3 in /usr/local/lib/python3.11/dist-packages (from datasets>=4.7.0->trl>=0.24) (4.70.1)
[fastapi] Requirement already satisfied: xxhash in /usr/local/lib/python3.11/dist-packages (from datasets>=4.7.0->trl>=0.24) (3.8.1)
[fastapi] Requirement already satisfied: multiprocess<0.70.20 in /usr/local/lib/python3.11/dist-packages (from datasets>=4.7.0->trl>=0.24) (0.70.16)
[fastapi] Requirement already satisfied: fsspec<=2026.6.0,>=2023.1.0 in /usr/local/lib/python3.11/dist-packages (from fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=4.7.0->trl>=0.24) (2024.2.0)
[fastapi] Requirement already satisfied: aiohttp!=4.0.0a0,!=4.0.0a1 in /usr/local/lib/python3.11/dist-packages (from fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=4.7.0->trl>=0.24) (3.14.3)
[fastapi] Requirement already satisfied: anyio in /usr/local/lib/python3.11/dist-packages (from httpx<1.0.0->datasets>=4.7.0->trl>=0.24) (4.15.1)
[fastapi] Requirement already satisfied: certifi in /usr/local/lib/python3.11/dist-packages (from httpx<1.0.0->datasets>=4.7.0->trl>=0.24) (2024.8.30)
[fastapi] Requirement already satisfied: httpcore==1.* in /usr/local/lib/python3.11/dist-packages (from httpx<1.0.0->datasets>=4.7.0->trl>=0.24) (1.0.9)
[fastapi] Requirement already satisfied: idna in /usr/local/lib/python3.11/dist-packages (from httpx<1.0.0->datasets>=4.7.0->trl>=0.24) (3.19)
[fastapi] Requirement already satisfied: sniffio in /usr/local/lib/python3.11/dist-packages (from httpx<1.0.0->datasets>=4.7.0->trl>=0.24) (1.3.1)
[fastapi] Requirement already satisfied: h11>=0.16 in /usr/local/lib/python3.11/dist-packages (from httpcore==1.*->httpx<1.0.0->datasets>=4.7.0->trl>=0.24) (0.16.0)
[fastapi] Requirement already satisfied: click<9.0.0,>=8.4.2 in /usr/local/lib/python3.11/dist-packages (from huggingface-hub>=0.21.0->accelerate>=1.4.0->trl>=0.24) (8.5.0)
[fastapi] Requirement already satisfied: hf-xet<2.0.0,>=1.5.2 in /usr/local/lib/python3.11/dist-packages (from huggingface-hub>=0.21.0->accelerate>=1.4.0->trl>=0.24) (1.6.0)
[fastapi] Requirement already satisfied: typing-extensions>=4.1.0 in /usr/local/lib/python3.11/dist-packages (from huggingface-hub>=0.21.0->accelerate>=1.4.0->trl>=0.24) (4.16.0)
[fastapi] Requirement already satisfied: aiohappyeyeballs>=2.5.0 in /usr/local/lib/python3.11/dist-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=4.7.0->trl>=0.24) (2.7.1)
[fastapi] Requirement already satisfied: aiosignal>=1.4.0 in /usr/local/lib/python3.11/dist-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=4.7.0->trl>=0.24) (1.4.0)
[fastapi] Requirement already satisfied: attrs>=17.3.0 in /usr/local/lib/python3.11/dist-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=4.7.0->trl>=0.24) (24.2.0)
[fastapi] Requirement already satisfied: frozenlist>=1.1.1 in /usr/local/lib/python3.11/dist-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=4.7.0->trl>=0.24) (1.8.0)
[fastapi] Requirement already satisfied: multidict<7.0,>=4.5 in /usr/local/lib/python3.11/dist-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=4.7.0->trl>=0.24) (6.8.0)
[fastapi] Requirement already satisfied: propcache>=0.2.0 in /usr/local/lib/python3.11/dist-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=4.7.0->trl>=0.24) (0.5.2)
[fastapi] Requirement already satisfied: yarl<2.0,>=1.17.0 in /usr/local/lib/python3.11/dist-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=4.7.0->trl>=0.24) (1.24.5)
[fastapi] Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.11/dist-packages (from requests>=2.32.2->datasets>=4.7.0->trl>=0.24) (3.3.2)
[fastapi] Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.11/dist-packages (from requests>=2.32.2->datasets>=4.7.0->trl>=0.24) (2.2.3)
[fastapi] Requirement already satisfied: networkx in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl>=0.24) (3.2.1)
[fastapi] Requirement already satisfied: nvidia-cuda-nvrtc-cu12==12.4.127 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl>=0.24) (12.4.127)
[fastapi] Requirement already satisfied: nvidia-cuda-runtime-cu12==12.4.127 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl>=0.24) (12.4.127)
[fastapi] Requirement already satisfied: nvidia-cuda-cupti-cu12==12.4.127 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl>=0.24) (12.4.127)
[fastapi] Requirement already satisfied: nvidia-cudnn-cu12==9.1.0.70 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl>=0.24) (9.1.0.70)
[fastapi] Requirement already satisfied: nvidia-cublas-cu12==12.4.5.8 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl>=0.24) (12.4.5.8)
[fastapi] Requirement already satisfied: nvidia-cufft-cu12==11.2.1.3 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl>=0.24) (11.2.1.3)
[fastapi] Requirement already satisfied: nvidia-curand-cu12==10.3.5.147 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl>=0.24) (10.3.5.147)
[fastapi] Requirement already satisfied: nvidia-cusolver-cu12==11.6.1.9 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl>=0.24) (11.6.1.9)
[fastapi] Requirement already satisfied: nvidia-cusparse-cu12==12.3.1.170 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl>=0.24) (12.3.1.170)
[fastapi] Requirement already satisfied: nvidia-cusparselt-cu12==0.6.2 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl>=0.24) (0.6.2)
[fastapi] Requirement already satisfied: nvidia-nccl-cu12==2.21.5 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl>=0.24) (2.21.5)
[fastapi] Requirement already satisfied: nvidia-nvtx-cu12==12.4.127 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl>=0.24) (12.4.127)
[fastapi] Requirement already satisfied: nvidia-nvjitlink-cu12==12.4.127 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl>=0.24) (12.4.127)
[fastapi] Requirement already satisfied: triton==3.2.0 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl>=0.24) (3.2.0)
[fastapi] Requirement already satisfied: sympy==1.13.1 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl>=0.24) (1.13.1)
[fastapi] Requirement already satisfied: mpmath<1.4,>=1.1.0 in /usr/local/lib/python3.11/dist-packages (from sympy==1.13.1->torch>=2.0.0->accelerate>=1.4.0->trl>=0.24) (1.3.0)
[fastapi] Requirement already satisfied: regex>=2025.10.22 in /usr/local/lib/python3.11/dist-packages (from transformers>=4.56.2->trl>=0.24) (2026.9.10)
[fastapi] Requirement already satisfied: tokenizers<=0.23.0,>=0.22.0 in /workspace/v5_py/lib/python3.11/site-packages (from transformers>=4.56.2->trl>=0.24) (0.22.2)
[fastapi] Requirement already satisfied: typer in /usr/local/lib/python3.11/dist-packages (from transformers>=4.56.2->trl>=0.24) (0.27.2)
[fastapi] Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.11/dist-packages (from jinja2->trl>=0.24) (2.1.5)
[fastapi] Requirement already satisfied: python-dateutil>=2.8.2 in /usr/local/lib/python3.11/dist-packages (from pandas->datasets>=4.7.0->trl>=0.24) (2.9.0.post0)
[fastapi] Requirement already satisfied: pytz>=2020.1 in /usr/local/lib/python3.11/dist-packages (from pandas->datasets>=4.7.0->trl>=0.24) (2026.3.post1)
[fastapi] Requirement already satisfied: tzdata>=2022.7 in /usr/local/lib/python3.11/dist-packages (from pandas->datasets>=4.7.0->trl>=0.24) (2026.4)
[fastapi] Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.11/dist-packages (from python-dateutil>=2.8.2->pandas->datasets>=4.7.0->trl>=0.24) (1.17.0)
[fastapi] Requirement already satisfied: shellingham>=1.3.0 in /usr/local/lib/python3.11/dist-packages (from typer->transformers>=4.56.2->trl>=0.24) (1.5.4)
[fastapi] Requirement already satisfied: rich>=13.8.0 in /usr/local/lib/python3.11/dist-packages (from typer->transformers>=4.56.2->trl>=0.24) (15.0.0)
[fastapi] Requirement already satisfied: annotated-doc>=0.0.2 in /usr/local/lib/python3.11/dist-packages (from typer->transformers>=4.56.2->trl>=0.24) (0.0.5)
[fastapi] Requirement already satisfied: markdown-it-py>=2.2.0 in /usr/local/lib/python3.11/dist-packages (from rich>=13.8.0->typer->transformers>=4.56.2->trl>=0.24) (4.2.0)
[fastapi] Requirement already satisfied: pygments<3.0.0,>=2.13.0 in /usr/local/lib/python3.11/dist-packages (from rich>=13.8.0->typer->transformers>=4.56.2->trl>=0.24) (2.18.0)
[fastapi] Requirement already satisfied: mdurl~=0.1 in /usr/local/lib/python3.11/dist-packages (from markdown-it-py>=2.2.0->rich>=13.8.0->typer->transformers>=4.56.2->trl>=0.24) (0.1.2)
[fastapi] Downloading trl-1.13.0-py3-none-any.whl (1.0 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.0/1.0 MB 64.6 MB/s  0:00:00
[fastapi] Downloading datasets-5.0.1-py3-none-any.whl (559 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 559.1/559.1 kB 149.9 MB/s  0:00:00
[fastapi] Installing collected packages: datasets, trl
[fastapi] Attempting uninstall: datasets
[fastapi] Found existing installation: datasets 3.5.0
[fastapi] Not uninstalling datasets at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'datasets'. No files were found to uninstall.
[fastapi] Attempting uninstall: trl
[fastapi] Found existing installation: trl 0.18.0
[fastapi] Not uninstalling trl at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'trl'. No files were found to uninstall.
[fastapi] Successfully installed datasets-5.0.1 trl-1.13.0
[fastapi] Found existing installation: nvidia-cublas-cu12 12.4.5.8
[fastapi] Not uninstalling nvidia-cublas-cu12 at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'nvidia-cublas-cu12'. No files were found to uninstall.
[fastapi] Found existing installation: nvidia-cuda-cupti-cu12 12.4.127
[fastapi] Not uninstalling nvidia-cuda-cupti-cu12 at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'nvidia-cuda-cupti-cu12'. No files were found to uninstall.
[fastapi] Found existing installation: nvidia-cuda-nvrtc-cu12 12.4.127
[fastapi] Not uninstalling nvidia-cuda-nvrtc-cu12 at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'nvidia-cuda-nvrtc-cu12'. No files were found to uninstall.
[fastapi] Found existing installation: nvidia-cuda-runtime-cu12 12.4.127
[fastapi] Not uninstalling nvidia-cuda-runtime-cu12 at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'nvidia-cuda-runtime-cu12'. No files were found to uninstall.
[fastapi] Found existing installation: nvidia-cudnn-cu12 9.1.0.70
[fastapi] Not uninstalling nvidia-cudnn-cu12 at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'nvidia-cudnn-cu12'. No files were found to uninstall.
[fastapi] Found existing installation: nvidia-cufft-cu12 11.2.1.3
[fastapi] Not uninstalling nvidia-cufft-cu12 at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'nvidia-cufft-cu12'. No files were found to uninstall.
[fastapi] Found existing installation: nvidia-curand-cu12 10.3.5.147
[fastapi] Not uninstalling nvidia-curand-cu12 at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'nvidia-curand-cu12'. No files were found to uninstall.
[fastapi] Found existing installation: nvidia-cusolver-cu12 11.6.1.9
[fastapi] Not uninstalling nvidia-cusolver-cu12 at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'nvidia-cusolver-cu12'. No files were found to uninstall.
[fastapi] Found existing installation: nvidia-cusparse-cu12 12.3.1.170
[fastapi] Not uninstalling nvidia-cusparse-cu12 at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'nvidia-cusparse-cu12'. No files were found to uninstall.
[fastapi] [91mFailed to load CPU gemm_4bit_forward from kernels-community: No module named 'kernels'. Please make sure you already `pip install kernels` and the kernels >= 0.11.1
[fastapi] [0mv5 venv: 5.12.1 0.19.1 1.6.0 2.6.0+cu124 0.50.1
[fastapi] ---> afd5817d5fa4
[fastapi] Step 14/14 : ENTRYPOINT ["./entrypoint.sh"]
[fastapi] ---> Running in 163d54b5899d
[fastapi] ---> 70e063ffcdcb
[fastapi] {'aux': {'ID': 'sha256:70e063ffcdcbe162e3fd9d4a59d1c677ceaf70f190ea0cb200f0e2207777673f'}}Successfully built 70e063ffcdcb
[fastapi] Successfully tagged standalone-text-trainer:b87ca400-5f50-4b20-a8c8-708f4749c818
[fastapi] Docker image built successfully.
[fastapi] Container.wait() returned: {'StatusCode': 0}
[fastapi] Cleaning up
[fastapi] Cleaned up Docker resources.
[fastapi] Starting upload container hf-upload-3230fe6e8b9945ca82a6c4b2d24345ed for task 067761fe-b567-44d7-8863-4cd41cc12261...
[hf-upload-32]  adapter_config.json not found
[hf-upload-32] README.md not found
[hf-upload-32] Creating repo gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5E2fNjMW...
[hf-upload-32] Uploading contents of /app/checkpoints/067761fe-b567-44d7-8863-4cd41cc12261/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5E2fNjMW to gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5E2fNjMW
[hf-upload-32] Uploaded successfully to https://huggingface.co/gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5E2fNjMW
[hf-upload-32] Deleted local folder: /app/checkpoints/067761fe-b567-44d7-8863-4cd41cc12261/tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5E2fNjMW
[text-trainer] [CUDA Allocator] PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
[text-trainer] [CUDA Health] available=True device_count=1
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_hash" in MinerSubmission has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] /workspace/axo_py/lib/python3.11/site-packages/requests/__init__.py:113: RequestsDependencyWarning: urllib3 (2.7.0) or chardet (6.0.0.post1)/charset_normalizer (3.5.1) doesn't match a supported version!
[text-trainer]   warnings.warn(
[text-trainer] [sn56][pack] mode=dense
[text-trainer] [sn56][rope] theta mismatch
[text-trainer] [sn56][soup] paired-accept=OFF
[text-trainer] df: /root/.triton/autotune: No such file or directory
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] [sn56][eval] batched
[text-trainer] [sn56][search] done tier-S1
[text-trainer] [sn56][relogio] fit
[text-trainer] [sn56][relogio] horizon synced
[text-trainer] wandb: WARNING The `run_name` is currently set to the same value as `TrainingArguments.output_dir`. If this was not intended, please specify a different run name by setting the `TrainingArguments.run_name` parameter.
[text-trainer] wandb: Tracking run with wandb version 0.19.10
[text-trainer] wandb: W&B syncing is set to `offline` in this directory. Run `wandb online` or set WANDB_MODE=online to enable cloud syncing.
[text-trainer] [sn56][eval] cadence adjusted
[text-trainer] [sn56][stop] margin adjusted
[text-trainer] [sn56][clip] high
[text-trainer] [sn56][stop] overfit
[text-trainer] [sn56][soup] budget
[text-trainer] [sn56][soup] done
[text-trainer] [sn56][devfit] RUN n_dev=92
[text-trainer] [sn56][devfit][cooldown] applied
[text-trainer] [1;34mwandb[0m: 
[text-trainer] [1;34mwandb[0m: You can sync this run to the cloud by running:
[text-trainer] [1;34mwandb[0m: [1mwandb sync /app/checkpoints/wandb_logs/067761fe-b567-44d7-8863-4cd41cc12261_5E2fNjMWkC7NhjFsobwdDT1ym9R8ws7iDMnaZtE1RcnAsfZf/wandb/offline-run-20260915_111211-067761fe-b567-44d7-8863-4cd41cc12261_tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5E2fNjMW[0m
[text-trainer] [1;34mwandb[0m: Find logs at: [1;35m../../app/checkpoints/wandb_logs/067761fe-b567-44d7-8863-4cd41cc12261_5E2fNjMWkC7NhjFsobwdDT1ym9R8ws7iDMnaZtE1RcnAsfZf/wandb/offline-run-20260915_111211-067761fe-b567-44d7-8863-4cd41cc12261_tournament-tourn_5c64e784a087074a_20260914-12a8c324-8bae-4f43-b01f-14b0fa6dbf62-5E2fNjMW/logs[0m
[text-trainer] [sn56][config-identity] normalized: ['transformers_version->base']