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

    # File is optional. Use MEDIA settings below
    attachment = models.FileField(upload_to='assignments/', blank=True, null=True)

    # New fields that previously caused migration issues
    due_date = models.DateField(blank=True, null=True)
    due_time = models.TimeField(blank=True, null=True)

    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments_uploaded')
    uploaded_at = models.DateTimeField(auto_now_add=True)  # safe default; no migration default needed

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} ({self.course})"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.due_time and not self.due_date:
            raise ValidationError({'due_date': 'Provide a due date if you set a due time.'})

    @property
    def due_datetime(self):
        if not self.due_date:
            return None
        base_time = self.due_time or datetime.min.time()
        dt = datetime.combine(self.due_date, base_time)
        # Make aware if naive to avoid tz comparison issues
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