"""
Validation personnalisée des données utilisateurs et formulaires.
"""

import re

from django.core.exceptions import ValidationError


def validate_email(value):
    """Vérifie si l'email est valide."""
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not re.match(email_regex, value):
        raise ValidationError("L'email fourni n'est pas valide.")


def validate_password(value):
    """Vérifie la sécurité du mot de passe (8+ caractères, majuscules, chiffres, symboles)."""
    if len(value) < 8:
        raise ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
    if not any(char.isupper() for char in value):
        raise ValidationError("Le mot de passe doit contenir au moins une majuscule.")
    if not any(char.isdigit() for char in value):
        raise ValidationError("Le mot de passe doit contenir au moins un chiffre.")
    if not any(char in "!@#$%^&*()-_=+{}[]|;:'\",.<>?/`~" for char in value):
        raise ValidationError("Le mot de passe doit contenir au moins un caractère spécial.")


def validate_reset_code(value):
    """Vérifie si le code de réinitialisation est un nombre à 6 chiffres."""
    if not value.isdigit() or len(value) != 6:
        raise ValidationError("Le code de réinitialisation doit être un nombre à 6 chiffres.")
