from django.urls import path
from .views import AnnouncementListView, views

app_name = 'announcements'

urlpatterns = [
    path('', AnnouncementListView.as_view(), name='announcement_list'),
    path('create/', views.create_announcement, name='create_announcement'),
]
