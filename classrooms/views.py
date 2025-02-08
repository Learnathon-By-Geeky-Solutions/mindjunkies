from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Classroom
from .forms import ClassroomForm
from django.http import HttpRequest, HttpResponse

def handle_classroom_form(request: HttpRequest, classroom: Classroom = None) -> HttpResponse:
    """Handles both classroom creation and editing logic to reduce redundancy."""
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
def create_classroom(request: HttpRequest) -> HttpResponse:
    """View to create a new classroom."""
    return handle_classroom_form(request)


@login_required
def edit_classroom(request: HttpRequest) -> HttpResponse:
    """View to edit an existing classroom."""
    slug = request.GET.get("slug")
    classroom = get_object_or_404(Classroom, slug=slug)
    return handle_classroom_form(request, classroom)


def classroom_details(request: HttpRequest, slug: str) -> HttpResponse:
    """View to show classroom details."""
    print(f"Received slug: {slug}")  # Debugging print statement
    classroom = get_object_or_404(Classroom, slug=slug)
    return render(request, "classrooms/classroom.html", {"classroom_detail": classroom})

