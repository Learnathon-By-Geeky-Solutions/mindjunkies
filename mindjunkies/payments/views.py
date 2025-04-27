import secrets
import string

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.views.generic import View
from sslcommerz_lib import SSLCOMMERZ

from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course, Enrollment

from .models import PaymentGateway, Transaction, Balance, BalanceHistory


def unique_transaction_id_generator(
    size=10, chars=string.ascii_uppercase + string.digits
):
    trans_id = "".join(secrets.choice(chars) for _ in range(size))
    if Transaction.objects.filter(tran_id=trans_id).exists():
        return unique_transaction_id_generator(size, chars)
    return trans_id


@method_decorator(require_GET, name="dispatch")
class CheckoutView(View, LoginRequiredMixin):
    def get(self, request, course_slug):
        if not request.user.is_authenticated:
            messages.error(request, "You need to be logged in to enroll in a course.")
            return redirect("account_login")
        user = request.user
        course = get_object_or_404(Course, slug=course_slug)

        Balance.objects.get_or_create(user=course.teacher, defaults={"amount": 0})

        transaction_id = unique_transaction_id_generator()
        enrollment, _ = Enrollment.objects.get_or_create(
            student=user,
            course=course,
        )

        if enrollment.status == "active":
            messages.success(request, "You have already enrolled in this course")
            return redirect("home")

        enrollment.status = "pending"
        enrollment.save()

        gateway = PaymentGateway.objects.first()
        if not gateway:
            messages.error(request, "Payment gateway not configured.")
            return redirect("home")

        sslcz_settings = {
            "store_id": gateway.store_id,
            "store_pass": gateway.store_pass,
            "issandbox": True,
        }

        sslcommez = SSLCOMMERZ(sslcz_settings)
        post_body = {
            "total_amount": course.course_price,
            "currency": "BDT",
            "tran_id": transaction_id,
            "success_url": f"http://localhost:8000/payment/{course_slug}/success/",
            "fail_url": f"http://localhost:8000/payment/{course_slug}/failed/",
            "cancel_url": "http://localhost:8000/",
            "emi_option": 0,
            "cus_name": user.username,
            "cus_email": user.email,
            "cus_phone": "01700000000",
            "cus_add1": "Goalpara",
            "cus_city": "Thakurgaon",
            "cus_country": "Bangladesh",
            "shipping_method": "NO",
            "multi_card_name": "",
            "num_of_item": 1,
            "product_name": course.title,
            "product_category": str(course.category),
            "product_profile": "general",
            "value_a": user.username,
            "value_b": course.slug,
        }

        try:
            response = sslcommez.createSession(post_body)
            if response.get("status") == "SUCCESS":
                return redirect(response["GatewayPageURL"])
        except Exception as e:
            print(f"Error in initiating payment: {e}")

        messages.error(request, "Payment gateway initialization failed")
        return redirect("home")


@method_decorator(csrf_exempt, name="dispatch")
class CheckoutSuccessView(View):
    """Handles payment success response from SSLCommerz."""

    template_name = "payments/checkout_success.html"

    def post(self, request, *args, **kwargs):
        """Process successful payments and update enrollment status."""
        data = self.request.POST
        try:
            user = get_object_or_404(User, username=data["value_a"])
            course = get_object_or_404(Course, slug=data["value_b"])
            enrollment = get_object_or_404(Enrollment, student=user, course=course)

            Transaction.objects.create(
                user=user,
                course=course,
                name=user.username,
                enrollment=enrollment,
                tran_id=data["tran_id"],
                val_id=data["val_id"],
                amount=data["amount"],
                card_type=data["card_type"],
                card_no=data["card_no"],
                store_amount=data["store_amount"],
                bank_tran_id=data["bank_tran_id"],
                status=data["status"],
                tran_date=data["tran_date"],
                currency=data["currency"],
                card_issuer=data["card_issuer"],
                card_brand=data["card_brand"],
                card_issuer_country=data["card_issuer_country"],
                card_issuer_country_code=data["card_issuer_country_code"],
                verify_sign=data["verify_sign"],
                verify_sign_sha2=data["verify_sign_sha2"],
                currency_rate=data["currency_rate"],
                risk_title=data["risk_title"],
                risk_level=data["risk_level"],
            )

            # BalanceHistory.objects.create(user=user, transaction)
            teacher = course.teacher
            balance, _ = Balance.objects.get_or_create(user=user, defaults={"amount": 0})

            transaction = Transaction.objects.get(tran_id=data["tran_id"])
            prev_balance = teacher.balance.amount
            teacher.balance.amount += course.course_price
            balance.save()

            new_balance = balance.amount

            BalanceHistory.objects.create(
                user=teacher,
                transaction=transaction,
                amount=course.course_price,
                new_balance=new_balance,
                previous_balance=prev_balance,
                description="Enrollment successful"
            )

            # Update enrollment status
            enrollment.status = "active"
            enrollment.save()

            messages.success(request, "Payment Successful")
            return render(request, self.template_name, {"enrollment": enrollment, "course": course})

        except Exception as e:
            print(f"Error in processing success response: {e}")
            messages.error(
                request, "Something went wrong while processing the payment."
            )
            return redirect("home")


@method_decorator(csrf_exempt, name="dispatch")
class CheckoutFailedView(View):
    """Handles failed payment responses."""

    template_name = "payments/failed.html"

    def post(self, request, *args, **kwargs):
        """Process failed payments."""
        data = self.request.POST
        print(f"Payment Failed Response: {data}")

        try:
            user = get_object_or_404(User, username=data["value_a"])
            course = get_object_or_404(Course, slug=data["value_b"])
            enrollment = get_object_or_404(Enrollment, student=user, course=course)

            enrollment.status = "withdrawn"
            enrollment.save()

            messages.error(request, "Payment Failed. Please try again.")
        except Exception as e:
            print(f"Error in processing failed payment: {e}")
            messages.error(request, "Payment failure processing error.")

        return render(request, self.template_name)
