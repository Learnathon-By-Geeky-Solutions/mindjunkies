from django.conf import settings
import uuid
from django.db import models
from django.utils.text import slugify

from mindjunkies.courses.models import Course, Module


class ForumTopic(models.Model):
    """Model for forum topics/threads"""

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    content = models.CharField(max_length=150)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="forum_topics"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="forum_posts"
    )  # Removed trailing comma
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="forum_posts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="likedTopics", through="LikedPost"
    )  # Changed related_name to be unique

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            # Check if slug already exists
            model_class = self.__class__
            if not model_class.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{str(uuid.uuid4())[:8]}"  # Add random 8 chars
            self.slug = slug
        super().save(*args, **kwargs)

    def get_reply_count(self):
        return (
            self.replies.count()
        )  # Ensuring 'replies' is the related_name for ForumReply

    def get_last_activity(self):
        """Returns the datetime of the most recent activity (post or reply)"""
        latest_reply = self.comments.order_by("-created_at").first()
        if latest_reply:
            return max(latest_reply.created_at, self.updated_at)
        return self.updated_at


class LikedPost(models.Model):
    topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} : {self.topic.content[:30]}"


class ForumComment(models.Model):
    """Model for replies to forum topics"""

    topic = models.ForeignKey(
        ForumTopic, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.CharField(max_length=150)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="forum_comments",
    )

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="likedComments", through="LikedComment"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = "Forum Comment"

    def __str__(self):
        return f"Reply by {self.author.username} on {self.topic.title}"


class LikedComment(models.Model):
    comment = models.ForeignKey(ForumComment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} : {self.comment.body[:30]}"


class Reply(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="replies",
    )
    parent_comment = models.ForeignKey(
        ForumComment,
        on_delete=models.CASCADE,
        related_name="replies",
        null=True,
        blank=True,
    )
    parent_reply = models.ForeignKey(
        "Reply", on_delete=models.CASCADE, related_name="replies", null=True, blank=True
    )
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="likedreplies", through="LikedReply"
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} : {self.body[:30]}"

    class Meta:
        ordering = ["created"]


class LikedReply(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} : {self.reply.body[:30]}"
