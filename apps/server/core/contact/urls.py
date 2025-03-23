"""
Routes API pour la gestion des messages de contact.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.contact import ContactMessageViewSet

router = DefaultRouter()
router.register(r"", ContactMessageViewSet, basename="contact-messages")

urlpatterns = [
    path("", include(router.urls)),
    path("unread/", ContactMessageViewSet.as_view({"get": "unread"}), name="contact-messages-unread"),
    path(
        "<int:pk>/mark-as-read/",
        ContactMessageViewSet.as_view({"post": "mark_as_read"}),
        name="contact-message-mark-as-read",
    ),
]
