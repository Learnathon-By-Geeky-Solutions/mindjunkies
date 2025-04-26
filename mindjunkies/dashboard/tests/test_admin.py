import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import Group
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory
from model_bakery import baker
from django.conf import settings

from mindjunkies.dashboard.admin import TeacherVerificationAdmin, CertificateAdmin
from mindjunkies.dashboard.models import TeacherVerification, Certificate


class MockRequest:
    def __init__(self):
        factory = RequestFactory()
        self.request = factory.get("/")
        self.request.session = {}
        self.request._messages = FallbackStorage(self.request)

    def __getattr__(self, name):
        return getattr(self.request, name)
    

@pytest.fixture
def admin_site():
    return AdminSite()


@pytest.fixture
def teacher_group():
    return baker.make(Group, name="Teacher")


@pytest.mark.django_db
class TestTeacherVerificationAdmin:
    def test_list_display(self, admin_site):
        teacher_admin = TeacherVerificationAdmin(TeacherVerification, admin_site)
        assert teacher_admin.list_display == ("user", "full_name", "email", "phone", "address", "verified")
        
    def test_actions(self, admin_site):
        teacher_admin = TeacherVerificationAdmin(TeacherVerification, admin_site)
        assert "approve_teacher" in teacher_admin.actions
        assert "disapprove_teacher" in teacher_admin.actions
    
    def test_approve_teacher_action(self, admin_site, teacher_group):
        # Create a test user with a verification request
        user = baker.make(settings.AUTH_USER_MODEL, is_teacher=False)
        verification = baker.make(TeacherVerification, user=user, verified=False)
        
        # Set up the admin action
        teacher_admin = TeacherVerificationAdmin(TeacherVerification, admin_site)
        request = MockRequest()
        
        # Execute the approve_teacher action
        queryset = TeacherVerification.objects.filter(pk=verification.pk)
        teacher_admin.approve_teacher(request, queryset)
        
        # Refresh the objects from the database
        verification.refresh_from_db()
        user.refresh_from_db()
        
        # Check that the action had the expected effects
        assert verification.verified is False
        assert user.is_teacher is True
        assert teacher_group in user.groups.all()
    
    def test_disapprove_teacher_action(self, admin_site, teacher_group):
        # Create a test user who is already a verified teacher
        user = baker.make(settings.AUTH_USER_MODEL, is_teacher=False)
        user.groups.add(teacher_group)
        verification = baker.make(TeacherVerification, user=user, verified=True)
        
        # Set up the admin action
        teacher_admin = TeacherVerificationAdmin(TeacherVerification, admin_site)
        request = MockRequest()
        
        # Execute the disapprove_teacher action
        queryset = TeacherVerification.objects.filter(pk=verification.pk)
        teacher_admin.disapprove_teacher(request, queryset)
        
        # Refresh the objects from the database
        verification.refresh_from_db()
        user.refresh_from_db()
        
        # Check that the action had the expected effects
        assert verification.verified is True
        assert user.is_teacher is False
        assert teacher_group not in user.groups.all()


@pytest.mark.django_db
class TestCertificateAdmin:
    def test_list_display(self, admin_site):
        certificate_admin = CertificateAdmin(Certificate, admin_site)
        assert certificate_admin.list_display == ("id", "image", "description")
        
    def test_search_fields(self, admin_site):
        certificate_admin = CertificateAdmin(Certificate, admin_site)
        assert certificate_admin.search_fields == ("description",)
        
    def test_list_filter(self, admin_site):
        certificate_admin = CertificateAdmin(Certificate, admin_site)
        assert certificate_admin.list_filter == ("created_at", "updated_at")
        
    def test_certificate_creation(self, admin_site):
        # Create a certificate using model_bakery
        certificate = baker.make(Certificate, description="Test Certificate")
        
        # Set up the admin
        CertificateAdmin(Certificate, admin_site)
        
        # Test that the certificate was created correctly
        assert certificate.description == "Test Certificate"
        assert certificate.id is not None
        
        # Test that the certificate appears in the admin list
        queryset = Certificate.objects.all()
        assert certificate in queryset