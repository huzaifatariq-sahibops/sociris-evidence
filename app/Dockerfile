FROM python:3.12-alpine3.22
LABEL org.opencontainers.image.title="SOCIRIS Evidence Application"

WORKDIR /app

RUN addgroup -S appgroup \
    && adduser -S appuser -G appgroup \
    && mkdir -p /data \
    && chown appuser:appgroup /data

COPY --chown=appuser:appgroup app.py index.html ./

ENV HOST=0.0.0.0 \
    PORT=8004 \
    DATABASE_PATH=/data/app.db \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

USER appuser

EXPOSE 8004

HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8004/health', timeout=2)"

CMD ["python", "app.py"]
