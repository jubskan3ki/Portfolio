"""Tâches Celery pour l'envoi des emails de contact."""

import logging
from smtplib import SMTPException

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.timezone import now

logger = logging.getLogger("core.contact")


@shared_task(bind=True, max_retries=3, name="contact.send_admin_notification")
def send_admin_notification(
    self,
    name: str,
    email: str,
    message: str,
) -> bool:
    """Envoie la notification de contact a l'administrateur.

    Args:
        name: Nom de l'expediteur
        email: Email de l'expediteur
        message: Contenu du message

    Returns:
        True si l'email a ete envoye avec succes

    Raises:
        Retry: En cas d'echec d'envoi (3 tentatives max)
    """
    admin_email = settings.ADMIN_EMAIL
    current_year = now().year

    admin_subject = f"Nouveau message de contact de {name}"
    admin_context = {
        "name": name,
        "email": email,
        "message": message,
        "year": current_year,
    }

    try:
        admin_html = render_to_string("contact_notification.html", admin_context)

        send_mail(
            subject=admin_subject,
            message=f"Nouveau message de contact de {name} ({email})\n\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email],
            html_message=admin_html,
            fail_silently=False,
        )

        logger.info("[CONTACT] Admin notification sent to %s for sender %s", admin_email, email)

    except (SMTPException, ConnectionError, TimeoutError, OSError) as exc:
        logger.exception("[CONTACT] Failed to send admin notification for %s", email)
        raise self.retry(exc=exc, countdown=60 * (2**self.request.retries)) from exc

    return True


@shared_task(bind=True, max_retries=3, name="contact.send_user_confirmation")
def send_user_confirmation(
    self,
    name: str,
    email: str,
) -> bool:
    """Envoie l'email de confirmation a l'utilisateur.

    Args:
        name: Nom de l'expediteur
        email: Email de l'expediteur

    Returns:
        True si l'email a ete envoye avec succes

    Raises:
        Retry: En cas d'echec d'envoi (3 tentatives max)
    """
    current_year = now().year

    user_context = {
        "name": name,
        "year": current_year,
    }

    try:
        user_html = render_to_string("contact_remerciment.html", user_context)
        user_text = (
            f"Bonjour {name},\n\n"
            "Merci pour votre message ! Je vous repondrai rapidement.\n\n"
            f"Bonne journee,\nL'equipe {settings.DEFAULT_FROM_EMAIL}"
        )

        send_mail(
            subject="Merci pour votre message !",
            message=user_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=user_html,
            fail_silently=False,
        )

        logger.info("[CONTACT] Confirmation email sent to %s", email)

    except (SMTPException, ConnectionError, TimeoutError, OSError) as exc:
        logger.exception("[CONTACT] Failed to send confirmation email to %s", email)
        raise self.retry(exc=exc, countdown=60 * (2**self.request.retries)) from exc

    return True
