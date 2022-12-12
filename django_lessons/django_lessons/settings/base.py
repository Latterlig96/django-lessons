import os
from pathlib import Path

from django.contrib.messages import constants

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Auth user

AUTH_USER_MODEL = "accounts.CustomUser"

LOGIN_REDIRECT_URL = "app:index"
LOGOUT_REDIRECT_URL = "app:index"

# Authentication backends

AUTHENTICATION_BACKENDS = (
    "accounts.backends.UsernameBackend",
    "accounts.backends.EmailBackend",
)

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts.apps.AccountsConfig",
    "app.apps.AppConfig",
    "order.apps.OrderConfig",
    "chat.apps.ChatConfig",
    "stripe",
    "channels",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "django_lessons.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ASGI_APPLICATION = "django_lessons.asgi.application"
WSGI_APPLICATION = "django_lessons.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

LANGUAGES = (("en", "English"), ("pl", "Polski"))

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


MESSAGE_TAGS = {
    constants.DEBUG: "alert-info",
    constants.INFO: "alert-info",
    constants.SUCCESS: "alert-success",
    constants.WARNING: "alert-warning",
    constants.ERROR: "alert-danger",
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
