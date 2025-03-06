# Étape 1 : Utiliser une image légère de Python 3.11
FROM python:3.11-slim

# Définition du répertoire de travail
WORKDIR /app

# Installation des dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Création du dossier logs et ajustement des permissions
RUN mkdir -p /app/logs && chmod -R 777 /app/logs

# Copier uniquement les fichiers de dépendances en premier pour optimiser le cache Docker
COPY requirements.txt .

# Vérifier que le fichier requirements.txt existe avant d'installer les dépendances
RUN if [ -f "requirements.txt" ]; then pip install --no-cache-dir -r requirements.txt; fi

# Installer Gunicorn et dotenv
RUN pip install --no-cache-dir gunicorn python-dotenv

# Copier le reste de l'application
COPY . .

# Exposer les ports 8000 et 80
EXPOSE 8000 80

# Définir le nombre de workers dynamiquement (en fonction du CPU)
ENV GUNICORN_WORKERS=3
ENV GUNICORN_TIMEOUT=120

# Lancer l'application Django avec Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "300", "--threads", "4", "--worker-class", "gthread", "config.wsgi:application"]
