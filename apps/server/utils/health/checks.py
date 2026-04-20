"""Health check functions for various services."""

import logging
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any

from django.conf import settings
from django.db import connection

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


@dataclass
class HealthCheckResult:
    name: str
    status: HealthStatus
    latency_ms: float
    message: str = ""
    details: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "name": self.name,
            "status": self.status.value,
            "latency_ms": round(self.latency_ms, 2),
        }
        if self.message:
            result["message"] = self.message
        if self.details:
            result["details"] = self.details
        return result


def check_database() -> HealthCheckResult:
    start = time.perf_counter()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        latency = (time.perf_counter() - start) * 1000

        status = HealthStatus.DEGRADED if latency > 100 else HealthStatus.HEALTHY

        return HealthCheckResult(
            name="database",
            status=status,
            latency_ms=latency,
            details={"vendor": connection.vendor},
        )
    except Exception as e:
        latency = (time.perf_counter() - start) * 1000
        logger.exception("Database health check failed")
        return HealthCheckResult(
            name="database",
            status=HealthStatus.UNHEALTHY,
            latency_ms=latency,
            message=str(e),
        )


def check_redis() -> HealthCheckResult:
    start = time.perf_counter()
    try:
        from django.core.cache import cache

        test_key = "_health_check_"
        cache.set(test_key, "ok", timeout=10)
        value = cache.get(test_key)
        cache.delete(test_key)

        latency = (time.perf_counter() - start) * 1000

        if value != "ok":
            return HealthCheckResult(
                name="redis",
                status=HealthStatus.UNHEALTHY,
                latency_ms=latency,
                message="Cache read/write test failed",
            )

        status = HealthStatus.DEGRADED if latency > 50 else HealthStatus.HEALTHY

        return HealthCheckResult(
            name="redis",
            status=status,
            latency_ms=latency,
        )
    except Exception as e:
        latency = (time.perf_counter() - start) * 1000
        logger.exception("Redis health check failed")
        return HealthCheckResult(
            name="redis",
            status=HealthStatus.UNHEALTHY,
            latency_ms=latency,
            message=str(e),
        )


def check_celery() -> HealthCheckResult:
    start = time.perf_counter()
    try:
        from config.celery import app as celery_app

        inspector = celery_app.control.inspect()
        stats = inspector.stats()

        latency = (time.perf_counter() - start) * 1000

        if not stats:
            return HealthCheckResult(
                name="celery",
                status=HealthStatus.UNHEALTHY,
                latency_ms=latency,
                message="No Celery workers responding",
            )

        worker_count = len(stats)
        return HealthCheckResult(
            name="celery",
            status=HealthStatus.HEALTHY,
            latency_ms=latency,
            details={"workers": worker_count},
        )
    except Exception as e:
        latency = (time.perf_counter() - start) * 1000
        logger.exception("Celery health check failed")
        return HealthCheckResult(
            name="celery",
            status=HealthStatus.UNHEALTHY,
            latency_ms=latency,
            message=str(e),
        )


def run_all_checks() -> dict[str, Any]:
    checks = [
        check_database(),
        check_redis(),
    ]

    # Celery optionnel (ping worker peut etre lent).
    if getattr(settings, "CELERY_BROKER_URL", None):
        checks.append(check_celery())

    statuses = [c.status for c in checks]
    if HealthStatus.UNHEALTHY in statuses:
        overall_status = HealthStatus.UNHEALTHY
    elif HealthStatus.DEGRADED in statuses:
        overall_status = HealthStatus.DEGRADED
    else:
        overall_status = HealthStatus.HEALTHY

    return {
        "status": overall_status.value,
        "checks": [c.to_dict() for c in checks],
        "version": getattr(settings, "APP_VERSION", "1.0.0"),
    }
