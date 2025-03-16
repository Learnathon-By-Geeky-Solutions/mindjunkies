import pytest
from decouple import config
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_user():
    """Test that a user can be created successfully."""
    user = User.objects.create_user(
        username="john_doe",
        email="johndoe@example.com",
        password=config("TEST_PASS"),
        first_name="John",
        last_name="Doe",
    )
    assert user.email == "johndoe@example.com"
    assert user.username == "john_doe"
    assert user.check_password(config("TEST_PASS"))
    assert user.is_staff is False
    assert user.is_superuser is False


@pytest.mark.django_db
def test_create_superuser():
    """Test that a superuser is created with correct permissions."""
    admin_user = User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password=config("TEST_PASS"),
    )
    assert admin_user.is_staff is True
    assert admin_user.is_superuser is True


@pytest.mark.django_db
def test_user_str(test_user):
    """Test the string representation of the user model."""
    assert str(test_user) == "testuser - testuser@gmail.com"


@pytest.mark.django_db
def test_user_name_property(test_user):
    """Test the name property of the User model."""
    assert test_user.name == "Test User"


def test_create_profile(test_user):
    """Test that a profile is created automatically for a user."""
    profile = test_user.profile
    assert profile.user == test_user
    assert str(profile) == f"{test_user.username}'s profile"
