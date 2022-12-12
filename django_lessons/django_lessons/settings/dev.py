from .base import *
from django.utils.crypto import get_random_string
import socket

SECRET_KEY = get_random_string(length=100)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = ["livereload", *INSTALLED_APPS, "debug_toolbar"]

INTERNAL_IPS = ['127.0.0.1', 'localhost']
ip = socket.gethostbyname(socket.gethostname())
INTERNAL_IPS += [ip[:-1] + '1']

MIDDLEWARE += ["livereload.middleware.LiveReloadScript", "debug_toolbar.middleware.DebugToolbarMiddleware"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

STRIPE_PUBLISHABLE_KEY = ""
STRIPE_SECRET_KEY = ""

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db/db.sqlite3",
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

STATIC_URL = "/static/"

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
