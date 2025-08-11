from django.views.generic import ListView
from .models import Announcement
from core.mixins import RoleRequiredMixin

class AnnouncementListView(RoleRequiredMixin, ListView):
    model = Announcement
    template_name = 'announcements/announcement_list.html'
    context_object_name = 'announcements'
    role_required = None  # No strict role check here; filtering done in get_queryset

    def get_queryset(self):
        user_role = self.request.user.role.lower()
        return Announcement.objects.filter(role_visible_to=user_role).order_by('-created_at')
