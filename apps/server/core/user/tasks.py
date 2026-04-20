"""Taches Celery pour l'envoi d'emails."""

import logging
from typing import Any

from celery import shared_task
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.template import TemplateDoesNotExist, TemplateSyntaxError
from django.template.loader import render_to_string
from django.utils import timezone

from config.constants import RESET_CODE_LENGTH

logger = logging.getLogger("core.user")


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    name="user.send_reset_password_email",
)
def _send_reset_password_email_task(self: Any, email: str, context: dict[str, Any]) -> bool:
    """Envoie un email de reinitialisation (tache Celery interne)."""
    try:
        return send_reset_password_email_sync(email, context)
    except (ConnectionError, OSError) as exc:
        logger.exception("Erreur transitoire Celery pour %s — retry", email)
        raise self.retry(exc=exc) from exc
    except (ValidationError, ValueError, TypeError):
        logger.exception("Erreur permanente Celery pour %s", email)
        raise


# Alias type Any pour que Pylance voie .delay() (expose par @shared_task).
_celery_task: Any = _send_reset_password_email_task


def send_reset_password_email_async(email: str, context: dict[str, Any]) -> None:
    """Lance l'envoi d'email de reinitialisation en arriere-plan via Celery.

    Args:
        email: Adresse email du destinataire.
        context: Contexte pour le template (reset_code, user_name, etc.).
    """
    _celery_task.delay(email, context)


def send_reset_password_email_sync(email: str, context: dict[str, Any]) -> bool:
    """Version synchrone de l'envoi d'email (fallback)."""
    reset_code = context.get("reset_code")
    user_name = context.get("user_name") or email.split("@", maxsplit=1)[0].capitalize()

    if not reset_code:
        logger.error("Code manquant pour %s", email)
        raise ValueError("Code de reinitialisation manquant")

    if len(reset_code) != RESET_CODE_LENGTH or not reset_code.isalnum():
        logger.error("Format code invalide pour %s: %s", email, reset_code)
        raise ValueError(f"Format de code invalide: {reset_code}")

    email_context = {
        "name": user_name,
        "reset_code": reset_code,
        "year": timezone.now().year,
    }

    try:
        html_message = render_to_string("reset_password.html", email_context)
    except (TemplateDoesNotExist, TemplateSyntaxError, ValueError) as e:
        logger.exception("Erreur template pour %s", email)
        raise ValidationError(f"Erreur de template: {e}") from e

    plain_text = (
        f"Bonjour {user_name},\n\n"
        f"Votre code de reinitialisation : {reset_code}\n"
        "Ce code est valable 10 minutes.\n\n"
        "Si vous n'etes pas a l'origine de cette demande, ignorez cet email.\n\n"
        f"© {email_context['year']} Juba Aitadda"
    )

    logger.info("Envoi email reinitialisation pour %s", email)

    result = send_mail(
        subject="Reinitialisation de votre mot de passe",
        message=plain_text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        html_message=html_message,
        fail_silently=False,
    )

    if result == 1:
        logger.info("Email reinitialisation envoye a %s", email)
        return True

    logger.warning("send_mail a retourne %s pour %s", result, email)
    raise OSError(f"Echec envoi email, send_mail a retourne: {result}")


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    name="user.send_password_changed_email",
)
def _send_password_changed_email_task(self: Any, email: str, context: dict[str, Any]) -> bool:
    """Envoie un email de confirmation de changement de mot de passe (tache Celery)."""
    try:
        return send_password_changed_email_sync(email, context)
    except (ConnectionError, OSError) as exc:
        logger.exception("Erreur transitoire Celery password_changed pour %s — retry", email)
        raise self.retry(exc=exc) from exc
    except (ValidationError, ValueError, TypeError):
        logger.exception("Erreur permanente Celery password_changed pour %s", email)
        raise


_password_changed_task: Any = _send_password_changed_email_task


def send_password_changed_email_async(email: str, context: dict[str, Any]) -> None:
    """Lance l'envoi de l'email de confirmation de changement de mot de passe via Celery."""
    _password_changed_task.delay(email, context)


def send_password_changed_email_sync(email: str, context: dict[str, Any]) -> bool:
    """Version synchrone de l'envoi d'email de changement de mot de passe."""
    user_name = context.get("user_name") or email.split("@", maxsplit=1)[0].capitalize()
    now = timezone.now()

    email_context = {
        "name": user_name,
        "email": email,
        "date": now.strftime("%d/%m/%Y à %H:%M"),
        "year": now.year,
    }

    try:
        html_message = render_to_string("password_changed.html", email_context)
    except (TemplateDoesNotExist, TemplateSyntaxError, ValueError) as e:
        logger.exception("Erreur template password_changed pour %s", email)
        raise ValidationError(f"Erreur de template: {e}") from e

    plain_text = (
        f"Bonjour {user_name},\n\n"
        "Votre mot de passe a ete modifie avec succes.\n"
        f"Date : {email_context['date']}\n\n"
        "Si vous n'etes pas a l'origine de ce changement, contactez-nous immediatement\n"
        "a contact@aitaddajuba.fr\n\n"
        f"© {email_context['year']} Juba Aitadda"
    )

    logger.info("Envoi email password_changed pour %s", email)

    result = send_mail(
        subject="Votre mot de passe a ete modifie",
        message=plain_text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        html_message=html_message,
        fail_silently=False,
    )

    if result == 1:
        logger.info("Email password_changed envoye a %s", email)
        return True

    logger.warning("send_mail password_changed a retourne %s pour %s", result, email)
    raise OSError(f"Echec envoi email password_changed, send_mail a retourne: {result}")
