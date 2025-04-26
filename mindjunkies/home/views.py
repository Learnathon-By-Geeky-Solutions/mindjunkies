from django.db import models
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_http_methods
from django.views import View

from mindjunkies.courses.models import Course, CourseCategory, Enrollment, LastVisitedCourse
from mindjunkies.lecture.models import LastVisitedModule, Lecture


class HomeView(View):
    def get(self, request):
        categories = CourseCategory.objects.filter(parent__isnull=True).prefetch_related("children")

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

        enrolled_courses = []
        teacher_courses = []

        if request.user.is_authenticated:
            enrollments = Enrollment.objects.filter(
                student=request.user, status="active"
            ).prefetch_related("course")

            enrolled_courses = [enrollment.course for enrollment in enrollments]
            teacher_courses = Course.objects.filter(teacher=request.user)

        new_courses = Course.objects.exclude(
            id__in=[course.id for course in enrolled_courses]
        ).order_by("-created_at")

        courses = Course.objects.exclude(
            id__in=new_courses.values_list("id", flat=True)
        ).exclude(id__in=[course.id for course in enrolled_courses])

        featured_courses = Course.objects.filter(status="published")

        progression = None
        last_lecture = None
        lastvisitedmodule = None

        if request.user.is_authenticated:
            lastvisitedmodule = LastVisitedModule.objects.filter(
                user=request.user, lecture__course__in=enrolled_courses
            ).order_by("-last_visited").first()

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


        context = {
            "new_courses": new_courses,
            "courses": courses,
            "categories": categories,
            "enrolled_courses": enrolled_courses,
            "enrolled_classes": enrolled_courses,
            "teacher_courses": teacher_courses,
            "course_list": featured_courses,
            "active_category": active_category,
            "last_lecture": last_lecture,
            "progression": progression,
            "lastvisitedmodule": lastvisitedmodule,
        }

        if request.headers.get("HX-Request"):
            return render(request, "home/subcategory.html", context)

        return render(request, "home/index.html", context)
    


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
