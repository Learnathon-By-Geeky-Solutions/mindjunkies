from django.contrib import admin

from .models import ForumNotification, ForumReply, ForumTopic


@admin.register(ForumTopic)
class ForumTopicAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "course", "created_at")
    search_fields = ("title", "content", "author__username", "course__title")
    list_filter = ("created_at", "course")
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("author", "course")


@admin.register(ForumReply)
class ForumReplyAdmin(admin.ModelAdmin):
    list_display = ("topic", "author", "created_at", "like_count")
    search_fields = ("content", "author__username", "topic__title")
    list_filter = ("created_at",)
    raw_id_fields = ("author", "topic", "parent_reply")


@admin.register(ForumNotification)
class ForumNotificationAdmin(admin.ModelAdmin):
    list_display = ("recipient", "notification_type", "actor", "created_at", "is_read")
    search_fields = (
        "recipient__username",
        "actor__username",
        "topic__title",
        "reply__content",
    )
    list_filter = ("notification_type", "created_at", "is_read")
    raw_id_fields = ("recipient", "actor", "topic", "reply")
