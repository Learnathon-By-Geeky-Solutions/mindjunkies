import pytest
from django.utils.text import slugify
from model_bakery import baker

from mindjunkies.courses.models import Course, Module
from mindjunkies.lecture.models import Lecture, LecturePDF, LectureVideo


@pytest.mark.django_db
class TestLectureModel:
    def test_lecture_str_returns_title_with_course(self):
        course = baker.make(Course, title="Python 101")
        module = baker.make(Module, course=course)
        lecture = baker.make(Lecture, course=course, module=module, title="Intro")

        assert str(lecture) == "Python 101 - Intro"

    def test_lecture_slug_is_generated_on_save(self):
        course = baker.make(Course)
        module = baker.make(Module, course=course)
        lecture = baker.make(
            Lecture, course=course, module=module, title="My First Lecture", slug=""
        )

        assert lecture.slug == slugify("My First Lecture")

    def test_lecture_ordering(self):
        course = baker.make(Course)
        module = baker.make(Module, course=course)
        baker.make(Lecture, course=course, module=module, order=3)
        baker.make(Lecture, course=course, module=module, order=1)
        baker.make(Lecture, course=course, module=module, order=2)

        ordered_lectures = Lecture.objects.all()
        assert [lec.order for lec in ordered_lectures] == [1, 2, 3]


@pytest.mark.django_db
class TestLecturePDFModel:
    def test_lecture_pdf_str(self):
        lecture = baker.make(Lecture)
        pdf = baker.make(LecturePDF, lecture=lecture, pdf_title="Week 1 Notes")

        assert str(pdf) == f"PDF for {lecture.title}"


@pytest.mark.django_db
class TestLectureVideoModel:
    def test_lecture_video_str(self):
        video = baker.make(LectureVideo, video_title="Lecture 1 - Intro")
        assert str(video) == "Lecture 1 - Intro"

    def test_lecture_video_status_default(self):
        video = baker.make(LectureVideo)
        assert video.status == LectureVideo.PENDING

    def test_lecture_video_fields_optional(self):
        video = baker.make(LectureVideo, hls=None, thumbnail=None)
        assert video.hls is None
        assert video.thumbnail.name is None
