import pytest
from django.conf import settings
from django.utils.timezone import now, make_aware
from freezegun import freeze_time
from model_bakery import baker
from datetime import datetime

from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course
from mindjunkies.live_classes.models import LiveClass
from model_bakery import baker
from unittest import mock
from mindjunkies.live_classes.models import LiveClass


@pytest.mark.django_db
def test_live_class_auto_generates_meeting_id():
    live_class = baker.make(LiveClass, meeting_id="")
    assert live_class.meeting_id.startswith("mindjunkies-")
    assert len(live_class.meeting_id) > 10


@pytest.mark.django_db
def test_live_class_string_representation():
    live_class = baker.make(LiveClass)
    result = str(live_class)
    assert live_class.topic in result
    assert live_class.course.title in result


@pytest.mark.django_db
def test_get_meeting_url_student(settings):
    settings.JITSI_APP_ID = "myapp"
    live_class = baker.make(LiveClass, meeting_id="abc123")
    assert (
        live_class.get_meeting_url_student()
        == f"https://8x8.vc/myapp/abc123"
    )


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
        scheduled_at=make_aware(datetime(2025, 3, 15, 12, 0, 0)),
    )

    assert str(live_class) == "Intro to Django - Django Basics (2025-03-15 12:00:00+06:00)"
