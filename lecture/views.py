import os
import mimetypes
from django.utils.encoding import smart_str
from django.conf import settings


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView,FormView,UpdateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.http import FileResponse, HttpRequest, HttpResponse, HttpResponseForbidden, Http404
from .forms import LectureForm, LecturePDFForm, ModuleForm, LectureVideoForm
from courses.models import Course, Module
from .models import Lecture, LectureVideo, LecturePDF

@login_required
@require_http_methods(["GET"])
def lecture_home(request: HttpRequest, course_slug: str) -> HttpResponse:
    """View to show lectures for a course."""
    course = get_object_or_404(Course, slug=course_slug)

    teacher = request.user.is_staff or course.teachers.filter(teacher=request.user).exists()

    module_id = request.GET.get("module_id")
    if module_id:
        current_module = get_object_or_404(Module, id=module_id)
    else:
        current_module = course.modules.first()

    if not current_module:
        messages.warning(request, "No lectures available for this course.")

 
    context = {
        "course": course,
        "modules": course.modules.all(),
        "current_module": current_module,
        "isTeacher": teacher,
    }

    return render(request, "lecture/lecture_home.html", context)

@require_http_methods(["GET"])
def serve_hls_playlist(request, course_slug, video_id):
    try:
        video = get_object_or_404(LectureVideo, pk=video_id)
        hls_playlist_path = video.hls

        if not os.path.exists(hls_playlist_path) or not os.path.abspath(hls_playlist_path).startswith(settings.MEDIA_ROOT):
            return HttpResponse("Invalid file path", status=400)

        with open(hls_playlist_path, 'r', encoding='utf-8') as m3u8_file:
            m3u8_content = m3u8_file.read()

        base_url = request.build_absolute_uri('/') + 'courses'
        serve_hls_segment_url = base_url + f"/{course_slug}/serve_hls_segment/" + str(video_id)
        m3u8_content = m3u8_content.replace('{{ dynamic_path }}', serve_hls_segment_url)

        response = HttpResponse(m3u8_content, content_type='application/vnd.apple.mpegurl')
        response["X-Content-Type-Options"] = "nosniff"
        return response
    except (LectureVideo.DoesNotExist, FileNotFoundError):
        return HttpResponse("Video or HLS playlist not found", status=404)

@require_http_methods(["GET"])
def serve_hls_segment(request, course_slug, video_id, segment_name):
    print("hello world")

    try:
        video = get_object_or_404(LectureVideo, pk=video_id)
        hls_directory = os.path.join(os.path.dirname(video.video_file.path), 'hls_output')
        # Validate and sanitize segment name
        safe_segment_name = os.path.basename(segment_name)  
        segment_path = os.path.join(hls_directory, safe_segment_name)

        print("Segment path:", segment_path)

        if not segment_path.startswith(hls_directory):
            return HttpResponseForbidden("Access denied")

        if not os.path.exists(segment_path):
            return HttpResponse("Video or HLS segment not found", status=404)
        

        content_type, _ = mimetypes.guess_type(segment_path)
        content_type = content_type or 'application/octet-stream'

        # Serve the HLS segment as a binary file response
        response = FileResponse(open(segment_path, 'rb'), content_type=content_type)
        response['Content-Disposition'] = f'inline; filename="{smart_str(safe_segment_name)}"'
        return response
    
    except LectureVideo.DoesNotExist:
        return HttpResponse("Video not found", status=404)
    except FileNotFoundError:
        return HttpResponse("Segment file not found", status=404)
    except ValueError as e:
        return HttpResponse(f"Error: {str(e)}", status=500)


@login_required
@require_http_methods(["GET"])
def lecture_video(request: HttpRequest, course_slug: str, module_id: str, video_id) -> HttpResponse:
    """View to display a lecture video."""

    # Get the video or return 404 if not found
    video = get_object_or_404(LectureVideo, id=video_id)
    module = Module.objects.get(id=module_id)
    # Ensure the user is enrolled in the related course
    if not request.user.is_staff and not video.lecture.course.enrollments.filter(student=request.user).exists():
        return HttpResponseForbidden("You are not enrolled in this course.")

    hls_playlist_url = reverse('serve_hls_playlist', args=[course_slug, video_id])

    context = {
        "course": video.lecture.course,
        "video": video,
        "module": module,
        "hls_url": hls_playlist_url,
    }

    return render(request, "lecture/lecture_video.html", context)


@login_required
@require_http_methods(["GET"])
def lecture_pdf(request: HttpRequest, slug: str, pdf_id: int) -> HttpResponse:
    """View to display a lecture video."""

    # Get the pdf or return 404 if not found
    pdf = get_object_or_404(LecturePDF, id=pdf_id)
    lecture = Lecture.objects.get(slug=slug)

    # Ensure the user is enrolled in the related course

    context = {
        "pdf": pdf,
        "lecture": lecture

    }

    return render(request, "lecture/lecture_pdf.html", context)

@method_decorator(csrf_protect, name="dispatch")  # Protects against CSRF attacks
class CreateLectureView(LoginRequiredMixin, CreateView):
    model = Lecture
    form_class = LectureForm
    template_name = "lecture/create_lecture.html"

    def dispatch(self, request, *args, **kwargs):
        """ Ensure the course exists before proceeding """
        self.course = get_object_or_404(Course, slug=self.kwargs["course_slug"])
        self.module=get_object_or_404(Module,id=self.kwargs["module_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """ Assign the lecture to the appropriate course """
        saved_lecture = form.save(commit=False)
        saved_lecture.course = self.course # Associate lecture with the course
        saved_lecture.module=self.module# Associate lecture with the module
        saved_lecture.save()
        messages.success(self.request, "Lecture created successfully!")
        return redirect(f"{reverse('lecture_home', kwargs={'course_slug': self.course.slug})}?module_id={self.module.id}")

    def form_invalid(self, form):
        messages.error(self.request, "There was an error processing the form. Please check the fields below.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        """ Pass the course to the template context """
        context = super().get_context_data(**kwargs)
        context["course"] = self.course
        return context

class CreateContentView(LoginRequiredMixin, FormView):
    template_name = "lecture/create_content.html"

    def get_form_class(self):
        """ Dynamically choose the form based on the 'type' parameter """
        content_type = self.kwargs.get('format')
        if content_type == "attachment":
            return LecturePDFForm
        elif content_type == "video":
            return LectureVideoForm
        else:
            messages.error(self.request, "Invalid content type specified.")
            return redirect("lecture_home", course_slug=self.kwargs["course_slug"])

    def dispatch(self, request, *args, **kwargs):
        """ Ensure the lecture exists before proceeding """
        self.lecture = get_object_or_404(Lecture, slug=self.kwargs["lecture_slug"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """ Save the content, attach it to the lecture, and show success message """
        saved_content = form.save(commit=False)
        saved_content.lecture = self.lecture
        saved_content.save()
        messages.success(self.request, f"Lecture {self.kwargs['format'].capitalize()} uploaded successfully!")
        return redirect("lecture_home", course_slug=self.kwargs["course_slug"])

    def form_invalid(self, form):
        """ Display errors if the form is invalid """
        messages.error(self.request, "There was an error processing the form. Please check the fields below.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        """ Add additional context to the template """
        context = super().get_context_data(**kwargs)
        context["content_type"] = self.kwargs["format"]
        return context
    

class EditLectureView(LoginRequiredMixin, UpdateView):
    model = Lecture
    form_class = LectureForm
    template_name = "lecture/create_lecture.html"

    def get_object(self):
        """ Get the lecture object based on the slug from the URL """
        lecture_slug = self.kwargs.get("lecture_slug")
        return get_object_or_404(Lecture, slug=lecture_slug)

    def form_valid(self, form):
        """ If the form is valid, save the lecture and redirect """
        form.save()
        messages.success(self.request, "Lecture saved successfully!")
        return redirect("lecture_home", slug=self.kwargs["course_slug"])

    def form_invalid(self, form):
        """ If the form is invalid, display errors and stay on the form page """
        messages.error(self.request, f"There was an error processing the form: {form.errors}")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        """ Add extra context, such as the lecture object """
        context = super().get_context_data(**kwargs)
        lecture_slug = self.kwargs.get("lecture_slug")
        lecture = get_object_or_404(Lecture, slug=lecture_slug)
        context["lecture"] = lecture
        return context



class CreateModuleView(LoginRequiredMixin, CreateView):
    model = Module
    form_class = ModuleForm
    template_name = "lecture/create_module.html"

    def dispatch(self, request, *args, **kwargs):
        """Ensure the course exists before proceeding"""
        self.course = get_object_or_404(Course, slug=self.kwargs["course_slug"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Assign the module to the correct course before saving"""
        instance = form.save(commit=False)
        instance.course = self.course
        instance.save()
        messages.success(self.request, "Module created successfully!")
        return redirect(reverse("lecture_home", kwargs={"course_slug": self.course.slug}))

    def get_context_data(self, **kwargs):
        """Pass the course to the template for context"""
        context = super().get_context_data(**kwargs)
        context["course"] = self.course
        return context





