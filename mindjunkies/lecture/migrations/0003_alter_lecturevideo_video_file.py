# Generated by Django 5.1.7 on 2025-04-13 11:32

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lecture', '0002_lecturecompletion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturevideo',
            name='video_file',
            field=cloudinary.models.CloudinaryField(max_length=255),
        ),
    ]
