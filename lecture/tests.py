from django.test import TestCase
from django.utils.text import slugify
from courses.models import Course, Module
from .models import Lecture, LecturePDF, LectureVideo
from django.core.files.uploadedfile import SimpleUploadedFile

# Constants
COURSE_TITLE = "Advanced Python Course"
MODULE_TITLE = "Introduction to Django"
LECTURE_TITLE = "Django ORM Basics"
LECTURE_DESC = "An overview of Django's ORM capabilities."
PDF_TITLE = "Lecture Notes"
PDF_FILE_NAME = "lecture_notes.pdf"
VIDEO_TITLE = "Django ORM Walkthrough"
VIDEO_FILE_NAME = "django_tutorial.mp4"
VIDEO_CONTENT = b"video content"
PDF_CONTENT = b"PDF content"


class LectureModelTest(TestCase):
    def setUp(self):
        self.sample_course = Course.objects.create(title=COURSE_TITLE)
        self.sample_module = Module.objects.create(title=MODULE_TITLE, course=self.sample_course)
        self.sample_lecture = Lecture.objects.create(
            course=self.sample_course,
            module=self.sample_module,
            title=LECTURE_TITLE,
            description=LECTURE_DESC,
            order=1
        )

    def test_lecture_creation(self):
        self.assertEqual(self.sample_lecture.title, LECTURE_TITLE)
        self.assertEqual(self.sample_lecture.course, self.sample_course)
        self.assertEqual(self.sample_lecture.module, self.sample_module)
        self.assertEqual(self.sample_lecture.order, 1)

    def test_slug_generation_on_save(self):
        self.assertEqual(self.sample_lecture.slug, slugify(LECTURE_TITLE))

    def test_str_representation(self):
        self.assertEqual(str(self.sample_lecture), f"{self.sample_course.title} - {LECTURE_TITLE}")


class LecturePDFModelTest(TestCase):
    def setUp(self):
        self.sample_course = Course.objects.create(title=COURSE_TITLE)
        self.sample_module = Module.objects.create(title=MODULE_TITLE, course=self.sample_course)
        self.sample_lecture = Lecture.objects.create(
            course=self.sample_course,
            module=self.sample_module,
            title=LECTURE_TITLE
        )
        self.sample_pdf = LecturePDF.objects.create(
            lecture=self.sample_lecture,
            pdf_file=SimpleUploadedFile(PDF_FILE_NAME, PDF_CONTENT),
            pdf_title=PDF_TITLE
        )

    def test_pdf_creation(self):
        self.assertEqual(self.sample_pdf.lecture, self.sample_lecture)
        self.assertEqual(self.sample_pdf.pdf_title, PDF_TITLE)

    def test_str_representation(self):
        self.assertEqual(str(self.sample_pdf), f"PDF for {self.sample_lecture.title}")


class LectureVideoModelTest(TestCase):
    def setUp(self):
        self.sample_course = Course.objects.create(title=COURSE_TITLE)
        self.sample_module = Module.objects.create(title=MODULE_TITLE, course=self.sample_course)
        self.sample_lecture = Lecture.objects.create(
            course=self.sample_course,
            module=self.sample_module,
            title=LECTURE_TITLE
        )
        self.sample_video = LectureVideo.objects.create(
            lecture=self.sample_lecture,
            video_file=SimpleUploadedFile(VIDEO_FILE_NAME, VIDEO_CONTENT),
            video_title=VIDEO_TITLE,
            status=LectureVideo.PENDING,
            is_running=False
        )

    def test_video_creation(self):
        self.assertEqual(self.sample_video.lecture, self.sample_lecture)
        self.assertEqual(self.sample_video.video_title, VIDEO_TITLE)
        self.assertEqual(self.sample_video.status, LectureVideo.PENDING)
        self.assertFalse(self.sample_video.is_running)

    def test_str_representation(self):
        self.assertEqual(str(self.sample_video), VIDEO_TITLE)
