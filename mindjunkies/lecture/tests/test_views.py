import pytest
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils import timezone
from model_bakery import baker
from django.contrib.messages import get_messages
from datetime import timedelta
from unittest.mock import PropertyMock, patch

from mindjunkies.courses.models import Enrollment
from mindjunkies.dashboard.tests.test_views import enrollment

baker.generators.add(
    CloudinaryField, lambda: "https://res.cloudinary.com/demo/upload/sample.pdf"
)

User = get_user_model()


@pytest.fixture
def user(db):
    return baker.make(User, is_staff=False)


@pytest.fixture
def staff_user(db):
    return baker.make(User, is_staff=True)


@pytest.fixture
def course(db, staff_user):
    return baker.make("courses.Course", teacher=staff_user, slug="test-course")


@pytest.fixture
def module(db, course):
    return baker.make("courses.Module", course=course, order=1)


@pytest.fixture
def lecture(db, module, course):
    return baker.make("lecture.Lecture", module=module, course=course)


@pytest.fixture
def lecture_video(db, lecture):
    return baker.make("lecture.LectureVideo", lecture=lecture)


@pytest.fixture
def course_token(db, course, user):
    return baker.make("courses.CourseToken", course=course, teacher=user, status="approved")


@pytest.fixture
def live_class(db, course, staff_user):
    return baker.make(
        "live_classes.LiveClass",
        course=course,
        teacher=staff_user,
        scheduled_at=timezone.now(),
        duration=60,
        status="Ongoing"
    )


@pytest.fixture
def live_class_today(db, course, staff_user):
    return baker.make(
        "live_classes.LiveClass",
        course=course,
        teacher=staff_user,
        scheduled_at=timezone.now(),
        duration=60,
        status="Upcoming"
    )


@pytest.fixture
def live_class_this_week(db, course, staff_user):
    return baker.make(
        "live_classes.LiveClass",
        course=course,
        teacher=staff_user,
        scheduled_at=timezone.now() + timedelta(days=2),
        duration=60,
        status="Upcoming"
    )


@pytest.mark.django_db
def test_lecture_video_view_forbidden(client, user, course, module, lecture, lecture_video):
    """Test lecture_video forbids access for non-enrolled users."""
    client.force_login(user)
    url = reverse(
        "lecture_video_content",
        kwargs={
            "course_slug": course.slug,
            "module_id": module.id,
            "lecture_id": lecture.id,
            "video_id": lecture_video.id,
        },
    )
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_create_lecture_view_forbidden(client, user, course, module):
    """Test CreateLectureView forbids non-teacher users."""
    client.force_login(user)
    url = reverse(
        "create_lecture",
        kwargs={"course_slug": course.slug, "module_id": module.id},
    )
    response = client.get(url)
    assert response.status_code == 403  # Expecting forbidden for non-teachers


@pytest.mark.django_db
def test_edit_lecture_view_forbidden(client, user, course, lecture):
    """Test EditLectureView forbids non-teacher users."""
    client.force_login(user)
    url = reverse(
        "edit_lecture",
        kwargs={"course_slug": course.slug, "lecture_id": lecture.id},
    )
    response = client.get(url)
    assert response.status_code == 403  # Expecting forbidden for non-teachers


@pytest.mark.django_db
def test_delete_lecture_view_forbidden(client, user, course, lecture):
    """Test DeleteLectureView forbids non-teachers."""
    client.force_login(user)
    url = reverse(
        "delete_lecture",
        kwargs={"course_slug": course.slug, "lecture_id": lecture.id},
    )
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_mark_lecture_complete_view_unauthenticated(client, course, lecture):
    """Test MarkLectureCompleteView redirects unauthenticated users."""
    url = reverse(
        "mark_lecture_complete",
        kwargs={"course_slug": course.slug, "lecture_id": lecture.id},
    )
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse("account_login"))


@pytest.mark.django_db
def test_module_edit_view_forbidden(client, user, course, module):
    """Test ModuleEditView forbids non-teacher users."""
    client.force_login(user)
    url = reverse(
        "edit_module",
        kwargs={"course_slug": course.slug, "module_id": module.id},
    )
    response = client.get(url)
    assert response.status_code == 403  # Expecting forbidden for non-teachers
