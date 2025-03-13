#!/bin/bash

# Charger les variables d'environnement
export $(grep -v '^#' ../apps/server/.env | xargs)

# Sauvegarde de la base de données
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="../infra/db/backup_$TIMESTAMP.sql"

echo "📦 Sauvegarde de la base de données..."
docker exec portfolio_db pg_dump -U $DB_USER -h $POSTGRES_HOST -p $POSTGRES_PORT $DB_NAME > $BACKUP_FILE

echo "✅ Sauvegarde réalisée avec succès : $BACKUP_FILE"
