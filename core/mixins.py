from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class RoleRequiredMixin(UserPassesTestMixin):
    role_required = 'admin', 'teacher'

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if self.role_required is None:
            return True
        return user.role.lower() == self.role_required.lower()

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return super().handle_no_permission()
