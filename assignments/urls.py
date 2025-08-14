from django.urls import path
from .views import (
    AssignmentListView,
    AssignmentDetailView,
    AssignmentCreateView,
    SubmissionCreateView,
)

app_name = 'assignments'

urlpatterns = [
    path('', AssignmentListView.as_view(), name='assignment_list'),
    path('create/', AssignmentCreateView.as_view(), name='assignment_create'),
    path('<int:pk>/', AssignmentDetailView.as_view(), name='assignment_detail'),
    path('<int:pk>/submit/', SubmissionCreateView.as_view(), name='submit'),

]
