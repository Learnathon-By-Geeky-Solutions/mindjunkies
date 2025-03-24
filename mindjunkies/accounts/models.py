import uuid

from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from config.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    REQUIRED_FIELDS = ["email", "first_name", "last_name"]
    is_teacher = models.BooleanField(default=False)
    objects = UserManager()

    def __str__(self):
        return f"{self.username} - {self.email}"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"


class Profile(BaseModel):
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
