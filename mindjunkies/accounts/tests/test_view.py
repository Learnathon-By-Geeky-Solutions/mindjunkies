import pytest
from decouple import config
from django.urls import reverse

from mindjunkies.accounts.models import Profile, User


@pytest.fixture
def user(db, django_user_model):
    user = django_user_model.objects.create_user(
        username="testuser", password=config("TEST_PASS")
    )
    return user


@pytest.fixture
def authenticated_client(client, user):
    client.login(username="testuser", password=config("TEST_PASS"))
    return client


def test_profile_update_view_get(authenticated_client):
    url = reverse("edit_profile")  # adjust this to your actual view name
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert b"Edit Profile" in response.content  # adjust to expected template content


def test_profile_update_view_post_valid(authenticated_client):
    url = reverse("edit_profile")
    data = {
        "bio": "Updated bio",
        "address": "Earth",
    }
    response = authenticated_client.post(url, data)
    print("\n ========================================= print me ", response)
