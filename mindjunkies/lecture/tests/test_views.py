import pytest
from django.urls import reverse
from model_bakery import baker

from mindjunkies.courses.models import Course, Module, CourseToken
from mindjunkies.lecture.models import Lecture, LectureVideo, LecturePDF, LectureCompletion


@pytest.fixture
def user(db):
    return baker.make('accounts.User')


@pytest.fixture
def teacher_user(db):
    return baker.make('accounts.User', is_teacher=True)


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
    return baker.make(CourseToken, course=course, teacher=teacher_user, status="approved")


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
