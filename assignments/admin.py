from django.contrib import admin
from .models import Assignment

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "course",
        "uploaded_by",
        "uploaded_at",
        "last_edited_by",
        "last_edited_at",
        "due_date",
    )
    list_select_related = ("course", "uploaded_by", "last_edited_by")
    search_fields = ("title", "description")
    list_filter = ("course", "uploaded_by")
    readonly_fields = ("uploaded_at", "last_edited_at")
