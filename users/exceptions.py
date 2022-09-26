from rest_framework.exceptions import (
    APIException,
    NotFound,
    PermissionDenied,
    NotAuthenticated,
)


class TokenExpired(NotAuthenticated):
    status_code = 403
    default_detail = "Access token expired"
    default_code = "forbidden"


class MultipleSessionsFound(PermissionDenied):
    status_code = 403
    default_detail = "There is already an active session using your account. Logout all sessions by going to /logout/all uri."
    default_code = "forbidden"


class UserNotFound(NotAuthenticated):
    status_code = 403
    default_detail = "User not found"
    default_code = "forbidden"
