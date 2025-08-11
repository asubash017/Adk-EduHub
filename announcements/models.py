from django.db import models


class Announcement(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('all', 'All'),   # <--- Make sure this is here
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    role_visible_to = models.CharField(max_length=20, choices=ROLE_CHOICES, default='all')
    created_at = models.DateTimeField(auto_now_add=True)

    # other fields...



