import uuid

from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.db import models

from config.models import BaseModel
from mindjunkies.courses.models import Enrollment, Rating


class User(AbstractUser):
    """Custom User model with UUID primary key."""

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    REQUIRED_FIELDS = ["email", "first_name", "last_name"]
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} - {self.email}"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def get_number_of_reviews(self):
        return self._get_reviews_queryset().count()

    def _get_reviews_queryset(self):
        return Rating.objects.filter(course__teacher=self)

    def get_instructor_rating(self):
        courses = self._get_courses_taught()
        number_of_ratings = self.get_number_of_reviews()

        if number_of_ratings == 0:
            return 0

        total_rating = sum(course.total_rating for course in courses)
        return total_rating / number_of_ratings

    def _get_courses_taught(self):
        return self.courses_taught.all()

    def get_number_of_students(self):
        return (
            Enrollment.objects.filter(course__teacher=self, status="active")
            .values("student")
            .distinct()
            .count()
        )

    def get_number_of_courses(self):
        return self.courses_taught.count()


class Profile(BaseModel):
    """User profile model storing additional user details."""

    user = models.OneToOneField(
        "accounts.User", on_delete=models.CASCADE, related_name="profile"
    )
    birthday = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    avatar = CloudinaryField(
        folder="avatars", overwrite=True, resource_type="image", null=True, blank=True
    )
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
