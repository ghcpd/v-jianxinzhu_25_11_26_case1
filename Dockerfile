FROM python:3.10-slim

LABEL maintainer="Development Team" \
      description="User Display Optimizer - Cross-platform execution environment" \
      version="1.0"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt .
COPY user_display_optimized.py .
COPY user_display_original.py .
COPY tests/ ./tests/

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Default command: run tests
CMD ["pytest", "tests/", "-v", "--tb=short", "--cov=user_display_optimized", "--cov-report=term-missing"]
