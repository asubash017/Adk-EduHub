from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Announcement
from .forms import AnnouncementForm
from core.mixins import RoleRequiredMixin  # If you created the mixin as I suggested

class AnnouncementListView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'announcements/announcement_list.html'
    context_object_name = 'announcements'

    def get_queryset(self):
        user_role = self.request.user.role
        return Announcement.objects.filter(role_visible_to=user_role).order_by('-created_at')

class AnnouncementCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcements/announcement_form.html'
    success_url = reverse_lazy('announcements:announcement_list')
    allowed_roles = ['admin', 'teacher']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AnnouncementUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcements/announcement_form.html'
    success_url = reverse_lazy('announcements:announcement_list')
    allowed_roles = ['admin', 'teacher']

class AnnouncementDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = Announcement
    template_name = 'announcements/announcement_confirm_delete.html'
    success_url = reverse_lazy('announcements:announcement_list')
    allowed_roles = ['admin', 'teacher']
