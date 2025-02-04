from django.contrib import admin

from .models import Classroom, ClassroomTeacher


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    model = Classroom
    list_display = ("title", "published", "upcoming", "published_on", "paid_course", "course_price")


@admin.register(ClassroomTeacher)
class ClassroomTeacherAdmin(admin.ModelAdmin):
    model = ClassroomTeacher
    list_display = ("classroom", "teacher", "role")
    list_filter = ("role",)

