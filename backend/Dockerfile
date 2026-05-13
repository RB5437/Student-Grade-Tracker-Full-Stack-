# ========================================
# STAGE 1: Builder
# Install all dependencies including build tools
# ========================================
FROM python:3.11 AS builder

WORKDIR /build

# Copy only requirements first (layer cache optimization)
COPY requirements.txt .

# Install dependencies into a local folder
RUN pip install --user --no-cache-dir -r requirements.txt

# ========================================
# STAGE 2: Runtime (FINAL IMAGE)
# Only copy what we need — no build tools
# ========================================
FROM python:3.11-slim AS runtime

# Security: run as non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY app.py .

# Set PATH so our installed packages are found
ENV PATH=/home/appuser/.local/bin:$PATH

# Switch to non-root user
USER appuser

# Expose app port
EXPOSE 5000

# Health check — Docker will restart if this fails
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

# Run with gunicorn (production WSGI server, not Flask dev server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
