from django.shortcuts import render
from classrooms.models import Classroom


def home(request):
    featured_classroom=Classroom.objects.all()
    return render(request, 'home/index.html',{'classroom_list':featured_classroom})

   
    