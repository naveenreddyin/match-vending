from django.contrib.auth import get_user_model
from django.contrib.auth import logout

from rest_framework import viewsets, status, exceptions
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
)

from products.api.v1.permissions import PermissionPolicyMixin
from users.api.v1.serializers import DepositSerializer
from users.api.v1.permissions import IsBuyer

User = get_user_model()


class LogoutViewSet(viewsets.ViewSet):
    def create(self, request):
        logout(request)
        return Response(
            {"status": "Logged out from everywhere."}, status=status.HTTP_200_OK
        )


class ResetDepositViewSet(viewsets.ViewSet):
    permission_classes = [IsBuyer]
    permission_classes_per_method = {
        # except for list and retrieve where both users with "write" or "read-only"
        # permissions can access the endpoints.
        "partial_update": [IsBuyer],
    }

    def partial_update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise exceptions.NotFound("user not found.")
        profile = user.user_profile
        profile.deposit = 0
        profile.save()
        return Response({"status": "deposit reset done"}, status=status.HTTP_200_OK)


class DepositViewSet(viewsets.ViewSet):
    permission_classes = [IsBuyer]
    permission_classes_per_method = {
        # except for list and retrieve where both users with "write" or "read-only"
        # permissions can access the endpoints.
        "partial_update": [IsBuyer],
    }

    @extend_schema(
        request=DepositSerializer,
        responses=DepositSerializer,
    )
    def partial_update(self, request, pk=None):
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(pk=pk)
                # get profile
                profile = user.user_profile
                profile.deposit = serializer.validated_data["deposit"]
                profile.save()
            except User.DoesNotExist:
                raise exceptions.NotFound("User not found")
            return Response({"status": "deposit set"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
