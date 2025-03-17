"""
Throttling personnalisé pour les articles de blog.
"""

from rest_framework.throttling import SimpleRateThrottle


class BlogPostThrottle(SimpleRateThrottle):
    """
    Throttle pour limiter les actions sur les articles de blog.
    """

    scope = "blog"

    def get_cache_key(self, request, view):
        return self.get_ident(request)
