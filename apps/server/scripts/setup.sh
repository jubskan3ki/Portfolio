#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Lancement du setup Django...${NC}"

# Attente que la base de données soit prête
echo -e "${GREEN}🕒 Attente de la DB sur $DB_HOST:$DB_PORT...${NC}"
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo -e "${GREEN}✅ DB disponible, on continue...${NC}"

# Lancement de makemigrations pour toutes les apps
echo -e "${GREEN}⚙️  Génération des migrations...${NC}"
python manage.py makemigrations

echo -e "${GREEN}✅ Makemigrations terminées.${NC}"

# Applique toutes les migrations
echo -e "${GREEN}⚙️  Application des migrations...${NC}"
python manage.py migrate --noinput
echo -e "${GREEN}✅ Migrations appliquées.${NC}"

# Création automatique du superuser si non existant
echo -e "${GREEN}👤 Vérification/Création du superuser ${ADMIN_EMAIL}...${NC}"

python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(email="${ADMIN_EMAIL}").exists():
    User.objects.create_superuser(email="${ADMIN_EMAIL}", password="${ADMIN_PASSWORD}")
    print("✅ Superuser ${ADMIN_EMAIL} créé.")
else:
    print("⚠️  Superuser ${ADMIN_EMAIL} déjà existant.")
EOF

echo -e "${GREEN}✅ Superuser setup terminé.${NC}"

# Lancer Gunicorn si tout est ok
echo -e "${GREEN}🚀 Lancement de Gunicorn...${NC}"
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers=${GUNICORN_WORKERS:-3} --timeout=${GUNICORN_TIMEOUT:-120}
