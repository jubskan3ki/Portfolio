"""Validation des donnees utilisateurs et formulaires."""

import ipaddress
import re
from datetime import UTC, datetime
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_validate_email

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
PHONE_REGEX = re.compile(r"^\+?[0-9]{1,4}[-\s]?[0-9]{6,14}$")
URL_REGEX = re.compile(r"^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$")
SLUG_REGEX = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SPECIAL_CHARS = "!@#$%^&*()-_=+{}[]|;:'\",.<>?/`~"
DEFAULT_EXTENSIONS = (".pdf", ".doc", ".docx", ".jpg", ".jpeg", ".png")


def validate_email(value):
    try:
        django_validate_email(value)
    except ValidationError as exc:
        raise ValidationError("L'email fourni n'est pas valide.") from exc

    if not EMAIL_REGEX.match(value):
        raise ValidationError("L'email fourni n'est pas valide.")


def validate_password(value):
    """8+ chars, majuscule, chiffre, symbole."""
    errors = []

    if len(value) < 8:
        errors.append("Le mot de passe doit contenir au moins 8 caracteres.")

    if not any(char.isupper() for char in value):
        errors.append("Le mot de passe doit contenir au moins une majuscule.")

    if not any(char.isdigit() for char in value):
        errors.append("Le mot de passe doit contenir au moins un chiffre.")

    if not any(char in SPECIAL_CHARS for char in value):
        errors.append("Le mot de passe doit contenir au moins un caractere special.")

    if errors:
        raise ValidationError(errors)


RESET_CODE_REGEX = re.compile(r"^[A-Z0-9]{8}$")


def validate_reset_code(value):
    if not RESET_CODE_REGEX.match(value):
        raise ValidationError(
            "Le code de reinitialisation doit contenir 8 caracteres alphanumeriques (majuscules et chiffres)."
        )


def validate_phone_number(value):
    if not PHONE_REGEX.match(value):
        raise ValidationError("Le numero de telephone doit etre au format international valide.")


def validate_url(value):
    if not URL_REGEX.match(value):
        raise ValidationError("L'URL doit commencer par http:// ou https:// et etre valide.")


def validate_date_format(value, format_str="%Y-%m-%d"):
    try:
        datetime.strptime(value, format_str).replace(tzinfo=UTC)
    except ValueError as exc:
        raise ValidationError(f"La date doit etre au format {format_str}.") from exc


def validate_slug(value):
    if not SLUG_REGEX.match(value):
        raise ValidationError("Le slug ne peut contenir que des lettres minuscules, chiffres et tirets.")


def validate_alphanumeric(value):
    if not value.isalnum():
        raise ValidationError("Ce champ ne peut contenir que des lettres et des chiffres.")


def validate_numeric(value):
    if not value.isdigit():
        raise ValidationError("Ce champ ne peut contenir que des chiffres.")


def validate_image_size(image, max_size_kb=2048):
    if image.size > max_size_kb * 1024:
        raise ValidationError(f"L'image ne doit pas depasser {max_size_kb} KB.")


def validate_string_list(value, item_label="element"):
    """Valide liste de strings; item_label pour les messages d'erreur."""
    if not isinstance(value, list):
        raise ValidationError("Doit etre une liste.")
    for item in value:
        if not isinstance(item, str):
            raise ValidationError(f"Chaque {item_label} doit etre une chaine.")
    return value


def validate_file_extension(value, allowed_extensions=None):
    if allowed_extensions is None:
        allowed_extensions = DEFAULT_EXTENSIONS

    ext = Path(value.name).suffix.lower()
    if ext not in allowed_extensions:
        raise ValidationError(f"Seules les extensions suivantes sont autorisees: {', '.join(allowed_extensions)}")


IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg")


def validate_image_upload(value):
    ext = Path(value.name).suffix.lower()
    if ext not in IMAGE_EXTENSIONS:
        raise ValidationError(f"Extension '{ext}' non autorisee. Extensions acceptees: {', '.join(IMAGE_EXTENSIONS)}")


# Anti-SSRF: plages privees/reservees interdites.
_BLOCKED_NETWORKS = [
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),  # link-local / metadata
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fe80::/10"),
    ipaddress.ip_network("fc00::/7"),
]

_BLOCKED_HOSTNAMES = {"localhost", "metadata.google.internal"}


def validate_webhook_url(value):
    """Anti-SSRF : refuse les URLs pointant vers des adresses privees/reservees."""
    import socket
    from urllib.parse import urlparse

    parsed = urlparse(value)
    hostname = parsed.hostname

    if not hostname:
        raise ValidationError("URL invalide : hostname manquant.")

    if hostname in _BLOCKED_HOSTNAMES:
        raise ValidationError("Les URLs pointant vers des adresses internes sont interdites.")

    try:
        resolved = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise ValidationError(f"Impossible de resoudre le hostname : {hostname}") from exc

    for _, _, _, _, sockaddr in resolved:
        ip = ipaddress.ip_address(sockaddr[0])
        for network in _BLOCKED_NETWORKS:
            if ip in network:
                raise ValidationError("Les URLs pointant vers des adresses privees ou reservees sont interdites.")
