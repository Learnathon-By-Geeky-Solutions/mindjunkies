import cloudinary
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from config.models import BaseModel
from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course, Module


class Lecture(BaseModel):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lectures"
    )
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="lectures"
    )

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    learning_objective = models.TextField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["module", "order"], name="unique_order_per_module"
            )
        ]

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if hasattr(self, "module") and self.module and self.order is not None:
            if (
                Lecture.objects.filter(module=self.module, order=self.order)
                .exclude(pk=self.pk)
                .exists()
            ):
                raise ValidationError(
                    f"Order {self.order} already exists in this module."
                )


class LecturePDF(BaseModel):
    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE, related_name="pdf_files"
    )
    pdf_file = models.FileField(upload_to="lecture_pdfs/")
    pdf_title = models.CharField(max_length=255)

    def __str__(self):
        return f"PDF for {self.lecture.title}"


class LectureVideo(BaseModel):
    PENDING = "Pending"
    PROCESSING = "Processing"
    COMPLETED = "Completed"

    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (PROCESSING, "Processing"),
        (COMPLETED, "Completed"),
    )

    lecture = models.ForeignKey(
        "Lecture", on_delete=models.CASCADE, related_name="videos"
    )
    video_file = cloudinary.models.CloudinaryField(resource_type="video")
    video_title = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to="thumbnails", null=True, blank=True)
    hls = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    is_running = models.BooleanField(default=False)

    def __str__(self):
        return str(self.video_title)


class LectureCompletion(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "lecture")


class LastVisitedModule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    video = models.ForeignKey(LectureVideo, on_delete=models.CASCADE, null=True, blank=True)
    last_visited = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-last_visited"]
        unique_together = ["module", "user", "lecture"]

    def __str__(self):
        return f"{self.user.username} - {self.lecture.title} - {self.last_visited}"
