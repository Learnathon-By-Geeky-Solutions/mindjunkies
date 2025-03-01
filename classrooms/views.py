from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed

from .models import Classroom, ClassroomTeacher, Enrollment
from .forms import ClassroomForm


@require_http_methods(["GET"])
def classroom_list(request: HttpRequest) -> HttpResponse:
    """View to show all classrooms."""
    classrooms = Classroom.objects.all()
    enrolled_classes = []
    teacher_classes = []
    role = None
    if request.user.is_authenticated:
        role = request.user.role
        enrolled = Enrollment.objects.filter(student=request.user)
        enrolled_classes = [ec.classroom for ec in enrolled]
        teaching = ClassroomTeacher.objects.filter(teacher=request.user)
        teacher_classes = [ec.classroom for ec in teaching]

    print(teacher_classes)

    context = {
        "classrooms": classrooms,
        "enrolled_classes": enrolled_classes,
        'teacher_classes': teacher_classes,
        "role": role,
    }
    return render(request, "classrooms/classroom_list.html", context)


@login_required
@require_http_methods(["POST", "GET"])
def create_classroom(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ClassroomForm(request.POST, request.FILES)
        if form.is_valid():
            saved_classroom = form.save()
            if request.user:
                ClassroomTeacher.objects.create(classroom=saved_classroom, teacher=request.user)
            messages.success(request, "Classroom saved successfully!")
            return redirect(reverse("classroom_details", kwargs={"slug": saved_classroom.slug}))
        else:
            print("Form errors:", form.errors)  # Log the errors to the console
            messages.error(request, f"There was an error processing the form: {form.errors}")
    else:
        form = ClassroomForm()

    return render(request, "classrooms/create_classroom.html", {"form": form, "classroom": None})


@login_required
@require_http_methods(["GET", "POST"])
def edit_classroom(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        slug = request.GET.get("slug")
        classroom = get_object_or_404(Classroom, slug=slug) if slug else None
        form = ClassroomForm(request.POST, request.FILES, instance=classroom)
        if form.is_valid():
            form.save()
            messages.success(request, "Classroom saved successfully!")
            return redirect(reverse("classroom_details", kwargs={"slug": slug}))
        else:
            print("Form errors:", form.errors)  # Log the errors to the console
            messages.error(request, f"There was an error processing the form: {form.errors}")
    else:
        slug = request.GET.get("slug")
        classroom = get_object_or_404(Classroom, slug=slug) if slug else None
        form = ClassroomForm(instance=classroom)

    return render(request, "classrooms/create_classroom.html", {"form": form, "classroom": classroom})


@require_http_methods(["GET"])
def classroom_details(request: HttpRequest, slug: str) -> HttpResponse:
    """View to show classroom details."""
    classroom = get_object_or_404(Classroom, slug=slug)
    enrolled_classrooms = ClassroomTeacher.objects.filter(classroom=classroom)
    teachers = [et.teacher for et in enrolled_classrooms]
    print(teachers)
    teacher = False
    if request.user in teachers:
        teacher = True
    context = {
        'classroom_detail': classroom,
        'teacher': teacher,
    }
    return render(request, "classrooms/classroom_details.html", context)


@login_required
@require_http_methods(["GET"])
def user_classroom_list(request: HttpRequest) -> HttpResponse:
    if request.user.role == 'teacher':
        teaching = ClassroomTeacher.objects.filter(teacher=request.user)
        classrooms = [ec.classroom for ec in teaching]

        context = {
            "classrooms": classrooms,
            "teacher_classes": classrooms,
        }
    else:
        enrolled = Enrollment.objects.filter(student=request.user)
        classrooms = [ec.classroom for ec in enrolled]

        context = {
            "classrooms": classrooms,
            "enrolled_classes": classrooms,
        }
    return render(request, "classrooms/classroom_list.html", context)
