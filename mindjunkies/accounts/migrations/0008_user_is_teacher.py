# Generated by Django 5.1.7 on 2025-03-24 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_remove_user_is_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_teacher',
            field=models.BooleanField(default=False),
        ),
    ]
