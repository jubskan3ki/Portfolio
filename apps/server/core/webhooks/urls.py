"""URLs pour le module webhooks."""

from rest_framework.routers import DefaultRouter

from .views import WebhookDeliveryViewSet, WebhookViewSet

router = DefaultRouter()
router.register(r"", WebhookViewSet, basename="webhook")
router.register(r"deliveries", WebhookDeliveryViewSet, basename="webhook-delivery")

urlpatterns = router.urls
