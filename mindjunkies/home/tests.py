from decouple import config
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from mindjunkies.courses.models import Course, CourseCategory, CourseTeacher, Enrollment

User = get_user_model()


class HomePageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up initial test data."""
        cls.user = User.objects.create_user(
            username="testuser",
            password=config("TEST_PASS"),
            email="testuser@gmail.com",
        )

        cls.category1 = CourseCategory.objects.create(
            name="Programming", slug="programming"
        )
        cls.category2 = CourseCategory.objects.create(
            name="Web Development", slug="web-development", parent=cls.category1
        )

        cls.course1 = Course.objects.create(
            title="Python Basics",
            category=cls.category1,
            course_description="Learn Python",
        )
        cls.course2 = Course.objects.create(
            title="Django Fundamentals",
            category=cls.category2,
            course_description="Learn Django",
        )

    def test_home_page_status_code(self):
        """Test that the home page loads successfully."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        """Test that the home page uses the correct template."""
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home/index.html")

    def test_home_page_contains_featured_courses(self):
        """Test that featured courses are displayed."""
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Python Basics")
        self.assertContains(response, "Django Fundamentals")

    def test_home_page_contains_categories(self):
        """Test that categories are displayed."""
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Programming")
        self.assertContains(response, "Web Development")

    def test_home_page_authenticated_user_enrolled_classes(self):
        """Test that enrolled classes are displayed for authenticated users."""
        self.client.login(username="testuser", password="password123")
        Enrollment.objects.create(student=self.user, course=self.course1)

        response = self.client.get(reverse("home"))
        self.assertContains(
            response, "Python Basics"
        )  # Course should be in enrolled list

    def test_home_page_authenticated_teacher_classes(self):
        """Test that teacher's classes are displayed."""
        self.client.login(username="testuser", password="password123")
        CourseTeacher.objects.create(teacher=self.user, course=self.course2)

        response = self.client.get(reverse("home"))
        self.assertContains(
            response, "Django Fundamentals"
        )  # Course should be in teacher's list


class SearchResultsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up initial test data for search functionality."""
        cls.course1 = Course.objects.create(
            title="Learn Python", course_description="Python for beginners"
        )
        cls.course2 = Course.objects.create(
            title="Django Web Development", course_description="Master Django"
        )

    def test_search_results_status_code(self):
        """Test that the search results page loads successfully."""
        response = self.client.get(reverse("search_results"), {"search": "Python"})
        self.assertEqual(response.status_code, 200)

    def test_search_results_template_used(self):
        """Test that the search results page uses the correct template."""
        response = self.client.get(reverse("search_results"), {"search": "Python"})
        self.assertTemplateUsed(response, "home/search_results.html")

    def test_search_results_contains_highlighted_courses(self):
        """Test that search results contain highlighted course titles."""
        response = self.client.get(reverse("search_results"), {"search": "Python"})
        self.assertContains(response, "<mark>Python</mark>")  # Highlighted title

    def test_search_results_no_query(self):
        """Test that search results return empty when no query is provided."""
        response = self.client.get(reverse("search_results"))
        self.assertEqual(len(response.context["courses"]), 0)

    def test_search_results_no_matching_courses(self):
        """Test that no courses are returned for an unmatched search query."""
        response = self.client.get(reverse("search_results"), {"search": "React"})
        self.assertEqual(len(response.context["courses"]), 0)
