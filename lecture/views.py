from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from .forms import LectureForm, LecturePDFForm,LectureVideoForm
from .models import Lecture,LectureVideo
from courses.models import Courses
from django.views.decorators.http import require_http_methods
from django.http import FileResponse
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest

def validate_file(file, type):
    """Validate file based on slug type."""
    if type == "video":
        allowed_extensions = ['.mp4', '.avi', '.mov', '.mkv']
        if not any(file.name.endswith(ext) for ext in allowed_extensions):
            raise ValidationError("Only video files (MP4, AVI, MOV, MKV) are allowed.")
    elif type == "pdf":
        if not file.name.endswith('.pdf'):
            raise ValidationError("Only PDF files are allowed.")
    else:
        raise ValidationError("Invalid upload type.")
    
@login_required
@require_http_methods(["POST", "GET"])  # Allow both GET & POST
def create_content(request: HttpRequest) -> HttpResponse:
    type = request.GET.get('type')
    slug = request.GET.get('slug')
    print(type)
    
    # Select the appropriate form based on slug
    form_class = LecturePDFForm if type == "pdf" else LectureVideoForm if type == "video" else None
    
    if not form_class:
        return HttpResponseBadRequest("Invalid content type.")
    
    form = form_class(request.POST, request.FILES)
    print(request.FILES)
    
    if request.method == "POST" and form.is_valid():
        # Get the file based on type
        file_field = 'pdf_file' if type == 'pdf' else 'video_file'
        file = request.FILES.get(file_field)
        
        try:
            validate_file(file, type)  # Validate file type
            form.save()  # Save the form instance (assuming it saves the file as well)
            return redirect(f'{reverse("lecture_home")}?slug={slug}')
        except ValidationError as e:
            form.add_error(file_field, e)  # Add validation error to the respective field
    
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

   