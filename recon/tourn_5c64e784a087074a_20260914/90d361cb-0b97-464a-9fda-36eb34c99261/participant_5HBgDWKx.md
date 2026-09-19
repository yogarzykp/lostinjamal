# Loki — task 90d361cb-0b97-464a-9fda-36eb34c99261 — hotkey 5HBgDWKxNX3333Yit3qMokkYY4Guz1r8Qfons2UJTSU5oqjV
fetched 2026-09-19T05:12:40+00:00  lines=1401  hit_page_cap=False  containers=['downloader-90d361cb-0b97-464a-9fda-36eb34c99261-92ee71e1', 'fastapi', 'hf-upload-867ca272887f4d23b506afbaa8e50fbc', 'text-trainer-ac4c3195819d407f9330a4e203fc0816']

[downloader-9] Downloading datasets to: /cache/datasets
[downloader-9] Downloading models to: /cache/models
[downloader-9] Model already cached at /cache/models/a0971600276b8e78.
[downloader-9] Skipping download.
[downloader-9] Model path: /cache/models/a0971600276b8e78
[downloader-9] Dataset path: /cache/datasets
[fastapi] Repository cloned successfully
[fastapi] Running Cache Download Container
[fastapi] Starting downloader container: downloader-90d361cb-0b97-464a-9fda-36eb34c99261-92ee71e1
[fastapi] Download completed successfully for task 90d361cb-0b97-464a-9fda-36eb34c99261
[fastapi] Building Docker image 'standalone-text-trainer:8980d979-e20a-47c8-8181-9abbddbeb83d' (timeout=1800s)...
[fastapi] Step 1/14 : FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04
[fastapi] ---> ff5fe688608b
[fastapi] Step 2/14 : RUN apt-get update && apt-get install -y     vim     zip     tmux     iotop     nvtop     bmon     wget     nano     zsh     htop     redis-server     && rm -rf /var/lib/apt/lists/*
[fastapi] ---> Running in 99a1e8285708
[fastapi] Get:1 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  InRelease [1578 B]
[fastapi] Get:2 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  Packages [3009 kB]
[fastapi] Get:3 http://archive.ubuntu.com/ubuntu jammy InRelease [270 kB]
[fastapi] Get:4 http://security.ubuntu.com/ubuntu jammy-security InRelease [129 kB]
[fastapi] Get:5 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [128 kB]
[fastapi] Get:6 http://archive.ubuntu.com/ubuntu jammy-backports InRelease [127 kB]
[fastapi] Get:7 http://archive.ubuntu.com/ubuntu jammy/main amd64 Packages [1792 kB]
[fastapi] Get:8 http://archive.ubuntu.com/ubuntu jammy/restricted amd64 Packages [164 kB]
[fastapi] Get:9 http://archive.ubuntu.com/ubuntu jammy/multiverse amd64 Packages [266 kB]
[fastapi] Get:10 http://archive.ubuntu.com/ubuntu jammy/universe amd64 Packages [17.5 MB]
[fastapi] Get:11 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy InRelease [18.1 kB]
[fastapi] Get:12 http://security.ubuntu.com/ubuntu jammy-security/multiverse amd64 Packages [84.6 kB]
[fastapi] Get:13 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 Packages [1620 kB]
[fastapi] Get:14 http://archive.ubuntu.com/ubuntu jammy-updates/restricted amd64 Packages [8007 kB]
[fastapi] Get:15 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 Packages [4624 kB]
[fastapi] Get:16 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy/main amd64 Packages [44.3 kB]
[fastapi] Get:17 http://archive.ubuntu.com/ubuntu jammy-updates/multiverse amd64 Packages [93.2 kB]
[fastapi] Get:18 http://archive.ubuntu.com/ubuntu jammy-backports/universe amd64 Packages [35.6 kB]
[fastapi] Get:19 http://archive.ubuntu.com/ubuntu jammy-backports/main amd64 Packages [82.8 kB]
[fastapi] Get:20 http://security.ubuntu.com/ubuntu jammy-security/restricted amd64 Packages [7717 kB]
[fastapi] Get:21 http://security.ubuntu.com/ubuntu jammy-security/main amd64 Packages [4290 kB]
[fastapi] Get:22 http://security.ubuntu.com/ubuntu jammy-security/universe amd64 Packages [1317 kB]
[fastapi] Fetched 51.3 MB in 2s (20.9 MB/s)
[fastapi] Reading package lists...
[fastapi] Reading package lists...
[fastapi] Building dependency tree...
[fastapi] Reading state information...
[fastapi] The following additional packages will be installed:
[fastapi] libconfuse-common libconfuse2 libevent-core-2.1-7 libgpm2 libjemalloc2
[fastapi] liblua5.1-0 liblzf1 libnl-3-200 libnl-genl-3-200 libnl-route-3-200
[fastapi] libpython3.10 libpython3.10-minimal libpython3.10-stdlib libsodium23
[fastapi] libutempter0 lua-bitop lua-cjson python3.10 python3.10-minimal redis-tools
[fastapi] unzip vim-common vim-runtime xxd zsh-common
[fastapi] Suggested packages:
[fastapi] lm-sensors lsof strace gpm hunspell python3.10-venv python3.10-doc
[fastapi] binfmt-support ruby-redis ctags vim-doc vim-scripts zsh-doc
[fastapi] The following NEW packages will be installed:
[fastapi] bmon htop iotop libconfuse-common libconfuse2 libevent-core-2.1-7 libgpm2
[fastapi] libjemalloc2 liblua5.1-0 liblzf1 libnl-3-200 libnl-genl-3-200
[fastapi] libnl-route-3-200 libpython3.10 libsodium23 libutempter0 lua-bitop lua-cjson
[fastapi] nano nvtop redis-server redis-tools tmux unzip vim vim-common vim-runtime
[fastapi] xxd zip zsh zsh-common
[fastapi] The following packages will be upgraded:
[fastapi] libpython3.10-minimal libpython3.10-stdlib python3.10 python3.10-minimal
[fastapi] wget
[fastapi] 5 upgraded, 31 newly installed, 0 to remove and 170 not upgraded.
[fastapi] Need to get 24.4 MB of archives.
[fastapi] After this operation, 73.5 MB of additional disk space will be used.
[fastapi] Get:1 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 python3.10 amd64 3.10.12-1~22.04.18 [508 kB]
[fastapi] Get:2 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libpython3.10-stdlib amd64 3.10.12-1~22.04.18 [1850 kB]
[fastapi] Get:3 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 python3.10-minimal amd64 3.10.12-1~22.04.18 [2277 kB]
[fastapi] Get:4 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libpython3.10-minimal amd64 3.10.12-1~22.04.18 [817 kB]
[fastapi] Get:5 http://archive.ubuntu.com/ubuntu jammy/universe amd64 libjemalloc2 amd64 5.2.1-4ubuntu1 [240 kB]
[fastapi] Get:6 http://archive.ubuntu.com/ubuntu jammy/universe amd64 liblua5.1-0 amd64 5.1.5-8.1build4 [99.9 kB]
[fastapi] Get:7 http://archive.ubuntu.com/ubuntu jammy/universe amd64 liblzf1 amd64 3.6-3 [7444 B]
[fastapi] Get:8 http://archive.ubuntu.com/ubuntu jammy/universe amd64 lua-bitop amd64 1.0.2-5 [6680 B]
[fastapi] Get:9 http://archive.ubuntu.com/ubuntu jammy/universe amd64 lua-cjson amd64 2.1.0+dfsg-2.1 [17.4 kB]
[fastapi] Get:10 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 redis-tools amd64 5:6.0.16-1ubuntu1.1 [856 kB]
[fastapi] Get:11 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 redis-server amd64 5:6.0.16-1ubuntu1.1 [45.9 kB]
[fastapi] Get:12 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 xxd amd64 2:8.2.3995-1ubuntu2.36 [51.5 kB]
[fastapi] Get:13 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 vim-common all 2:8.2.3995-1ubuntu2.36 [81.5 kB]
[fastapi] Get:14 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 nano amd64 6.2-1ubuntu0.2 [280 kB]
[fastapi] Get:15 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 wget amd64 1.21.2-2ubuntu1.5 [339 kB]
[fastapi] Get:16 http://archive.ubuntu.com/ubuntu jammy/universe amd64 libconfuse-common all 3.3-2 [6004 B]
[fastapi] Get:17 http://archive.ubuntu.com/ubuntu jammy/universe amd64 libconfuse2 amd64 3.3-2 [26.0 kB]
[fastapi] Get:18 http://archive.ubuntu.com/ubuntu jammy/main amd64 libnl-3-200 amd64 3.5.0-0.1 [59.1 kB]
[fastapi] Get:19 http://archive.ubuntu.com/ubuntu jammy/main amd64 libnl-route-3-200 amd64 3.5.0-0.1 [180 kB]
[fastapi] Get:20 http://archive.ubuntu.com/ubuntu jammy/universe amd64 bmon amd64 1:4.0-8 [48.1 kB]
[fastapi] Get:21 http://archive.ubuntu.com/ubuntu jammy/main amd64 libnl-genl-3-200 amd64 3.5.0-0.1 [12.4 kB]
[fastapi] Get:22 http://archive.ubuntu.com/ubuntu jammy/main amd64 htop amd64 3.0.5-7build2 [128 kB]
[fastapi] Get:23 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 iotop amd64 0.6-24-g733f3f8-1.1ubuntu0.1 [23.1 kB]
[fastapi] Get:24 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libevent-core-2.1-7 amd64 2.1.12-stable-1ubuntu0.1 [94.2 kB]
[fastapi] Get:25 http://archive.ubuntu.com/ubuntu jammy/main amd64 libgpm2 amd64 1.20.7-10build1 [15.3 kB]
[fastapi] Get:26 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libpython3.10 amd64 3.10.12-1~22.04.18 [1950 kB]
[fastapi] Get:27 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libsodium23 amd64 1.0.18-1ubuntu0.22.04.1 [164 kB]
[fastapi] Get:28 http://archive.ubuntu.com/ubuntu jammy/main amd64 libutempter0 amd64 1.2.1-2build2 [8848 B]
[fastapi] Get:29 http://archive.ubuntu.com/ubuntu jammy/multiverse amd64 nvtop amd64 1.2.2-1 [43.9 kB]
[fastapi] Get:30 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 tmux amd64 3.2a-4ubuntu0.2 [428 kB]
[fastapi] Get:31 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 unzip amd64 6.0-26ubuntu3.2 [175 kB]
[fastapi] Get:32 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 vim-runtime all 2:8.2.3995-1ubuntu2.36 [6824 kB]
[fastapi] Get:33 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 vim amd64 2:8.2.3995-1ubuntu2.36 [1733 kB]
[fastapi] Get:34 http://archive.ubuntu.com/ubuntu jammy/main amd64 zip amd64 3.0-12build2 [176 kB]
[fastapi] Get:35 http://archive.ubuntu.com/ubuntu jammy/main amd64 zsh-common all 5.8.1-1 [3985 kB]
[fastapi] Get:36 http://archive.ubuntu.com/ubuntu jammy/main amd64 zsh amd64 5.8.1-1 [809 kB]
[fastapi] [91mdebconf: delaying package configuration, since apt-utils is not installed
[fastapi] [0mFetched 24.4 MB in 1s (28.9 MB/s)
[fastapi] (Reading database ... (Reading database ... 5%(Reading database ... 10%(Reading database ... 15%(Reading database ... 20%(Reading database ... 25%(Reading database ... 30%(Reading database ... 35%(Reading database ... 40%(Reading database ... 45%(Reading database ... 50%(Reading database ... 55%(Reading database ... 60%(Reading database ... 65%(Reading database ... 70%(Reading database ... 75%(Reading database ... 80%(Reading database ... 85%(Reading database ... 90%(Reading database ... 95%(Reading database ... 100%(Reading database ... 24135 files and directories currently installed.)
[fastapi] Preparing to unpack .../00-python3.10_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking python3.10 (3.10.12-1~22.04.18) over (3.10.12-1~22.04.6) ...
[fastapi] Preparing to unpack .../01-libpython3.10-stdlib_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking libpython3.10-stdlib:amd64 (3.10.12-1~22.04.18) over (3.10.12-1~22.04.6) ...
[fastapi] Preparing to unpack .../02-python3.10-minimal_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking python3.10-minimal (3.10.12-1~22.04.18) over (3.10.12-1~22.04.6) ...
[fastapi] Preparing to unpack .../03-libpython3.10-minimal_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking libpython3.10-minimal:amd64 (3.10.12-1~22.04.18) over (3.10.12-1~22.04.6) ...
[fastapi] Selecting previously unselected package libjemalloc2:amd64.
[fastapi] Preparing to unpack .../04-libjemalloc2_5.2.1-4ubuntu1_amd64.deb ...
[fastapi] Unpacking libjemalloc2:amd64 (5.2.1-4ubuntu1) ...
[fastapi] Selecting previously unselected package liblua5.1-0:amd64.
[fastapi] Preparing to unpack .../05-liblua5.1-0_5.1.5-8.1build4_amd64.deb ...
[fastapi] Unpacking liblua5.1-0:amd64 (5.1.5-8.1build4) ...
[fastapi] Selecting previously unselected package liblzf1:amd64.
[fastapi] Preparing to unpack .../06-liblzf1_3.6-3_amd64.deb ...
[fastapi] Unpacking liblzf1:amd64 (3.6-3) ...
[fastapi] Selecting previously unselected package lua-bitop:amd64.
[fastapi] Preparing to unpack .../07-lua-bitop_1.0.2-5_amd64.deb ...
[fastapi] Unpacking lua-bitop:amd64 (1.0.2-5) ...
[fastapi] Selecting previously unselected package lua-cjson:amd64.
[fastapi] Preparing to unpack .../08-lua-cjson_2.1.0+dfsg-2.1_amd64.deb ...
[fastapi] Unpacking lua-cjson:amd64 (2.1.0+dfsg-2.1) ...
[fastapi] Selecting previously unselected package redis-tools.
[fastapi] Preparing to unpack .../09-redis-tools_5%3a6.0.16-1ubuntu1.1_amd64.deb ...
[fastapi] Unpacking redis-tools (5:6.0.16-1ubuntu1.1) ...
[fastapi] Selecting previously unselected package redis-server.
[fastapi] Preparing to unpack .../10-redis-server_5%3a6.0.16-1ubuntu1.1_amd64.deb ...
[fastapi] Unpacking redis-server (5:6.0.16-1ubuntu1.1) ...
[fastapi] Selecting previously unselected package xxd.
[fastapi] Preparing to unpack .../11-xxd_2%3a8.2.3995-1ubuntu2.36_amd64.deb ...
[fastapi] Unpacking xxd (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Selecting previously unselected package vim-common.
[fastapi] Preparing to unpack .../12-vim-common_2%3a8.2.3995-1ubuntu2.36_all.deb ...
[fastapi] Unpacking vim-common (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Selecting previously unselected package nano.
[fastapi] Preparing to unpack .../13-nano_6.2-1ubuntu0.2_amd64.deb ...
[fastapi] Unpacking nano (6.2-1ubuntu0.2) ...
[fastapi] Preparing to unpack .../14-wget_1.21.2-2ubuntu1.5_amd64.deb ...
[fastapi] Unpacking wget (1.21.2-2ubuntu1.5) over (1.21.2-2ubuntu1.1) ...
[fastapi] Selecting previously unselected package libconfuse-common.
[fastapi] Preparing to unpack .../15-libconfuse-common_3.3-2_all.deb ...
[fastapi] Unpacking libconfuse-common (3.3-2) ...
[fastapi] Selecting previously unselected package libconfuse2:amd64.
[fastapi] Preparing to unpack .../16-libconfuse2_3.3-2_amd64.deb ...
[fastapi] Unpacking libconfuse2:amd64 (3.3-2) ...
[fastapi] Selecting previously unselected package libnl-3-200:amd64.
[fastapi] Preparing to unpack .../17-libnl-3-200_3.5.0-0.1_amd64.deb ...
[fastapi] Unpacking libnl-3-200:amd64 (3.5.0-0.1) ...
[fastapi] Selecting previously unselected package libnl-route-3-200:amd64.
[fastapi] Preparing to unpack .../18-libnl-route-3-200_3.5.0-0.1_amd64.deb ...
[fastapi] Unpacking libnl-route-3-200:amd64 (3.5.0-0.1) ...
[fastapi] Selecting previously unselected package bmon.
[fastapi] Preparing to unpack .../19-bmon_1%3a4.0-8_amd64.deb ...
[fastapi] Unpacking bmon (1:4.0-8) ...
[fastapi] Selecting previously unselected package libnl-genl-3-200:amd64.
[fastapi] Preparing to unpack .../20-libnl-genl-3-200_3.5.0-0.1_amd64.deb ...
[fastapi] Unpacking libnl-genl-3-200:amd64 (3.5.0-0.1) ...
[fastapi] Selecting previously unselected package htop.
[fastapi] Preparing to unpack .../21-htop_3.0.5-7build2_amd64.deb ...
[fastapi] Unpacking htop (3.0.5-7build2) ...
[fastapi] Selecting previously unselected package iotop.
[fastapi] Preparing to unpack .../22-iotop_0.6-24-g733f3f8-1.1ubuntu0.1_amd64.deb ...
[fastapi] Unpacking iotop (0.6-24-g733f3f8-1.1ubuntu0.1) ...
[fastapi] Selecting previously unselected package libevent-core-2.1-7:amd64.
[fastapi] Preparing to unpack .../23-libevent-core-2.1-7_2.1.12-stable-1ubuntu0.1_amd64.deb ...
[fastapi] Unpacking libevent-core-2.1-7:amd64 (2.1.12-stable-1ubuntu0.1) ...
[fastapi] Selecting previously unselected package libgpm2:amd64.
[fastapi] Preparing to unpack .../24-libgpm2_1.20.7-10build1_amd64.deb ...
[fastapi] Unpacking libgpm2:amd64 (1.20.7-10build1) ...
[fastapi] Selecting previously unselected package libpython3.10:amd64.
[fastapi] Preparing to unpack .../25-libpython3.10_3.10.12-1~22.04.18_amd64.deb ...
[fastapi] Unpacking libpython3.10:amd64 (3.10.12-1~22.04.18) ...
[fastapi] Selecting previously unselected package libsodium23:amd64.
[fastapi] Preparing to unpack .../26-libsodium23_1.0.18-1ubuntu0.22.04.1_amd64.deb ...
[fastapi] Unpacking libsodium23:amd64 (1.0.18-1ubuntu0.22.04.1) ...
[fastapi] Selecting previously unselected package libutempter0:amd64.
[fastapi] Preparing to unpack .../27-libutempter0_1.2.1-2build2_amd64.deb ...
[fastapi] Unpacking libutempter0:amd64 (1.2.1-2build2) ...
[fastapi] Selecting previously unselected package nvtop.
[fastapi] Preparing to unpack .../28-nvtop_1.2.2-1_amd64.deb ...
[fastapi] Unpacking nvtop (1.2.2-1) ...
[fastapi] Selecting previously unselected package tmux.
[fastapi] Preparing to unpack .../29-tmux_3.2a-4ubuntu0.2_amd64.deb ...
[fastapi] Unpacking tmux (3.2a-4ubuntu0.2) ...
[fastapi] Selecting previously unselected package unzip.
[fastapi] Preparing to unpack .../30-unzip_6.0-26ubuntu3.2_amd64.deb ...
[fastapi] Unpacking unzip (6.0-26ubuntu3.2) ...
[fastapi] Selecting previously unselected package vim-runtime.
[fastapi] Preparing to unpack .../31-vim-runtime_2%3a8.2.3995-1ubuntu2.36_all.deb ...
[fastapi] Adding 'diversion of /usr/share/vim/vim82/doc/help.txt to /usr/share/vim/vim82/doc/help.txt.vim-tiny by vim-runtime'
[fastapi] Adding 'diversion of /usr/share/vim/vim82/doc/tags to /usr/share/vim/vim82/doc/tags.vim-tiny by vim-runtime'
[fastapi] Unpacking vim-runtime (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Selecting previously unselected package vim.
[fastapi] Preparing to unpack .../32-vim_2%3a8.2.3995-1ubuntu2.36_amd64.deb ...
[fastapi] Unpacking vim (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Selecting previously unselected package zip.
[fastapi] Preparing to unpack .../33-zip_3.0-12build2_amd64.deb ...
[fastapi] Unpacking zip (3.0-12build2) ...
[fastapi] Selecting previously unselected package zsh-common.
[fastapi] Preparing to unpack .../34-zsh-common_5.8.1-1_all.deb ...
[fastapi] Unpacking zsh-common (5.8.1-1) ...
[fastapi] Selecting previously unselected package zsh.
[fastapi] Preparing to unpack .../35-zsh_5.8.1-1_amd64.deb ...
[fastapi] Unpacking zsh (5.8.1-1) ...
[fastapi] Setting up nvtop (1.2.2-1) ...
[fastapi] Setting up libsodium23:amd64 (1.0.18-1ubuntu0.22.04.1) ...
[fastapi] Setting up libgpm2:amd64 (1.20.7-10build1) ...
[fastapi] Setting up wget (1.21.2-2ubuntu1.5) ...
[fastapi] Setting up zsh-common (5.8.1-1) ...
[fastapi] Setting up unzip (6.0-26ubuntu3.2) ...
[fastapi] Setting up libjemalloc2:amd64 (5.2.1-4ubuntu1) ...
[fastapi] Setting up xxd (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Setting up zip (3.0-12build2) ...
[fastapi] Setting up iotop (0.6-24-g733f3f8-1.1ubuntu0.1) ...
[fastapi] update-alternatives: using /usr/sbin/iotop-py to provide /usr/sbin/iotop (iotop) in auto mode
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/man8/iotop.8.gz because associated file /usr/share/man/man8/iotop-py.8.gz (of link group iotop) doesn't exist
[fastapi] Setting up vim-common (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Setting up lua-cjson:amd64 (2.1.0+dfsg-2.1) ...
[fastapi] Setting up liblzf1:amd64 (3.6-3) ...
[fastapi] Setting up libevent-core-2.1-7:amd64 (2.1.12-stable-1ubuntu0.1) ...
[fastapi] Setting up libpython3.10-minimal:amd64 (3.10.12-1~22.04.18) ...
[fastapi] Setting up lua-bitop:amd64 (1.0.2-5) ...
[fastapi] Setting up libutempter0:amd64 (1.2.1-2build2) ...
[fastapi] Setting up nano (6.2-1ubuntu0.2) ...
[fastapi] update-alternatives: using /bin/nano to provide /usr/bin/editor (editor) in auto mode
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/man1/editor.1.gz because associated file /usr/share/man/man1/nano.1.gz (of link group editor) doesn't exist
[fastapi] update-alternatives: using /bin/nano to provide /usr/bin/pico (pico) in auto mode
[fastapi] update-alternatives: warning: skip creation of /usr/share/man/man1/pico.1.gz because associated file /usr/share/man/man1/nano.1.gz (of link group pico) doesn't exist
[fastapi] Setting up libconfuse-common (3.3-2) ...
[fastapi] Setting up liblua5.1-0:amd64 (5.1.5-8.1build4) ...
[fastapi] Setting up libnl-3-200:amd64 (3.5.0-0.1) ...
[fastapi] Setting up zsh (5.8.1-1) ...
[fastapi] Setting up vim-runtime (2:8.2.3995-1ubuntu2.36) ...
[fastapi] Setting up libconfuse2:amd64 (3.3-2) ...
[fastapi] Setting up tmux (3.2a-4ubuntu0.2) ...
[fastapi] Setting up python3.10-minimal (3.10.12-1~22.04.18) ...
[fastapi] Setting up libnl-route-3-200:amd64 (3.5.0-0.1) ...
[fastapi] Setting up libpython3.10-stdlib:amd64 (3.10.12-1~22.04.18) ...
[fastapi] Setting up bmon (1:4.0-8) ...
[fastapi] Setting up redis-tools (5:6.0.16-1ubuntu1.1) ...
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
[fastapi] Setting up redis-server (5:6.0.16-1ubuntu1.1) ...
[fastapi] invoke-rc.d: could not determine current runlevel
[fastapi] invoke-rc.d: policy-rc.d denied execution of start.
[fastapi] Created symlink /etc/systemd/system/redis.service → /lib/systemd/system/redis-server.service.
[fastapi] Created symlink /etc/systemd/system/multi-user.target.wants/redis-server.service → /lib/systemd/system/redis-server.service.
[fastapi] Processing triggers for libc-bin (2.35-0ubuntu3.8) ...
[fastapi] Processing triggers for mailcap (3.70+nmu1ubuntu1) ...
[fastapi] ---> e7e81180aaf0
[fastapi] Step 3/14 : RUN mkdir -p /workspace
[fastapi] ---> Running in 78083cad35a4
[fastapi] ---> 028a58b27c42
[fastapi] Step 4/14 : RUN mkdir -p /cache
[fastapi] ---> Running in 49d784b3f196
[fastapi] ---> e5da8a31e027
[fastapi] Step 5/14 : RUN mkdir -p /workspace/scripts/datasets
[fastapi] ---> Running in f7e7e0ed79fd
[fastapi] ---> fbf62ffc62e2
[fastapi] Step 6/14 : RUN mkdir -p /app/checkpoints
[fastapi] ---> Running in b043577b2009
[fastapi] ---> df44c4a1ba70
[fastapi] Step 7/14 : WORKDIR /workspace/scripts
[fastapi] ---> Running in 6b4204f3eb8e
[fastapi] ---> 5e241b237cb9
[fastapi] Step 8/14 : COPY scripts /workspace/scripts
[fastapi] ---> 1e138877eb24
[fastapi] Step 9/14 : RUN chmod +x /workspace/scripts/entrypoint.sh
[fastapi] ---> Running in 12ca8abcb0c9
[fastapi] ---> 08382ba5fddf
[fastapi] Step 10/14 : RUN python -m venv /workspace/axo_py
[fastapi] ---> Running in 3526277a74c8
[fastapi] ---> 897a67378625
[fastapi] Step 11/14 : RUN bash -c "source /workspace/axo_py/bin/activate &&     pip install uv &&     pip install -U packaging==23.2 setuptools==75.8.0 wheel ninja &&     uv pip install --no-build-isolation axolotl==0.9.1 transformers==4.51.3 &&     pip install requests==2.32.3 &&     deactivate"
[fastapi] ---> Running in 55a33ff100e6
[fastapi] Collecting uv
[fastapi] Downloading uv-0.12.14-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] Downloading uv-0.12.14-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.0 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 20.0/20.0 MB 58.1 MB/s eta 0:00:00
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
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 51.4 MB/s eta 0:00:00
[fastapi] Downloading wheel-0.45.1-py3-none-any.whl (72 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 72.5/72.5 kB 19.0 MB/s eta 0:00:00
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (183 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 183.4/183.4 kB 55.8 MB/s eta 0:00:00
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
[fastapi] [0m[91mResolved 217 packages in 1.33s
[fastapi] [0m[91mDownloading networkx (2.0MiB)
[fastapi] [0m[91mDownloading pydantic-core (1.9MiB)
[fastapi] [0m[91mDownloading cryptography (4.5MiB)
[fastapi] [0m[91mDownloading pygments (1.2MiB)
[fastapi] [0m[91mDownloading botocore (13.7MiB)
[fastapi] [0m[91mDownloading pillow (6.3MiB)
[fastapi] [0m[91mDownloading torchao (5.4MiB)
[fastapi] [0m[91mDownloading wandb (24.9MiB)
[fastapi] [0m[91mDownloading hf-transfer (3.4MiB)
[fastapi] [0m[91mDownloading pandas (12.2MiB)
[fastapi] [0m[91mDownloading torch (731.2MiB)
[fastapi] [0m[91mDownloading hf-xet (51.1MiB)
[fastapi] [0m[91mDownloading bitsandbytes (72.5MiB)
[fastapi] [0m[91mDownloading aiohttp (1.7MiB)
[fastapi] [0m[91mDownloading pyarrow (47.7MiB)
[fastapi] [0m[91mDownloading zstandard (5.2MiB)
[fastapi] [0m[91mDownloading sentencepiece (1.3MiB)
[fastapi] [0m[91mDownloading numpy (18.6MiB)
[fastapi] [0m[91mDownloading tensorboard (5.3MiB)
[fastapi] [0m[91mDownloading scikit-learn (11.6MiB)
[fastapi] [0m[91mDownloading nvidia-cublas-cu12 (346.6MiB)
[fastapi] [0m[91mDownloading tensorboard-data-server (6.3MiB)
[fastapi] [0m[91mDownloading lm-eval (2.4MiB)
[fastapi] [0m[91mDownloading numba (3.6MiB)
[fastapi] [0m[91mDownloading nvidia-curand-cu12 (53.7MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-cupti-cu12 (13.2MiB)
[fastapi] [0m[91mDownloading transformers (9.9MiB)
[fastapi] [0m[91mDownloading nvidia-cusparselt-cu12 (143.1MiB)
[fastapi] [0m[91mDownloading tokenizers (3.0MiB)
[fastapi] [0m[91mDownloading gradio (44.3MiB)
[fastapi] [0m[91mDownloading nltk (1.7MiB)
[fastapi] [0m[91mDownloading nvidia-nvjitlink-cu12 (20.1MiB)
[fastapi] [0m[91mDownloading ruff (9.9MiB)
[fastapi] [0m[91mDownloading llvmlite (57.1MiB)
[fastapi] [0m[91mDownloading sympy (5.9MiB)
[fastapi] [0m[91mDownloading triton (241.4MiB)
[fastapi] [0m[91mDownloading nvidia-cufft-cu12 (201.7MiB)
[fastapi] [0m[91mDownloading nvidia-nccl-cu12 (179.9MiB)
[fastapi] [0m[91mDownloading grpcio (6.9MiB)
[fastapi] [0m[91mDownloading nvidia-cusolver-cu12 (122.0MiB)
[fastapi] [0m[91mDownloading scipy (33.7MiB)
[fastapi] [0m[91mDownloading lxml (5.0MiB)
[fastapi] [0m[91mDownloading nvidia-cusparse-cu12 (197.8MiB)
[fastapi] [0m[91mDownloading nvidia-cudnn-cu12 (634.0MiB)
[fastapi] [0m[91mDownloading xformers (42.2MiB)
[fastapi] [0m[91mDownloading oci (35.1MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-nvrtc-cu12 (23.5MiB)
[fastapi] [0m[91m Downloaded pygments
[fastapi] [0m[91m   Building langdetect==1.0.9
[fastapi] [0m[91m Downloaded sentencepiece
[fastapi] [0m[91m Downloaded aiohttp
[fastapi] [0m[91m Downloaded networkx
[fastapi] [0m[91m Downloaded nltk
[fastapi] [0m[91m Downloaded pydantic-core
[fastapi] [0m[91m Downloaded lm-eval
[fastapi] [0m[91m   Building axolotl==0.9.1
[fastapi] [0m[91m   Building axolotl-contribs-mit==0.0.3
[fastapi] [0m[91m   Building word2number==1.1
[fastapi] [0m[91m   Building axolotl-contribs-lgpl==0.0.6
[fastapi] [0m[91m   Building rouge-score==0.1.2
[fastapi] [0m[91m   Building sqlitedict==2.1.0
[fastapi] [0m[91m Downloaded tokenizers
[fastapi] [0m[91m   Building grpclib==0.4.7
[fastapi] [0m[91m   Building hqq==0.2.5
[fastapi] [0m[91m Downloaded hf-transfer
[fastapi] [0m[91m Downloaded numba
[fastapi] [0m[91m      Built word2number==1.1
[fastapi] [0m[91m      Built axolotl-contribs-mit==0.0.3
[fastapi] [0m[91m      Built langdetect==1.0.9
[fastapi] [0m[91m      Built rouge-score==0.1.2
[fastapi] [0m[91m      Built axolotl-contribs-lgpl==0.0.6
[fastapi] [0m[91m      Built sqlitedict==2.1.0
[fastapi] [0m[91m      Built grpclib==0.4.7
[fastapi] [0m[91m Downloaded cryptography
[fastapi] [0m[91m      Built axolotl==0.9.1
[fastapi] [0m[91m Downloaded lxml
[fastapi] [0m[91m Downloaded zstandard
[fastapi] [0m[91m Downloaded torchao
[fastapi] [0m[91m Downloaded tensorboard
[fastapi] [0m[91m Downloaded sympy
[fastapi] [0m[91m Downloaded pillow
[fastapi] [0m[91m Downloaded tensorboard-data-server
[fastapi] [0m[91m      Built hqq==0.2.5
[fastapi] [0m[91m Downloaded grpcio
[fastapi] [0m[91m Downloaded transformers
[fastapi] [0m[91m Downloaded ruff
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
[fastapi] [0m[91m Downloaded torch
[fastapi] [0m[91m Downloaded nvidia-cudnn-cu12
[fastapi] [0m[91mPrepared 215 packages in 12.12s
[fastapi] [0m[91mInstalled 215 packages in 401ms
[fastapi] [0m[91m + absl-py==2.5.0
[fastapi] + accelerate==1.6.0
[fastapi] + addict==2.4.0
[fastapi] + adlfs==2026.8.0
[fastapi] + aiobotocore==2.26.0
[fastapi] + aiofiles[0m[91m==23.2.1
[fastapi] + aiohappyeyeballs==2.7.1
[fastapi] + aiohttp==3.14[0m[91m.3
[fastapi] +[0m[91m aioitertools==0.13.0
[fastapi] + aiosignal==1.4.0
[fastapi] + annotated-doc==0.0.5
[fastapi] [0m[91m+ annotated-types==0.8.0
[fastapi] + antlr4-python3-runtime==4.13.2
[fastapi] + [0m[91manyio==4.15[0m[91m.1
[fastapi] + [0m[91mart==6.5[0m[91m
[fastapi] + [0m[91mattrs==26.1[0m[91m.0
[fastapi] +[0m[91m autoawq==0.2.7[0m[91m.post3
[fastapi] + axolotl==0.9.1
[fastapi] [0m[91m + [0m[91maxolotl-contribs-lgpl==0[0m[91m.0.6
[fastapi] [0m[91m + axolotl-contribs-mit[0m[91m==0.0.3
[fastapi] + azure-core[0m[91m==1.41.0[0m[91m
[fastapi] + azure-identity==1[0m[91m.25.3[0m[91m
[fastapi] + azure-storage-blob==12.30.1[0m[91m
[fastapi] + bitsandbytes==0.45.4[0m[91m
[fastapi] + [0m[91mbotocore==1.[0m[91m41.5
[fastapi] +[0m[91m certifi==2026[0m[91m.7.22
[fastapi] [0m[91m+ cffi[0m[91m==2.[0m[91m1.1
[fastapi] [0m[91m + chardet[0m[91m==6.0.0.post1
[fastapi] + charset-normalizer==3.5[0m[91m.1
[fastapi] + circuitbreaker[0m[91m==2.1.[0m[91m3
[fastapi] + click==8.5.0
[fastapi] [0m[91m+ cloudpickle==3.1.[0m[91m2
[fastapi] +[0m[91m colorama==0.4[0m[91m.6
[fastapi] + coloredlogs[0m[91m==15.0.[0m[91m1
[fastapi] + crc32c[0m[91m==2.8
[fastapi] + cryptography==50.0.1[0m[91m
[fastapi] + dataproperty==1[0m[91m.1.1[0m[91m
[fastapi] + datasets==3[0m[91m.5.1
[fastapi] + [0m[91mdecorator==5.3.1[0m[91m
[fastapi] + defusedxml[0m[91m==0.7.[0m[91m1
[fastapi] + [0m[91mdill==0.3[0m[91m.8
[fastapi] +[0m[91m einops==0.[0m[91m8.2
[fastapi] [0m[91m+ evaluate==0.4.[0m[91m1
[fastapi] + [0m[91mfastapi[0m[91m==0.[0m[91m141.1[0m[91m
[fastapi] [0m[91m+[0m[91m fastcore[0m[91m==2.2.[0m[91m27
[fastapi] + ffmpy==1.0[0m[91m.0
[fastapi] [0m[91m+ [0m[91mfilelock==[0m[91m3.[0m[91m32.6
[fastapi] [0m[91m+ fire==0.7.1
[fastapi] + frozenlist==1[0m[91m.8.0
[fastapi] + fsspec[0m[91m==2025.3.0[0m[91m
[fastapi] [0m[91m+[0m[91m gcsfs==2025.3.0
[fastapi] +[0m[91m google-api-core[0m[91m==2.33.0[0m[91m
[fastapi] [0m[91m + google-auth[0m[91m==2.58.0
[fastapi] [0m[91m+ google-auth-oauthlib==[0m[91m1.4.1[0m[91m
[fastapi] + google-cloud-core==[0m[91m2.7.0
[fastapi] + google-cloud-storage[0m[91m==3.14.1[0m[91m
[fastapi] + google-crc32c[0m[91m==1[0m[91m.8.0[0m[91m
[fastapi] + [0m[91mgoogle-resumable-media==[0m[91m2.10.[0m[91m2
[fastapi] [0m[91m+[0m[91m googleapis-common-protos[0m[91m==1.[0m[91m75.0[0m[91m
[fastapi] [0m[91m+ gradio[0m[91m==5.23.3[0m[91m
[fastapi] + gradio-client==1.8.0
[fastapi] + [0m[91mgroovy==0.1.2
[fastapi] +[0m[91m grpcio[0m[91m==1.84[0m[91m.0
[fastapi] [0m[91m +[0m[91m grpclib[0m[91m==0.[0m[91m4.7
[fastapi] + h11==0.16.0
[fastapi] [0m[91m + h2==4.4[0m[91m.1
[fastapi] [0m[91m +[0m[91m hf-transfer[0m[91m==0.1.9
[fastapi] + [0m[91mhf-xet==1[0m[91m.1.[0m[91m0[0m[91m
[fastapi] + [0m[91mhpack==4.[0m[91m2.0[0m[91m
[fastapi] +[0m[91m [0m[91mhqq==0.[0m[91m2[0m[91m.5
[fastapi] [0m[91m+ [0m[91mhttpcore==1.0.9
[fastapi] [0m[91m+ httpx==0[0m[91m.28.1
[fastapi] [0m[91m [0m[91m+ huggingface-hub[0m[91m==0[0m[91m.31[0m[91m.0[0m[91m
[fastapi] [0m[91m+ humanfriendly[0m[91m==[0m[91m10.0
[fastapi] [0m[91m [0m[91m+ hyperframe[0m[91m==[0m[91m6.1[0m[91m.0
[fastapi] [0m[91m+[0m[91m idna[0m[91m==3.[0m[91m19
[fastapi] + immutabledict==4.2.0
[fastapi] + [0m[91misodate==0.7.2
[fastapi] [0m[91m + [0m[91mjinja2[0m[91m==3[0m[91m.1.6
[fastapi] + jmespath[0m[91m==1.1.0
[fastapi] [0m[91m+ joblib[0m[91m==[0m[91m1.6[0m[91m.0
[fastapi] [0m[91m+ jsonlines[0m[91m==4.0.0
[fastapi] + langdetect==1.[0m[91m0.9
[fastapi] + liger-kernel==0.5[0m[91m.9
[fastapi] [0m[91m+ llvmlite[0m[91m==0.49.0
[fastapi] + lm-eval[0m[91m==0.[0m[91m4.7[0m[91m
[fastapi] [0m[91m+ lxml[0m[91m==6.1.[0m[91m3
[fastapi] [0m[91m +[0m[91m markdown[0m[91m==3[0m[91m.10.3[0m[91m
[fastapi] [0m[91m +[0m[91m markdown-it-py[0m[91m==[0m[91m4.2.0[0m[91m
[fastapi] + markupsafe==3.0.[0m[91m3
[fastapi] + mbstrdecoder==1[0m[91m.1.5
[fastapi] + [0m[91mmdurl==0.1[0m[91m.2
[fastapi] +[0m[91m modal==0[0m[91m.70.5
[fastapi] [0m[91m+ more-itertools==[0m[91m11.1.0[0m[91m
[fastapi] + mpmath[0m[91m==1.3.[0m[91m0
[fastapi] +[0m[91m msal==1[0m[91m.38.0
[fastapi] [0m[91m + msal-extensions==1.[0m[91m3.[0m[91m1
[fastapi] [0m[91m+ [0m[91mmultidict==6.8.0
[fastapi] + multiprocess==0.70[0m[91m.16
[fastapi] + networkx==3.[0m[91m6.1
[fastapi] [0m[91m + nltk==3.10.3
[fastapi] [0m[91m+ numba==0.67.0
[fastapi] [0m[91m+ numexpr[0m[91m==2.14[0m[91m.2
[fastapi] [0m[91m+ numpy[0m[91m==2.[0m[91m0[0m[91m.1
[fastapi] [0m[91m + nvidia-cublas-cu12[0m[91m==12.[0m[91m4.5[0m[91m.8
[fastapi] [0m[91m + nvidia-cuda-cupti-cu12==12.4.127
[fastapi] + nvidia-cuda-nvrtc-cu12==12.4.127
[fastapi] + nvidia-cuda-runtime-cu12==12.4.127
[fastapi] [0m[91m+ nvidia-cudnn-cu12==9.1.0.70
[fastapi] + nvidia-cufft-cu12==11.2[0m[91m.1.3
[fastapi] [0m[91m + nvidia-curand-cu12==10.3.5.147
[fastapi] [0m[91m+ nvidia-cusolver-cu12==11.6.1.9
[fastapi] [0m[91m + [0m[91mnvidia-cusparse-cu12[0m[91m==12.3.1.170
[fastapi] + nvidia-cusparselt-cu12==0[0m[91m.6.2
[fastapi] +[0m[91m nvidia-ml-py==12.560.[0m[91m30
[fastapi] + nvidia-nccl-cu12[0m[91m==2.21.[0m[91m5
[fastapi] +[0m[91m nvidia-nvjitlink-cu12==12[0m[91m.4.127
[fastapi] [0m[91m+ nvidia-nvtx-cu12==[0m[91m12.4.[0m[91m127
[fastapi] + oauthlib==[0m[91m3.3.1
[fastapi] + [0m[91moci==2.[0m[91m185.2[0m[91m
[fastapi] + ocifs[0m[91m==1.3.2
[fastapi] + opentelemetry-api==1[0m[91m.44.0
[fastapi] +[0m[91m opentelemetry-exporter-otlp-proto-common==[0m[91m1.44.0
[fastapi] [0m[91m+ opentelemetry-exporter-otlp-proto-http==1.44.0
[fastapi] + opentelemetry-proto[0m[91m==1.44.0
[fastapi] +[0m[91m opentelemetry-sdk==1.44.0
[fastapi] [0m[91m+ opentelemetry-semantic-conventions[0m[91m==0.65[0m[91mb0[0m[91m
[fastapi] +[0m[91m optimum==[0m[91m1.[0m[91m16.2
[fastapi] [0m[91m + orjson==3.12.0
[fastapi] + pandas[0m[91m==2.3.3
[fastapi] + pathvalidate[0m[91m==3.3.1[0m[91m
[fastapi] +[0m[91m peft==[0m[91m0[0m[91m.15.2
[fastapi] [0m[91m [0m[91m+ [0m[91mpillow==11.3.0
[fastapi] + platformdirs==4.11.[0m[91m8
[fastapi] + [0m[91mportalocker[0m[91m==4.3.2[0m[91m
[fastapi] + propcache==0[0m[91m.5.2[0m[91m
[fastapi] + [0m[91mproto-plus[0m[91m==1.28[0m[91m.[0m[91m2[0m[91m
[fastapi] + protobuf[0m[91m==5.29.6
[fastapi] [0m[91m+ psutil==[0m[91m7.2[0m[91m.2
[fastapi] [0m[91m + [0m[91mpyarrow[0m[91m==25.0[0m[91m.[0m[91m1
[fastapi] [0m[91m+[0m[91m pyasn1==0.6.4
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
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 64.9/64.9 kB 2.3 MB/s eta 0:00:00
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
[fastapi] [0m ---> 05cb1ea454fe
[fastapi] Step 12/14 : RUN bash -c "source /workspace/axo_py/bin/activate &&     python -c \"import transformers, trl, axolotl, jinja2, typer, yaml, torch, requests; from trl.trainer.dpo_trainer import DPOTrainer; assert transformers.__version__.startswith('4.51'), 'axo_py transformers=' + transformers.__version__; assert trl.__version__.startswith('0.17'), 'axo_py trl=' + trl.__version__; print('axo_py stack OK: transformers', transformers.__version__, 'trl', trl.__version__)\" &&     deactivate"
[fastapi] ---> Running in 7fa7d9513e30
[fastapi] [91m/workspace/axo_py/lib/python3.11/site-packages/requests/__init__.py:113: RequestsDependencyWarning: urllib3 (2.7.0) or chardet (6.0.0.post1)/charset_normalizer (3.5.1) doesn't match a supported version!
[fastapi] warnings.warn(
[fastapi] [0maxo_py stack OK: transformers 4.51.3 trl 0.17.0
[fastapi] ---> c504ead8b780
[fastapi] Step 13/14 : RUN pip install uv &&     pip install -U packaging==23.2 setuptools==75.8.0 wheel ninja &&     uv pip install -r /workspace/scripts/training_requirements.txt --system &&     pip install hf_transfer==0.1.9 &&     pip install tenacity==9.1.2 &&     pip install tiktoken==0.9.0 &&     pip install flash-attn==v2.7.4.post1 --no-build-isolation &&     uv pip install vllm==0.8.3 --system &&     pip install "fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0"
[fastapi] ---> Running in 2778df8b4b30
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
[fastapi] [0m[91mResolved 190 packages in 1.60s
[fastapi] [0m[91m   Building deepspeed==0.15.4
[fastapi] [0m[91mDownloading pydantic-core (2.0MiB)
[fastapi] [0m[91mDownloading fonttools (5.2MiB)
[fastapi] [0m[91mDownloading sqlalchemy (3.3MiB)
[fastapi] [0m[91mDownloading matplotlib (9.4MiB)
[fastapi] [0m[91mDownloading kiwisolver (1.4MiB)
[fastapi] [0m[91mDownloading mpi4py (1.3MiB)
[fastapi] [0m[91mDownloading plotly (8.6MiB)
[fastapi] [0m[91mDownloading pyphen (2.0MiB)
[fastapi] [0m[91mDownloading pandas (12.5MiB)
[fastapi] [0m[91mDownloading openai (1.9MiB)
[fastapi] [0m[91mDownloading scipy (35.9MiB)
[fastapi] [0m[91mDownloading hf-xet (4.3MiB)
[fastapi] [0m[91mDownloading mlflow-skinny (3.5MiB)
[fastapi] [0m[91mDownloading pycryptodome (2.2MiB)
[fastapi] [0m[91mDownloading dash (8.5MiB)
[fastapi] [0m[91mDownloading mlflow (11.0MiB)
[fastapi] [0m[91mDownloading wandb (20.4MiB)
[fastapi] [0m[91mDownloading scikit-learn (8.9MiB)
[fastapi] [0m[91mDownloading tensorboard (5.2MiB)
[fastapi] [0m[91mDownloading sentencepiece (1.2MiB)
[fastapi] [0m[91mDownloading mlflow-tracing (1.7MiB)
[fastapi] [0m[91m   Building antlr4-python3-runtime==4.9.3
[fastapi] [0m[91m Downloaded mpi4py
[fastapi] [0m[91m Downloaded sentencepiece
[fastapi] [0m[91m Downloaded kiwisolver
[fastapi] [0m[91m Downloaded mlflow-tracing
[fastapi] [0m[91m Downloaded pydantic-core
[fastapi] [0m[91m Downloaded pyphen
[fastapi] [0m[91m Downloaded pycryptodome
[fastapi] [0m[91m Downloaded openai
[fastapi] [0m[91m Downloaded sqlalchemy
[fastapi] [0m[91m Downloaded mlflow-skinny
[fastapi] [0m[91m      Built antlr4-python3-runtime==4.9.3
[fastapi] [0m[91m Downloaded hf-xet
[fastapi] [0m[91m Downloaded fonttools
[fastapi] [0m[91m Downloaded tensorboard
[fastapi] [0m[91m Downloaded dash
[fastapi] [0m[91m Downloaded plotly
[fastapi] [0m[91m Downloaded scikit-learn
[fastapi] [0m[91m Downloaded matplotlib
[fastapi] [0m[91m Downloaded pandas
[fastapi] [0m[91m Downloaded mlflow
[fastapi] [0m[91m Downloaded wandb
[fastapi] [0m[91m Downloaded scipy
[fastapi] [0m[91m      Built deepspeed==0.15.4
[fastapi] [0m[91mPrepared 91 packages in 839ms
[fastapi] [0m[91mUninstalled 6 packages in 31ms
[fastapi] [0m[91mInstalled 144 packages in 3.01s
[fastapi] [0m[91m + absl-py==2.5.0
[fastapi] + accelerate==1.6.0
[fastapi] + aiohappyeyeballs==2.7.1
[fastapi] + aiohttp==3.14.3
[fastapi] + aiosignal==1.4.0
[fastapi] + alembic==1.20.0
[fastapi] + annotated-doc==0[0m[91m.0.5
[fastapi] + annotated-types==0.8.0
[fastapi] + antlr4-python3-runtime==4.9.3
[fastapi] [0m[91m - anyio==4.6.0
[fastapi] + anyio==4.15.1
[fastapi] + astor==0.8.1
[fastapi] + bitsandbytes==0.45.4
[fastapi] + blinker[0m[91m==1.9.0
[fastapi] + cachetools==7.1.8
[fastapi] - cffi==[0m[91m1.17[0m[91m.1
[fastapi] + [0m[91mcffi==2.1[0m[91m.1
[fastapi] +[0m[91m click==8.5.0
[fastapi] + cloudpickle==3.1[0m[91m.2
[fastapi] [0m[91m+ cmudict==1[0m[91m.1.3
[fastapi] [0m[91m +[0m[91m colorlog==[0m[91m6.12.0[0m[91m
[fastapi] +[0m[91m contourpy==[0m[91m1.3[0m[91m.3
[fastapi] [0m[91m + cryptography[0m[91m==50.0.[0m[91m1
[fastapi] [0m[91m+ [0m[91mcycler==0[0m[91m.12.1
[fastapi] + dash==4.4.1[0m[91m
[fastapi] + databricks-sdk[0m[91m==[0m[91m0.139.0
[fastapi] [0m[91m + datasets[0m[91m==3.5.0
[fastapi] + deepspeed==0[0m[91m.15.4
[fastapi] + detoxify==0.[0m[91m5.2
[fastapi] +[0m[91m dill==0[0m[91m.3.8
[fastapi] + docker[0m[91m==7.2.0
[fastapi] + docker-pycreds[0m[91m==0[0m[91m.4.0[0m[91m
[fastapi] + [0m[91meinops==[0m[91m0.8.1[0m[91m
[fastapi] + fastapi==0.141.1
[fastapi] [0m[91m+ flask==3.[0m[91m1.3
[fastapi] [0m[91m+ flask-cors==6.0.5
[fastapi] +[0m[91m fonttools==4.65[0m[91m.0
[fastapi] + frozenlist[0m[91m==1.8.0
[fastapi] + [0m[91mgdown==6.2[0m[91m.0
[fastapi] +[0m[91m gitdb==4.[0m[91m0.12
[fastapi] +[0m[91m gitpython==3[0m[91m.1.62
[fastapi] [0m[91m+ google-auth[0m[91m==2.58.0[0m[91m
[fastapi] + [0m[91mgraphene==3.4.3
[fastapi] + [0m[91mgraphql-core==3.2.12
[fastapi] [0m[91m + graphql-relay==3[0m[91m.2.0[0m[91m
[fastapi] + [0m[91mgreenlet==[0m[91m3.5[0m[91m.6
[fastapi] [0m[91m [0m[91m+ grpcio[0m[91m==1.[0m[91m84.0[0m[91m
[fastapi] [0m[91m [0m[91m+ [0m[91mgunicorn==[0m[91m26.2[0m[91m.[0m[91m0
[fastapi] [0m[91m- [0m[91mh11[0m[91m==0.[0m[91m14.[0m[91m0
[fastapi] + h11[0m[91m==0.16.[0m[91m0
[fastapi] [0m[91m +[0m[91m [0m[91mhf-xet[0m[91m==1.6[0m[91m.0[0m[91m
[fastapi] [0m[91m+ hjson[0m[91m==[0m[91m3.[0m[91m1.0[0m[91m
[fastapi] [0m[91m+ [0m[91mhttpcore2[0m[91m==2.[0m[91m13[0m[91m.0
[fastapi] [0m[91m + httpx2[0m[91m==2.13.0
[fastapi] + huey[0m[91m==3.4.0[0m[91m
[fastapi] + [0m[91mhuggingface-hub==0.36.2
[fastapi] [0m[91m- idna==3.[0m[91m10
[fastapi] + [0m[91midna==3.19[0m[91m
[fastapi] + importlib-metadata[0m[91m==9.0.[0m[91m1
[fastapi] + [0m[91mimportlib-resources==7.[0m[91m1.0
[fastapi] + itsdangerous==2.2.0
[fastapi] [0m[91m + jaconv==[0m[91m0.5.0[0m[91m
[fastapi] + [0m[91mjanus==[0m[91m2.[0m[91m0.0
[fastapi] [0m[91m+ jiter[0m[91m==0.17.0
[fastapi] +[0m[91m joblib==[0m[91m1.[0m[91m6.0[0m[91m
[fastapi] + [0m[91mkiwisolver==1.5.1
[fastapi] [0m[91m + langcheck[0m[91m==[0m[91m0.[0m[91m9.0[0m[91m
[fastapi] + liger-kernel[0m[91m==0.5.9
[fastapi] + mako==1[0m[91m.4.1
[fastapi] + markdown==3.10[0m[91m.3[0m[91m
[fastapi] + matplotlib[0m[91m==3.11.[0m[91m2[0m[91m
[fastapi] + minio==7.2.20
[fastapi] + [0m[91mmlflow==3.16.0
[fastapi] + mlflow-skinny[0m[91m==3.16.0
[fastapi] [0m[91m+[0m[91m mlflow-tracing==3.[0m[91m16.0
[fastapi] [0m[91m + mpi4py==4.1.2
[fastapi] + msgpack==[0m[91m1.2.2
[fastapi] + multidict==6[0m[91m.8.0
[fastapi] + multiprocess==0.70.[0m[91m16
[fastapi] [0m[91m + narwhals==[0m[91m2[0m[91m.26.0[0m[91m
[fastapi] [0m[91m + nlpaug[0m[91m==1.1.11[0m[91m
[fastapi] + nltk==3.10[0m[91m.3
[fastapi] + omegaconf==2.3.1
[fastapi] + openai==3.14.[0m[91m0
[fastapi] + [0m[91mopentelemetry-api[0m[91m==1.44.0[0m[91m
[fastapi] + opentelemetry-proto==1.44.0
[fastapi] + opentelemetry-sdk[0m[91m==1.44.0
[fastapi] + opentelemetry-semantic-conventions==0.65b0
[fastapi] [0m[91m+ optuna[0m[91m==4.4.0
[fastapi] + pandas==2.2.[0m[91m3
[fastapi] + peft==0.15.1
[fastapi] [0m[91m + plotly==[0m[91m7.0.[0m[91m0
[fastapi] +[0m[91m [0m[91mprettytable==3.18[0m[91m.0[0m[91m
[fastapi] [0m[91m+ propcache[0m[91m==0.5.2[0m[91m
[fastapi] + protobuf[0m[91m==6.[0m[91m33.6[0m[91m
[fastapi] [0m[91m+ py-cpuinfo[0m[91m==[0m[91m9.0.0
[fastapi] + pyarrow==25.0.1[0m[91m
[fastapi] + [0m[91mpyasn1==0.[0m[91m6.[0m[91m4[0m[91m
[fastapi] + pyasn1-modules[0m[91m==[0m[91m0.4.2[0m[91m
[fastapi] +[0m[91m pycryptodome[0m[91m==3.[0m[91m23.0[0m[91m
[fastapi] [0m[91m [0m[91m+ pydantic==2.[0m[91m13.5[0m[91m
[fastapi] +[0m[91m pydantic-core[0m[91m==2.46.5
[fastapi] + [0m[91mpyparsing==3.3.2
[fastapi] [0m[91m+ pyphen==0[0m[91m.18[0m[91m.1
[fastapi] [0m[91m+ pysocks[0m[91m==1.7.1
[fastapi] + python-dotenv==1.[0m[91m2.3
[fastapi] + pytz[0m[91m==2026.3.post1
[fastapi] + [0m[91mredis[0m[91m==7.[0m[91m0.1[0m[91m
[fastapi] +[0m[91m regex==2026.9.10
[fastapi] +[0m[91m restrictedpython[0m[91m==8.[0m[91m0
[fastapi] [0m[91m+ [0m[91mretrying[0m[91m==1.4.2[0m[91m
[fastapi] [0m[91m + rouge-score[0m[91m==[0m[91m0.1[0m[91m.[0m[91m2
[fastapi] + safetensors==0.8.0
[fastapi] +[0m[91m scikit-learn==1.9.1
[fastapi] + [0m[91mscipy==1.[0m[91m15.2[0m[91m
[fastapi] [0m[91m+ [0m[91msentence-transformers==5.7.0
[fastapi] + sentencepiece==0.2.0[0m[91m
[fastapi] [0m[91m+ sentry-sdk==[0m[91m2.69.1
[fastapi] + [0m[91msetproctitle==1.3.7[0m[91m
[fastapi] + six==1.17.[0m[91m0
[fastapi] +[0m[91m skops[0m[91m==0.14.0
[fastapi] [0m[91m + [0m[91msmmap==5.0.3
[fastapi] + sqlalchemy==2[0m[91m.0.53
[fastapi] + sqlparse==0.6[0m[91m.0
[fastapi] + starlette[0m[91m==1.[0m[91m6.0[0m[91m
[fastapi] +[0m[91m tabulate==0.10.0
[fastapi] [0m[91m+ tenacity[0m[91m==[0m[91m9.[0m[91m1.4[0m[91m
[fastapi] [0m[91m+ [0m[91mtensorboard[0m[91m==2.19[0m[91m.0[0m[91m
[fastapi] [0m[91m + [0m[91mtensorboard-data-server[0m[91m==0[0m[91m.7.2
[fastapi] [0m[91m+[0m[91m textstat[0m[91m==[0m[91m0.7.8
[fastapi] + threadpoolctl==3.6.0
[fastapi] [0m[91m + tokenizers==0.21[0m[91m.4
[fastapi] + toml==0.10.2
[fastapi] [0m[91m + tqdm==[0m[91m4.70.1[0m[91m
[fastapi] + transformers==4[0m[91m.51.[0m[91m3
[fastapi] + [0m[91mtrl==[0m[91m0.18.[0m[91m0
[fastapi] [0m[91m+ [0m[91mtruststore==0.[0m[91m10.[0m[91m4
[fastapi] +[0m[91m typer==[0m[91m0.[0m[91m9.0
[fastapi] - typing-extensions==[0m[91m4.9.0
[fastapi] + [0m[91mtyping-extensions==4.16[0m[91m.0
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
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.6/3.6 MB 136.4 MB/s eta 0:00:00
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
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 96.9 MB/s eta 0:00:00
[fastapi] Installing collected packages: tiktoken
[fastapi] Successfully installed tiktoken-0.9.0
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0mCollecting flash-attn==v2.7.4.post1
[fastapi] Downloading flash_attn-2.7.4.post1.tar.gz (6.0 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.0/6.0 MB 53.6 MB/s eta 0:00:00
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
[fastapi] [0m[91mResolved 142 packages in 385ms
[fastapi] [0m[91mDownloading pycountry (7.7MiB)
[fastapi] [0m[91mDownloading torchaudio (3.2MiB)
[fastapi] [0m[91mDownloading numpy (15.6MiB)
[fastapi] [0m[91mDownloading mistral-common (6.2MiB)
[fastapi] [0m[91mDownloading cupy-cuda12x (130.3MiB)
[fastapi] [0m[91mDownloading numba (3.6MiB)
[fastapi] [0m[91mDownloading torchvision (6.9MiB)
[fastapi] [0m[91mDownloading uvloop (3.6MiB)
[fastapi] [0m[91mDownloading opencv-python-headless (58.4MiB)
[fastapi] [0m[91mDownloading pillow (6.6MiB)
[fastapi] [0m[91mDownloading llguidance (14.3MiB)
[fastapi] [0m[91mDownloading llvmlite (40.4MiB)
[fastapi] [0m[91mDownloading ray (74.7MiB)
[fastapi] [0m[91mDownloading xgrammar (4.1MiB)
[fastapi] [0m[91mDownloading vllm (280.4MiB)
[fastapi] [0m[91m Downloaded uvloop
[fastapi] [0m[91m Downloaded torchaudio
[fastapi] [0m[91m Downloaded mistral-common
[fastapi] [0m[91m Downloaded pillow
[fastapi] [0m[91m Downloaded pycountry
[fastapi] [0m[91m Downloaded xgrammar
[fastapi] [0m[91m Downloaded numpy
[fastapi] [0m[91m Downloaded llguidance
[fastapi] [0m[91m Downloaded numba
[fastapi] [0m[91m Downloaded torchvision
[fastapi] [0m[91m Downloaded opencv-python-headless
[fastapi] [0m[91m Downloaded llvmlite
[fastapi] [0m[91m Downloaded ray
[fastapi] [0m[91m Downloaded cupy-cuda12x
[fastapi] [0m[91m Downloaded vllm
[fastapi] [0m[91mPrepared 45 packages in 15.49s
[fastapi] [0m[91mUninstalled 23 packages in 1.70s
[fastapi] [0m[91mInstalled 71 packages in 13.25s
[fastapi] [0m[91m + agent-detector==2.0.0
[fastapi] + airportsdata==20260905
[fastapi] + blake3==1.0.9
[fastapi] + compressed-tensors==0.9.2
[fastapi] + cuda-pathfinder==1.8.1
[fastapi] [0m[91m+ cupy-cuda12x==14.2.0
[fastapi] + depyf[0m[91m==0.18.0
[fastapi] +[0m[91m detect-installer==0.2[0m[91m.1
[fastapi] +[0m[91m diskcache==5.6[0m[91m.3
[fastapi] +[0m[91m dnspython==2.[0m[91m8.0
[fastapi] [0m[91m+ email-validator==2.[0m[91m3.0
[fastapi] + fastapi-cli==0.0.32
[fastapi] +[0m[91m fastapi-cloud-cli[0m[91m==0.26[0m[91m.0
[fastapi] +[0m[91m fastar==0.12.0
[fastapi] - filelock==3.13.1
[fastapi] + filelock==3.32.6
[fastapi] +[0m[91m gguf==0.10.0
[fastapi] - [0m[91mhttpcore==1.0.5[0m[91m
[fastapi] + httpcore[0m[91m==1.0.9[0m[91m
[fastapi] + httptools[0m[91m==0.8[0m[91m.0
[fastapi] +[0m[91m interegular==[0m[91m0.3.3
[fastapi] [0m[91m - jinja2==[0m[91m3.1.3
[fastapi] + [0m[91mjinja2==3.1.6
[fastapi] + lark==1.2.2
[fastapi] [0m[91m + [0m[91mllguidance==0.7.30[0m[91m
[fastapi] + [0m[91mllvmlite[0m[91m==0.44[0m[91m.0
[fastapi] [0m[91m [0m[91m+ [0m[91mlm-format-enforcer==0[0m[91m.10.[0m[91m12
[fastapi] [0m[91m +[0m[91m markdown-it-py[0m[91m==[0m[91m4.2.[0m[91m0
[fastapi] [0m[91m+[0m[91m mdurl[0m[91m==0[0m[91m.1.[0m[91m2
[fastapi] [0m[91m+ [0m[91mmistral-common==[0m[91m1.11[0m[91m.7
[fastapi] [0m[91m+[0m[91m msgspec[0m[91m==0.[0m[91m21.1[0m[91m
[fastapi] [0m[91m + [0m[91mnanobind[0m[91m==3.0.1
[fastapi] [0m[91m + numba==0.61.0
[fastapi] [0m[91m- [0m[91mnumpy==1[0m[91m.26[0m[91m.3
[fastapi] [0m[91m +[0m[91m numpy==2.1.3
[fastapi] [0m[91m- [0m[91mnvidia-cublas-cu12==12[0m[91m.4.[0m[91m2.[0m[91m65[0m[91m
[fastapi] + nvidia-cublas-cu12==12.4.5.8
[fastapi] -[0m[91m nvidia-cuda-cupti-cu12==12.4.99
[fastapi] [0m[91m+ nvidia-cuda-cupti-cu12[0m[91m==[0m[91m12.4.127[0m[91m
[fastapi] [0m[91m- nvidia-cuda-nvrtc-cu12[0m[91m==12.[0m[91m4.99
[fastapi] + nvidia-cuda-nvrtc-cu12==12.4.127[0m[91m
[fastapi] - nvidia-cuda-runtime-cu12==12.4.99[0m[91m
[fastapi] + [0m[91mnvidia-cuda-runtime-cu12==12.[0m[91m4.[0m[91m127
[fastapi] [0m[91m - [0m[91mnvidia-cufft-cu12==[0m[91m11.2.[0m[91m0.44
[fastapi] [0m[91m+ [0m[91mnvidia-cufft-cu12==11.2.1.3
[fastapi] - nvidia-curand-cu12==10[0m[91m.3.5.119
[fastapi] + [0m[91mnvidia-curand-cu12==10.3.[0m[91m5.147
[fastapi] [0m[91m- [0m[91mnvidia-cusolver-cu12[0m[91m==11.6.[0m[91m0.99[0m[91m
[fastapi] [0m[91m+ [0m[91mnvidia-cusolver-cu12==[0m[91m11.6.[0m[91m1.[0m[91m9
[fastapi] -[0m[91m [0m[91mnvidia-cusparse-cu12==[0m[91m12.[0m[91m3.0[0m[91m.142
[fastapi] [0m[91m +[0m[91m nvidia-cusparse-cu12[0m[91m==12[0m[91m.3.1[0m[91m.170
[fastapi] [0m[91m +[0m[91m nvidia-cusparselt-cu12[0m[91m==0.6.2
[fastapi] - nvidia-nccl-cu12[0m[91m==2.[0m[91m20.5[0m[91m
[fastapi] +[0m[91m [0m[91mnvidia-nccl-cu12[0m[91m==2.21.[0m[91m5
[fastapi] [0m[91m- [0m[91mnvidia-nvjitlink-cu12==12.4.99
[fastapi] + nvidia-nvjitlink-cu12==12.4.[0m[91m127
[fastapi] - nvidia-nvtx-cu12[0m[91m==12.4.99[0m[91m
[fastapi] + [0m[91mnvidia-nvtx-cu12==12.4.127
[fastapi] + opencv-python-headless==5.[0m[91m0.0.93[0m[91m
[fastapi] + outlines==0.1.11
[fastapi] + outlines-core==0.1.26
[fastapi] - packaging==23.2
[fastapi] + packaging==26.3
[fastapi] + partial-json-parser==0.2.1.1.post7
[fastapi] - pillow==10.2.0
[fastapi] + pillow==12.3.0
[fastapi] + prometheus-fastapi-instrumentator==8.1.0
[fastapi] + pycountry==26.2.16
[fastapi] [0m[91m + pydantic-extra-types==2.11.1[0m[91m
[fastapi] + pydantic-settings==2[0m[91m.15.0
[fastapi] [0m[91m + python-multipart[0m[91m==0.0.[0m[91m32
[fastapi] +[0m[91m ray==2[0m[91m.58.0
[fastapi] [0m[91m+ rich==[0m[91m15.0.0
[fastapi] [0m[91m + rich-toolkit[0m[91m==0.20.5
[fastapi] [0m[91m+ rignore==0.8[0m[91m.1
[fastapi] +[0m[91m shellingham==[0m[91m1.5.4[0m[91m
[fastapi] - sympy[0m[91m==1.[0m[91m12
[fastapi] + [0m[91msympy==1.13[0m[91m.1
[fastapi] [0m[91m - torch==[0m[91m2.4.1+[0m[91mcu124
[fastapi] + torch==2.6.0
[fastapi] - torchaudio==2.4[0m[91m.1+cu124
[fastapi] + torchaudio==2.[0m[91m6.0
[fastapi] [0m[91m-[0m[91m torchvision==0[0m[91m.19[0m[91m.1+cu124[0m[91m
[fastapi] +[0m[91m [0m[91mtorchvision==0.[0m[91m21.0
[fastapi] [0m[91m -[0m[91m triton==3.0.0
[fastapi] + triton==3.[0m[91m2.0
[fastapi] [0m[91m - [0m[91mtyper==[0m[91m0.9.0[0m[91m
[fastapi] [0m[91m+ typer[0m[91m==0.[0m[91m27.[0m[91m2
[fastapi] +[0m[91m [0m[91muvloop==[0m[91m0.22.[0m[91m1
[fastapi] [0m[91m +[0m[91m [0m[91mvllm==0[0m[91m.8.3[0m[91m
[fastapi] [0m[91m + watchfiles[0m[91m==1.2.0[0m[91m
[fastapi] + websockets[0m[91m==17.[0m[91m1
[fastapi] [0m[91m+ [0m[91mxformers==0[0m[91m.0.[0m[91m29.post2
[fastapi] + xgrammar==0.1[0m[91m.17
[fastapi] [0mCollecting fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0
[fastapi] Cloning https://github.com/rayonlabs/fiber.git (to revision 2.4.0) to /tmp/pip-install-e_nmos6w/fiber_dbcc85f19cef4d2ea8a90ac15caaeadd
[fastapi] [91m  Running command git clone --filter=blob:none --quiet https://github.com/rayonlabs/fiber.git /tmp/pip-install-e_nmos6w/fiber_dbcc85f19cef4d2ea8a90ac15caaeadd
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
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 552.2/552.2 kB 21.1 MB/s eta 0:00:00
[fastapi] Downloading eth_typing-5.0.0-py3-none-any.whl (20 kB)
[fastapi] Downloading netaddr-1.3.0-py3-none-any.whl (2.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.3/2.3 MB 44.8 MB/s eta 0:00:00
[fastapi] Downloading python_dotenv-1.0.1-py3-none-any.whl (19 kB)
[fastapi] Downloading substrate_interface-1.7.10-py3-none-any.whl (60 kB)
[fastapi] Downloading tenacity-9.0.0-py3-none-any.whl (28 kB)
[fastapi] Downloading async_substrate_interface-1.6.4-py3-none-any.whl (97 kB)
[fastapi] Downloading bt_decode-0.8.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (647 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 647.8/647.8 kB 73.7 MB/s eta 0:00:00
[fastapi] Downloading colorama-0.4.6-py2.py3-none-any.whl (25 kB)
[fastapi] Downloading pydantic-2.9.2-py3-none-any.whl (434 kB)
[fastapi] Downloading pydantic_core-2.23.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 67.0 MB/s eta 0:00:00
[fastapi] Downloading aiosqlite-0.22.1-py3-none-any.whl (17 kB)
[fastapi] Downloading base58-2.1.1-py3-none-any.whl (5.6 kB)
[fastapi] Downloading ecdsa-0.19.2-py2.py3-none-any.whl (150 kB)
[fastapi] Downloading eth_keys-0.8.0-py3-none-any.whl (20 kB)
[fastapi] Downloading eth_utils-2.3.2-py3-none-any.whl (77 kB)
[fastapi] Downloading py_bip39_bindings-0.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (432 kB)
[fastapi] Downloading py_ed25519_zebra_bindings-1.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (323 kB)
[fastapi] Downloading py_sr25519_bindings-0.2.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (372 kB)
[fastapi] Downloading pynacl-1.6.2-cp38-abi3-manylinux_2_34_x86_64.whl (1.4 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.4/1.4 MB 175.8 MB/s eta 0:00:00
[fastapi] Downloading scalecodec-1.2.12-py3-none-any.whl (99 kB)
[fastapi] Downloading xxhash-3.8.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (220 kB)
[fastapi] Downloading cytoolz-1.1.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (2.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.8/2.8 MB 122.9 MB/s eta 0:00:00
[fastapi] Downloading eth_hash-0.8.0-py3-none-any.whl (8.0 kB)
[fastapi] Downloading toolz-1.1.0-py3-none-any.whl (58 kB)
[fastapi] Building wheels for collected packages: fiber
[fastapi] Building wheel for fiber (pyproject.toml): started
[fastapi] Building wheel for fiber (pyproject.toml): finished with status 'done'
[fastapi] Created wheel for fiber: filename=fiber-2.4.0-py3-none-any.whl size=51790 sha256=c50f803eff2fbcdf01560cfffdc65a3891a75b0b315d61d842fd3861f51b5d73
[fastapi] Stored in directory: /tmp/pip-ephem-wheel-cache-e6x86_m6/wheels/d1/5e/21/2fa1f403cd187996037f04f6328bf11973ce31440a275f6949
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
[fastapi] [0m ---> 8a435c7d15d4
[fastapi] Step 14/14 : ENTRYPOINT ["./entrypoint.sh"]
[fastapi] ---> Running in 7c6c2d948b51
[fastapi] ---> f066c80d4338
[fastapi] {'aux': {'ID': 'sha256:f066c80d43381c3448c9a7192242b7ebf4bd4b2cf273f85025d90831bd9006f0'}}Successfully built f066c80d4338
[fastapi] Successfully tagged standalone-text-trainer:8980d979-e20a-47c8-8181-9abbddbeb83d
[fastapi] Docker image built successfully.
[fastapi] Container.wait() returned: {'StatusCode': 0}
[fastapi] Cleaning up
[fastapi] Cleaned up Docker resources.
[fastapi] Starting upload container hf-upload-867ca272887f4d23b506afbaa8e50fbc for task 90d361cb-0b97-464a-9fda-36eb34c99261...
[hf-upload-86]  adapter_config.json not found
[hf-upload-86] Updated README.md with base_model: LiquidAI/LFM2.5-2.6B
[hf-upload-86] Creating repo gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-90d361cb-0b97-464a-9fda-36eb34c99261-5HBgDWKx...
[hf-upload-86] Uploading contents of /app/checkpoints/90d361cb-0b97-464a-9fda-36eb34c99261/tournament-tourn_5c64e784a087074a_20260914-90d361cb-0b97-464a-9fda-36eb34c99261-5HBgDWKx to gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-90d361cb-0b97-464a-9fda-36eb34c99261-5HBgDWKx
[hf-upload-86] Uploaded successfully to https://huggingface.co/gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-90d361cb-0b97-464a-9fda-36eb34c99261-5HBgDWKx
[hf-upload-86] Deleted local folder: /app/checkpoints/90d361cb-0b97-464a-9fda-36eb34c99261/tournament-tourn_5c64e784a087074a_20260914-90d361cb-0b97-464a-9fda-36eb34c99261-5HBgDWKx
[text-trainer] *****Running text trainer
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_hash" in MinerSubmission has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] ---STARTING TEXT TRAINING SCRIPT---
[text-trainer] submission_dir: /app/checkpoints/90d361cb-0b97-464a-9fda-36eb34c99261/tournament-tourn_5c64e784a087074a_20260914-90d361cb-0b97-464a-9fda-36eb34c99261-5HBgDWKx
[text-trainer] end_time:  2026-09-15 05:36:44
[text-trainer] [tokenizer-sanitize] removed placeholder tokenizer_class='TokenizersBackend' from /cache/models/a0971600276b8e78/tokenizer_config.json (AutoTokenizer will fall back to model_type)
[text-trainer] [tokenizer-sanitize] write fail (skip): /cache/models/a0971600276b8e78/tokenizer_config.json: [Errno 30] Read-only file system: '/cache/models/a0971600276b8e78/tokenizer_config.json'
[text-trainer] '(MaxRetryError('HTTPSConnectionPool(host=\'huggingface.co\', port=443): Max retries exceeded with url: /a0971600276b8e78/resolve/main/config.json (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x7f0ca6484510>: Failed to resolve \'huggingface.co\' ([Errno -3] Temporary failure in name resolution)"))'), '(Request ID: f4f4bab8-7b37-464a-9da6-36853c8aa84c)')' thrown while requesting HEAD https://huggingface.co/a0971600276b8e78/resolve/main/config.json
[text-trainer] Retrying in 1s [Retry 1/5].
[text-trainer] '(MaxRetryError('HTTPSConnectionPool(host=\'huggingface.co\', port=443): Max retries exceeded with url: /a0971600276b8e78/resolve/main/config.json (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x7f0ca64853d0>: Failed to resolve \'huggingface.co\' ([Errno -3] Temporary failure in name resolution)"))'), '(Request ID: 7ac433ac-18a3-4f2a-9685-4c6e27de30f9)')' thrown while requesting HEAD https://huggingface.co/a0971600276b8e78/resolve/main/config.json
[text-trainer] Retrying in 2s [Retry 2/5].
[text-trainer] '(MaxRetryError('HTTPSConnectionPool(host=\'huggingface.co\', port=443): Max retries exceeded with url: /a0971600276b8e78/resolve/main/config.json (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x7f0ca6486450>: Failed to resolve \'huggingface.co\' ([Errno -3] Temporary failure in name resolution)"))'), '(Request ID: c980004e-6463-4185-95c2-73fa51942646)')' thrown while requesting HEAD https://huggingface.co/a0971600276b8e78/resolve/main/config.json
[text-trainer] Retrying in 4s [Retry 3/5].
[text-trainer] '(MaxRetryError('HTTPSConnectionPool(host=\'huggingface.co\', port=443): Max retries exceeded with url: /a0971600276b8e78/resolve/main/config.json (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x7f0ca648b8d0>: Failed to resolve \'huggingface.co\' ([Errno -3] Temporary failure in name resolution)"))'), '(Request ID: 20f69e15-1a62-41b2-9215-299bbe48d033)')' thrown while requesting HEAD https://huggingface.co/a0971600276b8e78/resolve/main/config.json
[text-trainer] Retrying in 8s [Retry 4/5].
[text-trainer] '(MaxRetryError('HTTPSConnectionPool(host=\'huggingface.co\', port=443): Max retries exceeded with url: /a0971600276b8e78/resolve/main/config.json (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x7f0ca6487390>: Failed to resolve \'huggingface.co\' ([Errno -3] Temporary failure in name resolution)"))'), '(Request ID: 1ed554bb-bd51-45f5-b6cc-2a6485b6da33)')' thrown while requesting HEAD https://huggingface.co/a0971600276b8e78/resolve/main/config.json
[text-trainer] Retrying in 8s [Retry 5/5].
[text-trainer] '(MaxRetryError('HTTPSConnectionPool(host=\'huggingface.co\', port=443): Max retries exceeded with url: /a0971600276b8e78/resolve/main/config.json (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x7f0ca64861d0>: Failed to resolve \'huggingface.co\' ([Errno -3] Temporary failure in name resolution)"))'), '(Request ID: 3badad98-95f4-4ca4-bde4-871315b803c4)')' thrown while requesting HEAD https://huggingface.co/a0971600276b8e78/resolve/main/config.json
[text-trainer] [preflight] transformers cannot build this architecture: The checkpoint you are trying to load has model type `lfm2` but Transformers does not recognize this architecture. This could be because of an issue with the checkpoint, or because your version of Transformers is out of 
[text-trainer] [preflight] skipping tokenisation and training: no number of retries can load this model. Going straight to the fallback submission.
[text-trainer] [text_trainer] ADAPTIVE_MODE=on — using dynamics-driven config
[text-trainer] [baseline-stats] loaded: task_type=instruct, top_keys=['dataset', 'task_type', 'throughput', 'training', 'weights']
[text-trainer] [adaptive] baseline stats available: keys=['dataset', 'task_type', 'throughput', 'training', 'weights']
[text-trainer] [dynamics] AutoConfig failed: The checkpoint you are trying to load has model type `lfm2` but Transformers does not recognize this architecture. This could be because of an issue with the checkpoint, or because your version of Transformers is out of date.
[text-trainer] 
[text-trainer] You can update Transformers with the command `pip install --upgrade transformers`. If this does not work, and the checkpoint is very new, then there may not be a release version that supports this model yet. In this case, you can get the most up-to-date code by installing Transformers from source with the command `pip install git+https://github.com/huggingface/transformers.git`
[text-trainer] [dynamics] param_count: AutoConfig failed (The checkpoint you are trying to load has model type `lfm2` but Transformers does not recognize this architecture. This could be because of an issue with the checkpoint, or because your version of Transformers is out of date.
[text-trainer] 
[text-trainer] You can update Transformers with the command `pip install --upgrade transformers`. If this does not work, and the checkpoint is very new, then there may not be a release version that supports this model yet. In this case, you can get the most up-to-date code by installing Transformers from source with the command `pip install git+https://github.com/huggingface/transformers.git`); config.json readable, raw estimate=2.75B (ADVISORY, not applied) — using the 1B default
[text-trainer] [adaptive] WARN: param_count unknown, defaulting to 1B
[text-trainer] [adaptive] WARN: max_position probe failed (The checkpoint you are trying to load has model type `lfm2` but Transformers does not recognize this architecture. This could be because of an issue with the checkpoint, or because your version of Transformers is out of date.
[text-trainer] 
[text-trainer] You can update Transformers with the command `pip install --upgrade transformers`. If this does not work, and the checkpoint is very new, then there may not be a release version that supports this model yet. In this case, you can get the most up-to-date code by installing Transformers from source with the command `pip install git+https://github.com/huggingface/transformers.git`), skipping safety cap
[text-trainer] [adaptive] tokenizer load failed: Tokenizer class TokenizersBackend does not exist or is not currently imported. / Tokenizer class TokenizersBackend does not exist or is not currently imported.
[text-trainer] [adaptive] WARN: using conservative dataset defaults (no path or no tokenizer)
[text-trainer] [adaptive] seq_len p95: raised 1024->1316 from validator full-dataset p95
[text-trainer] [adaptive] max_length sized from seq_len_p95 (legacy chain)=1316
[text-trainer] [adaptive] batch bucket scaled for length: 100 -> 70 (max_length=1447 vs reference 1024)
[text-trainer] [adaptive] 1-GPU empirical bucket: batch=70 (target=70 for param=1.00B)
[text-trainer] [adaptive] Tier 1 family_lr MISS (no entry for arch=None task=instruct)
[text-trainer] [adaptive] Tier 2 AR-CSV MISS (no entry for arch=None)
[text-trainer] [adaptive] baseline_stats init_loss=1.132
[text-trainer] [adaptive] epoch loss signal=0.740 (masked_completion_loss)
[text-trainer] [adaptive-instruct] profile: io_jaccard=0.347 train_dev_jaccard=0.359 flags=cot:0.72 math:0.29 code:0.21 script=latin lang_ratio=0.97
[text-trainer] [adaptive-instruct] task_class=reasoning
[text-trainer] [adaptive-instruct] task_class=reasoning OVERRIDE: lr 1.00e-04→1.00e-04, epoch 4→2, neftune 0→0
[text-trainer] [adaptive] EXP-K2 max_length halving applied: instruct_hp=1536 → 1447 (validator-aligned via max_pos=None)
[text-trainer] [adaptive] EXP-T hours_budget=2.0h step_time_est=9.3s (measured) → max_steps_budget=711
[text-trainer] [2026-09-15 03:40:12,142] [INFO] [real_accelerator.py:219:get_accelerator] Setting ds_accelerator to cuda (auto detect)
[text-trainer] df: /root/.triton/autotune: No such file or directory
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] [adaptive] use_liger=False (model_type from config, liger dispatch map)
[text-trainer] [adaptive-instruct] family=unknown (arch=unknown, name=unknown) epoch=2 lr=1.00e-04 min_lr_rate=0.2 wd=0.01 max_len=1447 packing=True neftune=0 warmup=35 reg_ratio=1.0
[text-trainer] [adaptive] arch=unknown param=1,000,000,000 ds_n=10000 seq_p95=1316
[text-trainer] [adaptive] PLAN: lr=1.00e-04 batch=70 epochs=2 max_len=1447 lora=False grad_accum=1
[text-trainer] [hp-override:d2z] no fire: tpp=0.01≤1.0 OR epochs=3<2 (n_train=10000, params=1.00B, est_tokens=13160000)
[text-trainer] [resolver] SUGGESTION: lr=3.60e-04 (T1_empirical n=1 task_class=skill) vs adaptive_init_lr=1.00e-04 → ratio=3.60x
[text-trainer] [adaptive] reg_ratio=1.00000 (neutral, lr unchanged)
[text-trainer] [adaptive] packing disabled: disable_fa is set, and packing without flash-attn lets rows attend across block boundaries
[text-trainer] [CONFIG-RESOLVED] path=adaptive task_type=InstructTextTask task_id=90d361cb-0b97-464a-9fda-36eb34c99261 lr=0.0001 batch=70 steps_or_epochs=2 model=?
[text-trainer] Training failed for task 90d361cb-0b97-464a-9fda-36eb34c99261
[text-trainer] [stage] NaN/Inf + zero-weight scan of the submission: 0.0s (cumulative 0.0s, +6989s to end_time)
[text-trainer] [stage] dev absorption: 0.0s (cumulative 0.0s, +6989s to end_time)
[text-trainer] Training failed for task 90d361cb-0b97-464a-9fda-36eb34c99261
[text-trainer] [noise] cloning base model /cache/models/a0971600276b8e78 -> /app/checkpoints/90d361cb-0b97-464a-9fda-36eb34c99261/tournament-tourn_5c64e784a087074a_20260914-90d361cb-0b97-464a-9fda-36eb34c99261-5HBgDWKx
[text-trainer] [noise] clone method: copy
[text-trainer] [noise] perturbed noise disabled (FALLBACK_NOISE_STD=0.0) — clean copy of the base, model-00001-of-00002.safetensors un-linked
[text-trainer] [noise] submission ready: 11 entries in /app/checkpoints/90d361cb-0b97-464a-9fda-36eb34c99261/tournament-tourn_5c64e784a087074a_20260914-90d361cb-0b97-464a-9fda-36eb34c99261-5HBgDWKx
[text-trainer] [stage] noise fallback: 3.9s (cumulative 3.9s, +6985s to end_time)
[text-trainer] [stage] restore_submission_architectures: 0.0s (cumulative 3.9s, +6985s to end_time)