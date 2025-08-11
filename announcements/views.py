from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import AnnouncementForm
from .models import Announcement 
from django.db.models import Q

@login_required
def announcement_list_view(request):
    user_role = request.user.role.lower()
    if user_role == 'superadmin':
        announcements = Announcement.objects.all().order_by('-created_at')
    else:
        announcements = Announcement.objects.filter(
            Q(role_visible_to=user_role) | Q(role_visible_to='all')
        ).order_by('-created_at')
    return render(request, 'announcements/announcement_list.html', {'announcements': announcements})

@login_required
def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.user = request.user
            announcement.save()
            return redirect('announcements:announcement_list')
    else:
        form = AnnouncementForm()
    return render(request, 'announcements/create_announcement.html', {'form': form})
