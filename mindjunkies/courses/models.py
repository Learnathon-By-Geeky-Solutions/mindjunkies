import cloudinary
import cloudinary.uploader
from categories.models import CategoryBase
from cloudinary.models import CloudinaryField
from django.db import models
from django.utils.text import slugify

from config.models import BaseModel
from taggit.managers import TaggableManager

user = "accounts.User"


class CourseCategory(CategoryBase):
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Course Categories"

    def __str__(self):
        return self.name


class Course(BaseModel):
    """Model for storing course details."""

    slug = models.SlugField(max_length=255, unique=True)

    LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]
    title = models.CharField(max_length=255)
    short_introduction = models.CharField(max_length=500)
    course_description = models.TextField()
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES, default="beginner")
    category = models.ForeignKey(
        CourseCategory, on_delete=models.SET_NULL, related_name="courses", null=True
    )

    teacher = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="courses_taught"
    )

    course_image = CloudinaryField(
        folder="course_images/",
        resource_type="image",
        overwrite=True,
        null=True,
        blank=True,
    )

    published = models.BooleanField(default=False)
    published_on = models.DateTimeField(null=True, blank=True)

    paid_course = models.BooleanField(default=False)
    course_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    upcoming = models.BooleanField(default=False)

    preview_video = models.URLField(max_length=200, blank=True, default="")

    total_rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    number_of_ratings = models.PositiveIntegerField(default=0)

    # Tags for the course
    tags = TaggableManager(blank=True)    

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.teacher:
            raise ValueError("Teacher is required.")
        super().save(*args, **kwargs)

    def update_rating(self):
        """Recalculate average course rating."""
        ratings = self.ratings.all()
        self.number_of_ratings = ratings.count()
        self.total_rating = (
            sum(r.rating for r in ratings) / self.number_of_ratings
            if self.number_of_ratings > 0
            else 0
        )
        self.save(update_fields=["total_rating", "number_of_ratings"])

    def get_total_enrollments(self):
        """Get total number of enrollments for the course."""
        return self.enrollments.filter(status="active").count()

    def get_rating_distribution(self):
        ratings = self.ratings.values("rating").annotate(count=models.Count("rating"))
        total_ratings = self.number_of_ratings
        distribution = {i: 0 for i in range(1, 6)}
        for rating in ratings:
            distribution[rating["rating"]] = (rating["count"] / total_ratings) * 100
        return distribution

    def get_individual_ratings(self):
        return self.ratings.select_related("student").all()


class CourseInfo(BaseModel):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name="info")
    what_you_will_learn = models.TextField()
    who_this_course_is_for = models.TextField()
    requirements = models.TextField()

    def __str__(self):
        return self.course.title + " - Course Info"


class Rating(BaseModel):
    """Stores ratings and reviews for courses."""

    student = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name="ratings")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="ratings")
    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)], default=5  # 1 to 5 stars
    )
    review = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("student", "course")
        indexes = [models.Index(fields=["course"])]

    def __str__(self):
        return f"{self.student.username} rated {self.course.title} {self.rating}/5"

    def save(self, *args, **kwargs):
        """Update course rating when a new rating is saved."""
        super().save(*args, **kwargs)
        self.course.update_rating()


class Enrollment(BaseModel):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("pending", "Pending"),
        ("withdrawn", "Withdrawn"),
    ]

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments"
    )
    student = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="enrolled"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    class Meta:
        unique_together = ["course", "student"]

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Module(BaseModel):
    title = models.CharField(max_length=255)
    details = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    order = models.PositiveIntegerField(default=0)

    class Meta: 
        ordering = ["order"]

    def __str__(self):
        return f"{self.title} - {self.course.title}"


class CourseToken(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="tokens")
    teacher = models.ForeignKey(user, on_delete=models.CASCADE)
    motivation = models.TextField(
        help_text="Write your motivation or plan for the course, including how you plan to organize it.")
    intro_video = CloudinaryField(resource_type='video', default="")
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('approved', 'Approved')],
                              default='pending')

    def __str__(self):
        return f"Token for {self.course.title} by {self.teacher.username}"


class LastVisitedCourse(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    last_visited = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-last_visited"]
        unique_together = ["course", "user"]

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.last_visited}"
