from django import forms
from .models import Announcement

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'role_visible_to']  # Add your relevant fields here

    def __init__(self, *args, **kwargs):
        self.user_role = kwargs.pop('user_role', None)  # Optional if you want to use it
        super().__init__(*args, **kwargs)

        # Example: Limit role_visible_to choices based on user_role (optional)
        if self.user_role and self.user_role != 'superadmin':
            self.fields['role_visible_to'].choices = [
                (self.user_role, self.user_role.capitalize())
            ]
