"""Middleware for setting audit context from requests."""

from collections.abc import Callable

from django.http import HttpRequest, HttpResponse

from core.audit.signals import clear_audit_context, set_audit_context
from utils.network import get_client_ip


class AuditContextMiddleware:
    """
    Middleware that captures request context for audit logging.

    This middleware extracts user, IP, user agent, and correlation ID
    from the request and makes them available to the audit signal handlers.

    Add this middleware AFTER authentication middleware in settings.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        self._set_context(request)

        try:
            return self.get_response(request)
        finally:
            clear_audit_context()

    def _set_context(self, request: HttpRequest) -> None:
        """Extract and set audit context from request."""
        user = None
        if hasattr(request, "user") and request.user.is_authenticated:
            user = request.user

        ip_address = self._get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        # correlation_id est pose par CorrelationIdMiddleware (amont).
        correlation_id = getattr(request, "correlation_id", "")

        set_audit_context(
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
            correlation_id=correlation_id,
        )

    def _get_client_ip(self, request: HttpRequest) -> str | None:
        """Extract client IP (proxy-safe, voir utils.network)."""
        return get_client_ip(request) or None
