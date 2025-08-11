from django.urls import path
from . import views

app_name = 'announcements'

urlpatterns = [
    path('', views.AnnouncementListView.as_view(), name='announcement_list'),
    path('add/', views.AnnouncementCreateView.as_view(), name='announcement_add'),
    path('edit/<int:pk>/', views.AnnouncementUpdateView.as_view(), name='announcement_edit'),
    path('delete/<int:pk>/', views.AnnouncementDeleteView.as_view(), name='announcement_delete'),
    path('admin/add/', views.AdminAnnouncementCreateView.as_view(), name='adminannouncement_add'),
    path('admin/edit/<int:pk>/', views.AdminAnnouncementUpdateView.as_view(), name='adminannouncement_edit'),
    path('admin/delete/<int:pk>/', views.AdminAnnouncementDeleteView.as_view(), name='adminannouncement_delete'),
]

