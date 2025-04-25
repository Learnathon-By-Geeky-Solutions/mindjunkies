from project.settings.base import *
from decouple import config, Csv

DEBUG = False

# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

# CSRF_TRUSTED_ORIGINS = config("TRUSTED_DOMAINS", cast=Csv())

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT"),
    }
}

if not config("DB_IGNORE_SSL", default=False, cast=bool):
    DATABASES["default"]["OPTIONS"] = {
        "sslmode": "require",
    }

