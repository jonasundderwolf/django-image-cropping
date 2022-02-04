import logging
import os
import sys

from easy_thumbnails.conf import settings as thumbnail_settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}

TIME_ZONE = "Europe/Berlin"
# Keep pre Django 4.0 behaviour after upgrading
USE_TZ = False
LANGUAGE_CODE = "en-us"

SITE_ID = 1

USE_I18N = True
USE_L10N = True
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = "/media/"
STATIC_URL = "/static/"
SECRET_KEY = '0pfuvtvasdlkjasd76723"b)lna4*f_-xxkszs4##!+wpo'

ROOT_URLCONF = "example.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)


INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "easy_thumbnails",
    "image_cropping",
    "example",
]


THUMBNAIL_PROCESSORS = (
    "image_cropping.thumbnail_processors.crop_corners",
) + thumbnail_settings.THUMBNAIL_PROCESSORS

try:
    import django_extensions
except ImportError:
    pass
else:
    INSTALLED_APPS += ["django_extensions"]

# disable logging while testing
if len(sys.argv) > 1 and sys.argv[1] == "test":
    logging.disable(logging.CRITICAL)
    # use an in-memory db while testing
    DATABASES["default"]["NAME"] = ":memory:"

IMAGE_CROPPING_THUMB_SIZE = (300, 300)
IMAGE_CROPPING_JQUERY_URL = "js/jquery.min.js"
THUMBNAIL_DEBUG = True
HEADLESS = True
