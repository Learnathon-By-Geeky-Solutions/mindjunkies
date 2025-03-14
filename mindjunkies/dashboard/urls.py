from django.urls import path

from .views import content_list, enrollment_list, remove_enrollment

urlpatterns = [
    # Add your URL patterns here
    path("content/", content_list, name="dashboard_content"),
    path(
        "enrollments/<str:slug>/", enrollment_list, name="teacher_dashboard_enrollments"
    ),
    path(
        "remove/enrollment/<slug:course_slug>/<str:student_id>/",
        remove_enrollment,
        name="dashboard_enrollments_remove",
    ),
]
