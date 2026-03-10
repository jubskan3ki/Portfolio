"""Documentation Swagger pour le module User."""

from drf_yasg import openapi

# SCHEMAS COMMUNS

TOKEN_RESPONSE = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "access": openapi.Schema(type=openapi.TYPE_STRING, description="Token d'acces JWT"),
        "refresh": openapi.Schema(type=openapi.TYPE_STRING, description="Token de rafraichissement JWT"),
    },
)

USER_RESPONSE = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "email": openapi.Schema(type=openapi.TYPE_STRING),
        "first_name": openapi.Schema(type=openapi.TYPE_STRING),
        "last_name": openapi.Schema(type=openapi.TYPE_STRING),
    },
)

MESSAGE_RESPONSE = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "detail": openapi.Schema(type=openapi.TYPE_STRING, description="Message"),
    },
)

# LOGIN (tokens are set via HTTPOnly cookies)

LOGIN_RESPONSES = {
    200: openapi.Response(
        description="Connexion reussie (tokens dans cookies HTTPOnly)",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "user": USER_RESPONSE,
            },
        ),
    ),
    401: "Identifiants invalides",
    403: "Compte desactive ou sans permissions",
    400: "Format de donnees invalide",
}

# LOGOUT (reads refresh token from cookie)

LOGOUT_RESPONSES = {
    200: "Deconnexion reussie (cookies supprimes)",
}

# REFRESH (reads refresh token from cookie, sets new tokens in cookies)

REFRESH_RESPONSES = {
    200: openapi.Response(
        description="Token rafraichi (nouveaux tokens dans cookies HTTPOnly)",
        schema=MESSAGE_RESPONSE,
    ),
    401: "Token invalide ou expire",
}

# PROFILE

PROFILE_GET_RESPONSES = {
    200: "Profil recupere",
    404: "Profil non trouve",
    403: "Acces non autorise",
}

PROFILE_PUT_RESPONSES = {
    200: "Profil mis a jour",
    400: "Donnees invalides",
    404: "Profil non trouve",
    403: "Acces non autorise",
}

# PASSWORD RESET

REQUEST_RESET_RESPONSES = {
    200: openapi.Response(
        description="Email envoye si l'adresse est valide",
        schema=MESSAGE_RESPONSE,
    ),
}

RESET_PASSWORD_RESPONSES = {
    200: openapi.Response(description="Mot de passe reinitialise", schema=MESSAGE_RESPONSE),
    400: "Donnees invalides",
    403: "Code invalide ou expire",
    404: "Utilisateur non trouve",
}

CHANGE_PASSWORD_RESPONSES = {
    200: openapi.Response(description="Mot de passe modifie", schema=MESSAGE_RESPONSE),
    400: "Donnees invalides",
    403: "Mot de passe actuel incorrect",
}

# SESSIONS

SESSION_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_STRING, description="ID de session"),
        "device": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "browser": openapi.Schema(type=openapi.TYPE_STRING),
                "os": openapi.Schema(type=openapi.TYPE_STRING),
                "device": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        "created_at": openapi.Schema(type=openapi.TYPE_STRING, format="date-time"),
        "last_activity": openapi.Schema(type=openapi.TYPE_STRING, format="date-time"),
        "is_current": openapi.Schema(type=openapi.TYPE_BOOLEAN),
    },
)

SESSION_LIST_RESPONSES = {
    200: openapi.Response(
        description="Liste des sessions actives",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "sessions": openapi.Schema(type=openapi.TYPE_ARRAY, items=SESSION_SCHEMA),
                "count": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
    ),
}

SESSION_REVOKE_RESPONSES = {
    200: openapi.Response(description="Sessions revoquees", schema=MESSAGE_RESPONSE),
    404: "Session non trouvee",
}
