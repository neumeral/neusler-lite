import json
import logging.config

from decouple import config

from .base import *  # noqa

DEBUG = False

try:
    from .local import *  # noqa
except ImportError:
    pass

# ---- Frontend Cache with CloudFlare

NEUSLER_ENABLE_CLOUDFLARE = config("NEUSLER_ENABLE_CLOUDFLARE", default=False, cast=bool)

if NEUSLER_ENABLE_CLOUDFLARE:
    NEUSLER_CLOUDFLARE_BEARER_TOKEN = config("NEUSLER_CLOUDFLARE_BEARER_TOKEN")
    NEUSLER_CLOUDFLARE_ZONEID = config("NEUSLER_CLOUDFLARE_ZONEID")

    WAGTAILFRONTENDCACHE = {
        "cloudflare": {
            "BACKEND": "wagtail.contrib.frontend_cache.backends.CloudflareBackend",
            "BEARER_TOKEN": NEUSLER_CLOUDFLARE_BEARER_TOKEN,
            "ZONEID": NEUSLER_CLOUDFLARE_ZONEID,
        },
    }

# ---- Databases
# dj_database_url seems to have issues in connecting to a host other than localhost
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("NEUSLER_DB_NAME"),
        "USER": config("NEUSLER_DB_USER"),
        "PASSWORD": config("NEUSLER_DB_PASSWORD"),
        "HOST": config("NEUSLER_DB_HOST"),
        "PORT": config("NEUSLER_DB_PORT"),
        "OPTIONS": json.loads(config("NEUSLER_DATABASE_OPTIONS", default="{}")),
    }
}


# ---- Logging
LOGGING_CONFIG = None  # Reset current config

LOGLEVEL = config("NEUSLER_LOGLEVEL", default="info").upper()

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "format": "%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console",
            },
        },
        "loggers": {
            "": {
                "level": LOGLEVEL,
                "handlers": [
                    "console",
                ],
            },
        },
    }
)

# ---- Storages
NEUSLER_ENABLE_EXT_STORAGE = config("NEUSLER_ENABLE_EXT_STORAGE", default=False, cast=bool)

if NEUSLER_ENABLE_EXT_STORAGE:
    AWS_ACCESS_KEY_ID = config("NEUSLER_STATIC_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config("NEUSLER_STATIC_SECRET_KEY")
    AWS_STORAGE_BUCKET_NAME = config("NEUSLER_STATIC_BUCKET_NAME")
    AWS_DEFAULT_ACL = "public-read"
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
    }

    STATIC_LOCATION = "statics"
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"
    STATICFILES_STORAGE = "settings.storage_backends.StaticStorage"

    PUBLIC_MEDIA_LOCATION = "media"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"
    DEFAULT_FILE_STORAGE = "settings.storage_backends.PublicMediaStorage"
