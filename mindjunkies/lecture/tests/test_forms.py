import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker

from mindjunkies.lecture.forms import LectureForm, LecturePDFForm, LectureVideoForm, ModuleForm
from mindjunkies.courses.models import Module
from mindjunkies.lecture.models import Lecture, LecturePDF, LectureVideo


@pytest.fixture
def module():
    return baker.make(Module)


@pytest.fixture
def lecture(module):
    return baker.make(Lecture, module=module)


@pytest.mark.django_db
def test_lecture_form_creates_slug_correctly(module):
    course = baker.make('courses.Course', title='Test Course')
    module.course = course
    module.save()

    form = LectureForm(data={
        'title': 'Test Lecture Title',
        'description': 'A description',
        'learning_objective': 'Learn something',
        'order': 1,
    })
    assert form.is_valid()

    instance = form.save(commit=False)
    instance.module = module
    instance.course = course
    instance.save()

    assert instance.slug.startswith('test-lecture-title')
    assert instance.course == course


@pytest.mark.django_db
def test_module_form_creates_slug_correctly():
    course = baker.make('courses.Course', title='Test Course')
    form = ModuleForm(data={
        'title': 'New Module',
        'order': 1,
    })

    assert form.is_valid()
    instance = form.save(commit=False)
    instance.course = course
    instance = form.save()
    assert instance.title == 'New Module'


@pytest.mark.django_db
def test_lecture_pdf_form_accepts_valid_pdf(lecture):
    pdf_content = b'%PDF-1.4 test pdf content'
    pdf_file = SimpleUploadedFile('testfile.pdf', pdf_content, content_type='application/pdf')

    form = LecturePDFForm(data={'pdf_title': 'Test PDF'}, files={'pdf_file': pdf_file})
    assert form.is_valid()

    instance = form.save(commit=False, lecture=lecture)
    instance.save()

    assert instance.pdf_title == 'Test PDF'
    assert instance.lecture == lecture


@pytest.mark.django_db
def test_lecture_pdf_form_rejects_invalid_extension():
    fake_pdf = SimpleUploadedFile('not_a_pdf.txt', b'Fake content', content_type='text/plain')

    form = LecturePDFForm(data={'pdf_title': 'Bad PDF'}, files={'pdf_file': fake_pdf})
    assert not form.is_valid()
    assert 'pdf_file' in form.errors


@pytest.mark.django_db
def test_lecture_video_form_accepts_valid_video():
    video_content = b'video content'
    video_file = SimpleUploadedFile('testvideo.mp4', video_content, content_type='video/mp4')

    form = LectureVideoForm(data={'video_title': 'Test Video'}, files={'video_file': video_file})
    assert form.is_valid()

    instance = form.save(commit=False)
    assert instance.video_title == 'Test Video'


@pytest.mark.django_db
def test_lecture_video_form_rejects_invalid_extension():
    fake_video = SimpleUploadedFile('not_a_video.txt', b'Fake video content', content_type='text/plain')

    form = LectureVideoForm(data={'video_title': 'Bad Video'}, files={'video_file': fake_video})
    assert not form.is_valid()
    assert 'video_file' in form.errors
