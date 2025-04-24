from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from mindjunkies.courses.models import Enrollment
from .models import LectureCompletion, Lecture


def update_progression(lecture, user):
    """Helper function to update progression for a user in a course."""
    course = lecture.course
    total_lectures = course.lectures.count()

    try:
        enrollment = Enrollment.objects.get(course=course, student=user)

        completed_lectures = (
            course.lectures.filter(lecturecompletion__user=user).distinct().count()
        )

        if total_lectures > 0:
            percentage = round((completed_lectures / total_lectures) * 100)
            enrollment.progression = percentage
            enrollment.save()
    except Enrollment.DoesNotExist:
        # Handle case where enrollment doesn't exist
        pass


@receiver(post_save, sender=LectureCompletion)
def update_module_progression_on_save(sender, instance, created, **kwargs):
    if created:
        update_progression(instance.lecture, instance.user)


@receiver(post_delete, sender=LectureCompletion)
def update_module_progression_on_delete(sender, instance, **kwargs):
    """Update progression when a lecture completion is deleted."""
    update_progression(instance.lecture, instance.user)


@receiver(post_delete, sender=Lecture)
def update_all_progressions_on_lecture_delete(sender, instance, **kwargs):
    """Update progression for all users when a lecture is deleted."""
    course = instance.course
    # Get all users enrolled in this course
    enrollments = Enrollment.objects.filter(course=course)
    
    for enrollment in enrollments:
        user = enrollment.student
        # We can't use the deleted lecture, but we can use any lecture from the course
        # Just to get a reference to the course
        remaining_lecture = course.lectures.first()
        if remaining_lecture:
            update_progression(remaining_lecture, user)
        else:
            # No lectures left, set progression to 0 or 100 based on your business logic
            enrollment.progression = 0
            enrollment.save()