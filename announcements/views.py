from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import AnnouncementForm

@login_required
def create_announcement(request):
    user_role = request.user.role.lower()
    if user_role not in ['admin', 'teacher', 'superadmin']:
        return redirect('dashboard')  # no permission

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, user_role=user_role)
        if form.is_valid():
            form.save()
            return redirect('announcement_list')  # or wherever you want to go
    else:
        form = AnnouncementForm(user_role=user_role)
    return render(request, 'announcements/announcement_form.html', {'form': form})
