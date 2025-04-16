from django.db import models
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_http_methods

from mindjunkies.courses.models import Course, CourseCategory, Enrollment, LastVisitedCourse
from mindjunkies.lecture.models import LastVisitedModule, Lecture


@require_http_methods(["GET"])
def home(request):
    # Get course categories with their children
    categories = CourseCategory.objects.filter(parent__isnull=True).prefetch_related(
        "children"
    )

    # Determine active category
    active_category_slug = request.GET.get("category")
    active_category = None

    if active_category_slug:
        # Try to get the requested category
        try:
            active_category = CourseCategory.objects.prefetch_related("children").get(
                slug=active_category_slug, parent__isnull=True
            )
        except CourseCategory.DoesNotExist:
            pass

    # If no active category is specified or found, default to the first one
    if not active_category and categories.exists():
        active_category = categories.first()

    # Handle enrolled courses for authenticated users
    enrolled_courses = []
    teacher_courses = []

    if request.user.is_authenticated:
        # Get user's enrolled courses
        enrollments = Enrollment.objects.filter(
            student=request.user, status="active"
        ).prefetch_related("course")
        enrolled_courses = [enrollment.course for enrollment in enrollments]

        # Get courses taught by the user if they're a teacher
        teacher_courses = Course.objects.filter(teacher=request.user)

    # Get new courses (excluding enrolled ones)
    new_courses = Course.objects.exclude(
        id__in=[course.id for course in enrolled_courses]
    ).order_by("-created_at")[:3]

    # Get other courses (excluding new ones and enrolled ones)
    courses = Course.objects.exclude(
        id__in=new_courses.values_list("id", flat=True)
    ).exclude(id__in=[course.id for course in enrolled_courses])

    # Get featured courses (you might want to define criteria for this)
    featured_courses = Course.objects.filter(published=True)
    progression = 0

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
            progression = Enrollment.objects.get(student=request.user, course=last_lecture.course).progression
        else:
            last_lecture = None
            progression = None

    else:
        last_lecture = None

        


    # Build the context
    context = {
        "new_courses": new_courses,
        "courses": courses,
        "categories": categories,
        "enrolled_courses": enrolled_courses,
        "enrolled_classes": enrolled_courses,  # For compatibility with second version
        "teacher_courses": teacher_courses,
        "course_list": featured_courses,  # For compatibility with second version
        "active_category": active_category,
        'last_lecture': last_lecture,
        'progression': progression,
    }

    # Check if this is an HTMX request
    if request.headers.get("HX-Request"):
        # Return only the subcategories fragment
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

