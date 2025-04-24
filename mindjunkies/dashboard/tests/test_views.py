import pytest
from django.urls import reverse
from model_bakery import baker
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course, Enrollment
from mindjunkies.payments.models import Balance, Transaction
from mindjunkies.dashboard.models import TeacherVerification
from django.test import RequestFactory



pytestmark = pytest.mark.django_db

@pytest.fixture
def teacher():
    user = baker.make(User, is_teacher=True)
    content_type = ContentType.objects.get_for_model(Course)
    permission = Permission.objects.get(
        codename="view_course", content_type=content_type
    )
    user.user_permissions.add(permission)

    return user

@pytest.fixture
def student():
    return baker.make(User, is_teacher=False)

@pytest.fixture
def course(teacher):
    return baker.make(Course, teacher=teacher, status="published")

@pytest.fixture
def request_factory():
    return RequestFactory()


def test_teacher_has_permission(teacher):
    assert teacher.has_perm("courses.view_course")

def test_teacher_permission_view_teacher_redirect(client, teacher):
    client.force_login(teacher) 
    print(client)
    response = client.get(reverse("teacher_permission"))
    print("888888888888888888888888888888888888888888888888", response.url)
    assert response.status_code == 302
    assert response.url == reverse("dashboard", kwargs={"status": "published"})


# def test_teacher_permission_shows_form_if_not_teacher(client, student_user):
#     client.force_login(student_user)
#     response = client.get(reverse("teacher_permission"))
#     assert response.status_code == 200
#     assert "apply_teacher.html" in [t.name for t in response.templates]

# def test_content_list_view_published(client, teacher_user):
#     course = baker.make(Course, teacher=teacher_user, status="published")
#     client.force_login(teacher_user)
#     url = reverse("content_list", kwargs={"status": "published"})
#     response = client.get(url)
#     assert response.status_code == 200
#     assert course.title.encode() in response.content

# def test_content_list_view_balance(client, teacher_user):
#     balance = baker.make(Balance, user=teacher_user, amount=100)
#     baker.make(Transaction, user=teacher_user, _quantity=15)
#     client.force_login(teacher_user)
#     response = client.get(reverse("content_list", kwargs={"status": "balance"}))
#     assert response.status_code == 200
#     assert "components/balance.html" in [t.name for t in response.templates]
#     assert b"Balance" in response.content

# def test_enrollment_list_view(client, teacher_user):
#     course = baker.make(Course, teacher=teacher_user)
#     student = baker.make(User)
#     baker.make(Enrollment, course=course, student=student)
#     client.force_login(teacher_user)
#     url = reverse("teacher_dashboard_enrollments", kwargs={"slug": course.slug})
#     response = client.get(url)
#     assert response.status_code == 200
#     assert student.username.encode() in response.content

# def test_remove_enrollment_view(client, teacher_user):
#     course = baker.make(Course, teacher=teacher_user)
#     student = baker.make(User)
#     baker.make(Enrollment, course=course, student=student)
#     client.force_login(teacher_user)
#     url = reverse("remove_enrollment", kwargs={"course_slug": course.slug, "student_id": student.uuid})
#     response = client.get(url)
#     assert response.status_code == 302
#     assert response.url == reverse("teacher_dashboard_enrollments", kwargs={"slug": course.slug})
#     assert not Enrollment.objects.filter(course=course, student=student).exists()

# def test_teacher_verification_post(client, student_user):
#     client.force_login(student_user)
#     url = reverse("teacher_verification_form")
#     with open("path/to/sample_certificate.jpg", "rb") as f:
#         data = {
#             "full_name": "Test User",
#             "experience": "2 years",
#             "certificates": [f],
#         }
#         response = client.post(url, data)
#         assert response.status_code == 302 or response.status_code == 200  # success redirect or form error

# def test_verification_wait_view(client, student_user):
#     client.force_login(student_user)
#     url = reverse("verification_wait")
#     response = client.get(url)
#     assert response.status_code == 200
#     assert b"Please wait for your verification." in response.content
