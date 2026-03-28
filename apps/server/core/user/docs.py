"""Documentation pour le module User."""

from drf_spectacular.utils import OpenApiResponse

# LOGIN (tokens are set via HTTPOnly cookies)

LOGIN_RESPONSES = {
    200: OpenApiResponse(description="Connexion reussie, tokens dans cookies HTTPOnly"),
    401: OpenApiResponse(description="Identifiants invalides"),
    403: OpenApiResponse(description="Compte desactive ou sans permissions"),
    400: OpenApiResponse(description="Format de donnees invalide"),
}

# LOGOUT (reads refresh token from cookie)

LOGOUT_RESPONSES = {
    200: OpenApiResponse(description="Deconnexion reussie (cookies supprimes)"),
}

# REFRESH (reads refresh token from cookie, sets new tokens in cookies)

REFRESH_RESPONSES = {
    200: OpenApiResponse(description="Token rafraichi (nouveaux tokens dans cookies HTTPOnly)"),
    401: OpenApiResponse(description="Token invalide ou expire"),
}

# PROFILE

PROFILE_GET_RESPONSES = {
    200: OpenApiResponse(description="Profil recupere"),
    404: OpenApiResponse(description="Profil non trouve"),
    403: OpenApiResponse(description="Acces non autorise"),
}

PROFILE_PUT_RESPONSES = {
    200: OpenApiResponse(description="Profil mis a jour"),
    400: OpenApiResponse(description="Donnees invalides"),
    404: OpenApiResponse(description="Profil non trouve"),
    403: OpenApiResponse(description="Acces non autorise"),
}

# PASSWORD RESET

REQUEST_RESET_RESPONSES = {
    200: OpenApiResponse(description="Email envoye si l'adresse est valide"),
}

RESET_PASSWORD_RESPONSES = {
    200: OpenApiResponse(description="Mot de passe reinitialise"),
    400: OpenApiResponse(description="Donnees invalides"),
    403: OpenApiResponse(description="Code invalide ou expire"),
    404: OpenApiResponse(description="Utilisateur non trouve"),
}

CHANGE_PASSWORD_RESPONSES = {
    200: OpenApiResponse(description="Mot de passe modifie"),
    400: OpenApiResponse(description="Donnees invalides"),
    403: OpenApiResponse(description="Mot de passe actuel incorrect"),
}

# SESSIONS

SESSION_LIST_RESPONSES = {
    200: OpenApiResponse(description="Liste des sessions actives"),
}

SESSION_REVOKE_RESPONSES = {
    200: OpenApiResponse(description="Sessions revoquees"),
    404: OpenApiResponse(description="Session non trouvee"),
}
