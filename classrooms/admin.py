from django.contrib import admin

from .models import Classroom, ClassroomTeacher, Enrollment


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    model = Classroom
    list_display = ("title", "published", "published_on", "paid_course", "course_price")


@admin.register(ClassroomTeacher)
class ClassroomTeacherAdmin(admin.ModelAdmin):
    model = ClassroomTeacher
    list_display = ("classroom", "teacher", "role")
    list_filter = ("role",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    model = Enrollment
    list_display = ("classroom", "student", "status")
    list_filter = ("classroom", "status")
