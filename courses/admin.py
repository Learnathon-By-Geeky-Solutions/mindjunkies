from django.contrib import admin

from .models import Courses, CourseTeacher, Enrollment


@admin.register(Courses)
class CourseAdmin(admin.ModelAdmin):
    model = Courses
    list_display = ("title", "published", "published_on", "paid_course", "course_price")


@admin.register(CourseTeacher)
class CourseTeacherAdmin(admin.ModelAdmin):
    model = CourseTeacher
    list_display = ("course", "teacher", "role")
    list_filter = ("role",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    model = Enrollment
    list_display = ("course", "student", "status")
    list_filter = ("course", "status")
