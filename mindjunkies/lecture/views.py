from datetime import timedelta
from typing import Tuple

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.timezone import localtime, now
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView

from mindjunkies.courses.models import Course, Module, CourseToken

from .forms import LectureForm, LecturePDFForm, LectureVideoForm, ModuleForm
from .models import Lecture, LectureCompletion, LecturePDF, LectureVideo, LastVisitedModule


# Utility functions to reduce complexity
def get_today_range() -> Tuple[timezone.datetime, timezone.datetime]:
    """Get the start and end of the current day."""
    today = localtime(now())
    start = today.replace(hour=0, minute=0, second=0, microsecond=0)
    end = today.replace(hour=23, minute=59, second=59, microsecond=999999)
    return start, end


def get_this_week_range() -> Tuple[timezone.datetime, timezone.datetime]:
    """Get the start and end of the current week."""
    today = localtime(now())
    start = today - timedelta(days=today.weekday())
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=6, hours=23, minutes=59, seconds=59, microseconds=999999)
    return start, end


def check_course_enrollment(user, course):
    """Check if a user is enrolled in a course or is staff."""
    try:
        course_token = CourseToken.objects.get(course=course)
        return course_token.status == "approved"
    except CourseToken.DoesNotExist:
        return False


def is_teacher_for_course(user, course):
    """Check if user is a teacher for the course."""
    return course.teacher == user


def get_current_live_class(course):
    """Get the current live class if one is in progress."""
    now_time = timezone.now()
    for live_class in course.live_classes.all():
        end_time = live_class.scheduled_at + timedelta(minutes=live_class.duration)
        if live_class.scheduled_at <= now_time <= end_time:
            return live_class
    return None


class LectureHomeView(LoginRequiredMixin, TemplateView):
    template_name = "lecture/lecture_home.html"

    def get_course(self):
        return get_object_or_404(Course, slug=self.kwargs["course_slug"])

    def get_current_module(self, course):
        module_id = self.request.GET.get("module_id")
        if module_id:
            return get_object_or_404(Module, id=module_id)
        return course.modules.first()

    def check_course_enrollment(self, course):
        """Check if the user is enrolled in the course."""
        if course.teacher == self.request.user:
            course_token = CourseToken.objects.get(course=course)
            if course_token.status == "approved":
                return True
            return False
        return self.request.user.is_staff or course.enrollments.filter(student=self.request.user,
                                                                       status='active').exists()

    def dispatch(self, request, *args, **kwargs):
        course = self.get_course()
        if not self.check_course_enrollment(course):
            if course.teacher == request.user:
                messages.error(request, "Your course is not approved yet.")
            else:
                messages.error(request, "You are not enrolled in this course.")
            return redirect("course_details", slug=course.slug)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_course()
        today_start, today_end = get_today_range()
        week_start, week_end = get_this_week_range()

        # Use cached queryset to avoid repeating filters
        live_classes_today = list(
            course.live_classes.filter(
                scheduled_at__range=(today_start, today_end)
            ).
            order_by("scheduled_at")
        )
        live_classes_this_week = list(
            course.live_classes.filter(
                scheduled_at__range=(week_start, week_end)
            ).exclude(
                scheduled_at__range=(today_start, today_end)
            ).order_by("scheduled_at")
        )

        context.update({
            "course": course,
            "modules": course.modules.all(),
            "current_module": self.get_current_module(course),
            "isTeacher": is_teacher_for_course(self.request.user, course),
            "current_live_class": get_current_live_class(course),
            "todays_live_classes": live_classes_today,
            "this_weeks_live_classes": live_classes_this_week,
        })
        return context


@login_required
@require_http_methods(["GET"])
def lecture_video(request: HttpRequest, course_slug: str, module_id: str, lecture_id, video_id) -> HttpResponse:
    """View to display a lecture video."""
    video = get_object_or_404(LectureVideo, id=video_id)
    module = get_object_or_404(Module, id=module_id)
    lecture = get_object_or_404(Lecture, id=lecture_id)

    # Update last visited module
    LastVisitedModule.objects.update_or_create(
        user=request.user, module=module, lecture=lecture,
        defaults={"last_visited": timezone.now()}
    )

    # Ensure the user is enrolled in the related course
    if not check_course_enrollment(request.user, video.lecture.course):
        return HttpResponseForbidden("You are not enrolled in this course.")

    context = {
        "course": video.lecture.course,
        "video": video,
        "module": module,
        "lecture": lecture,
        "hls_url": video.video_file.url,
    }

    return render(request, "lecture/lecture_video.html", context)


@login_required
@require_http_methods(["GET"])
def lecture_pdf(request: HttpRequest, course_slug: str, module_id: int, lecture_id: int, pdf_id: int) -> HttpResponse:
    """View to display a lecture PDF."""
    pdf = get_object_or_404(LecturePDF, id=pdf_id)
    if not pdf.pdf_file:
        messages.error(request, "The requested PDF file is not available.")
        return redirect("lecture_home", course_slug=course_slug)
    lecture = get_object_or_404(Lecture, id=lecture_id)
    course = get_object_or_404(Course, slug=course_slug)
    module = get_object_or_404(Module, id=module_id)

    context = {"course": course, "pdf": pdf, "module": module, "lecture": lecture, }
    return render(request, "lecture/lecture_pdf.html", context)


class CourseObjectMixin:
    """Mixin to get course and check permissions."""

    def get_course(self):
        return get_object_or_404(Course, slug=self.kwargs["course_slug"])


class LectureFormMixin:
    """Mixin for common lecture form handling."""

    def handle_form_validation(self, form, success_message):
        """Common form validation handling."""
        try:
            saved_instance = form.save()
            messages.success(self.request, success_message)
            return self.get_success_url(saved_instance)
        except (ValidationError, IntegrityError) as e:
            error_message = "Order number already exists" if isinstance(e, IntegrityError) else str(e)
            messages.error(self.request, error_message)
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error processing the form. Please check the fields below.",
        )
        return self.render_to_response(self.get_context_data(form=form))


@method_decorator(csrf_protect, name="dispatch")
class CreateLectureView(LoginRequiredMixin, CourseObjectMixin, LectureFormMixin, CreateView):
    model = Lecture
    form_class = LectureForm
    template_name = "lecture/create_lecture.html"

    def dispatch(self, request, *args, **kwargs):
        self.module = get_object_or_404(Module, id=self.kwargs["module_id"])
        self.course = self.get_course()
        if not is_teacher_for_course(request.user, self.course):
            return HttpResponseForbidden("You are not allowed to create a lecture for this course.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Assign the lecture to the appropriate course"""
        saved_lecture = form.save(commit=False)
        saved_lecture.course = self.course
        saved_lecture.module = self.module

        return self.handle_form_validation(
            form,
            "Lecture created successfully!"
        )

    def get_success_url(self, instance):
        return redirect(
            f"{reverse('lecture_home', kwargs={'course_slug': self.course.slug})}?module_id={self.module.id}"
        )

    def get_context_data(self, **kwargs):
        """Pass the course to the template context"""
        context = super().get_context_data(**kwargs)
        context["course"] = self.course
        return context


class CreateContentView(LoginRequiredMixin, CourseObjectMixin, LectureFormMixin, FormView):
    template_name = "lecture/create_content.html"

    def dispatch(self, request, *args, **kwargs):
        self.lecture = get_object_or_404(Lecture, id=kwargs["lecture_id"])
        self.course = self.get_course()


    def get_form_class(self):
        content_type = self.kwargs.get("format")
        if content_type == "attachment":
            return LecturePDFForm
        elif content_type == "video":
            return LectureVideoForm
        else:
            raise ValueError("Invalid content type specified.")

    def form_valid(self, form):
        saved_content = form.save(commit=False)
        saved_content.lecture = self.lecture
        saved_content.save()

        messages.success(
            self.request,
            f"Lecture {self.kwargs['format'].capitalize()} uploaded successfully!",
        )
        return redirect("lecture_home", course_slug=self.kwargs["course_slug"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content_type"] = self.kwargs["format"]
        context["course"] = self.get_course()
        return context


class EditLectureView(LoginRequiredMixin, CourseObjectMixin, LectureFormMixin, UpdateView):
    model = Lecture
    form_class = LectureForm
    template_name = "lecture/create_lecture.html"

    def dispatch(self, request, *args, **kwargs):
        self.course = self.get_course()
        if not is_teacher_for_course(request.user, self.course):
            return HttpResponseForbidden("You are not allowed to edit this lecture.")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """Get the lecture object based on the slug from the URL"""
        lecture_id = self.kwargs.get("lecture_id")
        return get_object_or_404(Lecture, id=lecture_id)

    def form_valid(self, form):
        """If the form is valid, save the lecture and redirect"""
        return self.handle_form_validation(
            form,
            "Lecture saved successfully!"
        )

    def get_success_url(self, instance):
        return redirect("lecture_home", course_slug=self.kwargs["course_slug"])

    def get_context_data(self, **kwargs):
        """Add extra context, such as the lecture object"""
        context = super().get_context_data(**kwargs)
        context["lecture"] = self.get_object()
        context["course"] = self.get_course()
        return context


class CreateModuleView(LoginRequiredMixin, CourseObjectMixin, LectureFormMixin, CreateView):
    model = Module
    form_class = ModuleForm
    template_name = "lecture/create_module.html"

    def dispatch(self, request, *args, **kwargs):
        self.course = self.get_course()

        if not is_teacher_for_course(request.user, self.course):
            return HttpResponseForbidden("You are not allowed to edit this lecture.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Assign the module to the correct course before saving"""
        instance = form.save(commit=False)
        instance.course = self.course

        return self.handle_form_validation(
            form,
            "Module created successfully!"
        )

    def get_success_url(self, instance):
        return redirect(
            reverse("lecture_home", kwargs={"course_slug": self.course.slug})
        )

    def get_context_data(self, **kwargs):
        """Pass the course to the template for context"""
        context = super().get_context_data(**kwargs)
        context["course"] = self.get_course()
        return context


class DeleteLectureView(LoginRequiredMixin, CourseObjectMixin, View):
    """View to delete a lecture."""

    def get(self, request, course_slug, lecture_id):
        """Handle GET request to delete a lecture."""
        lecture = get_object_or_404(Lecture, id=lecture_id)
        if not is_teacher_for_course(request.user, lecture.course):
            return HttpResponseForbidden("You are not allowed to delete this lecture.")

        # Delete the lecture and redirect
        lecture.delete()
        messages.success(request, "Lecture deleted successfully.")
        return redirect(reverse("lecture_home", kwargs={"course_slug": course_slug}))


class MarkLectureCompleteView(LoginRequiredMixin, View):
    def get(self, request, course_slug, lecture_id):
        lecture = get_object_or_404(Lecture, id=lecture_id)
        LectureCompletion.objects.get_or_create(user=request.user, lecture=lecture)
        return redirect("lecture_home", course_slug=course_slug)


class ModuleEditView(LoginRequiredMixin, CourseObjectMixin, LectureFormMixin, UpdateView):
    model = Module
    form_class = ModuleForm
    template_name = "lecture/create_module.html"

    def dispatch(self, request, *args, **kwargs):
        self.course = self.get_course()
        if not is_teacher_for_course(request.user, self.course):
            return HttpResponseForbidden("You are not allowed to edit a module for this course.")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """Get the module object based on the slug from the URL"""
        module_id = self.kwargs.get("module_id")
        return get_object_or_404(Module, id=module_id)

    def form_valid(self, form):
        """If the form is valid, save the module and redirect"""
        return self.handle_form_validation(
            form,
            "Module saved successfully!"
        )

    def get_success_url(self, instance):
        return redirect("lecture_home", course_slug=self.kwargs["course_slug"])

    def get_context_data(self, **kwargs):
        """Add extra context, such as the module object"""
        context = super().get_context_data(**kwargs)
        context["module"] = self.get_object()
        context["course"] = self.get_course()
        return context


class DeleteModuleView(LoginRequiredMixin, CourseObjectMixin, View):
    def get(self, request, course_slug, module_id):
        module = get_object_or_404(Module, id=module_id)
        if not is_teacher_for_course(request.user, module.course):
            return HttpResponseForbidden("You are not allowed to delete this module.")

        # Delete the module and redirect
        module.delete()
        messages.success(request, "Module deleted successfully.")
        return redirect(reverse("lecture_home", kwargs={"course_slug": course_slug}))
