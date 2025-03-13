"""
Tâches Celery pour envoyer des emails après réception d'un message de contact.
"""

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from celery import shared_task


@shared_task
def send_contact_email(name, email, message):
    """
    Envoie un email de notification après réception d’un message de contact.
    """
    subject = f"📩 Nouveau message de contact de {name}"
    context = {"name": name, "email": email, "message": message}

    html_message = render_to_string("contact_notification.html", context)

    send_mail(
        subject=subject,
        message="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=email,
        html_message=html_message,
        fail_silently=False,
    )
