from django.db import models
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET
from django.views.decorators.vary import vary_on_cookie


from django.views.generic import TemplateView

from mindjunkies.courses.models import Course, CourseCategory, Enrollment
from mindjunkies.lecture.models import LastVisitedModule, Lecture


@method_decorator(require_GET, name='dispatch')
@method_decorator(cache_page(60 * 5), name="dispatch")  # cache for 5 minutes
class HomeView(TemplateView):
    template_name = "home/index.html"

    def get(self, request, *args, **kwargs):
        # Get course categories with their children
        categories = CourseCategory.objects.filter(parent__isnull=True).prefetch_related("children")

        # Determine active category
        active_category_slug = request.GET.get("category")
        active_category = None
        if active_category_slug:
            try:
                active_category = CourseCategory.objects.prefetch_related("children").get(
                    slug=active_category_slug, parent__isnull=True
                )
            except CourseCategory.DoesNotExist:
                pass
        if not active_category and categories.exists():
            active_category = categories.first()

        # Handle enrolled and teacher courses
        enrolled_courses = []
        teacher_courses = []
        if request.user.is_authenticated:
            enrollments = (
                Enrollment.objects
                .filter(student=request.user, status="active")
                .prefetch_related("course")
            )
            enrolled_courses = [e.course for e in enrollments]
            teacher_courses = Course.objects.filter(teacher=request.user)

        # New courses (excluding enrolled)
        new_courses = (
            Course.objects
            .exclude(id__in=[c.id for c in enrolled_courses])
            .order_by("-created_at")[:3]
        )

        # Other courses (excluding new and enrolled)
        courses = (
            Course.objects
            .exclude(id__in=new_courses.values_list("id", flat=True))
            .exclude(id__in=[c.id for c in enrolled_courses])
        )

        # Featured courses
        featured_courses = Course.objects.filter(status="published")

        # Continue-learning logic
        last_lecture = None
        progression = 0
        recommended_courses = None

        if request.user.is_authenticated:
            continue_lecture = (
                Lecture.objects.filter(course__enrollments__student=request.user)
                .annotate(
                    last_visited_at=models.Subquery(
                        LastVisitedModule.objects.filter(
                            user=request.user, lecture=models.OuterRef("pk")
                        ).values("last_visited")[:1]
                    )
                )
                .order_by("-last_visited_at", "title")
            )

            if continue_lecture.exists():
                last_lecture = continue_lecture.first()
                progression = Enrollment.objects.get(
                    student=request.user, course=last_lecture.course
                ).progression

                continue_course = last_lecture.course
                tags = continue_course.tags.all()
                recommended_courses = (
                    Course.objects.filter(tags__in=tags)
                    .exclude(id=continue_course.id)
                    .distinct()[:4]
                )

        # Build context
        context = {
            "new_courses": new_courses,
            "courses": courses,
            "categories": categories,
            "enrolled_courses": enrolled_courses,
            "enrolled_classes": enrolled_courses,  # compatibility
            "teacher_courses": teacher_courses,
            "course_list": featured_courses,        # compatibility
            "active_category": active_category,
            "last_lecture": last_lecture,
            "progression": progression,
            "recommended_courses": recommended_courses,
        }

        # Choose template for HTMX
        if request.headers.get("HX-Request"):
            return render(request, "home/subcategory.html", context)

        return render(request, self.template_name, context)
    
    # @method_decorator(cache_page(60 * 15, key_prefix="home_view"))
    # @method_decorator(vary_on_cookie)
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        import time
        time.sleep(10)
        return super().get_queryset()   

@require_http_methods(["GET"])
def search_view(request):
    query = request.GET.get("search", "").strip()
    highlighted_courses = []
    print(query)

    if query:
        courses = Course.objects.filter(title__icontains=query)
        for course in courses:
            highlighted_title = course.title.replace(query, f"<mark>{query}</mark>")
            highlighted_courses.append(
                {"course": course, "highlighted_title": mark_safe(highlighted_title)}
            )

    print(highlighted_courses)

    return render(
        request,
        "home/search_results.html",
        {"courses": highlighted_courses, "query": query},
    )
