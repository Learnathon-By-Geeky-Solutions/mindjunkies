import pytest
from decouple import config
from django.contrib.auth import get_user_model
from model_bakery import baker

from mindjunkies.accounts.models import Profile, User


@pytest.mark.django_db
class TestUserModel:
    def test_user_str_returns_username_and_email(self):
        user = baker.make(User, username="john", email="john@example.com")
        assert str(user) == "john - john@example.com"

    def test_user_name_property_full_name(self):
        user = baker.make(User, first_name="John", last_name="Doe")
        assert user.name == "John Doe"

    def test_user_get_number_of_reviews(self):
        user = baker.make(User)
        # simulate the user as a teacher with 2 course ratings
        course1 = baker.make("courses.Course", teacher=user, total_rating=4)
        course2 = baker.make("courses.Course", teacher=user, total_rating=5)
        baker.make("courses.Rating", course=course1, _quantity=2)
        baker.make("courses.Rating", course=course2, _quantity=1)

        assert user.get_number_of_reviews() == 3

    def test_user_get_instructor_rating(self):
        user = baker.make(User)
        course = baker.make("courses.Course", teacher=user)
        baker.make("courses.Rating", course=course, rating=3)

        assert user.get_instructor_rating() == 3

    def test_user_get_instructor_rating_zero_reviews(self):
        user = baker.make(User)
        baker.make("courses.Course", teacher=user, total_rating=10)
        assert user.get_instructor_rating() == 0

    def test_user_get_number_of_students(self):
        user = baker.make(User)
        course = baker.make("courses.Course", teacher=user)
        # 3 active, 1 inactive enrollment
        baker.make("courses.Enrollment", course=course, status="active", _quantity=3)
        baker.make("courses.Enrollment", course=course, status="inactive")
        assert user.get_number_of_students() == 3

    def test_user_get_number_of_courses(self):
        user = baker.make(User)
        baker.make("courses.Course", teacher=user, _quantity=5)
        assert user.get_number_of_courses() == 5


@pytest.mark.django_db
class TestProfileModel:
    def test_profile_str(self):
        user = baker.make(User, username="alice")
        profile = Profile.objects.get(user=user)
        assert str(profile) == "alice's profile"
