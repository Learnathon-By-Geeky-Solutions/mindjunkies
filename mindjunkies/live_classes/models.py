import os
import uuid

from django.conf import settings
from django.db import models

from config.jass_jwt import JaaSJwtBuilder
from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course


class LiveClass(models.Model):
    STATUS_CHOICES = [
        ("Upcoming", "Upcoming"),
        ("Ongoing", "Ongoing"),
        ("Completed", "Completed"),
    ]

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="live_classes"
    )
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="live_classes"
    )
    topic = models.CharField(max_length=255)
    meeting_id = models.CharField(
        max_length=50, unique=True, blank=True
    )  # Unique Jitsi meeting ID
    scheduled_at = models.DateTimeField()
    duration = models.IntegerField(default=60)  # Duration in minutes
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Upcoming")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.meeting_id:
            self.meeting_id = (
                f"mindjunkies-{uuid.uuid4().hex[:10]}"  # Unique meeting ID
            )
        super().save(*args, **kwargs)

    def generate_jwt_token(self):
        try:
            script_dir = os.path.dirname(__file__)
            fp = os.path.join(script_dir, "private.pem")

            with open(fp) as reader:
                jaas_jwt = JaaSJwtBuilder()

                token = (
                    jaas_jwt.with_defaults()
                    .with_api_key(settings.JITSI_SECRET)
                    .with_user_name(self.teacher.username)
                    .with_user_email(self.teacher.email)
                    .with_moderator(True)
                    .with_app_id(settings.JITSI_APP_ID)
                    .with_user_avatar("")
                    .sign_with(reader.read())
                )
                return token.decode()
        except Exception as e:
            print("Error generating jwt token: ", e)

    def get_meeting_url_teacher(self):
        """Return the secure Jitsi meeting URL with JWT authentication."""

        token = self.generate_jwt_token()
        return f"https://8x8.vc/{settings.JITSI_APP_ID}/{self.meeting_id}?jwt={token}"

    def get_meeting_url_student(self):
        return f"https://8x8.vc/{settings.JITSI_APP_ID}/{self.meeting_id}"

    def __str__(self):
        return f"{self.topic} - {self.course.title} ({self.scheduled_at})"
