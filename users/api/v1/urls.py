from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.api.v1.viewsets import DepositViewSet

app_name = "deposits"

router = DefaultRouter()
router.register("deposits", DepositViewSet, basename="deposits")

urlpatterns = [
    path("users/", include(router.urls)),
]
