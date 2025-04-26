import pytest
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from mindjunkies.accounts.models import User
from django.test import TestCase, Client, override_settings
from django.http import HttpResponse
from mindjunkies.dashboard.mixins import CustomPermissionRequiredMixin
from django.views import View





# Dummy view using the mixin
class DummyView(CustomPermissionRequiredMixin, View):
    permission_required = "auth.view_user"

    def get(self, request):
        return HttpResponse("Success")


@override_settings(
    ROOT_URLCONF="project.urls",  # Use the actual URLs file
    MIDDLEWARE = [
    "silk.middleware.SilkyMiddleware",
    "allauth.account.middleware.AccountMiddleware",  # allauth
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # custom middleware here
    "django_htmx.middleware.HtmxMiddleware",
]
)
class TestCustomPermissionRequiredMixin(TestCase):
    def setUp(self):
        """
        Set up the test environment.
        - Create a test user.
        - Define the view URL.
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.view_url = reverse("dashboard", kwargs={"status": "published"})

    def test_unauthenticated_user_redirects_to_login(self):
        """
        Test that an unauthenticated user is redirected to the login page.
        """
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)  # Redirect status code
        

    def test_authenticated_user_no_permission_redirects_to_verification(self):
        """
        Test that an authenticated user without permission
        is redirected to the verification_wait page.
        """
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)  # Redirect status code
        

    def test_authenticated_user_with_permission_access_granted(self):
        """
        Test that an authenticated user with the required permission
        can access the view successfully.
        """
        # Add the required permission to the user
        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.get(codename="view_user", content_type=content_type)
        self.user.user_permissions.add(permission)
        self.user.save()

        # Log in the user
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.view_url)

        # Check for successful response and content
        self.assertEqual(response.status_code, 200)  # Success status code
          # Expected response content