from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

from config.models import BaseModel
from mindjunkies.accounts.models import User


class Course(BaseModel):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    title = models.CharField(max_length=255)
    short_introduction = models.CharField(max_length=500)
    course_description = models.TextField()
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES, default='beginner')

    course_image = CloudinaryField(
        folder='course_images/',
        resource_type="image",
        overwrite=True,
        null=True,
        blank=True
    )
    preview_video_link = models.URLField(max_length=200, blank=True, default='')

    published = models.BooleanField(default=False)
    upcoming = models.BooleanField(default=False)
    published_on = models.DateTimeField(null=True, blank=True)
    paid_course = models.BooleanField(default=False)
    course_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    slug = models.SlugField(max_length=255, unique=True)
    total_rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    number_of_ratings = models.PositiveIntegerField(default=0)
    number_of_enrollments = models.PositiveIntegerField(default=0)

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


class CourseRequirement(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='requirements')
    requirement = models.CharField(max_length=255)

    def __str__(self):
        return self.requirement


class CourseObjective(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='objectives')
    objective = models.CharField(max_length=255)

    def __str__(self):
        return self.objective


class CourseTeacher(BaseModel):
    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('assistant', 'Teaching Assistant'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='teachers')
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='teaching_roles'
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='teacher')

    class Meta:
        unique_together = ['course', 'teacher']

    def __str__(self):
        return f"{self.teacher.username} teaches {self.course.title}"


class Enrollment(BaseModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('withdrawn', 'Withdrawn'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrolled'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ['course', 'student']

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"
    
    def save(self, *args, **kwargs):
        if self.pk is None:  # Check if the enrollment is being created
            self.course.number_of_enrollments += 1
            self.course.save()
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk is None:
            print("course name is", self.course)
            self.course.number_of_enrollments += 1
            self.course.save()
        super().save(*args, **kwargs)


class Module(BaseModel):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} - {self.course.title}"
