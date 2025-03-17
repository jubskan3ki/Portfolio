"""
Service d'envoi d'e-mails avec Django et Celery, sans MJML.
"""

from smtplib import SMTPException

from celery import shared_task
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.template.loader import render_to_string


@shared_task
def send_email(subject, recipient_email, template_path, context):
    """
    Envoie un email avec un template HTML chargé via Django.
    Utilisation de Celery pour un traitement asynchrone.
    """
    try:
        html_message = render_to_string(template_path, context)

        send_mail(
            subject=subject,
            message="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=html_message,
            fail_silently=False,
        )
    except (SMTPException, ImproperlyConfigured) as e:
        raise RuntimeError(f"Erreur critique lors de l'envoi de l'email : {str(e)}") from e
