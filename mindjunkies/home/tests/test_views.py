import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from model_bakery import baker
from mindjunkies.courses.models import Course, Enrollment, CourseCategory
from datetime import timedelta
from django.utils.timezone import now

User = get_user_model()

pytestmark = pytest.mark.django_db  # Use the database for tests


@pytest.fixture
def create_user():
    return User.objects.create_user(username="testuser", password="password123")


@pytest.fixture
def auth_client(client, create_user):
    client.force_login(create_user)
    return client


def test_home_view_unauthenticated(client):
    """Test home view for an unauthenticated user (should see all courses)."""
    new_courses = [
        baker.make(Course, created_at=now() - timedelta(days=i)) for i in range(3)
    ]
    other_courses = baker.make(Course, _quantity=5)

    response = client.get(reverse("home"))

    assert response.status_code == 200
    assert "new_courses" in response.context
    assert "courses" in response.context


def test_home_view_authenticated(auth_client, create_user):
    """Test home view for an authenticated user with enrolled courses."""
    enrolled_course = baker.make(Course)
    new_courses = baker.make(Course, _quantity=3)

    # Create an active enrollment
    baker.make(Enrollment, student=create_user, course=enrolled_course, status="active")

    response = auth_client.get(reverse("home"))

    assert response.status_code == 200
    assert "enrolled_courses" in response.context
    assert "new_courses" in response.context
    assert enrolled_course in response.context["enrolled_courses"]
    assert all(course not in response.context["new_courses"] for course in response.context["enrolled_courses"])


# ✅ Test `search_view` with a matching query
def test_search_view_with_results(client):
    """Test search with a query that matches course titles."""
    course1 = baker.make(Course, title="Python Programming")
    course2 = baker.make(Course, title="Advanced Python")

    response = client.get(reverse("search_view") + "?search=Python")

    assert response.status_code == 200
    assert "courses" in response.context
    assert len(response.context["courses"]) == 2  # Both courses match


# ✅ Test `search_view` with no results
def test_search_view_no_results(client):
    """Test search with a query that returns no courses."""
    baker.make(Course, title="Java Programming")  # This course should not match

    response = client.get(reverse("search_view") + "?search=Ruby")

    assert response.status_code == 200
    assert "courses" in response.context
    assert len(response.context["courses"]) == 0  # No match


# ✅ Test `search_view` with an empty query
def test_search_view_empty_query(client):
    """Test search with an empty query (should return no results)."""
    response = client.get(reverse("search_view") + "?search=")

    assert response.status_code == 200
    assert "courses" in response.context
    assert len(response.context["courses"]) == 0  # No search term entered
