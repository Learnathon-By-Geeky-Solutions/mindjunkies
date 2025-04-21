from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from decimal import Decimal

from mindjunkies.accounts.models import User, Profile
from mindjunkies.courses.models import Course, CourseCategory, CourseInfo

fake = Faker()

class Command(BaseCommand):
    help = "Creates 5 users (including admin) and 12 sample courses."

    def handle(self, *args, **kwargs):
        # Ensure course categories exist
        category_names = ["Development", "Design", "Marketing", "Business"]
        categories = []
        for name in category_names:
            cat, _ = CourseCategory.objects.get_or_create(name=name)
            categories.append(cat)

        # Create admin user
        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@mindjunkies.com",
                "first_name": "Admin",
                "last_name": "User",
                "is_staff": True,
                "is_superuser": True,
                "is_teacher": True,
            }
        )
        if created:
            admin.set_password("admin123")
            admin.save()
            self.stdout.write(self.style.SUCCESS("Admin user created."))
        else:
            self.stdout.write("Admin user already exists.")

        Profile.objects.get_or_create(user=admin, defaults={"bio": "Platform admin"})

        # Create 4 additional instructor users
        instructors = [admin]
        for i in range(4):
            username = f"instructor{i+1}"
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"{username}@mindjunkies.com",
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "is_teacher": True,
                    "is_staff": False,
                },
            )
            if created:
                user.set_password("test12345")
                user.save()
                self.stdout.write(self.style.SUCCESS(f"{username} created."))
            Profile.objects.get_or_create(user=user, defaults={"bio": fake.sentence()})
            instructors.append(user)

        # Create 12 courses (3 per instructor)
        course_count = 0
        for instructor in instructors:
            for _ in range(3):
                title = f"{fake.word().capitalize()} Course {course_count + 1}"
                category = categories[course_count % len(categories)]

                course = Course.objects.create(
                    title=title,
                    slug=slugify(title),
                    short_introduction=fake.sentence(),
                    course_description=fake.text(),
                    level="beginner",
                    category=category,
                    teacher=instructor,
                    status="published",
                    paid_course=True,
                    course_price=Decimal("49.99"),
                )
                CourseInfo.objects.create(
                    course=course,
                    what_you_will_learn=fake.text(),
                    who_this_course_is_for=fake.text(),
                    requirements=fake.text(),
                )
                course_count += 1

        self.stdout.write(self.style.SUCCESS("Created 5 users and 12 courses successfully."))
