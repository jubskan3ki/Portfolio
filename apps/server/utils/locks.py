"""Verrou applicatif simple base sur le cache (anti-chevauchement de taches)."""

import logging
from collections.abc import Iterator
from contextlib import contextmanager

from django.core.cache import cache

logger = logging.getLogger(__name__)


@contextmanager
def single_run_lock(lock_id: str, timeout: int) -> Iterator[bool]:
    """Verrou best-effort base sur `cache.add` (atomique cote Redis).

    Empeche deux executions concurrentes d'une meme tache periodique de se
    chevaucher (ex: un run Beat qui depasse son intervalle de planification).

    Args:
        lock_id: Identifiant logique du verrou (une tache = un id).
        timeout: TTL du verrou en secondes. Borne la duree de detention pour
            qu'un crash (sans liberation) ne bloque pas les runs suivants.

    Yields:
        True si le verrou est acquis (executer le travail), False si une autre
        instance le detient deja (sauter ce run).
    """
    key = f"task_lock:{lock_id}"
    # cache.add ne pose la cle que si elle n'existe pas encore -> acquisition atomique.
    acquired = cache.add(key, "1", timeout)
    try:
        yield acquired
    finally:
        if acquired:
            cache.delete(key)
