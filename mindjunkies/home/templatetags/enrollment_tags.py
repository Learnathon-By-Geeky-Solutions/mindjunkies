from django import template
from mindjunkies.courses.models import Enrollment

register = template.Library()

@register.filter
def get_enrollment(course, user):
    try:
        return Enrollment.objects.get(course=course, student=user)
    except Enrollment.DoesNotExist:
        return None