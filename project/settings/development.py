from project.settings.base import * # noqa

DEBUG = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
]

INSTALLED_APPS += [
    "django_browser_reload",
]

MIDDLEWARE += [
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


ELASTICSEARCH_DSL = {"default": {"hosts": "http://localhost:9200"}}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",         # <host>:<port>/<db>
        "OPTIONS": {
            "PASSWORD": config('REDIS_PASSWORD'),               # match your requirepass
            # optionally: "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Email server configuration
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")


ACCOUNT_EMAIL_VERIFICATION = "mandatory"
