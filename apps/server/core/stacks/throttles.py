"""Throttles pour le module Stacks."""

from utils.throttles.base import BaseModuleThrottle


class StacksThrottle(BaseModuleThrottle):
    """
    Throttle pour les requetes sur les stacks.

    Rates:
        - GET/HEAD/OPTIONS: 100/minute (lecture)
        - POST/PUT/PATCH/DELETE: 10/minute (ecriture)
    """

    scope = "stack"
    read_rate = "100/minute"
    write_rate = "10/minute"
