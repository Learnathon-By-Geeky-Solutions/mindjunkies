from django.apps import AppConfig


class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mindjunkies.courses'


    def ready(self):
        import mindjunkies.courses.signals
