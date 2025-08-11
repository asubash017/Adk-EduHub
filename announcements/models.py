from django.db import models

ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('teacher', 'Teacher'),
    ('student', 'Student'),
    ('all', 'All'),
)

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
   
    role_visible_to = models.CharField(max_length=10, choices=ROLE_CHOICES, default='all')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
