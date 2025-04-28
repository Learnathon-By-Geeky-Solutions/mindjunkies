from project.settings.base import *  # noqa

ELASTICSEARCH_DSL = {"default": {"hosts": "http://localhost:9200"}}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

