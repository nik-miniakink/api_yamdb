from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    The request is authenticated as a admin, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user.is_superuser or
            request.user.role == 'admin'
        )


class IsStaffOrAuthorOrReadOnly(BasePermission):
    """
    The request is authenticated as a staff, or is a read-only request.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if request.method in ('PATH', 'DELETE'):
                return (obj.author == request.user or request.user.role in (
                    'admin', 'moderator') or request.user.is_superuser)
            return (obj.author == request.user or request.user.role in (
                'admin', 'moderator') or request.user.is_superuser)

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.user.is_authenticated:
            return True
