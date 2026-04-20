"""Routes API pour le module User."""

from django.urls import path

from .views.admin import AdminLoginView, AdminLogoutView, AdminProfileView, AdminRefreshView, AdminSessionsView
from .views.password import ChangePasswordView, RequestResetPasswordView, ResetPasswordView

urlpatterns = [
    path("auth/login/", AdminLoginView.as_view(), name="user-login"),
    path("auth/logout/", AdminLogoutView.as_view(), name="user-logout"),
    path("auth/refresh/", AdminRefreshView.as_view(), name="token-refresh"),
    path("profile/", AdminProfileView.as_view(), name="admin-profile"),
    path("sessions/", AdminSessionsView.as_view(), name="admin-sessions"),
    path("password/change/", ChangePasswordView.as_view(), name="password-change"),
    path("request-reset-password/", RequestResetPasswordView.as_view(), name="request-reset-password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
]
