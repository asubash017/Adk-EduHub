from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy

from .models import Assignment, Submission
from .forms import AssignmentForm, SubmissionForm

TEACHER = 'teacher'
STUDENT = 'student'

def is_teacher(user):
    return getattr(user, 'role', None) == TEACHER

def is_student(user):
    return getattr(user, 'role', None) == STUDENT


class AssignmentListView(LoginRequiredMixin, ListView):
    model = Assignment
    template_name = 'assignments/assignment_list.html'
    context_object_name = 'assignments'

    def get_queryset(self):
        qs = super().get_queryset().select_related('course', 'uploaded_by')
        user = self.request.user
        if is_teacher(user):
            return qs.filter(uploaded_by=user)
        return qs


class AssignmentDetailView(LoginRequiredMixin, DetailView):
    model = Assignment
    template_name = 'assignments/assignment_detail.html'
    context_object_name = 'assignment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if is_teacher(self.request.user):
            context['submissions'] = self.object.submissions.select_related('student').all()
        return context


class AssignmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignments/assignment_form.html'
    success_url = reverse_lazy('assignments:assignment_list')

    def test_func(self):
        return getattr(self.request.user, 'role', None) == 'teacher'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)



class SubmissionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = 'assignments/submission_form.html'

    def test_func(self):
        return getattr(self.request.user, 'role', None) == 'student'

    def dispatch(self, request, *args, **kwargs):
        self.assignment = get_object_or_404(Assignment, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.assignment = self.assignment
        form.instance.student = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('assignments:assignment_detail', args=[self.assignment.pk])
