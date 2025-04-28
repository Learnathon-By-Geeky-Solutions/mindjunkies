import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from mindjunkies.courses.models import CourseCategory

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with sample CourseCategory data with related categories'

    def handle(self, *args, **options):
        self.stdout.write("Starting course category data population...")

        # Clear existing course category data
        CourseCategory.objects.all().delete()

        # Create course categories with related groupings
        categories = [
            {"name": "Data Science", "description": "Master data analysis, visualization, and statistical modeling."},
            {"name": "Machine Learning", "description": "Dive into algorithms and predictive modeling for data science."},
            {"name": "Programming", "description": "Learn coding and software development fundamentals."},
            {"name": "Web Development", "description": "Build dynamic websites and applications using programming."},
            {"name": "Design", "description": "Explore graphic design and visual communication."},
            {"name": "UI/UX Design", "description": "Create user-friendly interfaces and experiences for design."},
            {"name": "Business", "description": "Develop skills in entrepreneurship and management."},
            {"name": "Marketing", "description": "Learn digital marketing and branding strategies for business."},
            {"name": "Artificial Intelligence", "description": "Study intelligent systems and automation."},
            {"name": "Deep Learning", "description": "Explore neural networks and advanced AI techniques."},
            {"name": "Cybersecurity", "description": "Protect systems and networks from digital threats."},
            {"name": "Ethical Hacking", "description": "Learn penetration testing and security auditing for cybersecurity."},
            {"name": "Finance", "description": "Understand investments and financial planning."},
            {"name": "Cryptocurrency", "description": "Explore blockchain and digital currencies in finance."},
            {"name": "Photography", "description": "Master the art of capturing and editing images."},
            {"name": "Video Editing", "description": "Learn post-production techniques for photography and film."},
            {"name": "Language", "description": "Learn new languages and communication skills."},
            {"name": "Translation Studies", "description": "Develop skills in linguistic translation and interpretation."},
            {"name": "Health & Fitness", "description": "Explore wellness, nutrition, and exercise."},
            {"name": "Yoga & Meditation", "description": "Practice mindfulness and physical wellness techniques."}
        ]
        for cat in categories:
            category, created = CourseCategory.objects.get_or_create(
                name=cat["name"],
                defaults={"description": cat["description"]}
            )
            self.stdout.write(f"{'Created' if created else 'Updated'} category: {category.name}")

        self.stdout.write(self.style.SUCCESS("Course category data population completed successfully!"))