FROM python:3.11-slim
WORKDIR /app

# Copy source
COPY . /app

RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Run tests by default to validate the image
CMD ["/bin/sh", "-c", "python -m pytest --maxfail=1 --disable-warnings -q --cov=user_display_optimized --cov-report=term --cov-fail-under=85"]
