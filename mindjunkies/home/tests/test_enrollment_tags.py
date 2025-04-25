# mindjunkies/templates/tests/test_filters.py
import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django import template
from django.template import TemplateSyntaxError

from mindjunkies.courses.models import Course, Enrollment

from mindjunkies.home.templatetags.enrollment_tags import get_enrollment

User = get_user_model()

@pytest.mark.django_db
class TestGetEnrollmentFilter(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password",
            email="test@example.com",
        )
        self.teacher = User.objects.create_user(
            username="teacher",
            password="password",
            email="teacher@example.com",
        )
        self.course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_introduction="A short intro",
            course_description="Detailed description",
            teacher=self.teacher,
            level="beginner",
        )
        self.enrollment = Enrollment.objects.create(
            course=self.course,
            student=self.user,
        )

    def test_get_enrollment_exists(self):
        """Test that the filter returns the correct Enrollment object when it exists"""
        result = get_enrollment(self.course, self.user)
        self.assertEqual(result, self.enrollment)
        self.assertEqual(result.course, self.course)
        self.assertEqual(result.student, self.user)

    def test_get_enrollment_does_not_exist(self):
        """Test that the filter returns None when no Enrollment exists"""
        other_user = User.objects.create_user(
            username="otheruser",
            password="password",
            email="other@example.com",
        )
        result = get_enrollment(self.course, other_user)
        self.assertIsNone(result)

    def test_get_enrollment_with_none_course(self):
        """Test that the filter handles None as course gracefully"""
        result = get_enrollment(None, self.user)
        self.assertIsNone(result)

    def test_get_enrollment_with_none_user(self):
        """Test that the filter handles None as user gracefully"""
        result = get_enrollment(self.course, None)
        self.assertIsNone(result)

    def test_template_usage(self):
        """Test the filter in a template context"""
        context = template.Context({
            "course": self.course,
            "user": self.user,
        })
        template_str = "{% load enrollment_tags %}{{ course|get_enrollment:user }}"
        t = template.Template(template_str)
         # Check Enrollment object representation