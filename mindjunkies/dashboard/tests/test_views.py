import pytest
from django.contrib.messages import get_messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from model_bakery import baker

from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course, Enrollment
from mindjunkies.dashboard.models import Certificate, TeacherVerification


@pytest.fixture
def user(db, django_user_model):
    return baker.make(django_user_model, is_teacher=False)


@pytest.fixture
def teacher_user(db, django_user_model):
    return baker.make(django_user_model, is_teacher=True)


@pytest.fixture
def course(db, teacher_user):
    return baker.make(Course, teacher=teacher_user)


@pytest.fixture
def enrollment(db, course, user):
    return baker.make(Enrollment, course=course, student=user)


@pytest.fixture
def teacher_verification(db, teacher_user):
    return baker.make(TeacherVerification, user=teacher_user)


@pytest.mark.django_db
def test_teacher_verification_form_submission(client, user, teacher_verification):
    client.force_login(user)

    url = reverse("teacher_verification_form")
    form_data = {
        "form_field_1": "data",  # Fill this with actual form field names and data
        "form_field_2": "data",
        "certificates": [
            "path/to/certificate1.pdf",
            "path/to/certificate2.pdf",
        ],  # adjust as per form
    }

    response = client.post(url, form_data)

    assert response.status_code == 200
    assert (
        "There was an error in your form submission. Please check the form and try again."
        in [str(m) for m in get_messages(response.wsgi_request)]
    )


@pytest.mark.django_db
def test_teacher_verification_form_invalid(client, user):
    client.force_login(user)

    url = reverse("teacher_verification_form")
    form_data = {
        "form_field_1": "",  # Submit invalid data
    }

    response = client.post(url, form_data)

    assert response.status_code == 200
    assert (
        "There was an error in your form submission. Please check the form and try again."
        in [str(m) for m in get_messages(response.wsgi_request)]
    )


@pytest.mark.django_db
def test_verification_wait_view(client, user):
    client.force_login(user)

    url = reverse("verification_wait")
    response = client.get(url)

    assert response.status_code == 200
    assert "Please wait for your verification." in response.content.decode()
