import pytest
from django.conf import settings
from django.utils.timezone import now
from freezegun import freeze_time
from model_bakery import baker

from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course
from mindjunkies.live_classes.models import LiveClass


@pytest.mark.django_db
def test_create_live_class():
    """Test that a LiveClass instance can be created."""
    teacher = baker.make(User)
    course = baker.make(Course)

    live_class = baker.make(
        LiveClass,
        teacher=teacher,
        course=course,
        topic="Test Class",
        scheduled_at=now(),
    )

    assert live_class.teacher == teacher
    assert live_class.course == course
    assert live_class.topic == "Test Class"
    assert live_class.status == "Upcoming"


@pytest.mark.django_db
def test_meeting_id_auto_generation():
    """Test that `meeting_id` is automatically generated if not provided."""
    teacher = baker.make(User)
    course = baker.make(Course)

    live_class = LiveClass.objects.create(
        teacher=teacher, course=course, topic="Auto ID Test", scheduled_at=now()
    )

    assert live_class.meeting_id.startswith("mindjunkies-")
    assert len(live_class.meeting_id) == 22  # "mindjunkies-" + 10 hex characters


@pytest.mark.django_db
def test_get_meeting_url_teacher(mocker):
    """Test that `get_meeting_url_teacher()` returns correct JWT-secured URL."""
    teacher = baker.make(User)
    course = baker.make(Course)
    live_class = baker.make(
        LiveClass, teacher=teacher, course=course, scheduled_at=now()
    )

    mocker.patch.object(live_class, "generate_jwt_token", return_value="test_jwt_token")

    url = live_class.get_meeting_url_teacher()
    expected_url = f"https://8x8.vc/{settings.JITSI_APP_ID}/{live_class.meeting_id}?jwt=test_jwt_token"

    assert url == expected_url


@pytest.mark.django_db
def test_get_meeting_url_student():
    """Test that `get_meeting_url_student()` returns correct student URL."""
    teacher = baker.make(User)
    course = baker.make(Course)
    live_class = baker.make(
        LiveClass, teacher=teacher, course=course, scheduled_at=now()
    )

    url = live_class.get_meeting_url_student()
    expected_url = f"https://8x8.vc/{settings.JITSI_APP_ID}/{live_class.meeting_id}"

    assert url == expected_url


@pytest.mark.django_db
@freeze_time("2025-03-15 12:00:00")
def test_live_class_str_method():
    """Test the `__str__()` method of `LiveClass`."""
    teacher = baker.make(User)
    course = baker.make(Course, title="Django Basics")
    live_class = baker.make(
        LiveClass,
        teacher=teacher,
        course=course,
        topic="Intro to Django",
        scheduled_at="2025-03-15 12:00:00",
    )

    assert str(live_class) == "Intro to Django - Django Basics (2025-03-15 12:00:00)"
