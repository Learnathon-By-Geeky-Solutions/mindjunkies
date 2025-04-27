import pytest
from model_bakery import baker

from mindjunkies.dashboard.models import TeacherVerification, Certificate


@pytest.fixture
def user(db):
    return baker.make('accounts.User')


@pytest.fixture
def certificate(db):
    return baker.make(Certificate)


@pytest.fixture
def teacher_verification(db, user):
    return baker.make(
        TeacherVerification,
        user=user,
        full_name="John Doe",
        email="john@example.com"
    )


@pytest.mark.django_db
def test_certificate_creation(certificate):
    """
    Test creating a Certificate.
    """
    assert isinstance(certificate, Certificate)
    assert certificate.description is not None or certificate.description == ""


@pytest.mark.django_db
def test_certificate_str_method(certificate):
    """
    Test the __str__ method of Certificate.
    """
    assert str(certificate) == f"Certificate {certificate.id}"


@pytest.mark.django_db
def test_teacher_verification_creation(user):
    """
    Test creating a TeacherVerification.
    """
    verification = TeacherVerification.objects.create(
        user=user,
        full_name="Jane Smith",
        email="jane@example.com",
        phone="01700000000",
        address="123 Main Street",
        experience="5 years experience",
    )

    assert verification.full_name == "Jane Smith"
    assert not verification.verified


@pytest.mark.django_db
def test_teacher_verification_str_method(teacher_verification):
    """
    Test the __str__ method of TeacherVerification.
    """
    assert str(teacher_verification) == teacher_verification.full_name


@pytest.mark.django_db
def test_teacher_verification_with_certificates(teacher_verification, certificate):
    """
    Test adding certificates to TeacherVerification.
    """
    teacher_verification.certificates.add(certificate)

    assert teacher_verification.certificates.count() == 1
    assert teacher_verification.certificates.first() == certificate
