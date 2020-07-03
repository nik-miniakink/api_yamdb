from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Request user id superuser or role is admin
    """
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.role == 'admin':
            return True
        else:
            return False
