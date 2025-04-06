import pytest
from django.utils.text import slugify

from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course, Module
from mindjunkies.lecture.models import Lecture, LecturePDF, LectureVideo


@pytest.fixture
def teacher(db):
    return User.objects.create_user(username="test_teacher", password="password")


@pytest.fixture
def course(db, teacher):
    return Course.objects.create(title="Test Course", teacher=teacher)


@pytest.fixture
def module(db, course):
    return Module.objects.create(title="Test Module", course=course)


@pytest.fixture
def lecture(db, course, module):
    return Lecture.objects.create(
        course=course,
        module=module,
        title="Test Lecture",
        description="This is a test lecture.",
        learning_objective="Learn Django testing.",
        order=1,
    )


@pytest.mark.django_db
def test_lecture_creation(lecture):
    assert lecture.title == "Test Lecture"
    assert lecture.slug == slugify("Test Lecture")
    assert lecture.course.title == "Test Course"
    assert lecture.module.title == "Test Module"


@pytest.mark.django_db
def test_lecture_slug_auto_generation(course, module):
    lecture = Lecture.objects.create(
        course=course,
        module=module,
        title="New Lecture",
    )
    assert lecture.slug == slugify("New Lecture")


@pytest.fixture
def lecture_pdf(db, lecture):
    return LecturePDF.objects.create(
        lecture=lecture, pdf_file="lecture_pdfs/test.pdf", pdf_title="Test PDF"
    )


@pytest.mark.django_db
def test_lecture_pdf_creation(lecture_pdf):
    assert lecture_pdf.pdf_title == "Test PDF"
    assert lecture_pdf.lecture.title == "Test Lecture"


@pytest.fixture
def lecture_video(db, lecture):
    return LectureVideo.objects.create(
        lecture=lecture,
        video_file="lecture_videos/test.mp4",
        video_title="Test Video",
        status=LectureVideo.PENDING,
    )


@pytest.mark.django_db
def test_lecture_video_creation(lecture_video):
    assert lecture_video.video_title == "Test Video"
    assert lecture_video.status == LectureVideo.PENDING
