from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.api.v1.viewsets import DepositViewSet, ResetDepositViewSet

app_name = "deposits"

router = DefaultRouter()
router.register("deposits", DepositViewSet, basename="deposits")
router.register("reset", ResetDepositViewSet, basename="reset")

urlpatterns = [
    path("users/", include(router.urls)),
]
