import pytest

from mindjunkies.accounts.tests.fixtures import *  # noqa: F401, F403


@pytest.fixture(autouse=True)
def media_storage(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
