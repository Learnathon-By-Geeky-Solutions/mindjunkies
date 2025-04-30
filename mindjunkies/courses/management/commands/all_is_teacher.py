import random
from django.core.management.base import BaseCommand
from mindjunkies.accounts.models import User
from mindjunkies.dashboard.models import TeacherVerification  # Replace 'your_app' with your app name


class Command(BaseCommand):
    help = 'Create TeacherVerification entries for all users and set verified=True'

    def handle(self, *args, **options):
        users = User.objects.all()
        teacher_verifications = TeacherVerification.objects.all()

        teacher_verifications.delete()
        users = list(users)
        selected_users = random.sample(users, 5)  # pick 5 users randomly

        for user in selected_users:
            tv, created = TeacherVerification.objects.get_or_create(
                user=user,
                defaults={
                    'full_name': user.username,
                    'email': user.email,
                    'verified': True,
                }
            )
            if not created:
                tv.verified = True

            user.is_teacher = True
            user.save()
            tv.save()

        self.stdout.write(self.style.SUCCESS('Successfully created/updated TeacherVerification for all users.'))
