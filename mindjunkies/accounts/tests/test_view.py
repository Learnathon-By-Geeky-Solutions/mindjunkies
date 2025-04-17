import pytest
from django.urls import reverse
from mindjunkies.accounts.models import User

from mindjunkies.accounts.models import Profile

@pytest.fixture
def user(db, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='testpass123')
    return user

@pytest.fixture
def authenticated_client(client, user):
    client.login(username='testuser', password='testpass123')
    return client

def test_profile_update_view_get(authenticated_client):
    url = reverse('edit_profile')  # adjust this to your actual view name
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert b"Edit Profile" in response.content  # adjust to expected template content

def test_profile_update_view_post_valid(authenticated_client):
    url = reverse('edit_profile')
    data = {
        'bio': 'Updated bio',
        'address': 'Earth',
    }
    response = authenticated_client.post(url, data)
    print("\n ========================================= print me ", response)
    # assert response.status_code == 200  # Assuming redirect on success
    # profile = Profile.objects.get(user__username='testuser')
    # assert profile.bio == 'Updated bio'
    # assert profile.address == 'Earth'

# def test_profile_update_view_post_invalid(authenticated_client):
#     url = reverse('profile_update')
#     data = {
#         'bio': '',  # Assume bio is required
#         'address': 'Earth',
#     }
#     response = authenticated_client.post(url, data)
#     assert response.status_code == 200  # Re-render form on error
#     assert b"This field is required" in response.content  # Adjust to your form error
