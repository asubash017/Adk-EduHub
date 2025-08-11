from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import Announcement

@login_required
def announcement_list_view(request):
    # Filter announcements by role or show all for superadmin
    user_role = request.user.role.lower()
    if user_role == 'superadmin':
        announcements = Announcement.objects.all().order_by('-created_at')
    else:
        announcements = Announcement.objects.filter(role_visible_to=user_role).order_by('-created_at')
    return render(request, 'announcements/announcement_list.html', {'announcements': announcements})


@login_required
def create_announcement(request):
    user_role = request.user.role.lower()
    if user_role not in ['admin', 'teacher', 'superadmin']:
        return redirect('dashboard')  # no permission

    if request.method == 'POST':
        form = Announcement(request.POST, user_role=user_role)
        if form.is_valid():
            form.save()
            return redirect('announcement_list')  # or wherever you want to go
    else:
        form = Announcement(user_role=user_role)
    return render(request, 'announcements/create_announcement.html', {'form': form})
