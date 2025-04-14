from django.apps import AppConfig


class LectureConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mindjunkies.lecture"


    def ready(self):
        import mindjunkies.lecture.signals
