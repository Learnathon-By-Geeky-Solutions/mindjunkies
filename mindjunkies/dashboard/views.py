from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.timezone import now


from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course, Enrollment
from .forms import TeacherVerificationForm
from .models import TeacherVerification, Certificate


# Create your views here.


@login_required
@require_http_methods(["GET"])
def content_list(request: HttpRequest) -> HttpResponse:
    if not request.user.is_teacher:
        return redirect("teacher_verification_form")
    teaching = Course.objects.filter(teacher=request.user)
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
def remove_enrollment(
    request: HttpRequest, course_slug: str, student_id: str
) -> HttpResponse:
    print("watch me", course_slug, student_id)
    course = Course.objects.get(slug=course_slug)
    student = User.objects.get(uuid=student_id)
    t_enrollment = Enrollment.objects.get(student=student, course=course)
    print(t_enrollment)

    course.number_of_enrollments -= 1

    course.save()

    t_enrollment.delete()

    return redirect("teacher_dashboard_enrollments", course.slug)




@login_required
def teacher_verification(request):
    if request.method == 'POST':
        form = TeacherVerificationForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Save Teacher Verification info
            teacher_verification = form.save(commit=False)
            teacher_verification.user = request.user  # Link the form submission to the current user
            teacher_verification.verification_date = now()  # Store the current time of verification
            
            # Handle certificate files and save them
            certificates = request.FILES.getlist('certificates')
            for certificate_file in certificates:
                certificate = Certificate.objects.create(image=certificate_file)
                teacher_verification.certificates.add(certificate)
            
            teacher_verification.save()
            messages.success(request, "Your verification has been submitted successfully!")
            return redirect('some_success_url')  # Redirect after successful form submission    
        else:
            messages.error(request, "There was an error in your form submission. Please check the form and try again.")
    else:
        form = TeacherVerificationForm()

    return render(request, 'teacher_verification.html', {'form': form})


@login_required
def verification_wait(request):
    return render(request, "verification_wait.html")
