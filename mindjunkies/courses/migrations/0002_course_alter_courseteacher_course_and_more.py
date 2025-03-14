# Generated by Django 5.1.6 on 2025-02-24 17:27

import uuid

import django.db.models.deletion
from django.db import migrations, models

COURSES_TABLE = "courses.course"


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("title", models.CharField(max_length=255)),
                ("short_introduction", models.CharField(max_length=500)),
                ("course_description", models.TextField()),
                ("requirements", models.TextField()),
                ("learnings", models.TextField()),
                (
                    "level",
                    models.CharField(
                        choices=[
                            ("beginner", "Beginner"),
                            ("intermediate", "Intermediate"),
                            ("advanced", "Advanced"),
                        ],
                        default="beginner",
                        max_length=15,
                    ),
                ),
                (
                    "course_image",
                    models.ImageField(
                        blank=True,
                        default="course_images/default.jpg",
                        null=True,
                        upload_to="course_images/",
                    ),
                ),
                ("preview_video_link", models.URLField(blank=True, null=True)),
                ("published", models.BooleanField(default=False)),
                ("upcoming", models.BooleanField(default=False)),
                ("published_on", models.DateTimeField(blank=True, null=True)),
                ("paid_course", models.BooleanField(default=False)),
                (
                    "course_price",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                ("slug", models.SlugField(max_length=255, unique=True)),
                (
                    "total_rating",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
                ),
                ("number_of_ratings", models.PositiveIntegerField(default=0)),
            ],
            options={
                "ordering": ["-created_at", "-updated_at"],
                "abstract": False,
            },
        ),
        migrations.AlterField(
            model_name="courseteacher",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="teachers",
                to=COURSES_TABLE,
            ),
        ),
        migrations.AlterField(
            model_name="enrollment",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="enrollments",
                to=COURSES_TABLE,
            ),
        ),
        migrations.CreateModel(
            name="Module",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("title", models.CharField(max_length=255)),
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="modules",
                        to=COURSES_TABLE,
                    ),
                ),
            ],
            options={
                "ordering": ["order"],
            },
        ),
        migrations.DeleteModel(
            name="Courses",
        ),
    ]
