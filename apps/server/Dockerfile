# ──────────────────────────────────────────────
# Build arguments (overridable from docker-compose)
# ──────────────────────────────────────────────
ARG PYTHON_VERSION=3.13

# Étape 1: Image de construction
FROM python:${PYTHON_VERSION}-alpine AS builder

# Mise à jour des paquets Alpine + dépendances de compilation
RUN apk upgrade --no-cache --available && \
    apk add --no-cache \
    build-base \
    postgresql-dev \
    jpeg-dev \
    zlib-dev \
    libffi-dev

# Création de l'environnement virtuel
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Préparation pour l'installation des dépendances
WORKDIR /app
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir wheel && \
    pip install --no-cache-dir -r requirements.txt

# Étape 2: Image finale
FROM python:${PYTHON_VERSION}-alpine

# Mise à jour des paquets Alpine + dépendances d'exécution
RUN apk upgrade --no-cache --available && \
    apk add --no-cache \
    libpq \
    libjpeg-turbo \
    curl \
    bash \
    netcat-openbsd

# Copier l'environnement virtuel
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Configuration de l'environnement (valeurs par défaut, surchargées par docker-compose)
ENV DJANGO_SETTINGS_MODULE=config.settings \
    GUNICORN_WORKERS=3 \
    GUNICORN_TIMEOUT=120 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Définir le répertoire de travail
WORKDIR /app

# Créer un utilisateur non-root
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Créer les répertoires nécessaires
RUN mkdir -p /app/logs /app/media /app/staticfiles /app/.cache /app/swagger

COPY . .

# Définir les permissions
RUN chmod +x /app/scripts/*.sh \
    && chmod +x /app/scripts/*.py \
    && chown -R appuser:appgroup /app/logs /app/media /app/staticfiles /app/.cache /app/swagger

# Passer à l'utilisateur non-root
USER appuser

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["/app/scripts/setup.sh"]
