from django import forms
from .models import Announcement, ROLE_CHOICES

class AnnouncementForm(forms.ModelForm):
    role_visible_to = forms.MultipleChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = Announcement
        fields = ['title', 'content', 'role_visible_to']
