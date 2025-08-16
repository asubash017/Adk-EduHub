from django.utils import timezone
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Assignment, Submission
from .forms import AssignmentForm, StudentAssignmentForm, SubmissionForm, SubmissionFeedbackForm
from django.shortcuts import get_object_or_404, render

# --- role helpers ------------------------------------------------------------
ADMIN = "admin"
TEACHER = "teacher"
STUDENT = "student"

def user_role(user):
    return getattr(user, "role", None)

def is_admin(user):
    return user_role(user) == ADMIN

def is_teacher(user):
    return user_role(user) == TEACHER

def is_student(user):
    return user_role(user) == STUDENT


# --- permission mixins -------------------------------------------------------
class CanEditAssignmentMixin(UserPassesTestMixin):
    """Admin: can edit any. Teacher: only own. Student: cannot edit."""
    def test_func(self):
        user = self.request.user
        obj = self.get_object()
        if is_admin(user):
            return True
        if is_teacher(user):
            return obj.uploaded_by_id == user.id
        return False  # students cannot edit

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy("assignments:assignment_list"))


class CanDeleteAssignmentMixin(UserPassesTestMixin):
    """Admin: any. Teacher: own only. Student: own only."""
    def test_func(self):
        user = self.request.user
        obj = self.get_object()
        if is_admin(user):
            return True
        if is_teacher(user) or is_student(user):
            return obj.uploaded_by_id == user.id
        return False

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy("assignments:assignment_list"))


# --- views -------------------------------------------------------------------
class AssignmentListView(ListView):
    model = Assignment
    template_name = "assignments/assignment_list.html"
    context_object_name = "assignments"

    def get_queryset(self):
        # Prefetch submissions and related students to reduce queries
        return (
            super()
            .get_queryset()
            .select_related("course")
            .prefetch_related("submissions__student")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

         # Attach the student's submission directly to each assignment
        if user.role == "student":
            for assignment in context["assignments"]:
                assignment.student_submission = assignment.submissions.filter(student=user).first()

        return context
    




class AssignmentDetailView(DetailView):
    model = Assignment
    template_name = "assignments/assignment_detail.html"
    context_object_name = "assignment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assignment = self.get_object()
        user = self.request.user

        # Add submission for the logged-in student
        submission = None
        if user.is_authenticated and user.role == "student":
            submission = assignment.submissions.filter(student=user).first()

        context["submission"] = submission
        return context

class AssignmentCreateView(LoginRequiredMixin, CreateView):
    model = Assignment
    template_name = "assignments/assignment_form.html"

    def get_form_class(self):
        # Students: limited form; Admin/Teacher: full form.
        return StudentAssignmentForm if is_student(self.request.user) else AssignmentForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # You could pass user to form if you need further customization.
        kwargs["initial"] = kwargs.get("initial", {})
        if is_teacher(self.request.user) and "due_date" not in kwargs["initial"]:
            # Optional: set a sensible default due date for teachers/admins.
            kwargs["initial"]["due_date"] = timezone.now().date()
        return kwargs

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("assignments:assignment_list")


class AssignmentUpdateView(LoginRequiredMixin, CanEditAssignmentMixin, UpdateView):
    model = Assignment
    template_name = "assignments/assignment_form.html"
    form_class = AssignmentForm  # students never reach this view (blocked)

    def form_valid(self, form):
        form.instance.last_edited_by = self.request.user
        form.instance.last_edited_at = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("assignments:assignment_list")


class AssignmentDeleteView(LoginRequiredMixin, CanDeleteAssignmentMixin, DeleteView):
    model = Assignment
    template_name = "assignments/assignment_confirm_delete.html"
    success_url = reverse_lazy("assignments:assignment_list")



# Student: submit assignment
class SubmissionCreateView(LoginRequiredMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = "assignments/submission_form.html"

    def form_valid(self, form):
        form.instance.student = self.request.user
        # Match URL kwarg name exactly
        assignment_id = self.kwargs.get("assignment_id")
        form.instance.assignment = get_object_or_404(Assignment, pk=assignment_id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("assignments:assignment_list")



# Student: update submission
class SubmissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Submission
    form_class = SubmissionForm
    template_name = "assignments/submission_form.html"

    def get_queryset(self):
        # Student can only edit their own submission
        return Submission.objects.filter(student=self.request.user)

    def form_valid(self, form):
        form.instance.last_edited_at = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("assignments:assignment_list")

# Student: delete submission
class SubmissionDeleteView(LoginRequiredMixin, DeleteView):
    model = Submission
    template_name = "assignments/submission_confirm_delete.html"
    success_url = reverse_lazy("assignments:assignment_list")

    def get_queryset(self):
        return Submission.objects.filter(student=self.request.user)


#Can view all submissions, give rating and feedback.
class SubmissionFeedbackUpdateView(LoginRequiredMixin, UpdateView):
    model = Submission
    form_class = SubmissionFeedbackForm
    template_name = "assignments/submission_feedback_form.html"

    def get_queryset(self):
        # Only admin or teacher
        return Submission.objects.all()

    def form_valid(self, form):
        form.instance.rated_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("assignments:assignment_list")

class SubmissionDetailView(LoginRequiredMixin, DetailView):
    model = Submission
    template_name = "assignments/submission_detail.html"
    context_object_name = "submission"

