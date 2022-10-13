import os

from django.urls import reverse_lazy

import dj_database_url

from decouple import Csv, config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_DIR = os.path.join(BASE_DIR, "neusler")

SECRET_KEY = config(
    "NEUSLER_SECRET_KEY",
    default="EAAAGBANMIIxbeDZMweWJ4U1Gxv/rxhI82p2j0TK6pmWsI8npGuxItOTB+CAxVHZSLZDR4gJhv+vMKKOdKuUL6xSNnaN+n4tU0LRQqarN2lbs7ob7NRwX/SFKj9z6Sh5LPTk2fDXIJF4pbR02Oees9sETWhBdt5WOkW1Xm90B2PdyIaOiXnb+LqLgI2aa3j4VoPrcUHSwCdBQC3QZp$settings.dev",
)
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("NEUSLER_ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=Csv())

# Application definition

INSTALLED_APPS = [
    "neusler.accounts",
    "neusler.admin",
    "neusler.cms",
    "neusler.ads",
    "neusler.search",
    "neusler.front",
    "neusler.ops",
    "neusler.theme_a",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_extensions",
    "django_countries",
    "modelcluster",
    "taggit",
    "rest_framework",
    "rest_framework.authtoken",
    "wagtail.contrib.settings",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.routable_page",
    "wagtail.contrib.search_promotions",
    "wagtail.contrib.frontend_cache",
    "wagtail.api.v2",
    "wagtailseo",
    "wagtail_localize",
    "wagtail_localize.locales",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",
    "crispy_forms",
    "widget_tweaks",
    "django_comments_xtd",
    "django_comments",
    "celery",
    "django_celery_results",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "neusler.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
                "neusler.context_processors.default",
                "neusler.cms.context_processors.sidebar",
                "neusler.cms.context_processors.footer",
            ],
        },
    },
]

WSGI_APPLICATION = "neusler.wsgi.application"

NEUSLER_ENVIRONMENT = config("NEUSLER_ENVIRONMENT", default="development")

DATABASE_URL = config("NEUSLER_DATABASE_URL")

DATABASES = {
    "default": dj_database_url.config(
        default=DATABASE_URL,
        engine="django.db.backends.postgresql_psycopg2",
        conn_max_age=600,
    )
}

# sqlite3 database configuration
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "neuaccounts.User"

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

DEFAULT_RENDERER_CLASSES = ("rest_framework.renderers.JSONRenderer",)
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if DEBUG:
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + (
        "rest_framework.renderers.BrowsableAPIRenderer",
    )


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (),
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
}

LOGIN_URL = reverse_lazy("account_login")
LOGIN_REDIRECT_URL = reverse_lazy("account_profile")

SOCIALACCOUNT_PROVIDERS = {"google": {"APP": {"client_id": "abc", "secret": "abc", "key": "abc"}}}

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(PROJECT_DIR, "static"),
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/3.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

CRISPY_TEMPLATE_PACK = "bootstrap3"

# Wagtail settings

WAGTAIL_SITE_NAME = "Neusler"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = "https://demo.neusler.com"

WAGTAILADMIN_BASE_URL = "https://demo.neusler.com"

WAGTAIL_USER_EDIT_FORM = "neusler.accounts.forms.CustomUserEditForm"
WAGTAIL_USER_CREATION_FORM = "neusler.accounts.forms.CustomUserCreationForm"
WAGTAIL_USER_CUSTOM_FIELDS = ["display_name", "date_of_birth", "city", "country", "avatar"]

WAGTAIL_I18N_ENABLED = True
WAGTAIL_ENABLE_UPDATE_CHECK = False
WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ("en", "English"),
    ("fr", "French"),
]
WAGTAILEMBEDS_RESPONSIVE_HTML = True

TAGGIT_CASE_INSENSITIVE = True

SITE_ID = 1

COMMENTS_APP = "django_comments_xtd"

COMMENTS_XTD_SALT = b"Timendi causa est nescire. " b"Aequam memento rebus in arduis servare mentem."
COMMENTS_XTD_FROM_EMAIL = "noreply@example.com"
COMMENTS_XTD_CONTACT_EMAIL = "helpdesk@example.com"

COMMENTS_XTD_MODEL = "neusler.cms.models.CustomComment"

COMMENTS_XTD_MAX_THREAD_LEVEL = 1  # default is 0
COMMENTS_XTD_LIST_ORDER = ("-thread_id", "order")  # default is ('thread_id', 'order')
COMMENTS_XTD_APP_MODEL_OPTIONS = {
    "cms.articlepage": {
        "allow_flagging": False,
        "allow_feedback": True,
        "show_feedback": True,
        "who_can_post": "all",
    }
}

CMS_NAME = "Neusler"

# Search Backend config ----
NEUSLER_ENABLE_ELASTICSEARCH = config("NEUSLER_ENABLE_ELASTICSEARCH", default=False, cast=bool)

if NEUSLER_ENABLE_ELASTICSEARCH:
    WAGTAILSEARCH_BACKENDS = {
        "default": {
            "BACKEND": "wagtail.search.backends.elasticsearch7",
            "URLS": [config("NEUSLER_ELASTIC_SEARCH")],
            "INDEX": "wagtail",
            "TIMEOUT": 5,
            "OPTIONS": {},
            "INDEX_SETTINGS": {},
        }
    }
else:
    WAGTAILSEARCH_BACKENDS = {
        "default": {
            "BACKEND": "wagtail.search.backends.database",
        }
    }
# ----

PROTECTED_MEDIA_UPLOAD_WHITELIST = []
PROTECTED_MEDIA_UPLOAD_BLACKLIST = [
    ".app",
    ".bat",
    ".exe",
    ".jar",
    ".php",
    ".pl",
    ".ps1",
    ".py",
    ".rb",
    ".sh",
]

# To learn more, visit the docs here:
# https://cloud.google.com/docs/authentication/getting-started>

FCM_DJANGO_SETTINGS = {
    # default: _('FCM Django')
    "APP_VERBOSE_NAME": "neusler",
    # true if you want to have only one active device per registered user at a time
    # default: False
    "ONE_DEVICE_PER_USER": False,
    # devices to which notifications cannot be sent,
    # are deleted upon receiving error response from FCM
    # default: False
    "DELETE_INACTIVE_DEVICES": False,
    # Transform create of an existing Device (based on registration id) into
    # an update. See the section
    # "Update of device with duplicate registration ID" for more details.
    "UPDATE_ON_DUPLICATE_REG_ID": False,
}

CELERY_BROKER_URL = config("NEUSLER_REDIS_URL")
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"
