"""Service d'envoi d'emails avec Django et Celery."""

from __future__ import annotations

import logging
from smtplib import SMTPException
from typing import TYPE_CHECKING

from celery import Task, shared_task

if TYPE_CHECKING:
    from celery import Celery
    from celery.result import AsyncResult
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

logger = logging.getLogger("mail")

EMAIL_EXCEPTIONS = (SMTPException, ImproperlyConfigured)


def _get_sender(from_email: str | None = None) -> str:
    """Retourne l'expediteur ou l'email par defaut."""
    return from_email or str(settings.DEFAULT_FROM_EMAIL)


def _handle_retry(task: Task, exc: Exception, recipient_email: str) -> None:
    """Gere la logique de retry pour les taches Celery."""
    retry_count = task.request.retries
    retry_delay = 60 * (2**retry_count)

    if retry_count >= task.max_retries:
        logger.critical("Echec definitif d'envoi d'email a %s", recipient_email)
        raise exc

    task.retry(exc=exc, countdown=retry_delay)


def _send_html_email_sync(
    subject: str,
    recipient_email: str,
    template_path: str,
    context: dict,
    from_email: str | None = None,
) -> bool:
    """Envoie un email HTML de maniere synchrone."""
    html_message = render_to_string(template_path, context)
    num_sent = send_mail(
        subject=subject,
        message="",
        from_email=_get_sender(from_email),
        recipient_list=[recipient_email],
        html_message=html_message,
        fail_silently=False,
    )
    if num_sent == 0:
        logger.error("Echec d'envoi d'email a %s - aucun email envoye", recipient_email)
        raise SMTPException("Aucun email n'a ete envoye")
    return True


def _send_multipart_sync(
    subject: str,
    recipient_email: str,
    text_content: str,
    html_content: str,
    from_email: str | None = None,
) -> bool:
    """Envoie un email multipart de maniere synchrone."""
    email_msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=_get_sender(from_email),
        to=[recipient_email],
    )
    email_msg.attach_alternative(html_content, "text/html")
    num_sent = email_msg.send()
    if num_sent == 0:
        logger.error("Echec d'envoi d'email multipart a %s - aucun email envoye", recipient_email)
        raise SMTPException("Aucun email n'a ete envoye")
    return True


@shared_task(bind=True, max_retries=3, name="email.send_html")
def task_send_html_email(
    self: Task,
    subject: str,
    recipient_email: str,
    template_path: str,
    context: dict,
    from_email: str | None = None,
) -> bool:
    """Tache Celery pour envoyer un email HTML."""
    try:
        _send_html_email_sync(subject, recipient_email, template_path, context, from_email)
        logger.info("Email envoye avec succes a %s", recipient_email)
    except EMAIL_EXCEPTIONS as exc:
        logger.exception("Erreur envoi email a %s", recipient_email)
        _handle_retry(self, exc, recipient_email)
        return False
    else:
        return True


@shared_task(bind=True, max_retries=3, name="email.send_multipart")
def task_send_multipart_email(
    self: Task,
    subject: str,
    recipient_email: str,
    text_content: str,
    html_content: str,
    from_email: str | None = None,
) -> bool:
    """Tache Celery pour envoyer un email multipart."""
    try:
        _send_multipart_sync(subject, recipient_email, text_content, html_content, from_email)
        logger.info("Email multipart envoye avec succes a %s", recipient_email)
    except EMAIL_EXCEPTIONS as exc:
        logger.exception("Erreur envoi email multipart a %s", recipient_email)
        _handle_retry(self, exc, recipient_email)
        return False
    else:
        return True


def _get_celery_app() -> Celery:
    """Retourne l'application Celery."""
    from config.celery import app

    return app


def send_templated_email(
    subject: str,
    recipient_email: str,
    template_path: str,
    context: dict,
    from_email: str | None = None,
    *,
    async_send: bool = True,
) -> AsyncResult[bool] | bool:
    """Envoie un email avec un template HTML, sync ou async."""
    if async_send:
        celery_app = _get_celery_app()
        return celery_app.send_task(
            "email.send_html",
            args=[subject, recipient_email, template_path, context, from_email],
        )

    try:
        _send_html_email_sync(subject, recipient_email, template_path, context, from_email)
    except EMAIL_EXCEPTIONS:
        logger.exception("Erreur envoi email a %s", recipient_email)
        return False
    else:
        return True


def send_multi_part_email(
    subject: str,
    recipient_email: str,
    text_content: str,
    html_content: str,
    from_email: str | None = None,
    *,
    async_send: bool = True,
) -> AsyncResult[bool] | bool:
    """Envoie un email multipart avec versions texte et HTML."""
    if async_send:
        celery_app = _get_celery_app()
        return celery_app.send_task(
            "email.send_multipart",
            args=[subject, recipient_email, text_content, html_content, from_email],
        )

    try:
        _send_multipart_sync(subject, recipient_email, text_content, html_content, from_email)
    except EMAIL_EXCEPTIONS:
        logger.exception("Erreur envoi email multipart a %s", recipient_email)
        return False
    else:
        return True


# Expose tasks for Celery autodiscover
__all__ = [
    "send_multi_part_email",
    "send_templated_email",
    "task_send_html_email",
    "task_send_multipart_email",
]
