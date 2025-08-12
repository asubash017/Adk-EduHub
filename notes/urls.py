from django.urls import path
from . import views

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('upload/', views.note_upload, name='note_upload'),
    path('delete/<int:note_id>/', views.note_delete, name='note_delete'),
]
