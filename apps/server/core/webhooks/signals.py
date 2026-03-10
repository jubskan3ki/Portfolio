"""Signaux pour declencher les webhooks automatiquement."""

import logging

from .models import WebhookEventType
from .services import WebhookDispatcher

logger = logging.getLogger(__name__)

# Mapping des modeles vers les types d'evenements
MODEL_EVENT_MAPPING = {
    "articles.Article": {
        "created": WebhookEventType.ARTICLE_CREATED,
        "updated": WebhookEventType.ARTICLE_UPDATED,
        "deleted": WebhookEventType.ARTICLE_DELETED,
    },
    "projects.Project": {
        "created": WebhookEventType.PROJECT_CREATED,
        "updated": WebhookEventType.PROJECT_UPDATED,
        "deleted": WebhookEventType.PROJECT_DELETED,
    },
    "experiences.Experience": {
        "created": WebhookEventType.EXPERIENCE_CREATED,
        "updated": WebhookEventType.EXPERIENCE_UPDATED,
        "deleted": WebhookEventType.EXPERIENCE_DELETED,
    },
    "stacks.Stack": {
        "created": WebhookEventType.STACK_CREATED,
        "updated": WebhookEventType.STACK_UPDATED,
    },
    "contact.Contact": {
        "created": WebhookEventType.CONTACT_RECEIVED,
    },
}


def get_model_label(sender) -> str:
    """Retourne le label du modele (app.Model) a partir de la classe sender."""
    return f"{sender._meta.app_label}.{sender._meta.object_name}"


def get_payload(instance) -> dict:
    """Construit le payload pour un webhook."""
    payload = {
        "id": instance.pk,
        "model": get_model_label(type(instance)),
    }

    # Ajoute les champs communs s'ils existent
    if hasattr(instance, "title"):
        payload["title"] = instance.title
    if hasattr(instance, "name"):
        payload["name"] = instance.name
    if hasattr(instance, "slug"):
        payload["slug"] = instance.slug
    if hasattr(instance, "created_at"):
        payload["created_at"] = str(instance.created_at)
    if hasattr(instance, "updated_at"):
        payload["updated_at"] = str(instance.updated_at)

    return payload


def dispatch_save_webhook(sender, instance, created, **_kwargs):
    """Dispatch un webhook lors de la creation/mise a jour d'un modele."""
    model_label = get_model_label(sender)

    events = MODEL_EVENT_MAPPING[model_label]
    action = "created" if created else "updated"

    if action not in events:
        return

    event_type = events[action]
    payload = get_payload(instance)

    try:
        WebhookDispatcher.dispatch_async(str(event_type), payload)
    except Exception:
        logger.exception("Failed to dispatch webhook for %s", model_label)


def dispatch_delete_webhook(sender, instance, **_kwargs):
    """Dispatch un webhook lors de la suppression d'un modele."""
    model_label = get_model_label(sender)

    events = MODEL_EVENT_MAPPING[model_label]

    if "deleted" not in events:
        return

    event_type = events["deleted"]
    payload = get_payload(instance)

    try:
        WebhookDispatcher.dispatch_async(str(event_type), payload)
    except Exception:
        logger.exception("Failed to dispatch delete webhook for %s", model_label)
