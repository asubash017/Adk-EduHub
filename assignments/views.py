from django.utils import timezone
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Assignment
from .forms import AssignmentForm, StudentAssignmentForm

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
class AssignmentListView(LoginRequiredMixin, ListView):
    model = Assignment
    template_name = "assignments/assignment_list.html"
    context_object_name = "assignments"

    def get_queryset(self):
        # Everyone can view all assignments per spec.
        return (
            Assignment.objects.select_related("course", "uploaded_by", "last_edited_by")
            .all()
        )


class AssignmentDetailView(LoginRequiredMixin, DetailView):
    model = Assignment
    template_name = "assignments/assignment_detail.html"
    context_object_name = "assignment"


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
