# Portfolio — Nuxt 3 + Django REST + Docker

Portfolio fullstack personnel : **Nuxt 3** (SSR) pour le frontend, **Django REST Framework** pour l'API, **PostgreSQL** pour la base de donnees, le tout orchestre avec **Docker Compose**.

## Architecture

```text
apps/client/     Nuxt 3 SSR (TypeScript, Pinia, SCSS)
apps/server/     Django REST API (Python 3.13, Celery, Redis)
nginx/           Reverse proxy
monitoring/      Grafana, Prometheus, Loki, Promtail
```

### Services Docker

| Service     | Description                              |
| ----------- | ---------------------------------------- |
| `frontend`  | Nuxt 3 SSR (port 3000)                  |
| `backend`   | Django API via Gunicorn (port 8000)      |
| `nginx`     | Reverse proxy, point d'entree (port 80)  |
| `db`        | PostgreSQL 17                            |
| `pgbouncer` | Connection pooling                       |
| `redis`     | Cache et sessions                        |
| `rabbitmq`  | Message broker                           |
| `celery`    | Worker asynchrone                        |

### Routes

| Route                 | Destination          |
| --------------------- | -------------------- |
| `/api/*`              | Django backend       |
| `/django-admin/`      | Django admin         |
| `/admin/*`            | Dashboard admin Nuxt |
| `/static/`, `/media/` | Fichiers Django      |

## Prerequis

- [Docker](https://www.docker.com/products/docker-desktop) et [Docker Compose](https://docs.docker.com/compose/)
- [pnpm](https://pnpm.io/) (dev local frontend uniquement)

## Installation

```bash
git clone https://github.com/ton-profil/portfolio.git
cd portfolio
cp .env.example .env
# Remplir les variables dans .env
docker-compose up --build
```

Le site est accessible sur `http://localhost`.

## Commandes

### Docker

```bash
# Demarrage
docker-compose up --build

# Avec outils dev (Swagger UI :8085, pgAdmin :5050)
docker-compose --profile dev up --build

# Avec monitoring (Grafana :3001, Prometheus :9090)
docker-compose --profile monitoring up --build

# Arret
docker-compose down

# Logs backend
docker-compose logs -f backend
```

### Frontend (`apps/client/`)

```bash
pnpm install
pnpm dev              # Serveur de dev
pnpm build            # Build production
pnpm check            # Lint + Stylelint + TypeCheck
pnpm lint:fix         # Fix automatique ESLint
pnpm lighthouse:ci    # Audit Lighthouse
```

### Backend (`apps/server/`)

```bash
python manage.py runserver
python manage.py migrate
pytest                 # Tests
pytest --cov           # Tests + coverage
black . && isort . && ruff check .   # Formatage + lint
```

## Variables d'environnement

Copier `.env.example` vers `.env`. Variables essentielles :

| Variable                         | Description                     |
| -------------------------------- | ------------------------------- |
| `DJANGO_SECRET_KEY`              | Cle secrete Django              |
| `DB_PASSWORD`                    | Mot de passe PostgreSQL         |
| `JWT_SECRET_ACCESS_KEY`          | Secret JWT                      |
| `ADMIN_EMAIL` / `ADMIN_PASSWORD` | Compte admin initial            |
| `SMTP_*`                         | Configuration email             |
| `NUXT_PUBLIC_API_BASE`           | URL publique de l'API           |
| `NUXT_API_BASE_SERVER`           | URL interne Docker de l'API     |

## Profils Docker

| Profil         | Services                      | Usage                     |
| -------------- | ----------------------------- | ------------------------- |
| _(defaut)_     | App + infra                   | Production / dev standard |
| `dev`          | + Swagger UI, pgAdmin         | Developpement             |
| `monitoring`   | + Grafana, Prometheus, Loki   | Observabilite             |
| `backup`       | + pg_backup                   | Sauvegardes automatiques  |

## Debug

```bash
# Django Debug Toolbar
DJANGO_DEBUG=true
ENABLE_DEBUG_TOOLBAR=true
# -> http://localhost:8000/__debug__/

# Web Vitals (taux d'echantillonnage)
NUXT_PUBLIC_WEB_VITALS_SAMPLE_RATE=1.0   # dev
NUXT_PUBLIC_WEB_VITALS_SAMPLE_RATE=0.1   # prod
```

## Stack technique

**Frontend** : Nuxt 3, Vue 3, TypeScript, Pinia, TanStack Query, SCSS, Vite

**Backend** : Django 5, DRF, Celery, Redis, PostgreSQL, orjson, Gunicorn

**Infra** : Docker, Nginx, PgBouncer, RabbitMQ, Grafana, Prometheus, Loki
