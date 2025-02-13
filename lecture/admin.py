from django.contrib import admin
from .models import Lecture, LecturePDF

class LectureAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'classroom', 'uploaded_on', 'slug')  # Display the title directly from the Lecture model
    search_fields = ('title', 'classroom__name')  # Search by title and classroom name
    list_filter = ('classroom', 'uploaded_on')  # Filters for the list view
    prepopulated_fields = {'slug': ('title',)}  # Slug will be auto-generated from the title

    def get_title(self, obj):
        return obj.title if obj.title else "No Title"  # Directly access the title field
    get_title.admin_order_field = 'title'  # Allows sorting by title
    get_title.short_description = 'Lecture Title'  # Rename column header in admin

# Remove the LectureTitleAdmin as it's no longer needed

# Register LecturePDF to allow managing uploaded PDFs
class LecturePDFAdmin(admin.ModelAdmin):
    list_display = ('lecture', 'pdf_file')
    search_fields = ('lecture__title',)  # Search by lecture title

# Register models with the admin site
admin.site.register(Lecture, LectureAdmin)
admin.site.register(LecturePDF, LecturePDFAdmin)
