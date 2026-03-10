"""Throttles pour le module experiences."""

from utils.throttles.base import BaseModuleThrottle


class ExperienceThrottle(BaseModuleThrottle):
    """
    Throttle pour les endpoints experiences.

    Rates:
        - GET/HEAD/OPTIONS: 100/minute (lecture)
        - POST/PUT/PATCH/DELETE: 10/minute (ecriture)
    """

    scope = "experience"
    read_rate = "100/minute"
    write_rate = "10/minute"
