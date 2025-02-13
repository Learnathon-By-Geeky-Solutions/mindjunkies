from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from .forms import LectureForm, LecturePDFForm
from .models import Lecture
from classrooms.models import Classroom
from django.views.decorators.http import require_http_methods

@login_required
def handle_lecture_form(request: HttpRequest, form_type: str) -> HttpResponse:
    """
    Handles both Lecture creation (title) and PDF upload based on form_type passed.
    """
    slug = request.GET.get('slug')
    # Select the correct form based on the form_type
    if form_type == 'lecture':
        form = LectureForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            form.save()
            return redirect(f'{reverse("lecture_home")}?slug={slug}')  # Redirect after creating lecture title

    elif form_type == 'pdf':
        form = LecturePDFForm(request.POST or None, request.FILES)
        if request.method == "POST" and form.is_valid():
            form.save()
            return redirect(f'{reverse("lecture_home")}?slug={slug}')
          # Redirect after PDF is uploaded

    return render(request, "lecture/create_form.html", {"form": form,'form_type':form_type})

@login_required
@require_http_methods(["POST","GET"]) # Allow both GET & POST
def create_lecture(request: HttpRequest) -> HttpResponse:
    return handle_lecture_form(request,"pdf")

@require_http_methods(["GET"])
def lecture_home(request: HttpRequest) -> HttpResponse:
    """View to show Lecture details."""
    
    slug = request.GET.get('slug')  # Get the slug from the query parameter

    
    classroom = get_object_or_404(Classroom, slug=slug)
    lectures = Lecture.objects.filter(classroom=classroom).prefetch_related('pdf_files')

    return render(request, 'lecture/index.html', {
        'classroom': classroom,
        'lectures': lectures
    })

@login_required
@require_http_methods(["POST","GET"])
def create_title(request: HttpRequest) -> HttpResponse:
    return handle_lecture_form(request,'lecture')
