from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from mindjunkies.home.views import home
from mindjunkies.courses.models import Course, Enrollment, CourseTeacher

User = get_user_model()  # Use custom User model

class HomeViewTest(TestCase):
    def setUp(self):
        """Set up test environment"""
        self.client = self.client  # Use Django’s test client
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",  # Fix missing email
            password="testpass"
        )

    def test_home_view_unauthenticated(self):
        """Test home view for an unauthenticated user"""
        response = self.client.get(reverse('home'))  # Simulate GET request
        self.assertEqual(response.status_code, 200)
        self.assertIn("course_list", response.context)  # Ensure template receives course_list
        self.assertNotIn("enrolled_classes", response.context)
        self.assertNotIn("teacher_classes", response.context)

    def test_home_view_authenticated_no_courses(self):
        """Test home view for an authenticated user with no enrollments"""
        self.client.login(username="testuser", password="testpass")  # Log in user

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["enrolled_classes"], [])
        self.assertEqual(response.context["teacher_classes"], [])

    def test_home_view_authenticated_with_enrollments(self):
        """Test home view for an authenticated user with enrollments"""
        course = Course.objects.create(title="Test Course")
        Enrollment.objects.create(student=self.user, course=course)

        self.client.login(username="testuser", password="testpass")  # Log in user

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(course, response.context["enrolled_classes"])

    def test_home_view_authenticated_with_teaching_courses(self):
        """Test home view for an authenticated teacher"""
        course = Course.objects.create(title="Teaching Course")
        CourseTeacher.objects.create(teacher=self.user, course=course)

        self.client.login(username="testuser", password="testpass")  # Log in user

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(course, response.context["teacher_classes"])
