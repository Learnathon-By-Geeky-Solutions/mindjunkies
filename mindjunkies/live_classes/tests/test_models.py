import pytest
import uuid
from unittest.mock import patch, mock_open

from django.urls import reverse
from model_bakery import baker

from mindjunkies.live_classes.models import LiveClass


@pytest.fixture
def user(db):
    return baker.make('accounts.User')


@pytest.fixture
def course(db, user):
    return baker.make('courses.Course', teacher=user)


@pytest.fixture
def live_class(db, user, course):
    return baker.make(LiveClass, teacher=user, course=course)


@pytest.mark.django_db
def test_live_class_auto_meeting_id_generation(course, user):
    """
    Test that a meeting_id is auto-generated if not provided during save.
    """
    live_class = LiveClass.objects.create(
        course=course,
        teacher=user,
        topic="Test Live Class",
        scheduled_at="2025-05-01 12:00",
        duration=60,
    )
    assert live_class.meeting_id.startswith('mindjunkies-')
    assert len(live_class.meeting_id) > 10


@pytest.mark.django_db
def test_live_class_str_representation(live_class):
    """
    Test the __str__ method returns the correct format.
    """
    expected_str = f"{live_class.topic} - {live_class.course.title} ({live_class.scheduled_at})"
    assert str(live_class) == expected_str


@pytest.mark.django_db
@patch("mindjunkies.live_classes.models.open", new_callable=mock_open, read_data="PRIVATE_KEY")
@patch("mindjunkies.live_classes.models.JaaSJwtBuilder")
def test_generate_jwt_token_success(mock_jwt_builder, mock_file, live_class, settings):
    """
    Test successful JWT token generation.
    """
    fake_token = b'fake.jwt.token'
    mock_instance = mock_jwt_builder.return_value
    mock_instance.with_defaults.return_value = mock_instance
    mock_instance.with_api_key.return_value = mock_instance
    mock_instance.with_user_name.return_value = mock_instance
    mock_instance.with_user_email.return_value = mock_instance
    mock_instance.with_moderator.return_value = mock_instance
    mock_instance.with_app_id.return_value = mock_instance
    mock_instance.with_user_avatar.return_value = mock_instance
    mock_instance.sign_with.return_value = fake_token

    settings.JITSI_SECRET = "testsecret"
    settings.JITSI_APP_ID = "testappid"

    token = live_class.generate_jwt_token()

    assert token == "fake.jwt.token"
    mock_file.assert_called_once()  # Ensure private.pem was opened
    mock_instance.sign_with.assert_called_once()


@pytest.mark.django_db
@patch("mindjunkies.live_classes.models.open", side_effect=FileNotFoundError)
def test_generate_jwt_token_failure(mock_file, live_class):
    """
    Test generate_jwt_token handles missing file gracefully.
    """
    token = live_class.generate_jwt_token()
    assert token is None  # Since it prints error but doesn't crash


@pytest.mark.django_db
@patch("mindjunkies.live_classes.models.LiveClass.generate_jwt_token", return_value="test.jwt.token")
def test_get_meeting_url_teacher(mock_generate_token, live_class, settings):
    """
    Test teacher meeting URL generation with JWT.
    """
    settings.JITSI_APP_ID = "testappid"
    url = live_class.get_meeting_url_teacher()

    assert url == f"https://8x8.vc/testappid/{live_class.meeting_id}?jwt=test.jwt.token"
    mock_generate_token.assert_called_once()


@pytest.mark.django_db
def test_get_meeting_url_student(live_class, settings):
    """
    Test student meeting URL generation (without JWT).
    """
    settings.JITSI_APP_ID = "testappid"
    url = live_class.get_meeting_url_student()

    assert url == f"https://8x8.vc/testappid/{live_class.meeting_id}"
