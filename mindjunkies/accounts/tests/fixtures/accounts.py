import pytest
from decouple import config
from django.contrib.auth import get_user_model
from model_bakery import baker

User = get_user_model()


@pytest.fixture
def test_user(db):
    return baker.make(
        User,
        username="testuser",
        email="testuser@gmail.com",
        password=config("TEST_PASS"),
        first_name="Test",
        last_name="User",
    )
