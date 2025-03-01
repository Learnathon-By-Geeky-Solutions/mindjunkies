from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, Http404

from courses.models import Course
from .models import Lecture, LectureVideo,LecturePDF


@login_required
@require_http_methods(["GET"])
def lecture_home(request: HttpRequest, course_id: int) -> HttpResponse:
    """View to show lectures for a course."""
    
    # Get the course or return 404 if not found
    course = get_object_or_404(Course, id=course_id)
    
    # Ensure the user is enrolled in the course
    if not request.user.is_staff and not course.enrollments.filter(student=request.user).exists():
        return HttpResponseForbidden("You are not enrolled in this course.")

    # Fetch lectures for the course
    default_current_week = course.lectures.first()
    upcoming_deadlines = {}  # TODO: Add logic for upcoming deadlines

    # Get selected lecture if provided
    lecture_id = request.GET.get("lecture_id")
    current_week = Lecture.objects.filter(id=lecture_id).first() if lecture_id else default_current_week

    if not current_week:
        messages.warning(request, "No lectures available for this course.")
    
    context = {
        "course": course,
        "current_week": current_week,
        "upcoming_deadlines": upcoming_deadlines,
    }
    
    return render(request, "lecture/lecture_home.html", context)


@login_required
@require_http_methods(["GET"])
def lecture_video(request: HttpRequest, video_id: int) -> HttpResponse:
    """View to display a lecture video."""
    
    # Get the video or return 404 if not found
    video = get_object_or_404(LectureVideo, id=video_id)
    
    # Ensure the user is enrolled in the related course
    if not request.user.is_staff and not video.lecture.course.enrollments.filter(student=request.user).exists():
        return HttpResponseForbidden("You are not enrolled in this course.")

    context = {
        "video": video,
    }

    return render(request, "lecture/lecture_video.html", context)

@login_required
@require_http_methods(["GET"])
def lecture_pdf(request: HttpRequest, pdf_id: int) -> HttpResponse:
    """View to display a lecture video."""
    
    # Get the pdf or return 404 if not found
    pdf = get_object_or_404(LecturePDF, id=pdf_id)
    
    # Ensure the user is enrolled in the related course
    print(pdf.pdf_file.url)

    context = {
        "pdf": pdf,
    }

    return render(request, "lecture/lecture_pdf.html", context)
