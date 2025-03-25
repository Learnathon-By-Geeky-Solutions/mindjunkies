from categories.admin import CategoryBaseAdmin
from django.contrib import admin

from .models import Course, CourseCategory, CourseTeacher, Enrollment, Module, CourseToken


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    model = Course
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


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    model = Module
    list_display = ("title", "course", "order")
    list_filter = ("course",)


@admin.register(CourseCategory)
class CourseCategoryAdmin(CategoryBaseAdmin):
    pass


@admin.register(CourseToken)
class CourseTokeneAdmin(admin.ModelAdmin):
    model = CourseToken
    list_display = ("user", "course", "status")
    list_filter = ("course",)
