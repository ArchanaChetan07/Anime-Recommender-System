# ─────────────────────────────────────────────────────────────────
# Stage 1 — dependency builder
# ─────────────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Copy only dependency files first (layer-cache friendly)
COPY requirements.txt setup.py ./
COPY README.md ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# ─────────────────────────────────────────────────────────────────
# Stage 2 — runtime image
# ─────────────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

# Security: run as non-root
RUN useradd --create-home --shell /bin/bash appuser

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8501

# Healthcheck for Kubernetes readiness probe
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "app/app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--server.enableCORS=false", \
     "--server.enableXsrfProtection=true"]
