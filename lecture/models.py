from django.db import models
from classrooms.models import Classroom
from django.utils.text import slugify
class Lecture(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='lecture_pdfs/', blank=True, null=True)  # Single PDF Upload
    uploaded_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class LectureTitle(models.Model):
    lecture=models.ForeignKey(Lecture,on_delete=models.CASCADE,related_name='lectureTitle')
    title = models.CharField(max_length=255)
    def __str__(self):
        return self.title