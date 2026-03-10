"""Base throttle classes with differentiated GET/POST rates."""

import logging
from typing import ClassVar

from django.conf import settings
from rest_framework.request import Request
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.views import APIView

logger = logging.getLogger("django.request")

SAFE_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})


class BaseModuleThrottle(SimpleRateThrottle):
    """
    Base throttle that applies different rates for read vs write operations.

    Subclasses should define:
        - scope: The base scope name (e.g., "articles")
        - read_rate: Rate for GET/HEAD/OPTIONS (e.g., "100/minute")
        - write_rate: Rate for POST/PUT/PATCH/DELETE (e.g., "10/minute")

    If read_rate or write_rate is None, uses the default from settings.

    Standard rates used across most modules:
        - read_rate = "100/minute", write_rate = "10/minute"
          (articles, projects, stacks, experiences)
        - contact uses custom rates: read=30/min, write=5/hour
        - webhooks, transfer, stats have their own rates

    Each module defines its own throttle class with a unique scope for
    independent rate tracking, even when rates are identical.
    """

    scope: str = ""
    read_rate: str | None = None
    write_rate: str | None = None

    # Cache for parsed rates
    _rate_cache: ClassVar[dict[str, tuple[int, int] | None]] = {}

    def __init__(self) -> None:
        # Don't call parent __init__ as we override get_rate
        self.key: str | None = None
        self.history: list = []
        self.now: float = 0.0

    def get_cache_key(self, request: Request, view: APIView) -> str:
        """Generate a unique cache key for throttling."""
        ident = self.get_ident(request)
        action = getattr(view, "action", None) or view.__class__.__name__
        method = request.method
        rate_type = "read" if method in SAFE_METHODS else "write"

        return f"throttle_{self.scope}_{rate_type}_{action}_{ident}"

    def get_rate(self) -> str | None:
        """Get the appropriate rate based on request method."""
        if not hasattr(self, "request"):
            return self.write_rate or self._get_default_rate()

        if self.request.method in SAFE_METHODS:
            return self.read_rate or self._get_default_rate("read")
        return self.write_rate or self._get_default_rate("write")

    def _get_default_rate(self, rate_type: str = "write") -> str | None:
        """Get default rate from settings."""
        throttle_rates = getattr(settings, "REST_FRAMEWORK", {}).get("DEFAULT_THROTTLE_RATES", {})

        # Try module-specific rate first
        rate_key = f"{self.scope}_{rate_type}" if rate_type else self.scope
        if rate_key in throttle_rates:
            return throttle_rates[rate_key]

        # Fallback to base scope rate
        if self.scope in throttle_rates:
            return throttle_rates[self.scope]

        # Ultimate fallback
        return throttle_rates.get("anon", "20/minute")

    def allow_request(self, request: Request, view: APIView) -> bool:
        """Check if request is allowed and log abuse attempts."""
        # Store request for use in get_rate
        self.request = request

        # Parse rate for current request type
        self.rate = self.get_rate()
        if self.rate is None:
            return True

        self.num_requests, self.duration = self.parse_rate(self.rate)
        if self.num_requests is None or self.duration is None:
            return True

        # Check throttle
        self.key = self.get_cache_key(request, view)
        self.history = self.cache.get(self.key, [])
        self.now = self.timer()

        # Remove old entries
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()

        if len(self.history) >= self.num_requests:
            self._log_throttle_exceeded(request)
            return self.throttle_failure()

        return self.throttle_success()

    def throttle_success(self) -> bool:
        """Handle successful request (under rate limit)."""
        self.history.insert(0, self.now)
        self.cache.set(self.key, self.history, self.duration)
        return True

    def throttle_failure(self) -> bool:
        """Handle throttled request."""
        return False

    def _log_throttle_exceeded(self, request: Request) -> None:
        """Log when throttle limit is exceeded."""
        ip = self.get_ident(request)
        rate_type = "read" if request.method in SAFE_METHODS else "write"
        logger.warning(
            "Throttle exceeded for %s (%s): %s %s from IP %s - Rate: %s",
            self.scope,
            rate_type,
            request.method,
            request.path,
            ip,
            self.rate,
        )

    def wait(self) -> float | None:
        """Return the recommended wait time before next request."""
        if self.history and self.duration is not None and self.num_requests is not None:
            remaining_duration = self.duration - (self.now - self.history[-1])
            available_requests = self.num_requests - len(self.history) + 1
            if available_requests <= 0:
                return remaining_duration
        return None


class StaffBypassThrottle(BaseModuleThrottle):
    """Throttle that allows staff users to bypass rate limiting."""

    def allow_request(self, request: Request, view: APIView) -> bool:
        """Allow staff users to bypass throttling."""
        if request.user and request.user.is_authenticated and request.user.is_staff:
            return True
        return super().allow_request(request, view)
