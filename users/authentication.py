from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTSessionAuthentication(JWTAuthentication):
    def authenticate(self, request):
        authenticated = super().authenticate(request)
        if not authenticated:
            return None
        user, token = authenticated
        return user, token
