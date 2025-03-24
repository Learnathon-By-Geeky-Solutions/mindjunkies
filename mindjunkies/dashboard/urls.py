from django.urls import path

from .views import content_list, enrollment_list, remove_enrollment, teacher_verification_view, verification_wait

urlpatterns = [
    # Add your URL patterns here
    path("content/", content_list, name="dashboard"),
    path(
        "enrollments/<str:slug>/", enrollment_list, name="teacher_dashboard_enrollments"
    ),
    path(
        "remove/enrollment/<slug:course_slug>/<str:student_id>/",
        remove_enrollment,
        name="dashboard_enrollments_remove",
    ),
    path('teacher_verification/', teacher_verification_view, name='teacher_verification_form'),
        path('verification_wait/', verification_wait, name='teacher_wait'),

]
