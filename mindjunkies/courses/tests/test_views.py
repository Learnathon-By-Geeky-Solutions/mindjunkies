import pytest
from django.urls import reverse
from model_bakery import baker
from django.core.files.uploadedfile import SimpleUploadedFile

from mindjunkies.courses.models import Course


@pytest.fixture
def user(db):
    return baker.make('accounts.User')


@pytest.fixture
def teacher_user(db):
    return baker.make('accounts.User', is_teacher=True)


@pytest.fixture
def course(db, teacher_user):
    return baker.make('courses.Course', teacher=teacher_user)


@pytest.fixture
def enrollment(db, user, course):
    return baker.make('courses.Enrollment', student=user, course=course, status="active")


@pytest.fixture
def category(db):
    return baker.make('courses.CourseCategory')


@pytest.fixture
def rating(db, user, course):
    return baker.make('courses.Rating', student=user, course=course)


@pytest.mark.django_db
def test_course_list(client):
    url = reverse('course_list')
    response = client.get(url)
    assert response.status_code == 200
    assert "courses/course_list.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_new_course_view(client, user):
    client.force_login(user)
    url = reverse('new_course')
    response = client.get(url)
    assert response.status_code == 200
    assert "courses/new_course.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_popular_courses_view(client, user):
    client.force_login(user)
    url = reverse('popular_course')
    response = client.get(url)
    assert response.status_code == 200
    assert "courses/popular_course.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_my_courses_view(client, user, enrollment):
    client.force_login(user)
    url = reverse('my_courses')
    response = client.get(url)
    assert response.status_code == 200
    assert "courses/my_course.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_create_course_get(client, teacher_user):
    client.force_login(teacher_user)
    url = reverse('create_course')
    response = client.get(url)
    assert response.status_code == 200
    assert "courses/create_course.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_create_course_get_pending_token(client, teacher_user):
    client.force_login(teacher_user)
    baker.make('courses.CourseToken', teacher=teacher_user, status="pending")
    url = reverse('create_course')
    response = client.get(url)
    assert response.status_code == 302
    assert reverse('dashboard') in response.url


@pytest.mark.django_db
def test_create_course_post_success(client, teacher_user, category):
    course = "courses.Course"
    client.force_login(teacher_user)
    url = reverse('create_course')

    data = {
        'title': 'Test Course',
        'short_introduction': 'Short intro',
        'course_description': 'Description',
        'level': 'beginner',
        'category': category.id,
        'course_price': 100
    }

    response = client.post(url, data)
    assert response.status_code == 302  # Redirect after success
    assert Course.objects.filter(title="Test Course").exists()


@pytest.mark.django_db
def test_course_details_view(client, course):
    url = reverse('course_details', kwargs={"slug": course.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert "courses/course_details.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_user_course_list(client, user, enrollment):
    client.force_login(user)
    url = reverse('my_course_list')
    response = client.get(url)
    assert response.status_code == 200
    assert "courses/course_list.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_category_courses_view(client, category):
    url = reverse('category_courses', kwargs={"slug": category.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert "courses/category_courses.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_rating_create_view_get(client, user, course):
    client.force_login(user)
    url = reverse('rate_course', kwargs={"course_slug": course.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert "courses/rate_course.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_rating_create_own_course(client, teacher_user, course):
    client.force_login(teacher_user)
    course.teacher = teacher_user
    course.save()

    url = reverse('rate_course', kwargs={"course_slug": course.slug})
    response = client.get(url)

    assert response.status_code == 302
    assert reverse('lecture_home', kwargs={"course_slug": course.slug}) in response.url


@pytest.mark.django_db
def test_delete_course_view(client, teacher_user, course):
    client.force_login(teacher_user)
    url = reverse('delete_course', kwargs={"course_slug": course.slug})
    response = client.get(url)
    assert response.status_code == 302
    assert not Course.objects.filter(slug=course.slug).exists()
