import pytest
from django.urls import reverse
from model_bakery import baker

from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course, Enrollment
from mindjunkies.dashboard.models import TeacherVerification, Certificate
from mindjunkies.payments.models import Balance, Transaction


@pytest.fixture
def user(db):
    return baker.make(User)


@pytest.fixture
def verified_teacher_user(db):
    user = baker.make(User, is_teacher=True)
    baker.make(TeacherVerification, user=user, verified=True)
    return user


@pytest.fixture
def verified_teacher_course(db, verified_teacher_user):
    return baker.make(Course, teacher=verified_teacher_user, status='published')


@pytest.fixture
def draft_course(db, verified_teacher_user):
    return baker.make(Course, teacher=verified_teacher_user, status='draft')


@pytest.fixture
def enrollment(db, verified_teacher_course, user):
    return baker.make(Enrollment, student=user, course=verified_teacher_course)


@pytest.fixture
def transaction(db, user):
    return baker.make(Transaction, user=user)


@pytest.mark.django_db
def test_teacher_permission_view_redirects_teacher(client):
    teacher_user = baker.make(User, is_teacher=True)
    client.force_login(teacher_user)

    url = reverse('teacher_permission')
    response = client.get(url)

    assert response.status_code == 302
    assert reverse('dashboard') in response.url


@pytest.mark.django_db
def test_teacher_permission_view_redirects_verified_user(client, user):
    client.force_login(user)
    baker.make(TeacherVerification, user=user)
    url = reverse('teacher_permission')
    response = client.get(url)
    assert response.status_code == 302
    assert reverse('verification_wait') in response.url


@pytest.mark.django_db
def test_teacher_permission_view_renders_for_new_user(client, user):
    client.force_login(user)
    url = reverse('teacher_permission')
    response = client.get(url)
    assert response.status_code == 200
    assert "teacher_verification.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_teacher_home_renders(client, verified_teacher_user):
    client.force_login(verified_teacher_user)
    url = reverse('dashboard')
    response = client.get(url)
    assert response.status_code == 200
    assert "components/content.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_content_list_published(client, verified_teacher_user):
    client.force_login(verified_teacher_user)
    url = reverse('dashboard')
    response = client.get(url)
    assert response.status_code == 200
    assert "components/content.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_content_list_draft(client, verified_teacher_user):
    client.force_login(verified_teacher_user)
    url = reverse('dashboard-content', args=["draft"])
    response = client.get(url)
    assert response.status_code == 200
    assert "components/draft.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_content_list_archived(client, verified_teacher_user):
    client.force_login(verified_teacher_user)
    url = reverse('dashboard-content', args=["archived"])
    response = client.get(url)
    assert response.status_code == 200
    assert "components/archive.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_content_list_balance(client, verified_teacher_user):
    client.force_login(verified_teacher_user)
    url = reverse('dashboard-content', args=["balance"])
    response = client.get(url)
    assert response.status_code == 200
    assert "components/balance.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_content_list_redirect(client, verified_teacher_user):
    client.force_login(verified_teacher_user)
    url = reverse('dashboard-content', args=["unknown"])
    response = client.get(url)
    assert response.status_code == 302
    assert reverse('dashboard') in response.url


@pytest.mark.django_db
def test_enrollment_list_view(client, verified_teacher_user, verified_teacher_course, enrollment):
    client.force_login(verified_teacher_user)
    url = reverse('teacher_dashboard_enrollments', args=[verified_teacher_course.slug])
    response = client.get(url)
    assert response.status_code == 200
    assert "enrollmentList.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_remove_enrollment_view(client, verified_teacher_user, verified_teacher_course, enrollment):
    client.force_login(verified_teacher_user)
    url = reverse('dashboard_enrollments_remove', args=[verified_teacher_course.slug, enrollment.student.uuid])
    response = client.get(url)
    assert response.status_code == 302
    assert reverse('teacher_dashboard_enrollments', args=[verified_teacher_course.slug]) in response.url


@pytest.mark.django_db
def test_teacher_verification_form_get(client, user):
    client.force_login(user)
    url = reverse('teacher_verification_form')
    response = client.get(url)
    assert response.status_code == 200
    assert "teacher_verification.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_teacher_verification_form_submission(client, user):
    client.force_login(user)
    url = reverse('teacher_verification_form')
    data = {
        'full_name': "Test User",
        'email': "test@example.com",
    }
    response = client.post(url, data)
    assert response.status_code in (302, 200)


@pytest.mark.django_db
def test_verification_wait_view(client, user):
    client.force_login(user)
    url = reverse('verification_wait')
    response = client.get(url)
    assert response.status_code == 200
    assert "verification_wait.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_draft_view_renders(client, verified_teacher_user):
    client.force_login(verified_teacher_user)
    url = reverse("dashboard-content", args=["draft"])
    response = client.get(url)
    assert response.status_code == 200
    assert "components/draft.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_archive_view_renders(client, verified_teacher_user):
    client.force_login(verified_teacher_user)
    url = reverse("dashboard-content", args=["archived"])
    response = client.get(url)
    assert response.status_code == 200
    assert "components/archive.html" in [t.name for t in response.templates]
