from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from .models import LiveClass
from courses.models import Course

import uuid


@login_required
def list_live_classes(request, slug):
    """List all upcoming and ongoing live classes for a course."""

    course = get_object_or_404(Course, slug=slug)
    live_classes = LiveClass.objects.filter(course=course)

    teacher = course.teachers.filter(teacher=request.user).exists()
    print(teacher)

    return render(
        request,
        "liveclasses/list_live_classes.html",
        {
            "course": course,
            "live_classes": live_classes,
            "teacher": teacher,
        }
    )


@login_required
def create_live_class(request, slug):
    """Allows a teacher to create a live class."""
    course = get_object_or_404(Course, slug=slug)

    if request.method == "POST":
        topic = request.POST.get("topic")
        scheduled_at = request.POST.get("scheduled_at")
        duration = request.POST.get("duration")

        if LiveClass.objects.filter(teacher=request.user, scheduled_at=scheduled_at).exists():
            messages.error(request, "You already have a class scheduled at this time!")
            return redirect("create_live_class", slug=course.slug)

        LiveClass.objects.create(
            course=course,
            teacher=request.user,
            topic=topic,
            scheduled_at=scheduled_at,
            duration=duration
        )

        messages.success(request, "Live class created successfully!")
        return redirect("list_live_classes", slug=course.slug)

    return render(request, "liveclasses/create_live_class.html", {"course": course})


def join_live_class(request, meeting_id):
    """Render Jitsi meeting inside LMS with JWT authentication."""

    live_class = get_object_or_404(LiveClass, meeting_id=meeting_id)

    secure_meeting_url = live_class.get_meeting_url()

    return render(request, "live_classes/join_live_class.html",
                  {"live_class": live_class, "meeting_url": secure_meeting_url})
