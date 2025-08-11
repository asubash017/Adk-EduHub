from django.urls import path
from . import views
from .views import (
    announcement_list_view,
    create_announcement,
    edit_announcement,
    delete_announcement,
)

app_name = 'announcements'

urlpatterns = [
    path('', views.announcement_list_view, name='announcement_list'),
    path('create/', views.create_announcement, name='create'),
    path('edit/<int:pk>/', edit_announcement, name='edit'),
    path('delete/<int:pk>/', delete_announcement, name='delete'),
]
