import pytest
from model_bakery import baker
from unittest import mock
from mindjunkies.live.models import LiveClass


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
@mock.patch("mindjunkies.live.models.JaaSJwtBuilder")
@mock.patch("builtins.open", new_callable=mock.mock_open, read_data="fake-key")
def test_get_meeting_url_teacher(mock_open, mock_builder, settings):
    settings.JITSI_APP_ID = "myapp"
    settings.JITSI_SECRET = "secret"

    builder_instance = mock_builder.return_value
    builder_instance.with_defaults.return_value = builder_instance
    builder_instance.with_api_key.return_value = builder_instance
    builder_instance.with_user_name.return_value = builder_instance
    builder_instance.with_user_email.return_value = builder_instance
    builder_instance.with_moderator.return_value = builder_instance
    builder_instance.with_app_id.return_value = builder_instance
    builder_instance.with_user_avatar.return_value = builder_instance
    builder_instance.sign_with.return_value = b"mocked-jwt"

    live_class = baker.make(LiveClass, meeting_id="jwt123")
    url = live_class.get_meeting_url_teacher()
    assert url == "https://8x8.vc/myapp/jwt123?jwt=mocked-jwt"
