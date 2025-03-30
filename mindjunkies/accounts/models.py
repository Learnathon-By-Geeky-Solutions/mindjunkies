import uuid

from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.db import models

from config.models import BaseModel
from mindjunkies.courses.models import Rating, Enrollment


class User(AbstractUser):
    """Custom User model with UUID primary key."""

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    def __str__(self):
        return f"{self.username} - {self.email}"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.username

    def get_number_of_reviews(self):
        return Rating.objects.filter(course__teacher=self).count()

    def get_instructor_rating(self):
        courses = self.courses_taught.all()
        total_rating = sum(course.total_rating for course in courses)
        number_of_ratings = self.get_number_of_reviews()
        return total_rating / number_of_ratings if number_of_ratings > 0 else 0

    def get_number_of_students(self):
        return Enrollment.objects.filter(course__teacher=self, status="active").values('student').distinct().count()

    def get_number_of_courses(self):
        return self.courses_taught.count()


class Profile(BaseModel):
    """User profile model storing additional user details."""

    user = models.OneToOneField(
        "accounts.User", on_delete=models.CASCADE, related_name="profile"
    )
    birthday = models.DateField(null=True, blank=True)
    bio = models.TextField()
    avatar = CloudinaryField(
        folder="avatars", overwrite=True, resource_type="image", null=True, blank=True
    )
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
