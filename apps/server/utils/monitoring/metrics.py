"""Metriques Prometheus pour Django."""

from prometheus_client import Counter, Gauge, Histogram

PREFIX = "django"

REQUESTS_TOTAL = Counter(
    f"{PREFIX}_http_requests_total",
    "Total des requetes HTTP",
    ["method", "endpoint", "status"],
)

REQUEST_DURATION = Histogram(
    f"{PREFIX}_http_request_duration_seconds",
    "Duree des requetes HTTP en secondes",
    ["method", "endpoint"],
    buckets=(0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0),
)

REQUEST_IN_PROGRESS = Gauge(
    f"{PREFIX}_http_requests_in_progress",
    "Nombre de requetes en cours",
    ["method", "endpoint"],
)

DB_QUERY_DURATION = Histogram(
    f"{PREFIX}_db_query_duration_seconds",
    "Duree des requetes SQL en secondes",
    ["operation"],
    buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0),
)

DB_QUERY_TOTAL = Counter(
    f"{PREFIX}_db_queries_total",
    "Total des requetes SQL",
    ["operation"],
)

CACHE_HIT_COUNTER = Counter(
    f"{PREFIX}_cache_hits_total",
    "Total des cache hits",
    ["cache_name"],
)

CACHE_MISS_COUNTER = Counter(
    f"{PREFIX}_cache_misses_total",
    "Total des cache misses",
    ["cache_name"],
)

EXCEPTIONS_COUNTER = Counter(
    f"{PREFIX}_exceptions_total",
    "Total des exceptions",
    ["exception_type", "endpoint"],
)

ACTIVE_USERS_GAUGE = Gauge(
    f"{PREFIX}_active_users",
    "Nombre d'utilisateurs actifs",
)

ARTICLE_VIEWS_TOTAL = Counter(
    f"{PREFIX}_article_views_total",
    "Total des vues d'articles",
    ["article_slug"],
)

CELERY_TASKS_TOTAL = Counter(
    f"{PREFIX}_celery_tasks_total",
    "Total des taches Celery",
    ["task_name", "status"],
)

CELERY_TASK_DURATION = Histogram(
    f"{PREFIX}_celery_task_duration_seconds",
    "Duree des taches Celery en secondes",
    ["task_name"],
    buckets=(0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0, 120.0, 300.0),
)
