from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.api.v1.viewsets import ProductViewSet

app_name = "products"

router = DefaultRouter()
router.register("products", ProductViewSet, basename="products")

urlpatterns = [
    path("", include(router.urls)),
]
