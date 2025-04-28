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
        if active_category_slug:
            active_category = CourseCategory.objects.prefetch_related("children").get(
                slug=active_category_slug, parent__isnull=True
            )
        else:
            active_category = CourseCategory.objects.first()

        enrolled_courses = []
        teacher_courses = []

        if request.user.is_authenticated:
            enrollments = Enrollment.objects.filter(
                student=request.user, status="active"
            ).prefetch_related("course").filter(status="published")

            enrolled_courses = [enrollment.course for enrollment in enrollments][:4]
            teacher_courses = Course.objects.filter(teacher=request.user)

        new_courses = Course.objects.exclude(
            id__in=[course.id for course in enrolled_courses]
        ).order_by("-created_at").filter(status="published", verified=True)[:4]

        courses = Course.objects.exclude(
            id__in=new_courses.values_list("id", flat=True)
        ).exclude(id__in=[course.id for course in enrolled_courses]).filter(status="published", verified=True)[:4]

        featured_courses = Course.objects.filter(status="published", verified=True)

        context = {
            "new_courses": new_courses,
            "courses": courses,
            "categories": categories,
            "enrolled_courses": enrolled_courses,
            "enrolled_classes": enrolled_courses,
            "teacher_courses": teacher_courses,
            "course_list": featured_courses,
            "active_category": active_category,
        }

        if request.headers.get("HX-Request"):
            return render(request, "home/subcategory.html", context)

        return render(request, "home/index.html", context)


@require_http_methods(["GET"])
def search_view(request):
    query = request.GET.get("search", "").strip()
    highlighted_courses = []

    if query:
        courses = Course.objects.filter(title__icontains=query)
        for course in courses:
            highlighted_title = course.title.replace(query, f"<mark>{query}</mark>")
            highlighted_courses.append(
                {"course": course, "highlighted_title": mark_safe(highlighted_title)}
            )

    return render(
        request,
        "home/search_results.html",
        {"courses": highlighted_courses, "query": query},
    )
