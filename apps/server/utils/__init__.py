"""Utilitaires communs pour le projet."""

from .email import (
    send_multi_part_email,
    send_templated_email,
)
from .exceptions import (
    AccessDeniedError,
    APIError,
    AuthenticationError,
    ConflictError,
    NotFoundError,
    RateLimitError,
    ThirdPartyServiceError,
    ValidationError,
)
from .network import get_client_ip
from .pagination import (
    CursorBasedPagination,
    CustomPagination,
    StandardResultsSetPagination,
)
from .validators import (
    validate_alphanumeric,
    validate_date_format,
    validate_email,
    validate_file_extension,
    validate_image_size,
    validate_numeric,
    validate_password,
    validate_phone_number,
    validate_reset_code,
    validate_slug,
    validate_url,
)

__all__ = [
    "APIError",
    "AccessDeniedError",
    "AuthenticationError",
    "ConflictError",
    "CursorBasedPagination",
    "CustomPagination",
    "NotFoundError",
    "RateLimitError",
    "StandardResultsSetPagination",
    "ThirdPartyServiceError",
    "ValidationError",
    "get_client_ip",
    "send_multi_part_email",
    "send_templated_email",
    "validate_alphanumeric",
    "validate_date_format",
    "validate_email",
    "validate_file_extension",
    "validate_image_size",
    "validate_numeric",
    "validate_password",
    "validate_phone_number",
    "validate_reset_code",
    "validate_slug",
    "validate_url",
]
