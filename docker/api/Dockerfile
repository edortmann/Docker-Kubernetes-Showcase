ARG PYTHON_VERSION=3.10
ARG CUDA_TAG=11.8.0-runtime-ubuntu22.04

FROM nvidia/cuda:${CUDA_TAG}

ARG PYTHON_VERSION=3.10

# ---------- system packages ----------
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python${PYTHON_VERSION} python${PYTHON_VERSION}-distutils \
        python3-pip python3-venv \
        build-essential git ca-certificates && \
    ln -s /usr/bin/python${PYTHON_VERSION} /usr/local/bin/python && \
    ln -s /usr/bin/pip3 /usr/local/bin/pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ---------- Python dependencies ----------
# 1 / Install GPU-matched PyTorch wheel first so that the later
#    `pip install -r requirements.txt` does **not** pull a CPU build.
RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
        --index-url https://download.pytorch.org/whl/cu118 \
        torch==2.3.0+cu118 \
        torchvision==0.18.0+cu118 \
        torchaudio==2.3.0+cu118

# 2 / Project requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- application code ----------
COPY src ./src

EXPOSE 8000
# (health check is optional but keeps docker compose “healthy” flag green)
HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.translator_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
