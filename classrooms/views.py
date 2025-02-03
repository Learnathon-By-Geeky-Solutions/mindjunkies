from django.shortcuts import render

# Create your views here.
def classroom_details(request):
    return render(request, 'classrooms/classroom.html')