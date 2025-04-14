from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Lecture, LecturePDF, LectureVideo, LectureCompletion


@admin.register(Lecture)
class LectureAdmin(ModelAdmin):
    list_display = ("title", "course", "order", "deleted_at")
    list_filter = ("course", "deleted_at")
    search_fields = ("title", "course__title")
    ordering = ("order",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(LecturePDF)
class LecturePDFAdmin(ModelAdmin):
    list_display = ("lecture", "pdf_file")
    search_fields = ("lecture__title",)


@admin.register(LectureVideo)
class LectureVideoAdmin(ModelAdmin):
    list_display = ("video_title", "lecture", "video_file", "status", "is_running")
    search_fields = ("lecture__title",)



@admin.register(LectureCompletion)
class LectureCompletionAdmin(ModelAdmin):
    list_display = ("user", "lecture", "completed_at")
    search_fields = ("user__username", "lecture__title")
    list_filter = ("completed_at",)