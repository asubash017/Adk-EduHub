from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('<int:pk>/', views.note_detail, name='note_detail'),
    path('comment/delete/<int:comment_id>/', views.note_comment_delete, name='note_comment_delete'),
    path('comment/like/<int:comment_id>/', views.note_comment_like, name='note_comment_like'),
    path('comment/dislike/<int:comment_id>/', views.note_comment_dislike, name='note_comment_dislike'),
]
