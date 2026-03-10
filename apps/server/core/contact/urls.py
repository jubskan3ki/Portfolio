"""Configuration des URLs pour l'application Contact."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ContactInfoViewSet, ContactStatsView, ContactViewSet, FAQViewSet

router = DefaultRouter()
router.register(r"faqs", FAQViewSet, basename="faq")
router.register(r"infos", ContactInfoViewSet, basename="contact-info")
router.register(r"", ContactViewSet, basename="contact-submission")

urlpatterns = [
    path("stats/", ContactStatsView.as_view(), name="contact-stats"),
    path("", include(router.urls)),
]
