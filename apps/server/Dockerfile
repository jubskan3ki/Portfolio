# syntax=docker/dockerfile:1.7
ARG PYTHON_VERSION=3.14
ARG VCS_REF=unknown
ARG BUILD_DATE=unknown

FROM python:${PYTHON_VERSION}-alpine AS builder

RUN apk upgrade --no-cache --available && \
    apk add --no-cache \
    build-base \
    postgresql-dev \
    jpeg-dev \
    zlib-dev \
    libffi-dev

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY requirements.in .

RUN --mount=type=cache,target=/root/.cache/pip,sharing=locked \
    pip install --upgrade pip && \
    pip install pip-tools wheel && \
    pip-compile --quiet requirements.in -o requirements.txt && \
    pip install -r requirements.txt

FROM python:${PYTHON_VERSION}-alpine
ARG VCS_REF
ARG BUILD_DATE
LABEL org.opencontainers.image.title="portfolio-backend" \
      org.opencontainers.image.source="https://github.com/jubskan3ki/portfolio" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.licenses="MIT"

RUN apk upgrade --no-cache --available && \
    apk add --no-cache \
    libpq \
    libjpeg-turbo \
    curl \
    bash \
    netcat-openbsd \
    tini

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

ENV DJANGO_SETTINGS_MODULE=config.settings \
    GUNICORN_WORKERS=3 \
    GUNICORN_TIMEOUT=120 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

RUN mkdir -p /app/logs /app/media /app/staticfiles /app/.cache /app/swagger

COPY . .

RUN chmod +x /app/scripts/*.py /app/manage.py \
    && chown -R appuser:appgroup /app/logs /app/media /app/staticfiles /app/.cache /app/swagger

USER appuser

EXPOSE 8000

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["python", "manage.py", "bootstrap"]
