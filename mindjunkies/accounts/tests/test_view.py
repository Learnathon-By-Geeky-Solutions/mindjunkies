import pytest
from decouple import config
from django.contrib.messages import get_messages
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
    url = reverse("edit_profile")
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert b"Edit Profile" in response.content
    assert response.templates[0].name == "accounts/edit_profile.html"


@pytest.mark.django_db
def test_profile_update_view_post_valid(authenticated_client, user):
    data = {
        "bio": "Updated bio",
        "address": "Updated address",
        "first_name": "UpdatedFirstName",
        "last_name": "UpdatedLastName",
    }
    url = reverse("edit_profile")
    response = authenticated_client.post(url, data)
    print(response.content)

    assert response.status_code == 302
    assert response.url == reverse("profile")
    user.refresh_from_db()
    assert user.first_name == "UpdatedFirstName"
    assert user.last_name == "UpdatedLastName"
    assert user.profile.bio == "Updated bio"
    assert user.profile.address == "Updated address"

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert messages[0].message == "Profile updated successfully!"
