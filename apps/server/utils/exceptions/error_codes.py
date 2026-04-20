"""Codes d'erreur standardises (1xxx auth, 2xxx validation, 3xxx serveur, 4xxx rate-limit, 5xxx contenu)."""

AUTH_INVALID_CREDENTIALS = {"code": "1001", "message": "Identifiants invalides."}

AUTH_EXPIRED_TOKEN = {"code": "1002", "message": "Token expiré."}

AUTH_INVALID_TOKEN = {"code": "1003", "message": "Token invalide."}

AUTH_USER_INACTIVE = {"code": "1004", "message": "Utilisateur inactif ou désactivé."}

AUTH_PERMISSION_DENIED = {"code": "1005", "message": "Permission refusée pour cette opération."}

VALIDATION_REQUIRED_FIELD = {"code": "2001", "message": "Champ obligatoire manquant."}

VALIDATION_INVALID_FORMAT = {"code": "2002", "message": "Format de données invalide."}

VALIDATION_ALREADY_EXISTS = {"code": "2003", "message": "Cette ressource existe déjà."}

VALIDATION_NOT_FOUND = {"code": "2004", "message": "Ressource introuvable."}

VALIDATION_INVALID_OPERATION = {"code": "2005", "message": "Opération invalide pour cette ressource."}

SERVER_INTERNAL_ERROR = {"code": "3001", "message": "Erreur interne du serveur."}

SERVER_SERVICE_UNAVAILABLE = {"code": "3002", "message": "Service temporairement indisponible."}

SERVER_DATABASE_ERROR = {"code": "3003", "message": "Erreur de base de données."}

SERVER_THIRD_PARTY_ERROR = {"code": "3004", "message": "Erreur d'un service externe."}

RATE_LIMIT_EXCEEDED = {"code": "4001", "message": "Limite de requêtes dépassée. Veuillez réessayer plus tard."}

CONTENT_TOO_LARGE = {"code": "5001", "message": "Contenu trop volumineux."}

CONTENT_INVALID_TYPE = {"code": "5002", "message": "Type de contenu non pris en charge."}


def get_error_detail(error_code, **kwargs):
    """Copie error_code et formate message avec kwargs."""
    error = error_code.copy()

    if kwargs:
        error["message"] = error["message"].format(**kwargs)

    return error


def format_validation_errors(validation_errors: dict) -> list[dict[str, str]]:
    """Django ValidationError.message_dict -> liste {code, message, field}."""
    formatted_errors: list[dict[str, str]] = []

    for field, errors in validation_errors.items():
        formatted_errors.extend(
            {"code": VALIDATION_INVALID_FORMAT["code"], "message": f"{field}: {error}", "field": field}
            for error in errors
        )

    return formatted_errors
