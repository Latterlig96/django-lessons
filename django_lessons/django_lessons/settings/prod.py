from .base import *

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DEBUG = False

ALLOWED_HOSTS = os.environ["DJANGO_ALLOWED_HOSTS"].split(" ")

INSTALLED_APPS += ["storages", "django_lessons.settings.storage"]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

CSRF_TRUSTED_ORIGINS = os.environ["CSRF_TRUSTED_ORIGINS"].split(" ")

EMAIL_HOST = os.environ["DJANGO_MAIL_HOST"]
EMAIL_PORT = os.environ["DJANGO_MAIL_PORT"]

EMAIL_HOST_USER = os.environ["DJANGO_EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["DJANGO_EMAIL_HOST_PASSWORD"]
EMAIL_USE_TLS = os.environ["DJANGO_EMAIL_USE_TLS"]

STRIPE_PUBLISHABLE_KEY = os.environ["STRIPE_PUBLISHABLE_KEY"]
STRIPE_SECRET_KEY = os.environ["STRIPE_SECRET_KEY"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ["DJANGO_DB_NAME"],
        'USER': os.environ["DJANGO_DB_USER"],
        'PASSWORD': os.environ["DJANGO_DB_PASSWORD"],
        'HOST': os.environ["DJANGO_DB_HOST"],
        'PORT': os.environ["DJANGO_DB_PORT"],
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [(os.environ["DJANGO_REDIS_HOST"], int(os.environ["DJANGO_REDIS_PORT"]))]},
    }
}

AWS_S3_ACCESS_KEY_ID = os.environ["MINIO_ROOT_USER"]
AWS_S3_SECRET_ACCESS_KEY = os.environ["MINIO_ROOT_PASSWORD"]
AWS_S3_ENDPOINT_URL = os.environ["MINIO_ENDPOINT_URL"]
AWS_QUERYSTRING_AUTH = False
AWS_S3_LOCAL_ENDPOINT_URL = os.environ["MINIO_LOCAL_ENDPOINT_URL"]
AWS_S3_STATIC_BUCKET_NAME = os.environ["MINIO_STATIC_BUCKET_NAME"]
AWS_S3_MEDIA_BUCKET_NAME = os.environ["MINIO_MEDIA_BUCKET_NAME"]

DEFAULT_FILE_STORAGE = "django_lessons.settings.storage.backend.MediaStorage"
STATICFILES_STORAGE = "django_lessons.settings.storage.backend.StaticStorage"
