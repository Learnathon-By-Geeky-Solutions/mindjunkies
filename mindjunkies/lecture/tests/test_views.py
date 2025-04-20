from datetime import timedelta

import pytest
from cloudinary.models import CloudinaryField
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils import timezone
from model_bakery import baker

baker.generators.add(
    CloudinaryField, lambda: "https://res.cloudinary.com/demo/video/upload/sample.mp4"
)


@pytest.fixture
def user(db, django_user_model):
    return baker.make(django_user_model, is_staff=False)


@pytest.fixture
def staff_user(db, django_user_model):
    return baker.make(django_user_model, is_staff=True)


@pytest.fixture
def course(db, staff_user):
    return baker.make("courses.Course", teacher=staff_user)


@pytest.fixture
def module(db, course):
    return baker.make("courses.Module", course=course)


@pytest.fixture
def lecture(db, module, course):
    return baker.make("lecture.Lecture", module=module, course=course)


@pytest.fixture
def lecture_video(db, lecture):
    return baker.make("lecture.LectureVideo", lecture=lecture)


@pytest.fixture
def lecture_pdf(db, lecture):
    return baker.make("lecture.LecturePDF", lecture=lecture)


@pytest.mark.django_db
def test_lecture_home_view(client, user, course, module):
    client.force_login(user)
    response = client.get(reverse("lecture_home", kwargs={"course_slug": course.slug}))
    assert response.status_code == 200
    assert "course" in response.context
    assert response.context["course"] == course


@pytest.mark.django_db
def test_lecture_video_view(client, user, course, module, lecture, lecture_video):
    baker.make("courses.Enrollment", course=course, student=user)
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
    assert response.status_code == 200
    assert "video" in response.context


@pytest.mark.django_db
def test_lecture_video_forbidden_for_non_enrolled(
    client, user, course, module, lecture, lecture_video
):
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
def test_lecture_pdf_view(client, user, lecture, lecture_pdf):
    client.force_login(user)
    url = reverse(
        "create_content",
        kwargs={
            "course_slug": lecture.course.slug,
            "lecture_slug": lecture.slug,
            "format": "attachment",
        },
    )

    pdf_file = SimpleUploadedFile(
        "test.pdf", b"PDF content", content_type="application/pdf"
    )
    response = client.post(url, {"pdf_file": pdf_file, "pdf_title": "Sample PDF"})

    assert response.status_code == 302
    assert "Lecture Attachment uploaded successfully!" in [
        str(m) for m in response.wsgi_request._messages
    ]


@pytest.mark.django_db
def test_create_lecture_view(client, staff_user, module, course):
    client.force_login(staff_user)
    url = reverse(
        "create_lecture", kwargs={"course_slug": course.slug, "module_id": module.id}
    )
    response = client.post(
        url, {"title": "New Lecture", "description": "Lecture description", "order": 1}
    )

    assert response.status_code == 302
    assert "Lecture created successfully!" in [
        str(m) for m in response.wsgi_request._messages
    ]


@pytest.mark.django_db
def test_create_content_view_video(client, staff_user, lecture):
    client.force_login(staff_user)
    url = reverse(
        "create_content",
        kwargs={
            "course_slug": lecture.course.slug,
            "lecture_slug": lecture.slug,
            "format": "video",
        },
    )

    import os

    from django.conf import settings

    video_path = os.path.join(settings.BASE_DIR, "tests", "media", "test_video.mp4")
    with open(video_path, "rb") as video:
        video_file = SimpleUploadedFile(
            "test_video.mp4", video.read(), content_type="video/mp4"
        )

    response = client.post(
        url, {"video_file": video_file, "video_title": "Sample Video"}
    )

    assert response.status_code == 302
    assert "Lecture Video uploaded successfully!" in [
        str(m) for m in response.wsgi_request._messages
    ]


@pytest.mark.django_db
def test_edit_lecture_view(client, staff_user, lecture):
    client.force_login(staff_user)
    url = reverse(
        "edit_lecture",
        kwargs={"course_slug": lecture.course.slug, "lecture_slug": lecture.slug},
    )

    response = client.post(
        url,
        {"title": "Updated Lecture", "description": "Updated description", "order": 1},
    )

    assert response.status_code == 302
    assert "Lecture saved successfully!" in [
        str(m) for m in response.wsgi_request._messages
    ]


@pytest.mark.django_db
def test_create_module_view(client, staff_user, course):
    client.force_login(staff_user)
    url = reverse("create_module", kwargs={"course_slug": course.slug})

    response = client.post(url, {"title": "New Module", "order": 1})

    assert response.status_code == 302
    assert "Module created successfully!" in [
        str(m) for m in response.wsgi_request._messages
    ]
