import pytest
from categories.models import Category
from django.urls import reverse
from model_bakery import baker

from mindjunkies.courses.models import Course, CourseCategory, CourseToken, Enrollment, LastVisitedCourse, Rating

pytestmark = pytest.mark.django_db


def test_course_list_authenticated(client, django_user_model):
    user = baker.make(django_user_model)
    course = baker.make(Course)
    baker.make(Enrollment, student=user, course=course)

    client.force_login(user)
    response = client.get(reverse("course_list"))

    assert response.status_code == 200
    assert course.title.encode() in response.content


def test_category_courses_view(client):
    parent_category = baker.make(
        CourseCategory, name="Parent Category", slug="parent-category"
    )
    sub_category = baker.make(
        CourseCategory, name="Sub Category", parent=parent_category
    )

    CourseCategory._tree_manager.rebuild()

    course_1 = baker.make(Course, category=parent_category, title="Parent Course")
    course_2 = baker.make(Course, category=sub_category, title="Sub Course")

    url = reverse("category_courses", args=[parent_category.slug])
    response = client.get(url)
    content = response.content.decode("utf-8")
    print()
    print(content)
    print()

    assert response.status_code == 200
    assert course_1.title in content
    assert course_2.title in content


def test_rating_create_view_new(client):
    user = baker.make("accounts.User")
    course = baker.make(Course)
    baker.make(Enrollment, course=course, student=user)

    client.force_login(user)
    url = reverse("rate_course", kwargs={"course_slug": course.slug})

    response = client.post(url, {"rating": 5, "review": "Great!"})
    assert response.status_code == 302
    assert Rating.objects.filter(course=course, student=user).exists()


def test_rating_create_view_existing(client):
    user = baker.make("accounts.User")
    course = baker.make(Course)
    baker.make(Rating, course=course, student=user, rating=3, review="Okay")

    client.force_login(user)
    url = reverse("rate_course", kwargs={"course_slug": course.slug})

    response = client.get(url)
    assert response.status_code == 200
    assert b"Okay" in response.content
