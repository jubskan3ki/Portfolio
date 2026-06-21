"""Mode "import en masse" : suppression temporaire des signaux par-objet.

Pendant un import volumineux, chaque `.save()` declenche audit + versioning +
webhooks + invalidation cache. Ce surcout, proportionnel au nombre de lignes,
est evite en activant ce mode autour de la boucle d'import ; l'invalidation
cache est ensuite refaite une seule fois, de maniere groupee.

Le drapeau est stocke en thread-local : les signaux s'executent dans le meme
thread que le `.save()` qui les declenche.
"""

import threading
from collections.abc import Iterator
from contextlib import contextmanager

_state = threading.local()


def bulk_mode_active() -> bool:
    """Indique si le thread courant est dans un import en masse."""
    return getattr(_state, "active", False)


@contextmanager
def bulk_import_mode() -> Iterator[None]:
    """Active le mode import en masse pour le thread courant.

    Reentrant : restaure l'etat precedent en sortie (utile si imbrique).
    """
    previous = getattr(_state, "active", False)
    _state.active = True
    try:
        yield
    finally:
        _state.active = previous
