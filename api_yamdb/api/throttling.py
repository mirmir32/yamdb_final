from rest_framework import throttling

ALLOWED_REQUEST = 1


class PostUserRateThrottle(throttling.UserRateThrottle):
    """Контроль количества операций по созданию отзыва."""
    scope = 'post_user'

    def allow_request(self, request, view):
        if (request.method == 'POST') > ALLOWED_REQUEST:
            return False
        return True
