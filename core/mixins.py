from django.core.exceptions import PermissionDenied

class RoleRequiredMixin:
    """
    Restricts view access based on allowed_roles list.
    Example:
        allowed_roles = ['admin', 'teacher']
    """
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        if self.allowed_roles and request.user.role not in self.allowed_roles:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
