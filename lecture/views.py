from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, Http404
from .forms import LectureForm,LecturePDFForm
from courses.models import Course,Module
from .models import Lecture, LectureVideo,LecturePDF



@login_required
@require_http_methods(["GET"])
def lecture_home(request: HttpRequest,slug:str) -> HttpResponse:
    """View to show lectures for a course."""
    
    # Get the course or return 404 if not found
    
    course = get_object_or_404(Course, slug=slug)
    
    # Ensure the user is enrolled in the course
    if not request.user.is_staff and not course.enrollments.filter(student=request.user).exists():
        return HttpResponseForbidden("added to shopping cart")

    # Fetch lectures for the course
    default_current_week = course.modules.first()
    upcoming_deadlines = {}  # TODO: Add logic for upcoming deadlines


    teacher = False
    if request.user.is_staff or course.enrollments.filter(teacher=request.user).exists():
        print("TRUE")
        teacher = True

    # Get selected lecture if provided
    module_id = request.GET.get("module_id")
    current_week = Module.objects.filter(id=module_id).first() if module_id else default_current_week

    if not current_week:
        messages.warning(request, "No lectures available for this course.")
    
    context = {
        "course": course,
        "current_week": current_week,
        "upcoming_deadlines": upcoming_deadlines,
        "isTeacher": teacher,
    }
    
    return render(request, "lecture/lecture_home.html", context)


@login_required
@require_http_methods(["GET"])
def lecture_video(request: HttpRequest, module_id:str, video_id: int) -> HttpResponse:
    """View to display a lecture video."""
    
    # Get the video or return 404 if not found
    video = get_object_or_404(LectureVideo, id=video_id)
    module=Module.objects.get(id=module_id)
    # Ensure the user is enrolled in the related course
    if not request.user.is_staff and not video.lecture.course.enrollments.filter(student=request.user).exists():
        return HttpResponseForbidden("You are not enrolled in this course.")

    context = {
        "video": video,
        "module":module
    }

    return render(request, "lecture/lecture_video.html", context)

@login_required
@require_http_methods(["GET"])
def lecture_pdf(request: HttpRequest,slug:str,pdf_id: int) -> HttpResponse:
    """View to display a lecture video."""
    
    # Get the pdf or return 404 if not found
    pdf = get_object_or_404(LecturePDF, id=pdf_id)
    lecture=Lecture.objects.get(slug=slug)
   
    
    # Ensure the user is enrolled in the related course
   

    context = {
        "pdf": pdf,
        "lecture":lecture
       
    }

    return render(request, "lecture/lecture_pdf.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def create_lecture(request: HttpRequest,slug:str) -> HttpResponse:
    if request.method == "POST":
        form = LectureForm(request.POST)  # Pass the user if needed
        course = get_object_or_404(Course, slug=slug)
        if form.is_valid():
            saved_lecture = form.save(commit=False)
            saved_lecture.course=course
            saved_lecture.save()
            messages.success(request, "Lecture created successfully!")
            return redirect("lecture_home", slug=slug)  # Redirect to a relevant page
        else:
            messages.error(request, "There was an error processing the form. Please check the fields below.")

    else:
        form = LectureForm()

    return render(request, "lecture/create_lecture.html", {"form": form})

@login_required
@require_http_methods(["GET", "POST"])
def create_content(request: HttpRequest,course_slug:str,lecture_slug:str) -> HttpResponse:
    if request.method == "POST":
        form = LecturePDFForm(request.POST,request.FILES)  # Pass the user if needed
        lecture = get_object_or_404(Lecture, slug=lecture_slug)
        if form.is_valid():
            saved_content = form.save(commit=False)
            saved_content.lecture=lecture
            saved_content.save()
            messages.success(request, "Lecture Content created successfully!")
            return redirect("lecture_home", slug=course_slug)  # Redirect to a relevant page
        else:
            messages.error(request, "There was an error processing the form. Please check the fields below.")

    else:
        form = LecturePDFForm()

    return render(request, "lecture/create_content.html", {"form": form})

@login_required
@require_http_methods(["GET", "POST"])
def edit_lecture(request: HttpRequest,course_slug:str,lecture_slug:str) -> HttpResponse:
    lecture = get_object_or_404(Lecture, slug=lecture_slug) if lecture_slug else None
    if request.method == "POST":
       
        
        form = LectureForm(request.POST, request.FILES, instance=lecture)
        if form.is_valid():
            form.save()
            messages.success(request, "Lecture saved successfully!")
            return redirect("lecture_home",slug=course_slug)
        else:
            print("Form errors:", form.errors)  # Log the errors to the console
            messages.error(request, f"There was an error processing the form: {form.errors}")
    else:
       
        lecture = get_object_or_404(Lecture, slug=lecture_slug) if lecture_slug else None
        form =LectureForm(instance=lecture)

    return render(request, "lecture/create_lecture.html", {"form": form, "lecture": lecture})




     

