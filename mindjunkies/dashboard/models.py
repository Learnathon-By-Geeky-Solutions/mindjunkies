# Create your models here.
from django.db import models
from mindjunkies.accounts.models import User

# Create your models here.
class TeacherVerificationRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    portfolio_link = models.URLField(blank=True, null=True)
    certificates = models.FileField(upload_to="teacher_certificates/", blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Verified: {self.is_verified}"