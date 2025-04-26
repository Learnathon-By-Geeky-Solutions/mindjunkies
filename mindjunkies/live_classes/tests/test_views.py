import pytest
from django.urls import reverse
from model_bakery import baker
from mindjunkies.courses.models import Course, CourseToken
from mindjunkies.live_classes.models import LiveClass
from django.conf import settings


@pytest.fixture
def user(db):
    return baker.make(settings.AUTH_USER_MODEL, is_teacher=False)


@pytest.mark.django_db
def test_live_class_list_view(client, user):
    course = baker.make(Course, slug="python", teacher=user)
    live_class = baker.make(LiveClass, course=course)
    client.force_login(user)

    url = reverse("list_live_classes", kwargs={"slug": course.slug})
    response = client.get(url)

    assert response.status_code == 200
    assert live_class.topic in str(response.content)


@pytest.mark.django_db
def test_create_live_class_view_redirects_on_pending_token(client, user):
    course = baker.make(Course, slug="python", teacher=user)
    baker.make(CourseToken, course=course, teacher=user, status="pending")
    client.force_login(user)

    url = reverse("create_live_class", kwargs={"slug": course.slug})
    response = client.get(url)

    assert response.status_code == 302
    assert reverse("lecture_home", kwargs={"course_slug": course.slug}) in response.url


@pytest.mark.django_db
def test_create_live_class_view_redirects_on_missing_token(client, user):
    course = baker.make(Course, slug="python", teacher=user)
    client.force_login(user)

    url = reverse("create_live_class", kwargs={"slug": course.slug})
    response = client.get(url)

    assert response.status_code == 302
    assert reverse("lecture_home", kwargs={"course_slug": course.slug}) in response.url


@pytest.mark.django_db
def test_create_live_class_schedule_conflict(client, user):
    course = baker.make(Course, slug="python", teacher=user)
    baker.make(CourseToken, course=course, teacher=user, status="approved")
    scheduled_time = "2025-04-30 12:00"

    baker.make(LiveClass, teacher=user, scheduled_at=scheduled_time)
    client.force_login(user)

    url = reverse("create_live_class", kwargs={"slug": course.slug})
    data = {
        "topic": "Conflict Class",
        "scheduled_at": scheduled_time,
        "duration": 30,
    }

    response = client.post(url, data, follow=True)
    assert "already have a class scheduled" in str(response.content)


@pytest.mark.django_db
def test_create_live_class_success(client, user):
    course = baker.make(Course, slug="python", teacher=user)
    baker.make(CourseToken, course=course, teacher=user, status="approved")
    client.force_login(user)

    url = reverse("create_live_class", kwargs={"slug": course.slug})
    data = {
        "topic": "New Class",
        "scheduled_at": "2025-04-30 13:00",
        "duration": 30,
    }

    response = client.post(url, data)
    assert response.status_code == 302
    assert LiveClass.objects.filter(topic="New Class").exists()


@pytest.mark.django_db
def test_join_live_class_view(client, user):
    live_class = baker.make(LiveClass)
    client.force_login(user)

    url = reverse("join_live_class", kwargs={"meeting_id": live_class.meeting_id})
    response = client.get(url)

    assert response.status_code == 200
    assert live_class.topic in str(response.content)
