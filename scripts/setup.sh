#!/bin/bash

echo "🚀 Initialisation du projet Portfolio..."

# Charger les variables d'environnement
export $(grep -v '^#' ../apps/server/.env | xargs)

# Construire et démarrer Docker
echo "📦 Construction des services..."
docker-compose up --build -d

# Attendre que PostgreSQL soit prêt
echo "⏳ Attente de PostgreSQL..."
while ! docker exec portfolio_db pg_isready -U $POSTGRES_USER -h $POSTGRES_HOST -p $POSTGRES_PORT; do
    sleep 1
done

# Appliquer les migrations Django
echo "📜 Exécution des migrations Django..."
docker exec portfolio_backend python manage.py migrate

# Collecter les fichiers statiques
echo "🖼 Collecte des fichiers statiques..."
docker exec portfolio_backend python manage.py collectstatic --noinput

echo "✅ Projet Portfolio initialisé avec succès !"
