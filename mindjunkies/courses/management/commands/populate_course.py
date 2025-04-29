import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course, CourseCategory, CourseInfo, Module, Enrollment, Rating, CourseToken, \
    LastVisitedCourse
from datetime import datetime, timedelta

fake = Faker()


class Command(BaseCommand):
    help = 'Populate the database with sample [Course, CourseCategory, CourseInfo, Module, Enrollment, Rating, CourseToken, LastVisitedCourse]'

    def handle(self, *args, **options):
        self.stdout.write("Starting course data population...")

        # Clear existing course-related data (optional)
        Course.objects.all().delete()
        CourseCategory.objects.all().delete()
        CourseInfo.objects.all().delete()
        Module.objects.all().delete()
        Enrollment.objects.all().delete()
        Rating.objects.all().delete()
        CourseToken.objects.all().delete()
        LastVisitedCourse.objects.all().delete()

        # Create course categories
        categories = [
            {"name": "Programming", "description": "Learn coding and software development."},
            {"name": "Data Science", "description": "Master data analysis and machine learning."},
            {"name": "Design", "description": "Explore graphic and UI/UX design."},
            {"name": "Business", "description": "Develop business and entrepreneurship skills."},
            {"name": "Language", "description": "Learn new languages and communication skills."}
        ]
        for cat in categories:
            category, created = CourseCategory.objects.get_or_create(
                name=cat["name"],
                defaults={"description": cat["description"]}
            )
            self.stdout.write(f"{'Created' if created else 'Updated'} category: {category.name}")

        # Get teachers and students from existing users
        teachers = User.objects.filter(is_teacher=True)
        students = User.objects.filter(is_teacher=False)

        if not teachers.exists():
            self.stdout.write(self.style.ERROR("No teachers found. Please populate users first."))
            return
        if not students.exists():
            self.stdout.write(self.style.WARNING("No students found. Enrollments and ratings will not be created."))

        # Create courses
        for _ in range(10):
            teacher = random.choice(teachers)
            category = random.choice(categories)
            title = fake.catch_phrase()
            is_paid_course = random.choice([True, False])  # Determine paid_course first
            course = Course.objects.create(
                slug=slugify(title),
                title=title,
                short_introduction=fake.paragraph(nb_sentences=2),
                course_description=fake.paragraph(nb_sentences=5),
                level=random.choice(["beginner", "intermediate", "advanced"]),
                category=CourseCategory.objects.get(name=category["name"]),
                teacher=teacher,
                course_image=None,  # Cloudinary requires API setup
                status=random.choice(["draft", "published", "archived"]),
                published_on=datetime.now() - timedelta(days=random.randint(0, 365)) if random.choice(
                    [True, False]) else None,
                paid_course=is_paid_course,
                course_price=random.uniform(10.0, 100.0) if is_paid_course else 0.0,
                upcoming=random.choice([True, False]),
                total_rating=0.0,
                number_of_ratings=0
            )

            # Create course info
            CourseInfo.objects.create(
                course=course,
                what_you_will_learn=fake.paragraph(nb_sentences=4),
                who_this_course_is_for=fake.paragraph(nb_sentences=3),
                requirements=fake.paragraph(nb_sentences=2)
            )

            # Create modules
            for i in range(random.randint(3, 7)):
                Module.objects.create(
                    course=course,
                    title=f"Module {i + 1}: {fake.sentence(nb_words=4)}",
                    order=i
                )

            # Create enrollments and ratings
            if students.exists():
                num_enrollments = random.randint(1, min(8, students.count()))
                enrolled_students = random.sample(list(students), num_enrollments)
                for student in enrolled_students:
                    enrollment = Enrollment.objects.create(
                        course=course,
                        student=student,
                        status=random.choice(["active", "pending", "completed"]),
                        progression=random.randint(0, 100)
                    )

                    # Create rating (50% chance)
                    if random.choice([True, False]):
                        rating = Rating.objects.create(
                            course=course,
                            student=student,
                            rating=random.randint(1, 5),
                            review=fake.paragraph(nb_sentences=2) if random.choice([True, False]) else None
                        )

            # Create course token
            CourseToken.objects.create(
                course=course,
                teacher=teacher,
                status=random.choice(["pending", "approved"])
            )

            # Create last visited course (for some students and teachers)
            for user in random.sample(list(User.objects.all()), random.randint(1, min(5, User.objects.count()))):
                LastVisitedCourse.objects.create(
                    user=user,
                    course=course
                )

            self.stdout.write(
                f"Created course: {course.title} with {num_enrollments if students.exists() else 0} enrollments")

        self.stdout.write(self.style.SUCCESS("Course data population completed successfully!"))
