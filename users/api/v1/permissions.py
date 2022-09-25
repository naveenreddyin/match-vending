from rest_framework import permissions


class IsBuyer(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.user_profile.is_buyer

    def has_permission(self, request, view):

        return request.user.is_authenticated and request.user.user_profile.is_buyer
