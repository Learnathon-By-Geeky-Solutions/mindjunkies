# Generated by Django 5.1.7 on 2025-04-16 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "courses",
            "0007_remove_course_progression_remove_module_progression_and_more",
        ),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="module",
            constraint=models.UniqueConstraint(
                fields=("course", "order"), name="unique_order_per_course"
            ),
        ),
    ]
