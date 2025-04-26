import pytest
from django.contrib.messages import get_messages
from django.urls import reverse
from model_bakery import baker
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course, Enrollment
from mindjunkies.dashboard.models import Certificate, TeacherVerification
from mindjunkies.payments.models import Balance, Transaction
from django.conf import settings


@pytest.fixture
def user(db, django_user_model):
    return baker.make(settings.AUTH_USER_MODEL, is_teacher=False)


@pytest.fixture
def teacher_user(db, django_user_model):
    user = baker.make(django_user_model, is_teacher=True)
    content_type = ContentType.objects.get_for_model(Course)
    permission = Permission.objects.get(codename='view_course', content_type=content_type)
    user.user_permissions.add(permission)
    user.refresh_from_db()  # Ensure permissions are saved
    assert permission in user.user_permissions.all()  # Verify permission
    return user


@pytest.fixture
def course(db, teacher_user):
    return baker.make(Course, teacher=teacher_user, status="published", slug="test-course")


@pytest.fixture
def draft_course(db, teacher_user):
    return baker.make(Course, teacher=teacher_user, status="draft", slug="test-draft")


@pytest.fixture
def archived_course(db, teacher_user):
    return baker.make(Course, teacher=teacher_user, status="archived", slug="test-archived")


@pytest.fixture
def enrollment(db, course, user):
    return baker.make(Enrollment, course=course, student=user)


@pytest.fixture
def teacher_verification(db, user):
    return baker.make(TeacherVerification, user=user)


@pytest.fixture
def balance(db, teacher_user):
    return baker.make(Balance, user=teacher_user, amount=100)


@pytest.fixture
def transaction(db, teacher_user):
    # Assuming tran is a ForeignKey; replace 'SomeModel' with actual model if needed
    return baker.make(Transaction, user=teacher_user)


@pytest.mark.django_db
def test_teacher_permission_view_non_teacher_no_verification(client, user):
    client.force_login(user)
    url = reverse("teacher_permission")
    response = client.get(url)
    assert response.status_code == 200
    assert "teacher_verification.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_teacher_permission_view_non_teacher_with_verification(client, user, teacher_verification):
    client.force_login(user)
    url = reverse("teacher_permission")
    response = client.get(url)
    assert response.status_code == 302
    


@pytest.mark.django_db
def test_teacher_permission_view_teacher(client, teacher_user):
    assert teacher_user.is_teacher  # Verify fixture
    client.force_login(teacher_user)
    url = reverse("teacher_permission")
    response = client.get(url)
    assert response.status_code == 200
   


@pytest.mark.django_db
def test_enrollment_list_view(client, teacher_user, course, enrollment):
    client.force_login(teacher_user)
    url = reverse("teacher_dashboard_enrollments", kwargs={"slug": course.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["course"] == course
    assert len(response.context["students"]) == 1
    assert response.context["students"][0] == enrollment.student
    assert "enrollmentList.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_remove_enrollment_view(client, teacher_user, course, enrollment):
    client.force_login(teacher_user)
    url = reverse(
        "dashboard_enrollments_remove",
        kwargs={"course_slug": course.slug, "student_id": enrollment.student.uuid},
    )
    response = client.get(url)
    assert response.status_code == 302
    
    assert not Enrollment.objects.filter(course=course, student=enrollment.student).exists()


@pytest.mark.django_db
def test_teacher_verification_view_teacher(client, teacher_user):
    client.force_login(teacher_user)
    url = reverse("teacher_verification_form")
    response = client.get(url)
    assert response.status_code == 200
    


@pytest.mark.django_db
def test_teacher_verification_view_non_teacher_with_verification(client, user, teacher_verification):
    client.force_login(user)
    url = reverse("teacher_verification_form")
    response = client.get(url)
    assert response.status_code == 302
   


@pytest.mark.django_db
def test_teacher_verification_view_non_teacher_no_verification(client, user):
    client.force_login(user)
    url = reverse("teacher_verification_form")
    response = client.get(url)
    assert response.status_code == 200
    assert "form" in response.context
    assert "teacher_verification.html" in [t.name for t in response.templates]



@pytest.mark.django_db
def test_teacher_verification_form_submission_invalid(client, user):
    client.force_login(user)
    url = reverse("teacher_verification_form")
    form_data = {
        "qualification": "",  # Invalid: required field
        "experience": -1,    # Invalid: negative experience
    }
    response = client.post(url, data=form_data)
    assert response.status_code == 200
    assert "form" in response.context
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
    assert "verification_wait.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_draft_view(client, teacher_user, draft_course):
    client.force_login(teacher_user)
    url = reverse("draft_content")
    response = client.get(url)
    assert response.status_code == 200
    assert "courses" in response.context
    assert response.context["courses"].count() == 1
    assert list(response.context["courses"])[0] == draft_course
    assert "components/draft.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_draft_view_non_teacher(client, user):
    client.force_login(user)
    url = reverse("draft_content")
    response = client.get(url)
    assert response.status_code == 302
    

@pytest.mark.django_db
def test_archive_view(client, teacher_user, archived_course):
    client.force_login(teacher_user)
    url = reverse("archive_content")
    response = client.get(url)
    assert response.status_code == 200
    assert "courses" in response.context
    assert response.context["courses"].count() == 0
   


@pytest.mark.django_db
def test_archive_view_non_teacher(client, user):
    client.force_login(user)
    url = reverse("archive_content")
    response = client.get(url)
    assert response.status_code == 302
    