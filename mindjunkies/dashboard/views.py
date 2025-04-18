from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods
from django.views.generic.edit import FormView

from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course, Enrollment

from .forms import TeacherVerificationForm
from .models import Certificate, TeacherVerification


@login_required
@require_http_methods(["GET"])
def content_list(request: HttpRequest) -> HttpResponse:
    if not request.user.is_teacher:
        return redirect("teacher_verification_form")
    courses = Course.objects.filter(teacher=request.user)
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

    course.save()

    t_enrollment.delete()

    return redirect("teacher_dashboard_enrollments", course.slug)


class TeacherVerificationView(FormView):
    template_name = "teacher_verification.html"
    form_class = TeacherVerificationForm
    success_url = reverse_lazy("home")  # Redirect after successful form submission

    def get(self, request):
        if request.user.is_teacher:
            redirect("dashboard")  # Redirect if already a teacher

        elif TeacherVerification.objects.filter(user=request.user).exists():
            return redirect("verification_wait")
        return super().get(request)

    def form_valid(self, form):
        # Save Teacher Verification info
        teacher_verification = form.save(commit=False)
        teacher_verification.user = (
            self.request.user
        )  # Link the form submission to the current user
        teacher_verification.verification_date = (
            now()
        )  # Store the current time of verification

        # Handle certificate files and save them
        certificates = self.request.FILES.getlist("certificates")  # Get multiple files

        teacher_verification.save()

        for certificate in certificates:
            cert_instance = Certificate.objects.create(image=certificate)
            # Add the saved certificate instance to the ManyToManyField
            teacher_verification.certificates.add(cert_instance)

        messages.success(
            self.request, "Your verification has been submitted successfully!"
        )
        return super().form_valid(form)  # Redirects to success_url defined above

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error in your form submission. Please check the form and try again.",
        )
        return super().form_invalid(form)


@login_required
@require_http_methods(["GET"])
def verification_wait(request):
    return render(request, "verification_wait.html", {"message": "Please wait for your verification."})

