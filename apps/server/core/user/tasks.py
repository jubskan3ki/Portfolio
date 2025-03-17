"""
Tâches Celery pour envoyer des emails après une demande de réinitialisation de mot de passe.
"""

import secrets

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import ResetPasswordCode


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_reset_password_email(self, email):
    """
    Génère un code de réinitialisation et l'envoie par email à l'utilisateur.
    """
    code = "".join(secrets.choice("0123456789") for _ in range(6))

    ResetPasswordCode.objects.update_or_create(email=email, defaults={"code": code})

    subject = "🔐 Réinitialisation de votre mot de passe"
    context = {"name": email.split("@")[0].capitalize(), "reset_code": code, "year": "2025"}

    try:
        html_message = render_to_string("reset_password.html", context)

        send_mail(
            subject=subject,
            message="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )

        print(f"[TASK] ✅ Code de réinitialisation envoyé à {email}")

    except Exception as exc:
        print(f"[TASK] ❌ Échec de l'envoi à {email} : {str(exc)}")
        raise self.retry(exc=exc)
