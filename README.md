# Portfolio | Nuxt 3 + Django REST + Docker

Portfolio fullstack personnel : **Nuxt 3** (SSR) pour le frontend, **Django REST Framework** pour l'API, **PostgreSQL** pour la base de donnees, le tout orchestre avec **Docker Compose**.

## Architecture

```text
apps/client/     Nuxt 3 SSR (TypeScript, Pinia, SCSS)
apps/server/     Django REST API (Python 3.13, Celery, Redis)
nginx/           Reverse proxy
monitoring/      Grafana, Prometheus, Loki, Promtail
```

### Services Docker

| Service     | Description                             |
| ----------- | --------------------------------------- |
| `frontend`  | Nuxt 3 SSR (port 3000)                  |
| `backend`   | Django API via Gunicorn (port 8000)     |
| `nginx`     | Reverse proxy, point d'entree (port 80) |
| `db`        | PostgreSQL 17                           |
| `pgbouncer` | Connection pooling                      |
| `redis`     | Cache et sessions                       |
| `rabbitmq`  | Message broker                          |
| `celery`    | Worker asynchrone                       |

### Routes

| Route                 | Destination          |
| --------------------- | -------------------- |
| `/api/*`              | Django backend       |
| `/django-admin/`      | Django admin         |
| `/admin/*`            | Dashboard admin Nuxt |
| `/static/`, `/media/` | Fichiers Django      |

## Prerequis

- [Docker](https://www.docker.com/products/docker-desktop) et [Docker Compose](https://docs.docker.com/compose/)
- [Bun](https://bun.sh/) (dev local frontend uniquement)

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
bun install
bun run dev              # Serveur de dev
bun run build            # Build production
bun run check            # Biome lint + Oxlint + Stylelint + type-check + tests
bun run lint             # Biome lint (TS/JS) + Oxlint (TS/JS/.vue script)
bun run lint:fix         # Biome + Oxlint avec --fix
bun run lighthouse:ci    # Audit Lighthouse
```

**Outillage** :

- [Biome](https://biomejs.dev/) lint TS/JS/JSON (config : `biome.json`). Formatter Biome désactivé : pas de reformat opiniâtre.
- [Oxlint](https://oxc.rs/docs/guide/usage/linter.html) en complément : lint TS/JS et les `<script>` des `.vue`, plugins `vue`, `vitest`, `import`, `promise`, `typescript`, `oxc` (config : `.oxlintrc.json`). Ne lint pas les `<template>`/`<style>` Vue (limitation Rust-based linters).
- Stylelint pour les `<style>` Vue et les `.scss` (config : `stylelint.config.mjs`).

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

| Variable                         | Description                 |
| -------------------------------- | --------------------------- |
| `DJANGO_SECRET_KEY`              | Cle secrete Django          |
| `DB_PASSWORD`                    | Mot de passe PostgreSQL     |
| `JWT_SECRET_ACCESS_KEY`          | Secret JWT                  |
| `ADMIN_EMAIL` / `ADMIN_PASSWORD` | Compte admin initial        |
| `SMTP_*`                         | Configuration email         |
| `NUXT_PUBLIC_API_BASE`           | URL publique de l'API       |
| `NUXT_API_BASE_SERVER`           | URL interne Docker de l'API |

## Profils Docker

| Profil       | Services                    | Usage                     |
| ------------ | --------------------------- | ------------------------- |
| _(defaut)_   | App + infra                 | Production / dev standard |
| `dev`        | + Swagger UI, pgAdmin       | Developpement             |
| `monitoring` | + Grafana, Prometheus, Loki | Observabilite             |
| `backup`     | + pg_backup                 | Sauvegardes automatiques  |

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

## Deploiement

Le deploiement utilise `make` comme wrapper unique (local ET VPS). Toutes les commandes ci-dessous sont auto-documentees via `make help`.

### Variables requises (`.env`)

| Variable          | Role                                                 |
| ----------------- | ---------------------------------------------------- |
| `DOMAIN`          | Nom de domaine principal (ex: `aitaddajuba.fr`)      |
| `EMAIL`           | Email Let's Encrypt (contact admin)                  |
| `CERTBOT_STAGING` | `1` pour dry-run Let's Encrypt, `0` en prod          |
| `SSH_USER`        | Utilisateur SSH pour deploiement manuel depuis local |
| `SSH_HOST`        | Hote VPS                                             |
| `DEPLOY_PATH`     | Chemin du repo sur le VPS                            |

### Premier boot sur un nouveau VPS

Ordre imperatif (nginx demarre en HTTP-only le temps d'obtenir le cert) :

```bash
git clone ... && cd Portfolio
cp .env.example .env   # remplir DOMAIN, EMAIL, secrets
make up                # demarre la stack (nginx sert HTTP sur :80)
make ssl-issue         # challenge ACME via /.well-known/, delivre le cert
                       # puis reapplique init-ssl.sh -> nginx passe en HTTPS
make healthcheck       # verifie /health, /, /api/...
```

Le site est alors accessible en HTTPS sur `https://$DOMAIN`. Le port 80 ne sert plus qu'a rediriger vers 443 et a repondre aux renewals ACME.

### Redeploiement (apres merge)

Que ce soit depuis la CI ou en SSH manuel :

```bash
make deploy
```

Ce que `make deploy` fait :

1. `git pull --ff-only`
2. `docker compose up -d --build --remove-orphans` (pas de `down`, pas de `-v`)
3. Attend que `backend` soit healthy
4. `python manage.py migrate` + `collectstatic`
5. Reapplique `init-ssl.sh` dans nginx (picks up d'eventuels nouveaux templates)

**Aucun `down`, aucun `-v`** : les volumes `letsencrypt_certs`, `portfolio_db`, `backend_media`, etc. survivent a tous les deploiements.

### Ou sont les certs ?

Dans le volume Docker nomme `letsencrypt_certs` (monte en `/etc/letsencrypt` dans nginx et certbot). Pour inspecter :

```bash
docker compose --profile certbot run --rm certbot certificates
# ou
make ssl-status
```

### Renouvellement SSL

Manuellement :

```bash
make ssl-renew
```

Automatiquement via systemd timer sur le VPS (recommande, toutes les 12h) :

```ini
# /etc/systemd/system/portfolio-ssl-renew.service
[Unit]
Description=Renew Portfolio Let's Encrypt certs
[Service]
Type=oneshot
WorkingDirectory=/home/ubuntu/projects/Portfolio
ExecStart=/usr/bin/make ssl-renew
```

```ini
# /etc/systemd/system/portfolio-ssl-renew.timer
[Unit]
Description=Run portfolio-ssl-renew twice a day
[Timer]
OnCalendar=*-*-* 03,15:00:00
Persistent=true
[Install]
WantedBy=timers.target
```

Puis : `sudo systemctl enable --now portfolio-ssl-renew.timer`.

### Rollback

La CI enregistre le SHA precedent dans `.last-deployed-sha` avant chaque deploy. Pour revenir en arriere, declencher manuellement le job `deploy:rollback` dans GitLab, ou en SSH :

```bash
cd /path/to/Portfolio
prev=$(cat .last-deployed-sha)
git reset --hard "$prev"
make deploy
```

### Ordre de boot nginx (pour debug)

1. Container nginx demarre -> `/docker-entrypoint.d/40-init-ssl.sh` s'execute avant nginx
2. Le script genere `/etc/nginx/conf.d/` a partir de `nginx/templates/`
3. Si `letsencrypt_certs` contient `live/$DOMAIN/fullchain.pem` -> conf HTTPS + redirect HTTP->HTTPS
4. Sinon -> conf HTTP fallback qui sert le site + `/.well-known/acme-challenge/`
5. nginx demarre normalement

Voir [nginx/templates/](nginx/templates/) et [nginx/docker-entrypoint.d/40-init-ssl.sh](nginx/docker-entrypoint.d/40-init-ssl.sh).

## Stack technique

**Frontend** : Nuxt 3, Vue 3, TypeScript, Pinia, TanStack Query, SCSS, Vite

**Backend** : Django 5, DRF, Celery, Redis, PostgreSQL, orjson, Gunicorn

**Infra** : Docker, Traefik v3, PgBouncer, RabbitMQ, Grafana, Prometheus, Tempo, Loki, OpenTelemetry Collector, Alertmanager, Ansible

## Operations

Documentation opérationnelle : [docs/RUNBOOK.md](docs/RUNBOOK.md) (7 scénarios
incident avec RTO cible).

### Multi-environnement

`ENV=dev|staging|prod` pilote les overlays docker-compose et les settings
Django (`envs/<env>.py`) :

```bash
make up ENV=dev              # base compose seul (DB port exposé, build local)
make up ENV=staging          # overlay staging.yml (image registry, pas de ports)
make up ENV=prod             # overlay prod.yml (image pinée IMAGE_TAG, resource limits)
```

### Secrets (sops + age)

Les secrets runtime sont chiffrés avec [sops](https://github.com/getsops/sops) +
[age](https://github.com/FiloSottile/age). Bootstrap dans [secrets/README.md](secrets/README.md).

```bash
make secrets-edit ENV=prod          # sops edit in place
make secrets-decrypt ENV=prod       # -> /run/secrets/prod.env
make secrets-validate               # cohérence des clés entre envs
```

### Deploy zero-downtime + rollback

```bash
make deploy-zd ENV=prod IMAGE_TAG=$(git rev-parse --short HEAD)
make rollback  ENV=prod TAG=<previous-sha>       # <30s, aucune 502
```

Stratégie : scale=+1 → attente `healthy` via Docker healthcheck → scale=-1.
Traefik drain l'ancienne réplique via `stop_grace_period: 60s` + graceful
gunicorn (`--graceful-timeout 30`) et celery (`--soft-time-limit`).

### Observabilité

Stack OTel → Tempo (traces) + Loki (logs) + Prometheus + Alertmanager :

```bash
make monitoring                      # démarre le profil monitoring
make slo-check ENV=prod              # availability + p95 courants
make otel-logs                       # spans refused / batch queue
make dashboards-lint                 # JSON dashboards valides
```

Dashboards versionnés dans [monitoring/grafana/dashboards/](monitoring/grafana/dashboards/).
SLO : availability 99.5% / 30j · latency p95 < 300ms sur `/api/**`.

### Backups & restore

- `prodrigestivill/postgres-backup-local` prend un dump quotidien local.
- Sidecar `db-backup-sync` (rclone) pousse vers Backblaze B2, retention 30j.
- Test de restore mensuel automatique via cron Ansible (`make backup-test`).

```bash
make backup-sync ENV=prod
make backup-test ENV=prod
make db-restore-from-s3 ENV=prod FILE=portfolio-YYYYMMDD-HHMMSS.sql.gz
```

### Infrastructure as Code (Ansible)

Bootstrap VPS vierge (hardening SSH port 2200 + ufw + fail2ban + unattended
upgrades + lynis + Docker + systemd unit) :

```bash
make infra-check     ENV=prod        # dry-run
make infra-bootstrap ENV=prod        # from-scratch setup
make infra-deploy    ENV=prod        # git pull + rolling deploy à distance
```

### CI/CD

Pipeline GitLab : `validate → test → security (gitleaks, trivy fs/image bloquant,
pip-audit, npm audit) → build (push registry tags SHA + branche + latest) →
sbom (syft SPDX) → perf (Lighthouse + k6 nightly) → deploy (rolling) + rollback manuel`.

Voir [.gitlab-ci.yml](.gitlab-ci.yml).

### Bench perf (k6)

```bash
make bench-local   SCENARIO=browse         # charge réaliste localhost
make bench-staging SCENARIO=contact        # teste le rate-limit Traefik
make bench-staging SCENARIO=sustained      # 15min, détection fuites mémoire
```
