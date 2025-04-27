import pytest
from django.urls import reverse
from model_bakery import baker
from unittest.mock import patch
from django.contrib.messages import get_messages

from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course, Enrollment
from mindjunkies.payments.models import Transaction, Balance, BalanceHistory


@pytest.fixture
def user(db):
    return baker.make(User)


@pytest.fixture
def course(db, user):
    return baker.make(Course, teacher=user, course_price=1000)


@pytest.fixture
def enrollment(db, user, course):
    return baker.make(Enrollment, student=user, course=course, status='pending')


@pytest.fixture
def gateway(db):
    return baker.make('payments.PaymentGateway', store_id='test_store', store_pass='test_pass')


@pytest.fixture
def client_logged(client, user):
    client.force_login(user)
    return client


@pytest.fixture
def ssl_success_data(user, course):
    return {
        'value_a': user.username,
        'value_b': course.slug,
        'tran_id': 'TXN12345',
        'val_id': 'VAL12345',
        'amount': 1000,
        'card_type': 'VISA',
        'card_no': '123456******1234',
        'store_amount': 1000,
        'bank_tran_id': 'BANK123',
        'status': 'VALID',
        'tran_date': '2025-04-30 10:00:00',
        'currency': 'BDT',
        'card_issuer': 'Test Bank',
        'card_brand': 'VISA',
        'card_issuer_country': 'Bangladesh',
        'card_issuer_country_code': 'BD',
        'verify_sign': 'test_signature',
        'verify_sign_sha2': 'test_signature_sha2',
        'currency_rate': 1.0,
        'risk_title': 'Safe',
        'risk_level': '0'
    }


@pytest.mark.django_db
def test_checkout_redirects_if_not_logged_in(client, course):
    url = reverse('checkout', args=[course.slug])
    response = client.get(url)

    assert response.status_code == 302
    assert reverse('account_login') in response.url
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert messages[0].message == "You need to be logged in to enroll in a course."


@patch('mindjunkies.payments.views.SSLCOMMERZ')
def test_checkout_success_redirects_to_gateway(mock_sslcommerz, client_logged, course, gateway):
    mock_sslcommerz.return_value.createSession.return_value = {"status": "SUCCESS",
                                                               "GatewayPageURL": "https://sslcommerz.com/gateway"}

    url = reverse('checkout', args=[course.slug])
    response = client_logged.get(url)

    assert response.status_code == 302
    assert response.url.startswith("https://sslcommerz.com")


@patch('mindjunkies.payments.views.SSLCOMMERZ')
def test_checkout_fails_with_no_gateway(mock_sslcommerz, client_logged, course, db):
    from mindjunkies.payments.models import PaymentGateway
    PaymentGateway.objects.all().delete()

    url = reverse('checkout', args=[course.slug])
    response = client_logged.get(url)

    assert response.status_code == 302
    assert reverse('home') in response.url


def test_checkout_redirects_if_already_enrolled(client_logged, course, enrollment):
    enrollment.status = 'active'
    enrollment.save()

    url = reverse('checkout', args=[course.slug])
    response = client_logged.get(url)

    assert response.status_code == 302
    assert reverse('home') in response.url


@pytest.mark.django_db
def test_checkout_success(client_logged, course, enrollment, ssl_success_data):
    url = reverse('checkout_success', args=[course.slug])
    response = client_logged.post(url, data=ssl_success_data)

    enrollment.refresh_from_db()

    assert response.status_code == 200
    assert enrollment.status == 'active'
    assert Transaction.objects.filter(tran_id='TXN12345').exists()
    assert BalanceHistory.objects.filter(user=course.teacher).exists()


@pytest.mark.django_db
def test_checkout_success_handles_errors(client_logged):
    url = reverse('checkout_success', args=['non-existent-slug'])
    response = client_logged.post(url, data={})

    assert response.status_code == 302
    assert reverse('home') in response.url


@pytest.fixture
def ssl_failed_data(user, course):
    return {
        'value_a': user.username,
        'value_b': course.slug,
    }


@pytest.mark.django_db
def test_checkout_failed(client_logged, course, enrollment, ssl_failed_data):
    url = reverse('checkout_failed', args=[course.slug])
    response = client_logged.post(url, data=ssl_failed_data)

    enrollment.refresh_from_db()

    assert response.status_code == 200
    assert enrollment.status == 'withdrawn'


@pytest.mark.django_db
def test_checkout_failed_handles_errors(client_logged):
    url = reverse('checkout_failed', args=['non-existent-slug'])
    response = client_logged.post(url, data={})

    assert response.status_code == 200
