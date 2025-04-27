import pytest
from django.urls import reverse
from django.test import Client
from model_bakery import baker

from mindjunkies.dashboard.mixins import VerifiedTeacherRequiredMixin
from mindjunkies.dashboard.models import TeacherVerification


class DummyView(VerifiedTeacherRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


@pytest.fixture
def user(db):
    return baker.make('accounts.User')


@pytest.fixture
def teacher_user(db):
    return baker.make('accounts.User', is_teacher=True)


@pytest.fixture
def verified_teacher_user(db):
    user = baker.make('accounts.User', is_teacher=True)
    baker.make(TeacherVerification, user=user, verified=True)
    return user


@pytest.fixture
def client_instance():
    return Client()


@pytest.mark.django_db
def test_mixin_redirects_anonymous_user(client_instance):
    response = client_instance.get(reverse('dashboard'))
    assert response.status_code == 302
    assert reverse('account_login') in response.url


@pytest.mark.django_db
def test_mixin_redirects_non_teacher_user(client_instance, user):
    client_instance.force_login(user)
    response = client_instance.get(reverse('dashboard'))
    assert response.status_code == 302
    assert reverse('teacher_permission') in response.url


@pytest.mark.django_db
def test_mixin_redirects_teacher_without_verification_record(client_instance, teacher_user):
    client_instance.force_login(teacher_user)
    response = client_instance.get(reverse('dashboard'))
    assert response.status_code == 302
    assert reverse('teacher_permission') in response.url


@pytest.mark.django_db
def test_mixin_redirects_teacher_not_verified(client_instance, teacher_user):
    baker.make(TeacherVerification, user=teacher_user, verified=False)
    client_instance.force_login(teacher_user)
    response = client_instance.get(reverse('dashboard'))
    assert response.status_code == 302
    assert reverse('verification_wait') in response.url


@pytest.mark.django_db
def test_mixin_allows_verified_teacher_access(client_instance, verified_teacher_user):
    client_instance.force_login(verified_teacher_user)
    response = client_instance.get(reverse('dashboard'))
    assert response.status_code == 200
    assert "components/content.html" in [template.name for template in response.templates]
