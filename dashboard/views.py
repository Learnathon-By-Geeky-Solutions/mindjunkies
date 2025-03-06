from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest, HttpResponse
from courses.models import CourseTeacher, Enrollment, Course
from accounts.models import User


# Create your views here.

@login_required
@require_http_methods(["GET"])
def content_list(request: HttpRequest) -> HttpResponse:
    teaching = CourseTeacher.objects.filter(teacher=request.user)
    courses = [ec.course for ec in teaching]
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

    # print(course.__dict__)
    context = {
        "course": course,
        "students": students,
    }
    return render(request, "enrollmentList.html", context)



@login_required
@require_http_methods(["GET"])
def remove_enrollment(request: HttpRequest, course_slug: str, student_id: str) -> HttpResponse:
    print("watch me", course_slug, student_id)
    course = Course.objects.get(slug=course_slug)
    student = User.objects.get(uuid=student_id)
    t_enrollment = Enrollment.objects.get(student=student, course=course)
    print(t_enrollment)

    course.number_of_enrollments -= 1
    
    course.save()

    t_enrollment.delete()

    return redirect('teacher_dashboard_enrollments', course.slug)