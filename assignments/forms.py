from django import forms
from .models import Assignment, Submission
from courses.models import Course

class AssignmentForm(forms.ModelForm):
    due_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    due_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Assignment
        fields = ['course', 'title', 'description', 'attachment', 'due_date', 'due_time', 'is_active']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Optional: restrict courses to the teacher creating the assignment
        if self.user and hasattr(self.user, 'role') and self.user.role == 'teacher':
            try:
                self.fields['course'].queryset = Course.objects.filter(teacher=self.user)
            except Exception:
                # If your Course model has a different relation, adjust the filter
                pass

    def clean(self):
        cleaned = super().clean()
        due_date = cleaned.get('due_date')
        due_time = cleaned.get('due_time')
        if due_time and not due_date:
            self.add_error('due_date', 'Provide a due date if you set a due time.')
        return cleaned


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
