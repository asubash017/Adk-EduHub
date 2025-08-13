from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Note
from .forms import NoteForm
from django.http import FileResponse, Http404
import os

@login_required
def note_view(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    # Permissions: all logged-in users can view
    if request.user.role not in ['admin', 'teacher', 'student']:
        messages.error(request, "You don't have permission to view notes.")
        return redirect('notes:note_list')

    file_path = note.file.path
    if os.path.exists(file_path):
        # View in browser (remove as_attachment=True if you want inline)
        return FileResponse(open(file_path, 'rb'), as_attachment=False)
    else:
        raise Http404("File not found")


@login_required
def note_list(request):
    notes = Note.objects.all().order_by('-uploaded_at')  # show newest first
    return render(request, 'notes/note_list.html', {'notes': notes})

@login_required
def note_upload(request):
    if request.user.role not in ['teacher', 'admin']:
        messages.error(request, "You are not allowed to upload notes.")
        return redirect('notes:note_list')

    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.uploaded_by = request.user
            note.save()
            messages.success(request, "Note uploaded successfully.")
            return redirect('notes:note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/note_upload.html', {'form': form})


@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk)

    # Admin can edit any note
    if request.user.role.lower() == "admin":
        pass  # allowed

    # Teacher can edit any note
    elif request.user.role.lower() == "teacher":
        pass  # allowed

    else:
        messages.error(request, "You do not have permission to edit notes.")
        return redirect('notes:note_list')

    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, "Note updated successfully.")
            return redirect('notes:note_list')
    else:
        form = NoteForm(instance=note)

    return render(request, 'notes/note_form.html', {'form': form})



@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)

    # Admin can delete any note
    if request.user.role.lower() == "admin":
        note.delete()
        messages.success(request, "Note deleted successfully.")
        return redirect('notes:note_list')

    # Teacher can delete only their own notes
    if request.user.role.lower() == "teacher":
        if note.uploaded_by == request.user:
            note.delete()
            messages.success(request, "Note deleted successfully.")
        else:
            messages.error(request, "You can only delete notes you uploaded.")
        return redirect('notes:note_list')

    # Students & others - no access
    messages.error(request, "You do not have permission to delete this note.")
    return redirect('notes:note_list')

@login_required
def student_notes_list(request):
    notes = Note.objects.all()
    return render(request, 'notes/student_notes_list.html', {'notes': notes})


@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note})


