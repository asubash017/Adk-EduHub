from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('upload/', views.note_upload, name='note_upload'),
    path('edit/<int:pk>/', views.note_edit, name='note_edit'),
    path('delete/<int:note_id>/', views.note_delete, name='note_delete'),
    path('student/', views.student_notes_list, name='student_notes_list'),
    path('view/<int:note_id>/', views.note_view, name='note_view'),
    path('<int:pk>/', views.note_detail, name='note_detail'),




]
