from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest, HttpResponse
from courses.models import CourseTeacher, Enrollment


# Create your views here.

@login_required
@require_http_methods(["GET"])
def content_list(request: HttpRequest) -> HttpResponse:
    teaching = CourseTeacher.objects.filter(teacher=request.user)
    courses = [ec.course for ec in teaching]

    # enrolled = Enrollment.objects.filter(student=request.user)
    # courses = courses + [ec.course for ec in enrolled]

    print(courses[0])
    context = {
        "courses": courses,
    }
    return render(request, "dashboard.html", context)