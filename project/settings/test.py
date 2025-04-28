from project.settings.base import *  # noqa

ELASTICSEARCH_DSL = {"default": {"hosts": "http://localhost:9200"}}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

MIDDLEWARE = [
    "silk.middleware.SilkyMiddleware",
    "allauth.account.middleware.AccountMiddleware",  # allauth
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # custom middleware here
    "django_htmx.middleware.HtmxMiddleware",
]

