# Generated by Django 5.1.5 on 2025-03-08 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("lecture", "0004_lecturevideo_is_running"),
    ]

    operations = [
        migrations.RenameField(
            model_name="lecture",
            old_name="content",
            new_name="learning_objective",
        ),
        migrations.RemoveField(
            model_name="lecture",
            name="video_url",
        ),
    ]
