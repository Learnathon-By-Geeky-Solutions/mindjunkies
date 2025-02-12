from django.db import models
from classrooms.models import Classroom
from django.utils.text import slugify

# Predefined Lecture Titles
class LectureTitle(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title

# Model for storing multiple PDFs
class LecturePDF(models.Model):
    lecture = models.ForeignKey('Lecture', on_delete=models.CASCADE, related_name='pdf_files')
    pdf_file = models.FileField(upload_to='lecture_pdfs/')

    def __str__(self):
        return f"PDF for {self.lecture.title}"

# Main Lecture Model
class Lecture(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='lectures')
    title = models.ForeignKey(LectureTitle, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.title.title if self.title else "No Title"

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title.title)
        super().save(*args, **kwargs)
