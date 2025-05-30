# Generated by Django 5.1.7 on 2025-03-26 08:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("courses", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="LiveClass",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("topic", models.CharField(max_length=255)),
                (
                    "meeting_id",
                    models.CharField(blank=True, max_length=50, unique=True),
                ),
                ("scheduled_at", models.DateTimeField()),
                ("duration", models.IntegerField(default=60)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Upcoming", "Upcoming"),
                            ("Ongoing", "Ongoing"),
                            ("Completed", "Completed"),
                        ],
                        default="Upcoming",
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="live_classes",
                        to="courses.course",
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="live_classes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
