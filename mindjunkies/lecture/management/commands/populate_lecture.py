import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course, Module
from mindjunkies.lecture.models import Lecture, LectureCompletion, LastVisitedModule
from datetime import datetime, timedelta

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with sample [Lecture, LectureCompletion, LastVisitedModule]'

    def handle(self, *args, **options):
        self.stdout.write("Starting lecture data population...")

        # Clear existing lecture-related data (optional)
        Lecture.objects.all().delete()
        LectureCompletion.objects.all().delete()
        LastVisitedModule.objects.all().delete()

        # Get existing courses, modules, and users
        courses = Course.objects.all()
        modules = Module.objects.all()
        students = User.objects.filter(is_teacher=False)

        if not courses.exists() or not modules.exists():
            self.stdout.write(self.style.ERROR("No courses or modules found. Please populate courses first."))
            return
        if not students.exists():
            self.stdout.write(self.style.WARNING("No students found. Lecture completions and last visited modules will not be created."))

        # Create lectures for each module
        for module in modules:
            num_lectures = random.randint(3, 6)  # 3–6 lectures per module
            for i in range(num_lectures):
                title = fake.sentence(nb_words=5)
                base_slug = slugify(title)
                slug = base_slug
                counter = 1
                # Ensure unique slug
                while Lecture.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                lecture = Lecture.objects.create(
                    course=module.course,
                    module=module,
                    title=title,
                    description=fake.paragraph(nb_sentences=3),
                    learning_objective=fake.paragraph(nb_sentences=2),
                    order=i,
                    slug=slug
                )
                self.stdout.write(f"Created lecture: {lecture.title} for module {module.title}")

                # Create lecture completions (for some students)
                if students.exists():
                    num_completions = random.randint(0, min(3, students.count()))  # 0–3 completions per lecture
                    completion_students = random.sample(list(students), num_completions)
                    for student in completion_students:
                        LectureCompletion.objects.get_or_create(
                            user=student,
                            lecture=lecture,
                            defaults={
                                'completed_at': datetime.now() - timedelta(days=random.randint(0, 30))
                            }
                        )
                        self.stdout.write(f"Created completion for {student.username} on {lecture.title}")

                # Create last visited module entries (for some students)
                if students.exists():
                    num_visits = random.randint(0, min(3, students.count()))  # 0–3 visits per lecture
                    visit_users = random.sample(list(students), num_visits)
                    for user in visit_users:
                        LastVisitedModule.objects.get_or_create(
                            user=user,
                            module=module,
                            lecture=lecture,
                            defaults={
                                'last_visited': datetime.now() - timedelta(days=random.randint(0, 30))
                            }
                        )
                        self.stdout.write(f"Created last visited entry for {user.username} on {lecture.title}")

        self.stdout.write(self.style.SUCCESS("Lecture data population completed successfully!"))