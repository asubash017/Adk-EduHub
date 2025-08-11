from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Announcement
from .forms import AnnouncementForm

# Helper function to check if user can manage announcements
def can_manage_announcements(user):
    return user.role in ["admin", "teacher"]

@login_required
def announcement_list(request):
    announcements = Announcement.objects.all().order_by("-created_at")
    return render(request, "announcements/announcement_list.html", {"announcements": announcements})

@login_required
def announcement_create(request):
    if not can_manage_announcements(request.user):
        raise PermissionDenied("You do not have permission to create announcements.")
    
    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            ann = form.save(commit=False)
            ann.created_by = request.user
            ann.save()
            return redirect("announcement_list")
    else:
        form = AnnouncementForm()
    return render(request, "announcements/announcement_form.html", {"form": form})

@login_required
def announcement_edit(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if not can_manage_announcements(request.user):
        raise PermissionDenied
    if request.method == "POST":
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect("announcement_list")
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, "announcements/announcement_form.html", {"form": form})

@login_required
def announcement_delete(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if not can_manage_announcements(request.user):
        raise PermissionDenied
    if request.method == "POST":
        announcement.delete()
        return redirect("announcement_list")
    return render(request, "announcements/announcement_confirm_delete.html", {"announcement": announcement})
