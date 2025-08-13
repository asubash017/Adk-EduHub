from django import forms
from .models import Note, NoteComment

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'description', 'file']

class NoteCommentForm(forms.ModelForm):
    class Meta:
        model = NoteComment
        fields = ['content']
