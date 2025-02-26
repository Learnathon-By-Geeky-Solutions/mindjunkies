import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from django.test import TestCase
from django.utils.text import slugify
from courses.models import Courses
from lecture.models import Lecture

class LectureModelTest(TestCase):
    def setUp(self):
        self.course = Courses.objects.create(title="Django Basics")

    def test_lecture_creation(self):
        lecture = Lecture.objects.create(course=self.course, title="Introduction to Django")
        self.assertEqual(lecture.course, self.course)
        self.assertEqual(lecture.title, "Introduction to Django")

    def test_unique_title_constraint(self):
        Lecture.objects.create(course=self.course, title="Django ORM")
        with self.assertRaises(Exception):
            Lecture.objects.create(course=self.course, title="Django ORM")

    def test_slug_auto_generation(self):
        lecture = Lecture.objects.create(course=self.course, title="Django Testing")
        self.assertEqual(lecture.slug, slugify("Django Testing"))

    def test_str_method(self):
        lecture = Lecture.objects.create(course=self.course, title="Django Views")
        self.assertEqual(str(lecture), "Django Views")
