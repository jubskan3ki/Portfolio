"""
Codes d'erreur standardisés pour l'API.
Centralise les codes et messages d'erreur utilisés dans l'application.
"""

# Erreurs d'authentification (1000-1999)
AUTH_INVALID_CREDENTIALS = {"code": "1001", "message": "Identifiants invalides."}

AUTH_EXPIRED_TOKEN = {"code": "1002", "message": "Token expiré."}

AUTH_INVALID_TOKEN = {"code": "1003", "message": "Token invalide."}

AUTH_USER_INACTIVE = {"code": "1004", "message": "Utilisateur inactif ou désactivé."}

AUTH_PERMISSION_DENIED = {"code": "1005", "message": "Permission refusée pour cette opération."}

# Erreurs de validation (2000-2999)
VALIDATION_REQUIRED_FIELD = {"code": "2001", "message": "Champ obligatoire manquant."}

VALIDATION_INVALID_FORMAT = {"code": "2002", "message": "Format de données invalide."}

VALIDATION_ALREADY_EXISTS = {"code": "2003", "message": "Cette ressource existe déjà."}

VALIDATION_NOT_FOUND = {"code": "2004", "message": "Ressource introuvable."}

VALIDATION_INVALID_OPERATION = {"code": "2005", "message": "Opération invalide pour cette ressource."}

# Erreurs de serveur (3000-3999)
SERVER_INTERNAL_ERROR = {"code": "3001", "message": "Erreur interne du serveur."}

SERVER_SERVICE_UNAVAILABLE = {"code": "3002", "message": "Service temporairement indisponible."}

SERVER_DATABASE_ERROR = {"code": "3003", "message": "Erreur de base de données."}

SERVER_THIRD_PARTY_ERROR = {"code": "3004", "message": "Erreur d'un service externe."}

# Erreurs de limitation de débit (4000-4999)
RATE_LIMIT_EXCEEDED = {"code": "4001", "message": "Limite de requêtes dépassée. Veuillez réessayer plus tard."}

# Erreurs de contenu (5000-5999)
CONTENT_TOO_LARGE = {"code": "5001", "message": "Contenu trop volumineux."}

CONTENT_INVALID_TYPE = {"code": "5002", "message": "Type de contenu non pris en charge."}


def get_error_detail(error_code, **kwargs):
    """
    Récupère les détails d'erreur avec des placeholders optionnels.

    Args:
        error_code: Dictionnaire contenant code et message d'erreur
        **kwargs: Variables à insérer dans le message

    Returns:
        Dictionnaire avec le code et message formatés
    """
    error = error_code.copy()

    if kwargs:
        error["message"] = error["message"].format(**kwargs)

    return error


def format_validation_errors(validation_errors: dict) -> list[dict[str, str]]:
    """
    Formate les erreurs de validation Django en format API standardisé.

    Args:
        validation_errors: Dictionnaire d'erreurs de validation Django

    Returns:
        Liste d'erreurs au format standardisé
    """
    formatted_errors: list[dict[str, str]] = []

    for field, errors in validation_errors.items():
        formatted_errors.extend(
            {"code": VALIDATION_INVALID_FORMAT["code"], "message": f"{field}: {error}", "field": field}
            for error in errors
        )

    return formatted_errors
