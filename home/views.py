from django.shortcuts import render
from classrooms.models import Classroom, Enrollment, ClassroomTeacher


def home(request):
    featured_classroom=Classroom.objects.all()
    enrolled_classes = []
    teacher_classes = []
    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(student=request.user)
        enrolled_classes = [ec.classroom for ec in enrolled]
        teaching = ClassroomTeacher.objects.filter(teacher=request.user)
        teacher_classes = [ec.classroom for ec in teaching]
    context = {
        'classroom_list': featured_classroom,
        'enrolled_classes': enrolled_classes,
        'teacher_classes': teacher_classes,
    }
    return render(request, 'home/index.html',context)
