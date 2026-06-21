"""Configuration de l'app webhooks."""

from django.apps import AppConfig


class WebhooksConfig(AppConfig):
    """Configuration de l'application webhooks."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core.webhooks"
    verbose_name = "Webhooks"

    def ready(self) -> None:
        """Connecte les signaux aux modeles concernes."""
        from django.db.models.signals import post_delete, post_save

        from core.articles.models import Article
        from core.contact.models import Contact
        from core.experiences.models import Experience
        from core.projects.models import Project
        from core.stacks.models import Stack

        from .signals import dispatch_delete_webhook, dispatch_save_webhook

        save_models = [Article, Project, Experience, Stack, Contact]
        delete_models = [Article, Project, Experience]

        # dispatch_uid evite les doubles connexions (reload, ready() ré-appelé)
        # qui provoqueraient un double dispatch de chaque event.
        for model in save_models:
            post_save.connect(
                dispatch_save_webhook,
                sender=model,
                dispatch_uid=f"webhook_save_{model.__name__}",
            )

        for model in delete_models:
            post_delete.connect(
                dispatch_delete_webhook,
                sender=model,
                dispatch_uid=f"webhook_delete_{model.__name__}",
            )
