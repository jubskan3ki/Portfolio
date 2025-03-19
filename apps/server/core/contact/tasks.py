"""
Tâches Celery pour l'envoi des emails de contact.
"""

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.timezone import now


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_contact_email(self, name, email, message):
    """
    Envoie :
    1. Un mail à l'administrateur du site (moi-même)
    2. Un mail de confirmation à l'utilisateur
    """
    # Récupère l'adresse admin depuis les settings
    admin_email = settings.ADMIN_USER
    current_year = now().year

    # === Email pour l'administrateur ===
    admin_subject = f"📩 Nouveau message de contact de {name}"
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

        print(f"[TASK] ✅ Notification admin envoyée à {admin_email} pour {name} ({email})")

    except Exception as exc:
        print(f"[TASK] ❌ Échec de l'envoi admin pour {email} : {str(exc)}")
        raise self.retry(exc=exc)

    # === Email pour l'utilisateur ===
    user_subject = "✅ Merci pour votre message !"
    user_context = {
        "name": name,
        "year": current_year,
    }

    try:
        user_html = render_to_string("contact_remerciment.html", user_context)

        send_mail(
            subject=user_subject,
            message=(
                f"Bonjour {name},\n\n"
                "Merci pour votre message ! Je vous répondrai rapidement.\n\n"
                f"Bonne journée,\nL'équipe {settings.DEFAULT_FROM_EMAIL}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email, email],
            html_message=user_html,
            fail_silently=False,
        )

        print(f"[TASK] ✅ Email de remerciement envoyé à {email}")

    except Exception as exc:
        print(f"[TASK] ❌ Échec de l'envoi de l'email de remerciement à {email} : {str(exc)}")
        raise self.retry(exc=exc)
