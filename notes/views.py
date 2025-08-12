from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Note
from .forms import NoteForm

@login_required
def note_list(request):
    notes = Note.objects.all()
    return render(request, 'notes/note_list.html', {'notes': notes})

@login_required
def note_upload(request):
    if request.user.role not in ['teacher', 'admin']:
        messages.error(request, "You are not allowed to upload notes.")
        return redirect('note_list')

    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.uploaded_by = request.user
            note.save()
            messages.success(request, "Note uploaded successfully.")
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/note_upload.html', {'form': form})

@login_required
def note_delete(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.user == note.uploaded_by or request.user.role == 'admin':
        note.delete()
        messages.success(request, "Note deleted successfully.")
    else:
        messages.error(request, "You don't have permission to delete this note.")
    return redirect('note_list')
