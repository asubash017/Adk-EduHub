from django import forms
from .models import Announcement, ROLE_CHOICES

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'role_visible_to']

    # Limit roles selectable by user (optional, explained below)
    def __init__(self, *args, **kwargs):
        user_role = kwargs.pop('user_role', None)
        super().__init__(*args, **kwargs)
        if user_role == 'teacher':
            # Teacher can't create announcements for admin or all
            allowed_roles = [('teacher', 'Teacher'), ('student', 'Student')]
            self.fields['role_visible_to'].choices = allowed_roles
        elif user_role == 'admin':
            # Admin can't create for superadmin but can create for all others
            allowed_roles = [('admin', 'Admin'), ('teacher', 'Teacher'), ('student', 'Student'), ('all', 'All')]
            self.fields['role_visible_to'].choices = allowed_roles
        elif user_role == 'superadmin':
            self.fields['role_visible_to'].choices = ROLE_CHOICES
        else:
            # No permission to create announcements
            self.fields['role_visible_to'].choices = []
