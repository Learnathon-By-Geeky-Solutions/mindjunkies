import pytest
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser, Permission
from mindjunkies.accounts.models import User  # adjust the import path
from django.test import RequestFactory
from django.views import View
from django.http import HttpResponse
from django.test import override_settings
from django.test import TestCase, Client


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
@override_settings(
    ROOT_URLCONF="project.urls",
    MIDDLEWARE=[
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ],
)
class TestCustomPermissionRequiredMixin(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.view_url = "/test-view/"
