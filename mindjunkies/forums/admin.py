from django.contrib import admin

from .models import ForumComment, ForumTopic, LikedPost, Reply


@admin.register(ForumTopic)
class ForumTopicAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "course", "module", "created_at")
    search_fields = ("title", "content", "author__username", "course__title")
    list_filter = ("created_at", "course")
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("author", "course")


@admin.register(ForumComment)
class ForumCommentAdmin(admin.ModelAdmin):
    list_display = ("topic", "author", "created_at")
    search_fields = ("content", "author__username", "topic__title")
    list_filter = ("created_at",)
    raw_id_fields = ("author", "topic")


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ("parent_comment", "body", "author", "created")
    search_fields = ("body", "author__username", "parent_comment__id")
    list_filter = ("created", "parent_comment")
    raw_id_fields = ("author", "parent_comment")


@admin.register(LikedPost)
class LikedPostAdmin(admin.ModelAdmin):
    list_display = ("topic", "user", "created")
    list_filter = ("created", "user")
    search_fields = ("topic__title", "user__username")
