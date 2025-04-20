from categories.admin import CategoryBaseAdmin
from django.contrib import admin

from mindjunkies.courses.models import Course, CourseCategory, Enrollment

from .models import CourseToken, LastVisitedCourse, Module, Rating


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_display = (
        "title",
        "teacher",
        "status",
        "published_on",
        "paid_course",
        "course_price",
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    model = Enrollment
    list_display = ("course", "student", "status")
    list_filter = ("course", "status")


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    model = Module
    list_display = ("title", "course", "order")
    list_filter = ("course",)


@admin.register(CourseCategory)
class CourseCategoryAdmin(CategoryBaseAdmin):
    pass


@admin.register(CourseToken)
class CourseTokenAdmin(admin.ModelAdmin):
    model = CourseToken
    list_display = ("teacher", "course", "status")
    list_filter = ("course",)


@admin.register(LastVisitedCourse)
class LastVisitedCourseAdmin(admin.ModelAdmin):
    model = LastVisitedCourse
    list_display = ("user", "course")
    list_filter = ("course",)
    search_fields = ("user__username", "course__title")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    model = Rating
    list_display = ("student", "course", "rating", "created_at")
    list_filter = ("course", "rating")
    search_fields = ("student__username", "course__title")
    raw_id_fields = ("student", "course")
