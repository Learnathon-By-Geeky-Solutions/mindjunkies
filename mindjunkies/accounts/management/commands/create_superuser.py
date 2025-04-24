from django.core.management.base import BaseCommand
from decouple import config

from mindjunkies.accounts.models import User


class Command(BaseCommand):
    help = 'Create initial superuser if not exists'

    def handle(self, *args, **options):
        try:
            username = config("DJANGO_SUPERUSER_USERNAME")
            email = config("DJANGO_SUPERUSER_EMAIL")
            password = config("DJANGO_SUPERUSER_PASSWORD")
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f"Missing environment variable: {e}"))
            return

        if not username or not email or not password:
            self.stdout.write(self.style.ERROR("Superuser credentials are not fully defined in env variables."))
            return

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS('Superuser created'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))
