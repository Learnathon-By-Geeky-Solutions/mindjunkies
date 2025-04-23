from django.urls import path

from .views import (ContentListView, EnrollmentListView, RemoveEnrollmentView, TeacherVerificationView,
                    VerificationWaitView, DraftView,ArchiveView)

urlpatterns = [
    path("teacher/", TeacherVerificationView.as_view(), name="teacher_permission"),
    path("content/<str:status>/", ContentListView.as_view(), name="dashboard"),
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
    path('content/draft',DraftView.as_view(),name='draft_content' ),
    path('content/archive',ArchiveView.as_view(),name='archive_content' ),
]
