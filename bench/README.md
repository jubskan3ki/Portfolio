# Bench (k6) | charge + détection de régression perf

Scénarios :

- `browse.js` | parcours home → projects → detail, 50 VU 2 min (charge réaliste).
- `contact.js` | forme `POST /api/contacts/` pendant 30s avec 10 VU (teste le
  rate-limit contact | doit bloquer après 3 req/min).
- `sustained.js` | 5 VU pendant 15 min (détecte les fuites mémoire sur la durée).

## Local

```bash
make bench-local SCENARIO=browse       # http://localhost:80
```

## Staging / prod

```bash
make bench-staging SCENARIO=browse
make bench-prod    SCENARIO=sustained   # attention, compte dans le budget SLO
```

## CI nightly (staging uniquement)

Schedule GitLab CI `02:00 UTC` sur `main` → le job `perf:k6:nightly` lance
`browse.js + sustained.js` sur staging et pousse les métriques vers Prometheus
staging via `--out experimental-prometheus-rw=...`.

Les résultats sont visibles dans Grafana → dashboard `k6 Overview` (si créé)
ou directement via la datasource Prometheus (métriques `k6_http_req_*`).

## Seuils

Tous les scripts ont des `thresholds` k6 qui bloquent si dépassés :

- `http_req_failed < 1%`
- `http_req_duration p(95) < 500ms`
- `contact_rate_limited > 10` (prouve que le rate-limit Traefik fonctionne)

Un seuil dépassé → pipeline CI rouge → Discord ping via Alertmanager si la
régression remonte aussi dans les SLO Prometheus.
