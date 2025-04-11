import pytest
from model_bakery import baker

from mindjunkies.courses.models import (Course, CourseCategory, CourseInfo, CourseToken, Enrollment, LastVisitedCourse,
                                        Module, Rating)


@pytest.mark.django_db
def test_course_category_str():
    category = baker.make(CourseCategory, name="Development")
    assert str(category) == "Development"


@pytest.mark.django_db
def test_course_str_and_slug():
    teacher = baker.make("accounts.User")
    course = baker.make(Course, title="Python Basics", teacher=teacher, slug="")
    course.save()
    assert str(course) == "Python Basics"
    assert course.slug == "python-basics"


@pytest.mark.django_db
def test_course_update_rating():
    student = baker.make("accounts.User")
    teacher = baker.make("accounts.User")
    course = baker.make(Course, teacher=teacher)
    baker.make(Rating, course=course, student=student, rating=4)
    course.update_rating()
    assert course.total_rating == 4
    assert course.number_of_ratings == 1


@pytest.mark.django_db
def test_course_get_total_enrollments():
    course = baker.make(Course)
    baker.make(Enrollment, course=course, status="active", _quantity=3)
    baker.make(Enrollment, course=course, status="withdrawn", _quantity=2)
    assert course.get_total_enrollments() == 3


@pytest.mark.django_db
def test_course_info_str():
    course = baker.make(Course)
    course_info = baker.make(CourseInfo, course=course)
    assert str(course_info) == f"{course.title} - Course Info"


@pytest.mark.django_db
def test_rating_str_and_save():
    course = baker.make(Course)
    student = baker.make("accounts.User")
    rating = baker.make(Rating, course=course, student=student, rating=5)
    rating.save()
    assert str(rating) == f"{student.username} rated {course.title} 5/5"


@pytest.mark.django_db
def test_enrollment_str():
    course = baker.make(Course)
    student = baker.make("accounts.User")
    enrollment = baker.make(Enrollment, course=course, student=student)
    assert str(enrollment) == f"{student.username} enrolled in {course.title}"


@pytest.mark.django_db
def test_module_str():
    course = baker.make(Course)
    module = baker.make(Module, title="Intro", course=course)
    assert str(module) == f"Intro - {course.title}"


@pytest.mark.django_db
def test_course_token_str():
    user = baker.make("accounts.User")
    course = baker.make(Course)
    token = baker.make(CourseToken, teacher=user, course=course, status="accepted")
    assert str(token) == f"Token for {course.title} by {user.username}"


@pytest.mark.django_db
def test_last_visited_course_str():
    user = baker.make("accounts.User")
    course = baker.make(Course)
    visit = baker.make(LastVisitedCourse, user=user, course=course)
    assert str(visit) == f"{user.username} - {course.title} - {visit.last_visited}"
