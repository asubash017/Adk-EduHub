from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'role_visible_to', 'created_at')
    list_filter = ('role_visible_to',)
    search_fields = ('title', 'content')
