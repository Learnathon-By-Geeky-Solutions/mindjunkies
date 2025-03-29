from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_http_methods

from mindjunkies.courses.models import Course, CourseCategory, Enrollment


@require_http_methods(["GET"])
def home(request):
    if request.user.is_authenticated:
        enrollments = Enrollment.objects.filter(
            student=request.user, status="active"
        ).prefetch_related("course")
        enrolled_courses = [enrollment.course for enrollment in enrollments]
    else:
        enrolled_courses = []

    new_courses = Course.objects.exclude(id__in=[course.id for course in enrolled_courses]).order_by("-created_at")[:3]
    courses = Course.objects.exclude(id__in=new_courses.values_list('id', flat=True)).exclude(
        id__in=[course.id for course in enrolled_courses]
    )

    categories = CourseCategory.objects.filter(parent__isnull=True).prefetch_related("children")

    context = {
        "new_courses": new_courses,
        "courses": courses,
        "categories": categories,
        "enrolled_courses": enrolled_courses,
    }

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

    print(highlighted_courses)

    return render(
        request,
        "home/search_results.html",
        {"courses": highlighted_courses, "query": query},
    )
