from django.db import models
from django.utils.text import slugify

from courses.models import Course, Module
from core.models import BaseModel


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
    video_url = models.URLField(max_length=200, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
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

    def __str__(self):
        return f"PDF for {self.lecture.title}"

class LectureVideo(BaseModel):
    lecture=models.ForeignKey('Lecture',on_delete=models.CASCADE,related_name='videos')
    video_file=models.FileField(upload_to='lecture_videos/')
    def __str__(self):
        return   f"Video content for {self.lecture.title}"  
