from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orders.api.v1.viewsets import BuyViewSet

app_name = "buy"

router = DefaultRouter()
router.register("buy", BuyViewSet, basename="buy")

urlpatterns = [
    path("", include(router.urls)),
]
