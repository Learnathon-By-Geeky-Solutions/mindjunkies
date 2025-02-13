from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from .forms import LectureForm, LecturePDFForm
from .models import Lecture
from classrooms.models import Classroom
from django.views.decorators.http import require_POST

@login_required
def handle_lecture_form(request: HttpRequest, form_type: str) -> HttpResponse:
    """
    Handles both Lecture creation (title) and PDF upload based on form_type passed.
    """
    slug = request.GET.get('slug')
    form = None

    # Select the correct form based on form_type
    if form_type == 'lecture':
        form = LectureForm(request.POST or None)
    elif form_type == 'pdf':
        form = LecturePDFForm(request.POST or None, request.FILES)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(f'{reverse("lecture_home")}?slug={slug}')

    return render(request, "lecture/create_form.html", {"form": form, 'form_type': form_type})


@login_required
def create_lecture(request: HttpRequest) -> HttpResponse:
    """
    Handles the PDF upload.
    """
    if request.method == "POST":
        return handle_lecture_form(request, 'pdf')

    # For GET request, just show the form
    return render(request, "lecture/create_form.html", {"form": LecturePDFForm(), 'form_type': 'pdf'})


@login_required
def create_title(request: HttpRequest) -> HttpResponse:
    """
    Handles the lecture title creation.
    """
    if request.method == "POST":
        return handle_lecture_form(request, 'lecture')

    # For GET request, just show the form
    return render(request, "lecture/create_form.html", {"form": LectureForm(), 'form_type': 'lecture'})


@require_POST
def lecture_home(request: HttpRequest) -> HttpResponse:
    """View to show Lecture details."""
    slug = request.GET.get('slug')
    classroom = get_object_or_404(Classroom, slug=slug)
    lectures = Lecture.objects.filter(classroom=classroom).prefetch_related('pdf_files')

    return render(request, 'lecture/index.html', {
        'classroom': classroom,
        'lectures': lectures
    })
