from django.urls import path
from . import views

app_name = 'announcements'

urlpatterns = [
    path('', views.AnnouncementListView.as_view(), name='announcement_list'),
    path('add/', views.AnnouncementCreateView.as_view(), name='announcement_add'),
    path('edit/<int:pk>/', views.AnnouncementUpdateView.as_view(), name='announcement_edit'),
    path('delete/<int:pk>/', views.AnnouncementDeleteView.as_view(), name='announcement_delete'),
]
