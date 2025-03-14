from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic.edit import CreateView, UpdateView

from .forms import CourseForm
from .models import Course, CourseTeacher, Enrollment


@require_http_methods(["GET"])
def course_list(request: HttpRequest) -> HttpResponse:
    """View to show all courses."""
    courses = Course.objects.all()
    enrolled_classes = []
    teacher_classes = []
    role = None
    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(student=request.user)
        enrolled_classes = [ec.course for ec in enrolled]
        teaching = CourseTeacher.objects.filter(teacher=request.user)
        teacher_classes = [ec.course for ec in teaching]

    print(teacher_classes)

    context = {
        "courses": courses,
        "enrolled_classes": enrolled_classes,
        "teacher_classes": teacher_classes,
        "role": role,
    }
    return render(request, "courses/course_list.html", context)


class CreateCourseView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/create_course.html"

    def form_valid(self, form):
        saved_course = form.save()
        # LoginRequiredMixin ensures that the user is authenticated
        CourseTeacher.objects.create(course=saved_course, teacher=self.request.user)
        messages.success(self.request, "Course saved successfully!")
        return redirect(reverse("course_details", kwargs={"slug": saved_course.slug}))

    def form_invalid(self, form):
        messages.error(
            self.request, f"There was an error processing the form: {form.errors}"
        )
        return self.render_to_response(self.get_context_data(form=form))


class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/create_course.html"
    context_object_name = "course"

    def get_object(self, queryset=None):
        slug = self.request.GET.get("slug")
        return get_object_or_404(Course, slug=slug) if slug else None

    def form_valid(self, form):
        messages.success(self.request, "Course saved successfully!")
        return redirect(reverse("course_details", kwargs={"slug": form.instance.slug}))

    def form_invalid(self, form):
        print("Form errors:", form.errors)  # Log the errors to the console
        messages.error(
            self.request, f"There was an error processing the form: {form.errors}"
        )
        return self.render_to_response(self.get_context_data(form=form))


@require_http_methods(["GET"])
def course_details(request: HttpRequest, slug: str) -> HttpResponse:
    """View to show course details."""
    course = get_object_or_404(Course, slug=slug)
    enrolled_courses = CourseTeacher.objects.get(course=course)
    course_teacher = enrolled_courses.teacher
    accessed = False
    enrolled = course.enrollments.filter(student=request.user).exists()
    if request.user == course_teacher or enrolled:
        accessed = True
    context = {
        "course_detail": course,
        "accessed": accessed,
        "instructor": course_teacher,
        "teacher": request.user == course_teacher,
    }
    return render(request, "courses/course_details.html", context)


@login_required
@require_http_methods(["GET"])
def user_course_list(request: HttpRequest) -> HttpResponse:
    teaching = CourseTeacher.objects.filter(teacher=request.user)
    courses = [ec.course for ec in teaching]

    enrolled = Enrollment.objects.filter(student=request.user)
    courses = courses + [ec.course for ec in enrolled]

    print(courses)
    print("enrolled", enrolled)

    context = {
        "courses": courses,
        "enrolled_classes": courses,
    }
    return render(request, "courses/course_list.html", context)


@login_required
@require_http_methods(["GET"])
def course_view(request: HttpRequest, slug: str) -> HttpResponse:
    print(slug)
    course = get_object_or_404(Course, slug=slug)
    context = {
        "course": course,
    }
    return render(request, "courses/course_view.html", context)
