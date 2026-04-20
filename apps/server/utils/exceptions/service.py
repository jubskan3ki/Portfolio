"""Exceptions metier pour les services."""

from typing import Any


class ServiceError(Exception):
    default_message = "Une erreur est survenue."
    default_code = "service_error"

    def __init__(
        self,
        message: str | None = None,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message or self.default_message
        self.code = code or self.default_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        return {
            "error": self.code,
            "message": self.message,
            "details": self.details,
        }


class NotFoundError(ServiceError):
    default_message = "Ressource non trouvee."
    default_code = "not_found"


class ValidationError(ServiceError):
    default_message = "Donnees invalides."
    default_code = "validation_error"


class PermissionDeniedError(ServiceError):
    default_message = "Permission refusee."
    default_code = "permission_denied"


class ConflictError(ServiceError):
    default_message = "Conflit de donnees."
    default_code = "conflict"


class RateLimitError(ServiceError):
    default_message = "Trop de requetes. Reessayez plus tard."
    default_code = "rate_limit_exceeded"


class ExternalServiceError(ServiceError):
    default_message = "Erreur de service externe."
    default_code = "external_service_error"
