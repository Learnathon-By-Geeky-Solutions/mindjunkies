
from .forms import ClassroomForm
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Classroom

# Create your views here.
@login_required
def createClassroom(request):
    if request.method=='POST':
        forms=ClassroomForm(request.POST, request.FILES)
        
        if forms.is_valid():
            forms.save()
            return redirect('home')
    else:
        forms=ClassroomForm()
    return render(request,'classrooms/create_classroom.html',{'forms':forms})        


def classroom_details(request,slug):
    classroom_detail=get_object_or_404(Classroom,slug=slug)
    return render(request, 'classrooms/classroom.html',{'classroom_detail':classroom_detail})




def edit_classroom(request):
    slug = request.GET.get('slug')
    classroom_detail = get_object_or_404(Classroom, slug=slug)
    
    if request.method == 'POST':
        forms = ClassroomForm(request.POST, request.FILES, instance=classroom_detail)
        if forms.is_valid():
            forms.save()
            # After saving, redirect to a success page or classroom details page
            return redirect('classroom_details', slug=classroom_detail.slug)
    else:
        forms = ClassroomForm(instance=classroom_detail)
    
    return render(request, 'classrooms/edit_classroom.html', {'forms': forms, 'classroom_detail': classroom_detail})



