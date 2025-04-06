from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_http_methods

from mindjunkies.courses.models import Course, CourseCategory, Enrollment


@require_http_methods(["GET"])
def home(request):
    featured_course = Course.objects.all()
    course_categories = CourseCategory.objects.filter(
        parent__isnull=True
    ).prefetch_related("children")
     # Determine active category
    active_category_slug = request.GET.get('category')
    active_category = None
    
    if active_category_slug:
        # Try to get the requested category
        try:
            active_category = CourseCategory.objects.prefetch_related("children").get(
                slug=active_category_slug,
                parent__isnull=True
            )
        except CourseCategory.DoesNotExist:
            pass
    
    # If no active category is specified or found, default to the first one
    if not active_category and course_categories.exists():
        active_category = course_categories.first()
    context = {
        "course_list": featured_course,
        "categories": course_categories,
        "active_category": active_category
    }
    enrolled_classes = []
    teacher_classes = []
    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(
            student=request.user, status="active"
        ).prefetch_related("course")
        enrolled_classes = [ec.course for ec in enrolled]
        context["enrolled_classes"] = enrolled_classes
      # Check if this is an HTMX request
    if request.headers.get('HX-Request'):
        # Return only the subcategories fragment
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

    print(highlighted_courses)

    return render(
        request,
        "home/search_results.html",
        {"courses": highlighted_courses, "query": query},
    )
