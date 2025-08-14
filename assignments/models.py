from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from courses.models import Course

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(default=timezone.now)
    file = models.FileField(upload_to="assignments/", blank=True, null=True)

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="assignments"
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_assignments",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    last_edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="edited_assignments",
    )
    last_edited_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("assignments:assignment_detail", args=[self.pk])

    @property
    def uploaded_by_name(self):
        u = self.uploaded_by
        return (u.get_full_name() or u.get_username()) if u else ""

    @property
    def last_edited_by_name(self):
        u = self.last_edited_by
        return (u.get_full_name() or u.get_username()) if u else ""
