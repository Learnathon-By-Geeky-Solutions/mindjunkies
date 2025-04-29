from django.contrib import admin
from unfold.admin import ModelAdmin

from mindjunkies.courses.models import Course, CourseCategory, Enrollment

from .models import CourseToken, LastVisitedCourse, Module, Rating


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    model = Course
    list_display = (
        "title",
        "teacher",
        "status",
        "published_on",
        "paid_course",
        "course_price",
        "verified",
        "get_tags",
        "average_rating",
        "total_enrollments",
    )

    def get_tags(self, obj):
        return ", ".join(o.name for o in obj.tags.all())
    
    def average_rating(self, obj):
        """Show the average rating rounded to 2 decimal places."""
        return round(obj.total_rating, 2)

    average_rating.short_description = "Avg. Rating"

    def total_enrollments(self, obj):
        """Show total number of enrollments."""
        return obj.get_total_enrollments()

    total_enrollments.short_description = "Enrollments"


@admin.register(Enrollment)
class EnrollmentAdmin(ModelAdmin):
    model = Enrollment
    list_display = ("course", "student", "status")
    list_filter = ("course", "status")


@admin.register(Module)
class ModuleAdmin(ModelAdmin):
    model = Module
    list_display = ("title", "course", "order")
    list_filter = ("course",)


@admin.register(CourseCategory)
class CourseCategoryAdmin(ModelAdmin):
    model = CourseCategory
    list_display = ("name", "slug")


@admin.register(CourseToken)
class CourseTokenAdmin(ModelAdmin):
    model = CourseToken
    list_display = ("teacher", "course", "status")
    list_filter = ("course",)
    actions = ["approve_course", "disapprove_course"]

    def approve_course(self, request, queryset):
        for obj in queryset:
            obj.status = 'approved'
            obj.save()
            obj.course.verified = True
            obj.course.save()

    approve_course.short_description = "Approve selected Course"

    def disapprove_course(self, request, queryset):
        for obj in queryset:
            obj.status = 'pending'
            obj.save()
            obj.course.verified = False
            obj.course.save()

    disapprove_course.short_description = "Disapprove selected Course"


@admin.register(LastVisitedCourse)
class LastVisitedCourseAdmin(ModelAdmin):
    model = LastVisitedCourse
    list_display = ("user", "course")
    list_filter = ("course",)
    search_fields = ("user__username", "course__title")


@admin.register(Rating)
class RatingAdmin(ModelAdmin):
    model = Rating
    list_display = ("student", "course", "rating", "created_at")
    list_filter = ("course", "rating")
    search_fields = ("student__username", "course__title")
    raw_id_fields = ("student", "course")
