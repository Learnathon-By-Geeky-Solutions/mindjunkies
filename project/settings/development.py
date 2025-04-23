from project.settings.base import *

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

INSTALLED_APPS += [
    "django_browser_reload",
    "django_extensions",
    "silk",
    "django_tailwind_cli",
]

MIDDLEWARE = (
    ["silk.middleware.SilkyMiddleware"] + MIDDLEWARE +
    ["django_browser_reload.middleware.BrowserReloadMiddleware"]
)
