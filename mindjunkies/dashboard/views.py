from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views import View
from django.views.generic.edit import FormView
from django.core.paginator import Paginator

from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course, Enrollment
from mindjunkies.payments.models import Transaction, Balance, BalanceHistory

from .forms import TeacherVerificationForm
from .mixins import CustomPermissionRequiredMixin
from .models import Certificate, TeacherVerification

VIEW_COURSE_PERMISSION = "courses.view_course"


class TeacherPermissionView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_teacher:
            return redirect("dashboard")  # Redirect if already a teacher

        elif TeacherVerification.objects.filter(user=request.user).exists():
            return redirect("verification_wait")
        return render(request, "apply_teacher.html")

<<<<<<< HEAD
  # cache for 5 minutes
class ContentListView(LoginRequiredMixin, View):
    
=======

@method_decorator(cache_page(60 * 5), name="dispatch")  # cache for 5 minutes
class TeacherHome(LoginRequiredMixin, View):
>>>>>>> 9dff5337abe729fb28319a6ef60f194c16de99fb
    permission_required = VIEW_COURSE_PERMISSION

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.user.is_teacher:
            return redirect("teacher_permission")

        courses = Course.objects.filter(teacher=request.user, status="published")
        context = {
            "courses": courses,
            "status": "Published",
        }
        return render(request, "components/content.html", context)

<<<<<<< HEAD
        elif status == "draft":
            print("🔴 view code executing!")   # ← this only appears on a cache MISS
=======

@method_decorator(cache_page(60 * 5), name="dispatch")  # cache for 5 minutes
class ContentListView(LoginRequiredMixin, View):
    permission_required = VIEW_COURSE_PERMISSION

    def get_queryset(self):
        import time
        time.sleep(5)
        return super().get_queryset()

    def get(self, request: HttpRequest, status: str) -> HttpResponse:
        if not request.user.is_teacher:
            return redirect("teacher_permission")

        courses = Course.objects.filter(teacher=request.user, status="published")
        context = {
            "courses": courses,
            "status": "Published",
        }

        if status == "draft":
>>>>>>> 9dff5337abe729fb28319a6ef60f194c16de99fb
            courses = Course.objects.filter(teacher=request.user, status="draft")
            context["courses"] = courses
            print(courses)
            context["status"] = "Draft"
            return render(request, "components/draft.html", context)
        elif status == "archived":
            courses = Course.objects.filter(teacher=request.user, status="archived")
            context["courses"] = courses
            context["status"] = "Archived"
            return render(request, "components/archive.html", context)

        elif status == "balance":
            balance = Balance.objects.filter(user=request.user).first()
            print(balance)
            if not balance:
                balance = Balance.objects.create(user=request.user, amount=0)
            transactions = Transaction.objects.filter(user=request.user).order_by('-tran_date')

            page_number = request.GET.get("page", 1)
            paginator = Paginator(transactions, 10)  # Show 10 transactions per page
            page_obj = paginator.get_page(page_number)

            context["balance"] = balance
            context["transactions"] = page_obj
            context["status"] = "Balance"
            return render(request, "components/balance.html", context)
        else:
<<<<<<< HEAD
            return render(request, "components/content.html", context)
        

         
    

=======
            return redirect("dashboard")
>>>>>>> 9dff5337abe729fb28319a6ef60f194c16de99fb


class EnrollmentListView(LoginRequiredMixin, CustomPermissionRequiredMixin, View):
    permission_required = VIEW_COURSE_PERMISSION

    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        course = get_object_or_404(Course, slug=slug)
        enrollments = Enrollment.objects.filter(course=course)
        students = [enrollment.student for enrollment in enrollments]

        context = {
            "course": course,
            "students": students,
        }
        return render(request, "enrollmentList.html", context)


class RemoveEnrollmentView(LoginRequiredMixin, CustomPermissionRequiredMixin, View):
    permission_required = VIEW_COURSE_PERMISSION

    def get(
        self, request: HttpRequest, course_slug: str, student_id: str
    ) -> HttpResponse:
        print("watch me", course_slug, student_id)

        course = get_object_or_404(Course, slug=course_slug)
        student = get_object_or_404(User, uuid=student_id)
        t_enrollment = get_object_or_404(Enrollment, student=student, course=course)

        print(t_enrollment)

        course.save()  # Unclear why saving is necessary here — can possibly be removed

        t_enrollment.delete()

        return redirect("teacher_dashboard_enrollments", course.slug)


class TeacherVerificationView(FormView):
    template_name = "teacher_verification.html"
    form_class = TeacherVerificationForm
    success_url = reverse_lazy("home")  # Redirect after successful form submission

    def get(self, request):
        if request.user.is_teacher:
            redirect("dashboard", status="published")  # Redirect if already a teacher

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


class VerificationWaitView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request,
            "verification_wait.html",
            {"message": "Please wait for your verification."},
        )


class DraftView(LoginRequiredMixin, View):
    permission_required = VIEW_COURSE_PERMISSION

    def get(self, request: HttpRequest) -> HttpResponse:
        if not request.user.is_teacher:
            return redirect("teacher_verification_form")

        courses = Course.objects.filter(teacher=request.user, status="draft")
        context = {
            "courses": courses,
        }
        return render(request, "components/draft.html", context)


class ArchiveView(LoginRequiredMixin, View):
    permission_required = VIEW_COURSE_PERMISSION

    def get(self, request: HttpRequest) -> HttpResponse:
        if not request.user.is_teacher:
            return redirect("teacher_verification_form")

        courses = Course.objects.filter(teacher=request.user, status="draft")
        context = {
            "courses": courses,
        }
        return render(request, "components/archive.html", context)
