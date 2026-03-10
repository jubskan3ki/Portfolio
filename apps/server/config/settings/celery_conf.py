"""Celery configuration."""

from typing import cast

from config.settings.base import TIME_ZONE, env

# CELERY

CELERY_BROKER_URL = cast(str, env("CELERY_BROKER_URL"))
CELERY_RESULT_BACKEND = cast(str, env("REDIS_URL")).replace("/1", "/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_CONNECTION_RETRY = True
CELERY_BROKER_CONNECTION_MAX_RETRIES = 10
CELERY_BROKER_POOL_LIMIT = 10
CELERY_BROKER_HEARTBEAT = 30
CELERY_BROKER_HEARTBEAT_CHECKRATE = 2.0

CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1000
CELERY_WORKER_DISABLE_RATE_LIMITS = True

CELERY_TASK_SOFT_TIME_LIMIT = 300
CELERY_TASK_TIME_LIMIT = 600
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_TASK_DEFAULT_RETRY_DELAY = 60
CELERY_TASK_MAX_RETRIES = 3

CELERY_WORKER_HIJACK_ROOT_LOGGER = False
CELERY_WORKER_LOG_COLOR = False
CELERY_TASK_IGNORE_RESULT = False
CELERY_RESULT_EXPIRES = 3600

CELERY_RESULT_BACKEND_TRANSPORT_OPTIONS = {"retry_policy": {"timeout": 5.0}}
CELERY_BROKER_TRANSPORT_OPTIONS = {
    "priority_steps": list(range(10)),
    "max_retries": 5,
    "interval_start": 0,
    "interval_step": 0.2,
    "interval_max": 10,
}

# CELERY BEAT SCHEDULE

CELERY_BEAT_SCHEDULE = {
    "retry-failed-webhook-deliveries": {
        "task": "core.webhooks.tasks.retry_failed_webhook_deliveries",
        "schedule": 300.0,  # Every 5 minutes
    },
    "cleanup-old-webhook-deliveries": {
        "task": "core.webhooks.tasks.cleanup_old_webhook_deliveries",
        "schedule": 86400.0,  # Every 24 hours
    },
    "cleanup-old-transfer-jobs": {
        "task": "data_transfer.cleanup_old_jobs",
        "schedule": 86400.0,  # Every 24 hours
    },
}
