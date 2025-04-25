import pytest
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser, Permission
from mindjunkies.accounts.models import User  # adjust the import path
from django.test import RequestFactory
from django.views import View
from django.http import HttpResponse

from mindjunkies.dashboard.mixins import CustomPermissionRequiredMixin  # adjust the import path


# Dummy view using the mixin
class DummyView(CustomPermissionRequiredMixin, View):
    permission_required = "auth.view_user"

    def get(self, request):
        return HttpResponse("Success")


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.mark.django_db
def test_redirects_to_login_for_anonymous(factory):
    request = factory.get("/")
    request.user = AnonymousUser()
    response = DummyView.as_view()(request)
    
    assert response.status_code == 302
    assert response.url == reverse("account_login")


@pytest.mark.django_db
def test_redirects_to_verification_wait_for_unauthorized_user(factory):
    user = User.objects.create_user(username="user1", password="pass")
    request = factory.get("/")
    request.user = user
    response = DummyView.as_view()(request)

    assert response.status_code == 302
    assert response.url == reverse("verification_wait")


@pytest.mark.django_db
def test_allows_access_for_authorized_user(factory):
    user = User.objects.create_user(username="admin", password="pass")
    perm = Permission.objects.get(codename="view_user")
    user.user_permissions.add(perm)
    request = factory.get("/")
    request.user = user
    response = DummyView.as_view()(request)

    assert response.status_code == 302
