from django.db import models
from django.db.models import Count
# from django.core.cache import cache
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_http_methods
from django.views import View
import uuid

from mindjunkies.courses.models import Course, CourseCategory, Enrollment, LastVisitedCourse
from mindjunkies.lecture.models import LastVisitedModule, Lecture



# def get_popular_courses(user_uuid):
#     cache_key = f"popular_courses_{user_uuid}"
#     popular_courses = cache.get(cache_key)


#     print("Cache key:", popular_courses)
#     if popular_courses is None:
#         print("Cache miss for popular courses")
#         popular_courses = Course.objects.annotate(
#             active_enrollments=Count('enrollments', filter=models.Q(enrollments__status='active'))
#         ).filter(status="published", verified=True).order_by('-active_enrollments', '-total_rating')
#         print("popular_courses:", popular_courses)

#         popular_courses = list(popular_courses)
#         cache.set(cache_key, popular_courses, timeout=60 * 5)

#     return popular_courses


# def get_new_courses(user_uuid):
#     cache_key = f"new_courses_{user_uuid}"
#     new_courses = cache.get(cache_key)

#     if new_courses is None:
#         print("Cache miss for new courses")
#         new_courses = Course.objects.filter(status="published", verified=True).order_by("-created_at")[:4]
#         new_courses = list(new_courses)
#         cache.set(cache_key, new_courses, timeout=60 * 5)
#     return new_courses


    



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

        user = request.user

        if not user.is_authenticated:
            user_uuid = str(uuid.uuid4())

        else:
            user_uuid = str(user.uuid)

        if request.user.is_authenticated:
            enrollments = Enrollment.objects.filter(
                student=request.user, status="active"
            ).prefetch_related("course").filter(status="published")

            enrolled_courses = [enrollment.course for enrollment in enrollments][:4]
            teacher_courses = Course.objects.filter(teacher=request.user)

        popular_courses = popular_courses = Course.objects.annotate(
            active_enrollments=Count('enrollments', filter=models.Q(enrollments__status='active'))
        ).filter(status="published", verified=True).order_by('-active_enrollments', '-total_rating')
        print("popular_courses:", popular_courses)

        new_courses = new_courses = Course.objects.filter(status="published", verified=True).order_by("-created_at")[:4]



        featured_courses = Course.objects.filter(status="published", verified=True)

        context = {
            "new_courses": new_courses,
            "popular_courses": popular_courses,
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
    print(query)

    if query:
        courses = Course.objects.filter(title__icontains=query)
        print(courses)
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
