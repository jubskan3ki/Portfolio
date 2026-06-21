"""Signaux de l'application Contact."""

import logging
from typing import Any

from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .services.info import ADMIN_BIO_CACHE_KEY

logger = logging.getLogger("core.contact")


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="invalidate_admin_bio_cache")
def invalidate_admin_bio_cache(sender: type, **_kwargs: Any) -> None:
    """Purge le cache de la bio admin quand un User change.

    get_admin_bio() met la bio en cache 30 min sans invalidation : sans ce
    signal, une modification de la bio reste invisible jusqu'a expiration du
    TTL. on_commit pour ne purger qu'apres COMMIT (cf. invalidation cache).
    """
    del sender
    transaction.on_commit(lambda: cache.delete(ADMIN_BIO_CACHE_KEY))
