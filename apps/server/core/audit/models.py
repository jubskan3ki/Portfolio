"""Audit log models for tracking data changes."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.utils import timezone

from .managers import AuditLogManager

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser


class AuditLog(models.Model):
    """
    Model for storing audit logs of data changes.

    Tracks create, update, and delete operations on models
    with full context including user, IP, and change details.
    """

    class Action(models.TextChoices):
        """Available audit actions."""

        CREATE = "create", "Create"
        UPDATE = "update", "Update"
        DELETE = "delete", "Delete"

    # Who made the change
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
        help_text="User who performed the action",
    )

    # What action was performed
    action = models.CharField(
        max_length=10,
        choices=Action.choices,
        db_index=True,
        help_text="Type of action performed",
    )

    # What was changed
    model_name = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Name of the model that was modified",
    )
    object_id = models.CharField(
        max_length=100,
        help_text="Primary key of the modified object",
    )
    object_repr = models.CharField(
        max_length=255,
        blank=True,
        help_text="String representation of the object",
    )

    # Change details
    changes = models.JSONField(
        default=dict,
        blank=True,
        help_text="Dictionary of field changes (old_value, new_value)",
    )

    # Request context
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="IP address of the request",
    )
    user_agent = models.CharField(
        max_length=512,
        blank=True,
        help_text="User agent of the request",
    )
    correlation_id = models.CharField(
        max_length=64,
        blank=True,
        db_index=True,
        help_text="Correlation ID for request tracing",
    )

    # Timestamp
    timestamp = models.DateTimeField(
        default=timezone.now,
        db_index=True,
        help_text="When the action occurred",
    )

    objects: AuditLogManager = AuditLogManager()

    class Meta:
        """Model metadata."""

        db_table = "audit_logs"
        ordering = ["-timestamp"]
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"
        indexes = [
            models.Index(fields=["model_name", "object_id"]),
            models.Index(fields=["user", "timestamp"]),
            models.Index(fields=["action", "timestamp"]),
            models.Index(fields=["-timestamp"]),
        ]

    def __str__(self) -> str:
        """String representation."""
        user_str = self.user.email if self.user else "Anonymous"
        return f"{self.action} {self.model_name}:{self.object_id} by {user_str}"

    @classmethod
    def log(
        cls,
        action: str,
        model_name: str,
        object_id: str | int,
        object_repr: str = "",
        changes: dict[str, dict[str, str | int | float | bool | None]] | None = None,
        user: AbstractBaseUser | None = None,
        ip_address: str | None = None,
        user_agent: str = "",
        correlation_id: str = "",
    ) -> AuditLog:
        """
        Create an audit log entry.

        Args:
            action: The action performed (create, update, delete)
            model_name: Name of the model
            object_id: Primary key of the object
            object_repr: String representation of the object
            changes: Dictionary of changes {field: {old: x, new: y}}
            user: User who performed the action
            ip_address: IP address of the request
            user_agent: User agent string
            correlation_id: Correlation ID for tracing

        Returns:
            Created AuditLog instance
        """
        return cls.objects.create(
            action=action,
            model_name=model_name,
            object_id=str(object_id),
            object_repr=object_repr[:255] if object_repr else "",
            changes=changes or {},
            user=user,
            ip_address=ip_address,
            user_agent=user_agent[:512] if user_agent else "",
            correlation_id=correlation_id[:64] if correlation_id else "",
        )
