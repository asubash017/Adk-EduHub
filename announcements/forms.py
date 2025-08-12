from django import forms
from .models import Announcement, ROLE_CHOICES

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'role_visible_to']
        widgets = {
            'role_visible_to': forms.CheckboxSelectMultiple
        }

