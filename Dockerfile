FROM python:3.11-slim

WORKDIR /app

# Prevent Python from buffering stdout/stderr (helpful for tests/logs)
ENV PYTHONUNBUFFERED=1

# Install system dependencies needed by tests (none for this simple project)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["bash","-lc","pytest --maxfail=1 -q --cov=user_display_optimized --cov-report=term-missing --cov-fail-under=85"]
