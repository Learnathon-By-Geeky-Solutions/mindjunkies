from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from mindjunkies.courses.models import Course, Enrollment, Module

class Command(BaseCommand):
    help = 'Creates the Teacher group with required permissions'

    def handle(self, *args, **kwargs):
        teacher_group, created = Group.objects.get_or_create(name='Teacher')

        permissions = [
            ('add_course', Course),
            ('change_course', Course),
            ('delete_course', Course),
            ('view_course', Course),

            ('change_enrollment', Enrollment),
            ('delete_enrollment', Enrollment),
            ('view_enrollment', Enrollment),

            ('add_module', Module),
            ('change_module', Module),
        ]

        for codename, model in permissions:
            content_type = ContentType.objects.get_for_model(model)
            try:
                permission = Permission.objects.get(codename=codename, content_type=content_type)
                teacher_group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"❌ Permission {codename} not found for model {model.__name__}"))
                continue

        self.stdout.write(self.style.SUCCESS("✅ Teacher group and permissions set up successfully."))
