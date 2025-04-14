# mindjunkies/lecture/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LectureCompletion
from mindjunkies.courses.models import Module
from mindjunkies.lecture.models import Lecture

@receiver(post_save, sender=LectureCompletion)
def update_module_progression(sender, instance, created, **kwargs):
    if created:
        lecture = instance.lecture
        user = instance.user

        # module = lecture.module
        # total_lectures = module.lectures.count()

        course = lecture.course
        total_lectures = course.lectures.count()

        print(total_lectures)
        # completed_lectures = module.lectures.filter(
        #     lecturecompletion__user=user
        # ).distinct().count()

        completed_lectures = course.lectures.filter(
            lecturecompletion__user=user
        ).distinct().count()

        if total_lectures > 0:
            percentage = int((completed_lectures / total_lectures) * 100)
            print("before")
            print(course.title, percentage, course.progression)
            course.progression = percentage
            print("after")
            print(course.title, percentage, course.progression)
            course.save()
