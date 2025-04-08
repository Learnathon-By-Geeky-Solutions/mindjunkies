# Generated by Django 5.1.7 on 2025-04-08 12:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forumtopic',
            name='reactions',
        ),
        migrations.AddField(
            model_name='forumcomment',
            name='likes',
            field=models.ManyToManyField(related_name='likedComments', through='forums.LikedComment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='forumtopic',
            name='likes',
            field=models.ManyToManyField(related_name='likedTopics', through='forums.LikedPost', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='forumcomment',
            name='content',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='forumtopic',
            name='content',
            field=models.CharField(max_length=150),
        ),
    ]
