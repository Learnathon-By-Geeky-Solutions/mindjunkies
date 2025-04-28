from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView

from mindjunkies.courses.models import Course, CourseCategory, Enrollment
from .models import Course, Enrollment
from .forms import CourseForm, RatingForm
from .models import CourseToken, LastVisitedCourse, Rating


@require_http_methods(["GET"])
def course_list(request: HttpRequest) -> HttpResponse:
    """View to show all courses."""
    courses = Course.objects.all()
    context = {
        "courses": courses,
    }
    return render(request, "courses/course_list.html", context)


class BaseCourseView(TemplateView):
    def get_enrolled_courses(self):
        if self.request.user.is_authenticated:
            enrollments = Enrollment.objects.filter(
                student=self.request.user, status="active"
            ).prefetch_related("course")
            return [enrollment.course for enrollment in enrollments]
        return []


class NewCourseView(BaseCourseView):
    template_name = "courses/new_course.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enrolled_courses = self.get_enrolled_courses()

        new_courses = Course.objects.exclude(
            id__in=[course.id for course in enrolled_courses]
        ).filter(verified=True).order_by("-created_at")

        context["new_courses"] = new_courses
        return context


class PopularCoursesView(BaseCourseView):
    template_name = "courses/popular_course.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enrolled_courses = self.get_enrolled_courses()

        new_courses = Course.objects.exclude(
            id__in=[course.id for course in enrolled_courses]
        ).order_by("-created_at")

        courses = Course.objects.exclude(
            id__in=new_courses.values_list("id", flat=True)
        ).exclude(id__in=[course.id for course in enrolled_courses])

        popular_courses = courses.filter(verified=True).order_by("-enrollments")
        context["popular_courses"] = popular_courses
        return context


class MyCoursesView(LoginRequiredMixin, TemplateView):
    template_name = "courses/my_course.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # With prefetch for better performance
        enrolled_courses = (
            Course.objects.filter(
                enrollments__student=self.request.user, enrollments__status="active"
            )
            .prefetch_related("enrollments")
            .distinct()
        )

        enrolled_courses = enrolled_courses.filter(verified=True)
        context["enrolled_courses"] = enrolled_courses
        return context


class CreateCourseView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/create_course.html"
    success_url = reverse_lazy("dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["verification"] = CourseToken.objects.filter(
            teacher=self.request.user, status="pending"
        ).exists()
        return context

    def get(self, request, *args, **kwargs):
        if CourseToken.objects.filter(teacher=request.user, status="pending").exists():
            messages.error(
                request,
                "You have a pending course token. Please wait for it to be approved.",
            )
            return redirect(reverse("dashboard"))
        else:
            return super().get(request)

    def form_valid(self, form):
        course = form.save(commit=False)
        course.teacher = self.request.user
        course.save()
        form.save_m2m()

        CourseToken.objects.create(
            course=course, teacher=self.request.user, status="pending"
        )

        messages.success(self.request, "Course created successfully and is pending approval!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "There was an error processing the form. Please correct the errors below."
        )
        return self.render_to_response(self.get_context_data(form=form))


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

        form.save()
        return redirect(reverse("course_details", kwargs={"slug": form.instance.slug}))

    def form_invalid(self, form):
        messages.error(
            self.request, f"There was an error processing the form: {form.errors}"
        )
        return self.render_to_response(self.get_context_data(form=form))


@require_http_methods(["GET"])
def course_details(request: HttpRequest, slug: str) -> HttpResponse:
    """View to show course details."""
    course = get_object_or_404(Course, slug=slug)
    ratings = course.get_individual_ratings()
    enrolled = False
    num_lectures = course.modules.aggregate(models.Count("lectures"))["lectures__count"]

    if request.user.is_authenticated:
        enrolled = course.enrollments.filter(
            student=request.user, status="active"
        ).exists()

    paginator = Paginator(ratings, 5)
    page = request.GET.get("page", 1)
    try:
        paginated_ratings = paginator.page(page)
    except PageNotAnInteger:
        paginated_ratings = paginator.page(1)
    except EmptyPage:
        paginated_ratings = paginator.page(paginator.num_pages)

    context = {
        "course_detail": course,
        "ratings": paginated_ratings,
        "student": enrolled,
        "num_lectures": num_lectures,
    }
    return render(request, "courses/course_details.html", context)


@login_required
@require_http_methods(["GET"])
def user_course_list(request: HttpRequest) -> HttpResponse:
    courses = (
        Course.objects.filter(enrollments__student=request.user)
        .annotate(
            last_visited_at=models.Subquery(
                LastVisitedCourse.objects.filter(
                    user=request.user, course=models.OuterRef("pk")
                ).values("last_visited")[:1]
            )
        )
        .order_by("-last_visited_at", "title")
    )  # Order by last visited time, then alphabetically

    return render(request, "courses/course_list.html", {"courses": courses})


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


class RatingCreateView(CreateView):
    model = Rating
    form_class = RatingForm
    template_name = "courses/rate_course.html"

    def dispatch(self, request, *args, **kwargs):
        course = get_object_or_404(Course, slug=self.kwargs["course_slug"])
        if course.teacher == request.user:
            messages.error(request, "You cannot rate your own course.")
            return redirect(reverse("lecture_home", kwargs={"course_slug": course.slug}))
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        course = get_object_or_404(Course, slug=self.kwargs["course_slug"])
        try:
            rating = Rating.objects.get(student=self.request.user, course=course)
            initial.update(
                {
                    "rating": rating.rating,
                    "review": rating.review,
                }
            )
        except Rating.DoesNotExist:
            pass
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = get_object_or_404(Course, slug=self.kwargs["course_slug"])
        return context

    def form_valid(self, form):
        course = get_object_or_404(Course, slug=self.kwargs["course_slug"])
        student = self.request.user

        _, _ = Rating.objects.update_or_create(
            student=student,
            course=course,
            defaults={
                "rating": form.cleaned_data["rating"],
                "review": form.cleaned_data["review"],
            },
        )

        course.update_rating()

        return redirect(reverse("course_details", kwargs={"slug": course.slug}))


class DeleteCourseView(LoginRequiredMixin, TemplateView):
    model = Course
    template_name = "components/content.html"
    success_url = reverse_lazy("dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, slug=self.kwargs["course_slug"])
        context["course"] = course
        return context

    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, slug=self.kwargs["course_slug"])
        course.delete()
        messages.success(request, "Course deleted successfully!")
        return redirect(self.success_url)
