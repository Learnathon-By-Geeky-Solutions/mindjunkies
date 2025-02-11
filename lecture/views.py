from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from .forms import LectureForm
from .models import Lecture
# Create your views here.
@login_required
@require_http_methods(["GET", "POST"])
def handle_lecture_form(request: HttpRequest, slug: str = None) -> HttpResponse:
    """Handles both classroom creation and editing logic."""
    
    lecture = get_object_or_404(Lecture, slug=slug) if slug else None

    if request.method == "POST":
        form = LectureForm(request.POST, request.FILES)
        if form.is_valid():
            saved_lecture = form.save()
            messages.success(request, "Classroom saved successfully!")
            return redirect(reverse("classroom_details", kwargs={"slug": saved_lecture.slug}))
        # messages.error(request, "There was an error processing the form.")
    else:
        form =LectureForm(instance=lecture)

    return render(request, "lecture/create_form.html",{"form":form})
@login_required

def create_lecture(request: HttpRequest) -> HttpResponse:
    
    """Redirects to the classroom form without a slug for creation."""
    return handle_lecture_form(request)
def lecture_home(request):
    return render(request,'lecture/index.html')

