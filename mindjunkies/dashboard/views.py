from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views import View
from django.views.generic.edit import FormView
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin

from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course, Enrollment, CourseToken
from mindjunkies.payments.models import Transaction, Balance
from mindjunkies.dashboard.forms import TeacherVerificationForm
from mindjunkies.dashboard.mixins import VerifiedTeacherRequiredMixin
from mindjunkies.dashboard.models import TeacherVerification, Certificate

VIEW_COURSE_PERMISSION = "courses.view_course"


class TeacherHome(VerifiedTeacherRequiredMixin, View):
    """
    Dashboard for teachers - shows published courses and pending verifications.
    """

    def get(self, request, *args, **kwargs):
        courses = Course.objects.filter(teacher=request.user, status="published")
        unverified_courses = Course.objects.filter(teacher=request.user, verified=False)

        context = {
            "courses": courses,
            "unverified_courses": unverified_courses,
        }
        return render(request, "components/content.html", context)


class ContentListView(VerifiedTeacherRequiredMixin, View):
    """
    Displays courses by status: published, draft, archived, balance.
    """

    def get(self, request, status: str):
        courses = Course.objects.filter(teacher=request.user, status="published")
        unverified_courses = Course.objects.filter(teacher=request.user, verified=False)
        context = {"courses": courses, "status": "Published", "unverified_courses": unverified_courses}

        if status == "draft":
            courses = Course.objects.filter(teacher=request.user, status="draft")
            context.update({"courses": courses, "status": "Draft"})
            return render(request, "components/draft.html", context)

        if status == "archived":
            courses = Course.objects.filter(teacher=request.user, status="archived")
            context.update({"courses": courses, "status": "Archived"})
            return render(request, "components/archive.html", context)

        if status == "balance":
            balance = Balance.objects.filter(user=request.user).first() or Balance.objects.create(user=request.user,
                                                                                                  amount=0)
            transactions = Transaction.objects.filter(user=request.user).order_by('-tran_date')

            paginator = Paginator(transactions, 10)
            page_obj = paginator.get_page(request.GET.get("page", 1))

            context.update({
                "balance": balance,
                "transactions": page_obj,
                "status": "Balance",
            })
            return render(request, "components/balance.html", context)

        return redirect("dashboard")


class EnrollmentListView(VerifiedTeacherRequiredMixin, View):
    """
    Lists students enrolled in a specific course.
    """

    def get(self, request, slug: str):
        course = get_object_or_404(Course, slug=slug)
        enrollments = Enrollment.objects.filter(course=course)
        students = [enrollment.student for enrollment in enrollments]

        context = {
            "course": course,
            "students": students,
        }
        return render(request, "enrollmentList.html", context)


class RemoveEnrollmentView(VerifiedTeacherRequiredMixin, View):
    """
    Allows a teacher to remove a student from a course.
    """

    def get(self, request, course_slug: str, student_id: str):
        course = get_object_or_404(Course, slug=course_slug)
        student = get_object_or_404(User, uuid=student_id)
        enrollment = get_object_or_404(Enrollment, student=student, course=course)

        enrollment.delete()

        return redirect('teacher_dashboard_enrollments', course.slug)


class TeacherVerificationView(LoginRequiredMixin, FormView):
    """
    Form for users to submit verification to become a teacher.
    """
    template_name = "teacher_verification.html"
    form_class = TeacherVerificationForm
    success_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            print("teacher is true")
            return redirect('dashboard')
        if TeacherVerification.objects.filter(user=request.user).exists():
            print("verification exists")
            return redirect('verification_wait')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        verification = form.save(commit=False)
        verification.user = self.request.user
        verification.verification_date = now()
        verification.save()

        certificates = self.request.FILES.getlist("certificates")
        for certificate_file in certificates:
            certificate = Certificate.objects.create(image=certificate_file)
            verification.certificates.add(certificate)

        messages.success(self.request, "Your verification has been submitted successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error. Please try again.")
        return super().form_invalid(form)


class VerificationWaitView(LoginRequiredMixin, View):
    """
    Shows a waiting page after submitting teacher verification.
    """

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            messages.info(request, "You are already a verified teacher.")
            return redirect('dashboard')

        return render(
            request,
            "verification_wait.html",
            {"message": "Please wait for your verification."},
        )


class DraftView(VerifiedTeacherRequiredMixin, View):
    """
    Displays draft courses for the teacher.
    """

    def get(self, request, *args, **kwargs):
        courses = Course.objects.filter(teacher=request.user, status="draft")
        context = {"courses": courses}
        return render(request, "components/draft.html", context)


class ArchiveView(VerifiedTeacherRequiredMixin, View):
    """
    Displays archived courses for the teacher.
    """

    def get(self, request, *args, **kwargs):
        courses = Course.objects.filter(teacher=request.user, status="archived")
        context = {"courses": courses}
        return render(request, "components/archive.html", context)
