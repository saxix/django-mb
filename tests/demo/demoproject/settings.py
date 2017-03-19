from __future__ import absolute_import

import os

from django.utils.translation import ugettext_lazy as _

here = os.path.dirname(__file__)
# sys.path.append(os.path.abspath(os.path.join(here, os.pardir)))
# sys.path.append(os.path.abspath(os.path.join(here, os.pardir, "demo")))

DEBUG = True

DATABASES = {
    "default": {
        # "ENGINE": "django.db.backends.postgresql_psycopg2",
        "ENGINE": "django.db.backends.sqlite3",
        # "NAME": "::memory::",
        # "HOST": "127.0.0.1",
        # "PORT": "",
        # "USER": "postgres",
        # "PASSWORD": ""
    }}

TIME_ZONE = "Europe/Rome"
LANGUAGE_CODE = "en-us"

LANGUAGES = (
    ("de", _("German")),
    ("en", _("English")),
    ("fr", _("French")),
    ("es", _("Spanish")),
    ("pt", _("Portuguese"))
)
LOCALE_PATHS = (
    os.path.join(here, os.pardir, os.pardir, "src", "django_mb", "locale"),
)

SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = os.path.join(here, "media")
MEDIA_URL = ""
STATIC_ROOT = os.path.join(here, "static")
STATIC_URL = "/static/"
SECRET_KEY = "c73*n!y=)tziu^2)y*@5i2^)$8z$tx#b9*_r3i6o1ohxo%*2^a"
MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    # "django.contrib.auth.middleware.AuthenticationMiddleware",
    # "django.contrib.messages.middleware.MessageMiddleware",
)

ROOT_URLCONF = "demoproject.urls"

INSTALLED_APPS = [
    # "django.contrib.auth",
    # "django.contrib.contenttypes",
    # "django.contrib.sessions",
    # "django.contrib.messages",
    # "django.contrib.staticfiles",
    # "django.contrib.admin",
    "django_mb.apps.DjangoMqConfig",
    "demoproject"]

TEMPLATES = [
    {"BACKEND": "django.template.backends.django.DjangoTemplates",
     "DIRS": [
     ],
     "APP_DIRS": True,
     "OPTIONS": {
         "debug": DEBUG,
         "context_processors": [
             # "django.contrib.auth.context_processors.auth",
             # "django.template.context_processors.debug",
             # "django.template.context_processors.i18n",
             # "django.template.context_processors.media",
             # "django.template.context_processors.static",
             # "django.template.context_processors.tz",
             # "django.contrib.messages.context_processors.messages",
         ],
     },
     }
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        "LOCATION": "unique-snowflake"
    }
}

# ENABLE_SELENIUM = True
#
# DATE_FORMAT = "d-m-Y"
# TIME_FORMAT = "H:i"
# DATETIME_FORMAT = "d-m-Y H:i"
# YEAR_MONTH_FORMAT = "F Y"
# MONTH_DAY_FORMAT = "F j"
# SHORT_DATE_FORMAT = "m/d/Y"
# SHORT_DATETIME_FORMAT = "m/d/Y P"
# FIRST_DAY_OF_WEEK = 1
#

MB = {"SERVER": "localhost",
      "RETRIES": 10,
      "TIMEOUT": 10,
      "NOTIFY": [],
      "BROKER": "",
      "APPS": ["demoproject"]
      }

level = "DEBUG"
_LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "full": {
            "format": "%(levelname)-7s "
                      "%(name)-30s "
                      "%(funcName)-20s:%(lineno)3s "
                      "%(message)s"
        },
    },
    "handlers": {"null": {"class": "logging.NullHandler",
                          "formatter": "full"},
                 "console": {"class": "logging.StreamHandler",
                             "formatter": "full"}},
    "loggers": {
        "test": {
            "handlers": ["console"],
            "level": level,
            "propagate": False
        },
        "demoproject": {
            "handlers": ["console"],
            "level": level,
            "propagate": False
        },
        "django_mb": {
            "handlers": ["console"],
            "level": level,
            "propagate": False
        }
    }
}
