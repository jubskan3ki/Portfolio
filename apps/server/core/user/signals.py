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
    admin_email = settings.ADMIN_USER
    admin_password = settings.ADMIN_PASSWORD

    if not super_user.objects.filter(email=admin_email, is_superuser=True).exists():
        print(f"✅ Superadmin {admin_email} créé")
        super_user.objects.create_superuser(email=admin_email, password=admin_password)
    else:
        print(f"ℹ️ Superadmin {admin_email} existe déjà")
