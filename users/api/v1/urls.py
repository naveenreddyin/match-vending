from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.api.v1.viewsets import DepositViewSet, ResetDepositViewSet, LogoutViewSet

app_name = "deposits"

router = DefaultRouter()
router.register("deposits", DepositViewSet, basename="deposits")
router.register("reset", ResetDepositViewSet, basename="reset")
router.register("logout/all", LogoutViewSet, basename="logout")

urlpatterns = [
    path("users/", include(router.urls)),
]
