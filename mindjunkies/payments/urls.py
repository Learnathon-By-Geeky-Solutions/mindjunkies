from django.urls import path

from .views import CheckoutFailedView, CheckoutSuccessView, CheckoutView

urlpatterns = [
    path("<slug:course_slug>/checkout/", CheckoutView.as_view(), name="checkout"),
    path(
        "<slug:course_slug>/success/",
        CheckoutSuccessView.as_view(),
        name="checkout_success",
    ),
    path(
        "<slug:course_slug>/failed/",
        CheckoutFailedView.as_view(),
        name="checkout_failed",
    ),
]
