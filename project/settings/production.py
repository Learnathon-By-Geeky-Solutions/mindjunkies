from project.settings.base import *
from decouple import config, Csv

DEBUG = False

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

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "bucket_name": "mindjunkies",
            "access_key": config("AWS_ACCESS_KEY_ID"),
            "secret_key": config("AWS_SECRET_ACCESS_KEY"),
            "region_name": "blr1",
            "endpoint_url": "https://blr1.digitaloceanspaces.com",
            "default_acl": "public-read",
            "file_overwrite": False,
            "location": "static",
        },
    },
}

if not config("DB_IGNORE_SSL", default=False, cast=bool):
    DATABASES["default"]["OPTIONS"] = {
        "sslmode": "require",
    }

