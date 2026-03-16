# Stage 1: Build Rust extension
FROM python:3.12-slim AS builder
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    rm -rf /var/lib/apt/lists/*

ENV PATH=/root/.cargo/bin:$PATH

COPY . .
RUN pip install --no-cache-dir maturin cffi
RUN maturin build --release --features python --out dist

# Stage 2: Final image
FROM python:3.12-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m appuser

COPY --from=builder /app/dist/*.whl .
RUN pip install --no-cache-dir *.whl fastapi uvicorn pydantic && rm *.whl

COPY src ./src

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8090
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8090/health || exit 1

CMD ["uvicorn", "src.bridge.server:app", "--host", "0.0.0.0", "--port", "8090"]
