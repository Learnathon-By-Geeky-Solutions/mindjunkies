from django.db import models
from django.utils.text import slugify

from mindjunkies.courses.models import Course, Module
from config.models import BaseModel


class Lecture(BaseModel):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lectures'
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='lectures'
    )

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    learning_objective = models.TextField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class LecturePDF(BaseModel):
    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        related_name='pdf_files'
    )
    pdf_file = models.FileField(upload_to='lecture_pdfs/')
    pdf_title = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"PDF for {self.lecture.title}"


class LectureVideo(BaseModel):
    PENDING = 'Pending'
    PROCESSING = 'Processing'
    COMPLETED = 'Completed'

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (COMPLETED, 'Completed'),
    )
    lecture = models.ForeignKey('Lecture', on_delete=models.CASCADE, related_name='videos')
    video_file = models.FileField(upload_to='lecture_videos/')
    video_title = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to="thumbnails", null=True, blank=True)
    hls = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    is_running = models.BooleanField(default=False)

    def __str__(self):
        return str(self.video_title)
