import os
from django.test import TestCase
from mindjunkies.accounts.models import User
import django
from decouple import config

from .models import Course, CourseTeacher, Enrollment

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()


class CourseModelTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            title='Test Course',
            short_introduction='This is a test short introduction',
            course_description='This is a test course description',
            published=True,
            upcoming=False,
            paid_course=False,
            course_price=0.0,
            total_rating=0.0,
            number_of_ratings=0,
        )

    def test_course_creation(self):
        self.assertEqual(self.course.title, 'Test Course')
        self.assertEqual(self.course.course_description, 'This is a test course description')
        self.assertEqual(self.course.published, True)
        self.assertEqual(self.course.upcoming, False)
        self.assertEqual(self.course.paid_course, False)
        self.assertEqual(self.course.course_price, 0.0)
        self.assertEqual(self.course.total_rating, 0.0)
        self.assertEqual(self.course.number_of_ratings, 0)

    def test_course_str(self):
        self.assertEqual(str(self.course), 'Test Course')


class CourseTeacherModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(title="Python 101")
        self.teacher = User.objects.create_user(username="teacher1", password=config("TEST_PASS"),
                                                email="test@mail.com")

    def test_course_teacher_creation(self):
        course_teacher = CourseTeacher.objects.create(course=self.course, teacher=self.teacher, role="teacher")
        self.assertEqual(course_teacher.course, self.course)
        self.assertEqual(course_teacher.teacher, self.teacher)
        self.assertEqual(course_teacher.role, "teacher")

    def test_unique_together_constraint(self):
        CourseTeacher.objects.create(course=self.course, teacher=self.teacher, role="teacher")
        with self.assertRaises(Exception):  # IntegrityError
            CourseTeacher.objects.create(course=self.course, teacher=self.teacher, role="assistant")

    def test_str_method(self):
        course_teacher = CourseTeacher.objects.create(course=self.course, teacher=self.teacher, role="teacher")
        expected_str = f"{self.teacher.username} teaches {self.course.title}"
        self.assertEqual(str(course_teacher), expected_str)


class EnrollmentModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(title="Django Fundamentals")
        self.student = User.objects.create_user(username="student1", password=config("TEST_PASS"),
                                                email="test@gmail.com")

    def test_enrollment_creation(self):
        enrollment = Enrollment.objects.create(course=self.course, student=self.student, status="active")
        self.assertEqual(enrollment.course, self.course)
        self.assertEqual(enrollment.student, self.student)
        self.assertEqual(enrollment.status, "active")

    def test_unique_together_constraint(self):
        Enrollment.objects.create(course=self.course, student=self.student, status="pending")
        with self.assertRaises(Exception):
            Enrollment.objects.create(course=self.course, student=self.student, status="active")

    def test_str_method(self):
        enrollment = Enrollment.objects.create(course=self.course, student=self.student, status="pending")
        expected_str = f"{self.student.username} enrolled in {self.course.title}"
        self.assertEqual(str(enrollment), expected_str)
