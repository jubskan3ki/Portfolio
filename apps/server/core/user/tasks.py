"""
Tâches Celery pour envoyer des emails après une demande de réinitialisation.
"""

import random

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from celery import shared_task

from .models import ResetPasswordCode


@shared_task
def send_reset_password_email(email):
    """
    Génère un code de réinitialisation et l'envoie par email.
    """
    reset_code = "".join(random.choices("0123456789", k=6))
    ResetPasswordCode.objects.update_or_create(email=email, defaults={"code": reset_code})

    subject = "🔒 Code de réinitialisation de votre mot de passe"
    context = {"name": email.split("@")[0], "reset_code": reset_code}

    html_message = render_to_string("reset_password.html", context)

    send_mail(
        subject=subject,
        message="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        html_message=html_message,
        fail_silently=False,
    )
