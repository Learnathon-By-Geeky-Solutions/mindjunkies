from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from .forms import LectureForm
from .models import Lecture
from classrooms.models import Classroom
from django.views.decorators.http import require_http_methods


@login_required
@require_http_methods(["GET", "POST"])
def handle_lecture_form(request: HttpRequest, slug: str) -> HttpResponse:
    """Handles both Lecture creation and editing logic."""
    classroom = get_object_or_404(Classroom, slug=slug)
    print(f"Classroom: {classroom}")
    form = LectureForm()
    if request.method == "POST":
        form = LectureForm(request.POST)
        print(f"Form: {form}")
        print(f"Form data: {request.POST}")
        print(f"Files data: {request.FILES}")



    return render(request, "lecture/create_topic.html", {"form": form})

# @login_required
# def create_lecture(request: HttpRequest) -> HttpResponse:
#     slug = request.GET.get('slug')  # Get the slug from the query parameter
#     if not slug:
#         messages.error(request, "Invalid request. Classroom slug is missing.")
#         return redirect("some_fallback_url")  # Redirect to a safe page
    
#     return handle_lecture_form(request, slug)

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
def create_title(request):
    slug = request.GET.get('slug')
    return handle_lecture_form(request,slug)


    # return render(request, "lecture/index.html", {"classroom":classroom})
