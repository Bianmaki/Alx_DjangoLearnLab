from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Allow read methods for everyone. Write/delete only by the author (owner).
    """

    def has_permission(self, request, view):
        # Allow any to list or retrieve; require authentication for create/update/delete
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions ok
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only owner can edit/delete
        return getattr(obj, 'author', None) == request.user
