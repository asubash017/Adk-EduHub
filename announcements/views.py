from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import AnnouncementForm

@login_required
def announcement_list_view(request):
    # Filter announcements by role or show all for superadmin
    user_role = request.user.role.lower()
    if user_role == 'superadmin':
        announcements = AnnouncementForm.objects.all().order_by('-created_at')
    else:
        announcements = AnnouncementForm.objects.filter(role_visible_to=user_role).order_by('-created_at')
    return render(request, 'announcements/announcement_list.html', {'announcements': announcements})


@login_required
def create_announcement(request):
    user_role = request.user.role.lower()
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, user_role=user_role)
        if form.is_valid():
            form.save()
            return redirect('announcements:announcement_list')
    else:
        form = AnnouncementForm(user_role=user_role)
    return render(request, 'announcements/create_announcement.html', {'form': form})