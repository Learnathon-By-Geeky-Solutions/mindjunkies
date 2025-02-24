from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from .forms import LectureForm, LecturePDFForm
from .models import Lecture
from courses.models import Course
from django.views.decorators.http import require_http_methods


@login_required
@require_http_methods(["POST", "GET"])  # Allow both GET & POST
def create_lecture(request: HttpRequest) -> HttpResponse:
    slug = request.GET.get('slug')
    form = LecturePDFForm(request.POST or None, request.FILES)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(f'{reverse("lecture_home")}?slug={slug}')
    return render(request, "lecture/create_form.html", {"form": form, 'form_type': 'pdf'})


@require_http_methods(["GET"])
def lecture_home(request: HttpRequest) -> HttpResponse:
    """View to show Lecture details."""

    slug = request.GET.get('slug')  # Get the slug from the query parameter

    course = get_object_or_404(Courses, slug=slug)
    lectures = Lecture.objects.filter(course=course).prefetch_related('pdf_files')

    return render(request, 'lecture/index.html', {
        'course': course,
        'lectures': lectures
    })


@login_required
@require_http_methods(["POST", "GET"])
def create_title(request: HttpRequest) -> HttpResponse:
    """
    Handles Lecture creation (title).
    """
    slug = request.GET.get('slug')
    form = LectureForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(f'{reverse("lecture_home")}?slug={slug}')
    return render(request, "lecture/create_form.html", {"form": form, 'form_type': 'lecture'})
