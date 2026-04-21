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
    """Anonymous POST, admin for other methods. Combine with aggressive throttling."""

    def has_permission(self, request: Request, _view: APIView) -> bool:
        if request.method == "POST":
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class ThrottledAnonymousCreate(AllowAnonymousCreate):
    """AllowAnonymousCreate with IP abuse detection | blocks after threshold."""

    ABUSE_THRESHOLD = 20
    BLOCK_DURATION = 86400  # 24h

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
        """Record abuse from IP; atomic incr() prevents race conditions."""
        ip_header = request.META.get("HTTP_X_FORWARDED_FOR")
        ip = ip_header.split(",")[0].strip() if ip_header else request.META.get("REMOTE_ADDR", "unknown")

        abuse_key = f"abuse_count:{ip}"

        try:
            count = cache.incr(abuse_key)
        except ValueError:
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


AllowCreateAdminForRest = AllowAnonymousCreate
