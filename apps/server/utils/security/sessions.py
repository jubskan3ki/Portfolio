"""Gestion avancee des sessions utilisateur."""

import logging
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Any

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

logger = logging.getLogger("security")

DEFAULT_MAX_SESSIONS = 5
DEFAULT_SESSION_TIMEOUT = 24 * 60 * 60  # 24 heures
SESSION_CACHE_PREFIX = "user_session"
SESSION_LOCK_TIMEOUT = 5  # secondes
# update_activity est appele a chaque requete authentifiee. On ne reecrit la
# liste (verrou + read-modify-write) que si la derniere activite remonte a plus
# de ce seuil : le chemin critique se reduit alors a une seule lecture cache.
ACTIVITY_UPDATE_THROTTLE = 60  # secondes


class SessionManager:
    """Gestionnaire de sessions par utilisateur et appareil."""

    def __init__(self, user_id: int, max_sessions: int | None = None):
        self.user_id = user_id
        self.max_sessions = (
            max_sessions
            if max_sessions is not None
            else int(getattr(settings, "MAX_SESSIONS_PER_USER", DEFAULT_MAX_SESSIONS))
        )
        self.timeout = int(getattr(settings, "SESSION_TIMEOUT", DEFAULT_SESSION_TIMEOUT))

    @property
    def _cache_key(self) -> str:
        """Cle de cache pour les sessions de l'utilisateur."""
        return f"{SESSION_CACHE_PREFIX}:{self.user_id}"

    @contextmanager
    def _lock(self) -> Iterator[None]:
        """Serialise le read-modify-write des sessions (cache) par utilisateur.

        Sans verrou, deux requetes simultanees liraient la meme liste, la
        modifieraient et la reecriraient : la derniere ecriture ecrase l'autre
        (session perdue, ou limite max_sessions contournee). Utilise le verrou
        Redis de django-redis si disponible, sinon no-op (degradation propre).
        Ne PAS imbriquer (les helpers internes appeles sous ce verrou ne doivent
        pas le reprendre : le lock Redis n'est pas reentrant).
        """
        lock_factory = getattr(cache, "lock", None)
        if lock_factory is None:
            yield
            return
        with lock_factory(
            f"lock:{self._cache_key}",
            timeout=SESSION_LOCK_TIMEOUT,
            blocking_timeout=SESSION_LOCK_TIMEOUT,
        ):
            yield

    def get_sessions(self) -> list[dict[str, Any]]:
        """Recupere toutes les sessions actives de l'utilisateur."""
        sessions: list[dict[str, Any]] = cache.get(self._cache_key, [])
        return self._cleanup_expired(sessions)

    def add_session(self, session_id: str, device_info: dict[str, Any]) -> bool:
        """Ajoute une nouvelle session."""
        with self._lock():
            sessions = self.get_sessions()

            # Verifier si la session existe deja
            for session in sessions:
                if session.get("id") == session_id:
                    session["last_activity"] = timezone.now().isoformat()
                    cache.set(self._cache_key, sessions, self.timeout)
                    return True

            # Verifier la limite de sessions
            if len(sessions) >= self.max_sessions:
                # Supprimer la session la plus ancienne
                sessions.sort(key=lambda s: s.get("last_activity", ""))
                removed = sessions.pop(0)
                logger.info("Session removed for user %s: %s", self.user_id, removed.get("id", "unknown"))

            # Ajouter la nouvelle session
            new_session = {
                "id": session_id,
                "device": device_info,
                "created_at": timezone.now().isoformat(),
                "last_activity": timezone.now().isoformat(),
            }
            sessions.append(new_session)
            cache.set(self._cache_key, sessions, self.timeout)

            logger.info("New session added for user %s", self.user_id)
            return True

    def get_session(self, session_id: str) -> dict[str, Any] | None:
        """Recupere une session specifique par son ID."""
        sessions = self.get_sessions()
        for session in sessions:
            if session.get("id") == session_id:
                return session
        return None

    def remove_session(self, session_id: str) -> dict[str, Any] | None:
        """Supprime une session specifique et retourne ses donnees."""
        with self._lock():
            sessions = self.get_sessions()
            removed_session = None

            for session in sessions:
                if session.get("id") == session_id:
                    removed_session = session
                    break

            if removed_session:
                sessions = [s for s in sessions if s.get("id") != session_id]
                cache.set(self._cache_key, sessions, self.timeout)
                logger.info("Session %s removed for user %s", session_id, self.user_id)

            return removed_session

    def revoke_all_sessions(self, except_session_id: str | None = None) -> list[dict[str, Any]]:
        """Revoque toutes les sessions sauf celle specifiee. Retourne les sessions revoquees."""
        with self._lock():
            sessions = self.get_sessions()
            revoked_sessions = []
            remaining_sessions = []

            for session in sessions:
                if except_session_id and session.get("id") == except_session_id:
                    remaining_sessions.append(session)
                else:
                    revoked_sessions.append(session)

            cache.set(self._cache_key, remaining_sessions, self.timeout)
            logger.info("Revoked %d sessions for user %s", len(revoked_sessions), self.user_id)
            return revoked_sessions

    def update_activity(self, session_id: str) -> bool:
        """Met a jour la derniere activite d'une session.

        Chemin critique (activite recente) : une seule lecture cache, sans
        verrou ni reecriture. La reecriture serialisee sous verrou n'a lieu que
        si l'activite remonte a plus de ACTIVITY_UPDATE_THROTTLE secondes.
        """
        now = timezone.now()

        # Lecture brute (sans _cleanup_expired) pour rester sur 1 round-trip.
        sessions: list[dict[str, Any]] = cache.get(self._cache_key, [])
        for session in sessions:
            if session.get("id") == session_id:
                last = session.get("last_activity")
                if last:
                    try:
                        if (now - datetime.fromisoformat(last)).total_seconds() < ACTIVITY_UPDATE_THROTTLE:
                            return True
                    except (ValueError, TypeError):
                        pass
                break
        else:
            return False

        # Activite ancienne (ou date illisible) : MAJ serialisee sous verrou.
        with self._lock():
            sessions = self.get_sessions()
            for session in sessions:
                if session.get("id") == session_id:
                    session["last_activity"] = now.isoformat()
                    cache.set(self._cache_key, sessions, self.timeout)
                    return True
            return False

    def is_session_valid(self, session_id: str) -> bool:
        """Verifie si une session est valide."""
        sessions = self.get_sessions()
        return any(s.get("id") == session_id for s in sessions)

    def get_or_create_session(self, session_id: str, device_info: dict[str, Any]) -> bool:
        """Recupere ou cree une session en une seule operation.

        Optimisation pour eviter les appels multiples a get_sessions().
        """
        with self._lock():
            sessions = self.get_sessions()
            now_iso = timezone.now().isoformat()

            # Chercher la session existante
            for session in sessions:
                if session.get("id") == session_id:
                    session["last_activity"] = now_iso
                    cache.set(self._cache_key, sessions, self.timeout)
                    return True

            # Verifier la limite de sessions
            if len(sessions) >= self.max_sessions:
                sessions.sort(key=lambda s: s.get("last_activity", ""))
                removed = sessions.pop(0)
                logger.info("Session removed for user %s: %s", self.user_id, removed.get("id", "unknown"))

            # Ajouter la nouvelle session
            sessions.append(
                {
                    "id": session_id,
                    "device": device_info,
                    "created_at": now_iso,
                    "last_activity": now_iso,
                }
            )
            cache.set(self._cache_key, sessions, self.timeout)
            logger.info("New session added for user %s", self.user_id)
            return True

    def get_session_count(self) -> int:
        """Retourne le nombre de sessions actives."""
        return len(self.get_sessions())

    def _cleanup_expired(self, sessions: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Supprime les sessions expirees."""
        now = timezone.now()
        threshold = now - timedelta(seconds=self.timeout)

        valid_sessions = []
        for session in sessions:
            try:
                last_activity = datetime.fromisoformat(session.get("last_activity", ""))
                if last_activity > threshold:
                    valid_sessions.append(session)
            except (ValueError, TypeError):
                continue

        if len(valid_sessions) != len(sessions):
            cache.set(self._cache_key, valid_sessions, self.timeout)

        return valid_sessions


def get_session_manager(user: Any) -> SessionManager | None:
    """Factory pour creer un SessionManager."""
    if not user or not getattr(user, "is_authenticated", False):
        return None
    return SessionManager(user.id)
