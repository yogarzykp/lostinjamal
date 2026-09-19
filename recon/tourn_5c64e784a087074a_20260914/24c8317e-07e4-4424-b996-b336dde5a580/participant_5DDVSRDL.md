# Loki — task 24c8317e-07e4-4424-b996-b336dde5a580 — hotkey 5DDVSRDLbcd57ZHnzFNjHdvcffekjiRdRJeBfWUHeSkWFprv
fetched 2026-09-19T05:03:45+00:00  lines=1308  hit_page_cap=False  containers=['downloader-24c8317e-07e4-4424-b996-b336dde5a580-1c5461ae', 'fastapi', 'hf-upload-cf0c33a06c21414fa09db24a855e14aa', 'text-trainer-9166a57c900e4c72adbfd7b5d0f13301']

[downloader-2] Downloading datasets to: /cache/datasets
[downloader-2] Downloading models to: /cache/models
[downloader-2] Model already cached at /cache/models/45363f1dab78e110.
[downloader-2] Skipping download.
[downloader-2] Model path: /cache/models/45363f1dab78e110
[downloader-2] Dataset path: /cache/datasets
[fastapi] Repository cloned successfully
[fastapi] Running Cache Download Container
[fastapi] Starting downloader container: downloader-24c8317e-07e4-4424-b996-b336dde5a580-1c5461ae
[fastapi] Download completed successfully for task 24c8317e-07e4-4424-b996-b336dde5a580
[fastapi] Building Docker image 'standalone-text-trainer:39a07ca9-b67c-4949-b648-94572a09021e' (timeout=3600s)...
[fastapi] Step 1/13 : FROM runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04
[fastapi] ---> d451fe72f137
[fastapi] Step 2/13 : RUN apt-get update && apt-get install -y     vim zip tmux iotop nvtop bmon wget nano zsh htop     && rm -rf /var/lib/apt/lists/*
[fastapi] ---> Running in c7ba9797b30f
[fastapi] Get:1 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  InRelease [1578 B]
[fastapi] Get:2 http://archive.ubuntu.com/ubuntu jammy InRelease [270 kB]
[fastapi] Get:3 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  Packages [3009 kB]
[fastapi] Get:4 http://security.ubuntu.com/ubuntu jammy-security InRelease [129 kB]
[fastapi] Get:5 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy InRelease [18.1 kB]
[fastapi] Get:6 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [128 kB]
[fastapi] Get:7 http://archive.ubuntu.com/ubuntu jammy-backports InRelease [127 kB]
[fastapi] Get:8 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy/main amd64 Packages [44.3 kB]
[fastapi] Get:9 http://archive.ubuntu.com/ubuntu jammy/universe amd64 Packages [17.5 MB]
[fastapi] Get:10 http://security.ubuntu.com/ubuntu jammy-security/multiverse amd64 Packages [84.6 kB]
[fastapi] Get:11 http://security.ubuntu.com/ubuntu jammy-security/restricted amd64 Packages [7717 kB]
[fastapi] Get:12 http://security.ubuntu.com/ubuntu jammy-security/main amd64 Packages [4290 kB]
[fastapi] Get:13 http://security.ubuntu.com/ubuntu jammy-security/universe amd64 Packages [1317 kB]
[fastapi] Get:14 http://archive.ubuntu.com/ubuntu jammy/restricted amd64 Packages [164 kB]
[fastapi] Get:15 http://archive.ubuntu.com/ubuntu jammy/main amd64 Packages [1792 kB]
[fastapi] Get:16 http://archive.ubuntu.com/ubuntu jammy/multiverse amd64 Packages [266 kB]
[fastapi] Get:17 http://archive.ubuntu.com/ubuntu jammy-updates/restricted amd64 Packages [8007 kB]
[fastapi] Get:18 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 Packages [4624 kB]
[fastapi] Get:19 http://archive.ubuntu.com/ubuntu jammy-updates/multiverse amd64 Packages [93.2 kB]
[fastapi] Get:20 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 Packages [1620 kB]
[fastapi] Get:21 http://archive.ubuntu.com/ubuntu jammy-backports/main amd64 Packages [82.8 kB]
[fastapi] Get:22 http://archive.ubuntu.com/ubuntu jammy-backports/universe amd64 Packages [35.6 kB]
[fastapi] Fetched 51.3 MB in 19s (2657 kB/s)
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
[fastapi] [0mFetched 23.1 MB in 7s (3526 kB/s)
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
[fastapi] ---> 79c812199cab
[fastapi] Step 3/13 : RUN mkdir -p /workspace /cache /workspace/scripts/datasets /app/checkpoints
[fastapi] ---> Running in 30b0f6b37364
[fastapi] ---> f7a1f8065f04
[fastapi] Step 4/13 : WORKDIR /workspace/scripts
[fastapi] ---> Running in efecb952644e
[fastapi] ---> 38460ca06f29
[fastapi] Step 5/13 : COPY scripts/training_requirements.txt /workspace/scripts/training_requirements.txt
[fastapi] ---> 0ee208fcf6c2
[fastapi] Step 6/13 : COPY scripts/grpo_requirements.txt /workspace/scripts/grpo_requirements.txt
[fastapi] ---> 7d5137b83bbc
[fastapi] Step 7/13 : RUN pip install uv &&     pip install -U packaging==23.2 setuptools==75.8.0 wheel ninja &&     uv pip install -r /workspace/scripts/training_requirements.txt --system &&     pip install tenacity==9.1.2 tiktoken==0.9.0 &&     pip install https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu12torch2.8cxx11abiTRUE-cp311-cp311-linux_x86_64.whl &&     pip install "fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0"
[fastapi] ---> Running in 233717a4eac7
[fastapi] Collecting uv
[fastapi] Downloading uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] Downloading uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.1 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 20.1/20.1 MB 44.4 MB/s eta 0:00:00
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
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 28.1 MB/s eta 0:00:00
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
[fastapi] [0m[91mResolved 191 packages in 3.20s
[fastapi] [0m[91m   Building deepspeed==0.19.2
[fastapi] [0m[91m   Building antlr4-python3-runtime==4.9.3
[fastapi] [0m[91mDownloading pyphen (2.0MiB)
[fastapi] [0m[91mDownloading tensorboard (5.2MiB)
[fastapi] [0m[91mDownloading nvidia-cusparselt-cu12 (273.9MiB)
[fastapi] [0m[91mDownloading plotly (8.6MiB)
[fastapi] [0m[91mDownloading nvidia-nvjitlink-cu12 (37.4MiB)
[fastapi] [0m[91mDownloading nvidia-cudnn-cu12 (674.0MiB)
[fastapi] [0m[91mDownloading scikit-learn (8.9MiB)
[fastapi] [0m[91mDownloading pandas (12.5MiB)
[fastapi] [0m[91mDownloading mlflow (11.0MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-nvrtc-cu12 (84.0MiB)
[fastapi] [0m[91mDownloading pyarrow (47.7MiB)
[fastapi] [0m[91mDownloading transformers (10.6MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-cupti-cu12 (9.8MiB)
[fastapi] [0m[91mDownloading nvidia-cusparse-cu12 (274.9MiB)
[fastapi] [0m[91mDownloading nvidia-cublas-cu12 (566.8MiB)
[fastapi] [0m[91mDownloading nvidia-curand-cu12 (60.7MiB)
[fastapi] [0m[91mDownloading nvidia-cufft-cu12 (184.2MiB)
[fastapi] [0m[91mDownloading scipy (35.9MiB)
[fastapi] [0m[91mDownloading fonttools (5.2MiB)
[fastapi] [0m[91mDownloading torch (846.9MiB)
[fastapi] [0m[91mDownloading bitsandbytes (57.8MiB)
[fastapi] [0m[91mDownloading wandb (20.4MiB)
[fastapi] [0m[91mDownloading nvidia-cusolver-cu12 (255.1MiB)
[fastapi] [0m[91mDownloading triton (148.3MiB)
[fastapi] [0m[91mDownloading nvidia-nccl-cu12 (307.4MiB)
[fastapi] [0m[91mDownloading grpcio (6.9MiB)
[fastapi] [0m[91mDownloading matplotlib (9.4MiB)
[fastapi] [0m[91mDownloading dash (8.5MiB)
[fastapi] [0m[91mDownloading tensorboard-data-server (6.3MiB)
[fastapi] [0m[91mDownloading cryptography (4.5MiB)
[fastapi] [0m[91mDownloading mlflow-skinny (3.5MiB)
[fastapi] [0m[91mDownloading hf-xet (4.3MiB)
[fastapi] [0m[91mDownloading sqlalchemy (3.3MiB)
[fastapi] [0m[91mDownloading tokenizers (3.1MiB)
[fastapi] [0m[91mDownloading pycryptodome (2.2MiB)
[fastapi] [0m[91mDownloading openai (1.9MiB)
[fastapi] [0m[91mDownloading pydantic-core (2.0MiB)
[fastapi] [0m[91mDownloading mlflow-tracing (1.7MiB)
[fastapi] [0m[91mDownloading nltk (1.7MiB)
[fastapi] [0m[91mDownloading aiohttp (1.7MiB)
[fastapi] [0m[91mDownloading kiwisolver (1.4MiB)
[fastapi] [0m[91mDownloading mpi4py (1.3MiB)
[fastapi] [0m[91mDownloading sentencepiece (1.2MiB)
[fastapi] [0m[91mDownloading nvidia-cufile-cu12 (1.1MiB)
[fastapi] [0m[91m      Built antlr4-python3-runtime==4.9.3
[fastapi] [0m[91m Downloaded sentencepiece
[fastapi] [0m[91m Downloaded nvidia-cufile-cu12
[fastapi] [0m[91m Downloaded mpi4py
[fastapi] [0m[91m Downloaded kiwisolver
[fastapi] [0m[91m Downloaded mlflow-tracing
[fastapi] [0m[91m Downloaded aiohttp
[fastapi] [0m[91m Downloaded nltk
[fastapi] [0m[91m Downloaded pyphen
[fastapi] [0m[91m Downloaded openai
[fastapi] [0m[91m Downloaded pydantic-core
[fastapi] [0m[91m Downloaded pycryptodome
[fastapi] [0m[91m   Building rouge-score==0.1.2
[fastapi] [0m[91m      Built deepspeed==0.19.2
[fastapi] [0m[91m      Built rouge-score==0.1.2
[fastapi] [0m[91m Downloaded tokenizers
[fastapi] [0m[91m Downloaded sqlalchemy
[fastapi] [0m[91m Downloaded mlflow-skinny
[fastapi] [0m[91m Downloaded hf-xet
[fastapi] [0m[91m Downloaded cryptography
[fastapi] [0m[91m Downloaded tensorboard
[fastapi] [0m[91m Downloaded fonttools
[fastapi] [0m[91m Downloaded tensorboard-data-server
[fastapi] [0m[91m Downloaded grpcio
[fastapi] [0m[91m Downloaded plotly
[fastapi] [0m[91m Downloaded dash
[fastapi] [0m[91m Downloaded scikit-learn
[fastapi] [0m[91m Downloaded matplotlib
[fastapi] [0m[91m Downloaded nvidia-cuda-cupti-cu12
[fastapi] [0m[91m Downloaded transformers
[fastapi] [0m[91m Downloaded mlflow
[fastapi] [0m[91m Downloaded pandas
[fastapi] [0m[91m Downloaded wandb
[fastapi] [0m[91m Downloaded scipy
[fastapi] [0m[91m Downloaded nvidia-nvjitlink-cu12
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
[fastapi] [0m[91mPrepared 158 packages in 1m 15s
[fastapi] [0m[91mUninstalled 22 packages in 4.51s
[fastapi] [0m[91mInstalled 158 packages in 871ms
[fastapi] [0m[91m + absl-py==2.5.0
[fastapi] + accelerate==1.14.0
[fastapi] + aiohappyeyeballs==2.7.1
[fastapi] + aiohttp==3.14.3
[fastapi] + aiosignal==1.4.0
[fastapi] + alembic==1.20.0
[fastapi] + annotated-doc==0.0.5
[fastapi] + annotated-types==0.8.0
[fastapi] + antlr4-python3-runtime==4.9.3
[fastapi] [0m[91m - anyio==4.9.0
[fastapi] + anyio==4.15.1
[fastapi] + astor==0.8.1
[fastapi] +[0m[91m bitsandbytes==0.49[0m[91m.2[0m[91m
[fastapi] [0m[91m+ [0m[91mblinker==[0m[91m1.9[0m[91m.[0m[91m0
[fastapi] [0m[91m+ [0m[91mcachetools==7.1.8
[fastapi] - cffi==1.17.1
[fastapi] +[0m[91m cffi==2.1.1
[fastapi] + click==8.5[0m[91m.0
[fastapi] + cloudpickle==3.1.2
[fastapi] + cmudict==1.1.3
[fastapi] + contourpy==1[0m[91m.3.3
[fastapi] [0m[91m + cryptography==[0m[91m50.0.1
[fastapi] + cycler==0.12.1
[fastapi] + dash[0m[91m==4.4.1
[fastapi] [0m[91m + databricks-sdk[0m[91m==0[0m[91m.139.0[0m[91m
[fastapi] [0m[91m+ datasets[0m[91m==5.0.[0m[91m1
[fastapi] + deepspeed==0.19.2
[fastapi] + detoxify==0.5.2
[fastapi] + dill==0.4.1
[fastapi] + [0m[91mdocker==7.2.0[0m[91m
[fastapi] + docker-pycreds==0.4.0
[fastapi] + [0m[91meinops==0.8.1[0m[91m
[fastapi] + fastapi[0m[91m==0.141.1
[fastapi] + flask==3.1.3
[fastapi] + flask-cors==6.0.5
[fastapi] + fonttools==4.[0m[91m65.0
[fastapi] [0m[91m+ frozenlist==1.[0m[91m8.0
[fastapi] +[0m[91m gdown[0m[91m==6.2[0m[91m.0
[fastapi] [0m[91m+ gitdb[0m[91m==4.0.[0m[91m12
[fastapi] [0m[91m+ gitpython==3.1.62[0m[91m
[fastapi] + google-auth==[0m[91m2.58.0[0m[91m
[fastapi] + graphene==3.4.3
[fastapi] + graphql-core[0m[91m==3.2.[0m[91m12
[fastapi] +[0m[91m graphql-relay==3.[0m[91m2.0
[fastapi] +[0m[91m greenlet==3.5.[0m[91m6
[fastapi] + [0m[91mgrpcio==1.84.0
[fastapi] + gunicorn==26.2.0
[fastapi] - h11==0.14.0
[fastapi] + h11==0.16.0
[fastapi] + hf-xet[0m[91m==1.6.0
[fastapi] [0m[91m+ hjson[0m[91m==3.1.0
[fastapi] - httpcore==1.0.[0m[91m7
[fastapi] + httpcore==[0m[91m1.0.9[0m[91m
[fastapi] + [0m[91mhttpcore2==2[0m[91m.13[0m[91m.0[0m[91m
[fastapi] + [0m[91mhttpx2[0m[91m==[0m[91m2.13.0
[fastapi] + huey==3.4.0
[fastapi] + huggingface-hub==1.31.0
[fastapi] -[0m[91m idna==3.10
[fastapi] + idna==3.19
[fastapi] + importlib-metadata==9.0.1
[fastapi] + importlib-resources==7.1.0
[fastapi] + itsdangerous==2.2.0
[fastapi] + jaconv==0.5.0
[fastapi] + janus==2.0.0
[fastapi] + jiter==0.17[0m[91m.0
[fastapi] + joblib[0m[91m==1.6[0m[91m.0
[fastapi] + kiwisolver==1.5.1
[fastapi] +[0m[91m langcheck==0.9[0m[91m.0
[fastapi] +[0m[91m liger-kernel==0.[0m[91m8.2
[fastapi] + mako==1.4.1
[fastapi] + markdown==3.10.3
[fastapi] [0m[91m+ matplotlib==3.11.2
[fastapi] + minio==7.2.20
[fastapi] + mlflow==3.16.0
[fastapi] + mlflow-skinny==3.16.0
[fastapi] + mlflow-tracing==3.16.0
[fastapi] + mpi4py==4.1.2
[fastapi] [0m[91m + msgpack==1.2[0m[91m.2
[fastapi] + multidict==6.8.0
[fastapi] +[0m[91m multiprocess==0.70.19[0m[91m
[fastapi] + narwhals[0m[91m==2.26[0m[91m.0
[fastapi] +[0m[91m nlpaug==[0m[91m1.1.11[0m[91m
[fastapi] + nltk[0m[91m==3.10.[0m[91m3[0m[91m
[fastapi] - [0m[91mnvidia-cublas-cu12==12[0m[91m.8.[0m[91m3.14[0m[91m
[fastapi] + nvidia-cublas-cu12==12.8.4.1
[fastapi] - nvidia-cuda-cupti-cu12==12.8.57
[fastapi] + nvidia-cuda-cupti-cu12==12.8.90
[fastapi] - nvidia-cuda-nvrtc-cu12[0m[91m==12.8.61
[fastapi] [0m[91m + [0m[91mnvidia-cuda-nvrtc-cu12==12.8.93
[fastapi] - nvidia-cuda-runtime-cu12==12.8.57
[fastapi] + nvidia-cuda-runtime-cu12[0m[91m==12.8.90
[fastapi] - nvidia-cudnn-cu12==9.8.0.87
[fastapi] + nvidia-cudnn-cu12==9.10.2.21
[fastapi] - nvidia-cufft-cu12==11.3.3.41
[fastapi] [0m[91m + nvidia-cufft-cu12==11[0m[91m.3.3[0m[91m.83
[fastapi] - nvidia-cufile-cu12==1.13.0.11[0m[91m
[fastapi] + nvidia-cufile-cu12==1.13.1.3
[fastapi] [0m[91m- nvidia-curand-cu12==10[0m[91m.3.9.[0m[91m55
[fastapi] +[0m[91m nvidia-curand-cu12==10.3.[0m[91m9.90
[fastapi] [0m[91m- nvidia-cusolver-cu12==[0m[91m11.7.2.55
[fastapi] + nvidia-cusolver-cu12==11.7.[0m[91m3.90
[fastapi] -[0m[91m nvidia-cusparse-cu12[0m[91m==12.5.[0m[91m7.53
[fastapi] [0m[91m [0m[91m+ nvidia-cusparse-cu12[0m[91m==[0m[91m12[0m[91m.5.[0m[91m8.[0m[91m93
[fastapi] [0m[91m - nvidia-cusparselt-cu12==0.6.3
[fastapi] + nvidia-cusparselt-cu12==0.7.1
[fastapi] - nvidia-nccl-cu12[0m[91m==2.25.1
[fastapi] [0m[91m + nvidia-nccl-cu12==2.27.3
[fastapi] - nvidia-nvjitlink-cu12==12.8.61
[fastapi] + nvidia-nvjitlink-cu12==12.8.93
[fastapi] -[0m[91m nvidia-nvtx-cu12==12.8.[0m[91m55
[fastapi] + [0m[91mnvidia-nvtx-cu12==12.8[0m[91m.90
[fastapi] + omegaconf==2.3.1
[fastapi] + openai==3.14.0
[fastapi] + opentelemetry-api[0m[91m==1.44.0
[fastapi] + opentelemetry-proto==1.44.0
[fastapi] + opentelemetry-sdk==1[0m[91m.44.0
[fastapi] [0m[91m [0m[91m+ opentelemetry-semantic-conventions==0.65b0
[fastapi] + pandas==2.2.3
[fastapi] + peft==0.19.1[0m[91m
[fastapi] + plotly[0m[91m==7.[0m[91m0.0
[fastapi] + prettytable[0m[91m==3.18.0
[fastapi] + propcache==0.5.2
[fastapi] [0m[91m + protobuf==6.33[0m[91m.6
[fastapi] +[0m[91m py-cpuinfo==9[0m[91m.0.[0m[91m0
[fastapi] [0m[91m +[0m[91m [0m[91mpyarrow==[0m[91m25.0.[0m[91m1
[fastapi] [0m[91m + pyasn1==0.6.4
[fastapi] + pyasn1-modules==0.4.2
[fastapi] + pycryptodome==3.23.0
[fastapi] + pydantic==2.13.5
[fastapi] + pydantic-core==2.46[0m[91m.5
[fastapi] + pyparsing[0m[91m==3.[0m[91m3.2
[fastapi] + pyphen==0.18.1
[fastapi] +[0m[91m pysocks==1[0m[91m.7.1
[fastapi] + [0m[91mpython-dotenv==1.2.3[0m[91m
[fastapi] [0m[91m+ pytz==2026.3.post1[0m[91m
[fastapi] + regex==2026.9.10
[fastapi] + restrictedpython==8.0
[fastapi] + retrying==1.4.2
[fastapi] + rouge-score==0.1.[0m[91m2
[fastapi] + safetensors==0.8[0m[91m.0
[fastapi] + scikit-learn==1[0m[91m.9.1[0m[91m
[fastapi] [0m[91m+ scipy==1[0m[91m.15.[0m[91m2
[fastapi] +[0m[91m sentence-transformers[0m[91m==6.0[0m[91m.1
[fastapi] +[0m[91m sentencepiece==0[0m[91m.2.0
[fastapi] + [0m[91msentry-sdk==2[0m[91m.[0m[91m69.1[0m[91m
[fastapi] [0m[91m+ [0m[91msetproctitle[0m[91m==1.[0m[91m3[0m[91m.7[0m[91m
[fastapi] +[0m[91m [0m[91msix==[0m[91m1[0m[91m.17.0
[fastapi] [0m[91m + skops[0m[91m==[0m[91m0.14.0[0m[91m
[fastapi] [0m[91m +[0m[91m smmap==[0m[91m5.0.3
[fastapi] + sqlalchemy==2.0.53
[fastapi] + sqlparse==0.6.0
[fastapi] +[0m[91m starlette==1.6.[0m[91m0
[fastapi] +[0m[91m tabulate==0[0m[91m.10.0
[fastapi] [0m[91m+ tenacity[0m[91m==9.1.4[0m[91m
[fastapi] + [0m[91mtensorboard==[0m[91m2.[0m[91m19.0[0m[91m
[fastapi] [0m[91m + [0m[91mtensorboard-data-server==0.7.2
[fastapi] + textstat==0[0m[91m.7.[0m[91m8
[fastapi] +[0m[91m threadpoolctl[0m[91m==3.6.0
[fastapi] + tokenizers==0.22.2
[fastapi] + toml==0.10.2
[fastapi] -[0m[91m torch==2.[0m[91m8.0.dev20250319[0m[91m+[0m[91mcu128
[fastapi] + torch==2.8.0
[fastapi] + tqdm==4.70.1
[fastapi] + transformers==5.12.1
[fastapi] + triton==3.4.0
[fastapi] + trl==1.10.0
[fastapi] + truststore==0.10.4
[fastapi] [0m[91m+ typer==0[0m[91m.9.0[0m[91m
[fastapi] - typing-extensions==4.12.2
[fastapi] +[0m[91m typing-extensions[0m[91m==4.16.[0m[91m0[0m[91m
[fastapi] [0m[91m +[0m[91m [0m[91mtyping-inspection==0.4.4
[fastapi] + tzdata==2026.4
[fastapi] + uvicorn==0.53.0
[fastapi] + wandb==0.19.10
[fastapi] - wcwidth==0.2.13
[fastapi] + wcwidth==0.[0m[91m8.3
[fastapi] + [0m[91mwerkzeug==3.1.8
[fastapi] + xxhash[0m[91m==4.0[0m[91m.1
[fastapi] [0m[91m+ yarl==1[0m[91m.24.5
[fastapi] + [0m[91mzipp==4.1[0m[91m.0
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
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 24.2 MB/s eta 0:00:00
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
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 256.0/256.0 MB 37.7 MB/s eta 0:00:00
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
[fastapi] Cloning https://github.com/rayonlabs/fiber.git (to revision 2.4.0) to /tmp/pip-install-87wk3ij3/fiber_52f89b6e72894d8b9bb6ca8f7593ecac
[fastapi] [91m  Running command git clone --filter=blob:none --quiet https://github.com/rayonlabs/fiber.git /tmp/pip-install-87wk3ij3/fiber_52f89b6e72894d8b9bb6ca8f7593ecac
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
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 552.2/552.2 kB 15.7 MB/s eta 0:00:00
[fastapi] Downloading eth_typing-5.0.0-py3-none-any.whl (20 kB)
[fastapi] Downloading netaddr-1.3.0-py3-none-any.whl (2.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.3/2.3 MB 35.6 MB/s eta 0:00:00
[fastapi] Downloading python_dotenv-1.0.1-py3-none-any.whl (19 kB)
[fastapi] Downloading substrate_interface-1.7.10-py3-none-any.whl (60 kB)
[fastapi] Downloading tenacity-9.0.0-py3-none-any.whl (28 kB)
[fastapi] Downloading async_substrate_interface-1.6.4-py3-none-any.whl (97 kB)
[fastapi] Downloading bt_decode-0.8.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (647 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 647.8/647.8 kB 21.4 MB/s eta 0:00:00
[fastapi] Downloading colorama-0.4.6-py2.py3-none-any.whl (25 kB)
[fastapi] Downloading pydantic-2.9.2-py3-none-any.whl (434 kB)
[fastapi] Downloading pydantic_core-2.23.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 34.3 MB/s eta 0:00:00
[fastapi] Downloading aiosqlite-0.22.1-py3-none-any.whl (17 kB)
[fastapi] Downloading base58-2.1.1-py3-none-any.whl (5.6 kB)
[fastapi] Downloading ecdsa-0.19.2-py2.py3-none-any.whl (150 kB)
[fastapi] Downloading eth_keys-0.8.0-py3-none-any.whl (20 kB)
[fastapi] Downloading eth_utils-2.3.2-py3-none-any.whl (77 kB)
[fastapi] Downloading py_bip39_bindings-0.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (432 kB)
[fastapi] Downloading py_ed25519_zebra_bindings-1.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (323 kB)
[fastapi] Downloading py_sr25519_bindings-0.2.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (372 kB)
[fastapi] Downloading pynacl-1.6.2-cp38-abi3-manylinux_2_34_x86_64.whl (1.4 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.4/1.4 MB 28.9 MB/s eta 0:00:00
[fastapi] Downloading scalecodec-1.2.12-py3-none-any.whl (99 kB)
[fastapi] Downloading websockets-17.1-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (224 kB)
[fastapi] Downloading xxhash-3.8.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (220 kB)
[fastapi] Downloading cytoolz-1.1.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (2.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.8/2.8 MB 35.1 MB/s eta 0:00:00
[fastapi] Downloading eth_hash-0.8.0-py3-none-any.whl (8.0 kB)
[fastapi] Downloading toolz-1.1.0-py3-none-any.whl (58 kB)
[fastapi] Building wheels for collected packages: fiber
[fastapi] Building wheel for fiber (pyproject.toml): started
[fastapi] Building wheel for fiber (pyproject.toml): finished with status 'done'
[fastapi] Created wheel for fiber: filename=fiber-2.4.0-py3-none-any.whl size=51790 sha256=c50f803eff2fbcdf01560cfffdc65a3891a75b0b315d61d842fd3861f51b5d73
[fastapi] Stored in directory: /tmp/pip-ephem-wheel-cache-iwgu9jb1/wheels/d1/5e/21/2fa1f403cd187996037f04f6328bf11973ce31440a275f6949
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
[fastapi] Successfully installed PyNaCl-1.6.2 aiosqlite-0.22.1 async-substrate-interface-1.6.4 base58-2.1.1 bittensor-commit-reveal-0.1.0 bt-decode-0.8.0 colorama-0.4.6 cytoolz-1.1.0 ecdsa-0.19.2 eth-hash-0.8.0 eth-keys-0.8.0 eth-typing-5.0.0 eth-utils-2.3.2 fiber-2.4.0 netaddr-1.3.0 py-bip39-bindings-0.3.0 py-ed25519-zebra-bindings-1.3.0 py-sr25519-bindings-0.2.4 pydantic-2.9.2 pydantic-core-2.23.4 python-dotenv-1.0.1 scalecodec-1.2.12 substrate-interface-1.7.10 tenacity-9.0.0 toolz-1.1.0 websockets-17.1 xxhash-3.8.1
[fastapi] [91mERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
[fastapi] dash 4.4.1 requires pydantic>=2.10, but you have pydantic 2.9.2 which is incompatible.
[fastapi] WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 25.0.1 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0m ---> e354d38107a1
[fastapi] Step 8/13 : RUN pip install --index-url https://download.pytorch.org/whl/cu128     torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0
[fastapi] ---> Running in f77173d111af
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
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.6/8.6 MB 35.4 MB/s eta 0:00:00
[fastapi] Downloading https://download-r2.pytorch.org/whl/cu128/torchaudio-2.8.0%2Bcu128-cp311-cp311-manylinux_2_28_x86_64.whl (3.9 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.9/3.9 MB 28.0 MB/s eta 0:00:00
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
[fastapi] [0m ---> 24ff3d4c4f5f
[fastapi] Step 9/13 : RUN python -m venv /workspace/grpo_py &&     /workspace/grpo_py/bin/pip install -U pip uv &&     /workspace/grpo_py/bin/python -m uv pip install         --python /workspace/grpo_py/bin/python         -r /workspace/scripts/grpo_requirements.txt &&     /workspace/grpo_py/bin/python -c "import torch, vllm, trl, transformers; print('grpo venv', torch.__version__, vllm.__version__, trl.__version__, transformers.__version__)"
[fastapi] ---> Running in f193af058ab3
[fastapi] Requirement already satisfied: pip in /workspace/grpo_py/lib/python3.11/site-packages (24.0)
[fastapi] Collecting pip
[fastapi] Downloading pip-26.2.1-py3-none-any.whl.metadata (4.6 kB)
[fastapi] Collecting uv
[fastapi] Using cached uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] Downloading pip-26.2.1-py3-none-any.whl (1.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 12.4 MB/s eta 0:00:00
[fastapi] Using cached uv-0.12.15-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.1 MB)
[fastapi] Installing collected packages: uv, pip
[fastapi] Attempting uninstall: pip
[fastapi] Found existing installation: pip 24.0
[fastapi] Uninstalling pip-24.0:
[fastapi] Successfully uninstalled pip-24.0
[fastapi] Successfully installed pip-26.2.1 uv-0.12.15
[fastapi] [91mUsing Python 3.11.11 environment at: /workspace/grpo_py
[fastapi] [0m[91mResolved 258 packages in 872ms
[fastapi] [0m[91mDownloading networkx (2.0MiB)
[fastapi] [0m[91mDownloading mistral-common (6.2MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-cccl (3.7MiB)
[fastapi] [0m[91mDownloading nvidia-nvvm (69.2MiB)
[fastapi] [0m[91mDownloading nvidia-cusparse (139.2MiB)
[fastapi] [0m[91mDownloading nvidia-nccl-cu13 (187.4MiB)
[fastapi] [0m[91mDownloading nvidia-cutlass-dsl-libs-cu12 (84.3MiB)
[fastapi] [0m[91mDownloading nvidia-curand (56.8MiB)
[fastapi] [0m[91mDownloading nvidia-cutlass-dsl-libs-base (2.7MiB)
[fastapi] [0m[91mDownloading vllm (289.6MiB)
[fastapi] [0m[91mDownloading nvidia-nvjitlink (38.8MiB)
[fastapi] [0m[91mDownloading pycountry (7.7MiB)
[fastapi] [0m[91mDownloading flashinfer-python (13.9MiB)
[fastapi] [0m[91mDownloading nvidia-cusparselt-cu13 (162.0MiB)
[fastapi] [0m[91mDownloading nvidia-cublas (403.5MiB)
[fastapi] [0m[91mDownloading llguidance (2.9MiB)
[fastapi] [0m[91mDownloading sympy (6.0MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-nvrtc (86.0MiB)
[fastapi] [0m[91mDownloading pillow (6.6MiB)
[fastapi] [0m[91mDownloading nvidia-cusolver (191.6MiB)
[fastapi] [0m[91mDownloading z3-solver (27.9MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-nvcc (45.5MiB)
[fastapi] [0m[91mDownloading nvidia-cufft (204.2MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-cupti (10.2MiB)
[fastapi] [0m[91mDownloading[0m[91m llvmlite (53.7MiB)
[fastapi] [0m[91mDownloading nvidia-cudnn-cu13 (349.1MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-nvdisasm (5.0MiB)
[fastapi] [0m[91mDownloading torchcodec (9.0MiB)
[fastapi] [0m[91mDownloading cuda-bindings (6.8MiB)
[fastapi] [0m[91mDownloading uvloop (3.6MiB)
[fastapi] [0m[91mDownloading nvidia-cutlass-dsl-libs-cu13 (83.9MiB)
[fastapi] [0m[91mDownloading torch (506.0MiB)
[fastapi] [0m[91mDownloading tokenspeed-triton (77.9MiB)
[fastapi] [0m[91mDownloading pynvvideocodec (41.2MiB)
[fastapi] [0m[91mDownloading triton (179.5MiB)
[fastapi] [0m[91mDownloading nvidia-cudnn-frontend (5.4MiB)
[fastapi] [0m[91mDownloading numba (3.6MiB)
[fastapi] [0m[91mDownloading tilelang (43.3MiB)
[fastapi] [0m[91mDownloading nvidia-nvshmem-cu13 (57.6MiB)
[fastapi] [0m[91mDownloading numpy (16.1MiB)
[fastapi] [0m[91mDownloading opencv-python-headless (58.4MiB)
[fastapi] [0m[91mDownloading cuda-core (6.2MiB)
[fastapi] [0m[91mDownloading torchvision (7.2MiB)
[fastapi] [0m[91mDownloading apache-tvm-ffi (2.5MiB)
[fastapi] [0m[91mDownloading openai-harmony (2.8MiB)
[fastapi] [0m[91mDownloading outlines-core (2.2MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-runtime (2.1MiB)
[fastapi] [0m[91mDownloading fastsafetensors (2.0MiB)
[fastapi] [0m[91mDownloading torchaudio (1.7MiB)
[fastapi] [0m[91mDownloading pygments (1.2MiB)
[fastapi] [0m[91m Downloaded pygments
[fastapi] [0m[91mDownloading anthropic (1.2MiB)
[fastapi] [0m[91m Downloaded torchaudio
[fastapi] [0m[91mDownloading xgrammar (1.2MiB)
[fastapi] [0m[91m Downloaded networkx
[fastapi] [0m[91mDownloading nvidia-cufile (1.2MiB)
[fastapi] [0m[91m Downloaded fastsafetensors
[fastapi] [0m[91mDownloading tiktoken (1.2MiB)
[fastapi] [0m[91m Downloaded nvidia-cuda-runtime
[fastapi] [0m[91m Downloaded outlines-core
[fastapi] [0m[91m Downloaded apache-tvm-ffi
[fastapi] [0m[91m Downloaded nvidia-cutlass-dsl-libs-base
[fastapi] [0m[91m Downloaded openai-harmony
[fastapi] [0m[91m Downloaded anthropic
[fastapi] [0m[91m Downloaded llguidance
[fastapi] [0m[91m Downloaded xgrammar
[fastapi] [0m[91m Downloaded nvidia-cufile
[fastapi] [0m[91m Downloaded tiktoken
[fastapi] [0m[91m Downloaded uvloop
[fastapi] [0m[91m Downloaded numba
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
[fastapi] [0m[91m Downloaded nvidia-cutlass-dsl-libs-cu13
[fastapi] [0m[91m Downloaded nvidia-cutlass-dsl-libs-cu12
[fastapi] [0m[91m Downloaded nvidia-cuda-nvrtc
[fastapi] [0m[91m Downloaded nvidia-cusparse
[fastapi] [0m[91m Downloaded nvidia-cusparselt-cu13
[fastapi] [0m[91m Downloaded triton
[fastapi] [0m[91m Downloaded nvidia-nccl-cu13
[fastapi] [0m[91m Downloaded nvidia-cusolver
[fastapi] [0m[91m Downloaded nvidia-cufft
[fastapi] [0m[91m Downloaded vllm
[fastapi] [0m[91m Downloaded nvidia-cudnn-cu13
[fastapi] [0m[91m Downloaded nvidia-cublas
[fastapi] [0m[91m Downloaded torch
[fastapi] [0m[91mPrepared 151 packages in 1m 11s
[fastapi] [0m[91mInstalled 257 packages in 32.33s
[fastapi] [0m[91m + absl-py==2.5.0
[fastapi] + accelerate==1.14.0
[fastapi] + agent-detector==2.0.0
[fastapi] + aiohappyeyeballs==2.7.1
[fastapi] + aiohttp==3.14.3
[fastapi] + aiosignal==1.4.0
[fastapi] + annotated-doc==0.0.5
[fastapi] + annotated-types==0.8.0
[fastapi] + anthropic==1.6.0
[fastapi] + antlr4-python3-runtime==4.9.3
[fastapi] + anyio==4.15.1
[fastapi] + apache-tvm-ffi==0.1.[0m[91m10
[fastapi] + argon2-cffi==25.1.0
[fastapi] + argon2-cffi-bindings==26.1.0
[fastapi] +[0m[91m astor==0.8.1[0m[91m
[fastapi] [0m[91m+[0m[91m attrs==26.1.0
[fastapi] + beautifulsoup4==4[0m[91m.15.0
[fastapi] +[0m[91m bitsandbytes==0.[0m[91m49.2
[fastapi] + blake3==1.0.9
[fastapi] + blinker[0m[91m==1.9[0m[91m.0
[fastapi] [0m[91m +[0m[91m cachetools[0m[91m==7[0m[91m.1[0m[91m.8
[fastapi] [0m[91m + cbor2[0m[91m==6[0m[91m.1[0m[91m.4
[fastapi] + certifi==2026.7.22
[fastapi] + cffi==2.1.1
[fastapi] + charset-normalizer==3.5.1
[fastapi] + [0m[91mclick==8.5.0
[fastapi] + cloudpickle[0m[91m==3.1.2
[fastapi] [0m[91m + cmudict==1.1.[0m[91m3
[fastapi] +[0m[91m comm[0m[91m==0.2[0m[91m.3
[fastapi] [0m[91m + compressed-tensors==0[0m[91m.17.0
[fastapi] [0m[91m + cryptography==50.0.1
[fastapi] + cuda-bindings[0m[91m==13.4.1[0m[91m
[fastapi] + [0m[91mcuda-core==1.[0m[91m2.0
[fastapi] [0m[91m+ cuda-pathfinder[0m[91m==1.8.[0m[91m1
[fastapi] + cuda-python[0m[91m==13.4[0m[91m.1
[fastapi] + [0m[91mcuda-tile==1.6.0
[fastapi] + cuda-toolkit==13.0.2
[fastapi] + dash==4.4.1
[fastapi] + [0m[91mdatasets==5.0.[0m[91m1
[fastapi] + deepspeed==[0m[91m0.19.2
[fastapi] + [0m[91mdefusedxml[0m[91m==0.7.[0m[91m1[0m[91m
[fastapi] +[0m[91m [0m[91mdepyf==[0m[91m0[0m[91m.20.0
[fastapi] + detect-installer==0.2.1
[fastapi] + detoxify==0.5.2
[fastapi] + dill[0m[91m==0.4.1
[fastapi] +[0m[91m dnspython==2.[0m[91m8.0
[fastapi] + docker-pycreds==0.4.0
[fastapi] + docstring-parser[0m[91m==0.18.0[0m[91m
[fastapi] + einops[0m[91m==0.8.1[0m[91m
[fastapi] [0m[91m+[0m[91m email-validator==2.3[0m[91m.0[0m[91m
[fastapi] [0m[91m+ [0m[91mfastapi[0m[91m==0.[0m[91m136.3[0m[91m
[fastapi] + fastapi-cli==0[0m[91m.0.32
[fastapi] [0m[91m+ fastapi-cloud-cli[0m[91m==[0m[91m0.26[0m[91m.0[0m[91m
[fastapi] + fastar==0[0m[91m.12.0
[fastapi] +[0m[91m fastsafetensors==0.[0m[91m4.0
[fastapi] [0m[91m+ filelock==[0m[91m3.32.[0m[91m6
[fastapi] +[0m[91m flashinfer-python==[0m[91m0.6.14
[fastapi] + flask==3.1.3[0m[91m
[fastapi] +[0m[91m frozenlist[0m[91m==1.8.[0m[91m0
[fastapi] + fsspec==2026.6.0
[fastapi] + gdown==6.2.0
[fastapi] + gitdb==4.0[0m[91m.12
[fastapi] + [0m[91mgitpython==3.1[0m[91m.62
[fastapi] + googleapis-common-protos==1.75.3
[fastapi] +[0m[91m grpcio==1.84.0[0m[91m
[fastapi] + h11[0m[91m==0[0m[91m.16[0m[91m.[0m[91m0
[fastapi] +[0m[91m hf-xet==1.6.0
[fastapi] + hjson==3.1.0[0m[91m
[fastapi] + httpcore[0m[91m==1.0.[0m[91m9
[fastapi] + httpcore2==2.13.0
[fastapi] + httptools[0m[91m==0.8.0
[fastapi] [0m[91m + httpx==0.[0m[91m28.1
[fastapi] +[0m[91m httpx2==2.13[0m[91m.0
[fastapi] [0m[91m+ [0m[91mhuggingface-hub==[0m[91m1.31[0m[91m.0
[fastapi] + humming-kernels==0.1.10
[fastapi] + idna==3.19
[fastapi] + [0m[91mijson==3[0m[91m.5[0m[91m.1[0m[91m
[fastapi] [0m[91m+ [0m[91mimportlib-metadata[0m[91m==[0m[91m9.0[0m[91m.[0m[91m1[0m[91m
[fastapi] +[0m[91m importlib-resources==7.1.0[0m[91m
[fastapi] +[0m[91m interegular==0[0m[91m.3[0m[91m.3
[fastapi] + itsdangerous==2.2.0
[fastapi] + jaconv==0.5.0
[fastapi] + janus==2.0.0
[fastapi] + jinja2==3.1.[0m[91m6
[fastapi] + jiter==0.17.0
[fastapi] + jmespath==[0m[91m1.1.[0m[91m0[0m[91m
[fastapi] +[0m[91m joblib[0m[91m==1.6.0
[fastapi] + [0m[91mjsonschema==4.26[0m[91m.0
[fastapi] + [0m[91mjsonschema-specifications==2025.9.1[0m[91m
[fastapi] + langcheck[0m[91m==0.9.0
[fastapi] +[0m[91m lark==1[0m[91m.2.2[0m[91m
[fastapi] +[0m[91m llguidance==[0m[91m1.7.6[0m[91m
[fastapi] [0m[91m+ llvmlite==0.[0m[91m47.0
[fastapi] + [0m[91mlm-format-enforcer==0.11[0m[91m.3
[fastapi] +[0m[91m loguru==0[0m[91m.7.3
[fastapi] [0m[91m + markdown-it-py[0m[91m==4.2.[0m[91m0
[fastapi] +[0m[91m markupsafe==[0m[91m3.0.3[0m[91m
[fastapi] + mcp==[0m[91m2.2.0
[fastapi] + mcp-types==2.2.0
[fastapi] + mdurl[0m[91m==0.1.2
[fastapi] + minio==7.2.20
[fastapi] + mistral-common==1.11.7
[fastapi] + ml-dtypes==0.6.0
[fastapi] + model-hosting-container-standards==0[0m[91m.1.16
[fastapi] + mpmath[0m[91m==1.3.0
[fastapi] [0m[91m + msgpack==[0m[91m1.2.2
[fastapi] + msgspec==0.21.1
[fastapi] + multidict==6.8.0
[fastapi] + multiprocess==0[0m[91m.70.19
[fastapi] + narwhals[0m[91m==2.26.0
[fastapi] + nest-asyncio==1.6[0m[91m.0
[fastapi] [0m[91m [0m[91m+[0m[91m networkx==3[0m[91m.6.1
[fastapi] [0m[91m+ ninja[0m[91m==1.13.2
[fastapi] + nlpaug==1.1.11
[fastapi] + nltk==3.10.3
[fastapi] + numba[0m[91m==0.65.0
[fastapi] +[0m[91m numpy==2[0m[91m.3.5
[fastapi] [0m[91m+ nvidia-cublas==13[0m[91m.1.0.3
[fastapi] [0m[91m + nvidia-cuda-cccl==13.3.4.2.1
[fastapi] + nvidia-cuda-crt==13.4.59
[fastapi] + nvidia-cuda-cupti==13.0.85
[fastapi] + nvidia-cuda-nvcc==13.[0m[91m4.59
[fastapi] + nvidia-cuda-nvdisasm[0m[91m==13.[0m[91m4.49
[fastapi] + nvidia-cuda-nvrtc==13.0.88
[fastapi] [0m[91m+ nvidia-cuda-runtime==13.[0m[91m0.96
[fastapi] + [0m[91mnvidia-cudnn-cu13==9.19.0.[0m[91m56
[fastapi] + nvidia-cudnn-frontend==1.28.0
[fastapi] + nvidia-cufft==12.0.0[0m[91m.61
[fastapi] + [0m[91mnvidia-cufile==1[0m[91m.15.1.6
[fastapi] + nvidia-curand[0m[91m==10.[0m[91m4.0.35
[fastapi] [0m[91m+[0m[91m [0m[91mnvidia-cusolver[0m[91m==12.[0m[91m0.4.66[0m[91m
[fastapi] [0m[91m+[0m[91m nvidia-cusparse[0m[91m==[0m[91m12.6[0m[91m.3[0m[91m.3
[fastapi] [0m[91m [0m[91m+ nvidia-cusparselt-cu13==0.8.[0m[91m0
[fastapi] + [0m[91mnvidia-cutlass-dsl==4.6.0
[fastapi] + nvidia-cutlass-dsl-libs-base==4.6.0
[fastapi] + nvidia-cutlass-dsl-libs-core==4.6.0[0m[91m
[fastapi] + nvidia-cutlass-dsl-libs-cu12==[0m[91m4.6.0
[fastapi] +[0m[91m nvidia-cutlass-dsl-libs-cu13==4.[0m[91m6.0
[fastapi] [0m[91m + nvidia-ml-py[0m[91m==13.610.43
[fastapi] [0m[91m + [0m[91mnvidia-nccl-cu13==2.28.9
[fastapi] + nvidia-nvjitlink==13.0[0m[91m.88
[fastapi] [0m[91m+ [0m[91mnvidia-nvshmem-cu13==3.4.[0m[91m5
[fastapi] [0m[91m+ nvidia-nvtx[0m[91m==13.[0m[91m0.[0m[91m85
[fastapi] + nvidia-nvvm==13.4[0m[91m.[0m[91m59[0m[91m
[fastapi] +[0m[91m [0m[91mnvtx==[0m[91m0.2.15
[fastapi] + omegaconf==2.3.1
[fastapi] + openai==3.14.0
[fastapi] + openai-harmony==0.0.8
[fastapi] + opencv-python-headless==5.[0m[91m0.0.93
[fastapi] [0m[91m + opentelemetry-api[0m[91m==1.44.0
[fastapi] + opentelemetry-exporter-otlp==1.44.0
[fastapi] [0m[91m + opentelemetry-exporter-otlp-proto-common==1[0m[91m.44.0
[fastapi] [0m[91m+ opentelemetry-exporter-otlp-proto-grpc==1.44[0m[91m.0
[fastapi] +[0m[91m opentelemetry-exporter-otlp-proto-http[0m[91m==1.44[0m[91m.[0m[91m0
[fastapi] + [0m[91mopentelemetry-proto==[0m[91m1.44.0
[fastapi] + opentelemetry-sdk==1.44.0
[fastapi] + opentelemetry-semantic-conventions==0.65b0
[fastapi] + opentelemetry-semantic-conventions-ai[0m[91m==0.5.1
[fastapi] [0m[91m + [0m[91moutlines-core==0.2.14
[fastapi] + packaging==26.3
[fastapi] +[0m[91m pandas==2.2.[0m[91m3
[fastapi] + partial-json-parser==0.2.1.1.post7
[fastapi] + peft==0.19.1
[fastapi] + pillow==12[0m[91m.3.0
[fastapi] + [0m[91mplatformdirs==4.[0m[91m11.8
[fastapi] +[0m[91m plotly==7[0m[91m.0.0
[fastapi] [0m[91m + prometheus-client[0m[91m==0.26.0[0m[91m
[fastapi] + [0m[91mprometheus-fastapi-instrumentator==8.[0m[91m1.0
[fastapi] + propcache==0.5.2[0m[91m
[fastapi] + protobuf[0m[91m==6.[0m[91m33.6
[fastapi] [0m[91m+ psutil==[0m[91m7.2.2
[fastapi] [0m[91m+ py-cpuinfo==9[0m[91m.0.0
[fastapi] +[0m[91m pyarrow==[0m[91m25[0m[91m.0.1
[fastapi] [0m[91m+[0m[91m pybase64==1.5[0m[91m.0
[fastapi] [0m[91m+[0m[91m pycountry[0m[91m==26[0m[91m.2.16[0m[91m
[fastapi] [0m[91m + pycparser[0m[91m==3.0
[fastapi] + [0m[91mpycryptodome==3.23[0m[91m.0
[fastapi] +[0m[91m pydantic==2.13.5
[fastapi] + pydantic-core==2.46.5
[fastapi] + [0m[91mpydantic-extra-types==2.11.1
[fastapi] [0m[91m + [0m[91mpydantic-settings==2.[0m[91m15.0
[fastapi] + pyelftools==0.33
[fastapi] + pygments==2.21.0
[fastapi] + pyjwt[0m[91m==2.14.0
[fastapi] [0m[91m + pynvvideocodec[0m[91m==2.0.4[0m[91m
[fastapi] + pyphen==0.18.1
[fastapi] + pysocks==1.7.1
[fastapi] + python-dateutil==2.9.0.post0
[fastapi] + python-dotenv==1.2.3
[fastapi] + python-json-logger==4[0m[91m.2.0
[fastapi] + python-multipart[0m[91m==0.0.32
[fastapi] + pytz==2026.3.post[0m[91m1
[fastapi] +[0m[91m pyyaml[0m[91m==6.0.3
[fastapi] [0m[91m+ pyzmq==27.2.0[0m[91m
[fastapi] + quack-kernels==[0m[91m0.6.3
[fastapi] + referencing==0.37.0
[fastapi] + regex==2026.9.10[0m[91m
[fastapi] + requests==2.34[0m[91m.2
[fastapi] [0m[91m+[0m[91m restrictedpython==8.[0m[91m0[0m[91m
[fastapi] + [0m[91mretrying==1.4.2
[fastapi] + rich==15.0.0
[fastapi] + rich-toolkit==0.20.5
[fastapi] +[0m[91m rignore==0.8.[0m[91m1
[fastapi] + [0m[91mrouge-score==0.1.[0m[91m2
[fastapi] + rpds-py==2026.6.3
[fastapi] + [0m[91msafetensors==0.8.[0m[91m0[0m[91m
[fastapi] [0m[91m+ scikit-learn[0m[91m==[0m[91m1.9[0m[91m.1[0m[91m
[fastapi] + [0m[91mscipy==[0m[91m1.15.2
[fastapi] + sentence-transformers==6.0.1
[fastapi] + sentencepiece==0.2.0
[fastapi] + sentry-sdk[0m[91m==2.69.1
[fastapi] [0m[91m+ setproctitle==[0m[91m1.3.7
[fastapi] + shellingham==1.5.4
[fastapi] + six==1.17.0
[fastapi] + smmap==5.0.3
[fastapi] + [0m[91msniffio==1.3.[0m[91m1
[fastapi] +[0m[91m soupsieve[0m[91m==2.9.[0m[91m2
[fastapi] [0m[91m+ sse-starlette[0m[91m==3.4.11[0m[91m
[fastapi] + starlette[0m[91m==1.6.0[0m[91m
[fastapi] + supervisor==4.3.0[0m[91m
[fastapi] + sympy[0m[91m==1.14.0
[fastapi] + tabulate==0.10[0m[91m.0[0m[91m
[fastapi] +[0m[91m tenacity==9.[0m[91m1.4[0m[91m
[fastapi] + textstat[0m[91m==0.7[0m[91m.[0m[91m8[0m[91m
[fastapi] +[0m[91m threadpoolctl==3[0m[91m.6.0
[fastapi] [0m[91m [0m[91m+ tiktoken[0m[91m==0.14.0
[fastapi] + tilelang==0.1.9
[fastapi] + tokenizers==0.22.2
[fastapi] + [0m[91mtokenspeed-mla==0.1.[0m[91m8
[fastapi] + tokenspeed-triton==3.8.10.post20260906
[fastapi] [0m[91m [0m[91m+ torch[0m[91m==2.11.0
[fastapi] + torch-c-dlpack-ext[0m[91m==[0m[91m0[0m[91m.1.5[0m[91m
[fastapi] [0m[91m+[0m[91m torchaudio[0m[91m==[0m[91m2.11.0[0m[91m
[fastapi] [0m[91m + [0m[91mtorchcodec[0m[91m==0[0m[91m.16.[0m[91m0
[fastapi] [0m[91m+ torchvision[0m[91m==0.26.0
[fastapi] + tqdm==4.70.1
[fastapi] + transformers[0m[91m==5.12.1
[fastapi] [0m[91m + triton[0m[91m==3.6.0
[fastapi] + trl==1.[0m[91m10.0
[fastapi] + truststore==0[0m[91m.10.4
[fastapi] + typer==0.27.[0m[91m2
[fastapi] [0m[91m+ typing-extensions==[0m[91m4.16[0m[91m.0
[fastapi] [0m[91m+ [0m[91mtyping-inspection==0.4.4
[fastapi] + tzdata==2026.4
[fastapi] + urllib3==2.7.0
[fastapi] + uvicorn==0.53.0
[fastapi] + uvloop[0m[91m==0.22.1[0m[91m
[fastapi] + vllm[0m[91m==0.26.0
[fastapi] + wandb==[0m[91m0.19.10
[fastapi] + watchfiles==1.2.0
[fastapi] + websockets==17.1
[fastapi] + werkzeug==3.1.8
[fastapi] + xgrammar==0.2.6
[fastapi] + xxhash==4.0.1
[fastapi] +[0m[91m yarl==1.24[0m[91m.5
[fastapi] + z3-solver==4.15.4.0
[fastapi] +[0m[91m zipp==4.1.0
[fastapi] [0mgrpo venv 2.11.0+cu130 0.26.0 1.10.0 5.12.1
[fastapi] ---> c625bc7e4edf
[fastapi] Step 10/13 : RUN python -c "import transformers; v=transformers.__version__; assert v == '5.12.1', v" &&     python -c "import torch; assert torch.__version__.startswith('2.8.0'), torch.__version__" &&     python -c "import liger_kernel; from liger_kernel.ops.fused_linear_cross_entropy import LigerFusedLinearCrossEntropyFunction as F; assert hasattr(F.forward, '__call__')" &&     python -c "import flash_attn, trl, peft, bitsandbytes" &&     python -c "from deepspeed import DeepSpeedEngine; print('deps ok (deepspeed importable)')"
[fastapi] ---> Running in 8a0c0f9972da
[fastapi] [91m/usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[fastapi] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[fastapi] warnings.warn(
[fastapi] [0mdeps ok (deepspeed importable)
[fastapi] ---> 18d32199a1b5
[fastapi] Step 11/13 : COPY scripts /workspace/scripts
[fastapi] ---> 11e9a0e4d902
[fastapi] Step 12/13 : RUN chmod +x /workspace/scripts/entrypoint.sh
[fastapi] ---> Running in 54290d84b6b4
[fastapi] ---> ce2b76aac626
[fastapi] Step 13/13 : ENTRYPOINT ["./entrypoint.sh"]
[fastapi] ---> Running in 7be2ae190a77
[fastapi] ---> bb764562ecea
[fastapi] {'aux': {'ID': 'sha256:bb764562ecea41a234fb32349a70498fae97e7c9be04ee5d6913f3960f1277b2'}}Successfully built bb764562ecea
[fastapi] Successfully tagged standalone-text-trainer:39a07ca9-b67c-4949-b648-94572a09021e
[fastapi] Docker image built successfully.
[fastapi] Cleaning up
[fastapi] Cleaned up Docker resources.
[fastapi] Starting upload container hf-upload-cf0c33a06c21414fa09db24a855e14aa for task 24c8317e-07e4-4424-b996-b336dde5a580...
[hf-upload-cf] Updated adapter_config.json with base_model: Qwen/Qwen3-32B
[hf-upload-cf] Updated README.md with base_model: Qwen/Qwen3-32B
[hf-upload-cf] Creating repo gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-24c8317e-07e4-4424-b996-b336dde5a580-5DDVSRDL...
[hf-upload-cf] Uploading contents of /app/checkpoints/24c8317e-07e4-4424-b996-b336dde5a580/tournament-tourn_5c64e784a087074a_20260914-24c8317e-07e4-4424-b996-b336dde5a580-5DDVSRDL to gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-24c8317e-07e4-4424-b996-b336dde5a580-5DDVSRDL
[hf-upload-cf] Uploaded successfully to https://huggingface.co/gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-24c8317e-07e4-4424-b996-b336dde5a580-5DDVSRDL
[hf-upload-cf] Deleted local folder: /app/checkpoints/24c8317e-07e4-4424-b996-b336dde5a580/tournament-tourn_5c64e784a087074a_20260914-24c8317e-07e4-4424-b996-b336dde5a580-5DDVSRDL
[text-trainer] *****Running text trainer
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_hash" in MinerSubmission has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] [2026-09-15 15:25:57,407] [WARNING] [runner.py:232:fetch_hostfile] Unable to find hostfile, will proceed with training with local resources only.
[text-trainer] [2026-09-15 15:25:57,407] [INFO] [runner.py:630:main] cmd = /usr/bin/python -u -m deepspeed.launcher.launch --world_info=eyJsb2NhbGhvc3QiOiBbMCwgMSwgMiwgM119 --master_addr=127.0.0.1 --master_port=29500 --enable_each_rank_log=None --log_level=info train_instruct.py --request_path datasets/training_request_24c8317e-07e4-4424-b996-b336dde5a580.json --bf16 True --report_to wandb --output_dir /workspace/scripts/soutputs/24c8317e-07e4-4424-b996-b336dde5a580 --num_train_epochs 3 --per_device_train_batch_size 18 --per_device_eval_batch_size 1 --gradient_accumulation_steps 1 --eval_accumulation_steps 1 --eval_strategy no --save_strategy epoch --logging_steps 1 --learning_rate 1.2078594299760191e-05 --weight_decay 0. --warmup_steps 75 --lr_scheduler_type cosine_with_min_lr --lr_scheduler_kwargs {"min_lr_rate": 0.25} --tf32 True --gradient_checkpointing True --optim paged_adamw_8bit --use_liger True --packing True --disable_fa False --dataloader_pin_memory True --deepspeed ds_config/zero3.json --use_lora True
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] [2026-09-15 15:26:08,904] [INFO] [launch.py:155:main] 0 NV_LIBNCCL_PACKAGE_VERSION=2.25.1-1
[text-trainer] [2026-09-15 15:26:08,904] [INFO] [launch.py:155:main] 0 NV_LIBNCCL_DEV_PACKAGE_VERSION=2.25.1-1
[text-trainer] [2026-09-15 15:26:08,904] [INFO] [launch.py:155:main] 0 NV_LIBNCCL_PACKAGE_NAME=libnccl2
[text-trainer] [2026-09-15 15:26:08,904] [INFO] [launch.py:155:main] 0 NV_LIBNCCL_DEV_PACKAGE_NAME=libnccl-dev
[text-trainer] [2026-09-15 15:26:08,904] [INFO] [launch.py:155:main] 0 NV_LIBNCCL_PACKAGE=libnccl2=2.25.1-1+cuda12.8
[text-trainer] [2026-09-15 15:26:08,904] [INFO] [launch.py:155:main] 0 NV_LIBNCCL_DEV_PACKAGE=libnccl-dev=2.25.1-1+cuda12.8
[text-trainer] [2026-09-15 15:26:08,904] [INFO] [launch.py:155:main] 0 NCCL_VERSION=2.25.1-1
[text-trainer] [2026-09-15 15:26:08,904] [INFO] [launch.py:162:main] WORLD INFO DICT: {'localhost': [0, 1, 2, 3]}
[text-trainer] [2026-09-15 15:26:08,904] [INFO] [launch.py:168:main] nnodes=1, num_local_procs=4, node_rank=0
[text-trainer] [2026-09-15 15:26:08,904] [INFO] [launch.py:179:main] global_rank_mapping=defaultdict(<class 'list'>, {'localhost': [0, 1, 2, 3]})
[text-trainer] [2026-09-15 15:26:08,904] [INFO] [launch.py:180:main] dist_world_size=4
[text-trainer] [2026-09-15 15:26:08,904] [INFO] [launch.py:184:main] Setting CUDA_VISIBLE_DEVICES=0,1,2,3
[text-trainer] [2026-09-15 15:26:08,906] [INFO] [launch.py:272:main] process 921 spawned with command: ['/usr/bin/python', '-u', 'train_instruct.py', '--local_rank=0', '--request_path', 'datasets/training_request_24c8317e-07e4-4424-b996-b336dde5a580.json', '--bf16', 'True', '--report_to', 'wandb', '--output_dir', '/workspace/scripts/soutputs/24c8317e-07e4-4424-b996-b336dde5a580', '--num_train_epochs', '3', '--per_device_train_batch_size', '18', '--per_device_eval_batch_size', '1', '--gradient_accumulation_steps', '1', '--eval_accumulation_steps', '1', '--eval_strategy', 'no', '--save_strategy', 'epoch', '--logging_steps', '1', '--learning_rate', '1.2078594299760191e-05', '--weight_decay', '0.', '--warmup_steps', '75', '--lr_scheduler_type', 'cosine_with_min_lr', '--lr_scheduler_kwargs', '{"min_lr_rate": 0.25}', '--tf32', 'True', '--gradient_checkpointing', 'True', '--optim', 'paged_adamw_8bit', '--use_liger', 'True', '--packing', 'True', '--disable_fa', 'False', '--dataloader_pin_memory', 'True', '--deepspeed', 'ds_config/zero3.json', '--use_lora', 'True']
[text-trainer] [2026-09-15 15:26:08,908] [INFO] [launch.py:272:main] process 922 spawned with command: ['/usr/bin/python', '-u', 'train_instruct.py', '--local_rank=1', '--request_path', 'datasets/training_request_24c8317e-07e4-4424-b996-b336dde5a580.json', '--bf16', 'True', '--report_to', 'wandb', '--output_dir', '/workspace/scripts/soutputs/24c8317e-07e4-4424-b996-b336dde5a580', '--num_train_epochs', '3', '--per_device_train_batch_size', '18', '--per_device_eval_batch_size', '1', '--gradient_accumulation_steps', '1', '--eval_accumulation_steps', '1', '--eval_strategy', 'no', '--save_strategy', 'epoch', '--logging_steps', '1', '--learning_rate', '1.2078594299760191e-05', '--weight_decay', '0.', '--warmup_steps', '75', '--lr_scheduler_type', 'cosine_with_min_lr', '--lr_scheduler_kwargs', '{"min_lr_rate": 0.25}', '--tf32', 'True', '--gradient_checkpointing', 'True', '--optim', 'paged_adamw_8bit', '--use_liger', 'True', '--packing', 'True', '--disable_fa', 'False', '--dataloader_pin_memory', 'True', '--deepspeed', 'ds_config/zero3.json', '--use_lora', 'True']
[text-trainer] [2026-09-15 15:26:08,909] [INFO] [launch.py:272:main] process 923 spawned with command: ['/usr/bin/python', '-u', 'train_instruct.py', '--local_rank=2', '--request_path', 'datasets/training_request_24c8317e-07e4-4424-b996-b336dde5a580.json', '--bf16', 'True', '--report_to', 'wandb', '--output_dir', '/workspace/scripts/soutputs/24c8317e-07e4-4424-b996-b336dde5a580', '--num_train_epochs', '3', '--per_device_train_batch_size', '18', '--per_device_eval_batch_size', '1', '--gradient_accumulation_steps', '1', '--eval_accumulation_steps', '1', '--eval_strategy', 'no', '--save_strategy', 'epoch', '--logging_steps', '1', '--learning_rate', '1.2078594299760191e-05', '--weight_decay', '0.', '--warmup_steps', '75', '--lr_scheduler_type', 'cosine_with_min_lr', '--lr_scheduler_kwargs', '{"min_lr_rate": 0.25}', '--tf32', 'True', '--gradient_checkpointing', 'True', '--optim', 'paged_adamw_8bit', '--use_liger', 'True', '--packing', 'True', '--disable_fa', 'False', '--dataloader_pin_memory', 'True', '--deepspeed', 'ds_config/zero3.json', '--use_lora', 'True']
[text-trainer] [2026-09-15 15:26:08,910] [INFO] [launch.py:272:main] process 924 spawned with command: ['/usr/bin/python', '-u', 'train_instruct.py', '--local_rank=3', '--request_path', 'datasets/training_request_24c8317e-07e4-4424-b996-b336dde5a580.json', '--bf16', 'True', '--report_to', 'wandb', '--output_dir', '/workspace/scripts/soutputs/24c8317e-07e4-4424-b996-b336dde5a580', '--num_train_epochs', '3', '--per_device_train_batch_size', '18', '--per_device_eval_batch_size', '1', '--gradient_accumulation_steps', '1', '--eval_accumulation_steps', '1', '--eval_strategy', 'no', '--save_strategy', 'epoch', '--logging_steps', '1', '--learning_rate', '1.2078594299760191e-05', '--weight_decay', '0.', '--warmup_steps', '75', '--lr_scheduler_type', 'cosine_with_min_lr', '--lr_scheduler_kwargs', '{"min_lr_rate": 0.25}', '--tf32', 'True', '--gradient_checkpointing', 'True', '--optim', 'paged_adamw_8bit', '--use_liger', 'True', '--packing', 'True', '--disable_fa', 'False', '--dataloader_pin_memory', 'True', '--deepspeed', 'ds_config/zero3.json', '--use_lora', 'True']
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
[text-trainer] [W915 15:26:28.521137341 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W915 15:26:28.755546911 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W915 15:26:28.788739228 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W915 15:26:28.790893977 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W915 15:26:28.825948694 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W915 15:26:28.827640067 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W915 15:26:28.833519353 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W915 15:26:28.834463890 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W915 15:26:29.332131362 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] [W915 15:26:29.350411303 socket.cpp:200] [c10d] The hostname of the client socket cannot be retrieved. err=-3
[text-trainer] wandb: Tracking run with wandb version 0.19.10
[text-trainer] wandb: W&B syncing is set to `offline` in this directory. Run `wandb online` or set WANDB_MODE=online to enable cloud syncing.