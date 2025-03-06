from pathlib import Path
from decouple import config
import dj_database_url

import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = [
    config('ALLOWED_HOSTS', default='localhost'),
]

INTERNAL_IPS = [
    "127.0.0.1",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites",
    # custom apps
    'home',
    'accounts',
    'courses',
    'theme',
    'lecture',
    'dashboard',
    'liveclasses',
    # third party apps
    'tailwind',
    'django_browser_reload',
    'crispy_forms',
    'crispy_tailwind',
    'django_extensions',
    # allauth
    "allauth",
    "allauth.account",
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]


MIDDLEWARE = [
    "allauth.account.middleware.AccountMiddleware",  # allauth
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "templates",
            BASE_DIR / "accounts/templates/accounts/",
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',  # allauth
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

db_url = config('DATABASE_URL', default=None)
DATABASES['default'] = dj_database_url.parse(db_url)

db_url = config('DATABASE_URL', default=None)
if db_url:
    DATABASES['default'] = dj_database_url.parse(db_url)


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",  # allauth
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "theme" / "static",  # Correct path to the static directory inside the theme app
]
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = "/"

AUTH_USER_MODEL = 'accounts.User'

# allauth settings
SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_LOGIN_METHODS = {'username', 'email'}
ACCOUNT_CHANGE_EMAIL = True
ACCOUNT_EMAIL_NOTIFICATIONS = True

ACCOUNT_RATE_LIMITS = {
    'login_failed': '5/5m',
}

ACCOUNT_FORMS = {
    'add_email': 'allauth.account.forms.AddEmailForm',
    'change_password': 'allauth.account.forms.ChangePasswordForm',
    'confirm_login_code': 'allauth.account.forms.ConfirmLoginCodeForm',
    'login': 'allauth.account.forms.LoginForm',
    'request_login_code': 'allauth.account.forms.RequestLoginCodeForm',
    'reset_password': 'allauth.account.forms.ResetPasswordForm',
    'reset_password_from_key': 'allauth.account.forms.ResetPasswordKeyForm',
    'set_password': 'allauth.account.forms.SetPasswordForm',
    'signup': 'allauth.account.forms.SignupForm',
    'user_token': 'allauth.account.forms.UserTokenForm',
}

SOCIALACCOUNT_PROVIDERS = {
  'google': {
      'APP': {
            'client_id': config('GOOGLE_CLIENT_ID'),
            'secret': config('GOOGLE_CLIENT_SECRET'),
            'key': config('GOOGLE_API_KEY'),
      },
      'EMAIL_AUTHENTICATION': True,
      'FETCH_USERINFO': True,
  }
}

# Tailwind settings
TAILWIND_APP_NAME = 'theme'
NPM_BIN_PATH = config('NPM_BIN_PATH')

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# Email server configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')


JITSI_APP_ID = "vpaas-magic-cookie-fb583aeece2040b4805f50d0b267e75b"
JITSI_SECRET = "vpaas-magic-cookie-fb583aeece2040b4805f50d0b267e75b/ee88ba"
