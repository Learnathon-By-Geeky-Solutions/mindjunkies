from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Classroom, ClassroomTeacher
from .forms import ClassroomForm
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest, HttpResponse
from django.http import HttpResponseNotAllowed

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
@require_http_methods([ "POST"]) 
def create_classroom(request: HttpRequest) -> HttpResponse:
    """View to create a new classroom."""
    return handle_classroom_form(request)



@login_required
@require_http_methods(["GET", "POST"]) 
def edit_classroom(request: HttpRequest) -> HttpResponse:
    """View to edit an existing classroom."""
    slug = request.GET.get("slug")
    classroom = get_object_or_404(Classroom, slug=slug)

    if request.method == "GET":
        # Handle the GET request for fetching the form
        return render(request, "classrooms/edit_classroom.html", {"classroom": classroom})
    
    elif request.method == "POST":
        # Handle the POST request for updating the classroom
        return handle_classroom_form(request, classroom)
    
    else:
        # If the method is neither GET nor POST, return Method Not Allowed (405)
        return HttpResponseNotAllowed(["GET", "POST"])
def edit_classroom(request: HttpRequest) -> HttpResponse:
    """View to edit an existing classroom."""
    slug = request.GET.get("slug")
    classroom = get_object_or_404(Classroom, slug=slug)

    if request.method == "GET":
        # Handle the GET request for fetching the form
        return render(request, "classrooms/edit_classroom.html", {"classroom": classroom})
    
    elif request.method == "POST":
        # Handle the POST request for updating the classroom
        return handle_classroom_form(request, classroom)
    
    else:
        # If the method is neither GET nor POST, return Method Not Allowed (405)
        return HttpResponseNotAllowed(["GET", "POST"])


@require_http_methods(["GET"])
def classroom_details(request: HttpRequest, slug: str) -> HttpResponse:
    """View to show classroom details."""
    print(f"Received slug: {slug}")  # Debugging print statement
    classroom = get_object_or_404(Classroom, slug=slug)
    return render(request, "classrooms/classroom.html", {"classroom_detail": classroom})


@login_required
@require_http_methods(["GET"])
def user_classroom_list(request: HttpRequest) -> HttpResponse:
    user = request.user
    classroom_teacher = ClassroomTeacher.objects.filter(teacher=user)
    classrooms = [ct.classroom for ct in classroom_teacher]
    num_classrooms = len(classrooms)

    context = {
        "classrooms": classrooms,
        "num_classrooms": num_classrooms,
        "user": user,
    }
    return render(request, "classrooms/classroom_list.html", context)



