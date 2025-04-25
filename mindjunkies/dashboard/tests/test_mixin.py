import pytest
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import path, reverse
from django.views.generic import View
from django.http import HttpResponse
from django.test.utils import override_settings

from mindjunkies.dashboard.mixins import CustomPermissionRequiredMixin

User = get_user_model()


# Simple test view with the mixin
class _TestView(CustomPermissionRequiredMixin, View):
    permission_required = "courses.view_course"  # Generic permission
    def get(self, request, *args, **kwargs):
        return HttpResponse("Test view")


# Minimal URL configuration for tests
test_urls = type("test_urls", (), {"urlpatterns": [
    path("test-view/", _TestView.as_view(), name="test_view"),
    path("accounts/login/", lambda r: HttpResponse(), name="account_login"),
    path("dashboard/verification_wait/", lambda r: HttpResponse(), name="verification_wait"),
]})()


@pytest.mark.django_db
@override_settings(
    ROOT_URLCONF="test_urls",
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

    def test_unauthenticated_user_redirects_to_login(self):
        """Test unauthenticated user redirects to account_login"""
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("account_login"))

    def test_authenticated_user_no_permission_redirects_to_verification(self):
        """Test authenticated user without permission redirects to verification_wait"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("verification_wait"))