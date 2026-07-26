FROM python:3.11-slim AS runtime

# Prevent .pyc files and enable unbuffered stdout (so logs stream in `docker logs`)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install deps first so this layer is cached unless requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

COPY src/ ./src/

# Non-root user
RUN useradd --create-home --shell /bin/false app
USER app

# No exposed port: this service only consumes from Redis, it doesn't serve HTTP
CMD ["python", "-m", "src.main"]