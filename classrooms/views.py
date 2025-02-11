from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from .models import Classroom
from .forms import ClassroomForm


@login_required
@require_http_methods(["GET", "POST"])
def handle_classroom_form(request: HttpRequest, slug: str = None) -> HttpResponse:
    """Handles both classroom creation and editing logic."""
    
    classroom = get_object_or_404(Classroom, slug=slug) if slug else None

    if request.method == "POST":
        form = ClassroomForm(request.POST, request.FILES, instance=classroom)
        if form.is_valid():
            saved_classroom = form.save()
            messages.success(request, "Classroom saved successfully!")
            return redirect(reverse("classroom_details", kwargs={"slug": saved_classroom.slug}))
        messages.error(request, "There was an error processing the form.")
    else:
        form = ClassroomForm(instance=classroom)

    return render(request, "classrooms/classroom_form.html", {"form": form, "classroom": classroom})


@login_required
@require_http_methods(["POST"])
def create_classroom(request: HttpRequest) -> HttpResponse:
    """Redirects to the classroom form without a slug for creation."""
    return handle_classroom_form(request)


@login_required
@require_http_methods(["GET", "POST"])
def edit_classroom(request: HttpRequest) -> HttpResponse:
    """Redirects to the classroom form with a slug for editing."""
    slug = request.GET.get("slug")
    return handle_classroom_form(request, slug)


@require_http_methods(["GET"])
def classroom_details(request: HttpRequest, slug: str) -> HttpResponse:
    """View to show classroom details."""
    classroom = get_object_or_404(Classroom, slug=slug)
    return render(request, "classrooms/classroom.html", {"classroom_detail": classroom})
