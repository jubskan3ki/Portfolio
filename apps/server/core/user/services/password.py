"""Service de gestion des mots de passe."""

import hmac
import logging
import secrets
import time
from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError
from django.db import DatabaseError, IntegrityError, transaction
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
    @staticmethod
    def generate_reset_code() -> str:
        return "".join(secrets.choice(RESET_CODE_CHARS) for _ in range(RESET_CODE_LENGTH))

    @staticmethod
    def _ensure_min_response_time(start_time: float) -> None:
        """Assure un temps de reponse minimum avec jitter pour eviter les timing attacks."""
        elapsed = time.time() - start_time
        jitter = secrets.randbelow(500) / 1000.0
        target = MIN_RESPONSE_TIME + jitter
        if elapsed < target:
            time.sleep(target - elapsed)

    @staticmethod
    def request_password_reset(email: str) -> bool:
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
    def _revoke_sessions(user_id: int, *, except_session_id: str | None = None) -> None:
        """Revoque sessions et refresh tokens (un token vole avant le changement perd l'acces) ; fail-open car le mdp est deja change."""
        from utils.security.sessions import SessionManager

        from .token import TokenBlacklistService

        try:
            revoked = SessionManager(user_id).revoke_all_sessions(except_session_id=except_session_id)
            blacklisted = sum(1 for s in revoked if TokenBlacklistService.blacklist_session_token(s))
            logger.info(
                "Password change: %d session(s) revoquee(s), %d token(s) blackliste(s) pour user %s",
                len(revoked),
                blacklisted,
                user_id,
            )
        except Exception:
            logger.exception("Echec revocation des sessions apres changement mdp pour user %s", user_id)

    @staticmethod
    def validate_new_password(password: str, user: Any | None = None) -> None:
        try:
            validate_password(password, user=user)
        except ValidationError as e:
            raise PermissionDenied("Mot de passe invalide: " + " ".join(e.messages)) from e

    @staticmethod
    def reset_password(email: str, reset_code: str, new_password: str) -> bool:
        start_time = time.time()

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist as e:
            logger.warning("Reinitialisation email inexistant: %s", email)
            PasswordService._ensure_min_response_time(start_time)
            raise ObjectDoesNotExist("Aucun utilisateur trouve avec cet email.") from e

        try:
            # select_for_update + atomic : serialise les tentatives concurrentes (sinon TOCTOU sur attempts contourne le verrou anti-brute-force).
            # On ne leve pas dans le bloc atomic (annulerait l'increment) : on memorise le rejet et on leve apres COMMIT.
            rejection: str | None = None
            with transaction.atomic():
                reset_record = ResetPasswordCode.objects.select_for_update().filter(email=email).first()

                if not reset_record:
                    logger.warning("Aucun code trouve pour %s", email)
                    rejection = "Aucune demande de reinitialisation ou delai expire."
                elif reset_record.is_expired():
                    logger.warning("Code expire pour %s", email)
                    reset_record.delete()
                    rejection = "Code expire. Veuillez faire une nouvelle demande."
                elif reset_record.is_locked():
                    logger.warning("Code bloque pour %s apres trop de tentatives", email)
                    reset_record.delete()
                    rejection = "Trop de tentatives. Veuillez faire une nouvelle demande."
                elif not hmac.compare_digest(reset_record.code, reset_code):
                    logger.warning("Code incorrect pour %s (tentative %d)", email, reset_record.attempts + 1)
                    reset_record.increment_attempts()
                    rejection = "Code de reinitialisation incorrect."
                else:
                    # Si validate_new_password leve, le rollback est sans effet (aucune mutation prealable) et le code reste valide pour reessayer.
                    PasswordService.validate_new_password(new_password, user)
                    user.set_password(new_password)
                    user.save()
                    reset_record.delete()

            if rejection is not None:
                PasswordService._ensure_min_response_time(start_time)
                raise PermissionDenied(rejection)

            # Flux "mot de passe oublie" (non authentifie) : revoquer TOUTES les sessions/tokens, un attaquant peut en detenir.
            PasswordService._revoke_sessions(user.id)

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
    def change_password(
        user: Any,
        old_password: str,
        new_password: str,
        *,
        except_session_id: str | None = None,
    ) -> bool:
        """Change le mdp d'un utilisateur connecte ; except_session_id = session courante conservee, les autres sont revoquees."""
        if not user.check_password(old_password):
            raise PermissionDenied("Mot de passe actuel incorrect.")

        if old_password == new_password:
            raise PermissionDenied("Le nouveau mot de passe doit etre different.")

        PasswordService.validate_new_password(new_password, user)

        user.set_password(new_password)
        user.save(update_fields=["password"])

        # Un appareil ou token compromis ne doit pas survivre au changement de mot de passe.
        PasswordService._revoke_sessions(user.id, except_session_id=except_session_id)

        PasswordService._send_password_changed_notification(
            user.email,
            user.get_full_name() or user.first_name,
        )

        logger.info("Mot de passe change pour %s", user.email)
        return True
