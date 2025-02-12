from django.contrib import admin
from .models import Lecture, LectureTitle, LecturePDF

class LectureAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'classroom', 'uploaded_on', 'slug')  # Display the title from LectureTitle
    search_fields = ('title__title', 'classroom__name')  # Search by title (from LectureTitle) and classroom
    list_filter = ('classroom', 'uploaded_on')  # Filters for the list view
    prepopulated_fields = {'slug': ('title',)}  # Slug will be auto-generated from the LectureTitle

    def get_title(self, obj):
        return obj.title.title if obj.title else "No Title"  # Ensure title is displayed properly
    get_title.admin_order_field = 'title__title'  # Allows sorting by title
    get_title.short_description = 'Lecture Title'  # Rename column header in admin

# Register LectureTitle separately so titles can be managed
class LectureTitleAdmin(admin.ModelAdmin):
    list_display = ('title',)  # Show available titles in admin
    search_fields = ('title',)

# Register LecturePDF to allow managing uploaded PDFs
class LecturePDFAdmin(admin.ModelAdmin):
    list_display = ('lecture', 'pdf_file')
    search_fields = ('lecture__title__title',)

admin.site.register(Lecture, LectureAdmin)
admin.site.register(LectureTitle, LectureTitleAdmin)
admin.site.register(LecturePDF, LecturePDFAdmin)
