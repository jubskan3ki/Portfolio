"""Service pour gerer les soumissions de contact."""

import uuid
from typing import Any

from django.db import DatabaseError, IntegrityError, transaction
from django.db.models import QuerySet

from utils.exceptions.service import ServiceError
from utils.services import BaseService

from ..models import Contact
from ..tasks import send_admin_notification, send_user_confirmation


class ContactService(BaseService["Contact"]):
    """Service pour les operations sur les contacts."""

    model = Contact
    entity_name = "Contact"
    logger_name = "core.contact"

    @classmethod
    def get_all(cls) -> QuerySet[Contact]:
        """Recupere toutes les soumissions de contact."""
        return Contact.objects.only(
            "id", "name", "email", "subject", "status", "reference_id", "created_at", "updated_at"
        ).order_by("-created_at")

    # Filtre les champs non-modele (ex: recaptchaToken) avant create().
    _MODEL_FIELDS = {"name", "email", "subject", "message", "phone", "company"}

    @classmethod
    def submit_form(
        cls,
        data: dict[str, Any],
        ip_address: str | None = None,
    ) -> str:
        """Traite la soumission d'un formulaire de contact.

        Returns:
            reference_id de la soumission creee.

        Raises:
            ServiceError: Si une erreur survient lors du traitement.
        """
        reference_id = str(uuid.uuid4())[:8].upper()
        name = data["name"]
        email = data["email"]
        message = data["message"]

        model_data = {k: v for k, v in data.items() if k in cls._MODEL_FIELDS}

        try:
            with transaction.atomic():
                Contact.objects.create(
                    reference_id=reference_id,
                    ip_address=ip_address,
                    **model_data,
                )
                # on_commit: n'envoie les emails qu'apres COMMIT DB (evite les emails "fantomes").
                transaction.on_commit(lambda: send_admin_notification.delay(name, email, message))
                transaction.on_commit(lambda: send_user_confirmation.delay(name, email))
        except (IntegrityError, DatabaseError) as exc:
            cls._get_logger().exception("Erreur lors de la creation du contact")
            raise ServiceError(
                "Erreur lors du traitement de votre message.",
                details={"error": str(exc)},
            ) from exc

        return reference_id
