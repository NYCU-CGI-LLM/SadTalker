FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    git \
    zip \
    unzip \
    git-lfs \
    wget \
    curl \
    # ffmpeg \
    ffmpeg \
    x264 \
    # python build dependencies \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /sadtalker

RUN curl https://pyenv.run | bash

ENV PATH=/root/.pyenv/shims:/root/.pyenv/bin:${PATH}

ENV PYTHON_VERSION=3.10.9

RUN pyenv install ${PYTHON_VERSION} && \
    pyenv global ${PYTHON_VERSION} && \
    pyenv rehash && \
    pip install --no-cache-dir -U pip setuptools wheel

RUN pip install --no-cache-dir -U torch==1.12.1 torchvision==0.13.1

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -U -r /tmp/requirements.txt

COPY . /sadtalker

RUN ls -a

ENV PYTHONPATH=/sadtalker \
    PYTHONUNBUFFERED=1 \
    GRADIO_ALLOW_FLAGGING=never \
    GRADIO_NUM_PORTS=1 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    GRADIO_THEME=huggingface

# CMD ["python", "app.py"]