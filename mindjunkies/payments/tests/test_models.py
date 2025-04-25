import pytest
from decouple import config
from django.db.utils import IntegrityError
from model_bakery import baker

from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course, Enrollment
from mindjunkies.payments.models import PaymentGateway, Transaction


@pytest.mark.django_db
def test_create_transaction():
    """Test creating a transaction successfully."""
    user = baker.make(User)
    course = baker.make(Course)
    enrollment = baker.make(Enrollment)

    transaction = Transaction.objects.create(
        user=user,
        course=course,
        enrollment=enrollment,
        name="SSLCommerz Payment",
        amount=1500.00,
        tran_id="TXN12345",
        val_id="VAL67890",
        card_type="VISA",
        store_amount=1480.00,
        card_no="123456XXXXXX7890",
        bank_tran_id="BANKTXN0001",
        status="Completed",
        tran_date="2025-03-15 12:30:00",
        currency="BDT",
        card_issuer="Bank ABC",
        card_brand="Visa",
        card_issuer_country="Bangladesh",
        card_issuer_country_code="BD",
        currency_rate=1.00,
        verify_sign="abcd1234",
        verify_sign_sha2="sha256hash",
        risk_level="0",
        risk_title="Low Risk",
    )

    assert transaction.user == user
    assert transaction.course == course
    assert transaction.status == "Completed"
    assert str(transaction) == f"{user.username} - {course.title}"


@pytest.mark.django_db
def test_transaction_unique_together():
    """Test unique_together constraint (user, course)."""
    user = baker.make(User)
    course = baker.make(Course)

    # Create the first transaction
    baker.make(Transaction, user=user, course=course)

    # Creating another transaction for the same user & course should raise IntegrityError
    with pytest.raises(IntegrityError):
        baker.make(Transaction, user=user, course=course)


@pytest.mark.django_db
def test_create_payment_gateway():
    """Test creating a PaymentGateway entry."""
    gateway = PaymentGateway.objects.create(
        store_id="STORE_123", store_pass=config("TEST_PASS")
    )

    assert gateway.store_id == "STORE_123"
    assert gateway.store_pass == config("TEST_PASS")
    assert str(gateway) == "STORE_123"


@pytest.mark.django_db
def test_transaction_str():
    """Test __str__() method for Transaction model."""
    user = baker.make(User, username="testuser")
    course = baker.make(Course, title="Django Course")

    transaction = baker.make(Transaction, user=user, course=course)

    assert str(transaction) == f"{user.username} bought - {course.title}"


@pytest.mark.django_db
def test_payment_gateway_str():
    """Test __str__() method for PaymentGateway model."""
    gateway = baker.make(PaymentGateway, store_id="TEST_STORE")

    assert str(gateway) == "TEST_STORE"
