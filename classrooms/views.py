
from .forms import ClassroomForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def createClassroom(request):
    if request.method=='POST':
        forms=ClassroomForm(request.POST or None)
        if forms.is_valid():
            forms.save()
            return redirect('home')
    else:
        forms=ClassroomForm()
    return render(request,'classrooms/create_classroom.html',{'forms':forms})        


def classroom_details(request):
    return render(request, 'classrooms/classroom.html')

