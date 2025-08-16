# assignments/urls.py
from django.urls import path
from . import views
from .views import SubmissionDetailView

app_name = "assignments"

urlpatterns = [
    path("", views.AssignmentListView.as_view(), name="assignment_list"),
    path("create/", views.AssignmentCreateView.as_view(), name="assignment_create"),
    path("<int:pk>/", views.AssignmentDetailView.as_view(), name="assignment_detail"),
    path("<int:pk>/edit/", views.AssignmentUpdateView.as_view(), name="assignment_edit"),
    path("<int:pk>/delete/", views.AssignmentDeleteView.as_view(), name="assignment_delete"),

    # Submissions
    path("submission/create/<int:assignment_id>/", views.SubmissionCreateView.as_view(), name="submission_create"),
    path("submission/<int:pk>/edit/", views.SubmissionUpdateView.as_view(), name="submission_edit"),
    path("submission/<int:pk>/", SubmissionDetailView.as_view(), name="submission_detail"),
    path("submission/<int:pk>/delete/", views.SubmissionDeleteView.as_view(), name="submission_delete"),
    path("submission/<int:pk>/feedback/", views.SubmissionFeedbackUpdateView.as_view(), name="submission_feedback"),
    path('<int:pk>/grade/', views.grade_submissions, name='grade_submissions'),

]
