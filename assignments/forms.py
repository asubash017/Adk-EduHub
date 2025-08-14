from django import forms
from .models import Assignment

class AssignmentForm(forms.ModelForm):
    """Used by admin/teacher (has due_date & course)."""
    class Meta:
        model = Assignment
        fields = ["title", "description", "due_date", "file", "course"]

class StudentAssignmentForm(forms.ModelForm):
    """Used by students (no course/due_date fields)."""
    class Meta:
        model = Assignment
        fields = ["title", "description", "file"]
