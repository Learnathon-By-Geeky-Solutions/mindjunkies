from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.timezone import now
from model_bakery import baker

from mindjunkies.courses.models import Course, Enrollment

User = get_user_model()

pytestmark = pytest.mark.django_db


@pytest.fixture
def create_user():
    return User.objects.create_user(username="testuser", password="password123")


@pytest.fixture
def auth_client(client, create_user):
    client.force_login(create_user)
    return client


def test_home_view_unauthenticated(client):
    """Test home view for an unauthenticated user (should see all courses)."""
    [baker.make(Course, created_at=now() - timedelta(days=i)) for i in range(3)]
    baker.make(Course, _quantity=5)

    response = client.get(reverse("home"))

    assert response.status_code == 200
    assert "new_courses" in response.context
    assert "courses" in response.context


def test_home_view_authenticated(auth_client, create_user):
    """Test home view for an authenticated user with enrolled courses."""
    enrolled_course = baker.make(Course)
    baker.make(Course, _quantity=3)

    # Create an active enrollment
    baker.make(Enrollment, student=create_user, course=enrolled_course, status="active")

    response = auth_client.get(reverse("home"))

    assert response.status_code == 200
    assert "enrolled_courses" in response.context
    assert "new_courses" in response.context
    assert enrolled_course in response.context["enrolled_courses"]
    assert all(
        course not in response.context["new_courses"]
        for course in response.context["enrolled_courses"]
    )


def test_search_view_with_results(client):
    """Test search with a query that matches course titles."""
    baker.make(Course, title="Python Programming")
    baker.make(Course, title="Advanced Python")

    response = client.get(reverse("search_view") + "?search=Python")

    assert response.status_code == 200
    assert "courses" in response.context
    assert len(response.context["courses"]) == 2  # Both courses match


def test_search_view_no_results(client):
    """Test search with a query that returns no courses."""
    baker.make(Course, title="Java Programming")  # This course should not match

    response = client.get(reverse("search_view") + "?search=Ruby")

    assert response.status_code == 200
    assert "courses" in response.context
    assert len(response.context["courses"]) == 0  # No match


def test_search_view_empty_query(client):
    """Test search with an empty query (should return no results)."""
    response = client.get(reverse("search_view") + "?search=")

    assert response.status_code == 200
    assert "courses" in response.context
    assert len(response.context["courses"]) == 0  # No search term entered


def test_home_view_hx_request(auth_client):
    """Test home view with HX-Request header (should render subcategory template)."""
    response = auth_client.get(reverse("home"), HTTP_HX_Request="true")

    assert response.status_code == 200
    assert "home/subcategory.html" in [t.name for t in response.templates]
