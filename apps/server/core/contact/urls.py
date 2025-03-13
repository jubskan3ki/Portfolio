"""
Routes API pour la gestion des messages de contact.
"""

from django.urls import path

from .views import ContactMessageCreateView

urlpatterns = [
    path("", ContactMessageCreateView.as_view(), name="contact-message-create"),
]
