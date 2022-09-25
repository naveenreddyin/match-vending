from django.contrib.auth import get_user_model

from rest_framework import viewsets, status, exceptions
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
)

from products.api.v1.permissions import PermissionPolicyMixin
from orders.api.v1.serializers import BuySerializer
from users.api.v1.permissions import IsBuyer
from products.models import Product

User = get_user_model()


class BuyViewSet(viewsets.ViewSet):
    permission_classes = [IsBuyer]
    permission_classes_per_method = {
        # except for list and retrieve where both users with "write" or "read-only"
        # permissions can access the endpoints.
        "create": [IsBuyer],
    }

    @extend_schema(
        request=BuySerializer,
        responses=BuySerializer,
    )
    def create(self, request):
        user = request.user
        serializer = BuySerializer(data=request.data)
        if serializer.is_valid():
            desired_amount = serializer.validated_data["amount"]
            # get product
            try:
                product = Product.objects.get(pk=serializer.validated_data["product"])
            except Product.DoesNotExist:
                raise exceptions.NotFound("Product not found")
            # check stock
            print("amount ", serializer.validated_data)
            amount_needed = product.amount - desired_amount
            if amount_needed < 0:
                raise exceptions.ValidationError(
                    "cant fulfill purchase since the amount desired is not possible."
                )
            # check if balance is there
            total_purchase_cost = product.cost * desired_amount
            if user.user_profile.deposit == None:
                raise exceptions.ValidationError("please deposit some amount.")
            if total_purchase_cost > user.user_profile.deposit:
                raise exceptions.ValidationError("your balance is low.")

            # calculate remaining balance
            total_user_balance_after_purchase = (
                user.user_profile.deposit - total_purchase_cost
            )
            # save new user deposit
            user.user_profile.deposit = total_user_balance_after_purchase
            user.user_profile.save()
            # update product
            product.amount = amount_needed
            product.save()

            return Response(
                {
                    "status": {
                        "product": product.name,
                    }
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
