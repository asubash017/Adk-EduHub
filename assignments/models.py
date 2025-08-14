from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime

from courses.models import Course  # adjust if your app/model path differs

User = settings.AUTH_USER_MODEL

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    attachment = models.FileField(upload_to='assignments/', blank=True, null=True)
    
    # Only due_date now
    due_date = models.DateField(blank=True, null=True)
    
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments_uploaded')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} ({self.course})"

    @property
    def due_datetime(self):
        if not self.due_date:
            return None
        # Use start of day if you want datetime
        dt = datetime.combine(self.due_date, datetime.min.time())
        return timezone.make_aware(dt, timezone.get_current_timezone()) if timezone.is_naive(dt) else dt


class Submission(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
        ('returned', 'Returned'),
    ]

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')

    file = models.FileField(upload_to='submissions/', blank=True, null=True)
    text = models.TextField(blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        unique_together = ('assignment', 'student')
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.assignment.title} — {self.student}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.file and not (self.text and self.text.strip()):
            raise ValidationError('Upload a file or enter some text for your submission.')