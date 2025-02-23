from django.db import models
from django.utils.text import slugify
from core.models import BaseModel
from accounts.models import User


class Classroom(BaseModel):
    title = models.CharField(max_length=255)
    short_introduction = models.CharField(max_length=500)
    course_description = models.TextField()
    course_image = models.ImageField(upload_to='course_images/', default='course_images/default.jpg', null=True, blank=True)
    preview_video_link = models.URLField(max_length=200, null=True, blank=True)

    published = models.BooleanField(default=False)
    upcoming = models.BooleanField(default=False)
    published_on = models.DateTimeField(null=True, blank=True)
    paid_course = models.BooleanField(default=False)
    course_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
   
    slug = models.SlugField(max_length=255, unique=True)
    total_rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    number_of_ratings = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def average_rating(self):
        if self.number_of_ratings > 0:
            return self.total_rating / self.number_of_ratings
        return 0.0

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_teachers(self):
        return self.teachers.all()


class ClassroomTeacher(BaseModel):
    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('assistant', 'Teaching Assistant'),
    ]
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='teachers')
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'},
        related_name='teaching_roles'
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='teacher')

    class Meta:
        unique_together = ['classroom', 'teacher']

    def __str__(self):
        return f"{self.teacher.username} teaches {self.classroom.title}"


class Enrollment(BaseModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('withdrawn', 'Withdrawn'),
    ]

    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='enrolled'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ['classroom', 'student']

    def __str__(self):
        return f"{self.student.username} enrolled in {self.classroom.title}"
