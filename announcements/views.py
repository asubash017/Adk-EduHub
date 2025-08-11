from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AnnouncementForm
from .models import Announcement 
from django.db.models import Q
from core.decorators import role_required 

@login_required
def announcement_list_view(request):
    user_role = request.user.role.lower()
    if user_role == 'superadmin':
        announcements = Announcement.objects.all().order_by('-created_at')
    else:
        announcements = Announcement.objects.filter(
            role_visible_to__in=[user_role, 'all']
        ).order_by('-created_at')
    return render(request, 'announcements/announcement_list.html', {'announcements': announcements})


@login_required
@role_required(['admin', 'teacher', 'superadmin'])
def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('announcements:announcement_list')
    else:
        form = AnnouncementForm()
    return render(request, 'announcements/create_announcement.html', {'form': form})

@login_required
@role_required(['admin', 'teacher', 'superadmin'])
def edit_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('announcements:announcement_list')
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'announcements/edit_announcement.html', {'form': form})

@login_required
@role_required(['admin', 'teacher', 'superadmin'])
def delete_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        announcement.delete()
        return redirect('announcements:announcement_list')
    return render(request, 'announcements/confirm_delete.html', {'announcement': announcement})