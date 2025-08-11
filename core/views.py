from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import ProfileUpdateForm
from .models import CustomUser
from announcements.models import Announcement
from operator import attrgetter

from itertools import chain  # not really needed if only one model used


@login_required
def home_redirect_view(request):
    role = request.user.role.lower()
    if role == 'admin':
        return redirect('admin_dashboard')
    elif role == 'teacher':
        return redirect('teacher_dashboard')
    elif role == 'student':
        return redirect('student_dashboard')
    else:
        return redirect('login')  # fallback


class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        role = user.role.lower()
        if role == 'admin':
            return '/dashboard/admin/'
        elif role == 'teacher':
            return '/dashboard/teacher/'
        elif role == 'student':
            return '/dashboard/student/'
        return '/'  # fallback redirect


@login_required
def login_redirect_view(request):
    user = request.user
    role = user.role.lower()
    if role == 'admin':
        return redirect('admin_dashboard')
    elif role == 'teacher':
        return redirect('teacher_dashboard')
    elif role == 'student':
        return redirect('student_dashboard')
    else:
        return redirect('dashboard')  # fallback


@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, 'core/profile.html', {'form': form})


@login_required
def admin_dashboard(request):
    user = request.user
    # Admin sees all announcements (both teacher and student), or optionally filtered by role
    announcements = Announcement.objects.filter(
        role_visible_to__in=['teacher', 'student']
    ).order_by('-created_at')

    context = {
        'announcements': announcements,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
def teacher_dashboard(request):
    # Teachers see announcements meant for teachers only
    announcements = Announcement.objects.filter(
        role_visible_to='teacher'
    ).order_by('-created_at')

    context = {
        'announcements': announcements,
    }
    return render(request, 'dashboard/teacher_dashboard.html', context)


@login_required
def student_dashboard(request):
    announcements = Announcement.objects.filter(
        role_visible_to='student'
    ).order_by('-created_at')[:5]  # latest 5 for dashboard summary

    context = {
        'announcements': announcements,
    }
    return render(request, 'dashboard/student_dashboard.html', context)


@login_required
def settings_view(request):
    return render(request, 'core/settings.html')
