from project.settings.base import *
from decouple import config, Csv

DEBUG = True

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

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{config('REDIS_HOST')}:{config('REDIS_PORT', 6379)}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': config('ELASTICSEARCH_HOST', default='localhost:9200'),
    },
}

RESEND_API_KEY = config("RESEND_API_KEY")
EMAIL_BACKEND = 'utils.email_backends.ResendEmailBackend'
DEFAULT_FROM_EMAIL = config("RESEND_FROM_EMAIL")

ACCOUNT_EMAIL_VERIFICATION = "mandatory"
