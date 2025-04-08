import pytest
from mindjunkies.accounts.tests.fixtures import accounts


@pytest.fixture(autouse=True)
def media_storage(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
