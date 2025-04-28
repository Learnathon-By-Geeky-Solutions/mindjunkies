# mindjunkies/accounts/management/commands/populate_db.py
import random
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.hashers import make_password
from mindjunkies.accounts.models import User, Profile
from mindjunkies.courses.models import Course, Enrollment, Rating

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with sample users, profiles, courses, and enrollments'

    def handle(self, *args, **options):
        self.stdout.write("Starting database population...")

        # Clear existing data (optional)
        User.objects.all().delete()
        Profile.objects.all().delete()
        Course.objects.all().delete()
        Enrollment.objects.all().delete()
        Rating.objects.all().delete()

        # Create users and profiles
        for _ in range(20):
            is_teacher = random.choice([True, False])
            username = fake.user_name()
            user = User.objects.create(
                username=username,
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password=make_password('password123'),
                is_teacher=is_teacher
            )
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    'birthday': fake.date_of_birth(minimum_age=18, maximum_age=80),
                    'bio': fake.paragraph(nb_sentences=3),
                    'phone_number': fake.phone_number()[:15],
                    'address': fake.address(),
                    'avatar': None
                }
            )
            self.stdout.write(f"Created user: {username} ({'Teacher' if is_teacher else 'Student'}) - Profile {'created' if created else 'already existed'}")

        # Create courses and enrollments
        teachers = User.objects.filter(is_teacher=True)
        students = User.objects.filter(is_teacher=False)
        for _ in range(10):
            teacher = random.choice(teachers)
            course = Course.objects.create(
                teacher=teacher,
                title=fake.catch_phrase(),
                description=fake.paragraph(nb_sentences=5),
                price=random.uniform(10.0, 100.0)
            )
            num_enrollments = random.randint(1, min(8, students.count()))
            enrolled_students = random.sample(list(students), num_enrollments)
            for student in enrolled_students:
                Enrollment.objects.create(student=student, course=course, status="active")
                if random.choice([True, False]):
                    Rating.objects.create(
                        course=course,
                        student=student,
                        rating=random.randint(1, 5),
                        comment=fake.sentence()
                    )
            self.stdout.write(f"Created course: {course.title} with {num_enrollments} enrollments")

        self.stdout.write(self.style.SUCCESS("Database population completed successfully!"))