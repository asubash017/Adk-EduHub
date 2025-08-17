from django import forms
from .models import Assignment
from .models import Submission
from django.utils import timezone

class AssignmentForm(forms.ModelForm):
    """Used by admin/teacher (has due_date & course)."""
    class Meta:
        model = Assignment
        fields = ["title", "description", "due_date", "file", "course"]

    def clean_due_date(self):
        due_date = self.cleaned_data.get("due_date")
        if due_date <= timezone.now().date():
            raise forms.ValidationError("Due date must be in the future.")
        return due_date

class StudentAssignmentForm(forms.ModelForm):
    """Used by students (no course/due_date fields)."""
    class Meta:
        model = Assignment
        fields = ["title", "description", "file"]

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["submitted_file"]

class SubmissionFeedbackForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["rating", "feedback"]