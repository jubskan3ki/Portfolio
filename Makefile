SHELL := /bin/bash
.DEFAULT_GOAL := help

ifneq (,$(wildcard .env))
include .env
export
endif

ENV             ?= dev
COMPOSE_BIN     ?= docker compose
BUN             ?= bun
DOMAIN          ?= aitaddajuba.fr
EMAIL           ?= contact@aitaddajuba.fr
DATA_DIR        ?= Data
BACKUP_DIR      ?= backups
SECRETS_RUNTIME_DIR ?= /run/secrets
CLIENT_DIR      := apps/client
SERVER_DIR      := apps/server

ifeq ($(ENV),prod)
    COMPOSE_OVERLAY := -f docker-compose.yml -f docker-compose.prod.yml
    COMPOSE_ENV_FLAG := --env-file $(SECRETS_RUNTIME_DIR)/prod.env
else
    COMPOSE_OVERLAY := -f docker-compose.yml -f docker-compose.dev.yml
    COMPOSE_ENV_FLAG :=
endif
COMPOSE          := $(COMPOSE_BIN) $(COMPOSE_ENV_FLAG) $(COMPOSE_OVERLAY)
COMPOSE_ALL      := $(COMPOSE) --profile dev --profile monitoring
COMPOSE_DEV      := $(COMPOSE_BIN) -f docker-compose.yml -f docker-compose.dev.yml --profile dev
COMPOSE_EXEC     := $(COMPOSE) exec

##@ Help

.PHONY: help
help: ## Liste les targets groupés par section
	@awk 'BEGIN { FS = ":.*?##[ @]" } \
	      /^##@ / { printf "\n\033[1;33m%s\033[0m\n", substr($$0, 5); next } \
	      /^[a-zA-Z0-9_-]+:.*?## / { printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2 }' \
	      $(MAKEFILE_LIST)
	@echo -e "\n\033[1;33mVariables\033[0m  ENV=$(ENV) (dev|prod) · DOMAIN=$(DOMAIN)"

##@ Stack - lifecycle

.PHONY: up
up: ## Démarre la stack en arrière-plan (ENV=dev|prod)
	$(COMPOSE) up -d --build --remove-orphans

.PHONY: up-fg
up-fg: ## Démarre la stack en avant-plan (logs visibles)
	$(COMPOSE) up --build --remove-orphans

.PHONY: down
down: ## Arrête la stack (garde les volumes) | inclut tous les profils (dev, monitoring)
	$(COMPOSE_ALL) down --remove-orphans

.PHONY: restart
restart: ## Redémarre tous les services (ou SVC=<name>)
	$(COMPOSE) restart $(SVC)

.PHONY: build
build: ## Build les images (avec cache)
	$(COMPOSE) build

.PHONY: rebuild
rebuild: ## Rebuild sans cache puis redémarre
	$(COMPOSE) build --no-cache
	$(COMPOSE) up -d

.PHONY: logs
logs: ## Logs en live. SVC=<backend|frontend|traefik|celery|otel-collector|...>
	$(COMPOSE) logs -f --tail=100 $(SVC)

.PHONY: status
status: ## État détaillé: conteneurs + healthchecks + endpoints
	@echo -e "\033[1;33m# Conteneurs\033[0m"
	@$(COMPOSE) ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || $(COMPOSE) ps
	@echo -e "\n\033[1;33m# Healthchecks\033[0m"
	@for c in $$($(COMPOSE) ps -q 2>/dev/null); do \
	    n=$$(docker inspect -f '{{.Name}}' $$c | sed 's|^/||'); \
	    h=$$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}-{{end}}' $$c); \
	    printf "  %-22s %s\n" "$$n" "$$h"; \
	done
	@echo -e "\n\033[1;33m# Endpoints\033[0m"
	@$(MAKE) --no-print-directory healthcheck

.PHONY: healthcheck
healthcheck: ## Teste /health, /, /api via Traefik (+ HTTPS si cert ACME émis)
	@for p in /health / /api/users/; do \
	    printf "  %-14s : " "$$p"; \
	    curl -fsS -o /dev/null -w "%{http_code}\n" http://localhost:$${TRAEFIK_HTTP_PORT:-80}$$p || echo FAIL; \
	done
	@if $(COMPOSE_EXEC) -T traefik test -s /letsencrypt/acme.json 2>/dev/null; then \
	    printf "  https://%-6s : " "$(DOMAIN)"; \
	    curl -fsS -o /dev/null -w "%{http_code}\n" --max-time 5 https://$(DOMAIN)/ || echo FAIL; \
	fi

##@ Dev - HMR + outils

.PHONY: dev
dev: ## Stack dev avec HMR + Swagger UI + pgAdmin (avant-plan)
	@echo ">> http://localhost (Traefik, WebSocket HMR) · :3000 Nuxt direct · :8000 Django · :8085 Swagger · :5050 pgAdmin"
	$(COMPOSE_DEV) up --build --remove-orphans

.PHONY: dev-reset
dev-reset: ## Purge node_modules + cache Nuxt (sans toucher DB)
	$(COMPOSE_DEV) down
	-docker volume rm $$(docker volume ls -q | grep -E '_(frontend_node_modules|frontend_nuxt_cache)$$') 2>/dev/null
	@echo ">> Prochain 'make dev' fera un bun install propre"

.PHONY: clean-host
clean-host: ## Purge .nuxt/.output/cache hote (utile quand Docker les a write en root)
	@echo ">> Nettoyage des artefacts Nuxt (peut demander sudo si root-owned)"
	@if [ -w "$(CLIENT_DIR)/.nuxt" ] || ! [ -e "$(CLIENT_DIR)/.nuxt" ]; then \
		rm -rf "$(CLIENT_DIR)/.nuxt" "$(CLIENT_DIR)/.output" "$(CLIENT_DIR)/node_modules/.cache"; \
	else \
		sudo rm -rf "$(CLIENT_DIR)/.nuxt" "$(CLIENT_DIR)/.output" "$(CLIENT_DIR)/node_modules/.cache"; \
	fi
	@echo ">> OK"

.PHONY: shell
shell: ## Shell interactif. SVC=backend (défaut) | db | frontend | redis
	@svc="$${SVC:-backend}"; \
	case "$$svc" in \
	    backend|celery) $(COMPOSE_EXEC) $$svc bash ;; \
	    db) $(COMPOSE_EXEC) db psql -U $(DB_USER) -d $(DB_NAME) ;; \
	    frontend) $(COMPOSE_EXEC) $$svc sh ;; \
	    redis) $(COMPOSE_EXEC) redis redis-cli ;; \
	    *) $(COMPOSE_EXEC) $$svc sh ;; \
	esac

.PHONY: djshell
djshell: ## Shell Django (manage.py shell)
	$(COMPOSE_EXEC) backend python manage.py shell

##@ Code quality - lint · format · test · types

.PHONY: lint
lint: ## Lint front + back (check only, 0 modification)
	cd $(CLIENT_DIR) && $(BUN) run lint && $(BUN) run lint:css
	$(COMPOSE_EXEC) backend sh -c "black --check . && isort --check-only . && ruff check ."

.PHONY: format
format: ## Formate front + back (écrit les fixes)
	cd $(CLIENT_DIR) && $(BUN) run fix
	$(COMPOSE_EXEC) backend sh -c "black . && isort . && ruff check --fix ."

.PHONY: typecheck
typecheck: ## TypeScript (vue-tsc) + Python (mypy advisory)
	cd $(CLIENT_DIR) && $(BUN) run type-check

.PHONY: test
test: ## Tests unitaires front (vitest) + back (pytest)
	cd $(CLIENT_DIR) && $(BUN) run test
	$(COMPOSE_EXEC) backend pytest

.PHONY: check
check: lint typecheck test ## Tout valider (lint + typecheck + test)

##@ Database - Django migrations + pg_dump

.PHONY: backend-migrate
backend-migrate: ## Applique les migrations Django
	$(COMPOSE_EXEC) backend python manage.py migrate --noinput

.PHONY: migrate-check
migrate-check: ## Refuse un deploy si migration destructive détectée (exit 0/1/2)
	$(COMPOSE_EXEC) backend python manage.py migrate_check

.PHONY: makemigrations
makemigrations: ## Génère de nouvelles migrations
	$(COMPOSE_EXEC) backend python manage.py makemigrations

.PHONY: createsuperuser
createsuperuser: ## Crée un superuser Django interactif
	$(COMPOSE_EXEC) backend python manage.py createsuperuser

.PHONY: db-backup
db-backup: ## Dump SQL -> ./backups/portfolio-YYYYMMDD-HHMMSS.sql.gz
	@mkdir -p $(BACKUP_DIR)
	@test -n "$(DB_USER)" -a -n "$(DB_NAME)" || { echo "DB_USER/DB_NAME manquants (.env)"; exit 1; }
	@ts=$$(date +%Y%m%d-%H%M%S); out="$(BACKUP_DIR)/portfolio-$$ts.sql.gz"; \
	$(COMPOSE_EXEC) -T db pg_dump -U $(DB_USER) -d $(DB_NAME) --no-owner --no-privileges | gzip > "$$out"; \
	echo "Dump: $$out ($$(du -h $$out | cut -f1))"

.PHONY: db-restore
db-restore: ## Restore un dump local. FILE=backups/xxx.sql.gz
	@test -f "$(FILE)" || { echo "Usage: make db-restore FILE=backups/xxx.sql.gz"; exit 1; }
	@gunzip -c "$(FILE)" | $(COMPOSE_EXEC) -T db psql -U $(DB_USER) -d $(DB_NAME)
	@echo "Restore OK"

##@ TimescaleDB - hypertables + compression + retention

.PHONY: timescale-stats
timescale-stats: ## Affiche compression + chunks + policies pour toutes les hypertables
	@$(COMPOSE_EXEC) -T db psql -U $(DB_USER) -d $(DB_NAME) -x -c "\
		SELECT \
		    h.hypertable_name AS table_name, \
		    (SELECT count(*) FROM timescaledb_information.chunks c WHERE c.hypertable_name = h.hypertable_name) AS chunks, \
		    (SELECT count(*) FROM timescaledb_information.chunks c WHERE c.hypertable_name = h.hypertable_name AND c.is_compressed) AS chunks_compressed, \
		    pg_size_pretty(hypertable_size(format('%I.%I', h.hypertable_schema, h.hypertable_name)::regclass)) AS total_size, \
		    pg_size_pretty(COALESCE((SELECT sum(after_compression_total_bytes) FROM hypertable_compression_stats(format('%I.%I', h.hypertable_schema, h.hypertable_name)::regclass)), 0)) AS compressed_size, \
		    ROUND(CASE WHEN COALESCE((SELECT sum(after_compression_total_bytes) FROM hypertable_compression_stats(format('%I.%I', h.hypertable_schema, h.hypertable_name)::regclass)), 0) = 0 \
		         THEN 0 \
		         ELSE (SELECT sum(before_compression_total_bytes) FROM hypertable_compression_stats(format('%I.%I', h.hypertable_schema, h.hypertable_name)::regclass))::numeric / NULLIF((SELECT sum(after_compression_total_bytes) FROM hypertable_compression_stats(format('%I.%I', h.hypertable_schema, h.hypertable_name)::regclass)), 0) END, 2) AS compression_ratio \
		FROM timescaledb_information.hypertables h ORDER BY h.hypertable_name;"

.PHONY: timescale-policies
timescale-policies: ## Liste les jobs de compression + retention et leur dernier run
	@$(COMPOSE_EXEC) -T db psql -U $(DB_USER) -d $(DB_NAME) -c "\
		SELECT j.job_id, j.hypertable_name, j.proc_name AS policy, j.schedule_interval, \
		       s.last_run_started_at, s.last_run_status, s.next_start \
		FROM timescaledb_information.jobs j \
		LEFT JOIN timescaledb_information.job_stats s USING (job_id) \
		WHERE j.proc_name IN ('policy_compression', 'policy_retention') \
		ORDER BY j.hypertable_name, j.proc_name;"

.PHONY: timescale-version
timescale-version: ## Affiche la version TimescaleDB installée + version PG
	@$(COMPOSE_EXEC) -T db psql -U $(DB_USER) -d $(DB_NAME) -c "\
		SELECT extversion AS timescaledb, current_setting('server_version') AS postgres \
		FROM pg_extension WHERE extname = 'timescaledb';"

##@ Database - Django migrations + pg_dump (suite)

.PHONY: db-reset
db-reset: ## Drop + recreate DB + migrate (DANGER: perte totale)
	@read -p "Vider la base $(DB_NAME) ? (tapez 'oui') " ok && [ "$$ok" = "oui" ] || exit 1
	$(COMPOSE_EXEC) db dropdb -U $(DB_USER) --if-exists $(DB_NAME)
	$(COMPOSE_EXEC) db createdb -U $(DB_USER) $(DB_NAME)
	$(MAKE) backend-migrate

.PHONY: data-export
data-export: ## Exporte les fixtures JSON dans Data/
	@mkdir -p $(DATA_DIR)
	@ts=$$(date +%Y%m%d_%H%M%S); \
	for app in articles experiences projects stacks; do \
	    $(COMPOSE_EXEC) -T backend python manage.py dumpdata core.$$app --indent 2 --natural-foreign --natural-primary > "$(DATA_DIR)/$${app}_$$ts.json"; \
	    echo "-> $(DATA_DIR)/$${app}_$$ts.json"; \
	done

.PHONY: data-import
data-import: ## Importe tous les JSON de Data/ via loaddata
	@ls $(DATA_DIR)/*.json >/dev/null 2>&1 || { echo "Aucun JSON dans $(DATA_DIR)/"; exit 1; }
	@for f in $(DATA_DIR)/*.json; do \
	    $(COMPOSE) cp "$$f" backend:/app/_import.json; \
	    $(COMPOSE_EXEC) backend python manage.py loaddata /app/_import.json; \
	    $(COMPOSE_EXEC) backend rm -f /app/_import.json; \
	    echo "<- $$f"; \
	done

##@ Secrets - sops + age

.PHONY: secrets-edit
secrets-edit: ## Édite secrets/$(ENV).env.sops.yaml via sops
	@command -v sops >/dev/null || { echo "sops requis (voir secrets/README.md)"; exit 1; }
	@test -f "secrets/$(ENV).env.sops.yaml" || { echo "Fichier manquant | créer via sops --encrypt"; exit 1; }
	sops edit "secrets/$(ENV).env.sops.yaml"

.PHONY: secrets-decrypt
secrets-decrypt: ## Déchiffre -> $(SECRETS_RUNTIME_DIR)/$(ENV).env (tmpfs, 0600)
	@set -eu; dest="$(SECRETS_RUNTIME_DIR)/$(ENV).env"; \
	test -f "secrets/$(ENV).env.sops.yaml" || { echo "secrets/$(ENV).env.sops.yaml manquant"; exit 1; }; \
	mkdir -p "$(SECRETS_RUNTIME_DIR)"; chmod 700 "$(SECRETS_RUNTIME_DIR)" 2>/dev/null || true; \
	umask 077; sops --decrypt --input-type yaml --output-type dotenv "secrets/$(ENV).env.sops.yaml" > "$$dest"; \
	chmod 600 "$$dest"; echo "-> $$dest"

.PHONY: secrets-rotate
secrets-rotate: ## Régénère les clés de chiffrement (après rotation age)
	sops rotate -i "secrets/$(ENV).env.sops.yaml"

.PHONY: secrets-validate
secrets-validate: ## Vérifie que les envs sops ont les mêmes clés que .env.example
	@set -eu; expected=$$(grep -E '^[A-Z_][A-Z0-9_]*=' .env.example | cut -d= -f1 | sort -u); fail=0; \
	for e in dev prod; do \
	    src="secrets/$$e.env.sops.yaml"; [ -f "$$src" ] || { echo "skip $$src"; continue; }; \
	    actual=$$(sops --decrypt --input-type yaml --output-type dotenv "$$src" | grep -E '^[A-Z_][A-Z0-9_]*=' | cut -d= -f1 | sort -u); \
	    missing=$$(comm -23 <(echo "$$expected") <(echo "$$actual")); \
	    [ -z "$$missing" ] || { echo "[$$e] manquant:"; echo "$$missing" | sed 's/^/  /'; fail=1; }; \
	done; exit $$fail

##@ Deploy - zero-downtime + rollback

.PHONY: deploy-zd
deploy-zd: ## Deploy zero-downtime (scale+1 → healthy → scale-1). IMAGE_TAG=<sha>
	@set -eu; \
	services="$${SERVICES:-backend frontend}"; poll_max="$${HEALTH_POLL_MAX:-240}"; \
	export IMAGE_TAG="$${IMAGE_TAG:-$$(git rev-parse --short HEAD)}"; \
	echo "[deploy-zd] IMAGE_TAG=$$IMAGE_TAG services=$$services poll_max=$${poll_max}s"; \
	rc=0; $(COMPOSE) exec -T backend python manage.py migrate_check || rc=$$?; \
	case "$$rc" in \
	    0) ;; \
	    1) echo "[deploy-zd] applying migrations"; $(COMPOSE) exec -T backend python manage.py migrate --noinput ;; \
	    2) echo "[deploy-zd] destructive migrations detected | deploy refused"; exit 2 ;; \
	    *) exit $$rc ;; \
	esac; \
	$(COMPOSE) pull $$services 2>/dev/null || true; \
	for s in $$services; do \
	    for c in $$($(COMPOSE) ps -a -q $$s); do \
	        state=$$(docker inspect -f '{{.State.Status}}' $$c 2>/dev/null || echo gone); \
	        health=$$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' $$c 2>/dev/null || echo none); \
	        case "$$state:$$health" in \
	            running:healthy|running:none|running:starting) ;; \
	            *) echo "[deploy-zd] nettoyage stale $$s: $$c (state=$$state health=$$health)"; docker rm -f $$c >/dev/null ;; \
	        esac; \
	    done; \
	    cur=$$($(COMPOSE) ps --filter status=running -q $$s | wc -l); [ $$cur -lt 1 ] && cur=1; tgt=$$((cur + 1)); \
	    echo "[deploy-zd] $$s: $$cur → $$tgt"; \
	    $(COMPOSE) up -d --no-deps --no-recreate --scale $$s=$$tgt $$s; \
	    w=0; while [ $$w -lt $$poll_max ]; do \
	        h=$$($(COMPOSE) ps --filter status=running -q $$s | xargs -r -I{} docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{end}}' {} | grep -cx healthy || true); \
	        [ "$$h" -ge "$$tgt" ] && break; sleep 2; w=$$((w+2)); \
	    done; \
	    if [ $$w -ge $$poll_max ]; then \
	        echo "[deploy-zd] timeout after $${poll_max}s | état des conteneurs $$s :"; \
	        $(COMPOSE) ps -a $$s; \
	        for c in $$($(COMPOSE) ps -a -q $$s); do \
	            echo "--- logs $$c (tail 50) ---"; docker logs --tail 50 $$c 2>&1 || true; \
	        done; \
	        exit 1; \
	    fi; \
	    $(COMPOSE) up -d --no-deps --scale $$s=$$cur $$s; \
	done; echo "[deploy-zd] done"

.PHONY: rollback
rollback: ## Rollback vers un tag précédent: make rollback TAG=<sha>
	@test -n "$(TAG)" || { echo "Usage: make rollback TAG=<sha>"; exit 1; }
	@IMAGE_TAG=$(TAG) $(COMPOSE) pull backend frontend
	@IMAGE_TAG=$(TAG) $(MAKE) deploy-zd IMAGE_TAG=$(TAG)

.PHONY: registry-login
registry-login: ## docker login sur le registry (attend CI_REGISTRY_* en env)
	@test -n "$${CI_REGISTRY:-}" || { echo "Export CI_REGISTRY / CI_REGISTRY_USER / CI_REGISTRY_PASSWORD"; exit 1; }
	@echo "$$CI_REGISTRY_PASSWORD" | docker login -u "$$CI_REGISTRY_USER" --password-stdin "$$CI_REGISTRY"

.PHONY: sbom
sbom: ## Génère SBOM SPDX JSON via syft (front + back)
	@command -v syft >/dev/null || { echo "syft requis: https://github.com/anchore/syft"; exit 1; }
	@mkdir -p dist
	syft apps/server -o spdx-json > dist/sbom-backend.spdx.json
	syft apps/client -o spdx-json > dist/sbom-frontend.spdx.json
	@echo "-> dist/sbom-*.spdx.json"

##@ Infra - Ansible

.PHONY: infra-check
infra-check: ## Dry-run Ansible (--check --diff)
	cd ansible && ansible-playbook -i inventories/$(ENV) playbooks/bootstrap.yml --ask-vault-pass --check --diff

.PHONY: infra-bootstrap
infra-bootstrap: ## Bootstrap VPS: docker + hardening + systemd (ENV=prod)
	cd ansible && ansible-playbook -i inventories/$(ENV) playbooks/bootstrap.yml --ask-vault-pass

.PHONY: infra-deploy
infra-deploy: ## Redeploy à distance via Ansible (git pull + deploy-zd)
	cd ansible && IMAGE_TAG="$${IMAGE_TAG:-$$(git rev-parse --short HEAD)}" \
	    ansible-playbook -i inventories/$(ENV) playbooks/deploy.yml --ask-vault-pass

.PHONY: infra-rotate
infra-rotate: ## Rotate la clé age sur le VPS (après rechiffrement local)
	cd ansible && ansible-playbook -i inventories/$(ENV) playbooks/rotate-secrets.yml --ask-vault-pass

##@ Observability - monitoring + SLO + Traefik

.PHONY: monitoring
monitoring: ## Démarre le profil monitoring (Grafana + Prometheus + Tempo + OTel)
	$(COMPOSE) --profile monitoring up -d --build

.PHONY: slo
slo: ## Availability 1d + p95 latency courants (via Prometheus)
	@for q in slo:api_availability:ratio_rate1d slo:api_latency:p95_5m; do \
	    printf "  %-40s " "$$q"; \
	    curl -sf "http://localhost:$${PROMETHEUS_PORT:-9090}/api/v1/query?query=$$q" \
	        | python3 -c "import json,sys; d=json.load(sys.stdin).get('data',{}).get('result',[]); print(d[0]['value'][1] if d else '(no data)')" 2>/dev/null || echo "(Prometheus down)"; \
	done

.PHONY: rules-test
rules-test: ## Valide la syntaxe des rules Prometheus SLO
	$(COMPOSE) --profile monitoring exec -T prometheus promtool check rules /etc/prometheus/rules/slo.yml

.PHONY: dashboards-lint
dashboards-lint: ## Valide le JSON des dashboards Grafana
	@for f in monitoring/grafana/dashboards/*.json; do \
	    python3 -c "import json; json.load(open('$$f'))" && echo "  OK $$f" || { echo "  FAIL $$f"; exit 1; }; \
	done

.PHONY: traefik-dashboard
traefik-dashboard: ## URL du dashboard Traefik (BasicAuth)
	@echo "https://traefik.$(DOMAIN)/dashboard/"

.PHONY: traefik-acme
traefik-acme: ## Liste les certs émis par Traefik (acme.json)
	@$(COMPOSE_EXEC) traefik sh -c 'cat /letsencrypt/acme.json | grep -oE "\"main\":\"[^\"]+\"" 2>/dev/null' || echo "(acme.json vide)"

##@ Bench & Status - k6 + /status

.PHONY: bench-local
bench-local: ## k6 contre la stack locale (valide perf avant push). SCENARIO=browse|contact|sustained
	@s="$${SCENARIO:-browse}"; f="bench/scenarios/$$s.js"; \
	[ -f "$$f" ] || { echo "Scénario introuvable: $$f"; exit 1; }; \
	docker run --rm -i --network host -v $(PWD)/bench:/bench \
	    -e BASE_URL=$${BASE_URL:-http://localhost:80} grafana/k6:latest run /$$f

PROD_DOMAIN      ?= aitaddajuba.fr

.PHONY: bench-prod
bench-prod: ## k6 contre https://$(PROD_DOMAIN) (override: BASE_URL=<url>)
	@s="$${SCENARIO:-browse}"; f="bench/scenarios/$$s.js"; \
	[ -f "$$f" ] || { echo "Scénario introuvable: $$f"; exit 1; }; \
	url=$${BASE_URL:-https://$(PROD_DOMAIN)}; \
	printf "Probe %s ... " "$$url"; \
	code=$$(curl -sS -o /dev/null -w "%{http_code}" --max-time 5 "$$url/" 2>/dev/null || echo "KO"); \
	case "$$code" in \
	    2*|3*) echo "OK ($$code)" ;; \
	    *) echo "KO ($$code) | URL inatteignable en <5s — bench annulé"; exit 1 ;; \
	esac; \
	docker run --rm -i -v $(PWD)/bench:/bench -e BASE_URL="$$url" grafana/k6:latest run /$$f

.PHONY: status-check
status-check: ## Teste /api/public/status/ (agrégation Prometheus + Alertmanager)
	@curl -fsS "http://localhost:$${NGINX_PORT:-80}/api/public/status/" | python3 -m json.tool

##@ SEO - audit meta · JSON-LD · Lighthouse

.PHONY: seo-build
seo-build: ## Type-check + build client (vérifie que les changements SEO compilent)
	cd $(CLIENT_DIR) && $(BUN) run type-check && $(BUN) run build

.PHONY: seo-ssr-check
seo-ssr-check: ## Curl les pages publiques + extrait meta/JSON-LD (dev server requis sur :3000)
	@for p in / /contact /blog /projects /stacks /experience; do \
	    printf "\n\033[1;33m--- %s ---\033[0m\n" "$$p"; \
	    body=$$(curl -fsS "http://localhost:3000$$p" 2>/dev/null) || { echo "  (page injoignable)"; continue; }; \
	    echo "$$body" | tr '<' '\n' | grep -iE '^(meta|link rel="canonical"|title)' \
	        | grep -iE 'og:|twitter:|name="description"|canonical|^title' \
	        | sed 's/>.*//;s/^/  /' | head -12; \
	    echo "$$body" | grep -oE '"@type"[[:space:]]*:[[:space:]]*"[^"]+"' | sort -u \
	        | sed -E 's/.*"([^"]+)"$$/  JSON-LD @type=\1/' || true; \
	done

.PHONY: seo-lighthouse
seo-lighthouse: ## Audit Lighthouse SEO. URL=https://juba-aitadda.dev/contact make seo-lighthouse
	@test -n "$(URL)" || { echo "Usage: URL=<page> make seo-lighthouse"; exit 1; }
	npx --yes lighthouse "$(URL)" --only-categories=seo --quiet --chrome-flags="--headless"

##@ Maintenance - clean + reset

.PHONY: clean
clean: ## Arrête la stack. VOLUMES=1 supprime aussi les volumes (DANGER)
	@if [ "$(VOLUMES)" = "1" ]; then \
	    read -p "Supprimer DB + uploads + certs ? (tapez 'oui') " ok && [ "$$ok" = "oui" ] || exit 1; \
	    $(COMPOSE_ALL) down -v --remove-orphans; \
	else $(COMPOSE_ALL) down --remove-orphans; fi

.PHONY: clean-cache
clean-cache: ## Vide caches Docker build + pip + bun
	docker builder prune -f
	rm -rf $(CLIENT_DIR)/node_modules $(CLIENT_DIR)/.nuxt $(CLIENT_DIR)/.output .pip-cache .bun-cache

.PHONY: redis-reset
redis-reset: ## Reset le volume Redis (corrige AOF corrompu)
	-$(COMPOSE) stop redis
	-$(COMPOSE) rm -fv redis
	@vol=$$(docker volume ls -q | grep '_redis_data$$' | head -1); \
	 [ -n "$$vol" ] && docker volume rm "$$vol"
	$(COMPOSE) up -d redis
