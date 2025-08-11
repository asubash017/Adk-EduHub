from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from .models import Announcement
from .forms import AnnouncementForm

def is_admin_or_teacher(user):
    return user.role.lower() in ['admin', 'teacher']

@login_required
def announcement_list_view(request):
    user_role = request.user.role.lower()

    # Show announcements where role_visible_to matches user's role or is 'all'
    announcements = Announcement.objects.filter(
        role_visible_to__in=[user_role, 'all']
    ).order_by('-created_at')

    return render(request, 'announcements/announcement_list.html', {'announcements': announcements})

@login_required
@user_passes_test(is_admin_or_teacher)
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
@user_passes_test(is_admin_or_teacher)
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
@user_passes_test(is_admin_or_teacher)
def delete_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        announcement.delete()
        return redirect('announcements:announcement_list')
    return render(request, 'announcements/confirm_delete.html', {'announcement': announcement})
