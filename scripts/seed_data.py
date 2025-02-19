import json
import os
from django.utils import timezone
from django.db import transaction

from accounts.models import User, Profile
from courses.models import Courses, CourseTeacher, Enrollment


@transaction.atomic
def create_entities(data: dict) -> None:
    # Create users
    for user_data in data['users']:
        _user, _created = User.objects.get_or_create(
            uuid=user_data['uuid'],
            defaults={
                'username': user_data['username'],
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'role': user_data['role'],
            }
        )
    print("✅ User created successfully.")

    # Create profiles
    for profile_data in data['profiles']:
        user = User.objects.get(uuid=profile_data['user'])
        Profile.objects.get_or_create(
            user=user,
            defaults={
                'birthday': profile_data['birthday'],
                'bio': profile_data['bio'],
                'avatar': profile_data['avatar'],
                'phone_number': profile_data['phone_number'],
                'address': profile_data['address'],
            }
        )
    print("✅ Profile created successfully.")

    # Create courses
    for course_data in data['courses']:
        published_on = course_data['published_on']
        if published_on:
            published_on = timezone.datetime.fromisoformat(published_on)
            if timezone.is_naive(published_on):
                published_on = timezone.make_aware(published_on)

        Courses.objects.get_or_create(
            title=course_data['title'],
            defaults={
                'short_introduction': course_data['short_introduction'],
                'course_description': course_data['course_description'],
                'preview_video_link': course_data['preview_video_link'],
                'published': course_data['published'],
                'upcoming': course_data['upcoming'],
                'published_on': published_on,
                'paid_course': course_data['paid_course'],
                'course_price': course_data['course_price'],
                'slug': course_data['slug'],
                'total_rating': course_data['total_rating'],
                'number_of_ratings': course_data['number_of_ratings'],
            }
        )
    print("✅ Course created successfully.")

    # Create course teachers
    for course_teacher_data in data['course_teachers']:
        course = Courses.objects.get(title=course_teacher_data['course'])
        teacher = User.objects.get(uuid=course_teacher_data['teacher'])
        CourseTeacher.objects.get_or_create(
            course=course,
            teacher=teacher,
            defaults={'role': course_teacher_data['role']}
        )
    print("✅ Course-teacher created successfully.")

    # Create enrollments
    for enrollment_data in data['enrollments']:
        course = Courses.objects.get(title=enrollment_data['course'])
        student = User.objects.get(uuid=enrollment_data['student'])
        Enrollment.objects.get_or_create(
            course=course,
            student=student,
            defaults={'status': enrollment_data['status']}
        )
    print("✅ Enrollment created successfully.")


def run() -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'dummy_data.json')

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"❌ Error: {file_path} not found")
        return
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON format in {file_path}")
        return

    try:
        create_entities(data)
        print("🎉 Data loaded successfully")
    except (User.DoesNotExist, Courses.DoesNotExist) as e:
        print(f"❌ Entity not found: {str(e)}")
    except KeyError as e:
        print(f"❌ Missing required field: {str(e)}")
    except ValueError as e:
        print(f"❌ Invalid data format: {str(e)}")
    except Exception as e:
        print(f"❌ Error during data seeding: {str(e)}")
