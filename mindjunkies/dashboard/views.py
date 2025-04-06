from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course, Enrollment


@login_required
@require_http_methods(["GET"])
def content_list(request: HttpRequest) -> HttpResponse:
    courses = Course.objects.filter(teacher=request.user)
    context = {
        "courses": courses,
    }
    return render(request, "dashboard.html", context)


@login_required
@require_http_methods(["GET"])
def enrollment_list(request: HttpRequest, slug: str) -> HttpResponse:
    course = Course.objects.get(slug=slug)

    enrollments = Enrollment.objects.filter(course=course)
    students = [enrollment.student for enrollment in enrollments]

    context = {
        "course": course,
        "students": students,
    }
    return render(request, "enrollmentList.html", context)


@login_required
@require_http_methods(["GET"])
def remove_enrollment(
    request: HttpRequest, course_slug: str, student_id: str
) -> HttpResponse:
    print("watch me", course_slug, student_id)
    course = Course.objects.get(slug=course_slug)
    student = User.objects.get(uuid=student_id)
    t_enrollment = Enrollment.objects.get(student=student, course=course)
    print(t_enrollment)

    course.save()

    t_enrollment.delete()

    return redirect("teacher_dashboard_enrollments", course.slug)
