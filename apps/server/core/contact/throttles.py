"""
Throttle personnalisé pour limiter les envois de messages de contact.
"""

from rest_framework.throttling import SimpleRateThrottle


class ContactMessageThrottle(SimpleRateThrottle):
    """
    Limite les requêtes à la vue de contact.
    """

    scope = "contact"

    def get_cache_key(self, request, view):
        return self.get_ident(request)
