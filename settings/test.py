from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-hsll031%n5qn^6uv*v-is&0&^y=-5ag1jgj1vynb-5v*5r=nd3"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += ["coverage"]  # noqa

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}


try:
    from .local import *  # noqa
except ImportError:
    pass
