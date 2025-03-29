import secrets
import string

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.views.generic import View
from sslcommerz_lib import SSLCOMMERZ

from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course, Enrollment

from .models import PaymentGateway, Transaction


def unique_transaction_id_generator(
    size=10, chars=string.ascii_uppercase + string.digits
):
    return "".join(secrets.choice(chars) for _ in range(size))


@require_GET
def checkout(request, course_slug):
    """Initiate checkout and redirect to SSLCommerz payment gateway."""
    user = request.user
    course = get_object_or_404(Course, slug=course_slug)

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
    post_body = {}
    post_body["total_amount"] = course.course_price
    post_body["currency"] = "BDT"
    post_body["tran_id"] = transaction_id
    post_body["success_url"] = f"http://localhost:8000/payment/{course_slug}/success/"
    post_body["fail_url"] = f"http://localhost:8000/payment/{course_slug}/failed/"
    post_body["cancel_url"] = "http://localhost:8000/"
    post_body["emi_option"] = 0
    post_body["cus_name"] = user.username
    post_body["cus_email"] = user.email
    post_body["cus_phone"] = "01700000000"
    post_body["cus_add1"] = "Goalpara"
    post_body["cus_city"] = "Thakurgaon"
    post_body["cus_country"] = "Bangladesh"
    post_body["shipping_method"] = "NO"
    post_body["multi_card_name"] = ""
    post_body["num_of_item"] = 1
    post_body["product_name"] = course.title
    post_body["product_category"] = str(course.category)
    post_body["product_profile"] = "general"

    post_body["value_a"] = user.username
    post_body["value_b"] = course.slug

    try:
        response = sslcommez.createSession(post_body)
        if response["status"] == "SUCCESS":
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

            # Update enrollment status
            enrollment.status = "active"
            enrollment.save()

            messages.success(request, "Payment Successful")
            return render(request, self.template_name, {"enrollment": enrollment})

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
