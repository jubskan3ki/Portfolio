"""Middleware for request correlation ID tracking."""

import logging
import uuid
from collections.abc import Callable
from typing import Protocol, cast

from django.http import HttpRequest, HttpResponse

logger = logging.getLogger("django.request")


class CorrelatedRequest(Protocol):
    """Protocol for HttpRequest with correlation attributes."""

    correlation_id: str
    request_id: str


class CorrelationIdMiddleware:
    """
    Middleware that adds correlation IDs to requests for distributed tracing.

    The correlation ID is:
    - Extracted from X-Correlation-ID header if provided by client
    - Generated as a new UUID if not provided
    - Added to the response headers
    - Available on request.correlation_id for logging

    Usage in views/services:
        correlation_id = getattr(request, 'correlation_id', 'unknown')
        logger.info("Processing request", extra={'correlation_id': correlation_id})
    """

    HEADER_NAME = "X-Correlation-ID"
    REQUEST_ID_HEADER = "X-Request-ID"

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Get or generate correlation ID
        correlation_id = self._get_correlation_id(request)
        request_id = str(uuid.uuid4())[:8]  # Short unique ID for this specific request

        # Attach to request object (dynamic attributes)
        correlated = cast(CorrelatedRequest, request)
        correlated.correlation_id = correlation_id
        correlated.request_id = request_id

        # Process request
        response = self.get_response(request)

        # Add to response headers
        response[self.HEADER_NAME] = correlation_id
        response[self.REQUEST_ID_HEADER] = request_id

        return response

    def _get_correlation_id(self, request: HttpRequest) -> str:
        """Extract correlation ID from headers or generate a new one."""
        # Check for existing correlation ID in headers
        correlation_id = request.headers.get(self.HEADER_NAME)

        if correlation_id:
            # Validate format (should be a valid UUID or similar)
            if len(correlation_id) <= 64 and correlation_id.replace("-", "").isalnum():
                return correlation_id
            logger.warning(
                "Invalid correlation ID received: %s, generating new one",
                correlation_id[:50],
            )

        # Generate new UUID
        return str(uuid.uuid4())


def get_correlation_id(request: HttpRequest) -> str:
    """
    Helper function to get correlation ID from request.

    Args:
        request: Django HttpRequest object

    Returns:
        Correlation ID string or 'unknown' if not available
    """
    return getattr(request, "correlation_id", "unknown")


def get_request_id(request: HttpRequest) -> str:
    """
    Helper function to get request ID from request.

    Args:
        request: Django HttpRequest object

    Returns:
        Request ID string or 'unknown' if not available
    """
    return getattr(request, "request_id", "unknown")
