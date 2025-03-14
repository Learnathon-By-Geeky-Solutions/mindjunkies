# signals.py
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Enrollment


@receiver(post_save, sender=Enrollment)
def increment_course_enrollments(sender, instance, created, **kwargs):
    if created:
        instance.course.number_of_enrollments += 1
        instance.course.save()


@receiver(post_delete, sender=Enrollment)
def decrement_course_enrollments(sender, instance, **kwargs):
    if instance.course.number_of_enrollments > 0:
        instance.course.number_of_enrollments -= 1
        instance.course.save()
