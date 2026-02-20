FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir \
    flask==3.0.0 \
    cryptography==41.0.7 \
    gunicorn==21.2.0

# Create keys directory
RUN mkdir -p /app/keys

# Copy application
COPY app.py /app/

# Environment variables
ENV HMAC_SECRET=soc-hmac-secret-key-2024 \
    KEYS_DIR=/app/keys \
    PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "app:app"]
