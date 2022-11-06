from decouple import config

from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-hsll031%n5qn^6uv*v-is&0&^y=-5ag1jgj1vynb-5v*5r=nd3"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += ["coverage"]  # noqa

# Email configuration
NEUSLER_ENABLE_SMTP = config("NEUSLER_ENABLE_SMTP", default=False, cast=bool)

if NEUSLER_ENABLE_SMTP:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_FROM_EMAIL = "Neusler Test <donotreply@example.com>"

WAGTAILADMIN_BASE_URL = "http://localhost:8000"
BASE_URL = "https://abcd.ngrok.io/"  # FIXME


try:
    from .local import *  # noqa
except ImportError:
    pass
