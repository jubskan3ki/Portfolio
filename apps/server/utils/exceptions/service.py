"""Exceptions metier pour les services."""

from typing import Any


class ServiceError(Exception):
    """Exception de base pour les erreurs de service."""

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
        """Convertit l'exception en dictionnaire pour la reponse API."""
        return {
            "error": self.code,
            "message": self.message,
            "details": self.details,
        }


class NotFoundError(ServiceError):
    """Ressource non trouvee."""

    default_message = "Ressource non trouvee."
    default_code = "not_found"


class ValidationError(ServiceError):
    """Erreur de validation des donnees."""

    default_message = "Donnees invalides."
    default_code = "validation_error"


class PermissionDeniedError(ServiceError):
    """Permission refusee."""

    default_message = "Permission refusee."
    default_code = "permission_denied"


class ConflictError(ServiceError):
    """Conflit de donnees (ex: doublon)."""

    default_message = "Conflit de donnees."
    default_code = "conflict"


class RateLimitError(ServiceError):
    """Limite de requetes atteinte."""

    default_message = "Trop de requetes. Reessayez plus tard."
    default_code = "rate_limit_exceeded"


class ExternalServiceError(ServiceError):
    """Erreur d'un service externe (email, API tierce)."""

    default_message = "Erreur de service externe."
    default_code = "external_service_error"
