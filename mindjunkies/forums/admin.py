from django.contrib import admin

from .models import  ForumComment, ForumTopic


@admin.register(ForumTopic)
class ForumTopicAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "course","module", "created_at")
    search_fields = ("title", "content", "author__username", "course__title")
    list_filter = ("created_at", "course")
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("author", "course")


@admin.register(ForumComment)
class ForumReplyAdmin(admin.ModelAdmin):
    list_display = ("topic", "author", "created_at")
    search_fields = ("content", "author__username", "topic__title")
    list_filter = ("created_at",)
    raw_id_fields = ("author", "topic")



