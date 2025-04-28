from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_remove_course_preview_video_remove_module_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
