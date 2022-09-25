from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from products.models import Product
from products.api.v1.serializers import ProductSerializer
from products.api.v1.permissions import (
    PermissionPolicyMixin,
    IsSeller,
    IsSellerAndOwner,
)


class ProductViewSet(PermissionPolicyMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSeller]
    permission_classes_per_method = {
        # except for list and retrieve where both users with "write" or "read-only"
        # permissions can access the endpoints.
        "create": [IsSeller],
        "list": [IsAuthenticated],
        "update": [IsSellerAndOwner],
    }
    http_method_names = [
        "get",
        "post",
        "put",
        "delete",
    ]
