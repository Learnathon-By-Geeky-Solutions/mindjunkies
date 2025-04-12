import pytest
from django.urls import reverse
from model_bakery import baker
from django.contrib.messages import get_messages
from django.http import HttpResponseRedirect
from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course, Enrollment
from mindjunkies.dashboard.models import TeacherVerification, Certificate


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
def test_content_list_for_teacher(client, teacher_user, course):
    client.force_login(teacher_user)

    url = reverse("dashboard")
    response = client.get(url)

    assert response.status_code == 200
    assert "courses" in response.context
    assert len(response.context["courses"]) == 1
    assert response.context["courses"][0] == course


@pytest.mark.django_db
def test_content_list_redirect_for_non_teacher(client, user):
    client.force_login(user)

    url = reverse("dashboard")
    response = client.get(url)

    assert response.status_code == 302  # should redirect
    assert response.url == reverse("teacher_verification_form")


@pytest.mark.django_db
def test_enrollment_list(client, teacher_user, course, enrollment):
    client.force_login(teacher_user)

    url = reverse("teacher_dashboard_enrollments", kwargs={"slug": course.slug})
    response = client.get(url)

    assert response.status_code == 200
    assert "students" in response.context
    assert len(response.context["students"]) == 1
    assert response.context["students"][0] == enrollment.student


@pytest.mark.django_db
def test_remove_enrollment(client, teacher_user, course, enrollment):
    client.force_login(teacher_user)

    url = reverse("dashboard_enrollments_remove", kwargs={"course_slug": course.slug, "student_id": enrollment.student.uuid})
    response = client.get(url)

    assert response.status_code == 302
    assert not Enrollment.objects.filter(course=course, student=enrollment.student).exists()


@pytest.mark.django_db
def test_teacher_verification_form_for_teacher(client, teacher_user):
    client.force_login(teacher_user)

    url = reverse("teacher_verification_form")
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_teacher_verification_form_for_non_teacher(client, user):
    client.force_login(user)

    url = reverse("teacher_verification_form")
    response = client.get(url)

    assert response.status_code == 200
    assert "form" in response.context


@pytest.mark.django_db
def test_teacher_verification_form_submission(client, user, teacher_verification):
    client.force_login(user)

    url = reverse("teacher_verification_form")
    form_data = {
        "form_field_1": "data",  # Fill this with actual form field names and data
        "form_field_2": "data",
        "certificates": ["path/to/certificate1.pdf", "path/to/certificate2.pdf"]  # adjust as per form
    }

    response = client.post(url, form_data)

    assert response.status_code == 200
    assert "There was an error in your form submission. Please check the form and try again." in [str(m) for m in
                                                                    get_messages(response.wsgi_request)]


@pytest.mark.django_db
def test_teacher_verification_form_invalid(client, user):
    client.force_login(user)

    url = reverse("teacher_verification_form")
    form_data = {
        "form_field_1": "",  # Submit invalid data
    }

    response = client.post(url, form_data)

    assert response.status_code == 200
    assert "There was an error in your form submission. Please check the form and try again." in [str(m) for m in get_messages(response.wsgi_request)]


@pytest.mark.django_db
def test_verification_wait_view(client, user):
    client.force_login(user)

    url = reverse("verification_wait")
    response = client.get(url)

    assert response.status_code == 200
    assert "Please wait for your verification." in response.content.decode()
