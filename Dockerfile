FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

RUN pip install --no-cache-dir \
    feast[redis]==0.61.0 \
    "pandas>=2.0,<3" \
    "pyarrow>=21.0.0" \
    jupyter

CMD ["bash"]
