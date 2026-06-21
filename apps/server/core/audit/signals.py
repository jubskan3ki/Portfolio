"""Signal handlers for automatic audit logging."""

import logging
import threading
from typing import Any, TypedDict

from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Manager, Model
from django.db.models.signals import post_delete, post_save, pre_save

from core.audit.models import AuditLog

logger = logging.getLogger("core.audit")


class AuditContext(TypedDict):
    """Typed dictionary for audit context."""

    user: AbstractBaseUser | None
    ip_address: str | None
    user_agent: str
    correlation_id: str


_thread_locals = threading.local()

AUDITED_MODELS = {
    "Article",
    "Project",
    "Stack",
    "Experience",
    "Contact",
    "ContactInfo",
    "FAQ",
    "StackResource",
    "Category",
    "Tag",
    "ProjectCategory",
    "ProjectStatus",
    "StackCategory",
    "ExperienceType",
}

IGNORED_FIELDS = {
    "updated_at",
    "modified_at",
    "last_modified",
    "view_count",
}


def set_audit_context(
    user: AbstractBaseUser | None = None,
    ip_address: str | None = None,
    user_agent: str = "",
    correlation_id: str = "",
) -> None:
    """
    Set audit context for the current thread.

    Call this from middleware or views to provide context for audit logs.
    """
    _thread_locals.user = user
    _thread_locals.ip_address = ip_address
    _thread_locals.user_agent = user_agent
    _thread_locals.correlation_id = correlation_id


def clear_audit_context() -> None:
    """Clear audit context for the current thread."""
    _thread_locals.user = None
    _thread_locals.ip_address = None
    _thread_locals.user_agent = ""
    _thread_locals.correlation_id = ""


def get_audit_context() -> AuditContext:
    """Get current audit context."""
    return AuditContext(
        user=getattr(_thread_locals, "user", None),
        ip_address=getattr(_thread_locals, "ip_address", None),
        user_agent=getattr(_thread_locals, "user_agent", ""),
        correlation_id=getattr(_thread_locals, "correlation_id", ""),
    )


def _should_audit(instance: Model) -> bool:
    """Check if this model instance should be audited."""
    from utils.signals import bulk_mode_active

    # Import en masse : audit par-objet desactive (cf. utils.signals).
    if bulk_mode_active():
        return False
    model_name = instance.__class__.__name__
    return model_name in AUDITED_MODELS


def _get_manager(model_class: type[Model]) -> Manager[Model]:
    """Get the model's default manager with proper typing."""
    manager: Manager[Model] = model_class._default_manager
    return manager


def _serialize_value(value: object) -> str | int | float | bool | None:
    """Serialize a value for JSON storage."""
    if value is None:
        return None
    if isinstance(value, str | int | float | bool):
        return value
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def _store_old_values(sender: type[Model], instance: Model, **kwargs: object) -> None:
    """Store old values before save for comparison."""
    del kwargs
    if not _should_audit(instance):
        return

    audit_attr = "_audit_old_values"

    # Fail-open : le SELECT est isole dans un savepoint pour qu'une erreur DB n'empoisonne pas la transaction metier.
    try:
        if instance.pk:
            tracked_fields = [f.name for f in instance._meta.fields if f.name not in IGNORED_FIELDS]
            with transaction.atomic():
                old = _get_manager(sender).only(*tracked_fields).get(pk=instance.pk)
            old_values: dict[str, Any] = {f: getattr(old, f) for f in tracked_fields}
            setattr(instance, audit_attr, old_values)
        else:
            setattr(instance, audit_attr, {})
    except ObjectDoesNotExist:
        setattr(instance, audit_attr, {})
    except Exception:
        logger.exception("Audit: capture des anciennes valeurs echouee pour %s", instance.__class__.__name__)
        setattr(instance, audit_attr, {})


def _log_save(sender: type[Model], instance: Model, *, created: bool, **kwargs: object) -> None:
    """Log create/update operations (fail-open : ne propage jamais)."""
    del sender, kwargs
    if not _should_audit(instance):
        return
    # savepoint imbrique : sur PostgreSQL un echec d'insert empoisonnerait sinon toute la transaction metier malgre le try/except.
    try:
        with transaction.atomic():
            _do_log_save(instance, created=created)
    except Exception:
        logger.exception("Audit: enregistrement save echoue pour %s:%s", instance.__class__.__name__, instance.pk)


def _do_log_save(instance: Model, *, created: bool) -> None:
    """Construit et persiste l'entree d'audit pour un save."""
    model_name = instance.__class__.__name__
    context = get_audit_context()

    if created:
        AuditLog.log(
            action=str(AuditLog.Action.CREATE),
            model_name=model_name,
            object_id=instance.pk,
            object_repr=str(instance),
            changes={},
            user=context["user"],
            ip_address=context["ip_address"],
            user_agent=context["user_agent"],
            correlation_id=context["correlation_id"],
        )
        logger.debug("Audit: Created %s:%s", model_name, instance.pk)
    else:
        old_values = getattr(instance, "_audit_old_values", {})
        changes = {}

        for field in instance._meta.fields:
            field_name = field.name
            if field_name in IGNORED_FIELDS:
                continue

            old_value = old_values.get(field_name)
            new_value = getattr(instance, field_name, None)

            if hasattr(field, "remote_field") and field.remote_field:
                old_value = getattr(old_value, "pk", None) if old_value else None
                new_value = getattr(new_value, "pk", None) if new_value else None

            if old_value != new_value:
                changes[field_name] = {
                    "old": _serialize_value(old_value),
                    "new": _serialize_value(new_value),
                }

        if changes:
            AuditLog.log(
                action=str(AuditLog.Action.UPDATE),
                model_name=model_name,
                object_id=instance.pk,
                object_repr=str(instance),
                changes=changes,
                user=context["user"],
                ip_address=context["ip_address"],
                user_agent=context["user_agent"],
                correlation_id=context["correlation_id"],
            )
            logger.debug(
                "Audit: Updated %s:%s - %d fields changed",
                model_name,
                instance.pk,
                len(changes),
            )


def _log_delete(sender: type[Model], instance: Model, **kwargs: object) -> None:
    """Log delete operations (fail-open : ne propage jamais)."""
    del sender, kwargs
    if not _should_audit(instance):
        return
    try:
        with transaction.atomic():
            _do_log_delete(instance)
    except Exception:
        logger.exception("Audit: enregistrement delete echoue pour %s:%s", instance.__class__.__name__, instance.pk)


def _do_log_delete(instance: Model) -> None:
    """Construit et persiste l'entree d'audit pour un delete."""
    model_name = instance.__class__.__name__
    context = get_audit_context()

    AuditLog.log(
        action=str(AuditLog.Action.DELETE),
        model_name=model_name,
        object_id=instance.pk,
        object_repr=str(instance),
        changes={},
        user=context["user"],
        ip_address=context["ip_address"],
        user_agent=context["user_agent"],
        correlation_id=context["correlation_id"],
    )
    logger.debug("Audit: Deleted %s:%s", model_name, instance.pk)


# dispatch_uid evite les doubles enregistrements sur reload/apps.ready().
pre_save.connect(_store_old_values, dispatch_uid="audit_pre_save")
post_save.connect(_log_save, dispatch_uid="audit_post_save")
post_delete.connect(_log_delete, dispatch_uid="audit_post_delete")
