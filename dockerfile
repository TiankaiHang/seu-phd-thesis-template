FROM texlive/texlive:latest

# 安装必要的工具
RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 下载并安装 ctex
RUN tlmgr install ctex

# 清理缓存
RUN tlmgr option repository ctan
RUN tlmgr update --self
RUN tlmgr update --all