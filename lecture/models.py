from django.db import models
from courses.models import Courses
from django.utils.text import slugify

# Model for storing multiple PDFs
class LecturePDF(models.Model):
    lecture = models.ForeignKey('Lecture', on_delete=models.CASCADE, related_name='pdf_files')
    pdf_file = models.FileField(upload_to='lecture_pdfs/')

    def __str__(self):
        return f"PDF for {self.lecture.title}"

# Main Lecture Model (direct title input)
class Lecture(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=255, unique=True)  # Direct input for title
    uploaded_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)  # Auto-generate slug from title
        super().save(*args, **kwargs)

class LectureVideo(models.Model):
    lecture=models.ForeignKey('Lecture',on_delete=models.CASCADE,related_name='video_files')
    video_file=models.FileField(upload_to='lectur_videos/')
