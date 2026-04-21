"""Gestion des exceptions et codes d'erreur pour l'API."""

from rest_framework import status

from .error_codes import (
    AUTH_EXPIRED_TOKEN,
    AUTH_INVALID_CREDENTIALS,
    AUTH_INVALID_TOKEN,
    AUTH_PERMISSION_DENIED,
    AUTH_USER_INACTIVE,
    CONTENT_INVALID_TYPE,
    CONTENT_TOO_LARGE,
    RATE_LIMIT_EXCEEDED,
    SERVER_DATABASE_ERROR,
    SERVER_INTERNAL_ERROR,
    SERVER_SERVICE_UNAVAILABLE,
    SERVER_THIRD_PARTY_ERROR,
    VALIDATION_ALREADY_EXISTS,
    VALIDATION_INVALID_FORMAT,
    VALIDATION_INVALID_OPERATION,
    VALIDATION_NOT_FOUND,
    VALIDATION_REQUIRED_FIELD,
    format_validation_errors,
    get_error_detail,
)
from .handlers import custom_exception_handler
from .service import ConflictError as ServiceConflictError
from .service import ExternalServiceError
from .service import NotFoundError as ServiceNotFoundError
from .service import PermissionDeniedError
from .service import RateLimitError as ServiceRateLimitError
from .service import ServiceError
from .service import ValidationError as ServiceValidationError


class APIError(Exception):
    default_status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail: str = "Une erreur interne s'est produite."

    def __init__(self, detail=None, status_code=None, code=None):
        self.detail = detail or self.default_detail
        self.status_code = status_code or self.default_status_code
        self.code = code
        super().__init__(self.detail)


class ValidationError(APIError):
    default_status_code: int = status.HTTP_400_BAD_REQUEST
    default_detail: str = "Les donnees fournies sont invalides."


class AuthenticationError(APIError):
    default_status_code: int = status.HTTP_401_UNAUTHORIZED
    default_detail: str = "Authentification requise."


class AccessDeniedError(APIError):
    default_status_code: int = status.HTTP_403_FORBIDDEN
    default_detail: str = "Vous n'avez pas les permissions necessaires."


class NotFoundError(APIError):
    default_status_code: int = status.HTTP_404_NOT_FOUND
    default_detail: str = "La ressource demandee n'existe pas."


class ConflictError(APIError):
    default_status_code: int = status.HTTP_409_CONFLICT
    default_detail: str = "Un conflit est survenu avec la ressource existante."


class ThirdPartyServiceError(APIError):
    default_status_code: int = status.HTTP_502_BAD_GATEWAY
    default_detail: str = "Erreur lors de la communication avec un service externe."


class RateLimitError(APIError):
    default_status_code: int = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail: str = "Trop de requetes. Veuillez reessayer plus tard."


__all__ = [
    "AUTH_EXPIRED_TOKEN",
    "AUTH_INVALID_CREDENTIALS",
    "AUTH_INVALID_TOKEN",
    "AUTH_PERMISSION_DENIED",
    "AUTH_USER_INACTIVE",
    "CONTENT_INVALID_TYPE",
    "CONTENT_TOO_LARGE",
    "RATE_LIMIT_EXCEEDED",
    "SERVER_DATABASE_ERROR",
    "SERVER_INTERNAL_ERROR",
    "SERVER_SERVICE_UNAVAILABLE",
    "SERVER_THIRD_PARTY_ERROR",
    "VALIDATION_ALREADY_EXISTS",
    "VALIDATION_INVALID_FORMAT",
    "VALIDATION_INVALID_OPERATION",
    "VALIDATION_NOT_FOUND",
    "VALIDATION_REQUIRED_FIELD",
    "APIError",
    "AccessDeniedError",
    "AuthenticationError",
    "ConflictError",
    "ExternalServiceError",
    "NotFoundError",
    "PermissionDeniedError",
    "RateLimitError",
    "ServiceConflictError",
    "ServiceError",
    "ServiceNotFoundError",
    "ServiceRateLimitError",
    "ServiceValidationError",
    "ThirdPartyServiceError",
    "ValidationError",
    "custom_exception_handler",
    "format_validation_errors",
    "get_error_detail",
]
