from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import AnnouncementForm
from .models import Announcement  # Import the model here

@login_required
def announcement_list_view(request):
    user_role = request.user.role.lower()
    if user_role == 'superadmin':
        announcements = Announcement.objects.all().order_by('-created_at')
    else:
        announcements = Announcement.objects.filter(role_visible_to=user_role).order_by('-created_at')
    return render(request, 'announcements/announcement_list.html', {'announcements': announcements})

@login_required
def create_announcement(request):
    user_role = request.user.role.lower()
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            # Optionally set user_role if needed, or handle in the form/model save
            announcement = form.save(commit=False)
            # If you want to force role_visible_to based on user role, do it here, else leave as per form data
            if user_role != 'superadmin':
                announcement.role_visible_to = user_role
            announcement.save()
            return redirect('announcements:announcement_list')
    else:
        form = AnnouncementForm()
    return render(request, 'announcements/create_announcement.html', {'form': form})
