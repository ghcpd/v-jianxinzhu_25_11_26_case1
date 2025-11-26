FROM python:3.10-slim
WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

# Default: run tests
CMD ["bash", "-lc", "pytest --cov=user_display_optimized --cov-report=term-missing"]
