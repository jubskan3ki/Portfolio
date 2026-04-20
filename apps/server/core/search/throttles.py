"""Throttling pour la recherche full-text."""

from rest_framework.throttling import ScopedRateThrottle


class SearchThrottle(ScopedRateThrottle):
    """Throttle scope='search' : 60/min (anon + user confondus par defaut)."""

    scope = "search"
