FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl build-essential && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    rm -rf /var/lib/apt/lists/*
ENV PATH=/root/.cargo/bin:$PATH
COPY . .
RUN pip install maturin fastapi uvicorn pydantic && \
    maturin develop --features python 2>/dev/null || echo "Rust build skipped"
EXPOSE 8090
CMD ["uvicorn", "src.bridge.server:app", "--host", "0.0.0.0", "--port", "8090"]
