from django.db import models
from mindjunkies.accounts.models import User
from config.models import BaseModel


class TeacherVerification(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the user (teacher)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    portfolio_links = models.TextField(null=True, blank=True)
    important_links = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    social_media = models.TextField(null=True, blank=True)
    certificates = models.ManyToManyField('Certificate', related_name='teacher_verifications')
    verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.full_name


class Certificate(BaseModel):
    image = models.ImageField(upload_to='certificates/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Certificate {self.id}"
