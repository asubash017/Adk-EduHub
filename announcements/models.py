# announcements/models.py
from django.db import models
from core.models import CustomUser  # adjust path if different

class Announcement(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    role_visible_to = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.title
