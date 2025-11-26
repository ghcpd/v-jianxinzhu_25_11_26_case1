# Dockerfile for User Display Optimizer
# Multi-stage build for optimized image size

FROM python:3.10-slim as builder

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application files
COPY user_display_optimized.py .
COPY tests/ tests/

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Default command: run tests
CMD ["pytest", "tests/", "-v", "--cov=user_display_optimized", "--cov-report=term-missing"]
