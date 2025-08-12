from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import CustomLoginView
from django.contrib.auth.views import LogoutView
#from core import views as core_views


urlpatterns = [
    path('admin/', admin.site.urls),

    # Custom Login View with Role-Based Redirect
    path('accounts/login/', CustomLoginView.as_view(), name='login'),

    path('accounts/logout/', LogoutView.as_view(), name='logout'),

    # Django Auth URLs (logout, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),

    # Core App URLs
    path('', include('core.urls')),

    path('courses/', include('courses.urls')),

    path('announcements/', include('announcements.urls', namespace='announcements')),

    path('notes/', include('notes.urls')),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
