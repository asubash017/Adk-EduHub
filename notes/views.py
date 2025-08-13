from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Note, NoteComment
from .forms import NoteCommentForm

@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    comments = note.comments.filter(parent__isnull=True).order_by('-created_at')  # top-level comments

    if request.method == 'POST':
        form = NoteCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.note = note
            comment.save()
            messages.success(request, "Comment added!")
            return redirect('notes:note_detail', pk=note.pk)
    else:
        form = NoteCommentForm()

    return render(request, 'notes/note_detail.html', {
        'note': note,
        'comments': comments,
        'form': form
    })


@login_required
def note_comment_delete(request, comment_id):
    comment = get_object_or_404(NoteComment, id=comment_id)
    if request.user == comment.user or request.user.role == 'admin':
        comment.delete()
        messages.success(request, "Comment deleted!")
    else:
        messages.error(request, "No permission to delete!")
    return redirect('notes:note_detail', pk=comment.note.pk)


# AJAX Likes/Dislikes
@login_required
def note_comment_like(request, comment_id):
    comment = get_object_or_404(NoteComment, id=comment_id)
    user = request.user

    if user in comment.likes.all():
        comment.likes.remove(user)
    else:
        comment.likes.add(user)
        comment.dislikes.remove(user)

    return JsonResponse({
        'likes': comment.likes.count(),
        'dislikes': comment.dislikes.count()
    })

@login_required
def note_comment_dislike(request, comment_id):
    comment = get_object_or_404(NoteComment, id=comment_id)
    user = request.user

    if user in comment.dislikes.all():
        comment.dislikes.remove(user)
    else:
        comment.dislikes.add(user)
        comment.likes.remove(user)

    return JsonResponse({
        'likes': comment.likes.count(),
        'dislikes': comment.dislikes.count()
    })
