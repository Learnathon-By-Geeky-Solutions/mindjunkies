import pytest
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test.client import RequestFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path


def add_messages_to_request(request):
    """Attach a mock messages storage to the request."""
    setattr(request, '_messages', FallbackStorage(request))
    return request


def add_middleware_to_request(request):
    """Add session and messages manually to a RequestFactory request."""
    request.session = {}
    setattr(request, '_messages', FallbackStorage(request))
    return request
