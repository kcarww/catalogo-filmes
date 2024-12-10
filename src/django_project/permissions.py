from rest_framework import permissions

from core._shared.infrastructure.auth.jwt_auth_service import JWTAuthService


class IsAuthenticated(permissions.BasePermission):
    message = 'Invalid or expired token.'

    def has_permission(self, request, view):
        token = request.headers.get('Authorization', '')
        if not JWTAuthService(token).is_authenticated():
            return False
        return True


class IsAdmin(permissions.BasePermission):
    message = 'User does not have admin privileges.'

    def has_permission(self, request, view):
        token = request.headers.get('Authorization', '')
        if not JWTAuthService(token).has_role('admin'):
            return False
        return True