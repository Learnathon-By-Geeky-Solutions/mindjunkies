from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from mindjunkies.courses.models import Course, Enrollment, CourseTeacher


@require_http_methods(["GET"])
def home(request):
    featured_course = Course.objects.all()
    context = {
        'course_list': featured_course,
    }
    enrolled_classes = []
    teacher_classes = []
    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(student=request.user)
        enrolled_classes = [ec.course for ec in enrolled]
        teaching = CourseTeacher.objects.filter(teacher=request.user)
        teacher_classes = [ec.course for ec in teaching]
        context["enrolled_classes"] = enrolled_classes
        context["teacher_classes"] = teacher_classes

    return render(request, 'home/index.html', context)
