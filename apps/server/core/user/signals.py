"""
Ce fichier permet de créer un superadmin lors de la migration de la base de données.
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_admin(sender, **kwargs):  # pylint: disable=unused-argument
    """
    Crée un superadmin si aucun superadmin n'existe.
    """
    super_user = get_user_model()

    admin_email = getattr(settings, "ADMIN_EMAIL", None)
    admin_password = getattr(settings, "ADMIN_PASSWORD", None)

    if not admin_email or not admin_password:
        print("⚠️  ADMIN_EMAIL ou ADMIN_PASSWORD manquant dans les variables d'environnement.")
        return

    if not super_user.objects.filter(email=admin_email, is_superuser=True).exists():
        super_user.objects.create_superuser(email=admin_email, password=admin_password)
        print(f"✅ Superadmin {admin_email} créé")
    else:
        print(f"ℹ️ Superadmin {admin_email} existe déjà")
