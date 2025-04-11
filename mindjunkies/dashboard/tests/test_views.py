import pytest
from django.urls import reverse
from model_bakery import baker

from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course, Enrollment


@pytest.mark.django_db
class TestTeacherDashboardViews:
    def test_content_list_requires_login(self, client):
        url = reverse("dashboard")
        response = client.get(url)
        assert response.status_code == 302  # Redirect to login

    def test_content_list_view_for_teacher(self, client):
        teacher = baker.make(User)
        client.force_login(teacher)
        courses = baker.make(Course, teacher=teacher, _quantity=3)

        url = reverse("dashboard")
        response = client.get(url)

        assert response.status_code == 302  # Redirect to teacher verification

    def test_enrollment_list_view_requires_login(self, client):
        course = baker.make(Course)
        url = reverse("teacher_dashboard_enrollments", args=[course.slug])
        response = client.get(url)
        assert response.status_code == 302

    def test_enrollment_list_view_for_teacher(self, client):
        teacher = baker.make(User)
        course = baker.make(Course, teacher=teacher)
        students = baker.make(User, _quantity=2)
        for student in students:
            baker.make(Enrollment, student=student, course=course)

        client.force_login(teacher)
        url = reverse("teacher_dashboard_enrollments", args=[course.slug])
        response = client.get(url)

        assert response.status_code == 200
        for student in students:
            assert student.username in response.content.decode()

    def test_remove_enrollment_requires_login(self, client):
        course = baker.make(Course)
        student = baker.make(User)
        url = reverse("dashboard_enrollments_remove", args=[course.slug, student.uuid])
        response = client.get(url)
        assert response.status_code == 302

    def test_remove_enrollment_view(self, client):
        teacher = baker.make(User)
        student = baker.make(User)
        course = baker.make(Course, teacher=teacher)
        enrollment = baker.make(Enrollment, student=student, course=course)

        client.force_login(teacher)
        url = reverse("dashboard_enrollments_remove", args=[course.slug, student.uuid])
        response = client.get(url)

        assert response.status_code == 302
        assert not Enrollment.objects.filter(student=student, course=course).exists()
        course.refresh_from_db()
        assert course.get_total_enrollments() == 0
