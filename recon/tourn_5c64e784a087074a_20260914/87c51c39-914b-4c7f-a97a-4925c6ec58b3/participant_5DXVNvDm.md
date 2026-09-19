# Loki — task 87c51c39-914b-4c7f-a97a-4925c6ec58b3 — hotkey 5DXVNvDmGZqdXbqRzsJZdJVoAgbLdhdFrrrmtAAfsh4QkGUU
fetched 2026-09-19T05:05:39+00:00  lines=1769  hit_page_cap=False  containers=['downloader-87c51c39-914b-4c7f-a97a-4925c6ec58b3-0a760530', 'fastapi', 'hf-upload-2a93b29334df47e48123f82702d079df', 'text-trainer-3b3f33af059a459d81b2d6f4ff7bd8bf']

[downloader-8] Downloading datasets to: /cache/datasets
[downloader-8] Downloading models to: /cache/models
[downloader-8] Model already cached at /cache/models/b254e84a30620233.
[downloader-8] Skipping download.
[downloader-8] Model path: /cache/models/b254e84a30620233
[downloader-8] Dataset path: /cache/datasets
[fastapi] Repository cloned successfully
[fastapi] Running Cache Download Container
[fastapi] Starting downloader container: downloader-87c51c39-914b-4c7f-a97a-4925c6ec58b3-0a760530
[fastapi] Download completed successfully for task 87c51c39-914b-4c7f-a97a-4925c6ec58b3
[fastapi] Building Docker image 'standalone-text-trainer:d894466b-eed8-446f-918c-c4fe097799e2' (timeout=1800s)...
[fastapi] Step 1/14 : FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04
[fastapi] ---> ff5fe688608b
[fastapi] Step 2/14 : RUN apt-get update && apt-get install -y     vim     zip     tmux     iotop     nvtop     bmon     wget     nano     zsh     htop     redis-server     && rm -rf /var/lib/apt/lists/*
[fastapi] ---> Running in 1c73d8c8bea7
[fastapi] Get:1 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  InRelease [1578 B]
[fastapi] Get:2 http://security.ubuntu.com/ubuntu jammy-security InRelease [129 kB]
[fastapi] Get:3 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  Packages [3009 kB]
[fastapi] Get:4 http://archive.ubuntu.com/ubuntu jammy InRelease [270 kB]
[fastapi] Get:5 http://security.ubuntu.com/ubuntu jammy-security/multiverse amd64 Packages [84.6 kB]
[fastapi] Get:6 http://security.ubuntu.com/ubuntu jammy-security/main amd64 Packages [4290 kB]
[fastapi] Get:7 http://security.ubuntu.com/ubuntu jammy-security/restricted amd64 Packages [7717 kB]
[fastapi] Get:8 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy InRelease [18.1 kB]
[fastapi] Get:9 http://security.ubuntu.com/ubuntu jammy-security/universe amd64 Packages [1317 kB]
[fastapi] Get:10 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy/main amd64 Packages [44.3 kB]
[fastapi] Get:11 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [128 kB]
[fastapi] Get:12 http://archive.ubuntu.com/ubuntu jammy-backports InRelease [127 kB]
[fastapi] Get:13 http://archive.ubuntu.com/ubuntu jammy/multiverse amd64 Packages [266 kB]
[fastapi] Get:14 http://archive.ubuntu.com/ubuntu jammy/restricted amd64 Packages [164 kB]
[fastapi] Get:15 http://archive.ubuntu.com/ubuntu jammy/universe amd64 Packages [17.5 MB]
[fastapi] Get:16 http://archive.ubuntu.com/ubuntu jammy/main amd64 Packages [1792 kB]
[fastapi] Get:17 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 Packages [1620 kB]
[fastapi] Get:18 http://archive.ubuntu.com/ubuntu jammy-updates/multiverse amd64 Packages [93.2 kB]
[fastapi] Get:19 http://archive.ubuntu.com/ubuntu jammy-updates/restricted amd64 Packages [8007 kB]
[fastapi] Get:20 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 Packages [4624 kB]
[fastapi] Get:21 http://archive.ubuntu.com/ubuntu jammy-backports/universe amd64 Packages [35.6 kB]
[fastapi] Get:22 http://archive.ubuntu.com/ubuntu jammy-backports/main amd64 Packages [82.8 kB]
[fastapi] Fetched 51.3 MB in 4s (13.7 MB/s)
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
[fastapi] [0mFetched 24.4 MB in 1s (25.3 MB/s)
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
[fastapi] ---> f2e85b6bd07c
[fastapi] Step 3/14 : RUN mkdir -p /workspace
[fastapi] ---> Running in 418b02687272
[fastapi] ---> abb6242d1665
[fastapi] Step 4/14 : RUN mkdir -p /cache
[fastapi] ---> Running in 7342bc70b4f4
[fastapi] ---> 06f45c9d219c
[fastapi] Step 5/14 : RUN mkdir -p /workspace/scripts/datasets
[fastapi] ---> Running in 8a9208a32ea7
[fastapi] ---> a0787caff05e
[fastapi] Step 6/14 : RUN mkdir -p /app/checkpoints
[fastapi] ---> Running in bbc2ce9f70c1
[fastapi] ---> ebf128d4fd11
[fastapi] Step 7/14 : WORKDIR /workspace/scripts
[fastapi] ---> Running in d9d628bdadcd
[fastapi] ---> b160391fbba9
[fastapi] Step 8/14 : COPY scripts /workspace/scripts
[fastapi] ---> 16d404383a3b
[fastapi] Step 9/14 : RUN chmod +x /workspace/scripts/entrypoint.sh
[fastapi] ---> Running in f989b20bbcbf
[fastapi] ---> cd0be7a41f82
[fastapi] Step 10/14 : RUN python -m venv /workspace/axo_py
[fastapi] ---> Running in f8e631607150
[fastapi] ---> c0f8cb393982
[fastapi] Step 11/14 : RUN bash -c "source /workspace/axo_py/bin/activate &&     pip install uv &&     pip install -U packaging==23.2 setuptools==75.8.0 wheel ninja &&     uv pip install --no-build-isolation axolotl==0.9.1 &&     pip install requests==2.32.3 &&     deactivate"
[fastapi] ---> Running in 206d9b355db0
[fastapi] Collecting uv
[fastapi] Downloading uv-0.12.14-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
[fastapi] Downloading uv-0.12.14-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (20.0 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 20.0/20.0 MB 163.5 MB/s eta 0:00:00
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
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 53.0/53.0 kB 5.6 MB/s eta 0:00:00
[fastapi] Downloading setuptools-75.8.0-py3-none-any.whl (1.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 34.5 MB/s eta 0:00:00
[fastapi] Downloading wheel-0.45.1-py3-none-any.whl (72 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 72.5/72.5 kB 9.1 MB/s eta 0:00:00
[fastapi] Downloading ninja-1.13.2-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (183 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 183.4/183.4 kB 42.6 MB/s eta 0:00:00
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
[fastapi] [0m[91mResolved 217 packages in 1.48s
[fastapi] [0m[91mDownloading pygments (1.2MiB)
[fastapi] [0m[91mDownloading sentencepiece (1.3MiB)
[fastapi] [0m[91mDownloading nvidia-cusolver-cu12 (122.0MiB)
[fastapi] [0m[91mDownloading zstandard (5.2MiB)
[fastapi] [0m[91mDownloading torchao (5.4MiB)
[fastapi] [0m[91mDownloading scikit-learn (11.6MiB)
[fastapi] [0m[91mDownloading [0m[91mtokenizers [0m[91m(3.0MiB)
[fastapi] [0m[91mDownloading hf-transfer[0m[91m [0m[91m(3.4MiB)
[fastapi] [0m[91mDownloading nvidia-curand-cu12 (53.7MiB)[0m[91m
[fastapi] [0m[91mDownloading nvidia-cuda-nvrtc-cu12 (23.5MiB)
[fastapi] [0m[91mDownloading nvidia-cublas-cu12 (346.6MiB)
[fastapi] [0m[91mDownloading bitsandbytes (72.5MiB)
[fastapi] [0m[91mDownloading lxml (5.0MiB)
[fastapi] [0m[91mDownloading lm-eval (2.4MiB)
[fastapi] [0m[91mDownloading nvidia-cufft-cu12 (201.7MiB)
[fastapi] [0m[91mDownloading torch (731.2MiB)
[fastapi] [0m[91mDownloading pydantic-core (1.9MiB)
[fastapi] [0m[91mDownloading wandb (24.9MiB)
[fastapi] [0m[91mDownloading triton (241.4MiB)
[fastapi] [0m[91mDownloading nvidia-cudnn-cu12 (634.0MiB)
[fastapi] [0m[91mDownloading tensorboard-data-server (6.3MiB)
[fastapi] [0m[91mDownloading pyarrow (47.7MiB)
[fastapi] [0m[91mDownloading llvmlite (57.1MiB)
[fastapi] [0m[91mDownloading ruff (9.9MiB)
[fastapi] [0m[91mDownloading hf-xet (51.1MiB)
[fastapi] [0m[91mDownloading xformers (42.2MiB)
[fastapi] [0m[91mDownloading nvidia-cusparselt-cu12 (143.1MiB)
[fastapi] [0m[91mDownloading nvidia-cusparse-cu12 (197.8MiB)
[fastapi] [0m[91mDownloading botocore (13.7MiB)
[fastapi] [0m[91mDownloading scipy (33.7MiB)
[fastapi] [0m[91mDownloading[0m[91m numba (3.6MiB)
[fastapi] Downloading numpy (18.6MiB)
[fastapi] Downloading gradio (44.3MiB)
[fastapi] Downloading sympy (5.9MiB)
[fastapi] [0m[91mDownloading[0m[91m [0m[91mnvidia-nvjitlink-cu12 (20.1MiB)
[fastapi] [0m[91mDownloading networkx (2.0MiB)
[fastapi] [0m[91mDownloading nltk (1.7MiB)
[fastapi] [0m[91mDownloading grpcio (6.9MiB)
[fastapi] [0m[91mDownloading pandas (12.2MiB)
[fastapi] [0m[91mDownloading aiohttp (1.7MiB)
[fastapi] [0m[91mDownloading nvidia-cuda-cupti-cu12 (13.2MiB)
[fastapi] [0m[91mDownloading nvidia-nccl-cu12 (179.9MiB)
[fastapi] [0m[91mDownloading cryptography (4.5MiB)
[fastapi] [0m[91mDownloading oci (35.2MiB)
[fastapi] [0m[91mDownloading tensorboard (5.3MiB)
[fastapi] [0m[91mDownloading transformers (9.9MiB)
[fastapi] [0m[91m Downloaded pygments
[fastapi] [0m[91mDownloading pillow (6.3MiB)
[fastapi] [0m[91m Downloaded sentencepiece
[fastapi] [0m[91m Downloaded aiohttp
[fastapi] [0m[91m Downloaded nltk
[fastapi] [0m[91m Downloaded pydantic-core
[fastapi] [0m[91m Downloaded networkx
[fastapi] [0m[91m Downloaded lm-eval
[fastapi] [0m[91m   [0m[91mBuilding axolotl==0.9.1
[fastapi] [0m[91m Downloaded tokenizers
[fastapi] [0m[91m   [0m[91mBuilding axolotl-contribs-mit==0.0.3
[fastapi] [0m[91m   Building langdetect[0m[91m==1.0.9
[fastapi] [0m[91m   Building word2number==1.1
[fastapi] [0m[91m [0m[91mDownloaded hf-transfer
[fastapi] [0m[91m   Building axolotl-contribs-lgpl[0m[91m==0.0.6[0m[91m
[fastapi] [0m[91m   Building rouge-score==0.1.2
[fastapi] [0m[91m   Building sqlitedict==2.1.0
[fastapi] [0m[91m Downloaded numba
[fastapi] [0m[91m   [0m[91mBuilding grpclib==0.4.7
[fastapi] Building hqq==0.2.5
[fastapi] [0m[91m Downloaded zstandard
[fastapi] [0m[91m Downloaded cryptography
[fastapi] [0m[91m      Built word2number==1.1
[fastapi] [0m[91m      Built axolotl-contribs-mit==0.0.3
[fastapi] [0m[91m Downloaded lxml
[fastapi] [0m[91m Downloaded torchao
[fastapi] [0m[91m      Built rouge-score==0.1.2
[fastapi] [0m[91m      Built axolotl-contribs-lgpl==0.0.6
[fastapi] [0m[91m      Built sqlitedict==2.1.0
[fastapi] [0m[91m Downloaded tensorboard
[fastapi] [0m[91m Downloaded sympy
[fastapi] [0m[91m      Built axolotl==0.9.1
[fastapi] [0m[91m Downloaded tensorboard-data-server
[fastapi] [0m[91m Downloaded pillow
[fastapi] Built grpclib==0.4.7
[fastapi] [0m[91m Downloaded grpcio
[fastapi] [0m[91m      Built langdetect==1.0.9
[fastapi] [0m[91m Downloaded transformers
[fastapi] Downloaded ruff
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
[fastapi] [0m[91m Downloaded[0m[91m hf-xet
[fastapi] [0m[91m [0m[91mDownloaded nvidia-curand-cu12
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
[fastapi] [0m[91mPrepared 215 packages in 9.33s
[fastapi] [0m[91mInstalled 215 packages in 526ms
[fastapi] [0m[91m + absl-py==2.5.0
[fastapi] + accelerate==1.6.0
[fastapi] + addict==2.4.0
[fastapi] + adlfs==2026.8.0
[fastapi] + aiobotocore==2.26.0
[fastapi] + aiofiles==23.2.[0m[91m1
[fastapi] + aiohappyeyeballs==2.7.1
[fastapi] + aiohttp==3.14.3
[fastapi] + aioitertools==0.13.0[0m[91m
[fastapi] + aiosignal==1[0m[91m.4.0
[fastapi] +[0m[91m annotated-doc==0.[0m[91m0.5
[fastapi] + [0m[91mannotated-types==0.8.0
[fastapi] [0m[91m + antlr4-python3-runtime[0m[91m==4.13.2[0m[91m
[fastapi] + anyio[0m[91m==4.15.1
[fastapi] +[0m[91m art==6[0m[91m.5
[fastapi] + attrs[0m[91m==26.1[0m[91m.0
[fastapi] [0m[91m+ autoawq==[0m[91m0.2.7.post[0m[91m3
[fastapi] + [0m[91maxolotl==0.9[0m[91m.1
[fastapi] + [0m[91maxolotl-contribs-lgpl==0.[0m[91m0.6
[fastapi] +[0m[91m axolotl-contribs-mit==0.[0m[91m0.3
[fastapi] +[0m[91m azure-core==1.[0m[91m41.0
[fastapi] [0m[91m+ azure-identity[0m[91m==1.25.[0m[91m3
[fastapi] + [0m[91mazure-storage-blob==12[0m[91m.30.1
[fastapi] [0m[91m+ bitsandbytes==[0m[91m0.45.4
[fastapi] [0m[91m + botocore==1.41[0m[91m.5
[fastapi] +[0m[91m certifi==2026[0m[91m.7.22
[fastapi] [0m[91m + cffi[0m[91m==2.1[0m[91m.1
[fastapi] + chardet==6.0.0.post1
[fastapi] +[0m[91m charset-normalizer==3.[0m[91m5.1
[fastapi] [0m[91m+ circuitbreaker==[0m[91m2.1.3
[fastapi] [0m[91m+ click[0m[91m==8.5.[0m[91m0
[fastapi] +[0m[91m cloudpickle==3[0m[91m.1.2
[fastapi] [0m[91m+ colorama==[0m[91m0.4.6
[fastapi] [0m[91m + coloredlogs[0m[91m==15.0.[0m[91m1
[fastapi] + [0m[91mcrc32c==2.[0m[91m8
[fastapi] + [0m[91mcryptography==50.[0m[91m0.1
[fastapi] +[0m[91m dataproperty==1[0m[91m.1.1
[fastapi] [0m[91m+ datasets==[0m[91m3.5.1[0m[91m
[fastapi] + decorator[0m[91m==5.3.1[0m[91m
[fastapi] +[0m[91m defusedxml==0.[0m[91m7.1
[fastapi] +[0m[91m dill==0[0m[91m.3.8
[fastapi] [0m[91m + einops[0m[91m==0.8[0m[91m.2
[fastapi] +[0m[91m evaluate==0.4[0m[91m.1
[fastapi] [0m[91m+ fastapi==0[0m[91m.141.1
[fastapi] [0m[91m+ fastcore==[0m[91m2.2.27[0m[91m
[fastapi] + [0m[91mffmpy==1.[0m[91m0.0
[fastapi] [0m[91m+ filelock==3.[0m[91m32.6
[fastapi] [0m[91m+ fire==0.7.1
[fastapi] + frozenlist==[0m[91m1.8.0
[fastapi] [0m[91m + [0m[91mfsspec==2025.[0m[91m3.0
[fastapi] [0m[91m+ gcsfs==2025[0m[91m.3.0
[fastapi] [0m[91m+ google-api-core[0m[91m==2.33.0[0m[91m
[fastapi] + google-auth==2[0m[91m.58.0
[fastapi] + google-auth-oauthlib==1[0m[91m.4.1
[fastapi] [0m[91m+ google-cloud-core==2[0m[91m.7.0
[fastapi] +[0m[91m google-cloud-storage==3.[0m[91m14.1
[fastapi] + google-crc32c==1.8.0
[fastapi] [0m[91m + google-resumable-media[0m[91m==2.10.2
[fastapi] + googleapis-common-protos==1[0m[91m.75.0
[fastapi] + gradio==5.23.3[0m[91m
[fastapi] + gradio-client==1.8.0
[fastapi] + groovy[0m[91m==0.1.2
[fastapi] + grpcio==1.84[0m[91m.0
[fastapi] + [0m[91mgrpclib[0m[91m==0.4.7[0m[91m
[fastapi] [0m[91m + h11==[0m[91m0.16.[0m[91m0
[fastapi] [0m[91m+ [0m[91mh2==4[0m[91m.4.[0m[91m1
[fastapi] [0m[91m+ [0m[91mhf-transfer[0m[91m==0.[0m[91m1.9
[fastapi] [0m[91m +[0m[91m hf-xet[0m[91m==1[0m[91m.[0m[91m1.0
[fastapi] + hpack==4.2[0m[91m.0[0m[91m
[fastapi] [0m[91m + hqq[0m[91m==[0m[91m0.[0m[91m2.5
[fastapi] [0m[91m+[0m[91m httpcore[0m[91m==1.0[0m[91m.9
[fastapi] [0m[91m [0m[91m+ [0m[91mhttpx==0[0m[91m.[0m[91m28.1
[fastapi] +[0m[91m [0m[91mhuggingface-hub==[0m[91m0.31[0m[91m.0[0m[91m
[fastapi] [0m[91m+[0m[91m humanfriendly==[0m[91m10.[0m[91m0
[fastapi] +[0m[91m [0m[91mhyperframe==6[0m[91m.1.[0m[91m0[0m[91m
[fastapi] [0m[91m+ idna[0m[91m==[0m[91m3.19[0m[91m
[fastapi] +[0m[91m immutabledict[0m[91m==4.2.[0m[91m0
[fastapi] [0m[91m+[0m[91m isodate[0m[91m==0[0m[91m.7.2[0m[91m
[fastapi] [0m[91m + [0m[91mjinja2[0m[91m==[0m[91m3.1.6
[fastapi] [0m[91m +[0m[91m [0m[91mjmespath[0m[91m==1[0m[91m.1.0
[fastapi] [0m[91m +[0m[91m [0m[91mjoblib==1[0m[91m.6.0[0m[91m
[fastapi] [0m[91m + [0m[91mjsonlines==[0m[91m4.[0m[91m0.[0m[91m0
[fastapi] +[0m[91m [0m[91mlangdetect==[0m[91m1.0[0m[91m.[0m[91m9
[fastapi] + liger-kernel==0.[0m[91m5.9
[fastapi] + llvmlite==0[0m[91m.49.0
[fastapi] [0m[91m+ [0m[91mlm-eval==0.4[0m[91m.7
[fastapi] [0m[91m + [0m[91mlxml[0m[91m==6.1.3
[fastapi] [0m[91m+ markdown==[0m[91m3.10[0m[91m.3
[fastapi] [0m[91m +[0m[91m markdown-it-py[0m[91m==4.2[0m[91m.0[0m[91m
[fastapi] +[0m[91m markupsafe[0m[91m==3.[0m[91m0.3[0m[91m
[fastapi] [0m[91m+ [0m[91mmbstrdecoder==1[0m[91m.1[0m[91m.5
[fastapi] [0m[91m+[0m[91m mdurl[0m[91m==0.[0m[91m1.2
[fastapi] [0m[91m+[0m[91m modal[0m[91m==0.[0m[91m70.5[0m[91m
[fastapi] [0m[91m+ [0m[91mmore-itertools==[0m[91m11.[0m[91m1.[0m[91m0
[fastapi] [0m[91m+[0m[91m mpmath[0m[91m==1.3.0
[fastapi] + [0m[91mmsal==1.[0m[91m38.0[0m[91m
[fastapi] [0m[91m+ msal-extensions[0m[91m==[0m[91m1.3.[0m[91m1
[fastapi] + multidict==6.8.0
[fastapi] + multiprocess[0m[91m==0.70.16
[fastapi] + networkx[0m[91m==3.6.[0m[91m1
[fastapi] + nltk==3.10.3
[fastapi] + numba[0m[91m==0.67.0
[fastapi] +[0m[91m numexpr==2.[0m[91m14.2
[fastapi] [0m[91m + numpy[0m[91m==2.0[0m[91m.1[0m[91m
[fastapi] [0m[91m+ nvidia-cublas-cu12[0m[91m==12.4.5.8[0m[91m
[fastapi] + nvidia-cuda-cupti-cu12==[0m[91m12.4.127
[fastapi] [0m[91m + nvidia-cuda-nvrtc-cu12==12[0m[91m.4.127
[fastapi] [0m[91m + nvidia-cuda-runtime-cu12[0m[91m==12.4.[0m[91m127
[fastapi] + nvidia-cudnn-cu12[0m[91m==9.1[0m[91m.0.70
[fastapi] [0m[91m + nvidia-cufft-cu12[0m[91m==11.2.1[0m[91m.3
[fastapi] + nvidia-curand-cu12==[0m[91m10.3.5.[0m[91m147
[fastapi] + nvidia-cusolver-cu12==[0m[91m11[0m[91m.6.1.9[0m[91m
[fastapi] [0m[91m [0m[91m+ nvidia-cusparse-cu12==[0m[91m12[0m[91m.3.1.[0m[91m170
[fastapi] +[0m[91m nvidia-cusparselt-cu12==[0m[91m0.6.[0m[91m2[0m[91m
[fastapi] [0m[91m+ nvidia-ml-py==[0m[91m12[0m[91m.560[0m[91m.[0m[91m30
[fastapi] + nvidia-nccl-cu12==2.21.5
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
[fastapi] [0m ---> 6fbd1e1a33c3
[fastapi] Step 12/14 : RUN pip install uv &&     pip install -U packaging==23.2 setuptools==75.8.0 wheel ninja &&     uv pip install -r /workspace/scripts/training_requirements.txt --system &&     pip install hf_transfer==0.1.9 &&     pip install tenacity==9.1.2 &&     pip install tiktoken==0.9.0 &&     pip install flash-attn==v2.7.4.post1 --no-build-isolation &&     uv pip install vllm==0.8.3 --system &&     pip install "fiber @ git+https://github.com/rayonlabs/fiber.git@2.4.0"
[fastapi] ---> Running in 8200ae828352
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
[fastapi] [0m[91mResolved 190 packages in 1.62s
[fastapi] [0m[91m   Building deepspeed==0.15.4
[fastapi] [0m[91mDownloading pycryptodome (2.2MiB)
[fastapi] [0m[91mDownloading tensorboard (5.2MiB)
[fastapi] [0m[91m   Building antlr4-python3-runtime==4.9.3
[fastapi] [0m[91mDownloading wandb (20.4MiB)
[fastapi] [0m[91mDownloading plotly (8.6MiB)
[fastapi] [0m[91mDownloading scipy (35.9MiB)
[fastapi] [0m[91mDownloading mlflow (11.0MiB)
[fastapi] [0m[91mDownloading openai (1.9MiB)
[fastapi] [0m[91mDownloading mlflow-tracing (1.7MiB)
[fastapi] [0m[91mDownloading sqlalchemy (3.3MiB)
[fastapi] [0m[91mDownloading sentencepiece (1.2MiB)
[fastapi] [0m[91mDownloading hf-xet (4.3MiB)
[fastapi] [0m[91mDownloading dash (8.5MiB)
[fastapi] [0m[91mDownloading scikit-learn (8.9MiB)
[fastapi] [0m[91mDownloading pyphen (2.0MiB)
[fastapi] [0m[91mDownloading kiwisolver (1.4MiB)
[fastapi] [0m[91mDownloading fonttools (5.2MiB)
[fastapi] [0m[91mDownloading pandas (12.5MiB)
[fastapi] [0m[91mDownloading pydantic-core (2.0MiB)
[fastapi] [0m[91mDownloading mlflow-skinny (3.5MiB)
[fastapi] [0m[91mDownloading matplotlib (9.4MiB)
[fastapi] [0m[91mDownloading mpi4py (1.3MiB)
[fastapi] [0m[91m Downloaded sentencepiece
[fastapi] [0m[91m Downloaded mpi4py
[fastapi] [0m[91m Downloaded pycryptodome
[fastapi] [0m[91m Downloaded mlflow-tracing
[fastapi] [0m[91m Downloaded kiwisolver
[fastapi] [0m[91m Downloaded pydantic-core
[fastapi] [0m[91m Downloaded openai
[fastapi] [0m[91m Downloaded pyphen
[fastapi] [0m[91m Downloaded sqlalchemy
[fastapi] [0m[91m Downloaded mlflow-skinny
[fastapi] [0m[91m Downloaded hf-xet
[fastapi] [0m[91m Downloaded tensorboard
[fastapi] [0m[91m      Built antlr4-python3-runtime==4.9.3
[fastapi] [0m[91m Downloaded fonttools
[fastapi] [0m[91m Downloaded scikit-learn
[fastapi] [0m[91m Downloaded matplotlib
[fastapi] [0m[91m Downloaded dash
[fastapi] [0m[91m Downloaded plotly
[fastapi] [0m[91m Downloaded pandas
[fastapi] [0m[91m Downloaded mlflow
[fastapi] [0m[91m Downloaded wandb
[fastapi] [0m[91m Downloaded scipy
[fastapi] [0m[91m      Built deepspeed==0.15.4
[fastapi] [0m[91mPrepared 91 packages in 854ms
[fastapi] [0m[91mUninstalled 6 packages in 29ms
[fastapi] [0m[91mInstalled 144 packages in 3.21s
[fastapi] [0m[91m + absl-py==2.5.0
[fastapi] + accelerate==1.6.0
[fastapi] + aiohappyeyeballs==2.7.1
[fastapi] + aiohttp==3.14.3
[fastapi] + aiosignal==1.4.0
[fastapi] + alembic==1.20.0
[fastapi] + annotated-doc==0.0.5
[fastapi] [0m[91m + annotated-types==0.8.0
[fastapi] + antlr4-python3-runtime==4.9.3
[fastapi] - anyio==4.6[0m[91m.0
[fastapi] + anyio==[0m[91m4.15.1
[fastapi] + astor[0m[91m==0.8.1
[fastapi] + bitsandbytes==0[0m[91m.45.4
[fastapi] + blinker==1[0m[91m.9.0
[fastapi] + cachetools==7.1.8
[fastapi] - [0m[91mcffi==1.17.1
[fastapi] + cffi==2.1.1
[fastapi] + [0m[91mclick==8.5.0[0m[91m
[fastapi] [0m[91m+ cloudpickle[0m[91m==3.[0m[91m1.2[0m[91m
[fastapi] +[0m[91m cmudict[0m[91m==1.1.3[0m[91m
[fastapi] + colorlog==6.12.0
[fastapi] + contourpy[0m[91m==1.[0m[91m3.3
[fastapi] [0m[91m+ cryptography[0m[91m==50.0.1
[fastapi] + [0m[91mcycler==0.12.1
[fastapi] [0m[91m + dash==4.[0m[91m4.1
[fastapi] + databricks-sdk[0m[91m==0.139.0
[fastapi] [0m[91m + datasets[0m[91m==3.5.0
[fastapi] [0m[91m + deepspeed[0m[91m==0.15.4
[fastapi] [0m[91m + detoxify==0.5.2[0m[91m
[fastapi] + dill==0.3.8[0m[91m
[fastapi] + docker==7.[0m[91m2[0m[91m.0
[fastapi] + [0m[91mdocker-pycreds==0[0m[91m.4.0
[fastapi] [0m[91m +[0m[91m einops==0.8[0m[91m.1
[fastapi] +[0m[91m fastapi==0[0m[91m.141.[0m[91m1[0m[91m
[fastapi] + [0m[91mflask==[0m[91m3.1.[0m[91m3
[fastapi] [0m[91m+[0m[91m flask-cors==[0m[91m6.0[0m[91m.5
[fastapi] [0m[91m [0m[91m+ [0m[91mfonttools==4[0m[91m.65.0
[fastapi] + frozenlist==1[0m[91m.8.0
[fastapi] + gdown==6[0m[91m.2[0m[91m.0
[fastapi] + [0m[91mgitdb==4[0m[91m.0.[0m[91m12
[fastapi] +[0m[91m gitpython[0m[91m==3.[0m[91m1.62
[fastapi] [0m[91m+ google-auth[0m[91m==2.58[0m[91m.0
[fastapi] [0m[91m+ [0m[91mgraphene==3.4.3
[fastapi] + graphql-core==3.2[0m[91m.12
[fastapi] + graphql-relay==3.2.0
[fastapi] + [0m[91mgreenlet==3.5.[0m[91m6
[fastapi] + grpcio==[0m[91m1.84.0[0m[91m
[fastapi] [0m[91m + gunicorn[0m[91m==26.2.0[0m[91m
[fastapi] - h11[0m[91m==0.14[0m[91m.0
[fastapi] [0m[91m+[0m[91m h11[0m[91m==0.16.0
[fastapi] + hf-xet==1.6.0
[fastapi] + hjson==3.1.0
[fastapi] [0m[91m + httpcore2==2.13.0
[fastapi] + [0m[91mhttpx2==2.13[0m[91m.0
[fastapi] [0m[91m +[0m[91m huey[0m[91m==3[0m[91m.4.0
[fastapi] [0m[91m+ huggingface-hub[0m[91m==0.36.[0m[91m2[0m[91m
[fastapi] - idna[0m[91m==3[0m[91m.10[0m[91m
[fastapi] [0m[91m + [0m[91midna[0m[91m==3.19
[fastapi] [0m[91m [0m[91m+ importlib-metadata==9[0m[91m.0.1
[fastapi] + importlib-resources==7[0m[91m.1.0[0m[91m
[fastapi] + [0m[91mitsdangerous==[0m[91m2.[0m[91m2.0
[fastapi] [0m[91m+ jaconv[0m[91m==[0m[91m0.[0m[91m5.0
[fastapi] [0m[91m+[0m[91m janus==2[0m[91m.0.0[0m[91m
[fastapi] [0m[91m+ [0m[91mjiter[0m[91m==0.17.[0m[91m0[0m[91m
[fastapi] + [0m[91mjoblib[0m[91m==1.[0m[91m6.0
[fastapi] [0m[91m +[0m[91m kiwisolver[0m[91m==[0m[91m1.[0m[91m5.1
[fastapi] [0m[91m+[0m[91m [0m[91mlangcheck==0.[0m[91m9.0
[fastapi] + liger-kernel==0[0m[91m.5.9[0m[91m
[fastapi] [0m[91m+[0m[91m mako[0m[91m==1.4.1
[fastapi] + [0m[91mmarkdown==3.10.3[0m[91m
[fastapi] +[0m[91m matplotlib==3.11.2
[fastapi] +[0m[91m minio==7.2.[0m[91m20
[fastapi] + mlflow==3.16[0m[91m.0[0m[91m
[fastapi] [0m[91m+ mlflow-skinny[0m[91m==3.16.0
[fastapi] +[0m[91m mlflow-tracing[0m[91m==3.16[0m[91m.0
[fastapi] + mpi4py==4.1.[0m[91m2
[fastapi] + msgpack==1.2[0m[91m.2
[fastapi] + multidict==6.8.0[0m[91m
[fastapi] + [0m[91mmultiprocess==0[0m[91m.70.16
[fastapi] [0m[91m +[0m[91m narwhals==2[0m[91m.26.[0m[91m0
[fastapi] [0m[91m+ nlpaug[0m[91m==1.[0m[91m1.11
[fastapi] [0m[91m+[0m[91m nltk[0m[91m==3.10[0m[91m.3
[fastapi] + omegaconf[0m[91m==2.3.1
[fastapi] [0m[91m +[0m[91m openai[0m[91m==3.14[0m[91m.[0m[91m0
[fastapi] +[0m[91m [0m[91mopentelemetry-api==1[0m[91m.44.0[0m[91m
[fastapi] [0m[91m+ opentelemetry-proto[0m[91m==1.[0m[91m44.0[0m[91m
[fastapi] [0m[91m+ opentelemetry-sdk==1.44.0
[fastapi] [0m[91m+ opentelemetry-semantic-conventions==0.[0m[91m65b0[0m[91m
[fastapi] + [0m[91moptuna==4.9[0m[91m.0[0m[91m
[fastapi] +[0m[91m pandas[0m[91m==2.[0m[91m2[0m[91m.3
[fastapi] +[0m[91m [0m[91mpeft==0.[0m[91m15.1
[fastapi] [0m[91m+[0m[91m plotly==[0m[91m7.0.0[0m[91m
[fastapi] + [0m[91mprettytable==3.18.0
[fastapi] + propcache==[0m[91m0.5.2[0m[91m
[fastapi] [0m[91m [0m[91m+ protobuf[0m[91m==6.[0m[91m33.6[0m[91m
[fastapi] [0m[91m +[0m[91m py-cpuinfo[0m[91m==9.0.0[0m[91m
[fastapi] + [0m[91mpyarrow[0m[91m==[0m[91m25.[0m[91m0.1
[fastapi] [0m[91m [0m[91m+[0m[91m [0m[91mpyasn1==0[0m[91m.6.[0m[91m4
[fastapi] [0m[91m+ [0m[91mpyasn1-modules[0m[91m==0.4[0m[91m.[0m[91m2
[fastapi] [0m[91m+ [0m[91mpycryptodome[0m[91m==3.23.0
[fastapi] + pydantic==2.13.5
[fastapi] [0m[91m+ pydantic-core==2.46.5
[fastapi] [0m[91m+ pyparsing==3.[0m[91m3.2
[fastapi] + pyphen[0m[91m==0.18.1
[fastapi] +[0m[91m pysocks==1.7.1
[fastapi] [0m[91m+ python-dotenv==1.2.3[0m[91m
[fastapi] + pytz==2026[0m[91m.3.post1
[fastapi] + [0m[91mredis==7.0.1[0m[91m
[fastapi] + regex==2026[0m[91m.9.10
[fastapi] +[0m[91m restrictedpython==8.0
[fastapi] [0m[91m+ retrying==1.4.[0m[91m2
[fastapi] + rouge-score[0m[91m==0.1.2
[fastapi] [0m[91m+ safetensors==0.8.0
[fastapi] +[0m[91m scikit-learn==[0m[91m1.9.[0m[91m1
[fastapi] [0m[91m+ [0m[91mscipy==1[0m[91m.15.2[0m[91m
[fastapi] + sentence-transformers==5.7[0m[91m.0
[fastapi] + sentencepiece[0m[91m==0.2[0m[91m.0
[fastapi] +[0m[91m sentry-sdk==2[0m[91m.69.1[0m[91m
[fastapi] +[0m[91m setproctitle[0m[91m==1.[0m[91m3.7
[fastapi] + six==1.17.0
[fastapi] + skops==0.14.0
[fastapi] + [0m[91msmmap==5.0.3
[fastapi] + [0m[91msqlalchemy==2.[0m[91m0.53[0m[91m
[fastapi] + sqlparse==0.6.0
[fastapi] + starlette[0m[91m==1.6.0
[fastapi] + tabulate==0.10.0[0m[91m
[fastapi] +[0m[91m [0m[91mtenacity[0m[91m==9.[0m[91m1.4[0m[91m
[fastapi] [0m[91m +[0m[91m tensorboard[0m[91m==[0m[91m2.19.[0m[91m0[0m[91m
[fastapi] +[0m[91m [0m[91mtensorboard-data-server==0.[0m[91m7[0m[91m.2
[fastapi] + textstat==0.7.8
[fastapi] + threadpoolctl==3.6.0
[fastapi] + tokenizers==0.21.4
[fastapi] + toml==0.10.2
[fastapi] + tqdm==4.70.1
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
[fastapi] + yarl==1.24.5
[fastapi] + zipp==4.1.0
[fastapi] [0mCollecting hf_transfer==0.1.9
[fastapi] Downloading hf_transfer-0.1.9-cp38-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (1.7 kB)
[fastapi] Downloading hf_transfer-0.1.9-cp38-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.6 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.6/3.6 MB 170.1 MB/s eta 0:00:00
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
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 102.5 MB/s eta 0:00:00
[fastapi] Installing collected packages: tiktoken
[fastapi] Successfully installed tiktoken-0.9.0
[fastapi] [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable.It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
[fastapi] [0m[91m
[fastapi] [notice] A new release of pip is available: 24.2 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0mCollecting flash-attn==v2.7.4.post1
[fastapi] Downloading flash_attn-2.7.4.post1.tar.gz (6.0 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.0/6.0 MB 184.3 MB/s eta 0:00:00
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
[fastapi] [0m[91mResolved 142 packages in 254ms
[fastapi] [0m[91mDownloading torchvision (6.9MiB)
[fastapi] [0m[91mDownloading llguidance (14.3MiB)
[fastapi] [0m[91mDownloading ray (74.7MiB)
[fastapi] [0m[91mDownloading pycountry (7.7MiB)
[fastapi] [0m[91mDownloading xgrammar (4.1MiB)
[fastapi] [0m[91mDownloading numpy (15.6MiB)
[fastapi] [0m[91mDownloading torchaudio (3.2MiB)
[fastapi] [0m[91mDownloading cupy-cuda12x (130.3MiB)
[fastapi] [0m[91mDownloading llvmlite (40.4MiB)
[fastapi] [0m[91mDownloading numba (3.6MiB)
[fastapi] [0m[91mDownloading opencv-python-headless (58.4MiB)
[fastapi] [0m[91mDownloading uvloop (3.6MiB)
[fastapi] [0m[91mDownloading vllm (280.4MiB)
[fastapi] [0m[91mDownloading pillow (6.6MiB)
[fastapi] [0m[91mDownloading mistral-common (6.2MiB)
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
[fastapi] [0m[91mPrepared 45 packages in 2.68s
[fastapi] [0m[91mUninstalled 23 packages in 1.69s
[fastapi] [0m[91mInstalled 71 packages in 11.41s
[fastapi] [0m[91m + agent-detector==2.0.0
[fastapi] + airportsdata==20260905
[fastapi] + [0m[91mblake3==1.0.9
[fastapi] [0m[91m+ compressed-tensors==0.9.2[0m[91m
[fastapi] + cuda-pathfinder==[0m[91m1.8.1
[fastapi] + cupy-cuda12x==14.2.0
[fastapi] + depyf==0.18.[0m[91m0
[fastapi] +[0m[91m detect-installer==0[0m[91m.2.[0m[91m1
[fastapi] [0m[91m +[0m[91m diskcache[0m[91m==5.6.3
[fastapi] [0m[91m [0m[91m+ [0m[91mdnspython[0m[91m==2.8.[0m[91m0[0m[91m
[fastapi] +[0m[91m email-validator[0m[91m==2.[0m[91m3.[0m[91m0
[fastapi] [0m[91m+ [0m[91mfastapi-cli[0m[91m==0.[0m[91m0.32[0m[91m
[fastapi] +[0m[91m fastapi-cloud-cli[0m[91m==[0m[91m0.26.[0m[91m0
[fastapi] [0m[91m [0m[91m+ fastar[0m[91m==0.[0m[91m12[0m[91m.0
[fastapi] [0m[91m [0m[91m- filelock==3[0m[91m.13.[0m[91m1
[fastapi] [0m[91m +[0m[91m [0m[91mfilelock==3[0m[91m.32.[0m[91m6[0m[91m
[fastapi] +[0m[91m gguf==0[0m[91m.[0m[91m10.0[0m[91m
[fastapi] -[0m[91m httpcore==1.0.5
[fastapi] + [0m[91mhttpcore==1.0.9[0m[91m
[fastapi] + httptools[0m[91m==0.8.0
[fastapi] [0m[91m+ interegular==0.3.3
[fastapi] - jinja2==3.1.3
[fastapi] [0m[91m + jinja2==3.1.6
[fastapi] + lark==1.2.2[0m[91m
[fastapi] +[0m[91m llguidance==[0m[91m0.7.[0m[91m30[0m[91m
[fastapi] + [0m[91mllvmlite[0m[91m==0.44.[0m[91m0[0m[91m
[fastapi] +[0m[91m lm-format-enforcer[0m[91m==0.10[0m[91m.[0m[91m12
[fastapi] + markdown-it-py==4.2.0
[fastapi] [0m[91m + [0m[91mmdurl==0.[0m[91m1.2
[fastapi] [0m[91m [0m[91m+ mistral-common[0m[91m==1.11.7[0m[91m
[fastapi] + msgspec==0.21.[0m[91m1
[fastapi] + nanobind==[0m[91m3.0.1[0m[91m
[fastapi] + numba[0m[91m==0.[0m[91m61.0
[fastapi] - numpy==1[0m[91m.26.3
[fastapi] + numpy==[0m[91m2.1.3
[fastapi] - nvidia-cublas-cu12[0m[91m==[0m[91m12.4[0m[91m.2.[0m[91m65
[fastapi] [0m[91m+[0m[91m nvidia-cublas-cu12[0m[91m==12.[0m[91m4[0m[91m.5.8[0m[91m
[fastapi] - nvidia-cuda-cupti-cu12==12.4.99
[fastapi] + nvidia-cuda-cupti-cu12==12.4.127
[fastapi] - [0m[91mnvidia-cuda-nvrtc-cu12==12.4.99
[fastapi] + nvidia-cuda-nvrtc-cu12==12.4.127
[fastapi] [0m[91m - [0m[91mnvidia-cuda-runtime-cu12==12.4.99
[fastapi] + nvidia-cuda-runtime-cu12==12.4[0m[91m.127
[fastapi] - [0m[91mnvidia-cufft-cu12[0m[91m==11.2.[0m[91m0.44[0m[91m
[fastapi] + nvidia-cufft-cu12==11.2.1.3
[fastapi] [0m[91m- nvidia-curand-cu12==10.3.5.[0m[91m119[0m[91m
[fastapi] +[0m[91m nvidia-curand-cu12==[0m[91m10.3[0m[91m.5[0m[91m.147
[fastapi] [0m[91m- nvidia-cusolver-cu12==11.6[0m[91m.0.99[0m[91m
[fastapi] +[0m[91m nvidia-cusolver-cu12[0m[91m==11.[0m[91m6.1[0m[91m.9
[fastapi] [0m[91m -[0m[91m nvidia-cusparse-cu12[0m[91m==12.[0m[91m3.0.142[0m[91m
[fastapi] + nvidia-cusparse-cu12==12.3.[0m[91m1.170
[fastapi] + nvidia-cusparselt-cu12[0m[91m==0.6.2
[fastapi] [0m[91m - nvidia-nccl-cu12==2.20.5
[fastapi] +[0m[91m nvidia-nccl-cu12==2.21[0m[91m.5
[fastapi] - [0m[91mnvidia-nvjitlink-cu12==[0m[91m12.[0m[91m4.99
[fastapi] [0m[91m +[0m[91m [0m[91mnvidia-nvjitlink-cu12==12.[0m[91m4.[0m[91m127
[fastapi] -[0m[91m nvidia-nvtx-cu12[0m[91m==[0m[91m12.4.99[0m[91m
[fastapi] + [0m[91mnvidia-nvtx-cu12==12.4.127
[fastapi] [0m[91m+ [0m[91mopencv-python-headless[0m[91m==5.[0m[91m0.0.93[0m[91m
[fastapi] [0m[91m + [0m[91moutlines==[0m[91m0[0m[91m.1.11[0m[91m
[fastapi] [0m[91m+ outlines-core[0m[91m==0.1.26[0m[91m
[fastapi] - packaging==23.2
[fastapi] + packaging==26.3
[fastapi] + partial-json-parser==0.2.1.1.post7
[fastapi] [0m[91m- pillow==10.2.[0m[91m0
[fastapi] + [0m[91mpillow==12.[0m[91m3[0m[91m.0[0m[91m
[fastapi] + prometheus-fastapi-instrumentator==8.1.0
[fastapi] + pycountry==[0m[91m26.2[0m[91m.16
[fastapi] [0m[91m +[0m[91m [0m[91mpydantic-extra-types==2[0m[91m.11.[0m[91m1
[fastapi] +[0m[91m [0m[91mpydantic-settings==[0m[91m2.15[0m[91m.0[0m[91m
[fastapi] + [0m[91mpython-multipart==[0m[91m0.0.[0m[91m32
[fastapi] [0m[91m+[0m[91m [0m[91mray==2.[0m[91m58.0
[fastapi] [0m[91m+ rich[0m[91m==15.0.0
[fastapi] + [0m[91mrich-toolkit==0.20.5
[fastapi] + rignore[0m[91m==0.8.1
[fastapi] + shellingham==1[0m[91m.5[0m[91m.[0m[91m4
[fastapi] -[0m[91m sympy[0m[91m==1.12[0m[91m
[fastapi] [0m[91m+ sympy==1.13.1
[fastapi] - [0m[91mtorch==2.4.1+[0m[91mcu124
[fastapi] + torch==2.6.0
[fastapi] - torchaudio==2[0m[91m.4.1+cu124
[fastapi] + torchaudio[0m[91m==2.6[0m[91m.0[0m[91m
[fastapi] - torchvision[0m[91m==0.19.1+[0m[91mcu124
[fastapi] + torchvision[0m[91m==0.21[0m[91m.0
[fastapi] -[0m[91m triton==3[0m[91m.0.0[0m[91m
[fastapi] + [0m[91mtriton==3.[0m[91m2.0
[fastapi] [0m[91m- typer[0m[91m==0.9[0m[91m.0
[fastapi] + typer==0.27.2
[fastapi] [0m[91m + uvloop==0.22.1[0m[91m
[fastapi] +[0m[91m vllm==0.8.3
[fastapi] + watchfiles==1[0m[91m.2.0
[fastapi] + websockets[0m[91m==17.1
[fastapi] + xformers[0m[91m==0.0.29.post2
[fastapi] [0m[91m + xgrammar==0.[0m[91m1.17
[fastapi] [0mCollecting fiber@ git+https://github.com/rayonlabs/fiber.git@2.4.0
[fastapi] Cloning https://github.com/rayonlabs/fiber.git (to revision 2.4.0) to /tmp/pip-install-sx04cdie/fiber_24421a460ecc4f428b50b8a385a252f3
[fastapi] [91m  Running command git clone --filter=blob:none --quiet https://github.com/rayonlabs/fiber.git /tmp/pip-install-sx04cdie/fiber_24421a460ecc4f428b50b8a385a252f3
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
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 552.2/552.2 kB 52.6 MB/s eta 0:00:00
[fastapi] Downloading eth_typing-5.0.0-py3-none-any.whl (20 kB)
[fastapi] Downloading netaddr-1.3.0-py3-none-any.whl (2.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.3/2.3 MB 188.5 MB/s eta 0:00:00
[fastapi] Downloading python_dotenv-1.0.1-py3-none-any.whl (19 kB)
[fastapi] Downloading substrate_interface-1.7.10-py3-none-any.whl (60 kB)
[fastapi] Downloading tenacity-9.0.0-py3-none-any.whl (28 kB)
[fastapi] Downloading async_substrate_interface-1.6.4-py3-none-any.whl (97 kB)
[fastapi] Downloading bt_decode-0.8.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (647 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 647.8/647.8 kB 96.5 MB/s eta 0:00:00
[fastapi] Downloading colorama-0.4.6-py2.py3-none-any.whl (25 kB)
[fastapi] Downloading pydantic-2.9.2-py3-none-any.whl (434 kB)
[fastapi] Downloading pydantic_core-2.23.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 206.3 MB/s eta 0:00:00
[fastapi] Downloading aiosqlite-0.22.1-py3-none-any.whl (17 kB)
[fastapi] Downloading base58-2.1.1-py3-none-any.whl (5.6 kB)
[fastapi] Downloading ecdsa-0.19.2-py2.py3-none-any.whl (150 kB)
[fastapi] Downloading eth_keys-0.8.0-py3-none-any.whl (20 kB)
[fastapi] Downloading eth_utils-2.3.2-py3-none-any.whl (77 kB)
[fastapi] Downloading py_bip39_bindings-0.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (432 kB)
[fastapi] Downloading py_ed25519_zebra_bindings-1.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (323 kB)
[fastapi] Downloading py_sr25519_bindings-0.2.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (372 kB)
[fastapi] Downloading pynacl-1.6.2-cp38-abi3-manylinux_2_34_x86_64.whl (1.4 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.4/1.4 MB 157.0 MB/s eta 0:00:00
[fastapi] Downloading scalecodec-1.2.12-py3-none-any.whl (99 kB)
[fastapi] Downloading xxhash-3.8.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (220 kB)
[fastapi] Downloading cytoolz-1.1.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (2.8 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.8/2.8 MB 192.5 MB/s eta 0:00:00
[fastapi] Downloading eth_hash-0.8.0-py3-none-any.whl (8.0 kB)
[fastapi] Downloading toolz-1.1.0-py3-none-any.whl (58 kB)
[fastapi] Building wheels for collected packages: fiber
[fastapi] Building wheel for fiber (pyproject.toml): started
[fastapi] Building wheel for fiber (pyproject.toml): finished with status 'done'
[fastapi] Created wheel for fiber: filename=fiber-2.4.0-py3-none-any.whl size=51790 sha256=c50f803eff2fbcdf01560cfffdc65a3891a75b0b315d61d842fd3861f51b5d73
[fastapi] Stored in directory: /tmp/pip-ephem-wheel-cache-o3xdvq9_/wheels/d1/5e/21/2fa1f403cd187996037f04f6328bf11973ce31440a275f6949
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
[fastapi] [0m ---> 11af04e86dcd
[fastapi] Step 13/14 : RUN python -m venv --system-site-packages /workspace/v5_py &&     /workspace/v5_py/bin/pip install --no-cache-dir "transformers==5.12.1" "peft==0.19.1" &&     /workspace/v5_py/bin/pip install --no-cache-dir "bitsandbytes==0.50.1" &&     (/workspace/v5_py/bin/pip uninstall -y         nvidia-cublas-cu12 nvidia-cuda-cupti-cu12 nvidia-cuda-nvrtc-cu12         nvidia-cuda-runtime-cu12 nvidia-cudnn-cu12 nvidia-cufft-cu12         nvidia-curand-cu12 nvidia-cusolver-cu12 nvidia-cusparse-cu12         nvidia-nccl-cu12 nvidia-nvjitlink-cu12 nvidia-nvtx-cu12 || true) &&     (/workspace/v5_py/bin/pip install --no-cache-dir --upgrade trl || true)
[fastapi] ---> Running in fdd120fe4e32
[fastapi] Collecting transformers==5.12.1
[fastapi] Downloading transformers-5.12.1-py3-none-any.whl.metadata (33 kB)
[fastapi] Collecting peft==0.19.1
[fastapi] Downloading peft-0.19.1-py3-none-any.whl.metadata (15 kB)
[fastapi] Collecting huggingface-hub<2.0,>=1.5.0 (from transformers==5.12.1)
[fastapi] Downloading huggingface_hub-1.31.0-py3-none-any.whl.metadata (16 kB)
[fastapi] Requirement already satisfied: numpy>=1.17 in /usr/local/lib/python3.11/dist-packages (from transformers==5.12.1) (2.1.3)
[fastapi] Requirement already satisfied: packaging>=20.0 in /usr/local/lib/python3.11/dist-packages (from transformers==5.12.1) (26.3)
[fastapi] Requirement already satisfied: pyyaml>=5.1 in /usr/local/lib/python3.11/dist-packages (from transformers==5.12.1) (6.0.2)
[fastapi] Requirement already satisfied: regex>=2025.10.22 in /usr/local/lib/python3.11/dist-packages (from transformers==5.12.1) (2026.9.10)
[fastapi] Collecting tokenizers<=0.23.0,>=0.22.0 (from transformers==5.12.1)
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
[fastapi] Requirement already satisfied: shellingham>=1.3.0 in /usr/local/lib/python3.11/dist-packages (from typer->transformers==5.12.1) (1.5.4)
[fastapi] Requirement already satisfied: rich>=13.8.0 in /usr/local/lib/python3.11/dist-packages (from typer->transformers==5.12.1) (15.0.0)
[fastapi] Requirement already satisfied: annotated-doc>=0.0.2 in /usr/local/lib/python3.11/dist-packages (from typer->transformers==5.12.1) (0.0.5)
[fastapi] Requirement already satisfied: anyio in /usr/local/lib/python3.11/dist-packages (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers==5.12.1) (4.15.1)
[fastapi] Requirement already satisfied: certifi in /usr/local/lib/python3.11/dist-packages (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers==5.12.1) (2024.8.30)
[fastapi] Requirement already satisfied: httpcore==1.* in /usr/local/lib/python3.11/dist-packages (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers==5.12.1) (1.0.9)
[fastapi] Requirement already satisfied: idna in /usr/local/lib/python3.11/dist-packages (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers==5.12.1) (3.19)
[fastapi] Requirement already satisfied: sniffio in /usr/local/lib/python3.11/dist-packages (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers==5.12.1) (1.3.1)
[fastapi] Requirement already satisfied: h11>=0.16 in /usr/local/lib/python3.11/dist-packages (from httpcore==1.*->httpx<1,>=0.23.0->huggingface-hub<2.0,>=1.5.0->transformers==5.12.1) (0.16.0)
[fastapi] Requirement already satisfied: markdown-it-py>=2.2.0 in /usr/local/lib/python3.11/dist-packages (from rich>=13.8.0->typer->transformers==5.12.1) (4.2.0)
[fastapi] Requirement already satisfied: pygments<3.0.0,>=2.13.0 in /usr/local/lib/python3.11/dist-packages (from rich>=13.8.0->typer->transformers==5.12.1) (2.18.0)
[fastapi] Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.11/dist-packages (from jinja2->torch>=1.13.0->peft==0.19.1) (2.1.5)
[fastapi] Requirement already satisfied: mdurl~=0.1 in /usr/local/lib/python3.11/dist-packages (from markdown-it-py>=2.2.0->rich>=13.8.0->typer->transformers==5.12.1) (0.1.2)
[fastapi] Downloading transformers-5.12.1-py3-none-any.whl (11.2 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 11.2/11.2 MB 227.7 MB/s eta 0:00:00
[fastapi] Downloading peft-0.19.1-py3-none-any.whl (680 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 680.7/680.7 kB 402.0 MB/s eta 0:00:00
[fastapi] Downloading huggingface_hub-1.31.0-py3-none-any.whl (798 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 798.3/798.3 kB 396.7 MB/s eta 0:00:00
[fastapi] Downloading tokenizers-0.22.2-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.3 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.3/3.3 MB 317.3 MB/s eta 0:00:00
[fastapi] Installing collected packages: huggingface-hub, tokenizers, transformers, peft
[fastapi] Attempting uninstall: huggingface-hub
[fastapi] Found existing installation: huggingface_hub 0.36.2
[fastapi] Not uninstalling huggingface-hub at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'huggingface_hub'. No files were found to uninstall.
[fastapi] Attempting uninstall: tokenizers
[fastapi] Found existing installation: tokenizers 0.21.4
[fastapi] Not uninstalling tokenizers at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'tokenizers'. No files were found to uninstall.
[fastapi] Attempting uninstall: transformers
[fastapi] Found existing installation: transformers 4.51.3
[fastapi] Not uninstalling transformers at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'transformers'. No files were found to uninstall.
[fastapi] Attempting uninstall: peft
[fastapi] Found existing installation: peft 0.15.1
[fastapi] Not uninstalling peft at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'peft'. No files were found to uninstall.
[fastapi] Successfully installed huggingface-hub-1.31.0 peft-0.19.1 tokenizers-0.22.2 transformers-5.12.1
[fastapi] [91m
[fastapi] [notice] A new release of pip is available: 24.0 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0mCollecting bitsandbytes==0.50.1
[fastapi] Downloading bitsandbytes-0.50.1-py3-none-manylinux_2_24_x86_64.whl.metadata (10 kB)
[fastapi] Requirement already satisfied: torch<3,>=2.4 in /usr/local/lib/python3.11/dist-packages (from bitsandbytes==0.50.1) (2.6.0)
[fastapi] Requirement already satisfied: numpy>=1.17 in /usr/local/lib/python3.11/dist-packages (from bitsandbytes==0.50.1) (2.1.3)
[fastapi] Requirement already satisfied: packaging>=20.9 in /usr/local/lib/python3.11/dist-packages (from bitsandbytes==0.50.1) (26.3)
[fastapi] Requirement already satisfied: filelock in /usr/local/lib/python3.11/dist-packages (from torch<3,>=2.4->bitsandbytes==0.50.1) (3.32.6)
[fastapi] Requirement already satisfied: typing-extensions>=4.10.0 in /usr/local/lib/python3.11/dist-packages (from torch<3,>=2.4->bitsandbytes==0.50.1) (4.16.0)
[fastapi] Requirement already satisfied: networkx in /usr/local/lib/python3.11/dist-packages (from torch<3,>=2.4->bitsandbytes==0.50.1) (3.2.1)
[fastapi] Requirement already satisfied: jinja2 in /usr/local/lib/python3.11/dist-packages (from torch<3,>=2.4->bitsandbytes==0.50.1) (3.1.6)
[fastapi] Requirement already satisfied: fsspec in /usr/local/lib/python3.11/dist-packages (from torch<3,>=2.4->bitsandbytes==0.50.1) (2024.2.0)
[fastapi] Requirement already satisfied: nvidia-cuda-nvrtc-cu12==12.4.127 in /usr/local/lib/python3.11/dist-packages (from torch<3,>=2.4->bitsandbytes==0.50.1) (12.4.127)
[fastapi] Requirement already satisfied: nvidia-cuda-runtime-cu12==12.4.127 in /usr/local/lib/python3.11/dist-packages (from torch<3,>=2.4->bitsandbytes==0.50.1) (12.4.127)
[fastapi] Requirement already satisfied: nvidia-cuda-cupti-cu12==12.4.127 in /usr/local/lib/python3.11/dist-packages (from torch<3,>=2.4->bitsandbytes==0.50.1) (12.4.127)
[fastapi] Requirement already satisfied: nvidia-cudnn-cu12==9.1.0.70 in /usr/local/lib/python3.11/dist-packages (from torch<3,>=2.4->bitsandbytes==0.50.1) (9.1.0.70)
[fastapi] Requirement already satisfied: nvidia-cublas-cu12==12.4.5.8 in /usr/local/lib/python3.11/dist-packages (from torch<3,>=2.4->bitsandbytes==0.50.1) (12.4.5.8)
[fastapi] Requirement already satisfied: nvidia-cufft-cu12==11.2.1.3 in /usr/local/lib/python3.11/dist-packages (from torch<3,>=2.4->bitsandbytes==0.50.1) (11.2.1.3)
[fastapi] Requirement already satisfied: nvidia-curand-cu12==10.3.5.147 in /usr/local/lib/python3.11/dist-packages (from torch<3,>=2.4->bitsandbytes==0.50.1) (10.3.5.147)
[fastapi] Requirement already satisfied: nvidia-cusolver-cu12==11.6.1.9 in /usr/local/lib/python3.11/dist-packages (from torch<3,>=2.4->bitsandbytes==0.50.1) (11.6.1.9)
[fastapi] Requirement already satisfied: nvidia-cusparse-cu12==12.3.1.170 in /usr/local/lib/python3.11/dist-packages (from torch<3,>=2.4->bitsandbytes==0.50.1) (12.3.1.170)
[fastapi] Requirement already satisfied: nvidia-cusparselt-cu12==0.6.2 in /usr/local/lib/python3.11/dist-packages (from torch<3,>=2.4->bitsandbytes==0.50.1) (0.6.2)
[fastapi] Requirement already satisfied: nvidia-nccl-cu12==2.21.5 in /usr/local/lib/python3.11/dist-packages (from torch<3,>=2.4->bitsandbytes==0.50.1) (2.21.5)
[fastapi] Requirement already satisfied: nvidia-nvtx-cu12==12.4.127 in /usr/local/lib/python3.11/dist-packages (from torch<3,>=2.4->bitsandbytes==0.50.1) (12.4.127)
[fastapi] Requirement already satisfied: nvidia-nvjitlink-cu12==12.4.127 in /usr/local/lib/python3.11/dist-packages (from torch<3,>=2.4->bitsandbytes==0.50.1) (12.4.127)
[fastapi] Requirement already satisfied: triton==3.2.0 in /usr/local/lib/python3.11/dist-packages (from torch<3,>=2.4->bitsandbytes==0.50.1) (3.2.0)
[fastapi] Requirement already satisfied: sympy==1.13.1 in /usr/local/lib/python3.11/dist-packages (from torch<3,>=2.4->bitsandbytes==0.50.1) (1.13.1)
[fastapi] Requirement already satisfied: mpmath<1.4,>=1.1.0 in /usr/local/lib/python3.11/dist-packages (from sympy==1.13.1->torch<3,>=2.4->bitsandbytes==0.50.1) (1.3.0)
[fastapi] Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.11/dist-packages (from jinja2->torch<3,>=2.4->bitsandbytes==0.50.1) (2.1.5)
[fastapi] Downloading bitsandbytes-0.50.1-py3-none-manylinux_2_24_x86_64.whl (41.0 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 41.0/41.0 MB 162.7 MB/s eta 0:00:00
[fastapi] Installing collected packages: bitsandbytes
[fastapi] Attempting uninstall: bitsandbytes
[fastapi] Found existing installation: bitsandbytes 0.45.4
[fastapi] Not uninstalling bitsandbytes at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'bitsandbytes'. No files were found to uninstall.
[fastapi] Successfully installed bitsandbytes-0.50.1
[fastapi] [91m
[fastapi] [notice] A new release of pip is available: 24.0 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0mFound existing installation: nvidia-cublas-cu12 12.4.5.8
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
[fastapi] Found existing installation: nvidia-nccl-cu12 2.21.5
[fastapi] Not uninstalling nvidia-nccl-cu12 at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'nvidia-nccl-cu12'. No files were found to uninstall.
[fastapi] Found existing installation: nvidia-nvjitlink-cu12 12.4.127
[fastapi] Not uninstalling nvidia-nvjitlink-cu12 at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'nvidia-nvjitlink-cu12'. No files were found to uninstall.
[fastapi] Found existing installation: nvidia-nvtx-cu12 12.4.127
[fastapi] Not uninstalling nvidia-nvtx-cu12 at /usr/local/lib/python3.11/dist-packages, outside environment /workspace/v5_py
[fastapi] Can't uninstall 'nvidia-nvtx-cu12'. No files were found to uninstall.
[fastapi] Requirement already satisfied: trl in /usr/local/lib/python3.11/dist-packages (0.18.0)
[fastapi] Collecting trl
[fastapi] Downloading trl-1.13.0-py3-none-any.whl.metadata (12 kB)
[fastapi] Requirement already satisfied: accelerate>=1.4.0 in /usr/local/lib/python3.11/dist-packages (from trl) (1.6.0)
[fastapi] Collecting datasets>=4.7.0 (from trl)
[fastapi] Downloading datasets-5.0.1-py3-none-any.whl.metadata (23 kB)
[fastapi] Requirement already satisfied: jinja2 in /usr/local/lib/python3.11/dist-packages (from trl) (3.1.6)
[fastapi] Requirement already satisfied: packaging>20.0 in /usr/local/lib/python3.11/dist-packages (from trl) (26.3)
[fastapi] Requirement already satisfied: transformers>=4.56.2 in /workspace/v5_py/lib/python3.11/site-packages (from trl) (5.12.1)
[fastapi] Requirement already satisfied: numpy<3.0.0,>=1.17 in /usr/local/lib/python3.11/dist-packages (from accelerate>=1.4.0->trl) (2.1.3)
[fastapi] Requirement already satisfied: psutil in /usr/local/lib/python3.11/dist-packages (from accelerate>=1.4.0->trl) (6.0.0)
[fastapi] Requirement already satisfied: pyyaml in /usr/local/lib/python3.11/dist-packages (from accelerate>=1.4.0->trl) (6.0.2)
[fastapi] Requirement already satisfied: torch>=2.0.0 in /usr/local/lib/python3.11/dist-packages (from accelerate>=1.4.0->trl) (2.6.0)
[fastapi] Requirement already satisfied: huggingface-hub>=0.21.0 in /workspace/v5_py/lib/python3.11/site-packages (from accelerate>=1.4.0->trl) (1.31.0)
[fastapi] Requirement already satisfied: safetensors>=0.4.3 in /usr/local/lib/python3.11/dist-packages (from accelerate>=1.4.0->trl) (0.8.0)
[fastapi] Requirement already satisfied: filelock in /usr/local/lib/python3.11/dist-packages (from datasets>=4.7.0->trl) (3.32.6)
[fastapi] Requirement already satisfied: pyarrow>=21.0.0 in /usr/local/lib/python3.11/dist-packages (from datasets>=4.7.0->trl) (25.0.1)
[fastapi] Requirement already satisfied: dill<0.4.2,>=0.3.0 in /usr/local/lib/python3.11/dist-packages (from datasets>=4.7.0->trl) (0.3.8)
[fastapi] Requirement already satisfied: pandas in /usr/local/lib/python3.11/dist-packages (from datasets>=4.7.0->trl) (2.2.3)
[fastapi] Requirement already satisfied: requests>=2.32.2 in /usr/local/lib/python3.11/dist-packages (from datasets>=4.7.0->trl) (2.32.3)
[fastapi] Requirement already satisfied: httpx<1.0.0 in /usr/local/lib/python3.11/dist-packages (from datasets>=4.7.0->trl) (0.27.2)
[fastapi] Requirement already satisfied: tqdm>=4.66.3 in /usr/local/lib/python3.11/dist-packages (from datasets>=4.7.0->trl) (4.70.1)
[fastapi] Requirement already satisfied: xxhash in /usr/local/lib/python3.11/dist-packages (from datasets>=4.7.0->trl) (3.8.1)
[fastapi] Requirement already satisfied: multiprocess<0.70.20 in /usr/local/lib/python3.11/dist-packages (from datasets>=4.7.0->trl) (0.70.16)
[fastapi] Requirement already satisfied: fsspec<=2026.6.0,>=2023.1.0 in /usr/local/lib/python3.11/dist-packages (from fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=4.7.0->trl) (2024.2.0)
[fastapi] Requirement already satisfied: regex>=2025.10.22 in /usr/local/lib/python3.11/dist-packages (from transformers>=4.56.2->trl) (2026.9.10)
[fastapi] Requirement already satisfied: tokenizers<=0.23.0,>=0.22.0 in /workspace/v5_py/lib/python3.11/site-packages (from transformers>=4.56.2->trl) (0.22.2)
[fastapi] Requirement already satisfied: typer in /usr/local/lib/python3.11/dist-packages (from transformers>=4.56.2->trl) (0.27.2)
[fastapi] Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.11/dist-packages (from jinja2->trl) (2.1.5)
[fastapi] Requirement already satisfied: aiohttp!=4.0.0a0,!=4.0.0a1 in /usr/local/lib/python3.11/dist-packages (from fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=4.7.0->trl) (3.14.3)
[fastapi] Requirement already satisfied: anyio in /usr/local/lib/python3.11/dist-packages (from httpx<1.0.0->datasets>=4.7.0->trl) (4.15.1)
[fastapi] Requirement already satisfied: certifi in /usr/local/lib/python3.11/dist-packages (from httpx<1.0.0->datasets>=4.7.0->trl) (2024.8.30)
[fastapi] Requirement already satisfied: httpcore==1.* in /usr/local/lib/python3.11/dist-packages (from httpx<1.0.0->datasets>=4.7.0->trl) (1.0.9)
[fastapi] Requirement already satisfied: idna in /usr/local/lib/python3.11/dist-packages (from httpx<1.0.0->datasets>=4.7.0->trl) (3.19)
[fastapi] Requirement already satisfied: sniffio in /usr/local/lib/python3.11/dist-packages (from httpx<1.0.0->datasets>=4.7.0->trl) (1.3.1)
[fastapi] Requirement already satisfied: h11>=0.16 in /usr/local/lib/python3.11/dist-packages (from httpcore==1.*->httpx<1.0.0->datasets>=4.7.0->trl) (0.16.0)
[fastapi] Requirement already satisfied: click<9.0.0,>=8.4.2 in /usr/local/lib/python3.11/dist-packages (from huggingface-hub>=0.21.0->accelerate>=1.4.0->trl) (8.5.0)
[fastapi] Requirement already satisfied: hf-xet<2.0.0,>=1.5.2 in /usr/local/lib/python3.11/dist-packages (from huggingface-hub>=0.21.0->accelerate>=1.4.0->trl) (1.6.0)
[fastapi] Requirement already satisfied: typing-extensions>=4.1.0 in /usr/local/lib/python3.11/dist-packages (from huggingface-hub>=0.21.0->accelerate>=1.4.0->trl) (4.16.0)
[fastapi] Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.11/dist-packages (from requests>=2.32.2->datasets>=4.7.0->trl) (3.3.2)
[fastapi] Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.11/dist-packages (from requests>=2.32.2->datasets>=4.7.0->trl) (2.2.3)
[fastapi] Requirement already satisfied: networkx in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl) (3.2.1)
[fastapi] Requirement already satisfied: nvidia-cuda-nvrtc-cu12==12.4.127 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl) (12.4.127)
[fastapi] Requirement already satisfied: nvidia-cuda-runtime-cu12==12.4.127 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl) (12.4.127)
[fastapi] Requirement already satisfied: nvidia-cuda-cupti-cu12==12.4.127 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl) (12.4.127)
[fastapi] Requirement already satisfied: nvidia-cudnn-cu12==9.1.0.70 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl) (9.1.0.70)
[fastapi] Requirement already satisfied: nvidia-cublas-cu12==12.4.5.8 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl) (12.4.5.8)
[fastapi] Requirement already satisfied: nvidia-cufft-cu12==11.2.1.3 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl) (11.2.1.3)
[fastapi] Requirement already satisfied: nvidia-curand-cu12==10.3.5.147 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl) (10.3.5.147)
[fastapi] Requirement already satisfied: nvidia-cusolver-cu12==11.6.1.9 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl) (11.6.1.9)
[fastapi] Requirement already satisfied: nvidia-cusparse-cu12==12.3.1.170 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl) (12.3.1.170)
[fastapi] Requirement already satisfied: nvidia-cusparselt-cu12==0.6.2 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl) (0.6.2)
[fastapi] Requirement already satisfied: nvidia-nccl-cu12==2.21.5 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl) (2.21.5)
[fastapi] Requirement already satisfied: nvidia-nvtx-cu12==12.4.127 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl) (12.4.127)
[fastapi] Requirement already satisfied: nvidia-nvjitlink-cu12==12.4.127 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl) (12.4.127)
[fastapi] Requirement already satisfied: triton==3.2.0 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl) (3.2.0)
[fastapi] Requirement already satisfied: sympy==1.13.1 in /usr/local/lib/python3.11/dist-packages (from torch>=2.0.0->accelerate>=1.4.0->trl) (1.13.1)
[fastapi] Requirement already satisfied: mpmath<1.4,>=1.1.0 in /usr/local/lib/python3.11/dist-packages (from sympy==1.13.1->torch>=2.0.0->accelerate>=1.4.0->trl) (1.3.0)
[fastapi] Requirement already satisfied: python-dateutil>=2.8.2 in /usr/local/lib/python3.11/dist-packages (from pandas->datasets>=4.7.0->trl) (2.9.0.post0)
[fastapi] Requirement already satisfied: pytz>=2020.1 in /usr/local/lib/python3.11/dist-packages (from pandas->datasets>=4.7.0->trl) (2026.3.post1)
[fastapi] Requirement already satisfied: tzdata>=2022.7 in /usr/local/lib/python3.11/dist-packages (from pandas->datasets>=4.7.0->trl) (2026.4)
[fastapi] Requirement already satisfied: shellingham>=1.3.0 in /usr/local/lib/python3.11/dist-packages (from typer->transformers>=4.56.2->trl) (1.5.4)
[fastapi] Requirement already satisfied: rich>=13.8.0 in /usr/local/lib/python3.11/dist-packages (from typer->transformers>=4.56.2->trl) (15.0.0)
[fastapi] Requirement already satisfied: annotated-doc>=0.0.2 in /usr/local/lib/python3.11/dist-packages (from typer->transformers>=4.56.2->trl) (0.0.5)
[fastapi] Requirement already satisfied: aiohappyeyeballs>=2.5.0 in /usr/local/lib/python3.11/dist-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=4.7.0->trl) (2.7.1)
[fastapi] Requirement already satisfied: aiosignal>=1.4.0 in /usr/local/lib/python3.11/dist-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=4.7.0->trl) (1.4.0)
[fastapi] Requirement already satisfied: attrs>=17.3.0 in /usr/local/lib/python3.11/dist-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=4.7.0->trl) (24.2.0)
[fastapi] Requirement already satisfied: frozenlist>=1.1.1 in /usr/local/lib/python3.11/dist-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=4.7.0->trl) (1.8.0)
[fastapi] Requirement already satisfied: multidict<7.0,>=4.5 in /usr/local/lib/python3.11/dist-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=4.7.0->trl) (6.8.0)
[fastapi] Requirement already satisfied: propcache>=0.2.0 in /usr/local/lib/python3.11/dist-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=4.7.0->trl) (0.5.2)
[fastapi] Requirement already satisfied: yarl<2.0,>=1.17.0 in /usr/local/lib/python3.11/dist-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.6.0,>=2023.1.0->datasets>=4.7.0->trl) (1.24.5)
[fastapi] Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.11/dist-packages (from python-dateutil>=2.8.2->pandas->datasets>=4.7.0->trl) (1.17.0)
[fastapi] Requirement already satisfied: markdown-it-py>=2.2.0 in /usr/local/lib/python3.11/dist-packages (from rich>=13.8.0->typer->transformers>=4.56.2->trl) (4.2.0)
[fastapi] Requirement already satisfied: pygments<3.0.0,>=2.13.0 in /usr/local/lib/python3.11/dist-packages (from rich>=13.8.0->typer->transformers>=4.56.2->trl) (2.18.0)
[fastapi] Requirement already satisfied: mdurl~=0.1 in /usr/local/lib/python3.11/dist-packages (from markdown-it-py>=2.2.0->rich>=13.8.0->typer->transformers>=4.56.2->trl) (0.1.2)
[fastapi] Downloading trl-1.13.0-py3-none-any.whl (1.0 MB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.0/1.0 MB 21.3 MB/s eta 0:00:00
[fastapi] Downloading datasets-5.0.1-py3-none-any.whl (559 kB)
[fastapi] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 559.1/559.1 kB 69.7 MB/s eta 0:00:00
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
[fastapi] [91m
[fastapi] [notice] A new release of pip is available: 24.0 -> 26.2.1
[fastapi] [notice] To update, run: python -m pip install --upgrade pip
[fastapi] [0m ---> 8a6ef304ebb1
[fastapi] Step 14/14 : ENTRYPOINT ["./entrypoint.sh"]
[fastapi] ---> Running in 1dd9a367c1d6
[fastapi] ---> 76db0da9a75a
[fastapi] {'aux': {'ID': 'sha256:76db0da9a75a17e3759433b1b11f138fc1545e548f999d5f19c68cb8a20e65e8'}}Successfully built 76db0da9a75a
[fastapi] Successfully tagged standalone-text-trainer:d894466b-eed8-446f-918c-c4fe097799e2
[fastapi] Docker image built successfully.
[fastapi] Container.wait() returned: {'StatusCode': 0}
[fastapi] Cleaning up
[fastapi] Cleaned up Docker resources.
[fastapi] Starting upload container hf-upload-2a93b29334df47e48123f82702d079df for task 87c51c39-914b-4c7f-a97a-4925c6ec58b3...
[hf-upload-2a]  adapter_config.json not found
[hf-upload-2a] README.md not found
[hf-upload-2a] Creating repo gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5DXVNvDm...
[hf-upload-2a] Uploading contents of /app/checkpoints/87c51c39-914b-4c7f-a97a-4925c6ec58b3/tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5DXVNvDm to gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5DXVNvDm
[hf-upload-2a] Uploaded successfully to https://huggingface.co/gradients-io-tournaments/tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5DXVNvDm
[hf-upload-2a] Deleted local folder: /app/checkpoints/87c51c39-914b-4c7f-a97a-4925c6ec58b3/tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5DXVNvDm
[text-trainer] [infra-audit] timestamp: 2026-09-15T11:50:47+00:00
[text-trainer] [infra-audit] /dev/shm df: shm             8.0G     0  8.0G   0% /dev/shm
[text-trainer] [infra-audit] /dev/shm size_kb: 8388608
[text-trainer] [infra-audit] /dev/shm used: 0	/dev/shm
[text-trainer] [infra-audit] NCCL_SHM_DISABLE (validator-set): unset
[text-trainer] [infra-audit] NCCL_P2P_DISABLE (validator-set): unset
[text-trainer] [infra-audit] NCCL_DEBUG (validator-set): unset
[text-trainer] [infra-audit] NCCL_IB_DISABLE (validator-set): unset
[text-trainer] [infra-audit] CUDA_VISIBLE_DEVICES: unset
[text-trainer] [infra-audit] nvidia-smi -L:
[text-trainer] [infra-audit]   GPU 0: NVIDIA H100 80GB HBM3 (UUID: GPU-ed3519cc-01a1-7bb4-f206-ae4d86d3bc45)
[text-trainer] [infra-audit] nvidia-smi topo -m:
[text-trainer] [infra-audit]   	[4mGPU0	NIC0	CPU Affinity	NUMA Affinity	GPU NUMA ID[0m
[text-trainer] [infra-audit]   GPU0	 X 	PHB	0-103	0		N/A
[text-trainer] [infra-audit]   NIC0	PHB	 X 				
[text-trainer] [infra-audit]   
[text-trainer] [infra-audit]   Legend:
[text-trainer] [infra-audit]   
[text-trainer] [infra-audit]     X    = Self
[text-trainer] [infra-audit]     SYS  = Connection traversing PCIe as well as the SMP interconnect between NUMA nodes (e.g., QPI/UPI)
[text-trainer] [infra-audit]     NODE = Connection traversing PCIe as well as the interconnect between PCIe Host Bridges within a NUMA node
[text-trainer] [infra-audit]     PHB  = Connection traversing PCIe as well as a PCIe Host Bridge (typically the CPU)
[text-trainer] [infra-audit]     PXB  = Connection traversing multiple PCIe bridges (without traversing the PCIe Host Bridge)
[text-trainer] [infra-audit]     PIX  = Connection traversing at most a single PCIe bridge
[text-trainer] [infra-audit]     NV#  = Connection traversing a bonded set of # NVLinks
[text-trainer] [infra-audit]   
[text-trainer] [infra-audit]   NIC Legend:
[text-trainer] [infra-audit] -- end --
[text-trainer] [CUDA Allocator] PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
[text-trainer] [CUDA Health] running pre-flight check...
[text-trainer] [CUDA Health] OK: 1 GPU(s) accessible
[text-trainer] [stack-select] model_type=qwen2 known to v4 -> default
[text-trainer] [stack-select] interpreter: default
[text-trainer] *****Running text trainer
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_hash" in MinerSubmission has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] /workspace/axo_py/lib/python3.11/site-packages/requests/__init__.py:113: RequestsDependencyWarning: urllib3 (2.7.0) or chardet (6.0.0.post1)/charset_normalizer (3.5.1) doesn't match a supported version!
[text-trainer]   warnings.warn(
[text-trainer] [dyn-pad] skipped
[text-trainer] [dyn-pad] dev armed
[text-trainer] [LR-finder] off (default)
[text-trainer] df: /root/.triton/autotune: No such file or directory
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] wandb: WARNING The `run_name` is currently set to the same value as `TrainingArguments.output_dir`. If this was not intended, please specify a different run name by setting the `TrainingArguments.run_name` parameter.
[text-trainer] wandb: Tracking run with wandb version 0.19.10
[text-trainer] wandb: W&B syncing is set to `offline` in this directory. Run `wandb online` or set WANDB_MODE=online to enable cloud syncing.
[text-trainer] [eval-batch] token-budget active
[text-trainer] [macro-eval] active
[text-trainer] [1;34mwandb[0m: 
[text-trainer] [1;34mwandb[0m: You can sync this run to the cloud by running:
[text-trainer] [1;34mwandb[0m: [1mwandb sync /app/checkpoints/wandb_logs/87c51c39-914b-4c7f-a97a-4925c6ec58b3_5DXVNvDmGZqdXbqRzsJZdJVoAgbLdhdFrrrmtAAfsh4QkGUU/wandb/offline-run-20260915_115306-87c51c39-914b-4c7f-a97a-4925c6ec58b3_tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5DXVNvDm[0m
[text-trainer] [1;34mwandb[0m: Find logs at: [1;35m../../app/checkpoints/wandb_logs/87c51c39-914b-4c7f-a97a-4925c6ec58b3_5DXVNvDmGZqdXbqRzsJZdJVoAgbLdhdFrrrmtAAfsh4QkGUU/wandb/offline-run-20260915_115306-87c51c39-914b-4c7f-a97a-4925c6ec58b3_tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5DXVNvDm/logs[0m
[text-trainer] [dyn-pad] skipped
[text-trainer] [dyn-pad] dev armed
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] wandb: WARNING The `run_name` is currently set to the same value as `TrainingArguments.output_dir`. If this was not intended, please specify a different run name by setting the `TrainingArguments.run_name` parameter.
[text-trainer] wandb: Tracking run with wandb version 0.19.10
[text-trainer] wandb: W&B syncing is set to `offline` in this directory. Run `wandb online` or set WANDB_MODE=online to enable cloud syncing.
[text-trainer] [eval-batch] token-budget active
[text-trainer] [macro-eval] active
[text-trainer] [1;34mwandb[0m: 
[text-trainer] [1;34mwandb[0m: You can sync this run to the cloud by running:
[text-trainer] [1;34mwandb[0m: [1mwandb sync /app/checkpoints/wandb_logs/87c51c39-914b-4c7f-a97a-4925c6ec58b3_5DXVNvDmGZqdXbqRzsJZdJVoAgbLdhdFrrrmtAAfsh4QkGUU/wandb/offline-run-20260915_115456-87c51c39-914b-4c7f-a97a-4925c6ec58b3_tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5DXVNvDm[0m
[text-trainer] [1;34mwandb[0m: Find logs at: [1;35m../../app/checkpoints/wandb_logs/87c51c39-914b-4c7f-a97a-4925c6ec58b3_5DXVNvDmGZqdXbqRzsJZdJVoAgbLdhdFrrrmtAAfsh4QkGUU/wandb/offline-run-20260915_115456-87c51c39-914b-4c7f-a97a-4925c6ec58b3_tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5DXVNvDm/logs[0m
[text-trainer] /workspace/scripts/bo_augmentation.py:328: ExperimentalWarning: GPSampler is experimental (supported from v3.6.0). The interface can change in the future.
[text-trainer]   sampler=GPSampler(
[text-trainer] [dyn-pad] skipped
[text-trainer] [dyn-pad] dev armed
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] wandb: WARNING The `run_name` is currently set to the same value as `TrainingArguments.output_dir`. If this was not intended, please specify a different run name by setting the `TrainingArguments.run_name` parameter.
[text-trainer] wandb: Tracking run with wandb version 0.19.10
[text-trainer] wandb: W&B syncing is set to `offline` in this directory. Run `wandb online` or set WANDB_MODE=online to enable cloud syncing.
[text-trainer] [eval-batch] token-budget active
[text-trainer] [macro-eval] active
[text-trainer] [1;34mwandb[0m: 
[text-trainer] [1;34mwandb[0m: You can sync this run to the cloud by running:
[text-trainer] [1;34mwandb[0m: [1mwandb sync /app/checkpoints/wandb_logs/87c51c39-914b-4c7f-a97a-4925c6ec58b3_5DXVNvDmGZqdXbqRzsJZdJVoAgbLdhdFrrrmtAAfsh4QkGUU/wandb/offline-run-20260915_115641-87c51c39-914b-4c7f-a97a-4925c6ec58b3_tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5DXVNvDm[0m
[text-trainer] [1;34mwandb[0m: Find logs at: [1;35m../../app/checkpoints/wandb_logs/87c51c39-914b-4c7f-a97a-4925c6ec58b3_5DXVNvDmGZqdXbqRzsJZdJVoAgbLdhdFrrrmtAAfsh4QkGUU/wandb/offline-run-20260915_115641-87c51c39-914b-4c7f-a97a-4925c6ec58b3_tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5DXVNvDm/logs[0m
[text-trainer] [dyn-pad] skipped
[text-trainer] [dyn-pad] dev armed
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] wandb: WARNING The `run_name` is currently set to the same value as `TrainingArguments.output_dir`. If this was not intended, please specify a different run name by setting the `TrainingArguments.run_name` parameter.
[text-trainer] wandb: Tracking run with wandb version 0.19.10
[text-trainer] wandb: W&B syncing is set to `offline` in this directory. Run `wandb online` or set WANDB_MODE=online to enable cloud syncing.
[text-trainer] [eval-batch] token-budget active
[text-trainer] [macro-eval] active
[text-trainer] [1;34mwandb[0m: 
[text-trainer] [1;34mwandb[0m: You can sync this run to the cloud by running:
[text-trainer] [1;34mwandb[0m: [1mwandb sync /app/checkpoints/wandb_logs/87c51c39-914b-4c7f-a97a-4925c6ec58b3_5DXVNvDmGZqdXbqRzsJZdJVoAgbLdhdFrrrmtAAfsh4QkGUU/wandb/offline-run-20260915_115825-87c51c39-914b-4c7f-a97a-4925c6ec58b3_tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5DXVNvDm[0m
[text-trainer] [1;34mwandb[0m: Find logs at: [1;35m../../app/checkpoints/wandb_logs/87c51c39-914b-4c7f-a97a-4925c6ec58b3_5DXVNvDmGZqdXbqRzsJZdJVoAgbLdhdFrrrmtAAfsh4QkGUU/wandb/offline-run-20260915_115825-87c51c39-914b-4c7f-a97a-4925c6ec58b3_tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5DXVNvDm/logs[0m
[text-trainer] [dyn-pad] skipped
[text-trainer] [dyn-pad] dev armed
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] wandb: WARNING The `run_name` is currently set to the same value as `TrainingArguments.output_dir`. If this was not intended, please specify a different run name by setting the `TrainingArguments.run_name` parameter.
[text-trainer] wandb: Tracking run with wandb version 0.19.10
[text-trainer] wandb: W&B syncing is set to `offline` in this directory. Run `wandb online` or set WANDB_MODE=online to enable cloud syncing.
[text-trainer] [eval-batch] token-budget active
[text-trainer] [macro-eval] active
[text-trainer] [1;34mwandb[0m: 
[text-trainer] [1;34mwandb[0m: You can sync this run to the cloud by running:
[text-trainer] [1;34mwandb[0m: [1mwandb sync /app/checkpoints/wandb_logs/87c51c39-914b-4c7f-a97a-4925c6ec58b3_5DXVNvDmGZqdXbqRzsJZdJVoAgbLdhdFrrrmtAAfsh4QkGUU/wandb/offline-run-20260915_120010-87c51c39-914b-4c7f-a97a-4925c6ec58b3_tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5DXVNvDm[0m
[text-trainer] [1;34mwandb[0m: Find logs at: [1;35m../../app/checkpoints/wandb_logs/87c51c39-914b-4c7f-a97a-4925c6ec58b3_5DXVNvDmGZqdXbqRzsJZdJVoAgbLdhdFrrrmtAAfsh4QkGUU/wandb/offline-run-20260915_120010-87c51c39-914b-4c7f-a97a-4925c6ec58b3_tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5DXVNvDm/logs[0m
[text-trainer] [wsd] final scheduler switched (explore)
[text-trainer] [dyn-pad] skipped
[text-trainer] [dyn-pad] dev armed
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] /usr/local/lib/python3.11/dist-packages/transformers/optimization.py:475: UserWarning: Both num_training_steps and num_stable_steps are specified. num_stable_steps will be used.
[text-trainer]   warnings.warn("Both num_training_steps and num_stable_steps are specified. num_stable_steps will be used.")
[text-trainer] wandb: WARNING The `run_name` is currently set to the same value as `TrainingArguments.output_dir`. If this was not intended, please specify a different run name by setting the `TrainingArguments.run_name` parameter.
[text-trainer] wandb: Tracking run with wandb version 0.19.10
[text-trainer] wandb: W&B syncing is set to `offline` in this directory. Run `wandb online` or set WANDB_MODE=online to enable cloud syncing.
[text-trainer] [eval-batch] token-budget active
[text-trainer] [macro-eval] active
[text-trainer] /usr/local/lib/python3.11/dist-packages/transformers/optimization.py:475: UserWarning: Both num_training_steps and num_stable_steps are specified. num_stable_steps will be used.
[text-trainer]   warnings.warn("Both num_training_steps and num_stable_steps are specified. num_stable_steps will be used.")
[text-trainer] [wsm] edge-blocked
[text-trainer] [ship-telemetry] recorded (7652B)
[text-trainer] [1;34mwandb[0m: 
[text-trainer] [1;34mwandb[0m: You can sync this run to the cloud by running:
[text-trainer] [1;34mwandb[0m: [1mwandb sync /app/checkpoints/wandb_logs/87c51c39-914b-4c7f-a97a-4925c6ec58b3_5DXVNvDmGZqdXbqRzsJZdJVoAgbLdhdFrrrmtAAfsh4QkGUU/wandb/offline-run-20260915_120154-87c51c39-914b-4c7f-a97a-4925c6ec58b3_tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5DXVNvDm[0m
[text-trainer] [1;34mwandb[0m: Find logs at: [1;35m../../app/checkpoints/wandb_logs/87c51c39-914b-4c7f-a97a-4925c6ec58b3_5DXVNvDmGZqdXbqRzsJZdJVoAgbLdhdFrrrmtAAfsh4QkGUU/wandb/offline-run-20260915_120154-87c51c39-914b-4c7f-a97a-4925c6ec58b3_tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5DXVNvDm/logs[0m
[text-trainer] [final2] twin-seed applied
[text-trainer] [dyn-pad] skipped
[text-trainer] [dyn-pad] dev armed
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] /usr/local/lib/python3.11/dist-packages/transformers/optimization.py:475: UserWarning: Both num_training_steps and num_stable_steps are specified. num_stable_steps will be used.
[text-trainer]   warnings.warn("Both num_training_steps and num_stable_steps are specified. num_stable_steps will be used.")
[text-trainer] wandb: WARNING The `run_name` is currently set to the same value as `TrainingArguments.output_dir`. If this was not intended, please specify a different run name by setting the `TrainingArguments.run_name` parameter.
[text-trainer] wandb: Tracking run with wandb version 0.19.10
[text-trainer] wandb: W&B syncing is set to `offline` in this directory. Run `wandb online` or set WANDB_MODE=online to enable cloud syncing.
[text-trainer] [eval-batch] token-budget active
[text-trainer] [macro-eval] active
[text-trainer] [wsm] ship: twin
[text-trainer] [ship-telemetry] recorded (1955B)
[text-trainer] [1;34mwandb[0m: 
[text-trainer] [1;34mwandb[0m: You can sync this run to the cloud by running:
[text-trainer] [1;34mwandb[0m: [1mwandb sync /app/checkpoints/wandb_logs/87c51c39-914b-4c7f-a97a-4925c6ec58b3_5DXVNvDmGZqdXbqRzsJZdJVoAgbLdhdFrrrmtAAfsh4QkGUU/wandb/offline-run-20260915_120849-87c51c39-914b-4c7f-a97a-4925c6ec58b3_tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5DXVNvDm[0m
[text-trainer] [1;34mwandb[0m: Find logs at: [1;35m../../app/checkpoints/wandb_logs/87c51c39-914b-4c7f-a97a-4925c6ec58b3_5DXVNvDmGZqdXbqRzsJZdJVoAgbLdhdFrrrmtAAfsh4QkGUU/wandb/offline-run-20260915_120849-87c51c39-914b-4c7f-a97a-4925c6ec58b3_tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5DXVNvDm/logs[0m
[text-trainer] [ship-ledger] recorded
[text-trainer] [artifact-scan] verdict=ok
[text-trainer] [dyn-pad] skipped
[text-trainer] [dyn-pad] dev armed
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] /usr/local/lib/python3.11/dist-packages/transformers/optimization.py:475: UserWarning: Both num_training_steps and num_stable_steps are specified. num_stable_steps will be used.
[text-trainer]   warnings.warn("Both num_training_steps and num_stable_steps are specified. num_stable_steps will be used.")
[text-trainer] wandb: WARNING The `run_name` is currently set to the same value as `TrainingArguments.output_dir`. If this was not intended, please specify a different run name by setting the `TrainingArguments.run_name` parameter.
[text-trainer] wandb: Tracking run with wandb version 0.19.10
[text-trainer] wandb: W&B syncing is set to `offline` in this directory. Run `wandb online` or set WANDB_MODE=online to enable cloud syncing.
[text-trainer] [eval-batch] token-budget active
[text-trainer] [macro-eval] active
[text-trainer] [1;34mwandb[0m: 
[text-trainer] [1;34mwandb[0m: You can sync this run to the cloud by running:
[text-trainer] [1;34mwandb[0m: [1mwandb sync /app/checkpoints/wandb_logs/87c51c39-914b-4c7f-a97a-4925c6ec58b3_5DXVNvDmGZqdXbqRzsJZdJVoAgbLdhdFrrrmtAAfsh4QkGUU/wandb/offline-run-20260915_121551-87c51c39-914b-4c7f-a97a-4925c6ec58b3_tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5DXVNvDm[0m
[text-trainer] [1;34mwandb[0m: Find logs at: [1;35m../../app/checkpoints/wandb_logs/87c51c39-914b-4c7f-a97a-4925c6ec58b3_5DXVNvDmGZqdXbqRzsJZdJVoAgbLdhdFrrrmtAAfsh4QkGUU/wandb/offline-run-20260915_121551-87c51c39-914b-4c7f-a97a-4925c6ec58b3_tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5DXVNvDm/logs[0m
[text-trainer] [dyn-pad] skipped
[text-trainer] [dyn-pad] dev armed
[text-trainer] /usr/local/lib/python3.11/dist-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_name" in PromptModelConfig has conflict with protected namespace "model_".
[text-trainer] 
[text-trainer] You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
[text-trainer]   warnings.warn(
[text-trainer] /usr/local/lib/python3.11/dist-packages/transformers/optimization.py:475: UserWarning: Both num_training_steps and num_stable_steps are specified. num_stable_steps will be used.
[text-trainer]   warnings.warn("Both num_training_steps and num_stable_steps are specified. num_stable_steps will be used.")
[text-trainer] wandb: WARNING The `run_name` is currently set to the same value as `TrainingArguments.output_dir`. If this was not intended, please specify a different run name by setting the `TrainingArguments.run_name` parameter.
[text-trainer] wandb: Tracking run with wandb version 0.19.10
[text-trainer] wandb: W&B syncing is set to `offline` in this directory. Run `wandb online` or set WANDB_MODE=online to enable cloud syncing.
[text-trainer] [eval-batch] token-budget active
[text-trainer] [macro-eval] active
[text-trainer] [1;34mwandb[0m: 
[text-trainer] [1;34mwandb[0m: You can sync this run to the cloud by running:
[text-trainer] [1;34mwandb[0m: [1mwandb sync /app/checkpoints/wandb_logs/87c51c39-914b-4c7f-a97a-4925c6ec58b3_5DXVNvDmGZqdXbqRzsJZdJVoAgbLdhdFrrrmtAAfsh4QkGUU/wandb/offline-run-20260915_121732-87c51c39-914b-4c7f-a97a-4925c6ec58b3_tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5DXVNvDm[0m
[text-trainer] [1;34mwandb[0m: Find logs at: [1;35m../../app/checkpoints/wandb_logs/87c51c39-914b-4c7f-a97a-4925c6ec58b3_5DXVNvDmGZqdXbqRzsJZdJVoAgbLdhdFrrrmtAAfsh4QkGUU/wandb/offline-run-20260915_121732-87c51c39-914b-4c7f-a97a-4925c6ec58b3_tournament-tourn_5c64e784a087074a_20260914-92e83f80-9629-4499-8be5-48d2f0cdfbc7-5DXVNvDm/logs[0m