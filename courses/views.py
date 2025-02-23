from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed

from .models import Courses, CourseTeacher, Enrollment
from .forms import CourseForm


@require_http_methods(["GET"])
def course_list(request: HttpRequest) -> HttpResponse:
    """View to show all courses."""
    courses = Courses.objects.all()
    enrolled_classes = []
    teacher_classes = []
    role = None
    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(student=request.user)
        enrolled_classes = [ec.course for ec in enrolled]
        teaching = CourseTeacher.objects.filter(teacher=request.user)
        teacher_classes = [ec.course for ec in teaching]

    print(teacher_classes)

    context = {
        "courses": courses,
        "enrolled_classes": enrolled_classes,
        'teacher_classes': teacher_classes,
        "role": role,
    }
    return render(request, "courses/course_list.html", context)


@login_required
@require_http_methods(["POST", "GET"])
def create_course(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            saved_course = form.save()
            if request.user:
                CourseTeacher.objects.create(course=saved_course, teacher=request.user)
            messages.success(request, "Course saved successfully!")
            return redirect(reverse("course_details", kwargs={"slug": saved_course.slug}))
        else:
            print("Form errors:", form.errors)  # Log the errors to the console
            messages.error(request, f"There was an error processing the form: {form.errors}")
    else:
        form = CourseForm()

    return render(request, "courses/create_course.html", {"form": form, "course": None})


@login_required
@require_http_methods(["GET", "POST"])
def edit_course(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        slug = request.GET.get("slug")
        course = get_object_or_404(Courses, slug=slug) if slug else None
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course saved successfully!")
            return redirect(reverse("course_details", kwargs={"slug": slug}))
        else:
            print("Form errors:", form.errors)  # Log the errors to the console
            messages.error(request, f"There was an error processing the form: {form.errors}")
    else:
        slug = request.GET.get("slug")
        course = get_object_or_404(Courses, slug=slug) if slug else None
        form = CourseForm(instance=course)

    return render(request, "courses/create_course.html", {"form": form, "course": course})


@require_http_methods(["GET"])
def course_details(request: HttpRequest, slug: str) -> HttpResponse:
    """View to show course details."""
    course = get_object_or_404(Courses, slug=slug)
    enrolled_courses = CourseTeacher.objects.filter(course=course)
    teachers = [et.teacher for et in enrolled_courses]
    print(teachers)
    teacher = False
    if request.user in teachers:
        teacher = True
    context = {
        'course_detail': course,
        'teacher': teacher,
    }
    return render(request, "courses/course_details.html", context)


@login_required
@require_http_methods(["GET"])
def user_course_list(request: HttpRequest) -> HttpResponse:
    teaching = CourseTeacher.objects.filter(teacher=request.user)
    courses = [ec.course for ec in teaching]

    enrolled = Enrollment.objects.filter(student=request.user)
    courses = courses + [ec.course for ec in enrolled]

    context = {
        "courses": courses,
        "enrolled_classes": courses,
    }
    return render(request, "courses/course_list.html", context)
