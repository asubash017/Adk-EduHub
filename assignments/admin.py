from django.contrib import admin
from .models import Assignment, Submission

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'due_date', 'uploaded_by', 'uploaded_at')
    search_fields = ('title', 'description')
    list_filter = ('due_date', 'uploaded_by')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'submitted_by', 'status', 'grade')

    def submitted_by(self, obj):
        return obj.student
