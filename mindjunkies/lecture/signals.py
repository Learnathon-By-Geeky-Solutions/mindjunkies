from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LectureCompletion
from mindjunkies.courses.models import Module, Enrollment
from mindjunkies.lecture.models import Lecture


@receiver(post_save, sender=LectureCompletion)
def update_module_progression(sender, instance, created, **kwargs):
    if created:
        lecture = instance.lecture
        user = instance.user

        course = lecture.course
        total_lectures = course.lectures.count()

        enrollment = Enrollment.objects.get(course=course, student=user)

        completed_lectures = course.lectures.filter(
            lecturecompletion__user=user
        ).distinct().count()

        if total_lectures > 0:
            percentage = int((completed_lectures / total_lectures) * 100)
            enrollment.progression = percentage
            enrollment.save()
