from django.urls import path

from .views import TeacherVerificationView, content_list, enrollment_list, remove_enrollment, verification_wait

urlpatterns = [
    path("content/", content_list, name="dashboard"),
    path(
        "enrollments/<str:slug>/", enrollment_list, name="teacher_dashboard_enrollments"
    ),
    path(
        "remove/enrollment/<slug:course_slug>/<str:student_id>/",
        remove_enrollment,
        name="dashboard_enrollments_remove",
    ),
    path(
        "teacher_verification/",
        TeacherVerificationView.as_view(),
        name="teacher_verification_form",
    ),
    path("verification_wait/", verification_wait, name="verification_wait"),
]
