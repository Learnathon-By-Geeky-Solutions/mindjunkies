import json
import os
from django.utils import timezone

from accounts.models import User, Profile
from classrooms.models import Classroom, ClassroomTeacher, Enrollment


def run():
    # Get the absolute path to the dummy_data.json file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'dummy_data.json')

    with open(file_path, 'r') as file:
        data = json.load(file)

    # Create users
    for user_data in data['users']:
        user, _created = User.objects.get_or_create(
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

    # Create classrooms
    for classroom_data in data['classrooms']:
        published_on = classroom_data['published_on']
        if published_on:
            published_on = timezone.datetime.fromisoformat(published_on)
            if timezone.is_naive(published_on):
                published_on = timezone.make_aware(published_on)

        Classroom.objects.get_or_create(
            title=classroom_data['title'],
            defaults={
                'short_introduction': classroom_data['short_introduction'],
                'course_description': classroom_data['course_description'],
                'course_image': classroom_data['course_image'],
                'preview_video_link': classroom_data['preview_video_link'],
                'published': classroom_data['published'],
                'upcoming': classroom_data['upcoming'],
                'published_on': published_on,
                'paid_course': classroom_data['paid_course'],
                'course_price': classroom_data['course_price'],
                'slug': classroom_data['slug'],
                'total_rating': classroom_data['total_rating'],
                'number_of_ratings': classroom_data['number_of_ratings'],
            }
        )
    print("✅ Classroom created successfully.")

    # Create classroom teachers
    for classroom_teacher_data in data['classroom_teachers']:
        classroom = Classroom.objects.get(title=classroom_teacher_data['classroom'])
        teacher = User.objects.get(uuid=classroom_teacher_data['teacher'])
        ClassroomTeacher.objects.get_or_create(
            classroom=classroom,
            teacher=teacher,
            defaults={'role': classroom_teacher_data['role']}
        )
    print("✅ Classroom-teacher created successfully.")

    # Create enrollments
    for enrollment_data in data['enrollments']:
        classroom = Classroom.objects.get(title=enrollment_data['classroom'])
        student = User.objects.get(uuid=enrollment_data['student'])
        Enrollment.objects.get_or_create(
            classroom=classroom,
            student=student,
            defaults={'status': enrollment_data['status']}
        )
    print("✅ Enrollment created successfully.")

    print("🎉 Data loaded successfully")
