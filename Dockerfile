# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install numpy first so joblib/sklearn unpickling uses the expected runtime version
RUN pip install --upgrade pip && \
    pip install numpy==1.26.4 && \
    pip install -r requirements.txt

# Copy application code, including model.pkl
COPY . .

# Fail the build early if the packaged model is missing
RUN test -f /app/model.pkl

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health', timeout=5)" || exit 1

# Run the application with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
