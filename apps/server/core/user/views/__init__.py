"""Vues pour le module user."""

from .auth import AdminLoginView, AdminLogoutView, AdminRefreshView
from .password import ChangePasswordView, RequestResetPasswordView, ResetPasswordView
from .profile import AdminProfileView
from .sessions import AdminSessionsView

__all__ = [
    "AdminLoginView",
    "AdminLogoutView",
    "AdminProfileView",
    "AdminRefreshView",
    "AdminSessionsView",
    "ChangePasswordView",
    "RequestResetPasswordView",
    "ResetPasswordView",
]
