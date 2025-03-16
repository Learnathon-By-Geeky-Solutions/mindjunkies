from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mindjunkies.accounts"

    def ready(self):
        pass
