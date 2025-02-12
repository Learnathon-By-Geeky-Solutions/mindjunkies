from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from .forms import LectureForm
from .models import Lecture
from classrooms.models import Classroom
from django.views.decorators.http import require_http_methods

# @login_required
# @require_http_methods(["GET", "POST"])
# def handle_lecture_form(request: HttpRequest, slug: str) -> HttpResponse:
#     """Handles both classroom creation and editing logic."""
#     classroom = get_object_or_404(Classroom, slug=slug)
#     print(f"Classroom: {classroom}")

#     if request.method == "POST":
#         form = LectureForm(request.POST, request.FILES)
#         print(f"Form: {form}")
#         print(f"Form data: {request.POST}")
#         print(f"Files data: {request.FILES}")

#         if form.is_valid():
#             # Create the lecture instance without saving it to the database
#             lecture_instance = form.save(commit=False)
#             print(f"Lecture instance before saving: {lecture_instance}")

#             if lecture_instance:  # Make sure the instance is not None
#                 # Set the classroom relation
#                 lecture_instance.classroom = classroom

#                 # Save the lecture instance to the database
#                 lecture_instance.save()
#                 messages.success(request, "Lecture saved successfully!")
                
#             else:
#                 messages.error(request, "Failed to create a lecture instance.")
#                 print("Lecture instance is None.")
#         else:
#             # Print form errors for debugging
#             print("Form errors:", form.errors)
#             messages.error(request, "There was an error with the form. Please check the inputs.")
#     else:
#         form = LectureForm()

#     return render(request, "lecture/create_form.html", {"form": form})

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

    classroom=get_object_or_404(Classroom,slug=slug)
    # lectures = Lecture.objects.filter(classroom=classroom)

    return render(request, "lecture/index.html", {"classroom":classroom})
