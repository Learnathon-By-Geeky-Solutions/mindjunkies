from django.shortcuts import render,get_object_or_404
from datetime import datetime, timedelta
from courses.models import Courses
from .models import Lecture

def lecture_home(request,course_id):
  
    courses=get_object_or_404(Courses,id=course_id) if course_id else None
    default_current_week=courses.lectures.all().first()
    upcoming_deadlines={}
    lecture_id=request.GET.get('lecture_id') 
    current_week=Lecture.objects.filter(id=lecture_id).first() if lecture_id else default_current_week
    print(current_week)

    context = {
        'course': courses,
        'current_week': current_week,
        'upcoming_deadlines': upcoming_deadlines,
    }
    return render(request, 'lecture/lecture_home.html', context)