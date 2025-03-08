from django.contrib import admin

from .models import LiveClass

@admin.register(LiveClass)
class LiveClassAdmin(admin.ModelAdmin):
    list_display = ["course", "topic", "teacher", "scheduled_at", "duration", "status"]
    list_filter = ["course", "teacher", "status"]
    search_fields = ["course__title", "topic", "teacher__username"]
    date_hierarchy = "scheduled_at"
