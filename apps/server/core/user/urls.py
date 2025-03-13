"""
Routes API pour la gestion de l'administrateur unique.
"""

from django.urls import path

from .views import (
    AdminLoginView,
    AdminView,
    RequestResetPasswordView,
    ResetPasswordView,
)

urlpatterns = [
    path("login/", AdminLoginView.as_view(), name="admin-login"),
    path("profile/", AdminView.as_view(), name="admin-profile"),
    path("request-reset-password/", RequestResetPasswordView.as_view(), name="request-reset-password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
]
