"""Service de gestion des mots de passe."""

import hmac
import logging
import random
import secrets
import time
from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError
from django.db import DatabaseError, IntegrityError
from django.utils.timezone import now

from config.constants import MIN_RESPONSE_TIME, RESET_CODE_CHARS, RESET_CODE_LENGTH

from ..models import ResetPasswordCode
from ..tasks import (
    send_password_changed_email_async,
    send_reset_password_email_async,
    send_reset_password_email_sync,
)

logger = logging.getLogger("core.user")
User = get_user_model()


class PasswordService:
    """Service pour la gestion des mots de passe."""

    @staticmethod
    def generate_reset_code() -> str:
        """Genere un code de reinitialisation aleatoire."""
        return "".join(secrets.choice(RESET_CODE_CHARS) for _ in range(RESET_CODE_LENGTH))

    @staticmethod
    def _ensure_min_response_time(start_time: float) -> None:
        """Assure un temps de reponse minimum avec jitter pour eviter les timing attacks."""
        elapsed = time.time() - start_time
        jitter = random.uniform(0, 0.5)  # noqa: S311
        target = MIN_RESPONSE_TIME + jitter
        if elapsed < target:
            time.sleep(target - elapsed)

    @staticmethod
    def request_password_reset(email: str) -> bool:
        """Traite une demande de reinitialisation de mot de passe."""
        start_time = time.time()
        try:
            user = User.objects.filter(email=email, is_active=True).first()
            if not user:
                logger.info("Demande reinitialisation traitee pour: %s", email)
                PasswordService._ensure_min_response_time(start_time)
                return True

            reset_code = PasswordService.generate_reset_code()

            ResetPasswordCode.objects.update_or_create(
                email=email,
                defaults={"code": reset_code, "created_at": now(), "attempts": 0},
            )

            context = {
                "reset_code": reset_code,
                "user_email": email,
                "user_name": user.get_full_name() or user.first_name or email.split("@", maxsplit=1)[0].capitalize(),
                "user_first_name": user.first_name or email.split("@", maxsplit=1)[0].capitalize(),
            }

            PasswordService._send_reset_email(email, context)
            logger.info("Demande reinitialisation initiee pour %s", email)
            PasswordService._ensure_min_response_time(start_time)
            return True

        except (DatabaseError, IntegrityError):
            logger.exception("Erreur DB pour %s", email)
        except (ValueError, TypeError):
            logger.exception("Erreur validation pour %s", email)
        except OSError:
            logger.exception("Erreur IO pour %s", email)
        except (ImportError, AttributeError):
            logger.exception("Erreur import pour %s", email)

        PasswordService._ensure_min_response_time(start_time)
        return True

    @staticmethod
    def _send_reset_email(email: str, context: dict[str, Any]) -> None:
        """Envoie l'email de reinitialisation avec fallback synchrone."""
        try:
            send_reset_password_email_async(email, context)
            logger.info("Tache Celery creee pour %s", email)
        except (ConnectionError, ImportError, AttributeError, RuntimeError):
            logger.exception("Erreur Celery pour %s", email)
            try:
                send_reset_password_email_sync(email, context)
                logger.info("Email envoye directement a %s", email)
            except (ValueError, TypeError, OSError):
                logger.exception("Echec envoi direct pour %s", email)

    @staticmethod
    def validate_new_password(password: str, user: Any | None = None) -> None:
        """Valide le nouveau mot de passe selon les regles Django."""
        try:
            validate_password(password, user=user)
        except ValidationError as e:
            raise PermissionDenied("Mot de passe invalide: " + " ".join(e.messages)) from e

    @staticmethod
    def reset_password(email: str, reset_code: str, new_password: str) -> bool:
        """Reinitialise le mot de passe avec le code fourni."""
        start_time = time.time()

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist as e:
            logger.warning("Reinitialisation email inexistant: %s", email)
            PasswordService._ensure_min_response_time(start_time)
            raise ObjectDoesNotExist("Aucun utilisateur trouve avec cet email.") from e

        try:
            reset_record = ResetPasswordCode.objects.filter(email=email).first()

            if not reset_record:
                logger.warning("Aucun code trouve pour %s", email)
                PasswordService._ensure_min_response_time(start_time)
                raise PermissionDenied("Aucune demande de reinitialisation ou delai expire.")

            if reset_record.is_expired():
                logger.warning("Code expire pour %s", email)
                reset_record.delete()
                PasswordService._ensure_min_response_time(start_time)
                raise PermissionDenied("Code expire. Veuillez faire une nouvelle demande.")

            if reset_record.is_locked():
                logger.warning("Code bloque pour %s apres trop de tentatives", email)
                reset_record.delete()
                PasswordService._ensure_min_response_time(start_time)
                raise PermissionDenied("Trop de tentatives. Veuillez faire une nouvelle demande.")

            # Comparaison securisee contre timing attack
            if not hmac.compare_digest(reset_record.code, reset_code):
                logger.warning("Code incorrect pour %s (tentative %d)", email, reset_record.attempts + 1)
                reset_record.increment_attempts()
                PasswordService._ensure_min_response_time(start_time)
                raise PermissionDenied("Code de reinitialisation incorrect.")

            # Validation du mot de passe
            PasswordService.validate_new_password(new_password, user)

            user.set_password(new_password)
            user.save()
            reset_record.delete()

            PasswordService._send_password_changed_notification(
                email,
                user.get_full_name() or user.first_name,
            )

            logger.info("Mot de passe reinitialise pour %s", email)
            PasswordService._ensure_min_response_time(start_time)
            return True

        except (DatabaseError, IntegrityError) as e:
            logger.exception("Erreur DB reinitialisation pour %s", email)
            PasswordService._ensure_min_response_time(start_time)
            raise PermissionDenied("Erreur lors de la reinitialisation.") from e
        except ValidationError as e:
            logger.exception("Erreur validation reinitialisation pour %s", email)
            PasswordService._ensure_min_response_time(start_time)
            raise PermissionDenied("Donnees invalides pour la reinitialisation.") from e

    @staticmethod
    def _send_password_changed_notification(
        email: str,
        user_name: str,
    ) -> None:
        """Envoie l'email de confirmation de changement de mot de passe."""
        context = {"user_name": user_name}
        try:
            send_password_changed_email_async(email, context)
            logger.info("Notification password_changed envoyee pour %s", email)
        except (ConnectionError, ImportError, AttributeError, RuntimeError):
            logger.exception(
                "Erreur envoi notification password_changed pour %s",
                email,
            )

    @staticmethod
    def change_password(user: Any, old_password: str, new_password: str) -> bool:
        """Change le mot de passe d'un utilisateur connecte."""
        if not user.check_password(old_password):
            raise PermissionDenied("Mot de passe actuel incorrect.")

        if old_password == new_password:
            raise PermissionDenied("Le nouveau mot de passe doit etre different.")

        PasswordService.validate_new_password(new_password, user)

        user.set_password(new_password)
        user.save(update_fields=["password"])

        PasswordService._send_password_changed_notification(
            user.email,
            user.get_full_name() or user.first_name,
        )

        logger.info("Mot de passe change pour %s", user.email)
        return True
