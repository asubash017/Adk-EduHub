from django import forms
from .models import Assignment, Submission
from courses.models import Course

from django import forms
from django.utils import timezone
from .models import Assignment, Submission
from courses.models import Course

class AssignmentForm(forms.ModelForm):
    due_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'min': timezone.localdate()})
    )

    class Meta:
        model = Assignment
        fields = ['course', 'title', 'description', 'attachment', 'due_date', 'is_active']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user and getattr(self.user, 'role', None) == 'teacher':
            try:
                self.fields['course'].queryset = Course.objects.filter(teacher=self.user)
            except Exception:
                pass

    def clean_due_date(self):
        due_date = self.cleaned_data['due_date']
        if due_date < timezone.localdate():
            raise forms.ValidationError("Due date cannot be in the past.")
        return due_date

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file', 'text']

    def clean(self):
        cleaned = super().clean()
        file = cleaned.get('file')
        text = cleaned.get('text')
        if not file and not (text and text.strip()):
            raise forms.ValidationError('Upload a file or enter some text.')
        return cleaned
