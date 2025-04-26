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
def lecture_pdf(db, lecture):
    pdf = baker.make("lecture.LecturePDF", lecture=lecture)
    with patch("cloudinary.models.CloudinaryField.url", new_callable=PropertyMock) as mock_url:
        mock_url.return_value = "https://res.cloudinary.com/demo/upload/sample.pdf"
        yield pdf


@pytest.fixture
def course_token(db, course, user):
    return baker.make("courses.CourseToken", course=course, teacher=user, status="approved")


@pytest.fixture
def live_class(db, course, staff_user):
    return baker.make(
        "courses.LiveClass",
        course=course,
        teacher=staff_user,
        scheduled_at=timezone.now(),
        duration=60,
        status="Ongoing"
    )


@pytest.fixture
def live_class_today(db, course, staff_user):
    return baker.make(
        "courses.LiveClass",
        course=course,
        teacher=staff_user,
        scheduled_at=timezone.now(),
        duration=60,
        status="Upcoming"
    )


@pytest.fixture
def live_class_this_week(db, course, staff_user):
    return baker.make(
        "courses.LiveClass",
        course=course,
        teacher=staff_user,
        scheduled_at=timezone.now() + timedelta(days=2),
        duration=60,
        status="Upcoming"
    )


@pytest.mark.django_db
def test_lecture_home_view_success(client, user, course, module, live_class, live_class_today, live_class_this_week):
    """Test LectureHomeView displays course, modules, and live classes for enrolled users."""
    baker.make("courses.Enrollment", course=course, student=user)
    client.force_login(user)
    response = client.get(reverse("lecture_home", kwargs={"course_slug": course.slug}))
    assert response.status_code == 200
    assert "course" in response.context
    assert "modules" in response.context
    assert "current_module" in response.context
    assert "current_live_class" in response.context
    assert "todays_live_classes" in response.context
    assert "this_weeks_live_classes" in response.context
    assert response.context["course"] == course
    assert response.context["current_module"] == module
    assert response.context["current_live_class"] == live_class
    assert live_class_today in response.context["todays_live_classes"]
    assert live_class_this_week in response.context["this_weeks_live_classes"]


@pytest.mark.django_db
def test_lecture_home_view_unauthenticated(client, course):
    """Test LectureHomeView redirects unauthenticated users."""
    response = client.get(reverse("lecture_home", kwargs={"course_slug": course.slug}))
    assert response.status_code == 302
    assert response.url.startswith(reverse("account_login"))


@pytest.mark.django_db
def test_lecture_video_view_success(client, user, course, module, lecture, lecture_video):
    """Test lecture_video view displays video for enrolled users."""
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
    assert response.context["video"] == lecture_video
    assert "hls_url" in response.context
    assert lecture.lastvisitedmodule_set.filter(user=user, module=module).exists()


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
def test_lecture_pdf_view_success(client, user, course, module, lecture, lecture_pdf):
    """Test lecture_pdf view displays PDF for enrolled users."""
    baker.make("courses.Enrollment", course=course, student=user)
    client.force_login(user)
    url = reverse(
        "lecture_pdf",
        kwargs={
            "course_slug": course.slug,
            "module_id": module.id,
            "lecture_id": lecture.id,
            "pdf_id": lecture_pdf.id,
        },
    )
    response = client.get(url)
    assert response.status_code == 200
    assert "pdf" in response.context
    assert response.context["pdf"] == lecture_pdf


@pytest.mark.django_db
def test_lecture_pdf_view_forbidden(client, user, course, module, lecture, lecture_pdf):
    """Test lecture_pdf forbids access for non-enrolled users."""
    client.force_login(user)
    url = reverse(
        "lecture_pdf",
        kwargs={
            "course_slug": course.slug,
            "module_id": module.id,
            "lecture_id": lecture.id,
            "pdf_id": lecture_pdf.id,
        },
    )
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_create_lecture_view_success(client, staff_user, course, module):
    """Test CreateLectureView creates a lecture for staff users."""
    client.force_login(staff_user)
    url = reverse(
        "create_lecture",
        kwargs={"course_slug": course.slug, "module_id": module.id},
    )
    data = {"title": "New Lecture", "description": "Lecture description", "order": 1}
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert any("Lecture created successfully" in str(m) for m in get_messages(response.wsgi_request))
    assert response.redirect_chain[-1][0] == f"{reverse('lecture_home', kwargs={'course_slug': course.slug})}?module_id={module.id}"
    


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
def test_create_content_video_success(client, user, course, lecture, course_token):
    """Test CreateContentView creates video content for authorized users."""
    client.force_login(user)
    url = reverse(
        "create_content",
        kwargs={"course_slug": course.slug, "lecture_id": lecture.id, "format": "video"},
    )
    data = {
        "video_title": "Test Video",  # Adjusted field name based on original test
        "video_file": SimpleUploadedFile(
            "test_video.mp4", b"file_content", content_type="video/mp4"
        ),
    }
   


@pytest.mark.django_db
def test_create_content_pdf_success(client, user, course, lecture, course_token):
    """Test CreateContentView creates PDF content for authorized users."""
    client.force_login(user)
    url = reverse(
        "create_content",
        kwargs={"course_slug": course.slug, "lecture_id": lecture.id, "format": "attachment"},
    )
    data = {
        "pdf_title": "Test PDF",  # Adjusted field name based on original test
        "pdf_file": SimpleUploadedFile(
            "test.pdf", b"file_content", content_type="application/pdf"
        ),
    }
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert any("Lecture Attachment uploaded successfully" in str(m) for m in get_messages(response.wsgi_request))
    assert response.redirect_chain[-1][0] == reverse("lecture_home", kwargs={"course_slug": course.slug})
    assert lecture.pdf_files.filter(pdf_title="Test PDF").exists()


@pytest.mark.django_db
def test_create_content_pending_token(client, user, course, lecture):
    """Test CreateContentView blocks users with pending CourseToken."""
    baker.make("courses.CourseToken", course=course, teacher=user, status="pending")
    client.force_login(user)
    url = reverse(
        "create_content",
        kwargs={"course_slug": course.slug, "lecture_id": lecture.id, "format": "video"},
    )
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert any("This course is not approved yet" in str(m) for m in get_messages(response.wsgi_request))
    assert response.redirect_chain[-1][0] == reverse("lecture_home", kwargs={"course_slug": course.slug})


@pytest.mark.django_db
def test_create_content_no_token(client, user, course, lecture):
    """Test CreateContentView blocks users without CourseToken."""
    client.force_login(user)
    url = reverse(
        "create_content",
        kwargs={"course_slug": course.slug, "lecture_id": lecture.id, "format": "video"},
    )
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert any("You do not have permission for this course" in str(m) for m in get_messages(response.wsgi_request))
    assert response.redirect_chain[-1][0] == reverse("lecture_home", kwargs={"course_slug": course.slug})


@pytest.mark.django_db
def test_edit_lecture_view_success(client, staff_user, course, lecture):
    """Test EditLectureView updates lecture for staff users."""
    client.force_login(staff_user)
    url = reverse(
        "edit_lecture",
        kwargs={"course_slug": course.slug, "lecture_id": lecture.id},
    )
    data = {"title": "Updated Lecture", "description": "Updated description", "order": 1}
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert any("Lecture saved successfully" in str(m) for m in get_messages(response.wsgi_request))
    assert response.redirect_chain[-1][0] == reverse("lecture_home", kwargs={"course_slug": course.slug})
    lecture.refresh_from_db()
    assert lecture.title == "Updated Lecture"


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
def test_delete_lecture_view_success(client, staff_user, course, lecture):
    """Test DeleteLectureView deletes lecture for staff users."""
    client.force_login(staff_user)
    url = reverse(
        "delete_lecture",
        kwargs={"course_slug": course.slug, "lecture_id": lecture.id},
    )
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert any("Lecture deleted successfully" in str(m) for m in get_messages(response.wsgi_request))
    assert response.redirect_chain[-1][0] == reverse("lecture_home", kwargs={"course_slug": course.slug})
    assert not lecture.__class__.objects.filter(id=lecture.id).exists()


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
def test_mark_lecture_complete_view_success(client, user, course, module, lecture, lecture_video):
    """Test MarkLectureCompleteView marks lecture as complete for enrolled users."""
    baker.make("courses.Enrollment", course=course, student=user)
    client.force_login(user)
    url = reverse(
        "mark_lecture_complete",
        kwargs={"course_slug": course.slug, "lecture_id": lecture.id},
    )
    referer_url = reverse(
        "lecture_video_content",
        kwargs={
            "course_slug": course.slug,
            "module_id": module.id,
            "lecture_id": lecture.id,
            "video_id": lecture_video.id,
        },
    )
    response = client.get(url, HTTP_REFERER=referer_url, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[-1][0] == referer_url
    assert lecture.lecturecompletion_set.filter(user=user).exists()


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
def test_module_edit_view_success(client, staff_user, course, module):
    """Test ModuleEditView updates module for staff users."""
    client.force_login(staff_user)
    url = reverse(
        "edit_module",
        kwargs={"course_slug": course.slug, "module_id": module.id},
    )
    data = {"title": "Updated Module", "order": 1}
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert any("Module saved successfully" in str(m) for m in get_messages(response.wsgi_request))
    assert response.redirect_chain[-1][0] == reverse("lecture_home", kwargs={"course_slug": course.slug})
    module.refresh_from_db()
    assert module.title == "Updated Module"


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


@pytest.mark.django_db
def test_delete_module_view_success(client, staff_user, course, module):
    """Test DeleteModuleView deletes module for staff users."""
    client.force_login(staff_user)
    url = reverse(
        "delete_module",
        kwargs={"course_slug": course.slug, "module_id": module.id},
    )
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert any("Module deleted successfully" in str(m) for m in get_messages(response.wsgi_request))
    assert response.redirect_chain[-1][0] == reverse("lecture_home", kwargs={"course_slug": course.slug})
    assert not module.__class__.objects.filter(id=module.id).exists()


@pytest.mark.django_db
def test_delete_module_view_forbidden(client, user, course, module):
    """Test DeleteModuleView forbids non-teachers."""
    client.force_login(user)
    url = reverse(
        "delete_module",
        kwargs={"course_slug": course.slug, "module_id": module.id},
    )
    response = client.get(url)
    assert response.status_code == 403