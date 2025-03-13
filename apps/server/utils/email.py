"""
Service d'envoi d'e-mails avec Django et Celery, sans MJML.
"""

from smtplib import SMTPException

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.template.loader import render_to_string

from celery import shared_task


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


def send_reset_password_email(email, reset_code):
    """
    Envoie un email avec le code de réinitialisation du mot de passe.
    """
    subject = "🔒 Code de réinitialisation de votre mot de passe"
    template_path = "emails/reset_password.html"
    context = {"name": email.split("@")[0], "reset_code": reset_code}
    send_email.delay(subject, email, template_path, context)


def send_contact_notification_email(admin_email, name, sender_email, message):
    """
    Envoie une notification à l'admin après réception d'un message de contact.
    """
    subject = "📩 Nouveau message de contact"
    template_path = "emails/contact_notification.html"
    context = {
        "name": name,
        "email": sender_email,
        "message": message,
    }
    send_email.delay(subject, admin_email, template_path, context)
