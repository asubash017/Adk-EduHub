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
    
class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name="submissions"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="submissions"
    )
    submitted_file = models.FileField(upload_to="submissions/")
    submitted_at = models.DateTimeField(auto_now_add=True)
    last_edited_at = models.DateTimeField(blank=True, null=True)
    
    # Rating and feedback by teacher/admin
    rating = models.IntegerField(blank=True, null=True)  # e.g., 0-100 or 1-5
    feedback = models.TextField(blank=True, null=True)
    rated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="graded_submissions"
    )

    class Meta:
        unique_together = ("assignment", "student")
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.assignment.title} - {self.student.get_full_name()}"

    @property
    def student_name(self):
        return self.student.get_full_name() or self.student.get_username()

    @property
    def rated_by_name(self):
        return self.rated_by.get_full_name() if self.rated_by else ""

class Submission(models.Model):
    assignment = models.ForeignKey("Assignment", related_name="submissions", on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    submitted_file = models.FileField(upload_to="submissions/", null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    # Grading fields
    rating = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.student} - {self.assignment.title}"
