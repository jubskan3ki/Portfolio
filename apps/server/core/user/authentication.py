"""
Fichier de configuration de l'authentification de l'utilisateur.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class EmailBackend(ModelBackend):
    """
    Authentifie l'utilisateur via l'email au lieu du username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        email = username or kwargs.get("email")
        if not email or not password:
            return None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        if not user.is_active:
            return None
        if user.check_password(password):
            return user
        return None
