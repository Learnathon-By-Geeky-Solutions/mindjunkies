from django.urls import path

from mindjunkies.dashboard.views import ContentListView, EnrollmentListView, RemoveEnrollmentView, TeacherVerificationView,
from mindjunkies.dashboard.views import TeacherPermissionView, VerificationWaitView
urlpatterns = [
    path("teacher/", TeacherPermissionView.as_view(), name="teacher_permission"),
    path("content/", ContentListView.as_view(), name="dashboard"),
    path(
        "enrollments/<str:slug>/",
        EnrollmentListView.as_view(),
        name="teacher_dashboard_enrollments",
    ),
    path(
        "remove/enrollment/<slug:course_slug>/<str:student_id>/",
        RemoveEnrollmentView.as_view(),
        name="dashboard_enrollments_remove",
    ),
    path(
        "teacher_verification/",
        TeacherVerificationView.as_view(),
        name="teacher_verification_form",
    ),
    path(
        "verification_wait/", VerificationWaitView.as_view(), name="verification_wait"
    ),

]
