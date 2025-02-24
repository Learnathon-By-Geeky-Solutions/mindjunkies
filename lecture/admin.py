from django.contrib import admin
from .models import Lecture, LecturePDF


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'is_deleted')
    list_filter = ('course', 'is_deleted')
    search_fields = ('title', 'course__title')
    ordering = ('order',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(LecturePDF)
class LecturePDFAdmin(admin.ModelAdmin):
    list_display = ('lecture', 'pdf_file')
    search_fields = ('lecture__title',)
