"""Throttling pour le module webhooks."""

from utils.throttles.base import BaseModuleThrottle


class WebhooksThrottle(BaseModuleThrottle):
    """
    Throttle pour limiter les actions sur les webhooks.

    Rates:
        - GET/HEAD/OPTIONS: 60/minute (lecture)
        - POST/PUT/PATCH/DELETE: 10/minute (ecriture)
    """

    scope = "webhooks"
    read_rate = "60/minute"
    write_rate = "10/minute"
