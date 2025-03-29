import pytest
import requests_mock
from django.contrib.messages import get_messages
from django.urls import reverse
from model_bakery import baker

from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course, Enrollment
from mindjunkies.payments.models import PaymentGateway, Transaction


@pytest.mark.django_db
def test_checkout_successful_redirect(client):
    """Test that checkout redirects to SSLCommerz payment gateway."""
    user = baker.make(User)
    course = baker.make(Course, course_price=500)

    # Ensure a payment gateway exists
    baker.make(PaymentGateway, store_id="test_store", store_pass="test_pass")

    client.force_login(user)  # Log in as the user

    url = reverse("checkout", kwargs={"course_slug": course.slug})

    with requests_mock.Mocker() as mock_request:
        mock_request.post(
            "https://sandbox.sslcommerz.com/gwprocess/v4/api.php",
            json={"status": "SUCCESS", "GatewayPageURL": "https://payment.test.url"},
        )

        response = client.get(url)

    assert response.status_code == 302
    assert response.url == "https://payment.test.url"

    # Check that an enrollment was created
    enrollment = Enrollment.objects.filter(student=user, course=course).first()
    assert enrollment is not None
    assert enrollment.payments == "pending"


@pytest.mark.django_db
def test_checkout_missing_gateway(client):
    """Test that checkout fails when PaymentGateway is missing."""
    user = baker.make(User)
    course = baker.make(Course, course_price=500)
    client.force_login(user)

    url = reverse("checkout", kwargs={"course_slug": course.slug})
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse("home")

    messages = [msg.message for msg in get_messages(response.wsgi_request)]
    assert "Payment gateway not configured." in messages


@pytest.mark.django_db
def test_checkout_already_enrolled(client):
    """Test that users already enrolled in a course cannot checkout again."""
    user = baker.make(User)
    course = baker.make(Course)
    baker.make(PaymentGateway, store_id="test_store", store_pass="test_pass")

    # Create a completed enrollment
    baker.make(Enrollment, student=user, course=course, status="active")

    client.force_login(user)
    url = reverse("checkout", kwargs={"course_slug": course.slug})
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse("home")

    messages = [msg.message for msg in get_messages(response.wsgi_request)]
    assert "You have already enrolled in this course" in messages


@pytest.mark.django_db
def test_checkout_successful_payment(client):
    """Test successful payment processing."""
    user = baker.make(User, username="testuser")
    course = baker.make(Course, slug="test-course")
    baker.make(
        Enrollment,
        student=user,
        course=course,
        status="pending",
    )

    client.force_login(user)

    url = reverse("checkout_success", kwargs={"course_slug": "test-course"})
    data = {
        "value_a": "testuser",
        "value_b": "test-course",
        "tran_id": "TXN123",
        "val_id": "VAL67890",
        "status": "Completed",
        "amount": "500.00",
        "card_type": "VISA",
        "card_no": "123456XXXXXX7890",
        "store_amount": "490.00",
        "bank_tran_id": "BANK123",
        "tran_date": "2025-03-15 12:30:00",
        "currency": "BDT",
        "card_issuer": "Bank ABC",
        "card_brand": "Visa",
        "card_issuer_country": "Bangladesh",
        "card_issuer_country_code": "BD",
        "verify_sign": "abcd1234",
        "verify_sign_sha2": "sha256hash",
        "currency_rate": "1.00",
        "risk_title": "Low Risk",
        "risk_level": "0",
    }

    response = client.post(url, data)

    assert response.status_code == 200
    assert Transaction.objects.filter(tran_id="TXN123").exists()

    enrollment = Enrollment.objects.get(student=user, course=course)
    assert enrollment.payment_status == "completed"
    assert enrollment.status == "active"

    messages = [msg.message for msg in get_messages(response.wsgi_request)]
    assert "Payment Successful" in messages


@pytest.mark.django_db
def test_checkout_failed_payment(client):
    """Test failed payment handling."""
    user = baker.make(User, username="testuser")
    course = baker.make(Course, slug="test-course")
    baker.make(
        Enrollment,
        student=user,
        course=course,
        status="pending",
    )

    client.force_login(user)

    url = reverse("checkout_failed", kwargs={"course_slug": "test-course"})
    data = {
        "value_a": "testuser",
        "value_b": "test-course",
        "tran_id": "TXN123",
        "status": "Failed",
    }

    response = client.post(url, data)

    assert response.status_code == 200

    enrollment = Enrollment.objects.get(student=user, course=course)
    assert enrollment.payment_status == "failed"

    messages = [msg.message for msg in get_messages(response.wsgi_request)]
    assert "Payment Failed. Please try again." in messages
