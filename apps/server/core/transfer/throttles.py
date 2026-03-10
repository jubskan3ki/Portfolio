"""Throttling pour le module Data Transfer."""

from rest_framework.throttling import UserRateThrottle


class ExportThrottle(UserRateThrottle):
    """Limite le nombre d'exports par utilisateur."""

    scope = "export"
    rate = "60/hour"


class ImportThrottle(UserRateThrottle):
    """Limite le nombre d'imports par utilisateur."""

    scope = "import"
    rate = "30/hour"
