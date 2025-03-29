from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic.edit import CreateView, UpdateView, FormView
from .forms import CourseForm, CourseTokenForm, CourseInfoFormSet
from .models import Course, CourseCategory, Enrollment, CourseToken


@require_http_methods(["GET"])
def course_list(request: HttpRequest) -> HttpResponse:
    """View to show all courses."""
    courses = Course.objects.all()
    enrolled_classes = []
    teacher_classes = []
    role = None
    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(student=request.user)
        enrolled_classes = [ec.course for ec in enrolled]

    print(teacher_classes)

    context = {
        "courses": courses,
        "enrolled_classes": enrolled_classes,
        "teacher_classes": teacher_classes,
        "role": role,
    }
    return render(request, "courses/course_list.html", context)


class CreateCourseView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/create_course.html"
    success_url = reverse_lazy("course_list")

    def get(self, request):
        if CourseToken.objects.filter(user=request.user, status="pending").exists():
            messages.error(
                request,
                "You have a pending course token. Please wait for it to be approved.",
            )
            return redirect(reverse("dashboard"))
        else:
            return super().get(request)

    def get_context_data(self, **kwargs):
        """Add the formset to the context"""
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = CourseInfoFormSet(self.request.POST)
        else:
            context["formset"] = CourseInfoFormSet()
        return context

    def form_valid(self, form):
        """Save the Course and CourseInfo forms together"""
        form.instance.teacher = self.request.user
        self.object = form.save()

        formset = CourseInfoFormSet(self.request.POST, instance=self.object)
        if formset.is_valid():
            formset.save()
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

        return redirect(self.get_success_url())


class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/create_course.html"
    context_object_name = "course"

    def get_object(self, queryset=None):
        slug = self.request.GET.get("slug")
        return get_object_or_404(Course, slug=slug) if slug else None

    def form_valid(self, form):
        messages.success(self.request, "Course saved successfully!")
        return redirect(reverse("course_details", kwargs={"slug": form.instance.slug}))

    def form_invalid(self, form):
        print("Form errors:", form.errors)  # Log the errors to the console
        messages.error(
            self.request, f"There was an error processing the form: {form.errors}"
        )
        return self.render_to_response(self.get_context_data(form=form))


@require_http_methods(["GET"])
def course_details(request: HttpRequest, slug: str) -> HttpResponse:
    """View to show course details."""
    course = get_object_or_404(Course, slug=slug)
    enrolled = course.enrollments.filter(student=request.user, status="active").exists()
    context = {
        "course_detail": course,
    }
    return render(request, "courses/course_details.html", context)


@login_required
@require_http_methods(["GET"])
def user_course_list(request: HttpRequest) -> HttpResponse:
    enrolled = Enrollment.objects.filter(student=request.user)
    courses = [ec.course for ec in enrolled]

    print(courses)
    print("enrolled", enrolled)

    context = {
        "courses": courses,
        "enrolled_classes": courses,
    }
    return render(request, "courses/course_list.html", context)


@require_http_methods(["GET"])
def category_courses(request, slug):
    category = get_object_or_404(CourseCategory, slug=slug)
    sub_categories = category.get_descendants(include_self=True)
    courses = Course.objects.filter(category__in=sub_categories)
    return render(
        request,
        "courses/category_courses.html",
        {"category": category, "courses": courses},
    )


class CreateCourseTokenView(LoginRequiredMixin, FormView):
    template_name = "course_token_form.html"
    form_class = CourseTokenForm

    def form_valid(self, form):
        token = form.save(commit=False)
        token.user = self.request.user  # Automatically assign logged-in user
        token.save()
        messages.success(self.request, "Course token created successfully!")
        return redirect(reverse("home"))  # Redirect to a success page

    def form_invalid(self, form):
        messages.error(self.request, "There was an error processing the form.")
        return self.render_to_response(self.get_context_data(form=form))
