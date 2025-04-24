from project.settings_modules.base import *

DEBUG = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


