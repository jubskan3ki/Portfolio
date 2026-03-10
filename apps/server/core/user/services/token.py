"""Service pour la gestion des tokens JWT."""

import logging

from django.db import DatabaseError, IntegrityError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

logger = logging.getLogger(__name__)


class TokenBlacklistService:
    """Service pour blacklister les tokens JWT."""

    @classmethod
    def blacklist_by_jti(cls, jti: str) -> bool:
        """Blacklist un refresh token via son JTI.

        Args:
            jti: JSON Token Identifier du token a blacklister.

        Returns:
            True si le token a ete blackliste, False sinon.
        """
        if not jti:
            logger.warning("Tentative de blacklist avec un JTI vide")
            return False

        try:
            outstanding_token = OutstandingToken.objects.get(jti=jti)
            BlacklistedToken.objects.get_or_create(token=outstanding_token)
            logger.info("Token blackliste avec JTI: %s", jti)
            return True
        except OutstandingToken.DoesNotExist:
            logger.warning("Outstanding token non trouve pour JTI: %s", jti)
            return False
        except (IntegrityError, DatabaseError):
            logger.exception("Erreur DB lors du blacklist du token")
            return False

    @classmethod
    def blacklist_session_token(cls, session: dict) -> bool:
        """Blacklist le refresh token associe a une session.

        Args:
            session: Dictionnaire de session contenant device.refresh_jti.

        Returns:
            True si le token a ete blackliste, False sinon.
        """
        refresh_jti = session.get("device", {}).get("refresh_jti")
        if not refresh_jti:
            logger.warning("Pas de refresh_jti dans la session: %s", session.get("id"))
            return False

        return cls.blacklist_by_jti(refresh_jti)
