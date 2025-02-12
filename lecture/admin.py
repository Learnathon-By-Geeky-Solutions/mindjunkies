from django.contrib import admin
from .models import Lecture

class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'classroom', 'uploaded_on', 'slug')  # Columns to display in list view
    search_fields = ('title', 'classroom__name')  # Searchable fields
    list_filter = ('classroom', 'uploaded_on')  # Filters for the list view
    prepopulated_fields = {'slug': ('title',)}  # Automatically generate slug based on the title

admin.site.register(Lecture, LectureAdmin)
