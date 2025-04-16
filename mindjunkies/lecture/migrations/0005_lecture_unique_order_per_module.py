# Generated by Django 5.1.7 on 2025-04-16 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_module_unique_order_per_course'),
        ('lecture', '0004_lastvisitedmodule'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='lecture',
            constraint=models.UniqueConstraint(fields=('module', 'order'), name='unique_order_per_module'),
        ),
    ]
