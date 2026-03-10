"""Custom permissions for the API."""

import logging
from typing import Any

from django.core.cache import cache
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

logger = logging.getLogger("security")


class IsAdminOnly(permissions.BasePermission):
    """Allow only admin/staff users."""

    def has_permission(self, request: Request, _view: APIView) -> bool:
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)

    def has_object_permission(self, request: Request, _view: APIView, obj: Any) -> bool:
        if request.user.is_staff:
            return True
        if hasattr(obj, "user"):
            return obj.user == request.user
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow read for all, write for admin only."""

    def has_permission(self, request: Request, _view: APIView) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class AllowAnonymousCreate(permissions.BasePermission):
    """
    Allow anonymous POST requests, require admin for other methods.

    WARNING: This permission allows unauthenticated users to create resources.
    Use ONLY with aggressive throttling and validation.

    Intended use cases:
        - Contact forms
        - Newsletter signups
        - Public feedback forms

    Security recommendations:
        - Always combine with ContactsThrottle or similar
        - Validate all input data thoroughly
        - Consider adding CAPTCHA for high-volume endpoints
        - Monitor for abuse patterns

    Example usage:
        class ContactViewSet(viewsets.ModelViewSet):
            permission_classes = [AllowAnonymousCreate]
            throttle_classes = [ContactsThrottle]
    """

    def has_permission(self, request: Request, _view: APIView) -> bool:
        if request.method == "POST":
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class ThrottledAnonymousCreate(AllowAnonymousCreate):
    """
    AllowAnonymousCreate with built-in IP abuse detection.

    Tracks POST attempts per IP and denies access after threshold.
    """

    # Number of failed attempts before blocking
    ABUSE_THRESHOLD = 20
    # Block duration in seconds (24 hours)
    BLOCK_DURATION = 86400

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method == "POST":
            if self._is_blocked_ip(request):
                logger.warning(
                    "Blocked IP attempted POST: %s on %s",
                    self._get_client_ip(request),
                    request.path,
                )
                return False
            return True
        return super().has_permission(request, view)

    def _get_client_ip(self, request: Request) -> str:
        """Get client IP from request."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "unknown")

    def _is_blocked_ip(self, request: Request) -> bool:
        """Check if IP is blocked due to abuse."""
        ip = self._get_client_ip(request)
        cache_key = f"abuse_block:{ip}"
        return cache.get(cache_key) is not None

    @classmethod
    def record_abuse(cls, request: Request) -> None:
        """
        Record an abuse attempt from the request IP.
        Call this from views when suspicious activity is detected.

        Uses atomic cache.incr() to prevent race conditions.
        """
        ip_header = request.META.get("HTTP_X_FORWARDED_FOR")
        ip = ip_header.split(",")[0].strip() if ip_header else request.META.get("REMOTE_ADDR", "unknown")

        abuse_key = f"abuse_count:{ip}"

        # Utiliser incr() atomique au lieu de get()+set()
        # Si la cle n'existe pas, on la cree d'abord
        try:
            count = cache.incr(abuse_key)
        except ValueError:
            # La cle n'existe pas, on la cree avec valeur 1
            cache.set(abuse_key, 1, cls.BLOCK_DURATION)
            count = 1

        if count >= cls.ABUSE_THRESHOLD:
            block_key = f"abuse_block:{ip}"
            cache.set(block_key, 1, cls.BLOCK_DURATION)
            logger.error(
                "IP blocked for abuse: %s after %d attempts",
                ip,
                count,
            )


class IsOwnerOrAdmin(permissions.BasePermission):
    """Allow access to resource owner or admin."""

    def has_object_permission(self, request: Request, _view: APIView, obj: Any) -> bool:
        if request.user.is_staff:
            return True
        if hasattr(obj, "user"):
            return obj.user == request.user
        if hasattr(obj, "owner"):
            return obj.owner == request.user
        return False


# Backward compatibility alias
AllowCreateAdminForRest = AllowAnonymousCreate
