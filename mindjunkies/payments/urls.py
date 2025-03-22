from django.urls import path

from .views import CheckoutFailedView, CheckoutSuccessView, checkout

urlpatterns = [
    path("<slug:course_slug>/checkout/", checkout, name="checkout"),
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
