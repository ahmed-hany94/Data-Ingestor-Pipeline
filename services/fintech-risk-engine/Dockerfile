FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install deps first so this layer is cached unless requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

COPY . .

RUN useradd --create-home --shell /bin/false app && \
    chown -R app:app /app
USER app

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/healthz').status==200 else 1)"

# Runs migrations on boot, then serves via gunicorn (not Django's dev server)
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn risk_engine.wsgi:application --bind 0.0.0.0:8000 --workers 3"]