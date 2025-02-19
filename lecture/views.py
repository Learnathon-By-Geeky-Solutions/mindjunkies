from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from .forms import LectureForm, LecturePDFForm
from .models import Lecture,LectureVideo
from courses.models import Courses
from django.views.decorators.http import require_http_methods
from django.http import FileResponse


@login_required
@require_http_methods(["POST", "GET"])  # Allow both GET & POST
def create_content(request: HttpRequest) -> HttpResponse:
    slug = request.GET.get('slug')
    form = LecturePDFForm(request.POST or None, request.FILES)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(f'{reverse("lecture_home")}?slug={slug}')
    return render(request, "lecture/create_form.html", {"form": form, 'form_type': 'content'})


@require_http_methods(["GET"])
def lecture_home(request: HttpRequest) -> HttpResponse:
    """View to show Lecture details."""

    slug = request.GET.get('slug')  # Get the slug from the query parameter

    course = get_object_or_404(Courses, slug=slug)
    lectures = Lecture.objects.filter(course=course).prefetch_related('pdf_files')

    return render(request, 'lecture/index.html', {
        'course': course,
        'lectures': lectures,
        'type':"pdf"
    })


@login_required
@require_http_methods(["POST", "GET"])
def create_module(request: HttpRequest) -> HttpResponse:
    """
    Handles module creation (title).
    """
    slug = request.GET.get('slug')
    course_instance = Courses.objects.get(slug=slug)
    form = LectureForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        module_instance=form.save(commit=False)
        module_instance.course=course_instance
        module_instance.save()
        return redirect(f'{reverse("lecture_home")}?slug={slug}')
    return render(request, "lecture/create_form.html", {"form": form, 'form_type': 'module'})


def lecture_video_content(request):
    """View to show Lecture details."""
    slug = request.GET.get('slug')  # Get the slug from the query parameter

    course = get_object_or_404(Courses, slug=slug)
    lectures = Lecture.objects.filter(course=course).prefetch_related('video_files')

    return render(request, 'lecture/video_content.html', {
        'course': course,
        'lectures': lectures,
        'type': "video"
    })

def stream_video(request, video_id):
    """ Serve video files in-browser instead of forcing download """
    video = get_object_or_404(LectureVideo, id=video_id)
    response = FileResponse(video.video_file.open(), content_type='video/mp4')
    response['Content-Disposition'] = 'inline'  # Forces browser to play instead of download
    return response

   