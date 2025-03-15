from django.conf import settings
from django.db import models
from django.utils.text import slugify

from mindjunkies.courses.models import Course


class ForumTopic(models.Model):
    """Model for forum topics/threads"""

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="forum_topics"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="forum_topics"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    reaction = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="posts")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_reply_count(self):
        return self.replies.count()

    def get_last_activity(self):
        """Returns the datetime of the most recent activity (post or reply)"""
        latest_reply = self.replies.order_by("-created_at").first()
        if latest_reply:
            return max(latest_reply.created_at, self.updated_at)
        return self.updated_at


class ForumReply(models.Model):
    """Model for replies to forum topics"""

    topic = models.ForeignKey(
        ForumTopic, on_delete=models.CASCADE, related_name="replies"
    )
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="forum_replies"
    )
    parent_reply = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="child_replies",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Simple reaction counter
    like_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = "Forum replies"

    def __str__(self):
        return f"Reply by {self.author.username} on {self.topic.title}"


class ForumNotification(models.Model):
    """Model for forum notifications"""

    NOTIFICATION_TYPES = (
        ("reply", "New Reply"),
        ("mention", "Mention"),
        ("reaction", "Reaction"),
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="forum_notifications",
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    topic = models.ForeignKey(
        ForumTopic, on_delete=models.CASCADE, null=True, blank=True
    )
    reply = models.ForeignKey(
        ForumReply, on_delete=models.CASCADE, null=True, blank=True
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="forum_actions"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.get_notification_type_display()}"
