from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser

from rest_framework.authentication import BaseAuthentication

from users.exceptions import TokenExpired, UserNotFound, MultipleSessionsFound
from users.models import LoggedInUser


class MultipleLoginBackend(BaseAuthentication):
    def authenticate(self, request, username=None, password=None):
        try:
            if LoggedInUser.objects.filter(user__username=username).exists():
                raise MultipleSessionsFound()
        except KeyError as _e:
            request.user = AnonymousUser()
            raise UserNotFound()

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
