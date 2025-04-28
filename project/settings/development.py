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

