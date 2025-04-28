import pytest
from django.urls import reverse
from model_bakery import baker
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.contrib.messages import get_messages
from django.db import IntegrityError
from django.test import RequestFactory
from django.http import HttpResponseForbidden
from django.contrib.auth.models import AnonymousUser

from mindjunkies.courses.models import Course, Module, CourseToken
from mindjunkies.lecture.models import Lecture, LectureVideo, LecturePDF, LectureCompletion, LastVisitedModule
from mindjunkies.lecture.views import check_course_enrollment, get_current_live_class, CreateContentView, \
    ModuleEditView, lecture_video
from mindjunkies.lecture.forms import LecturePDFForm, LectureVideoForm
from mindjunkies.live_classes.models import LiveClass
from mindjunkies.accounts.models import User

from conftest import add_middleware_to_request


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def user(db):
    return baker.make('accounts.User')


@pytest.fixture
def teacher_user(db):
    return baker.make('accounts.User', is_teacher=True)


@pytest.fixture
def student_user():
    return baker.make(User, is_teacher=False)


@pytest.fixture
def course(db, teacher_user):
    return baker.make(Course, teacher=teacher_user)


@pytest.fixture
def module(db, course):
    return baker.make(Module, course=course)


@pytest.fixture
def lecture(db, course, module):
    return baker.make(Lecture, course=course, module=module)


@pytest.fixture
def video(db, lecture):
    return baker.make(LectureVideo, lecture=lecture)


@pytest.fixture
def pdf(db, lecture):
    return baker.make(LecturePDF, lecture=lecture)


@pytest.fixture
def course_token(db, course, teacher_user):
    return baker.make('courses.CourseToken', course=course, teacher=teacher_user, status="approved")


@pytest.mark.django_db
def test_check_course_enrollment_returns_true_if_token_approved(user, course):
    baker.make('courses.CourseToken', course=course, teacher=user, status="approved")
    result = check_course_enrollment(user, course)

    assert result is True


@pytest.mark.django_db
def test_check_course_enrollment_returns_false_if_token_not_approved(user, course):
    baker.make('courses.CourseToken', course=course, teacher=user, status="pending")
    result = check_course_enrollment(user, course)

    assert result is False


@pytest.mark.django_db
def test_check_course_enrollment_returns_false_if_no_course_token(user, course):
    result = check_course_enrollment(user, course)

    assert result is False


@pytest.mark.django_db
def test_get_current_live_class_returns_live_class_if_in_progress(course):
    now = timezone.now()

    # Live class started 5 minutes ago, ends in 55 minutes
    live_class = baker.make(
        LiveClass,
        course=course,
        teacher=course.teacher,
        scheduled_at=now - timedelta(minutes=5),
        duration=60,
    )

    result = get_current_live_class(course)

    assert result == live_class


@pytest.mark.django_db
def test_get_current_live_class_returns_none_if_class_in_future(course):
    now = timezone.now()

    # Live class starts in 10 minutes
    baker.make(
        LiveClass,
        course=course,
        teacher=course.teacher,
        scheduled_at=now + timedelta(minutes=10),
        duration=60,
    )

    result = get_current_live_class(course)

    assert result is None


@pytest.mark.django_db
def test_get_current_live_class_returns_none_if_class_ended(course):
    now = timezone.now()

    # Live class ended 30 minutes ago
    baker.make(
        LiveClass,
        course=course,
        teacher=course.teacher,
        scheduled_at=now - timedelta(minutes=90),
        duration=60,
    )

    result = get_current_live_class(course)

    assert result is None


@pytest.mark.django_db
def test_get_current_live_class_returns_none_if_no_classes(course):
    # No live classes created
    result = get_current_live_class(course)

    assert result is None


@pytest.mark.django_db
def test_lecture_home_enrolled_user(client, user, course, module, course_token):
    baker.make('courses.Enrollment', student=user, course=course, status='active')
    client.force_login(user)

    url = reverse('lecture_home', kwargs={"course_slug": course.slug})
    response = client.get(url)

    assert response.status_code == 200
    assert "lecture/lecture_home.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_lecture_pdf_view(client, user, pdf):
    pdf.pdf_file = "test.pdf"  # Assign a valid file path or mock file
    pdf.save()

    client.force_login(user)

    url = reverse('lecture_pdf', kwargs={
        "course_slug": pdf.lecture.course.slug,
        "module_id": pdf.lecture.module.id,
        "lecture_id": pdf.lecture.id,
        "pdf_id": pdf.id,
    })
    response = client.get(url)

    assert response.status_code == 200
    assert "lecture/lecture_pdf.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_create_lecture_view_get(client, teacher_user, course, module, course_token):
    client.force_login(teacher_user)

    url = reverse('create_lecture', kwargs={
        "course_slug": course.slug,
        "module_id": module.id,
    })
    response = client.get(url)

    assert response.status_code == 200
    assert "lecture/create_lecture.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_create_module_view_get(client, teacher_user, course, course_token):
    client.force_login(teacher_user)

    url = reverse('create_module', kwargs={"course_slug": course.slug})
    response = client.get(url)

    assert response.status_code == 200
    assert "lecture/create_module.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_delete_lecture_view(client, teacher_user, course, lecture):
    client.force_login(teacher_user)

    url = reverse('delete_lecture', kwargs={"course_slug": course.slug, "lecture_id": lecture.id})
    response = client.get(url)

    assert response.status_code == 302
    assert not Lecture.objects.filter(id=lecture.id).exists()


@pytest.mark.django_db
def test_delete_module_view(client, teacher_user, course, module):
    client.force_login(teacher_user)

    url = reverse('delete_module', kwargs={"course_slug": course.slug, "module_id": module.id})
    response = client.get(url)

    assert response.status_code == 302
    assert not Module.objects.filter(id=module.id).exists()


@pytest.mark.django_db
def test_mark_lecture_complete(client, user, lecture):
    client.force_login(user)

    url = reverse('mark_lecture_complete', kwargs={"course_slug": lecture.course.slug, "lecture_id": lecture.id})
    response = client.get(url)

    assert response.status_code == 302
    assert LectureCompletion.objects.filter(user=user, lecture=lecture).exists()


@pytest.mark.django_db
def test_dispatch_allows_access_when_token_approved(factory, teacher_user, course, lecture):
    request = factory.get('/')
    request.user = teacher_user

    baker.make(CourseToken, course=course, teacher=teacher_user, status='approved')

    view = CreateContentView.as_view()

    response = view(request, course_slug=course.slug, lecture_id=lecture.id, format='attachment')

    assert response.status_code == 200


@pytest.mark.django_db
def test_dispatch_redirects_if_token_pending(factory, teacher_user, course, lecture):
    request = factory.get('/')
    request.user = teacher_user

    baker.make(CourseToken, course=course, teacher=teacher_user, status='pending')

    response = CreateContentView.as_view()(request, course_slug=course.slug, lecture_id=lecture.id,
                                           format='attachment')

    assert response.status_code == 302
    assert reverse("lecture_home", kwargs={"course_slug": course.slug}) in response.url


@pytest.mark.django_db
def test_dispatch_redirects_if_no_token(factory, teacher_user, course, lecture):
    request = factory.get('/')
    request.user = teacher_user

    response = CreateContentView.as_view()(request, course_slug=course.slug, lecture_id=lecture.id,
                                           format='attachment')

    assert response.status_code == 302
    assert reverse("lecture_home", kwargs={"course_slug": course.slug}) in response.url


@pytest.mark.django_db
def test_get_form_class_attachment(factory, teacher_user, course, lecture):
    request = factory.get('/')
    request.user = teacher_user

    view = CreateContentView()
    view.request = request
    view.kwargs = {"format": "attachment", "lecture_id": lecture.id, "course_slug": course.slug}
    view.course = course
    view.lecture = lecture

    assert view.get_form_class() == LecturePDFForm


@pytest.mark.django_db
def test_get_form_class_video(factory, teacher_user, course, lecture):
    request = factory.get('/')
    request.user = teacher_user

    view = CreateContentView()
    view.request = request
    view.kwargs = {"format": "video", "lecture_id": lecture.id, "course_slug": course.slug}
    view.course = course
    view.lecture = lecture

    assert view.get_form_class() == LectureVideoForm


@pytest.mark.django_db
def test_get_form_class_invalid_format(factory, teacher_user, course, lecture):
    request = factory.get('/')
    request = add_middleware_to_request(request)
    request.user = teacher_user

    view = CreateContentView()
    view.request = request
    view.kwargs = {"format": "invalid", "lecture_id": lecture.id, "course_slug": course.slug}
    view.course = course
    view.lecture = lecture

    with pytest.raises(ValueError):
        view.get_form_class()


@pytest.mark.django_db
def test_form_valid_saves_content_correctly(factory, teacher_user, course, lecture):
    request = factory.get('/')
    request = add_middleware_to_request(request)
    request.user = teacher_user

    form = LecturePDFForm(data={'pdf_title': 'Test PDF'}, files={})
    view = CreateContentView()
    view.request = request
    view.kwargs = {"format": "attachment", "lecture_id": lecture.id, "course_slug": course.slug}
    view.course = course
    view.lecture = lecture

    class DummyForm:
        def save(self, commit=False):
            instance = baker.make('lecture.LecturePDF')
            return instance

    result = view.form_valid(DummyForm())

    assert result.status_code == 302
    assert reverse("lecture_home", kwargs={"course_slug": course.slug}) in result.url


@pytest.mark.django_db
def test_dispatch_redirects_if_token_pending(factory, course, lecture, teacher_user):
    request = factory.get('/')
    request = add_middleware_to_request(request)

    request.user = teacher_user

    response = CreateContentView.as_view()(request, course_slug=course.slug, lecture_id=lecture.id)
    assert response.status_code == 302


@pytest.mark.django_db
def test_dispatch_redirects_if_no_token(factory, course, lecture, teacher_user):
    request = factory.get('/')
    request = add_middleware_to_request(request)

    request.user = teacher_user

    response = CreateContentView.as_view()(request, course_slug=course.slug, lecture_id=lecture.id)
    assert response.status_code == 302


@pytest.mark.django_db
def test_dispatch_allows_teacher(factory, teacher_user, course, module):
    request = factory.get('/')
    request.user = teacher_user

    view = ModuleEditView()
    view.request = request
    view.kwargs = {"module_id": module.id, "course_slug": course.slug}
    view.course = course

    response = view.dispatch(request, module_id=module.id, course_slug=course.slug)

    assert response.status_code != 403  # Not forbidden


@pytest.mark.django_db
def test_dispatch_forbids_non_teacher(factory, student_user, course, module):
    request = factory.get('/')
    request.user = student_user

    view = ModuleEditView()
    view.request = request
    view.kwargs = {"module_id": module.id, "course_slug": course.slug}
    view.course = course

    response = view.dispatch(request, module_id=module.id, course_slug=course.slug)

    assert isinstance(response, HttpResponseForbidden)


@pytest.mark.django_db
def test_get_object_fetches_correct_module(factory, teacher_user, course, module):
    request = factory.get('/')
    request.user = teacher_user

    view = ModuleEditView()
    view.request = request
    view.kwargs = {"module_id": module.id, "course_slug": course.slug}

    found_module = view.get_object()

    assert found_module == module


@pytest.mark.django_db
def test_form_valid_calls_handle_form_validation(factory, teacher_user, course, module):
    request = factory.post('/')
    request.user = teacher_user

    view = ModuleEditView()
    view.request = request
    view.kwargs = {"module_id": module.id, "course_slug": course.slug}
    view.course = course

    dummy_form = object()

    view.handle_form_validation = lambda form, message: "handled"

    result = view.form_valid(dummy_form)

    assert result == "handled"


@pytest.mark.django_db
def test_get_success_url_returns_correct_redirect(factory, teacher_user, course, module):
    request = factory.get('/')
    request.user = teacher_user

    view = ModuleEditView()
    view.request = request
    view.kwargs = {"module_id": module.id, "course_slug": course.slug}

    result = view.get_success_url(module)

    assert reverse("lecture_home", kwargs={'course_slug': course.slug}) in result.url


@pytest.mark.django_db
def test_get_context_data_includes_module_and_course(factory, teacher_user, course, module):
    request = factory.get('/')
    request.user = teacher_user

    view = ModuleEditView()
    view.request = request
    view.kwargs = {"module_id": module.id, "course_slug": course.slug}
    view.course = course
    view.object = module

    context = view.get_context_data()

    assert context["module"] == module
    assert context["course"] == course


@pytest.mark.django_db
def test_lecture_video_forbidden_if_not_enrolled(factory, teacher_user, course, module, lecture, video, monkeypatch):
    """Test forbidden if user not enrolled."""

    request = factory.get('/')
    request.user = teacher_user

    monkeypatch.setattr('mindjunkies.lecture.views.check_course_enrollment', lambda user, course: False)

    response = lecture_video(request, course_slug=course.slug, module_id=module.id, lecture_id=lecture.id,
                             video_id=video.id)

    assert isinstance(response, HttpResponseForbidden)


@pytest.mark.django_db
def test_last_visited_module_created(factory, teacher_user, course, module, lecture, video, monkeypatch):
    """Test if LastVisitedModule is created."""

    request = factory.get('/')
    request.user = teacher_user

    monkeypatch.setattr('mindjunkies.lecture.views.check_course_enrollment', lambda user, course: True)

    assert LastVisitedModule.objects.count() == 0

    lecture_video(request, course_slug=course.slug, module_id=module.id, lecture_id=lecture.id, video_id=video.id)

    assert LastVisitedModule.objects.count() == 1


@pytest.mark.django_db
def test_lecture_video_not_found(factory, teacher_user, course, module, lecture):
    """Test 404 error if lecture video not found."""

    request = factory.get('/')
    request.user = teacher_user

    with pytest.raises(Exception):
        lecture_video(request, course_slug=course.slug, module_id=module.id, lecture_id=lecture.id,
                      video_id=999999)  # Nonexistent video
