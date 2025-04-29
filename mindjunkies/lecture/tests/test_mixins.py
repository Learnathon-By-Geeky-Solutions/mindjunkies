import pytest
from unittest import mock
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.messages.storage.fallback import FallbackStorage

from mindjunkies.lecture.views import LectureFormMixin


class DummyRequest:
    """Simple fake request with messages attached."""

    def __init__(self):
        self.session = {}
        self._messages_storage = FallbackStorage(self)
        self._messages_storage.used = False

    @property
    def _messages(self):
        return self._messages_storage

    @_messages.setter
    def _messages(self, value):
        self._messages_storage = FallbackStorage(self)


class DummyForm:
    """Simple form stub."""

    def save(self):
        return mock.Mock()


@pytest.fixture
def dummy_mixin():
    """Mixin with fake request attached."""
    mixin = LectureFormMixin()
    mixin.request = DummyRequest()
    return mixin


@pytest.mark.django_db
def test_handle_form_validation_success(dummy_mixin):
    form = DummyForm()
    dummy_mixin.get_success_url = mock.Mock(return_value='/success-url/')

    result = dummy_mixin.handle_form_validation(form, "Successfully saved!")

    assert result == '/success-url/'


@pytest.mark.django_db
def test_handle_form_validation_validation_error(dummy_mixin):
    form = DummyForm()
    form.save = mock.Mock(side_effect=ValidationError("Some validation error"))
    dummy_mixin.form_invalid = mock.Mock(return_value='/invalid-url/')

    result = dummy_mixin.handle_form_validation(form, "Should not succeed!")

    dummy_mixin.form_invalid.assert_called_once_with(form)
    assert result == '/invalid-url/'


@pytest.mark.django_db
def test_handle_form_validation_integrity_error(dummy_mixin):
    form = DummyForm()
    form.save = mock.Mock(side_effect=IntegrityError("Integrity constraint"))
    dummy_mixin.form_invalid = mock.Mock(return_value='/invalid-url/')

    result = dummy_mixin.handle_form_validation(form, "Should not succeed!")

    dummy_mixin.form_invalid.assert_called_once_with(form)
    assert result == '/invalid-url/'
