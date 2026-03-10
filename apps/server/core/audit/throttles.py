"""Throttling pour le module audit."""

from utils.throttles.base import BaseModuleThrottle


class AuditThrottle(BaseModuleThrottle):
    """
    Throttle pour limiter les actions sur les logs d'audit.

    Rates:
        - GET/HEAD/OPTIONS: 60/minute (lecture)
        - POST/PUT/PATCH/DELETE: 0 (pas d'ecriture via API)
    """

    scope = "audit"
    read_rate = "60/minute"
    write_rate = "0/minute"
