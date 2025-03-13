from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_admin(sender, **kwargs):
    User = get_user_model()
    admin_email = settings.ADMIN_USER
    if not User.objects.filter(email=admin_email, is_superuser=True).exists():
        print(f"✅ Création du superuser {admin_email} automatique...")
        User.objects.create_superuser(email=admin_email, password=settings.ADMIN_PASSWORD)
    else:
        print(f"⚠️ Superuser {admin_email} déjà existant, aucune création effectuée.")
