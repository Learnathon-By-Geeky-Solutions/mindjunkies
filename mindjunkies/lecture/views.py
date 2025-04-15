from datetime import timedelta
from typing import Tuple

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.timezone import localtime, now
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView

from mindjunkies.courses.models import Course, Module

from .forms import LectureForm, LecturePDFForm, LectureVideoForm, ModuleForm
from .models import Lecture, LecturePDF, LectureVideo, LectureCompletion, LastVisitedModule
from django.utils.timezone import localtime, now
from django.views.generic import TemplateView
from django.views import View


class LectureHomeView(LoginRequiredMixin, TemplateView):
    template_name = "lecture/lecture_home.html"

    def get_course(self):
        return get_object_or_404(Course, slug=self.kwargs["course_slug"])

    def get_is_teacher(self, course):
        return self.request.user.is_staff or course.teacher == self.request.user

    def get_today_range(self) -> Tuple[timezone.datetime, timezone.datetime]:
        today = localtime(now())
        start = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end = today.replace(hour=23, minute=59, second=59, microsecond=999999)
        return start, end

    def get_current_module(self, course):
        module_id = self.request.GET.get("module_id")
        if module_id:
            return get_object_or_404(Module, id=module_id)
        return course.modules.first()

    def get_current_live_class(self, course):
        now_time = timezone.now()
        for live_class in course.live_classes.all():
            end_time = live_class.scheduled_at + timedelta(minutes=live_class.duration)
            if live_class.scheduled_at <= now_time <= end_time:
                return live_class
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_course()
        is_teacher = self.get_is_teacher(course)
        today_start, today_end = self.get_today_range()

        # Use cached queryset to avoid repeating filters
        live_classes_today = list(
            course.live_classes.filter(
                scheduled_at__range=(today_start, today_end)
            ).order_by("scheduled_at")
        )

        current_live_class = self.get_current_live_class(course)
        current_module = self.get_current_module(course)

        context.update(
            {
                "course": course,
                "modules": course.modules.all(),
                "current_module": current_module,
                "isTeacher": is_teacher,
                "current_live_class": current_live_class,
                "todays_live_classes": live_classes_today,
            }
        )
        return context


def check_course_enrollment(user, course):
    """Check if a user is enrolled in a course or is staff."""
    return user.is_staff or course.enrollments.filter(student=user).exists()


@login_required
@require_http_methods(["GET"])
def lecture_video(request: HttpRequest, course_slug: str, module_id: str, lecture_id, video_id) -> HttpResponse:
    """View to display a lecture video."""
    video = get_object_or_404(LectureVideo, id=video_id)
    module = get_object_or_404(Module, id=module_id)
    lecture = get_object_or_404(Lecture, id=lecture_id)

    LastVisitedModule.objects.update_or_create(
        user=request.user, module=module, lecture=lecture, defaults={"last_visited": timezone.now()}
    )



    # Ensure the user is enrolled in the related course
    if not check_course_enrollment(request.user, video.lecture.course):
        return HttpResponseForbidden("You are not enrolled in this course.")

    context = {
        "course": video.lecture.course,
        "video": video,
        "module": module,
        "hls_url": video.video_file.url,
    }

    return render(request, "lecture/lecture_video.html", context)


@login_required
@require_http_methods(["GET"])
def lecture_pdf(request: HttpRequest, course_slug: str, lecture_id: int, pdf_id: int) -> HttpResponse:
    """View to display a lecture PDF."""
    pdf = get_object_or_404(LecturePDF, id=pdf_id)
    lecture = get_object_or_404(Lecture, id=lecture_id)
    course = get_object_or_404(Course, slug=course_slug)

    context = {"course": course, "pdf": pdf, "lecture": lecture}
    return render(request, "lecture/lecture_pdf.html", context)


class CourseObjectMixin:
    """Mixin to get course and check permissions."""

    def get_course(self):
        return get_object_or_404(Course, slug=self.kwargs["course_slug"])


@method_decorator(csrf_protect, name="dispatch")
class CreateLectureView(LoginRequiredMixin, CourseObjectMixin, CreateView):
    model = Lecture
    form_class = LectureForm
    template_name = "lecture/create_lecture.html"

    def dispatch(self, request, *args, **kwargs):
        """Ensure the course exists before proceeding"""
        self.module = get_object_or_404(Module, id=self.kwargs["module_id"])
        self.course = self.get_course()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Assign the lecture to the appropriate course"""
        saved_lecture = form.save(commit=False)
        saved_lecture.course = self.course
        saved_lecture.module = self.module
        saved_lecture.save()
        messages.success(self.request, "Lecture created successfully!")
        return redirect(
            f"{reverse('lecture_home', kwargs={'course_slug': self.course.slug})}?module_id={self.module.id}"
        )

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error processing the form. Please check the fields below.",
        )
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        """Pass the course to the template context"""
        context = super().get_context_data(**kwargs)
        context["course"] = self.course
        return context


class CreateContentView(LoginRequiredMixin, CourseObjectMixin, FormView):
    template_name = "lecture/create_content.html"

    def dispatch(self, request, *args, **kwargs):
        self.lecture = get_object_or_404(Lecture, slug=kwargs["lecture_slug"])
        self.course = self.get_course()
        return super().dispatch(request, *args, **kwargs)

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

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error processing the form. Please check the fields below.",
        )
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content_type"] = self.kwargs["format"]
        context["course"] = self.get_course()
        return context


class EditLectureView(LoginRequiredMixin, CourseObjectMixin, UpdateView):
    model = Lecture
    form_class = LectureForm
    template_name = "lecture/create_lecture.html"

    def get_object(self, queryset=None):
        """Get the lecture object based on the slug from the URL"""
        lecture_slug = self.kwargs.get("lecture_slug")
        return get_object_or_404(Lecture, slug=lecture_slug)

    def form_valid(self, form):
        """If the form is valid, save the lecture and redirect"""
        form.save()
        messages.success(self.request, "Lecture saved successfully!")
        return redirect("lecture_home", course_slug=self.kwargs["course_slug"])

    def form_invalid(self, form):
        """If the form is invalid, display errors and stay on the form page"""
        messages.error(
            self.request, f"There was an error processing the form: {form.errors}"
        )
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        """Add extra context, such as the lecture object"""
        context = super().get_context_data(**kwargs)
        context["lecture"] = self.get_object()
        context["course"] = self.get_course()
        return context


class CreateModuleView(LoginRequiredMixin, CourseObjectMixin, CreateView):
    model = Module
    form_class = ModuleForm
    template_name = "lecture/create_module.html"

    def dispatch(self, request, *args, **kwargs):
        """Ensure the course exists before proceeding"""
        self.course = self.get_course()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Assign the module to the correct course before saving"""
        instance = form.save(commit=False)
        instance.course = self.course
        instance.save()
        messages.success(self.request, "Module created successfully!")
        return redirect(
            reverse("lecture_home", kwargs={"course_slug": self.course.slug})
        )

    def get_context_data(self, **kwargs):
        """Pass the course to the template for context"""
        context = super().get_context_data(**kwargs)
        context["course"] = self.course
        return context


class MarkLectureCompleteView(LoginRequiredMixin, View):
    def get(self, request, course_slug, lecture_id):
        lecture = get_object_or_404(Lecture, id=lecture_id)
        LectureCompletion.objects.get_or_create(user=request.user, lecture=lecture)
        return redirect(request.META.get('HTTP_REFERER', '/'))
